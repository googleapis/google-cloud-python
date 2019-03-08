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

from google.cloud import bigtable_v2
from google.cloud.bigtable_v2.proto import bigtable_pb2


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


class TestBigtableClient(object):
    def test_read_rows(self):
        # Setup Expected Response
        last_scanned_row_key = b"-126"
        expected_response = {"last_scanned_row_key": last_scanned_row_key}
        expected_response = bigtable_pb2.ReadRowsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup Request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        response = client.read_rows(table_name)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = bigtable_pb2.ReadRowsRequest(table_name=table_name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_read_rows_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        with pytest.raises(CustomException):
            client.read_rows(table_name)

    def test_sample_row_keys(self):
        # Setup Expected Response
        row_key = b"122"
        offset_bytes = 889884095
        expected_response = {"row_key": row_key, "offset_bytes": offset_bytes}
        expected_response = bigtable_pb2.SampleRowKeysResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup Request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        response = client.sample_row_keys(table_name)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = bigtable_pb2.SampleRowKeysRequest(table_name=table_name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_sample_row_keys_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        with pytest.raises(CustomException):
            client.sample_row_keys(table_name)

    def test_mutate_row(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = bigtable_pb2.MutateRowResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup Request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        row_key = b"122"
        mutations = []

        response = client.mutate_row(table_name, row_key, mutations)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_pb2.MutateRowRequest(
            table_name=table_name, row_key=row_key, mutations=mutations
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_mutate_row_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        row_key = b"122"
        mutations = []

        with pytest.raises(CustomException):
            client.mutate_row(table_name, row_key, mutations)

    def test_mutate_rows(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = bigtable_pb2.MutateRowsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup Request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        entries = []

        response = client.mutate_rows(table_name, entries)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        expected_request = bigtable_pb2.MutateRowsRequest(
            table_name=table_name, entries=entries
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_mutate_rows_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        entries = []

        with pytest.raises(CustomException):
            client.mutate_rows(table_name, entries)

    def test_check_and_mutate_row(self):
        # Setup Expected Response
        predicate_matched = True
        expected_response = {"predicate_matched": predicate_matched}
        expected_response = bigtable_pb2.CheckAndMutateRowResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup Request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        row_key = b"122"

        response = client.check_and_mutate_row(table_name, row_key)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_pb2.CheckAndMutateRowRequest(
            table_name=table_name, row_key=row_key
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_check_and_mutate_row_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        row_key = b"122"

        with pytest.raises(CustomException):
            client.check_and_mutate_row(table_name, row_key)

    def test_read_modify_write_row(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = bigtable_pb2.ReadModifyWriteRowResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup Request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        row_key = b"122"
        rules = []

        response = client.read_modify_write_row(table_name, row_key, rules)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_pb2.ReadModifyWriteRowRequest(
            table_name=table_name, row_key=row_key, rules=rules
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_read_modify_write_row_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_v2.BigtableClient()

        # Setup request
        table_name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        row_key = b"122"
        rules = []

        with pytest.raises(CustomException):
            client.read_modify_write_row(table_name, row_key, rules)
