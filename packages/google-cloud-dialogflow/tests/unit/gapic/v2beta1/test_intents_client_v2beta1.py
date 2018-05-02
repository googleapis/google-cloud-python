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

import dialogflow_v2beta1
from dialogflow_v2beta1.proto import intent_pb2
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


class TestIntentsClient(object):
    def test_list_intents(self):
        # Setup Expected Response
        next_page_token = ''
        intents_element = {}
        intents = [intents_element]
        expected_response = {
            'next_page_token': next_page_token,
            'intents': intents
        }
        expected_response = intent_pb2.ListIntentsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        parent = client.project_agent_path('[PROJECT]')

        paged_list_response = client.list_intents(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.intents[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = intent_pb2.ListIntentsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_intents_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup request
        parent = client.project_agent_path('[PROJECT]')

        paged_list_response = client.list_intents(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_intent(self):
        # Setup Expected Response
        name_2 = 'name2-1052831874'
        display_name = 'displayName1615086568'
        priority = 1165461084
        is_fallback = False
        ml_enabled = False
        ml_disabled = True
        action = 'action-1422950858'
        reset_contexts = True
        root_followup_intent_name = 'rootFollowupIntentName402253784'
        parent_followup_intent_name = 'parentFollowupIntentName-1131901680'
        expected_response = {
            'name': name_2,
            'display_name': display_name,
            'priority': priority,
            'is_fallback': is_fallback,
            'ml_enabled': ml_enabled,
            'ml_disabled': ml_disabled,
            'action': action,
            'reset_contexts': reset_contexts,
            'root_followup_intent_name': root_followup_intent_name,
            'parent_followup_intent_name': parent_followup_intent_name
        }
        expected_response = intent_pb2.Intent(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        name = client.intent_path('[PROJECT]', '[INTENT]')

        response = client.get_intent(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = intent_pb2.GetIntentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup request
        name = client.intent_path('[PROJECT]', '[INTENT]')

        with pytest.raises(CustomException):
            client.get_intent(name)

    def test_create_intent(self):
        # Setup Expected Response
        name = 'name3373707'
        display_name = 'displayName1615086568'
        priority = 1165461084
        is_fallback = False
        ml_enabled = False
        ml_disabled = True
        action = 'action-1422950858'
        reset_contexts = True
        root_followup_intent_name = 'rootFollowupIntentName402253784'
        parent_followup_intent_name = 'parentFollowupIntentName-1131901680'
        expected_response = {
            'name': name,
            'display_name': display_name,
            'priority': priority,
            'is_fallback': is_fallback,
            'ml_enabled': ml_enabled,
            'ml_disabled': ml_disabled,
            'action': action,
            'reset_contexts': reset_contexts,
            'root_followup_intent_name': root_followup_intent_name,
            'parent_followup_intent_name': parent_followup_intent_name
        }
        expected_response = intent_pb2.Intent(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        parent = client.project_agent_path('[PROJECT]')
        intent = {}

        response = client.create_intent(parent, intent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = intent_pb2.CreateIntentRequest(
            parent=parent, intent=intent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup request
        parent = client.project_agent_path('[PROJECT]')
        intent = {}

        with pytest.raises(CustomException):
            client.create_intent(parent, intent)

    def test_update_intent(self):
        # Setup Expected Response
        name = 'name3373707'
        display_name = 'displayName1615086568'
        priority = 1165461084
        is_fallback = False
        ml_enabled = False
        ml_disabled = True
        action = 'action-1422950858'
        reset_contexts = True
        root_followup_intent_name = 'rootFollowupIntentName402253784'
        parent_followup_intent_name = 'parentFollowupIntentName-1131901680'
        expected_response = {
            'name': name,
            'display_name': display_name,
            'priority': priority,
            'is_fallback': is_fallback,
            'ml_enabled': ml_enabled,
            'ml_disabled': ml_disabled,
            'action': action,
            'reset_contexts': reset_contexts,
            'root_followup_intent_name': root_followup_intent_name,
            'parent_followup_intent_name': parent_followup_intent_name
        }
        expected_response = intent_pb2.Intent(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        intent = {}
        language_code = 'languageCode-412800396'

        response = client.update_intent(intent, language_code)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = intent_pb2.UpdateIntentRequest(
            intent=intent, language_code=language_code)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup request
        intent = {}
        language_code = 'languageCode-412800396'

        with pytest.raises(CustomException):
            client.update_intent(intent, language_code)

    def test_delete_intent(self):
        channel = ChannelStub()
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        name = client.intent_path('[PROJECT]', '[INTENT]')

        client.delete_intent(name)

        assert len(channel.requests) == 1
        expected_request = intent_pb2.DeleteIntentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup request
        name = client.intent_path('[PROJECT]', '[INTENT]')

        with pytest.raises(CustomException):
            client.delete_intent(name)

    def test_batch_update_intents(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = intent_pb2.BatchUpdateIntentsResponse(
            **expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_batch_update_intents', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        parent = client.agent_path('[PROJECT]', '[AGENT]')
        language_code = 'languageCode-412800396'

        response = client.batch_update_intents(parent, language_code)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = intent_pb2.BatchUpdateIntentsRequest(
            parent=parent, language_code=language_code)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_update_intents_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_batch_update_intents_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        parent = client.agent_path('[PROJECT]', '[AGENT]')
        language_code = 'languageCode-412800396'

        response = client.batch_update_intents(parent, language_code)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_batch_delete_intents(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_batch_delete_intents', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')
        intents = []

        response = client.batch_delete_intents(parent, intents)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = intent_pb2.BatchDeleteIntentsRequest(
            parent=parent, intents=intents)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_delete_intents_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_batch_delete_intents_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = dialogflow_v2beta1.IntentsClient(channel=channel)

        # Setup Request
        parent = client.project_path('[PROJECT]')
        intents = []

        response = client.batch_delete_intents(parent, intents)
        exception = response.exception()
        assert exception.errors[0] == error
