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
        op_type = 'fake-op'
        op_id = 8915
        operation = self._makeOne(op_type, op_id, cluster=cluster)

        self.assertEqual(operation.op_type, op_type)
        self.assertEqual(operation.op_id, op_id)
        self.assertEqual(operation._cluster, cluster)
        self.assertFalse(operation._complete)

    def test_constructor_defaults(self):
        self._constructor_test_helper()

    def test_constructor_explicit_cluster(self):
        cluster = object()
        self._constructor_test_helper(cluster=cluster)

    def test___eq__(self):
        op_type = 'fake-op'
        op_id = 8915
        cluster = object()
        operation1 = self._makeOne(op_type, op_id, cluster=cluster)
        operation2 = self._makeOne(op_type, op_id, cluster=cluster)
        self.assertEqual(operation1, operation2)

    def test___eq__type_differ(self):
        operation1 = self._makeOne('foo', 123, None)
        operation2 = object()
        self.assertNotEqual(operation1, operation2)

    def test___ne__same_value(self):
        op_type = 'fake-op'
        op_id = 8915
        cluster = object()
        operation1 = self._makeOne(op_type, op_id, cluster=cluster)
        operation2 = self._makeOne(op_type, op_id, cluster=cluster)
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
        from google.longrunning import operations_pb2
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable.cluster import Cluster

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        CLUSTER_ID = 'cluster-id'
        OP_TYPE = 'fake-op'
        OP_ID = 789
        timeout_seconds = 1

        client = _Client(PROJECT, timeout_seconds=timeout_seconds)
        instance = _Instance(INSTANCE_ID, client)
        cluster = Cluster(CLUSTER_ID, instance)
        operation = self._makeOne(OP_TYPE, OP_ID, cluster=cluster)

        # Create request_pb
        op_name = ('operations/projects/' + PROJECT +
                   '/instances/' + INSTANCE_ID +
                   '/clusters/' + CLUSTER_ID +
                   '/operations/%d' % (OP_ID,))
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

    PROJECT = 'project'
    INSTANCE_ID = 'instance-id'
    CLUSTER_ID = 'cluster-id'
    CLUSTER_NAME = ('projects/' + PROJECT +
                    '/instances/' + INSTANCE_ID +
                    '/clusters/' + CLUSTER_ID)
    TIMEOUT_SECONDS = 123

    def _getTargetClass(self):
        from gcloud.bigtable.cluster import Cluster
        return Cluster

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._makeOne(self.CLUSTER_ID, instance)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertTrue(cluster._instance is instance)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

    def test_constructor_non_default(self):
        SERVE_NODES = 8
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._makeOne(self.CLUSTER_ID, instance,
                                serve_nodes=SERVE_NODES)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertTrue(cluster._instance is instance)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)

    def test_copy(self):
        SERVE_NODES = 8

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._makeOne(self.CLUSTER_ID, instance,
                                serve_nodes=SERVE_NODES)
        new_cluster = cluster.copy()

        # Make sure the client copy succeeded.
        self.assertFalse(new_cluster._instance is instance)
        self.assertEqual(new_cluster.serve_nodes, SERVE_NODES)
        # Make sure the client got copied to a new instance.
        self.assertFalse(cluster is new_cluster)
        self.assertEqual(cluster, new_cluster)

    def test__update_from_pb_success(self):
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES

        SERVE_NODES = 8
        cluster_pb = _ClusterPB(
            serve_nodes=SERVE_NODES,
        )
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._makeOne(self.CLUSTER_ID, instance)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)
        cluster._update_from_pb(cluster_pb)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)

    def test__update_from_pb_no_serve_nodes(self):
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES

        cluster_pb = _ClusterPB()
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._makeOne(self.CLUSTER_ID, instance)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)
        with self.assertRaises(ValueError):
            cluster._update_from_pb(cluster_pb)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

    def test_from_pb_success(self):
        SERVE_NODES = 331
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster_pb = _ClusterPB(
            name=self.CLUSTER_NAME,
            serve_nodes=SERVE_NODES,
        )

        klass = self._getTargetClass()
        cluster = klass.from_pb(cluster_pb, instance)
        self.assertTrue(isinstance(cluster, klass))
        self.assertTrue(cluster._instance is instance)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)

    def test_from_pb_bad_cluster_name(self):
        BAD_CLUSTER_NAME = 'INCORRECT_FORMAT'
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster_pb = _ClusterPB(name=BAD_CLUSTER_NAME)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test_from_pb_project_mistmatch(self):
        ALT_PROJECT = 'ALT_PROJECT'
        client = _Client(ALT_PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)

        cluster_pb = _ClusterPB(name=self.CLUSTER_NAME)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test_from_pb_instance_mistmatch(self):
        ALT_INSTANCE_ID = 'ALT_INSTANCE_ID'
        client = _Client(self.PROJECT)
        instance = _Instance(ALT_INSTANCE_ID, client)

        self.assertNotEqual(self.INSTANCE_ID, ALT_INSTANCE_ID)

        cluster_pb = _ClusterPB(name=self.CLUSTER_NAME)

        klass = self._getTargetClass()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test_name_property(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._makeOne(self.CLUSTER_ID, instance)
        self.assertEqual(cluster.name, self.CLUSTER_NAME)

    def test___eq__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._makeOne(self.CLUSTER_ID, instance)
        cluster2 = self._makeOne(self.CLUSTER_ID, instance)
        self.assertEqual(cluster1, cluster2)

    def test___eq__type_differ(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._makeOne(self.CLUSTER_ID, instance)
        cluster2 = object()
        self.assertNotEqual(cluster1, cluster2)

    def test___ne__same_value(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._makeOne(self.CLUSTER_ID, instance)
        cluster2 = self._makeOne(self.CLUSTER_ID, instance)
        comparison_val = (cluster1 != cluster2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._makeOne('cluster_id1', instance)
        cluster2 = self._makeOne('cluster_id2', instance)
        self.assertNotEqual(cluster1, cluster2)

    def test_reload(self):
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES

        SERVE_NODES = 31
        LOCATION = 'LOCATION'
        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._makeOne(self.CLUSTER_ID, instance)

        # Create request_pb
        request_pb = _GetClusterRequestPB(name=self.CLUSTER_NAME)

        # Create response_pb
        response_pb = _ClusterPB(
            serve_nodes=SERVE_NODES,
            location=LOCATION,
        )

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check Cluster optional config values before.
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

        # Perform the method and check the result.
        result = cluster.reload()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'GetCluster',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])

        # Check Cluster optional config values before.
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)
        self.assertEqual(cluster.location, LOCATION)

    def test_create(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import cluster as MUT

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._makeOne(self.CLUSTER_ID, instance)

        # Create request_pb. Just a mock since we monkey patch
        # _prepare_create_request
        request_pb = object()

        # Create response_pb
        OP_ID = 5678
        OP_NAME = (
            'operations/projects/%s/instances/%s/clusters/%s/operations/%d' %
            (self.PROJECT, self.INSTANCE_ID, self.CLUSTER_ID, OP_ID))
        response_pb = operations_pb2.Operation(name=OP_NAME)

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = MUT.Operation('create', OP_ID, cluster=cluster)

        # Create the mocks.
        prep_create_called = []

        def mock_prep_create_req(cluster):
            prep_create_called.append(cluster)
            return request_pb

        process_operation_called = []

        def mock_process_operation(operation_pb):
            process_operation_called.append(operation_pb)
            return OP_ID

        # Perform the method and check the result.
        with _Monkey(MUT, _prepare_create_request=mock_prep_create_req,
                     _process_operation=mock_process_operation):
            result = cluster.create()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'CreateCluster',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])
        self.assertEqual(prep_create_called, [cluster])
        self.assertEqual(process_operation_called, [response_pb])

    def test_update(self):
        from google.longrunning import operations_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import cluster as MUT

        SERVE_NODES = 81

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._makeOne(self.CLUSTER_ID, instance,
                                serve_nodes=SERVE_NODES)

        # Create request_pb
        request_pb = _ClusterPB(
            name=self.CLUSTER_NAME,
            serve_nodes=SERVE_NODES,
        )

        # Create response_pb
        response_pb = operations_pb2.Operation()

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        OP_ID = 5678
        expected_result = MUT.Operation('update', OP_ID, cluster=cluster)

        # Create mocks
        process_operation_called = []

        def mock_process_operation(operation_pb):
            process_operation_called.append(operation_pb)
            return OP_ID

        # Perform the method and check the result.
        with _Monkey(MUT, _process_operation=mock_process_operation):
            result = cluster.update()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'UpdateCluster',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])
        self.assertEqual(process_operation_called, [response_pb])

    def test_delete(self):
        from google.protobuf import empty_pb2
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(self.PROJECT, timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._makeOne(self.CLUSTER_ID, instance)

        # Create request_pb
        request_pb = _DeleteClusterRequestPB(name=self.CLUSTER_NAME)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = cluster.delete()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'DeleteCluster',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])


