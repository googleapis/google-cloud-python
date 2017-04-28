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

"""Virtual bases classes for uploading media via Google APIs.

Supported here are:

* simple (media) uploads
* multipart uploads that contain both metadata and a small file as payload
* resumable uploads (with metadata as well)
"""


from six.moves import http_client

from google.resumable_media import _helpers


class UploadBase(object):
    """Base class for upload helpers.

    Defines core shared behavior across different upload types.

    Args:
        upload_url (str): The URL where the content will be uploaded.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.
    """

    def __init__(self, upload_url, headers=None):
        self.upload_url = upload_url
        """str: The URL where the content will be uploaded."""
        if headers is None:
            headers = {}
        self._headers = headers
        self._finished = False

    @property
    def finished(self):
        """bool: Flag indicating if the upload has completed."""
        return self._finished

    def _process_response(self, response):
        """Process the response from an HTTP request.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Args:
            response (object): The HTTP response object.

        Raises:
            ~google.resumable_media.exceptions.InvalidResponse: If the status
                code is not 200.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        # Tombstone the current upload so it cannot be used again (in either
        # failure or success).
        self._finished = True
        _helpers.require_status_code(
            response, (http_client.OK,), self._get_status_code)

    @staticmethod
    def _get_status_code(response):
        """Access the status code from an HTTP response.

        Args:
            response (object): The HTTP response object.

        Raises:
            NotImplementedError: Always, since virtual.
        """
        raise NotImplementedError(u'This implementation is virtual.')
