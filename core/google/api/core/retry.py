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

"""Helpers for retrying functions with exponential back-off."""

import datetime
import logging
import random
import time

import six

from google.api.core import exceptions
from google.api.core.helpers import datetime_helpers

_LOGGER = logging.getLogger(__name__)
_DEFAULT_JITTER_AMOUNT = 0.2


def if_exception_type(*exception_types):
    """Creates a predicate to check if the exception is of a given type.

    Args:
        exception_types (Sequence[type]): The exception types to check for.

    Returns:
        Callable[Exception]: A predicate that returns True if the provided
            exception is of the given type(s).
    """
    def inner(exception):
        """Bound predicate for checking an exception type."""
        return isinstance(exception, exception_types)
    return inner


# pylint: disable=invalid-name
# Pylint sees this as a constant, but it is also an alias that should be
# considered a function.
if_transient_error = if_exception_type((
    exceptions.InternalServerError,
    exceptions.TooManyRequests))
"""A predicate that checks if an exception is a transient API error."""
# pylint: enable=invalid-name


def exponential_sleep_generator(
        initial, maximum, multiplier=2, jitter=_DEFAULT_JITTER_AMOUNT):
    """Generates sleep intervals based on the exponential back-off algorithm.

    This implements the `Truncated Exponential Back-off`_ algorithm.

    .. _Truncated Exponential Back-off:
        https://cloud.google.com/storage/docs/exponential-backoff

    Args:
        initial (float): The minimum about of time to delay. This must
            be greater than 0.
        maximum (float): The maximum about of time to delay.
        multiplier (float): The multiplier applied to the delay.
        jitter (float): The maximum about of randomness to apply to the delay.

    Yields:
        float: successive sleep intervals.
    """
    delay = initial
    while True:
        yield delay
        delay = min(
            delay * multiplier + random.uniform(0, jitter), maximum)


def retry_target(target, predicate, sleep_generator, deadline):
    """Call a function and retry if it fails.

    This is the lowest-level retry helper. Generally, you'll use the
    higher-level retry helper :class:`Retry`.

    Args:
        target(Callable): The function to call and retry. This must be a
            nullary function - apply arguments with `functools.partial`.
        predicate (Callable[Exception]): A callable used to determine if an
            exception raised by the target should be considered retryable.
            It should return True to retry or False otherwise.
        sleep_generator (Iterator[float]): An infinite iterator that determines
            how long to sleep between retries.
        deadline (float): How long to keep retrying the target.

    Returns:
        Any: the return value of the target function.

    Raises:
        google.api.core.RetryError: If the deadline is exceeded while retrying.
        ValueError: If the sleep generator stops yielding values.
        Exception: If the target raises a method that isn't retryable.
    """
    if deadline is not None:
        deadline_datetime = (
            datetime_helpers.utcnow() + datetime.timedelta(seconds=deadline))
    else:
        deadline_datetime = None

    last_exc = None

    for sleep in sleep_generator:
        try:
            return target()

        # pylint: disable=broad-except
        # This function explicitly must deal with broad exceptions.
        except Exception as exc:
            if not predicate(exc):
                raise
            last_exc = exc

        now = datetime_helpers.utcnow()
        if deadline_datetime is not None and deadline_datetime < now:
            six.raise_from(
                exceptions.RetryError(
                    'Deadline of {:.1f}s exceeded while calling {}'.format(
                        deadline, target),
                    last_exc),
                last_exc)

        _LOGGER.debug('Retrying due to {}, sleeping {:.1f}s ...'.format(
            last_exc, sleep))
        time.sleep(sleep)

    raise ValueError('Sleep generator stopped yielding sleep values.')
