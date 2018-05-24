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

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

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

    def test_name_property(self):
        from google.cloud.bigtable.instance import Instance

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = Instance(self.INSTANCE_ID, client)
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
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        LOCATION = 'LOCATION'
        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance)

        # Create response_pb
        response_pb = _ClusterPB(
            serve_nodes=DEFAULT_SERVE_NODES,
            location=LOCATION,
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.bigtable_instance_admin_stub
        instance_stub.GetCluster.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check Cluster optional config values before.
        self.assertEqual(cluster.serve_nodes, DEFAULT_SERVE_NODES)

        # Perform the method and check the result.
        result = cluster.reload()
        self.assertEqual(result, expected_result)

    def test_create(self):
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance)

        # Create response_pb
        OP_ID = 5678
        OP_NAME = (
            'operations/projects/%s/instances/%s/clusters/%s/operations/%d' %
            (self.PROJECT, self.INSTANCE_ID, self.CLUSTER_ID, OP_ID))
        response_pb = operations_pb2.Operation(name=OP_NAME)

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.bigtable_instance_admin_stub
        instance_stub.CreateCluster.side_effect = [response_pb]

        # Perform the method and check the result.
        result = cluster.create()

        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, OP_NAME)
        self.assertIsNone(result.metadata)

    def test_update(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)

        SERVE_NODES = 81

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = Instance(self.INSTANCE_ID, client)
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
        client._instance_admin_client = api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.bigtable_instance_admin_stub
        instance_stub.UpdateCluster.side_effect = [response_pb]

        result = cluster.update()

        self.assertIsInstance(result, operation.Operation)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.UpdateClusterMetadata)

        self.assertIsInstance(request_pb, data_v2_pb2.Cluster)
        self.assertEqual(request_pb.name, self.CLUSTER_NAME)
        self.assertEqual(request_pb.serve_nodes, SERVE_NODES)

    def test_delete(self):
        from google.protobuf import empty_pb2
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance,
                                 serve_nodes=DEFAULT_SERVE_NODES)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.bigtable_instance_admin_stub
        instance_stub.DeleteCluster.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = cluster.delete()

        self.assertEqual(result, expected_result)


def _ClusterPB(*args, **kw):
    from google.cloud.bigtable_admin_v2.proto import (
        instance_pb2 as instance_v2_pb2)

    return instance_v2_pb2.Cluster(*args, **kw)


class _Instance(object):

    def __init__(self, instance_id, client):
        self.instance_id = instance_id
        self._client = client

    def __eq__(self, other):
        return (other.instance_id == self.instance_id and
                other._client == self._client)


class _Client(object):

    def __init__(self, project):
        self.project = project
        self.project_name = 'projects/' + self.project
        self._operations_stub = mock.sentinel.operations_stub

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name)
