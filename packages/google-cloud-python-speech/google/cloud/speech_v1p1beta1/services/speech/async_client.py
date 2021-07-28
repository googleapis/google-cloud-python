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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.speech_v1p1beta1.types import cloud_speech
from google.protobuf import duration_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import SpeechTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SpeechGrpcAsyncIOTransport
from .client import SpeechClient


class SpeechAsyncClient:
    """Service that implements Google Cloud Speech API."""

    _client: SpeechClient

    DEFAULT_ENDPOINT = SpeechClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SpeechClient.DEFAULT_MTLS_ENDPOINT

    custom_class_path = staticmethod(SpeechClient.custom_class_path)
    parse_custom_class_path = staticmethod(SpeechClient.parse_custom_class_path)
    phrase_set_path = staticmethod(SpeechClient.phrase_set_path)
    parse_phrase_set_path = staticmethod(SpeechClient.parse_phrase_set_path)
    common_billing_account_path = staticmethod(SpeechClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(
        SpeechClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SpeechClient.common_folder_path)
    parse_common_folder_path = staticmethod(SpeechClient.parse_common_folder_path)
    common_organization_path = staticmethod(SpeechClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        SpeechClient.parse_common_organization_path
    )
    common_project_path = staticmethod(SpeechClient.common_project_path)
    parse_common_project_path = staticmethod(SpeechClient.parse_common_project_path)
    common_location_path = staticmethod(SpeechClient.common_location_path)
    parse_common_location_path = staticmethod(SpeechClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SpeechAsyncClient: The constructed client.
        """
        return SpeechClient.from_service_account_info.__func__(SpeechAsyncClient, info, *args, **kwargs)  # type: ignore

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
            SpeechAsyncClient: The constructed client.
        """
        return SpeechClient.from_service_account_file.__func__(SpeechAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SpeechTransport:
        """Returns the transport used by the client instance.

        Returns:
            SpeechTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(SpeechClient).get_transport_class, type(SpeechClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, SpeechTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the speech client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SpeechTransport]): The
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
        self._client = SpeechClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def recognize(
        self,
        request: cloud_speech.RecognizeRequest = None,
        *,
        config: cloud_speech.RecognitionConfig = None,
        audio: cloud_speech.RecognitionAudio = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_speech.RecognizeResponse:
        r"""Performs synchronous speech recognition: receive
        results after all audio has been sent and processed.

        Args:
            request (:class:`google.cloud.speech_v1p1beta1.types.RecognizeRequest`):
                The request object. The top-level message sent by the
                client for the `Recognize` method.
            config (:class:`google.cloud.speech_v1p1beta1.types.RecognitionConfig`):
                Required. Provides information to the
                recognizer that specifies how to process
                the request.

                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audio (:class:`google.cloud.speech_v1p1beta1.types.RecognitionAudio`):
                Required. The audio data to be
                recognized.

                This corresponds to the ``audio`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v1p1beta1.types.RecognizeResponse:
                The only message returned to the client by the Recognize method. It
                   contains the result as zero or more sequential
                   SpeechRecognitionResult messages.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([config, audio])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_speech.RecognizeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if config is not None:
            request.config = config
        if audio is not None:
            request.audio = audio

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.recognize,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5000.0,
            ),
            default_timeout=5000.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def long_running_recognize(
        self,
        request: cloud_speech.LongRunningRecognizeRequest = None,
        *,
        config: cloud_speech.RecognitionConfig = None,
        audio: cloud_speech.RecognitionAudio = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Performs asynchronous speech recognition: receive results via
        the google.longrunning.Operations interface. Returns either an
        ``Operation.error`` or an ``Operation.response`` which contains
        a ``LongRunningRecognizeResponse`` message. For more information
        on asynchronous speech recognition, see the
        `how-to <https://cloud.google.com/speech-to-text/docs/async-recognize>`__.

        Args:
            request (:class:`google.cloud.speech_v1p1beta1.types.LongRunningRecognizeRequest`):
                The request object. The top-level message sent by the
                client for the `LongRunningRecognize` method.
            config (:class:`google.cloud.speech_v1p1beta1.types.RecognitionConfig`):
                Required. Provides information to the
                recognizer that specifies how to process
                the request.

                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audio (:class:`google.cloud.speech_v1p1beta1.types.RecognitionAudio`):
                Required. The audio data to be
                recognized.

                This corresponds to the ``audio`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.speech_v1p1beta1.types.LongRunningRecognizeResponse` The only message returned to the client by the LongRunningRecognize method.
                   It contains the result as zero or more sequential
                   SpeechRecognitionResult messages. It is included in
                   the result.response field of the Operation returned
                   by the GetOperation call of the
                   google::longrunning::Operations service.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([config, audio])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_speech.LongRunningRecognizeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if config is not None:
            request.config = config
        if audio is not None:
            request.audio = audio

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.long_running_recognize,
            default_timeout=5000.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_speech.LongRunningRecognizeResponse,
            metadata_type=cloud_speech.LongRunningRecognizeMetadata,
        )

        # Done; return the response.
        return response

    def streaming_recognize(
        self,
        requests: AsyncIterator[cloud_speech.StreamingRecognizeRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[cloud_speech.StreamingRecognizeResponse]]:
        r"""Performs bidirectional streaming speech recognition:
        receive results while sending audio. This method is only
        available via the gRPC API (not REST).

        Args:
            requests (AsyncIterator[`google.cloud.speech_v1p1beta1.types.StreamingRecognizeRequest`]):
                The request object AsyncIterator. The top-level message sent by the
                client for the `StreamingRecognize` method. Multiple
                `StreamingRecognizeRequest` messages are sent. The first
                message must contain a `streaming_config` message and
                must not contain `audio_content`. All subsequent
                messages must contain `audio_content` and must not
                contain a `streaming_config` message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.speech_v1p1beta1.types.StreamingRecognizeResponse]:
                StreamingRecognizeResponse is the only message returned to the client by
                   StreamingRecognize. A series of zero or more
                   StreamingRecognizeResponse messages are streamed back
                   to the client. If there is no recognizable audio, and
                   single_utterance is set to false, then no messages
                   are streamed back to the client.

                   Here's an example of a series of
                   StreamingRecognizeResponses that might be returned
                   while processing audio:

                   1. results { alternatives { transcript: "tube" }
                      stability: 0.01 }
                   2. results { alternatives { transcript: "to be a" }
                      stability: 0.01 }
                   3. results { alternatives { transcript: "to be" }
                      stability: 0.9 } results { alternatives {
                      transcript: " or not to be" } stability: 0.01 }
                   4.

                      results { alternatives { transcript: "to be or not to be"
                         confidence: 0.92 }

                      alternatives { transcript: "to bee or not to bee" }
                         is_final: true }

                   5. results { alternatives { transcript: " that's" }
                      stability: 0.01 }
                   6. results { alternatives { transcript: " that is" }
                      stability: 0.9 } results { alternatives {
                      transcript: " the question" } stability: 0.01 }
                   7.

                      results { alternatives { transcript: " that is the question"
                         confidence: 0.98 }

                      alternatives { transcript: " that was the question" }
                         is_final: true }

                   Notes:

                   -  Only two of the above responses #4 and #7 contain
                      final results; they are indicated by
                      is_final: true. Concatenating these together
                      generates the full transcript: "to be or not to be
                      that is the question".
                   -  The others contain interim results. #3 and #6
                      contain two interim \`results`: the first portion
                      has a high stability and is less likely to change;
                      the second portion has a low stability and is very
                      likely to change. A UI designer might choose to
                      show only high stability results.
                   -  The specific stability and confidence values shown
                      above are only for illustrative purposes. Actual
                      values may vary.
                   -

                      In each response, only one of these fields will be set:
                         error, speech_event_type, or one or more
                         (repeated) results.

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.streaming_recognize,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=5000.0,
            ),
            default_timeout=5000.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-speech",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SpeechAsyncClient",)
