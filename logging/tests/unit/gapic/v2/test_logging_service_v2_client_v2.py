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

from google.api import monitored_resource_pb2
from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
from google.cloud.logging_v2.proto import logging_pb2
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


class TestLoggingServiceV2Client(object):
    def test_delete_log(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        # Setup Request
        log_name = client.log_path("[PROJECT]", "[LOG]")

        client.delete_log(log_name)

        assert len(channel.requests) == 1
        expected_request = logging_pb2.DeleteLogRequest(log_name=log_name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_log_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        # Setup request
        log_name = client.log_path("[PROJECT]", "[LOG]")

        with pytest.raises(CustomException):
            client.delete_log(log_name)

    def test_write_log_entries(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = logging_pb2.WriteLogEntriesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        # Setup Request
        entries = []

        response = client.write_log_entries(entries)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = logging_pb2.WriteLogEntriesRequest(entries=entries)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_write_log_entries_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        # Setup request
        entries = []

        with pytest.raises(CustomException):
            client.write_log_entries(entries)

    def test_list_log_entries(self):
        # Setup Expected Response
        next_page_token = ""
        entries_element = {}
        entries = [entries_element]
        expected_response = {"next_page_token": next_page_token, "entries": entries}
        expected_response = logging_pb2.ListLogEntriesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        # Setup Request
        resource_names = []

        paged_list_response = client.list_log_entries(resource_names)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.entries[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = logging_pb2.ListLogEntriesRequest(
            resource_names=resource_names
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_log_entries_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        # Setup request
        resource_names = []

        paged_list_response = client.list_log_entries(resource_names)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_monitored_resource_descriptors(self):
        # Setup Expected Response
        next_page_token = ""
        resource_descriptors_element = {}
        resource_descriptors = [resource_descriptors_element]
        expected_response = {
            "next_page_token": next_page_token,
            "resource_descriptors": resource_descriptors,
        }
        expected_response = logging_pb2.ListMonitoredResourceDescriptorsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        paged_list_response = client.list_monitored_resource_descriptors()
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.resource_descriptors[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = logging_pb2.ListMonitoredResourceDescriptorsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_monitored_resource_descriptors_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        paged_list_response = client.list_monitored_resource_descriptors()
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_logs(self):
        # Setup Expected Response
        next_page_token = ""
        log_names_element = "logNamesElement-1079688374"
        log_names = [log_names_element]
        expected_response = {"next_page_token": next_page_token, "log_names": log_names}
        expected_response = logging_pb2.ListLogsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_logs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.log_names[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = logging_pb2.ListLogsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_logs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.LoggingServiceV2Client()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_logs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)
