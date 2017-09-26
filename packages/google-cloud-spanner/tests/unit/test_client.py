# Copyright 2016 Google Inc. All rights reserved.
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

    def test_list_instance_configs_wo_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.gax import INITIAL_PAGE
        from google.cloud.spanner_v1.client import InstanceConfig

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client.connection = object()
        api = client._instance_admin_api = _FauxInstanceAdminAPI()
        config = _InstanceConfigPB(name=self.CONFIGURATION_NAME,
                                   display_name=self.DISPLAY_NAME)
        response = _GAXPageIterator([config])
        api._list_instance_configs_response = response

        iterator = client.list_instance_configs()
        configs = list(iterator)

        self.assertEqual(len(configs), 1)
        config = configs[0]
        self.assertTrue(isinstance(config, InstanceConfig))
        self.assertEqual(config.name, self.CONFIGURATION_NAME)
        self.assertEqual(config.display_name, self.DISPLAY_NAME)

        project, page_size, options = api._listed_instance_configs
        self.assertEqual(project, self.PATH)
        self.assertEqual(page_size, None)
        self.assertIs(options.page_token, INITIAL_PAGE)
        self.assertEqual(
            options.kwargs['metadata'],
            [('google-cloud-resource-prefix', client.project_name)])

    def test_list_instance_configs_w_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.spanner_v1.client import InstanceConfig

        SIZE = 15
        TOKEN_RETURNED = 'TOKEN_RETURNED'
        TOKEN_PASSED = 'TOKEN_PASSED'
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client.connection = object()
        api = client._instance_admin_api = _FauxInstanceAdminAPI()
        config = _InstanceConfigPB(name=self.CONFIGURATION_NAME,
                                   display_name=self.DISPLAY_NAME)
        response = _GAXPageIterator([config], page_token=TOKEN_RETURNED)
        api._list_instance_configs_response = response

        iterator = client.list_instance_configs(SIZE, TOKEN_PASSED)
        page = six.next(iterator.pages)
        next_token = iterator.next_page_token
        configs = list(page)

        self.assertEqual(len(configs), 1)
        config = configs[0]
        self.assertTrue(isinstance(config, InstanceConfig))
        self.assertEqual(config.name, self.CONFIGURATION_NAME)
        self.assertEqual(config.display_name, self.DISPLAY_NAME)
        self.assertEqual(next_token, TOKEN_RETURNED)

        project, page_size, options = api._listed_instance_configs
        self.assertEqual(project, self.PATH)
        self.assertEqual(page_size, SIZE)
        self.assertEqual(options.page_token, TOKEN_PASSED)
        self.assertEqual(
            options.kwargs['metadata'],
            [('google-cloud-resource-prefix', client.project_name)])

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

    def test_list_instances_wo_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.gax import INITIAL_PAGE
        from google.cloud.spanner_v1.instance import Instance

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client.connection = object()
        api = client._instance_admin_api = _FauxInstanceAdminAPI()
        instance = _InstancePB(name=self.INSTANCE_NAME,
                               config=self.CONFIGURATION_NAME,
                               display_name=self.DISPLAY_NAME,
                               node_count=self.NODE_COUNT)
        response = _GAXPageIterator([instance])
        api._list_instances_response = response

        iterator = client.list_instances(filter_='name:TEST')
        instances = list(iterator)

        self.assertEqual(len(instances), 1)
        instance = instances[0]
        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.configuration_name, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)

        project, filter_, page_size, options = api._listed_instances
        self.assertEqual(project, self.PATH)
        self.assertEqual(filter_, 'name:TEST')
        self.assertEqual(page_size, None)
        self.assertIs(options.page_token, INITIAL_PAGE)
        self.assertEqual(
            options.kwargs['metadata'],
            [('google-cloud-resource-prefix', client.project_name)])

    def test_list_instances_w_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.spanner_v1.instance import Instance

        SIZE = 15
        TOKEN_RETURNED = 'TOKEN_RETURNED'
        TOKEN_PASSED = 'TOKEN_PASSED'
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        client.connection = object()
        api = client._instance_admin_api = _FauxInstanceAdminAPI()
        instance = _InstancePB(name=self.INSTANCE_NAME,
                               config=self.CONFIGURATION_NAME,
                               display_name=self.DISPLAY_NAME,
                               node_count=self.NODE_COUNT)
        response = _GAXPageIterator([instance], page_token=TOKEN_RETURNED)
        api._list_instances_response = response

        iterator = client.list_instances(
            page_size=SIZE, page_token=TOKEN_PASSED)
        page = six.next(iterator.pages)
        next_token = iterator.next_page_token
        instances = list(page)

        self.assertEqual(len(instances), 1)
        instance = instances[0]
        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.name, self.INSTANCE_NAME)
        self.assertEqual(instance.configuration_name, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertEqual(next_token, TOKEN_RETURNED)

        project, filter_, page_size, options = api._listed_instances
        self.assertEqual(project, self.PATH)
        self.assertEqual(filter_, '')
        self.assertEqual(page_size, SIZE)
        self.assertEqual(options.page_token, TOKEN_PASSED)
        self.assertEqual(
            options.kwargs['metadata'],
            [('google-cloud-resource-prefix', client.project_name)])


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
