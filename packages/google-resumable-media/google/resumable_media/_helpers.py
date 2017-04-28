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


import random
import time

from six.moves import http_client

from google.resumable_media import constants
from google.resumable_media import exceptions


RANGE_HEADER = u'range'
CONTENT_RANGE_HEADER = u'content-range'
RETRYABLE = (
    constants.TOO_MANY_REQUESTS,
    http_client.INTERNAL_SERVER_ERROR,
    http_client.BAD_GATEWAY,
    http_client.SERVICE_UNAVAILABLE,
    http_client.GATEWAY_TIMEOUT,
)
MAX_SLEEP = 64.0  # Just over 1 minute.
MAX_SLEEP_EXPONENT = 6  # 2^6 = 64.
MAX_CUMULATIVE_RETRY = 600.0  # 10 minutes


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
        ~google.resumable_media.exceptions.InvalidResponse: If the header
            is missing.
    """
    headers = get_headers(response)
    if name not in headers:
        callback()
        raise exceptions.InvalidResponse(
            response, u'Response headers must contain header', name)

    return headers[name]


def require_status_code(response, status_codes, get_status_code,
                        callback=do_nothing):
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


def calculate_retry_wait(num_retries):
    """Calculate the amount of time to wait before a retry attempt.

    Wait time grows exponentially with the number of attempts, until
    it hits :attr:`MAX_SLEEP`.

    A random amount of jitter (between 0 and 1 seconds) is added to spread out
    retry attempts from different clients.

    Args:
        num_retries (int): The number of retries already attempted. If
            no retries have been attempted, should return 1 second with
            some jitter.

    Returns:
        float: The number of seconds to wait before retrying (with a random
        amount of jitter between 0 and 1 seconds added).
    """
    if num_retries < MAX_SLEEP_EXPONENT:
        wait_time = 2**num_retries
    else:
        wait_time = MAX_SLEEP

    jitter_ms = random.randint(0, 1000)
    return wait_time + 0.001 * jitter_ms


def wait_and_retry(func, get_status_code):
    """Attempts to retry a call to ``func`` until success.

    Expects ``func`` to return an HTTP response and uses ``get_status_code``
    to check if the response is retry-able.

    Will retry until :attr:`MAX_CUMULATIVE_RETRY` seconds of wait time
    have accrued. Uses :func:`calculate_retry_wait` to double the
    wait time (with jitter) after each attempt.

    Args:
        func (Callable): A callable that takes no arguments and produces
            an HTTP response which will be checked as retry-able.
        get_status_code (Callable[Any, int]): Helper to get a status code
            from a response.

    Returns:
        object: The return value of ``func``.
    """
    response = func()
    if get_status_code(response) not in RETRYABLE:
        return response

    total_sleep = 0.0
    num_retries = 0
    while total_sleep < MAX_CUMULATIVE_RETRY:
        wait_time = calculate_retry_wait(num_retries)
        num_retries += 1
        total_sleep += wait_time
        time.sleep(wait_time)
        response = func()
        if get_status_code(response) not in RETRYABLE:
            return response

    return response
