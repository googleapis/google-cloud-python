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


import datetime

from google.protobuf import duration_pb2

from gcloud._helpers import _total_seconds
from gcloud.bigtable._generated_v2 import (
    table_pb2 as table_v2_pb2)
from gcloud.bigtable._generated_v2 import (
    bigtable_table_admin_pb2 as table_admin_v2_pb2)


def _timedelta_to_duration_pb(timedelta_val):
    """Convert a Python timedelta object to a duration protobuf.

    .. note::

        The Python timedelta has a granularity of microseconds while
        the protobuf duration type has a duration of nanoseconds.

    :type timedelta_val: :class:`datetime.timedelta`
    :param timedelta_val: A timedelta object.

    :rtype: :class:`google.protobuf.duration_pb2.Duration`
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


def _duration_pb_to_timedelta(duration_pb):
    """Convert a duration protobuf to a Python timedelta object.

    .. note::

        The Python timedelta has a granularity of microseconds while
        the protobuf duration type has a duration of nanoseconds.

    :type duration_pb: :class:`google.protobuf.duration_pb2.Duration`
    :param duration_pb: A protobuf duration object.

    :rtype: :class:`datetime.timedelta`
    :returns: The converted timedelta object.
    """
    return datetime.timedelta(
        seconds=duration_pb.seconds,
        microseconds=(duration_pb.nanos / 1000.0),
    )


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

        :rtype: :class:`.table_v2_pb2.GcRule`
        :returns: The converted current object.
        """
        return table_v2_pb2.GcRule(max_num_versions=self.max_num_versions)


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

        :rtype: :class:`.table_v2_pb2.GcRule`
        :returns: The converted current object.
        """
        max_age = _timedelta_to_duration_pb(self.max_age)
        return table_v2_pb2.GcRule(max_age=max_age)


class GCRuleUnion(GarbageCollectionRule):
    """Union of garbage collection rules.

    :type rules: list
    :param rules: List of :class:`GarbageCollectionRule`.
    """

    def __init__(self, rules):
        self.rules = rules

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.rules == self.rules

    def to_pb(self):
        """Converts the union into a single GC rule as a protobuf.

        :rtype: :class:`.table_v2_pb2.GcRule`
        :returns: The converted current object.
        """
        union = table_v2_pb2.GcRule.Union(
            rules=[rule.to_pb() for rule in self.rules])
        return table_v2_pb2.GcRule(union=union)


class GCRuleIntersection(GarbageCollectionRule):
    """Intersection of garbage collection rules.

    :type rules: list
    :param rules: List of :class:`GarbageCollectionRule`.
    """

    def __init__(self, rules):
        self.rules = rules

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.rules == self.rules

    def to_pb(self):
        """Converts the intersection into a single GC rule as a protobuf.

        :rtype: :class:`.table_v2_pb2.GcRule`
        :returns: The converted current object.
        """
        intersection = table_v2_pb2.GcRule.Intersection(
            rules=[rule.to_pb() for rule in self.rules])
        return table_v2_pb2.GcRule(intersection=intersection)


class ColumnFamily(object):
    """Representation of a Google Cloud Bigtable Column Family.

    We can use a :class:`ColumnFamily` to:

    * :meth:`create` itself
    * :meth:`update` itself
    * :meth:`delete` itself

    :type column_family_id: str
    :param column_family_id: The ID of the column family. Must be of the
                             form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

    :type table: :class:`Table <gcloud.bigtable.table.Table>`
    :param table: The table that owns the column family.

    :type gc_rule: :class:`GarbageCollectionRule`
    :param gc_rule: (Optional) The garbage collection settings for this
                    column family.
    """

    def __init__(self, column_family_id, table, gc_rule=None):
        self.column_family_id = column_family_id
        self._table = table
        self.gc_rule = gc_rule

    @property
    def name(self):
        """Column family name used in requests.

        .. note::

          This property will not change if ``column_family_id`` does not, but
          the return value is not cached.

        The table name is of the form

            ``"projects/../zones/../clusters/../tables/../columnFamilies/.."``

        :rtype: str
        :returns: The column family name.
        """
        return self._table.name + '/columnFamilies/' + self.column_family_id

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.column_family_id == self.column_family_id and
                other._table == self._table and
                other.gc_rule == self.gc_rule)

    def __ne__(self, other):
        return not self.__eq__(other)

    def create(self):
        """Create this column family."""
        if self.gc_rule is None:
            column_family = table_v2_pb2.ColumnFamily()
        else:
            column_family = table_v2_pb2.ColumnFamily(
                gc_rule=self.gc_rule.to_pb())
        request_pb = table_admin_v2_pb2.ModifyColumnFamiliesRequest(
            name=self._table.name)
        request_pb.modifications.add(
            id=self.column_family_id,
            create=column_family,
        )
        client = self._table._instance._client
        # We expect a `.table_v2_pb2.ColumnFamily`. We ignore it since the only
        # data it contains are the GC rule and the column family ID already
        # stored on this instance.
        client._table_stub.ModifyColumnFamilies(request_pb,
                                                client.timeout_seconds)

    def update(self):
        """Update this column family.

        .. note::

            Only the GC rule can be updated. By changing the column family ID,
            you will simply be referring to a different column family.
        """
        if self.gc_rule is None:
            column_family = table_v2_pb2.ColumnFamily()
        else:
            column_family = table_v2_pb2.ColumnFamily(
                gc_rule=self.gc_rule.to_pb())
        request_pb = table_admin_v2_pb2.ModifyColumnFamiliesRequest(
            name=self._table.name)
        request_pb.modifications.add(
            id=self.column_family_id,
            update=column_family)
        client = self._table._instance._client
        # We expect a `.table_v2_pb2.ColumnFamily`. We ignore it since the only
        # data it contains are the GC rule and the column family ID already
        # stored on this instance.
        client._table_stub.ModifyColumnFamilies(request_pb,
                                                client.timeout_seconds)

    def delete(self):
        """Delete this column family."""
        request_pb = table_admin_v2_pb2.ModifyColumnFamiliesRequest(
            name=self._table.name)
        request_pb.modifications.add(
            id=self.column_family_id,
            drop=True)
        client = self._table._instance._client
        # We expect a `google.protobuf.empty_pb2.Empty`
        client._table_stub.ModifyColumnFamilies(request_pb,
                                                client.timeout_seconds)


def _gc_rule_from_pb(gc_rule_pb):
    """Convert a protobuf GC rule to a native object.

    :type gc_rule_pb: :class:`.table_v2_pb2.GcRule`
    :param gc_rule_pb: The GC rule to convert.

    :rtype: :class:`GarbageCollectionRule` or :data:`NoneType <types.NoneType>`
    :returns: An instance of one of the native rules defined
              in :module:`column_family` or :data:`None` if no values were
              set on the protobuf passed in.
    :raises: :class:`ValueError <exceptions.ValueError>` if the rule name
             is unexpected.
    """
    rule_name = gc_rule_pb.WhichOneof('rule')
    if rule_name is None:
        return None

    if rule_name == 'max_num_versions':
        return MaxVersionsGCRule(gc_rule_pb.max_num_versions)
    elif rule_name == 'max_age':
        max_age = _duration_pb_to_timedelta(gc_rule_pb.max_age)
        return MaxAgeGCRule(max_age)
    elif rule_name == 'union':
        return GCRuleUnion([_gc_rule_from_pb(rule)
                            for rule in gc_rule_pb.union.rules])
    elif rule_name == 'intersection':
        rules = [_gc_rule_from_pb(rule)
                 for rule in gc_rule_pb.intersection.rules]
        return GCRuleIntersection(rules)
    else:
        raise ValueError('Unexpected rule name', rule_name)
