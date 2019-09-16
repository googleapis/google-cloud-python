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

from google.resumable_media import common


RANGE_HEADER = u"range"
CONTENT_RANGE_HEADER = u"content-range"
RETRYABLE = (
    common.TOO_MANY_REQUESTS,
    http_client.INTERNAL_SERVER_ERROR,
    http_client.BAD_GATEWAY,
    http_client.SERVICE_UNAVAILABLE,
    http_client.GATEWAY_TIMEOUT,
)


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


def calculate_retry_wait(base_wait, max_sleep):
    """Calculate the amount of time to wait before a retry attempt.

    Wait time grows exponentially with the number of attempts, until
    it hits ``max_sleep``.

    A random amount of jitter (between 0 and 1 seconds) is added to spread out
    retry attempts from different clients.

    Args:
        base_wait (float): The "base" wait time (i.e. without any jitter)
            that will be doubled until it reaches the maximum sleep.
        max_sleep (float): Maximum value that a sleep time is allowed to be.

    Returns:
        Tuple[float, float]: The new base wait time as well as the wait time
        to be applied (with a random amount of jitter between 0 and 1 seconds
        added).
    """
    new_base_wait = 2.0 * base_wait
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
    response = func()
    if get_status_code(response) not in RETRYABLE:
        return response

    total_sleep = 0.0
    num_retries = 0
    base_wait = 0.5  # When doubled will give 1.0
    while retry_strategy.retry_allowed(total_sleep, num_retries):
        base_wait, wait_time = calculate_retry_wait(base_wait, retry_strategy.max_sleep)
        num_retries += 1
        total_sleep += wait_time
        time.sleep(wait_time)
        response = func()
        if get_status_code(response) not in RETRYABLE:
            return response

    return response
