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


class TestCluster(unittest.TestCase):

    PROJECT = 'project'
    INSTANCE_ID = 'instance-id'
    CLUSTER_ID = 'cluster-id'
    CLUSTER_NAME = ('projects/' + PROJECT +
                    '/instances/' + INSTANCE_ID +
                    '/clusters/' + CLUSTER_ID)

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.cluster import Cluster

        return Cluster

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor_defaults(self):
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._make_one(self.CLUSTER_ID, instance)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertIs(cluster._instance, instance)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

    def test_constructor_non_default(self):
        SERVE_NODES = 8
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._make_one(self.CLUSTER_ID, instance,
                                 serve_nodes=SERVE_NODES)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertIs(cluster._instance, instance)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)

    def test_copy(self):
        SERVE_NODES = 8

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance,
                                 serve_nodes=SERVE_NODES)
        new_cluster = cluster.copy()

        # Make sure the client copy succeeded.
        self.assertIsNot(new_cluster._instance, instance)
        self.assertEqual(new_cluster.serve_nodes, SERVE_NODES)
        # Make sure the client got copied to a new instance.
        self.assertIsNot(cluster, new_cluster)
        self.assertEqual(cluster, new_cluster)

    def test__update_from_pb_success(self):
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES

        SERVE_NODES = 8
        cluster_pb = _ClusterPB(
            serve_nodes=SERVE_NODES,
        )
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._make_one(self.CLUSTER_ID, instance)
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)
        cluster._update_from_pb(cluster_pb)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)

    def test__update_from_pb_no_serve_nodes(self):
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES

        cluster_pb = _ClusterPB()
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._make_one(self.CLUSTER_ID, instance)
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

        klass = self._get_target_class()
        cluster = klass.from_pb(cluster_pb, instance)
        self.assertIsInstance(cluster, klass)
        self.assertIs(cluster._instance, instance)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)

    def test_from_pb_bad_cluster_name(self):
        BAD_CLUSTER_NAME = 'INCORRECT_FORMAT'
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster_pb = _ClusterPB(name=BAD_CLUSTER_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test_from_pb_project_mistmatch(self):
        ALT_PROJECT = 'ALT_PROJECT'
        client = _Client(ALT_PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)

        cluster_pb = _ClusterPB(name=self.CLUSTER_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test_from_pb_instance_mistmatch(self):
        ALT_INSTANCE_ID = 'ALT_INSTANCE_ID'
        client = _Client(self.PROJECT)
        instance = _Instance(ALT_INSTANCE_ID, client)

        self.assertNotEqual(self.INSTANCE_ID, ALT_INSTANCE_ID)

        cluster_pb = _ClusterPB(name=self.CLUSTER_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test_name_property(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._make_one(self.CLUSTER_ID, instance)
        self.assertEqual(cluster.name, self.CLUSTER_NAME)

    def test___eq__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one(self.CLUSTER_ID, instance)
        cluster2 = self._make_one(self.CLUSTER_ID, instance)
        self.assertEqual(cluster1, cluster2)

    def test___eq__type_differ(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one(self.CLUSTER_ID, instance)
        cluster2 = object()
        self.assertNotEqual(cluster1, cluster2)

    def test___ne__same_value(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one(self.CLUSTER_ID, instance)
        cluster2 = self._make_one(self.CLUSTER_ID, instance)
        comparison_val = (cluster1 != cluster2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one('cluster_id1', instance)
        cluster2 = self._make_one('cluster_id2', instance)
        self.assertNotEqual(cluster1, cluster2)

    def test_reload(self):
        from unit_tests._testing import _FakeStub
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES

        SERVE_NODES = 31
        LOCATION = 'LOCATION'
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance)

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
            (request_pb,),
            {},
        )])

        # Check Cluster optional config values before.
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)
        self.assertEqual(cluster.location, LOCATION)

    def test_create(self):
        from google.longrunning import operations_pb2
        from google.cloud.operation import Operation
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from unit_tests._testing import _FakeStub

        SERVE_NODES = 4
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(
            self.CLUSTER_ID, instance, serve_nodes=SERVE_NODES)

        # Create response_pb
        OP_ID = 5678
        OP_NAME = (
            'operations/projects/%s/instances/%s/clusters/%s/operations/%d' %
            (self.PROJECT, self.INSTANCE_ID, self.CLUSTER_ID, OP_ID))
        response_pb = operations_pb2.Operation(name=OP_NAME)

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        # Perform the method and check the result.
        result = cluster.create()

        self.assertIsInstance(result, Operation)
        self.assertEqual(result.name, OP_NAME)
        self.assertIs(result.target, cluster)
        self.assertIs(result.client, client)
        self.assertIsNone(result.metadata)
        self.assertEqual(result.caller_metadata,
                         {'request_type': 'CreateCluster'})

        self.assertEqual(len(stub.method_calls), 1)
        api_name, args, kwargs = stub.method_calls[0]
        self.assertEqual(api_name, 'CreateCluster')
        request_pb, = args
        self.assertIsInstance(request_pb,
                              messages_v2_pb2.CreateClusterRequest)
        self.assertEqual(request_pb.parent, instance.name)
        self.assertEqual(request_pb.cluster_id, self.CLUSTER_ID)
        self.assertEqual(request_pb.cluster.serve_nodes, SERVE_NODES)
        self.assertEqual(kwargs, {})

    def test_update(self):
        import datetime
        from google.longrunning import operations_pb2
        from google.cloud.operation import Operation
        from google.protobuf.any_pb2 import Any
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from unit_tests._testing import _FakeStub

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)

        SERVE_NODES = 81

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance,
                                 serve_nodes=SERVE_NODES)

        # Create request_pb
        request_pb = _ClusterPB(
            name=self.CLUSTER_NAME,
            serve_nodes=SERVE_NODES,
        )

        # Create response_pb
        OP_ID = 5678
        OP_NAME = (
            'operations/projects/%s/instances/%s/clusters/%s/operations/%d' %
            (self.PROJECT, self.INSTANCE_ID, self.CLUSTER_ID, OP_ID))
        metadata = messages_v2_pb2.UpdateClusterMetadata(request_time=NOW_PB)
        type_url = 'type.googleapis.com/%s' % (
            messages_v2_pb2.UpdateClusterMetadata.DESCRIPTOR.full_name,)
        response_pb = operations_pb2.Operation(
            name=OP_NAME,
            metadata=Any(
                type_url=type_url,
                value=metadata.SerializeToString()
            )
        )

        # Patch the stub used by the API method.
        client._instance_stub = stub = _FakeStub(response_pb)

        result = cluster.update()

        self.assertIsInstance(result, Operation)
        self.assertEqual(result.name, OP_NAME)
        self.assertIs(result.target, cluster)
        self.assertIs(result.client, client)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.UpdateClusterMetadata)
        self.assertEqual(result.metadata.request_time, NOW_PB)
        self.assertEqual(result.caller_metadata,
                         {'request_type': 'UpdateCluster'})

        self.assertEqual(len(stub.method_calls), 1)
        api_name, args, kwargs = stub.method_calls[0]
        self.assertEqual(api_name, 'UpdateCluster')
        request_pb, = args
        self.assertIsInstance(request_pb, data_v2_pb2.Cluster)
        self.assertEqual(request_pb.name, self.CLUSTER_NAME)
        self.assertEqual(request_pb.serve_nodes, SERVE_NODES)
        self.assertEqual(kwargs, {})

    def test_delete(self):
        from google.protobuf import empty_pb2
        from unit_tests._testing import _FakeStub

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance)

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
            (request_pb,),
            {},
        )])


