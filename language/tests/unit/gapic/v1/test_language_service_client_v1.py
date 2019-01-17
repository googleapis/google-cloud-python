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

from google.cloud import language_v1
from google.cloud.language_v1.proto import language_service_pb2


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


class TestLanguageServiceClient(object):
    def test_analyze_sentiment(self):
        # Setup Expected Response
        language = "language-1613589672"
        expected_response = {"language": language}
        expected_response = language_service_pb2.AnalyzeSentimentResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup Request
        document = {}

        response = client.analyze_sentiment(document)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = language_service_pb2.AnalyzeSentimentRequest(
            document=document
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_analyze_sentiment_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup request
        document = {}

        with pytest.raises(CustomException):
            client.analyze_sentiment(document)

    def test_analyze_entities(self):
        # Setup Expected Response
        language = "language-1613589672"
        expected_response = {"language": language}
        expected_response = language_service_pb2.AnalyzeEntitiesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup Request
        document = {}

        response = client.analyze_entities(document)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = language_service_pb2.AnalyzeEntitiesRequest(
            document=document
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_analyze_entities_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup request
        document = {}

        with pytest.raises(CustomException):
            client.analyze_entities(document)

    def test_analyze_entity_sentiment(self):
        # Setup Expected Response
        language = "language-1613589672"
        expected_response = {"language": language}
        expected_response = language_service_pb2.AnalyzeEntitySentimentResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup Request
        document = {}

        response = client.analyze_entity_sentiment(document)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = language_service_pb2.AnalyzeEntitySentimentRequest(
            document=document
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_analyze_entity_sentiment_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup request
        document = {}

        with pytest.raises(CustomException):
            client.analyze_entity_sentiment(document)

    def test_analyze_syntax(self):
        # Setup Expected Response
        language = "language-1613589672"
        expected_response = {"language": language}
        expected_response = language_service_pb2.AnalyzeSyntaxResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup Request
        document = {}

        response = client.analyze_syntax(document)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = language_service_pb2.AnalyzeSyntaxRequest(document=document)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_analyze_syntax_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup request
        document = {}

        with pytest.raises(CustomException):
            client.analyze_syntax(document)

    def test_classify_text(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = language_service_pb2.ClassifyTextResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup Request
        document = {}

        response = client.classify_text(document)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = language_service_pb2.ClassifyTextRequest(document=document)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_classify_text_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup request
        document = {}

        with pytest.raises(CustomException):
            client.classify_text(document)

    def test_annotate_text(self):
        # Setup Expected Response
        language = "language-1613589672"
        expected_response = {"language": language}
        expected_response = language_service_pb2.AnnotateTextResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup Request
        document = {}
        features = {}

        response = client.annotate_text(document, features)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = language_service_pb2.AnnotateTextRequest(
            document=document, features=features
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_annotate_text_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = language_v1.LanguageServiceClient()

        # Setup request
        document = {}
        features = {}

        with pytest.raises(CustomException):
            client.annotate_text(document, features)
