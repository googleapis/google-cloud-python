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

    def _getTargetClass(self):
        from google.cloud.spanner.client import Client

        return Client

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _constructor_test_helper(self, expected_scopes, creds,
                                 user_agent=None,
                                 expected_creds=None):
        from google.cloud.spanner import client as MUT

        user_agent = user_agent or MUT.DEFAULT_USER_AGENT
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                user_agent=user_agent)

        expected_creds = expected_creds or creds.with_scopes.return_value
        self.assertIs(client._credentials, expected_creds)

        self.assertTrue(client._credentials is expected_creds)
        if expected_scopes is not None:
            creds.with_scopes.assert_called_once_with(expected_scopes)

        self.assertEqual(client.project, self.PROJECT)
        self.assertEqual(client.user_agent, user_agent)

    def test_constructor_default_scopes(self):
        from google.cloud.spanner import client as MUT

        expected_scopes = [
            MUT.SPANNER_ADMIN_SCOPE,
        ]
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_user_agent_and_timeout(self):
        from google.cloud.spanner import client as MUT

        CUSTOM_USER_AGENT = 'custom-application'
        expected_scopes = [
            MUT.SPANNER_ADMIN_SCOPE,
        ]
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds,
                                      user_agent=CUSTOM_USER_AGENT)

    def test_constructor_implicit_credentials(self):
        from google.cloud._testing import _Monkey
        from google.cloud.spanner import client as MUT

        creds = _make_credentials()

        def mock_get_credentials():
            return creds

        with _Monkey(MUT, get_credentials=mock_get_credentials):
            self._constructor_test_helper(
                None, None,
                expected_creds=creds.with_scopes.return_value)

    def test_constructor_credentials_wo_create_scoped(self):
        creds = _make_credentials()
        expected_scopes = None
        self._constructor_test_helper(expected_scopes, creds)

    def test_admin_api_lib_name(self):
        from google.cloud.spanner import __version__
        from google.cloud.gapic.spanner_admin_database import v1 as db
        from google.cloud.gapic.spanner_admin_instance import v1 as inst

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
        from google.cloud._testing import _Monkey
        from google.cloud.spanner import client as MUT

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)

        class _Client(object):
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        with _Monkey(MUT, InstanceAdminClient=_Client):
            api = client.instance_admin_api

        self.assertTrue(isinstance(api, _Client))
        again = client.instance_admin_api
        self.assertTrue(again is api)
        self.assertEqual(api.kwargs['lib_name'], 'gccl')

    def test_database_admin_api(self):
        from google.cloud._testing import _Monkey
        from google.cloud.spanner import client as MUT

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)

        class _Client(object):
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        with _Monkey(MUT, DatabaseAdminClient=_Client):
            api = client.database_admin_api

        self.assertTrue(isinstance(api, _Client))
        again = client.database_admin_api
        self.assertTrue(again is api)
        self.assertEqual(api.kwargs['lib_name'], 'gccl')

    def test_copy(self):
        credentials = _Credentials('value')
        client = self._make_one(
            project=self.PROJECT,
            credentials=credentials,
            user_agent=self.USER_AGENT)

        new_client = client.copy()
        self.assertEqual(new_client._credentials, client._credentials)
        self.assertEqual(new_client.project, client.project)
        self.assertEqual(new_client.user_agent, client.user_agent)

    def test_credentials_property(self):
        credentials = _Credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        self.assertTrue(client.credentials is credentials)

    def test_project_name_property(self):
        credentials = _Credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        project_name = 'projects/' + self.PROJECT
        self.assertEqual(client.project_name, project_name)

    def test_list_instance_configs_wo_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.gax import INITIAL_PAGE
        from google.cloud.spanner.client import InstanceConfig

        credentials = _Credentials()
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
        self.assertTrue(options.page_token is INITIAL_PAGE)
        self.assertEqual(
            options.kwargs['metadata'],
            [('google-cloud-resource-prefix', client.project_name)])

    def test_list_instance_configs_w_paging(self):
        import six
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.spanner.client import InstanceConfig

        SIZE = 15
        TOKEN_RETURNED = 'TOKEN_RETURNED'
        TOKEN_PASSED = 'TOKEN_PASSED'
        credentials = _Credentials()
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
        from google.cloud.spanner.instance import DEFAULT_NODE_COUNT
        from google.cloud.spanner.instance import Instance

        credentials = _Credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        instance = client.instance(self.INSTANCE_ID)

        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertIsNone(instance.configuration_name)
        self.assertEqual(instance.display_name, self.INSTANCE_ID)
        self.assertEqual(instance.node_count, DEFAULT_NODE_COUNT)
        self.assertTrue(instance._client is client)

    def test_instance_factory_explicit(self):
        from google.cloud.spanner.instance import Instance

        credentials = _Credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        instance = client.instance(self.INSTANCE_ID, self.CONFIGURATION_NAME,
                                   display_name=self.DISPLAY_NAME,
                                   node_count=self.NODE_COUNT)

        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.instance_id, self.INSTANCE_ID)
        self.assertEqual(instance.configuration_name, self.CONFIGURATION_NAME)
        self.assertEqual(instance.display_name, self.DISPLAY_NAME)
        self.assertEqual(instance.node_count, self.NODE_COUNT)
        self.assertTrue(instance._client is client)

    def test_list_instances_wo_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.gax import INITIAL_PAGE
        from google.cloud.spanner.instance import Instance

        credentials = _Credentials()
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
        self.assertTrue(options.page_token is INITIAL_PAGE)
        self.assertEqual(
            options.kwargs['metadata'],
            [('google-cloud-resource-prefix', client.project_name)])

    def test_list_instances_w_paging(self):
        import six
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.spanner.instance import Instance

        SIZE = 15
        TOKEN_RETURNED = 'TOKEN_RETURNED'
        TOKEN_PASSED = 'TOKEN_PASSED'
        credentials = _Credentials()
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


class _Credentials(object):

    scopes = None

    def __init__(self, access_token=None):
        self._access_token = access_token
        self._tokens = []

    def create_scoped(self, scope):
        self.scopes = scope
        return self

    def __eq__(self, other):
        return self._access_token == other._access_token


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
