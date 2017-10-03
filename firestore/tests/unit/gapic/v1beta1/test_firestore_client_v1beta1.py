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

from google.cloud.firestore_v1beta1.gapic import firestore_client
from google.cloud.firestore_v1beta1.proto import common_pb2
from google.cloud.firestore_v1beta1.proto import document_pb2
from google.cloud.firestore_v1beta1.proto import firestore_pb2
from google.protobuf import empty_pb2


class CustomException(Exception):
    pass


class TestFirestoreClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_document(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        name = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                    '[ANY_PATH]')

        # Mock response
        name_2 = 'name2-1052831874'
        expected_response = {'name': name_2}
        expected_response = document_pb2.Document(**expected_response)
        grpc_stub.GetDocument.return_value = expected_response

        response = client.get_document(name)
        self.assertEqual(expected_response, response)

        grpc_stub.GetDocument.assert_called_once()
        args, kwargs = grpc_stub.GetDocument.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.GetDocumentRequest(name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_document_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        name = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                    '[ANY_PATH]')

        # Mock exception response
        grpc_stub.GetDocument.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_document, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_documents(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                      '[ANY_PATH]')
        collection_id = 'collectionId-821242276'

        # Mock response
        next_page_token = ''
        documents_element = {}
        documents = [documents_element]
        expected_response = {
            'next_page_token': next_page_token,
            'documents': documents
        }
        expected_response = firestore_pb2.ListDocumentsResponse(
            **expected_response)
        grpc_stub.ListDocuments.return_value = expected_response

        paged_list_response = client.list_documents(parent, collection_id)
        resources = list(paged_list_response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response.documents[0], resources[0])

        grpc_stub.ListDocuments.assert_called_once()
        args, kwargs = grpc_stub.ListDocuments.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.ListDocumentsRequest(
            parent=parent, collection_id=collection_id)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_documents_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                      '[ANY_PATH]')
        collection_id = 'collectionId-821242276'

        # Mock exception response
        grpc_stub.ListDocuments.side_effect = CustomException()

        paged_list_response = client.list_documents(parent, collection_id)
        self.assertRaises(errors.GaxError, list, paged_list_response)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_document(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                      '[ANY_PATH]')
        collection_id = 'collectionId-821242276'
        document_id = 'documentId506676927'
        document = {}

        # Mock response
        name = 'name3373707'
        expected_response = {'name': name}
        expected_response = document_pb2.Document(**expected_response)
        grpc_stub.CreateDocument.return_value = expected_response

        response = client.create_document(parent, collection_id, document_id,
                                          document)
        self.assertEqual(expected_response, response)

        grpc_stub.CreateDocument.assert_called_once()
        args, kwargs = grpc_stub.CreateDocument.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.CreateDocumentRequest(
            parent=parent,
            collection_id=collection_id,
            document_id=document_id,
            document=document)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_create_document_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                      '[ANY_PATH]')
        collection_id = 'collectionId-821242276'
        document_id = 'documentId506676927'
        document = {}

        # Mock exception response
        grpc_stub.CreateDocument.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.create_document, parent,
                          collection_id, document_id, document)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_update_document(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        document = {}
        update_mask = {}

        # Mock response
        name = 'name3373707'
        expected_response = {'name': name}
        expected_response = document_pb2.Document(**expected_response)
        grpc_stub.UpdateDocument.return_value = expected_response

        response = client.update_document(document, update_mask)
        self.assertEqual(expected_response, response)

        grpc_stub.UpdateDocument.assert_called_once()
        args, kwargs = grpc_stub.UpdateDocument.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.UpdateDocumentRequest(
            document=document, update_mask=update_mask)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_update_document_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        document = {}
        update_mask = {}

        # Mock exception response
        grpc_stub.UpdateDocument.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.update_document, document,
                          update_mask)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_delete_document(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        name = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                    '[ANY_PATH]')

        client.delete_document(name)

        grpc_stub.DeleteDocument.assert_called_once()
        args, kwargs = grpc_stub.DeleteDocument.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.DeleteDocumentRequest(name=name)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_delete_document_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        name = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                    '[ANY_PATH]')

        # Mock exception response
        grpc_stub.DeleteDocument.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.delete_document, name)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_batch_get_documents(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        documents = []

        # Mock response
        missing = 'missing1069449574'
        transaction = b'-34'
        expected_response = {'missing': missing, 'transaction': transaction}
        expected_response = firestore_pb2.BatchGetDocumentsResponse(
            **expected_response)
        grpc_stub.BatchGetDocuments.return_value = iter([expected_response])

        response = client.batch_get_documents(database, documents)
        resources = list(response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response, resources[0])

        grpc_stub.BatchGetDocuments.assert_called_once()
        args, kwargs = grpc_stub.BatchGetDocuments.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.BatchGetDocumentsRequest(
            database=database, documents=documents)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_batch_get_documents_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        documents = []

        # Mock exception response
        grpc_stub.BatchGetDocuments.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.batch_get_documents,
                          database, documents)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_begin_transaction(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')

        # Mock response
        transaction = b'-34'
        expected_response = {'transaction': transaction}
        expected_response = firestore_pb2.BeginTransactionResponse(
            **expected_response)
        grpc_stub.BeginTransaction.return_value = expected_response

        response = client.begin_transaction(database)
        self.assertEqual(expected_response, response)

        grpc_stub.BeginTransaction.assert_called_once()
        args, kwargs = grpc_stub.BeginTransaction.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.BeginTransactionRequest(
            database=database)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_begin_transaction_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')

        # Mock exception response
        grpc_stub.BeginTransaction.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.begin_transaction, database)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_commit(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        writes = []

        # Mock response
        expected_response = {}
        expected_response = firestore_pb2.CommitResponse(**expected_response)
        grpc_stub.Commit.return_value = expected_response

        response = client.commit(database, writes)
        self.assertEqual(expected_response, response)

        grpc_stub.Commit.assert_called_once()
        args, kwargs = grpc_stub.Commit.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.CommitRequest(
            database=database, writes=writes)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_commit_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        writes = []

        # Mock exception response
        grpc_stub.Commit.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.commit, database, writes)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_rollback(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        transaction = b'-34'

        client.rollback(database, transaction)

        grpc_stub.Rollback.assert_called_once()
        args, kwargs = grpc_stub.Rollback.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.RollbackRequest(
            database=database, transaction=transaction)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_rollback_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        transaction = b'-34'

        # Mock exception response
        grpc_stub.Rollback.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.rollback, database,
                          transaction)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_run_query(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                      '[ANY_PATH]')

        # Mock response
        transaction = b'-34'
        skipped_results = 880286183
        expected_response = {
            'transaction': transaction,
            'skipped_results': skipped_results
        }
        expected_response = firestore_pb2.RunQueryResponse(**expected_response)
        grpc_stub.RunQuery.return_value = iter([expected_response])

        response = client.run_query(parent)
        resources = list(response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response, resources[0])

        grpc_stub.RunQuery.assert_called_once()
        args, kwargs = grpc_stub.RunQuery.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.RunQueryRequest(parent=parent)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_run_query_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                      '[ANY_PATH]')

        # Mock exception response
        grpc_stub.RunQuery.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.run_query, parent)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_write(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        request = {'database': database}
        requests = [request]

        # Mock response
        stream_id = 'streamId-315624902'
        stream_token = b'122'
        expected_response = {
            'stream_id': stream_id,
            'stream_token': stream_token
        }
        expected_response = firestore_pb2.WriteResponse(**expected_response)
        grpc_stub.Write.return_value = iter([expected_response])

        response = client.write(requests)
        resources = list(response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response, resources[0])

        grpc_stub.Write.assert_called_once()
        args, kwargs = grpc_stub.Write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_requests = args[0]
        self.assertEqual(1, len(actual_requests))
        actual_request = list(actual_requests)[0]
        self.assertEqual(request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_write_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        request = {'database': database}
        requests = [request]

        # Mock exception response
        grpc_stub.Write.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.write, requests)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_listen(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        request = {'database': database}
        requests = [request]

        # Mock response
        expected_response = {}
        expected_response = firestore_pb2.ListenResponse(**expected_response)
        grpc_stub.Listen.return_value = iter([expected_response])

        response = client.listen(requests)
        resources = list(response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response, resources[0])

        grpc_stub.Listen.assert_called_once()
        args, kwargs = grpc_stub.Listen.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_requests = args[0]
        self.assertEqual(1, len(actual_requests))
        actual_request = list(actual_requests)[0]
        self.assertEqual(request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_listen_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        database = client.database_root_path('[PROJECT]', '[DATABASE]')
        request = {'database': database}
        requests = [request]

        # Mock exception response
        grpc_stub.Listen.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.listen, requests)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_collection_ids(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                      '[ANY_PATH]')

        # Mock response
        next_page_token = ''
        collection_ids_element = 'collectionIdsElement1368994900'
        collection_ids = [collection_ids_element]
        expected_response = {
            'next_page_token': next_page_token,
            'collection_ids': collection_ids
        }
        expected_response = firestore_pb2.ListCollectionIdsResponse(
            **expected_response)
        grpc_stub.ListCollectionIds.return_value = expected_response

        paged_list_response = client.list_collection_ids(parent)
        resources = list(paged_list_response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response.collection_ids[0], resources[0])

        grpc_stub.ListCollectionIds.assert_called_once()
        args, kwargs = grpc_stub.ListCollectionIds.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = firestore_pb2.ListCollectionIdsRequest(
            parent=parent)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_collection_ids_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = firestore_client.FirestoreClient()

        # Mock request
        parent = client.any_path_path('[PROJECT]', '[DATABASE]', '[DOCUMENT]',
                                      '[ANY_PATH]')

        # Mock exception response
        grpc_stub.ListCollectionIds.side_effect = CustomException()

        paged_list_response = client.list_collection_ids(parent)
        self.assertRaises(errors.GaxError, list, paged_list_response)
