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

import base64
import hashlib
import os

import google.auth
import google.auth.transport.requests as tr_requests
import pytest
from six.moves import http_client
from six.moves import urllib_parse

import gooresmed
import gooresmed.upload as upload_mod
from tests.system import utils


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CURR_DIR, u'..', u'data')
ICO_FILE = os.path.realpath(os.path.join(DATA_DIR, u'favicon.ico'))
IMAGE_FILE = os.path.realpath(os.path.join(DATA_DIR, u'image1.jpg'))
ICO_CONTENT_TYPE = u'image/x-icon'
JPEG_CONTENT_TYPE = u'image/jpeg'
BAD_CHUNK_SIZE_MSG = (
    b'Invalid request.  The number of bytes uploaded is required to be equal '
    b'or greater than 262144, except for the final request (it\'s recommended '
    b'to be the exact multiple of 262144).  The received request contained '
    b'1024 bytes, which does not meet this requirement.')


@pytest.fixture(scope=u'module')
def authorized_transport():
    credentials, _ = google.auth.default(scopes=(utils.GCS_RW_SCOPE,))
    yield tr_requests.AuthorizedSession(credentials)


@pytest.fixture
def cleanup():
    to_delete = []

    def add_cleanup(item_url, transport):
        to_delete.append((item_url, transport))

    yield add_cleanup

    for item_url, transport in to_delete:
        response = transport.delete(item_url)
        assert response.status_code == http_client.NO_CONTENT


def get_md5(data):
    hash_obj = hashlib.md5(data)
    return base64.b64encode(hash_obj.digest())


def check_response(response, blob_name, actual_contents=None,
                   total_bytes=None, metadata=None,
                   content_type=ICO_CONTENT_TYPE):
    assert response.status_code == http_client.OK
    json_response = response.json()
    assert json_response[u'bucket'] == utils.BUCKET_NAME
    assert json_response[u'contentType'] == content_type
    if actual_contents is not None:
        md5_hash = json_response[u'md5Hash'].encode(u'ascii')
        assert md5_hash == get_md5(actual_contents)
        total_bytes = len(actual_contents)
    assert json_response[u'metageneration'] == u'1'
    assert json_response[u'name'] == blob_name
    assert json_response[u'size'] == u'{:d}'.format(total_bytes)
    assert json_response[u'storageClass'] == u'STANDARD'
    if metadata is None:
        assert u'metadata' not in json_response
    else:
        assert json_response[u'metadata'] == metadata


def check_content(blob_name, expected_content, transport):
    media_url = utils.DOWNLOAD_URL_TEMPLATE.format(blob_name=blob_name)
    download = gooresmed.Download(media_url)
    response = download.consume(transport)
    assert response.status_code == http_client.OK
    assert response.content == expected_content


def test_simple_upload(authorized_transport, cleanup):
    with open(ICO_FILE, u'rb') as file_obj:
        actual_contents = file_obj.read()

    blob_name = os.path.basename(ICO_FILE)
    upload_url = utils.SIMPLE_UPLOAD_TEMPLATE.format(blob_name=blob_name)
    metadata_url = utils.METADATA_URL_TEMPLATE.format(blob_name=blob_name)
    # Make sure to clean up the uploaded blob when we are done.
    cleanup(metadata_url, authorized_transport)
    # Make sure we are creating a **new** object.
    response = authorized_transport.get(metadata_url)
    assert response.status_code == http_client.NOT_FOUND

    # Create the actual upload object.
    upload = gooresmed.SimpleUpload(upload_url)
    # Transmit the resource.
    response = upload.transmit(
        authorized_transport, actual_contents, ICO_CONTENT_TYPE)
    check_response(response, blob_name, actual_contents=actual_contents)
    # Download the content to make sure it's "working as expected".
    check_content(blob_name, actual_contents, authorized_transport)
    # Make sure the upload is tombstoned.
    with pytest.raises(ValueError):
        upload.transmit(
            authorized_transport, actual_contents, ICO_CONTENT_TYPE)


def test_multipart_upload(authorized_transport, cleanup):
    with open(ICO_FILE, u'rb') as file_obj:
        actual_contents = file_obj.read()

    blob_name = os.path.basename(ICO_FILE)
    upload_url = utils.MULTIPART_UPLOAD
    metadata_url = utils.METADATA_URL_TEMPLATE.format(blob_name=blob_name)
    # Make sure to clean up the uploaded blob when we are done.
    cleanup(metadata_url, authorized_transport)
    # Make sure we are creating a **new** object.
    response = authorized_transport.get(metadata_url)
    assert response.status_code == http_client.NOT_FOUND

    # Create the actual upload object.
    upload = gooresmed.MultipartUpload(upload_url)
    # Transmit the resource.
    metadata = {
        u'name': blob_name,
        u'metadata': {u'color': u'yellow'},
    }
    response = upload.transmit(
        authorized_transport, actual_contents, metadata, ICO_CONTENT_TYPE)
    check_response(
        response, blob_name, actual_contents=actual_contents,
        metadata=metadata[u'metadata'])
    # Download the content to make sure it's "working as expected".
    check_content(blob_name, actual_contents, authorized_transport)
    # Make sure the upload is tombstoned.
    with pytest.raises(ValueError):
        upload.transmit(
            authorized_transport, actual_contents, metadata, ICO_CONTENT_TYPE)


