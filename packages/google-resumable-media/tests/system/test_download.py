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

import io
import os

import google.auth
import google.auth.transport.requests as tr_requests
import pytest
from six.moves import http_client

from google import resumable_media
from tests.system import utils


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CURR_DIR, u'..', u'data')
IMG_FILES = (
    os.path.realpath(os.path.join(DATA_DIR, u'image1.jpg')),
    os.path.realpath(os.path.join(DATA_DIR, u'image2.jpg')),
)
PLAIN_TEXT = u'text/plain'
ENCRYPTED_ERR = (
    b'The target object is encrypted by a customer-supplied encryption key.')


@pytest.fixture(scope=u'module')
def authorized_transport():
    credentials, _ = google.auth.default(scopes=(utils.GCS_RW_SCOPE,))
    yield tr_requests.AuthorizedSession(credentials)


def delete_blob(transport, blob_name):
    metadata_url = utils.METADATA_URL_TEMPLATE.format(blob_name=blob_name)
    response = transport.delete(metadata_url)
    assert response.status_code == http_client.NO_CONTENT


@pytest.fixture(scope=u'module')
def add_files(authorized_transport):
    blob_names = []
    for img_file in IMG_FILES:
        with open(img_file, u'rb') as file_obj:
            actual_contents = file_obj.read()

        blob_name = os.path.basename(img_file)
        blob_names.append(blob_name)
        upload_url = utils.SIMPLE_UPLOAD_TEMPLATE.format(blob_name=blob_name)
        upload = resumable_media.SimpleUpload(upload_url)
        response = upload.transmit(
            authorized_transport, actual_contents, u'image/jpeg')
        assert response.status_code == http_client.OK

    yield

    # Clean-up the blobs we created.
    for blob_name in blob_names:
        delete_blob(authorized_transport, blob_name)


def test_download_full(add_files, authorized_transport):
    for img_file in IMG_FILES:
        with open(img_file, u'rb') as file_obj:
            actual_contents = file_obj.read()

        blob_name = os.path.basename(img_file)

        # Create the actual download object.
        media_url = utils.DOWNLOAD_URL_TEMPLATE.format(blob_name=blob_name)
        download = resumable_media.Download(media_url)
        # Consume the resource.
        response = download.consume(authorized_transport)
        assert response.status_code == http_client.OK
        assert response.content == actual_contents
        # Make sure the download is tombstoned.
        with pytest.raises(ValueError):
            download.consume(authorized_transport)


@pytest.fixture
def secret_file(authorized_transport):
    blob_name = u'super-seekrit.txt'
    data = b'Please do not tell anyone my encrypted seekrit.'

    upload_url = utils.SIMPLE_UPLOAD_TEMPLATE.format(blob_name=blob_name)
    headers = utils.get_encryption_headers()
    upload = resumable_media.SimpleUpload(upload_url, headers=headers)
    response = upload.transmit(authorized_transport, data, PLAIN_TEXT)
    assert response.status_code == http_client.OK

    yield blob_name, data, headers

    delete_blob(authorized_transport, blob_name)


def test_extra_headers(authorized_transport, secret_file):
    blob_name, data, headers = secret_file
    # Create the actual download object.
    media_url = utils.DOWNLOAD_URL_TEMPLATE.format(blob_name=blob_name)
    download = resumable_media.Download(media_url, headers=headers)
    # Consume the resource.
    response = download.consume(authorized_transport)
    assert response.status_code == http_client.OK
    assert response.content == data
    # Make sure the download is tombstoned.
    with pytest.raises(ValueError):
        download.consume(authorized_transport)
    # Attempt to consume the resource **without** the headers.
    download_wo = resumable_media.Download(media_url)
    with pytest.raises(resumable_media.InvalidResponse) as exc_info:
        download_wo.consume(authorized_transport)

    error = exc_info.value
    response = error.response
    assert response.status_code == http_client.BAD_REQUEST
    assert response.content == ENCRYPTED_ERR
    assert len(error.args) == 5
    assert error.args[1] == http_client.BAD_REQUEST
    assert error.args[3] == http_client.OK
    assert error.args[4] == http_client.PARTIAL_CONTENT


def test_non_existent_file(authorized_transport):
    blob_name = u'does-not-exist.txt'
    media_url = utils.DOWNLOAD_URL_TEMPLATE.format(blob_name=blob_name)
    download = resumable_media.Download(media_url)

    # Try to consume the resource and fail.
    with pytest.raises(resumable_media.InvalidResponse) as exc_info:
        download.consume(authorized_transport)

    error = exc_info.value
    response = error.response
    assert response.status_code == http_client.NOT_FOUND
    assert response.content == b'Not Found'
    assert len(error.args) == 5
    assert error.args[1] == http_client.NOT_FOUND
    assert error.args[3] == http_client.OK
    assert error.args[4] == http_client.PARTIAL_CONTENT
    # Make sure the download is tombstoned (even though it failed).
    with pytest.raises(ValueError):
        download.consume(authorized_transport)


