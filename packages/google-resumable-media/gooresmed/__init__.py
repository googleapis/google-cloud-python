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

====================
Authorized Transport
====================

In order to download or upload a resource, an authorized transport
is required. For download requests, this must be an object that
supports ``GET`` requests via ``transport.get(url, headers=headers)``.

For example, ``google-auth`` and ``requests`` can be used to
create an authorized transport that has read-only access to
Google Cloud Storage (GCS):

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
   >>>
   >>> ro_scope = 'https://www.googleapis.com/auth/devstorage.read_only'
   >>> credentials, _ = google.auth.default(scopes=(ro_scope,))
   >>> transport = tr_requests.AuthorizedSession(credentials)
   >>> transport
   <google.auth.transport.requests.AuthorizedSession object at 0x...>

.. testcleanup:: get-credentials

   # Put back the correct ``default`` function on the module.
   google.auth.default = original_default

================
Simple Downloads
================

To download an object from Google Cloud Storage, construct the media URL
for the GCS object and download it with an authorized transport that has
access to the resource:

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

To download only a portion of the bytes in the object,
specify ``start`` and ``end`` byte positions (both optional):

.. testsetup:: basic-download-with-slice

   import mock
   import requests
   from six.moves import http_client

   import gooresmed

   media_url = 'test.invalid'
   start = 4096
   end = 8191
   slice_size = end - start + 1

   fake_response = requests.Response()
   fake_response.status_code = int(http_client.PARTIAL_CONTENT)
   fake_response.headers['Content-Length'] = u'{:d}'.format(slice_size)
   content_range = 'bytes {:d}-{:d}/1364156'.format(start, end)
   fake_response.headers['Content-Range'] = content_range
   fake_content = mock.MagicMock(spec=['__len__'])
   fake_content.__len__.return_value = slice_size
   fake_response._content = fake_content

   get_method = mock.Mock(return_value=fake_response, spec=[])
   transport = mock.Mock(get=get_method, spec=['get'])

.. doctest:: basic-download-with-slice

   >>> download = gooresmed.Download(media_url, start=4096, end=8191)
   >>> response = download.consume(transport)
   >>> download.finished
   True
   >>> response
   <Response [206]>
   >>> response.headers['Content-Length']
   '4096'
   >>> response.headers['Content-Range']
   'bytes 4096-8191/1364156'
   >>> len(response.content)
   4096

=================
Chunked Downloads
=================

For very large objects or objects of unknown size, it may make more sense
to download the object in chunks rather than all at once. This can be done
to avoid dropped connections with a poor internet connection or can allow
multiple chunks to be downloaded in parallel to speed up the total
download.

Using the same media URL and authorized transport for a basic
:class:`.Download`, a :class:`.ChunkedDownload` also requires a chunk size:

.. testsetup:: chunked-download

   import mock
   import requests
   from six.moves import http_client

   import gooresmed

   media_url = 'test.invalid'

   fifty_mb = 50 * 1024 * 1024
   one_gb = 1024 * 1024 * 1024
   fake_response = requests.Response()
   fake_response.status_code = int(http_client.PARTIAL_CONTENT)
   fake_response.headers['Content-Length'] = u'{:d}'.format(fifty_mb)
   content_range = 'bytes 0-{:d}/{:d}'.format(fifty_mb - 1, one_gb)
   fake_response.headers['Content-Range'] = content_range
   fake_content = mock.MagicMock(spec=['__len__'])
   fake_content.__len__.return_value = fifty_mb
   fake_response._content = fake_content

   get_method = mock.Mock(return_value=fake_response, spec=[])
   transport = mock.Mock(get=get_method, spec=['get'])

.. doctest:: chunked-download

   >>> chunk_size = 50 * 1024 * 1024  # 50MB
   >>> download = gooresmed.ChunkedDownload(media_url, chunk_size)
   >>> # Check the state of the download before starting.
   >>> download.bytes_downloaded
   0
   >>> download.total_bytes is None
   True
   >>> response = download.consume_next_chunk(transport)
   >>> # Check the state of the download after consuming one chunk.
   >>> download.finished
   False
   >>> download.bytes_downloaded  # chunk_size
   52428800
   >>> download.total_bytes  # 1GB
   1073741824
   >>> response
   <Response [206]>
   >>> response.headers['Content-Length']
   '52428800'
   >>> response.headers['Content-Range']
   'bytes 0-52428799/1073741824'
   >>> len(response.content) == chunk_size
   True

The download will change it's ``finished`` status to :data:`True`
once the final chunk is consumed. In some cases, the final chunk may
not be the same size as the other chunks:

.. testsetup:: chunked-download-end

   import mock
   import requests
   from six.moves import http_client

   import gooresmed

   media_url = 'test.invalid'

   fifty_mb = 50 * 1024 * 1024
   one_gb = 1024 * 1024 * 1024
   download = gooresmed.ChunkedDownload(media_url, fifty_mb)
   download._bytes_downloaded = 20 * fifty_mb
   download._total_bytes = one_gb

   fake_response = requests.Response()
   fake_response.status_code = int(http_client.PARTIAL_CONTENT)
   slice_size = one_gb - 20 * fifty_mb
   fake_response.headers['Content-Length'] = u'{:d}'.format(slice_size)
   content_range = 'bytes {:d}-{:d}/{:d}'.format(
       20 * fifty_mb, one_gb - 1, one_gb)
   fake_response.headers['Content-Range'] = content_range
   fake_content = mock.MagicMock(spec=['__len__'])
   fake_content.__len__.return_value = slice_size
   fake_response._content = fake_content

   get_method = mock.Mock(return_value=fake_response, spec=[])
   transport = mock.Mock(get=get_method, spec=['get'])

.. doctest:: chunked-download-end

   >>> # The state of the download in progress.
   >>> download.finished
   False
   >>> download.bytes_downloaded  # 20 chunks at 50MB
   1048576000
   >>> download.total_bytes  # 1GB
   1073741824
   >>> response = download.consume_next_chunk(transport)
   >>> # The state of the download after consuming the final chunk.
   >>> download.finished
   True
   >>> download.bytes_downloaded == download.total_bytes
   True
   >>> response
   <Response [206]>
   >>> response.headers['Content-Length']
   '25165824'
   >>> response.headers['Content-Range']
   'bytes 1048576000-1073741823/1073741824'
   >>> len(response.content) < download.chunk_size
   True

In addition, a :class:`.ChunkedDownload` can also take optional
``start`` and ``end`` byte positions.
"""


from gooresmed.download import ChunkedDownload
from gooresmed.download import Download
from gooresmed.exceptions import InvalidResponse
from gooresmed.upload import MultipartUpload
from gooresmed.upload import ResumableUpload
from gooresmed.upload import SimpleUpload


__all__ = [
    u'ChunkedDownload',
    u'Download',
    u'InvalidResponse',
    u'MultipartUpload',
    u'ResumableUpload',
    u'SimpleUpload',
]
