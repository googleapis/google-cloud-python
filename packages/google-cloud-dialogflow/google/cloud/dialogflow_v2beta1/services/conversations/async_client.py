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

from google.cloud.dialogflow_v2beta1.services.conversations import pagers
from google.cloud.dialogflow_v2beta1.types import conversation
from google.cloud.dialogflow_v2beta1.types import conversation as gcd_conversation
from google.cloud.dialogflow_v2beta1.types import participant
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import ConversationsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ConversationsGrpcAsyncIOTransport
from .client import ConversationsClient


class ConversationsAsyncClient:
    """Service for managing
    [Conversations][google.cloud.dialogflow.v2beta1.Conversation].
    """

    _client: ConversationsClient

    DEFAULT_ENDPOINT = ConversationsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ConversationsClient.DEFAULT_MTLS_ENDPOINT

    conversation_path = staticmethod(ConversationsClient.conversation_path)
    parse_conversation_path = staticmethod(ConversationsClient.parse_conversation_path)
    conversation_profile_path = staticmethod(
        ConversationsClient.conversation_profile_path
    )
    parse_conversation_profile_path = staticmethod(
        ConversationsClient.parse_conversation_profile_path
    )
    message_path = staticmethod(ConversationsClient.message_path)
    parse_message_path = staticmethod(ConversationsClient.parse_message_path)
    common_billing_account_path = staticmethod(
        ConversationsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ConversationsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ConversationsClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ConversationsClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ConversationsClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ConversationsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ConversationsClient.common_project_path)
    parse_common_project_path = staticmethod(
        ConversationsClient.parse_common_project_path
    )
    common_location_path = staticmethod(ConversationsClient.common_location_path)
    parse_common_location_path = staticmethod(
        ConversationsClient.parse_common_location_path
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
            ConversationsAsyncClient: The constructed client.
        """
        return ConversationsClient.from_service_account_info.__func__(ConversationsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ConversationsAsyncClient: The constructed client.
        """
        return ConversationsClient.from_service_account_file.__func__(ConversationsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ConversationsTransport:
        """Returns the transport used by the client instance.

        Returns:
            ConversationsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ConversationsClient).get_transport_class, type(ConversationsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ConversationsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the conversations client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ConversationsTransport]): The
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
        self._client = ConversationsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_conversation(
        self,
        request: gcd_conversation.CreateConversationRequest = None,
        *,
        parent: str = None,
        conversation: gcd_conversation.Conversation = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_conversation.Conversation:
        r"""Creates a new conversation. Conversations are auto-completed
        after 24 hours.

        Conversation Lifecycle: There are two stages during a
        conversation: Automated Agent Stage and Assist Stage.

        For Automated Agent Stage, there will be a dialogflow agent
        responding to user queries.

        For Assist Stage, there's no dialogflow agent responding to user
        queries. But we will provide suggestions which are generated
        from conversation.

        If
        [Conversation.conversation_profile][google.cloud.dialogflow.v2beta1.Conversation.conversation_profile]
        is configured for a dialogflow agent, conversation will start
        from ``Automated Agent Stage``, otherwise, it will start from
        ``Assist Stage``. And during ``Automated Agent Stage``, once an
        [Intent][google.cloud.dialogflow.v2beta1.Intent] with
        [Intent.live_agent_handoff][google.cloud.dialogflow.v2beta1.Intent.live_agent_handoff]
        is triggered, conversation will transfer to Assist Stage.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.CreateConversationRequest`):
                The request object. The request message for
                [Conversations.CreateConversation][google.cloud.dialogflow.v2beta1.Conversations.CreateConversation].
            parent (:class:`str`):
                Required. Resource identifier of the project creating
                the conversation. Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            conversation (:class:`google.cloud.dialogflow_v2beta1.types.Conversation`):
                Required. The conversation to create.
                This corresponds to the ``conversation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.Conversation:
                Represents a conversation.
                A conversation is an interaction between
                an agent, including live agents and
                Dialogflow agents, and a support
                customer. Conversations can include
                phone calls and text-based chat
                sessions.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, conversation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_conversation.CreateConversationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if conversation is not None:
            request.conversation = conversation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_conversation,
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

    async def list_conversations(
        self,
        request: conversation.ListConversationsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConversationsAsyncPager:
        r"""Returns the list of all conversations in the
        specified project.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.ListConversationsRequest`):
                The request object. The request message for
                [Conversations.ListConversations][google.cloud.dialogflow.v2beta1.Conversations.ListConversations].
            parent (:class:`str`):
                Required. The project from which to list all
                conversation. Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.services.conversations.pagers.ListConversationsAsyncPager:
                The response message for
                [Conversations.ListConversations][google.cloud.dialogflow.v2beta1.Conversations.ListConversations].

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

        request = conversation.ListConversationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_conversations,
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
        response = pagers.ListConversationsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_conversation(
        self,
        request: conversation.GetConversationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> conversation.Conversation:
        r"""Retrieves the specific conversation.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.GetConversationRequest`):
                The request object. The request message for
                [Conversations.GetConversation][google.cloud.dialogflow.v2beta1.Conversations.GetConversation].
            name (:class:`str`):
                Required. The name of the conversation. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.Conversation:
                Represents a conversation.
                A conversation is an interaction between
                an agent, including live agents and
                Dialogflow agents, and a support
                customer. Conversations can include
                phone calls and text-based chat
                sessions.

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

        request = conversation.GetConversationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_conversation,
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

    async def complete_conversation(
        self,
        request: conversation.CompleteConversationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> conversation.Conversation:
        r"""Completes the specified conversation. Finished
        conversations are purged from the database after 30
        days.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.CompleteConversationRequest`):
                The request object. The request message for
                [Conversations.CompleteConversation][google.cloud.dialogflow.v2beta1.Conversations.CompleteConversation].
            name (:class:`str`):
                Required. Resource identifier of the conversation to
                close. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.Conversation:
                Represents a conversation.
                A conversation is an interaction between
                an agent, including live agents and
                Dialogflow agents, and a support
                customer. Conversations can include
                phone calls and text-based chat
                sessions.

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

        request = conversation.CompleteConversationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.complete_conversation,
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

    async def batch_create_messages(
        self,
        request: conversation.BatchCreateMessagesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> conversation.BatchCreateMessagesResponse:
        r"""Batch ingests messages to conversation. Customers can
        use this RPC to ingest historical messages to
        conversation.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.BatchCreateMessagesRequest`):
                The request object. The request message for
                [Conversations.BatchCreateMessagesRequest][].
            parent (:class:`str`):
                Required. Resource identifier of the conversation to
                create message. Format:
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
            google.cloud.dialogflow_v2beta1.types.BatchCreateMessagesResponse:
                The request message for
                [Conversations.BatchCreateMessagesResponse][].

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

        request = conversation.BatchCreateMessagesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_create_messages,
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

    async def list_messages(
        self,
        request: conversation.ListMessagesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMessagesAsyncPager:
        r"""Lists messages that belong to a given conversation. ``messages``
        are ordered by ``create_time`` in descending order. To fetch
        updates without duplication, send request with filter
        ``create_time_epoch_microseconds > [first item's create_time of previous request]``
        and empty page_token.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.ListMessagesRequest`):
                The request object. The request message for
                [Conversations.ListMessages][google.cloud.dialogflow.v2beta1.Conversations.ListMessages].
            parent (:class:`str`):
                Required. The name of the conversation to list messages
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.services.conversations.pagers.ListMessagesAsyncPager:
                The response message for
                [Conversations.ListMessages][google.cloud.dialogflow.v2beta1.Conversations.ListMessages].

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

        request = conversation.ListMessagesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_messages,
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
        response = pagers.ListMessagesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

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


__all__ = ("ConversationsAsyncClient",)
