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

from google.cloud.dialogflow_v2.types import audio_config
from google.cloud.dialogflow_v2.types import session
from google.cloud.dialogflow_v2.types import session as gcd_session
from google.rpc import status_pb2  # type: ignore
from .transports.base import SessionsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SessionsGrpcAsyncIOTransport
from .client import SessionsClient


class SessionsAsyncClient:
    """A service used for session interactions.

    For more information, see the `API interactions
    guide <https://cloud.google.com/dialogflow/docs/api-overview>`__.
    """

    _client: SessionsClient

    DEFAULT_ENDPOINT = SessionsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SessionsClient.DEFAULT_MTLS_ENDPOINT

    context_path = staticmethod(SessionsClient.context_path)
    parse_context_path = staticmethod(SessionsClient.parse_context_path)
    intent_path = staticmethod(SessionsClient.intent_path)
    parse_intent_path = staticmethod(SessionsClient.parse_intent_path)
    session_path = staticmethod(SessionsClient.session_path)
    parse_session_path = staticmethod(SessionsClient.parse_session_path)
    session_entity_type_path = staticmethod(SessionsClient.session_entity_type_path)
    parse_session_entity_type_path = staticmethod(
        SessionsClient.parse_session_entity_type_path
    )
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
        request: gcd_session.DetectIntentRequest = None,
        *,
        session: str = None,
        query_input: gcd_session.QueryInput = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_session.DetectIntentResponse:
        r"""Processes a natural language query and returns structured,
        actionable data as a result. This method is not idempotent,
        because it may cause contexts and session entity types to be
        updated, which in turn might affect results of future queries.

        Note: Always use agent versions for production traffic. See
        `Versions and
        environments <https://cloud.google.com/dialogflow/es/docs/agents-versions>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.DetectIntentRequest`):
                The request object. The request to detect user's intent.
            session (:class:`str`):
                Required. The name of the session this query is sent to.
                Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>``,
                or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment (``Environment ID`` might be
                referred to as environment name at some places). If
                ``User ID`` is not specified, we are using "-". It's up
                to the API caller to choose an appropriate
                ``Session ID`` and ``User Id``. They can be a random
                number or some type of user and session identifiers
                (preferably hashed). The length of the ``Session ID``
                and ``User ID`` must not exceed 36 characters.

                For more information, see the `API interactions
                guide <https://cloud.google.com/dialogflow/docs/api-overview>`__.

                Note: Always use agent versions for production traffic.
                See `Versions and
                environments <https://cloud.google.com/dialogflow/es/docs/agents-versions>`__.

                This corresponds to the ``session`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query_input (:class:`google.cloud.dialogflow_v2.types.QueryInput`):
                Required. The input specification. It
                can be set to:
                1.  an audio config
                    which instructs the speech
                recognizer how to process the speech
                audio,
                2.  a conversational query in the form
                of text, or
                3.  an event that specifies which intent
                to trigger.

                This corresponds to the ``query_input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.DetectIntentResponse:
                The message returned from the
                DetectIntent method.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([session, query_input])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_session.DetectIntentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if session is not None:
            request.session = session
        if query_input is not None:
            request.query_input = query_input

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
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[session.StreamingDetectIntentResponse]]:
        r"""Processes a natural language query in audio format in a
        streaming fashion and returns structured, actionable data as a
        result. This method is only available via the gRPC API (not
        REST).

        Note: Always use agent versions for production traffic. See
        `Versions and
        environments <https://cloud.google.com/dialogflow/es/docs/agents-versions>`__.

        Args:
            requests (AsyncIterator[`google.cloud.dialogflow_v2.types.StreamingDetectIntentRequest`]):
                The request object AsyncIterator. The top-level message sent by the
                client to the
                [Sessions.StreamingDetectIntent][google.cloud.dialogflow.v2.Sessions.StreamingDetectIntent]
                method.
                Multiple request messages should be sent in order:

                1.  The first message must contain
                [session][google.cloud.dialogflow.v2.StreamingDetectIntentRequest.session],
                [query_input][google.cloud.dialogflow.v2.StreamingDetectIntentRequest.query_input]
                plus optionally
                [query_params][google.cloud.dialogflow.v2.StreamingDetectIntentRequest.query_params].
                If the client     wants to receive an audio response, it
                should also contain
                [output_audio_config][google.cloud.dialogflow.v2.StreamingDetectIntentRequest.output_audio_config].
                The message must not contain
                [input_audio][google.cloud.dialogflow.v2.StreamingDetectIntentRequest.input_audio].
                2.  If
                [query_input][google.cloud.dialogflow.v2.StreamingDetectIntentRequest.query_input]
                was set to
                [query_input.audio_config][google.cloud.dialogflow.v2.InputAudioConfig],
                all subsequent     messages must contain
                [input_audio][google.cloud.dialogflow.v2.StreamingDetectIntentRequest.input_audio]
                to continue with     Speech recognition.
                    If you decide to rather detect an intent from text
                input after you     already started Speech recognition,
                please send a message with
                [query_input.text][google.cloud.dialogflow.v2.QueryInput.text].
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
            AsyncIterable[google.cloud.dialogflow_v2.types.StreamingDetectIntentResponse]:
                The top-level message returned from the
                   StreamingDetectIntent method.

                   Multiple response messages can be returned in order:

                   1. If the input was set to streaming audio, the first
                      one or more messages contain recognition_result.
                      Each recognition_result represents a more complete
                      transcript of what the user said. The last
                      recognition_result has is_final set to true.
                   2. The next message contains response_id,
                      query_result and optionally webhook_status if a
                      WebHook was called.

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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SessionsAsyncClient",)