class Test__prepare_create_request(unittest.TestCase):

    def _call_fut(self, cluster):
        from google.cloud.bigtable.cluster import _prepare_create_request

        return _prepare_create_request(cluster)

    def test_it(self):
        from google.cloud.bigtable.cluster import Cluster

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        CLUSTER_ID = 'cluster-id'
        SERVE_NODES = 8

        client = _Client(PROJECT)
        instance = _Instance(INSTANCE_ID, client)
        cluster = Cluster(CLUSTER_ID, instance,
                          serve_nodes=SERVE_NODES)

        request_pb = self._call_fut(cluster)

        self.assertEqual(request_pb.cluster_id, CLUSTER_ID)
        self.assertEqual(request_pb.parent, instance.name)
        self.assertEqual(request_pb.cluster.serve_nodes, SERVE_NODES)


def _ClusterPB(*args, **kw):
    from google.cloud.bigtable._generated import (
        instance_pb2 as instance_v2_pb2)

    return instance_v2_pb2.Cluster(*args, **kw)


def _DeleteClusterRequestPB(*args, **kw):
    from google.cloud.bigtable._generated import (
        bigtable_instance_admin_pb2 as messages_v2_pb2)

    return messages_v2_pb2.DeleteClusterRequest(*args, **kw)


def _GetClusterRequestPB(*args, **kw):
    from google.cloud.bigtable._generated import (
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

    def __init__(self, project):
        self.project = project
        self.project_name = 'projects/' + self.project

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name)
