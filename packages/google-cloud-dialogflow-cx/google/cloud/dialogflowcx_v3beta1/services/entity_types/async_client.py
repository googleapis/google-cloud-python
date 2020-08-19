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
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dialogflowcx_v3beta1.services.entity_types import pagers
from google.cloud.dialogflowcx_v3beta1.types import entity_type
from google.cloud.dialogflowcx_v3beta1.types import entity_type as gcdc_entity_type
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore

from .transports.base import EntityTypesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import EntityTypesGrpcAsyncIOTransport
from .client import EntityTypesClient


class EntityTypesAsyncClient:
    """Service for managing
    [EntityTypes][google.cloud.dialogflow.cx.v3beta1.EntityType].
    """

    _client: EntityTypesClient

    DEFAULT_ENDPOINT = EntityTypesClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = EntityTypesClient.DEFAULT_MTLS_ENDPOINT

    entity_type_path = staticmethod(EntityTypesClient.entity_type_path)

    from_service_account_file = EntityTypesClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(EntityTypesClient).get_transport_class, type(EntityTypesClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, EntityTypesTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the entity types client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.EntityTypesTransport]): The
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

        self._client = EntityTypesClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_entity_types(
        self,
        request: entity_type.ListEntityTypesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEntityTypesAsyncPager:
        r"""Returns the list of all entity types in the specified
        agent.

        Args:
            request (:class:`~.entity_type.ListEntityTypesRequest`):
                The request object. The request message for
                [EntityTypes.ListEntityTypes][google.cloud.dialogflow.cx.v3beta1.EntityTypes.ListEntityTypes].
            parent (:class:`str`):
                Required. The agent to list all entity types for.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListEntityTypesAsyncPager:
                The response message for
                [EntityTypes.ListEntityTypes][google.cloud.dialogflow.cx.v3beta1.EntityTypes.ListEntityTypes].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = entity_type.ListEntityTypesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_entity_types,
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
        response = pagers.ListEntityTypesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_entity_type(
        self,
        request: entity_type.GetEntityTypeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> entity_type.EntityType:
        r"""Retrieves the specified entity type.

        Args:
            request (:class:`~.entity_type.GetEntityTypeRequest`):
                The request object. The request message for
                [EntityTypes.GetEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.GetEntityType].
            name (:class:`str`):
                Required. The name of the entity type. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/entityTypes/<Entity Type ID>``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.entity_type.EntityType:
                Entities are extracted from user input and represent
                parameters that are meaningful to your application. For
                example, a date range, a proper name such as a
                geographic location or landmark, and so on. Entities
                represent actionable data for your application.

                When you define an entity, you can also include synonyms
                that all map to that entity. For example, "soft drink",
                "soda", "pop", and so on.

                There are three types of entities:

                -  **System** - entities that are defined by the
                   Dialogflow API for common data types such as date,
                   time, currency, and so on. A system entity is
                   represented by the ``EntityType`` type.

                -  **Custom** - entities that are defined by you that
                   represent actionable data that is meaningful to your
                   application. For example, you could define a
                   ``pizza.sauce`` entity for red or white pizza sauce,
                   a ``pizza.cheese`` entity for the different types of
                   cheese on a pizza, a ``pizza.topping`` entity for
                   different toppings, and so on. A custom entity is
                   represented by the ``EntityType`` type.

                -  **User** - entities that are built for an individual
                   user such as favorites, preferences, playlists, and
                   so on. A user entity is represented by the
                   [SessionEntityType][google.cloud.dialogflow.cx.v3beta1.SessionEntityType]
                   type.

                For more information about entity types, see the
                `Dialogflow
                documentation <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = entity_type.GetEntityTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_entity_type,
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

    async def create_entity_type(
        self,
        request: gcdc_entity_type.CreateEntityTypeRequest = None,
        *,
        parent: str = None,
        entity_type: gcdc_entity_type.EntityType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_entity_type.EntityType:
        r"""Creates an entity type in the specified agent.

        Args:
            request (:class:`~.gcdc_entity_type.CreateEntityTypeRequest`):
                The request object. The request message for
                [EntityTypes.CreateEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.CreateEntityType].
            parent (:class:`str`):
                Required. The agent to create a entity type for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entity_type (:class:`~.gcdc_entity_type.EntityType`):
                Required. The entity type to create.
                This corresponds to the ``entity_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcdc_entity_type.EntityType:
                Entities are extracted from user input and represent
                parameters that are meaningful to your application. For
                example, a date range, a proper name such as a
                geographic location or landmark, and so on. Entities
                represent actionable data for your application.

                When you define an entity, you can also include synonyms
                that all map to that entity. For example, "soft drink",
                "soda", "pop", and so on.

                There are three types of entities:

                -  **System** - entities that are defined by the
                   Dialogflow API for common data types such as date,
                   time, currency, and so on. A system entity is
                   represented by the ``EntityType`` type.

                -  **Custom** - entities that are defined by you that
                   represent actionable data that is meaningful to your
                   application. For example, you could define a
                   ``pizza.sauce`` entity for red or white pizza sauce,
                   a ``pizza.cheese`` entity for the different types of
                   cheese on a pizza, a ``pizza.topping`` entity for
                   different toppings, and so on. A custom entity is
                   represented by the ``EntityType`` type.

                -  **User** - entities that are built for an individual
                   user such as favorites, preferences, playlists, and
                   so on. A user entity is represented by the
                   [SessionEntityType][google.cloud.dialogflow.cx.v3beta1.SessionEntityType]
                   type.

                For more information about entity types, see the
                `Dialogflow
                documentation <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, entity_type]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_entity_type.CreateEntityTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if entity_type is not None:
            request.entity_type = entity_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_entity_type,
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

    async def update_entity_type(
        self,
        request: gcdc_entity_type.UpdateEntityTypeRequest = None,
        *,
        entity_type: gcdc_entity_type.EntityType = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_entity_type.EntityType:
        r"""Updates the specified entity type.

        Args:
            request (:class:`~.gcdc_entity_type.UpdateEntityTypeRequest`):
                The request object. The request message for
                [EntityTypes.UpdateEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.UpdateEntityType].
            entity_type (:class:`~.gcdc_entity_type.EntityType`):
                Required. The entity type to update.
                This corresponds to the ``entity_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
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
            ~.gcdc_entity_type.EntityType:
                Entities are extracted from user input and represent
                parameters that are meaningful to your application. For
                example, a date range, a proper name such as a
                geographic location or landmark, and so on. Entities
                represent actionable data for your application.

                When you define an entity, you can also include synonyms
                that all map to that entity. For example, "soft drink",
                "soda", "pop", and so on.

                There are three types of entities:

                -  **System** - entities that are defined by the
                   Dialogflow API for common data types such as date,
                   time, currency, and so on. A system entity is
                   represented by the ``EntityType`` type.

                -  **Custom** - entities that are defined by you that
                   represent actionable data that is meaningful to your
                   application. For example, you could define a
                   ``pizza.sauce`` entity for red or white pizza sauce,
                   a ``pizza.cheese`` entity for the different types of
                   cheese on a pizza, a ``pizza.topping`` entity for
                   different toppings, and so on. A custom entity is
                   represented by the ``EntityType`` type.

                -  **User** - entities that are built for an individual
                   user such as favorites, preferences, playlists, and
                   so on. A user entity is represented by the
                   [SessionEntityType][google.cloud.dialogflow.cx.v3beta1.SessionEntityType]
                   type.

                For more information about entity types, see the
                `Dialogflow
                documentation <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([entity_type, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_entity_type.UpdateEntityTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if entity_type is not None:
            request.entity_type = entity_type
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_entity_type,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("entity_type.name", request.entity_type.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_entity_type(
        self,
        request: entity_type.DeleteEntityTypeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified entity type.

        Args:
            request (:class:`~.entity_type.DeleteEntityTypeRequest`):
                The request object. The request message for
                [EntityTypes.DeleteEntityType][google.cloud.dialogflow.cx.v3beta1.EntityTypes.DeleteEntityType].
            name (:class:`str`):
                Required. The name of the entity type to delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/entityTypes/<Entity Type ID>``.
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
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = entity_type.DeleteEntityTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_entity_type,
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
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("EntityTypesAsyncClient",)
