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

"""User friendly container for Google Cloud Bigtable Column Family."""


from gcloud._helpers import _total_seconds
from gcloud.bigtable._generated import bigtable_table_data_pb2 as data_pb2
from gcloud.bigtable._generated import duration_pb2


def _timedelta_to_duration_pb(timedelta_val):
    """Convert a Python timedelta object to a duration protobuf.

    .. note::

        The Python timedelta has a granularity of microseconds while
        the protobuf duration type has a duration of nanoseconds.

    :type timedelta_val: :class:`datetime.timedelta`
    :param timedelta_val: A timedelta object.

    :rtype: :class:`duration_pb2.Duration`
    :returns: A duration object equivalent to the time delta.
    """
    seconds_decimal = _total_seconds(timedelta_val)
    # Truncate the parts other than the integer.
    seconds = int(seconds_decimal)
    if seconds_decimal < 0:
        signed_micros = timedelta_val.microseconds - 10**6
    else:
        signed_micros = timedelta_val.microseconds
    # Convert nanoseconds to microseconds.
    nanos = 1000 * signed_micros
    return duration_pb2.Duration(seconds=seconds, nanos=nanos)


class GarbageCollectionRule(object):
    """Garbage collection rule for column families within a table.

    Cells in the column family (within a table) fitting the rule will be
    deleted during garbage collection.

    .. note::

        This class is a do-nothing base class for all GC rules.

    .. note::

        A string ``gc_expression`` can also be used with API requests, but
        that value would be superceded by a ``gc_rule``. As a result, we
        don't support that feature and instead support via native classes.
    """

    def to_pb(self):
        """Converts the :class:`GarbageCollectionRule` to a protobuf.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always since a virtual class.
        """
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)


class MaxVersionsGCRule(GarbageCollectionRule):
    """Garbage collection limiting the number of versions of a cell.

    :type max_num_versions: int
    :param max_num_versions: The maximum number of versions
    """

    def __init__(self, max_num_versions):
        self.max_num_versions = max_num_versions

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.max_num_versions == self.max_num_versions

    def to_pb(self):
        """Converts the garbage collection rule to a protobuf.

        :rtype: :class:`.data_pb2.GcRule`
        :returns: The converted current object.
        """
        return data_pb2.GcRule(max_num_versions=self.max_num_versions)


class MaxAgeGCRule(GarbageCollectionRule):
    """Garbage collection limiting the age of a cell.

    :type max_age: :class:`datetime.timedelta`
    :param max_age: The maximum age allowed for a cell in the table.
    """

    def __init__(self, max_age):
        self.max_age = max_age

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.max_age == self.max_age

    def to_pb(self):
        """Converts the garbage collection rule to a protobuf.

        :rtype: :class:`.data_pb2.GcRule`
        :returns: The converted current object.
        """
        max_age = _timedelta_to_duration_pb(self.max_age)
        return data_pb2.GcRule(max_age=max_age)


class ColumnFamily(object):
    """Representation of a Google Cloud Bigtable Column Family.

    :type column_family_id: str
    :param column_family_id: The ID of the column family. Must be of the
                             form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

    :type table: :class:`Table <gcloud.bigtable.table.Table>`
    :param table: The table that owns the column family.
    """

    def __init__(self, column_family_id, table):
        self.column_family_id = column_family_id
        self._table = table
