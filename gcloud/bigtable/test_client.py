# Copyright 2015 Google Inc. All rights reserved.
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


import unittest2


class TestClient(unittest2.TestCase):

    PROJECT = 'PROJECT'
    INSTANCE_ID = 'instance-id'
    DISPLAY_NAME = 'display-name'
    TIMEOUT_SECONDS = 80
    USER_AGENT = 'you-sir-age-int'

    def _getTargetClass(self):
        from gcloud.bigtable.client import Client
        return Client

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _constructor_test_helper(self, expected_scopes, creds,
                                 read_only=False, admin=False,
                                 user_agent=None, timeout_seconds=None,
                                 expected_creds=None):
        from gcloud.bigtable import client as MUT

        user_agent = user_agent or MUT.DEFAULT_USER_AGENT
        timeout_seconds = timeout_seconds or MUT.DEFAULT_TIMEOUT_SECONDS
        client = self._makeOne(project=self.PROJECT, credentials=creds,
                               read_only=read_only, admin=admin,
                               user_agent=user_agent,
                               timeout_seconds=timeout_seconds)

        expected_creds = expected_creds or creds
        self.assertTrue(client._credentials is expected_creds)
        if expected_scopes is not None:
            self.assertEqual(client._credentials.scopes, expected_scopes)

        self.assertEqual(client.project, self.PROJECT)
        self.assertEqual(client.timeout_seconds, timeout_seconds)
        self.assertEqual(client.user_agent, user_agent)
        # Check stubs are set (but null)
        self.assertEqual(client._data_stub_internal, None)
        self.assertEqual(client._instance_stub_internal, None)
        self.assertEqual(client._operations_stub_internal, None)
        self.assertEqual(client._table_stub_internal, None)

    def test_constructor_default_scopes(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_user_agent_and_timeout(self):
        from gcloud.bigtable import client as MUT

        CUSTOM_TIMEOUT_SECONDS = 1337
        CUSTOM_USER_AGENT = 'custom-application'
        expected_scopes = [MUT.DATA_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds,
                                      user_agent=CUSTOM_USER_AGENT,
                                      timeout_seconds=CUSTOM_TIMEOUT_SECONDS)

    def test_constructor_with_admin(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE, MUT.ADMIN_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds, admin=True)

    def test_constructor_with_read_only(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.READ_ONLY_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds, read_only=True)

    def test_constructor_both_admin_and_read_only(self):
        creds = _Credentials()
        with self.assertRaises(ValueError):
            self._constructor_test_helper([], creds, admin=True,
                                          read_only=True)

    def test_constructor_implicit_credentials(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT

        creds = _Credentials()
        expected_scopes = [MUT.DATA_SCOPE]

        def mock_get_credentials():
            return creds

        with _Monkey(MUT, get_credentials=mock_get_credentials):
            self._constructor_test_helper(expected_scopes, None,
                                          expected_creds=creds)

    def test_constructor_credentials_wo_create_scoped(self):
        creds = object()
        expected_scopes = None
        self._constructor_test_helper(expected_scopes, creds)

    def _context_manager_helper(self):
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)

        def mock_start():
            client._data_stub_internal = object()
        client.start = mock_start

        def mock_stop():
            client._data_stub_internal = None
        client.stop = mock_stop
        return client

    def test_context_manager(self):
        client = self._context_manager_helper()
        self.assertFalse(client.is_started())
        with client:
            self.assertTrue(client.is_started())
        self.assertFalse(client.is_started())

    def test_context_manager_as_keyword(self):
        with self._context_manager_helper() as client:
            self.assertIsNotNone(client)

    def test_context_manager_with_exception(self):
        client = self._context_manager_helper()
        self.assertFalse(client.is_started())

        class DummyException(Exception):
            pass
        try:
            with client:
                self.assertTrue(client.is_started())
                raise DummyException()
        except DummyException:
            pass
        self.assertFalse(client.is_started())

    def _copy_test_helper(self, read_only=False, admin=False):
        credentials = _Credentials('value')
        client = self._makeOne(
            project=self.PROJECT,
            credentials=credentials,
            read_only=read_only,
            admin=admin,
            timeout_seconds=self.TIMEOUT_SECONDS,
            user_agent=self.USER_AGENT)
        # Put some fake stubs in place so that we can verify they
        # don't get copied.
        client._data_stub_internal = object()
        client._instance_stub_internal = object()
        client._operations_stub_internal = object()
        client._table_stub_internal = object()

        new_client = client.copy()
        self.assertEqual(new_client._admin, client._admin)
        self.assertEqual(new_client._credentials, client._credentials)
        self.assertEqual(new_client.project, client.project)
        self.assertEqual(new_client.user_agent, client.user_agent)
        self.assertEqual(new_client.timeout_seconds, client.timeout_seconds)
        # Make sure stubs are not preserved.
        self.assertEqual(new_client._data_stub_internal, None)
        self.assertEqual(new_client._instance_stub_internal, None)
        self.assertEqual(new_client._operations_stub_internal, None)
        self.assertEqual(new_client._table_stub_internal, None)

    def test_copy(self):
        self._copy_test_helper()

    def test_copy_admin(self):
        self._copy_test_helper(admin=True)

    def test_copy_read_only(self):
        self._copy_test_helper(read_only=True)

    def test_credentials_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        self.assertTrue(client.credentials is credentials)

    def test_project_name_property(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        project_name = 'projects/' + project
        self.assertEqual(client.project_name, project_name)

    def test_data_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        client._data_stub_internal = object()
        self.assertTrue(client._data_stub is client._data_stub_internal)

    def test_data_stub_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        with self.assertRaises(ValueError):
            getattr(client, '_data_stub')

    def test_instance_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        client._instance_stub_internal = object()
        self.assertTrue(
            client._instance_stub is client._instance_stub_internal)

    def test_instance_stub_non_admin_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_instance_stub')

    def test_instance_stub_unset_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        with self.assertRaises(ValueError):
            getattr(client, '_instance_stub')

    def test_operations_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        client._operations_stub_internal = object()
        self.assertTrue(client._operations_stub is
                        client._operations_stub_internal)

    def test_operations_stub_non_admin_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_operations_stub')

    def test_operations_stub_unset_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        with self.assertRaises(ValueError):
            getattr(client, '_operations_stub')

    def test_table_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        client._table_stub_internal = object()
        self.assertTrue(client._table_stub is client._table_stub_internal)

    def test_table_stub_non_admin_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_table_stub')

    def test_table_stub_unset_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        with self.assertRaises(ValueError):
            getattr(client, '_table_stub')

    def test__make_data_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import DATA_API_HOST_V2
        from gcloud.bigtable.client import DATA_API_PORT_V2
        from gcloud.bigtable.client import DATA_STUB_FACTORY_V2

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, _make_stub=mock_make_stub):
            result = client._make_data_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                DATA_STUB_FACTORY_V2,
                DATA_API_HOST_V2,
                DATA_API_PORT_V2,
            ),
        ])

    def test__make_instance_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import INSTANCE_ADMIN_HOST_V2
        from gcloud.bigtable.client import INSTANCE_ADMIN_PORT_V2
        from gcloud.bigtable.client import INSTANCE_STUB_FACTORY_V2

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, _make_stub=mock_make_stub):
            result = client._make_instance_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                INSTANCE_STUB_FACTORY_V2,
                INSTANCE_ADMIN_HOST_V2,
                INSTANCE_ADMIN_PORT_V2,
            ),
        ])

    def test__make_operations_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import OPERATIONS_API_HOST_V2
        from gcloud.bigtable.client import OPERATIONS_API_PORT_V2
        from gcloud.bigtable.client import OPERATIONS_STUB_FACTORY_V2

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, _make_stub=mock_make_stub):
            result = client._make_operations_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                OPERATIONS_STUB_FACTORY_V2,
                OPERATIONS_API_HOST_V2,
                OPERATIONS_API_PORT_V2,
            ),
        ])

    def test__make_table_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import TABLE_ADMIN_HOST_V2
        from gcloud.bigtable.client import TABLE_ADMIN_PORT_V2
        from gcloud.bigtable.client import TABLE_STUB_FACTORY_V2

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, _make_stub=mock_make_stub):
            result = client._make_table_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                TABLE_STUB_FACTORY_V2,
                TABLE_ADMIN_HOST_V2,
                TABLE_ADMIN_PORT_V2,
            ),
        ])

    def test_is_started(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        self.assertFalse(client.is_started())
        client._data_stub_internal = object()
        self.assertTrue(client.is_started())
        client._data_stub_internal = None
        self.assertFalse(client.is_started())

    def _start_method_helper(self, admin):
        from gcloud._testing import _Monkey
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import client as MUT

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=admin)

        stub = _FakeStub()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return stub

        with _Monkey(MUT, _make_stub=mock_make_stub):
            client.start()

        self.assertTrue(client._data_stub_internal is stub)
        if admin:
            self.assertTrue(client._instance_stub_internal is stub)
            self.assertTrue(client._operations_stub_internal is stub)
            self.assertTrue(client._table_stub_internal is stub)
            self.assertEqual(stub._entered, 4)
            self.assertEqual(len(make_stub_args), 4)
        else:
            self.assertTrue(client._instance_stub_internal is None)
            self.assertTrue(client._operations_stub_internal is None)
            self.assertTrue(client._table_stub_internal is None)
            self.assertEqual(stub._entered, 1)
            self.assertEqual(len(make_stub_args), 1)
        self.assertEqual(stub._exited, [])

    def test_start_non_admin(self):
        self._start_method_helper(admin=False)

    def test_start_with_admin(self):
        self._start_method_helper(admin=True)

    def test_start_while_started(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        client._data_stub_internal = data_stub = object()
        self.assertTrue(client.is_started())
        client.start()

        # Make sure the stub did not change.
        self.assertEqual(client._data_stub_internal, data_stub)

    def _stop_method_helper(self, admin):
        from gcloud.bigtable._testing import _FakeStub

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=admin)

        stub1 = _FakeStub()
        stub2 = _FakeStub()
        client._data_stub_internal = stub1
        client._instance_stub_internal = stub2
        client._operations_stub_internal = stub2
        client._table_stub_internal = stub2
        client.stop()
        self.assertTrue(client._data_stub_internal is None)
        self.assertTrue(client._instance_stub_internal is None)
        self.assertTrue(client._operations_stub_internal is None)
        self.assertTrue(client._table_stub_internal is None)
        self.assertEqual(stub1._entered, 0)
        self.assertEqual(stub2._entered, 0)
        exc_none_triple = (None, None, None)
        self.assertEqual(stub1._exited, [exc_none_triple])
        if admin:
            self.assertEqual(stub2._exited, [exc_none_triple] * 3)
        else:
            self.assertEqual(stub2._exited, [])

    def test_stop_non_admin(self):
        self._stop_method_helper(admin=False)

    def test_stop_with_admin(self):
        self._stop_method_helper(admin=True)

    def test_stop_while_stopped(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        self.assertFalse(client.is_started())

        # This is a bit hacky. We set the cluster stub protected value
        # since it isn't used in is_started() and make sure that stop
        # doesn't reset this value to None.
        client._instance_stub_internal = instance_stub = object()
        client.stop()
        # Make sure the cluster stub did not change.
        self.assertEqual(client._instance_stub_internal, instance_stub)

    def test_instance_factory_defaults(self):
        from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES
        from gcloud.bigtable.instance import Instance
        from gcloud.bigtable.instance import _EXISTING_INSTANCE_LOCATION_ID

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        DISPLAY_NAME = 'display-name'
        credentials = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=credentials)

        instance = client.instance(INSTANCE_ID, display_name=DISPLAY_NAME)

        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.instance_id, INSTANCE_ID)
        self.assertEqual(instance.display_name, DISPLAY_NAME)
        self.assertEqual(instance._cluster_location_id,
                         _EXISTING_INSTANCE_LOCATION_ID)
        self.assertEqual(instance._cluster_serve_nodes, DEFAULT_SERVE_NODES)
        self.assertTrue(instance._client is client)

    def test_instance_factory_w_explicit_serve_nodes(self):
        from gcloud.bigtable.instance import Instance

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        DISPLAY_NAME = 'display-name'
        LOCATION_ID = 'locname'
        SERVE_NODES = 5
        credentials = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=credentials)

        instance = client.instance(
            INSTANCE_ID, display_name=DISPLAY_NAME,
            location=LOCATION_ID, serve_nodes=SERVE_NODES)

        self.assertTrue(isinstance(instance, Instance))
        self.assertEqual(instance.instance_id, INSTANCE_ID)
        self.assertEqual(instance.display_name, DISPLAY_NAME)
        self.assertEqual(instance._cluster_location_id, LOCATION_ID)
        self.assertEqual(instance._cluster_serve_nodes, SERVE_NODES)
        self.assertTrue(instance._client is client)

    def test_list_instances(self):
        from gcloud.bigtable._generated_v2 import (
            instance_pb2 as data_v2_pb2)
        from gcloud.bigtable._generated_v2 import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from gcloud.bigtable._testing import _FakeStub

        LOCATION = 'projects/' + self.PROJECT + '/locations/locname'
        FAILED_LOCATION = 'FAILED'
        INSTANCE_ID1 = 'instance-id1'
        INSTANCE_ID2 = 'instance-id2'
        INSTANCE_NAME1 = (
            'projects/' + self.PROJECT + '/instances/' + INSTANCE_ID1)
        INSTANCE_NAME2 = (
            'projects/' + self.PROJECT + '/instances/' + INSTANCE_ID2)

        credentials = _Credentials()
        client = self._makeOne(
            project=self.PROJECT,
            credentials=credentials,
            admin=True,
            timeout_seconds=self.TIMEOUT_SECONDS,
        )

        # Create request_pb
        request_pb = messages_v2_pb2.ListInstancesRequest(
            parent='projects/' + self.PROJECT,
        )

        # Create response_pb
        response_pb = messages_v2_pb2.ListInstancesResponse(
            failed_locations=[
                FAILED_LOCATION,
            ],
            instances=[
                data_v2_pb2.Instance(
                    name=INSTANCE_NAME1,
                    display_name=INSTANCE_NAME1,
                ),
                data_v2_pb2.Instance(
                    name=INSTANCE_NAME2,
                    display_name=INSTANCE_NAME2,
                ),
            ],
        )

        # Patch the stub used by the API method.
        client._instance_stub_internal = stub = _FakeStub(response_pb)

        # Create expected_result.
        failed_locations = [FAILED_LOCATION]
        instances = [
            client.instance(INSTANCE_ID1, LOCATION),
            client.instance(INSTANCE_ID2, LOCATION),
        ]
        expected_result = (instances, failed_locations)

        # Perform the method and check the result.
        result = client.list_instances()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ListInstances',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])


