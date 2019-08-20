# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.language_v1.types import language_service

from .transports.base import LanguageServiceTransport
from .transports.grpc import LanguageServiceGrpcTransport


class LanguageServiceMeta(type):
    """Metaclass for the LanguageService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[LanguageServiceTransport]]
    _transport_registry["grpc"] = LanguageServiceGrpcTransport

    def get_transport_class(cls, label: str = None) -> Type[LanguageServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class LanguageService(metaclass=LanguageServiceMeta):
    """Provides text analysis operations such as sentiment analysis
    and entity recognition.
    """

    def __init__(
        self,
        *,
        host: str = "language.googleapis.com",
        credentials: credentials.Credentials = None,
        transport: Union[str, LanguageServiceTransport] = None,
    ) -> None:
        """Instantiate the language service.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credential]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.LanguageServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
        """
        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, LanguageServiceTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(credentials=credentials, host=host)

    def analyze_sentiment(
        self,
        request: language_service.AnalyzeSentimentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeSentimentResponse:
        r"""Analyzes the sentiment of the provided text.

        Args:
            request (:class:`~.language_service.AnalyzeSentimentRequest`):
                The request object. The sentiment analysis request
                message.
            retry (~.retries.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.language_service.AnalyzeSentimentResponse:
                The sentiment analysis response message.
        """
        # Create or coerce a protobuf request object.
        request = language_service.AnalyzeSentimentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.analyze_sentiment,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def analyze_entities(
        self,
        request: language_service.AnalyzeEntitiesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeEntitiesResponse:
        r"""Finds named entities (currently proper names and
        common nouns) in the text along with entity types,
        salience, mentions for each entity, and other
        properties.

        Args:
            request (:class:`~.language_service.AnalyzeEntitiesRequest`):
                The request object. The entity analysis request message.
            retry (~.retries.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.language_service.AnalyzeEntitiesResponse:
                The entity analysis response message.
        """
        # Create or coerce a protobuf request object.
        request = language_service.AnalyzeEntitiesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.analyze_entities,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def analyze_entity_sentiment(
        self,
        request: language_service.AnalyzeEntitySentimentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeEntitySentimentResponse:
        r"""Finds entities, similar to
        [AnalyzeEntities][google.cloud.language.v1.LanguageService.AnalyzeEntities]
        in the text and analyzes sentiment associated with each entity
        and its mentions.

        Args:
            request (:class:`~.language_service.AnalyzeEntitySentimentRequest`):
                The request object. The entity-level sentiment analysis
                request message.
            retry (~.retries.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.language_service.AnalyzeEntitySentimentResponse:
                The entity-level sentiment analysis response message.
        """
        # Create or coerce a protobuf request object.
        request = language_service.AnalyzeEntitySentimentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.analyze_entity_sentiment,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def analyze_syntax(
        self,
        request: language_service.AnalyzeSyntaxRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeSyntaxResponse:
        r"""Analyzes the syntax of the text and provides sentence
        boundaries and tokenization along with part of speech
        tags, dependency trees, and other properties.

        Args:
            request (:class:`~.language_service.AnalyzeSyntaxRequest`):
                The request object. The syntax analysis request message.
            retry (~.retries.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.language_service.AnalyzeSyntaxResponse:
                The syntax analysis response message.
        """
        # Create or coerce a protobuf request object.
        request = language_service.AnalyzeSyntaxRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.analyze_syntax,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def classify_text(
        self,
        request: language_service.ClassifyTextRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.ClassifyTextResponse:
        r"""Classifies a document into categories.

        Args:
            request (:class:`~.language_service.ClassifyTextRequest`):
                The request object. The document classification request
                message.
            retry (~.retries.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.language_service.ClassifyTextResponse:
                The document classification response message.
        """
        # Create or coerce a protobuf request object.
        request = language_service.ClassifyTextRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.classify_text,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def annotate_text(
        self,
        request: language_service.AnnotateTextRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnnotateTextResponse:
        r"""A convenience method that provides all the features
        that analyzeSentiment, analyzeEntities, and
        analyzeSyntax provide in one call.

        Args:
            request (:class:`~.language_service.AnnotateTextRequest`):
                The request object. The request message for the text
                annotation API, which can perform multiple analysis
                types (sentiment, entities, and syntax) in one call.
            retry (~.retries.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.language_service.AnnotateTextResponse:
                The text annotations response message.
        """
        # Create or coerce a protobuf request object.
        request = language_service.AnnotateTextRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.annotate_text,
            default_retry=retries.Retry(
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable)
            ),
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-language").version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("LanguageService",)