class Test__prepare_create_request(unittest2.TestCase):

    def _callFUT(self, cluster):
        from gcloud.bigtable.cluster import _prepare_create_request
        return _prepare_create_request(cluster)

    def test_it(self):
        from gcloud.bigtable.cluster import Cluster

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        CLUSTER_ID = 'cluster-id'
        SERVE_NODES = 8

        client = _Client(PROJECT)
        instance = _Instance(INSTANCE_ID, client)
        cluster = Cluster(CLUSTER_ID, instance,
                          serve_nodes=SERVE_NODES)

        request_pb = self._callFUT(cluster)

        self.assertEqual(request_pb.cluster_id, CLUSTER_ID)
        self.assertEqual(request_pb.parent, instance.name)
        self.assertEqual(request_pb.cluster.serve_nodes, SERVE_NODES)


class Test__parse_pb_any_to_native(unittest2.TestCase):

    def _callFUT(self, any_val, expected_type=None):
        from gcloud.bigtable.cluster import _parse_pb_any_to_native
        return _parse_pb_any_to_native(any_val, expected_type=expected_type)

    def test_with_known_type_url(self):
        from google.protobuf import any_pb2
        from gcloud._testing import _Monkey
        from gcloud.bigtable import cluster as MUT

        cell = _CellPB(
            timestamp_micros=0,
            value=b'foobar',
        )

        type_url = 'type.googleapis.com/' + cell.DESCRIPTOR.full_name
        fake_type_url_map = {type_url: cell.__class__}

        any_val = any_pb2.Any(
            type_url=type_url,
            value=cell.SerializeToString(),
        )
        with _Monkey(MUT, _TYPE_URL_MAP=fake_type_url_map):
            result = self._callFUT(any_val)

        self.assertEqual(result, cell)

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

        PROJECT = 'project'
        INSTANCE_ID = 'instance-id'
        CLUSTER_ID = 'cluster-id'
        EXPECTED_OPERATION_ID = 234
        OPERATION_NAME = (
            'operations/projects/%s/instances/%s/clusters/%s/operations/%d' %
            (PROJECT, INSTANCE_ID, CLUSTER_ID, EXPECTED_OPERATION_ID))

        operation_pb = operations_pb2.Operation(name=OPERATION_NAME)

        # Exectute method with mocks in place.
        operation_id = self._callFUT(operation_pb)

        # Check outputs.
        self.assertEqual(operation_id, EXPECTED_OPERATION_ID)

    def test_op_name_parsing_failure(self):
        from google.longrunning import operations_pb2

        operation_pb = operations_pb2.Operation(name='invalid')
        with self.assertRaises(ValueError):
            self._callFUT(operation_pb)