class Test_MetadataPlugin(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.client import _MetadataPlugin
        return _MetadataPlugin

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        from gcloud.bigtable.client import Client
        from gcloud.bigtable.client import DATA_SCOPE
        PROJECT = 'PROJECT'
        USER_AGENT = 'USER_AGENT'

        credentials = _Credentials()
        client = Client(project=PROJECT, credentials=credentials,
                        user_agent=USER_AGENT)
        transformer = self._makeOne(client)
        self.assertTrue(transformer._credentials is credentials)
        self.assertEqual(transformer._user_agent, USER_AGENT)
        self.assertEqual(credentials.scopes, [DATA_SCOPE])

    def test___call__(self):
        from gcloud.bigtable.client import Client
        from gcloud.bigtable.client import DATA_SCOPE
        from gcloud.bigtable.client import DEFAULT_USER_AGENT

        access_token_expected = 'FOOBARBAZ'
        credentials = _Credentials(access_token=access_token_expected)
        project = 'PROJECT'
        client = Client(project=project, credentials=credentials)
        callback_args = []

        def callback(*args):
            callback_args.append(args)

        transformer = self._makeOne(client)
        result = transformer(None, callback)
        cb_headers = [
            ('Authorization', 'Bearer ' + access_token_expected),
            ('User-agent', DEFAULT_USER_AGENT),
        ]
        self.assertEqual(result, None)
        self.assertEqual(callback_args, [(cb_headers, None)])
        self.assertEqual(credentials.scopes, [DATA_SCOPE])
        self.assertEqual(len(credentials._tokens), 1)


class Test__make_stub(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.client import _make_stub
        return _make_stub(*args, **kwargs)

    def test_it(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT

        mock_result = object()
        stub_inputs = []

        SSL_CREDS = object()
        METADATA_CREDS = object()
        COMPOSITE_CREDS = object()
        CHANNEL = object()

        class _ImplementationsModule(object):

            def __init__(self):
                self.ssl_channel_credentials_args = None
                self.metadata_call_credentials_args = None
                self.composite_channel_credentials_args = None
                self.secure_channel_args = None

            def ssl_channel_credentials(self, *args):
                self.ssl_channel_credentials_args = args
                return SSL_CREDS

            def metadata_call_credentials(self, *args, **kwargs):
                self.metadata_call_credentials_args = (args, kwargs)
                return METADATA_CREDS

            def composite_channel_credentials(self, *args):
                self.composite_channel_credentials_args = args
                return COMPOSITE_CREDS

            def secure_channel(self, *args):
                self.secure_channel_args = args
                return CHANNEL

        implementations_mod = _ImplementationsModule()

        def mock_stub_factory(channel):
            stub_inputs.append(channel)
            return mock_result

        metadata_plugin = object()
        clients = []

        def mock_plugin(client):
            clients.append(client)
            return metadata_plugin

        host = 'HOST'
        port = 1025
        client = object()
        with _Monkey(MUT, implementations=implementations_mod,
                     _MetadataPlugin=mock_plugin):
            result = self._callFUT(client, mock_stub_factory, host, port)

        self.assertTrue(result is mock_result)
        self.assertEqual(stub_inputs, [CHANNEL])
        self.assertEqual(clients, [client])
        self.assertEqual(implementations_mod.ssl_channel_credentials_args,
                         (None, None, None))
        self.assertEqual(implementations_mod.metadata_call_credentials_args,
                         ((metadata_plugin,), {'name': 'google_creds'}))
        self.assertEqual(
            implementations_mod.composite_channel_credentials_args,
            (SSL_CREDS, METADATA_CREDS))
        self.assertEqual(implementations_mod.secure_channel_args,
                         (host, port, COMPOSITE_CREDS))


class _Credentials(object):

    scopes = None

    def __init__(self, access_token=None):
        self._access_token = access_token
        self._tokens = []

    def get_access_token(self):
        from oauth2client.client import AccessTokenInfo
        token = AccessTokenInfo(access_token=self._access_token,
                                expires_in=None)
        self._tokens.append(token)
        return token

    def create_scoped(self, scope):
        self.scopes = scope
        return self

    def __eq__(self, other):
        return self._access_token == other._access_token
