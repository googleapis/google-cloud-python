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

    def _make_oneWithMocks(self, *args, **kwargs):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import client as MUT

        mock_make_data_stub = _MakeStubMock()
        mock_make_instance_stub = _MakeStubMock()
        mock_make_operations_stub = _MakeStubMock()
        mock_make_table_stub = _MakeStubMock()
        with _Monkey(MUT, _make_data_stub=mock_make_data_stub,
                     _make_instance_stub=mock_make_instance_stub,
                     _make_operations_stub=mock_make_operations_stub,
                     _make_table_stub=mock_make_table_stub):
            return self._make_one(*args, **kwargs)

    def _constructor_test_helper(self, expected_scopes, creds,
                                 read_only=False, admin=False,
                                 user_agent=None, expected_creds=None):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import client as MUT

        user_agent = user_agent or MUT.DEFAULT_USER_AGENT

        mock_make_data_stub = _MakeStubMock()
        mock_make_instance_stub = _MakeStubMock()
        mock_make_operations_stub = _MakeStubMock()
        mock_make_table_stub = _MakeStubMock()
        with _Monkey(MUT, _make_data_stub=mock_make_data_stub,
                     _make_instance_stub=mock_make_instance_stub,
                     _make_operations_stub=mock_make_operations_stub,
                     _make_table_stub=mock_make_table_stub):
            client = self._make_one(project=self.PROJECT, credentials=creds,
                                    read_only=read_only, admin=admin,
                                    user_agent=user_agent)

        # Verify the mocks.
        self.assertEqual(mock_make_data_stub.calls, [client])
        if admin:
            self.assertSequenceEqual(mock_make_instance_stub.calls, [client])
            self.assertSequenceEqual(mock_make_operations_stub.calls, [client])
            self.assertSequenceEqual(mock_make_table_stub.calls, [client])
        else:
            self.assertSequenceEqual(mock_make_instance_stub.calls, [])
            self.assertSequenceEqual(mock_make_operations_stub.calls, [])
            self.assertSequenceEqual(mock_make_table_stub.calls, [])

        expected_creds = expected_creds or creds.with_scopes.return_value
        self.assertIs(client._credentials, expected_creds)

        if expected_scopes is not None:
            creds.with_scopes.assert_called_once_with(expected_scopes)

        self.assertEqual(client.project, self.PROJECT)
        self.assertEqual(client.user_agent, user_agent)
        # Check gRPC stubs (or mocks of them) are set
        self.assertIs(client._data_stub, mock_make_data_stub.result)
        if admin:
            self.assertIs(client._instance_stub_internal,
                          mock_make_instance_stub.result)
            self.assertIs(client._operations_stub_internal,
                          mock_make_operations_stub.result)
            self.assertIs(client._table_stub_internal,
                          mock_make_table_stub.result)
        else:
            self.assertIsNone(client._instance_stub_internal)
            self.assertIsNone(client._operations_stub_internal)
            self.assertIsNone(client._table_stub_internal)

    def test_constructor_default_scopes(self):
        from google.cloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE]
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_user_agent(self):
        from google.cloud.bigtable import client as MUT

        CUSTOM_USER_AGENT = 'custom-application'
        expected_scopes = [MUT.DATA_SCOPE]
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds,
                                      user_agent=CUSTOM_USER_AGENT)

    def test_constructor_with_admin(self):
        from google.cloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE, MUT.ADMIN_SCOPE]
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds, admin=True)

    def test_constructor_with_read_only(self):
        from google.cloud.bigtable import client as MUT

        expected_scopes = [MUT.READ_ONLY_SCOPE]
        creds = _make_credentials()
        self._constructor_test_helper(expected_scopes, creds, read_only=True)

    def test_constructor_both_admin_and_read_only(self):
        creds = _make_credentials()
        with self.assertRaises(ValueError):
            self._constructor_test_helper([], creds, admin=True,
                                          read_only=True)

    def test_constructor_implicit_credentials(self):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import client as MUT

        creds = _make_credentials()
        expected_scopes = [MUT.DATA_SCOPE]

        def mock_get_credentials():
            return creds

        with _Monkey(MUT, get_credentials=mock_get_credentials):
            self._constructor_test_helper(
                None, None,
                expected_creds=creds.with_scopes.return_value)

        creds.with_scopes.assert_called_once_with(expected_scopes)

    def test_constructor_credentials_wo_create_scoped(self):
        creds = _make_credentials()
        expected_scopes = None
        self._constructor_test_helper(expected_scopes, creds)

    def _copy_test_helper(self, read_only=False, admin=False):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import client as MUT

        credentials = _make_credentials()
        client = self._make_oneWithMocks(
            project=self.PROJECT,
            credentials=credentials,
            read_only=read_only,
            admin=admin,
            user_agent=self.USER_AGENT)
        # Put some fake stubs in place so that we can verify they don't
        # get copied. In the admin=False case, only the data stub will
        # not be None, so we over-ride all the internal values.
        client._data_stub = object()
        client._instance_stub_internal = object()
        client._operations_stub_internal = object()
        client._table_stub_internal = object()

        mock_make_data_stub = _MakeStubMock()
        mock_make_instance_stub = _MakeStubMock()
        mock_make_operations_stub = _MakeStubMock()
        mock_make_table_stub = _MakeStubMock()
        with _Monkey(MUT, _make_data_stub=mock_make_data_stub,
                     _make_instance_stub=mock_make_instance_stub,
                     _make_operations_stub=mock_make_operations_stub,
                     _make_table_stub=mock_make_table_stub):
            new_client = client.copy()
        self.assertEqual(new_client._admin, client._admin)
        self.assertEqual(new_client._credentials, client._credentials)
        self.assertEqual(new_client.project, client.project)
        self.assertEqual(new_client.user_agent, client.user_agent)
        # Make sure stubs are not preserved.
        self.assertNotEqual(new_client._data_stub, client._data_stub)
        self.assertNotEqual(new_client._instance_stub_internal,
                            client._instance_stub_internal)
        self.assertNotEqual(new_client._operations_stub_internal,
                            client._operations_stub_internal)
        self.assertNotEqual(new_client._table_stub_internal,
                            client._table_stub_internal)

    def test_copy(self):
        self._copy_test_helper()

    def test_copy_admin(self):
        self._copy_test_helper(admin=True)

    def test_copy_read_only(self):
        self._copy_test_helper(read_only=True)

    def test_credentials_getter(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_oneWithMocks(project=project,
                                         credentials=credentials)
        self.assertIs(client.credentials, credentials.with_scopes.return_value)

    def test_project_name_property(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_oneWithMocks(project=project,
                                         credentials=credentials)
        project_name = 'projects/' + project
        self.assertEqual(client.project_name, project_name)

    def test_instance_stub_getter(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_oneWithMocks(project=project,
                                         credentials=credentials, admin=True)
        self.assertIs(client._instance_stub, client._instance_stub_internal)

    def test_instance_stub_non_admin_failure(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_oneWithMocks(project=project,
                                         credentials=credentials, admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_instance_stub')

    def test_operations_stub_getter(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_oneWithMocks(project=project,
                                         credentials=credentials, admin=True)
        self.assertIs(client._operations_stub,
                      client._operations_stub_internal)

    def test_operations_stub_non_admin_failure(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_oneWithMocks(project=project,
                                         credentials=credentials, admin=False)
        with self.assertRaises(ValueError):
            getattr(client, '_operations_stub')

    def test_table_stub_getter(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_oneWithMocks(project=project,
                                         credentials=credentials, admin=True)
        self.assertIs(client._table_stub, client._table_stub_internal)

    def test_table_stub_non_admin_failure(self):
        credentials = _make_credentials()
        project = 'PROJECT'
        client = self._make_oneWithMocks(project=project,
                                         credentials=credentials, admin=False)
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
        client = self._make_oneWithMocks(project=PROJECT,
                                         credentials=credentials)

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
        client = self._make_oneWithMocks(project=PROJECT,
                                         credentials=credentials)

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
        client = self._make_oneWithMocks(
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


class _MakeStubMock(object):

    def __init__(self):
        self.result = object()
        self.calls = []

    def __call__(self, client):
        self.calls.append(client)
        return self.result
