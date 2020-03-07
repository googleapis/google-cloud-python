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

from google.cloud import asset_v1p1beta1
from google.cloud.asset_v1p1beta1.proto import asset_service_pb2
from google.cloud.asset_v1p1beta1.proto import assets_pb2


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
            client = asset_v1p1beta1.AssetServiceClient()

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
            client = asset_v1p1beta1.AssetServiceClient()

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
            client = asset_v1p1beta1.AssetServiceClient()

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
            client = asset_v1p1beta1.AssetServiceClient()

        # Setup request
        scope = "scope109264468"

        paged_list_response = client.search_all_iam_policies(scope)
        with pytest.raises(CustomException):
            list(paged_list_response)
