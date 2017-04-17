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

import gooresmed


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CURR_DIR, u'..', u'data')
ICO_FILE = os.path.realpath(os.path.join(DATA_DIR, u'favicon.ico'))
ICO_CONTENT_TYPE = u'image/x-icon'
BUCKET_NAME = os.environ[u'GOORESMED_BUCKET']
SIMPLE_UPLOAD_TEMPLATE = (
    u'https://www.googleapis.com/upload/storage/v1/b/' +
    BUCKET_NAME +
    u'/o?uploadType=media&name={blob_name}')
MULTIPART_UPLOAD = (
    u'https://www.googleapis.com/upload/storage/v1/b/' +
    BUCKET_NAME +
    u'/o?uploadType=multipart')
METADATA_URL_TEMPLATE = (
    u'https://www.googleapis.com/storage/v1/b/' +
    BUCKET_NAME +
    u'/o/{blob_name}')
GCS_SCOPE = (u'https://www.googleapis.com/auth/devstorage.read_write',)


@pytest.fixture(scope=u'module')
def authorized_transport():
    credentials, _ = google.auth.default(scopes=GCS_SCOPE)
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


def test_simple_upload(authorized_transport, cleanup):
    with open(ICO_FILE, u'rb') as file_obj:
        actual_contents = file_obj.read()

    blob_name = os.path.basename(ICO_FILE)
    upload_url = SIMPLE_UPLOAD_TEMPLATE.format(blob_name=blob_name)
    metadata_url = METADATA_URL_TEMPLATE.format(blob_name=blob_name)
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
    assert response.status_code == http_client.OK
    json_response = response.json()
    assert json_response[u'bucket'] == BUCKET_NAME
    assert json_response[u'contentType'] == ICO_CONTENT_TYPE
    md5_hash = json_response[u'md5Hash'].encode(u'ascii')
    assert md5_hash == get_md5(actual_contents)
    assert json_response[u'metageneration'] == u'1'
    assert json_response[u'name'] == blob_name
    assert json_response[u'size'] == u'{:d}'.format(len(actual_contents))
    assert json_response[u'storageClass'] == u'STANDARD'

    # Make sure the upload is tombstoned.
    with pytest.raises(ValueError):
        upload.transmit(
            authorized_transport, actual_contents, ICO_CONTENT_TYPE)


def test_multipart_upload(authorized_transport, cleanup):
    with open(ICO_FILE, u'rb') as file_obj:
        actual_contents = file_obj.read()

    blob_name = os.path.basename(ICO_FILE)
    upload_url = MULTIPART_UPLOAD
    metadata_url = METADATA_URL_TEMPLATE.format(blob_name=blob_name)
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
    assert response.status_code == http_client.OK
    json_response = response.json()
    assert json_response[u'bucket'] == BUCKET_NAME
    assert json_response[u'contentType'] == ICO_CONTENT_TYPE
    md5_hash = json_response[u'md5Hash'].encode(u'ascii')
    assert md5_hash == get_md5(actual_contents)
    assert json_response[u'metadata'] == metadata[u'metadata']
    assert json_response[u'metageneration'] == u'1'
    assert json_response[u'name'] == blob_name
    assert json_response[u'size'] == u'{:d}'.format(len(actual_contents))
    assert json_response[u'storageClass'] == u'STANDARD'
    # Download the content to make sure it's "working as expected".

    # Make sure the upload is tombstoned.
    with pytest.raises(ValueError):
        upload.transmit(
            authorized_transport, actual_contents, metadata, ICO_CONTENT_TYPE)
