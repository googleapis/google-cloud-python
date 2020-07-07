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


import functools
import warnings

from google.resumable_media import _helpers
from google.resumable_media import common


_DEFAULT_RETRY_STRATEGY = common.RetryStrategy()
_SINGLE_GET_CHUNK_SIZE = 8192
# The number of seconds to wait to establish a connection
# (connect() call on socket). Avoid setting this to a multiple of 3 to not
# Align with TCP Retransmission timing. (typically 2.5-3s)
_DEFAULT_CONNECT_TIMEOUT = 61
# The number of seconds to wait between bytes sent from the server.
_DEFAULT_READ_TIMEOUT = 60

_SLOW_CRC32C_WARNING = (
    "Currently using crcmod in pure python form. This is a slow "
    "implementation. Python 3 has a faster implementation, `google-crc32c`, "
    "which will be used if it is installed."
)


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


def http_request(
    transport,
    method,
    url,
    data=None,
    headers=None,
    retry_strategy=_DEFAULT_RETRY_STRATEGY,
    **transport_kwargs
):
    """Make an HTTP request.

    Args:
        transport (~requests.Session): A ``requests`` object which can make
            authenticated requests via a ``request()`` method. This method
            must accept an HTTP method, an upload URL, a ``data`` keyword
            argument and a ``headers`` keyword argument.
        method (str): The HTTP method for the request.
        url (str): The URL for the request.
        data (Optional[bytes]): The body of the request.
        headers (Mapping[str, str]): The headers for the request (``transport``
            may also add additional headers).
        retry_strategy (~google.resumable_media.common.RetryStrategy): The
            strategy to use if the request fails and must be retried.
        transport_kwargs (Dict[str, str]): Extra keyword arguments to be
            passed along to ``transport.request``.

    Returns:
        ~requests.Response: The return value of ``transport.request()``.
    """
    if "timeout" not in transport_kwargs:
        transport_kwargs["timeout"] = (_DEFAULT_CONNECT_TIMEOUT, _DEFAULT_READ_TIMEOUT)

    func = functools.partial(
        transport.request, method, url, data=data, headers=headers, **transport_kwargs
    )
    return _helpers.wait_and_retry(func, RequestsMixin._get_status_code, retry_strategy)


def _get_crc32c_object():
    """ Get crc32c object
    Attempt to use the Google-CRC32c package. If it isn't available, try
    to use CRCMod. CRCMod might be using a 'slow' varietal. If so, warn...
    """
    try:
        import crc32c

        crc_obj = crc32c.Checksum()
    except ImportError:
        try:
            import crcmod

            crc_obj = crcmod.predefined.Crc("crc-32c")
            _is_fast_crcmod()

        except ImportError:
            raise ImportError("Failed to import either `google-crc32c` or `crcmod`")

    return crc_obj


def _is_fast_crcmod():
    # Determine if this is using the slow form of crcmod.
    nested_crcmod = __import__(
        "crcmod.crcmod", globals(), locals(), ["_usingExtension"], 0,
    )
    fast_crc = getattr(nested_crcmod, "_usingExtension", False)
    if not fast_crc:
        warnings.warn(_SLOW_CRC32C_WARNING, RuntimeWarning, stacklevel=2)
    return fast_crc
