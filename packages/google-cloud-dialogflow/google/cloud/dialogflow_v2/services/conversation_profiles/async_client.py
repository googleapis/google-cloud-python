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

from google.cloud.dialogflow_v2.services.conversation_profiles import pagers
from google.cloud.dialogflow_v2.types import audio_config
from google.cloud.dialogflow_v2.types import conversation_profile
from google.cloud.dialogflow_v2.types import (
    conversation_profile as gcd_conversation_profile,
)
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import ConversationProfilesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ConversationProfilesGrpcAsyncIOTransport
from .client import ConversationProfilesClient


class ConversationProfilesAsyncClient:
    """Service for managing
    [ConversationProfiles][google.cloud.dialogflow.v2.ConversationProfile].
    """

    _client: ConversationProfilesClient

    DEFAULT_ENDPOINT = ConversationProfilesClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ConversationProfilesClient.DEFAULT_MTLS_ENDPOINT

    agent_path = staticmethod(ConversationProfilesClient.agent_path)
    parse_agent_path = staticmethod(ConversationProfilesClient.parse_agent_path)
    conversation_model_path = staticmethod(
        ConversationProfilesClient.conversation_model_path
    )
    parse_conversation_model_path = staticmethod(
        ConversationProfilesClient.parse_conversation_model_path
    )
    conversation_profile_path = staticmethod(
        ConversationProfilesClient.conversation_profile_path
    )
    parse_conversation_profile_path = staticmethod(
        ConversationProfilesClient.parse_conversation_profile_path
    )
    document_path = staticmethod(ConversationProfilesClient.document_path)
    parse_document_path = staticmethod(ConversationProfilesClient.parse_document_path)
    knowledge_base_path = staticmethod(ConversationProfilesClient.knowledge_base_path)
    parse_knowledge_base_path = staticmethod(
        ConversationProfilesClient.parse_knowledge_base_path
    )
    common_billing_account_path = staticmethod(
        ConversationProfilesClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ConversationProfilesClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ConversationProfilesClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ConversationProfilesClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ConversationProfilesClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ConversationProfilesClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ConversationProfilesClient.common_project_path)
    parse_common_project_path = staticmethod(
        ConversationProfilesClient.parse_common_project_path
    )
    common_location_path = staticmethod(ConversationProfilesClient.common_location_path)
    parse_common_location_path = staticmethod(
        ConversationProfilesClient.parse_common_location_path
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
            ConversationProfilesAsyncClient: The constructed client.
        """
        return ConversationProfilesClient.from_service_account_info.__func__(ConversationProfilesAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ConversationProfilesAsyncClient: The constructed client.
        """
        return ConversationProfilesClient.from_service_account_file.__func__(ConversationProfilesAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ConversationProfilesTransport:
        """Returns the transport used by the client instance.

        Returns:
            ConversationProfilesTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ConversationProfilesClient).get_transport_class,
        type(ConversationProfilesClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ConversationProfilesTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the conversation profiles client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ConversationProfilesTransport]): The
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
        self._client = ConversationProfilesClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_conversation_profiles(
        self,
        request: conversation_profile.ListConversationProfilesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConversationProfilesAsyncPager:
        r"""Returns the list of all conversation profiles in the
        specified project.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.ListConversationProfilesRequest`):
                The request object. The request message for
                [ConversationProfiles.ListConversationProfiles][google.cloud.dialogflow.v2.ConversationProfiles.ListConversationProfiles].
            parent (:class:`str`):
                Required. The project to list all conversation profiles
                from. Format:
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
            google.cloud.dialogflow_v2.services.conversation_profiles.pagers.ListConversationProfilesAsyncPager:
                The response message for
                [ConversationProfiles.ListConversationProfiles][google.cloud.dialogflow.v2.ConversationProfiles.ListConversationProfiles].

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

        request = conversation_profile.ListConversationProfilesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_conversation_profiles,
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
        response = pagers.ListConversationProfilesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_conversation_profile(
        self,
        request: conversation_profile.GetConversationProfileRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> conversation_profile.ConversationProfile:
        r"""Retrieves the specified conversation profile.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.GetConversationProfileRequest`):
                The request object. The request message for
                [ConversationProfiles.GetConversationProfile][google.cloud.dialogflow.v2.ConversationProfiles.GetConversationProfile].
            name (:class:`str`):
                Required. The resource name of the conversation profile.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/conversationProfiles/<Conversation Profile ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.ConversationProfile:
                Defines the services to connect to
                incoming Dialogflow conversations.

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

        request = conversation_profile.GetConversationProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_conversation_profile,
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

    async def create_conversation_profile(
        self,
        request: gcd_conversation_profile.CreateConversationProfileRequest = None,
        *,
        parent: str = None,
        conversation_profile: gcd_conversation_profile.ConversationProfile = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_conversation_profile.ConversationProfile:
        r"""Creates a conversation profile in the specified project.

        [ConversationProfile.CreateTime][] and
        [ConversationProfile.UpdateTime][] aren't populated in the
        response. You can retrieve them via
        [GetConversationProfile][google.cloud.dialogflow.v2.ConversationProfiles.GetConversationProfile]
        API.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.CreateConversationProfileRequest`):
                The request object. The request message for
                [ConversationProfiles.CreateConversationProfile][google.cloud.dialogflow.v2.ConversationProfiles.CreateConversationProfile].
            parent (:class:`str`):
                Required. The project to create a conversation profile
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            conversation_profile (:class:`google.cloud.dialogflow_v2.types.ConversationProfile`):
                Required. The conversation profile to
                create.

                This corresponds to the ``conversation_profile`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.ConversationProfile:
                Defines the services to connect to
                incoming Dialogflow conversations.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, conversation_profile])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_conversation_profile.CreateConversationProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if conversation_profile is not None:
            request.conversation_profile = conversation_profile

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_conversation_profile,
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

    async def update_conversation_profile(
        self,
        request: gcd_conversation_profile.UpdateConversationProfileRequest = None,
        *,
        conversation_profile: gcd_conversation_profile.ConversationProfile = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_conversation_profile.ConversationProfile:
        r"""Updates the specified conversation profile.

        [ConversationProfile.CreateTime][] and
        [ConversationProfile.UpdateTime][] aren't populated in the
        response. You can retrieve them via
        [GetConversationProfile][google.cloud.dialogflow.v2.ConversationProfiles.GetConversationProfile]
        API.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.UpdateConversationProfileRequest`):
                The request object. The request message for
                [ConversationProfiles.UpdateConversationProfile][google.cloud.dialogflow.v2.ConversationProfiles.UpdateConversationProfile].
            conversation_profile (:class:`google.cloud.dialogflow_v2.types.ConversationProfile`):
                Required. The conversation profile to
                update.

                This corresponds to the ``conversation_profile`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to control which
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
            google.cloud.dialogflow_v2.types.ConversationProfile:
                Defines the services to connect to
                incoming Dialogflow conversations.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([conversation_profile, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_conversation_profile.UpdateConversationProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if conversation_profile is not None:
            request.conversation_profile = conversation_profile
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_conversation_profile,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("conversation_profile.name", request.conversation_profile.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_conversation_profile(
        self,
        request: conversation_profile.DeleteConversationProfileRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified conversation profile.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.DeleteConversationProfileRequest`):
                The request object. The request message for
                [ConversationProfiles.DeleteConversationProfile][google.cloud.dialogflow.v2.ConversationProfiles.DeleteConversationProfile].
                This operation fails if the conversation profile is
                still referenced from a phone number.
            name (:class:`str`):
                Required. The name of the conversation profile to
                delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversationProfiles/<Conversation Profile ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = conversation_profile.DeleteConversationProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_conversation_profile,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ConversationProfilesAsyncClient",)
