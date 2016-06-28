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


import datetime
import unittest2


class TestOperation(unittest2.TestCase):

    OP_TYPE = 'fake-op'
    OP_ID = 8915
    BEGIN = datetime.datetime(2015, 10, 22, 1, 1)
    LOCATION_ID = 'loc-id'

    def _getTargetClass(self):
        from gcloud.bigtable.instance import Operation
        return Operation

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _constructor_test_helper(self, instance=None):
        operation = self._makeOne(
            self.OP_TYPE, self.OP_ID, self.BEGIN, self.LOCATION_ID,
            instance=instance)

        self.assertEqual(operation.op_type, self.OP_TYPE)
        self.assertEqual(operation.op_id, self.OP_ID)
        self.assertEqual(operation.begin, self.BEGIN)
        self.assertEqual(operation.location_id, self.LOCATION_ID)
        self.assertEqual(operation._instance, instance)
        self.assertFalse(operation._complete)

    def test_constructor_defaults(self):
        self._constructor_test_helper()

    def test_constructor_explicit_instance(self):
        instance = object()
        self._constructor_test_helper(instance=instance)

    def test___eq__(self):
        instance = object()
        operation1 = self._makeOne(
            self.OP_TYPE, self.OP_ID, self.BEGIN, self.LOCATION_ID,
            instance=instance)
        operation2 = self._makeOne(
            self.OP_TYPE, self.OP_ID, self.BEGIN, self.LOCATION_ID,
            instance=instance)
        self.assertEqual(operation1, operation2)

    def test___eq__type_differ(self):
        operation1 = self._makeOne('foo', 123, None, self.LOCATION_ID)
        operation2 = object()
        self.assertNotEqual(operation1, operation2)

    def test___ne__same_value(self):
        instance = object()
        operation1 = self._makeOne(
            self.OP_TYPE, self.OP_ID, self.BEGIN, self.LOCATION_ID,
            instance=instance)
        operation2 = self._makeOne(
            self.OP_TYPE, self.OP_ID, self.BEGIN, self.LOCATION_ID,
            instance=instance)
        comparison_val = (operation1 != operation2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        operation1 = self._makeOne('foo', 123, None, self.LOCATION_ID)
        operation2 = self._makeOne('bar', 456, None, self.LOCATION_ID)
        self.assertNotEqual(operation1, operation2)

    def test_finished_without_operation(self):
        operation = self._makeOne(None, None, None, None)
        operation._complete = True
        with self.assertRaises(ValueError):
            operation.finished()

    def _finished_helper(self, done):
        from google.longrunning import operations_pb2
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable.instance import Instance

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        TIMEOUT_SECONDS = 1

        client = _Client(PROJECT, timeout_seconds=TIMEOUT_SECONDS)
        instance = Instance(INSTANCE_ID, client, self.LOCATION_ID)
        operation = self._makeOne(
            self.OP_TYPE, self.OP_ID, self.BEGIN, self.LOCATION_ID,
            instance=instance)

        # Create request_pb
        op_name = ('operations/projects/' + PROJECT +
                   '/instances/' + INSTANCE_ID +
                   '/locations/' + self.LOCATION_ID +
                   '/operations/%d' % (self.OP_ID,))
        request_pb = operations_pb2.GetOperationRequest(name=op_name)

        # Create response_pb
        response_pb = operations_pb2.Operation(done=done)

        # Patch the stub used by the API method.
        client._operations_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = done

        # Perform the method and check the result.
        result = operation.finished()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'GetOperation',
            (request_pb, TIMEOUT_SECONDS),
            {},
        )])

        if done:
            self.assertTrue(operation._complete)
        else:
            self.assertFalse(operation._complete)

    def test_finished(self):
        self._finished_helper(done=True)

    def test_finished_not_done(self):
        self._finished_helper(done=False)


