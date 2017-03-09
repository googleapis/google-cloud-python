# Copyright 2015 Google Inc.
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

    def test_constructor_defaults(self):
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES

        client = object()
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertIs(instance._client, client)
        self.assertEqual(instance._cluster_location_id, self.LOCATION_ID)
        self.assertEqual(instance._cluster_serve_nodes, DEFAULT_SERVE_NODES)

    def test_constructor_non_default(self):
        display_name = 'display_name'
        client = object()

        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID,
                                  display_name=display_name)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, display_name)
        self.assertIs(instance._client, client)

    def test_copy(self):
        display_name = 'display_name'

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID,
                                  display_name=display_name)
        new_instance = instance.copy()

        # Make sure the client copy succeeded.
        self.assertIsNot(new_instance._client, client)
        self.assertEqual(new_instance._client, client)
        # Make sure the client got copied to a new instance.
        self.assertIsNot(instance, new_instance)
        self.assertEqual(instance, new_instance)

    def test_table_factory(self):
        from google.cloud.bigtable.table import Table

        instance = self._make_one(self.INSTANCE_ID, None, self.LOCATION_ID)

        table = instance.table(self.TABLE_ID)
        self.assertIsInstance(table, Table)
        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertEqual(table._instance, instance)

    def test__update_from_pb_success(self):
        from google.cloud.bigtable._generated import (
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
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)

        instance_pb = data_v2_pb2.Instance()
        instance = self._make_one(None, None, None, None)
        self.assertIsNone(instance.display_name)
        with self.assertRaises(ValueError):
            instance._update_from_pb(instance_pb)
        self.assertIsNone(instance.display_name)

    def test_from_pb_success(self):
        from google.cloud.bigtable.instance import (
            _EXISTING_INSTANCE_LOCATION_ID)
        from google.cloud.bigtable._generated import (
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
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)

        instance_name = 'INCORRECT_FORMAT'
        instance_pb = data_v2_pb2.Instance(name=instance_name)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, None)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)

        ALT_PROJECT = 'ALT_PROJECT'
        client = _Client(project=ALT_PROJECT)

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)

        instance_pb = data_v2_pb2.Instance(name=self.INSTANCE_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, client)

    def test_name_property(self):
        client = _Client(project=self.PROJECT)

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

    def test_reload(self):
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from tests.unit._testing import _FakeStub

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)

        # Create request_pb
        request_pb = messages_v2_pb.GetInstanceRequest(
            name=self.INSTANCE_NAME)

        # Create response_pb
        DISPLAY_NAME = u'hey-hi-hello'
        response_pb = data_v2_pb2.Instance(
            display_name=DISPLAY_NAME,
        )

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check Instance optional config values before.
        self.assertEqual(instance.display_name, self.INSTANCE_ID)

        # Perform the method and check the result.
        result = instance.reload()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'GetInstance',
            (request_pb,),
            {},
        )])

        # Check Instance optional config values before.
        self.assertEqual(instance.display_name, DISPLAY_NAME)

    def test_create(self):
        import datetime
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from tests.unit._testing import _FakeStub
        from google.cloud.operation import Operation
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)
        client = _Client(self.PROJECT)
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
        client._instance_stub = stub = _FakeStub(response_pb)

        # Perform the method and check the result.
        result = instance.create()

        self.assertIsInstance(result, Operation)
        self.assertEqual(result.name, self.OP_NAME)
        self.assertIs(result.target, instance)
        self.assertIs(result.client, client)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.CreateInstanceMetadata)
        self.assertEqual(result.metadata.request_time, NOW_PB)
        self.assertEqual(result.caller_metadata,
                         {'request_type': 'CreateInstance'})

        self.assertEqual(len(stub.method_calls), 1)
        api_name, args, kwargs = stub.method_calls[0]
        self.assertEqual(api_name, 'CreateInstance')
        request_pb, = args
        self.assertIsInstance(request_pb,
                              messages_v2_pb2.CreateInstanceRequest)
        self.assertEqual(request_pb.parent, 'projects/%s' % (self.PROJECT,))
        self.assertEqual(request_pb.instance_id, self.INSTANCE_ID)
        self.assertEqual(request_pb.instance.display_name, self.DISPLAY_NAME)
        cluster = request_pb.clusters[self.INSTANCE_ID]
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)
        self.assertEqual(kwargs, {})

    def test_create_w_explicit_serve_nodes(self):
        from google.longrunning import operations_pb2
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from tests.unit._testing import _FakeStub
        from google.cloud.operation import Operation

        SERVE_NODES = 5

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID,
                                  serve_nodes=SERVE_NODES)

        # Create response_pb
        response_pb = operations_pb2.Operation(name=self.OP_NAME)

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Perform the method and check the result.
        result = instance.create()

        self.assertIsInstance(result, Operation)
        self.assertEqual(result.name, self.OP_NAME)
        self.assertIs(result.target, instance)
        self.assertIs(result.client, client)

        self.assertEqual(len(stub.method_calls), 1)
        api_name, args, kwargs = stub.method_calls[0]
        self.assertEqual(api_name, 'CreateInstance')
        request_pb, = args
        self.assertIsInstance(request_pb,
                              messages_v2_pb2.CreateInstanceRequest)
        self.assertEqual(request_pb.parent, 'projects/%s' % (self.PROJECT,))
        self.assertEqual(request_pb.instance_id, self.INSTANCE_ID)
        self.assertEqual(request_pb.instance.display_name, self.INSTANCE_ID)
        cluster = request_pb.clusters[self.INSTANCE_ID]
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)
        self.assertEqual(kwargs, {})

    def test_update(self):
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)
        from tests.unit._testing import _FakeStub

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID,
                                  display_name=self.DISPLAY_NAME)

        # Create request_pb
        request_pb = data_v2_pb2.Instance(
            name=self.INSTANCE_NAME,
            display_name=self.DISPLAY_NAME,
        )

        # Create response_pb
        response_pb = data_v2_pb2.Instance()

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None

        # Perform the method and check the result.
        result = instance.update()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'UpdateInstance',
            (request_pb,),
            {},
        )])

    def test_delete(self):
        from google.protobuf import empty_pb2
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from tests.unit._testing import _FakeStub

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)

        # Create request_pb
        request_pb = messages_v2_pb.DeleteInstanceRequest(
            name=self.INSTANCE_NAME)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = instance.delete()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'DeleteInstance',
            (request_pb,),
            {},
        )])

    def test_list_clusters(self):
        from google.cloud.bigtable._generated import (
            instance_pb2 as instance_v2_pb2)
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from tests.unit._testing import _FakeStub

        FAILED_LOCATION = 'FAILED'
        FAILED_LOCATIONS = [FAILED_LOCATION]
        CLUSTER_ID1 = 'cluster-id1'
        CLUSTER_ID2 = 'cluster-id2'
        SERVE_NODES = 4

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)

        CLUSTER_NAME1 = (instance.name + '/clusters/' + CLUSTER_ID1)
        CLUSTER_NAME2 = (instance.name + '/clusters/' + CLUSTER_ID2)
        # Create request_pb
        request_pb = messages_v2_pb2.ListClustersRequest(
            parent=instance.name,
        )

        # Create response_pb
        response_pb = messages_v2_pb2.ListClustersResponse(
            failed_locations=[FAILED_LOCATION],
            clusters=[
                instance_v2_pb2.Cluster(
                    name=CLUSTER_NAME1,
                    serve_nodes=SERVE_NODES,
                ),
                instance_v2_pb2.Cluster(
                    name=CLUSTER_NAME2,
                    serve_nodes=SERVE_NODES,
                ),
            ],
        )

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        clusters = [
            instance.cluster(CLUSTER_ID1),
            instance.cluster(CLUSTER_ID2),
        ]
        expected_result = (clusters, FAILED_LOCATIONS)

        # Perform the method and check the result.
        result = instance.list_clusters()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ListClusters',
            (request_pb,),
            {},
        )])

    def _list_tables_helper(self, table_name=None):
        from google.cloud.bigtable._generated import (
            table_pb2 as table_data_v2_pb2)
        from google.cloud.bigtable._generated import (
            bigtable_table_admin_pb2 as table_messages_v1_pb2)
        from tests.unit._testing import _FakeStub

        client = _Client(self.PROJECT)
        instance = self._make_one(self.INSTANCE_ID, client, self.LOCATION_ID)

        # Create request_
        request_pb = table_messages_v1_pb2.ListTablesRequest(
            parent=self.INSTANCE_NAME)

        # Create response_pb
        if table_name is None:
            table_name = self.TABLE_NAME

        response_pb = table_messages_v1_pb2.ListTablesResponse(
            tables=[
                table_data_v2_pb2.Table(name=table_name),
            ],
        )

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_table = instance.table(self.TABLE_ID)
        expected_result = [expected_table]

        # Perform the method and check the result.
        result = instance.list_tables()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ListTables',
            (request_pb,),
            {},
        )])

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