@pytest.fixture
def stream():
    """Open-file as a fixture.

    This is so that an entire test can execute in the context of
    the context manager without worrying about closing the file.
    """
    with open(IMAGE_FILE, u'rb') as file_obj:
        yield file_obj


def get_upload_id(upload_url):
    parse_result = urllib_parse.urlparse(upload_url)
    parsed_query = urllib_parse.parse_qs(parse_result.query)
    # NOTE: We are unpacking here, so asserting exactly one match.
    upload_id, = parsed_query[u'upload_id']
    return upload_id


def get_num_chunks(total_bytes, chunk_size):
    expected_chunks, remainder = divmod(total_bytes, chunk_size)
    if remainder > 0:
        expected_chunks += 1
    return expected_chunks


def transmit_chunks(upload, transport, blob_name, metadata):
    num_chunks = 0
    while not upload.finished:
        num_chunks += 1
        response = upload.transmit_next_chunk(transport)
        if upload.finished:
            assert upload.bytes_uploaded == upload.total_bytes
            check_response(
                response, blob_name, total_bytes=upload.total_bytes,
                metadata=metadata, content_type=JPEG_CONTENT_TYPE)
        else:
            assert upload.bytes_uploaded == num_chunks * upload.chunk_size
            assert response.status_code == upload_mod.PERMANENT_REDIRECT

    return num_chunks


def check_initiate(response, upload, stream, transport, metadata):
    assert response.status_code == http_client.OK
    assert response.content == b''
    upload_id = get_upload_id(upload.upload_url_with_id)
    assert response.headers[u'x-guploader-uploadid'] == upload_id
    assert stream.tell() == 0
    # Make sure the upload cannot be re-initiated.
    with pytest.raises(ValueError):
        upload.initiate(
            transport, stream, metadata, JPEG_CONTENT_TYPE)


def test_resumable_upload(authorized_transport, stream, cleanup):
    blob_name = os.path.basename(stream.name)
    # Make sure to clean up the uploaded blob when we are done.
    metadata_url = utils.METADATA_URL_TEMPLATE.format(blob_name=blob_name)
    cleanup(metadata_url, authorized_transport)
    # Create the actual upload object.
    chunk_size = upload_mod.UPLOAD_CHUNK_SIZE
    upload = gooresmed.ResumableUpload(utils.RESUMABLE_UPLOAD, chunk_size)
    # Initiate the upload.
    metadata = {
        u'name': blob_name,
        u'metadata': {u'direction': u'north'},
    }
    response = upload.initiate(
        authorized_transport, stream, metadata, JPEG_CONTENT_TYPE)
    # Make sure ``initiate`` succeeded and did not mangle the stream.
    check_initiate(response, upload, stream, authorized_transport, metadata)
    # Actually upload the file in chunks.
    num_chunks = transmit_chunks(
        upload, authorized_transport, blob_name, metadata[u'metadata'])
    assert num_chunks == get_num_chunks(upload.total_bytes, chunk_size)
    # Download the content to make sure it's "working as expected".
    stream.seek(0)
    actual_contents = stream.read()
    check_content(blob_name, actual_contents, authorized_transport)
    # Make sure the upload is tombstoned.
    with pytest.raises(ValueError):
        upload.transmit_next_chunk(authorized_transport)


def check_bad_chunk(upload, transport):
    with pytest.raises(gooresmed.InvalidResponse) as exc_info:
        upload.transmit_next_chunk(transport)
    error = exc_info.value
    response = error.response
    assert response.status_code == http_client.BAD_REQUEST
    assert response.content == BAD_CHUNK_SIZE_MSG


def test_resumable_upload_bad_chunk_size(authorized_transport, stream):
    blob_name = os.path.basename(stream.name)
    # Create the actual upload object.
    upload = gooresmed.ResumableUpload(
        utils.RESUMABLE_UPLOAD, upload_mod.UPLOAD_CHUNK_SIZE)
    # Modify the ``upload`` **after** construction so we can
    # use a bad chunk size.
    upload._chunk_size = 1024
    assert upload._chunk_size < upload_mod.UPLOAD_CHUNK_SIZE
    # Initiate the upload.
    metadata = {u'name': blob_name}
    response = upload.initiate(
        authorized_transport, stream, metadata, JPEG_CONTENT_TYPE)
    # Make sure ``initiate`` succeeded and did not mangle the stream.
    check_initiate(response, upload, stream, authorized_transport, metadata)
    # Make the first request and verify that it fails.
    check_bad_chunk(upload, authorized_transport)
    # Reset the chunk size (and the stream) and verify the "resumable"
    # URL is unusable.
    upload._chunk_size = upload_mod.UPLOAD_CHUNK_SIZE
    stream.seek(0)
    upload._invalid = False
    check_bad_chunk(upload, authorized_transport)
