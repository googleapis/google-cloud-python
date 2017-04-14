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

"""Utilities for Google Media Downloads and Resumable Uploads.

For example, to download an object from Google Cloud Storage (GCS),
first create an authorized transport that has access to the
resource you'd like to download:

.. testsetup:: get-credentials

   import google.auth
   import google.auth.credentials as creds_mod
   import mock

   def mock_default(scopes=None):
       credentials = mock.Mock(spec=creds_mod.Credentials)
       return credentials, 'mock-project'

   # Patch the ``default`` function on the module.
   original_default = google.auth.default
   google.auth.default = mock_default

.. doctest:: get-credentials

   >>> import google.auth
   >>> import google.auth.transport.requests as tr_requests
   >>> ro_scope = 'https://www.googleapis.com/auth/devstorage.read_only'
   >>> credentials, _ = google.auth.default(scopes=(ro_scope,))
   >>> transport = tr_requests.AuthorizedSession(credentials)
   >>> transport
   <google.auth.transport.requests.AuthorizedSession object at 0x...>

.. testcleanup:: get-credentials

   # Put back the correct ``default`` function on the module.
   google.auth.default = original_default

then construct the media URL for the GCS object and download it:

.. testsetup:: basic-download

   import mock
   import requests
   from six.moves import http_client

   bucket = 'bucket-foo'
   blob_name = 'file.txt'

   fake_response = requests.Response()
   fake_response.status_code = int(http_client.OK)
   fake_response.headers['Content-Length'] = '1364156'
   fake_content = mock.MagicMock(spec=['__len__'])
   fake_content.__len__.return_value = 1364156
   fake_response._content = fake_content

   get_method = mock.Mock(return_value=fake_response, spec=[])
   transport = mock.Mock(get=get_method, spec=['get'])

.. doctest:: basic-download

   >>> import gooresmed
   >>>
   >>> url_template = (
   ...     'https://www.googleapis.com/download/storage/v1/b/'
   ...     '{bucket}/o/{blob_name}?alt=media')
   >>> media_url = url_template.format(
   ...     bucket=bucket, blob_name=blob_name)
   >>>
   >>> download = gooresmed.Download(media_url)
   >>> response = download.consume(transport)
   >>> download.finished
   True
   >>> response
   <Response [200]>
   >>> response.headers['Content-Length']
   '1364156'
   >>> len(response.content)
   1364156
"""

from gooresmed.download import ChunkedDownload
from gooresmed.download import Download
from gooresmed.upload import Upload


__all__ = [
    'ChunkedDownload',
    'Download',
    'Upload',
]
