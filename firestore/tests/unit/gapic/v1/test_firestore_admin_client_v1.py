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

from google.cloud import firestore_admin_v1
from google.cloud.firestore_admin_v1.proto import field_pb2
from google.cloud.firestore_admin_v1.proto import firestore_admin_pb2
from google.cloud.firestore_admin_v1.proto import index_pb2
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


class TestFirestoreAdminClient(object):
    def test_create_index(self):
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
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        parent = client.parent_path("[PROJECT]", "[DATABASE]", "[COLLECTION_ID]")
        index = {}

        response = client.create_index(parent, index)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.CreateIndexRequest(
            parent=parent, index=index
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_index_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        parent = client.parent_path("[PROJECT]", "[DATABASE]", "[COLLECTION_ID]")
        index = {}

        with pytest.raises(CustomException):
            client.create_index(parent, index)

    def test_list_indexes(self):
        # Setup Expected Response
        next_page_token = ""
        indexes_element = {}
        indexes = [indexes_element]
        expected_response = {"next_page_token": next_page_token, "indexes": indexes}
        expected_response = firestore_admin_pb2.ListIndexesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        parent = client.parent_path("[PROJECT]", "[DATABASE]", "[COLLECTION_ID]")

        paged_list_response = client.list_indexes(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.indexes[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.ListIndexesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_indexes_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        parent = client.parent_path("[PROJECT]", "[DATABASE]", "[COLLECTION_ID]")

        paged_list_response = client.list_indexes(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_index(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = index_pb2.Index(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        name = client.index_path(
            "[PROJECT]", "[DATABASE]", "[COLLECTION_ID]", "[INDEX_ID]"
        )

        response = client.get_index(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.GetIndexRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_index_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        name = client.index_path(
            "[PROJECT]", "[DATABASE]", "[COLLECTION_ID]", "[INDEX_ID]"
        )

        with pytest.raises(CustomException):
            client.get_index(name)

    def test_delete_index(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        name = client.index_path(
            "[PROJECT]", "[DATABASE]", "[COLLECTION_ID]", "[INDEX_ID]"
        )

        client.delete_index(name)

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.DeleteIndexRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_index_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        name = client.index_path(
            "[PROJECT]", "[DATABASE]", "[COLLECTION_ID]", "[INDEX_ID]"
        )

        with pytest.raises(CustomException):
            client.delete_index(name)

    def test_import_documents(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        done = True
        expected_response = {"name": name_2, "done": done}
        expected_response = operations_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        name = client.database_path("[PROJECT]", "[DATABASE]")

        response = client.import_documents(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.ImportDocumentsRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_import_documents_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        name = client.database_path("[PROJECT]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.import_documents(name)

    def test_export_documents(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        done = True
        expected_response = {"name": name_2, "done": done}
        expected_response = operations_pb2.Operation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        name = client.database_path("[PROJECT]", "[DATABASE]")

        response = client.export_documents(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.ExportDocumentsRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_export_documents_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        name = client.database_path("[PROJECT]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.export_documents(name)

    def test_get_field(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = field_pb2.Field(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        name = client.field_path(
            "[PROJECT]", "[DATABASE]", "[COLLECTION_ID]", "[FIELD_ID]"
        )

        response = client.get_field(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.GetFieldRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_field_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        name = client.field_path(
            "[PROJECT]", "[DATABASE]", "[COLLECTION_ID]", "[FIELD_ID]"
        )

        with pytest.raises(CustomException):
            client.get_field(name)

    def test_list_fields(self):
        # Setup Expected Response
        next_page_token = ""
        fields_element = {}
        fields = [fields_element]
        expected_response = {"next_page_token": next_page_token, "fields": fields}
        expected_response = firestore_admin_pb2.ListFieldsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        parent = client.parent_path("[PROJECT]", "[DATABASE]", "[COLLECTION_ID]")

        paged_list_response = client.list_fields(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.fields[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.ListFieldsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_fields_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        parent = client.parent_path("[PROJECT]", "[DATABASE]", "[COLLECTION_ID]")

        paged_list_response = client.list_fields(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_field(self):
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
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup Request
        field = {}

        response = client.update_field(field)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = firestore_admin_pb2.UpdateFieldRequest(field=field)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_field_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = firestore_admin_v1.FirestoreAdminClient()

        # Setup request
        field = {}

        with pytest.raises(CustomException):
            client.update_field(field)
