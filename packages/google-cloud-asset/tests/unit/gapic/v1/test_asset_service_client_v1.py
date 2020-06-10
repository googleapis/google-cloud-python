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

from google.rpc import status_pb2

from google.cloud import asset_v1
from google.cloud.asset_v1.proto import asset_service_pb2
from google.cloud.asset_v1.proto import assets_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


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


class TestAssetServiceClient(object):
    def test_delete_feed(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        name = "name3373707"

        client.delete_feed(name)

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.DeleteFeedRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_feed_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup request
        name = "name3373707"

        with pytest.raises(CustomException):
            client.delete_feed(name)

    def test_export_assets(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = asset_service_pb2.ExportAssetsResponse(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_export_assets", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        parent = "parent-995424086"
        output_config = {}

        response = client.export_assets(parent, output_config)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.ExportAssetsRequest(
            parent=parent, output_config=output_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_export_assets_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_export_assets_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        parent = "parent-995424086"
        output_config = {}

        response = client.export_assets(parent, output_config)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_batch_get_assets_history(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = asset_service_pb2.BatchGetAssetsHistoryResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        parent = "parent-995424086"

        response = client.batch_get_assets_history(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.BatchGetAssetsHistoryRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_get_assets_history_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup request
        parent = "parent-995424086"

        with pytest.raises(CustomException):
            client.batch_get_assets_history(parent)

    def test_create_feed(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = asset_service_pb2.Feed(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        parent = "parent-995424086"
        feed_id = "feedId-976011428"
        feed = {}

        response = client.create_feed(parent, feed_id, feed)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.CreateFeedRequest(
            parent=parent, feed_id=feed_id, feed=feed
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_feed_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup request
        parent = "parent-995424086"
        feed_id = "feedId-976011428"
        feed = {}

        with pytest.raises(CustomException):
            client.create_feed(parent, feed_id, feed)

    def test_get_feed(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = asset_service_pb2.Feed(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        name = "name3373707"

        response = client.get_feed(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.GetFeedRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_feed_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup request
        name = "name3373707"

        with pytest.raises(CustomException):
            client.get_feed(name)

    def test_list_feeds(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = asset_service_pb2.ListFeedsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        parent = "parent-995424086"

        response = client.list_feeds(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.ListFeedsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_feeds_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup request
        parent = "parent-995424086"

        with pytest.raises(CustomException):
            client.list_feeds(parent)

    def test_update_feed(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = asset_service_pb2.Feed(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        feed = {}
        update_mask = {}

        response = client.update_feed(feed, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.UpdateFeedRequest(
            feed=feed, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_feed_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup request
        feed = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_feed(feed, update_mask)

    def test_search_all_resources(self):
        # Setup Expected Response
        next_page_token = ""
        results_element = {}
        results = [results_element]
        expected_response = {"next_page_token": next_page_token, "results": results}
        expected_response = asset_service_pb2.SearchAllResourcesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        scope = "scope109264468"

        paged_list_response = client.search_all_resources(scope)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.results[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.SearchAllResourcesRequest(scope=scope)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_all_resources_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup request
        scope = "scope109264468"

        paged_list_response = client.search_all_resources(scope)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_search_all_iam_policies(self):
        # Setup Expected Response
        next_page_token = ""
        results_element = {}
        results = [results_element]
        expected_response = {"next_page_token": next_page_token, "results": results}
        expected_response = asset_service_pb2.SearchAllIamPoliciesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup Request
        scope = "scope109264468"

        paged_list_response = client.search_all_iam_policies(scope)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.results[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = asset_service_pb2.SearchAllIamPoliciesRequest(scope=scope)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_all_iam_policies_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = asset_v1.AssetServiceClient()

        # Setup request
        scope = "scope109264468"

        paged_list_response = client.search_all_iam_policies(scope)
        with pytest.raises(CustomException):
            list(paged_list_response)
