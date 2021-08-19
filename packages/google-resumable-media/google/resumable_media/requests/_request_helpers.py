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

"""Shared utilities used by both downloads and uploads.

This utilities are explicitly catered to ``requests``-like transports.
"""


from google.resumable_media import common


_DEFAULT_RETRY_STRATEGY = common.RetryStrategy()
_SINGLE_GET_CHUNK_SIZE = 8192
# The number of seconds to wait to establish a connection
# (connect() call on socket). Avoid setting this to a multiple of 3 to not
# Align with TCP Retransmission timing. (typically 2.5-3s)
_DEFAULT_CONNECT_TIMEOUT = 61
# The number of seconds to wait between bytes sent from the server.
_DEFAULT_READ_TIMEOUT = 60


class RequestsMixin(object):
    """Mix-in class implementing ``requests``-specific behavior.

    These are methods that are more general purpose, with implementations
    specific to the types defined in ``requests``.
    """

    @staticmethod
    def _get_status_code(response):
        """Access the status code from an HTTP response.

        Args:
            response (~requests.Response): The HTTP response object.

        Returns:
            int: The status code.
        """
        return response.status_code

    @staticmethod
    def _get_headers(response):
        """Access the headers from an HTTP response.

        Args:
            response (~requests.Response): The HTTP response object.

        Returns:
            ~requests.structures.CaseInsensitiveDict: The header mapping (keys
            are case-insensitive).
        """
        return response.headers

    @staticmethod
    def _get_body(response):
        """Access the response body from an HTTP response.

        Args:
            response (~requests.Response): The HTTP response object.

        Returns:
            bytes: The body of the ``response``.
        """
        return response.content


class RawRequestsMixin(RequestsMixin):
    @staticmethod
    def _get_body(response):
        """Access the response body from an HTTP response.

        Args:
            response (~requests.Response): The HTTP response object.

        Returns:
            bytes: The body of the ``response``.
        """
        if response._content is False:
            response._content = b"".join(
                response.raw.stream(_SINGLE_GET_CHUNK_SIZE, decode_content=False)
            )
            response._content_consumed = True
        return response._content
