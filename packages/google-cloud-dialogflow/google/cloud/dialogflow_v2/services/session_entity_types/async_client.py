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

from google.cloud.dialogflow_v2.services.session_entity_types import pagers
from google.cloud.dialogflow_v2.types import entity_type
from google.cloud.dialogflow_v2.types import session_entity_type
from google.cloud.dialogflow_v2.types import (
    session_entity_type as gcd_session_entity_type,
)
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import SessionEntityTypesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SessionEntityTypesGrpcAsyncIOTransport
from .client import SessionEntityTypesClient


class SessionEntityTypesAsyncClient:
    """Service for managing
    [SessionEntityTypes][google.cloud.dialogflow.v2.SessionEntityType].
    """

    _client: SessionEntityTypesClient

    DEFAULT_ENDPOINT = SessionEntityTypesClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SessionEntityTypesClient.DEFAULT_MTLS_ENDPOINT

    session_entity_type_path = staticmethod(
        SessionEntityTypesClient.session_entity_type_path
    )
    parse_session_entity_type_path = staticmethod(
        SessionEntityTypesClient.parse_session_entity_type_path
    )
    common_billing_account_path = staticmethod(
        SessionEntityTypesClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        SessionEntityTypesClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SessionEntityTypesClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        SessionEntityTypesClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        SessionEntityTypesClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        SessionEntityTypesClient.parse_common_organization_path
    )
    common_project_path = staticmethod(SessionEntityTypesClient.common_project_path)
    parse_common_project_path = staticmethod(
        SessionEntityTypesClient.parse_common_project_path
    )
    common_location_path = staticmethod(SessionEntityTypesClient.common_location_path)
    parse_common_location_path = staticmethod(
        SessionEntityTypesClient.parse_common_location_path
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
            SessionEntityTypesAsyncClient: The constructed client.
        """
        return SessionEntityTypesClient.from_service_account_info.__func__(SessionEntityTypesAsyncClient, info, *args, **kwargs)  # type: ignore

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
            SessionEntityTypesAsyncClient: The constructed client.
        """
        return SessionEntityTypesClient.from_service_account_file.__func__(SessionEntityTypesAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SessionEntityTypesTransport:
        """Returns the transport used by the client instance.

        Returns:
            SessionEntityTypesTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(SessionEntityTypesClient).get_transport_class,
        type(SessionEntityTypesClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, SessionEntityTypesTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the session entity types client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SessionEntityTypesTransport]): The
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
        self._client = SessionEntityTypesClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_session_entity_types(
        self,
        request: session_entity_type.ListSessionEntityTypesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSessionEntityTypesAsyncPager:
        r"""Returns the list of all session entity types in the
        specified session.
        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.ListSessionEntityTypesRequest`):
                The request object. The request message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.v2.SessionEntityTypes.ListSessionEntityTypes].
            parent (:class:`str`):
                Required. The session to list all session entity types
                from. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>`` or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/ sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment. If ``User ID`` is not
                specified, we assume default '-' user.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.services.session_entity_types.pagers.ListSessionEntityTypesAsyncPager:
                The response message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.v2.SessionEntityTypes.ListSessionEntityTypes].

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

        request = session_entity_type.ListSessionEntityTypesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_session_entity_types,
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
        response = pagers.ListSessionEntityTypesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_session_entity_type(
        self,
        request: session_entity_type.GetSessionEntityTypeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session_entity_type.SessionEntityType:
        r"""Retrieves the specified session entity type.
        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.GetSessionEntityTypeRequest`):
                The request object. The request message for
                [SessionEntityTypes.GetSessionEntityType][google.cloud.dialogflow.v2.SessionEntityTypes.GetSessionEntityType].
            name (:class:`str`):
                Required. The name of the session entity type. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment. If ``User ID`` is not
                specified, we assume default '-' user.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.SessionEntityType:
                A session represents a conversation between a Dialogflow agent and an
                   end-user. You can create special entities, called
                   session entities, during a session. Session entities
                   can extend or replace custom entity types and only
                   exist during the session that they were created for.
                   All session data, including session entities, is
                   stored by Dialogflow for 20 minutes.

                   For more information, see the [session entity
                   guide](\ https://cloud.google.com/dialogflow/docs/entities-session).

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

        request = session_entity_type.GetSessionEntityTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_session_entity_type,
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

    async def create_session_entity_type(
        self,
        request: gcd_session_entity_type.CreateSessionEntityTypeRequest = None,
        *,
        parent: str = None,
        session_entity_type: gcd_session_entity_type.SessionEntityType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_session_entity_type.SessionEntityType:
        r"""Creates a session entity type.
        If the specified session entity type already exists,
        overrides the session entity type.

        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.CreateSessionEntityTypeRequest`):
                The request object. The request message for
                [SessionEntityTypes.CreateSessionEntityType][google.cloud.dialogflow.v2.SessionEntityTypes.CreateSessionEntityType].
            parent (:class:`str`):
                Required. The session to create a session entity type
                for. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>`` or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/ sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment. If ``User ID`` is not
                specified, we assume default '-' user.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            session_entity_type (:class:`google.cloud.dialogflow_v2.types.SessionEntityType`):
                Required. The session entity type to
                create.

                This corresponds to the ``session_entity_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.SessionEntityType:
                A session represents a conversation between a Dialogflow agent and an
                   end-user. You can create special entities, called
                   session entities, during a session. Session entities
                   can extend or replace custom entity types and only
                   exist during the session that they were created for.
                   All session data, including session entities, is
                   stored by Dialogflow for 20 minutes.

                   For more information, see the [session entity
                   guide](\ https://cloud.google.com/dialogflow/docs/entities-session).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, session_entity_type])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_session_entity_type.CreateSessionEntityTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if session_entity_type is not None:
            request.session_entity_type = session_entity_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_session_entity_type,
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

    async def update_session_entity_type(
        self,
        request: gcd_session_entity_type.UpdateSessionEntityTypeRequest = None,
        *,
        session_entity_type: gcd_session_entity_type.SessionEntityType = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_session_entity_type.SessionEntityType:
        r"""Updates the specified session entity type.
        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.UpdateSessionEntityTypeRequest`):
                The request object. The request message for
                [SessionEntityTypes.UpdateSessionEntityType][google.cloud.dialogflow.v2.SessionEntityTypes.UpdateSessionEntityType].
            session_entity_type (:class:`google.cloud.dialogflow_v2.types.SessionEntityType`):
                Required. The session entity type to
                update.

                This corresponds to the ``session_entity_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. The mask to control which
                fields get updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.SessionEntityType:
                A session represents a conversation between a Dialogflow agent and an
                   end-user. You can create special entities, called
                   session entities, during a session. Session entities
                   can extend or replace custom entity types and only
                   exist during the session that they were created for.
                   All session data, including session entities, is
                   stored by Dialogflow for 20 minutes.

                   For more information, see the [session entity
                   guide](\ https://cloud.google.com/dialogflow/docs/entities-session).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([session_entity_type, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_session_entity_type.UpdateSessionEntityTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if session_entity_type is not None:
            request.session_entity_type = session_entity_type
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_session_entity_type,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("session_entity_type.name", request.session_entity_type.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_session_entity_type(
        self,
        request: session_entity_type.DeleteSessionEntityTypeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified session entity type.
        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.DeleteSessionEntityTypeRequest`):
                The request object. The request message for
                [SessionEntityTypes.DeleteSessionEntityType][google.cloud.dialogflow.v2.SessionEntityTypes.DeleteSessionEntityType].
            name (:class:`str`):
                Required. The name of the entity type to delete. Format:
                ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                or
                ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment. If ``User ID`` is not
                specified, we assume default '-' user.

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

        request = session_entity_type.DeleteSessionEntityTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_session_entity_type,
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


__all__ = ("SessionEntityTypesAsyncClient",)
