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
from dialogflow_v2.proto import entity_type_pb2
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


class TestEntityTypesClient(object):
    def test_list_entity_types(self):
        # Setup Expected Response
        next_page_token = ''
        entity_types_element = {}
        entity_types = [entity_types_element]
        expected_response = {
            'next_page_token': next_page_token,
            'entity_types': entity_types
        }
        expected_response = entity_type_pb2.ListEntityTypesResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.project_agent_path('[PROJECT]')

        paged_list_response = client.list_entity_types(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.entity_types[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.ListEntityTypesRequest(
            parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_entity_types_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup request
        parent = client.project_agent_path('[PROJECT]')

        paged_list_response = client.list_entity_types(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_entity_type(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        display_name = 'displayName1615086568'
        expected_response = {'name': name_2, 'display_name': display_name}
        expected_response = entity_type_pb2.EntityType(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        name = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')

        response = client.get_entity_type(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.GetEntityTypeRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_entity_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup request
        name = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')

        with pytest.raises(CustomException):
            client.get_entity_type(name)

    def test_create_entity_type(self):
        # Setup Expected Response
        name = 'name3373707'
        display_name = 'displayName1615086568'
        expected_response = {'name': name, 'display_name': display_name}
        expected_response = entity_type_pb2.EntityType(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.project_agent_path('[PROJECT]')
        entity_type = {}

        response = client.create_entity_type(parent, entity_type)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.CreateEntityTypeRequest(
            parent=parent, entity_type=entity_type)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_entity_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup request
        parent = client.project_agent_path('[PROJECT]')
        entity_type = {}

        with pytest.raises(CustomException):
            client.create_entity_type(parent, entity_type)

    def test_update_entity_type(self):
        # Setup Expected Response
        name = 'name3373707'
        display_name = 'displayName1615086568'
        expected_response = {'name': name, 'display_name': display_name}
        expected_response = entity_type_pb2.EntityType(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        entity_type = {}

        response = client.update_entity_type(entity_type)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.UpdateEntityTypeRequest(
            entity_type=entity_type)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_entity_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup request
        entity_type = {}

        with pytest.raises(CustomException):
            client.update_entity_type(entity_type)

    def test_delete_entity_type(self):
        channel = ChannelStub()
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        name = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')

        client.delete_entity_type(name)

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.DeleteEntityTypeRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_entity_type_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup request
        name = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')

        with pytest.raises(CustomException):
            client.delete_entity_type(name)

    def test_batch_update_entity_types(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = entity_type_pb2.BatchUpdateEntityTypesResponse(
            **expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_batch_update_entity_types', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.project_agent_path('[PROJECT]')

        response = client.batch_update_entity_types(parent)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.BatchUpdateEntityTypesRequest(
            parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_update_entity_types_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_batch_update_entity_types_exception',
            done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.project_agent_path('[PROJECT]')

        response = client.batch_update_entity_types(parent)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_batch_delete_entity_types(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_batch_delete_entity_types', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.project_agent_path('[PROJECT]')
        entity_type_names = []

        response = client.batch_delete_entity_types(parent, entity_type_names)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.BatchDeleteEntityTypesRequest(
            parent=parent, entity_type_names=entity_type_names)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_delete_entity_types_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_batch_delete_entity_types_exception',
            done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.project_agent_path('[PROJECT]')
        entity_type_names = []

        response = client.batch_delete_entity_types(parent, entity_type_names)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_batch_create_entities(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_batch_create_entities', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
        entities = []

        response = client.batch_create_entities(parent, entities)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.BatchCreateEntitiesRequest(
            parent=parent, entities=entities)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_create_entities_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_batch_create_entities_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
        entities = []

        response = client.batch_create_entities(parent, entities)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_batch_update_entities(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_batch_update_entities', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
        entities = []

        response = client.batch_update_entities(parent, entities)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.BatchUpdateEntitiesRequest(
            parent=parent, entities=entities)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_update_entities_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_batch_update_entities_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
        entities = []

        response = client.batch_update_entities(parent, entities)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_batch_delete_entities(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_batch_delete_entities', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
        entity_values = []

        response = client.batch_delete_entities(parent, entity_values)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = entity_type_pb2.BatchDeleteEntitiesRequest(
            parent=parent, entity_values=entity_values)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_delete_entities_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_batch_delete_entities_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2.EntityTypesClient(channel=channel)

        # Setup Request
        parent = client.entity_type_path('[PROJECT]', '[ENTITY_TYPE]')
        entity_values = []

        response = client.batch_delete_entities(parent, entity_values)
        exception = response.exception()
        assert exception.errors[0] == error
