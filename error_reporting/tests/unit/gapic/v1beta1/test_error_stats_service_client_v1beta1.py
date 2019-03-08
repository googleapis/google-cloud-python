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
from google.cloud.errorreporting_v1beta1.proto import error_stats_service_pb2


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


class TestErrorStatsServiceClient(object):
    def test_list_group_stats(self):
        # Setup Expected Response
        next_page_token = ""
        error_group_stats_element = {}
        error_group_stats = [error_group_stats_element]
        expected_response = {
            "next_page_token": next_page_token,
            "error_group_stats": error_group_stats,
        }
        expected_response = error_stats_service_pb2.ListGroupStatsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorStatsServiceClient()

        # Setup Request
        project_name = client.project_path("[PROJECT]")
        time_range = {}

        paged_list_response = client.list_group_stats(project_name, time_range)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.error_group_stats[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = error_stats_service_pb2.ListGroupStatsRequest(
            project_name=project_name, time_range=time_range
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_group_stats_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorStatsServiceClient()

        # Setup request
        project_name = client.project_path("[PROJECT]")
        time_range = {}

        paged_list_response = client.list_group_stats(project_name, time_range)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_events(self):
        # Setup Expected Response
        next_page_token = ""
        error_events_element = {}
        error_events = [error_events_element]
        expected_response = {
            "next_page_token": next_page_token,
            "error_events": error_events,
        }
        expected_response = error_stats_service_pb2.ListEventsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorStatsServiceClient()

        # Setup Request
        project_name = client.project_path("[PROJECT]")
        group_id = "groupId506361563"

        paged_list_response = client.list_events(project_name, group_id)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.error_events[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = error_stats_service_pb2.ListEventsRequest(
            project_name=project_name, group_id=group_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_events_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorStatsServiceClient()

        # Setup request
        project_name = client.project_path("[PROJECT]")
        group_id = "groupId506361563"

        paged_list_response = client.list_events(project_name, group_id)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_events(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = error_stats_service_pb2.DeleteEventsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorStatsServiceClient()

        # Setup Request
        project_name = client.project_path("[PROJECT]")

        response = client.delete_events(project_name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = error_stats_service_pb2.DeleteEventsRequest(
            project_name=project_name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_events_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = errorreporting_v1beta1.ErrorStatsServiceClient()

        # Setup request
        project_name = client.project_path("[PROJECT]")

        with pytest.raises(CustomException):
            client.delete_events(project_name)
