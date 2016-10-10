# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Transport adapter for urllib3."""

from __future__ import absolute_import

import logging

import urllib3
import urllib3.exceptions

from google.auth import exceptions
from google.auth import transport

_LOGGER = logging.getLogger(__name__)


class Response(transport.Response):
    """urllib3 transport response adapter.

    Args:
        response (urllib3.response.HTTPResponse): The raw urllib3 response.
    """
    def __init__(self, response):
        self._response = response

    @property
    def status(self):
        return self._response.status

    @property
    def headers(self):
        return self._response.headers

    @property
    def data(self):
        return self._response.data


class Request(transport.Request):
    """urllib3 request adapter

    Args:
        http (urllib3.requests.RequestMethods): An instance of any urllib3
            class that implements :class:`~urllib3.requests.RequestMethods`,
            usually :class:`urllib3.PoolManager`.
    """
    def __init__(self, http):
        self.http = http

    def __call__(self, url, method='GET', body=None, headers=None,
                 timeout=None, **kwargs):
        """Make an HTTP request using urllib3.

        Args:
            url (str): The URI to be requested.
            method (str): The HTTP method to use for the request. Defaults
                to 'GET'.
            body (bytes): The payload / body in HTTP request.
            headers (Mapping): Request headers.
            timeout (Optional(int)): The number of seconds to wait for a
                response from the server. If not specified or if None, the
                urllib3 default timeout will be used.
            kwargs: Additional arguments passed throught to the underlying
                urllib3 :meth:`urlopen` method.

        Returns:
            Response: The HTTP response.

        Raises:
            google.auth.exceptions.TransportError: If any exception occurred.
        """
        # urllib3 uses a sentinel default value for timeout, so only set it if
        # specified.
        if timeout is not None:
            kwargs['timeout'] = timeout

        try:
            _LOGGER.debug('Making request: %s %s', method, url)
            response = self.http.request(
                method, url, body=body, headers=headers, **kwargs)
            return Response(response)
        except urllib3.exceptions.HTTPError as exc:
            raise exceptions.TransportError(exc)
