# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.rpc import status_pb2

import dialogflow_v2beta1
from dialogflow_v2beta1.proto import document_pb2
from google.longrunning import operations_pb2
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


class CustomException(Exception):
    pass


class TestDocumentsClient(object):
    def test_list_documents(self):
        # Setup Expected Response
        next_page_token = ""
        documents_element = {}
        documents = [documents_element]
        expected_response = {"next_page_token": next_page_token, "documents": documents}
        expected_response = document_pb2.ListDocumentsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup Request
        parent = client.knowledge_base_path("[PROJECT]", "[KNOWLEDGE_BASE]")

        paged_list_response = client.list_documents(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.documents[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = document_pb2.ListDocumentsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_documents_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup request
        parent = client.knowledge_base_path("[PROJECT]", "[KNOWLEDGE_BASE]")

        paged_list_response = client.list_documents(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_document(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        mime_type = "mimeType-196041627"
        content_uri = "contentUri-388807514"
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "mime_type": mime_type,
            "content_uri": content_uri,
        }
        expected_response = document_pb2.Document(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup Request
        name = client.document_path("[PROJECT]", "[KNOWLEDGE_BASE]", "[DOCUMENT]")

        response = client.get_document(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = document_pb2.GetDocumentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_document_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup request
        name = client.document_path("[PROJECT]", "[KNOWLEDGE_BASE]", "[DOCUMENT]")

        with pytest.raises(CustomException):
            client.get_document(name)

    def test_create_document(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        mime_type = "mimeType-196041627"
        content_uri = "contentUri-388807514"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "mime_type": mime_type,
            "content_uri": content_uri,
        }
        expected_response = document_pb2.Document(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_document", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup Request
        parent = client.knowledge_base_path("[PROJECT]", "[KNOWLEDGE_BASE]")
        document = {}

        response = client.create_document(parent, document)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = document_pb2.CreateDocumentRequest(
            parent=parent, document=document
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_document_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_document_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup Request
        parent = client.knowledge_base_path("[PROJECT]", "[KNOWLEDGE_BASE]")
        document = {}

        response = client.create_document(parent, document)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_delete_document(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_delete_document", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup Request
        name = client.document_path("[PROJECT]", "[KNOWLEDGE_BASE]", "[DOCUMENT]")

        response = client.delete_document(name)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = document_pb2.DeleteDocumentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_document_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_delete_document_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup Request
        name = client.document_path("[PROJECT]", "[KNOWLEDGE_BASE]", "[DOCUMENT]")

        response = client.delete_document(name)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_update_document(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        mime_type = "mimeType-196041627"
        content_uri = "contentUri-388807514"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "mime_type": mime_type,
            "content_uri": content_uri,
        }
        expected_response = document_pb2.Document(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_update_document", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup Request
        document = {}

        response = client.update_document(document)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = document_pb2.UpdateDocumentRequest(document=document)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_document_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_update_document_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        # Setup Request
        document = {}

        response = client.update_document(document)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_reload_document(self):
        # Setup Expected Response
        name = "name3373707"
        done = True
        expected_response = {"name": name, "done": done}
        expected_response = operations_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        response = client.reload_document()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = document_pb2.ReloadDocumentRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_reload_document_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.DocumentsClient()

        with pytest.raises(CustomException):
            client.reload_document()
