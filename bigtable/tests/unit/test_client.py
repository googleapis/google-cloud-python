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


class Test__create_gapic_client(unittest.TestCase):
    def _invoke_client_factory(self, client_class):
        from google.cloud.bigtable.client import _create_gapic_client

        return _create_gapic_client(client_class)

    def test_without_emulator(self):
        from google.cloud.bigtable.client import _CLIENT_INFO

        client_class = mock.Mock()
        credentials = _make_credentials()
        client = _Client(credentials)

        result = self._invoke_client_factory(client_class)(client)

        self.assertIs(result, client_class.return_value)
        client_class.assert_called_once_with(
            credentials=client._credentials, client_info=_CLIENT_INFO
        )

    def test_with_emulator(self):
        from google.cloud.bigtable.client import _CLIENT_INFO

        client_class = mock.Mock()
        emulator_host = emulator_channel = object()
        credentials = _make_credentials()
        client = _Client(
            credentials, emulator_host=emulator_host, emulator_channel=emulator_channel
        )

        result = self._invoke_client_factory(client_class)(client)

        self.assertIs(result, client_class.return_value)
        client_class.assert_called_once_with(
            channel=client._emulator_channel, client_info=_CLIENT_INFO
        )


class _Client(object):
    def __init__(self, credentials, emulator_host=None, emulator_channel=None):
        self._credentials = credentials
        self._emulator_host = emulator_host
        self._emulator_channel = emulator_channel


