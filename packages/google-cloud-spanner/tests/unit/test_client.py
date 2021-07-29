# Copyright 2016 Google LLC All rights reserved.
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


def _make_credentials():
    import google.auth.credentials

    class _CredentialsWithScopes(
        google.auth.credentials.Credentials, google.auth.credentials.Scoped
    ):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


class TestClient(unittest.TestCase):

    PROJECT = "PROJECT"
    PATH = "projects/%s" % (PROJECT,)
    CONFIGURATION_NAME = "config-name"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "%s/instances/%s" % (PATH, INSTANCE_ID)
    DISPLAY_NAME = "display-name"
    NODE_COUNT = 5
    PROCESSING_UNITS = 5000
    LABELS = {"test": "true"}
    TIMEOUT_SECONDS = 80
    LEADER_OPTIONS = ["leader1", "leader2"]

    def _get_target_class(self):
        from google.cloud import spanner

        return spanner.Client

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def _constructor_test_helper(
        self,
        expected_scopes,
        creds,
        expected_creds=None,
        client_info=None,
        client_options=None,
        query_options=None,
        expected_query_options=None,
    ):
        import google.api_core.client_options
        from google.cloud.spanner_v1 import client as MUT

        kwargs = {}

        if client_info is not None:
            kwargs["client_info"] = expected_client_info = client_info
        else:
            expected_client_info = MUT._CLIENT_INFO

        kwargs["client_options"] = client_options
        if type(client_options) == dict:
            expected_client_options = google.api_core.client_options.from_dict(
                client_options
            )
        else:
            expected_client_options = client_options

        client = self._make_one(
            project=self.PROJECT,
            credentials=creds,
            query_options=query_options,
            **kwargs
        )

        expected_creds = expected_creds or creds.with_scopes.return_value
        self.assertIs(client._credentials, expected_creds)

        self.assertIs(client._credentials, expected_creds)
        if expected_scopes is not None:
            creds.with_scopes.assert_called_once_with(
                expected_scopes, default_scopes=None
            )

        self.assertEqual(client.project, self.PROJECT)
        self.assertIs(client._client_info, expected_client_info)
        if expected_client_options is not None:
            self.assertIsInstance(
                client._client_options, google.api_core.client_options.ClientOptions
            )
            self.assertEqual(
                client._client_options.api_endpoint,
                expected_client_options.api_endpoint,
            )
        if expected_query_options is not None:
            self.assertEqual(client._query_options, expected_query_options)

    @mock.patch("google.cloud.spanner_v1.client._get_spanner_emulator_host")
    @mock.patch("warnings.warn")
    def test_constructor_emulator_host_warning(self, mock_warn, mock_em):
        from google.cloud.spanner_v1 import client as MUT
        from google.auth.credentials import AnonymousCredentials

        expected_scopes = None
        creds = _make_credentials()
        mock_em.return_value = "http://emulator.host.com"
        with mock.patch("google.cloud.spanner_v1.client.AnonymousCredentials") as patch:
            expected_creds = patch.return_value = AnonymousCredentials()
            self._constructor_test_helper(expected_scopes, creds, expected_creds)
        mock_warn.assert_called_once_with(MUT._EMULATOR_HOST_HTTP_SCHEME)

    def test_constructor_default_scopes(self):
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_client_info(self):
        from google.cloud.spanner_v1 import client as MUT

        client_info = mock.Mock()
        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds, client_info=client_info)

    def test_constructor_implicit_credentials(self):
        from google.cloud.spanner_v1 import client as MUT

        creds = _make_credentials()

        patch = mock.patch("google.auth.default", return_value=(creds, None))
        with patch as default:
            self._constructor_test_helper(
                None, None, expected_creds=creds.with_scopes.return_value
            )

        default.assert_called_once_with(scopes=(MUT.SPANNER_ADMIN_SCOPE,))

    def test_constructor_credentials_wo_create_scoped(self):
        creds = _make_credentials()
        expected_scopes = None
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_client_options_obj(self):
        from google.api_core.client_options import ClientOptions
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(
            expected_scopes,
            creds,
            client_options=ClientOptions(api_endpoint="endpoint"),
        )

    def test_constructor_custom_client_options_dict(self):
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        self._constructor_test_helper(
            expected_scopes, creds, client_options={"api_endpoint": "endpoint"}
        )

    def test_constructor_custom_query_options_client_config(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        query_options = expected_query_options = ExecuteSqlRequest.QueryOptions(
            optimizer_version="1",
            optimizer_statistics_package="auto_20191128_14_47_22UTC",
        )
        self._constructor_test_helper(
            expected_scopes,
            creds,
            query_options=query_options,
            expected_query_options=expected_query_options,
        )

    @mock.patch(
        "google.cloud.spanner_v1.client._get_spanner_optimizer_statistics_package"
    )
    @mock.patch("google.cloud.spanner_v1.client._get_spanner_optimizer_version")
    def test_constructor_custom_query_options_env_config(self, mock_ver, mock_stats):
        from google.cloud.spanner_v1 import ExecuteSqlRequest
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (MUT.SPANNER_ADMIN_SCOPE,)
        creds = _make_credentials()
        mock_ver.return_value = "2"
        mock_stats.return_value = "auto_20191128_14_47_22UTC"
        query_options = ExecuteSqlRequest.QueryOptions(
            optimizer_version="1",
            optimizer_statistics_package="auto_20191128_10_47_22UTC",
        )
        expected_query_options = ExecuteSqlRequest.QueryOptions(
            optimizer_version="2",
            optimizer_statistics_package="auto_20191128_14_47_22UTC",
        )
        self._constructor_test_helper(
            expected_scopes,
            creds,
            query_options=query_options,
            expected_query_options=expected_query_options,
        )

    @mock.patch("google.cloud.spanner_v1.client._get_spanner_emulator_host")
    def test_instance_admin_api(self, mock_em):
        from google.cloud.spanner_v1.client import SPANNER_ADMIN_SCOPE
        from google.api_core.client_options import ClientOptions

        mock_em.return_value = None

        credentials = _make_credentials()
        client_info = mock.Mock()
        client_options = ClientOptions(quota_project_id="QUOTA-PROJECT")
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )
        expected_scopes = (SPANNER_ADMIN_SCOPE,)

        inst_module = "google.cloud.spanner_v1.client.InstanceAdminClient"
        with mock.patch(inst_module) as instance_admin_client:
            api = client.instance_admin_api

        self.assertIs(api, instance_admin_client.return_value)

        # API instance is cached
        again = client.instance_admin_api
        self.assertIs(again, api)

        instance_admin_client.assert_called_once_with(
            credentials=mock.ANY, client_info=client_info, client_options=client_options
        )

        credentials.with_scopes.assert_called_once_with(
            expected_scopes, default_scopes=None
        )

    @mock.patch("google.cloud.spanner_v1.client._get_spanner_emulator_host")
    def test_instance_admin_api_emulator_env(self, mock_em):
        from google.api_core.client_options import ClientOptions

        mock_em.return_value = "emulator.host"
        credentials = _make_credentials()
        client_info = mock.Mock()
        client_options = ClientOptions(api_endpoint="endpoint")
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )

        inst_module = "google.cloud.spanner_v1.client.InstanceAdminClient"
        with mock.patch(inst_module) as instance_admin_client:
            api = client.instance_admin_api

        self.assertIs(api, instance_admin_client.return_value)

        # API instance is cached
        again = client.instance_admin_api
        self.assertIs(again, api)

        self.assertEqual(len(instance_admin_client.call_args_list), 1)
        called_args, called_kw = instance_admin_client.call_args
        self.assertEqual(called_args, ())
        self.assertEqual(called_kw["client_info"], client_info)
        self.assertEqual(called_kw["client_options"], client_options)
        self.assertIn("transport", called_kw)
        self.assertNotIn("credentials", called_kw)

    def test_instance_admin_api_emulator_code(self):
        from google.auth.credentials import AnonymousCredentials
        from google.api_core.client_options import ClientOptions

        credentials = AnonymousCredentials()
        client_info = mock.Mock()
        client_options = ClientOptions(api_endpoint="emulator.host")
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )

        inst_module = "google.cloud.spanner_v1.client.InstanceAdminClient"
        with mock.patch(inst_module) as instance_admin_client:
            api = client.instance_admin_api

        self.assertIs(api, instance_admin_client.return_value)

        # API instance is cached
        again = client.instance_admin_api
        self.assertIs(again, api)

        self.assertEqual(len(instance_admin_client.call_args_list), 1)
        called_args, called_kw = instance_admin_client.call_args
        self.assertEqual(called_args, ())
        self.assertEqual(called_kw["client_info"], client_info)
        self.assertEqual(called_kw["client_options"], client_options)
        self.assertIn("transport", called_kw)
        self.assertNotIn("credentials", called_kw)

    @mock.patch("google.cloud.spanner_v1.client._get_spanner_emulator_host")
    def test_database_admin_api(self, mock_em):
        from google.cloud.spanner_v1.client import SPANNER_ADMIN_SCOPE
        from google.api_core.client_options import ClientOptions

        mock_em.return_value = None
        credentials = _make_credentials()
        client_info = mock.Mock()
        client_options = ClientOptions(quota_project_id="QUOTA-PROJECT")
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )
        expected_scopes = (SPANNER_ADMIN_SCOPE,)

        db_module = "google.cloud.spanner_v1.client.DatabaseAdminClient"
        with mock.patch(db_module) as database_admin_client:
            api = client.database_admin_api

        self.assertIs(api, database_admin_client.return_value)

        # API instance is cached
        again = client.database_admin_api
        self.assertIs(again, api)

        database_admin_client.assert_called_once_with(
            credentials=mock.ANY, client_info=client_info, client_options=client_options
        )

        credentials.with_scopes.assert_called_once_with(
            expected_scopes, default_scopes=None
        )

    @mock.patch("google.cloud.spanner_v1.client._get_spanner_emulator_host")
    def test_database_admin_api_emulator_env(self, mock_em):
        from google.api_core.client_options import ClientOptions

        mock_em.return_value = "host:port"
        credentials = _make_credentials()
        client_info = mock.Mock()
        client_options = ClientOptions(api_endpoint="endpoint")
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )

        db_module = "google.cloud.spanner_v1.client.DatabaseAdminClient"
        with mock.patch(db_module) as database_admin_client:
            api = client.database_admin_api

        self.assertIs(api, database_admin_client.return_value)

        # API instance is cached
        again = client.database_admin_api
        self.assertIs(again, api)

        self.assertEqual(len(database_admin_client.call_args_list), 1)
        called_args, called_kw = database_admin_client.call_args
        self.assertEqual(called_args, ())
        self.assertEqual(called_kw["client_info"], client_info)
        self.assertEqual(called_kw["client_options"], client_options)
        self.assertIn("transport", called_kw)
        self.assertNotIn("credentials", called_kw)

    def test_database_admin_api_emulator_code(self):
        from google.auth.credentials import AnonymousCredentials
        from google.api_core.client_options import ClientOptions

        credentials = AnonymousCredentials()
        client_info = mock.Mock()
        client_options = ClientOptions(api_endpoint="emulator.host")
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            client_info=client_info,
            client_options=client_options,
        )

        db_module = "google.cloud.spanner_v1.client.DatabaseAdminClient"
        with mock.patch(db_module) as database_admin_client:
            api = client.database_admin_api

        self.assertIs(api, database_admin_client.return_value)

        # API instance is cached
        again = client.database_admin_api
        self.assertIs(again, api)

        self.assertEqual(len(database_admin_client.call_args_list), 1)
        called_args, called_kw = database_admin_client.call_args
        self.assertEqual(called_args, ())
        self.assertEqual(called_kw["client_info"], client_info)
        self.assertEqual(called_kw["client_options"], client_options)
        self.assertIn("transport", called_kw)
        self.assertNotIn("credentials", called_kw)

    def test_copy(self):
        credentials = _make_credentials()
        # Make sure it "already" is scoped.
        credentials.requires_scopes = False

        client = self._make_one(project=self.PROJECT, credentials=credentials)

        new_client = client.copy()
        self.assertIs(new_client._credentials, client._credentials)
        self.assertEqual(new_client.project, client.project)

    def test_credentials_property(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        self.assertIs(client.credentials, credentials.with_scopes.return_value)

    def test_project_name_property(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        project_name = "projects/" + self.PROJECT
        self.assertEqual(client.project_name, project_name)

    def test_list_instance_configs(self):
        from google.cloud.spanner_admin_instance_v1 import InstanceAdminClient
        from google.cloud.spanner_admin_instance_v1 import (
            InstanceConfig as InstanceConfigPB,
        )
        from google.cloud.spanner_admin_instance_v1 import ListInstanceConfigsRequest
        from google.cloud.spanner_admin_instance_v1 import ListInstanceConfigsResponse

        api = InstanceAdminClient(credentials=mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_config_pbs = ListInstanceConfigsResponse(
            instance_configs=[
                InstanceConfigPB(
                    name=self.CONFIGURATION_NAME,
                    display_name=self.DISPLAY_NAME,
                    leader_options=self.LEADER_OPTIONS,
                )
            ]
        )

        lic_api = api._transport._wrapped_methods[
            api._transport.list_instance_configs
        ] = mock.Mock(return_value=instance_config_pbs)

        response = client.list_instance_configs()
        instance_configs = list(response)

        instance_config = instance_configs[0]
        self.assertIsInstance(instance_config, InstanceConfigPB)
        self.assertEqual(instance_config.name, self.CONFIGURATION_NAME)
        self.assertEqual(instance_config.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance_config.leader_options, self.LEADER_OPTIONS)

        expected_metadata = (
            ("google-cloud-resource-prefix", client.project_name),
            ("x-goog-request-params", "parent={}".format(client.project_name)),
        )
        lic_api.assert_called_once_with(
            ListInstanceConfigsRequest(parent=self.PATH),
            metadata=expected_metadata,
            retry=mock.ANY,
            timeout=mock.ANY,
        )

    def test_list_instance_configs_w_options(self):
        from google.cloud.spanner_admin_instance_v1 import InstanceAdminClient
        from google.cloud.spanner_admin_instance_v1 import (
            InstanceConfig as InstanceConfigPB,
        )
        from google.cloud.spanner_admin_instance_v1 import ListInstanceConfigsRequest
        from google.cloud.spanner_admin_instance_v1 import ListInstanceConfigsResponse

        api = InstanceAdminClient(credentials=mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_config_pbs = ListInstanceConfigsResponse(
            instance_configs=[
                InstanceConfigPB(
                    name=self.CONFIGURATION_NAME, display_name=self.DISPLAY_NAME
                )
            ]
        )

        lic_api = api._transport._wrapped_methods[
            api._transport.list_instance_configs
        ] = mock.Mock(return_value=instance_config_pbs)

        page_size = 42
        list(client.list_instance_configs(page_size=42))

        expected_metadata = (
            ("google-cloud-resource-prefix", client.project_name),
            ("x-goog-request-params", "parent={}".format(client.project_name)),
        )
        lic_api.assert_called_once_with(
            ListInstanceConfigsRequest(parent=self.PATH, page_size=page_size),
            metadata=expected_metadata,
            retry=mock.ANY,
            timeout=mock.ANY,
        )

    def test_instance_factory_defaults(self):
        from google.cloud.spanner_v1.instance import DEFAULT_NODE_COUNT
        from google.cloud.spanner_v1.instance import Instance

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        instance = client.instance(self.INSTANCE_ID)

        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertIsNone(instance.configuration_name)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertEqual(instance.labels, {})
        self.assertIs(instance._client, client)

    def test_instance_factory_explicit(self):
        from google.cloud.spanner_v1.instance import Instance

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        instance = client.instance(
            self.INSTANCE_ID,
            self.CONFIGURATION_NAME,
            display_name=self.DISPLAY_NAME,
            node_count=self.NODE_COUNT,
            labels=self.LABELS,
        )

        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.configuration_name, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(instance.labels, self.LABELS)
        self.assertIs(instance._client, client)

    def test_list_instances(self):
        from google.cloud.spanner_admin_instance_v1 import InstanceAdminClient
        from google.cloud.spanner_admin_instance_v1 import Instance as InstancePB
        from google.cloud.spanner_admin_instance_v1 import ListInstancesRequest
        from google.cloud.spanner_admin_instance_v1 import ListInstancesResponse

        api = InstanceAdminClient(credentials=mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_pbs = ListInstancesResponse(
            instances=[
                InstancePB(
                    name=self.INSTANCE_NAME,
                    config=self.CONFIGURATION_NAME,
                    display_name=self.DISPLAY_NAME,
                    node_count=self.NODE_COUNT,
                    processing_units=self.PROCESSING_UNITS,
                )
            ]
        )

        li_api = api._transport._wrapped_methods[
            api._transport.list_instances
        ] = mock.Mock(return_value=instance_pbs)

        response = client.list_instances()
        instances = list(response)

        instance = instances[0]
        self.assertIsInstance(instance, InstancePB)
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.config, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(instance.processing_units, self.PROCESSING_UNITS)

        expected_metadata = (
            ("google-cloud-resource-prefix", client.project_name),
            ("x-goog-request-params", "parent={}".format(client.project_name)),
        )
        li_api.assert_called_once_with(
            ListInstancesRequest(parent=self.PATH),
            metadata=expected_metadata,
            retry=mock.ANY,
            timeout=mock.ANY,
        )

    def test_list_instances_w_options(self):
        from google.cloud.spanner_admin_instance_v1 import InstanceAdminClient
        from google.cloud.spanner_admin_instance_v1 import ListInstancesRequest
        from google.cloud.spanner_admin_instance_v1 import ListInstancesResponse

        api = InstanceAdminClient(credentials=mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_pbs = ListInstancesResponse(instances=[])

        li_api = api._transport._wrapped_methods[
            api._transport.list_instances
        ] = mock.Mock(return_value=instance_pbs)

        page_size = 42
        filter_ = "name:instance"
        list(client.list_instances(filter_=filter_, page_size=42))

        expected_metadata = (
            ("google-cloud-resource-prefix", client.project_name),
            ("x-goog-request-params", "parent={}".format(client.project_name)),
        )
        li_api.assert_called_once_with(
            ListInstancesRequest(parent=self.PATH, filter=filter_, page_size=page_size),
            metadata=expected_metadata,
            retry=mock.ANY,
            timeout=mock.ANY,
        )
