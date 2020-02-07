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

from google.cloud import accessapproval_v1
from google.cloud.accessapproval_v1.proto import accessapproval_pb2
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


class TestAccessApprovalClient(object):
    def test_list_approval_requests(self):
        # Setup Expected Response
        next_page_token = ""
        approval_requests_element = {}
        approval_requests = [approval_requests_element]
        expected_response = {
            "next_page_token": next_page_token,
            "approval_requests": approval_requests,
        }
        expected_response = accessapproval_pb2.ListApprovalRequestsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        paged_list_response = client.list_approval_requests()
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.approval_requests[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = accessapproval_pb2.ListApprovalRequestsMessage()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_approval_requests_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        paged_list_response = client.list_approval_requests()
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_approval_request(self):
        # Setup Expected Response
        name = "name3373707"
        requested_resource_name = "requestedResourceName-1409378037"
        expected_response = {
            "name": name,
            "requested_resource_name": requested_resource_name,
        }
        expected_response = accessapproval_pb2.ApprovalRequest(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        response = client.get_approval_request()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = accessapproval_pb2.GetApprovalRequestMessage()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_approval_request_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        with pytest.raises(CustomException):
            client.get_approval_request()

    def test_approve_approval_request(self):
        # Setup Expected Response
        name = "name3373707"
        requested_resource_name = "requestedResourceName-1409378037"
        expected_response = {
            "name": name,
            "requested_resource_name": requested_resource_name,
        }
        expected_response = accessapproval_pb2.ApprovalRequest(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        response = client.approve_approval_request()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = accessapproval_pb2.ApproveApprovalRequestMessage()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_approve_approval_request_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        with pytest.raises(CustomException):
            client.approve_approval_request()

    def test_dismiss_approval_request(self):
        # Setup Expected Response
        name = "name3373707"
        requested_resource_name = "requestedResourceName-1409378037"
        expected_response = {
            "name": name,
            "requested_resource_name": requested_resource_name,
        }
        expected_response = accessapproval_pb2.ApprovalRequest(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        response = client.dismiss_approval_request()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = accessapproval_pb2.DismissApprovalRequestMessage()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_dismiss_approval_request_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        with pytest.raises(CustomException):
            client.dismiss_approval_request()

    def test_get_access_approval_settings(self):
        # Setup Expected Response
        name = "name3373707"
        enrolled_ancestor = False
        expected_response = {"name": name, "enrolled_ancestor": enrolled_ancestor}
        expected_response = accessapproval_pb2.AccessApprovalSettings(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        response = client.get_access_approval_settings()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = accessapproval_pb2.GetAccessApprovalSettingsMessage()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_access_approval_settings_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        with pytest.raises(CustomException):
            client.get_access_approval_settings()

    def test_update_access_approval_settings(self):
        # Setup Expected Response
        name = "name3373707"
        enrolled_ancestor = False
        expected_response = {"name": name, "enrolled_ancestor": enrolled_ancestor}
        expected_response = accessapproval_pb2.AccessApprovalSettings(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        response = client.update_access_approval_settings()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = accessapproval_pb2.UpdateAccessApprovalSettingsMessage()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_access_approval_settings_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        with pytest.raises(CustomException):
            client.update_access_approval_settings()

    def test_delete_access_approval_settings(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        client.delete_access_approval_settings()

        assert len(channel.requests) == 1
        expected_request = accessapproval_pb2.DeleteAccessApprovalSettingsMessage()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_access_approval_settings_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = accessapproval_v1.AccessApprovalClient()

        with pytest.raises(CustomException):
            client.delete_access_approval_settings()
