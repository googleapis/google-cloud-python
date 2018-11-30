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


class TestInstance(unittest.TestCase):

    PROJECT = "project"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT + "/instances/" + INSTANCE_ID
    LOCATION_ID = "locid"
    LOCATION = "projects/" + PROJECT + "/locations/" + LOCATION_ID
    APP_PROFILE_PATH = (
        "projects/" + PROJECT + "/instances/" + INSTANCE_ID + "/appProfiles/"
    )
    DISPLAY_NAME = "display_name"
    LABELS = {"foo": "bar"}
    OP_ID = 8915
    OP_NAME = "operations/projects/{}/instances/{}operations/{}".format(
        PROJECT, INSTANCE_ID, OP_ID
    )
    TABLE_ID = "table_id"
    TABLE_NAME = INSTANCE_NAME + "/tables/" + TABLE_ID

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
        labels = {"test": "test"}
        client = object()

        instance = self._make_one(
            self.INSTANCE_ID,
            client,
            display_name=self.DISPLAY_NAME,
            instance_type=instance_type,
            labels=labels,
            _state=state,
        )
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.type_, instance_type)
        self.assertEqual(instance.labels, labels)
        self.assertIs(instance._client, client)
        self.assertEqual(instance.state, state)

    def test__update_from_pb_success(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable import enums

        instance_type = enums.Instance.Type.PRODUCTION
        state = enums.Instance.State.READY
        instance_pb = data_v2_pb2.Instance(
            display_name=self.DISPLAY_NAME,
            type=instance_type,
            labels=self.LABELS,
            state=state,
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
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable import enums

        instance_pb = data_v2_pb2.Instance(display_name=self.DISPLAY_NAME)

        instance = self._make_one(None, None)
        self.assertIsNone(instance.display_name)
        self.assertIsNone(instance.type_)
        self.assertIsNone(instance.labels)
        instance._update_from_pb(instance_pb)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.type_, enums.Instance.Type.UNSPECIFIED)
        self.assertFalse(instance.labels)

    def test__update_from_pb_no_display_name(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        instance_pb = data_v2_pb2.Instance()
        instance = self._make_one(None, None)
        self.assertIsNone(instance.display_name)
        with self.assertRaises(ValueError):
            instance._update_from_pb(instance_pb)

    def test_from_pb_success(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable import enums

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance_type = enums.Instance.Type.PRODUCTION
        state = enums.Instance.State.READY
        instance_pb = data_v2_pb2.Instance(
            name=self.INSTANCE_NAME,
            display_name=self.INSTANCE_ID,
            type=instance_type,
            labels=self.LABELS,
            state=state,
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
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        instance_name = "INCORRECT_FORMAT"
        instance_pb = data_v2_pb2.Instance(name=instance_name)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, None)

    def test_from_pb_project_mistmatch(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2

        ALT_PROJECT = "ALT_PROJECT"
        credentials = _make_credentials()
        client = self._make_client(
            project=ALT_PROJECT, credentials=credentials, admin=True
        )

        self.assertNotEqual(self.PROJECT, ALT_PROJECT)

        instance_pb = data_v2_pb2.Instance(name=self.INSTANCE_NAME)

        klass = self._get_target_class()
        with self.assertRaises(ValueError):
            klass.from_pb(instance_pb, client)

    def test_name_property(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )

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
        comparison_val = instance1 != instance2
        self.assertFalse(comparison_val)

    def test___ne__(self):
        instance1 = self._make_one("instance_id1", "client1")
        instance2 = self._make_one("instance_id2", "client2")
        self.assertNotEqual(instance1, instance2)

    def test_create_check_location_and_clusters(self):
        instance = self._make_one(self.INSTANCE_ID, None)

        with self.assertRaises(ValueError):
            instance.create(location_id=self.LOCATION_ID, clusters=[object(), object()])

    def test_create_check_serve_nodes_and_clusters(self):
        instance = self._make_one(self.INSTANCE_ID, None)

        with self.assertRaises(ValueError):
            instance.create(serve_nodes=3, clusters=[object(), object()])

    def test_create_check_default_storage_type_and_clusters(self):
        instance = self._make_one(self.INSTANCE_ID, None)

        with self.assertRaises(ValueError):
            instance.create(default_storage_type=1, clusters=[object(), object()])

    def _instance_api_response_for_create(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable_admin_v2.types import instance_pb2

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)
        metadata = messages_v2_pb2.CreateInstanceMetadata(request_time=NOW_PB)
        type_url = "type.googleapis.com/{}".format(
            messages_v2_pb2.CreateInstanceMetadata.DESCRIPTOR.full_name
        )
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(type_url=type_url, value=metadata.SerializeToString()),
        )
        response = operation.from_gapic(
            response_pb,
            mock.Mock(),
            instance_pb2.Instance,
            metadata_type=messages_v2_pb2.CreateInstanceMetadata,
        )
        project_path_template = "projects/{}"
        location_path_template = "projects/{}/locations/{}"
        instance_api = mock.create_autospec(
            bigtable_instance_admin_client.BigtableInstanceAdminClient
        )
        instance_api.create_instance.return_value = response
        instance_api.project_path = project_path_template.format
        instance_api.location_path = location_path_template.format
        return instance_api, response

    def test_create(self):
        from google.cloud.bigtable import enums
        from google.cloud.bigtable_admin_v2.types import instance_pb2

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(
            self.INSTANCE_ID,
            client,
            self.DISPLAY_NAME,
            enums.Instance.Type.PRODUCTION,
            self.LABELS,
        )
        instance_api, response = self._instance_api_response_for_create()
        client._instance_admin_client = instance_api
        serve_nodes = 3

        result = instance.create(location_id=self.LOCATION_ID, serve_nodes=serve_nodes)

        cluster_pb = instance_pb2.Cluster(
            location=instance_api.location_path(self.PROJECT, self.LOCATION_ID),
            serve_nodes=serve_nodes,
            default_storage_type=enums.StorageType.UNSPECIFIED,
        )
        instance_pb = instance_pb2.Instance(
            display_name=self.DISPLAY_NAME,
            type=enums.Instance.Type.PRODUCTION,
            labels=self.LABELS,
        )
        cluster_id = "{}-cluster".format(self.INSTANCE_ID)
        instance_api.create_instance.assert_called_once_with(
            parent=instance_api.project_path(self.PROJECT),
            instance_id=self.INSTANCE_ID,
            instance=instance_pb,
            clusters={cluster_id: cluster_pb},
        )

        self.assertIs(result, response)

    def test_create_w_clusters(self):
        from google.cloud.bigtable import enums
        from google.cloud.bigtable_admin_v2.types import instance_pb2

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(
            self.INSTANCE_ID,
            client,
            self.DISPLAY_NAME,
            enums.Instance.Type.PRODUCTION,
            self.LABELS,
        )
        instance_api, response = self._instance_api_response_for_create()
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        cluster_id_1 = "cluster-1"
        cluster_id_2 = "cluster-2"
        location_id_1 = "location-id-1"
        location_id_2 = "location-id-2"
        serve_nodes_1 = 3
        serve_nodes_2 = 5
        clusters = [
            Cluster(
                cluster_id_1,
                instance,
                location_id=location_id_1,
                serve_nodes=serve_nodes_1,
            ),
            Cluster(
                cluster_id_2,
                instance,
                location_id=location_id_2,
                serve_nodes=serve_nodes_2,
            ),
        ]

        result = instance.create(clusters=clusters)

        cluster_pb_1 = instance_pb2.Cluster(
            location=instance_api.location_path(self.PROJECT, location_id_1),
            serve_nodes=serve_nodes_1,
            default_storage_type=enums.StorageType.UNSPECIFIED,
        )
        cluster_pb_2 = instance_pb2.Cluster(
            location=instance_api.location_path(self.PROJECT, location_id_2),
            serve_nodes=serve_nodes_2,
            default_storage_type=enums.StorageType.UNSPECIFIED,
        )
        instance_pb = instance_pb2.Instance(
            display_name=self.DISPLAY_NAME,
            type=enums.Instance.Type.PRODUCTION,
            labels=self.LABELS,
        )
        instance_api.create_instance.assert_called_once_with(
            parent=instance_api.project_path(self.PROJECT),
            instance_id=self.INSTANCE_ID,
            instance=instance_pb,
            clusters={cluster_id_1: cluster_pb_1, cluster_id_2: cluster_pb_2},
        )

        self.assertIs(result, response)

    def test_exists(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.api_core import exceptions

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )

        # Create response_pb
        instance_name = client.instance_admin_client.instance_path(
            self.PROJECT, self.INSTANCE_ID
        )
        response_pb = data_v2_pb2.Instance(name=instance_name)

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        instance_admin_client = client._instance_admin_client
        instance_stub = instance_admin_client.transport
        instance_stub.get_instance.side_effect = [
            response_pb,
            exceptions.NotFound("testing"),
            exceptions.BadRequest("testing"),
        ]

        # Perform the method and check the result.
        non_existing_instance_id = "instance-id-2"
        alt_instance_1 = self._make_one(self.INSTANCE_ID, client)
        alt_instance_2 = self._make_one(non_existing_instance_id, client)
        self.assertTrue(alt_instance_1.exists())
        self.assertFalse(alt_instance_2.exists())

        with self.assertRaises(exceptions.BadRequest):
            alt_instance_2.exists()

    def test_reload(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable import enums

        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        # Create response_pb
        DISPLAY_NAME = u"hey-hi-hello"
        instance_type = enums.Instance.Type.PRODUCTION
        response_pb = data_v2_pb2.Instance(
            display_name=DISPLAY_NAME, type=instance_type, labels=self.LABELS
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        bigtable_instance_stub = client._instance_admin_client.transport
        bigtable_instance_stub.get_instance.side_effect = [response_pb]

        # Create expected_result.
        expected_result = None  # reload() has no return value.

        # Check Instance optional config values before.
        self.assertEqual(instance.display_name, self.INSTANCE_ID)

        # Perform the method and check the result.
        result = instance.reload()
        self.assertEqual(result, expected_result)

        # Check Instance optional config values before.
        self.assertEqual(instance.display_name, DISPLAY_NAME)

    def _instance_api_response_for_update(self):
        import datetime
        from google.api_core import operation
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable_admin_v2.types import instance_pb2

        NOW = datetime.datetime.utcnow()
        NOW_PB = _datetime_to_pb_timestamp(NOW)
        metadata = messages_v2_pb2.UpdateInstanceMetadata(request_time=NOW_PB)
        type_url = "type.googleapis.com/{}".format(
            messages_v2_pb2.UpdateInstanceMetadata.DESCRIPTOR.full_name
        )
        response_pb = operations_pb2.Operation(
            name=self.OP_NAME,
            metadata=Any(type_url=type_url, value=metadata.SerializeToString()),
        )
        response = operation.from_gapic(
            response_pb,
            mock.Mock(),
            instance_pb2.Instance,
            metadata_type=messages_v2_pb2.UpdateInstanceMetadata,
        )
        instance_path_template = "projects/{project}/instances/{instance}"
        instance_api = mock.create_autospec(
            bigtable_instance_admin_client.BigtableInstanceAdminClient
        )
        instance_api.partial_update_instance.return_value = response
        instance_api.instance_path = instance_path_template.format
        return instance_api, response

    def test_update(self):
        from google.cloud.bigtable import enums
        from google.protobuf import field_mask_pb2
        from google.cloud.bigtable_admin_v2.types import instance_pb2

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(
            self.INSTANCE_ID,
            client,
            display_name=self.DISPLAY_NAME,
            instance_type=enums.Instance.Type.DEVELOPMENT,
            labels=self.LABELS,
        )
        instance_api, response = self._instance_api_response_for_update()
        client._instance_admin_client = instance_api

        result = instance.update()

        instance_pb = instance_pb2.Instance(
            name=instance.name,
            display_name=instance.display_name,
            type=instance.type_,
            labels=instance.labels,
        )
        update_mask_pb = field_mask_pb2.FieldMask(
            paths=["display_name", "type", "labels"]
        )

        instance_api.partial_update_instance.assert_called_once_with(
            instance=instance_pb, update_mask=update_mask_pb
        )

        self.assertIs(result, response)

    def test_update_empty(self):
        from google.protobuf import field_mask_pb2
        from google.cloud.bigtable_admin_v2.types import instance_pb2

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(None, client)
        instance_api, response = self._instance_api_response_for_update()
        client._instance_admin_client = instance_api

        result = instance.update()

        instance_pb = instance_pb2.Instance(
            name=instance.name,
            display_name=instance.display_name,
            type=instance.type_,
            labels=instance.labels,
        )
        update_mask_pb = field_mask_pb2.FieldMask()

        instance_api.partial_update_instance.assert_called_once_with(
            instance=instance_pb, update_mask=update_mask_pb
        )

        self.assertIs(result, response)

    def test_delete(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(self.INSTANCE_ID, client)
        instance_api = mock.create_autospec(
            bigtable_instance_admin_client.BigtableInstanceAdminClient
        )
        instance_api.delete_instance.return_value = None
        client._instance_admin_client = instance_api

        result = instance.delete()

        instance_api.delete_instance.assert_called_once_with(instance.name)

        self.assertIsNone(result)

    def test_get_iam_policy(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.iam.v1 import policy_pb2
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        version = 1
        etag = b"etag_v1"
        members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
        bindings = [{"role": BIGTABLE_ADMIN_ROLE, "members": members}]
        iam_policy = policy_pb2.Policy(version=version, etag=etag, bindings=bindings)

        # Patch the stub used by the API method.
        instance_api = mock.create_autospec(
            bigtable_instance_admin_client.BigtableInstanceAdminClient
        )
        client._instance_admin_client = instance_api
        instance_api.get_iam_policy.return_value = iam_policy

        # Perform the method and check the result.
        result = instance.get_iam_policy()

        instance_api.get_iam_policy.assert_called_once_with(resource=instance.name)
        self.assertEqual(result.version, version)
        self.assertEqual(result.etag, etag)
        admins = result.bigtable_admins
        self.assertEqual(len(admins), len(members))
        for found, expected in zip(sorted(admins), sorted(members)):
            self.assertEqual(found, expected)

    def test_set_iam_policy(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.iam.v1 import policy_pb2
        from google.cloud.bigtable.policy import Policy
        from google.cloud.bigtable.policy import BIGTABLE_ADMIN_ROLE

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        version = 1
        etag = b"etag_v1"
        members = ["serviceAccount:service_acc1@test.com", "user:user1@test.com"]
        bindings = [{"role": BIGTABLE_ADMIN_ROLE, "members": members}]
        iam_policy_pb = policy_pb2.Policy(version=version, etag=etag, bindings=bindings)

        # Patch the stub used by the API method.
        instance_api = mock.create_autospec(
            bigtable_instance_admin_client.BigtableInstanceAdminClient
        )
        instance_api.set_iam_policy.return_value = iam_policy_pb
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        iam_policy = Policy(etag=etag, version=version)
        iam_policy[BIGTABLE_ADMIN_ROLE] = [
            Policy.user("user1@test.com"),
            Policy.service_account("service_acc1@test.com"),
        ]

        result = instance.set_iam_policy(iam_policy)

        instance_api.set_iam_policy.assert_called_once_with(
            resource=instance.name,
            policy={"version": version, "etag": etag, "bindings": bindings},
        )
        self.assertEqual(result.version, version)
        self.assertEqual(result.etag, etag)
        admins = result.bigtable_admins
        self.assertEqual(len(admins), len(members))
        for found, expected in zip(sorted(admins), sorted(members)):
            self.assertEqual(found, expected)

    def test_test_iam_permissions(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.iam.v1 import iam_policy_pb2

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        permissions = ["bigtable.tables.create", "bigtable.clusters.create"]

        response = iam_policy_pb2.TestIamPermissionsResponse(permissions=permissions)

        instance_api = mock.create_autospec(
            bigtable_instance_admin_client.BigtableInstanceAdminClient
        )
        instance_api.test_iam_permissions.return_value = response
        client._instance_admin_client = instance_api

        result = instance.test_iam_permissions(permissions)

        self.assertEqual(result, permissions)
        instance_api.test_iam_permissions.assert_called_once_with(
            resource=instance.name, permissions=permissions
        )

    def test_cluster_factory(self):
        from google.cloud.bigtable import enums

        CLUSTER_ID = "{}-cluster".format(self.INSTANCE_ID)
        LOCATION_ID = "us-central1-c"
        SERVE_NODES = 3
        STORAGE_TYPE = enums.StorageType.HDD

        instance = self._make_one(self.INSTANCE_ID, None)

        cluster = instance.cluster(
            CLUSTER_ID,
            location_id=LOCATION_ID,
            serve_nodes=SERVE_NODES,
            default_storage_type=STORAGE_TYPE,
        )
        self.assertIsInstance(cluster, Cluster)
        self.assertEqual(cluster.cluster_id, CLUSTER_ID)
        self.assertEqual(cluster.location_id, LOCATION_ID)
        self.assertIsNone(cluster._state)
        self.assertEqual(cluster.serve_nodes, SERVE_NODES)
        self.assertEqual(cluster.default_storage_type, STORAGE_TYPE)

    def test_list_clusters(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable.instance import Cluster

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = Instance(self.INSTANCE_ID, client)

        failed_location = "FAILED"
        cluster_id1 = "cluster-id1"
        cluster_id2 = "cluster-id2"
        cluster_path_template = "projects/{}/instances/{}/clusters/{}"
        cluster_name1 = cluster_path_template.format(
            self.PROJECT, self.INSTANCE_ID, cluster_id1
        )
        cluster_name2 = cluster_path_template.format(
            self.PROJECT, self.INSTANCE_ID, cluster_id2
        )

        # Create response_pb
        response_pb = messages_v2_pb2.ListClustersResponse(
            failed_locations=[failed_location],
            clusters=[
                data_v2_pb2.Cluster(name=cluster_name1),
                data_v2_pb2.Cluster(name=cluster_name2),
            ],
        )

        # Patch the stub used by the API method.
        instance_api = mock.create_autospec(
            bigtable_instance_admin_client.BigtableInstanceAdminClient
        )
        instance_api.list_clusters.side_effect = [response_pb]
        instance_api.cluster_path = cluster_path_template.format
        client._instance_admin_client = instance_api

        # Perform the method and check the result.
        clusters, failed_locations = instance.list_clusters()

        cluster_1, cluster_2 = clusters

        self.assertIsInstance(cluster_1, Cluster)
        self.assertEqual(cluster_1.name, cluster_name1)

        self.assertIsInstance(cluster_2, Cluster)
        self.assertEqual(cluster_2.name, cluster_name2)

        self.assertEqual(failed_locations, [failed_location])

    def test_table_factory(self):
        from google.cloud.bigtable.table import Table

        app_profile_id = "appProfileId1262094415"
        instance = self._make_one(self.INSTANCE_ID, None)

        table = instance.table(self.TABLE_ID, app_profile_id=app_profile_id)
        self.assertIsInstance(table, Table)
        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertEqual(table._instance, instance)
        self.assertEqual(table._app_profile_id, app_profile_id)

    def _list_tables_helper(self, table_name=None):
        from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_data_v2_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_table_admin_pb2 as table_messages_v1_pb2,
        )
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client,
            bigtable_instance_admin_client,
        )

        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock()
        )
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        # Create response_pb
        if table_name is None:
            table_name = self.TABLE_NAME

        response_pb = table_messages_v1_pb2.ListTablesResponse(
            tables=[table_data_v2_pb2.Table(name=table_name)]
        )

        # Patch the stub used by the API method.
        client._table_admin_client = table_api
        client._instance_admin_client = instance_api
        bigtable_table_stub = client._table_admin_client.transport
        bigtable_table_stub.list_tables.side_effect = [response_pb]

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
            self._list_tables_helper(table_name="wrong-format")

    def test_list_tables_failure_name_bad_before(self):
        BAD_TABLE_NAME = (
            "nonempty-section-before"
            + "projects/"
            + self.PROJECT
            + "/instances/"
            + self.INSTANCE_ID
            + "/tables/"
            + self.TABLE_ID
        )
        with self.assertRaises(ValueError):
            self._list_tables_helper(table_name=BAD_TABLE_NAME)

    def test_app_profile_factory(self):
        from google.cloud.bigtable.enums import RoutingPolicyType

        APP_PROFILE_ID_1 = "app-profile-id-1"
        ANY = RoutingPolicyType.ANY
        DESCRIPTION_1 = "routing policy any"
        APP_PROFILE_ID_2 = "app-profile-id-2"
        SINGLE = RoutingPolicyType.SINGLE
        DESCRIPTION_2 = "routing policy single"
        ALLOW_WRITES = True
        CLUSTER_ID = "cluster-id"

        instance = self._make_one(self.INSTANCE_ID, None)

        app_profile1 = instance.app_profile(
            APP_PROFILE_ID_1, routing_policy_type=ANY, description=DESCRIPTION_1
        )

        app_profile2 = instance.app_profile(
            APP_PROFILE_ID_2,
            routing_policy_type=SINGLE,
            description=DESCRIPTION_2,
            cluster_id=CLUSTER_ID,
            allow_transactional_writes=ALLOW_WRITES,
        )
        self.assertEqual(app_profile1.app_profile_id, APP_PROFILE_ID_1)
        self.assertIs(app_profile1._instance, instance)
        self.assertEqual(app_profile1.routing_policy_type, ANY)
        self.assertEqual(app_profile1.description, DESCRIPTION_1)
        self.assertEqual(app_profile2.app_profile_id, APP_PROFILE_ID_2)
        self.assertIs(app_profile2._instance, instance)
        self.assertEqual(app_profile2.routing_policy_type, SINGLE)
        self.assertEqual(app_profile2.description, DESCRIPTION_2)
        self.assertEqual(app_profile2.cluster_id, CLUSTER_ID)
        self.assertEqual(app_profile2.allow_transactional_writes, ALLOW_WRITES)

    def test_list_app_profiles(self):
        from google.api_core.page_iterator import Iterator
        from google.api_core.page_iterator import Page
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable.app_profile import AppProfile

        class _Iterator(Iterator):
            def __init__(self, pages):
                super(_Iterator, self).__init__(client=None)
                self._pages = pages

            def _next_page(self):
                if self._pages:
                    page, self._pages = self._pages[0], self._pages[1:]
                    return Page(self, page, self.item_to_value)

        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT, credentials=credentials, admin=True
        )
        instance = self._make_one(self.INSTANCE_ID, client)

        # Setup Expected Response
        app_profile_path_template = "projects/{}/instances/{}/appProfiles/{}"
        app_profile_id1 = "app-profile-id1"
        app_profile_id2 = "app-profile-id2"
        app_profile_name1 = app_profile_path_template.format(
            self.PROJECT, self.INSTANCE_ID, app_profile_id1
        )
        app_profile_name2 = app_profile_path_template.format(
            self.PROJECT, self.INSTANCE_ID, app_profile_id2
        )
        routing_policy = data_v2_pb2.AppProfile.MultiClusterRoutingUseAny()

        app_profiles = [
            data_v2_pb2.AppProfile(
                name=app_profile_name1, multi_cluster_routing_use_any=routing_policy
            ),
            data_v2_pb2.AppProfile(
                name=app_profile_name2, multi_cluster_routing_use_any=routing_policy
            ),
        ]
        iterator = _Iterator(pages=[app_profiles])

        # Patch the stub used by the API method.
        instance_api = mock.create_autospec(
            bigtable_instance_admin_client.BigtableInstanceAdminClient
        )
        client._instance_admin_client = instance_api
        instance_api.app_profile_path = app_profile_path_template.format
        instance_api.list_app_profiles.return_value = iterator

        # Perform the method and check the result.
        app_profiles = instance.list_app_profiles()

        app_profile_1, app_profile_2 = app_profiles

        self.assertIsInstance(app_profile_1, AppProfile)
        self.assertEqual(app_profile_1.name, app_profile_name1)

        self.assertIsInstance(app_profile_2, AppProfile)
        self.assertEqual(app_profile_2.name, app_profile_name2)
