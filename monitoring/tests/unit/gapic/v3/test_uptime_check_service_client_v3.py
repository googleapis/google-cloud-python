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
from google.cloud.monitoring_v3.proto import uptime_pb2
from google.cloud.monitoring_v3.proto import uptime_service_pb2
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


class TestUptimeCheckServiceClient(object):
    def test_list_uptime_check_configs(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        uptime_check_configs_element = {}
        uptime_check_configs = [uptime_check_configs_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "uptime_check_configs": uptime_check_configs,
        }
        expected_response = uptime_service_pb2.ListUptimeCheckConfigsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_uptime_check_configs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.uptime_check_configs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = uptime_service_pb2.ListUptimeCheckConfigsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_uptime_check_configs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_uptime_check_configs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_uptime_check_config(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        is_internal = True
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "is_internal": is_internal,
        }
        expected_response = uptime_pb2.UptimeCheckConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup Request
        name = client.uptime_check_config_path("[PROJECT]", "[UPTIME_CHECK_CONFIG]")

        response = client.get_uptime_check_config(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = uptime_service_pb2.GetUptimeCheckConfigRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_uptime_check_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup request
        name = client.uptime_check_config_path("[PROJECT]", "[UPTIME_CHECK_CONFIG]")

        with pytest.raises(CustomException):
            client.get_uptime_check_config(name)

    def test_create_uptime_check_config(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        is_internal = True
        expected_response = {
            "name": name,
            "display_name": display_name,
            "is_internal": is_internal,
        }
        expected_response = uptime_pb2.UptimeCheckConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        uptime_check_config = {}

        response = client.create_uptime_check_config(parent, uptime_check_config)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = uptime_service_pb2.CreateUptimeCheckConfigRequest(
            parent=parent, uptime_check_config=uptime_check_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_uptime_check_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        uptime_check_config = {}

        with pytest.raises(CustomException):
            client.create_uptime_check_config(parent, uptime_check_config)

    def test_update_uptime_check_config(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        is_internal = True
        expected_response = {
            "name": name,
            "display_name": display_name,
            "is_internal": is_internal,
        }
        expected_response = uptime_pb2.UptimeCheckConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup Request
        uptime_check_config = {}

        response = client.update_uptime_check_config(uptime_check_config)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = uptime_service_pb2.UpdateUptimeCheckConfigRequest(
            uptime_check_config=uptime_check_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_uptime_check_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup request
        uptime_check_config = {}

        with pytest.raises(CustomException):
            client.update_uptime_check_config(uptime_check_config)

    def test_delete_uptime_check_config(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup Request
        name = client.uptime_check_config_path("[PROJECT]", "[UPTIME_CHECK_CONFIG]")

        client.delete_uptime_check_config(name)

        assert len(channel.requests) == 1
        expected_request = uptime_service_pb2.DeleteUptimeCheckConfigRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_uptime_check_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        # Setup request
        name = client.uptime_check_config_path("[PROJECT]", "[UPTIME_CHECK_CONFIG]")

        with pytest.raises(CustomException):
            client.delete_uptime_check_config(name)

    def test_list_uptime_check_ips(self):
        # Setup Expected Response
        next_page_token = ""
        uptime_check_ips_element = {}
        uptime_check_ips = [uptime_check_ips_element]
        expected_response = {
            "next_page_token": next_page_token,
            "uptime_check_ips": uptime_check_ips,
        }
        expected_response = uptime_service_pb2.ListUptimeCheckIpsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        paged_list_response = client.list_uptime_check_ips()
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.uptime_check_ips[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = uptime_service_pb2.ListUptimeCheckIpsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_uptime_check_ips_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.UptimeCheckServiceClient()

        paged_list_response = client.list_uptime_check_ips()
        with pytest.raises(CustomException):
            list(paged_list_response)
