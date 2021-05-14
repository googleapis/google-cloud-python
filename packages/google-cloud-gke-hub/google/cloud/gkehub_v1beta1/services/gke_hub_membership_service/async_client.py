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
from google.cloud.gkehub_v1beta1.services.gke_hub_membership_service import pagers
from google.cloud.gkehub_v1beta1.types import membership
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import GkeHubMembershipServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import GkeHubMembershipServiceGrpcAsyncIOTransport
from .client import GkeHubMembershipServiceClient


class GkeHubMembershipServiceAsyncClient:
    """GKE Hub CRUD API for the Membership resource.
    The Membership service is currently only available in the global
    location.
    """

    _client: GkeHubMembershipServiceClient

    DEFAULT_ENDPOINT = GkeHubMembershipServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = GkeHubMembershipServiceClient.DEFAULT_MTLS_ENDPOINT

    membership_path = staticmethod(GkeHubMembershipServiceClient.membership_path)
    parse_membership_path = staticmethod(
        GkeHubMembershipServiceClient.parse_membership_path
    )
    common_billing_account_path = staticmethod(
        GkeHubMembershipServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        GkeHubMembershipServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(GkeHubMembershipServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        GkeHubMembershipServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        GkeHubMembershipServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        GkeHubMembershipServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        GkeHubMembershipServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        GkeHubMembershipServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        GkeHubMembershipServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        GkeHubMembershipServiceClient.parse_common_location_path
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
            GkeHubMembershipServiceAsyncClient: The constructed client.
        """
        return GkeHubMembershipServiceClient.from_service_account_info.__func__(GkeHubMembershipServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            GkeHubMembershipServiceAsyncClient: The constructed client.
        """
        return GkeHubMembershipServiceClient.from_service_account_file.__func__(GkeHubMembershipServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> GkeHubMembershipServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            GkeHubMembershipServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(GkeHubMembershipServiceClient).get_transport_class,
        type(GkeHubMembershipServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, GkeHubMembershipServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the gke hub membership service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.GkeHubMembershipServiceTransport]): The
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
        self._client = GkeHubMembershipServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_memberships(
        self,
        request: membership.ListMembershipsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMembershipsAsyncPager:
        r"""Lists Memberships in a given project and location.

        Args:
            request (:class:`google.cloud.gkehub_v1beta1.types.ListMembershipsRequest`):
                The request object. Request message for
                `GkeHubMembershipService.ListMemberships` method.
            parent (:class:`str`):
                Required. The parent (project and location) where the
                Memberships will be listed. Specified in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gkehub_v1beta1.services.gke_hub_membership_service.pagers.ListMembershipsAsyncPager:
                Response message for the
                GkeHubMembershipService.ListMemberships method.

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

        request = membership.ListMembershipsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_memberships,
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
        response = pagers.ListMembershipsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_membership(
        self,
        request: membership.GetMembershipRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> membership.Membership:
        r"""Gets the details of a Membership.

        Args:
            request (:class:`google.cloud.gkehub_v1beta1.types.GetMembershipRequest`):
                The request object. Request message for
                `GkeHubMembershipService.GetMembership` method.
            name (:class:`str`):
                Required. The Membership resource name in the format
                ``projects/*/locations/*/memberships/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gkehub_v1beta1.types.Membership:
                Membership contains information about
                a member cluster.

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

        request = membership.GetMembershipRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_membership,
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

    async def create_membership(
        self,
        request: membership.CreateMembershipRequest = None,
        *,
        parent: str = None,
        resource: membership.Membership = None,
        membership_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Adds a new Membership.

        Args:
            request (:class:`google.cloud.gkehub_v1beta1.types.CreateMembershipRequest`):
                The request object. Request message for the
                `GkeHubMembershipService.CreateMembership` method.
            parent (:class:`str`):
                Required. The parent (project and location) where the
                Memberships will be created. Specified in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (:class:`google.cloud.gkehub_v1beta1.types.Membership`):
                Required. The membership to create.
                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            membership_id (:class:`str`):
                Required. Client chosen ID for the membership.
                ``membership_id`` must be a valid RFC 1123 compliant DNS
                label:

                1. At most 63 characters in length
                2. It must consist of lower case alphanumeric characters
                   or ``-``
                3. It must start and end with an alphanumeric character

                Which can be expressed as the regex:
                ``[a-z0-9]([-a-z0-9]*[a-z0-9])?``, with a maximum length
                of 63 characters.

                This corresponds to the ``membership_id`` field
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
                :class:`google.cloud.gkehub_v1beta1.types.Membership`
                Membership contains information about a member cluster.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, resource, membership_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = membership.CreateMembershipRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if resource is not None:
            request.resource = resource
        if membership_id is not None:
            request.membership_id = membership_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_membership,
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
            membership.Membership,
            metadata_type=membership.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_membership(
        self,
        request: membership.DeleteMembershipRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Removes a Membership.

        Args:
            request (:class:`google.cloud.gkehub_v1beta1.types.DeleteMembershipRequest`):
                The request object. Request message for
                `GkeHubMembershipService.DeleteMembership` method.
            name (:class:`str`):
                Required. The Membership resource name in the format
                ``projects/*/locations/*/memberships/*``.

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

        request = membership.DeleteMembershipRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_membership,
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
            metadata_type=membership.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_membership(
        self,
        request: membership.UpdateMembershipRequest = None,
        *,
        name: str = None,
        resource: membership.Membership = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates an existing Membership.

        Args:
            request (:class:`google.cloud.gkehub_v1beta1.types.UpdateMembershipRequest`):
                The request object. Request message for
                `GkeHubMembershipService.UpdateMembership` method.
            name (:class:`str`):
                Required. The membership resource name in the format:
                ``projects/[project_id]/locations/global/memberships/[membership_id]``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (:class:`google.cloud.gkehub_v1beta1.types.Membership`):
                Required. Only fields specified in update_mask are
                updated. If you specify a field in the update_mask but
                don't specify its value here that field will be deleted.
                If you are updating a map field, set the value of a key
                to null or empty string to delete the key from the map.
                It's not possible to update a key's value to the empty
                string.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Mask of fields to update.
                At least one field path must be
                specified in this mask.

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
                :class:`google.cloud.gkehub_v1beta1.types.Membership`
                Membership contains information about a member cluster.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, resource, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = membership.UpdateMembershipRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if resource is not None:
            request.resource = resource
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_membership,
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
            membership.Membership,
            metadata_type=membership.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def generate_connect_manifest(
        self,
        request: membership.GenerateConnectManifestRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> membership.GenerateConnectManifestResponse:
        r"""Generates the manifest for deployment of the GKE
        connect agent.

        Args:
            request (:class:`google.cloud.gkehub_v1beta1.types.GenerateConnectManifestRequest`):
                The request object. Request message for
                `GkeHubMembershipService.GenerateConnectManifest`
                method. .
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gkehub_v1beta1.types.GenerateConnectManifestResponse:
                GenerateConnectManifestResponse
                contains manifest information for
                installing/upgrading a Connect agent.

        """
        # Create or coerce a protobuf request object.
        request = membership.GenerateConnectManifestRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.generate_connect_manifest,
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

    async def validate_exclusivity(
        self,
        request: membership.ValidateExclusivityRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> membership.ValidateExclusivityResponse:
        r"""ValidateExclusivity validates the state of
        exclusivity in the cluster. The validation does not
        depend on an existing Hub membership resource.

        Args:
            request (:class:`google.cloud.gkehub_v1beta1.types.ValidateExclusivityRequest`):
                The request object. The request to validate the existing
                state of the membership CR in the cluster.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gkehub_v1beta1.types.ValidateExclusivityResponse:
                The response of exclusivity artifacts
                validation result status.

        """
        # Create or coerce a protobuf request object.
        request = membership.ValidateExclusivityRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.validate_exclusivity,
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

    async def generate_exclusivity_manifest(
        self,
        request: membership.GenerateExclusivityManifestRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> membership.GenerateExclusivityManifestResponse:
        r"""GenerateExclusivityManifest generates the manifests
        to update the exclusivity artifacts in the cluster if
        needed.
        Exclusivity artifacts include the Membership custom
        resource definition (CRD) and the singleton Membership
        custom resource (CR). Combined with ValidateExclusivity,
        exclusivity artifacts guarantee that a Kubernetes
        cluster is only registered to a single GKE Hub.

        The Membership CRD is versioned, and may require
        conversion when the GKE Hub API server begins serving a
        newer version of the CRD and corresponding CR. The
        response will be the converted CRD and CR if there are
        any differences between the versions.

        Args:
            request (:class:`google.cloud.gkehub_v1beta1.types.GenerateExclusivityManifestRequest`):
                The request object. The request to generate the
                manifests for exclusivity artifacts.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gkehub_v1beta1.types.GenerateExclusivityManifestResponse:
                The response of the exclusivity
                artifacts manifests for the client to
                apply.

        """
        # Create or coerce a protobuf request object.
        request = membership.GenerateExclusivityManifestRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.generate_exclusivity_manifest,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-gke-hub",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("GkeHubMembershipServiceAsyncClient",)
