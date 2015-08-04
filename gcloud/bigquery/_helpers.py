# Copyright 2015 Google Inc. All rights reserved.
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

"""BigQuery utility functions."""


import datetime
import sys

import pytz

_EPOCH = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)


def _millis(when):
    """Convert a zone-aware datetime to integer milliseconds.

    :type when: ``datetime.datetime``
    :param when: the datetime to convert

    :rtype: integer
    :returns: milliseconds since epoch for ``when``
    """
    return int(_total_seconds(when - _EPOCH) * 1000)


def _datetime_from_prop(value):
    """Convert non-none timestamp to datetime, assuming UTC.

    :rtype: ``datetime.datetime``, or ``NoneType``
    """
    if value is not None:
        # back-end returns timestamps as milliseconds since the epoch
        seconds = int(value / 1000.0)
        microseconds = 1000.0 * (value - 1000 * seconds)
        return (
            _EPOCH +
            datetime.timedelta(seconds=seconds, microseconds=microseconds)
        )


def _prop_from_datetime(value):
    """Convert non-none datetime to timestamp, assuming UTC.

    :type value: ``datetime.datetime``, or None
    :param value: the timestamp

    :rtype: integer, or ``NoneType``
    :returns: the timestamp, in milliseconds, or None
    """
    if value is not None:
        if value.tzinfo is None:
            # Assume UTC
            value = value.replace(tzinfo=pytz.utc)
        # back-end wants timestamps as milliseconds since the epoch
        return _millis(value)


if sys.version_info[:2] < (2, 7):
    def _total_seconds(offset):  # pragma: NO COVER
        """Backport of timedelta.total_seconds() from python 2.7+."""
        seconds = offset.days * 24 * 60 * 60 + offset.seconds
        microseconds = seconds * 10**6 + offset.microseconds
        return microseconds / (10**6 * 1.0)
else:
    def _total_seconds(offset):
        return offset.total_seconds()
