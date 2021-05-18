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

from __future__ import absolute_import

import base64
import hashlib
import logging
import random
import time
import warnings

from google.resumable_media import common


RANGE_HEADER = u"range"
CONTENT_RANGE_HEADER = u"content-range"

_SLOW_CRC32C_WARNING = (
    "Currently using crcmod in pure python form. This is a slow "
    "implementation. Python 3 has a faster implementation, `google-crc32c`, "
    "which will be used if it is installed."
)
_HASH_HEADER = u"x-goog-hash"
_MISSING_CHECKSUM = u"""\
No {checksum_type} checksum was returned from the service while downloading {}
(which happens for composite objects), so client-side content integrity
checking is not being performed."""
_LOGGER = logging.getLogger(__name__)


def do_nothing():
    """Simple default callback."""


def header_required(response, name, get_headers, callback=do_nothing):
    """Checks that a specific header is in a headers dictionary.

    Args:
        response (object): An HTTP response object, expected to have a
            ``headers`` attribute that is a ``Mapping[str, str]``.
        name (str): The name of a required header.
        get_headers (Callable[Any, Mapping[str, str]]): Helper to get headers
            from an HTTP response.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        str: The desired header.

    Raises:
        ~google.resumable_media.common.InvalidResponse: If the header
            is missing.
    """
    headers = get_headers(response)
    if name not in headers:
        callback()
        raise common.InvalidResponse(
            response, u"Response headers must contain header", name
        )

    return headers[name]


def require_status_code(response, status_codes, get_status_code, callback=do_nothing):
    """Require a response has a status code among a list.

    Args:
        response (object): The HTTP response object.
        status_codes (tuple): The acceptable status codes.
        get_status_code (Callable[Any, int]): Helper to get a status code
            from a response.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        int: The status code.

    Raises:
        ~google.resumable_media.common.InvalidResponse: If the status code
            is not one of the values in ``status_codes``.
    """
    status_code = get_status_code(response)
    if status_code not in status_codes:
        callback()
        raise common.InvalidResponse(
            response,
            u"Request failed with status code",
            status_code,
            u"Expected one of",
            *status_codes
        )
    return status_code


def calculate_retry_wait(base_wait, max_sleep, multiplier=2.0):
    """Calculate the amount of time to wait before a retry attempt.

    Wait time grows exponentially with the number of attempts, until
    ``max_sleep``.

    A random amount of jitter (between 0 and 1 seconds) is added to spread out
    retry attempts from different clients.

    Args:
        base_wait (float): The "base" wait time (i.e. without any jitter)
            that will be multiplied until it reaches the maximum sleep.
        max_sleep (float): Maximum value that a sleep time is allowed to be.
        multiplier (float): Multiplier to apply to the base wait.

    Returns:
        Tuple[float, float]: The new base wait time as well as the wait time
        to be applied (with a random amount of jitter between 0 and 1 seconds
        added).
    """
    new_base_wait = multiplier * base_wait
    if new_base_wait > max_sleep:
        new_base_wait = max_sleep

    jitter_ms = random.randint(0, 1000)
    return new_base_wait, new_base_wait + 0.001 * jitter_ms


def wait_and_retry(func, get_status_code, retry_strategy):
    """Attempts to retry a call to ``func`` until success.

    Expects ``func`` to return an HTTP response and uses ``get_status_code``
    to check if the response is retry-able.

    Will retry until :meth:`~.RetryStrategy.retry_allowed` (on the current
    ``retry_strategy``) returns :data:`False`. Uses
    :func:`calculate_retry_wait` to double the wait time (with jitter) after
    each attempt.

    Args:
        func (Callable): A callable that takes no arguments and produces
            an HTTP response which will be checked as retry-able.
        get_status_code (Callable[Any, int]): Helper to get a status code
            from a response.
        retry_strategy (~google.resumable_media.common.RetryStrategy): The
            strategy to use if the request fails and must be retried.

    Returns:
        object: The return value of ``func``.
    """
    total_sleep = 0.0
    num_retries = 0
    # base_wait will be multiplied by the multiplier on the first retry.
    base_wait = float(retry_strategy.initial_delay) / retry_strategy.multiplier

    # Set the retriable_exception_type if possible. We expect requests to be
    # present here and the transport to be using requests.exceptions errors,
    # but due to loose coupling with the transport layer we can't guarantee it.
    try:
        connection_error_exceptions = _get_connection_error_classes()
    except ImportError:
        # We don't know the correct classes to use to catch connection errors,
        # so an empty tuple here communicates "catch no exceptions".
        connection_error_exceptions = ()

    while True:  # return on success or when retries exhausted.
        error = None
        try:
            response = func()
        except connection_error_exceptions as e:
            error = e
        else:
            if get_status_code(response) not in common.RETRYABLE:
                return response

        if not retry_strategy.retry_allowed(total_sleep, num_retries):
            # Retries are exhausted and no acceptable response was received. Raise the
            # retriable_error or return the unacceptable response.
            if error:
                raise error

            return response

        base_wait, wait_time = calculate_retry_wait(
            base_wait, retry_strategy.max_sleep, retry_strategy.multiplier
        )

        num_retries += 1
        total_sleep += wait_time
        time.sleep(wait_time)


