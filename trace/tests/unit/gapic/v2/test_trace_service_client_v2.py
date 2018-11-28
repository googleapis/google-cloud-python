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

from google.cloud import trace_v2
from google.cloud.trace_v2.proto import trace_pb2
from google.cloud.trace_v2.proto import tracing_pb2
from google.protobuf import empty_pb2
from google.protobuf import timestamp_pb2


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
    def test_batch_write_spans(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v2.TraceServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")
        spans = []

        client.batch_write_spans(name, spans)

        assert len(channel.requests) == 1
        expected_request = tracing_pb2.BatchWriteSpansRequest(name=name, spans=spans)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_write_spans_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v2.TraceServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")
        spans = []

        with pytest.raises(CustomException):
            client.batch_write_spans(name, spans)

    def test_create_span(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        span_id_2 = "spanId2-643891741"
        parent_span_id = "parentSpanId-1757797477"
        expected_response = {
            "name": name_2,
            "span_id": span_id_2,
            "parent_span_id": parent_span_id,
        }
        expected_response = trace_pb2.Span(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v2.TraceServiceClient()

        # Setup Request
        name = client.span_path("[PROJECT]", "[TRACE]", "[SPAN]")
        span_id = "spanId-2011840976"
        display_name = {}
        start_time = {}
        end_time = {}

        response = client.create_span(name, span_id, display_name, start_time, end_time)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = trace_pb2.Span(
            name=name,
            span_id=span_id,
            display_name=display_name,
            start_time=start_time,
            end_time=end_time,
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_span_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = trace_v2.TraceServiceClient()

        # Setup request
        name = client.span_path("[PROJECT]", "[TRACE]", "[SPAN]")
        span_id = "spanId-2011840976"
        display_name = {}
        start_time = {}
        end_time = {}

        with pytest.raises(CustomException):
            client.create_span(name, span_id, display_name, start_time, end_time)
