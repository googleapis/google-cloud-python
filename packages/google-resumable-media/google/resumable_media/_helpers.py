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

"""Shared utilities used by both downloads and uploads."""


from google.resumable_media import exceptions


RANGE_HEADER = u'range'
CONTENT_RANGE_HEADER = u'content-range'


def do_nothing():
    """Simple default callback."""


def get_headers(response):
    """Access the headers from an HTTP response.

    Args:
        response (object): The HTTP response object.

    Returns:
        Mapping[str, str]: The header mapping (expect keys to either be
        all lowercase, or case-insensitive).
    """
    return response.headers


def header_required(response, name, callback=do_nothing):
    """Checks that a specific header is in a headers dictionary.

    Args:
        response (object): An HTTP response object, expected to have a
            ``headers`` attribute that is a ``Mapping[str, str]``.
        name (str): The name of a required header.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        str: The desired header.

    Raises:
        ~google.resumable_media.exceptions.InvalidResponse: If the header
            is missing.
    """
    headers = get_headers(response)
    if name not in headers:
        callback()
        raise exceptions.InvalidResponse(
            response, u'Response headers must contain header', name)

    return headers[name]


def get_status_code(response):
    """Access the status code from an HTTP response.

    Args:
        response (object): The HTTP response object.

    Returns:
        int: The status code.
    """
    return response.status_code


def get_body(response):
    """Access the response body from an HTTP response.

    Args:
        response (object): The HTTP response object.

    Returns:
        bytes: The body of the ``response``.
    """
    return response.content


def require_status_code(response, status_codes, callback=do_nothing):
    """Require a response has a status code among a list.

    Args:
        response (object): The HTTP response object.
        status_codes (tuple): The acceptable status codes.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        int: The status code.

    Raises:
        ~google.resumable_media.exceptions.InvalidResponse: If the status code
            is not one of the values in ``status_codes``.
    """
    status_code = get_status_code(response)
    if status_code not in status_codes:
        callback()
        raise exceptions.InvalidResponse(
            response, u'Request failed with status code',
            status_code, u'Expected one of', *status_codes)
    return status_code


def http_request(transport, method, url, data=None, headers=None):
    """Make an HTTP request.

    Args:
        transport (object): An object which can make authenticated requests
            via a ``request()`` method. This method mustaccept an HTTP method,
            an upload URL, a ``data`` keyword argument and a
            ``headers`` keyword argument.
        method (str): The HTTP method for the request.
        url (str): The URL for the request.
        data (Optional[bytes]): The body of the request.
        headers (Mapping[str, str]): The headers for the request (``transport``
            may also add additional headers).

    Returns:
        object: The return value of ``transport.request()``.
    """
    return transport.request(method, url, data=data, headers=headers)
