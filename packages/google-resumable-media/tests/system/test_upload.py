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
from tests.system import utils


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CURR_DIR, u'..', u'data')
ICO_FILE = os.path.realpath(os.path.join(DATA_DIR, u'favicon.ico'))
ICO_CONTENT_TYPE = u'image/x-icon'


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


def check_response(response, blob_name, actual_contents, metadata=None):
    assert response.status_code == http_client.OK
    json_response = response.json()
    assert json_response[u'bucket'] == utils.BUCKET_NAME
    assert json_response[u'contentType'] == ICO_CONTENT_TYPE
    md5_hash = json_response[u'md5Hash'].encode(u'ascii')
    assert md5_hash == get_md5(actual_contents)
    assert json_response[u'metageneration'] == u'1'
    assert json_response[u'name'] == blob_name
    assert json_response[u'size'] == u'{:d}'.format(len(actual_contents))
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
    check_response(response, blob_name, actual_contents)
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
    check_response(response, blob_name, actual_contents,
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
    with open(ICO_FILE, u'rb') as file_obj:
        yield file_obj


def get_upload_id(upload_url):
    parse_result = urllib_parse.urlparse(upload_url)
    parsed_query = urllib_parse.parse_qs(parse_result.query)
    # NOTE: We are unpacking here, so asserting exactly one match.
    upload_id, = parsed_query[u'upload_id']
    return upload_id


def test_resumable_upload(authorized_transport, stream):
    blob_name = os.path.basename(stream.name)
    metadata = {
        u'name': blob_name,
        u'metadata': {u'direction': u'north'},
    }
    chunk_size = 1024 * 1024  # 1 MB
    # Create the actual upload object.
    upload = gooresmed.ResumableUpload(utils.RESUMABLE_UPLOAD, chunk_size)
    # Initiate the upload.
    response = upload.initiate(
        authorized_transport, stream, metadata, ICO_CONTENT_TYPE)
    # Make sure ``initiate`` succeeded and did not mangle the stream.
    assert response.status_code == http_client.OK
    assert response.content == b''
    upload_id = get_upload_id(upload.upload_url_with_id)
    assert response.headers[u'x-guploader-uploadid'] == upload_id
    assert stream.tell() == 0
    # Make sure the upload cannot be re-initiated.
    with pytest.raises(ValueError):
        upload.initiate(
            authorized_transport, stream, metadata, ICO_CONTENT_TYPE)
