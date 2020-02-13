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

from google.cloud import videointelligence_v1p3beta1
from google.cloud.videointelligence_v1p3beta1.proto import video_intelligence_pb2


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

    def stream_stream(
        self, method, request_serializer=None, response_deserializer=None
    ):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestStreamingVideoIntelligenceServiceClient(object):
    def test_streaming_annotate_video(self):
        # Setup Expected Response
        annotation_results_uri = "annotationResultsUri-238075757"
        expected_response = {"annotation_results_uri": annotation_results_uri}
        expected_response = video_intelligence_pb2.StreamingAnnotateVideoResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = (
                videointelligence_v1p3beta1.StreamingVideoIntelligenceServiceClient()
            )

        # Setup Request
        request = {}
        request = video_intelligence_pb2.StreamingAnnotateVideoRequest(**request)
        requests = [request]

        response = client.streaming_annotate_video(requests)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        actual_requests = channel.requests[0][1]
        assert len(actual_requests) == 1
        actual_request = list(actual_requests)[0]
        assert request == actual_request

    def test_streaming_annotate_video_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = (
                videointelligence_v1p3beta1.StreamingVideoIntelligenceServiceClient()
            )

        # Setup request
        request = {}

        request = video_intelligence_pb2.StreamingAnnotateVideoRequest(**request)
        requests = [request]

        with pytest.raises(CustomException):
            client.streaming_annotate_video(requests)
