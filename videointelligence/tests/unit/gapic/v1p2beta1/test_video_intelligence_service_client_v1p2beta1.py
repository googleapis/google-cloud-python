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

from google.rpc import status_pb2

from google.cloud import videointelligence_v1p2beta1
from google.cloud.videointelligence_v1p2beta1 import enums
from google.cloud.videointelligence_v1p2beta1.proto import video_intelligence_pb2
from google.longrunning import operations_pb2


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


class TestVideoIntelligenceServiceClient(object):
    def test_annotate_video(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = video_intelligence_pb2.AnnotateVideoResponse(
            **expected_response
        )
        operation = operations_pb2.Operation(
            name="operations/test_annotate_video", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = videointelligence_v1p2beta1.VideoIntelligenceServiceClient()

        # Setup Request
        input_uri = "gs://demomaker/cat.mp4"
        features_element = enums.Feature.LABEL_DETECTION
        features = [features_element]

        response = client.annotate_video(input_uri=input_uri, features=features)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = video_intelligence_pb2.AnnotateVideoRequest(
            input_uri=input_uri, features=features
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_annotate_video_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_annotate_video_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = videointelligence_v1p2beta1.VideoIntelligenceServiceClient()

        # Setup Request
        input_uri = "gs://demomaker/cat.mp4"
        features_element = enums.Feature.LABEL_DETECTION
        features = [features_element]

        response = client.annotate_video(input_uri=input_uri, features=features)
        exception = response.exception()
        assert exception.errors[0] == error
