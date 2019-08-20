# -*- coding: utf-8 -*-
from typing import Callable, Dict, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.auth import credentials  # type: ignore

import grpc  # type: ignore

from google.cloud.language_v1.types import language_service

from .base import LanguageServiceTransport


class LanguageServiceGrpcTransport(LanguageServiceTransport):
    """gRPC backend transport for LanguageService.

    Provides text analysis operations such as sentiment analysis
    and entity recognition.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "language.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
        """
        # Sanity check: Ensure that channel and credentials are not both
        # provided.
        if channel:
            credentials = False

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

        # If a channel was explicitly provided, set it.
        if channel:
            self._grpc_channel = channel

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = grpc_helpers.create_channel(
                self._host, credentials=self._credentials, scopes=self.AUTH_SCOPES
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def analyze_sentiment(
        self
    ) -> Callable[
        [language_service.AnalyzeSentimentRequest],
        language_service.AnalyzeSentimentResponse,
    ]:
        r"""Return a callable for the analyze sentiment method over gRPC.

        Analyzes the sentiment of the provided text.

        Returns:
            Callable[[~.AnalyzeSentimentRequest],
                    ~.AnalyzeSentimentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_sentiment" not in self._stubs:
            self._stubs["analyze_sentiment"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnalyzeSentiment",
                request_serializer=language_service.AnalyzeSentimentRequest.serialize,
                response_deserializer=language_service.AnalyzeSentimentResponse.deserialize,
            )
        return self._stubs["analyze_sentiment"]

    @property
    def analyze_entities(
        self
    ) -> Callable[
        [language_service.AnalyzeEntitiesRequest],
        language_service.AnalyzeEntitiesResponse,
    ]:
        r"""Return a callable for the analyze entities method over gRPC.

        Finds named entities (currently proper names and
        common nouns) in the text along with entity types,
        salience, mentions for each entity, and other
        properties.

        Returns:
            Callable[[~.AnalyzeEntitiesRequest],
                    ~.AnalyzeEntitiesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_entities" not in self._stubs:
            self._stubs["analyze_entities"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnalyzeEntities",
                request_serializer=language_service.AnalyzeEntitiesRequest.serialize,
                response_deserializer=language_service.AnalyzeEntitiesResponse.deserialize,
            )
        return self._stubs["analyze_entities"]

    @property
    def analyze_entity_sentiment(
        self
    ) -> Callable[
        [language_service.AnalyzeEntitySentimentRequest],
        language_service.AnalyzeEntitySentimentResponse,
    ]:
        r"""Return a callable for the analyze entity sentiment method over gRPC.

        Finds entities, similar to
        [AnalyzeEntities][google.cloud.language.v1.LanguageService.AnalyzeEntities]
        in the text and analyzes sentiment associated with each entity
        and its mentions.

        Returns:
            Callable[[~.AnalyzeEntitySentimentRequest],
                    ~.AnalyzeEntitySentimentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_entity_sentiment" not in self._stubs:
            self._stubs["analyze_entity_sentiment"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnalyzeEntitySentiment",
                request_serializer=language_service.AnalyzeEntitySentimentRequest.serialize,
                response_deserializer=language_service.AnalyzeEntitySentimentResponse.deserialize,
            )
        return self._stubs["analyze_entity_sentiment"]

    @property
    def analyze_syntax(
        self
    ) -> Callable[
        [language_service.AnalyzeSyntaxRequest], language_service.AnalyzeSyntaxResponse
    ]:
        r"""Return a callable for the analyze syntax method over gRPC.

        Analyzes the syntax of the text and provides sentence
        boundaries and tokenization along with part of speech
        tags, dependency trees, and other properties.

        Returns:
            Callable[[~.AnalyzeSyntaxRequest],
                    ~.AnalyzeSyntaxResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_syntax" not in self._stubs:
            self._stubs["analyze_syntax"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnalyzeSyntax",
                request_serializer=language_service.AnalyzeSyntaxRequest.serialize,
                response_deserializer=language_service.AnalyzeSyntaxResponse.deserialize,
            )
        return self._stubs["analyze_syntax"]

    @property
    def classify_text(
        self
    ) -> Callable[
        [language_service.ClassifyTextRequest], language_service.ClassifyTextResponse
    ]:
        r"""Return a callable for the classify text method over gRPC.

        Classifies a document into categories.

        Returns:
            Callable[[~.ClassifyTextRequest],
                    ~.ClassifyTextResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "classify_text" not in self._stubs:
            self._stubs["classify_text"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/ClassifyText",
                request_serializer=language_service.ClassifyTextRequest.serialize,
                response_deserializer=language_service.ClassifyTextResponse.deserialize,
            )
        return self._stubs["classify_text"]

    @property
    def annotate_text(
        self
    ) -> Callable[
        [language_service.AnnotateTextRequest], language_service.AnnotateTextResponse
    ]:
        r"""Return a callable for the annotate text method over gRPC.

        A convenience method that provides all the features
        that analyzeSentiment, analyzeEntities, and
        analyzeSyntax provide in one call.

        Returns:
            Callable[[~.AnnotateTextRequest],
                    ~.AnnotateTextResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "annotate_text" not in self._stubs:
            self._stubs["annotate_text"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnnotateText",
                request_serializer=language_service.AnnotateTextRequest.serialize,
                response_deserializer=language_service.AnnotateTextResponse.deserialize,
            )
        return self._stubs["annotate_text"]


__all__ = ("LanguageServiceGrpcTransport",)
