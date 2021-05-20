# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.language_v1beta2.types import language_service
from .transports.base import LanguageServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import LanguageServiceGrpcAsyncIOTransport
from .client import LanguageServiceClient


class LanguageServiceAsyncClient:
    """Provides text analysis operations such as sentiment analysis
    and entity recognition.
    """

    _client: LanguageServiceClient

    DEFAULT_ENDPOINT = LanguageServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = LanguageServiceClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        LanguageServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        LanguageServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(LanguageServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        LanguageServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        LanguageServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        LanguageServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(LanguageServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        LanguageServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(LanguageServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        LanguageServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            LanguageServiceAsyncClient: The constructed client.
        """
        return LanguageServiceClient.from_service_account_info.__func__(LanguageServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            LanguageServiceAsyncClient: The constructed client.
        """
        return LanguageServiceClient.from_service_account_file.__func__(LanguageServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> LanguageServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            LanguageServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(LanguageServiceClient).get_transport_class, type(LanguageServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, LanguageServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the language service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.LanguageServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = LanguageServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def analyze_sentiment(
        self,
        request: language_service.AnalyzeSentimentRequest = None,
        *,
        document: language_service.Document = None,
        encoding_type: language_service.EncodingType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeSentimentResponse:
        r"""Analyzes the sentiment of the provided text.

        Args:
            request (:class:`google.cloud.language_v1beta2.types.AnalyzeSentimentRequest`):
                The request object. The sentiment analysis request
                message.
            document (:class:`google.cloud.language_v1beta2.types.Document`):
                Required. Input document.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            encoding_type (:class:`google.cloud.language_v1beta2.types.EncodingType`):
                The encoding type used by the API to
                calculate sentence offsets for the
                sentence sentiment.

                This corresponds to the ``encoding_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.language_v1beta2.types.AnalyzeSentimentResponse:
                The sentiment analysis response
                message.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([document, encoding_type])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = language_service.AnalyzeSentimentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if document is not None:
            request.document = document
        if encoding_type is not None:
            request.encoding_type = encoding_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.analyze_sentiment,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def analyze_entities(
        self,
        request: language_service.AnalyzeEntitiesRequest = None,
        *,
        document: language_service.Document = None,
        encoding_type: language_service.EncodingType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeEntitiesResponse:
        r"""Finds named entities (currently proper names and
        common nouns) in the text along with entity types,
        salience, mentions for each entity, and other
        properties.

        Args:
            request (:class:`google.cloud.language_v1beta2.types.AnalyzeEntitiesRequest`):
                The request object. The entity analysis request message.
            document (:class:`google.cloud.language_v1beta2.types.Document`):
                Required. Input document.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            encoding_type (:class:`google.cloud.language_v1beta2.types.EncodingType`):
                The encoding type used by the API to
                calculate offsets.

                This corresponds to the ``encoding_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.language_v1beta2.types.AnalyzeEntitiesResponse:
                The entity analysis response message.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([document, encoding_type])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = language_service.AnalyzeEntitiesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if document is not None:
            request.document = document
        if encoding_type is not None:
            request.encoding_type = encoding_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.analyze_entities,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def analyze_entity_sentiment(
        self,
        request: language_service.AnalyzeEntitySentimentRequest = None,
        *,
        document: language_service.Document = None,
        encoding_type: language_service.EncodingType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeEntitySentimentResponse:
        r"""Finds entities, similar to
        [AnalyzeEntities][google.cloud.language.v1beta2.LanguageService.AnalyzeEntities]
        in the text and analyzes sentiment associated with each entity
        and its mentions.

        Args:
            request (:class:`google.cloud.language_v1beta2.types.AnalyzeEntitySentimentRequest`):
                The request object. The entity-level sentiment analysis
                request message.
            document (:class:`google.cloud.language_v1beta2.types.Document`):
                Required. Input document.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            encoding_type (:class:`google.cloud.language_v1beta2.types.EncodingType`):
                The encoding type used by the API to
                calculate offsets.

                This corresponds to the ``encoding_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.language_v1beta2.types.AnalyzeEntitySentimentResponse:
                The entity-level sentiment analysis
                response message.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([document, encoding_type])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = language_service.AnalyzeEntitySentimentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if document is not None:
            request.document = document
        if encoding_type is not None:
            request.encoding_type = encoding_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.analyze_entity_sentiment,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def analyze_syntax(
        self,
        request: language_service.AnalyzeSyntaxRequest = None,
        *,
        document: language_service.Document = None,
        encoding_type: language_service.EncodingType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeSyntaxResponse:
        r"""Analyzes the syntax of the text and provides sentence
        boundaries and tokenization along with part-of-speech
        tags, dependency trees, and other properties.

        Args:
            request (:class:`google.cloud.language_v1beta2.types.AnalyzeSyntaxRequest`):
                The request object. The syntax analysis request message.
            document (:class:`google.cloud.language_v1beta2.types.Document`):
                Required. Input document.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            encoding_type (:class:`google.cloud.language_v1beta2.types.EncodingType`):
                The encoding type used by the API to
                calculate offsets.

                This corresponds to the ``encoding_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.language_v1beta2.types.AnalyzeSyntaxResponse:
                The syntax analysis response message.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([document, encoding_type])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = language_service.AnalyzeSyntaxRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if document is not None:
            request.document = document
        if encoding_type is not None:
            request.encoding_type = encoding_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.analyze_syntax,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def classify_text(
        self,
        request: language_service.ClassifyTextRequest = None,
        *,
        document: language_service.Document = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.ClassifyTextResponse:
        r"""Classifies a document into categories.

        Args:
            request (:class:`google.cloud.language_v1beta2.types.ClassifyTextRequest`):
                The request object. The document classification request
                message.
            document (:class:`google.cloud.language_v1beta2.types.Document`):
                Required. Input document.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.language_v1beta2.types.ClassifyTextResponse:
                The document classification response
                message.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([document])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = language_service.ClassifyTextRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if document is not None:
            request.document = document

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.classify_text,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def annotate_text(
        self,
        request: language_service.AnnotateTextRequest = None,
        *,
        document: language_service.Document = None,
        features: language_service.AnnotateTextRequest.Features = None,
        encoding_type: language_service.EncodingType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnnotateTextResponse:
        r"""A convenience method that provides all syntax,
        sentiment, entity, and classification features in one
        call.

        Args:
            request (:class:`google.cloud.language_v1beta2.types.AnnotateTextRequest`):
                The request object. The request message for the text
                annotation API, which can perform multiple analysis
                types (sentiment, entities, and syntax) in one call.
            document (:class:`google.cloud.language_v1beta2.types.Document`):
                Required. Input document.
                This corresponds to the ``document`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            features (:class:`google.cloud.language_v1beta2.types.AnnotateTextRequest.Features`):
                Required. The enabled features.
                This corresponds to the ``features`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            encoding_type (:class:`google.cloud.language_v1beta2.types.EncodingType`):
                The encoding type used by the API to
                calculate offsets.

                This corresponds to the ``encoding_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.language_v1beta2.types.AnnotateTextResponse:
                The text annotations response
                message.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([document, features, encoding_type])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = language_service.AnnotateTextRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if document is not None:
            request.document = document
        if features is not None:
            request.features = features
        if encoding_type is not None:
            request.encoding_type = encoding_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.annotate_text,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-language",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("LanguageServiceAsyncClient",)
