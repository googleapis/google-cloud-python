# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import re
from typing import (
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.texttospeech_v1beta1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.longrunning import operations_pb2  # type: ignore

from google.cloud.texttospeech_v1beta1.types import cloud_tts

from .client import TextToSpeechClient
from .transports.base import DEFAULT_CLIENT_INFO, TextToSpeechTransport
from .transports.grpc_asyncio import TextToSpeechGrpcAsyncIOTransport


class TextToSpeechAsyncClient:
    """Service that implements Google Cloud Text-to-Speech API."""

    _client: TextToSpeechClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = TextToSpeechClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TextToSpeechClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = TextToSpeechClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = TextToSpeechClient._DEFAULT_UNIVERSE

    model_path = staticmethod(TextToSpeechClient.model_path)
    parse_model_path = staticmethod(TextToSpeechClient.parse_model_path)
    common_billing_account_path = staticmethod(
        TextToSpeechClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        TextToSpeechClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TextToSpeechClient.common_folder_path)
    parse_common_folder_path = staticmethod(TextToSpeechClient.parse_common_folder_path)
    common_organization_path = staticmethod(TextToSpeechClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        TextToSpeechClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TextToSpeechClient.common_project_path)
    parse_common_project_path = staticmethod(
        TextToSpeechClient.parse_common_project_path
    )
    common_location_path = staticmethod(TextToSpeechClient.common_location_path)
    parse_common_location_path = staticmethod(
        TextToSpeechClient.parse_common_location_path
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
            TextToSpeechAsyncClient: The constructed client.
        """
        return TextToSpeechClient.from_service_account_info.__func__(TextToSpeechAsyncClient, info, *args, **kwargs)  # type: ignore

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
            TextToSpeechAsyncClient: The constructed client.
        """
        return TextToSpeechClient.from_service_account_file.__func__(TextToSpeechAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
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
        return TextToSpeechClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> TextToSpeechTransport:
        """Returns the transport used by the client instance.

        Returns:
            TextToSpeechTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = TextToSpeechClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[str, TextToSpeechTransport, Callable[..., TextToSpeechTransport]]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the text to speech async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,TextToSpeechTransport,Callable[..., TextToSpeechTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the TextToSpeechTransport constructor.
                If set to None, a transport is chosen automatically.
                NOTE: "rest" transport functionality is currently in a
                beta state (preview). We welcome your feedback via an
                issue in this library's source repository.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = TextToSpeechClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_voices(
        self,
        request: Optional[Union[cloud_tts.ListVoicesRequest, dict]] = None,
        *,
        language_code: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tts.ListVoicesResponse:
        r"""Returns a list of Voice supported for synthesis.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import texttospeech_v1beta1

            async def sample_list_voices():
                # Create a client
                client = texttospeech_v1beta1.TextToSpeechAsyncClient()

                # Initialize request argument(s)
                request = texttospeech_v1beta1.ListVoicesRequest(
                )

                # Make the request
                response = await client.list_voices(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.texttospeech_v1beta1.types.ListVoicesRequest, dict]]):
                The request object. The top-level message sent by the client for the
                ``ListVoices`` method.
            language_code (:class:`str`):
                Optional. Recommended.
                `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
                language tag. If not specified, the API will return all
                supported voices. If specified, the ListVoices call will
                only return voices that can be used to synthesize this
                language_code. For example, if you specify ``"en-NZ"``,
                all ``"en-NZ"`` voices will be returned. If you specify
                ``"no"``, both ``"no-\*"`` (Norwegian) and ``"nb-\*"``
                (Norwegian Bokmal) voices will be returned.

                This corresponds to the ``language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.texttospeech_v1beta1.types.ListVoicesResponse:
                The message returned to the client by the ListVoices
                method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([language_code])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_tts.ListVoicesRequest):
            request = cloud_tts.ListVoicesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if language_code is not None:
            request.language_code = language_code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_voices
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def synthesize_speech(
        self,
        request: Optional[Union[cloud_tts.SynthesizeSpeechRequest, dict]] = None,
        *,
        input: Optional[cloud_tts.SynthesisInput] = None,
        voice: Optional[cloud_tts.VoiceSelectionParams] = None,
        audio_config: Optional[cloud_tts.AudioConfig] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tts.SynthesizeSpeechResponse:
        r"""Synthesizes speech synchronously: receive results
        after all text input has been processed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import texttospeech_v1beta1

            async def sample_synthesize_speech():
                # Create a client
                client = texttospeech_v1beta1.TextToSpeechAsyncClient()

                # Initialize request argument(s)
                input = texttospeech_v1beta1.SynthesisInput()
                input.text = "text_value"

                voice = texttospeech_v1beta1.VoiceSelectionParams()
                voice.language_code = "language_code_value"

                audio_config = texttospeech_v1beta1.AudioConfig()
                audio_config.audio_encoding = "ALAW"

                request = texttospeech_v1beta1.SynthesizeSpeechRequest(
                    input=input,
                    voice=voice,
                    audio_config=audio_config,
                )

                # Make the request
                response = await client.synthesize_speech(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.texttospeech_v1beta1.types.SynthesizeSpeechRequest, dict]]):
                The request object. The top-level message sent by the client for the
                ``SynthesizeSpeech`` method.
            input (:class:`google.cloud.texttospeech_v1beta1.types.SynthesisInput`):
                Required. The Synthesizer requires
                either plain text or SSML as input.

                This corresponds to the ``input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            voice (:class:`google.cloud.texttospeech_v1beta1.types.VoiceSelectionParams`):
                Required. The desired voice of the
                synthesized audio.

                This corresponds to the ``voice`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audio_config (:class:`google.cloud.texttospeech_v1beta1.types.AudioConfig`):
                Required. The configuration of the
                synthesized audio.

                This corresponds to the ``audio_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.texttospeech_v1beta1.types.SynthesizeSpeechResponse:
                The message returned to the client by the
                SynthesizeSpeech method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([input, voice, audio_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_tts.SynthesizeSpeechRequest):
            request = cloud_tts.SynthesizeSpeechRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if input is not None:
            request.input = input
        if voice is not None:
            request.voice = voice
        if audio_config is not None:
            request.audio_config = audio_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.synthesize_speech
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def streaming_synthesize(
        self,
        requests: Optional[AsyncIterator[cloud_tts.StreamingSynthesizeRequest]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[cloud_tts.StreamingSynthesizeResponse]]:
        r"""Performs bidirectional streaming speech synthesis:
        receive audio while sending text.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import texttospeech_v1beta1

            async def sample_streaming_synthesize():
                # Create a client
                client = texttospeech_v1beta1.TextToSpeechAsyncClient()

                # Initialize request argument(s)
                streaming_config = texttospeech_v1beta1.StreamingSynthesizeConfig()
                streaming_config.voice.language_code = "language_code_value"

                request = texttospeech_v1beta1.StreamingSynthesizeRequest(
                    streaming_config=streaming_config,
                )

                # This method expects an iterator which contains
                # 'texttospeech_v1beta1.StreamingSynthesizeRequest' objects
                # Here we create a generator that yields a single `request` for
                # demonstrative purposes.
                requests = [request]

                def request_generator():
                    for request in requests:
                        yield request

                # Make the request
                stream = await client.streaming_synthesize(requests=request_generator())

                # Handle the response
                async for response in stream:
                    print(response)

        Args:
            requests (AsyncIterator[`google.cloud.texttospeech_v1beta1.types.StreamingSynthesizeRequest`]):
                The request object AsyncIterator. Request message for the ``StreamingSynthesize`` method.
                Multiple ``StreamingSynthesizeRequest`` messages are
                sent in one call. The first message must contain a
                ``streaming_config`` that fully specifies the request
                configuration and must not contain ``input``. All
                subsequent messages must only have ``input`` set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.texttospeech_v1beta1.types.StreamingSynthesizeResponse]:
                StreamingSynthesizeResponse is the only message returned to the
                   client by StreamingSynthesize method. A series of
                   zero or more StreamingSynthesizeResponse messages are
                   streamed back to the client.

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.streaming_synthesize
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = rpc(
            requests,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self.transport._wrapped_methods[self._client._transport.list_operations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self.transport._wrapped_methods[self._client._transport.get_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "TextToSpeechAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("TextToSpeechAsyncClient",)
