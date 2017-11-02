# Copyright 2017, Google LLC All rights reserved.
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
#
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/cloud/language/v1beta2/language_service.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.cloud.language.v1beta2 LanguageService API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers

from google.cloud.language_v1beta2.gapic import enums
from google.cloud.language_v1beta2.gapic import language_service_client_config
from google.cloud.language_v1beta2.proto import language_service_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-language', ).version


class LanguageServiceClient(object):
    """
    Provides text analysis operations such as sentiment analysis and entity
    recognition.
    """

    SERVICE_ADDRESS = 'language.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = ('google.cloud.language.v1beta2.LanguageService')

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=language_service_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. If specified, then the ``credentials``
                argument is ignored.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict):
                A dictionary of call options for each method. If not specified
                the default configuration is used. Generally, you only need
                to set this if you're developing your own client library.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        if channel is not None and credentials is not None:
            raise ValueError(
                'channel and credentials arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__))

        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES)

        self.language_service_stub = (
            language_service_pb2.LanguageServiceStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)

        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._analyze_sentiment = google.api_core.gapic_v1.method.wrap_method(
            self.language_service_stub.AnalyzeSentiment,
            default_retry=method_configs['AnalyzeSentiment'].retry,
            default_timeout=method_configs['AnalyzeSentiment'].timeout,
            client_info=client_info)
        self._analyze_entities = google.api_core.gapic_v1.method.wrap_method(
            self.language_service_stub.AnalyzeEntities,
            default_retry=method_configs['AnalyzeEntities'].retry,
            default_timeout=method_configs['AnalyzeEntities'].timeout,
            client_info=client_info)
        self._analyze_entity_sentiment = google.api_core.gapic_v1.method.wrap_method(
            self.language_service_stub.AnalyzeEntitySentiment,
            default_retry=method_configs['AnalyzeEntitySentiment'].retry,
            default_timeout=method_configs['AnalyzeEntitySentiment'].timeout,
            client_info=client_info)
        self._analyze_syntax = google.api_core.gapic_v1.method.wrap_method(
            self.language_service_stub.AnalyzeSyntax,
            default_retry=method_configs['AnalyzeSyntax'].retry,
            default_timeout=method_configs['AnalyzeSyntax'].timeout,
            client_info=client_info)
        self._classify_text = google.api_core.gapic_v1.method.wrap_method(
            self.language_service_stub.ClassifyText,
            default_retry=method_configs['ClassifyText'].retry,
            default_timeout=method_configs['ClassifyText'].timeout,
            client_info=client_info)
        self._annotate_text = google.api_core.gapic_v1.method.wrap_method(
            self.language_service_stub.AnnotateText,
            default_retry=method_configs['AnnotateText'].retry,
            default_timeout=method_configs['AnnotateText'].timeout,
            client_info=client_info)

    # Service calls
    def analyze_sentiment(self,
                          document,
                          encoding_type=None,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Analyzes the sentiment of the provided text.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> document = {}
            >>>
            >>> response = client.analyze_sentiment(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            encoding_type (~google.cloud.language_v1beta2.types.EncodingType): The encoding type used by the API to calculate sentence offsets for the
                sentence sentiment.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnalyzeSentimentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = language_service_pb2.AnalyzeSentimentRequest(
            document=document, encoding_type=encoding_type)
        return self._analyze_sentiment(request, retry=retry, timeout=timeout)

    def analyze_entities(self,
                         document,
                         encoding_type=None,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Finds named entities (currently proper names and common nouns) in the text
        along with entity types, salience, mentions for each entity, and
        other properties.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> document = {}
            >>>
            >>> response = client.analyze_entities(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            encoding_type (~google.cloud.language_v1beta2.types.EncodingType): The encoding type used by the API to calculate offsets.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnalyzeEntitiesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = language_service_pb2.AnalyzeEntitiesRequest(
            document=document, encoding_type=encoding_type)
        return self._analyze_entities(request, retry=retry, timeout=timeout)

    def analyze_entity_sentiment(
            self,
            document,
            encoding_type=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Finds entities, similar to ``AnalyzeEntities`` in the text and analyzes
        sentiment associated with each entity and its mentions.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> document = {}
            >>>
            >>> response = client.analyze_entity_sentiment(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            encoding_type (~google.cloud.language_v1beta2.types.EncodingType): The encoding type used by the API to calculate offsets.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnalyzeEntitySentimentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = language_service_pb2.AnalyzeEntitySentimentRequest(
            document=document, encoding_type=encoding_type)
        return self._analyze_entity_sentiment(
            request, retry=retry, timeout=timeout)

    def analyze_syntax(self,
                       document,
                       encoding_type=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Analyzes the syntax of the text and provides sentence boundaries and
        tokenization along with part of speech tags, dependency trees, and other
        properties.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> document = {}
            >>>
            >>> response = client.analyze_syntax(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            encoding_type (~google.cloud.language_v1beta2.types.EncodingType): The encoding type used by the API to calculate offsets.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnalyzeSyntaxResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = language_service_pb2.AnalyzeSyntaxRequest(
            document=document, encoding_type=encoding_type)
        return self._analyze_syntax(request, retry=retry, timeout=timeout)

    def classify_text(self,
                      document,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Classifies a document into categories.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> document = {}
            >>>
            >>> response = client.classify_text(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.ClassifyTextResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = language_service_pb2.ClassifyTextRequest(document=document)
        return self._classify_text(request, retry=retry, timeout=timeout)

    def annotate_text(self,
                      document,
                      features,
                      encoding_type=None,
                      retry=google.api_core.gapic_v1.method.DEFAULT,
                      timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        A convenience method that provides all syntax, sentiment, entity, and
        classification features in one call.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> document = {}
            >>> features = {}
            >>>
            >>> response = client.annotate_text(document, features)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            features (Union[dict, ~google.cloud.language_v1beta2.types.Features]): The enabled features.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Features`
            encoding_type (~google.cloud.language_v1beta2.types.EncodingType): The encoding type used by the API to calculate offsets.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnnotateTextResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = language_service_pb2.AnnotateTextRequest(
            document=document, features=features, encoding_type=encoding_type)
        return self._annotate_text(request, retry=retry, timeout=timeout)
