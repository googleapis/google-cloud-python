# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union
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

from google.cloud.dialogflowcx_v3.services.session_entity_types import pagers
from google.cloud.dialogflowcx_v3.types import entity_type
from google.cloud.dialogflowcx_v3.types import session_entity_type
from google.cloud.dialogflowcx_v3.types import (
    session_entity_type as gcdc_session_entity_type,
)
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import SessionEntityTypesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SessionEntityTypesGrpcAsyncIOTransport
from .client import SessionEntityTypesClient


class SessionEntityTypesAsyncClient:
    """Service for managing
    [SessionEntityTypes][google.cloud.dialogflow.cx.v3.SessionEntityType].
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

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return SessionEntityTypesClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

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
        request: Union[session_entity_type.ListSessionEntityTypesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSessionEntityTypesAsyncPager:
        r"""Returns the list of all session entity types in the
        specified session.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_list_session_entity_types():
                # Create a client
                client = dialogflowcx_v3.SessionEntityTypesAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3.ListSessionEntityTypesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_session_entity_types(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.ListSessionEntityTypesRequest, dict]):
                The request object. The request message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.cx.v3.SessionEntityTypes.ListSessionEntityTypes].
            parent (:class:`str`):
                Required. The session to list all session entity types
                from. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.services.session_entity_types.pagers.ListSessionEntityTypesAsyncPager:
                The response message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.cx.v3.SessionEntityTypes.ListSessionEntityTypes].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSessionEntityTypesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_session_entity_type(
        self,
        request: Union[session_entity_type.GetSessionEntityTypeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session_entity_type.SessionEntityType:
        r"""Retrieves the specified session entity type.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_get_session_entity_type():
                # Create a client
                client = dialogflowcx_v3.SessionEntityTypesAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3.GetSessionEntityTypeRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_session_entity_type(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.GetSessionEntityTypeRequest, dict]):
                The request object. The request message for
                [SessionEntityTypes.GetSessionEntityType][google.cloud.dialogflow.cx.v3.SessionEntityTypes.GetSessionEntityType].
            name (:class:`str`):
                Required. The name of the session entity type. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.SessionEntityType:
                Session entity types are referred to as **User** entity types and are
                   entities that are built for an individual user such
                   as favorites, preferences, playlists, and so on.

                   You can redefine a session entity type at the session
                   level to extend or replace a [custom entity
                   type][google.cloud.dialogflow.cx.v3.EntityType] at
                   the user session level (we refer to the entity types
                   defined at the agent level as "custom entity types").

                   Note: session entity types apply to all queries,
                   regardless of the language.

                   For more information about entity types, see the
                   [Dialogflow
                   documentation](\ https://cloud.google.com/dialogflow/docs/entities-overview).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_session_entity_type(
        self,
        request: Union[
            gcdc_session_entity_type.CreateSessionEntityTypeRequest, dict
        ] = None,
        *,
        parent: str = None,
        session_entity_type: gcdc_session_entity_type.SessionEntityType = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_session_entity_type.SessionEntityType:
        r"""Creates a session entity type.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_create_session_entity_type():
                # Create a client
                client = dialogflowcx_v3.SessionEntityTypesAsyncClient()

                # Initialize request argument(s)
                session_entity_type = dialogflowcx_v3.SessionEntityType()
                session_entity_type.name = "name_value"
                session_entity_type.entity_override_mode = "ENTITY_OVERRIDE_MODE_SUPPLEMENT"
                session_entity_type.entities.value = "value_value"
                session_entity_type.entities.synonyms = ['synonyms_value_1', 'synonyms_value_2']

                request = dialogflowcx_v3.CreateSessionEntityTypeRequest(
                    parent="parent_value",
                    session_entity_type=session_entity_type,
                )

                # Make the request
                response = await client.create_session_entity_type(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.CreateSessionEntityTypeRequest, dict]):
                The request object. The request message for
                [SessionEntityTypes.CreateSessionEntityType][google.cloud.dialogflow.cx.v3.SessionEntityTypes.CreateSessionEntityType].
            parent (:class:`str`):
                Required. The session to create a session entity type
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            session_entity_type (:class:`google.cloud.dialogflowcx_v3.types.SessionEntityType`):
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
            google.cloud.dialogflowcx_v3.types.SessionEntityType:
                Session entity types are referred to as **User** entity types and are
                   entities that are built for an individual user such
                   as favorites, preferences, playlists, and so on.

                   You can redefine a session entity type at the session
                   level to extend or replace a [custom entity
                   type][google.cloud.dialogflow.cx.v3.EntityType] at
                   the user session level (we refer to the entity types
                   defined at the agent level as "custom entity types").

                   Note: session entity types apply to all queries,
                   regardless of the language.

                   For more information about entity types, see the
                   [Dialogflow
                   documentation](\ https://cloud.google.com/dialogflow/docs/entities-overview).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, session_entity_type])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_session_entity_type.CreateSessionEntityTypeRequest(request)

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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_session_entity_type(
        self,
        request: Union[
            gcdc_session_entity_type.UpdateSessionEntityTypeRequest, dict
        ] = None,
        *,
        session_entity_type: gcdc_session_entity_type.SessionEntityType = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_session_entity_type.SessionEntityType:
        r"""Updates the specified session entity type.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_update_session_entity_type():
                # Create a client
                client = dialogflowcx_v3.SessionEntityTypesAsyncClient()

                # Initialize request argument(s)
                session_entity_type = dialogflowcx_v3.SessionEntityType()
                session_entity_type.name = "name_value"
                session_entity_type.entity_override_mode = "ENTITY_OVERRIDE_MODE_SUPPLEMENT"
                session_entity_type.entities.value = "value_value"
                session_entity_type.entities.synonyms = ['synonyms_value_1', 'synonyms_value_2']

                request = dialogflowcx_v3.UpdateSessionEntityTypeRequest(
                    session_entity_type=session_entity_type,
                )

                # Make the request
                response = await client.update_session_entity_type(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.UpdateSessionEntityTypeRequest, dict]):
                The request object. The request message for
                [SessionEntityTypes.UpdateSessionEntityType][google.cloud.dialogflow.cx.v3.SessionEntityTypes.UpdateSessionEntityType].
            session_entity_type (:class:`google.cloud.dialogflowcx_v3.types.SessionEntityType`):
                Required. The session entity type to update. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.

                This corresponds to the ``session_entity_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The mask to control which fields get
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.SessionEntityType:
                Session entity types are referred to as **User** entity types and are
                   entities that are built for an individual user such
                   as favorites, preferences, playlists, and so on.

                   You can redefine a session entity type at the session
                   level to extend or replace a [custom entity
                   type][google.cloud.dialogflow.cx.v3.EntityType] at
                   the user session level (we refer to the entity types
                   defined at the agent level as "custom entity types").

                   Note: session entity types apply to all queries,
                   regardless of the language.

                   For more information about entity types, see the
                   [Dialogflow
                   documentation](\ https://cloud.google.com/dialogflow/docs/entities-overview).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([session_entity_type, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_session_entity_type.UpdateSessionEntityTypeRequest(request)

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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_session_entity_type(
        self,
        request: Union[session_entity_type.DeleteSessionEntityTypeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified session entity type.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_delete_session_entity_type():
                # Create a client
                client = dialogflowcx_v3.SessionEntityTypesAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3.DeleteSessionEntityTypeRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_session_entity_type(request=request)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.DeleteSessionEntityTypeRequest, dict]):
                The request object. The request message for
                [SessionEntityTypes.DeleteSessionEntityType][google.cloud.dialogflow.cx.v3.SessionEntityTypes.DeleteSessionEntityType].
            name (:class:`str`):
                Required. The name of the session entity type to delete.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.

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
        # Quick check: If we got a request object, we should *not* have
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

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


__all__ = ("SessionEntityTypesAsyncClient",)
