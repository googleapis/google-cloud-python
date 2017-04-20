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


BUCKET_NAME = os.environ[u'GOOGLE_RESUMABLE_MEDIA_BUCKET']
DOWNLOAD_URL_TEMPLATE = (
    u'https://www.googleapis.com/download/storage/v1/b/' +
    BUCKET_NAME +
    u'/o/{blob_name}?alt=media')
_UPLOAD_BASE = (
    u'https://www.googleapis.com/upload/storage/v1/b/' +
    BUCKET_NAME +
    u'/o?uploadType=')
SIMPLE_UPLOAD_TEMPLATE = _UPLOAD_BASE + u'media&name={blob_name}'
MULTIPART_UPLOAD = _UPLOAD_BASE + u'multipart'
RESUMABLE_UPLOAD = _UPLOAD_BASE + u'resumable'
METADATA_URL_TEMPLATE = (
    u'https://www.googleapis.com/storage/v1/b/' +
    BUCKET_NAME +
    u'/o/{blob_name}')

GCS_RW_SCOPE = u'https://www.googleapis.com/auth/devstorage.read_write'
