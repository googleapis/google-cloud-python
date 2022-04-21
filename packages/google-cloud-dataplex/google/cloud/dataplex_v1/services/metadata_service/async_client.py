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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import pkg_resources

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.dataplex_v1.services.metadata_service import pagers
from google.cloud.dataplex_v1.types import metadata_

from .client import MetadataServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, MetadataServiceTransport
from .transports.grpc_asyncio import MetadataServiceGrpcAsyncIOTransport


class MetadataServiceAsyncClient:
    """Metadata service manages metadata resources such as tables,
    filesets and partitions.
    """

    _client: MetadataServiceClient

    DEFAULT_ENDPOINT = MetadataServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = MetadataServiceClient.DEFAULT_MTLS_ENDPOINT

    entity_path = staticmethod(MetadataServiceClient.entity_path)
    parse_entity_path = staticmethod(MetadataServiceClient.parse_entity_path)
    partition_path = staticmethod(MetadataServiceClient.partition_path)
    parse_partition_path = staticmethod(MetadataServiceClient.parse_partition_path)
    zone_path = staticmethod(MetadataServiceClient.zone_path)
    parse_zone_path = staticmethod(MetadataServiceClient.parse_zone_path)
    common_billing_account_path = staticmethod(
        MetadataServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        MetadataServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(MetadataServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        MetadataServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        MetadataServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        MetadataServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(MetadataServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        MetadataServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(MetadataServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        MetadataServiceClient.parse_common_location_path
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
            MetadataServiceAsyncClient: The constructed client.
        """
        return MetadataServiceClient.from_service_account_info.__func__(MetadataServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            MetadataServiceAsyncClient: The constructed client.
        """
        return MetadataServiceClient.from_service_account_file.__func__(MetadataServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return MetadataServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> MetadataServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            MetadataServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(MetadataServiceClient).get_transport_class, type(MetadataServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, MetadataServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the metadata service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.MetadataServiceTransport]): The
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
        self._client = MetadataServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_entity(
        self,
        request: Union[metadata_.CreateEntityRequest, dict] = None,
        *,
        parent: str = None,
        entity: metadata_.Entity = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_.Entity:
        r"""Create a metadata entity.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_create_entity():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                entity = dataplex_v1.Entity()
                entity.id = "id_value"
                entity.type_ = "FILESET"
                entity.asset = "asset_value"
                entity.data_path = "data_path_value"
                entity.system = "BIGQUERY"
                entity.format_.mime_type = "mime_type_value"
                entity.schema.user_managed = True

                request = dataplex_v1.CreateEntityRequest(
                    parent="parent_value",
                    entity=entity,
                )

                # Make the request
                response = client.create_entity(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.CreateEntityRequest, dict]):
                The request object. Create a metadata entity request.
            parent (:class:`str`):
                Required. The resource name of the parent zone:
                ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entity (:class:`google.cloud.dataplex_v1.types.Entity`):
                Required. Entity resource.
                This corresponds to the ``entity`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.types.Entity:
                Represents tables and fileset
                metadata contained within a zone.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, entity])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metadata_.CreateEntityRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if entity is not None:
            request.entity = entity

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_entity,
            default_timeout=60.0,
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

    async def update_entity(
        self,
        request: Union[metadata_.UpdateEntityRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_.Entity:
        r"""Update a metadata entity. Only supports full resource
        update.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_update_entity():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                entity = dataplex_v1.Entity()
                entity.id = "id_value"
                entity.type_ = "FILESET"
                entity.asset = "asset_value"
                entity.data_path = "data_path_value"
                entity.system = "BIGQUERY"
                entity.format_.mime_type = "mime_type_value"
                entity.schema.user_managed = True

                request = dataplex_v1.UpdateEntityRequest(
                    entity=entity,
                )

                # Make the request
                response = client.update_entity(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.UpdateEntityRequest, dict]):
                The request object. Update a metadata entity request.
                The exiting entity will be fully replaced by the entity
                in the request. The entity ID is mutable. To modify the
                ID, use the current entity ID in the request URL and
                specify the new ID in the request body.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.types.Entity:
                Represents tables and fileset
                metadata contained within a zone.

        """
        # Create or coerce a protobuf request object.
        request = metadata_.UpdateEntityRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_entity,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("entity.name", request.entity.name),)
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

    async def delete_entity(
        self,
        request: Union[metadata_.DeleteEntityRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete a metadata entity.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_delete_entity():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.DeleteEntityRequest(
                    name="name_value",
                    etag="etag_value",
                )

                # Make the request
                client.delete_entity(request=request)

        Args:
            request (Union[google.cloud.dataplex_v1.types.DeleteEntityRequest, dict]):
                The request object. Delete a metadata entity request.
            name (:class:`str`):
                Required. The resource name of the entity:
                ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}``.

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

        request = metadata_.DeleteEntityRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_entity,
            default_timeout=60.0,
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

    async def get_entity(
        self,
        request: Union[metadata_.GetEntityRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_.Entity:
        r"""Get a metadata entity.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_get_entity():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.GetEntityRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_entity(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.GetEntityRequest, dict]):
                The request object. Get metadata entity request.
            name (:class:`str`):
                Required. The resource name of the entity:
                ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}.``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.types.Entity:
                Represents tables and fileset
                metadata contained within a zone.

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

        request = metadata_.GetEntityRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_entity,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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

    async def list_entities(
        self,
        request: Union[metadata_.ListEntitiesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEntitiesAsyncPager:
        r"""List metadata entities in a zone.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_list_entities():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.ListEntitiesRequest(
                    parent="parent_value",
                    view="FILESETS",
                )

                # Make the request
                page_result = client.list_entities(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.ListEntitiesRequest, dict]):
                The request object. List metadata entities request.
            parent (:class:`str`):
                Required. The resource name of the parent zone:
                ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.services.metadata_service.pagers.ListEntitiesAsyncPager:
                List metadata entities response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = metadata_.ListEntitiesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_entities,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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
        response = pagers.ListEntitiesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_partition(
        self,
        request: Union[metadata_.CreatePartitionRequest, dict] = None,
        *,
        parent: str = None,
        partition: metadata_.Partition = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_.Partition:
        r"""Create a metadata partition.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_create_partition():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                partition = dataplex_v1.Partition()
                partition.values = ['values_value_1', 'values_value_2']
                partition.location = "location_value"

                request = dataplex_v1.CreatePartitionRequest(
                    parent="parent_value",
                    partition=partition,
                )

                # Make the request
                response = client.create_partition(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.CreatePartitionRequest, dict]):
                The request object. Create metadata partition request.
            parent (:class:`str`):
                Required. The resource name of the parent zone:
                ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            partition (:class:`google.cloud.dataplex_v1.types.Partition`):
                Required. Partition resource.
                This corresponds to the ``partition`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.types.Partition:
                Represents partition metadata
                contained within entity instances.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, partition])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metadata_.CreatePartitionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if partition is not None:
            request.partition = partition

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_partition,
            default_timeout=60.0,
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

    async def delete_partition(
        self,
        request: Union[metadata_.DeletePartitionRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete a metadata partition.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_delete_partition():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.DeletePartitionRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_partition(request=request)

        Args:
            request (Union[google.cloud.dataplex_v1.types.DeletePartitionRequest, dict]):
                The request object. Delete metadata partition request.
            name (:class:`str`):
                Required. The resource name of the partition. format:
                ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}/partitions/{partition_value_path}``.
                The {partition_value_path} segment consists of an
                ordered sequence of partition values separated by "/".
                All values must be provided.

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

        request = metadata_.DeletePartitionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_partition,
            default_timeout=60.0,
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

    async def get_partition(
        self,
        request: Union[metadata_.GetPartitionRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metadata_.Partition:
        r"""Get a metadata partition of an entity.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_get_partition():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.GetPartitionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_partition(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.GetPartitionRequest, dict]):
                The request object. Get metadata partition request.
            name (:class:`str`):
                Required. The resource name of the partition:
                ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}/partitions/{partition_value_path}``.
                The {partition_value_path} segment consists of an
                ordered sequence of partition values separated by "/".
                All values must be provided.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.types.Partition:
                Represents partition metadata
                contained within entity instances.

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

        request = metadata_.GetPartitionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_partition,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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

    async def list_partitions(
        self,
        request: Union[metadata_.ListPartitionsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPartitionsAsyncPager:
        r"""List metadata partitions of an entity.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_list_partitions():
                # Create a client
                client = dataplex_v1.MetadataServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.ListPartitionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_partitions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.ListPartitionsRequest, dict]):
                The request object. List metadata partitions request.
            parent (:class:`str`):
                Required. The resource name of the parent entity:
                ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/zones/{zone_id}/entities/{entity_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.services.metadata_service.pagers.ListPartitionsAsyncPager:
                List metadata partitions response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = metadata_.ListPartitionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_partitions,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
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
        response = pagers.ListPartitionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dataplex",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("MetadataServiceAsyncClient",)
