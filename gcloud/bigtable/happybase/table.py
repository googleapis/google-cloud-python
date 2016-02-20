# Copyright 2016 Google Inc. All rights reserved.
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

"""Google Cloud Bigtable HappyBase table module."""


import six

from gcloud._helpers import _total_seconds
from gcloud.bigtable.column_family import GCRuleIntersection
from gcloud.bigtable.column_family import MaxAgeGCRule
from gcloud.bigtable.column_family import MaxVersionsGCRule
from gcloud.bigtable.table import Table as _LowLevelTable


_SIMPLE_GC_RULES = (MaxAgeGCRule, MaxVersionsGCRule)


def make_row(cell_map, include_timestamp):
    """Make a row dict for a Thrift cell mapping.

    .. note::

        This method is only provided for HappyBase compatibility, but does not
        actually work.

    :type cell_map: dict
    :param cell_map: Dictionary with ``fam:col`` strings as keys and ``TCell``
                     instances as values.

    :type include_timestamp: bool
    :param include_timestamp: Flag to indicate if cell timestamps should be
                              included with the output.

    :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
             always
    """
    raise NotImplementedError('The Cloud Bigtable API output is not the same '
                              'as the output from the Thrift server, so this '
                              'helper can not be implemented.', 'Called with',
                              cell_map, include_timestamp)


def make_ordered_row(sorted_columns, include_timestamp):
    """Make a row dict for sorted Thrift column results from scans.

    .. note::

        This method is only provided for HappyBase compatibility, but does not
        actually work.

    :type sorted_columns: list
    :param sorted_columns: List of ``TColumn`` instances from Thrift.

    :type include_timestamp: bool
    :param include_timestamp: Flag to indicate if cell timestamps should be
                              included with the output.

    :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
             always
    """
    raise NotImplementedError('The Cloud Bigtable API output is not the same '
                              'as the output from the Thrift server, so this '
                              'helper can not be implemented.', 'Called with',
                              sorted_columns, include_timestamp)


class Table(object):
    """Representation of Cloud Bigtable table.

    Used for adding data and

    :type name: str
    :param name: The name of the table.

    :type connection: :class:`.Connection`
    :param connection: The connection which has access to the table.
    """

    def __init__(self, name, connection):
        self.name = name
        # This remains as legacy for HappyBase, but only the cluster
        # from the connection is needed.
        self.connection = connection
        self._low_level_table = None
        if self.connection is not None:
            self._low_level_table = _LowLevelTable(self.name,
                                                   self.connection._cluster)

    def __repr__(self):
        return '<table.Table name=%r>' % (self.name,)

    def families(self):
        """Retrieve the column families for this table.

        :rtype: dict
        :returns: Mapping from column family name to garbage collection rule
                  for a column family.
        """
        column_family_map = self._low_level_table.list_column_families()
        result = {}
        for col_fam, col_fam_obj in six.iteritems(column_family_map):
            result[col_fam] = _gc_rule_to_dict(col_fam_obj.gc_rule)
        return result

    def regions(self):
        """Retrieve the regions for this table.

        Cloud Bigtable does not give information about how a table is laid
        out in memory, so regions so this method does not work. It is
        provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API does not have a '
                                  'concept of splitting a table into regions.')


def _gc_rule_to_dict(gc_rule):
    """Converts garbage collection rule to dictionary if possible.

    This is in place to support dictionary values as was done
    in HappyBase, which has somewhat different garbage collection rule
    settings for column families.

    Only does this if the garbage collection rule is:

    * :class:`.MaxAgeGCRule`
    * :class:`.MaxVersionsGCRule`
    * Composite :class:`.GCRuleIntersection` with two rules, one each
      of type :class:`.MaxAgeGCRule` and :class:`.MaxVersionsGCRule`

    Otherwise, just returns the input without change.

    :type gc_rule: :data:`NoneType <types.NoneType>`,
                   :class:`.GarbageCollectionRule`
    :param gc_rule: A garbage collection rule to convert to a dictionary
                    (if possible).

    :rtype: dict or :class:`.GarbageCollectionRule`
    :returns: The converted garbage collection rule.
    """
    result = gc_rule
    if gc_rule is None:
        result = {}
    elif isinstance(gc_rule, MaxAgeGCRule):
        result = {'time_to_live': _total_seconds(gc_rule.max_age)}
    elif isinstance(gc_rule, MaxVersionsGCRule):
        result = {'max_versions': gc_rule.max_num_versions}
    elif isinstance(gc_rule, GCRuleIntersection):
        if len(gc_rule.rules) == 2:
            rule1, rule2 = gc_rule.rules
            if (isinstance(rule1, _SIMPLE_GC_RULES) and
                    isinstance(rule2, _SIMPLE_GC_RULES)):
                rule1 = _gc_rule_to_dict(rule1)
                rule2 = _gc_rule_to_dict(rule2)
                key1, = rule1.keys()
                key2, = rule2.keys()
                if key1 != key2:
                    result = {key1: rule1[key1], key2: rule2[key2]}
    return result
