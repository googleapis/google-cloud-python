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

from google.cloud import recommender_v1
from google.cloud.recommender_v1.proto import recommendation_pb2
from google.cloud.recommender_v1.proto import recommender_service_pb2


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


class TestRecommenderClient(object):
    def test_list_recommendations(self):
        # Setup Expected Response
        next_page_token = ""
        recommendations_element = {}
        recommendations = [recommendations_element]
        expected_response = {
            "next_page_token": next_page_token,
            "recommendations": recommendations,
        }
        expected_response = recommender_service_pb2.ListRecommendationsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup Request
        parent = client.recommender_path("[PROJECT]", "[LOCATION]", "[RECOMMENDER]")

        paged_list_response = client.list_recommendations(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.recommendations[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = recommender_service_pb2.ListRecommendationsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_recommendations_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup request
        parent = client.recommender_path("[PROJECT]", "[LOCATION]", "[RECOMMENDER]")

        paged_list_response = client.list_recommendations(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_recommendation(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        recommender_subtype = "recommenderSubtype-1488504412"
        etag = "etag3123477"
        expected_response = {
            "name": name_2,
            "description": description,
            "recommender_subtype": recommender_subtype,
            "etag": etag,
        }
        expected_response = recommendation_pb2.Recommendation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup Request
        name = client.recommendation_path(
            "[PROJECT]", "[LOCATION]", "[RECOMMENDER]", "[RECOMMENDATION]"
        )

        response = client.get_recommendation(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = recommender_service_pb2.GetRecommendationRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_recommendation_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup request
        name = client.recommendation_path(
            "[PROJECT]", "[LOCATION]", "[RECOMMENDER]", "[RECOMMENDATION]"
        )

        with pytest.raises(CustomException):
            client.get_recommendation(name)

    def test_mark_recommendation_claimed(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        recommender_subtype = "recommenderSubtype-1488504412"
        etag_2 = "etag2-1293302904"
        expected_response = {
            "name": name_2,
            "description": description,
            "recommender_subtype": recommender_subtype,
            "etag": etag_2,
        }
        expected_response = recommendation_pb2.Recommendation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup Request
        name = client.recommendation_path(
            "[PROJECT]", "[LOCATION]", "[RECOMMENDER]", "[RECOMMENDATION]"
        )
        etag = "etag3123477"

        response = client.mark_recommendation_claimed(name, etag)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = recommender_service_pb2.MarkRecommendationClaimedRequest(
            name=name, etag=etag
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_mark_recommendation_claimed_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup request
        name = client.recommendation_path(
            "[PROJECT]", "[LOCATION]", "[RECOMMENDER]", "[RECOMMENDATION]"
        )
        etag = "etag3123477"

        with pytest.raises(CustomException):
            client.mark_recommendation_claimed(name, etag)

    def test_mark_recommendation_succeeded(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        recommender_subtype = "recommenderSubtype-1488504412"
        etag_2 = "etag2-1293302904"
        expected_response = {
            "name": name_2,
            "description": description,
            "recommender_subtype": recommender_subtype,
            "etag": etag_2,
        }
        expected_response = recommendation_pb2.Recommendation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup Request
        name = client.recommendation_path(
            "[PROJECT]", "[LOCATION]", "[RECOMMENDER]", "[RECOMMENDATION]"
        )
        etag = "etag3123477"

        response = client.mark_recommendation_succeeded(name, etag)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = recommender_service_pb2.MarkRecommendationSucceededRequest(
            name=name, etag=etag
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_mark_recommendation_succeeded_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup request
        name = client.recommendation_path(
            "[PROJECT]", "[LOCATION]", "[RECOMMENDER]", "[RECOMMENDATION]"
        )
        etag = "etag3123477"

        with pytest.raises(CustomException):
            client.mark_recommendation_succeeded(name, etag)

    def test_mark_recommendation_failed(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        description = "description-1724546052"
        recommender_subtype = "recommenderSubtype-1488504412"
        etag_2 = "etag2-1293302904"
        expected_response = {
            "name": name_2,
            "description": description,
            "recommender_subtype": recommender_subtype,
            "etag": etag_2,
        }
        expected_response = recommendation_pb2.Recommendation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup Request
        name = client.recommendation_path(
            "[PROJECT]", "[LOCATION]", "[RECOMMENDER]", "[RECOMMENDATION]"
        )
        etag = "etag3123477"

        response = client.mark_recommendation_failed(name, etag)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = recommender_service_pb2.MarkRecommendationFailedRequest(
            name=name, etag=etag
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_mark_recommendation_failed_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recommender_v1.RecommenderClient()

        # Setup request
        name = client.recommendation_path(
            "[PROJECT]", "[LOCATION]", "[RECOMMENDER]", "[RECOMMENDATION]"
        )
        etag = "etag3123477"

        with pytest.raises(CustomException):
            client.mark_recommendation_failed(name, etag)
