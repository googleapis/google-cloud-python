# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.translate_v3 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.translate_v3.services.translation_service import pagers
from google.cloud.translate_v3.types import adaptive_mt, translation_service

from .transports.base import DEFAULT_CLIENT_INFO, TranslationServiceTransport
from .transports.grpc import TranslationServiceGrpcTransport
from .transports.grpc_asyncio import TranslationServiceGrpcAsyncIOTransport
from .transports.rest import TranslationServiceRestTransport


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
    _transport_registry["rest"] = TranslationServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[TranslationServiceTransport]:
        """Returns an appropriate transport class.

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
        """Converts api endpoint to mTLS endpoint.

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
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TranslationServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            TranslationServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> TranslationServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            TranslationServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def adaptive_mt_dataset_path(
        project: str,
        location: str,
        dataset: str,
    ) -> str:
        """Returns a fully-qualified adaptive_mt_dataset string."""
        return "projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}".format(
            project=project,
            location=location,
            dataset=dataset,
        )

    @staticmethod
    def parse_adaptive_mt_dataset_path(path: str) -> Dict[str, str]:
        """Parses a adaptive_mt_dataset path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/adaptiveMtDatasets/(?P<dataset>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def adaptive_mt_file_path(
        project: str,
        location: str,
        dataset: str,
        file: str,
    ) -> str:
        """Returns a fully-qualified adaptive_mt_file string."""
        return "projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}".format(
            project=project,
            location=location,
            dataset=dataset,
            file=file,
        )

    @staticmethod
    def parse_adaptive_mt_file_path(path: str) -> Dict[str, str]:
        """Parses a adaptive_mt_file path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/adaptiveMtDatasets/(?P<dataset>.+?)/adaptiveMtFiles/(?P<file>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def adaptive_mt_sentence_path(
        project: str,
        location: str,
        dataset: str,
        file: str,
        sentence: str,
    ) -> str:
        """Returns a fully-qualified adaptive_mt_sentence string."""
        return "projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}/adaptiveMtSentences/{sentence}".format(
            project=project,
            location=location,
            dataset=dataset,
            file=file,
            sentence=sentence,
        )

    @staticmethod
    def parse_adaptive_mt_sentence_path(path: str) -> Dict[str, str]:
        """Parses a adaptive_mt_sentence path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/adaptiveMtDatasets/(?P<dataset>.+?)/adaptiveMtFiles/(?P<file>.+?)/adaptiveMtSentences/(?P<sentence>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def glossary_path(
        project: str,
        location: str,
        glossary: str,
    ) -> str:
        """Returns a fully-qualified glossary string."""
        return "projects/{project}/locations/{location}/glossaries/{glossary}".format(
            project=project,
            location=location,
            glossary=glossary,
        )

    @staticmethod
    def parse_glossary_path(path: str) -> Dict[str, str]:
        """Parses a glossary path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/glossaries/(?P<glossary>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, TranslationServiceTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the translation service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, TranslationServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        client_options = cast(client_options_lib.ClientOptions, client_options)

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, TranslationServiceTransport):
            # transport is a TranslationServiceTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def translate_text(
        self,
        request: Optional[Union[translation_service.TranslateTextRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        target_language_code: Optional[str] = None,
        contents: Optional[MutableSequence[str]] = None,
        model: Optional[str] = None,
        mime_type: Optional[str] = None,
        source_language_code: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.TranslateTextResponse:
        r"""Translates input text and returns translated text.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_translate_text():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.TranslateTextRequest(
                    contents=['contents_value1', 'contents_value2'],
                    target_language_code="target_language_code_value",
                    parent="parent_value",
                )

                # Make the request
                response = client.translate_text(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.TranslateTextRequest, dict]):
                The request object. The request message for synchronous
                translation.
            parent (str):
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
            target_language_code (str):
                Required. The ISO-639 language code
                to use for translation of the input
                text, set to one of the language codes
                listed in Language Support.

                This corresponds to the ``target_language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            contents (MutableSequence[str]):
                Required. The content of the input in
                string format. We recommend the total
                content be less than 30,000 codepoints.
                The max length of this field is 1024.
                Use BatchTranslateText for larger text.

                This corresponds to the ``contents`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            model (str):
                Optional. The ``model`` type requested for this
                translation.

                The format depends on model type:

                -  AutoML Translation models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/{model-id}``

                -  General (built-in) models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/nmt``,

                For global (non-regionalized) requests, use
                ``location-id`` ``global``. For example,
                ``projects/{project-number-or-id}/locations/global/models/general/nmt``.

                If not provided, the default Google model (NMT) will be
                used

                This corresponds to the ``model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mime_type (str):
                Optional. The format of the source
                text, for example, "text/html",
                "text/plain". If left blank, the MIME
                type defaults to "text/html".

                This corresponds to the ``mime_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source_language_code (str):
                Optional. The ISO-639 language code
                of the input text if known, for example,
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
            google.cloud.translate_v3.types.TranslateTextResponse:

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def detect_language(
        self,
        request: Optional[
            Union[translation_service.DetectLanguageRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        model: Optional[str] = None,
        mime_type: Optional[str] = None,
        content: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.DetectLanguageResponse:
        r"""Detects the language of text within a request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_detect_language():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.DetectLanguageRequest(
                    content="content_value",
                    parent="parent_value",
                )

                # Make the request
                response = client.detect_language(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.DetectLanguageRequest, dict]):
                The request object. The request message for language
                detection.
            parent (str):
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
            model (str):
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
            mime_type (str):
                Optional. The format of the source
                text, for example, "text/html",
                "text/plain". If left blank, the MIME
                type defaults to "text/html".

                This corresponds to the ``mime_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            content (str):
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
            google.cloud.translate_v3.types.DetectLanguageResponse:
                The response message for language
                detection.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_supported_languages(
        self,
        request: Optional[
            Union[translation_service.GetSupportedLanguagesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        model: Optional[str] = None,
        display_language_code: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.SupportedLanguages:
        r"""Returns a list of supported languages for
        translation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_get_supported_languages():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.GetSupportedLanguagesRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.get_supported_languages(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.GetSupportedLanguagesRequest, dict]):
                The request object. The request message for discovering
                supported languages.
            parent (str):
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
            model (str):
                Optional. Get supported languages of this model.

                The format depends on model type:

                -  AutoML Translation models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/{model-id}``

                -  General (built-in) models:
                   ``projects/{project-number-or-id}/locations/{location-id}/models/general/nmt``,

                Returns languages supported by the specified model. If
                missing, we get supported languages of Google general
                NMT model.

                This corresponds to the ``model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            display_language_code (str):
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
            google.cloud.translate_v3.types.SupportedLanguages:
                The response message for discovering
                supported languages.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def translate_document(
        self,
        request: Optional[
            Union[translation_service.TranslateDocumentRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.TranslateDocumentResponse:
        r"""Translates documents in synchronous mode.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_translate_document():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                document_input_config = translate_v3.DocumentInputConfig()
                document_input_config.content = b'content_blob'

                request = translate_v3.TranslateDocumentRequest(
                    parent="parent_value",
                    target_language_code="target_language_code_value",
                    document_input_config=document_input_config,
                )

                # Make the request
                response = client.translate_document(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.TranslateDocumentRequest, dict]):
                The request object. A document translation request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.types.TranslateDocumentResponse:
                A translated document response
                message.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.TranslateDocumentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.TranslateDocumentRequest):
            request = translation_service.TranslateDocumentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.translate_document]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def batch_translate_text(
        self,
        request: Optional[
            Union[translation_service.BatchTranslateTextRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
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

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_batch_translate_text():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                input_configs = translate_v3.InputConfig()
                input_configs.gcs_source.input_uri = "input_uri_value"

                output_config = translate_v3.OutputConfig()
                output_config.gcs_destination.output_uri_prefix = "output_uri_prefix_value"

                request = translate_v3.BatchTranslateTextRequest(
                    parent="parent_value",
                    source_language_code="source_language_code_value",
                    target_language_codes=['target_language_codes_value1', 'target_language_codes_value2'],
                    input_configs=input_configs,
                    output_config=output_config,
                )

                # Make the request
                operation = client.batch_translate_text(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.BatchTranslateTextRequest, dict]):
                The request object. The batch translation request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.translate_v3.types.BatchTranslateResponse` Stored in the
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
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            translation_service.BatchTranslateResponse,
            metadata_type=translation_service.BatchTranslateMetadata,
        )

        # Done; return the response.
        return response

    def batch_translate_document(
        self,
        request: Optional[
            Union[translation_service.BatchTranslateDocumentRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        source_language_code: Optional[str] = None,
        target_language_codes: Optional[MutableSequence[str]] = None,
        input_configs: Optional[
            MutableSequence[translation_service.BatchDocumentInputConfig]
        ] = None,
        output_config: Optional[translation_service.BatchDocumentOutputConfig] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Translates a large volume of document in asynchronous
        batch mode. This function provides real-time output as
        the inputs are being processed. If caller cancels a
        request, the partial results (for an input file, it's
        all or nothing) may still be available on the specified
        output location.

        This call returns immediately and you can use
        google.longrunning.Operation.name to poll the status of
        the call.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_batch_translate_document():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                input_configs = translate_v3.BatchDocumentInputConfig()
                input_configs.gcs_source.input_uri = "input_uri_value"

                output_config = translate_v3.BatchDocumentOutputConfig()
                output_config.gcs_destination.output_uri_prefix = "output_uri_prefix_value"

                request = translate_v3.BatchTranslateDocumentRequest(
                    parent="parent_value",
                    source_language_code="source_language_code_value",
                    target_language_codes=['target_language_codes_value1', 'target_language_codes_value2'],
                    input_configs=input_configs,
                    output_config=output_config,
                )

                # Make the request
                operation = client.batch_translate_document(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.BatchTranslateDocumentRequest, dict]):
                The request object. The BatchTranslateDocument request.
            parent (str):
                Required. Location to make a regional call.

                Format:
                ``projects/{project-number-or-id}/locations/{location-id}``.

                The ``global`` location is not supported for batch
                translation.

                Only AutoML Translation models or glossaries within the
                same region (have the same location-id) can be used,
                otherwise an INVALID_ARGUMENT (400) error is returned.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source_language_code (str):
                Required. The ISO-639 language code of the input
                document if known, for example, "en-US" or "sr-Latn".
                Supported language codes are listed in `Language
                Support <https://cloud.google.com/translate/docs/languages>`__.

                This corresponds to the ``source_language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target_language_codes (MutableSequence[str]):
                Required. The ISO-639 language code
                to use for translation of the input
                document. Specify up to 10 language
                codes here.

                This corresponds to the ``target_language_codes`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            input_configs (MutableSequence[google.cloud.translate_v3.types.BatchDocumentInputConfig]):
                Required. Input configurations.
                The total number of files matched should
                be <= 100. The total content size to
                translate should be <= 100M Unicode
                codepoints. The files must use UTF-8
                encoding.

                This corresponds to the ``input_configs`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_config (google.cloud.translate_v3.types.BatchDocumentOutputConfig):
                Required. Output configuration.
                If 2 input configs match to the same
                file (that is, same input path), we
                don't generate output for duplicate
                inputs.

                This corresponds to the ``output_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.translate_v3.types.BatchTranslateDocumentResponse` Stored in the
                   [google.longrunning.Operation.response][google.longrunning.Operation.response]
                   field returned by BatchTranslateDocument if at least
                   one document is translated successfully.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                parent,
                source_language_code,
                target_language_codes,
                input_configs,
                output_config,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a translation_service.BatchTranslateDocumentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, translation_service.BatchTranslateDocumentRequest):
            request = translation_service.BatchTranslateDocumentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if source_language_code is not None:
                request.source_language_code = source_language_code
            if target_language_codes is not None:
                request.target_language_codes = target_language_codes
            if input_configs is not None:
                request.input_configs = input_configs
            if output_config is not None:
                request.output_config = output_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_translate_document]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            translation_service.BatchTranslateDocumentResponse,
            metadata_type=translation_service.BatchTranslateDocumentMetadata,
        )

        # Done; return the response.
        return response

    def create_glossary(
        self,
        request: Optional[
            Union[translation_service.CreateGlossaryRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        glossary: Optional[translation_service.Glossary] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a glossary and returns the long-running operation.
        Returns NOT_FOUND, if the project doesn't exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_create_glossary():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                glossary = translate_v3.Glossary()
                glossary.name = "name_value"

                request = translate_v3.CreateGlossaryRequest(
                    parent="parent_value",
                    glossary=glossary,
                )

                # Make the request
                operation = client.create_glossary(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.CreateGlossaryRequest, dict]):
                The request object. Request message for CreateGlossary.
            parent (str):
                Required. The project name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            glossary (google.cloud.translate_v3.types.Glossary):
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.translate_v3.types.Glossary`
                Represents a glossary built from user-provided data.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

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
        request: Optional[
            Union[translation_service.ListGlossariesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGlossariesPager:
        r"""Lists glossaries in a project. Returns NOT_FOUND, if the project
        doesn't exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_list_glossaries():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.ListGlossariesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_glossaries(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.ListGlossariesRequest, dict]):
                The request object. Request message for ListGlossaries.
            parent (str):
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
            google.cloud.translate_v3.services.translation_service.pagers.ListGlossariesPager:
                Response message for ListGlossaries.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListGlossariesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_glossary(
        self,
        request: Optional[Union[translation_service.GetGlossaryRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.Glossary:
        r"""Gets a glossary. Returns NOT_FOUND, if the glossary doesn't
        exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_get_glossary():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.GetGlossaryRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_glossary(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.GetGlossaryRequest, dict]):
                The request object. Request message for GetGlossary.
            name (str):
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
            google.cloud.translate_v3.types.Glossary:
                Represents a glossary built from
                user-provided data.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_glossary(
        self,
        request: Optional[
            Union[translation_service.DeleteGlossaryRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a glossary, or cancels glossary construction if the
        glossary isn't created yet. Returns NOT_FOUND, if the glossary
        doesn't exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_delete_glossary():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.DeleteGlossaryRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_glossary(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.DeleteGlossaryRequest, dict]):
                The request object. Request message for DeleteGlossary.
            name (str):
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.translate_v3.types.DeleteGlossaryResponse` Stored in the
                   [google.longrunning.Operation.response][google.longrunning.Operation.response]
                   field returned by DeleteGlossary.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            translation_service.DeleteGlossaryResponse,
            metadata_type=translation_service.DeleteGlossaryMetadata,
        )

        # Done; return the response.
        return response

    def create_adaptive_mt_dataset(
        self,
        request: Optional[
            Union[adaptive_mt.CreateAdaptiveMtDatasetRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        adaptive_mt_dataset: Optional[adaptive_mt.AdaptiveMtDataset] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> adaptive_mt.AdaptiveMtDataset:
        r"""Creates an Adaptive MT dataset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_create_adaptive_mt_dataset():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                adaptive_mt_dataset = translate_v3.AdaptiveMtDataset()
                adaptive_mt_dataset.name = "name_value"

                request = translate_v3.CreateAdaptiveMtDatasetRequest(
                    parent="parent_value",
                    adaptive_mt_dataset=adaptive_mt_dataset,
                )

                # Make the request
                response = client.create_adaptive_mt_dataset(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.CreateAdaptiveMtDatasetRequest, dict]):
                The request object. Request message for creating an
                AdaptiveMtDataset.
            parent (str):
                Required. Name of the parent project. In form of
                ``projects/{project-number-or-id}/locations/{location-id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            adaptive_mt_dataset (google.cloud.translate_v3.types.AdaptiveMtDataset):
                Required. The AdaptiveMtDataset to be
                created.

                This corresponds to the ``adaptive_mt_dataset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.types.AdaptiveMtDataset:
                An Adaptive MT Dataset.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, adaptive_mt_dataset])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.CreateAdaptiveMtDatasetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.CreateAdaptiveMtDatasetRequest):
            request = adaptive_mt.CreateAdaptiveMtDatasetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if adaptive_mt_dataset is not None:
                request.adaptive_mt_dataset = adaptive_mt_dataset

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_adaptive_mt_dataset
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_adaptive_mt_dataset(
        self,
        request: Optional[
            Union[adaptive_mt.DeleteAdaptiveMtDatasetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an Adaptive MT dataset, including all its
        entries and associated metadata.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_delete_adaptive_mt_dataset():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.DeleteAdaptiveMtDatasetRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_adaptive_mt_dataset(request=request)

        Args:
            request (Union[google.cloud.translate_v3.types.DeleteAdaptiveMtDatasetRequest, dict]):
                The request object. Request message for deleting an
                AdaptiveMtDataset.
            name (str):
                Required. Name of the dataset. In the form of
                ``projects/{project-number-or-id}/locations/{location-id}/adaptiveMtDatasets/{adaptive-mt-dataset-id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.DeleteAdaptiveMtDatasetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.DeleteAdaptiveMtDatasetRequest):
            request = adaptive_mt.DeleteAdaptiveMtDatasetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_adaptive_mt_dataset
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_adaptive_mt_dataset(
        self,
        request: Optional[Union[adaptive_mt.GetAdaptiveMtDatasetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> adaptive_mt.AdaptiveMtDataset:
        r"""Gets the Adaptive MT dataset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_get_adaptive_mt_dataset():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.GetAdaptiveMtDatasetRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_adaptive_mt_dataset(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.GetAdaptiveMtDatasetRequest, dict]):
                The request object. Request message for getting an
                Adaptive MT dataset.
            name (str):
                Required. Name of the dataset. In the form of
                ``projects/{project-number-or-id}/locations/{location-id}/adaptiveMtDatasets/{adaptive-mt-dataset-id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.types.AdaptiveMtDataset:
                An Adaptive MT Dataset.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.GetAdaptiveMtDatasetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.GetAdaptiveMtDatasetRequest):
            request = adaptive_mt.GetAdaptiveMtDatasetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_adaptive_mt_dataset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_adaptive_mt_datasets(
        self,
        request: Optional[
            Union[adaptive_mt.ListAdaptiveMtDatasetsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAdaptiveMtDatasetsPager:
        r"""Lists all Adaptive MT datasets for which the caller
        has read permission.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_list_adaptive_mt_datasets():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.ListAdaptiveMtDatasetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_adaptive_mt_datasets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.ListAdaptiveMtDatasetsRequest, dict]):
                The request object. Request message for listing all
                Adaptive MT datasets that the requestor
                has access to.
            parent (str):
                Required. The resource name of the project from which to
                list the Adaptive MT datasets.
                ``projects/{project-number-or-id}/locations/{location-id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.services.translation_service.pagers.ListAdaptiveMtDatasetsPager:
                A list of AdaptiveMtDatasets.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.ListAdaptiveMtDatasetsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.ListAdaptiveMtDatasetsRequest):
            request = adaptive_mt.ListAdaptiveMtDatasetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_adaptive_mt_datasets
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAdaptiveMtDatasetsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def adaptive_mt_translate(
        self,
        request: Optional[Union[adaptive_mt.AdaptiveMtTranslateRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        content: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> adaptive_mt.AdaptiveMtTranslateResponse:
        r"""Translate text using Adaptive MT.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_adaptive_mt_translate():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.AdaptiveMtTranslateRequest(
                    parent="parent_value",
                    dataset="dataset_value",
                    content=['content_value1', 'content_value2'],
                )

                # Make the request
                response = client.adaptive_mt_translate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.AdaptiveMtTranslateRequest, dict]):
                The request object. The request for sending an AdaptiveMt
                translation query.
            parent (str):
                Required. Location to make a regional call.

                Format:
                ``projects/{project-number-or-id}/locations/{location-id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            content (MutableSequence[str]):
                Required. The content of the input in
                string format. For now only one sentence
                per request is supported.

                This corresponds to the ``content`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.types.AdaptiveMtTranslateResponse:
                An AdaptiveMtTranslate response.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, content])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.AdaptiveMtTranslateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.AdaptiveMtTranslateRequest):
            request = adaptive_mt.AdaptiveMtTranslateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if content is not None:
                request.content = content

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.adaptive_mt_translate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_adaptive_mt_file(
        self,
        request: Optional[Union[adaptive_mt.GetAdaptiveMtFileRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> adaptive_mt.AdaptiveMtFile:
        r"""Gets and AdaptiveMtFile

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_get_adaptive_mt_file():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.GetAdaptiveMtFileRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_adaptive_mt_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.GetAdaptiveMtFileRequest, dict]):
                The request object. The request for getting an
                AdaptiveMtFile.
            name (str):
                Required. The resource name of the file, in form of
                ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.types.AdaptiveMtFile:
                An AdaptiveMtFile.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.GetAdaptiveMtFileRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.GetAdaptiveMtFileRequest):
            request = adaptive_mt.GetAdaptiveMtFileRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_adaptive_mt_file]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_adaptive_mt_file(
        self,
        request: Optional[Union[adaptive_mt.DeleteAdaptiveMtFileRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an AdaptiveMtFile along with its sentences.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_delete_adaptive_mt_file():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.DeleteAdaptiveMtFileRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_adaptive_mt_file(request=request)

        Args:
            request (Union[google.cloud.translate_v3.types.DeleteAdaptiveMtFileRequest, dict]):
                The request object. The request for deleting an
                AdaptiveMt file.
            name (str):
                Required. The resource name of the file to delete, in
                form of
                ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.DeleteAdaptiveMtFileRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.DeleteAdaptiveMtFileRequest):
            request = adaptive_mt.DeleteAdaptiveMtFileRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_adaptive_mt_file]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def import_adaptive_mt_file(
        self,
        request: Optional[Union[adaptive_mt.ImportAdaptiveMtFileRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> adaptive_mt.ImportAdaptiveMtFileResponse:
        r"""Imports an AdaptiveMtFile and adds all of its
        sentences into the AdaptiveMtDataset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_import_adaptive_mt_file():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                file_input_source = translate_v3.FileInputSource()
                file_input_source.mime_type = "mime_type_value"
                file_input_source.content = b'content_blob'
                file_input_source.display_name = "display_name_value"

                request = translate_v3.ImportAdaptiveMtFileRequest(
                    file_input_source=file_input_source,
                    parent="parent_value",
                )

                # Make the request
                response = client.import_adaptive_mt_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.ImportAdaptiveMtFileRequest, dict]):
                The request object. The request for importing an
                AdaptiveMt file along with its
                sentences.
            parent (str):
                Required. The resource name of the file, in form of
                ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.types.ImportAdaptiveMtFileResponse:
                The response for importing an
                AdaptiveMtFile

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.ImportAdaptiveMtFileRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.ImportAdaptiveMtFileRequest):
            request = adaptive_mt.ImportAdaptiveMtFileRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.import_adaptive_mt_file]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_adaptive_mt_files(
        self,
        request: Optional[Union[adaptive_mt.ListAdaptiveMtFilesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAdaptiveMtFilesPager:
        r"""Lists all AdaptiveMtFiles associated to an
        AdaptiveMtDataset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_list_adaptive_mt_files():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.ListAdaptiveMtFilesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_adaptive_mt_files(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.ListAdaptiveMtFilesRequest, dict]):
                The request object. The request to list all AdaptiveMt
                files under a given dataset.
            parent (str):
                Required. The resource name of the project from which to
                list the Adaptive MT files.
                ``projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.services.translation_service.pagers.ListAdaptiveMtFilesPager:
                The response for listing all
                AdaptiveMt files under a given dataset.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.ListAdaptiveMtFilesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.ListAdaptiveMtFilesRequest):
            request = adaptive_mt.ListAdaptiveMtFilesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_adaptive_mt_files]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAdaptiveMtFilesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_adaptive_mt_sentences(
        self,
        request: Optional[
            Union[adaptive_mt.ListAdaptiveMtSentencesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAdaptiveMtSentencesPager:
        r"""Lists all AdaptiveMtSentences under a given
        file/dataset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import translate_v3

            def sample_list_adaptive_mt_sentences():
                # Create a client
                client = translate_v3.TranslationServiceClient()

                # Initialize request argument(s)
                request = translate_v3.ListAdaptiveMtSentencesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_adaptive_mt_sentences(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.translate_v3.types.ListAdaptiveMtSentencesRequest, dict]):
                The request object. The request for listing Adaptive MT
                sentences from a Dataset/File.
            parent (str):
                Required. The resource name of the project from which to
                list the Adaptive MT files. The following format lists
                all sentences under a file.
                ``projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}``
                The following format lists all sentences within a
                dataset.
                ``projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.translate_v3.services.translation_service.pagers.ListAdaptiveMtSentencesPager:
                List AdaptiveMt sentences response.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a adaptive_mt.ListAdaptiveMtSentencesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, adaptive_mt.ListAdaptiveMtSentencesRequest):
            request = adaptive_mt.ListAdaptiveMtSentencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_adaptive_mt_sentences
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAdaptiveMtSentencesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "TranslationServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("TranslationServiceClient",)
