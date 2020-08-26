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
from dialogflow_v2beta1.proto import environment_pb2


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


class TestEnvironmentsClient(object):
    def test_list_environments(self):
        # Setup Expected Response
        next_page_token = ""
        environments_element = {}
        environments = [environments_element]
        expected_response = {
            "next_page_token": next_page_token,
            "environments": environments,
        }
        expected_response = environment_pb2.ListEnvironmentsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.EnvironmentsClient()

        # Setup Request
        parent = "parent-995424086"

        paged_list_response = client.list_environments(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.environments[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = environment_pb2.ListEnvironmentsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_environments_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflow_v2beta1.EnvironmentsClient()

        # Setup request
        parent = "parent-995424086"

        paged_list_response = client.list_environments(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)
