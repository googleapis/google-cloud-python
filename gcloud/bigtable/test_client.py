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
        PROJECT = 'PROJECT'
        client = self._makeOne(project=PROJECT, credentials=creds,
                               read_only=read_only, admin=admin,
                               user_agent=user_agent,
                               timeout_seconds=timeout_seconds)

        expected_creds = expected_creds or creds
        self.assertTrue(client._credentials is expected_creds)
        if expected_scopes is not None:
            self.assertEqual(client._credentials.scopes, expected_scopes)

        self.assertEqual(client.project, PROJECT)
        self.assertEqual(client.timeout_seconds, timeout_seconds)
        self.assertEqual(client.user_agent, user_agent)
        # Check stubs are set (but null)
        self.assertEqual(client._data_stub_internal, None)
        self.assertEqual(client._cluster_stub_internal, None)
        self.assertEqual(client._operations_stub_internal, None)
        self.assertEqual(client._table_stub_internal, None)

    def test_constructor_default_scopes(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_user_agent_and_timeout(self):
        from gcloud.bigtable import client as MUT

        timeout_seconds = 1337
        user_agent = 'custom-application'
        expected_scopes = [MUT.DATA_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds,
                                      user_agent=user_agent,
                                      timeout_seconds=timeout_seconds)

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
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

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
        project = 'PROJECT'
        timeout_seconds = 123
        user_agent = 'you-sir-age-int'
        client = self._makeOne(project=project, credentials=credentials,
                               read_only=read_only, admin=admin,
                               timeout_seconds=timeout_seconds,
                               user_agent=user_agent)
        # Put some fake stubs in place so that we can verify they
        # don't get copied.
        client._data_stub_internal = object()
        client._cluster_stub_internal = object()
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
        self.assertEqual(new_client._cluster_stub_internal, None)
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

    def test_cluster_stub_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        client._cluster_stub_internal = object()
        self.assertTrue(client._cluster_stub is client._cluster_stub_internal)

    def test_cluster_stub_non_admin_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_cluster_stub')

    def test_cluster_stub_unset_failure(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True)
        with self.assertRaises(ValueError):
            getattr(client, '_cluster_stub')

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
        from gcloud.bigtable.client import DATA_API_HOST
        from gcloud.bigtable.client import DATA_API_PORT
        from gcloud.bigtable.client import DATA_STUB_FACTORY

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
                DATA_STUB_FACTORY,
                DATA_API_HOST,
                DATA_API_PORT,
            ),
        ])

    def test__make_cluster_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import CLUSTER_ADMIN_HOST
        from gcloud.bigtable.client import CLUSTER_ADMIN_PORT
        from gcloud.bigtable.client import CLUSTER_STUB_FACTORY

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        fake_stub = object()
        make_stub_args = []

        def mock_make_stub(*args):
            make_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, _make_stub=mock_make_stub):
            result = client._make_cluster_stub()

        self.assertTrue(result is fake_stub)
        self.assertEqual(make_stub_args, [
            (
                client,
                CLUSTER_STUB_FACTORY,
                CLUSTER_ADMIN_HOST,
                CLUSTER_ADMIN_PORT,
            ),
        ])

    def test__make_operations_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import CLUSTER_ADMIN_HOST
        from gcloud.bigtable.client import CLUSTER_ADMIN_PORT
        from gcloud.bigtable.client import OPERATIONS_STUB_FACTORY

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
                OPERATIONS_STUB_FACTORY,
                CLUSTER_ADMIN_HOST,
                CLUSTER_ADMIN_PORT,
            ),
        ])

    def test__make_table_stub(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT
        from gcloud.bigtable.client import TABLE_ADMIN_HOST
        from gcloud.bigtable.client import TABLE_ADMIN_PORT
        from gcloud.bigtable.client import TABLE_STUB_FACTORY

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
                TABLE_STUB_FACTORY,
                TABLE_ADMIN_HOST,
                TABLE_ADMIN_PORT,
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
            self.assertTrue(client._cluster_stub_internal is stub)
            self.assertTrue(client._operations_stub_internal is stub)
            self.assertTrue(client._table_stub_internal is stub)
            self.assertEqual(stub._entered, 4)
            self.assertEqual(len(make_stub_args), 4)
        else:
            self.assertTrue(client._cluster_stub_internal is None)
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
        client._cluster_stub_internal = stub2
        client._operations_stub_internal = stub2
        client._table_stub_internal = stub2
        client.stop()
        self.assertTrue(client._data_stub_internal is None)
        self.assertTrue(client._cluster_stub_internal is None)
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
        client._cluster_stub_internal = cluster_stub = object()
        client.stop()
        # Make sure the cluster stub did not change.
        self.assertEqual(client._cluster_stub_internal, cluster_stub)

    def test_cluster_factory(self):
        from gcloud.bigtable.cluster import Cluster

        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)

        zone = 'zone'
        cluster_id = 'cluster-id'
        display_name = 'display-name'
        serve_nodes = 42
        cluster = client.cluster(zone, cluster_id, display_name=display_name,
                                 serve_nodes=serve_nodes)
        self.assertTrue(isinstance(cluster, Cluster))
        self.assertEqual(cluster.zone, zone)
        self.assertEqual(cluster.cluster_id, cluster_id)
        self.assertEqual(cluster.display_name, display_name)
        self.assertEqual(cluster.serve_nodes, serve_nodes)
        self.assertTrue(cluster._client is client)

    def _list_zones_helper(self, zone_status):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        credentials = _Credentials()
        project = 'PROJECT'
        timeout_seconds = 281330
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True, timeout_seconds=timeout_seconds)

        # Create request_pb
        request_pb = messages_pb2.ListZonesRequest(
            name='projects/' + project,
        )

        # Create response_pb
        zone1 = 'foo'
        zone2 = 'bar'
        response_pb = messages_pb2.ListZonesResponse(
            zones=[
                data_pb2.Zone(display_name=zone1, status=zone_status),
                data_pb2.Zone(display_name=zone2, status=zone_status),
            ],
        )

        # Patch the stub used by the API method.
        client._cluster_stub_internal = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = [zone1, zone2]

        # Perform the method and check the result.
        result = client.list_zones()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ListZones',
            (request_pb, timeout_seconds),
            {},
        )])

    def test_list_zones(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        self._list_zones_helper(data_pb2.Zone.OK)

    def test_list_zones_failure(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        with self.assertRaises(ValueError):
            self._list_zones_helper(data_pb2.Zone.EMERGENCY_MAINENANCE)

    def test_list_clusters(self):
        from gcloud.bigtable._generated import (
            bigtable_cluster_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_cluster_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        credentials = _Credentials()
        project = 'PROJECT'
        timeout_seconds = 8004
        client = self._makeOne(project=project, credentials=credentials,
                               admin=True, timeout_seconds=timeout_seconds)

        # Create request_pb
        request_pb = messages_pb2.ListClustersRequest(
            name='projects/' + project,
        )

        # Create response_pb
        zone = 'foo'
        failed_zone = 'bar'
        cluster_id1 = 'cluster-id1'
        cluster_id2 = 'cluster-id2'
        cluster_name1 = ('projects/' + project + '/zones/' + zone +
                         '/clusters/' + cluster_id1)
        cluster_name2 = ('projects/' + project + '/zones/' + zone +
                         '/clusters/' + cluster_id2)
        response_pb = messages_pb2.ListClustersResponse(
            failed_zones=[
                data_pb2.Zone(display_name=failed_zone),
            ],
            clusters=[
                data_pb2.Cluster(
                    name=cluster_name1,
                    display_name=cluster_name1,
                    serve_nodes=3,
                ),
                data_pb2.Cluster(
                    name=cluster_name2,
                    display_name=cluster_name2,
                    serve_nodes=3,
                ),
            ],
        )

        # Patch the stub used by the API method.
        client._cluster_stub_internal = stub = _FakeStub(response_pb)

        # Create expected_result.
        failed_zones = [failed_zone]
        clusters = [
            client.cluster(zone, cluster_id1),
            client.cluster(zone, cluster_id2),
        ]
        expected_result = (clusters, failed_zones)

        # Perform the method and check the result.
        result = client.list_clusters()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ListClusters',
            (request_pb, timeout_seconds),
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

        credentials = _Credentials()
        project = 'PROJECT'
        user_agent = 'USER_AGENT'
        client = Client(project=project, credentials=credentials,
                        user_agent=user_agent)
        transformer = self._makeOne(client)
        self.assertTrue(transformer._credentials is credentials)
        self.assertEqual(transformer._user_agent, user_agent)
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
