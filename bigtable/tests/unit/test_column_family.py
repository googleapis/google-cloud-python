# Copyright 2015 Google LLC
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

import unittest

import mock

from ._testing import _make_credentials


class TestMaxVersionsGCRule(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        return MaxVersionsGCRule

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test___eq__type_differ(self):
        gc_rule1 = self._make_one(10)
        self.assertNotEqual(gc_rule1, object())
        self.assertEqual(gc_rule1, mock.ANY)

    def test___eq__same_value(self):
        gc_rule1 = self._make_one(2)
        gc_rule2 = self._make_one(2)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        gc_rule1 = self._make_one(99)
        gc_rule2 = self._make_one(99)
        comparison_val = gc_rule1 != gc_rule2
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        max_num_versions = 1337
        gc_rule = self._make_one(max_num_versions=max_num_versions)
        pb_val = gc_rule.to_pb()
        expected = _GcRulePB(max_num_versions=max_num_versions)
        self.assertEqual(pb_val, expected)


class TestMaxAgeGCRule(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.column_family import MaxAgeGCRule

        return MaxAgeGCRule

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test___eq__type_differ(self):
        max_age = object()
        gc_rule1 = self._make_one(max_age=max_age)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___eq__same_value(self):
        max_age = object()
        gc_rule1 = self._make_one(max_age=max_age)
        gc_rule2 = self._make_one(max_age=max_age)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        max_age = object()
        gc_rule1 = self._make_one(max_age=max_age)
        gc_rule2 = self._make_one(max_age=max_age)
        comparison_val = gc_rule1 != gc_rule2
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        import datetime
        from google.protobuf import duration_pb2

        max_age = datetime.timedelta(seconds=1)
        duration = duration_pb2.Duration(seconds=1)
        gc_rule = self._make_one(max_age=max_age)
        pb_val = gc_rule.to_pb()
        self.assertEqual(pb_val, _GcRulePB(max_age=duration))


class TestGCRuleUnion(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.column_family import GCRuleUnion

        return GCRuleUnion

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        rules = object()
        rule_union = self._make_one(rules)
        self.assertIs(rule_union.rules, rules)

    def test___eq__(self):
        rules = object()
        gc_rule1 = self._make_one(rules)
        gc_rule2 = self._make_one(rules)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___eq__type_differ(self):
        rules = object()
        gc_rule1 = self._make_one(rules)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        rules = object()
        gc_rule1 = self._make_one(rules)
        gc_rule2 = self._make_one(rules)
        comparison_val = gc_rule1 != gc_rule2
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        import datetime
        from google.protobuf import duration_pb2
        from google.cloud.bigtable.column_family import MaxAgeGCRule
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        max_num_versions = 42
        rule1 = MaxVersionsGCRule(max_num_versions)
        pb_rule1 = _GcRulePB(max_num_versions=max_num_versions)

        max_age = datetime.timedelta(seconds=1)
        rule2 = MaxAgeGCRule(max_age)
        pb_rule2 = _GcRulePB(max_age=duration_pb2.Duration(seconds=1))

        rule3 = self._make_one(rules=[rule1, rule2])
        pb_rule3 = _GcRulePB(union=_GcRuleUnionPB(rules=[pb_rule1, pb_rule2]))

        gc_rule_pb = rule3.to_pb()
        self.assertEqual(gc_rule_pb, pb_rule3)

    def test_to_pb_nested(self):
        import datetime
        from google.protobuf import duration_pb2
        from google.cloud.bigtable.column_family import MaxAgeGCRule
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        max_num_versions1 = 42
        rule1 = MaxVersionsGCRule(max_num_versions1)
        pb_rule1 = _GcRulePB(max_num_versions=max_num_versions1)

        max_age = datetime.timedelta(seconds=1)
        rule2 = MaxAgeGCRule(max_age)
        pb_rule2 = _GcRulePB(max_age=duration_pb2.Duration(seconds=1))

        rule3 = self._make_one(rules=[rule1, rule2])
        pb_rule3 = _GcRulePB(union=_GcRuleUnionPB(rules=[pb_rule1, pb_rule2]))

        max_num_versions2 = 1337
        rule4 = MaxVersionsGCRule(max_num_versions2)
        pb_rule4 = _GcRulePB(max_num_versions=max_num_versions2)

        rule5 = self._make_one(rules=[rule3, rule4])
        pb_rule5 = _GcRulePB(union=_GcRuleUnionPB(rules=[pb_rule3, pb_rule4]))

        gc_rule_pb = rule5.to_pb()
        self.assertEqual(gc_rule_pb, pb_rule5)


class TestGCRuleIntersection(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.column_family import GCRuleIntersection

        return GCRuleIntersection

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        rules = object()
        rule_intersection = self._make_one(rules)
        self.assertIs(rule_intersection.rules, rules)

    def test___eq__(self):
        rules = object()
        gc_rule1 = self._make_one(rules)
        gc_rule2 = self._make_one(rules)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___eq__type_differ(self):
        rules = object()
        gc_rule1 = self._make_one(rules)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        rules = object()
        gc_rule1 = self._make_one(rules)
        gc_rule2 = self._make_one(rules)
        comparison_val = gc_rule1 != gc_rule2
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        import datetime
        from google.protobuf import duration_pb2
        from google.cloud.bigtable.column_family import MaxAgeGCRule
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        max_num_versions = 42
        rule1 = MaxVersionsGCRule(max_num_versions)
        pb_rule1 = _GcRulePB(max_num_versions=max_num_versions)

        max_age = datetime.timedelta(seconds=1)
        rule2 = MaxAgeGCRule(max_age)
        pb_rule2 = _GcRulePB(max_age=duration_pb2.Duration(seconds=1))

        rule3 = self._make_one(rules=[rule1, rule2])
        pb_rule3 = _GcRulePB(
            intersection=_GcRuleIntersectionPB(rules=[pb_rule1, pb_rule2])
        )

        gc_rule_pb = rule3.to_pb()
        self.assertEqual(gc_rule_pb, pb_rule3)

    def test_to_pb_nested(self):
        import datetime
        from google.protobuf import duration_pb2
        from google.cloud.bigtable.column_family import MaxAgeGCRule
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        max_num_versions1 = 42
        rule1 = MaxVersionsGCRule(max_num_versions1)
        pb_rule1 = _GcRulePB(max_num_versions=max_num_versions1)

        max_age = datetime.timedelta(seconds=1)
        rule2 = MaxAgeGCRule(max_age)
        pb_rule2 = _GcRulePB(max_age=duration_pb2.Duration(seconds=1))

        rule3 = self._make_one(rules=[rule1, rule2])
        pb_rule3 = _GcRulePB(
            intersection=_GcRuleIntersectionPB(rules=[pb_rule1, pb_rule2])
        )

        max_num_versions2 = 1337
        rule4 = MaxVersionsGCRule(max_num_versions2)
        pb_rule4 = _GcRulePB(max_num_versions=max_num_versions2)

        rule5 = self._make_one(rules=[rule3, rule4])
        pb_rule5 = _GcRulePB(
            intersection=_GcRuleIntersectionPB(rules=[pb_rule3, pb_rule4])
        )

        gc_rule_pb = rule5.to_pb()
        self.assertEqual(gc_rule_pb, pb_rule5)


class TestColumnFamily(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.column_family import ColumnFamily

        return ColumnFamily

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def test_constructor(self):
        column_family_id = u"column-family-id"
        table = object()
        gc_rule = object()
        column_family = self._make_one(column_family_id, table, gc_rule=gc_rule)

        self.assertEqual(column_family.column_family_id, column_family_id)
        self.assertIs(column_family._table, table)
        self.assertIs(column_family.gc_rule, gc_rule)

    def test_name_property(self):
        column_family_id = u"column-family-id"
        table_name = "table_name"
        table = _Table(table_name)
        column_family = self._make_one(column_family_id, table)

        expected_name = table_name + "/columnFamilies/" + column_family_id
        self.assertEqual(column_family.name, expected_name)

    def test___eq__(self):
        column_family_id = "column_family_id"
        table = object()
        gc_rule = object()
        column_family1 = self._make_one(column_family_id, table, gc_rule=gc_rule)
        column_family2 = self._make_one(column_family_id, table, gc_rule=gc_rule)
        self.assertEqual(column_family1, column_family2)

    def test___eq__type_differ(self):
        column_family1 = self._make_one("column_family_id", None)
        column_family2 = object()
        self.assertNotEqual(column_family1, column_family2)

    def test___ne__same_value(self):
        column_family_id = "column_family_id"
        table = object()
        gc_rule = object()
        column_family1 = self._make_one(column_family_id, table, gc_rule=gc_rule)
        column_family2 = self._make_one(column_family_id, table, gc_rule=gc_rule)
        comparison_val = column_family1 != column_family2
        self.assertFalse(comparison_val)

    def test___ne__(self):
        column_family1 = self._make_one("column_family_id1", None)
        column_family2 = self._make_one("column_family_id2", None)
        self.assertNotEqual(column_family1, column_family2)

    def test_to_pb_no_rules(self):
        column_family = self._make_one("column_family_id", None)
        pb_val = column_family.to_pb()
        expected = _ColumnFamilyPB()
        self.assertEqual(pb_val, expected)

    def test_to_pb_with_rule(self):
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        gc_rule = MaxVersionsGCRule(1)
        column_family = self._make_one("column_family_id", None, gc_rule=gc_rule)
        pb_val = column_family.to_pb()
        expected = _ColumnFamilyPB(gc_rule=gc_rule.to_pb())
        self.assertEqual(pb_val, expected)

    def _create_test_helper(self, gc_rule=None):
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_table_admin_pb2 as table_admin_v2_pb2,
        )
        from tests.unit._testing import _FakeStub
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        project_id = "project-id"
        zone = "zone"
        cluster_id = "cluster-id"
        table_id = "table-id"
        column_family_id = "column-family-id"
        table_name = (
            "projects/"
            + project_id
            + "/zones/"
            + zone
            + "/clusters/"
            + cluster_id
            + "/tables/"
            + table_id
        )

        api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=project_id, credentials=credentials, admin=True
        )
        table = _Table(table_name, client=client)
        column_family = self._make_one(column_family_id, table, gc_rule=gc_rule)

        # Create request_pb
        if gc_rule is None:
            column_family_pb = _ColumnFamilyPB()
        else:
            column_family_pb = _ColumnFamilyPB(gc_rule=gc_rule.to_pb())
        request_pb = table_admin_v2_pb2.ModifyColumnFamiliesRequest(name=table_name)
        request_pb.modifications.add(id=column_family_id, create=column_family_pb)

        # Create response_pb
        response_pb = _ColumnFamilyPB()

        # Patch the stub used by the API method.
        stub = _FakeStub(response_pb)
        client._table_admin_client = api
        client._table_admin_client.transport.create = stub

        # Create expected_result.
        expected_result = None  # create() has no return value.

        # Perform the method and check the result.
        self.assertEqual(stub.results, (response_pb,))
        result = column_family.create()
        self.assertEqual(result, expected_result)

    def test_create(self):
        self._create_test_helper(gc_rule=None)

    def test_create_with_gc_rule(self):
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        gc_rule = MaxVersionsGCRule(1337)
        self._create_test_helper(gc_rule=gc_rule)

    def _update_test_helper(self, gc_rule=None):
        from tests.unit._testing import _FakeStub
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_table_admin_pb2 as table_admin_v2_pb2,
        )
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        project_id = "project-id"
        zone = "zone"
        cluster_id = "cluster-id"
        table_id = "table-id"
        column_family_id = "column-family-id"
        table_name = (
            "projects/"
            + project_id
            + "/zones/"
            + zone
            + "/clusters/"
            + cluster_id
            + "/tables/"
            + table_id
        )

        api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=project_id, credentials=credentials, admin=True
        )
        table = _Table(table_name, client=client)
        column_family = self._make_one(column_family_id, table, gc_rule=gc_rule)

        # Create request_pb
        if gc_rule is None:
            column_family_pb = _ColumnFamilyPB()
        else:
            column_family_pb = _ColumnFamilyPB(gc_rule=gc_rule.to_pb())
        request_pb = table_admin_v2_pb2.ModifyColumnFamiliesRequest(name=table_name)
        request_pb.modifications.add(id=column_family_id, update=column_family_pb)

        # Create response_pb
        response_pb = _ColumnFamilyPB()

        # Patch the stub used by the API method.
        stub = _FakeStub(response_pb)
        client._table_admin_client = api
        client._table_admin_client.transport.update = stub

        # Create expected_result.
        expected_result = None  # update() has no return value.

        # Perform the method and check the result.
        self.assertEqual(stub.results, (response_pb,))
        result = column_family.update()
        self.assertEqual(result, expected_result)

    def test_update(self):
        self._update_test_helper(gc_rule=None)

    def test_update_with_gc_rule(self):
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        gc_rule = MaxVersionsGCRule(1337)
        self._update_test_helper(gc_rule=gc_rule)

    def test_delete(self):
        from google.protobuf import empty_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_table_admin_pb2 as table_admin_v2_pb2,
        )
        from tests.unit._testing import _FakeStub
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        project_id = "project-id"
        zone = "zone"
        cluster_id = "cluster-id"
        table_id = "table-id"
        column_family_id = "column-family-id"
        table_name = (
            "projects/"
            + project_id
            + "/zones/"
            + zone
            + "/clusters/"
            + cluster_id
            + "/tables/"
            + table_id
        )

        api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=project_id, credentials=credentials, admin=True
        )
        table = _Table(table_name, client=client)
        column_family = self._make_one(column_family_id, table)

        # Create request_pb
        request_pb = table_admin_v2_pb2.ModifyColumnFamiliesRequest(name=table_name)
        request_pb.modifications.add(id=column_family_id, drop=True)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        stub = _FakeStub(response_pb)
        client._table_admin_client = api
        client._table_admin_client.transport.delete = stub

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        self.assertEqual(stub.results, (response_pb,))
        result = column_family.delete()
        self.assertEqual(result, expected_result)