def _CellPB(*args, **kw):
    from gcloud.bigtable._generated_v2 import (
        data_pb2 as data_v2_pb2)
    return data_v2_pb2.Cell(*args, **kw)


def _ClusterPB(*args, **kw):
    from gcloud.bigtable._generated_v2 import (
        instance_pb2 as instance_v2_pb2)
    return instance_v2_pb2.Cluster(*args, **kw)


def _DeleteClusterRequestPB(*args, **kw):
    from gcloud.bigtable._generated_v2 import (
        bigtable_instance_admin_pb2 as messages_v2_pb2)
    return messages_v2_pb2.DeleteClusterRequest(*args, **kw)


def _GetClusterRequestPB(*args, **kw):
    from gcloud.bigtable._generated_v2 import (
        bigtable_instance_admin_pb2 as messages_v2_pb2)
    return messages_v2_pb2.GetClusterRequest(*args, **kw)


class _Instance(object):

    def __init__(self, instance_id, client):
        self.instance_id = instance_id
        self._client = client

    @property
    def name(self):
        return 'projects/%s/instances/%s' % (
            self._client.project, self.instance_id)

    def copy(self):
        return self.__class__(self.instance_id, self._client)

    def __eq__(self, other):
        return (other.instance_id == self.instance_id and
                other._client == self._client)


class _Client(object):

    def __init__(self, project, timeout_seconds=None):
        self.project = project
        self.project_name = 'projects/' + self.project
        self.timeout_seconds = timeout_seconds

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name and
                other.timeout_seconds == self.timeout_seconds)
