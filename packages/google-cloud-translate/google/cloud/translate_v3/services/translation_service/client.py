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
import os
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation
from google.api_core import operation_async
from google.cloud.translate_v3.services.translation_service import pagers
from google.cloud.translate_v3.types import translation_service
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import TranslationServiceTransport
from .transports.grpc import TranslationServiceGrpcTransport
from .transports.grpc_asyncio import TranslationServiceGrpcAsyncIOTransport


class TranslationServiceClientMeta(type):
    """Metaclass for the TranslationService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[TranslationServiceTransport]]
    _transport_registry["grpc"] = TranslationServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = TranslationServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[TranslationServiceTransport]:
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


class TranslationServiceClient(metaclass=TranslationServiceClientMeta):
    """Provides natural language translation operations."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "translate.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def glossary_path(project: str, location: str, glossary: str,) -> str:
        """Return a fully-qualified glossary string."""
        return "projects/{project}/locations/{location}/glossaries/{glossary}".format(
            project=project, location=location, glossary=glossary,
        )

    @staticmethod
    def parse_glossary_path(path: str) -> Dict[str, str]:
        """Parse a glossary path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/glossaries/(?P<glossary>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, TranslationServiceTransport] = None,
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the translation service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TranslationServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        if client_options.api_endpoint is None:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS", "never")
            if use_mtls_env == "never":
                client_options.api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                client_options.api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                has_client_cert_source = (
                    client_options.client_cert_source is not None
                    or mtls.has_default_client_cert_source()
                )
                client_options.api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if has_client_cert_source
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, TranslationServiceTransport):
            # transport is a TranslationServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=client_options.api_endpoint,
                scopes=client_options.scopes,
                api_mtls_endpoint=client_options.api_endpoint,
                client_cert_source=client_options.client_cert_source,
                quota_project_id=client_options.quota_project_id,
            )

    def translate_text(
        self,
        request: translation_service.TranslateTextRequest = None,
        *,
        parent: str = None,
        target_language_code: str = None,
        contents: Sequence[str] = None,
        model: str = None,
        mime_type: str = None,
        source_language_code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.TranslateTextResponse:
        r"""Translates input text and returns translated text.

        Args:
            request (:class:`~.translation_service.TranslateTextRequest`):
                The request object. The request message for synchronous
                translation.
            parent (:class:`str`):
                Required. Project or location to make a call. Must refer
                to a caller's project.

                Format: ``projects/{project-number-or-id}`` or
                ``projects/{project-number-or-id}/locations/{location-id}``.

                For global calls, use
                ``projects/{project-number-or-id}/locations/global`` or
                ``projects/{project-number-or-id}``.

                Non-global location is required for requests using
                AutoML models or custom glossaries.

                Models and glossaries must be within the same region
                (have same location-id), otherwise an INVALID_ARGUMENT
                (400) error is returned.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target_language_code (:class:`str`):
                Required. The BCP-47 language code to
                use for translation of the input text,
                set to one of the language codes listed
                in Language Support.
                This corresponds to the ``target_language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            contents (:class:`Sequence[str]`):
                Required. The content of the input in
                string format. We recommend the total
                content be less than 30k codepoints. Use
                BatchTranslateText for larger text.
                This corresponds to the ``contents`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            model (:class:`str`):
                Optional. The ``model`` type requested for this
                translation.

                The format depends on model type:

                -  AutoML Translation models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/{model-id}``

                -  General (built-in) models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/nmt``,
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/base``

                For global (non-regionalized) requests, use
                ``location-id`` ``global``. For example,
                ``projects/{project-number-or-id}/locations/global/models/general/nmt``.

                If missing, the system decides which google base model
                to use.
                This corresponds to the ``model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mime_type (:class:`str`):
                Optional. The format of the source
                text, for example, "text/html",
                "text/plain". If left blank, the MIME
                type defaults to "text/html".
                This corresponds to the ``mime_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source_language_code (:class:`str`):
                Optional. The BCP-47 language code of
                the input text if known, for example,
                "en-US" or "sr-Latn". Supported language
                codes are listed in Language Support. If
                the source language isn't specified, the
                API attempts to identify the source
                language automatically and returns the
                source language within the response.
                This corresponds to the ``source_language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.translation_service.TranslateTextResponse:

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                parent,
                target_language_code,
                contents,
                model,
                mime_type,
                source_language_code,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.TranslateTextRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.TranslateTextRequest):
            request = translation_service.TranslateTextRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if target_language_code is not None:
                request.target_language_code = target_language_code
            if contents is not None:
                request.contents = contents
            if model is not None:
                request.model = model
            if mime_type is not None:
                request.mime_type = mime_type
            if source_language_code is not None:
                request.source_language_code = source_language_code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.translate_text]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def detect_language(
        self,
        request: translation_service.DetectLanguageRequest = None,
        *,
        parent: str = None,
        model: str = None,
        mime_type: str = None,
        content: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.DetectLanguageResponse:
        r"""Detects the language of text within a request.

        Args:
            request (:class:`~.translation_service.DetectLanguageRequest`):
                The request object. The request message for language
                detection.
            parent (:class:`str`):
                Required. Project or location to make a call. Must refer
                to a caller's project.

                Format:
                ``projects/{project-number-or-id}/locations/{location-id}``
                or ``projects/{project-number-or-id}``.

                For global calls, use
                ``projects/{project-number-or-id}/locations/global`` or
                ``projects/{project-number-or-id}``.

                Only models within the same region (has same
                location-id) can be used. Otherwise an INVALID_ARGUMENT
                (400) error is returned.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            model (:class:`str`):
                Optional. The language detection model to be used.

                Format:
                ``projects/{project-number-or-id}/locations/{location-id}/models/language-detection/{model-id}``

                Only one language detection model is currently
                supported:
                ``projects/{project-number-or-id}/locations/{location-id}/models/language-detection/default``.

                If not specified, the default model is used.
                This corresponds to the ``model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mime_type (:class:`str`):
                Optional. The format of the source
                text, for example, "text/html",
                "text/plain". If left blank, the MIME
                type defaults to "text/html".
                This corresponds to the ``mime_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            content (:class:`str`):
                The content of the input stored as a
                string.
                This corresponds to the ``content`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.translation_service.DetectLanguageResponse:
                The response message for language
                detection.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, model, mime_type, content])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.DetectLanguageRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.DetectLanguageRequest):
            request = translation_service.DetectLanguageRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if model is not None:
                request.model = model
            if mime_type is not None:
                request.mime_type = mime_type
            if content is not None:
                request.content = content

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.detect_language]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_supported_languages(
        self,
        request: translation_service.GetSupportedLanguagesRequest = None,
        *,
        parent: str = None,
        model: str = None,
        display_language_code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.SupportedLanguages:
        r"""Returns a list of supported languages for
        translation.

        Args:
            request (:class:`~.translation_service.GetSupportedLanguagesRequest`):
                The request object. The request message for discovering
                supported languages.
            parent (:class:`str`):
                Required. Project or location to make a call. Must refer
                to a caller's project.

                Format: ``projects/{project-number-or-id}`` or
                ``projects/{project-number-or-id}/locations/{location-id}``.

                For global calls, use
                ``projects/{project-number-or-id}/locations/global`` or
                ``projects/{project-number-or-id}``.

                Non-global location is required for AutoML models.

                Only models within the same region (have same
                location-id) can be used, otherwise an INVALID_ARGUMENT
                (400) error is returned.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            model (:class:`str`):
                Optional. Get supported languages of this model.

                The format depends on model type:

                -  AutoML Translation models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/{model-id}``

                -  General (built-in) models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/nmt``,
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/base``

                Returns languages supported by the specified model. If
                missing, we get supported languages of Google general
                base (PBMT) model.
                This corresponds to the ``model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            display_language_code (:class:`str`):
                Optional. The language to use to
                return localized, human readable names
                of supported languages. If missing, then
                display names are not returned in a
                response.
                This corresponds to the ``display_language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.translation_service.SupportedLanguages:
                The response message for discovering
                supported languages.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, model, display_language_code])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.GetSupportedLanguagesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.GetSupportedLanguagesRequest):
            request = translation_service.GetSupportedLanguagesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if model is not None:
                request.model = model
            if display_language_code is not None:
                request.display_language_code = display_language_code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_supported_languages]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_translate_text(
        self,
        request: translation_service.BatchTranslateTextRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Translates a large volume of text in asynchronous
        batch mode. This function provides real-time output as
        the inputs are being processed. If caller cancels a
        request, the partial results (for an input file, it's
        all or nothing) may still be available on the specified
        output location.
        This call returns immediately and you can
        use google.longrunning.Operation.name to poll the status
        of the call.

        Args:
            request (:class:`~.translation_service.BatchTranslateTextRequest`):
                The request object. The batch translation request.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.translation_service.BatchTranslateResponse``:
                Stored in the
                [google.longrunning.Operation.response][google.longrunning.Operation.response]
                field returned by BatchTranslateText if at least one
                sentence is translated successfully.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.BatchTranslateTextRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.BatchTranslateTextRequest):
            request = translation_service.BatchTranslateTextRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_translate_text]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            translation_service.BatchTranslateResponse,
            metadata_type=translation_service.BatchTranslateMetadata,
        )

        # Done; return the response.
        return response

    def create_glossary(
        self,
        request: translation_service.CreateGlossaryRequest = None,
        *,
        parent: str = None,
        glossary: translation_service.Glossary = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a glossary and returns the long-running operation.
        Returns NOT_FOUND, if the project doesn't exist.

        Args:
            request (:class:`~.translation_service.CreateGlossaryRequest`):
                The request object. Request message for CreateGlossary.
            parent (:class:`str`):
                Required. The project name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            glossary (:class:`~.translation_service.Glossary`):
                Required. The glossary to create.
                This corresponds to the ``glossary`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.translation_service.Glossary``: Represents a
                glossary built from user provided data.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, glossary])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.CreateGlossaryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.CreateGlossaryRequest):
            request = translation_service.CreateGlossaryRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if glossary is not None:
                request.glossary = glossary

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_glossary]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            translation_service.Glossary,
            metadata_type=translation_service.CreateGlossaryMetadata,
        )

        # Done; return the response.
        return response

    def list_glossaries(
        self,
        request: translation_service.ListGlossariesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGlossariesPager:
        r"""Lists glossaries in a project. Returns NOT_FOUND, if the project
        doesn't exist.

        Args:
            request (:class:`~.translation_service.ListGlossariesRequest`):
                The request object. Request message for ListGlossaries.
            parent (:class:`str`):
                Required. The name of the project
                from which to list all of the
                glossaries.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListGlossariesPager:
                Response message for ListGlossaries.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.ListGlossariesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.ListGlossariesRequest):
            request = translation_service.ListGlossariesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_glossaries]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListGlossariesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_glossary(
        self,
        request: translation_service.GetGlossaryRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.Glossary:
        r"""Gets a glossary. Returns NOT_FOUND, if the glossary doesn't
        exist.

        Args:
            request (:class:`~.translation_service.GetGlossaryRequest`):
                The request object. Request message for GetGlossary.
            name (:class:`str`):
                Required. The name of the glossary to
                retrieve.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.translation_service.Glossary:
                Represents a glossary built from user
                provided data.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.GetGlossaryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.GetGlossaryRequest):
            request = translation_service.GetGlossaryRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_glossary]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_glossary(
        self,
        request: translation_service.DeleteGlossaryRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a glossary, or cancels glossary construction if the
        glossary isn't created yet. Returns NOT_FOUND, if the glossary
        doesn't exist.

        Args:
            request (:class:`~.translation_service.DeleteGlossaryRequest`):
                The request object. Request message for DeleteGlossary.
            name (:class:`str`):
                Required. The name of the glossary to
                delete.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.translation_service.DeleteGlossaryResponse``:
                Stored in the
                [google.longrunning.Operation.response][google.longrunning.Operation.response]
                field returned by DeleteGlossary.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.DeleteGlossaryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.DeleteGlossaryRequest):
            request = translation_service.DeleteGlossaryRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_glossary]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            translation_service.DeleteGlossaryResponse,
            metadata_type=translation_service.DeleteGlossaryMetadata,
        )

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-translate",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("TranslationServiceClient",)
