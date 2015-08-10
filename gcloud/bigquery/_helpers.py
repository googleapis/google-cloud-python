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

from gcloud._helpers import UTC
from gcloud._helpers import _millis


_EPOCH = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=UTC)


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
            value = value.replace(tzinfo=UTC)
        # back-end wants timestamps as milliseconds since the epoch
        return _millis(value)