class Test__gc_rule_from_pb(unittest.TestCase):
    def _call_fut(self, *args, **kwargs):
        from google.cloud.bigtable.column_family import _gc_rule_from_pb

        return _gc_rule_from_pb(*args, **kwargs)

    def test_empty(self):

        gc_rule_pb = _GcRulePB()
        self.assertIsNone(self._call_fut(gc_rule_pb))

    def test_max_num_versions(self):
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        orig_rule = MaxVersionsGCRule(1)
        gc_rule_pb = orig_rule.to_pb()
        result = self._call_fut(gc_rule_pb)
        self.assertIsInstance(result, MaxVersionsGCRule)
        self.assertEqual(result, orig_rule)

    def test_max_age(self):
        import datetime
        from google.cloud.bigtable.column_family import MaxAgeGCRule

        orig_rule = MaxAgeGCRule(datetime.timedelta(seconds=1))
        gc_rule_pb = orig_rule.to_pb()
        result = self._call_fut(gc_rule_pb)
        self.assertIsInstance(result, MaxAgeGCRule)
        self.assertEqual(result, orig_rule)

    def test_union(self):
        import datetime
        from google.cloud.bigtable.column_family import GCRuleUnion
        from google.cloud.bigtable.column_family import MaxAgeGCRule
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        rule1 = MaxVersionsGCRule(1)
        rule2 = MaxAgeGCRule(datetime.timedelta(seconds=1))
        orig_rule = GCRuleUnion([rule1, rule2])
        gc_rule_pb = orig_rule.to_pb()
        result = self._call_fut(gc_rule_pb)
        self.assertIsInstance(result, GCRuleUnion)
        self.assertEqual(result, orig_rule)

    def test_intersection(self):
        import datetime
        from google.cloud.bigtable.column_family import GCRuleIntersection
        from google.cloud.bigtable.column_family import MaxAgeGCRule
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        rule1 = MaxVersionsGCRule(1)
        rule2 = MaxAgeGCRule(datetime.timedelta(seconds=1))
        orig_rule = GCRuleIntersection([rule1, rule2])
        gc_rule_pb = orig_rule.to_pb()
        result = self._call_fut(gc_rule_pb)
        self.assertIsInstance(result, GCRuleIntersection)
        self.assertEqual(result, orig_rule)

    def test_unknown_field_name(self):
        class MockProto(object):

            names = []

            @classmethod
            def WhichOneof(cls, name):
                cls.names.append(name)
                return "unknown"

        self.assertEqual(MockProto.names, [])
        self.assertRaises(ValueError, self._call_fut, MockProto)
        self.assertEqual(MockProto.names, ["rule"])


def _GcRulePB(*args, **kw):
    from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_v2_pb2

    return table_v2_pb2.GcRule(*args, **kw)


def _GcRuleIntersectionPB(*args, **kw):
    from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_v2_pb2

    return table_v2_pb2.GcRule.Intersection(*args, **kw)


def _GcRuleUnionPB(*args, **kw):
    from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_v2_pb2

    return table_v2_pb2.GcRule.Union(*args, **kw)


def _ColumnFamilyPB(*args, **kw):
    from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_v2_pb2

    return table_v2_pb2.ColumnFamily(*args, **kw)


class _Instance(object):
    def __init__(self, client=None):
        self._client = client


class _Client(object):
    pass


class _Table(object):
    def __init__(self, name, client=None):
        self.name = name
        self._instance = _Instance(client)
