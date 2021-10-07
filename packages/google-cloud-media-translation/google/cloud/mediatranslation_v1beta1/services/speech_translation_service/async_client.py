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
from typing import (
    Dict,
    AsyncIterable,
    Awaitable,
    AsyncIterator,
    Sequence,
    Tuple,
    Type,
    Union,
)
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.mediatranslation_v1beta1.types import media_translation
from google.rpc import status_pb2  # type: ignore
from .transports.base import SpeechTranslationServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SpeechTranslationServiceGrpcAsyncIOTransport
from .client import SpeechTranslationServiceClient


class SpeechTranslationServiceAsyncClient:
    """Provides translation from/to media types."""

    _client: SpeechTranslationServiceClient

    DEFAULT_ENDPOINT = SpeechTranslationServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SpeechTranslationServiceClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        SpeechTranslationServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        SpeechTranslationServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SpeechTranslationServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        SpeechTranslationServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        SpeechTranslationServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        SpeechTranslationServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        SpeechTranslationServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        SpeechTranslationServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        SpeechTranslationServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        SpeechTranslationServiceClient.parse_common_location_path
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
            SpeechTranslationServiceAsyncClient: The constructed client.
        """
        return SpeechTranslationServiceClient.from_service_account_info.__func__(SpeechTranslationServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            SpeechTranslationServiceAsyncClient: The constructed client.
        """
        return SpeechTranslationServiceClient.from_service_account_file.__func__(SpeechTranslationServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SpeechTranslationServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            SpeechTranslationServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(SpeechTranslationServiceClient).get_transport_class,
        type(SpeechTranslationServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, SpeechTranslationServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the speech translation service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SpeechTranslationServiceTransport]): The
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
        self._client = SpeechTranslationServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    def streaming_translate_speech(
        self,
        requests: AsyncIterator[
            media_translation.StreamingTranslateSpeechRequest
        ] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[media_translation.StreamingTranslateSpeechResponse]]:
        r"""Performs bidirectional streaming speech translation:
        receive results while sending audio. This method is only
        available via the gRPC API (not REST).

        Args:
            requests (AsyncIterator[`google.cloud.mediatranslation_v1beta1.types.StreamingTranslateSpeechRequest`]):
                The request object AsyncIterator. The top-level message sent by the
                client for the `StreamingTranslateSpeech` method.
                Multiple `StreamingTranslateSpeechRequest` messages are
                sent. The first message must contain a
                `streaming_config` message and must not contain
                `audio_content` data. All subsequent messages must
                contain `audio_content` data and must not contain a
                `streaming_config` message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.mediatranslation_v1beta1.types.StreamingTranslateSpeechResponse]:
                A streaming speech translation
                response corresponding to a portion of
                the audio currently processed.

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.streaming_translate_speech,
            default_timeout=400.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-media-translation",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SpeechTranslationServiceAsyncClient",)
