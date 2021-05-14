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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.networkconnectivity_v1alpha1.services.hub_service import pagers
from google.cloud.networkconnectivity_v1alpha1.types import common
from google.cloud.networkconnectivity_v1alpha1.types import hub
from google.cloud.networkconnectivity_v1alpha1.types import hub as gcn_hub
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import HubServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import HubServiceGrpcAsyncIOTransport
from .client import HubServiceClient


class HubServiceAsyncClient:
    """Network Connectivity Center is a hub-and-spoke abstraction
    for network connectivity management in Google Cloud. It reduces
    operational complexity through a simple, centralized
    connectivity management model.
    """

    _client: HubServiceClient

    DEFAULT_ENDPOINT = HubServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = HubServiceClient.DEFAULT_MTLS_ENDPOINT

    hub_path = staticmethod(HubServiceClient.hub_path)
    parse_hub_path = staticmethod(HubServiceClient.parse_hub_path)
    instance_path = staticmethod(HubServiceClient.instance_path)
    parse_instance_path = staticmethod(HubServiceClient.parse_instance_path)
    interconnect_attachment_path = staticmethod(
        HubServiceClient.interconnect_attachment_path
    )
    parse_interconnect_attachment_path = staticmethod(
        HubServiceClient.parse_interconnect_attachment_path
    )
    spoke_path = staticmethod(HubServiceClient.spoke_path)
    parse_spoke_path = staticmethod(HubServiceClient.parse_spoke_path)
    vpn_tunnel_path = staticmethod(HubServiceClient.vpn_tunnel_path)
    parse_vpn_tunnel_path = staticmethod(HubServiceClient.parse_vpn_tunnel_path)
    common_billing_account_path = staticmethod(
        HubServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        HubServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(HubServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(HubServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(HubServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        HubServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(HubServiceClient.common_project_path)
    parse_common_project_path = staticmethod(HubServiceClient.parse_common_project_path)
    common_location_path = staticmethod(HubServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        HubServiceClient.parse_common_location_path
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
            HubServiceAsyncClient: The constructed client.
        """
        return HubServiceClient.from_service_account_info.__func__(HubServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            HubServiceAsyncClient: The constructed client.
        """
        return HubServiceClient.from_service_account_file.__func__(HubServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> HubServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            HubServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(HubServiceClient).get_transport_class, type(HubServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, HubServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the hub service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.HubServiceTransport]): The
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
        self._client = HubServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_hubs(
        self,
        request: hub.ListHubsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListHubsAsyncPager:
        r"""Lists Hubs in a given project and location.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.ListHubsRequest`):
                The request object. Request for
                [HubService.ListHubs][google.cloud.networkconnectivity.v1alpha1.HubService.ListHubs]
                method.
            parent (:class:`str`):
                Required. The parent resource's name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.networkconnectivity_v1alpha1.services.hub_service.pagers.ListHubsAsyncPager:
                Response for
                [HubService.ListHubs][google.cloud.networkconnectivity.v1alpha1.HubService.ListHubs]
                method.

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

        request = hub.ListHubsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_hubs,
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
        response = pagers.ListHubsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_hub(
        self,
        request: hub.GetHubRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> hub.Hub:
        r"""Gets details of a single Hub.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.GetHubRequest`):
                The request object. Request for
                [HubService.GetHub][google.cloud.networkconnectivity.v1alpha1.HubService.GetHub]
                method.
            name (:class:`str`):
                Required. Name of the Hub resource to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.networkconnectivity_v1alpha1.types.Hub:
                Network Connectivity Center is a hub-
                nd-spoke abstraction for network
                connectivity management in Google Cloud.
                It reduces operational complexity
                through a simple, centralized
                connectivity management model. Following
                is the resource message of a hub.

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

        request = hub.GetHubRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_hub,
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

    async def create_hub(
        self,
        request: gcn_hub.CreateHubRequest = None,
        *,
        parent: str = None,
        hub: gcn_hub.Hub = None,
        hub_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Hub in a given project and location.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.CreateHubRequest`):
                The request object. Request for
                [HubService.CreateHub][google.cloud.networkconnectivity.v1alpha1.HubService.CreateHub]
                method.
            parent (:class:`str`):
                Required. The parent resource's name
                of the Hub.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            hub (:class:`google.cloud.networkconnectivity_v1alpha1.types.Hub`):
                Required. Initial values for a new
                Hub.

                This corresponds to the ``hub`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            hub_id (:class:`str`):
                Optional. Unique id for the Hub to
                create.

                This corresponds to the ``hub_id`` field
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

                The result type for the operation will be :class:`google.cloud.networkconnectivity_v1alpha1.types.Hub` Network Connectivity Center is a hub-and-spoke abstraction for
                   network connectivity management in Google Cloud. It
                   reduces operational complexity through a simple,
                   centralized connectivity management model. Following
                   is the resource message of a hub.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, hub, hub_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcn_hub.CreateHubRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if hub is not None:
            request.hub = hub
        if hub_id is not None:
            request.hub_id = hub_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_hub,
            default_timeout=60.0,
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
            gcn_hub.Hub,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_hub(
        self,
        request: gcn_hub.UpdateHubRequest = None,
        *,
        hub: gcn_hub.Hub = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single Hub.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.UpdateHubRequest`):
                The request object. Request for
                [HubService.UpdateHub][google.cloud.networkconnectivity.v1alpha1.HubService.UpdateHub]
                method.
            hub (:class:`google.cloud.networkconnectivity_v1alpha1.types.Hub`):
                Required. The state that the Hub
                should be in after the update.

                This corresponds to the ``hub`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. Field mask is used to specify the fields to be
                overwritten in the Hub resource by the update. The
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

                The result type for the operation will be :class:`google.cloud.networkconnectivity_v1alpha1.types.Hub` Network Connectivity Center is a hub-and-spoke abstraction for
                   network connectivity management in Google Cloud. It
                   reduces operational complexity through a simple,
                   centralized connectivity management model. Following
                   is the resource message of a hub.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([hub, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcn_hub.UpdateHubRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if hub is not None:
            request.hub = hub
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_hub,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("hub.name", request.hub.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcn_hub.Hub,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_hub(
        self,
        request: hub.DeleteHubRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Hub.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.DeleteHubRequest`):
                The request object. The request for
                [HubService.DeleteHub][google.cloud.networkconnectivity.v1alpha1.HubService.DeleteHub].
            name (:class:`str`):
                Required. The name of the Hub to
                delete.

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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = hub.DeleteHubRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_hub,
            default_timeout=60.0,
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
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_spokes(
        self,
        request: hub.ListSpokesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSpokesAsyncPager:
        r"""Lists Spokes in a given project and location.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.ListSpokesRequest`):
                The request object. The request for
                [HubService.ListSpokes][google.cloud.networkconnectivity.v1alpha1.HubService.ListSpokes].
            parent (:class:`str`):
                Required. The parent's resource name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.networkconnectivity_v1alpha1.services.hub_service.pagers.ListSpokesAsyncPager:
                The response for
                [HubService.ListSpokes][google.cloud.networkconnectivity.v1alpha1.HubService.ListSpokes].

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

        request = hub.ListSpokesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_spokes,
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
        response = pagers.ListSpokesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_spoke(
        self,
        request: hub.GetSpokeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> hub.Spoke:
        r"""Gets details of a single Spoke.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.GetSpokeRequest`):
                The request object. The request for
                [HubService.GetSpoke][google.cloud.networkconnectivity.v1alpha1.HubService.GetSpoke].
            name (:class:`str`):
                Required. The name of Spoke resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.networkconnectivity_v1alpha1.types.Spoke:
                A Spoke is an  abstraction of a
                network attachment being attached to a
                Hub. A Spoke can be underlying a VPN
                tunnel, a VLAN (interconnect)
                attachment, a Router appliance, etc.

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

        request = hub.GetSpokeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_spoke,
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

    async def create_spoke(
        self,
        request: hub.CreateSpokeRequest = None,
        *,
        parent: str = None,
        spoke: hub.Spoke = None,
        spoke_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Spoke in a given project and location.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.CreateSpokeRequest`):
                The request object. The request for
                [HubService.CreateSpoke][google.cloud.networkconnectivity.v1alpha1.HubService.CreateSpoke].
            parent (:class:`str`):
                Required. The parent's resource name
                of the Spoke.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            spoke (:class:`google.cloud.networkconnectivity_v1alpha1.types.Spoke`):
                Required. Initial values for a new
                Hub.

                This corresponds to the ``spoke`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            spoke_id (:class:`str`):
                Optional. Unique id for the Spoke to
                create.

                This corresponds to the ``spoke_id`` field
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

                The result type for the operation will be :class:`google.cloud.networkconnectivity_v1alpha1.types.Spoke` A Spoke is an abstraction of a network attachment being attached
                   to a Hub. A Spoke can be underlying a VPN tunnel, a
                   VLAN (interconnect) attachment, a Router appliance,
                   etc.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, spoke, spoke_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = hub.CreateSpokeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if spoke is not None:
            request.spoke = spoke
        if spoke_id is not None:
            request.spoke_id = spoke_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_spoke,
            default_timeout=60.0,
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
            hub.Spoke,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_spoke(
        self,
        request: hub.UpdateSpokeRequest = None,
        *,
        spoke: hub.Spoke = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single Spoke.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.UpdateSpokeRequest`):
                The request object. Request for
                [HubService.UpdateSpoke][google.cloud.networkconnectivity.v1alpha1.HubService.UpdateSpoke]
                method.
            spoke (:class:`google.cloud.networkconnectivity_v1alpha1.types.Spoke`):
                Required. The state that the Spoke
                should be in after the update.

                This corresponds to the ``spoke`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. Field mask is used to specify the fields to be
                overwritten in the Spoke resource by the update. The
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

                The result type for the operation will be :class:`google.cloud.networkconnectivity_v1alpha1.types.Spoke` A Spoke is an abstraction of a network attachment being attached
                   to a Hub. A Spoke can be underlying a VPN tunnel, a
                   VLAN (interconnect) attachment, a Router appliance,
                   etc.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([spoke, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = hub.UpdateSpokeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if spoke is not None:
            request.spoke = spoke
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_spoke,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("spoke.name", request.spoke.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            hub.Spoke,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_spoke(
        self,
        request: hub.DeleteSpokeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Spoke.

        Args:
            request (:class:`google.cloud.networkconnectivity_v1alpha1.types.DeleteSpokeRequest`):
                The request object. The request for
                [HubService.DeleteSpoke][google.cloud.networkconnectivity.v1alpha1.HubService.DeleteSpoke].
            name (:class:`str`):
                Required. The name of the Spoke to
                delete.

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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = hub.DeleteSpokeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_spoke,
            default_timeout=60.0,
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
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-network-connectivity",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("HubServiceAsyncClient",)
