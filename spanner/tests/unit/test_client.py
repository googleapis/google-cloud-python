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
import six


def _make_credentials():
    import google.auth.credentials

    class _CredentialsWithScopes(
            google.auth.credentials.Credentials,
            google.auth.credentials.Scoped):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


class TestClient(unittest.TestCase):

    PROJECT = 'PROJECT'
    PATH = 'projects/%s' % (PROJECT,)
    CONFIGURATION_NAME = 'config-name'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = '%s/instances/%s' % (PATH, INSTANCE_ID)
    DISPLAY_NAME = 'display-name'
    NODE_COUNT = 5
    TIMEOUT_SECONDS = 80
    USER_AGENT = 'you-sir-age-int'

    def _get_target_class(self):
        from google.cloud import spanner

        return spanner.Client

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def _constructor_test_helper(self, expected_scopes, creds,
                                 user_agent=None,
                                 expected_creds=None):
        from google.cloud.spanner_v1 import client as MUT

        user_agent = user_agent or MUT.DEFAULT_USER_AGENT
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                user_agent=user_agent)

        expected_creds = expected_creds or creds.with_scopes.return_value
        self.assertIs(client._credentials, expected_creds)

        self.assertIs(client._credentials, expected_creds)
        if expected_scopes is not None:
            creds.with_scopes.assert_called_once_with(expected_scopes)

        self.assertEqual(client.project, self.PROJECT)
        self.assertEqual(client.user_agent, user_agent)

    def test_constructor_default_scopes(self):
        from google.cloud.spanner_v1 import client as MUT

        expected_scopes = (
            MUT.SPANNER_ADMIN_SCOPE,
        )
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_user_agent_and_timeout(self):
        from google.cloud.spanner_v1 import client as MUT

        CUSTOM_USER_AGENT = 'custom-application'
        expected_scopes = (
            MUT.SPANNER_ADMIN_SCOPE,
        )
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds,
                                      user_agent=CUSTOM_USER_AGENT)

    def test_constructor_implicit_credentials(self):
        creds = _make_credentials()

        patch = mock.patch(
            'google.auth.default', return_value=(creds, None))
        with patch as default:
            self._constructor_test_helper(
                None, None,
                expected_creds=creds.with_scopes.return_value)

        default.assert_called_once_with()

    def test_constructor_credentials_wo_create_scoped(self):
        creds = _make_credentials()
        expected_scopes = None
        self._constructor_test_helper(expected_scopes, creds)

    def test_admin_api_lib_name(self):
        from google.cloud.spanner_v1 import __version__
        from google.cloud.spanner_admin_database_v1 import gapic as db
        from google.cloud.spanner_admin_instance_v1 import gapic as inst

        # Get the actual admin client classes.
        DatabaseAdminClient = db.database_admin_client.DatabaseAdminClient
        InstanceAdminClient = inst.instance_admin_client.InstanceAdminClient

        # Test that the DatabaseAdminClient is called with the gccl library
        # name and version.
        with mock.patch.object(DatabaseAdminClient, '__init__') as mock_dac:
            mock_dac.return_value = None
            client = self._make_one(
                credentials=_make_credentials(),
                project='foo',
            )
            self.assertIsInstance(client.database_admin_api,
                                  DatabaseAdminClient)
            mock_dac.assert_called_once()
            self.assertEqual(mock_dac.mock_calls[0][2]['lib_name'], 'gccl')
            self.assertEqual(mock_dac.mock_calls[0][2]['lib_version'],
                             __version__)

        # Test that the InstanceAdminClient is called with the gccl library
        # name and version.
        with mock.patch.object(InstanceAdminClient, '__init__') as mock_iac:
            mock_iac.return_value = None
            client = self._make_one(
                credentials=_make_credentials(),
                project='foo',
            )
            self.assertIsInstance(client.instance_admin_api,
                                  InstanceAdminClient)
            mock_iac.assert_called_once()
            self.assertEqual(mock_iac.mock_calls[0][2]['lib_name'], 'gccl')
            self.assertEqual(mock_iac.mock_calls[0][2]['lib_version'],
                             __version__)

    def test_instance_admin_api(self):
        from google.cloud.spanner_v1 import __version__
        from google.cloud.spanner_v1.client import SPANNER_ADMIN_SCOPE

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        expected_scopes = (SPANNER_ADMIN_SCOPE,)

        inst_module = 'google.cloud.spanner_v1.client.InstanceAdminClient'
        with mock.patch(inst_module) as instance_admin_client:
            api = client.instance_admin_api

        self.assertIs(api, instance_admin_client.return_value)

        # API instance is cached
        again = client.instance_admin_api
        self.assertIs(again, api)

        instance_admin_client.assert_called_once_with(
            lib_name='gccl',
            lib_version=__version__,
            credentials=credentials.with_scopes.return_value)

        credentials.with_scopes.assert_called_once_with(expected_scopes)

    def test_database_admin_api(self):
        from google.cloud.spanner_v1 import __version__
        from google.cloud.spanner_v1.client import SPANNER_ADMIN_SCOPE

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        expected_scopes = (SPANNER_ADMIN_SCOPE,)

        db_module = 'google.cloud.spanner_v1.client.DatabaseAdminClient'
        with mock.patch(db_module) as database_admin_client:
            api = client.database_admin_api

        self.assertIs(api, database_admin_client.return_value)

        # API instance is cached
        again = client.database_admin_api
        self.assertIs(again, api)

        database_admin_client.assert_called_once_with(
            lib_name='gccl',
            lib_version=__version__,
            credentials=credentials.with_scopes.return_value)

        credentials.with_scopes.assert_called_once_with(expected_scopes)

    def test_copy(self):
        credentials = _make_credentials()
        # Make sure it "already" is scoped.
        credentials.requires_scopes = False

        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            user_agent=self.USER_AGENT)

        new_client = client.copy()
        self.assertIs(new_client._credentials, client._credentials)
        self.assertEqual(new_client.project, client.project)
        self.assertEqual(new_client.user_agent, client.user_agent)

    def test_credentials_property(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        self.assertIs(client.credentials, credentials.with_scopes.return_value)

    def test_project_name_property(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        project_name = 'projects/' + self.PROJECT
        self.assertEqual(client.project_name, project_name)

    def test_list_instance_configs(self):
        from google.cloud.spanner_admin_instance_v1.gapic import (
            instance_admin_client)
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2)
        from google.cloud.spanner_v1.client import InstanceConfig

        api = instance_admin_client.InstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_config_pbs = (
            spanner_instance_admin_pb2.ListInstanceConfigsResponse(
                instance_configs=[
                    spanner_instance_admin_pb2.InstanceConfig(
                        name=self.CONFIGURATION_NAME,
                        display_name=self.DISPLAY_NAME),
                ]
            )
        )

        api._list_instance_configs = mock.Mock(
            return_value=instance_config_pbs)

        response = client.list_instance_configs()
        instance_configs = list(response)

        instance_config = instance_configs[0]
        self.assertIsInstance(instance_config, InstanceConfig)
        self.assertEqual(instance_config.name, self.CONFIGURATION_NAME)
        self.assertEqual(instance_config.display_name, self.DISPLAY_NAME)

        api._list_instance_configs.assert_called_once_with(
            spanner_instance_admin_pb2.ListInstanceConfigsRequest(
                parent=self.PATH),
            metadata=[('google-cloud-resource-prefix', client.project_name)],
            retry=mock.ANY,
            timeout=mock.ANY)

    def test_list_instance_configs_w_options(self):
        from google.cloud.spanner_admin_instance_v1.gapic import (
            instance_admin_client)
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2)

        api = instance_admin_client.InstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_config_pbs = (
            spanner_instance_admin_pb2.ListInstanceConfigsResponse(
                instance_configs=[
                    spanner_instance_admin_pb2.InstanceConfig(
                        name=self.CONFIGURATION_NAME,
                        display_name=self.DISPLAY_NAME),
                ]
            )
        )

        api._list_instance_configs = mock.Mock(
            return_value=instance_config_pbs)

        token = 'token'
        page_size = 42
        list(client.list_instance_configs(page_token=token, page_size=42))

        api._list_instance_configs.assert_called_once_with(
            spanner_instance_admin_pb2.ListInstanceConfigsRequest(
                parent=self.PATH,
                page_size=page_size,
                page_token=token),
            metadata=[('google-cloud-resource-prefix', client.project_name)],
            retry=mock.ANY,
            timeout=mock.ANY)

    def test_instance_factory_defaults(self):
        from google.cloud.spanner_v1.instance import DEFAULT_NODE_COUNT
        from google.cloud.spanner_v1.instance import Instance

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        instance = client.instance(self.INSTANCE_ID)

        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertIsNone(instance.configuration_name)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertIs(instance._client, client)

    def test_instance_factory_explicit(self):
        from google.cloud.spanner_v1.instance import Instance

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        instance = client.instance(self.INSTANCE_ID, self.CONFIGURATION_NAME,
                                   display_name=self.DISPLAY_NAME,
                                   node_count=self.NODE_COUNT)

        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.configuration_name, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertIs(instance._client, client)

    def test_list_instances(self):
        from google.cloud.spanner_admin_instance_v1.gapic import (
            instance_admin_client)
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2)
        from google.cloud.spanner_v1.client import Instance

        api = instance_admin_client.InstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_pbs = (
            spanner_instance_admin_pb2.ListInstancesResponse(
                instances=[
                    spanner_instance_admin_pb2.Instance(
                        name=self.INSTANCE_NAME,
                        config=self.CONFIGURATION_NAME,
                        display_name=self.DISPLAY_NAME,
                        node_count=self.NODE_COUNT),
                ]
            )
        )

        api._list_instances = mock.Mock(
            return_value=instance_pbs)

        response = client.list_instances()
        instances = list(response)

        instance = instances[0]
        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.configuration_name, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)

        api._list_instances.assert_called_once_with(
            spanner_instance_admin_pb2.ListInstancesRequest(
                parent=self.PATH),
            metadata=[('google-cloud-resource-prefix', client.project_name)],
            retry=mock.ANY,
            timeout=mock.ANY)

    def test_list_instances_w_options(self):
        from google.cloud.spanner_admin_instance_v1.gapic import (
            instance_admin_client)
        from google.cloud.spanner_admin_instance_v1.proto import (
            spanner_instance_admin_pb2)

        api = instance_admin_client.InstanceAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client._instance_admin_api = api

        instance_pbs = (
            spanner_instance_admin_pb2.ListInstancesResponse(
                instances=[]
            )
        )

        api._list_instances = mock.Mock(
            return_value=instance_pbs)

        token = 'token'
        page_size = 42
        list(client.list_instances(page_token=token, page_size=42))

        api._list_instances.assert_called_once_with(
            spanner_instance_admin_pb2.ListInstancesRequest(
                parent=self.PATH,
                page_size=page_size,
                page_token=token),
            metadata=[('google-cloud-resource-prefix', client.project_name)],
            retry=mock.ANY,
            timeout=mock.ANY)


class _FauxInstanceAdminAPI(object):

    def list_instance_configs(self, name, page_size, options):
        self._listed_instance_configs = (name, page_size, options)
        return self._list_instance_configs_response

    def list_instances(self, name, filter_, page_size, options):
        self._listed_instances = (name, filter_, page_size, options)
        return self._list_instances_response


class _InstanceConfigPB(object):

    def __init__(self, name, display_name):
        self.name = name
        self.display_name = display_name


class _InstancePB(object):

    def __init__(self, name, config, display_name=None, node_count=None):
        self.name = name
        self.config = config
        self.display_name = display_name
        self.node_count = node_count
