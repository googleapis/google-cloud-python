# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google.auth
import google.auth.transport.requests as tr_requests
from google.cloud import storage
import pytest
from six.moves import http_client

import gooresmed.download as download_mod


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CURR_DIR, '..', 'data')
IMG_FILES = (
    os.path.realpath(os.path.join(DATA_DIR, 'image1.jpg')),
    os.path.realpath(os.path.join(DATA_DIR, 'image2.jpg')),
)
MIME_TYPE = 'image/jpeg'
BUCKET_NAME = os.environ['GOORESMED_BUCKET']
MEDIA_URL_TEMPLATE = (
    'https://www.googleapis.com/download/storage/v1/b/' +
    BUCKET_NAME +
    '/o/{blob_name}?alt=media')
GCS_SCOPE = ('https://www.googleapis.com/auth/devstorage.read_only',)


@pytest.fixture(scope='module')
def bucket():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    bucket.reload()

    blobs = []
    for img_file in IMG_FILES:
        blob_name = os.path.basename(img_file)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(img_file, content_type=MIME_TYPE)
        blobs.append(blob)

    yield bucket

    # Clean-up the blobs we created.
    for blob in blobs:
        blob.delete()


@pytest.fixture(scope='module')
def authorized_transport():
    credentials, _ = google.auth.default(scopes=GCS_SCOPE)
    yield tr_requests.AuthorizedSession(credentials)


def test_download_full(bucket, authorized_transport):
    for img_file in IMG_FILES:
        with open(img_file, 'rb') as file_obj:
            actual_contents = file_obj.read()

        blob_name = os.path.basename(img_file)

        # Create the actual download object.
        media_url = MEDIA_URL_TEMPLATE.format(blob_name=blob_name)
        download = download_mod.Download(media_url)
        # Consume the resource.
        response = download.consume(authorized_transport)
        assert response.status_code == http_client.OK
        assert response.content == actual_contents
        # Make sure the download is tombstoned.
        with pytest.raises(ValueError):
            download.consume(authorized_transport)


def test_download_partial(bucket, authorized_transport):
    slices = (
        slice(1024, 16386, None),  # obj[1024:16386]
        slice(None, 8192, None),  # obj[:8192]
        slice(-256, None, None),  # obj[-256:]
        slice(262144, None, None),  # obj[262144:]
    )
    for img_file in IMG_FILES:
        with open(img_file, 'rb') as file_obj:
            actual_contents = file_obj.read()

        blob_name = os.path.basename(img_file)

        # Create the multiple download "slices".
        media_url = MEDIA_URL_TEMPLATE.format(blob_name=blob_name)
        downloads = (
            download_mod.Download(media_url, start=1024, end=16385),
            download_mod.Download(media_url, end=8191),
            download_mod.Download(media_url, start=-256),
            download_mod.Download(media_url, start=262144),
        )
        for download, slice_ in zip(downloads, slices):
            response = download.consume(authorized_transport)
            assert response.status_code == http_client.PARTIAL_CONTENT
            assert response.content == actual_contents[slice_]
            with pytest.raises(ValueError):
                download.consume(authorized_transport)


def get_chunk_size(min_chunks, total_bytes):
    # Make sure the number of chunks **DOES NOT** evenly divide.
    num_chunks = min_chunks
    while total_bytes % num_chunks == 0:
        num_chunks += 1

    chunk_size = total_bytes // num_chunks
    # Since we know an integer division has remainder, increment by 1.
    chunk_size += 1
    assert total_bytes < num_chunks * chunk_size

    return num_chunks, chunk_size


def consume_chunks(download, authorized_transport,
                   total_bytes, actual_contents):
    start_byte = download.start
    end_byte = download.end
    if end_byte is None:
        end_byte = total_bytes - 1

    num_responses = 0
    all_parts = []
    while not download.finished:
        response = download.consume_next_chunk(authorized_transport)
        all_parts.append(response.content)
        num_responses += 1

        next_byte = min(start_byte + download.chunk_size, end_byte + 1)
        assert download.bytes_downloaded == next_byte - download.start
        assert download.total_bytes == total_bytes
        assert response.status_code == http_client.PARTIAL_CONTENT
        assert response.content == actual_contents[start_byte:next_byte]
        start_byte = next_byte

    all_bytes = b''.join(all_parts)
    return num_responses, response, all_bytes


def test_chunked_download(bucket, authorized_transport):
    for img_file in IMG_FILES:
        blob_name = os.path.basename(img_file)
        with open(img_file, 'rb') as file_obj:
            actual_contents = file_obj.read()

        total_bytes = len(actual_contents)
        num_chunks, chunk_size = get_chunk_size(7, total_bytes)
        # Create the actual download object.
        media_url = MEDIA_URL_TEMPLATE.format(blob_name=blob_name)
        download = download_mod.ChunkedDownload(media_url, chunk_size)
        # Consume the resource in chunks.
        num_responses, last_response, all_bytes = consume_chunks(
            download, authorized_transport,
            total_bytes, actual_contents)
        # Make sure the combined chunks are the whole object.
        assert all_bytes == actual_contents
        # Check that we have the right number of responses.
        assert num_responses == num_chunks
        # Make sure the last chunk isn't the same size.
        assert total_bytes % chunk_size != 0
        assert len(last_response.content) < chunk_size
        # Make sure the download is tombstoned.
        assert download.finished
        with pytest.raises(ValueError):
            download.consume_next_chunk(authorized_transport)


def test_chunked_download_partial(bucket, authorized_transport):
    slices = (
        slice(1024, 16386, None),  # obj[1024:16386]
        slice(0, 8192, None),  # obj[0:8192]
        slice(262144, None, None),  # obj[262144:]
    )
    for img_file in IMG_FILES:
        with open(img_file, 'rb') as file_obj:
            actual_contents = file_obj.read()

        blob_name = os.path.basename(img_file)
        media_url = MEDIA_URL_TEMPLATE.format(blob_name=blob_name)
        for slice_ in slices:
            # First determine how much content is in the slice and
            # use it to determine a chunking strategy.
            total_bytes = len(actual_contents)
            if slice_.stop is None:
                end_byte = total_bytes - 1
                end = None
            else:
                # Python slices DO NOT include the last index, though a byte
                # range **is** inclusive of both endpoints.
                end_byte = slice_.stop - 1
                end = end_byte

            num_chunks, chunk_size = get_chunk_size(
                7, end_byte - slice_.start + 1)
            # Create the actual download object.
            download = download_mod.ChunkedDownload(
                media_url, chunk_size, start=slice_.start, end=end)
            # Consume the resource in chunks.
            num_responses, last_response, all_bytes = consume_chunks(
                download, authorized_transport, total_bytes, actual_contents)

            # Make sure the combined chunks are the whole slice.
            assert all_bytes == actual_contents[slice_]
            # Check that we have the right number of responses.
            assert num_responses == num_chunks
            # Make sure the last chunk isn't the same size.
            assert len(last_response.content) < chunk_size
            # Make sure the download is tombstoned.
            assert download.finished
            with pytest.raises(ValueError):
                download.consume_next_chunk(authorized_transport)
