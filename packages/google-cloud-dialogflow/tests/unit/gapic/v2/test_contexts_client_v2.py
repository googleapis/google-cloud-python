# Copyright 2018 Google LLC
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

import pytest

import dialogflow_v2
from dialogflow_v2.proto import context_pb2


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

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestContextsClient(object):
    def test_list_contexts(self):
        # Setup Expected Response
        next_page_token = ''
        contexts_element = {}
        contexts = [contexts_element]
        expected_response = {
            'next_page_token': next_page_token,
            'contexts': contexts
        }
        expected_response = context_pb2.ListContextsResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup Request
        parent = client.session_path('[PROJECT]', '[SESSION]')

        paged_list_response = client.list_contexts(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.contexts[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = context_pb2.ListContextsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_contexts_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup request
        parent = client.session_path('[PROJECT]', '[SESSION]')

        paged_list_response = client.list_contexts(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_context(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        lifespan_count = 1178775510
        expected_response = {'name': name_2, 'lifespan_count': lifespan_count}
        expected_response = context_pb2.Context(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup Request
        name = client.context_path('[PROJECT]', '[SESSION]', '[CONTEXT]')

        response = client.get_context(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = context_pb2.GetContextRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_context_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup request
        name = client.context_path('[PROJECT]', '[SESSION]', '[CONTEXT]')

        with pytest.raises(CustomException):
            client.get_context(name)

    def test_create_context(self):
        # Setup Expected Response
        name = 'name3373707'
        lifespan_count = 1178775510
        expected_response = {'name': name, 'lifespan_count': lifespan_count}
        expected_response = context_pb2.Context(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup Request
        parent = client.session_path('[PROJECT]', '[SESSION]')
        context = {}

        response = client.create_context(parent, context)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = context_pb2.CreateContextRequest(
            parent=parent, context=context)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_context_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup request
        parent = client.session_path('[PROJECT]', '[SESSION]')
        context = {}

        with pytest.raises(CustomException):
            client.create_context(parent, context)

    def test_update_context(self):
        # Setup Expected Response
        name = 'name3373707'
        lifespan_count = 1178775510
        expected_response = {'name': name, 'lifespan_count': lifespan_count}
        expected_response = context_pb2.Context(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup Request
        context = {}

        response = client.update_context(context)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = context_pb2.UpdateContextRequest(context=context)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_context_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup request
        context = {}

        with pytest.raises(CustomException):
            client.update_context(context)

    def test_delete_context(self):
        channel = ChannelStub()
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup Request
        name = client.context_path('[PROJECT]', '[SESSION]', '[CONTEXT]')

        client.delete_context(name)

        assert len(channel.requests) == 1
        expected_request = context_pb2.DeleteContextRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_context_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup request
        name = client.context_path('[PROJECT]', '[SESSION]', '[CONTEXT]')

        with pytest.raises(CustomException):
            client.delete_context(name)

    def test_delete_all_contexts(self):
        channel = ChannelStub()
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup Request
        parent = client.session_path('[PROJECT]', '[SESSION]')

        client.delete_all_contexts(parent)

        assert len(channel.requests) == 1
        expected_request = context_pb2.DeleteAllContextsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_all_contexts_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.ContextsClient(channel=channel)

        # Setup request
        parent = client.session_path('[PROJECT]', '[SESSION]')

        with pytest.raises(CustomException):
            client.delete_all_contexts(parent)
