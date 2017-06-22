# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Types used in the Google BigQuery DB-API.

See `PEP 249`_ for details.

.. _`PEP 249`:
    https://www.python.org/dev/peps/pep-0249/#type-objects-and-constructors
"""

import datetime

import six


Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime
DateFromTicks = datetime.date.fromtimestamp
TimestampFromTicks = datetime.datetime.fromtimestamp
Binary = six.binary_type


def TimeFromTicks(ticks, tz=None):
    """Construct a DB-API time value from the given ticks value.

    :type ticks: float
    :param ticks:
        a number of seconds since the epoch; see the documentation of the
        standard Python time module for details.

    :type tz: :class:`datetime.tzinfo`
    :param tz: (Optional) time zone to use for conversion

    :rtype: :class:`datetime.time`
    :returns: time represented by ticks.
    """
    dt = datetime.datetime.fromtimestamp(ticks, tz=tz)
    return dt.timetz()


class _DBAPITypeObject(object):
    """DB-API type object which compares equal to many different strings.

    See `PEP 249`_ for details.

    .. _`PEP 249`:
        https://www.python.org/dev/peps/pep-0249/#implementation-hints-for-module-authors
    """

    def __init__(self, *values):
        self.values = values

    def __eq__(self, other):
        if other in self.values:
            return True
        return False


STRING = 'STRING'
BINARY = _DBAPITypeObject('BYTES', 'RECORD', 'STRUCT')
NUMBER = _DBAPITypeObject(
    'INTEGER', 'INT64', 'FLOAT', 'FLOAT64', 'BOOLEAN', 'BOOL')
DATETIME = _DBAPITypeObject('TIMESTAMP', 'DATE', 'TIME', 'DATETIME')
ROWID = 'ROWID'