@pytest.fixture(scope=u'module')
def simple_file(authorized_transport):
    blob_name = u'basic-file.txt'
    upload_url = utils.SIMPLE_UPLOAD_TEMPLATE.format(blob_name=blob_name)
    upload = resumable_media.SimpleUpload(upload_url)
    data = b'Simple contents'
    response = upload.transmit(authorized_transport, data, PLAIN_TEXT)
    assert response.status_code == http_client.OK

    yield blob_name, data

    delete_blob(authorized_transport, blob_name)


def test_bad_range(simple_file, authorized_transport):
    blob_name, data = simple_file
    # Make sure we have an invalid range.
    start = 32
    end = 63
    assert len(data) < start < end
    # Create the actual download object.
    media_url = utils.DOWNLOAD_URL_TEMPLATE.format(blob_name=blob_name)
    download = resumable_media.Download(media_url, start=start, end=end)

    # Try to consume the resource and fail.
    with pytest.raises(resumable_media.InvalidResponse) as exc_info:
        download.consume(authorized_transport)

    error = exc_info.value
    response = error.response
    assert response.status_code == http_client.REQUESTED_RANGE_NOT_SATISFIABLE
    assert response.content == b'Request range not satisfiable'
    assert len(error.args) == 5
    assert error.args[1] == http_client.REQUESTED_RANGE_NOT_SATISFIABLE
    assert error.args[3] == http_client.OK
    assert error.args[4] == http_client.PARTIAL_CONTENT
    # Make sure the download is tombstoned (even though it failed).
    with pytest.raises(ValueError):
        download.consume(authorized_transport)


def test_download_partial(add_files, authorized_transport):
    slices = (
        slice(1024, 16386, None),  # obj[1024:16386]
        slice(None, 8192, None),  # obj[:8192]
        slice(-256, None, None),  # obj[-256:]
        slice(262144, None, None),  # obj[262144:]
    )
    for img_file in IMG_FILES:
        with open(img_file, u'rb') as file_obj:
            actual_contents = file_obj.read()

        blob_name = os.path.basename(img_file)

        # Create the multiple download "slices".
        media_url = utils.DOWNLOAD_URL_TEMPLATE.format(blob_name=blob_name)
        downloads = (
            resumable_media.Download(media_url, start=1024, end=16385),
            resumable_media.Download(media_url, end=8191),
            resumable_media.Download(media_url, start=-256),
            resumable_media.Download(media_url, start=262144),
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
    while not download.finished:
        response = download.consume_next_chunk(authorized_transport)
        num_responses += 1

        next_byte = min(start_byte + download.chunk_size, end_byte + 1)
        assert download.bytes_downloaded == next_byte - download.start
        assert download.total_bytes == total_bytes
        assert response.status_code == http_client.PARTIAL_CONTENT
        assert response.content == actual_contents[start_byte:next_byte]
        start_byte = next_byte

    return num_responses, response


def test_chunked_download(add_files, authorized_transport):
    for img_file in IMG_FILES:
        blob_name = os.path.basename(img_file)
        with open(img_file, u'rb') as file_obj:
            actual_contents = file_obj.read()

        total_bytes = len(actual_contents)
        num_chunks, chunk_size = get_chunk_size(7, total_bytes)
        # Create the actual download object.
        media_url = utils.DOWNLOAD_URL_TEMPLATE.format(blob_name=blob_name)
        stream = io.BytesIO()
        download = resumable_media.ChunkedDownload(
            media_url, chunk_size, stream)
        # Consume the resource in chunks.
        num_responses, last_response = consume_chunks(
            download, authorized_transport,
            total_bytes, actual_contents)
        # Make sure the combined chunks are the whole object.
        assert stream.getvalue() == actual_contents
        # Check that we have the right number of responses.
        assert num_responses == num_chunks
        # Make sure the last chunk isn't the same size.
        assert total_bytes % chunk_size != 0
        assert len(last_response.content) < chunk_size
        # Make sure the download is tombstoned.
        assert download.finished
        with pytest.raises(ValueError):
            download.consume_next_chunk(authorized_transport)


def test_chunked_download_partial(add_files, authorized_transport):
    slices = (
        slice(1024, 16386, None),  # obj[1024:16386]
        slice(0, 8192, None),  # obj[0:8192]
        slice(262144, None, None),  # obj[262144:]
    )
    for img_file in IMG_FILES:
        with open(img_file, u'rb') as file_obj:
            actual_contents = file_obj.read()

        blob_name = os.path.basename(img_file)
        media_url = utils.DOWNLOAD_URL_TEMPLATE.format(blob_name=blob_name)
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
            stream = io.BytesIO()
            download = resumable_media.ChunkedDownload(
                media_url, chunk_size, stream, start=slice_.start, end=end)
            # Consume the resource in chunks.
            num_responses, last_response = consume_chunks(
                download, authorized_transport, total_bytes, actual_contents)

            # Make sure the combined chunks are the whole slice.
            assert stream.getvalue() == actual_contents[slice_]
            # Check that we have the right number of responses.
            assert num_responses == num_chunks
            # Make sure the last chunk isn't the same size.
            assert len(last_response.content) < chunk_size
            # Make sure the download is tombstoned.
            assert download.finished
            with pytest.raises(ValueError):
                download.consume_next_chunk(authorized_transport)
