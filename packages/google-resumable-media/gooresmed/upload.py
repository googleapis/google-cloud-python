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

"""Support for resumable uploads.

Also supported here are simple (media) uploads and multipart
uploads that contain both metadata and a small file as payload.
"""


class SimpleUpload(object):
    """Upload a resource to a Google API.

    A **simple** media upload sends no metadata and completes the upload
    in a single request.

    Args:
       upload_url (str): The URL where the content will be uploaded.
    """

    def __init__(self, upload_url):
        self.upload_url = upload_url
        """str: The URL where the content will be uploaded."""
        self._finished = False

    @property
    def finished(self):
        """bool: Flag indicating if the upload has completed."""
        return self._finished

    def _prepare_request(self, content_type):
        """Prepare the contents of an HTTP request.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Args:
            content_type (str): The content type for the request.

        Returns:
            dict: The headers for the request.

        Raises:
            ValueError: If the current :class:`Upload` has already finished.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.finished:
            raise ValueError('An upload can only be used once.')

        headers = {'content-type': content_type}
        return headers

    def _process_response(self):
        """Process the response from an HTTP request.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        # Tombstone the current Upload so it cannot be used again.
        self._finished = True

    def transmit(self, transport, data, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (object): An object which can make authenticated
                requests via a ``post()`` method which accepts an
                upload URL, a ``data`` keyword argument and a
                ``headers`` keyword argument.

        Returns:
            object: The return value of ``transport.post()``.
        """
        headers = self._prepare_request(content_type)
        result = transport.post(self.upload_url, data=data, headers=headers)
        self._process_response()
        return result
