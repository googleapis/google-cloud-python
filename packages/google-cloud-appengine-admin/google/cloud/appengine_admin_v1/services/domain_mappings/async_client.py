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

from google.api_core import operation as gac_operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.appengine_admin_v1.services.domain_mappings import pagers
from google.cloud.appengine_admin_v1.types import appengine
from google.cloud.appengine_admin_v1.types import domain_mapping
from google.cloud.appengine_admin_v1.types import operation as ga_operation
from google.protobuf import empty_pb2  # type: ignore
from .transports.base import DomainMappingsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import DomainMappingsGrpcAsyncIOTransport
from .client import DomainMappingsClient


class DomainMappingsAsyncClient:
    """Manages domains serving an application."""

    _client: DomainMappingsClient

    DEFAULT_ENDPOINT = DomainMappingsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DomainMappingsClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        DomainMappingsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DomainMappingsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DomainMappingsClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        DomainMappingsClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        DomainMappingsClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        DomainMappingsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DomainMappingsClient.common_project_path)
    parse_common_project_path = staticmethod(
        DomainMappingsClient.parse_common_project_path
    )
    common_location_path = staticmethod(DomainMappingsClient.common_location_path)
    parse_common_location_path = staticmethod(
        DomainMappingsClient.parse_common_location_path
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
            DomainMappingsAsyncClient: The constructed client.
        """
        return DomainMappingsClient.from_service_account_info.__func__(DomainMappingsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            DomainMappingsAsyncClient: The constructed client.
        """
        return DomainMappingsClient.from_service_account_file.__func__(DomainMappingsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DomainMappingsTransport:
        """Returns the transport used by the client instance.

        Returns:
            DomainMappingsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DomainMappingsClient).get_transport_class, type(DomainMappingsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, DomainMappingsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the domain mappings client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DomainMappingsTransport]): The
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
        self._client = DomainMappingsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_domain_mappings(
        self,
        request: appengine.ListDomainMappingsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDomainMappingsAsyncPager:
        r"""Lists the domain mappings on an application.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.ListDomainMappingsRequest`):
                The request object. Request message for
                `DomainMappings.ListDomainMappings`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.services.domain_mappings.pagers.ListDomainMappingsAsyncPager:
                Response message for DomainMappings.ListDomainMappings.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = appengine.ListDomainMappingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_domain_mappings,
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
        response = pagers.ListDomainMappingsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_domain_mapping(
        self,
        request: appengine.GetDomainMappingRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> domain_mapping.DomainMapping:
        r"""Gets the specified domain mapping.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.GetDomainMappingRequest`):
                The request object. Request message for
                `DomainMappings.GetDomainMapping`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.DomainMapping:
                A domain serving an App Engine
                application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.GetDomainMappingRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_domain_mapping,
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

    async def create_domain_mapping(
        self,
        request: appengine.CreateDomainMappingRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Maps a domain to an application. A user must be authorized to
        administer a domain in order to map it to an application. For a
        list of available authorized domains, see
        ```AuthorizedDomains.ListAuthorizedDomains`` <>`__.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.CreateDomainMappingRequest`):
                The request object. Request message for
                `DomainMappings.CreateDomainMapping`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.appengine_admin_v1.types.DomainMapping`
                A domain serving an App Engine application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.CreateDomainMappingRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_domain_mapping,
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
            domain_mapping.DomainMapping,
            metadata_type=ga_operation.OperationMetadataV1,
        )

        # Done; return the response.
        return response

    async def update_domain_mapping(
        self,
        request: appengine.UpdateDomainMappingRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the specified domain mapping. To map an SSL certificate
        to a domain mapping, update ``certificate_id`` to point to an
        ``AuthorizedCertificate`` resource. A user must be authorized to
        administer the associated domain in order to update a
        ``DomainMapping`` resource.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.UpdateDomainMappingRequest`):
                The request object. Request message for
                `DomainMappings.UpdateDomainMapping`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.appengine_admin_v1.types.DomainMapping`
                A domain serving an App Engine application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.UpdateDomainMappingRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_domain_mapping,
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
            domain_mapping.DomainMapping,
            metadata_type=ga_operation.OperationMetadataV1,
        )

        # Done; return the response.
        return response

    async def delete_domain_mapping(
        self,
        request: appengine.DeleteDomainMappingRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes the specified domain mapping. A user must be authorized
        to administer the associated domain in order to delete a
        ``DomainMapping`` resource.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.DeleteDomainMappingRequest`):
                The request object. Request message for
                `DomainMappings.DeleteDomainMapping`.
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
        request = appengine.DeleteDomainMappingRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_domain_mapping,
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
            metadata_type=ga_operation.OperationMetadataV1,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-appengine-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DomainMappingsAsyncClient",)
