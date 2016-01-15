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


import unittest2


class Test__timedelta_to_duration_pb(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.column_family import _timedelta_to_duration_pb
        return _timedelta_to_duration_pb(*args, **kwargs)

    def test_it(self):
        import datetime
        from google.protobuf import duration_pb2

        seconds = microseconds = 1
        timedelta_val = datetime.timedelta(seconds=seconds,
                                           microseconds=microseconds)
        result = self._callFUT(timedelta_val)
        self.assertTrue(isinstance(result, duration_pb2.Duration))
        self.assertEqual(result.seconds, seconds)
        self.assertEqual(result.nanos, 1000 * microseconds)

    def test_with_negative_microseconds(self):
        import datetime
        from google.protobuf import duration_pb2

        seconds = 1
        microseconds = -5
        timedelta_val = datetime.timedelta(seconds=seconds,
                                           microseconds=microseconds)
        result = self._callFUT(timedelta_val)
        self.assertTrue(isinstance(result, duration_pb2.Duration))
        self.assertEqual(result.seconds, seconds - 1)
        self.assertEqual(result.nanos, 10**9 + 1000 * microseconds)

    def test_with_negative_seconds(self):
        import datetime
        from google.protobuf import duration_pb2

        seconds = -1
        microseconds = 5
        timedelta_val = datetime.timedelta(seconds=seconds,
                                           microseconds=microseconds)
        result = self._callFUT(timedelta_val)
        self.assertTrue(isinstance(result, duration_pb2.Duration))
        self.assertEqual(result.seconds, seconds + 1)
        self.assertEqual(result.nanos, -(10**9 - 1000 * microseconds))


class Test__duration_pb_to_timedelta(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.column_family import _duration_pb_to_timedelta
        return _duration_pb_to_timedelta(*args, **kwargs)

    def test_it(self):
        import datetime
        from google.protobuf import duration_pb2

        seconds = microseconds = 1
        duration_pb = duration_pb2.Duration(seconds=seconds,
                                            nanos=1000 * microseconds)
        timedelta_val = datetime.timedelta(seconds=seconds,
                                           microseconds=microseconds)
        result = self._callFUT(duration_pb)
        self.assertTrue(isinstance(result, datetime.timedelta))
        self.assertEqual(result, timedelta_val)


class TestMaxVersionsGCRule(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import MaxVersionsGCRule
        return MaxVersionsGCRule

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test___eq__type_differ(self):
        gc_rule1 = self._makeOne(10)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___eq__same_value(self):
        gc_rule1 = self._makeOne(2)
        gc_rule2 = self._makeOne(2)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        gc_rule1 = self._makeOne(99)
        gc_rule2 = self._makeOne(99)
        comparison_val = (gc_rule1 != gc_rule2)
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        max_num_versions = 1337
        gc_rule = self._makeOne(max_num_versions=max_num_versions)
        pb_val = gc_rule.to_pb()
        self.assertEqual(pb_val,
                         data_pb2.GcRule(max_num_versions=max_num_versions))


class TestMaxAgeGCRule(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import MaxAgeGCRule
        return MaxAgeGCRule

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test___eq__type_differ(self):
        max_age = object()
        gc_rule1 = self._makeOne(max_age=max_age)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___eq__same_value(self):
        max_age = object()
        gc_rule1 = self._makeOne(max_age=max_age)
        gc_rule2 = self._makeOne(max_age=max_age)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        max_age = object()
        gc_rule1 = self._makeOne(max_age=max_age)
        gc_rule2 = self._makeOne(max_age=max_age)
        comparison_val = (gc_rule1 != gc_rule2)
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        import datetime
        from google.protobuf import duration_pb2
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)

        max_age = datetime.timedelta(seconds=1)
        duration = duration_pb2.Duration(seconds=1)
        gc_rule = self._makeOne(max_age=max_age)
        pb_val = gc_rule.to_pb()
        self.assertEqual(pb_val, data_pb2.GcRule(max_age=duration))


class TestGCRuleUnion(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import GCRuleUnion
        return GCRuleUnion

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        rules = object()
        rule_union = self._makeOne(rules)
        self.assertTrue(rule_union.rules is rules)

    def test___eq__(self):
        rules = object()
        gc_rule1 = self._makeOne(rules)
        gc_rule2 = self._makeOne(rules)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___eq__type_differ(self):
        rules = object()
        gc_rule1 = self._makeOne(rules)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        rules = object()
        gc_rule1 = self._makeOne(rules)
        gc_rule2 = self._makeOne(rules)
        comparison_val = (gc_rule1 != gc_rule2)
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        import datetime
        from google.protobuf import duration_pb2
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        max_num_versions = 42
        rule1 = MaxVersionsGCRule(max_num_versions)
        pb_rule1 = data_pb2.GcRule(max_num_versions=max_num_versions)

        max_age = datetime.timedelta(seconds=1)
        rule2 = MaxAgeGCRule(max_age)
        pb_rule2 = data_pb2.GcRule(max_age=duration_pb2.Duration(seconds=1))

        rule3 = self._makeOne(rules=[rule1, rule2])
        pb_rule3 = data_pb2.GcRule(
            union=data_pb2.GcRule.Union(rules=[pb_rule1, pb_rule2]))

        gc_rule_pb = rule3.to_pb()
        self.assertEqual(gc_rule_pb, pb_rule3)

    def test_to_pb_nested(self):
        import datetime
        from google.protobuf import duration_pb2
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        max_num_versions1 = 42
        rule1 = MaxVersionsGCRule(max_num_versions1)
        pb_rule1 = data_pb2.GcRule(max_num_versions=max_num_versions1)

        max_age = datetime.timedelta(seconds=1)
        rule2 = MaxAgeGCRule(max_age)
        pb_rule2 = data_pb2.GcRule(max_age=duration_pb2.Duration(seconds=1))

        rule3 = self._makeOne(rules=[rule1, rule2])
        pb_rule3 = data_pb2.GcRule(
            union=data_pb2.GcRule.Union(rules=[pb_rule1, pb_rule2]))

        max_num_versions2 = 1337
        rule4 = MaxVersionsGCRule(max_num_versions2)
        pb_rule4 = data_pb2.GcRule(max_num_versions=max_num_versions2)

        rule5 = self._makeOne(rules=[rule3, rule4])
        pb_rule5 = data_pb2.GcRule(
            union=data_pb2.GcRule.Union(rules=[pb_rule3, pb_rule4]))

        gc_rule_pb = rule5.to_pb()
        self.assertEqual(gc_rule_pb, pb_rule5)


class TestGCRuleIntersection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import GCRuleIntersection
        return GCRuleIntersection

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        rules = object()
        rule_intersection = self._makeOne(rules)
        self.assertTrue(rule_intersection.rules is rules)

    def test___eq__(self):
        rules = object()
        gc_rule1 = self._makeOne(rules)
        gc_rule2 = self._makeOne(rules)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___eq__type_differ(self):
        rules = object()
        gc_rule1 = self._makeOne(rules)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        rules = object()
        gc_rule1 = self._makeOne(rules)
        gc_rule2 = self._makeOne(rules)
        comparison_val = (gc_rule1 != gc_rule2)
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        import datetime
        from google.protobuf import duration_pb2
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        max_num_versions = 42
        rule1 = MaxVersionsGCRule(max_num_versions)
        pb_rule1 = data_pb2.GcRule(max_num_versions=max_num_versions)

        max_age = datetime.timedelta(seconds=1)
        rule2 = MaxAgeGCRule(max_age)
        pb_rule2 = data_pb2.GcRule(max_age=duration_pb2.Duration(seconds=1))

        rule3 = self._makeOne(rules=[rule1, rule2])
        pb_rule3 = data_pb2.GcRule(
            intersection=data_pb2.GcRule.Intersection(
                rules=[pb_rule1, pb_rule2]))

        gc_rule_pb = rule3.to_pb()
        self.assertEqual(gc_rule_pb, pb_rule3)

    def test_to_pb_nested(self):
        import datetime
        from google.protobuf import duration_pb2
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        max_num_versions1 = 42
        rule1 = MaxVersionsGCRule(max_num_versions1)
        pb_rule1 = data_pb2.GcRule(max_num_versions=max_num_versions1)

        max_age = datetime.timedelta(seconds=1)
        rule2 = MaxAgeGCRule(max_age)
        pb_rule2 = data_pb2.GcRule(max_age=duration_pb2.Duration(seconds=1))

        rule3 = self._makeOne(rules=[rule1, rule2])
        pb_rule3 = data_pb2.GcRule(
            intersection=data_pb2.GcRule.Intersection(
                rules=[pb_rule1, pb_rule2]))

        max_num_versions2 = 1337
        rule4 = MaxVersionsGCRule(max_num_versions2)
        pb_rule4 = data_pb2.GcRule(max_num_versions=max_num_versions2)

        rule5 = self._makeOne(rules=[rule3, rule4])
        pb_rule5 = data_pb2.GcRule(
            intersection=data_pb2.GcRule.Intersection(
                rules=[pb_rule3, pb_rule4]))

        gc_rule_pb = rule5.to_pb()
        self.assertEqual(gc_rule_pb, pb_rule5)


class TestColumnFamily(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import ColumnFamily
        return ColumnFamily

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        column_family_id = u'column-family-id'
        table = object()
        gc_rule = object()
        column_family = self._makeOne(column_family_id, table, gc_rule=gc_rule)

        self.assertEqual(column_family.column_family_id, column_family_id)
        self.assertTrue(column_family._table is table)
        self.assertTrue(column_family.gc_rule is gc_rule)

    def test_name_property(self):
        column_family_id = u'column-family-id'
        table_name = 'table_name'
        table = _Table(table_name)
        column_family = self._makeOne(column_family_id, table)

        expected_name = table_name + '/columnFamilies/' + column_family_id
        self.assertEqual(column_family.name, expected_name)

    def test___eq__(self):
        column_family_id = 'column_family_id'
        table = object()
        gc_rule = object()
        column_family1 = self._makeOne(column_family_id, table,
                                       gc_rule=gc_rule)
        column_family2 = self._makeOne(column_family_id, table,
                                       gc_rule=gc_rule)
        self.assertEqual(column_family1, column_family2)

    def test___eq__type_differ(self):
        column_family1 = self._makeOne('column_family_id', None)
        column_family2 = object()
        self.assertNotEqual(column_family1, column_family2)

    def test___ne__same_value(self):
        column_family_id = 'column_family_id'
        table = object()
        gc_rule = object()
        column_family1 = self._makeOne(column_family_id, table,
                                       gc_rule=gc_rule)
        column_family2 = self._makeOne(column_family_id, table,
                                       gc_rule=gc_rule)
        comparison_val = (column_family1 != column_family2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        column_family1 = self._makeOne('column_family_id1', None)
        column_family2 = self._makeOne('column_family_id2', None)
        self.assertNotEqual(column_family1, column_family2)

    def _create_test_helper(self, gc_rule=None):
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_table_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        project_id = 'project-id'
        zone = 'zone'
        cluster_id = 'cluster-id'
        table_id = 'table-id'
        column_family_id = 'column-family-id'
        timeout_seconds = 4
        table_name = ('projects/' + project_id + '/zones/' + zone +
                      '/clusters/' + cluster_id + '/tables/' + table_id)

        client = _Client(timeout_seconds=timeout_seconds)
        table = _Table(table_name, client=client)
        column_family = self._makeOne(column_family_id, table, gc_rule=gc_rule)

        # Create request_pb
        if gc_rule is None:
            column_family_pb = data_pb2.ColumnFamily()
        else:
            column_family_pb = data_pb2.ColumnFamily(gc_rule=gc_rule.to_pb())
        request_pb = messages_pb2.CreateColumnFamilyRequest(
            name=table_name,
            column_family_id=column_family_id,
            column_family=column_family_pb,
        )

        # Create response_pb
        response_pb = data_pb2.ColumnFamily()

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # create() has no return value.

        # Perform the method and check the result.
        self.assertEqual(stub.results, (response_pb,))
        result = column_family.create()
        self.assertEqual(stub.results, ())
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'CreateColumnFamily',
            (request_pb, timeout_seconds),
            {},
        )])

    def test_create(self):
        self._create_test_helper(gc_rule=None)

    def test_create_with_gc_rule(self):
        from gcloud.bigtable.column_family import MaxVersionsGCRule
        gc_rule = MaxVersionsGCRule(1337)
        self._create_test_helper(gc_rule=gc_rule)

    def _update_test_helper(self, gc_rule=None):
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        from gcloud.bigtable._testing import _FakeStub

        project_id = 'project-id'
        zone = 'zone'
        cluster_id = 'cluster-id'
        table_id = 'table-id'
        column_family_id = 'column-family-id'
        timeout_seconds = 28
        table_name = ('projects/' + project_id + '/zones/' + zone +
                      '/clusters/' + cluster_id + '/tables/' + table_id)
        column_family_name = table_name + '/columnFamilies/' + column_family_id

        client = _Client(timeout_seconds=timeout_seconds)
        table = _Table(table_name, client=client)
        column_family = self._makeOne(column_family_id, table, gc_rule=gc_rule)

        # Create request_pb
        if gc_rule is None:
            request_pb = data_pb2.ColumnFamily(name=column_family_name)
        else:
            request_pb = data_pb2.ColumnFamily(
                name=column_family_name,
                gc_rule=gc_rule.to_pb(),
            )

        # Create response_pb
        response_pb = data_pb2.ColumnFamily()

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # update() has no return value.

        # Perform the method and check the result.
        self.assertEqual(stub.results, (response_pb,))
        result = column_family.update()
        self.assertEqual(stub.results, ())
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'UpdateColumnFamily',
            (request_pb, timeout_seconds),
            {},
        )])

    def test_update(self):
        self._update_test_helper(gc_rule=None)

    def test_update_with_gc_rule(self):
        from gcloud.bigtable.column_family import MaxVersionsGCRule
        gc_rule = MaxVersionsGCRule(1337)
        self._update_test_helper(gc_rule=gc_rule)

    def test_delete(self):
        from google.protobuf import empty_pb2
        from gcloud.bigtable._generated import (
            bigtable_table_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        project_id = 'project-id'
        zone = 'zone'
        cluster_id = 'cluster-id'
        table_id = 'table-id'
        column_family_id = 'column-family-id'
        timeout_seconds = 7
        table_name = ('projects/' + project_id + '/zones/' + zone +
                      '/clusters/' + cluster_id + '/tables/' + table_id)
        column_family_name = table_name + '/columnFamilies/' + column_family_id

        client = _Client(timeout_seconds=timeout_seconds)
        table = _Table(table_name, client=client)
        column_family = self._makeOne(column_family_id, table)

        # Create request_pb
        request_pb = messages_pb2.DeleteColumnFamilyRequest(
            name=column_family_name)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        self.assertEqual(stub.results, (response_pb,))
        result = column_family.delete()
        self.assertEqual(stub.results, ())
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'DeleteColumnFamily',
            (request_pb, timeout_seconds),
            {},
        )])


