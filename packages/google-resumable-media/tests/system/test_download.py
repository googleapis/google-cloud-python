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


def test_download_full(bucket):
    credentials, _ = google.auth.default()
    credentials = credentials.with_scopes(GCS_SCOPE)
    transport = tr_requests.AuthorizedSession(credentials)

    img_file = IMG_FILES[0]
    with open(img_file, 'rb') as file_obj:
        actual_contents = file_obj.read()

    blob_name = os.path.basename(img_file)

    # Create the actual download object.
    media_url = MEDIA_URL_TEMPLATE.format(blob_name=blob_name)
    download = download_mod.Download(media_url)
    # Consume the resource.
    response = download.consume(transport)
    assert response.status_code == http_client.OK
    assert response.content == actual_contents
    # Make sure the download is tombstoned.
    with pytest.raises(ValueError):
        download.consume(transport)
