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

from google.cloud import talent_v4beta1
from google.cloud.talent_v4beta1.proto import event_pb2
from google.cloud.talent_v4beta1.proto import event_service_pb2


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


class TestEventServiceClient(object):
    def test_create_client_event(self):
        # Setup Expected Response
        request_id = "requestId37109963"
        event_id = "eventId278118624"
        event_notes = "eventNotes445073628"
        expected_response = {
            "request_id": request_id,
            "event_id": event_id,
            "event_notes": event_notes,
        }
        expected_response = event_pb2.ClientEvent(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.EventServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        client_event = {}

        response = client.create_client_event(parent, client_event)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = event_service_pb2.CreateClientEventRequest(
            parent=parent, client_event=client_event
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_client_event_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.EventServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        client_event = {}

        with pytest.raises(CustomException):
            client.create_client_event(parent, client_event)
