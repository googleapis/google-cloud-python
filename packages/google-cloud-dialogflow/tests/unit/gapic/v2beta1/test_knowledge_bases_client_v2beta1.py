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

import dialogflow_v2beta1
from dialogflow_v2beta1.proto import knowledge_base_pb2
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


class TestKnowledgeBasesClient(object):
    def test_list_knowledge_bases(self):
        # Setup Expected Response
        next_page_token = ""
        knowledge_bases_element = {}
        knowledge_bases = [knowledge_bases_element]
        expected_response = {
            "next_page_token": next_page_token,
            "knowledge_bases": knowledge_bases,
        }
        expected_response = knowledge_base_pb2.ListKnowledgeBasesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_knowledge_bases(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.knowledge_bases[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = knowledge_base_pb2.ListKnowledgeBasesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_knowledge_bases_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_knowledge_bases(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_knowledge_base(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        language_code = "languageCode-412800396"
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "language_code": language_code,
        }
        expected_response = knowledge_base_pb2.KnowledgeBase(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup Request
        name = client.knowledge_base_path("[PROJECT]", "[KNOWLEDGE_BASE]")

        response = client.get_knowledge_base(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = knowledge_base_pb2.GetKnowledgeBaseRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_knowledge_base_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup request
        name = client.knowledge_base_path("[PROJECT]", "[KNOWLEDGE_BASE]")

        with pytest.raises(CustomException):
            client.get_knowledge_base(name)

    def test_create_knowledge_base(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        language_code = "languageCode-412800396"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "language_code": language_code,
        }
        expected_response = knowledge_base_pb2.KnowledgeBase(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        knowledge_base = {}

        response = client.create_knowledge_base(parent, knowledge_base)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = knowledge_base_pb2.CreateKnowledgeBaseRequest(
            parent=parent, knowledge_base=knowledge_base
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_knowledge_base_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        knowledge_base = {}

        with pytest.raises(CustomException):
            client.create_knowledge_base(parent, knowledge_base)

    def test_delete_knowledge_base(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup Request
        name = client.knowledge_base_path("[PROJECT]", "[KNOWLEDGE_BASE]")

        client.delete_knowledge_base(name)

        assert len(channel.requests) == 1
        expected_request = knowledge_base_pb2.DeleteKnowledgeBaseRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_knowledge_base_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup request
        name = client.knowledge_base_path("[PROJECT]", "[KNOWLEDGE_BASE]")

        with pytest.raises(CustomException):
            client.delete_knowledge_base(name)

    def test_update_knowledge_base(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        language_code = "languageCode-412800396"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "language_code": language_code,
        }
        expected_response = knowledge_base_pb2.KnowledgeBase(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup Request
        knowledge_base = {}

        response = client.update_knowledge_base(knowledge_base)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = knowledge_base_pb2.UpdateKnowledgeBaseRequest(
            knowledge_base=knowledge_base
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_knowledge_base_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.KnowledgeBasesClient()

        # Setup request
        knowledge_base = {}

        with pytest.raises(CustomException):
            client.update_knowledge_base(knowledge_base)
