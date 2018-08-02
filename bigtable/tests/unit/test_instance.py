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
from google.cloud.bigtable.cluster import Cluster


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

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)


class TestInstance(unittest.TestCase):

    PROJECT = 'project'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = 'projects/' + PROJECT + '/instances/' + INSTANCE_ID
    LOCATION_ID = 'locid'
    LOCATION = 'projects/' + PROJECT + '/locations/' + LOCATION_ID
    APP_PROFILE_PATH = (
            'projects/' + PROJECT + '/instances/' + INSTANCE_ID
            + '/appProfiles/')
    DISPLAY_NAME = 'display_name'
    LABELS = {'foo': 'bar'}
    OP_ID = 8915
    OP_NAME = ('operations/projects/{}/instances/{}operations/{}'
               .format(PROJECT, INSTANCE_ID, OP_ID))
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
        instance = self._make_one(self.INSTANCE_ID, client)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertIsNone(instance.type_)
        self.assertIsNone(instance.labels)
        self.assertIs(instance._client, client)
        self.assertIsNone(instance.state)

    def test_constructor_non_default(self):
        from google.cloud.bigtable import enums

        instance_type = enums.Instance.Type.DEVELOPMENT
        state = enums.Instance.State.READY
        labels = {'test': 'test'}
        client = object()

        instance = self._make_one(self.INSTANCE_ID, client,
                                  display_name=self.DISPLAY_NAME,
                                  instance_type=instance_type,
                                  labels=labels, _state=state)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.type_, instance_type)
        self.assertEqual(instance.labels, labels)
        self.assertIs(instance._client, client)
        self.assertEqual(instance.state, state)

    def test_table_factory(self):
        from google.cloud.bigtable.table import Table

        app_profile_id = 'appProfileId1262094415'
        instance = self._make_one(self.INSTANCE_ID, None)

        table = instance.table(self.TABLE_ID, app_profile_id=app_profile_id)
        self.assertIsInstance(table, Table)
        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertEqual(table._instance, instance)
        self.assertEqual(table._app_profile_id, app_profile_id)

    def test_cluster_factory(self):
        from google.cloud.bigtable import enums

        CLUSTER_ID = '{}-cluster'.format(self.INSTANCE_ID)
        LOCATION_ID = 'us-central1-c'
        SERVE_NODES = 3
        STORAGE_TYPE = enums.StorageType.HDD

        instance = self._make_one(self.INSTANCE_ID, None)

        cluster = instance.cluster(CLUSTER_ID, location_id=LOCATION_ID,
                                   serve_nodes=SERVE_NODES,
                                   default_storage_type=STORAGE_TYPE)
        self.assertIsInstance(cluster, Cluster)
        self.assertEqual(cluster.cluster_id, CLUSTER_ID)
        self.assertEqual(cluster.location_id, LOCATION_ID)
        self.assertIsNone(cluster._state)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)
        self.assertEqual(cluster.default_storage_type, STORAGE_TYPE)

    def test_list_clusters(self):
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable.instance import Cluster

        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                mock.Mock()))
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = Instance(self.INSTANCE_ID, client)

        failed_location = 'FAILED'
        cluster_id1 = 'cluster-id1'
        cluster_id2 = 'ckuster-id2'
        cluster_name1 = (client.instance_admin_client.cluster_path(
                         self.PROJECT, self.INSTANCE_ID, cluster_id1))
        cluster_name2 = (client.instance_admin_client.cluster_path(
                         self.PROJECT, self.INSTANCE_ID, cluster_id2))

        # Create response_pb
        response_pb = messages_v2_pb2.ListClustersResponse(
            failed_locations=[
                failed_location
            ],
            clusters=[
                data_v2_pb2.Cluster(
                    name=cluster_name1,
                ),
                data_v2_pb2.Cluster(
                    name=cluster_name2,
                ),
            ],
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.bigtable_instance_admin_stub
        instance_stub.ListClusters.side_effect = [response_pb]

        # Perform the method and check the result.
        clusters, failed_locations = instance.list_clusters()

        cluster_1, cluster_2 = clusters

        self.assertIsInstance(cluster_1, Cluster)
        self.assertEqual(cluster_1.name, cluster_name1)

        self.assertIsInstance(cluster_2, Cluster)
        self.assertEqual(cluster_2.name, cluster_name2)

        self.assertEqual(failed_locations, [failed_location])

    def test__update_from_pb_success(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable import enums

        instance_type = enums.Instance.Type.PRODUCTION
        state = enums.Instance.State.READY
        instance_pb = data_v2_pb2.Instance(
            display_name=self.DISPLAY_NAME,
            type=instance_type,
            labels=self.LABELS,
            state=state
        )

        instance = self._make_one(None, None)
        self.assertIsNone(instance.display_name)
        self.assertIsNone(instance.type_)
        self.assertIsNone(instance.labels)
        instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.type_, instance_type)
        self.assertEqual(instance.labels, self.LABELS)
        self.assertEqual(instance._state, state)

    def test__update_from_pb_success_defaults(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable import enums

        instance_pb = data_v2_pb2.Instance(
            display_name=self.DISPLAY_NAME,
        )

        instance = self._make_one(None, None)
        self.assertIsNone(instance.display_name)
        self.assertIsNone(instance.type_)
        self.assertIsNone(instance.labels)
        instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.type_,
                         enums.Instance.Type.UNSPECIFIED)
        self.assertFalse(instance.labels)

    def test__update_from_pb_no_display_name(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)

        instance_pb = data_v2_pb2.Instance()
        instance = self._make_one(None, None)
        self.assertIsNone(instance.display_name)
        with self.assertRaises(ValueError):
            instance._update_from_pb(instance_pb)

    def test_from_pb_success(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable import enums

        client = _Client(project=self.PROJECT)

        instance_type = enums.Instance.Type.PRODUCTION
        state = enums.Instance.State.READY
        instance_pb = data_v2_pb2.Instance(
            name=self.INSTANCE_NAME,
            display_name=self.INSTANCE_ID,
            type=instance_type,
            labels=self.LABELS,
            state=state
        )

        klass = self._get_target_class()
        instance = klass.from_pb(instance_pb, client)
        self.assertIsInstance(instance, klass)
        self.assertEqual(instance._client, client)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.type_, instance_type)
        self.assertEqual(instance.labels, self.LABELS)
        self.assertEqual(instance._state, state)

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
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)

        # Patch the the API method.
        client._instance_admin_client = api

        instance = self._make_one(self.INSTANCE_ID, client)
        self.assertEqual(instance.name, self.INSTANCE_NAME)

    def test___eq__(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client)
        instance2 = self._make_one(self.INSTANCE_ID, client)
        self.assertEqual(instance1, instance2)

    def test___eq__type_differ(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client)
        instance2 = object()
        self.assertNotEqual(instance1, instance2)

    def test___ne__same_value(self):
        client = object()
        instance1 = self._make_one(self.INSTANCE_ID, client)
        instance2 = self._make_one(self.INSTANCE_ID, client)
        comparison_val = (instance1 != instance2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        instance1 = self._make_one('instance_id1', 'client1')
        instance2 = self._make_one('instance_id2', 'client2')
        self.assertNotEqual(instance1, instance2)

    def test_reload(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.cloud.bigtable import enums

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        # Create response_pb
        DISPLAY_NAME = u'hey-hi-hello'
        instance_type = enums.Instance.Type.PRODUCTION
        response_pb = data_v2_pb2.Instance(
            display_name=DISPLAY_NAME,
            type=instance_type,
            labels=self.LABELS
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        bigtable_instance_stub = (
            client._instance_admin_client.bigtable_instance_admin_stub)
        bigtable_instance_stub.GetInstance.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check Instance optional config values before.
        self.assertEqual(instance.display_name, self.INSTANCE_ID)

        # Perform the method and check the result.
        result = instance.reload()
        self.assertEqual(result, expected_result)

        # Check Instance optional config values before.
        self.assertEqual(instance.display_name, DISPLAY_NAME)

    def test_create_check_conflicts(self):
        instance = self._make_one(self.INSTANCE_ID, None)
        with self.assertRaises(ValueError):
            instance.create(location_id=self.LOCATION_ID,
                            clusters=[object(), object()])
        with self.assertRaises(ValueError):
            instance.create(serve_nodes=3,
                            clusters=[object(), object()])
        with self.assertRaises(ValueError):
            instance.create(default_storage_type=1,
                            clusters=[object(), object()])

    def test_create(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable import enums
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client,
                                  self.DISPLAY_NAME,
                                  enums.Instance.Type.PRODUCTION,
                                  self.LABELS)

        # Create response_pb
        metadata = messages_v2_pb2.CreateInstanceMetadata(request_time=NOW_PB)
        type_url = 'type.googleapis.com/{}'.format(
            messages_v2_pb2.CreateInstanceMetadata.DESCRIPTOR.full_name)
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(
                type_url=type_url,
                value=metadata.SerializeToString(),
            )
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[response_pb])
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                channel=channel))
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        serve_nodes = 3
        cluster_id = '{}-cluster'.format(self.INSTANCE_ID)
        # cluster = instance.cluster(cluster_id, location_id=self.LOCATION_ID,
        #                            serve_nodes=serve_nodes)
        # result = instance.create(clusters=[cluster])

        # TODO: replace this example with above once the otpion is removed
        # from instance.create() method
        result = instance.create(location_id=self.LOCATION_ID,
                                 serve_nodes=serve_nodes)

        actual_request = channel.requests[0][1]

        cluster = self._create_cluster_pb(
            instance_api, cluster_id, self.LOCATION_ID, serve_nodes,
            enums.StorageType.UNSPECIFIED)

        expected_request = self._create_instance_request({cluster_id: cluster})
        self.assertEqual(expected_request, actual_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.CreateInstanceMetadata)

    def test_create_w_clusters(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable import enums
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client,
                                  self.DISPLAY_NAME,
                                  enums.Instance.Type.PRODUCTION,
                                  self.LABELS)

        # Create response_pb
        metadata = messages_v2_pb2.CreateInstanceMetadata(request_time=NOW_PB)
        type_url = 'type.googleapis.com/{}'.format(
            messages_v2_pb2.CreateInstanceMetadata.DESCRIPTOR.full_name)
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(
                type_url=type_url,
                value=metadata.SerializeToString(),
            )
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[response_pb])
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                channel=channel))
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        cluster_id_1 = 'cluster-1'
        cluster_id_2 = 'cluster-2'
        location_id_1 = 'location-id-1'
        location_id_2 = 'location-id-2'
        serve_nodes_1 = 3
        serve_nodes_2 = 5
        clusters = [
            Cluster(cluster_id_1, instance,
                    location_id=location_id_1,
                    serve_nodes=serve_nodes_1),
            Cluster(cluster_id_2, instance,
                    location_id=location_id_2,
                    serve_nodes=serve_nodes_2)]
        result = instance.create(clusters=clusters)
        actual_request = channel.requests[0][1]

        cluster_1_pb = self._create_cluster_pb(
            instance_api, cluster_id_1, location_id_1, serve_nodes_1,
            enums.StorageType.UNSPECIFIED)

        cluster_2_pb = self._create_cluster_pb(
            instance_api, cluster_id_2, location_id_2, serve_nodes_2,
            enums.StorageType.UNSPECIFIED)

        expected_request = self._create_instance_request(
            {cluster_id_1: cluster_1_pb,
             cluster_id_2: cluster_2_pb}
        )
        self.assertEqual(expected_request, actual_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.CreateInstanceMetadata)

    def _create_cluster_pb(self, instance_api, cluster_id, location_id,
                           serve_nodes, storage_type):
        from google.cloud.bigtable_admin_v2.types import instance_pb2

        location = instance_api.location_path(
            self.PROJECT, location_id)
        return instance_pb2.Cluster(
            location=location,
            serve_nodes=serve_nodes,
            default_storage_type=storage_type)

    def _create_instance_request(self, clusters):
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud.bigtable_admin_v2.types import instance_pb2
        from google.cloud.bigtable import enums

        instance = instance_pb2.Instance(display_name=self.DISPLAY_NAME,
                                         type=enums.Instance.Type.PRODUCTION,
                                         labels=self.LABELS)

        return messages_v2_pb2.CreateInstanceRequest(
            parent='projects/{}'.format(self.PROJECT),
            instance_id=self.INSTANCE_ID,
            instance=instance,
            clusters=clusters
        )

    def test_update(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable import enums
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.protobuf import field_mask_pb2
        from google.cloud.bigtable_admin_v2.types import instance_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as instance_v2_pb2)

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(
            self.INSTANCE_ID, client, display_name=self.DISPLAY_NAME,
            instance_type=enums.Instance.Type.DEVELOPMENT, labels=self.LABELS)

        expected_request_instance = instance_pb2.Instance(
            name=instance.name, display_name=instance.display_name,
            type=instance.type_, labels=instance.labels)
        expected_request_update_mask = field_mask_pb2.FieldMask(
            paths=['display_name', 'type', 'labels'])
        expected_request = instance_v2_pb2.PartialUpdateInstanceRequest(
            instance=expected_request_instance,
            update_mask=expected_request_update_mask)

        metadata = messages_v2_pb2.UpdateInstanceMetadata(
            request_time=NOW_PB)
        type_url = 'type.googleapis.com/{}'.format(
            messages_v2_pb2.UpdateInstanceMetadata.DESCRIPTOR.full_name)
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(
                type_url=type_url,
                value=metadata.SerializeToString(),
            )
        )

        channel = ChannelStub(responses=[response_pb])
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                channel=channel))

        # Mock api calls
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        result = instance.update()
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.UpdateInstanceMetadata)

    def test_update_empty(self):
        from google.api_core import operation
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.longrunning import operations_pb2
        from google.protobuf import field_mask_pb2
        from google.cloud.bigtable_admin_v2.types import instance_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as instance_v2_pb2)

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(None, client)

        expected_request_instance = instance_pb2.Instance(
            name=instance.name, display_name=instance.display_name,
            type=instance.type_, labels=instance.labels)
        expected_request_update_mask = field_mask_pb2.FieldMask()
        expected_request = instance_v2_pb2.PartialUpdateInstanceRequest(
            instance=expected_request_instance,
            update_mask=expected_request_update_mask)

        response_pb = operations_pb2.Operation(name=self.OP_NAME)

        channel = ChannelStub(responses=[response_pb])
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                channel=channel))

        # Mock api calls
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        result = instance.update()
        actual_request = channel.requests[0][1]

        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(actual_request, expected_request)

    def test_delete(self):
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        # Mock api calls
        client._instance_admin_client = api

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
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client, bigtable_instance_admin_client)

        table_api = bigtable_table_admin_client.BigtableTableAdminClient(
            mock.Mock())
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                mock.Mock()))
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        # Create response_pb
        if table_name is None:
            table_name = self.TABLE_NAME

        response_pb = table_messages_v1_pb2.ListTablesResponse(
            tables=[
                table_data_v2_pb2.Table(name=table_name),
            ],
        )

        # Patch the stub used by the API method.
        client._table_admin_client = table_api
        client._instance_admin_client = instance_api
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

    def test_create_app_profile_with_wrong_routing_policy(self):
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        app_profile_id = 'appProfileId1262094415'

        # Create AppProfile with exception
        with self.assertRaises(ValueError):
            instance.create_app_profile(app_profile_id=app_profile_id,
                                        routing_policy_type=None)

        with self.assertRaises(ValueError):
            instance.update_app_profile(app_profile_id,
                                        routing_policy_type=None)

    def test_create_app_profile_with_multi_routing_policy(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.cloud.bigtable.enums import RoutingPolicyType

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        description = 'description-1724546052'
        app_profile_id = 'appProfileId1262094415'
        expected_response = {
            'name': self.APP_PROFILE_PATH + app_profile_id,
            'description': description,
            'multi_cluster_routing_use_any':
                instance_pb2.AppProfile.MultiClusterRoutingUseAny()
        }
        expected_request = {
            'app_profile_id': app_profile_id,
            'routing_policy_type': RoutingPolicyType.ANY,
            'description': description
        }
        expected_response = instance_pb2.AppProfile(**expected_response)

        channel = ChannelStub(responses=[expected_response])
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                channel=channel))

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        result = instance.create_app_profile(**expected_request)

        parent = client._instance_admin_client.instance_path(
            self.PROJECT, self.INSTANCE_ID)
        expected_request = _CreateAppProfileRequestPB(
            parent=parent, app_profile_id=app_profile_id,
            app_profile=expected_response,
        )

        actual_request = channel.requests[0][1]
        self.assertEqual(expected_request, actual_request)
        self.assertEqual(result, expected_response)

    def test_create_app_profile_with_single_routing_policy(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.cloud.bigtable.enums import RoutingPolicyType

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        description = 'description-1724546052'
        app_profile_id = 'appProfileId1262094415'
        cluster_id = 'cluster-id'
        expected_response = {
            'name': self.APP_PROFILE_PATH + app_profile_id,
            'description': description,
            'single_cluster_routing':
                instance_pb2.AppProfile.SingleClusterRouting(
                    cluster_id=cluster_id,
                    allow_transactional_writes=False
                )
        }
        expected_request = {
            'app_profile_id': app_profile_id,
            'routing_policy_type': RoutingPolicyType.SINGLE,
            'description': description,
            'cluster_id': cluster_id
        }
        expected_response = instance_pb2.AppProfile(**expected_response)

        channel = ChannelStub(responses=[expected_response])
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                channel=channel))

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        result = instance.create_app_profile(**expected_request)

        parent = client._instance_admin_client.instance_path(
            self.PROJECT, self.INSTANCE_ID)
        expected_request = _CreateAppProfileRequestPB(
            parent=parent, app_profile_id=app_profile_id,
            app_profile=expected_response,
        )

        actual_request = channel.requests[0][1]
        self.assertEqual(expected_request, actual_request)
        self.assertEqual(result, expected_response)

    def test_get_app_profile(self):
        from google.cloud.bigtable_admin_v2.proto import (
            instance_pb2 as instance_data_v2_pb2)
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                mock.Mock()))

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        name = 'name3373707'
        etag = 'etag3123477'
        description = 'description-1724546052'
        expected_response = {
            'name': name,
            'etag': etag,
            'description': description
        }
        expected_response = instance_data_v2_pb2.AppProfile(
            **expected_response)

        response_pb = instance_data_v2_pb2.AppProfile(
            name=name,
            etag=etag,
            description=description
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api
        bigtable_instance_stub = (
            client._instance_admin_client.bigtable_instance_admin_stub)
        bigtable_instance_stub.GetAppProfile.side_effect = [response_pb]

        # Perform the method and check the result.
        app_profile_id = 'appProfileId1262094415'
        result = instance.get_app_profile(app_profile_id=app_profile_id)

        self.assertEqual(result, expected_response)

    def test_list_app_profiles(self):
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as instance_messages_v1_pb2)
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                mock.Mock()))

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        # Setup Expected Response
        next_page_token = ''
        app_profiles_element = {}
        app_profiles = [app_profiles_element]
        expected_response = {
            'next_page_token': next_page_token,
            'app_profiles': app_profiles
        }
        expected_response = instance_messages_v1_pb2.ListAppProfilesResponse(
            **expected_response)

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api
        bigtable_instance_stub = (
            client._instance_admin_client.bigtable_instance_admin_stub)
        bigtable_instance_stub.ListAppProfiles.side_effect = [
            expected_response]

        # Perform the method and check the result.
        response = instance.list_app_profiles()

        self.assertEqual(response[0], expected_response.app_profiles[0])

    def test_update_app_profile_multi_cluster_routing_policy(self):
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.cloud.bigtable_admin_v2.types import instance_pb2
        from google.protobuf import field_mask_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as instance_v2_pb2)
        from google.cloud.bigtable.enums import RoutingPolicyType

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        # Create response_pb
        metadata = messages_v2_pb2.UpdateAppProfileMetadata()
        type_url = 'type.googleapis.com/{}'.format(
            messages_v2_pb2.UpdateAppProfileMetadata.DESCRIPTOR.full_name)
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(
                type_url=type_url,
                value=metadata.SerializeToString(),
            )
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[response_pb])
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                channel=channel))
        # Mock api calls
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        description = 'description-1724546052'
        app_profile_id = 'appProfileId1262094415'
        ignore_warnings = True
        multi_cluster_routing_use_any = (
            instance_pb2.AppProfile.MultiClusterRoutingUseAny())
        expected_request_app_profile = instance_pb2.AppProfile(
            name=self.APP_PROFILE_PATH + app_profile_id,
            description=description,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any
            )
        expected_request_update_mask = field_mask_pb2.FieldMask(
            paths=['description', 'multi_cluster_routing_use_any']
        )
        expected_request = instance_v2_pb2.UpdateAppProfileRequest(
            app_profile=expected_request_app_profile,
            update_mask=expected_request_update_mask,
            ignore_warnings=ignore_warnings
        )

        result = instance.update_app_profile(app_profile_id,
                                             RoutingPolicyType.ANY,
                                             description=description,
                                             ignore_warnings=ignore_warnings)
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.UpdateAppProfileMetadata)

    def test_update_app_profile_single_routing_policy(self):
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)
        from google.cloud.bigtable_admin_v2.types import instance_pb2
        from google.protobuf import field_mask_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as instance_v2_pb2)
        from google.cloud.bigtable.enums import RoutingPolicyType

        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        # Create response_pb
        metadata = messages_v2_pb2.UpdateAppProfileMetadata()
        type_url = 'type.googleapis.com/{}'.format(
            messages_v2_pb2.UpdateAppProfileMetadata.DESCRIPTOR.full_name)
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(
                type_url=type_url,
                value=metadata.SerializeToString(),
            )
        )

        # Patch the stub used by the API method.
        channel = ChannelStub(responses=[response_pb])
        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                channel=channel))
        # Mock api calls
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        app_profile_id = 'appProfileId1262094415'
        cluster_id = 'cluster-id'
        allow_transactional_writes = True
        ignore_warnings = True
        single_cluster_routing = (
                instance_pb2.AppProfile.SingleClusterRouting(
                    cluster_id=cluster_id,
                    allow_transactional_writes=allow_transactional_writes
                ))
        expected_request_app_profile = instance_pb2.AppProfile(
            name=self.APP_PROFILE_PATH + app_profile_id,
            single_cluster_routing=single_cluster_routing
            )
        expected_request_update_mask = field_mask_pb2.FieldMask(
            paths=['single_cluster_routing']
        )
        expected_request = instance_v2_pb2.UpdateAppProfileRequest(
            app_profile=expected_request_app_profile,
            update_mask=expected_request_update_mask,
            ignore_warnings=ignore_warnings
        )

        result = instance.update_app_profile(app_profile_id,
                                             RoutingPolicyType.SINGLE,
                                             ignore_warnings=ignore_warnings,
                                             cluster_id=cluster_id,
                                             allow_transactional_writes=(
                                                allow_transactional_writes))
        actual_request = channel.requests[0][1]

        self.assertEqual(actual_request, expected_request)
        self.assertIsInstance(result, operation.Operation)
        self.assertEqual(result.operation.name, self.OP_NAME)
        self.assertIsInstance(result.metadata,
                              messages_v2_pb2.UpdateAppProfileMetadata)

    def test_delete_app_profile(self):
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client)

        instance_api = (
            bigtable_instance_admin_client.BigtableInstanceAdminClient(
                mock.Mock()))
        credentials = _make_credentials()
        client = self._make_client(project=self.PROJECT,
                                   credentials=credentials, admin=True)
        instance = self._make_one(self.INSTANCE_ID, client)

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api

        ignore_warnings = True

        expected_result = None  # delete() has no return value.

        app_profile_id = 'appProfileId1262094415'
        result = instance.delete_app_profile(app_profile_id, ignore_warnings)

        self.assertEqual(expected_result, result)


class _Client(object):

    def __init__(self, project):
        self.project = project
        self.project_name = 'projects/' + self.project
        self._operations_stub = mock.sentinel.operations_stub

    def __eq__(self, other):
        return (other.project == self.project and
                other.project_name == self.project_name)


def _CreateAppProfileRequestPB(*args, **kw):
    from google.cloud.bigtable_admin_v2.proto import (
        bigtable_instance_admin_pb2 as instance_v2_pb2)

    return instance_v2_pb2.CreateAppProfileRequest(*args, **kw)