class Test__prepare_create_request(unittest.TestCase):
    PROJECT = 'PROJECT'
    PARENT = 'projects/' + PROJECT
    LOCATION_ID = 'locname'
    LOCATION_NAME = 'projects/' + PROJECT + '/locations/' + LOCATION_ID
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = PARENT + '/instances/' + INSTANCE_ID
    CLUSTER_NAME = INSTANCE_NAME + '/clusters/' + INSTANCE_ID

    def _call_fut(self, instance, **kw):
        from google.cloud.bigtable.instance import _prepare_create_request

        return _prepare_create_request(instance, **kw)

    def test_w_defaults(self):
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from google.cloud.bigtable.instance import Instance

        client = _Client(self.PROJECT)

        instance = Instance(self.INSTANCE_ID, client, self.LOCATION_ID)
        request_pb = self._call_fut(instance)
        self.assertIsInstance(request_pb,
                              messages_v2_pb.CreateInstanceRequest)
        self.assertEqual(request_pb.instance_id, self.INSTANCE_ID)
        self.assertEqual(request_pb.parent, self.PARENT)
        self.assertIsInstance(request_pb.instance, data_v2_pb2.Instance)
        self.assertEqual(request_pb.instance.name, u'')
        self.assertEqual(request_pb.instance.display_name, self.INSTANCE_ID)

        # An instance must also define a same-named cluster
        cluster = request_pb.clusters[self.INSTANCE_ID]
        self.assertIsInstance(cluster, data_v2_pb2.Cluster)
        self.assertEqual(cluster.name, self.CLUSTER_NAME)
        self.assertEqual(cluster.location, self.LOCATION_NAME)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

    def test_w_explicit_serve_nodes(self):
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from google.cloud.bigtable.instance import Instance

        DISPLAY_NAME = u'DISPLAY_NAME'
        SERVE_NODES = 5
        client = _Client(self.PROJECT)
        instance = Instance(self.INSTANCE_ID, client, self.LOCATION_ID,
                            display_name=DISPLAY_NAME,
                            serve_nodes=SERVE_NODES)

        request_pb = self._call_fut(instance)

        self.assertIsInstance(request_pb,
                              messages_v2_pb.CreateInstanceRequest)
        self.assertEqual(request_pb.instance_id, self.INSTANCE_ID)
        self.assertEqual(request_pb.parent,
                         'projects/' + self.PROJECT)
        self.assertIsInstance(request_pb.instance, data_v2_pb2.Instance)
        self.assertEqual(request_pb.instance.display_name, DISPLAY_NAME)
        # An instance must also define a same-named cluster
        cluster = request_pb.clusters[self.INSTANCE_ID]
        self.assertIsInstance(cluster, data_v2_pb2.Cluster)
        self.assertEqual(cluster.location, self.LOCATION_NAME)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)


class _Client(object):

    def __init__(self, project):
        self.project = project
        self.project_name = 'projects/' + self.project

    def copy(self):
        from copy import deepcopy

        return deepcopy(self)

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name)
