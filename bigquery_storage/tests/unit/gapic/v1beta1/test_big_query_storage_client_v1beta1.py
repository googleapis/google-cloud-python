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

from google.cloud.bigquery_storage_v1beta1.gapic import big_query_storage_client  # noqa
from google.cloud.bigquery_storage_v1beta1.proto import storage_pb2
from google.cloud.bigquery_storage_v1beta1.proto import table_reference_pb2
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

    def unary_stream(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestBigQueryStorageClient(object):
    def test_create_read_session(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = storage_pb2.ReadSession(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup Request
        table_reference = {}
        parent = "parent-995424086"

        response = client.create_read_session(table_reference, parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = storage_pb2.CreateReadSessionRequest(
            table_reference=table_reference, parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_read_session_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup request
        table_reference = {}
        parent = "parent-995424086"

        with pytest.raises(CustomException):
            client.create_read_session(table_reference, parent)

    def test_read_rows(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = storage_pb2.ReadRowsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup Request
        read_position = {}

        response = client.read_rows(read_position)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = storage_pb2.ReadRowsRequest(read_position=read_position)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_read_rows_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup request
        read_position = {}

        with pytest.raises(CustomException):
            client.read_rows(read_position)

    def test_batch_create_read_session_streams(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = storage_pb2.BatchCreateReadSessionStreamsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup Request
        session = {}
        requested_streams = 1017221410

        response = client.batch_create_read_session_streams(session, requested_streams)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = storage_pb2.BatchCreateReadSessionStreamsRequest(
            session=session, requested_streams=requested_streams
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_create_read_session_streams_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup request
        session = {}
        requested_streams = 1017221410

        with pytest.raises(CustomException):
            client.batch_create_read_session_streams(session, requested_streams)

    def test_finalize_stream(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup Request
        stream = {}

        client.finalize_stream(stream)

        assert len(channel.requests) == 1
        expected_request = storage_pb2.FinalizeStreamRequest(stream=stream)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_finalize_stream_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup request
        stream = {}

        with pytest.raises(CustomException):
            client.finalize_stream(stream)

    def test_split_read_stream(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = storage_pb2.SplitReadStreamResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup Request
        original_stream = {}

        response = client.split_read_stream(original_stream)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = storage_pb2.SplitReadStreamRequest(
            original_stream=original_stream
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_split_read_stream_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = big_query_storage_client.BigQueryStorageClient()

        # Setup request
        original_stream = {}

        with pytest.raises(CustomException):
            client.split_read_stream(original_stream)
