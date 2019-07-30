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

"""Accesses the google.cloud.language.v1beta2 LanguageService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import grpc

from google.cloud.language_v1beta2.gapic import enums
from google.cloud.language_v1beta2.gapic import language_service_client_config
from google.cloud.language_v1beta2.gapic.transports import (
    language_service_grpc_transport,
)
from google.cloud.language_v1beta2.proto import language_service_pb2
from google.cloud.language_v1beta2.proto import language_service_pb2_grpc


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-language").version


class LanguageServiceClient(object):
    """
    Provides text analysis operations such as sentiment analysis and entity
    recognition.
    """

    SERVICE_ADDRESS = "language.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.language.v1beta2.LanguageService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            LanguageServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.LanguageServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.LanguageServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = language_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=language_service_grpc_transport.LanguageServiceGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = language_service_grpc_transport.LanguageServiceGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def analyze_sentiment(
        self,
        document,
        encoding_type=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Analyzes the sentiment of the provided text.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> # TODO: Initialize `document`:
            >>> document = {}
            >>>
            >>> response = client.analyze_sentiment(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            encoding_type (~google.cloud.language_v1beta2.enums.EncodingType): The encoding type used by the API to calculate sentence offsets for the
                sentence sentiment.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnalyzeSentimentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "analyze_sentiment" not in self._inner_api_calls:
            self._inner_api_calls[
                "analyze_sentiment"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.analyze_sentiment,
                default_retry=self._method_configs["AnalyzeSentiment"].retry,
                default_timeout=self._method_configs["AnalyzeSentiment"].timeout,
                client_info=self._client_info,
            )

        request = language_service_pb2.AnalyzeSentimentRequest(
            document=document, encoding_type=encoding_type
        )
        return self._inner_api_calls["analyze_sentiment"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def analyze_entities(
        self,
        document,
        encoding_type=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Finds named entities (currently proper names and common nouns) in the text
        along with entity types, salience, mentions for each entity, and
        other properties.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> # TODO: Initialize `document`:
            >>> document = {}
            >>>
            >>> response = client.analyze_entities(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            encoding_type (~google.cloud.language_v1beta2.enums.EncodingType): The encoding type used by the API to calculate offsets.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnalyzeEntitiesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "analyze_entities" not in self._inner_api_calls:
            self._inner_api_calls[
                "analyze_entities"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.analyze_entities,
                default_retry=self._method_configs["AnalyzeEntities"].retry,
                default_timeout=self._method_configs["AnalyzeEntities"].timeout,
                client_info=self._client_info,
            )

        request = language_service_pb2.AnalyzeEntitiesRequest(
            document=document, encoding_type=encoding_type
        )
        return self._inner_api_calls["analyze_entities"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def analyze_entity_sentiment(
        self,
        document,
        encoding_type=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Finds entities, similar to ``AnalyzeEntities`` in the text and analyzes
        sentiment associated with each entity and its mentions.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> # TODO: Initialize `document`:
            >>> document = {}
            >>>
            >>> response = client.analyze_entity_sentiment(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            encoding_type (~google.cloud.language_v1beta2.enums.EncodingType): The encoding type used by the API to calculate offsets.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnalyzeEntitySentimentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "analyze_entity_sentiment" not in self._inner_api_calls:
            self._inner_api_calls[
                "analyze_entity_sentiment"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.analyze_entity_sentiment,
                default_retry=self._method_configs["AnalyzeEntitySentiment"].retry,
                default_timeout=self._method_configs["AnalyzeEntitySentiment"].timeout,
                client_info=self._client_info,
            )

        request = language_service_pb2.AnalyzeEntitySentimentRequest(
            document=document, encoding_type=encoding_type
        )
        return self._inner_api_calls["analyze_entity_sentiment"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def analyze_syntax(
        self,
        document,
        encoding_type=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Analyzes the syntax of the text and provides sentence boundaries and
        tokenization along with part of speech tags, dependency trees, and other
        properties.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> # TODO: Initialize `document`:
            >>> document = {}
            >>>
            >>> response = client.analyze_syntax(document)

        Args:
            document (Union[dict, ~google.cloud.language_v1beta2.types.Document]): Input document.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.language_v1beta2.types.Document`
            encoding_type (~google.cloud.language_v1beta2.enums.EncodingType): The encoding type used by the API to calculate offsets.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnalyzeSyntaxResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "analyze_syntax" not in self._inner_api_calls:
            self._inner_api_calls[
                "analyze_syntax"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.analyze_syntax,
                default_retry=self._method_configs["AnalyzeSyntax"].retry,
                default_timeout=self._method_configs["AnalyzeSyntax"].timeout,
                client_info=self._client_info,
            )

        request = language_service_pb2.AnalyzeSyntaxRequest(
            document=document, encoding_type=encoding_type
        )
        return self._inner_api_calls["analyze_syntax"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def classify_text(
        self,
        document,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Classifies a document into categories.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> # TODO: Initialize `document`:
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
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.ClassifyTextResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "classify_text" not in self._inner_api_calls:
            self._inner_api_calls[
                "classify_text"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.classify_text,
                default_retry=self._method_configs["ClassifyText"].retry,
                default_timeout=self._method_configs["ClassifyText"].timeout,
                client_info=self._client_info,
            )

        request = language_service_pb2.ClassifyTextRequest(document=document)
        return self._inner_api_calls["classify_text"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def annotate_text(
        self,
        document,
        features,
        encoding_type=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        A convenience method that provides all syntax, sentiment, entity, and
        classification features in one call.

        Example:
            >>> from google.cloud import language_v1beta2
            >>>
            >>> client = language_v1beta2.LanguageServiceClient()
            >>>
            >>> # TODO: Initialize `document`:
            >>> document = {}
            >>>
            >>> # TODO: Initialize `features`:
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
            encoding_type (~google.cloud.language_v1beta2.enums.EncodingType): The encoding type used by the API to calculate offsets.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.language_v1beta2.types.AnnotateTextResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "annotate_text" not in self._inner_api_calls:
            self._inner_api_calls[
                "annotate_text"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.annotate_text,
                default_retry=self._method_configs["AnnotateText"].retry,
                default_timeout=self._method_configs["AnnotateText"].timeout,
                client_info=self._client_info,
            )

        request = language_service_pb2.AnnotateTextRequest(
            document=document, features=features, encoding_type=encoding_type
        )
        return self._inner_api_calls["annotate_text"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