class TestInstance(unittest2.TestCase):

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
    TIMEOUT_SECONDS = 1

    def _getTargetClass(self):
        from gcloud.bigtable.instance import Instance
        return Instance

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES

        client = object()
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertTrue(instance._client is client)
        self.assertEqual(instance._cluster_location_id, self.LOCATION_ID)
        self.assertEqual(instance._cluster_serve_nodes, DEFAULT_SERVE_NODES)

    def test_constructor_non_default(self):
        display_name = 'display_name'
        client = object()

        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID,
                                 display_name=display_name)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, display_name)
        self.assertTrue(instance._client is client)

    def test_copy(self):
        display_name = 'display_name'

        client = _Client(self.PROJECT)
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID,
                                 display_name=display_name)
        new_instance = instance.copy()

        # Make sure the client copy succeeded.
        self.assertFalse(new_instance._client is client)
        self.assertEqual(new_instance._client, client)
        # Make sure the client got copied to a new instance.
        self.assertFalse(instance is new_instance)
        self.assertEqual(instance, new_instance)

    def test_table_factory(self):
        from gcloud.bigtable.table import Table

        instance = self._makeOne(self.INSTANCE_ID, None, self.LOCATION_ID)

        table = instance.table(self.TABLE_ID)
        self.assertTrue(isinstance(table, Table))
        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertEqual(table._instance, instance)

    def test__update_from_pb_success(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)

        display_name = 'display_name'
        instance_pb = data_v2_pb2.Instance(
            display_name=display_name,
        )

        instance = self._makeOne(None, None, None, None)
        self.assertEqual(instance.display_name, None)
        instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, display_name)

    def test__update_from_pb_no_display_name(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)

        instance_pb = data_v2_pb2.Instance()
        instance = self._makeOne(None, None, None, None)
        self.assertEqual(instance.display_name, None)
        with self.assertRaises(ValueError):
            instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, None)

    def test_from_pb_success(self):
        from gcloud.bigtable.instance import _EXISTING_INSTANCE_LOCATION_ID
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)

        client = _Client(project=self.PROJECT)

        instance_pb = data_v2_pb2.Instance(
            name=self.INSTANCE_NAME,
            display_name=self.INSTANCE_ID,
        )

        klass = self._getTargetClass()
        instance = klass.from_pb(instance_pb, client)
        self.assertTrue(isinstance(instance, klass))
        self.assertEqual(instance._client, client)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance._cluster_location_id,
                         _EXISTING_INSTANCE_LOCATION_ID)

    def test_from_pb_bad_instance_name(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)

        instance_name = 'INCORRECT_FORMAT'
        instance_pb = data_v2_pb2.Instance(name=instance_name)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, None)

    def test_from_pb_project_mistmatch(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)

        ALT_PROJECT = 'ALT_PROJECT'
        client = _Client(project=ALT_PROJECT)

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)

        instance_pb = data_v2_pb2.Instance(name=self.INSTANCE_NAME)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, client)

    def test_name_property(self):
        client = _Client(project=self.PROJECT)

        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)
        self.assertEqual(instance.name, self.INSTANCE_NAME)

    def test___eq__(self):
        client = object()
        instance1 = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)
        instance2 = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)
        self.assertEqual(instance1, instance2)

    def test___eq__type_differ(self):
        client = object()
        instance1 = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)
        instance2 = object()
        self.assertNotEqual(instance1, instance2)

    def test___ne__same_value(self):
        client = object()
        instance1 = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)
        instance2 = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)
        comparison_val = (instance1 != instance2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        instance1 = self._makeOne('instance_id1', 'client1', self.LOCATION_ID)
        instance2 = self._makeOne('instance_id2', 'client2', self.LOCATION_ID)
        self.assertNotEqual(instance1, instance2)

    def test_reload(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)
        from gcloud.bigtable._generated_v2 import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)

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
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])

        # Check Instance optional config values before.
        self.assertEqual(instance.display_name, DISPLAY_NAME)

    def test_create(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import instance as MUT

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)

        # Create request_pb. Just a mock since we monkey patch
        # _prepare_create_request
        request_pb = object()

        # Create response_pb
        OP_BEGIN = object()
        response_pb = operations_pb2.Operation(name=self.OP_NAME)

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = MUT.Operation('create', self.OP_ID, OP_BEGIN,
                                        self.LOCATION_ID, instance=instance)

        # Create the mocks.
        prep_create_called = []

        def mock_prep_create_req(instance):
            prep_create_called.append(instance)
            return request_pb

        process_operation_called = []

        def mock_process_operation(operation_pb):
            process_operation_called.append(operation_pb)
            return self.OP_ID, self.LOCATION_ID, OP_BEGIN

        # Perform the method and check the result.
        with _Monkey(MUT,
                     _prepare_create_request=mock_prep_create_req,
                     _process_operation=mock_process_operation):
            result = instance.create()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'CreateInstance',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])
        self.assertEqual(prep_create_called, [instance])
        self.assertEqual(process_operation_called, [response_pb])

    def test_create_w_explicit_serve_nodes(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import instance as MUT

        SERVE_NODES = 5

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID,
                                 serve_nodes=SERVE_NODES)

        # Create request_pb. Just a mock since we monkey patch
        # _prepare_create_request
        request_pb = object()

        # Create response_pb
        OP_BEGIN = object()
        response_pb = operations_pb2.Operation(name=self.OP_NAME)

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = MUT.Operation('create', self.OP_ID, OP_BEGIN,
                                        self.LOCATION_ID, instance=instance)

        # Create the mocks.
        prep_create_called = []

        def mock_prep_create_req(instance):
            prep_create_called.append(instance)
            return request_pb

        process_operation_called = []

        def mock_process_operation(operation_pb):
            process_operation_called.append(operation_pb)
            return self.OP_ID, self.LOCATION_ID, OP_BEGIN

        # Perform the method and check the result.
        with _Monkey(MUT,
                     _prepare_create_request=mock_prep_create_req,
                     _process_operation=mock_process_operation):
            result = instance.create()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'CreateInstance',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])
        self.assertEqual(prep_create_called, [instance])
        self.assertEqual(process_operation_called, [response_pb])

    def test_update(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID,
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
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])

    def test_delete(self):
        from google.protobuf import empty_pb2
        from gcloud.bigtable._generated_v2 import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)

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
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])

    def test_list_clusters(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as instance_v2_pb2)
        from gcloud.bigtable._generated_v2 import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from gcloud.bigtable._testing import _FakeStub

        FAILED_LOCATION = 'FAILED'
        FAILED_LOCATIONS = [FAILED_LOCATION]
        CLUSTER_ID1 = 'cluster-id1'
        CLUSTER_ID2 = 'cluster-id2'
        SERVE_NODES = 4

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)

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
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])

    def _list_tables_helper(self, table_name=None):
        from gcloud.bigtable._generated_v2 import (
            table_pb2 as table_data_v2_pb2)
        from gcloud.bigtable._generated_v2 import (
            bigtable_table_admin_pb2 as table_messages_v1_pb2)
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = self._makeOne(self.INSTANCE_ID, client, self.LOCATION_ID)

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
            (request_pb, self.TIMEOUT_SECONDS),
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


