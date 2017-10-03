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

from google.cloud.firestore_v1beta1.gapic import firestore_admin_client
from google.cloud.firestore_v1beta1.proto.admin import firestore_admin_pb2
from google.cloud.firestore_v1beta1.proto.admin import index_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2


class CustomException(Exception):
    pass


class TestFirestoreAdminClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_index(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_admin_client.FirestoreAdminClient()

        # Mock request
        parent = client.database_path('[PROJECT]', '[DATABASE]')
        index = {}

        # Mock response
        name = 'name3373707'
        done = True
        expected_response = {'name': name, 'done': done}
        expected_response = operations_pb2.Operation(**expected_response)
        grpc_stub.CreateIndex.return_value = expected_response

        response = client.create_index(parent, index)
        self.assertEqual(expected_response, response)

        grpc_stub.CreateIndex.assert_called_once()
        args, kwargs = grpc_stub.CreateIndex.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_admin_pb2.CreateIndexRequest(
            parent=parent, index=index)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_index_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_admin_client.FirestoreAdminClient()

        # Mock request
        parent = client.database_path('[PROJECT]', '[DATABASE]')
        index = {}

        # Mock exception response
        grpc_stub.CreateIndex.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.create_index, parent, index)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_indexes(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_admin_client.FirestoreAdminClient()

        # Mock request
        parent = client.database_path('[PROJECT]', '[DATABASE]')

        # Mock response
        next_page_token = ''
        indexes_element = {}
        indexes = [indexes_element]
        expected_response = {
            'next_page_token': next_page_token,
            'indexes': indexes
        }
        expected_response = firestore_admin_pb2.ListIndexesResponse(
            **expected_response)
        grpc_stub.ListIndexes.return_value = expected_response

        paged_list_response = client.list_indexes(parent)
        resources = list(paged_list_response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response.indexes[0], resources[0])

        grpc_stub.ListIndexes.assert_called_once()
        args, kwargs = grpc_stub.ListIndexes.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_admin_pb2.ListIndexesRequest(
            parent=parent)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_indexes_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_admin_client.FirestoreAdminClient()

        # Mock request
        parent = client.database_path('[PROJECT]', '[DATABASE]')

        # Mock exception response
        grpc_stub.ListIndexes.side_effect = CustomException()

        paged_list_response = client.list_indexes(parent)
        self.assertRaises(errors.GaxError, list, paged_list_response)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_index(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_admin_client.FirestoreAdminClient()

        # Mock request
        name = client.index_path('[PROJECT]', '[DATABASE]', '[INDEX]')

        # Mock response
        name_2 = 'name2-1052831874'
        collection_id = 'collectionId-821242276'
        expected_response = {'name': name_2, 'collection_id': collection_id}
        expected_response = index_pb2.Index(**expected_response)
        grpc_stub.GetIndex.return_value = expected_response

        response = client.get_index(name)
        self.assertEqual(expected_response, response)

        grpc_stub.GetIndex.assert_called_once()
        args, kwargs = grpc_stub.GetIndex.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_admin_pb2.GetIndexRequest(name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_index_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_admin_client.FirestoreAdminClient()

        # Mock request
        name = client.index_path('[PROJECT]', '[DATABASE]', '[INDEX]')

        # Mock exception response
        grpc_stub.GetIndex.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_index, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_delete_index(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_admin_client.FirestoreAdminClient()

        # Mock request
        name = client.index_path('[PROJECT]', '[DATABASE]', '[INDEX]')

        client.delete_index(name)

        grpc_stub.DeleteIndex.assert_called_once()
        args, kwargs = grpc_stub.DeleteIndex.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_admin_pb2.DeleteIndexRequest(name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_delete_index_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_admin_client.FirestoreAdminClient()

        # Mock request
        name = client.index_path('[PROJECT]', '[DATABASE]', '[INDEX]')

        # Mock exception response
        grpc_stub.DeleteIndex.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.delete_index, name)
