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


class TestOperation(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.cluster import Operation
        return Operation

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _constructor_test_helper(self, cluster=None):
        import datetime
        op_type = 'fake-op'
        op_id = 8915
        begin = datetime.datetime(2015, 10, 22, 1, 1)
        operation = self._makeOne(op_type, op_id, begin, cluster=cluster)

        self.assertEqual(operation.op_type, op_type)
        self.assertEqual(operation.op_id, op_id)
        self.assertEqual(operation.begin, begin)
        self.assertEqual(operation._cluster, cluster)
        self.assertFalse(operation._complete)

    def test_constructor_defaults(self):
        self._constructor_test_helper()

    def test_constructor_explicit_cluster(self):
        cluster = object()
        self._constructor_test_helper(cluster=cluster)

    def test___eq__(self):
        import datetime
        op_type = 'fake-op'
        op_id = 8915
        begin = datetime.datetime(2015, 10, 22, 1, 1)
        cluster = object()
        operation1 = self._makeOne(op_type, op_id, begin, cluster=cluster)
        operation2 = self._makeOne(op_type, op_id, begin, cluster=cluster)
        self.assertEqual(operation1, operation2)

    def test___eq__type_differ(self):
        operation1 = self._makeOne('foo', 123, None)
        operation2 = object()
        self.assertNotEqual(operation1, operation2)

    def test___ne__same_value(self):
        import datetime
        op_type = 'fake-op'
        op_id = 8915
        begin = datetime.datetime(2015, 10, 22, 1, 1)
        cluster = object()
        operation1 = self._makeOne(op_type, op_id, begin, cluster=cluster)
        operation2 = self._makeOne(op_type, op_id, begin, cluster=cluster)
        comparison_val = (operation1 != operation2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        operation1 = self._makeOne('foo', 123, None)
        operation2 = self._makeOne('bar', 456, None)
        self.assertNotEqual(operation1, operation2)

    def test_finished_without_operation(self):
        operation = self._makeOne(None, None, None)
        operation._complete = True
        with self.assertRaises(ValueError):
            operation.finished()

    def _finished_helper(self, done):
        import datetime
        from google.longrunning import operations_pb2
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable.cluster import Cluster

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        op_type = 'fake-op'
        op_id = 789
        begin = datetime.datetime(2015, 10, 22, 1, 1)
        timeout_seconds = 1

        client = _Client(project, timeout_seconds=timeout_seconds)
        cluster = Cluster(zone, cluster_id, client)
        operation = self._makeOne(op_type, op_id, begin, cluster=cluster)

        # Create request_pb
        op_name = ('operations/projects/' + project + '/zones/' +
                   zone + '/clusters/' + cluster_id +
                   '/operations/%d' % (op_id,))
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
            (request_pb, timeout_seconds),
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


class TestCluster(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.cluster import Cluster
        return Cluster

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        zone = 'zone'
        cluster_id = 'cluster-id'
        client = object()

        cluster = self._makeOne(zone, cluster_id, client)
        self.assertEqual(cluster.zone, zone)
        self.assertEqual(cluster.cluster_id, cluster_id)
        self.assertEqual(cluster.display_name, cluster_id)
        self.assertEqual(cluster.serve_nodes, 3)
        self.assertTrue(cluster._client is client)

    def test_constructor_non_default(self):
        zone = 'zone'
        cluster_id = 'cluster-id'
        display_name = 'display_name'
        serve_nodes = 8
        client = object()

        cluster = self._makeOne(zone, cluster_id, client,
                                display_name=display_name,
                                serve_nodes=serve_nodes)
        self.assertEqual(cluster.zone, zone)
        self.assertEqual(cluster.cluster_id, cluster_id)
        self.assertEqual(cluster.display_name, display_name)
        self.assertEqual(cluster.serve_nodes, serve_nodes)
        self.assertTrue(cluster._client is client)

    def test_copy(self):
        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        display_name = 'display_name'
        serve_nodes = 8

        client = _Client(project)
        cluster = self._makeOne(zone, cluster_id, client,
                                display_name=display_name,
                                serve_nodes=serve_nodes)
        new_cluster = cluster.copy()

        # Make sure the client copy succeeded.
        self.assertFalse(new_cluster._client is client)
        self.assertEqual(new_cluster._client, client)
        # Make sure the client got copied to a new instance.
        self.assertFalse(cluster is new_cluster)
        self.assertEqual(cluster, new_cluster)

    def test_table_factory(self):
        from gcloud.bigtable.table import Table

        zone = 'zone'
        cluster_id = 'cluster-id'
        cluster = self._makeOne(zone, cluster_id, None)

        table_id = 'table_id'
        table = cluster.table(table_id)
        self.assertTrue(isinstance(table, Table))
        self.assertEqual(table.table_id, table_id)
        self.assertEqual(table._cluster, cluster)

    def test__update_from_pb_success(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES

        display_name = 'display_name'
        serve_nodes = 8
        cluster_pb = data_pb2.Cluster(
            display_name=display_name,
            serve_nodes=serve_nodes,
        )

        cluster = self._makeOne(None, None, None)
        self.assertEqual(cluster.display_name, None)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)
        cluster._update_from_pb(cluster_pb)
        self.assertEqual(cluster.display_name, display_name)
        self.assertEqual(cluster.serve_nodes, serve_nodes)

    def test__update_from_pb_no_display_name(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES

        cluster_pb = data_pb2.Cluster(serve_nodes=331)
        cluster = self._makeOne(None, None, None)
        self.assertEqual(cluster.display_name, None)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)
        with self.assertRaises(ValueError):
            cluster._update_from_pb(cluster_pb)
        self.assertEqual(cluster.display_name, None)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

    def test__update_from_pb_no_serve_nodes(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES

        cluster_pb = data_pb2.Cluster(display_name='name')
        cluster = self._makeOne(None, None, None)
        self.assertEqual(cluster.display_name, None)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)
        with self.assertRaises(ValueError):
            cluster._update_from_pb(cluster_pb)
        self.assertEqual(cluster.display_name, None)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

    def test_from_pb_success(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        client = _Client(project=project)

        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        cluster_pb = data_pb2.Cluster(
            name=cluster_name,
            display_name=cluster_id,
            serve_nodes=331,
        )

        klass = self._getTargetClass()
        cluster = klass.from_pb(cluster_pb, client)
        self.assertTrue(isinstance(cluster, klass))
        self.assertEqual(cluster._client, client)
        self.assertEqual(cluster.zone, zone)
        self.assertEqual(cluster.cluster_id, cluster_id)

    def test_from_pb_bad_cluster_name(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)

        cluster_name = 'INCORRECT_FORMAT'
        cluster_pb = data_pb2.Cluster(name=cluster_name)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, None)

    def test_from_pb_project_mistmatch(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        alt_project = 'ALT_PROJECT'
        client = _Client(project=alt_project)

        self.assertNotEqual(project, alt_project)

        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        cluster_pb = data_pb2.Cluster(name=cluster_name)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, client)

    def test_name_property(self):
        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        client = _Client(project=project)

        cluster = self._makeOne(zone, cluster_id, client)
        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        self.assertEqual(cluster.name, cluster_name)

    def test___eq__(self):
        zone = 'zone'
        cluster_id = 'cluster_id'
        client = object()
        cluster1 = self._makeOne(zone, cluster_id, client)
        cluster2 = self._makeOne(zone, cluster_id, client)
        self.assertEqual(cluster1, cluster2)

    def test___eq__type_differ(self):
        cluster1 = self._makeOne('zone', 'cluster_id', 'client')
        cluster2 = object()
        self.assertNotEqual(cluster1, cluster2)

    def test___ne__same_value(self):
        zone = 'zone'
        cluster_id = 'cluster_id'
        client = object()
        cluster1 = self._makeOne(zone, cluster_id, client)
        cluster2 = self._makeOne(zone, cluster_id, client)
        comparison_val = (cluster1 != cluster2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        cluster1 = self._makeOne('zone1', 'cluster_id1', 'client1')
        cluster2 = self._makeOne('zone2', 'cluster_id2', 'client2')
        self.assertNotEqual(cluster1, cluster2)

    def test_reload(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        timeout_seconds = 123

        client = _Client(project, timeout_seconds=timeout_seconds)
        cluster = self._makeOne(zone, cluster_id, client)

        # Create request_pb
        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        request_pb = messages_pb2.GetClusterRequest(name=cluster_name)

        # Create response_pb
        serve_nodes = 31
        display_name = u'hey-hi-hello'
        response_pb = data_pb2.Cluster(
            display_name=display_name,
            serve_nodes=serve_nodes,
        )

        # Patch the stub used by the API method.
        client._cluster_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check Cluster optional config values before.
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)
        self.assertEqual(cluster.display_name, cluster_id)

        # Perform the method and check the result.
        result = cluster.reload()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'GetCluster',
            (request_pb, timeout_seconds),
            {},
        )])

        # Check Cluster optional config values before.
        self.assertEqual(cluster.serve_nodes, serve_nodes)
        self.assertEqual(cluster.display_name, display_name)

    def test_create(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import cluster as MUT

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        timeout_seconds = 578

        client = _Client(project, timeout_seconds=timeout_seconds)
        cluster = self._makeOne(zone, cluster_id, client)

        # Create request_pb. Just a mock since we monkey patch
        # _prepare_create_request
        request_pb = object()

        # Create response_pb
        op_id = 5678
        op_begin = object()
        op_name = ('operations/projects/%s/zones/%s/clusters/%s/'
                   'operations/%d' % (project, zone, cluster_id, op_id))
        current_op = operations_pb2.Operation(name=op_name)
        response_pb = data_pb2.Cluster(current_operation=current_op)

        # Patch the stub used by the API method.
        client._cluster_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = MUT.Operation('create', op_id, op_begin,
                                        cluster=cluster)

        # Create the mocks.
        prep_create_called = []

        def mock_prep_create_req(cluster):
            prep_create_called.append(cluster)
            return request_pb

        process_operation_called = []

        def mock_process_operation(operation_pb):
            process_operation_called.append(operation_pb)
            return op_id, op_begin

        # Perform the method and check the result.
        with _Monkey(MUT, _prepare_create_request=mock_prep_create_req,
                     _process_operation=mock_process_operation):
            result = cluster.create()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'CreateCluster',
            (request_pb, timeout_seconds),
            {},
        )])
        self.assertEqual(prep_create_called, [cluster])
        self.assertEqual(process_operation_called, [current_op])

    def test_update(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import cluster as MUT

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        serve_nodes = 81
        display_name = 'display_name'
        timeout_seconds = 9

        client = _Client(project, timeout_seconds=timeout_seconds)
        cluster = self._makeOne(zone, cluster_id, client,
                                display_name=display_name,
                                serve_nodes=serve_nodes)

        # Create request_pb
        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        request_pb = data_pb2.Cluster(
            name=cluster_name,
            display_name=display_name,
            serve_nodes=serve_nodes,
        )

        # Create response_pb
        current_op = operations_pb2.Operation()
        response_pb = data_pb2.Cluster(current_operation=current_op)

        # Patch the stub used by the API method.
        client._cluster_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        op_id = 5678
        op_begin = object()
        expected_result = MUT.Operation('update', op_id, op_begin,
                                        cluster=cluster)

        # Create mocks
        process_operation_called = []

        def mock_process_operation(operation_pb):
            process_operation_called.append(operation_pb)
            return op_id, op_begin

        # Perform the method and check the result.
        with _Monkey(MUT, _process_operation=mock_process_operation):
            result = cluster.update()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'UpdateCluster',
            (request_pb, timeout_seconds),
            {},
        )])
        self.assertEqual(process_operation_called, [current_op])

    def test_delete(self):
        from google.protobuf import empty_pb2
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        timeout_seconds = 57

        client = _Client(project, timeout_seconds=timeout_seconds)
        cluster = self._makeOne(zone, cluster_id, client)

        # Create request_pb
        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        request_pb = messages_pb2.DeleteClusterRequest(name=cluster_name)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._cluster_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = cluster.delete()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'DeleteCluster',
            (request_pb, timeout_seconds),
            {},
        )])

    def test_undelete(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import cluster as MUT

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        timeout_seconds = 78

        client = _Client(project, timeout_seconds=timeout_seconds)
        cluster = self._makeOne(zone, cluster_id, client)

        # Create request_pb
        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        request_pb = messages_pb2.UndeleteClusterRequest(name=cluster_name)

        # Create response_pb
        response_pb = operations_pb2.Operation()

        # Patch the stub used by the API method.
        client._cluster_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        op_id = 5678
        op_begin = object()
        expected_result = MUT.Operation('undelete', op_id, op_begin,
                                        cluster=cluster)

        # Create the mocks.
        process_operation_called = []

        def mock_process_operation(operation_pb):
            process_operation_called.append(operation_pb)
            return op_id, op_begin

        # Perform the method and check the result.
        with _Monkey(MUT, _process_operation=mock_process_operation):
            result = cluster.undelete()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'UndeleteCluster',
            (request_pb, timeout_seconds),
            {},
        )])
        self.assertEqual(process_operation_called, [response_pb])

    def _list_tables_helper(self, table_id, table_name=None):
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as table_data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_table_service_messages_pb2 as table_messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        timeout_seconds = 45

        client = _Client(project, timeout_seconds=timeout_seconds)
        cluster = self._makeOne(zone, cluster_id, client)

        # Create request_
        cluster_name = ('projects/' + project + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        request_pb = table_messages_pb2.ListTablesRequest(name=cluster_name)

        # Create response_pb
        table_name = table_name or (cluster_name + '/tables/' + table_id)
        response_pb = table_messages_pb2.ListTablesResponse(
            tables=[
                table_data_pb2.Table(name=table_name),
            ],
        )

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_table = cluster.table(table_id)
        expected_result = [expected_table]

        # Perform the method and check the result.
        result = cluster.list_tables()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ListTables',
            (request_pb, timeout_seconds),
            {},
        )])

    def test_list_tables(self):
        table_id = 'table_id'
        self._list_tables_helper(table_id)

    def test_list_tables_failure_bad_split(self):
        with self.assertRaises(ValueError):
            self._list_tables_helper(None, table_name='wrong-format')

    def test_list_tables_failure_name_bad_before(self):
        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'

        table_id = 'table_id'
        bad_table_name = ('nonempty-section-before' +
                          'projects/' + project + '/zones/' + zone +
                          '/clusters/' + cluster_id + '/tables/' + table_id)
        with self.assertRaises(ValueError):
            self._list_tables_helper(table_id, table_name=bad_table_name)


