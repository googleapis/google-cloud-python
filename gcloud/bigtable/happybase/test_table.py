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

import unittest2


class Test_make_row(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import make_row
        return make_row(*args, **kwargs)

    def test_it(self):
        with self.assertRaises(NotImplementedError):
            self._callFUT({}, False)


class Test_make_ordered_row(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import make_ordered_row
        return make_ordered_row(*args, **kwargs)

    def test_it(self):
        with self.assertRaises(NotImplementedError):
            self._callFUT([], False)


class TestTable(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.happybase.table import Table
        return Table

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        cluster = object()
        connection = _Connection(cluster)
        tables_constructed = []

        def make_low_level_table(*args, **kwargs):
            result = _MockLowLevelTable(*args, **kwargs)
            tables_constructed.append(result)
            return result

        with _Monkey(MUT, _LowLevelTable=make_low_level_table):
            table = self._makeOne(name, connection)
        self.assertEqual(table.name, name)
        self.assertEqual(table.connection, connection)

        table_instance, = tables_constructed
        self.assertEqual(table._low_level_table, table_instance)
        self.assertEqual(table_instance.args, (name, cluster))
        self.assertEqual(table_instance.kwargs, {})

    def test_constructor_null_connection(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        self.assertEqual(table.name, name)
        self.assertEqual(table.connection, connection)
        self.assertEqual(table._low_level_table, None)

    def test_families(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()

        # Mock the column families to be returned.
        col_fam_name = 'fam'
        gc_rule = object()
        col_fam = _MockLowLevelColumnFamily(col_fam_name, gc_rule=gc_rule)
        col_fams = {col_fam_name: col_fam}
        table._low_level_table.column_families = col_fams

        to_dict_result = object()
        to_dict_calls = []

        def mock_gc_rule_to_dict(gc_rule):
            to_dict_calls.append(gc_rule)
            return to_dict_result

        with _Monkey(MUT, _gc_rule_to_dict=mock_gc_rule_to_dict):
            result = table.families()

        self.assertEqual(result, {col_fam_name: to_dict_result})
        self.assertEqual(table._low_level_table.list_column_families_calls, 1)
        self.assertEqual(to_dict_calls, [gc_rule])

    def test___repr__(self):
        name = 'table-name'
        table = self._makeOne(name, None)
        self.assertEqual(repr(table), '<table.Table name=\'table-name\'>')

    def test_regions(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)

        with self.assertRaises(NotImplementedError):
            table.regions()


class Test__gc_rule_to_dict(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import _gc_rule_to_dict
        return _gc_rule_to_dict(*args, **kwargs)

    def test_with_null(self):
        gc_rule = None
        result = self._callFUT(gc_rule)
        self.assertEqual(result, {})

    def test_with_max_versions(self):
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        max_versions = 2
        gc_rule = MaxVersionsGCRule(max_versions)
        result = self._callFUT(gc_rule)
        expected_result = {'max_versions': max_versions}
        self.assertEqual(result, expected_result)

    def test_with_max_age(self):
        import datetime
        from gcloud.bigtable.column_family import MaxAgeGCRule

        time_to_live = 101
        max_age = datetime.timedelta(seconds=time_to_live)
        gc_rule = MaxAgeGCRule(max_age)
        result = self._callFUT(gc_rule)
        expected_result = {'time_to_live': time_to_live}
        self.assertEqual(result, expected_result)

    def test_with_non_gc_rule(self):
        gc_rule = object()
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)

    def test_with_gc_rule_union(self):
        from gcloud.bigtable.column_family import GCRuleUnion

        gc_rule = GCRuleUnion(rules=[])
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)

    def test_with_intersection_other_than_two(self):
        from gcloud.bigtable.column_family import GCRuleIntersection

        gc_rule = GCRuleIntersection(rules=[])
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)

    def test_with_intersection_two_max_num_versions(self):
        from gcloud.bigtable.column_family import GCRuleIntersection
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        rule1 = MaxVersionsGCRule(1)
        rule2 = MaxVersionsGCRule(2)
        gc_rule = GCRuleIntersection(rules=[rule1, rule2])
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)

    def test_with_intersection_two_rules(self):
        import datetime
        from gcloud.bigtable.column_family import GCRuleIntersection
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        time_to_live = 101
        max_age = datetime.timedelta(seconds=time_to_live)
        rule1 = MaxAgeGCRule(max_age)
        max_versions = 2
        rule2 = MaxVersionsGCRule(max_versions)
        gc_rule = GCRuleIntersection(rules=[rule1, rule2])
        result = self._callFUT(gc_rule)
        expected_result = {
            'max_versions': max_versions,
            'time_to_live': time_to_live,
        }
        self.assertEqual(result, expected_result)

    def test_with_intersection_two_nested_rules(self):
        from gcloud.bigtable.column_family import GCRuleIntersection

        rule1 = GCRuleIntersection(rules=[])
        rule2 = GCRuleIntersection(rules=[])
        gc_rule = GCRuleIntersection(rules=[rule1, rule2])
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)


class _Connection(object):

    def __init__(self, cluster):
        self._cluster = cluster


class _MockLowLevelColumnFamily(object):

    def __init__(self, column_family_id, gc_rule=None):
        self.column_family_id = column_family_id
        self.gc_rule = gc_rule


class _MockLowLevelTable(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.list_column_families_calls = 0
        self.column_families = {}

    def list_column_families(self):
        self.list_column_families_calls += 1
        return self.column_families
