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

from google.cloud.bigquery_storage_v1.gapic import big_query_read_client  # noqa
from google.cloud.bigquery_storage_v1.proto import storage_pb2
from google.cloud.bigquery_storage_v1.proto import stream_pb2


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

    def unary_stream(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestBigQueryReadClient(object):
    def test_create_read_session(self):
        # Setup Expected Response
        name = "name3373707"
        table = "table110115790"
        expected_response = {"name": name, "table": table}
        expected_response = stream_pb2.ReadSession(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_read_client.BigQueryReadClient()

        response = client.create_read_session()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = storage_pb2.CreateReadSessionRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_read_session_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_read_client.BigQueryReadClient()

        with pytest.raises(CustomException):
            client.create_read_session()

    def test_read_rows(self):
        # Setup Expected Response
        row_count = 1340416618
        expected_response = {"row_count": row_count}
        expected_response = storage_pb2.ReadRowsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_read_client.BigQueryReadClient()

        response = client.read_rows()
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = storage_pb2.ReadRowsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_read_rows_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_read_client.BigQueryReadClient()

        with pytest.raises(CustomException):
            client.read_rows()

    def test_split_read_stream(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = storage_pb2.SplitReadStreamResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_read_client.BigQueryReadClient()

        response = client.split_read_stream()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = storage_pb2.SplitReadStreamRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_split_read_stream_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_read_client.BigQueryReadClient()

        with pytest.raises(CustomException):
            client.split_read_stream()