class Test__prepare_create_request(unittest2.TestCase):

    def _callFUT(self, cluster):
        from gcloud.bigtable.cluster import _prepare_create_request
        return _prepare_create_request(cluster)

    def test_it(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable.cluster import Cluster

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        display_name = u'DISPLAY_NAME'
        serve_nodes = 8
        client = _Client(project)

        cluster = Cluster(zone, cluster_id, client,
                          display_name=display_name, serve_nodes=serve_nodes)
        request_pb = self._callFUT(cluster)
        self.assertTrue(isinstance(request_pb,
                                   messages_pb2.CreateClusterRequest))
        self.assertEqual(request_pb.cluster_id, cluster_id)
        self.assertEqual(request_pb.name,
                         'projects/' + project + '/zones/' + zone)
        self.assertTrue(isinstance(request_pb.cluster, data_pb2.Cluster))
        self.assertEqual(request_pb.cluster.display_name, display_name)
        self.assertEqual(request_pb.cluster.serve_nodes, serve_nodes)


class Test__parse_pb_any_to_native(unittest2.TestCase):

    def _callFUT(self, any_val, expected_type=None):
        from gcloud.bigtable.cluster import _parse_pb_any_to_native
        return _parse_pb_any_to_native(any_val, expected_type=expected_type)

    def test_with_known_type_url(self):
        from google.protobuf import any_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2
        from gcloud.bigtable import cluster as MUT

        type_url = 'type.googleapis.com/' + data_pb2._CELL.full_name
        fake_type_url_map = {type_url: data_pb2.Cell}

        cell = data_pb2.Cell(
            timestamp_micros=0,
            value=b'foobar',
        )
        any_val = any_pb2.Any(
            type_url=type_url,
            value=cell.SerializeToString(),
        )
        with _Monkey(MUT, _TYPE_URL_MAP=fake_type_url_map):
            result = self._callFUT(any_val)

        self.assertEqual(result, cell)

    def test_with_create_cluster_metadata(self):
        from google.protobuf import any_pb2
        from google.protobuf.timestamp_pb2 import Timestamp
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)

        type_url = ('type.googleapis.com/' +
                    messages_pb2._CREATECLUSTERMETADATA.full_name)
        metadata = messages_pb2.CreateClusterMetadata(
            request_time=Timestamp(seconds=1, nanos=1234),
            finish_time=Timestamp(seconds=10, nanos=891011),
            original_request=messages_pb2.CreateClusterRequest(
                name='foo',
                cluster_id='bar',
                cluster=data_pb2.Cluster(
                    display_name='quux',
                    serve_nodes=1337,
                ),
            ),
        )

        any_val = any_pb2.Any(
            type_url=type_url,
            value=metadata.SerializeToString(),
        )
        result = self._callFUT(any_val)
        self.assertEqual(result, metadata)

    def test_with_update_cluster_metadata(self):
        from google.protobuf import any_pb2
        from google.protobuf.timestamp_pb2 import Timestamp
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)

        type_url = ('type.googleapis.com/' +
                    messages_pb2._UPDATECLUSTERMETADATA.full_name)
        metadata = messages_pb2.UpdateClusterMetadata(
            request_time=Timestamp(seconds=1, nanos=1234),
            finish_time=Timestamp(seconds=10, nanos=891011),
            cancel_time=Timestamp(seconds=100, nanos=76543),
            original_request=data_pb2.Cluster(
                display_name='the-end',
                serve_nodes=42,
            ),
        )

        any_val = any_pb2.Any(
            type_url=type_url,
            value=metadata.SerializeToString(),
        )
        result = self._callFUT(any_val)
        self.assertEqual(result, metadata)

    def test_with_undelete_cluster_metadata(self):
        from google.protobuf import any_pb2
        from google.protobuf.timestamp_pb2 import Timestamp
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)

        type_url = ('type.googleapis.com/' +
                    messages_pb2._UNDELETECLUSTERMETADATA.full_name)
        metadata = messages_pb2.UndeleteClusterMetadata(
            request_time=Timestamp(seconds=1, nanos=1234),
            finish_time=Timestamp(seconds=10, nanos=891011),
        )

        any_val = any_pb2.Any(
            type_url=type_url,
            value=metadata.SerializeToString(),
        )
        result = self._callFUT(any_val)
        self.assertEqual(result, metadata)

    def test_unknown_type_url(self):
        from google.protobuf import any_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable import cluster as MUT

        fake_type_url_map = {}
        any_val = any_pb2.Any()
        with _Monkey(MUT, _TYPE_URL_MAP=fake_type_url_map):
            with self.assertRaises(KeyError):
                self._callFUT(any_val)

    def test_disagreeing_type_url(self):
        from google.protobuf import any_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable import cluster as MUT

        type_url1 = 'foo'
        type_url2 = 'bar'
        fake_type_url_map = {type_url1: None}
        any_val = any_pb2.Any(type_url=type_url2)
        with _Monkey(MUT, _TYPE_URL_MAP=fake_type_url_map):
            with self.assertRaises(ValueError):
                self._callFUT(any_val, expected_type=type_url1)


