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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.bare_metal_solution_v2.services.bare_metal_solution import pagers
from google.cloud.bare_metal_solution_v2.types import baremetalsolution
from google.cloud.bare_metal_solution_v2.types import instance
from google.cloud.bare_metal_solution_v2.types import instance as gcb_instance
from google.cloud.bare_metal_solution_v2.types import lun
from google.cloud.bare_metal_solution_v2.types import network
from google.cloud.bare_metal_solution_v2.types import network as gcb_network
from google.cloud.bare_metal_solution_v2.types import nfs_share
from google.cloud.bare_metal_solution_v2.types import nfs_share as gcb_nfs_share
from google.cloud.bare_metal_solution_v2.types import volume
from google.cloud.bare_metal_solution_v2.types import volume as gcb_volume
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import BareMetalSolutionTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import BareMetalSolutionGrpcAsyncIOTransport
from .client import BareMetalSolutionClient


class BareMetalSolutionAsyncClient:
    """Performs management operations on Bare Metal Solution servers.

    The ``baremetalsolution.googleapis.com`` service provides management
    capabilities for Bare Metal Solution servers. To access the API
    methods, you must assign Bare Metal Solution IAM roles containing
    the desired permissions to your staff in your Google Cloud project.
    You must also enable the Bare Metal Solution API. Once enabled, the
    methods act upon specific servers in your Bare Metal Solution
    environment.
    """

    _client: BareMetalSolutionClient

    DEFAULT_ENDPOINT = BareMetalSolutionClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = BareMetalSolutionClient.DEFAULT_MTLS_ENDPOINT

    instance_path = staticmethod(BareMetalSolutionClient.instance_path)
    parse_instance_path = staticmethod(BareMetalSolutionClient.parse_instance_path)
    lun_path = staticmethod(BareMetalSolutionClient.lun_path)
    parse_lun_path = staticmethod(BareMetalSolutionClient.parse_lun_path)
    network_path = staticmethod(BareMetalSolutionClient.network_path)
    parse_network_path = staticmethod(BareMetalSolutionClient.parse_network_path)
    nfs_share_path = staticmethod(BareMetalSolutionClient.nfs_share_path)
    parse_nfs_share_path = staticmethod(BareMetalSolutionClient.parse_nfs_share_path)
    server_network_template_path = staticmethod(
        BareMetalSolutionClient.server_network_template_path
    )
    parse_server_network_template_path = staticmethod(
        BareMetalSolutionClient.parse_server_network_template_path
    )
    volume_path = staticmethod(BareMetalSolutionClient.volume_path)
    parse_volume_path = staticmethod(BareMetalSolutionClient.parse_volume_path)
    common_billing_account_path = staticmethod(
        BareMetalSolutionClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        BareMetalSolutionClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(BareMetalSolutionClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        BareMetalSolutionClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        BareMetalSolutionClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        BareMetalSolutionClient.parse_common_organization_path
    )
    common_project_path = staticmethod(BareMetalSolutionClient.common_project_path)
    parse_common_project_path = staticmethod(
        BareMetalSolutionClient.parse_common_project_path
    )
    common_location_path = staticmethod(BareMetalSolutionClient.common_location_path)
    parse_common_location_path = staticmethod(
        BareMetalSolutionClient.parse_common_location_path
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
            BareMetalSolutionAsyncClient: The constructed client.
        """
        return BareMetalSolutionClient.from_service_account_info.__func__(BareMetalSolutionAsyncClient, info, *args, **kwargs)  # type: ignore

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
            BareMetalSolutionAsyncClient: The constructed client.
        """
        return BareMetalSolutionClient.from_service_account_file.__func__(BareMetalSolutionAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return BareMetalSolutionClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> BareMetalSolutionTransport:
        """Returns the transport used by the client instance.

        Returns:
            BareMetalSolutionTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(BareMetalSolutionClient).get_transport_class, type(BareMetalSolutionClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, BareMetalSolutionTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the bare metal solution client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BareMetalSolutionTransport]): The
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
        self._client = BareMetalSolutionClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_instances(
        self,
        request: Union[instance.ListInstancesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstancesAsyncPager:
        r"""List servers in a given project and location.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_list_instances():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListInstancesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_instances(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListInstancesRequest, dict]):
                The request object. Message for requesting the list of
                servers.
            parent (:class:`str`):
                Required. Parent value for
                ListInstancesRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListInstancesAsyncPager:
                Response message for the list of
                servers.
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

        request = instance.ListInstancesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_instances,
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
        response = pagers.ListInstancesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_instance(
        self,
        request: Union[instance.GetInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance.Instance:
        r"""Get details about a single server.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_get_instance():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetInstanceRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_instance(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetInstanceRequest, dict]):
                The request object. Message for requesting server
                information.
            name (:class:`str`):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.Instance:
                A server.
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

        request = instance.GetInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_instance,
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

    async def update_instance(
        self,
        request: Union[gcb_instance.UpdateInstanceRequest, dict] = None,
        *,
        instance: gcb_instance.Instance = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update details of a single server.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_update_instance():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.UpdateInstanceRequest(
                )

                # Make the request
                operation = client.update_instance(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.UpdateInstanceRequest, dict]):
                The request object. Message requesting to updating a
                server.
            instance (:class:`google.cloud.bare_metal_solution_v2.types.Instance`):
                Required. The server to update.

                The ``name`` field is used to identify the instance to
                update. Format:
                projects/{project}/locations/{location}/instances/{instance}

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to update. The currently supported
                fields are: ``labels`` ``hyperthreading_enabled``
                ``os_image``

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

                The result type for the operation will be
                :class:`google.cloud.bare_metal_solution_v2.types.Instance`
                A server.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([instance, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcb_instance.UpdateInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if instance is not None:
            request.instance = instance
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_instance,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("instance.name", request.instance.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcb_instance.Instance,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def reset_instance(
        self,
        request: Union[instance.ResetInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Perform an ungraceful, hard reset on a server.
        Equivalent to shutting the power off and then turning it
        back on.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_reset_instance():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ResetInstanceRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.reset_instance(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ResetInstanceRequest, dict]):
                The request object. Message requesting to reset a
                server.
            name (:class:`str`):
                Required. Name of the resource.
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
                :class:`google.cloud.bare_metal_solution_v2.types.ResetInstanceResponse`
                Response message from resetting a server.

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

        request = instance.ResetInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.reset_instance,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            baremetalsolution.ResetInstanceResponse,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def start_instance(
        self,
        request: Union[instance.StartInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts a server that was shutdown.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_start_instance():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.StartInstanceRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.start_instance(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.StartInstanceRequest, dict]):
                The request object. Message requesting to start a
                server.
            name (:class:`str`):
                Required. Name of the resource.
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
                :class:`google.cloud.bare_metal_solution_v2.types.StartInstanceResponse`
                Response message from starting a server.

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

        request = instance.StartInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_instance,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            instance.StartInstanceResponse,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def stop_instance(
        self,
        request: Union[instance.StopInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Stop a running server.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_stop_instance():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.StopInstanceRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.stop_instance(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.StopInstanceRequest, dict]):
                The request object. Message requesting to stop a server.
            name (:class:`str`):
                Required. Name of the resource.
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
                :class:`google.cloud.bare_metal_solution_v2.types.StopInstanceResponse`
                Response message from stopping a server.

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

        request = instance.StopInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.stop_instance,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            instance.StopInstanceResponse,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def detach_lun(
        self,
        request: Union[gcb_instance.DetachLunRequest, dict] = None,
        *,
        instance: str = None,
        lun: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Detach LUN from Instance.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_detach_lun():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.DetachLunRequest(
                    instance="instance_value",
                    lun="lun_value",
                )

                # Make the request
                operation = client.detach_lun(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.DetachLunRequest, dict]):
                The request object. Message for detach specific LUN from
                an Instance.
            instance (:class:`str`):
                Required. Name of the instance.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            lun (:class:`str`):
                Required. Name of the Lun to detach.
                This corresponds to the ``lun`` field
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
                :class:`google.cloud.bare_metal_solution_v2.types.Instance`
                A server.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([instance, lun])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcb_instance.DetachLunRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if instance is not None:
            request.instance = instance
        if lun is not None:
            request.lun = lun

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.detach_lun,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("instance", request.instance),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcb_instance.Instance,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_volumes(
        self,
        request: Union[volume.ListVolumesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVolumesAsyncPager:
        r"""List storage volumes in a given project and location.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_list_volumes():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListVolumesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_volumes(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListVolumesRequest, dict]):
                The request object. Message for requesting a list of
                storage volumes.
            parent (:class:`str`):
                Required. Parent value for
                ListVolumesRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListVolumesAsyncPager:
                Response message containing the list
                of storage volumes.
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

        request = volume.ListVolumesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_volumes,
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
        response = pagers.ListVolumesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_volume(
        self,
        request: Union[volume.GetVolumeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> volume.Volume:
        r"""Get details of a single storage volume.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_get_volume():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetVolumeRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_volume(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetVolumeRequest, dict]):
                The request object. Message for requesting storage
                volume information.
            name (:class:`str`):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.Volume:
                A storage volume.
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

        request = volume.GetVolumeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_volume,
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

    async def update_volume(
        self,
        request: Union[gcb_volume.UpdateVolumeRequest, dict] = None,
        *,
        volume: gcb_volume.Volume = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update details of a single storage volume.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_update_volume():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.UpdateVolumeRequest(
                )

                # Make the request
                operation = client.update_volume(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.UpdateVolumeRequest, dict]):
                The request object. Message for updating a volume.
            volume (:class:`google.cloud.bare_metal_solution_v2.types.Volume`):
                Required. The volume to update.

                The ``name`` field is used to identify the volume to
                update. Format:
                projects/{project}/locations/{location}/volumes/{volume}

                This corresponds to the ``volume`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to update. The only currently
                supported fields are: ``snapshot_auto_delete_behavior``
                ``snapshot_schedule_policy_name`` 'labels'
                'snapshot_enabled'
                'snapshot_reservation_detail.reserved_space_percent'

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

                The result type for the operation will be
                :class:`google.cloud.bare_metal_solution_v2.types.Volume`
                A storage volume.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([volume, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcb_volume.UpdateVolumeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if volume is not None:
            request.volume = volume
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_volume,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("volume.name", request.volume.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcb_volume.Volume,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def resize_volume(
        self,
        request: Union[gcb_volume.ResizeVolumeRequest, dict] = None,
        *,
        volume: str = None,
        size_gib: int = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Emergency Volume resize.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_resize_volume():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ResizeVolumeRequest(
                    volume="volume_value",
                )

                # Make the request
                operation = client.resize_volume(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ResizeVolumeRequest, dict]):
                The request object. Request for emergency resize Volume.
            volume (:class:`str`):
                Required. Volume to resize.
                This corresponds to the ``volume`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            size_gib (:class:`int`):
                New Volume size, in GiB.
                This corresponds to the ``size_gib`` field
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
                :class:`google.cloud.bare_metal_solution_v2.types.Volume`
                A storage volume.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([volume, size_gib])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcb_volume.ResizeVolumeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if volume is not None:
            request.volume = volume
        if size_gib is not None:
            request.size_gib = size_gib

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.resize_volume,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("volume", request.volume),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcb_volume.Volume,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_networks(
        self,
        request: Union[network.ListNetworksRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNetworksAsyncPager:
        r"""List network in a given project and location.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_list_networks():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListNetworksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_networks(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListNetworksRequest, dict]):
                The request object. Message for requesting a list of
                networks.
            parent (:class:`str`):
                Required. Parent value for
                ListNetworksRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListNetworksAsyncPager:
                Response message containing the list
                of networks.
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

        request = network.ListNetworksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_networks,
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
        response = pagers.ListNetworksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_network_usage(
        self,
        request: Union[network.ListNetworkUsageRequest, dict] = None,
        *,
        location: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> network.ListNetworkUsageResponse:
        r"""List all Networks (and used IPs for each Network) in
        the vendor account associated with the specified
        project.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_list_network_usage():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListNetworkUsageRequest(
                    location="location_value",
                )

                # Make the request
                response = await client.list_network_usage(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListNetworkUsageRequest, dict]):
                The request object. Request to get networks with IPs.
            location (:class:`str`):
                Required. Parent value (project and
                location).

                This corresponds to the ``location`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.ListNetworkUsageResponse:
                Response with Networks with IPs
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([location])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = network.ListNetworkUsageRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if location is not None:
            request.location = location

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_network_usage,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("location", request.location),)),
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

    async def get_network(
        self,
        request: Union[network.GetNetworkRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> network.Network:
        r"""Get details of a single network.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_get_network():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetNetworkRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_network(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetNetworkRequest, dict]):
                The request object. Message for requesting network
                information.
            name (:class:`str`):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.Network:
                A Network.
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

        request = network.GetNetworkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_network,
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

    async def update_network(
        self,
        request: Union[gcb_network.UpdateNetworkRequest, dict] = None,
        *,
        network: gcb_network.Network = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update details of a single network.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_update_network():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.UpdateNetworkRequest(
                )

                # Make the request
                operation = client.update_network(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.UpdateNetworkRequest, dict]):
                The request object. Message requesting to updating a
                network.
            network (:class:`google.cloud.bare_metal_solution_v2.types.Network`):
                Required. The network to update.

                The ``name`` field is used to identify the instance to
                update. Format:
                projects/{project}/locations/{location}/networks/{network}

                This corresponds to the ``network`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to update. The only currently
                supported fields are: ``labels``, ``reservations``

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

                The result type for the operation will be
                :class:`google.cloud.bare_metal_solution_v2.types.Network`
                A Network.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([network, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcb_network.UpdateNetworkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if network is not None:
            request.network = network
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_network,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("network.name", request.network.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcb_network.Network,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_lun(
        self,
        request: Union[lun.GetLunRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> lun.Lun:
        r"""Get details of a single storage logical unit
        number(LUN).

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_get_lun():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetLunRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_lun(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetLunRequest, dict]):
                The request object. Message for requesting storage lun
                information.
            name (:class:`str`):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.Lun:
                A storage volume logical unit number
                (LUN).

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

        request = lun.GetLunRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_lun,
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

    async def list_luns(
        self,
        request: Union[lun.ListLunsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLunsAsyncPager:
        r"""List storage volume luns for given storage volume.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_list_luns():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListLunsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_luns(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListLunsRequest, dict]):
                The request object. Message for requesting a list of
                storage volume luns.
            parent (:class:`str`):
                Required. Parent value for
                ListLunsRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListLunsAsyncPager:
                Response message containing the list
                of storage volume luns.
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

        request = lun.ListLunsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_luns,
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
        response = pagers.ListLunsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_nfs_share(
        self,
        request: Union[nfs_share.GetNfsShareRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> nfs_share.NfsShare:
        r"""Get details of a single NFS share.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_get_nfs_share():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetNfsShareRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_nfs_share(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetNfsShareRequest, dict]):
                The request object. Message for requesting NFS share
                information.
            name (:class:`str`):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.NfsShare:
                An NFS share.
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

        request = nfs_share.GetNfsShareRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_nfs_share,
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

    async def list_nfs_shares(
        self,
        request: Union[nfs_share.ListNfsSharesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNfsSharesAsyncPager:
        r"""List NFS shares.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_list_nfs_shares():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListNfsSharesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_nfs_shares(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListNfsSharesRequest, dict]):
                The request object. Message for requesting a list of NFS
                shares.
            parent (:class:`str`):
                Required. Parent value for
                ListNfsSharesRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListNfsSharesAsyncPager:
                Response message containing the list
                of NFS shares.
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

        request = nfs_share.ListNfsSharesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_nfs_shares,
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
        response = pagers.ListNfsSharesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_nfs_share(
        self,
        request: Union[gcb_nfs_share.UpdateNfsShareRequest, dict] = None,
        *,
        nfs_share: gcb_nfs_share.NfsShare = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update details of a single NFS share.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            async def sample_update_nfs_share():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionAsyncClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.UpdateNfsShareRequest(
                )

                # Make the request
                operation = client.update_nfs_share(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.UpdateNfsShareRequest, dict]):
                The request object. Message requesting to updating a NFS
                share.
            nfs_share (:class:`google.cloud.bare_metal_solution_v2.types.NfsShare`):
                Required. The NFS share to update.

                The ``name`` field is used to identify the NFS share to
                update. Format:
                projects/{project}/locations/{location}/nfsShares/{nfs_share}

                This corresponds to the ``nfs_share`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to update. The only currently
                supported fields are: ``labels``

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

                The result type for the operation will be
                :class:`google.cloud.bare_metal_solution_v2.types.NfsShare`
                An NFS share.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([nfs_share, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcb_nfs_share.UpdateNfsShareRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if nfs_share is not None:
            request.nfs_share = nfs_share
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_nfs_share,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("nfs_share.name", request.nfs_share.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcb_nfs_share.NfsShare,
            metadata_type=baremetalsolution.OperationMetadata,
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
            "google-cloud-bare-metal-solution",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BareMetalSolutionAsyncClient",)