class Test__prepare_create_request(unittest2.TestCase):
    PROJECT = 'PROJECT'
    PARENT = 'projects/' + PROJECT
    LOCATION_ID = 'locname'
    LOCATION_NAME = 'projects/' + PROJECT + '/locations/' + LOCATION_ID
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = PARENT + '/instances/' + INSTANCE_ID
    CLUSTER_NAME = INSTANCE_NAME + '/clusters/' + INSTANCE_ID

    def _callFUT(self, instance, **kw):
        from gcloud.bigtable.instance import _prepare_create_request
        return _prepare_create_request(instance, **kw)

    def test_w_defaults(self):
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)
        from gcloud.bigtable._generated_v2 import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from gcloud.bigtable.instance import Instance

        client = _Client(self.PROJECT)

        instance = Instance(self.INSTANCE_ID, client, self.LOCATION_ID)
        request_pb = self._callFUT(instance)
        self.assertTrue(isinstance(request_pb,
                                   messages_v2_pb.CreateInstanceRequest))
        self.assertEqual(request_pb.instance_id, self.INSTANCE_ID)
        self.assertEqual(request_pb.parent, self.PARENT)
        self.assertTrue(isinstance(request_pb.instance, data_v2_pb2.Instance))
        self.assertEqual(request_pb.instance.name, u'')
        self.assertEqual(request_pb.instance.display_name, self.INSTANCE_ID)

        # An instance must also define a same-named cluster
        cluster = request_pb.clusters[self.INSTANCE_ID]
        self.assertTrue(isinstance(cluster, data_v2_pb2.Cluster))
        self.assertEqual(cluster.name, self.CLUSTER_NAME)
        self.assertEqual(cluster.location, self.LOCATION_NAME)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

    def test_w_explicit_serve_nodes(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)
        from gcloud.bigtable._generated_v2 import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from gcloud.bigtable.instance import Instance
        DISPLAY_NAME = u'DISPLAY_NAME'
        SERVE_NODES = 5
        client = _Client(self.PROJECT)
        instance = Instance(self.INSTANCE_ID, client, self.LOCATION_ID,
                            display_name=DISPLAY_NAME,
                            serve_nodes=SERVE_NODES)

        request_pb = self._callFUT(instance)

        self.assertTrue(isinstance(request_pb,
                                   messages_v2_pb.CreateInstanceRequest))
        self.assertEqual(request_pb.instance_id, self.INSTANCE_ID)
        self.assertEqual(request_pb.parent,
                         'projects/' + self.PROJECT)
        self.assertTrue(isinstance(request_pb.instance, data_v2_pb2.Instance))
        self.assertEqual(request_pb.instance.display_name, DISPLAY_NAME)
        # An instance must also define a same-named cluster
        cluster = request_pb.clusters[self.INSTANCE_ID]
        self.assertTrue(isinstance(cluster, data_v2_pb2.Cluster))
        self.assertEqual(cluster.location, self.LOCATION_NAME)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)


