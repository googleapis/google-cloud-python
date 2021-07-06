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

from google.cloud.iap_v1.services.identity_aware_proxy_o_auth_service import pagers
from google.cloud.iap_v1.types import service
from .transports.base import (
    IdentityAwareProxyOAuthServiceTransport,
    DEFAULT_CLIENT_INFO,
)
from .transports.grpc_asyncio import IdentityAwareProxyOAuthServiceGrpcAsyncIOTransport
from .client import IdentityAwareProxyOAuthServiceClient


class IdentityAwareProxyOAuthServiceAsyncClient:
    """API to programmatically create, list and retrieve Identity
    Aware Proxy (IAP) OAuth brands; and create, retrieve, delete and
    reset-secret of IAP OAuth clients.
    """

    _client: IdentityAwareProxyOAuthServiceClient

    DEFAULT_ENDPOINT = IdentityAwareProxyOAuthServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = IdentityAwareProxyOAuthServiceClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.common_folder_path
    )
    parse_common_folder_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        IdentityAwareProxyOAuthServiceClient.parse_common_location_path
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
            IdentityAwareProxyOAuthServiceAsyncClient: The constructed client.
        """
        return IdentityAwareProxyOAuthServiceClient.from_service_account_info.__func__(IdentityAwareProxyOAuthServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            IdentityAwareProxyOAuthServiceAsyncClient: The constructed client.
        """
        return IdentityAwareProxyOAuthServiceClient.from_service_account_file.__func__(IdentityAwareProxyOAuthServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> IdentityAwareProxyOAuthServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            IdentityAwareProxyOAuthServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(IdentityAwareProxyOAuthServiceClient).get_transport_class,
        type(IdentityAwareProxyOAuthServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, IdentityAwareProxyOAuthServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the identity aware proxy o auth service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.IdentityAwareProxyOAuthServiceTransport]): The
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
        self._client = IdentityAwareProxyOAuthServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_brands(
        self,
        request: service.ListBrandsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.ListBrandsResponse:
        r"""Lists the existing brands for the project.

        Args:
            request (:class:`google.cloud.iap_v1.types.ListBrandsRequest`):
                The request object. The request sent to ListBrands.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iap_v1.types.ListBrandsResponse:
                Response message for ListBrands.
        """
        # Create or coerce a protobuf request object.
        request = service.ListBrandsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_brands,
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

    async def create_brand(
        self,
        request: service.CreateBrandRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.Brand:
        r"""Constructs a new OAuth brand for the project if one
        does not exist. The created brand is "internal only",
        meaning that OAuth clients created under it only accept
        requests from users who belong to the same G Suite
        organization as the project. The brand is created in an
        un-reviewed status. NOTE: The "internal only" status can
        be manually changed in the Google Cloud console.
        Requires that a brand does not already exist for the
        project, and that the specified support email is owned
        by the caller.

        Args:
            request (:class:`google.cloud.iap_v1.types.CreateBrandRequest`):
                The request object. The request sent to CreateBrand.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iap_v1.types.Brand:
                OAuth brand data.
                NOTE: Only contains a portion of the
                data that describes a brand.

        """
        # Create or coerce a protobuf request object.
        request = service.CreateBrandRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_brand,
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

    async def get_brand(
        self,
        request: service.GetBrandRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.Brand:
        r"""Retrieves the OAuth brand of the project.

        Args:
            request (:class:`google.cloud.iap_v1.types.GetBrandRequest`):
                The request object. The request sent to GetBrand.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iap_v1.types.Brand:
                OAuth brand data.
                NOTE: Only contains a portion of the
                data that describes a brand.

        """
        # Create or coerce a protobuf request object.
        request = service.GetBrandRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_brand,
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

    async def create_identity_aware_proxy_client(
        self,
        request: service.CreateIdentityAwareProxyClientRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.IdentityAwareProxyClient:
        r"""Creates an Identity Aware Proxy (IAP) OAuth client.
        The client is owned by IAP. Requires that the brand for
        the project exists and that it is set for internal-only
        use.

        Args:
            request (:class:`google.cloud.iap_v1.types.CreateIdentityAwareProxyClientRequest`):
                The request object. The request sent to
                CreateIdentityAwareProxyClient.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iap_v1.types.IdentityAwareProxyClient:
                Contains the data that describes an
                Identity Aware Proxy owned client.

        """
        # Create or coerce a protobuf request object.
        request = service.CreateIdentityAwareProxyClientRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_identity_aware_proxy_client,
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

    async def list_identity_aware_proxy_clients(
        self,
        request: service.ListIdentityAwareProxyClientsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIdentityAwareProxyClientsAsyncPager:
        r"""Lists the existing clients for the brand.

        Args:
            request (:class:`google.cloud.iap_v1.types.ListIdentityAwareProxyClientsRequest`):
                The request object. The request sent to
                ListIdentityAwareProxyClients.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iap_v1.services.identity_aware_proxy_o_auth_service.pagers.ListIdentityAwareProxyClientsAsyncPager:
                Response message for
                ListIdentityAwareProxyClients.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListIdentityAwareProxyClientsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_identity_aware_proxy_clients,
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
        response = pagers.ListIdentityAwareProxyClientsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_identity_aware_proxy_client(
        self,
        request: service.GetIdentityAwareProxyClientRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.IdentityAwareProxyClient:
        r"""Retrieves an Identity Aware Proxy (IAP) OAuth client.
        Requires that the client is owned by IAP.

        Args:
            request (:class:`google.cloud.iap_v1.types.GetIdentityAwareProxyClientRequest`):
                The request object. The request sent to
                GetIdentityAwareProxyClient.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iap_v1.types.IdentityAwareProxyClient:
                Contains the data that describes an
                Identity Aware Proxy owned client.

        """
        # Create or coerce a protobuf request object.
        request = service.GetIdentityAwareProxyClientRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_identity_aware_proxy_client,
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

    async def reset_identity_aware_proxy_client_secret(
        self,
        request: service.ResetIdentityAwareProxyClientSecretRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.IdentityAwareProxyClient:
        r"""Resets an Identity Aware Proxy (IAP) OAuth client
        secret. Useful if the secret was compromised. Requires
        that the client is owned by IAP.

        Args:
            request (:class:`google.cloud.iap_v1.types.ResetIdentityAwareProxyClientSecretRequest`):
                The request object. The request sent to
                ResetIdentityAwareProxyClientSecret.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iap_v1.types.IdentityAwareProxyClient:
                Contains the data that describes an
                Identity Aware Proxy owned client.

        """
        # Create or coerce a protobuf request object.
        request = service.ResetIdentityAwareProxyClientSecretRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.reset_identity_aware_proxy_client_secret,
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

    async def delete_identity_aware_proxy_client(
        self,
        request: service.DeleteIdentityAwareProxyClientRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an Identity Aware Proxy (IAP) OAuth client.
        Useful for removing obsolete clients, managing the
        number of clients in a given project, and cleaning up
        after tests. Requires that the client is owned by IAP.

        Args:
            request (:class:`google.cloud.iap_v1.types.DeleteIdentityAwareProxyClientRequest`):
                The request object. The request sent to
                DeleteIdentityAwareProxyClient.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = service.DeleteIdentityAwareProxyClientRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_identity_aware_proxy_client,
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
        gapic_version=pkg_resources.get_distribution("google-cloud-iap",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("IdentityAwareProxyOAuthServiceAsyncClient",)