class TestClient(unittest.TestCase):

    PROJECT = "PROJECT"
    INSTANCE_ID = "instance-id"
    DISPLAY_NAME = "display-name"
    USER_AGENT = "you-sir-age-int"

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor_defaults(self):
        from google.cloud.bigtable.client import DATA_SCOPE

        credentials = _make_credentials()

        with mock.patch("google.auth.default") as mocked:
            mocked.return_value = credentials, self.PROJECT
            client = self._make_one()

        self.assertEqual(client.project, self.PROJECT)
        self.assertIs(client._credentials, credentials.with_scopes.return_value)
        self.assertFalse(client._read_only)
        self.assertFalse(client._admin)
        self.assertIsNone(client._channel)
        self.assertIsNone(client._emulator_host)
        self.assertIsNone(client._emulator_channel)
        self.assertEqual(client.SCOPE, (DATA_SCOPE,))

    def test_constructor_explicit(self):
        import warnings
        from google.cloud.bigtable.client import ADMIN_SCOPE
        from google.cloud.bigtable.client import DATA_SCOPE

        credentials = _make_credentials()

        with warnings.catch_warnings(record=True) as warned:
            client = self._make_one(
                project=self.PROJECT,
                credentials=credentials,
                read_only=False,
                admin=True,
                channel=mock.sentinel.channel,
            )

        self.assertEqual(len(warned), 1)

        self.assertEqual(client.project, self.PROJECT)
        self.assertIs(client._credentials, credentials.with_scopes.return_value)
        self.assertFalse(client._read_only)
        self.assertTrue(client._admin)
        self.assertIs(client._channel, mock.sentinel.channel)
        self.assertEqual(client.SCOPE, (DATA_SCOPE, ADMIN_SCOPE))

    def test_constructor_both_admin_and_read_only(self):
        credentials = _make_credentials()
        with self.assertRaises(ValueError):
            self._make_one(
                project=self.PROJECT,
                credentials=credentials,
                admin=True,
                read_only=True,
            )

    def test_constructor_with_emulator_host(self):
        from google.cloud.environment_vars import BIGTABLE_EMULATOR

        credentials = _make_credentials()
        emulator_host = "localhost:8081"
        with mock.patch("os.getenv") as getenv:
            getenv.return_value = emulator_host
            with mock.patch("grpc.insecure_channel") as factory:
                getenv.return_value = emulator_host
                client = self._make_one(project=self.PROJECT, credentials=credentials)

        self.assertEqual(client._emulator_host, emulator_host)
        self.assertIs(client._emulator_channel, factory.return_value)
        factory.assert_called_once_with(emulator_host)
        getenv.assert_called_once_with(BIGTABLE_EMULATOR)

    def test__get_scopes_default(self):
        from google.cloud.bigtable.client import DATA_SCOPE

        client = self._make_one(project=self.PROJECT, credentials=_make_credentials())
        self.assertEqual(client._get_scopes(), (DATA_SCOPE,))

    def test__get_scopes_admin(self):
        from google.cloud.bigtable.client import ADMIN_SCOPE
        from google.cloud.bigtable.client import DATA_SCOPE

        client = self._make_one(
            project=self.PROJECT, credentials=_make_credentials(), admin=True
        )
        expected_scopes = (DATA_SCOPE, ADMIN_SCOPE)
        self.assertEqual(client._get_scopes(), expected_scopes)

    def test__get_scopes_read_only(self):
        from google.cloud.bigtable.client import READ_ONLY_SCOPE

        client = self._make_one(
            project=self.PROJECT, credentials=_make_credentials(), read_only=True
        )
        self.assertEqual(client._get_scopes(), (READ_ONLY_SCOPE,))

    def test_project_path_property(self):
        credentials = _make_credentials()
        project = "PROJECT"
        client = self._make_one(project=project, credentials=credentials, admin=True)
        project_name = "projects/" + project
        self.assertEqual(client.project_path, project_name)

    def test_table_data_client_not_initialized(self):
        from google.cloud.bigtable_v2 import BigtableClient

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        table_data_client = client.table_data_client
        self.assertIsInstance(table_data_client, BigtableClient)
        self.assertIs(client._table_data_client, table_data_client)

    def test_table_data_client_initialized(self):
        credentials = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, admin=True
        )

        already = client._table_data_client = object()
        self.assertIs(client.table_data_client, already)

    def test_table_admin_client_not_initialized_no_admin_flag(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        with self.assertRaises(ValueError):
            client.table_admin_client()

    def test_table_admin_client_not_initialized_w_admin_flag(self):
        from google.cloud.bigtable_admin_v2 import BigtableTableAdminClient

        credentials = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, admin=True
        )

        table_admin_client = client.table_admin_client
        self.assertIsInstance(table_admin_client, BigtableTableAdminClient)

    def test_table_admin_client_initialized(self):
        credentials = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, admin=True
        )

        already = client._table_admin_client = object()
        self.assertIs(client.table_admin_client, already)

    def test_instance_admin_client_not_initialized_no_admin_flag(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        with self.assertRaises(ValueError):
            client.instance_admin_client()

    def test_instance_admin_client_not_initialized_w_admin_flag(self):
        from google.cloud.bigtable_admin_v2 import BigtableInstanceAdminClient

        credentials = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, admin=True
        )

        instance_admin_client = client.instance_admin_client
        self.assertIsInstance(instance_admin_client, BigtableInstanceAdminClient)

    def test_instance_admin_client_initialized(self):
        credentials = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, admin=True
        )

        already = client._instance_admin_client = object()
        self.assertIs(client.instance_admin_client, already)

    def test_instance_factory_defaults(self):
        from google.cloud.bigtable.instance import Instance

        PROJECT = "PROJECT"
        INSTANCE_ID = "instance-id"
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)

        instance = client.instance(INSTANCE_ID)

        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.instance_id, INSTANCE_ID)
        self.assertEqual(instance.display_name, INSTANCE_ID)
        self.assertIsNone(instance.type_)
        self.assertIsNone(instance.labels)
        self.assertIs(instance._client, client)

    def test_instance_factory_non_defaults(self):
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable import enums

        PROJECT = "PROJECT"
        INSTANCE_ID = "instance-id"
        DISPLAY_NAME = "display-name"
        instance_type = enums.Instance.Type.DEVELOPMENT
        labels = {"foo": "bar"}
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)

        instance = client.instance(
            INSTANCE_ID,
            display_name=DISPLAY_NAME,
            instance_type=instance_type,
            labels=labels,
        )

        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.instance_id, INSTANCE_ID)
        self.assertEqual(instance.display_name, DISPLAY_NAME)
        self.assertEqual(instance.type_, instance_type)
        self.assertEqual(instance.labels, labels)
        self.assertIs(instance._client, client)

    def test_list_instances(self):
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable.instance import Instance

        FAILED_LOCATION = "FAILED"
        INSTANCE_ID1 = "instance-id1"
        INSTANCE_ID2 = "instance-id2"
        INSTANCE_NAME1 = "projects/" + self.PROJECT + "/instances/" + INSTANCE_ID1
        INSTANCE_NAME2 = "projects/" + self.PROJECT + "/instances/" + INSTANCE_ID2

        credentials = _make_credentials()
        api = bigtable_instance_admin_client.BigtableInstanceAdminClient(mock.Mock())
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, admin=True
        )

        # Create response_pb
        response_pb = messages_v2_pb2.ListInstancesResponse(
            failed_locations=[FAILED_LOCATION],
            instances=[
                data_v2_pb2.Instance(name=INSTANCE_NAME1, display_name=INSTANCE_NAME1),
                data_v2_pb2.Instance(name=INSTANCE_NAME2, display_name=INSTANCE_NAME2),
            ],
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = api
        bigtable_instance_stub = client.instance_admin_client.transport
        bigtable_instance_stub.list_instances.side_effect = [response_pb]

        # Perform the method and check the result.
        instances, failed_locations = client.list_instances()

        instance_1, instance_2 = instances

        self.assertIsInstance(instance_1, Instance)
        self.assertEqual(instance_1.name, INSTANCE_NAME1)
        self.assertTrue(instance_1._client is client)

        self.assertIsInstance(instance_2, Instance)
        self.assertEqual(instance_2.name, INSTANCE_NAME2)
        self.assertTrue(instance_2._client is client)

        self.assertEqual(failed_locations, [FAILED_LOCATION])

    def test_list_clusters(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_instance_admin_pb2 as messages_v2_pb2,
        )
        from google.cloud.bigtable_admin_v2.proto import instance_pb2 as data_v2_pb2
        from google.cloud.bigtable.instance import Cluster

        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock()
        )
        credentials = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, admin=True
        )

        INSTANCE_ID1 = "instance-id1"
        INSTANCE_ID2 = "instance-id2"

        failed_location = "FAILED"
        cluster_id1 = "{}-cluster".format(INSTANCE_ID1)
        cluster_id2 = "{}-cluster-1".format(INSTANCE_ID2)
        cluster_id3 = "{}-cluster-2".format(INSTANCE_ID2)
        cluster_name1 = client.instance_admin_client.cluster_path(
            self.PROJECT, INSTANCE_ID1, cluster_id1
        )
        cluster_name2 = client.instance_admin_client.cluster_path(
            self.PROJECT, INSTANCE_ID2, cluster_id2
        )
        cluster_name3 = client.instance_admin_client.cluster_path(
            self.PROJECT, INSTANCE_ID2, cluster_id3
        )

        # Create response_pb
        response_pb = messages_v2_pb2.ListClustersResponse(
            failed_locations=[failed_location],
            clusters=[
                data_v2_pb2.Cluster(name=cluster_name1),
                data_v2_pb2.Cluster(name=cluster_name2),
                data_v2_pb2.Cluster(name=cluster_name3),
            ],
        )

        # Patch the stub used by the API method.
        client._instance_admin_client = instance_api
        instance_stub = client._instance_admin_client.transport
        instance_stub.list_clusters.side_effect = [response_pb]

        # Perform the method and check the result.
        clusters, failed_locations = client.list_clusters()

        cluster_1, cluster_2, cluster_3 = clusters

        self.assertIsInstance(cluster_1, Cluster)
        self.assertEqual(cluster_1.name, cluster_name1)
        self.assertEqual(cluster_1._instance.instance_id, INSTANCE_ID1)

        self.assertIsInstance(cluster_2, Cluster)
        self.assertEqual(cluster_2.name, cluster_name2)
        self.assertEqual(cluster_2._instance.instance_id, INSTANCE_ID2)

        self.assertIsInstance(cluster_3, Cluster)
        self.assertEqual(cluster_3.name, cluster_name3)
        self.assertEqual(cluster_3._instance.instance_id, INSTANCE_ID2)

        self.assertEqual(failed_locations, [failed_location])
