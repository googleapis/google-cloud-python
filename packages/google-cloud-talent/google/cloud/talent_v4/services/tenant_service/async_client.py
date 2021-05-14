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

from google.cloud.talent_v4.services.tenant_service import pagers
from google.cloud.talent_v4.types import tenant
from google.cloud.talent_v4.types import tenant as gct_tenant
from google.cloud.talent_v4.types import tenant_service
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import TenantServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import TenantServiceGrpcAsyncIOTransport
from .client import TenantServiceClient


class TenantServiceAsyncClient:
    """A service that handles tenant management, including CRUD and
    enumeration.
    """

    _client: TenantServiceClient

    DEFAULT_ENDPOINT = TenantServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TenantServiceClient.DEFAULT_MTLS_ENDPOINT

    tenant_path = staticmethod(TenantServiceClient.tenant_path)
    parse_tenant_path = staticmethod(TenantServiceClient.parse_tenant_path)
    common_billing_account_path = staticmethod(
        TenantServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        TenantServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TenantServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        TenantServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        TenantServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        TenantServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TenantServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        TenantServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(TenantServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        TenantServiceClient.parse_common_location_path
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
            TenantServiceAsyncClient: The constructed client.
        """
        return TenantServiceClient.from_service_account_info.__func__(TenantServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            TenantServiceAsyncClient: The constructed client.
        """
        return TenantServiceClient.from_service_account_file.__func__(TenantServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> TenantServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            TenantServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(TenantServiceClient).get_transport_class, type(TenantServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, TenantServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the tenant service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TenantServiceTransport]): The
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
        self._client = TenantServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_tenant(
        self,
        request: tenant_service.CreateTenantRequest = None,
        *,
        parent: str = None,
        tenant: gct_tenant.Tenant = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_tenant.Tenant:
        r"""Creates a new tenant entity.

        Args:
            request (:class:`google.cloud.talent_v4.types.CreateTenantRequest`):
                The request object. The Request of the CreateTenant
                method.
            parent (:class:`str`):
                Required. Resource name of the project under which the
                tenant is created.

                The format is "projects/{project_id}", for example,
                "projects/foo".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            tenant (:class:`google.cloud.talent_v4.types.Tenant`):
                Required. The tenant to be created.
                This corresponds to the ``tenant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.Tenant:
                A Tenant resource represents a tenant
                in the service. A tenant is a group or
                entity that shares common access with
                specific privileges for resources like
                jobs. Customer may create multiple
                tenants to provide data isolation for
                different groups.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, tenant])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = tenant_service.CreateTenantRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if tenant is not None:
            request.tenant = tenant

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_tenant,
            default_timeout=30.0,
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

    async def get_tenant(
        self,
        request: tenant_service.GetTenantRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> tenant.Tenant:
        r"""Retrieves specified tenant.

        Args:
            request (:class:`google.cloud.talent_v4.types.GetTenantRequest`):
                The request object. Request for getting a tenant by
                name.
            name (:class:`str`):
                Required. The resource name of the tenant to be
                retrieved.

                The format is
                "projects/{project_id}/tenants/{tenant_id}", for
                example, "projects/foo/tenants/bar".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.Tenant:
                A Tenant resource represents a tenant
                in the service. A tenant is a group or
                entity that shares common access with
                specific privileges for resources like
                jobs. Customer may create multiple
                tenants to provide data isolation for
                different groups.

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

        request = tenant_service.GetTenantRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_tenant,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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

    async def update_tenant(
        self,
        request: tenant_service.UpdateTenantRequest = None,
        *,
        tenant: gct_tenant.Tenant = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_tenant.Tenant:
        r"""Updates specified tenant.

        Args:
            request (:class:`google.cloud.talent_v4.types.UpdateTenantRequest`):
                The request object. Request for updating a specified
                tenant.
            tenant (:class:`google.cloud.talent_v4.types.Tenant`):
                Required. The tenant resource to
                replace the current resource in the
                system.

                This corresponds to the ``tenant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Strongly recommended for the best service experience.

                If
                [update_mask][google.cloud.talent.v4.UpdateTenantRequest.update_mask]
                is provided, only the specified fields in
                [tenant][google.cloud.talent.v4.UpdateTenantRequest.tenant]
                are updated. Otherwise all the fields are updated.

                A field mask to specify the tenant fields to be updated.
                Only top level fields of
                [Tenant][google.cloud.talent.v4.Tenant] are supported.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.Tenant:
                A Tenant resource represents a tenant
                in the service. A tenant is a group or
                entity that shares common access with
                specific privileges for resources like
                jobs. Customer may create multiple
                tenants to provide data isolation for
                different groups.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tenant, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = tenant_service.UpdateTenantRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if tenant is not None:
            request.tenant = tenant
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_tenant,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("tenant.name", request.tenant.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_tenant(
        self,
        request: tenant_service.DeleteTenantRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes specified tenant.

        Args:
            request (:class:`google.cloud.talent_v4.types.DeleteTenantRequest`):
                The request object. Request to delete a tenant.
            name (:class:`str`):
                Required. The resource name of the tenant to be deleted.

                The format is
                "projects/{project_id}/tenants/{tenant_id}", for
                example, "projects/foo/tenants/bar".

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

        request = tenant_service.DeleteTenantRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_tenant,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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

    async def list_tenants(
        self,
        request: tenant_service.ListTenantsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTenantsAsyncPager:
        r"""Lists all tenants associated with the project.

        Args:
            request (:class:`google.cloud.talent_v4.types.ListTenantsRequest`):
                The request object. List tenants for which the client
                has ACL visibility.
            parent (:class:`str`):
                Required. Resource name of the project under which the
                tenant is created.

                The format is "projects/{project_id}", for example,
                "projects/foo".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.services.tenant_service.pagers.ListTenantsAsyncPager:
                The List tenants response object.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = tenant_service.ListTenantsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_tenants,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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
        response = pagers.ListTenantsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-talent",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TenantServiceAsyncClient",)
