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

"""Common utilities for Google Media Downloads and Resumable Uploads.

Includes custom exception types, useful constants and shared helpers.
"""


_SLEEP_RETRY_ERROR_MSG = (
    u'At most one of `max_cumulative_retry` and `max_retries` '
    u'can be specified.')

UPLOAD_CHUNK_SIZE = 262144  # 256 * 1024
"""int: Chunks in a resumable upload must come in multiples of 256 KB."""
PERMANENT_REDIRECT = 308
"""int: Permanent redirect status code.

It is used by Google services to indicate some (but not all) of
a resumable upload has been completed.

``http.client.PERMANENT_REDIRECT`` was added in Python 3.5, so
can't be used in a "general" code base.

For more information, see `RFC 7238`_.

.. _RFC 7238: https://tools.ietf.org/html/rfc7238
"""
TOO_MANY_REQUESTS = 429
"""int: Status code indicating rate-limiting.

``http.client.TOO_MANY_REQUESTS`` was added in Python 3.3, so
can't be used in a "general" code base.

For more information, see `RFC 6585`_.

.. _RFC 6585: https://tools.ietf.org/html/rfc6585#section-4
"""
MAX_SLEEP = 64.0
"""float: Maximum amount of time allowed between requests.

Used during the retry process for sleep after a failed request.
Chosen since it is the power of two nearest to one minute.
"""
MAX_CUMULATIVE_RETRY = 600.0
"""float: Maximum total sleep time allowed during retry process.

This is provided (10 minutes) as a default. When the cumulative sleep
exceeds this limit, no more retries will occur.
"""


class InvalidResponse(Exception):
    """Error class for responses which are not in the correct state.

    Args:
        response (object): The HTTP response which caused the failure.
        args (tuple): The positional arguments typically passed to an
            exception class.
    """

    def __init__(self, response, *args):
        super(InvalidResponse, self).__init__(*args)
        self.response = response
        """object: The HTTP response object that caused the failure."""


class DataCorruption(Exception):
    """Error class for corrupt media transfers.

    Args:
        response (object): The HTTP response which caused the failure.
        args (tuple): The positional arguments typically passed to an
            exception class.
    """

    def __init__(self, response, *args):
        super(DataCorruption, self).__init__(*args)
        self.response = response
        """object: The HTTP response object that caused the failure."""


class RetryStrategy(object):
    """Configuration class for retrying failed requests.

    At most one of ``max_cumulative_retry`` and ``max_retries`` can be
    specified (they are both caps on the total number of retries). If
    neither are specified, then ``max_cumulative_retry`` is set as
    :data:`MAX_CUMULATIVE_RETRY`.

    Args:
        max_sleep (Optional[float]): The maximum amount of time to sleep after
            a failed request. Default is :attr:`MAX_SLEEP`.
        max_cumulative_retry (Optional[float]): The maximum **total** amount of
            time to sleep during retry process.
        max_retries (Optional[int]): The number of retries to attempt.

    Attributes:
        max_sleep (float): Maximum amount of time allowed between requests.
        max_cumulative_retry (Optional[float]): Maximum total sleep time
            allowed during retry process.
        max_retries (Optional[int]): The number retries to attempt.

    Raises:
        ValueError: If both of ``max_cumulative_retry`` and ``max_retries``
            are passed.
    """

    def __init__(self, max_sleep=MAX_SLEEP, max_cumulative_retry=None,
                 max_retries=None):
        if max_cumulative_retry is not None and max_retries is not None:
            raise ValueError(_SLEEP_RETRY_ERROR_MSG)
        if max_cumulative_retry is None and max_retries is None:
            max_cumulative_retry = MAX_CUMULATIVE_RETRY

        self.max_sleep = max_sleep
        self.max_cumulative_retry = max_cumulative_retry
        self.max_retries = max_retries

    def retry_allowed(self, total_sleep, num_retries):
        """Check if another retry is allowed.

        Args:
            total_sleep (float): The amount of sleep accumulated by the caller.
            num_retries (int): The number of retries already attempted by
                the caller.

        Returns:
            bool: Indicating if another retry is allowed (depending on either
            the cumulative sleep allowed or the maximum number of retries
            allowed.
        """
        if self.max_cumulative_retry is None:
            return num_retries <= self.max_retries
        else:
            return total_sleep <= self.max_cumulative_retry