def _get_crc32c_object():
    """Get crc32c object
    Attempt to use the Google-CRC32c package. If it isn't available, try
    to use CRCMod. CRCMod might be using a 'slow' varietal. If so, warn...
    """
    try:
        import google_crc32c

        crc_obj = google_crc32c.Checksum()
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
        "crcmod.crcmod",
        globals(),
        locals(),
        ["_usingExtension"],
        0,
    )
    fast_crc = getattr(nested_crcmod, "_usingExtension", False)
    if not fast_crc:
        warnings.warn(_SLOW_CRC32C_WARNING, RuntimeWarning, stacklevel=2)
    return fast_crc


def _get_metadata_key(checksum_type):
    if checksum_type == "md5":
        return "md5Hash"
    else:
        return checksum_type


def prepare_checksum_digest(digest_bytestring):
    """Convert a checksum object into a digest encoded for an HTTP header.

    Args:
        bytes: A checksum digest bytestring.

    Returns:
        str: A base64 string representation of the input.
    """
    encoded_digest = base64.b64encode(digest_bytestring)
    # NOTE: ``b64encode`` returns ``bytes``, but HTTP headers expect ``str``.
    return encoded_digest.decode(u"utf-8")


def _get_expected_checksum(response, get_headers, media_url, checksum_type):
    """Get the expected checksum and checksum object for the download response.

    Args:
        response (~requests.Response): The HTTP response object.
        get_headers (callable: response->dict): returns response headers.
        media_url (str): The URL containing the media to be downloaded.
        checksum_type Optional(str): The checksum type to read from the headers,
            exactly as it will appear in the headers (case-sensitive). Must be
            "md5", "crc32c" or None.

    Returns:
        Tuple (Optional[str], object): The expected checksum of the response,
        if it can be detected from the ``X-Goog-Hash`` header, and the
        appropriate checksum object for the expected checksum.
    """
    if checksum_type not in ["md5", "crc32c", None]:
        raise ValueError("checksum must be ``'md5'``, ``'crc32c'`` or ``None``")
    elif checksum_type in ["md5", "crc32c"]:
        headers = get_headers(response)
        expected_checksum = _parse_checksum_header(
            headers.get(_HASH_HEADER), response, checksum_label=checksum_type
        )

        if expected_checksum is None:
            msg = _MISSING_CHECKSUM.format(
                media_url, checksum_type=checksum_type.upper()
            )
            _LOGGER.info(msg)
            checksum_object = _DoNothingHash()
        else:
            if checksum_type == "md5":
                checksum_object = hashlib.md5()
            else:
                checksum_object = _get_crc32c_object()
    else:
        expected_checksum = None
        checksum_object = _DoNothingHash()

    return (expected_checksum, checksum_object)


def _parse_checksum_header(header_value, response, checksum_label):
    """Parses the checksum header from an ``X-Goog-Hash`` value.

    .. _header reference: https://cloud.google.com/storage/docs/\
                          xml-api/reference-headers#xgooghash

    Expects ``header_value`` (if not :data:`None`) to be in one of the three
    following formats:

    * ``crc32c=n03x6A==``
    * ``md5=Ojk9c3dhfxgoKVVHYwFbHQ==``
    * ``crc32c=n03x6A==,md5=Ojk9c3dhfxgoKVVHYwFbHQ==``

    See the `header reference`_ for more information.

    Args:
        header_value (Optional[str]): The ``X-Goog-Hash`` header from
            a download response.
        response (~requests.Response): The HTTP response object.
        checksum_label (str): The label of the header value to read, as in the
            examples above. Typically "md5" or "crc32c"

    Returns:
        Optional[str]: The expected checksum of the response, if it
        can be detected from the ``X-Goog-Hash`` header; otherwise, None.

    Raises:
        ~google.resumable_media.common.InvalidResponse: If there are
            multiple checksums of the requested type in ``header_value``.
    """
    if header_value is None:
        return None

    matches = []
    for checksum in header_value.split(u","):
        name, value = checksum.split(u"=", 1)
        # Official docs say "," is the separator, but real-world responses have encountered ", "
        if name.lstrip() == checksum_label:
            matches.append(value)

    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        raise common.InvalidResponse(
            response,
            u"X-Goog-Hash header had multiple ``{}`` values.".format(checksum_label),
            header_value,
            matches,
        )


def _get_checksum_object(checksum_type):
    """Respond with a checksum object for a supported type, if not None.

    Raises ValueError if checksum_type is unsupported.
    """
    if checksum_type == "md5":
        return hashlib.md5()
    elif checksum_type == "crc32c":
        return _get_crc32c_object()
    elif checksum_type is None:
        return None
    else:
        raise ValueError("checksum must be ``'md5'``, ``'crc32c'`` or ``None``")


def _get_connection_error_classes():
    """Get the exception error classes.

    Requests is a soft dependency here so that multiple transport layers can be
    added in the future. This code is in a separate function here so that the
    test framework can override its behavior to simulate requests being
    unavailable."""

    import requests.exceptions

    return (
        requests.exceptions.ConnectionError,
        requests.exceptions.ChunkedEncodingError,
    )


class _DoNothingHash(object):
    """Do-nothing hash object.

    Intended as a stand-in for ``hashlib.md5`` or a crc32c checksum
    implementation in cases where it isn't necessary to compute the hash.
    """

    def update(self, unused_chunk):
        """Do-nothing ``update`` method.

        Intended to match the interface of ``hashlib.md5`` and other checksums.

        Args:
            unused_chunk (bytes): A chunk of data.
        """
