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

from google.cloud.monitoring_dashboard import v1
from google.cloud.monitoring_dashboard.v1.proto import dashboard_pb2
from google.cloud.monitoring_dashboard.v1.proto import dashboards_service_pb2
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


class TestDashboardsServiceClient(object):
    def test_create_dashboard(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        etag = "etag3123477"
        expected_response = {"name": name, "display_name": display_name, "etag": etag}
        expected_response = dashboard_pb2.Dashboard(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup Request
        parent = "parent-995424086"
        dashboard = {}

        response = client.create_dashboard(parent, dashboard)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dashboards_service_pb2.CreateDashboardRequest(
            parent=parent, dashboard=dashboard
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_dashboard_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup request
        parent = "parent-995424086"
        dashboard = {}

        with pytest.raises(CustomException):
            client.create_dashboard(parent, dashboard)

    def test_list_dashboards(self):
        # Setup Expected Response
        next_page_token = ""
        dashboards_element = {}
        dashboards = [dashboards_element]
        expected_response = {
            "next_page_token": next_page_token,
            "dashboards": dashboards,
        }
        expected_response = dashboards_service_pb2.ListDashboardsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup Request
        parent = "parent-995424086"

        paged_list_response = client.list_dashboards(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.dashboards[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = dashboards_service_pb2.ListDashboardsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_dashboards_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup request
        parent = "parent-995424086"

        paged_list_response = client.list_dashboards(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_dashboard(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        etag = "etag3123477"
        expected_response = {"name": name_2, "display_name": display_name, "etag": etag}
        expected_response = dashboard_pb2.Dashboard(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup Request
        name = "name3373707"

        response = client.get_dashboard(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dashboards_service_pb2.GetDashboardRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_dashboard_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup request
        name = "name3373707"

        with pytest.raises(CustomException):
            client.get_dashboard(name)

    def test_delete_dashboard(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup Request
        name = "name3373707"

        client.delete_dashboard(name)

        assert len(channel.requests) == 1
        expected_request = dashboards_service_pb2.DeleteDashboardRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_dashboard_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup request
        name = "name3373707"

        with pytest.raises(CustomException):
            client.delete_dashboard(name)

    def test_update_dashboard(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        etag = "etag3123477"
        expected_response = {"name": name, "display_name": display_name, "etag": etag}
        expected_response = dashboard_pb2.Dashboard(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup Request
        dashboard = {}

        response = client.update_dashboard(dashboard)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = dashboards_service_pb2.UpdateDashboardRequest(
            dashboard=dashboard
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_dashboard_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = v1.DashboardsServiceClient()

        # Setup request
        dashboard = {}

        with pytest.raises(CustomException):
            client.update_dashboard(dashboard)
