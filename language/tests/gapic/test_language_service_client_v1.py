# Copyright 2017, Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests."""

import mock
import unittest

from google.gax import errors

from google.cloud.gapic.language.v1 import language_service_client
from google.cloud.proto.language.v1 import language_service_pb2


class CustomException(Exception):
    pass


class TestLanguageServiceClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_analyze_sentiment(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = language_service_client.LanguageServiceClient()

        # Mock request
        document = language_service_pb2.Document()

        # Mock response
        language = 'language-1613589672'
        expected_response = language_service_pb2.AnalyzeSentimentResponse(
            language=language)
        grpc_stub.AnalyzeSentiment.return_value = expected_response

        response = client.analyze_sentiment(document)
        self.assertEqual(expected_response, response)

        grpc_stub.AnalyzeSentiment.assert_called_once()
        args, kwargs = grpc_stub.AnalyzeSentiment.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = language_service_pb2.AnalyzeSentimentRequest(
            document=document)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_analyze_sentiment_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = language_service_client.LanguageServiceClient()

        # Mock request
        document = language_service_pb2.Document()

        # Mock exception response
        grpc_stub.AnalyzeSentiment.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.analyze_sentiment, document)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_analyze_entities(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = language_service_client.LanguageServiceClient()

        # Mock request
        document = language_service_pb2.Document()

        # Mock response
        language = 'language-1613589672'
        expected_response = language_service_pb2.AnalyzeEntitiesResponse(
            language=language)
        grpc_stub.AnalyzeEntities.return_value = expected_response

        response = client.analyze_entities(document)
        self.assertEqual(expected_response, response)

        grpc_stub.AnalyzeEntities.assert_called_once()
        args, kwargs = grpc_stub.AnalyzeEntities.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = language_service_pb2.AnalyzeEntitiesRequest(
            document=document)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_analyze_entities_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = language_service_client.LanguageServiceClient()

        # Mock request
        document = language_service_pb2.Document()

        # Mock exception response
        grpc_stub.AnalyzeEntities.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.analyze_entities, document)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_analyze_syntax(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = language_service_client.LanguageServiceClient()

        # Mock request
        document = language_service_pb2.Document()

        # Mock response
        language = 'language-1613589672'
        expected_response = language_service_pb2.AnalyzeSyntaxResponse(
            language=language)
        grpc_stub.AnalyzeSyntax.return_value = expected_response

        response = client.analyze_syntax(document)
        self.assertEqual(expected_response, response)

        grpc_stub.AnalyzeSyntax.assert_called_once()
        args, kwargs = grpc_stub.AnalyzeSyntax.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = language_service_pb2.AnalyzeSyntaxRequest(
            document=document)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_analyze_syntax_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = language_service_client.LanguageServiceClient()

        # Mock request
        document = language_service_pb2.Document()

        # Mock exception response
        grpc_stub.AnalyzeSyntax.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.analyze_syntax, document)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_annotate_text(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = language_service_client.LanguageServiceClient()

        # Mock request
        document = language_service_pb2.Document()
        features = language_service_pb2.AnnotateTextRequest.Features()

        # Mock response
        language = 'language-1613589672'
        expected_response = language_service_pb2.AnnotateTextResponse(
            language=language)
        grpc_stub.AnnotateText.return_value = expected_response

        response = client.annotate_text(document, features)
        self.assertEqual(expected_response, response)

        grpc_stub.AnnotateText.assert_called_once()
        args, kwargs = grpc_stub.AnnotateText.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = language_service_pb2.AnnotateTextRequest(
            document=document, features=features)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_annotate_text_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = language_service_client.LanguageServiceClient()

        # Mock request
        document = language_service_pb2.Document()
        features = language_service_pb2.AnnotateTextRequest.Features()

        # Mock exception response
        grpc_stub.AnnotateText.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.annotate_text, document,
                          features)
