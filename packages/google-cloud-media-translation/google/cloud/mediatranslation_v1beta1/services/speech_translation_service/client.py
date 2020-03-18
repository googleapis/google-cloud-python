# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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
from typing import Dict, Iterable, Iterator, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.mediatranslation_v1beta1.types import media_translation
from google.rpc import status_pb2 as status  # type: ignore

from .transports.base import SpeechTranslationServiceTransport
from .transports.grpc import SpeechTranslationServiceGrpcTransport


class SpeechTranslationServiceClientMeta(type):
    """Metaclass for the SpeechTranslationService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[SpeechTranslationServiceTransport]]
    _transport_registry["grpc"] = SpeechTranslationServiceGrpcTransport

    def get_transport_class(
        cls, label: str = None
    ) -> Type[SpeechTranslationServiceTransport]:
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


class SpeechTranslationServiceClient(metaclass=SpeechTranslationServiceClientMeta):
    """Provides translation from/to media types."""

    DEFAULT_OPTIONS = ClientOptions.ClientOptions(
        api_endpoint="mediatranslation.googleapis.com"
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

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, SpeechTranslationServiceTransport] = None,
        client_options: ClientOptions = DEFAULT_OPTIONS,
    ) -> None:
        """Instantiate the speech translation service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SpeechTranslationServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, SpeechTranslationServiceTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                host=client_options.api_endpoint or "mediatranslation.googleapis.com",
            )

    def streaming_translate_speech(
        self,
        requests: Iterator[media_translation.StreamingTranslateSpeechRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[media_translation.StreamingTranslateSpeechResponse]:
        r"""Performs bidirectional streaming speech translation:
        receive results while sending audio. This method is only
        available via the gRPC API (not REST).

        Args:
            requests (Iterator[`~.media_translation.StreamingTranslateSpeechRequest`]):
                The request object iterator. The top-level message sent by the
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
            Iterable[~.media_translation.StreamingTranslateSpeechResponse]:
                A streaming speech translation
                response corresponding to a portion of
                the audio currently processed.

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.streaming_translate_speech,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-media-translation"
        ).version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("SpeechTranslationServiceClient",)
