# Copyright 2017 Google LLC
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

"""Helpers for :mod:`datetime`."""

import calendar
import datetime
import re

import pytz


_UTC_EPOCH = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
_RFC3339_MICROS = '%Y-%m-%dT%H:%M:%S.%fZ'
_RFC3339_NO_FRACTION = '%Y-%m-%dT%H:%M:%S'
# datetime.strptime cannot handle nanosecond precision:  parse w/ regex
_RFC3339_NANOS = re.compile(r"""
    (?P<no_fraction>
        \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}  # YYYY-MM-DDTHH:MM:SS
    )
    (                                        # Optional decimal part
     \.                                      # decimal point
     (?P<nanos>\d{1,9})                      # nanoseconds, maybe truncated
    )?
    Z                                        # Zulu
""", re.VERBOSE)


def utcnow():
    """A :meth:`datetime.datetime.utcnow()` alias to allow mocking in tests."""
    return datetime.datetime.utcnow()


def to_milliseconds(value):
    """Convert a zone-aware datetime to milliseconds since the unix epoch.

    Args:
        value (datetime.datetime): The datetime to covert.

    Returns:
        int: Milliseconds since the unix epoch.
    """
    micros = to_microseconds(value)
    return micros // 1000


def from_microseconds(value):
    """Convert timestamp in microseconds since the unix epoch to datetime.

    Args:
        value (float): The timestamp to convert, in microseconds.

    Returns:
        datetime.datetime: The datetime object equivalent to the timestamp in
            UTC.
    """
    return _UTC_EPOCH + datetime.timedelta(microseconds=value)


def to_microseconds(value):
    """Convert a datetime to microseconds since the unix epoch.

    Args:
        value (datetime.datetime): The datetime to covert.

    Returns:
        int: Microseconds since the unix epoch.
    """
    if not value.tzinfo:
        value = value.replace(tzinfo=pytz.utc)
    # Regardless of what timezone is on the value, convert it to UTC.
    value = value.astimezone(pytz.utc)
    # Convert the datetime to a microsecond timestamp.
    return int(calendar.timegm(value.timetuple()) * 1e6) + value.microsecond


def from_iso8601_date(value):
    """Convert a ISO8601 date string to a date.

    Args:
        value (str): The ISO8601 date string.

    Returns:
        datetime.date: A date equivalent to the date string.
    """
    return datetime.datetime.strptime(value, '%Y-%m-%d').date()


def from_iso8601_time(value):
    """Convert a zoneless ISO8601 time string to a time.

    Args:
        value (str): The ISO8601 time string.

    Returns:
        datetime.time: A time equivalent to the time string.
    """
    return datetime.datetime.strptime(value, '%H:%M:%S').time()


def from_rfc3339(value):
    """Convert a microsecond-precision timestamp to datetime.

    Args:
        value (str): The RFC3339 string to convert.

    Returns:
        datetime.datetime: The datetime object equivalent to the timestamp in
            UTC.
    """
    return datetime.datetime.strptime(
        value, _RFC3339_MICROS).replace(tzinfo=pytz.utc)


def from_rfc3339_nanos(value):
    """Convert a nanosecond-precision timestamp to a native datetime.

    .. note::
        Python datetimes do not support nanosecond precision; this function
        therefore truncates such values to microseconds.

    Args:
        value (str): The RFC3339 string to convert.

    Returns:
        datetime.datetime: The datetime object equivalent to the timestamp in
            UTC.

    Raises:
        ValueError: If the timestamp does not match the RFC 3339
            regular expression.
    """
    with_nanos = _RFC3339_NANOS.match(value)

    if with_nanos is None:
        raise ValueError(
            'Timestamp: {!r}, does not match pattern: {!r}'.format(
                value, _RFC3339_NANOS.pattern))

    bare_seconds = datetime.datetime.strptime(
        with_nanos.group('no_fraction'), _RFC3339_NO_FRACTION)
    fraction = with_nanos.group('nanos')

    if fraction is None:
        micros = 0
    else:
        scale = 9 - len(fraction)
        nanos = int(fraction) * (10 ** scale)
        micros = nanos // 1000

    return bare_seconds.replace(microsecond=micros, tzinfo=pytz.utc)


def to_rfc3339(value, ignore_zone=True):
    """Convert a datetime to an RFC3339 timestamp string.

    Args:
        value (datetime.datetime):
            The datetime object to be converted to a string.
        ignore_zone (bool): If True, then the timezone (if any) of the
            datetime object is ignored and the datetime is treated as UTC.

    Returns:
        str: The RFC3339 formated string representing the datetime.
    """
    if not ignore_zone and value.tzinfo is not None:
        # Convert to UTC and remove the time zone info.
        value = value.replace(tzinfo=None) - value.utcoffset()

    return value.strftime(_RFC3339_MICROS)
