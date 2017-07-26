# Copyright 2015 Google Inc.
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


class Test__make_data_stub(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.bigtable.client import _make_data_stub

        return _make_data_stub(client)

    @mock.patch('google.cloud.bigtable.client.make_secure_stub',
                return_value=mock.sentinel.stub)
    def test_without_emulator(self, make_stub):
        from google.cloud.bigtable import client as MUT

        credentials = _make_credentials()
        user_agent = 'you-sir-age-int'
        client = _Client(credentials, user_agent)

        result = self._call_fut(client)
        self.assertIs(result, mock.sentinel.stub)
        make_stub.assert_called_once_with(
            client.credentials,
            client.user_agent,
            MUT.bigtable_pb2.BigtableStub,
            MUT.DATA_API_HOST,
            extra_options=MUT._GRPC_MAX_LENGTH_OPTIONS,
        )

    def test_with_emulator(self):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import client as MUT

        emulator_host = object()
        client = _Client(None, None, emulator_host=emulator_host)

        fake_stub = object()
        make_insecure_stub_args = []

        def mock_make_insecure_stub(*args):
            make_insecure_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, make_insecure_stub=mock_make_insecure_stub):
            result = self._call_fut(client)

        self.assertIs(result, fake_stub)
        self.assertEqual(make_insecure_stub_args, [
            (
                MUT.bigtable_pb2.BigtableStub,
                emulator_host,
            ),
        ])


class Test__make_instance_stub(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.bigtable.client import _make_instance_stub

        return _make_instance_stub(client)

    @mock.patch('google.cloud.bigtable.client.make_secure_stub',
                return_value=mock.sentinel.stub)
    def test_without_emulator(self, make_stub):
        from google.cloud.bigtable import client as MUT

        credentials = _make_credentials()
        user_agent = 'you-sir-age-int'
        client = _Client(credentials, user_agent)

        result = self._call_fut(client)
        self.assertIs(result, mock.sentinel.stub)
        make_stub.assert_called_once_with(
            client.credentials,
            client.user_agent,
            MUT.bigtable_instance_admin_pb2.BigtableInstanceAdminStub,
            MUT.INSTANCE_ADMIN_HOST,
            extra_options=MUT._GRPC_EXTRA_OPTIONS,
        )

    def test_with_emulator(self):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import client as MUT

        emulator_host = object()
        client = _Client(None, None, emulator_host=emulator_host)

        fake_stub = object()
        make_insecure_stub_args = []

        def mock_make_insecure_stub(*args):
            make_insecure_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, make_insecure_stub=mock_make_insecure_stub):
            result = self._call_fut(client)

        self.assertIs(result, fake_stub)
        self.assertEqual(make_insecure_stub_args, [
            (
                MUT.bigtable_instance_admin_pb2.BigtableInstanceAdminStub,
                emulator_host,
            ),
        ])


class Test__make_operations_stub(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.bigtable.client import _make_operations_stub

        return _make_operations_stub(client)

    @mock.patch('google.cloud.bigtable.client.make_secure_stub',
                return_value=mock.sentinel.stub)
    def test_without_emulator(self, make_stub):
        from google.longrunning import operations_grpc
        from google.cloud.bigtable import client as MUT

        credentials = _make_credentials()
        user_agent = 'you-sir-age-int'
        client = _Client(credentials, user_agent)

        result = self._call_fut(client)
        self.assertIs(result, mock.sentinel.stub)
        make_stub.assert_called_once_with(
            client.credentials,
            client.user_agent,
            operations_grpc.OperationsStub,
            MUT.OPERATIONS_API_HOST,
            extra_options=MUT._GRPC_EXTRA_OPTIONS,
        )

    def test_with_emulator(self):
        from google.longrunning import operations_grpc

        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import client as MUT

        emulator_host = object()
        client = _Client(None, None, emulator_host=emulator_host)

        fake_stub = object()
        make_insecure_stub_args = []

        def mock_make_insecure_stub(*args):
            make_insecure_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, make_insecure_stub=mock_make_insecure_stub):
            result = self._call_fut(client)

        self.assertIs(result, fake_stub)
        self.assertEqual(make_insecure_stub_args, [
            (
                operations_grpc.OperationsStub,
                emulator_host,
            ),
        ])


