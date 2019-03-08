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

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.proto import notification_pb2
from google.cloud.monitoring_v3.proto import notification_service_pb2
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


class TestNotificationChannelServiceClient(object):
    def test_list_notification_channel_descriptors(self):
        # Setup Expected Response
        next_page_token = ""
        channel_descriptors_element = {}
        channel_descriptors = [channel_descriptors_element]
        expected_response = {
            "next_page_token": next_page_token,
            "channel_descriptors": channel_descriptors,
        }
        expected_response = notification_service_pb2.ListNotificationChannelDescriptorsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_notification_channel_descriptors(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.channel_descriptors[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = notification_service_pb2.ListNotificationChannelDescriptorsRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_notification_channel_descriptors_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_notification_channel_descriptors(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_notification_channel_descriptor(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        type_ = "type3575610"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name_2,
            "type": type_,
            "display_name": display_name,
            "description": description,
        }
        expected_response = notification_pb2.NotificationChannelDescriptor(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup Request
        name = client.notification_channel_descriptor_path(
            "[PROJECT]", "[CHANNEL_DESCRIPTOR]"
        )

        response = client.get_notification_channel_descriptor(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = notification_service_pb2.GetNotificationChannelDescriptorRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_notification_channel_descriptor_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup request
        name = client.notification_channel_descriptor_path(
            "[PROJECT]", "[CHANNEL_DESCRIPTOR]"
        )

        with pytest.raises(CustomException):
            client.get_notification_channel_descriptor(name)

    def test_list_notification_channels(self):
        # Setup Expected Response
        next_page_token = ""
        notification_channels_element = {}
        notification_channels = [notification_channels_element]
        expected_response = {
            "next_page_token": next_page_token,
            "notification_channels": notification_channels,
        }
        expected_response = notification_service_pb2.ListNotificationChannelsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_notification_channels(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.notification_channels[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = notification_service_pb2.ListNotificationChannelsRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_notification_channels_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_notification_channels(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_notification_channel(self):
        # Setup Expected Response
        type_ = "type3575610"
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "type": type_,
            "name": name_2,
            "display_name": display_name,
            "description": description,
        }
        expected_response = notification_pb2.NotificationChannel(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup Request
        name = client.notification_channel_path("[PROJECT]", "[NOTIFICATION_CHANNEL]")

        response = client.get_notification_channel(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = notification_service_pb2.GetNotificationChannelRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_notification_channel_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup request
        name = client.notification_channel_path("[PROJECT]", "[NOTIFICATION_CHANNEL]")

        with pytest.raises(CustomException):
            client.get_notification_channel(name)

    def test_create_notification_channel(self):
        # Setup Expected Response
        type_ = "type3575610"
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "type": type_,
            "name": name_2,
            "display_name": display_name,
            "description": description,
        }
        expected_response = notification_pb2.NotificationChannel(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")
        notification_channel = {}

        response = client.create_notification_channel(name, notification_channel)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = notification_service_pb2.CreateNotificationChannelRequest(
            name=name, notification_channel=notification_channel
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_notification_channel_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")
        notification_channel = {}

        with pytest.raises(CustomException):
            client.create_notification_channel(name, notification_channel)

    def test_update_notification_channel(self):
        # Setup Expected Response
        type_ = "type3575610"
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "type": type_,
            "name": name,
            "display_name": display_name,
            "description": description,
        }
        expected_response = notification_pb2.NotificationChannel(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup Request
        notification_channel = {}

        response = client.update_notification_channel(notification_channel)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = notification_service_pb2.UpdateNotificationChannelRequest(
            notification_channel=notification_channel
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_notification_channel_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup request
        notification_channel = {}

        with pytest.raises(CustomException):
            client.update_notification_channel(notification_channel)

    def test_delete_notification_channel(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup Request
        name = client.notification_channel_path("[PROJECT]", "[NOTIFICATION_CHANNEL]")

        client.delete_notification_channel(name)

        assert len(channel.requests) == 1
        expected_request = notification_service_pb2.DeleteNotificationChannelRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_notification_channel_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.NotificationChannelServiceClient()

        # Setup request
        name = client.notification_channel_path("[PROJECT]", "[NOTIFICATION_CHANNEL]")

        with pytest.raises(CustomException):
            client.delete_notification_channel(name)
