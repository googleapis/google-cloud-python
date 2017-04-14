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
from google.cloud import storage
import pytest
from six.moves import http_client

import gooresmed


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CURR_DIR, '..', 'data')
ICO_FILE = os.path.realpath(os.path.join(DATA_DIR, 'favicon.ico'))
ICO_CONTENT_TYPE = 'image/x-icon'
BUCKET_NAME = os.environ['GOORESMED_BUCKET']
UPLOAD_URL_TEMPLATE = (
    'https://www.googleapis.com/upload/storage/v1/b/' +
    BUCKET_NAME +
    '/o?uploadType=media&name={blob_name}')
GCS_SCOPE = ('https://www.googleapis.com/auth/devstorage.read_write',)


@pytest.fixture(scope='module')
def bucket():
    client = storage.Client()
    loc_bucket = client.bucket(BUCKET_NAME)
    loc_bucket.reload()
    yield loc_bucket


@pytest.fixture(scope='module')
def authorized_transport():
    credentials, _ = google.auth.default(scopes=GCS_SCOPE)
    yield tr_requests.AuthorizedSession(credentials)


def get_md5(data):
    hash_obj = hashlib.md5(data)
    return base64.b64encode(hash_obj.digest())


def test_simple_upload(bucket, authorized_transport):
    with open(ICO_FILE, 'rb') as file_obj:
        actual_contents = file_obj.read()

    blob_name = os.path.basename(ICO_FILE)

    # Create the actual upload object.
    upload_url = UPLOAD_URL_TEMPLATE.format(blob_name=blob_name)
    upload = gooresmed.SimpleUpload(upload_url)
    # Transmit the resource.
    response = upload.transmit(
        authorized_transport, actual_contents, ICO_CONTENT_TYPE)
    assert response.status_code == http_client.OK
    json_response = response.json()
    assert json_response['bucket'] == BUCKET_NAME
    assert json_response['contentType'] == ICO_CONTENT_TYPE
    assert json_response['md5Hash'].encode('ascii') == get_md5(actual_contents)
    assert json_response['metageneration'] == '1'
    assert json_response['name'] == blob_name
    assert json_response['size'] == str(len(actual_contents))
    assert json_response['storageClass'] == 'STANDARD'

    # Make sure the upload is tombstoned.
    with pytest.raises(ValueError):
        upload.transmit(
            authorized_transport, actual_contents, ICO_CONTENT_TYPE)

    # Make sure to clean up the uploaded blob.
    blob = bucket.blob(blob_name)
    blob.delete()