class Test__parse_pb_any_to_native(unittest2.TestCase):

    def _callFUT(self, any_val, expected_type=None):
        from gcloud.bigtable.instance import _parse_pb_any_to_native
        return _parse_pb_any_to_native(any_val, expected_type=expected_type)

    def test_with_known_type_url(self):
        from google.protobuf import any_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._generated_v2 import (
            data_pb2 as data_v2_pb2)
        from gcloud.bigtable import instance as MUT

        TYPE_URL = 'type.googleapis.com/' + data_v2_pb2._CELL.full_name
        fake_type_url_map = {TYPE_URL: data_v2_pb2.Cell}

        cell = data_v2_pb2.Cell(
            timestamp_micros=0,
            value=b'foobar',
        )
        any_val = any_pb2.Any(
            type_url=TYPE_URL,
            value=cell.SerializeToString(),
        )
        with _Monkey(MUT, _TYPE_URL_MAP=fake_type_url_map):
            result = self._callFUT(any_val)

        self.assertEqual(result, cell)

    def test_with_create_instance_metadata(self):
        from google.protobuf import any_pb2
        from google.protobuf.timestamp_pb2 import Timestamp
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)
        from gcloud.bigtable._generated_v2 import (
            bigtable_instance_admin_pb2 as messages_v2_pb)

        TYPE_URL = ('type.googleapis.com/' +
                    messages_v2_pb._CREATEINSTANCEMETADATA.full_name)
        metadata = messages_v2_pb.CreateInstanceMetadata(
            request_time=Timestamp(seconds=1, nanos=1234),
            finish_time=Timestamp(seconds=10, nanos=891011),
            original_request=messages_v2_pb.CreateInstanceRequest(
                parent='foo',
                instance_id='bar',
                instance=data_v2_pb2.Instance(
                    display_name='quux',
                ),
            ),
        )

        any_val = any_pb2.Any(
            type_url=TYPE_URL,
            value=metadata.SerializeToString(),
        )
        result = self._callFUT(any_val)
        self.assertEqual(result, metadata)

    def test_unknown_type_url(self):
        from google.protobuf import any_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable import instance as MUT

        fake_type_url_map = {}
        any_val = any_pb2.Any()
        with _Monkey(MUT, _TYPE_URL_MAP=fake_type_url_map):
            with self.assertRaises(KeyError):
                self._callFUT(any_val)

    def test_disagreeing_type_url(self):
        from google.protobuf import any_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable import instance as MUT

        TYPE_URL1 = 'foo'
        TYPE_URL2 = 'bar'
        fake_type_url_map = {TYPE_URL1: None}
        any_val = any_pb2.Any(type_url=TYPE_URL2)
        with _Monkey(MUT, _TYPE_URL_MAP=fake_type_url_map):
            with self.assertRaises(ValueError):
                self._callFUT(any_val, expected_type=TYPE_URL1)


class Test__process_operation(unittest2.TestCase):

    def _callFUT(self, operation_pb):
        from gcloud.bigtable.instance import _process_operation
        return _process_operation(operation_pb)

    def test_it(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._generated_v2 import (
            bigtable_instance_admin_pb2 as messages_v2_pb)
        from gcloud.bigtable import instance as MUT

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        LOCATION_ID = 'location'
        OP_ID = 234
        OPERATION_NAME = (
            'operations/projects/%s/instances/%s/locations/%s/operations/%d' %
            (PROJECT, INSTANCE_ID, LOCATION_ID, OP_ID))

        current_op = operations_pb2.Operation(name=OPERATION_NAME)

        # Create mocks.
        request_metadata = messages_v2_pb.CreateInstanceMetadata()
        parse_pb_any_called = []

        def mock_parse_pb_any_to_native(any_val, expected_type=None):
            parse_pb_any_called.append((any_val, expected_type))
            return request_metadata

        expected_operation_begin = object()
        ts_to_dt_called = []

        def mock_pb_timestamp_to_datetime(timestamp):
            ts_to_dt_called.append(timestamp)
            return expected_operation_begin

        # Exectute method with mocks in place.
        with _Monkey(MUT, _parse_pb_any_to_native=mock_parse_pb_any_to_native,
                     _pb_timestamp_to_datetime=mock_pb_timestamp_to_datetime):
            op_id, loc_id, op_begin = self._callFUT(current_op)

        # Check outputs.
        self.assertEqual(op_id, OP_ID)
        self.assertTrue(op_begin is expected_operation_begin)
        self.assertEqual(loc_id, LOCATION_ID)

        # Check mocks were used correctly.
        self.assertEqual(parse_pb_any_called, [(current_op.metadata, None)])
        self.assertEqual(ts_to_dt_called, [request_metadata.request_time])

    def test_op_name_parsing_failure(self):
        from google.longrunning import operations_pb2

        operation_pb = operations_pb2.Operation(name='invalid')
        with self.assertRaises(ValueError):
            self._callFUT(operation_pb)


class _Client(object):

    def __init__(self, project, timeout_seconds=None):
        self.project = project
        self.project_name = 'projects/' + self.project
        self.timeout_seconds = timeout_seconds

    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name and
                other.timeout_seconds == self.timeout_seconds)
