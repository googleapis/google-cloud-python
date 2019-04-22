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

from google.cloud import recaptchaenterprise_v1beta1
from google.cloud.recaptchaenterprise_v1beta1 import enums
from google.cloud.recaptchaenterprise_v1beta1.proto import recaptchaenterprise_pb2


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


class TestRecaptchaEnterpriseServiceClient(object):
    def test_create_assessment(self):
        # Setup Expected Response
        name = "name3373707"
        score = 1.0926453e7
        expected_response = {"name": name, "score": score}
        expected_response = recaptchaenterprise_pb2.Assessment(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recaptchaenterprise_v1beta1.RecaptchaEnterpriseServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        assessment = {}

        response = client.create_assessment(parent, assessment)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = recaptchaenterprise_pb2.CreateAssessmentRequest(
            parent=parent, assessment=assessment
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_assessment_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recaptchaenterprise_v1beta1.RecaptchaEnterpriseServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        assessment = {}

        with pytest.raises(CustomException):
            client.create_assessment(parent, assessment)

    def test_annotate_assessment(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = recaptchaenterprise_pb2.AnnotateAssessmentResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recaptchaenterprise_v1beta1.RecaptchaEnterpriseServiceClient()

        # Setup Request
        name = client.assessment_path("[PROJECT]", "[ASSESSMENT]")
        annotation = enums.AnnotateAssessmentRequest.Annotation.ANNOTATION_UNSPECIFIED

        response = client.annotate_assessment(name, annotation)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = recaptchaenterprise_pb2.AnnotateAssessmentRequest(
            name=name, annotation=annotation
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_annotate_assessment_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = recaptchaenterprise_v1beta1.RecaptchaEnterpriseServiceClient()

        # Setup request
        name = client.assessment_path("[PROJECT]", "[ASSESSMENT]")
        annotation = enums.AnnotateAssessmentRequest.Annotation.ANNOTATION_UNSPECIFIED

        with pytest.raises(CustomException):
            client.annotate_assessment(name, annotation)
