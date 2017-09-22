# Copyright 2017, Google Inc. All rights reserved.
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
"""Unit tests."""

import mock
import unittest

from google.gax import errors
from google.rpc import status_pb2

from google.cloud import spanner_admin_database_v1
from google.cloud.spanner_admin_database_v1.proto import spanner_database_admin_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2


class CustomException(Exception):
    pass


class TestDatabaseAdminClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_databases(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        parent = client.instance_path('[PROJECT]', '[INSTANCE]')

        # Mock response
        next_page_token = ''
        databases_element = {}
        databases = [databases_element]
        expected_response = {
            'next_page_token': next_page_token,
            'databases': databases
        }
        expected_response = spanner_database_admin_pb2.ListDatabasesResponse(
            **expected_response)
        grpc_stub.ListDatabases.return_value = expected_response

        paged_list_response = client.list_databases(parent)
        resources = list(paged_list_response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response.databases[0], resources[0])

        grpc_stub.ListDatabases.assert_called_once()
        args, kwargs = grpc_stub.ListDatabases.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_database_admin_pb2.ListDatabasesRequest(
            parent=parent)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_databases_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        parent = client.instance_path('[PROJECT]', '[INSTANCE]')

        # Mock exception response
        grpc_stub.ListDatabases.side_effect = CustomException()

        paged_list_response = client.list_databases(parent)
        self.assertRaises(errors.GaxError, list, paged_list_response)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_database(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        parent = client.instance_path('[PROJECT]', '[INSTANCE]')
        create_statement = 'createStatement552974828'

        # Mock response
        name = 'name3373707'
        expected_response = {'name': name}
        expected_response = spanner_database_admin_pb2.Database(
            **expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_create_database', done=True)
        operation.response.Pack(expected_response)
        grpc_stub.CreateDatabase.return_value = operation

        response = client.create_database(parent, create_statement)
        self.assertEqual(expected_response, response.result())

        grpc_stub.CreateDatabase.assert_called_once()
        args, kwargs = grpc_stub.CreateDatabase.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_database_admin_pb2.CreateDatabaseRequest(
            parent=parent, create_statement=create_statement)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_database_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        parent = client.instance_path('[PROJECT]', '[INSTANCE]')
        create_statement = 'createStatement552974828'

        # Mock exception response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_create_database_exception', done=True)
        operation.error.CopyFrom(error)
        grpc_stub.CreateDatabase.return_value = operation

        response = client.create_database(parent, create_statement)
        self.assertEqual(error, response.exception())

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_database(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        name = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')

        # Mock response
        name_2 = 'name2-1052831874'
        expected_response = {'name': name_2}
        expected_response = spanner_database_admin_pb2.Database(
            **expected_response)
        grpc_stub.GetDatabase.return_value = expected_response

        response = client.get_database(name)
        self.assertEqual(expected_response, response)

        grpc_stub.GetDatabase.assert_called_once()
        args, kwargs = grpc_stub.GetDatabase.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_database_admin_pb2.GetDatabaseRequest(
            name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_database_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        name = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')

        # Mock exception response
        grpc_stub.GetDatabase.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_database, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_update_database_ddl(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        database = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')
        statements = []

        # Mock response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_update_database_ddl', done=True)
        operation.response.Pack(expected_response)
        grpc_stub.UpdateDatabaseDdl.return_value = operation

        response = client.update_database_ddl(database, statements)
        self.assertEqual(expected_response, response.result())

        grpc_stub.UpdateDatabaseDdl.assert_called_once()
        args, kwargs = grpc_stub.UpdateDatabaseDdl.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_database_admin_pb2.UpdateDatabaseDdlRequest(
            database=database, statements=statements)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_update_database_ddl_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        database = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')
        statements = []

        # Mock exception response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_update_database_ddl_exception', done=True)
        operation.error.CopyFrom(error)
        grpc_stub.UpdateDatabaseDdl.return_value = operation

        response = client.update_database_ddl(database, statements)
        self.assertEqual(error, response.exception())

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_drop_database(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        database = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')

        client.drop_database(database)

        grpc_stub.DropDatabase.assert_called_once()
        args, kwargs = grpc_stub.DropDatabase.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_database_admin_pb2.DropDatabaseRequest(
            database=database)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_drop_database_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        database = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')

        # Mock exception response
        grpc_stub.DropDatabase.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.drop_database, database)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_database_ddl(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        database = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')

        # Mock response
        expected_response = {}
        expected_response = spanner_database_admin_pb2.GetDatabaseDdlResponse(
            **expected_response)
        grpc_stub.GetDatabaseDdl.return_value = expected_response

        response = client.get_database_ddl(database)
        self.assertEqual(expected_response, response)

        grpc_stub.GetDatabaseDdl.assert_called_once()
        args, kwargs = grpc_stub.GetDatabaseDdl.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = spanner_database_admin_pb2.GetDatabaseDdlRequest(
            database=database)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_database_ddl_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        database = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')

        # Mock exception response
        grpc_stub.GetDatabaseDdl.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_database_ddl, database)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_set_iam_policy(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        resource = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')
        policy = {}

        # Mock response
        version = 351608024
        etag = b'21'
        expected_response = {'version': version, 'etag': etag}
        expected_response = policy_pb2.Policy(**expected_response)
        grpc_stub.SetIamPolicy.return_value = expected_response

        response = client.set_iam_policy(resource, policy)
        self.assertEqual(expected_response, response)

        grpc_stub.SetIamPolicy.assert_called_once()
        args, kwargs = grpc_stub.SetIamPolicy.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_set_iam_policy_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        resource = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')
        policy = {}

        # Mock exception response
        grpc_stub.SetIamPolicy.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.set_iam_policy, resource,
                          policy)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_iam_policy(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        resource = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')

        # Mock response
        version = 351608024
        etag = b'21'
        expected_response = {'version': version, 'etag': etag}
        expected_response = policy_pb2.Policy(**expected_response)
        grpc_stub.GetIamPolicy.return_value = expected_response

        response = client.get_iam_policy(resource)
        self.assertEqual(expected_response, response)

        grpc_stub.GetIamPolicy.assert_called_once()
        args, kwargs = grpc_stub.GetIamPolicy.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_iam_policy_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        resource = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')

        # Mock exception response
        grpc_stub.GetIamPolicy.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_iam_policy, resource)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_test_iam_permissions(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        resource = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')
        permissions = []

        # Mock response
        expected_response = {}
        expected_response = iam_policy_pb2.TestIamPermissionsResponse(
            **expected_response)
        grpc_stub.TestIamPermissions.return_value = expected_response

        response = client.test_iam_permissions(resource, permissions)
        self.assertEqual(expected_response, response)

        grpc_stub.TestIamPermissions.assert_called_once()
        args, kwargs = grpc_stub.TestIamPermissions.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_test_iam_permissions_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = spanner_admin_database_v1.DatabaseAdminClient()

        # Mock request
        resource = client.database_path('[PROJECT]', '[INSTANCE]',
                                        '[DATABASE]')
        permissions = []

        # Mock exception response
        grpc_stub.TestIamPermissions.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.test_iam_permissions,
                          resource, permissions)
