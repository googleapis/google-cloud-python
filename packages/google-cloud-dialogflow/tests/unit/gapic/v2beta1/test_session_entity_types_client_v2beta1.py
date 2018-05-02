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

import dialogflow_v2beta1
from dialogflow_v2beta1.proto import session_entity_type_pb2
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

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestSessionEntityTypesClient(object):
    def test_list_session_entity_types(self):
        # Setup Expected Response
        next_page_token = ''
        session_entity_types_element = {}
        session_entity_types = [session_entity_types_element]
        expected_response = {
            'next_page_token': next_page_token,
            'session_entity_types': session_entity_types
        }
        expected_response = session_entity_type_pb2.ListSessionEntityTypesResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup Request
        parent = client.session_path('[PROJECT]', '[SESSION]')

        paged_list_response = client.list_session_entity_types(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.session_entity_types[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = session_entity_type_pb2.ListSessionEntityTypesRequest(
            parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_session_entity_types_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup request
        parent = client.session_path('[PROJECT]', '[SESSION]')

        paged_list_response = client.list_session_entity_types(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_session_entity_type(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        expected_response = {'name': name_2}
        expected_response = session_entity_type_pb2.SessionEntityType(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup Request
        name = client.session_entity_type_path('[PROJECT]', '[SESSION]',
                                               '[ENTITY_TYPE]')

        response = client.get_session_entity_type(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = session_entity_type_pb2.GetSessionEntityTypeRequest(
            name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_session_entity_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup request
        name = client.session_entity_type_path('[PROJECT]', '[SESSION]',
                                               '[ENTITY_TYPE]')

        with pytest.raises(CustomException):
            client.get_session_entity_type(name)

    def test_create_session_entity_type(self):
        # Setup Expected Response
        name = 'name3373707'
        expected_response = {'name': name}
        expected_response = session_entity_type_pb2.SessionEntityType(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup Request
        parent = client.session_path('[PROJECT]', '[SESSION]')
        session_entity_type = {}

        response = client.create_session_entity_type(parent,
                                                     session_entity_type)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = session_entity_type_pb2.CreateSessionEntityTypeRequest(
            parent=parent, session_entity_type=session_entity_type)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_session_entity_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup request
        parent = client.session_path('[PROJECT]', '[SESSION]')
        session_entity_type = {}

        with pytest.raises(CustomException):
            client.create_session_entity_type(parent, session_entity_type)

    def test_update_session_entity_type(self):
        # Setup Expected Response
        name = 'name3373707'
        expected_response = {'name': name}
        expected_response = session_entity_type_pb2.SessionEntityType(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup Request
        session_entity_type = {}

        response = client.update_session_entity_type(session_entity_type)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = session_entity_type_pb2.UpdateSessionEntityTypeRequest(
            session_entity_type=session_entity_type)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_session_entity_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup request
        session_entity_type = {}

        with pytest.raises(CustomException):
            client.update_session_entity_type(session_entity_type)

    def test_delete_session_entity_type(self):
        channel = ChannelStub()
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup Request
        name = client.session_entity_type_path('[PROJECT]', '[SESSION]',
                                               '[ENTITY_TYPE]')

        client.delete_session_entity_type(name)

        assert len(channel.requests) == 1
        expected_request = session_entity_type_pb2.DeleteSessionEntityTypeRequest(
            name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_session_entity_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.SessionEntityTypesClient(channel=channel)

        # Setup request
        name = client.session_entity_type_path('[PROJECT]', '[SESSION]',
                                               '[ENTITY_TYPE]')

        with pytest.raises(CustomException):
            client.delete_session_entity_type(name)
