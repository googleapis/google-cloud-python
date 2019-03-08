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

from google.cloud import errorreporting_v1beta1
from google.cloud.errorreporting_v1beta1.proto import common_pb2
from google.cloud.errorreporting_v1beta1.proto import error_group_service_pb2


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


class TestErrorGroupServiceClient(object):
    def test_get_group(self):
        # Setup Expected Response
        name = "name3373707"
        group_id = "groupId506361563"
        expected_response = {"name": name, "group_id": group_id}
        expected_response = common_pb2.ErrorGroup(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorGroupServiceClient()

        # Setup Request
        group_name = client.group_path("[PROJECT]", "[GROUP]")

        response = client.get_group(group_name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = error_group_service_pb2.GetGroupRequest(
            group_name=group_name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_group_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorGroupServiceClient()

        # Setup request
        group_name = client.group_path("[PROJECT]", "[GROUP]")

        with pytest.raises(CustomException):
            client.get_group(group_name)

    def test_update_group(self):
        # Setup Expected Response
        name = "name3373707"
        group_id = "groupId506361563"
        expected_response = {"name": name, "group_id": group_id}
        expected_response = common_pb2.ErrorGroup(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorGroupServiceClient()

        # Setup Request
        group = {}

        response = client.update_group(group)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = error_group_service_pb2.UpdateGroupRequest(group=group)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_group_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorGroupServiceClient()

        # Setup request
        group = {}

        with pytest.raises(CustomException):
            client.update_group(group)
