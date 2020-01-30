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

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.proto import alert_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2
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


class TestAlertPolicyServiceClient(object):
    def test_list_alert_policies(self):
        # Setup Expected Response
        next_page_token = ""
        alert_policies_element = {}
        alert_policies = [alert_policies_element]
        expected_response = {
            "next_page_token": next_page_token,
            "alert_policies": alert_policies,
        }
        expected_response = alert_service_pb2.ListAlertPoliciesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_alert_policies(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.alert_policies[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = alert_service_pb2.ListAlertPoliciesRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_alert_policies_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_alert_policies(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_alert_policy(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        expected_response = {"name": name_2, "display_name": display_name}
        expected_response = alert_pb2.AlertPolicy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup Request
        name = client.alert_policy_path("[PROJECT]", "[ALERT_POLICY]")

        response = client.get_alert_policy(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = alert_service_pb2.GetAlertPolicyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_alert_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup request
        name = client.alert_policy_path("[PROJECT]", "[ALERT_POLICY]")

        with pytest.raises(CustomException):
            client.get_alert_policy(name)

    def test_create_alert_policy(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        expected_response = {"name": name_2, "display_name": display_name}
        expected_response = alert_pb2.AlertPolicy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")
        alert_policy = {}

        response = client.create_alert_policy(name, alert_policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = alert_service_pb2.CreateAlertPolicyRequest(
            name=name, alert_policy=alert_policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_alert_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")
        alert_policy = {}

        with pytest.raises(CustomException):
            client.create_alert_policy(name, alert_policy)

    def test_delete_alert_policy(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup Request
        name = client.alert_policy_path("[PROJECT]", "[ALERT_POLICY]")

        client.delete_alert_policy(name)

        assert len(channel.requests) == 1
        expected_request = alert_service_pb2.DeleteAlertPolicyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_alert_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup request
        name = client.alert_policy_path("[PROJECT]", "[ALERT_POLICY]")

        with pytest.raises(CustomException):
            client.delete_alert_policy(name)

    def test_update_alert_policy(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = alert_pb2.AlertPolicy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup Request
        alert_policy = {}

        response = client.update_alert_policy(alert_policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = alert_service_pb2.UpdateAlertPolicyRequest(
            alert_policy=alert_policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_alert_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.AlertPolicyServiceClient()

        # Setup request
        alert_policy = {}

        with pytest.raises(CustomException):
            client.update_alert_policy(alert_policy)
