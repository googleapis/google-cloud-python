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

from google.rpc import status_pb2

import dialogflow_v2
from dialogflow_v2.proto import agent_pb2
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

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestAgentsClient(object):
    def test_get_agent(self):
        # Setup Expected Response
        parent_2 = 'parent21175163357'
        display_name = 'displayName1615086568'
        default_language_code = 'defaultLanguageCode856575222'
        time_zone = 'timeZone36848094'
        description = 'description-1724546052'
        avatar_uri = 'avatarUri-402824826'
        enable_logging = False
        classification_threshold = 1.11581064E8
        expected_response = {
            'parent': parent_2,
            'display_name': display_name,
            'default_language_code': default_language_code,
            'time_zone': time_zone,
            'description': description,
            'avatar_uri': avatar_uri,
            'enable_logging': enable_logging,
            'classification_threshold': classification_threshold
        }
        expected_response = agent_pb2.Agent(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.get_agent(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = agent_pb2.GetAgentRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_agent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        with pytest.raises(CustomException):
            client.get_agent(parent)

    def test_search_agents(self):
        # Setup Expected Response
        next_page_token = ''
        agents_element = {}
        agents = [agents_element]
        expected_response = {
            'next_page_token': next_page_token,
            'agents': agents
        }
        expected_response = agent_pb2.SearchAgentsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        paged_list_response = client.search_agents(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.agents[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = agent_pb2.SearchAgentsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_agents_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup request
        parent = client.project_path('[PROJECT]')

        paged_list_response = client.search_agents(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_train_agent(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_train_agent', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.train_agent(parent)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = agent_pb2.TrainAgentRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_train_agent_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_train_agent_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.train_agent(parent)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_export_agent(self):
        # Setup Expected Response
        agent_uri = 'agentUri-1700713166'
        agent_content = b'63'
        expected_response = {
            'agent_uri': agent_uri,
            'agent_content': agent_content
        }
        expected_response = agent_pb2.ExportAgentResponse(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_export_agent', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.export_agent(parent)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = agent_pb2.ExportAgentRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_export_agent_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_export_agent_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.export_agent(parent)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_import_agent(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_import_agent', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.import_agent(parent)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = agent_pb2.ImportAgentRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_import_agent_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_import_agent_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.import_agent(parent)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_restore_agent(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_restore_agent', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.restore_agent(parent)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = agent_pb2.RestoreAgentRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_restore_agent_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_restore_agent_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.AgentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')

        response = client.restore_agent(parent)
        exception = response.exception()
        assert exception.errors[0] == error
