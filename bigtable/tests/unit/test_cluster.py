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
    LOCATION_ID = 'location-id'
    CLUSTER_ID = 'cluster-id'
    LOCATION_ID = 'location-id'
    CLUSTER_NAME = ('projects/' + PROJECT +
                    '/instances/' + INSTANCE_ID +
                    '/clusters/' + CLUSTER_ID)
    LOCATION_PATH = 'projects/' + PROJECT + '/locations/'
    SERVE_NODES = 5

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
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertIs(cluster._instance, instance)
        self.assertIsNone(cluster.location_id)
        self.assertIsNone(cluster.serve_nodes)
        self.assertIsNone(cluster.default_storage_type)

    def test_constructor_non_default(self):
        from google.cloud.bigtable.enums import StorageType
        STORAGE_TYPE_SSD = StorageType.SSD
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._make_one(self.CLUSTER_ID, instance,
                                 location_id=self.LOCATION_ID,
                                 serve_nodes=self.SERVE_NODES,
                                 default_storage_type=STORAGE_TYPE_SSD)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertIs(cluster._instance, instance)
        self.assertEqual(cluster.location_id, self.LOCATION_ID)
        self.assertEqual(cluster.serve_nodes, self.SERVE_NODES)
        self.assertEqual(cluster.default_storage_type, STORAGE_TYPE_SSD)

    def test_name_property(self):
        from google.cloud.bigtable.instance import Instance

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)

        self.assertEqual(cluster.name, self.CLUSTER_NAME)

    def test_update_from_pb(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        from google.cloud.bigtable import enums

        location = self.LOCATION_PATH + self.LOCATION_ID
        state = enums.ClusterState.READY
        storage_type = enums.StorageType.SSD
        cluster_pb = data_v2_pb2.Cluster(
            location=location,
            state=state,
            serve_nodes=self.SERVE_NODES,
            default_storage_type=storage_type
        )

        cluster = self._make_one(None, None)
        self.assertIsNone(cluster.location_id)
        self.assertIsNone(cluster.state)
        self.assertIsNone(cluster.serve_nodes)
        self.assertIsNone(cluster.default_storage_type)
        cluster._update_from_pb(cluster_pb)
        self.assertEqual(cluster.location_id, self.LOCATION_ID)
        self.assertEqual(cluster.state, state)
        self.assertEqual(cluster.serve_nodes, self.SERVE_NODES)
        self.assertEqual(cluster.default_storage_type, storage_type)

    def test_update_from_pb_defaults(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable.enums import ClusterState
        from google.cloud.bigtable.enums import StorageType

        cluster_pb = data_v2_pb2.Cluster()

        cluster = self._make_one(None, None)
        self.assertIsNone(cluster.location_id)
        self.assertIsNone(cluster.state)
        self.assertIsNone(cluster.serve_nodes)
        self.assertIsNone(cluster.default_storage_type)
        cluster._update_from_pb(cluster_pb)
        self.assertFalse(cluster.location_id)
        self.assertEqual(cluster.state, ClusterState.STATE_NOT_KNOWN)
        self.assertEqual(cluster.serve_nodes, 0)
        self.assertEqual(cluster.default_storage_type, StorageType.UNSPECIFIED)

    def test_from_pb_success(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable import enums

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        location = self.LOCATION_PATH + self.LOCATION_ID
        state = enums.ClusterState.RESIZING
        storage_type = enums.StorageType.SSD
        cluster_pb = data_v2_pb2.Cluster(
            name=self.CLUSTER_NAME,
            location=location,
            state=state,
            serve_nodes=self.SERVE_NODES,
            default_storage_type=storage_type
        )

        klass = self._get_target_class()
        cluster = klass.from_pb(cluster_pb, instance)
        self.assertIsInstance(cluster, klass)
        self.assertEqual(cluster._instance, instance)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertEqual(cluster.location_id, self.LOCATION_ID)
        self.assertEqual(cluster.state, state)
        self.assertEqual(cluster.serve_nodes, self.SERVE_NODES)
        self.assertEqual(cluster.default_storage_type, storage_type)

    def test_from_pb_bad_cluster_name(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        bad_cluster_name = 'BAD_NAME'

        cluster_pb = data_v2_pb2.Cluster(name=bad_cluster_name)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, None)

    def test_from_pb_instance_id_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        ALT_INSTANCE_ID = 'ALT_INSTANCE_ID'
        client = _Client(self.PROJECT)
        instance = _Instance(ALT_INSTANCE_ID, client)

        self.assertNotEqual(self.INSTANCE_ID, ALT_INSTANCE_ID)
        cluster_pb = data_v2_pb2.Cluster(name=self.CLUSTER_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        ALT_PROJECT = 'ALT_PROJECT'
        client = _Client(project=ALT_PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)
        cluster_pb = data_v2_pb2.Cluster(name=self.CLUSTER_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test___eq__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)
        cluster2 = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)
        self.assertEqual(cluster1, cluster2)

    def test___eq__type_differ(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)
        cluster2 = object()
        self.assertNotEqual(cluster1, cluster2)

    def test___ne__same_value(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)
        cluster2 = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)
        comparison_val = (cluster1 != cluster2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one('cluster_id1', instance, self.LOCATION_ID)
        cluster2 = self._make_one('cluster_id2', instance, self.LOCATION_ID)
        self.assertNotEqual(cluster1, cluster2)

    def test_reload(self):
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable.enums import StorageType

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        STORAGE_TYPE_SSD = StorageType.SSD
        instance = Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance,
                                 location_id=self.LOCATION_ID,
                                 serve_nodes=self.SERVE_NODES,
                                 default_storage_type=STORAGE_TYPE_SSD)

        # Create response_pb
        LOCATION_ID_FROM_SERVER = 'new-location-id'
        SERVE_NODES_FROM_SERVER = 10
        STORAGE_TYPE_FROM_SERVER = StorageType.HDD

        response_pb = data_v2_pb2.Cluster(
            location=self.LOCATION_PATH + LOCATION_ID_FROM_SERVER,
            serve_nodes=SERVE_NODES_FROM_SERVER,
            default_storage_type=STORAGE_TYPE_FROM_SERVER
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.bigtable_instance_admin_stub
        instance_stub.GetCluster.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check Cluster optional config values before.
        self.assertEqual(cluster.location_id, self.LOCATION_ID)
        self.assertEqual(cluster.serve_nodes, self.SERVE_NODES)
        self.assertEqual(cluster.default_storage_type, STORAGE_TYPE_SSD)

        # Perform the method and check the result.
        result = cluster.reload()
        self.assertEqual(result, expected_result)
        self.assertEqual(cluster.location_id, LOCATION_ID_FROM_SERVER)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES_FROM_SERVER)
        self.assertEqual(cluster.default_storage_type,
                         STORAGE_TYPE_FROM_SERVER)

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
        cluster = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)

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
                                 self.LOCATION_ID, serve_nodes=SERVE_NODES)

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
                                 self.LOCATION_ID,
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
