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

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.dialogflowcx_v3.types import audio_config
from google.cloud.dialogflowcx_v3.types import page
from google.cloud.dialogflowcx_v3.types import session
from .transports.base import SessionsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SessionsGrpcAsyncIOTransport
from .client import SessionsClient


class SessionsAsyncClient:
    """A session represents an interaction with a user. You retrieve user
    input and pass it to the
    [DetectIntent][google.cloud.dialogflow.cx.v3.Sessions.DetectIntent]
    method to determine user intent and respond.
    """

    _client: SessionsClient

    DEFAULT_ENDPOINT = SessionsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SessionsClient.DEFAULT_MTLS_ENDPOINT

    entity_type_path = staticmethod(SessionsClient.entity_type_path)
    parse_entity_type_path = staticmethod(SessionsClient.parse_entity_type_path)
    flow_path = staticmethod(SessionsClient.flow_path)
    parse_flow_path = staticmethod(SessionsClient.parse_flow_path)
    intent_path = staticmethod(SessionsClient.intent_path)
    parse_intent_path = staticmethod(SessionsClient.parse_intent_path)
    page_path = staticmethod(SessionsClient.page_path)
    parse_page_path = staticmethod(SessionsClient.parse_page_path)
    session_path = staticmethod(SessionsClient.session_path)
    parse_session_path = staticmethod(SessionsClient.parse_session_path)
    session_entity_type_path = staticmethod(SessionsClient.session_entity_type_path)
    parse_session_entity_type_path = staticmethod(
        SessionsClient.parse_session_entity_type_path
    )
    transition_route_group_path = staticmethod(
        SessionsClient.transition_route_group_path
    )
    parse_transition_route_group_path = staticmethod(
        SessionsClient.parse_transition_route_group_path
    )
    version_path = staticmethod(SessionsClient.version_path)
    parse_version_path = staticmethod(SessionsClient.parse_version_path)
    webhook_path = staticmethod(SessionsClient.webhook_path)
    parse_webhook_path = staticmethod(SessionsClient.parse_webhook_path)
    common_billing_account_path = staticmethod(
        SessionsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        SessionsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SessionsClient.common_folder_path)
    parse_common_folder_path = staticmethod(SessionsClient.parse_common_folder_path)
    common_organization_path = staticmethod(SessionsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        SessionsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(SessionsClient.common_project_path)
    parse_common_project_path = staticmethod(SessionsClient.parse_common_project_path)
    common_location_path = staticmethod(SessionsClient.common_location_path)
    parse_common_location_path = staticmethod(SessionsClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SessionsAsyncClient: The constructed client.
        """
        return SessionsClient.from_service_account_info.__func__(SessionsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            SessionsAsyncClient: The constructed client.
        """
        return SessionsClient.from_service_account_file.__func__(SessionsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SessionsTransport:
        """Returns the transport used by the client instance.

        Returns:
            SessionsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(SessionsClient).get_transport_class, type(SessionsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, SessionsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the sessions client.

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
        self._client = SessionsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def detect_intent(
        self,
        request: Union[session.DetectIntentRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session.DetectIntentResponse:
        r"""Processes a natural language query and returns structured,
        actionable data as a result. This method is not idempotent,
        because it may cause session entity types to be updated, which
        in turn might affect results of future queries.

        Note: Always use agent versions for production traffic. See
        `Versions and
        environments <https://cloud.google.com/dialogflow/cx/docs/concept/version>`__.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.DetectIntentRequest, dict]):
                The request object. The request to detect user's intent.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.DetectIntentResponse:
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
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=220.0,
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
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[session.StreamingDetectIntentResponse]]:
        r"""Processes a natural language query in audio format in a
        streaming fashion and returns structured, actionable data as a
        result. This method is only available via the gRPC API (not
        REST).

        Note: Always use agent versions for production traffic. See
        `Versions and
        environments <https://cloud.google.com/dialogflow/cx/docs/concept/version>`__.

        Args:
            requests (AsyncIterator[`google.cloud.dialogflowcx_v3.types.StreamingDetectIntentRequest`]):
                The request object AsyncIterator. The top-level message sent by the
                client to the
                [Sessions.StreamingDetectIntent][google.cloud.dialogflow.cx.v3.Sessions.StreamingDetectIntent]
                method.
                Multiple request messages should be sent in order:

                1.  The first message must contain
                [session][google.cloud.dialogflow.cx.v3.StreamingDetectIntentRequest.session],
                [query_input][google.cloud.dialogflow.cx.v3.StreamingDetectIntentRequest.query_input]
                plus optionally
                [query_params][google.cloud.dialogflow.cx.v3.StreamingDetectIntentRequest.query_params].
                If the client     wants to receive an audio response, it
                should also contain
                [output_audio_config][google.cloud.dialogflow.cx.v3.StreamingDetectIntentRequest.output_audio_config].
                2.  If
                [query_input][google.cloud.dialogflow.cx.v3.StreamingDetectIntentRequest.query_input]
                was set to
                [query_input.audio.config][google.cloud.dialogflow.cx.v3.AudioInput.config],
                all subsequent messages     must contain
                [query_input.audio.audio][google.cloud.dialogflow.cx.v3.AudioInput.audio]
                to continue with     Speech recognition.
                    If you decide to rather detect an intent from text
                input after you already started Speech recognition,
                please send a message     with
                [query_input.text][google.cloud.dialogflow.cx.v3.QueryInput.text].
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
            AsyncIterable[google.cloud.dialogflowcx_v3.types.StreamingDetectIntentResponse]:
                The top-level message returned from the
                   [StreamingDetectIntent][google.cloud.dialogflow.cx.v3.Sessions.StreamingDetectIntent]
                   method.

                   Multiple response messages (N) can be returned in
                   order.

                   The first (N-1) responses set either the
                   recognition_result or detect_intent_response field,
                   depending on the request:

                   -  If the
                      StreamingDetectIntentRequest.query_input.audio
                      field was set, and the
                      StreamingDetectIntentRequest.enable_partial_response
                      field was false, the recognition_result field is
                      populated for each of the (N-1) responses. See the
                      [StreamingRecognitionResult][google.cloud.dialogflow.cx.v3.StreamingRecognitionResult]
                      message for details about the result message
                      sequence.
                   -  If the
                      StreamingDetectIntentRequest.enable_partial_response
                      field was true, the detect_intent_response field
                      is populated for each of the (N-1) responses,
                      where 1 <= N <= 4. These responses set the
                      [DetectIntentResponse.response_type][google.cloud.dialogflow.cx.v3.DetectIntentResponse.response_type]
                      field to PARTIAL.

                   For the final Nth response message, the
                   detect_intent_response is fully populated, and
                   [DetectIntentResponse.response_type][google.cloud.dialogflow.cx.v3.DetectIntentResponse.response_type]
                   is set to FINAL.

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
        request: Union[session.MatchIntentRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session.MatchIntentResponse:
        r"""Returns preliminary intent match results, doesn't
        change the session status.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.MatchIntentRequest, dict]):
                The request object. Request of [MatchIntent][].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.MatchIntentResponse:
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
        request: Union[session.FulfillIntentRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session.FulfillIntentResponse:
        r"""Fulfills a matched intent returned by
        [MatchIntent][google.cloud.dialogflow.cx.v3.Sessions.MatchIntent].
        Must be called after
        [MatchIntent][google.cloud.dialogflow.cx.v3.Sessions.MatchIntent],
        with input from
        [MatchIntentResponse][google.cloud.dialogflow.cx.v3.MatchIntentResponse].
        Otherwise, the behavior is undefined.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.FulfillIntentRequest, dict]):
                The request object. Request of [FulfillIntent][]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.FulfillIntentResponse:
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SessionsAsyncClient",)