class Test__process_operation(unittest2.TestCase):

    def _callFUT(self, operation_pb):
        from gcloud.bigtable.cluster import _process_operation
        return _process_operation(operation_pb)

    def test_it(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable import cluster as MUT

        project = 'PROJECT'
        zone = 'zone'
        cluster_id = 'cluster-id'
        expected_operation_id = 234
        operation_name = ('operations/projects/%s/zones/%s/clusters/%s/'
                          'operations/%d' % (project, zone, cluster_id,
                                             expected_operation_id))

        current_op = operations_pb2.Operation(name=operation_name)

        # Create mocks.
        request_metadata = messages_pb2.CreateClusterMetadata()
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
            operation_id, operation_begin = self._callFUT(current_op)

        # Check outputs.
        self.assertEqual(operation_id, expected_operation_id)
        self.assertTrue(operation_begin is expected_operation_begin)

        # Check mocks were used correctly.
        self.assertEqual(parse_pb_any_called, [(current_op.metadata, None)])
        self.assertEqual(ts_to_dt_called, [request_metadata.request_time])

    def test_op_name_parsing_failure(self):
        from google.longrunning import operations_pb2
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)

        current_op = operations_pb2.Operation(name='invalid')
        cluster = data_pb2.Cluster(current_operation=current_op)
        with self.assertRaises(ValueError):
            self._callFUT(cluster)


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
