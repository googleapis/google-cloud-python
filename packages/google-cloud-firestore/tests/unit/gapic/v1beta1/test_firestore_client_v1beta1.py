# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests."""

import mock
import pytest

from google.cloud.firestore_v1beta1.gapic import firestore_client
from google.cloud.firestore_v1beta1.proto import common_pb2
from google.cloud.firestore_v1beta1.proto import document_pb2
from google.cloud.firestore_v1beta1.proto import firestore_pb2
from google.protobuf import empty_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)

    def unary_stream(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)

    def stream_stream(
        self, method, request_serializer=None, response_deserializer=None
    ):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestFirestoreClient(object):
    def test_get_document(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = document_pb2.Document(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        name = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )

        response = client.get_document(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.GetDocumentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_document_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        name = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )

        with pytest.raises(CustomException):
            client.get_document(name)

    def test_list_documents(self):
        # Setup Expected Response
        next_page_token = ""
        documents_element = {}
        documents = [documents_element]
        expected_response = {"next_page_token": next_page_token, "documents": documents}
        expected_response = firestore_pb2.ListDocumentsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        parent = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )
        collection_id = "collectionId-821242276"

        paged_list_response = client.list_documents(parent, collection_id)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.documents[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.ListDocumentsRequest(
            parent=parent, collection_id=collection_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_documents_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        parent = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )
        collection_id = "collectionId-821242276"

        paged_list_response = client.list_documents(parent, collection_id)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_document(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = document_pb2.Document(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        parent = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )
        collection_id = "collectionId-821242276"
        document_id = "documentId506676927"
        document = {}

        response = client.create_document(parent, collection_id, document_id, document)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.CreateDocumentRequest(
            parent=parent,
            collection_id=collection_id,
            document_id=document_id,
            document=document,
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_document_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        parent = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )
        collection_id = "collectionId-821242276"
        document_id = "documentId506676927"
        document = {}

        with pytest.raises(CustomException):
            client.create_document(parent, collection_id, document_id, document)

    def test_update_document(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = document_pb2.Document(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        document = {}
        update_mask = {}

        response = client.update_document(document, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.UpdateDocumentRequest(
            document=document, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_document_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        document = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_document(document, update_mask)

    def test_delete_document(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        name = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )

        client.delete_document(name)

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.DeleteDocumentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_document_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        name = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )

        with pytest.raises(CustomException):
            client.delete_document(name)

    def test_batch_get_documents(self):
        # Setup Expected Response
        missing = "missing1069449574"
        transaction = b"-34"
        expected_response = {"missing": missing, "transaction": transaction}
        expected_response = firestore_pb2.BatchGetDocumentsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        documents = []

        response = client.batch_get_documents(database, documents)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.BatchGetDocumentsRequest(
            database=database, documents=documents
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_get_documents_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        documents = []

        with pytest.raises(CustomException):
            client.batch_get_documents(database, documents)

    def test_begin_transaction(self):
        # Setup Expected Response
        transaction = b"-34"
        expected_response = {"transaction": transaction}
        expected_response = firestore_pb2.BeginTransactionResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")

        response = client.begin_transaction(database)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.BeginTransactionRequest(database=database)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_begin_transaction_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.begin_transaction(database)

    def test_commit(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = firestore_pb2.CommitResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        writes = []

        response = client.commit(database, writes)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.CommitRequest(database=database, writes=writes)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_commit_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        writes = []

        with pytest.raises(CustomException):
            client.commit(database, writes)

    def test_rollback(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        transaction = b"-34"

        client.rollback(database, transaction)

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.RollbackRequest(
            database=database, transaction=transaction
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_rollback_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        transaction = b"-34"

        with pytest.raises(CustomException):
            client.rollback(database, transaction)

    def test_run_query(self):
        # Setup Expected Response
        transaction = b"-34"
        skipped_results = 880286183
        expected_response = {
            "transaction": transaction,
            "skipped_results": skipped_results,
        }
        expected_response = firestore_pb2.RunQueryResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        parent = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )

        response = client.run_query(parent)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.RunQueryRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_run_query_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        parent = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )

        with pytest.raises(CustomException):
            client.run_query(parent)

    def test_write(self):
        # Setup Expected Response
        stream_id = "streamId-315624902"
        stream_token = b"122"
        expected_response = {"stream_id": stream_id, "stream_token": stream_token}
        expected_response = firestore_pb2.WriteResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        request = {"database": database}
        request = firestore_pb2.WriteRequest(**request)
        requests = [request]

        response = client.write(requests)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        actual_requests = channel.requests[0][1]
        assert len(actual_requests) == 1
        actual_request = list(actual_requests)[0]
        assert request == actual_request

    def test_write_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        request = {"database": database}

        request = firestore_pb2.WriteRequest(**request)
        requests = [request]

        with pytest.raises(CustomException):
            client.write(requests)

    def test_listen(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = firestore_pb2.ListenResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        request = {"database": database}
        request = firestore_pb2.ListenRequest(**request)
        requests = [request]

        response = client.listen(requests)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        actual_requests = channel.requests[0][1]
        assert len(actual_requests) == 1
        actual_request = list(actual_requests)[0]
        assert request == actual_request

    def test_listen_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        database = client.database_root_path("[PROJECT]", "[DATABASE]")
        request = {"database": database}

        request = firestore_pb2.ListenRequest(**request)
        requests = [request]

        with pytest.raises(CustomException):
            client.listen(requests)

    def test_list_collection_ids(self):
        # Setup Expected Response
        next_page_token = ""
        collection_ids_element = "collectionIdsElement1368994900"
        collection_ids = [collection_ids_element]
        expected_response = {
            "next_page_token": next_page_token,
            "collection_ids": collection_ids,
        }
        expected_response = firestore_pb2.ListCollectionIdsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup Request
        parent = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )

        paged_list_response = client.list_collection_ids(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.collection_ids[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = firestore_pb2.ListCollectionIdsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_collection_ids_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_client.FirestoreClient()

        # Setup request
        parent = client.any_path_path(
            "[PROJECT]", "[DATABASE]", "[DOCUMENT]", "[ANY_PATH]"
        )

        paged_list_response = client.list_collection_ids(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)
