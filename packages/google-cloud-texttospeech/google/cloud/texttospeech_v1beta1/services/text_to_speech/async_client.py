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
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.texttospeech_v1beta1.types import cloud_tts

from .transports.base import TextToSpeechTransport
from .transports.grpc_asyncio import TextToSpeechGrpcAsyncIOTransport
from .client import TextToSpeechClient


class TextToSpeechAsyncClient:
    """Service that implements Google Cloud Text-to-Speech API."""

    _client: TextToSpeechClient

    DEFAULT_ENDPOINT = TextToSpeechClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TextToSpeechClient.DEFAULT_MTLS_ENDPOINT

    from_service_account_file = TextToSpeechClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(TextToSpeechClient).get_transport_class, type(TextToSpeechClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, TextToSpeechTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the text to speech client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TextToSpeechTransport]): The
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
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = TextToSpeechClient(
            credentials=credentials, transport=transport, client_options=client_options
        )

    async def list_voices(
        self,
        request: cloud_tts.ListVoicesRequest = None,
        *,
        language_code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tts.ListVoicesResponse:
        r"""Returns a list of Voice supported for synthesis.

        Args:
            request (:class:`~.cloud_tts.ListVoicesRequest`):
                The request object. The top-level message sent by the
                client for the `ListVoices` method.
            language_code (:class:`str`):
                Optional. Recommended.
                `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
                language tag. If specified, the ListVoices call will
                only return voices that can be used to synthesize this
                language_code. E.g. when specifying "en-NZ", you will
                get supported "en-\*" voices; when specifying "no", you
                will get supported "no-\*" (Norwegian) and "nb-*"
                (Norwegian Bokmal) voices; specifying "zh" will also get
                supported "cmn-*" voices; specifying "zh-hk" will also
                get supported "yue-\*" voices.
                This corresponds to the ``language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloud_tts.ListVoicesResponse:
                The message returned to the client by the ``ListVoices``
                method.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([language_code]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tts.ListVoicesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if language_code is not None:
            request.language_code = language_code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_voices,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    async def synthesize_speech(
        self,
        request: cloud_tts.SynthesizeSpeechRequest = None,
        *,
        input: cloud_tts.SynthesisInput = None,
        voice: cloud_tts.VoiceSelectionParams = None,
        audio_config: cloud_tts.AudioConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tts.SynthesizeSpeechResponse:
        r"""Synthesizes speech synchronously: receive results
        after all text input has been processed.

        Args:
            request (:class:`~.cloud_tts.SynthesizeSpeechRequest`):
                The request object. The top-level message sent by the
                client for the `SynthesizeSpeech` method.
            input (:class:`~.cloud_tts.SynthesisInput`):
                Required. The Synthesizer requires
                either plain text or SSML as input.
                This corresponds to the ``input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            voice (:class:`~.cloud_tts.VoiceSelectionParams`):
                Required. The desired voice of the
                synthesized audio.
                This corresponds to the ``voice`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audio_config (:class:`~.cloud_tts.AudioConfig`):
                Required. The configuration of the
                synthesized audio.
                This corresponds to the ``audio_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloud_tts.SynthesizeSpeechResponse:
                The message returned to the client by the
                ``SynthesizeSpeech`` method.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([input, voice, audio_config]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.synthesize_speech,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-texttospeech"
        ).version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("TextToSpeechAsyncClient",)