class Test__make_table_stub(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.bigtable.client import _make_table_stub

        return _make_table_stub(client)

    @mock.patch('google.cloud.bigtable.client.make_secure_stub',
                return_value=mock.sentinel.stub)
    def test_without_emulator(self, make_stub):
        from google.cloud.bigtable import client as MUT

        credentials = _make_credentials()
        user_agent = 'you-sir-age-int'
        client = _Client(credentials, user_agent)

        result = self._call_fut(client)
        self.assertIs(result, mock.sentinel.stub)
        make_stub.assert_called_once_with(
            client.credentials,
            client.user_agent,
            MUT.bigtable_table_admin_pb2.BigtableTableAdminStub,
            MUT.TABLE_ADMIN_HOST,
            extra_options=MUT._GRPC_EXTRA_OPTIONS,
        )

    def test_with_emulator(self):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import client as MUT

        emulator_host = object()
        client = _Client(None, None, emulator_host=emulator_host)

        fake_stub = object()
        make_insecure_stub_args = []

        def mock_make_insecure_stub(*args):
            make_insecure_stub_args.append(args)
            return fake_stub

        with _Monkey(MUT, make_insecure_stub=mock_make_insecure_stub):
            result = self._call_fut(client)

        self.assertIs(result, fake_stub)
        self.assertEqual(make_insecure_stub_args, [
            (
                MUT.bigtable_table_admin_pb2.BigtableTableAdminStub,
                emulator_host,
            ),
        ])


class TestClient(unittest.TestCase):

    PROJECT = 'PROJECT'
    INSTANCE_ID = 'instance-id'
    DISPLAY_NAME = 'display-name'
    USER_AGENT = 'you-sir-age-int'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @mock.patch('google.cloud.bigtable.client._make_table_stub')
    @mock.patch('google.cloud.bigtable.client._make_operations_stub')
    @mock.patch('google.cloud.bigtable.client._make_instance_stub')
    @mock.patch('google.cloud.bigtable.client._make_data_stub')
    def _make_one_with_mocks(
            self, _make_data_stub, _make_instance_stub,
            _make_operations_stub, _make_table_stub,
            *args, **kwargs):
        return self._make_one(*args, **kwargs)

    @mock.patch('google.cloud.bigtable.client._make_table_stub')
    @mock.patch('google.cloud.bigtable.client._make_operations_stub')
    @mock.patch('google.cloud.bigtable.client._make_instance_stub')
    @mock.patch('google.cloud.bigtable.client._make_data_stub')
    def test_constructor_default_scopes(
            self, _make_data_stub, _make_instance_stub,
            _make_operations_stub, _make_table_stub):
        from google.cloud.bigtable.client import DATA_SCOPE

        expected_scopes = (DATA_SCOPE,)
        credentials = _make_credentials()
        custom_user_agent = 'custom-application'
        client = self._make_one(
            project=self.PROJECT, credentials=credentials,
            user_agent=custom_user_agent)

        self.assertEqual(client.project, self.PROJECT)
        self.assertIs(
            client._credentials, credentials.with_scopes.return_value)
        self.assertIsNone(client._http_internal)
        self.assertFalse(client._read_only)
        self.assertFalse(client._admin)
        self.assertEqual(client.SCOPE, expected_scopes)
        self.assertEqual(client.user_agent, custom_user_agent)
        self.assertIsNone(client.emulator_host)
        self.assertIs(client._data_stub, _make_data_stub.return_value)
        self.assertIsNone(client._instance_stub_internal)
        self.assertIsNone(client._operations_stub_internal)
        self.assertIsNone(client._table_stub_internal)

        # Check mocks.
        credentials.with_scopes.assert_called_once_with(expected_scopes)
        _make_data_stub.assert_called_once_with(client)
        _make_instance_stub.assert_not_called()
        _make_operations_stub.assert_not_called()
        _make_table_stub.assert_not_called()

    @mock.patch('google.cloud.bigtable.client._make_table_stub')
    @mock.patch('google.cloud.bigtable.client._make_operations_stub')
    @mock.patch('google.cloud.bigtable.client._make_instance_stub')
    @mock.patch('google.cloud.bigtable.client._make_data_stub')
    def test_constructor_with_admin(
            self, _make_data_stub, _make_instance_stub,
            _make_operations_stub, _make_table_stub):
        from google.cloud._http import DEFAULT_USER_AGENT
        from google.cloud.bigtable.client import ADMIN_SCOPE
        from google.cloud.bigtable.client import DATA_SCOPE

        expected_scopes = (DATA_SCOPE, ADMIN_SCOPE)
        credentials = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=credentials, admin=True)

        self.assertEqual(client.project, self.PROJECT)
        self.assertIs(
            client._credentials, credentials.with_scopes.return_value)
        self.assertIsNone(client._http_internal)
        self.assertFalse(client._read_only)
        self.assertTrue(client._admin)
        self.assertEqual(client.SCOPE, expected_scopes)
        self.assertEqual(client.user_agent, DEFAULT_USER_AGENT)
        self.assertIsNone(client.emulator_host)
        self.assertIs(client._data_stub, _make_data_stub.return_value)
        self.assertIs(
            client._instance_stub_internal, _make_instance_stub.return_value)
        self.assertIs(
            client._operations_stub_internal,
            _make_operations_stub.return_value)
        self.assertIs(
            client._table_stub_internal, _make_table_stub.return_value)

        # Check mocks.
        credentials.with_scopes.assert_called_once_with(expected_scopes)
        _make_data_stub.assert_called_once_with(client)
        _make_instance_stub.assert_called_once_with(client)
        _make_operations_stub.assert_called_once_with(client)
        _make_table_stub.assert_called_once_with(client)

    def test_constructor_both_admin_and_read_only(self):
        credentials = _make_credentials()
        with self.assertRaises(ValueError):
            self._make_one(
                project=self.PROJECT, credentials=credentials,
                admin=True, read_only=True)

    def test__get_scopes_default(self):
        from google.cloud.bigtable.client import DATA_SCOPE

        client = self._make_one(
            project=self.PROJECT, credentials=_make_credentials())
        self.assertEqual(client._get_scopes(), (DATA_SCOPE,))

    def test__get_scopes_admin(self):
        from google.cloud.bigtable.client import ADMIN_SCOPE
        from google.cloud.bigtable.client import DATA_SCOPE

        client = self._make_one(
            project=self.PROJECT, credentials=_make_credentials(),
            admin=True)
        expected_scopes = (DATA_SCOPE, ADMIN_SCOPE)
        self.assertEqual(client._get_scopes(), expected_scopes)

    def test__get_scopes_read_only(self):
        from google.cloud.bigtable.client import READ_ONLY_SCOPE

        client = self._make_one(
            project=self.PROJECT, credentials=_make_credentials(),
            read_only=True)
        self.assertEqual(client._get_scopes(), (READ_ONLY_SCOPE,))

    def _copy_helper_check_stubs(self, client, new_client):
        if client._admin:
            # Check the instance stub.
            self.assertIs(
                client._instance_stub_internal, mock.sentinel.inst_stub1)
            self.assertIs(
                new_client._instance_stub_internal, mock.sentinel.inst_stub2)
            self.assertIsNot(
                new_client._instance_stub_internal,
                client._instance_stub_internal)
            # Check the operations stub.
            self.assertIs(
                client._operations_stub_internal, mock.sentinel.ops_stub1)
            self.assertIs(
                new_client._operations_stub_internal, mock.sentinel.ops_stub2)
            self.assertIsNot(
                new_client._operations_stub_internal,
                client._operations_stub_internal)
            # Check the table stub.
            self.assertIs(
                client._table_stub_internal, mock.sentinel.table_stub1)
            self.assertIs(
                new_client._table_stub_internal, mock.sentinel.table_stub2)
            self.assertIsNot(
                new_client._table_stub_internal, client._table_stub_internal)
        else:
            # Check the instance stub.
            self.assertIsNone(client._instance_stub_internal)
            self.assertIsNone(new_client._instance_stub_internal)
            # Check the operations stub.
            self.assertIsNone(client._operations_stub_internal)
            self.assertIsNone(new_client._operations_stub_internal)
            # Check the table stub.
            self.assertIsNone(client._table_stub_internal)
            self.assertIsNone(new_client._table_stub_internal)

    @mock.patch(
        'google.cloud.bigtable.client._make_table_stub',
        side_effect=[mock.sentinel.table_stub1, mock.sentinel.table_stub2],
    )
    @mock.patch(
        'google.cloud.bigtable.client._make_operations_stub',
        side_effect=[mock.sentinel.ops_stub1, mock.sentinel.ops_stub2],
    )
    @mock.patch(
        'google.cloud.bigtable.client._make_instance_stub',
        side_effect=[mock.sentinel.inst_stub1, mock.sentinel.inst_stub2],
    )
    @mock.patch(
        'google.cloud.bigtable.client._make_data_stub',
        side_effect=[mock.sentinel.data_stub1, mock.sentinel.data_stub2],
    )
    def _copy_test_helper(
            self, _make_data_stub, _make_instance_stub,
            _make_operations_stub, _make_table_stub, **kwargs):
        credentials = _make_credentials()
        # Make sure it "already" is scoped.
        credentials.requires_scopes = False

        client = self._make_one(
            project=self.PROJECT, credentials=credentials, **kwargs)
        self.assertIs(client._credentials, credentials)

        new_client = client.copy()
        self.assertEqual(new_client._admin, client._admin)
        self.assertEqual(new_client._credentials, client._credentials)
        self.assertEqual(new_client.project, client.project)
        self.assertEqual(new_client.user_agent, client.user_agent)
        # Make sure stubs are not preserved.
        self.assertIs(client._data_stub, mock.sentinel.data_stub1)
        self.assertIs(new_client._data_stub, mock.sentinel.data_stub2)
        self.assertIsNot(new_client._data_stub, client._data_stub)
        self._copy_helper_check_stubs(client, new_client)

        # Check mocks.
        credentials.with_scopes.assert_not_called()
        stub_calls = [
            mock.call(client),
            mock.call(new_client),
        ]
        self.assertEqual(_make_data_stub.mock_calls, stub_calls)
        if client._admin:
            self.assertEqual(_make_instance_stub.mock_calls, stub_calls)
            self.assertEqual(_make_operations_stub.mock_calls, stub_calls)
            self.assertEqual(_make_table_stub.mock_calls, stub_calls)
        else:
            _make_instance_stub.assert_not_called()
            _make_operations_stub.assert_not_called()
            _make_table_stub.assert_not_called()

    def test_copy(self):
        self._copy_test_helper()

    def test_copy_admin(self):
        self._copy_test_helper(admin=True)

    def test_copy_read_only(self):
        self._copy_test_helper(read_only=True)

    def test_credentials_getter(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_one_with_mocks(
            project=project, credentials=credentials)
        self.assertIs(client.credentials, credentials.with_scopes.return_value)

    def test_project_name_property(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_one_with_mocks(
            project=project, credentials=credentials)
        project_name = 'projects/' + project
        self.assertEqual(client.project_name, project_name)

    def test_instance_stub_getter(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_one_with_mocks(
            project=project, credentials=credentials, admin=True)
        self.assertIs(client._instance_stub, client._instance_stub_internal)

    def test_instance_stub_non_admin_failure(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_one_with_mocks(
            project=project, credentials=credentials, admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_instance_stub')

    def test_operations_stub_getter(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_one_with_mocks(
            project=project, credentials=credentials, admin=True)
        self.assertIs(client._operations_stub,
                      client._operations_stub_internal)

    def test_operations_stub_non_admin_failure(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_one_with_mocks(
            project=project, credentials=credentials, admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_operations_stub')

    def test_table_stub_getter(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_one_with_mocks(
            project=project, credentials=credentials, admin=True)
        self.assertIs(client._table_stub, client._table_stub_internal)

    def test_table_stub_non_admin_failure(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_one_with_mocks(
            project=project, credentials=credentials, admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_table_stub')

    def test_instance_factory_defaults(self):
        from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES
        from google.cloud.bigtable.instance import Instance
        from google.cloud.bigtable.instance import (
            _EXISTING_INSTANCE_LOCATION_ID)

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        DISPLAY_NAME = 'display-name'
        credentials = _make_credentials()
        client = self._make_one_with_mocks(
            project=PROJECT, credentials=credentials)

        instance = client.instance(INSTANCE_ID, display_name=DISPLAY_NAME)

        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.instance_id, INSTANCE_ID)
        self.assertEqual(instance.display_name, DISPLAY_NAME)
        self.assertEqual(instance._cluster_location_id,
                         _EXISTING_INSTANCE_LOCATION_ID)
        self.assertEqual(instance._cluster_serve_nodes, DEFAULT_SERVE_NODES)
        self.assertIs(instance._client, client)

    def test_instance_factory_w_explicit_serve_nodes(self):
        from google.cloud.bigtable.instance import Instance

        PROJECT = 'PROJECT'
        INSTANCE_ID = 'instance-id'
        DISPLAY_NAME = 'display-name'
        LOCATION_ID = 'locname'
        SERVE_NODES = 5
        credentials = _make_credentials()
        client = self._make_one_with_mocks(
            project=PROJECT, credentials=credentials)

        instance = client.instance(
            INSTANCE_ID, display_name=DISPLAY_NAME,
            location=LOCATION_ID, serve_nodes=SERVE_NODES)

        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.instance_id, INSTANCE_ID)
        self.assertEqual(instance.display_name, DISPLAY_NAME)
        self.assertEqual(instance._cluster_location_id, LOCATION_ID)
        self.assertEqual(instance._cluster_serve_nodes, SERVE_NODES)
        self.assertIs(instance._client, client)

    def test_list_instances(self):
        from google.cloud.bigtable._generated import (
            instance_pb2 as data_v2_pb2)
        from google.cloud.bigtable._generated import (
            bigtable_instance_admin_pb2 as messages_v2_pb2)
        from tests.unit._testing import _FakeStub

        LOCATION = 'projects/' + self.PROJECT + '/locations/locname'
        FAILED_LOCATION = 'FAILED'
        INSTANCE_ID1 = 'instance-id1'
        INSTANCE_ID2 = 'instance-id2'
        INSTANCE_NAME1 = (
            'projects/' + self.PROJECT + '/instances/' + INSTANCE_ID1)
        INSTANCE_NAME2 = (
            'projects/' + self.PROJECT + '/instances/' + INSTANCE_ID2)

        credentials = _make_credentials()
        client = self._make_one_with_mocks(
            project=self.PROJECT,
            credentials=credentials,
            admin=True,
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
            (request_pb,),
            {},
        )])


class _Client(object):

    def __init__(self, credentials, user_agent, emulator_host=None):
        self.credentials = credentials
        self.user_agent = user_agent
        self.emulator_host = emulator_host
