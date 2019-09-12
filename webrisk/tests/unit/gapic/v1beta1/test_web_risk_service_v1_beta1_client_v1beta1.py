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

from google.cloud import webrisk_v1beta1
from google.cloud.webrisk_v1beta1 import enums
from google.cloud.webrisk_v1beta1.proto import webrisk_pb2


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


class TestWebRiskServiceV1Beta1Client(object):
    def test_compute_threat_list_diff(self):
        # Setup Expected Response
        new_version_token = b"115"
        expected_response = {"new_version_token": new_version_token}
        expected_response = webrisk_pb2.ComputeThreatListDiffResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()

        # Setup Request
        threat_type = enums.ThreatType.THREAT_TYPE_UNSPECIFIED
        constraints = {}

        response = client.compute_threat_list_diff(threat_type, constraints)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = webrisk_pb2.ComputeThreatListDiffRequest(
            threat_type=threat_type, constraints=constraints
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_compute_threat_list_diff_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()

        # Setup request
        threat_type = enums.ThreatType.THREAT_TYPE_UNSPECIFIED
        constraints = {}

        with pytest.raises(CustomException):
            client.compute_threat_list_diff(threat_type, constraints)

    def test_search_uris(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = webrisk_pb2.SearchUrisResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()

        # Setup Request
        uri = "uri116076"
        threat_types = []

        response = client.search_uris(uri, threat_types)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = webrisk_pb2.SearchUrisRequest(
            uri=uri, threat_types=threat_types
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_uris_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()

        # Setup request
        uri = "uri116076"
        threat_types = []

        with pytest.raises(CustomException):
            client.search_uris(uri, threat_types)

    def test_search_hashes(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = webrisk_pb2.SearchHashesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()

        # Setup Request
        threat_types = []

        response = client.search_hashes(threat_types)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = webrisk_pb2.SearchHashesRequest(threat_types=threat_types)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_hashes_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()

        # Setup request
        threat_types = []

        with pytest.raises(CustomException):
            client.search_hashes(threat_types)
