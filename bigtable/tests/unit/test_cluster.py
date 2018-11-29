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


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        return self.channel_stub.responses.pop()


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class TestCluster(unittest.TestCase):

    PROJECT = "project"
    INSTANCE_ID = "instance-id"
    LOCATION_ID = "location-id"
    CLUSTER_ID = "cluster-id"
    LOCATION_ID = "location-id"
    CLUSTER_NAME = (
        "projects/" + PROJECT + "/instances/" + INSTANCE_ID + "/clusters/" + CLUSTER_ID
    )
    LOCATION_PATH = "projects/" + PROJECT + "/locations/"
    SERVE_NODES = 5
    OP_ID = 5678
    OP_NAME = "operations/projects/{}/instances/{}/clusters/{}/operations/{}".format(
        PROJECT, INSTANCE_ID, CLUSTER_ID, OP_ID
    )

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

        cluster = self._make_one(self.CLUSTER_ID, instance)
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertIs(cluster._instance, instance)
        self.assertIsNone(cluster.location_id)
        self.assertIsNone(cluster.state)
        self.assertIsNone(cluster.serve_nodes)
        self.assertIsNone(cluster.default_storage_type)

    def test_constructor_non_default(self):
        from google.cloud.bigtable.enums import StorageType
        from google.cloud.bigtable.enums import Cluster

        STATE = Cluster.State.READY
        STORAGE_TYPE_SSD = StorageType.SSD
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        cluster = self._make_one(
            self.CLUSTER_ID,
            instance,
            location_id=self.LOCATION_ID,
            _state=STATE,
            serve_nodes=self.SERVE_NODES,
            default_storage_type=STORAGE_TYPE_SSD,
        )
        self.assertEqual(cluster.cluster_id, self.CLUSTER_ID)
        self.assertIs(cluster._instance, instance)
        self.assertEqual(cluster.location_id, self.LOCATION_ID)
        self.assertEqual(cluster.state, STATE)
        self.assertEqual(cluster.serve_nodes, self.SERVE_NODES)
        self.assertEqual(cluster.default_storage_type, STORAGE_TYPE_SSD)

    def test_name_property(self):
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance)

        self.assertEqual(cluster.name, self.CLUSTER_NAME)

    def test_from_pb_success(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable import enums

        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)

        location = self.LOCATION_PATH + self.LOCATION_ID
        state = enums.Cluster.State.RESIZING
        storage_type = enums.StorageType.SSD
        cluster_pb = data_v2_pb2.Cluster(
            name=self.CLUSTER_NAME,
            location=location,
            state=state,
            serve_nodes=self.SERVE_NODES,
            default_storage_type=storage_type,
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
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        bad_cluster_name = "BAD_NAME"

        cluster_pb = data_v2_pb2.Cluster(name=bad_cluster_name)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, None)

    def test_from_pb_instance_id_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        ALT_INSTANCE_ID = "ALT_INSTANCE_ID"
        client = _Client(self.PROJECT)
        instance = _Instance(ALT_INSTANCE_ID, client)

        self.assertNotEqual(self.INSTANCE_ID, ALT_INSTANCE_ID)
        cluster_pb = data_v2_pb2.Cluster(name=self.CLUSTER_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(cluster_pb, instance)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        ALT_PROJECT = "ALT_PROJECT"
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
        comparison_val = cluster1 != cluster2
        self.assertFalse(comparison_val)

    def test___ne__(self):
        client = _Client(self.PROJECT)
        instance = _Instance(self.INSTANCE_ID, client)
        cluster1 = self._make_one("cluster_id1", instance, self.LOCATION_ID)
        cluster2 = self._make_one("cluster_id2", instance, self.LOCATION_ID)
        self.assertNotEqual(cluster1, cluster2)

    def test_reload(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable.enums import StorageType
        from google.cloud.bigtable.enums import Cluster

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        STORAGE_TYPE_SSD = StorageType.SSD
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(
            self.CLUSTER_ID,
            instance,
            location_id=self.LOCATION_ID,
            serve_nodes=self.SERVE_NODES,
            default_storage_type=STORAGE_TYPE_SSD,
        )

        # Create response_pb
        LOCATION_ID_FROM_SERVER = "new-location-id"
        STATE = Cluster.State.READY
        SERVE_NODES_FROM_SERVER = 10
        STORAGE_TYPE_FROM_SERVER = StorageType.HDD

        response_pb = data_v2_pb2.Cluster(
            name=cluster.name,
            location=self.LOCATION_PATH + LOCATION_ID_FROM_SERVER,
            state=STATE,
            serve_nodes=SERVE_NODES_FROM_SERVER,
            default_storage_type=STORAGE_TYPE_FROM_SERVER,
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.transport
        instance_stub.get_cluster.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check Cluster optional config values before.
        self.assertEqual(cluster.location_id, self.LOCATION_ID)
        self.assertIsNone(cluster.state)
        self.assertEqual(cluster.serve_nodes, self.SERVE_NODES)
        self.assertEqual(cluster.default_storage_type, STORAGE_TYPE_SSD)

        # Perform the method and check the result.
        result = cluster.reload()
        self.assertEqual(result, expected_result)
        self.assertEqual(cluster.location_id, LOCATION_ID_FROM_SERVER)
        self.assertEqual(cluster.state, STATE)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES_FROM_SERVER)
        self.assertEqual(cluster.default_storage_type, STORAGE_TYPE_FROM_SERVER)

    def test_exists(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable.instance import Instance
        from google.api_core import exceptions

        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock()
        )
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = Instance(self.INSTANCE_ID, client)

        # Create response_pb
        cluster_name = client.instance_admin_client.cluster_path(
            self.PROJECT, self.INSTANCE_ID, self.CLUSTER_ID
        )
        response_pb = data_v2_pb2.Cluster(name=cluster_name)

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.transport
        instance_stub.get_cluster.side_effect = [
            response_pb,
            exceptions.NotFound("testing"),
            exceptions.BadRequest("testing"),
        ]

        # Perform the method and check the result.
        non_existing_cluster_id = "cluster-id-2"
        alt_cluster_1 = self._make_one(self.CLUSTER_ID, instance)
        alt_cluster_2 = self._make_one(non_existing_cluster_id, instance)
        self.assertTrue(alt_cluster_1.exists())
        self.assertFalse(alt_cluster_2.exists())
        with self.assertRaises(exceptions.BadRequest):
            alt_cluster_1.exists()

    def test_create(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable_admin_v2.types import instance_pb2
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as instance_v2_pb2,
        )
        from google.cloud.bigtable.enums import StorageType

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        STORAGE_TYPE_SSD = StorageType.SSD
        LOCATION = self.LOCATION_PATH + self.LOCATION_ID
        instance = Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(
            self.CLUSTER_ID,
            instance,
            location_id=self.LOCATION_ID,
            serve_nodes=self.SERVE_NODES,
            default_storage_type=STORAGE_TYPE_SSD,
        )
        expected_request_cluster = instance_pb2.Cluster(
            location=LOCATION,
            serve_nodes=cluster.serve_nodes,
            default_storage_type=cluster.default_storage_type,
        )
        expected_request = instance_v2_pb2.CreateClusterRequest(
            parent=instance.name,
            cluster_id=self.CLUSTER_ID,
            cluster=expected_request_cluster,
        )

        metadata = messages_v2_pb2.CreateClusterMetadata(request_time=NOW_PB)
        type_url = "type.googleapis.com/{}".format(
            messages_v2_pb2.CreateClusterMetadata.DESCRIPTOR.full_name
        )
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(type_url=type_url, value=metadata.SerializeToString()),
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[response_pb])
        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            channel=channel
        )
        client._instance_admin_client = api

        # Perform the method and check the result.
        result = cluster.create()
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata, messages_v2_pb2.CreateClusterMetadata)

    def test_update(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable_admin_v2.types import instance_pb2
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable.enums import StorageType

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        STORAGE_TYPE_SSD = StorageType.SSD
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(
            self.CLUSTER_ID,
            instance,
            location_id=self.LOCATION_ID,
            serve_nodes=self.SERVE_NODES,
            default_storage_type=STORAGE_TYPE_SSD,
        )
        # Create expected_request
        expected_request = instance_pb2.Cluster(
            name=cluster.name, serve_nodes=self.SERVE_NODES
        )

        metadata = messages_v2_pb2.UpdateClusterMetadata(request_time=NOW_PB)
        type_url = "type.googleapis.com/{}".format(
            messages_v2_pb2.UpdateClusterMetadata.DESCRIPTOR.full_name
        )
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(type_url=type_url, value=metadata.SerializeToString()),
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[response_pb])
        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            channel=channel
        )
        client._instance_admin_client = api

        # Perform the method and check the result.
        result = cluster.update()
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata, messages_v2_pb2.UpdateClusterMetadata)

    def test_delete(self):
        from google.protobuf import empty_pb2
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = _Instance(self.INSTANCE_ID, client)
        cluster = self._make_one(self.CLUSTER_ID, instance, self.LOCATION_ID)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.transport
        instance_stub.delete_cluster.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = cluster.delete()

        self.assertEqual(result, expected_result)


class _Instance(object):
    def __init__(self, instance_id, client):
        self.instance_id = instance_id
        self._client = client

    def __eq__(self, other):
        return other.instance_id == self.instance_id and other._client == self._client


class _Client(object):
    def __init__(self, project):
        self.project = project
        self.project_name = "projects/" + self.project
        self._operations_stub = mock.sentinel.operations_stub

    def __eq__(self, other):
        return other.project == self.project and other.project_name == self.project_name
