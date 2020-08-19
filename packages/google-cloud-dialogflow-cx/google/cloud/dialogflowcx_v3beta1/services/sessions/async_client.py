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
from typing import Dict, AsyncIterable, AsyncIterator, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dialogflowcx_v3beta1.types import audio_config
from google.cloud.dialogflowcx_v3beta1.types import page
from google.cloud.dialogflowcx_v3beta1.types import session

from .transports.base import SessionsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SessionsGrpcAsyncIOTransport
from .client import SessionsClient


class SessionsAsyncClient:
    """A session represents an interaction with a user. You retrieve user
    input and pass it to the
    [DetectIntent][google.cloud.dialogflow.cx.v3beta1.Sessions.DetectIntent]
    method to determine user intent and respond.
    """

    _client: SessionsClient

    DEFAULT_ENDPOINT = SessionsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SessionsClient.DEFAULT_MTLS_ENDPOINT

    session_entity_type_path = staticmethod(SessionsClient.session_entity_type_path)

    intent_path = staticmethod(SessionsClient.intent_path)

    from_service_account_file = SessionsClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(SessionsClient).get_transport_class, type(SessionsClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, SessionsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the sessions client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SessionsTransport]): The
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

        self._client = SessionsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def detect_intent(
        self,
        request: session.DetectIntentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session.DetectIntentResponse:
        r"""Processes a natural language query and returns
        structured, actionable data as a result. This method is
        not idempotent, because it may cause session entity
        types to be updated, which in turn might affect results
        of future queries.

        Args:
            request (:class:`~.session.DetectIntentRequest`):
                The request object. The request to detect user's intent.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.session.DetectIntentResponse:
                The message returned from the
                DetectIntent method.

        """
        # Create or coerce a protobuf request object.

        request = session.DetectIntentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.detect_intent,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=220.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("session", request.session),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def streaming_detect_intent(
        self,
        requests: AsyncIterator[session.StreamingDetectIntentRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> AsyncIterable[session.StreamingDetectIntentResponse]:
        r"""Processes a natural language query in audio format in
        a streaming fashion and returns structured, actionable
        data as a result. This method is only available via the
        gRPC API (not REST).

        Args:
            requests (AsyncIterator[`~.session.StreamingDetectIntentRequest`]):
                The request object AsyncIterator. The top-level message sent by the
                client to the
                [Sessions.StreamingDetectIntent][google.cloud.dialogflow.cx.v3beta1.Sessions.StreamingDetectIntent]
                method.

                Multiple request messages should be sent in order:

                1.  The first message must contain
                [session][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.session],
                [query_input][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.query_input]
                plus optionally
                [query_params][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.query_params].
                If the client wants to receive an audio response, it
                should also contain
                [output_audio_config][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.output_audio_config].
                2.  If
                [query_input][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.query_input]
                was set to
                [query_input.audio.config][google.cloud.dialogflow.cx.v3beta1.AudioInput.config],
                all subsequent messages must contain
                [query_input.audio.audio][google.cloud.dialogflow.cx.v3beta1.AudioInput.audio]
                to continue with Speech recognition. If you decide to
                rather detect an     intent from text input after you
                already started Speech recognition,     please send a
                message with
                [query_input.text][google.cloud.dialogflow.cx.v3beta1.QueryInput.text].
                    However, note that:

                    * Dialogflow will bill you for the audio duration so
                far.     * Dialogflow discards all Speech recognition
                results in favor of the       input text.
                    * Dialogflow will use the language code from the
                first message.
                After you sent all input, you must half-close or abort
                the request stream.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[~.session.StreamingDetectIntentResponse]:
                The top-level message returned from the
                ``StreamingDetectIntent`` method.

                Multiple response messages can be returned in order:

                1. If the input was set to streaming audio, the first
                   one or more messages contain ``recognition_result``.
                   Each ``recognition_result`` represents a more
                   complete transcript of what the user said. The last
                   ``recognition_result`` has ``is_final`` set to
                   ``true``.

                2. The last message contains ``detect_intent_response``.

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.streaming_detect_intent,
            default_timeout=220.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def match_intent(
        self,
        request: session.MatchIntentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session.MatchIntentResponse:
        r"""Returns preliminary intent match results, doesn't
        change the session status.

        Args:
            request (:class:`~.session.MatchIntentRequest`):
                The request object. Request of [MatchIntent][].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.session.MatchIntentResponse:
                Response of [MatchIntent][].
        """
        # Create or coerce a protobuf request object.

        request = session.MatchIntentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.match_intent,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("session", request.session),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def fulfill_intent(
        self,
        request: session.FulfillIntentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session.FulfillIntentResponse:
        r"""Fulfills a matched intent returned by
        [MatchIntent][google.cloud.dialogflow.cx.v3beta1.Sessions.MatchIntent].
        Must be called after
        [MatchIntent][google.cloud.dialogflow.cx.v3beta1.Sessions.MatchIntent],
        with input from
        [MatchIntentResponse][google.cloud.dialogflow.cx.v3beta1.MatchIntentResponse].
        Otherwise, the behavior is undefined.

        Args:
            request (:class:`~.session.FulfillIntentRequest`):
                The request object. Request of [FulfillIntent][]

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.session.FulfillIntentResponse:
                Response of [FulfillIntent][]
        """
        # Create or coerce a protobuf request object.

        request = session.FulfillIntentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fulfill_intent,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "match_intent_request.session",
                        request.match_intent_request.session,
                    ),
                )
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SessionsAsyncClient",)
