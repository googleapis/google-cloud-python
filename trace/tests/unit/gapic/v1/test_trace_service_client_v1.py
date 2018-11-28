# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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

from google.cloud import trace_v1
from google.cloud.trace_v1.proto import trace_pb2
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


class TestTraceServiceClient(object):
    def test_patch_traces(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v1.TraceServiceClient()

        # Setup Request
        project_id = "projectId-1969970175"
        traces = {}

        client.patch_traces(project_id, traces)

        assert len(channel.requests) == 1
        expected_request = trace_pb2.PatchTracesRequest(
            project_id=project_id, traces=traces
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_patch_traces_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v1.TraceServiceClient()

        # Setup request
        project_id = "projectId-1969970175"
        traces = {}

        with pytest.raises(CustomException):
            client.patch_traces(project_id, traces)

    def test_get_trace(self):
        # Setup Expected Response
        project_id_2 = "projectId2939242356"
        trace_id_2 = "traceId2987826376"
        expected_response = {"project_id": project_id_2, "trace_id": trace_id_2}
        expected_response = trace_pb2.Trace(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v1.TraceServiceClient()

        # Setup Request
        project_id = "projectId-1969970175"
        trace_id = "traceId1270300245"

        response = client.get_trace(project_id, trace_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = trace_pb2.GetTraceRequest(
            project_id=project_id, trace_id=trace_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_trace_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v1.TraceServiceClient()

        # Setup request
        project_id = "projectId-1969970175"
        trace_id = "traceId1270300245"

        with pytest.raises(CustomException):
            client.get_trace(project_id, trace_id)

    def test_list_traces(self):
        # Setup Expected Response
        next_page_token = ""
        traces_element = {}
        traces = [traces_element]
        expected_response = {"next_page_token": next_page_token, "traces": traces}
        expected_response = trace_pb2.ListTracesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v1.TraceServiceClient()

        # Setup Request
        project_id = "projectId-1969970175"

        paged_list_response = client.list_traces(project_id)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.traces[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = trace_pb2.ListTracesRequest(project_id=project_id)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_traces_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v1.TraceServiceClient()

        # Setup request
        project_id = "projectId-1969970175"

        paged_list_response = client.list_traces(project_id)
        with pytest.raises(CustomException):
            list(paged_list_response)
