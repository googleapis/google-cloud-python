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

from google.cloud import dataproc_v1beta2
from google.cloud.dataproc_v1beta2.proto import autoscaling_policies_pb2
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


class TestAutoscalingPolicyServiceClient(object):
    def test_create_autoscaling_policy(self):
        # Setup Expected Response
        id_ = "id3355"
        name = "name3373707"
        expected_response = {"id": id_, "name": name}
        expected_response = autoscaling_policies_pb2.AutoscalingPolicy(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup Request
        parent = client.region_path("[PROJECT]", "[REGION]")
        policy = {}

        response = client.create_autoscaling_policy(parent, policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = autoscaling_policies_pb2.CreateAutoscalingPolicyRequest(
            parent=parent, policy=policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_autoscaling_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup request
        parent = client.region_path("[PROJECT]", "[REGION]")
        policy = {}

        with pytest.raises(CustomException):
            client.create_autoscaling_policy(parent, policy)

    def test_update_autoscaling_policy(self):
        # Setup Expected Response
        id_ = "id3355"
        name = "name3373707"
        expected_response = {"id": id_, "name": name}
        expected_response = autoscaling_policies_pb2.AutoscalingPolicy(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup Request
        policy = {}

        response = client.update_autoscaling_policy(policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = autoscaling_policies_pb2.UpdateAutoscalingPolicyRequest(
            policy=policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_autoscaling_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup request
        policy = {}

        with pytest.raises(CustomException):
            client.update_autoscaling_policy(policy)

    def test_get_autoscaling_policy(self):
        # Setup Expected Response
        id_ = "id3355"
        name_2 = "name2-1052831874"
        expected_response = {"id": id_, "name": name_2}
        expected_response = autoscaling_policies_pb2.AutoscalingPolicy(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup Request
        name = client.autoscaling_policy_path(
            "[PROJECT]", "[REGION]", "[AUTOSCALING_POLICY]"
        )

        response = client.get_autoscaling_policy(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = autoscaling_policies_pb2.GetAutoscalingPolicyRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_autoscaling_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup request
        name = client.autoscaling_policy_path(
            "[PROJECT]", "[REGION]", "[AUTOSCALING_POLICY]"
        )

        with pytest.raises(CustomException):
            client.get_autoscaling_policy(name)

    def test_list_autoscaling_policies(self):
        # Setup Expected Response
        next_page_token = ""
        policies_element = {}
        policies = [policies_element]
        expected_response = {"next_page_token": next_page_token, "policies": policies}
        expected_response = autoscaling_policies_pb2.ListAutoscalingPoliciesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup Request
        parent = client.region_path("[PROJECT]", "[REGION]")

        paged_list_response = client.list_autoscaling_policies(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.policies[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = autoscaling_policies_pb2.ListAutoscalingPoliciesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_autoscaling_policies_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup request
        parent = client.region_path("[PROJECT]", "[REGION]")

        paged_list_response = client.list_autoscaling_policies(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_autoscaling_policy(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup Request
        name = client.autoscaling_policy_path(
            "[PROJECT]", "[REGION]", "[AUTOSCALING_POLICY]"
        )

        client.delete_autoscaling_policy(name)

        assert len(channel.requests) == 1
        expected_request = autoscaling_policies_pb2.DeleteAutoscalingPolicyRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_autoscaling_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dataproc_v1beta2.AutoscalingPolicyServiceClient()

        # Setup request
        name = client.autoscaling_policy_path(
            "[PROJECT]", "[REGION]", "[AUTOSCALING_POLICY]"
        )

        with pytest.raises(CustomException):
            client.delete_autoscaling_policy(name)
