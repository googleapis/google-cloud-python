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
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dialogflow_v2.services.participants import pagers
from google.cloud.dialogflow_v2.types import participant
from google.cloud.dialogflow_v2.types import participant as gcd_participant
from google.cloud.dialogflow_v2.types import session
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import ParticipantsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ParticipantsGrpcAsyncIOTransport
from .client import ParticipantsClient


class ParticipantsAsyncClient:
    """Service for managing
    [Participants][google.cloud.dialogflow.v2.Participant].
    """

    _client: ParticipantsClient

    DEFAULT_ENDPOINT = ParticipantsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ParticipantsClient.DEFAULT_MTLS_ENDPOINT

    context_path = staticmethod(ParticipantsClient.context_path)
    parse_context_path = staticmethod(ParticipantsClient.parse_context_path)
    intent_path = staticmethod(ParticipantsClient.intent_path)
    parse_intent_path = staticmethod(ParticipantsClient.parse_intent_path)
    message_path = staticmethod(ParticipantsClient.message_path)
    parse_message_path = staticmethod(ParticipantsClient.parse_message_path)
    participant_path = staticmethod(ParticipantsClient.participant_path)
    parse_participant_path = staticmethod(ParticipantsClient.parse_participant_path)
    session_entity_type_path = staticmethod(ParticipantsClient.session_entity_type_path)
    parse_session_entity_type_path = staticmethod(
        ParticipantsClient.parse_session_entity_type_path
    )
    common_billing_account_path = staticmethod(
        ParticipantsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ParticipantsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ParticipantsClient.common_folder_path)
    parse_common_folder_path = staticmethod(ParticipantsClient.parse_common_folder_path)
    common_organization_path = staticmethod(ParticipantsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        ParticipantsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ParticipantsClient.common_project_path)
    parse_common_project_path = staticmethod(
        ParticipantsClient.parse_common_project_path
    )
    common_location_path = staticmethod(ParticipantsClient.common_location_path)
    parse_common_location_path = staticmethod(
        ParticipantsClient.parse_common_location_path
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
            ParticipantsAsyncClient: The constructed client.
        """
        return ParticipantsClient.from_service_account_info.__func__(ParticipantsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ParticipantsAsyncClient: The constructed client.
        """
        return ParticipantsClient.from_service_account_file.__func__(ParticipantsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ParticipantsTransport:
        """Returns the transport used by the client instance.

        Returns:
            ParticipantsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ParticipantsClient).get_transport_class, type(ParticipantsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ParticipantsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the participants client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ParticipantsTransport]): The
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
        self._client = ParticipantsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_participant(
        self,
        request: gcd_participant.CreateParticipantRequest = None,
        *,
        parent: str = None,
        participant: gcd_participant.Participant = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_participant.Participant:
        r"""Creates a new participant in a conversation.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.CreateParticipantRequest`):
                The request object. The request message for
                [Participants.CreateParticipant][google.cloud.dialogflow.v2.Participants.CreateParticipant].
            parent (:class:`str`):
                Required. Resource identifier of the conversation adding
                the participant. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            participant (:class:`google.cloud.dialogflow_v2.types.Participant`):
                Required. The participant to create.
                This corresponds to the ``participant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Participant:
                Represents a conversation participant
                (human agent, virtual agent, end-user).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, participant])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_participant.CreateParticipantRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if participant is not None:
            request.participant = participant

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_participant,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_participant(
        self,
        request: participant.GetParticipantRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> participant.Participant:
        r"""Retrieves a conversation participant.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.GetParticipantRequest`):
                The request object. The request message for
                [Participants.GetParticipant][google.cloud.dialogflow.v2.Participants.GetParticipant].
            name (:class:`str`):
                Required. The name of the participant. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Participant:
                Represents a conversation participant
                (human agent, virtual agent, end-user).

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

        request = participant.GetParticipantRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_participant,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_participants(
        self,
        request: participant.ListParticipantsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListParticipantsAsyncPager:
        r"""Returns the list of all participants in the specified
        conversation.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.ListParticipantsRequest`):
                The request object. The request message for
                [Participants.ListParticipants][google.cloud.dialogflow.v2.Participants.ListParticipants].
            parent (:class:`str`):
                Required. The conversation to list all participants
                from. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.services.participants.pagers.ListParticipantsAsyncPager:
                The response message for
                [Participants.ListParticipants][google.cloud.dialogflow.v2.Participants.ListParticipants].

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = participant.ListParticipantsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_participants,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListParticipantsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_participant(
        self,
        request: gcd_participant.UpdateParticipantRequest = None,
        *,
        participant: gcd_participant.Participant = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_participant.Participant:
        r"""Updates the specified participant.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.UpdateParticipantRequest`):
                The request object. The request message for
                [Participants.UpdateParticipant][google.cloud.dialogflow.v2.Participants.UpdateParticipant].
            participant (:class:`google.cloud.dialogflow_v2.types.Participant`):
                Required. The participant to update.
                This corresponds to the ``participant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to specify which
                fields to update.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Participant:
                Represents a conversation participant
                (human agent, virtual agent, end-user).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([participant, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_participant.UpdateParticipantRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if participant is not None:
            request.participant = participant
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_participant,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("participant.name", request.participant.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def analyze_content(
        self,
        request: gcd_participant.AnalyzeContentRequest = None,
        *,
        participant: str = None,
        text_input: session.TextInput = None,
        event_input: session.EventInput = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_participant.AnalyzeContentResponse:
        r"""Adds a text (chat, for example), or audio (phone recording, for
        example) message from a participant into the conversation.

        Note: Always use agent versions for production traffic sent to
        virtual agents. See `Versions and
        environments <https://cloud.google.com/dialogflow/es/docs/agents-versions>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.AnalyzeContentRequest`):
                The request object. The request message for
                [Participants.AnalyzeContent][google.cloud.dialogflow.v2.Participants.AnalyzeContent].
            participant (:class:`str`):
                Required. The name of the participant this text comes
                from. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.

                This corresponds to the ``participant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            text_input (:class:`google.cloud.dialogflow_v2.types.TextInput`):
                The natural language text to be
                processed.

                This corresponds to the ``text_input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event_input (:class:`google.cloud.dialogflow_v2.types.EventInput`):
                An input event to send to Dialogflow.
                This corresponds to the ``event_input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.AnalyzeContentResponse:
                The response message for
                [Participants.AnalyzeContent][google.cloud.dialogflow.v2.Participants.AnalyzeContent].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([participant, text_input, event_input])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_participant.AnalyzeContentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if participant is not None:
            request.participant = participant
        if text_input is not None:
            request.text_input = text_input
        if event_input is not None:
            request.event_input = event_input

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.analyze_content,
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("participant", request.participant),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def suggest_articles(
        self,
        request: participant.SuggestArticlesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> participant.SuggestArticlesResponse:
        r"""Gets suggested articles for a participant based on
        specific historical messages.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.SuggestArticlesRequest`):
                The request object. The request message for
                [Participants.SuggestArticles][google.cloud.dialogflow.v2.Participants.SuggestArticles].
            parent (:class:`str`):
                Required. The name of the participant to fetch
                suggestion for. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.SuggestArticlesResponse:
                The response message for
                [Participants.SuggestArticles][google.cloud.dialogflow.v2.Participants.SuggestArticles].

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

        request = participant.SuggestArticlesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.suggest_articles,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def suggest_faq_answers(
        self,
        request: participant.SuggestFaqAnswersRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> participant.SuggestFaqAnswersResponse:
        r"""Gets suggested faq answers for a participant based on
        specific historical messages.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.SuggestFaqAnswersRequest`):
                The request object. The request message for
                [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2.Participants.SuggestFaqAnswers].
            parent (:class:`str`):
                Required. The name of the participant to fetch
                suggestion for. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.SuggestFaqAnswersResponse:
                The request message for
                [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2.Participants.SuggestFaqAnswers].

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

        request = participant.SuggestFaqAnswersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.suggest_faq_answers,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

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


__all__ = ("ParticipantsAsyncClient",)