class Test__gc_rule_from_pb(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.column_family import _gc_rule_from_pb
        return _gc_rule_from_pb(*args, **kwargs)

    def test_empty(self):
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)

        gc_rule_pb = data_pb2.GcRule()
        self.assertEqual(self._callFUT(gc_rule_pb), None)

    def test_max_num_versions(self):
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        orig_rule = MaxVersionsGCRule(1)
        gc_rule_pb = orig_rule.to_pb()
        result = self._callFUT(gc_rule_pb)
        self.assertTrue(isinstance(result, MaxVersionsGCRule))
        self.assertEqual(result, orig_rule)

    def test_max_age(self):
        import datetime
        from gcloud.bigtable.column_family import MaxAgeGCRule

        orig_rule = MaxAgeGCRule(datetime.timedelta(seconds=1))
        gc_rule_pb = orig_rule.to_pb()
        result = self._callFUT(gc_rule_pb)
        self.assertTrue(isinstance(result, MaxAgeGCRule))
        self.assertEqual(result, orig_rule)

    def test_union(self):
        import datetime
        from gcloud.bigtable.column_family import GCRuleUnion
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        rule1 = MaxVersionsGCRule(1)
        rule2 = MaxAgeGCRule(datetime.timedelta(seconds=1))
        orig_rule = GCRuleUnion([rule1, rule2])
        gc_rule_pb = orig_rule.to_pb()
        result = self._callFUT(gc_rule_pb)
        self.assertTrue(isinstance(result, GCRuleUnion))
        self.assertEqual(result, orig_rule)

    def test_intersection(self):
        import datetime
        from gcloud.bigtable.column_family import GCRuleIntersection
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        rule1 = MaxVersionsGCRule(1)
        rule2 = MaxAgeGCRule(datetime.timedelta(seconds=1))
        orig_rule = GCRuleIntersection([rule1, rule2])
        gc_rule_pb = orig_rule.to_pb()
        result = self._callFUT(gc_rule_pb)
        self.assertTrue(isinstance(result, GCRuleIntersection))
        self.assertEqual(result, orig_rule)

    def test_unknown_field_name(self):
        class MockProto(object):

            names = []

            @classmethod
            def WhichOneof(cls, name):
                cls.names.append(name)
                return 'unknown'

        self.assertEqual(MockProto.names, [])
        self.assertRaises(ValueError, self._callFUT, MockProto)
        self.assertEqual(MockProto.names, ['rule'])


class _Cluster(object):

    def __init__(self, client=None):
        self._client = client


class _Client(object):

    def __init__(self, timeout_seconds=None):
        self.timeout_seconds = timeout_seconds


class _Table(object):

    def __init__(self, name, client=None):
        self.name = name
        self._cluster = _Cluster(client)
