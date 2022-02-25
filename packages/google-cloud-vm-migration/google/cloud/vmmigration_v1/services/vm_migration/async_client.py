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
from typing import Dict, Optional, Sequence, Tuple, Type, Union
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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.vmmigration_v1.services.vm_migration import pagers
from google.cloud.vmmigration_v1.types import vmmigration
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import VmMigrationTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import VmMigrationGrpcAsyncIOTransport
from .client import VmMigrationClient


class VmMigrationAsyncClient:
    """VM Migration Service"""

    _client: VmMigrationClient

    DEFAULT_ENDPOINT = VmMigrationClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = VmMigrationClient.DEFAULT_MTLS_ENDPOINT

    clone_job_path = staticmethod(VmMigrationClient.clone_job_path)
    parse_clone_job_path = staticmethod(VmMigrationClient.parse_clone_job_path)
    cutover_job_path = staticmethod(VmMigrationClient.cutover_job_path)
    parse_cutover_job_path = staticmethod(VmMigrationClient.parse_cutover_job_path)
    datacenter_connector_path = staticmethod(
        VmMigrationClient.datacenter_connector_path
    )
    parse_datacenter_connector_path = staticmethod(
        VmMigrationClient.parse_datacenter_connector_path
    )
    group_path = staticmethod(VmMigrationClient.group_path)
    parse_group_path = staticmethod(VmMigrationClient.parse_group_path)
    migrating_vm_path = staticmethod(VmMigrationClient.migrating_vm_path)
    parse_migrating_vm_path = staticmethod(VmMigrationClient.parse_migrating_vm_path)
    source_path = staticmethod(VmMigrationClient.source_path)
    parse_source_path = staticmethod(VmMigrationClient.parse_source_path)
    target_project_path = staticmethod(VmMigrationClient.target_project_path)
    parse_target_project_path = staticmethod(
        VmMigrationClient.parse_target_project_path
    )
    utilization_report_path = staticmethod(VmMigrationClient.utilization_report_path)
    parse_utilization_report_path = staticmethod(
        VmMigrationClient.parse_utilization_report_path
    )
    common_billing_account_path = staticmethod(
        VmMigrationClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        VmMigrationClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(VmMigrationClient.common_folder_path)
    parse_common_folder_path = staticmethod(VmMigrationClient.parse_common_folder_path)
    common_organization_path = staticmethod(VmMigrationClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        VmMigrationClient.parse_common_organization_path
    )
    common_project_path = staticmethod(VmMigrationClient.common_project_path)
    parse_common_project_path = staticmethod(
        VmMigrationClient.parse_common_project_path
    )
    common_location_path = staticmethod(VmMigrationClient.common_location_path)
    parse_common_location_path = staticmethod(
        VmMigrationClient.parse_common_location_path
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
            VmMigrationAsyncClient: The constructed client.
        """
        return VmMigrationClient.from_service_account_info.__func__(VmMigrationAsyncClient, info, *args, **kwargs)  # type: ignore

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
            VmMigrationAsyncClient: The constructed client.
        """
        return VmMigrationClient.from_service_account_file.__func__(VmMigrationAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return VmMigrationClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> VmMigrationTransport:
        """Returns the transport used by the client instance.

        Returns:
            VmMigrationTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(VmMigrationClient).get_transport_class, type(VmMigrationClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, VmMigrationTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the vm migration client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.VmMigrationTransport]): The
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
        self._client = VmMigrationClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_sources(
        self,
        request: Union[vmmigration.ListSourcesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSourcesAsyncPager:
        r"""Lists Sources in a given project and location.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_list_sources():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ListSourcesRequest(
                    parent="parent_value",
                    page_token="page_token_value",
                )

                # Make the request
                page_result = client.list_sources(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ListSourcesRequest, dict]):
                The request object. Request message for 'ListSources'
                request.
            parent (:class:`str`):
                Required. The parent, which owns this
                collection of sources.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.services.vm_migration.pagers.ListSourcesAsyncPager:
                Response message for 'ListSources'
                request.
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

        request = vmmigration.ListSourcesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_sources,
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
        response = pagers.ListSourcesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_source(
        self,
        request: Union[vmmigration.GetSourceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.Source:
        r"""Gets details of a single Source.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_get_source():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.GetSourceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_source(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.GetSourceRequest, dict]):
                The request object. Request message for 'GetSource'
                request.
            name (:class:`str`):
                Required. The Source name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.Source:
                Source message describes a specific
                vm migration Source resource. It
                contains the source environment
                information.

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

        request = vmmigration.GetSourceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_source,
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

    async def create_source(
        self,
        request: Union[vmmigration.CreateSourceRequest, dict] = None,
        *,
        parent: str = None,
        source: vmmigration.Source = None,
        source_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Source in a given project and location.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_create_source():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CreateSourceRequest(
                    parent="parent_value",
                    source_id="source_id_value",
                )

                # Make the request
                operation = client.create_source(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CreateSourceRequest, dict]):
                The request object. Request message for 'CreateSource'
                request.
            parent (:class:`str`):
                Required. The Source's parent.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source (:class:`google.cloud.vmmigration_v1.types.Source`):
                Required. The create request body.
                This corresponds to the ``source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source_id (:class:`str`):
                Required. The source identifier.
                This corresponds to the ``source_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.Source` Source message describes a specific vm migration Source resource. It contains
                   the source environment information.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, source, source_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.CreateSourceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if source is not None:
            request.source = source
        if source_id is not None:
            request.source_id = source_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_source,
            default_timeout=900.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.Source,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_source(
        self,
        request: Union[vmmigration.UpdateSourceRequest, dict] = None,
        *,
        source: vmmigration.Source = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single Source.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_update_source():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.UpdateSourceRequest(
                )

                # Make the request
                operation = client.update_source(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.UpdateSourceRequest, dict]):
                The request object. Update message for 'UpdateSources'
                request.
            source (:class:`google.cloud.vmmigration_v1.types.Source`):
                Required. The update request body.
                This corresponds to the ``source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the Source resource by the update. The
                fields specified in the update_mask are relative to the
                resource, not the full request. A field will be
                overwritten if it is in the mask. If the user does not
                provide a mask then all fields will be overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.Source` Source message describes a specific vm migration Source resource. It contains
                   the source environment information.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([source, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.UpdateSourceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if source is not None:
            request.source = source
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_source,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("source.name", request.source.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.Source,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_source(
        self,
        request: Union[vmmigration.DeleteSourceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Source.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_delete_source():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.DeleteSourceRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_source(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.DeleteSourceRequest, dict]):
                The request object. Request message for 'DeleteSource'
                request.
            name (:class:`str`):
                Required. The Source name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = vmmigration.DeleteSourceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_source,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def fetch_inventory(
        self,
        request: Union[vmmigration.FetchInventoryRequest, dict] = None,
        *,
        source: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.FetchInventoryResponse:
        r"""List remote source's inventory of VMs.
        The remote source is the onprem vCenter (remote in the
        sense it's not in Compute Engine). The inventory
        describes the list of existing VMs in that source. Note
        that this operation lists the VMs on the remote source,
        as opposed to listing the MigratingVms resources in the
        vmmigration service.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_fetch_inventory():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.FetchInventoryRequest(
                    source="source_value",
                )

                # Make the request
                response = client.fetch_inventory(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.FetchInventoryRequest, dict]):
                The request object. Request message for
                [fetchInventory][google.cloud.vmmigration.v1.VmMigration.FetchInventory].
            source (:class:`str`):
                Required. The name of the Source.
                This corresponds to the ``source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.FetchInventoryResponse:
                Response message for
                   [fetchInventory][google.cloud.vmmigration.v1.VmMigration.FetchInventory].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([source])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.FetchInventoryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if source is not None:
            request.source = source

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fetch_inventory,
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("source", request.source),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_utilization_reports(
        self,
        request: Union[vmmigration.ListUtilizationReportsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListUtilizationReportsAsyncPager:
        r"""Lists Utilization Reports of the given Source.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_list_utilization_reports():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ListUtilizationReportsRequest(
                    parent="parent_value",
                    page_token="page_token_value",
                )

                # Make the request
                page_result = client.list_utilization_reports(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ListUtilizationReportsRequest, dict]):
                The request object. Request message for
                'ListUtilizationReports' request.
            parent (:class:`str`):
                Required. The Utilization Reports
                parent.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.services.vm_migration.pagers.ListUtilizationReportsAsyncPager:
                Response message for
                'ListUtilizationReports' request.
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

        request = vmmigration.ListUtilizationReportsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_utilization_reports,
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
        response = pagers.ListUtilizationReportsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_utilization_report(
        self,
        request: Union[vmmigration.GetUtilizationReportRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.UtilizationReport:
        r"""Gets a single Utilization Report.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_get_utilization_report():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.GetUtilizationReportRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_utilization_report(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.GetUtilizationReportRequest, dict]):
                The request object. Request message for
                'GetUtilizationReport' request.
            name (:class:`str`):
                Required. The Utilization Report
                name.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.UtilizationReport:
                Utilization report details the
                utilization (CPU, memory, etc.) of
                selected source VMs.

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

        request = vmmigration.GetUtilizationReportRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_utilization_report,
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

    async def create_utilization_report(
        self,
        request: Union[vmmigration.CreateUtilizationReportRequest, dict] = None,
        *,
        parent: str = None,
        utilization_report: vmmigration.UtilizationReport = None,
        utilization_report_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new UtilizationReport.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_create_utilization_report():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CreateUtilizationReportRequest(
                    parent="parent_value",
                    utilization_report_id="utilization_report_id_value",
                )

                # Make the request
                operation = client.create_utilization_report(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CreateUtilizationReportRequest, dict]):
                The request object. Request message for
                'CreateUtilizationReport' request.
            parent (:class:`str`):
                Required. The Utilization Report's
                parent.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            utilization_report (:class:`google.cloud.vmmigration_v1.types.UtilizationReport`):
                Required. The report to create.
                This corresponds to the ``utilization_report`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            utilization_report_id (:class:`str`):
                Required. The ID to use for the report, which will
                become the final component of the reports's resource
                name.

                This value maximum length is 63 characters, and valid
                characters are /[a-z][0-9]-/. It must start with an
                english letter and must not end with a hyphen.

                This corresponds to the ``utilization_report_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.UtilizationReport` Utilization report details the utilization (CPU, memory, etc.) of selected
                   source VMs.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, utilization_report, utilization_report_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.CreateUtilizationReportRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if utilization_report is not None:
            request.utilization_report = utilization_report
        if utilization_report_id is not None:
            request.utilization_report_id = utilization_report_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_utilization_report,
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.UtilizationReport,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_utilization_report(
        self,
        request: Union[vmmigration.DeleteUtilizationReportRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Utilization Report.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_delete_utilization_report():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.DeleteUtilizationReportRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_utilization_report(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.DeleteUtilizationReportRequest, dict]):
                The request object. Request message for
                'DeleteUtilizationReport' request.
            name (:class:`str`):
                Required. The Utilization Report
                name.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = vmmigration.DeleteUtilizationReportRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_utilization_report,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_datacenter_connectors(
        self,
        request: Union[vmmigration.ListDatacenterConnectorsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDatacenterConnectorsAsyncPager:
        r"""Lists DatacenterConnectors in a given Source.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_list_datacenter_connectors():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ListDatacenterConnectorsRequest(
                    parent="parent_value",
                    page_token="page_token_value",
                )

                # Make the request
                page_result = client.list_datacenter_connectors(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ListDatacenterConnectorsRequest, dict]):
                The request object. Request message for
                'ListDatacenterConnectors' request.
            parent (:class:`str`):
                Required. The parent, which owns this
                collection of connectors.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.services.vm_migration.pagers.ListDatacenterConnectorsAsyncPager:
                Response message for
                'ListDatacenterConnectors' request.
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

        request = vmmigration.ListDatacenterConnectorsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_datacenter_connectors,
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
        response = pagers.ListDatacenterConnectorsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_datacenter_connector(
        self,
        request: Union[vmmigration.GetDatacenterConnectorRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.DatacenterConnector:
        r"""Gets details of a single DatacenterConnector.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_get_datacenter_connector():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.GetDatacenterConnectorRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_datacenter_connector(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.GetDatacenterConnectorRequest, dict]):
                The request object. Request message for
                'GetDatacenterConnector' request.
            name (:class:`str`):
                Required. The name of the
                DatacenterConnector.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.DatacenterConnector:
                DatacenterConnector message describes
                a connector between the Source and GCP,
                which is installed on a vmware
                datacenter (an OVA vm installed by the
                user) to connect the Datacenter to GCP
                and support vm migration data transfer.

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

        request = vmmigration.GetDatacenterConnectorRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_datacenter_connector,
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

    async def create_datacenter_connector(
        self,
        request: Union[vmmigration.CreateDatacenterConnectorRequest, dict] = None,
        *,
        parent: str = None,
        datacenter_connector: vmmigration.DatacenterConnector = None,
        datacenter_connector_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new DatacenterConnector in a given Source.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_create_datacenter_connector():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CreateDatacenterConnectorRequest(
                    parent="parent_value",
                    datacenter_connector_id="datacenter_connector_id_value",
                )

                # Make the request
                operation = client.create_datacenter_connector(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CreateDatacenterConnectorRequest, dict]):
                The request object. Request message for
                'CreateDatacenterConnector' request.
            parent (:class:`str`):
                Required. The DatacenterConnector's parent. Required.
                The Source in where the new DatacenterConnector will be
                created. For example:
                ``projects/my-project/locations/us-central1/sources/my-source``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            datacenter_connector (:class:`google.cloud.vmmigration_v1.types.DatacenterConnector`):
                Required. The create request body.
                This corresponds to the ``datacenter_connector`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            datacenter_connector_id (:class:`str`):
                Required. The datacenterConnector
                identifier.

                This corresponds to the ``datacenter_connector_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.DatacenterConnector` DatacenterConnector message describes a connector between the Source and GCP,
                   which is installed on a vmware datacenter (an OVA vm
                   installed by the user) to connect the Datacenter to
                   GCP and support vm migration data transfer.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, datacenter_connector, datacenter_connector_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.CreateDatacenterConnectorRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if datacenter_connector is not None:
            request.datacenter_connector = datacenter_connector
        if datacenter_connector_id is not None:
            request.datacenter_connector_id = datacenter_connector_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_datacenter_connector,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.DatacenterConnector,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_datacenter_connector(
        self,
        request: Union[vmmigration.DeleteDatacenterConnectorRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single DatacenterConnector.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_delete_datacenter_connector():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.DeleteDatacenterConnectorRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_datacenter_connector(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.DeleteDatacenterConnectorRequest, dict]):
                The request object. Request message for
                'DeleteDatacenterConnector' request.
            name (:class:`str`):
                Required. The DatacenterConnector
                name.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = vmmigration.DeleteDatacenterConnectorRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_datacenter_connector,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_migrating_vm(
        self,
        request: Union[vmmigration.CreateMigratingVmRequest, dict] = None,
        *,
        parent: str = None,
        migrating_vm: vmmigration.MigratingVm = None,
        migrating_vm_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new MigratingVm in a given Source.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_create_migrating_vm():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CreateMigratingVmRequest(
                    parent="parent_value",
                    migrating_vm_id="migrating_vm_id_value",
                )

                # Make the request
                operation = client.create_migrating_vm(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CreateMigratingVmRequest, dict]):
                The request object. Request message for
                'CreateMigratingVm' request.
            parent (:class:`str`):
                Required. The MigratingVm's parent.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            migrating_vm (:class:`google.cloud.vmmigration_v1.types.MigratingVm`):
                Required. The create request body.
                This corresponds to the ``migrating_vm`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            migrating_vm_id (:class:`str`):
                Required. The migratingVm identifier.
                This corresponds to the ``migrating_vm_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.MigratingVm` MigratingVm describes the VM that will be migrated from a Source environment
                   and its replication state.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, migrating_vm, migrating_vm_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.CreateMigratingVmRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if migrating_vm is not None:
            request.migrating_vm = migrating_vm
        if migrating_vm_id is not None:
            request.migrating_vm_id = migrating_vm_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_migrating_vm,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.MigratingVm,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_migrating_vms(
        self,
        request: Union[vmmigration.ListMigratingVmsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMigratingVmsAsyncPager:
        r"""Lists MigratingVms in a given Source.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_list_migrating_vms():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ListMigratingVmsRequest(
                    parent="parent_value",
                    page_token="page_token_value",
                )

                # Make the request
                page_result = client.list_migrating_vms(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ListMigratingVmsRequest, dict]):
                The request object. Request message for
                'LisMigratingVmsRequest' request.
            parent (:class:`str`):
                Required. The parent, which owns this
                collection of MigratingVms.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.services.vm_migration.pagers.ListMigratingVmsAsyncPager:
                Response message for
                'ListMigratingVms' request.
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

        request = vmmigration.ListMigratingVmsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_migrating_vms,
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
        response = pagers.ListMigratingVmsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_migrating_vm(
        self,
        request: Union[vmmigration.GetMigratingVmRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.MigratingVm:
        r"""Gets details of a single MigratingVm.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_get_migrating_vm():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.GetMigratingVmRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_migrating_vm(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.GetMigratingVmRequest, dict]):
                The request object. Request message for 'GetMigratingVm'
                request.
            name (:class:`str`):
                Required. The name of the
                MigratingVm.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.MigratingVm:
                MigratingVm describes the VM that
                will be migrated from a Source
                environment and its replication state.

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

        request = vmmigration.GetMigratingVmRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_migrating_vm,
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

    async def update_migrating_vm(
        self,
        request: Union[vmmigration.UpdateMigratingVmRequest, dict] = None,
        *,
        migrating_vm: vmmigration.MigratingVm = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single MigratingVm.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_update_migrating_vm():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.UpdateMigratingVmRequest(
                )

                # Make the request
                operation = client.update_migrating_vm(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.UpdateMigratingVmRequest, dict]):
                The request object. Request message for
                'UpdateMigratingVm' request.
            migrating_vm (:class:`google.cloud.vmmigration_v1.types.MigratingVm`):
                Required. The update request body.
                This corresponds to the ``migrating_vm`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the MigratingVm resource by the update.
                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask. If the user does not
                provide a mask then all fields will be overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.MigratingVm` MigratingVm describes the VM that will be migrated from a Source environment
                   and its replication state.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([migrating_vm, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.UpdateMigratingVmRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if migrating_vm is not None:
            request.migrating_vm = migrating_vm
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_migrating_vm,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("migrating_vm.name", request.migrating_vm.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.MigratingVm,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_migrating_vm(
        self,
        request: Union[vmmigration.DeleteMigratingVmRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single MigratingVm.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_delete_migrating_vm():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.DeleteMigratingVmRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_migrating_vm(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.DeleteMigratingVmRequest, dict]):
                The request object. Request message for
                'DeleteMigratingVm' request.
            name (:class:`str`):
                Required. The name of the
                MigratingVm.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = vmmigration.DeleteMigratingVmRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_migrating_vm,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def start_migration(
        self,
        request: Union[vmmigration.StartMigrationRequest, dict] = None,
        *,
        migrating_vm: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts migration for a VM. Starts the process of
        uploading data and creating snapshots, in replication
        cycles scheduled by the policy.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_start_migration():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.StartMigrationRequest(
                    migrating_vm="migrating_vm_value",
                )

                # Make the request
                operation = client.start_migration(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.StartMigrationRequest, dict]):
                The request object. Request message for
                'StartMigrationRequest' request.
            migrating_vm (:class:`str`):
                Required. The name of the
                MigratingVm.

                This corresponds to the ``migrating_vm`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vmmigration_v1.types.StartMigrationResponse`
                Response message for 'StartMigration' request.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([migrating_vm])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.StartMigrationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if migrating_vm is not None:
            request.migrating_vm = migrating_vm

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_migration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("migrating_vm", request.migrating_vm),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.StartMigrationResponse,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def resume_migration(
        self,
        request: Union[vmmigration.ResumeMigrationRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Resumes a migration for a VM. When called on a paused
        migration, will start the process of uploading data and
        creating snapshots; when called on a completed cut-over
        migration, will update the migration to active state and
        start the process of uploading data and creating
        snapshots.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_resume_migration():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ResumeMigrationRequest(
                    migrating_vm="migrating_vm_value",
                )

                # Make the request
                operation = client.resume_migration(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ResumeMigrationRequest, dict]):
                The request object. Request message for
                'ResumeMigration' request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vmmigration_v1.types.ResumeMigrationResponse`
                Response message for 'ResumeMigration' request.

        """
        # Create or coerce a protobuf request object.
        request = vmmigration.ResumeMigrationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.resume_migration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("migrating_vm", request.migrating_vm),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.ResumeMigrationResponse,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def pause_migration(
        self,
        request: Union[vmmigration.PauseMigrationRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Pauses a migration for a VM. If cycle tasks are
        running they will be cancelled, preserving source task
        data. Further replication cycles will not be triggered
        while the VM is paused.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_pause_migration():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.PauseMigrationRequest(
                    migrating_vm="migrating_vm_value",
                )

                # Make the request
                operation = client.pause_migration(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.PauseMigrationRequest, dict]):
                The request object. Request message for 'PauseMigration'
                request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vmmigration_v1.types.PauseMigrationResponse`
                Response message for 'PauseMigration' request.

        """
        # Create or coerce a protobuf request object.
        request = vmmigration.PauseMigrationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.pause_migration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("migrating_vm", request.migrating_vm),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.PauseMigrationResponse,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def finalize_migration(
        self,
        request: Union[vmmigration.FinalizeMigrationRequest, dict] = None,
        *,
        migrating_vm: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Marks a migration as completed, deleting migration
        resources that are no longer being used. Only applicable
        after cutover is done.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_finalize_migration():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.FinalizeMigrationRequest(
                    migrating_vm="migrating_vm_value",
                )

                # Make the request
                operation = client.finalize_migration(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.FinalizeMigrationRequest, dict]):
                The request object. Request message for
                'FinalizeMigration' request.
            migrating_vm (:class:`str`):
                Required. The name of the
                MigratingVm.

                This corresponds to the ``migrating_vm`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vmmigration_v1.types.FinalizeMigrationResponse`
                Response message for 'FinalizeMigration' request.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([migrating_vm])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.FinalizeMigrationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if migrating_vm is not None:
            request.migrating_vm = migrating_vm

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.finalize_migration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("migrating_vm", request.migrating_vm),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.FinalizeMigrationResponse,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_clone_job(
        self,
        request: Union[vmmigration.CreateCloneJobRequest, dict] = None,
        *,
        parent: str = None,
        clone_job: vmmigration.CloneJob = None,
        clone_job_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Initiates a Clone of a specific migrating VM.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_create_clone_job():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CreateCloneJobRequest(
                    parent="parent_value",
                    clone_job_id="clone_job_id_value",
                )

                # Make the request
                operation = client.create_clone_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CreateCloneJobRequest, dict]):
                The request object. Request message for 'CreateCloneJob'
                request.
            parent (:class:`str`):
                Required. The Clone's parent.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            clone_job (:class:`google.cloud.vmmigration_v1.types.CloneJob`):
                Required. The clone request body.
                This corresponds to the ``clone_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            clone_job_id (:class:`str`):
                Required. The clone job identifier.
                This corresponds to the ``clone_job_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.CloneJob` CloneJob describes the process of creating a clone of a
                   [MigratingVM][google.cloud.vmmigration.v1.MigratingVm]
                   to the requested target based on the latest
                   successful uploaded snapshots. While the migration
                   cycles of a MigratingVm take place, it is possible to
                   verify the uploaded VM can be started in the cloud,
                   by creating a clone. The clone can be created without
                   any downtime, and it is created using the latest
                   snapshots which are already in the cloud. The
                   cloneJob is only responsible for its work, not its
                   products, which means once it is finished, it will
                   never touch the instance it created. It will only
                   delete it in case of the CloneJob being cancelled or
                   upon failure to clone.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, clone_job, clone_job_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.CreateCloneJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if clone_job is not None:
            request.clone_job = clone_job
        if clone_job_id is not None:
            request.clone_job_id = clone_job_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_clone_job,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.CloneJob,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def cancel_clone_job(
        self,
        request: Union[vmmigration.CancelCloneJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Initiates the cancellation of a running clone job.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_cancel_clone_job():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CancelCloneJobRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.cancel_clone_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CancelCloneJobRequest, dict]):
                The request object. Request message for 'CancelCloneJob'
                request.
            name (:class:`str`):
                Required. The clone job id
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vmmigration_v1.types.CancelCloneJobResponse`
                Response message for 'CancelCloneJob' request.

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

        request = vmmigration.CancelCloneJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_clone_job,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.CancelCloneJobResponse,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_clone_jobs(
        self,
        request: Union[vmmigration.ListCloneJobsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCloneJobsAsyncPager:
        r"""Lists CloneJobs of a given migrating VM.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_list_clone_jobs():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ListCloneJobsRequest(
                    parent="parent_value",
                    page_token="page_token_value",
                )

                # Make the request
                page_result = client.list_clone_jobs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ListCloneJobsRequest, dict]):
                The request object. Request message for
                'ListCloneJobsRequest' request.
            parent (:class:`str`):
                Required. The parent, which owns this
                collection of source VMs.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.services.vm_migration.pagers.ListCloneJobsAsyncPager:
                Response message for 'ListCloneJobs'
                request.
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

        request = vmmigration.ListCloneJobsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_clone_jobs,
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
        response = pagers.ListCloneJobsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_clone_job(
        self,
        request: Union[vmmigration.GetCloneJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.CloneJob:
        r"""Gets details of a single CloneJob.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_get_clone_job():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.GetCloneJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_clone_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.GetCloneJobRequest, dict]):
                The request object. Request message for 'GetCloneJob'
                request.
            name (:class:`str`):
                Required. The name of the CloneJob.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.CloneJob:
                CloneJob describes the process of creating a clone of a
                   [MigratingVM][google.cloud.vmmigration.v1.MigratingVm]
                   to the requested target based on the latest
                   successful uploaded snapshots. While the migration
                   cycles of a MigratingVm take place, it is possible to
                   verify the uploaded VM can be started in the cloud,
                   by creating a clone. The clone can be created without
                   any downtime, and it is created using the latest
                   snapshots which are already in the cloud. The
                   cloneJob is only responsible for its work, not its
                   products, which means once it is finished, it will
                   never touch the instance it created. It will only
                   delete it in case of the CloneJob being cancelled or
                   upon failure to clone.

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

        request = vmmigration.GetCloneJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_clone_job,
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

    async def create_cutover_job(
        self,
        request: Union[vmmigration.CreateCutoverJobRequest, dict] = None,
        *,
        parent: str = None,
        cutover_job: vmmigration.CutoverJob = None,
        cutover_job_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Initiates a Cutover of a specific migrating VM.
        The returned LRO is completed when the cutover job
        resource is created and the job is initiated.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_create_cutover_job():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CreateCutoverJobRequest(
                    parent="parent_value",
                    cutover_job_id="cutover_job_id_value",
                )

                # Make the request
                operation = client.create_cutover_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CreateCutoverJobRequest, dict]):
                The request object. Request message for
                'CreateCutoverJob' request.
            parent (:class:`str`):
                Required. The Cutover's parent.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cutover_job (:class:`google.cloud.vmmigration_v1.types.CutoverJob`):
                Required. The cutover request body.
                This corresponds to the ``cutover_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cutover_job_id (:class:`str`):
                Required. The cutover job identifier.
                This corresponds to the ``cutover_job_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.CutoverJob` CutoverJob message describes a cutover of a migrating VM. The CutoverJob is
                   the operation of shutting down the VM, creating a
                   snapshot and clonning the VM using the replicated
                   snapshot.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, cutover_job, cutover_job_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.CreateCutoverJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if cutover_job is not None:
            request.cutover_job = cutover_job
        if cutover_job_id is not None:
            request.cutover_job_id = cutover_job_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_cutover_job,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.CutoverJob,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def cancel_cutover_job(
        self,
        request: Union[vmmigration.CancelCutoverJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Initiates the cancellation of a running cutover job.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_cancel_cutover_job():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CancelCutoverJobRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.cancel_cutover_job(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CancelCutoverJobRequest, dict]):
                The request object. Request message for
                'CancelCutoverJob' request.
            name (:class:`str`):
                Required. The cutover job id
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vmmigration_v1.types.CancelCutoverJobResponse`
                Response message for 'CancelCutoverJob' request.

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

        request = vmmigration.CancelCutoverJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_cutover_job,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.CancelCutoverJobResponse,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_cutover_jobs(
        self,
        request: Union[vmmigration.ListCutoverJobsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCutoverJobsAsyncPager:
        r"""Lists CutoverJobs of a given migrating VM.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_list_cutover_jobs():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ListCutoverJobsRequest(
                    parent="parent_value",
                    page_token="page_token_value",
                )

                # Make the request
                page_result = client.list_cutover_jobs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ListCutoverJobsRequest, dict]):
                The request object. Request message for
                'ListCutoverJobsRequest' request.
            parent (:class:`str`):
                Required. The parent, which owns this
                collection of migrating VMs.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.services.vm_migration.pagers.ListCutoverJobsAsyncPager:
                Response message for
                'ListCutoverJobs' request.
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

        request = vmmigration.ListCutoverJobsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_cutover_jobs,
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
        response = pagers.ListCutoverJobsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_cutover_job(
        self,
        request: Union[vmmigration.GetCutoverJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.CutoverJob:
        r"""Gets details of a single CutoverJob.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_get_cutover_job():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.GetCutoverJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_cutover_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.GetCutoverJobRequest, dict]):
                The request object. Request message for 'GetCutoverJob'
                request.
            name (:class:`str`):
                Required. The name of the CutoverJob.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.CutoverJob:
                CutoverJob message describes a
                cutover of a migrating VM. The
                CutoverJob is the operation of shutting
                down the VM, creating a snapshot and
                clonning the VM using the replicated
                snapshot.

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

        request = vmmigration.GetCutoverJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_cutover_job,
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

    async def list_groups(
        self,
        request: Union[vmmigration.ListGroupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGroupsAsyncPager:
        r"""Lists Groups in a given project and location.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_list_groups():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ListGroupsRequest(
                    parent="parent_value",
                    page_token="page_token_value",
                )

                # Make the request
                page_result = client.list_groups(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ListGroupsRequest, dict]):
                The request object. Request message for 'ListGroups'
                request.
            parent (:class:`str`):
                Required. The parent, which owns this
                collection of groups.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.services.vm_migration.pagers.ListGroupsAsyncPager:
                Response message for 'ListGroups'
                request.
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

        request = vmmigration.ListGroupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_groups,
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
        response = pagers.ListGroupsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_group(
        self,
        request: Union[vmmigration.GetGroupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.Group:
        r"""Gets details of a single Group.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_get_group():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.GetGroupRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_group(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.GetGroupRequest, dict]):
                The request object. Request message for 'GetGroup'
                request.
            name (:class:`str`):
                Required. The group name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.Group:
                Describes message for 'Group'
                resource. The Group is a collections of
                several MigratingVms.

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

        request = vmmigration.GetGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_group,
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

    async def create_group(
        self,
        request: Union[vmmigration.CreateGroupRequest, dict] = None,
        *,
        parent: str = None,
        group: vmmigration.Group = None,
        group_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Group in a given project and location.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_create_group():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CreateGroupRequest(
                    parent="parent_value",
                    group_id="group_id_value",
                )

                # Make the request
                operation = client.create_group(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CreateGroupRequest, dict]):
                The request object. Request message for 'CreateGroup'
                request.
            parent (:class:`str`):
                Required. The Group's parent.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            group (:class:`google.cloud.vmmigration_v1.types.Group`):
                Required. The create request body.
                This corresponds to the ``group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            group_id (:class:`str`):
                Required. The group identifier.
                This corresponds to the ``group_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.Group` Describes message for 'Group' resource. The Group is a collections of several
                   MigratingVms.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, group, group_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.CreateGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if group is not None:
            request.group = group
        if group_id is not None:
            request.group_id = group_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_group,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.Group,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_group(
        self,
        request: Union[vmmigration.UpdateGroupRequest, dict] = None,
        *,
        group: vmmigration.Group = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single Group.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_update_group():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.UpdateGroupRequest(
                )

                # Make the request
                operation = client.update_group(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.UpdateGroupRequest, dict]):
                The request object. Update message for 'UpdateGroups'
                request.
            group (:class:`google.cloud.vmmigration_v1.types.Group`):
                Required. The update request body.
                This corresponds to the ``group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the Group resource by the update. The
                fields specified in the update_mask are relative to the
                resource, not the full request. A field will be
                overwritten if it is in the mask. If the user does not
                provide a mask then all fields will be overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.Group` Describes message for 'Group' resource. The Group is a collections of several
                   MigratingVms.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([group, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.UpdateGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if group is not None:
            request.group = group
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_group,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("group.name", request.group.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.Group,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_group(
        self,
        request: Union[vmmigration.DeleteGroupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Group.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_delete_group():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.DeleteGroupRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_group(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.DeleteGroupRequest, dict]):
                The request object. Request message for 'DeleteGroup'
                request.
            name (:class:`str`):
                Required. The Group name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = vmmigration.DeleteGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_group,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def add_group_migration(
        self,
        request: Union[vmmigration.AddGroupMigrationRequest, dict] = None,
        *,
        group: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Adds a MigratingVm to a Group.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_add_group_migration():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.AddGroupMigrationRequest(
                    group="group_value",
                )

                # Make the request
                operation = client.add_group_migration(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.AddGroupMigrationRequest, dict]):
                The request object. Request message for
                'AddGroupMigration' request.
            group (:class:`str`):
                Required. The full path name of the
                Group to add to.

                This corresponds to the ``group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vmmigration_v1.types.AddGroupMigrationResponse`
                Response message for 'AddGroupMigration' request.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.AddGroupMigrationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if group is not None:
            request.group = group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.add_group_migration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("group", request.group),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.AddGroupMigrationResponse,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def remove_group_migration(
        self,
        request: Union[vmmigration.RemoveGroupMigrationRequest, dict] = None,
        *,
        group: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Removes a MigratingVm from a Group.

        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_remove_group_migration():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.RemoveGroupMigrationRequest(
                    group="group_value",
                )

                # Make the request
                operation = client.remove_group_migration(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.RemoveGroupMigrationRequest, dict]):
                The request object. Request message for
                'RemoveMigration' request.
            group (:class:`str`):
                Required. The name of the Group.
                This corresponds to the ``group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.vmmigration_v1.types.RemoveGroupMigrationResponse`
                Response message for 'RemoveMigration' request.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.RemoveGroupMigrationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if group is not None:
            request.group = group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.remove_group_migration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("group", request.group),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.RemoveGroupMigrationResponse,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_target_projects(
        self,
        request: Union[vmmigration.ListTargetProjectsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTargetProjectsAsyncPager:
        r"""Lists TargetProjects in a given project.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_list_target_projects():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.ListTargetProjectsRequest(
                    parent="parent_value",
                    page_token="page_token_value",
                )

                # Make the request
                page_result = client.list_target_projects(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.ListTargetProjectsRequest, dict]):
                The request object. Request message for
                'ListTargetProjects' call.
            parent (:class:`str`):
                Required. The parent, which owns this
                collection of targets.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.services.vm_migration.pagers.ListTargetProjectsAsyncPager:
                Response message for
                'ListTargetProjects' call.
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

        request = vmmigration.ListTargetProjectsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_target_projects,
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
        response = pagers.ListTargetProjectsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_target_project(
        self,
        request: Union[vmmigration.GetTargetProjectRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vmmigration.TargetProject:
        r"""Gets details of a single TargetProject.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_get_target_project():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.GetTargetProjectRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_target_project(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.GetTargetProjectRequest, dict]):
                The request object. Request message for
                'GetTargetProject' call.
            name (:class:`str`):
                Required. The TargetProject name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.vmmigration_v1.types.TargetProject:
                TargetProject message represents a
                target Compute Engine project for a
                migration or a clone.

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

        request = vmmigration.GetTargetProjectRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_target_project,
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

    async def create_target_project(
        self,
        request: Union[vmmigration.CreateTargetProjectRequest, dict] = None,
        *,
        parent: str = None,
        target_project: vmmigration.TargetProject = None,
        target_project_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new TargetProject in a given project.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_create_target_project():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.CreateTargetProjectRequest(
                    parent="parent_value",
                    target_project_id="target_project_id_value",
                )

                # Make the request
                operation = client.create_target_project(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.CreateTargetProjectRequest, dict]):
                The request object. Request message for
                'CreateTargetProject' request.
            parent (:class:`str`):
                Required. The TargetProject's parent.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target_project (:class:`google.cloud.vmmigration_v1.types.TargetProject`):
                Required. The create request body.
                This corresponds to the ``target_project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target_project_id (:class:`str`):
                Required. The target_project identifier.
                This corresponds to the ``target_project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.TargetProject` TargetProject message represents a target Compute Engine project for a
                   migration or a clone.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, target_project, target_project_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.CreateTargetProjectRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if target_project is not None:
            request.target_project = target_project
        if target_project_id is not None:
            request.target_project_id = target_project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_target_project,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.TargetProject,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_target_project(
        self,
        request: Union[vmmigration.UpdateTargetProjectRequest, dict] = None,
        *,
        target_project: vmmigration.TargetProject = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single TargetProject.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_update_target_project():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.UpdateTargetProjectRequest(
                )

                # Make the request
                operation = client.update_target_project(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.UpdateTargetProjectRequest, dict]):
                The request object. Update message for
                'UpdateTargetProject' request.
            target_project (:class:`google.cloud.vmmigration_v1.types.TargetProject`):
                Required. The update request body.
                This corresponds to the ``target_project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the TargetProject resource by the update.
                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask. If the user does not
                provide a mask then all fields will be overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.vmmigration_v1.types.TargetProject` TargetProject message represents a target Compute Engine project for a
                   migration or a clone.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([target_project, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = vmmigration.UpdateTargetProjectRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if target_project is not None:
            request.target_project = target_project
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_target_project,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("target_project.name", request.target_project.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            vmmigration.TargetProject,
            metadata_type=vmmigration.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_target_project(
        self,
        request: Union[vmmigration.DeleteTargetProjectRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single TargetProject.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.


        .. code-block:: python

            from google.cloud import vmmigration_v1

            def sample_delete_target_project():
                # Create a client
                client = vmmigration_v1.VmMigrationClient()

                # Initialize request argument(s)
                request = vmmigration_v1.DeleteTargetProjectRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_target_project(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.vmmigration_v1.types.DeleteTargetProjectRequest, dict]):
                The request object. Request message for
                'DeleteTargetProject' request.
            name (:class:`str`):
                Required. The TargetProject name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = vmmigration.DeleteTargetProjectRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_target_project,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=vmmigration.OperationMetadata,
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
            "google-cloud-vm-migration",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("VmMigrationAsyncClient",)
