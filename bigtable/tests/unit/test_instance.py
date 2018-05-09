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


@mock.patch('google.auth.transport.grpc.secure_authorized_channel')
def _make_channel(secure_authorized_channel):
    from google.api_core import grpc_helpers
    target = 'example.com:443'

    channel = grpc_helpers.create_channel(
        target, credentials=mock.sentinel.credentials)

    return channel


class TestInstance(unittest.TestCase):

    PROJECT = 'project'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = 'projects/' + PROJECT + '/instances/' + INSTANCE_ID
    LOCATION_ID = 'locname'
    LOCATION = 'projects/' + PROJECT + '/locations/' + LOCATION_ID
    DISPLAY_NAME = 'display_name'
    OP_ID = 8915
    OP_NAME = ('operations/projects/%s/instances/%soperations/%d' %
               (PROJECT, INSTANCE_ID, OP_ID))
    TABLE_ID = 'table_id'
    TABLE_NAME = INSTANCE_NAME + '/tables/' + TABLE_ID

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.instance import Instance

        return Instance

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def test_constructor_defaults(self):

        client = object()
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertIs(instance._client, client)
        self.assertEqual(instance._cluster_location_id, self.LOCATION_ID)

    def test_constructor_non_default(self):
        display_name = 'display_name'
        client = object()

        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID,
                                  display_name=display_name)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, display_name)
        self.assertIs(instance._client, client)

    def test_table_factory(self):
        from google.cloud.bigtable.table import Table

        instance = self._make_one(self.INSTANCE_ID, None, self.LOCATION_ID)

        table = instance.table(self.TABLE_ID)
        self.assertIsInstance(table, Table)
        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertEqual(table._instance, instance)

    def test__update_from_pb_success(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        display_name = 'display_name'
        instance_pb = data_v2_pb2.Instance(
            display_name=display_name,
        )

        instance = self._make_one(None, None, None, None)
        self.assertIsNone(instance.display_name)
        instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, display_name)

    def test__update_from_pb_no_display_name(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        instance_pb = data_v2_pb2.Instance()
        instance = self._make_one(None, None, None, None)
        self.assertIsNone(instance.display_name)
        with self.assertRaises(ValueError):
            instance._update_from_pb(instance_pb)

    def test_from_pb_success(self):
        from google.cloud.bigtable.instance import (
            _EXISTING_INSTANCE_LOCATION_ID)
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        client = _Client(project=self.PROJECT)

        instance_pb = data_v2_pb2.Instance(
            name=self.INSTANCE_NAME,
            display_name=self.INSTANCE_ID,
        )

        klass = self._get_target_class()
        instance = klass.from_pb(instance_pb, client)
        self.assertIsInstance(instance, klass)
        self.assertEqual(instance._client, client)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance._cluster_location_id,
                         _EXISTING_INSTANCE_LOCATION_ID)

    def test_from_pb_bad_instance_name(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        instance_name = 'INCORRECT_FORMAT'
        instance_pb = data_v2_pb2.Instance(name=instance_name)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, None)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        ALT_PROJECT = 'ALT_PROJECT'
        client = _Client(project=ALT_PROJECT)

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)

        instance_pb = data_v2_pb2.Instance(name=self.INSTANCE_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, client)

    def test_name_property(self):
        channel = _make_channel()
        client = self._make_client(project=self.PROJECT, channel=channel,
                                   admin=True)

        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)
        self.assertEqual(instance.name, self.INSTANCE_NAME)

    def test___eq__(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)
        instance2 = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)
        self.assertEqual(instance1, instance2)

    def test___eq__type_differ(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)
        instance2 = object()
        self.assertNotEqual(instance1, instance2)

    def test___ne__same_value(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)
        instance2 = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)
        comparison_val = (instance1 != instance2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        instance1 = self._make_one('instance_id1', 'client1', self.LOCATION_ID)
        instance2 = self._make_one('instance_id2', 'client2', self.LOCATION_ID)
        self.assertNotEqual(instance1, instance2)

    def test_create(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from tests.unit._testing import _FakeStub

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)
        channel = _make_channel()
        client = self._make_client(project=self.PROJECT, channel=channel,
                                   admin=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID,
                                  display_name=self.DISPLAY_NAME)

        # Create response_pb
        metadata = messages_v2_pb2.CreateInstanceMetadata(request_time=NOW_PB)
        type_url = 'type.googleapis.com/%s' % (
            messages_v2_pb2.CreateInstanceMetadata.DESCRIPTOR.full_name,)
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(
                type_url=type_url,
                value=metadata.SerializeToString(),
            )
        )

        # Patch the stub used by the API method.
        stub = _FakeStub(response_pb)
        client._instance_admin_client.bigtable_instance_admin_stub = stub

        # Perform the method and check the result.
        result = instance.create()

        self.assertIsInstance(result, operation.Operation)
        # self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.CreateInstanceMetadata)

    def test_create_w_explicit_serve_nodes(self):
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from tests.unit._testing import _FakeStub

        channel = _make_channel()
        client = self._make_client(project=self.PROJECT, channel=channel,
                                   admin=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)

        # Create response_pb
        response_pb = operations_pb2.Operation(name=self.OP_NAME)

        # Patch the stub used by the API method.
        stub = _FakeStub(response_pb)
        client._instance_admin_client.bigtable_instance_admin_stub = stub

        # Perform the method and check the result.
        result = instance.create()

        self.assertIsInstance(result, operation.Operation)

    def test_update(self):
        channel = _make_channel()
        client = self._make_client(project=self.PROJECT, channel=channel,
                                   admin=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID,
                                  display_name=self.DISPLAY_NAME)

        # Create expected_result.
        expected_result = None

        # Perform the method and check the result.
        result = instance.update()

        self.assertEqual(result, expected_result)

    def test_delete(self):
        channel = _make_channel()
        client = self._make_client(project=self.PROJECT, channel=channel,
                                   admin=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = instance.delete()

        self.assertEqual(result, expected_result)

    def _list_tables_helper(self, table_name=None):
        from google.cloud.bigtable_admin_v2.proto import (
            table_pb2 as table_data_v2_pb2)
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_table_admin_pb2 as table_messages_v1_pb2)

        channel = _make_channel()
        client = self._make_client(project=self.PROJECT, channel=channel,
                                   admin=True)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)

        # Create response_pb
        if table_name is None:
            table_name = self.TABLE_NAME

        response_pb = table_messages_v1_pb2.ListTablesResponse(
            tables=[
                table_data_v2_pb2.Table(name=table_name),
            ],
        )

        # Patch the stub used by the API method.
        bigtable_table_stub = (
            client._table_admin_client.bigtable_table_admin_stub)
        bigtable_table_stub.ListTables.side_effect = [response_pb]

        # Create expected_result.
        expected_table = instance.table(self.TABLE_ID)
        expected_result = [expected_table]

        # Perform the method and check the result.
        result = instance.list_tables()

        self.assertEqual(result, expected_result)

    def test_list_tables(self):
        self._list_tables_helper()

    def test_list_tables_failure_bad_split(self):
        with self.assertRaises(ValueError):
            self._list_tables_helper(table_name='wrong-format')

    def test_list_tables_failure_name_bad_before(self):
        BAD_TABLE_NAME = ('nonempty-section-before' +
                          'projects/' + self.PROJECT +
                          '/instances/' + self.INSTANCE_ID +
                          '/tables/' + self.TABLE_ID)
        with self.assertRaises(ValueError):
            self._list_tables_helper(table_name=BAD_TABLE_NAME)


class _Client(object):

    def __init__(self, project):
        self.project = project
        self.project_name = 'projects/' + self.project
        self._operations_stub = mock.sentinel.operations_stub

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name)
