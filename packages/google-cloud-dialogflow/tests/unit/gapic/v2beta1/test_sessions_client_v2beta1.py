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
from dialogflow_v2beta1.proto import session_pb2


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

    def stream_stream(self,
                      method,
                      request_serializer=None,
                      response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestSessionsClient(object):
    def test_detect_intent(self):
        # Setup Expected Response
        response_id = 'responseId1847552473'
        expected_response = {'response_id': response_id}
        expected_response = session_pb2.DetectIntentResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = dialogflow_v2beta1.SessionsClient(channel=channel)

        # Setup Request
        session = client.session_path('[PROJECT]', '[SESSION]')
        query_input = {}

        response = client.detect_intent(session, query_input)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = session_pb2.DetectIntentRequest(
            session=session, query_input=query_input)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_detect_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.SessionsClient(channel=channel)

        # Setup request
        session = client.session_path('[PROJECT]', '[SESSION]')
        query_input = {}

        with pytest.raises(CustomException):
            client.detect_intent(session, query_input)

    def test_streaming_detect_intent(self):
        # Setup Expected Response
        response_id = 'responseId1847552473'
        expected_response = {'response_id': response_id}
        expected_response = session_pb2.StreamingDetectIntentResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        client = dialogflow_v2beta1.SessionsClient(channel=channel)

        # Setup Request
        session = 'session1984987798'
        query_input = {}
        request = {'session': session, 'query_input': query_input}
        request = session_pb2.StreamingDetectIntentRequest(**request)
        requests = [request]

        response = client.streaming_detect_intent(requests)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        actual_requests = channel.requests[0][1]
        assert len(actual_requests) == 1
        actual_request = list(actual_requests)[0]
        assert request == actual_request

    def test_streaming_detect_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = dialogflow_v2beta1.SessionsClient(channel=channel)

        # Setup request
        session = 'session1984987798'
        query_input = {}
        request = {'session': session, 'query_input': query_input}

        request = session_pb2.StreamingDetectIntentRequest(**request)
        requests = [request]

        with pytest.raises(CustomException):
            client.streaming_detect_intent(requests)
