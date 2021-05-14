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
from google.cloud.apigateway_v1.services.api_gateway_service import pagers
from google.cloud.apigateway_v1.types import apigateway
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import ApiGatewayServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ApiGatewayServiceGrpcAsyncIOTransport
from .client import ApiGatewayServiceClient


class ApiGatewayServiceAsyncClient:
    """The API Gateway Service is the interface for managing API
    Gateways.
    """

    _client: ApiGatewayServiceClient

    DEFAULT_ENDPOINT = ApiGatewayServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ApiGatewayServiceClient.DEFAULT_MTLS_ENDPOINT

    api_path = staticmethod(ApiGatewayServiceClient.api_path)
    parse_api_path = staticmethod(ApiGatewayServiceClient.parse_api_path)
    api_config_path = staticmethod(ApiGatewayServiceClient.api_config_path)
    parse_api_config_path = staticmethod(ApiGatewayServiceClient.parse_api_config_path)
    gateway_path = staticmethod(ApiGatewayServiceClient.gateway_path)
    parse_gateway_path = staticmethod(ApiGatewayServiceClient.parse_gateway_path)
    managed_service_path = staticmethod(ApiGatewayServiceClient.managed_service_path)
    parse_managed_service_path = staticmethod(
        ApiGatewayServiceClient.parse_managed_service_path
    )
    service_path = staticmethod(ApiGatewayServiceClient.service_path)
    parse_service_path = staticmethod(ApiGatewayServiceClient.parse_service_path)
    service_account_path = staticmethod(ApiGatewayServiceClient.service_account_path)
    parse_service_account_path = staticmethod(
        ApiGatewayServiceClient.parse_service_account_path
    )
    common_billing_account_path = staticmethod(
        ApiGatewayServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ApiGatewayServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ApiGatewayServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ApiGatewayServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ApiGatewayServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ApiGatewayServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ApiGatewayServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ApiGatewayServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ApiGatewayServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ApiGatewayServiceClient.parse_common_location_path
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
            ApiGatewayServiceAsyncClient: The constructed client.
        """
        return ApiGatewayServiceClient.from_service_account_info.__func__(ApiGatewayServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ApiGatewayServiceAsyncClient: The constructed client.
        """
        return ApiGatewayServiceClient.from_service_account_file.__func__(ApiGatewayServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ApiGatewayServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ApiGatewayServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ApiGatewayServiceClient).get_transport_class, type(ApiGatewayServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ApiGatewayServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the api gateway service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ApiGatewayServiceTransport]): The
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
        self._client = ApiGatewayServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_gateways(
        self,
        request: apigateway.ListGatewaysRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGatewaysAsyncPager:
        r"""Lists Gateways in a given project and location.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.ListGatewaysRequest`):
                The request object. Request message for
                ApiGatewayService.ListGateways
            parent (:class:`str`):
                Required. Parent resource of the Gateway, of the form:
                ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigateway_v1.services.api_gateway_service.pagers.ListGatewaysAsyncPager:
                Response message for
                ApiGatewayService.ListGateways
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

        request = apigateway.ListGatewaysRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_gateways,
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
        response = pagers.ListGatewaysAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_gateway(
        self,
        request: apigateway.GetGatewayRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> apigateway.Gateway:
        r"""Gets details of a single Gateway.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.GetGatewayRequest`):
                The request object. Request message for
                ApiGatewayService.GetGateway
            name (:class:`str`):
                Required. Resource name of the form:
                ``projects/*/locations/*/gateways/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigateway_v1.types.Gateway:
                A Gateway is an API-aware HTTP proxy.
                It performs API-Method and/or API-
                Consumer specific actions based on an
                API Config such as authentication,
                policy enforcement, and backend
                selection.

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

        request = apigateway.GetGatewayRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_gateway,
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

    async def create_gateway(
        self,
        request: apigateway.CreateGatewayRequest = None,
        *,
        parent: str = None,
        gateway: apigateway.Gateway = None,
        gateway_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Gateway in a given project and
        location.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.CreateGatewayRequest`):
                The request object. Request message for
                ApiGatewayService.CreateGateway
            parent (:class:`str`):
                Required. Parent resource of the Gateway, of the form:
                ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            gateway (:class:`google.cloud.apigateway_v1.types.Gateway`):
                Required. Gateway resource.
                This corresponds to the ``gateway`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            gateway_id (:class:`str`):
                Required. Identifier to assign to the
                Gateway. Must be unique within scope of
                the parent resource.

                This corresponds to the ``gateway_id`` field
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

                The result type for the operation will be :class:`google.cloud.apigateway_v1.types.Gateway` A Gateway is an API-aware HTTP proxy. It performs API-Method and/or
                   API-Consumer specific actions based on an API Config
                   such as authentication, policy enforcement, and
                   backend selection.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, gateway, gateway_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = apigateway.CreateGatewayRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if gateway is not None:
            request.gateway = gateway
        if gateway_id is not None:
            request.gateway_id = gateway_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_gateway,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            apigateway.Gateway,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_gateway(
        self,
        request: apigateway.UpdateGatewayRequest = None,
        *,
        gateway: apigateway.Gateway = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single Gateway.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.UpdateGatewayRequest`):
                The request object. Request message for
                ApiGatewayService.UpdateGateway
            gateway (:class:`google.cloud.apigateway_v1.types.Gateway`):
                Required. Gateway resource.
                This corresponds to the ``gateway`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the Gateway resource by the update. The
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

                The result type for the operation will be :class:`google.cloud.apigateway_v1.types.Gateway` A Gateway is an API-aware HTTP proxy. It performs API-Method and/or
                   API-Consumer specific actions based on an API Config
                   such as authentication, policy enforcement, and
                   backend selection.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([gateway, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = apigateway.UpdateGatewayRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if gateway is not None:
            request.gateway = gateway
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_gateway,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("gateway.name", request.gateway.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            apigateway.Gateway,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_gateway(
        self,
        request: apigateway.DeleteGatewayRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Gateway.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.DeleteGatewayRequest`):
                The request object. Request message for
                ApiGatewayService.DeleteGateway
            name (:class:`str`):
                Required. Resource name of the form:
                ``projects/*/locations/*/gateways/*``

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

        request = apigateway.DeleteGatewayRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_gateway,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_apis(
        self,
        request: apigateway.ListApisRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApisAsyncPager:
        r"""Lists Apis in a given project and location.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.ListApisRequest`):
                The request object. Request message for
                ApiGatewayService.ListApis
            parent (:class:`str`):
                Required. Parent resource of the API, of the form:
                ``projects/*/locations/global``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigateway_v1.services.api_gateway_service.pagers.ListApisAsyncPager:
                Response message for
                ApiGatewayService.ListApis
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

        request = apigateway.ListApisRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_apis,
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
        response = pagers.ListApisAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_api(
        self,
        request: apigateway.GetApiRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> apigateway.Api:
        r"""Gets details of a single Api.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.GetApiRequest`):
                The request object. Request message for
                ApiGatewayService.GetApi
            name (:class:`str`):
                Required. Resource name of the form:
                ``projects/*/locations/global/apis/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigateway_v1.types.Api:
                An API that can be served by one or
                more Gateways.

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

        request = apigateway.GetApiRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_api,
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

    async def create_api(
        self,
        request: apigateway.CreateApiRequest = None,
        *,
        parent: str = None,
        api: apigateway.Api = None,
        api_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Api in a given project and location.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.CreateApiRequest`):
                The request object. Request message for
                ApiGatewayService.CreateApi
            parent (:class:`str`):
                Required. Parent resource of the API, of the form:
                ``projects/*/locations/global``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api (:class:`google.cloud.apigateway_v1.types.Api`):
                Required. API resource.
                This corresponds to the ``api`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_id (:class:`str`):
                Required. Identifier to assign to the
                API. Must be unique within scope of the
                parent resource.

                This corresponds to the ``api_id`` field
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
                :class:`google.cloud.apigateway_v1.types.Api` An API
                that can be served by one or more Gateways.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, api, api_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = apigateway.CreateApiRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if api is not None:
            request.api = api
        if api_id is not None:
            request.api_id = api_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_api,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            apigateway.Api,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_api(
        self,
        request: apigateway.UpdateApiRequest = None,
        *,
        api: apigateway.Api = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single Api.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.UpdateApiRequest`):
                The request object. Request message for
                ApiGatewayService.UpdateApi
            api (:class:`google.cloud.apigateway_v1.types.Api`):
                Required. API resource.
                This corresponds to the ``api`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the Api resource by the update. The
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

                The result type for the operation will be
                :class:`google.cloud.apigateway_v1.types.Api` An API
                that can be served by one or more Gateways.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([api, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = apigateway.UpdateApiRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if api is not None:
            request.api = api
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_api,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("api.name", request.api.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            apigateway.Api,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_api(
        self,
        request: apigateway.DeleteApiRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Api.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.DeleteApiRequest`):
                The request object. Request message for
                ApiGatewayService.DeleteApi
            name (:class:`str`):
                Required. Resource name of the form:
                ``projects/*/locations/global/apis/*``

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

        request = apigateway.DeleteApiRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_api,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_api_configs(
        self,
        request: apigateway.ListApiConfigsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApiConfigsAsyncPager:
        r"""Lists ApiConfigs in a given project and location.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.ListApiConfigsRequest`):
                The request object. Request message for
                ApiGatewayService.ListApiConfigs
            parent (:class:`str`):
                Required. Parent resource of the API Config, of the
                form: ``projects/*/locations/global/apis/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigateway_v1.services.api_gateway_service.pagers.ListApiConfigsAsyncPager:
                Response message for
                ApiGatewayService.ListApiConfigs
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

        request = apigateway.ListApiConfigsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_api_configs,
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
        response = pagers.ListApiConfigsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_api_config(
        self,
        request: apigateway.GetApiConfigRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> apigateway.ApiConfig:
        r"""Gets details of a single ApiConfig.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.GetApiConfigRequest`):
                The request object. Request message for
                ApiGatewayService.GetApiConfig
            name (:class:`str`):
                Required. Resource name of the form:
                ``projects/*/locations/global/apis/*/configs/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigateway_v1.types.ApiConfig:
                An API Configuration is a combination
                of settings for both the Managed Service
                and Gateways serving this API Config.

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

        request = apigateway.GetApiConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_api_config,
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

    async def create_api_config(
        self,
        request: apigateway.CreateApiConfigRequest = None,
        *,
        parent: str = None,
        api_config: apigateway.ApiConfig = None,
        api_config_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new ApiConfig in a given project and
        location.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.CreateApiConfigRequest`):
                The request object. Request message for
                ApiGatewayService.CreateApiConfig
            parent (:class:`str`):
                Required. Parent resource of the API Config, of the
                form: ``projects/*/locations/global/apis/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_config (:class:`google.cloud.apigateway_v1.types.ApiConfig`):
                Required. API resource.
                This corresponds to the ``api_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_config_id (:class:`str`):
                Required. Identifier to assign to the
                API Config. Must be unique within scope
                of the parent resource.

                This corresponds to the ``api_config_id`` field
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

                The result type for the operation will be :class:`google.cloud.apigateway_v1.types.ApiConfig` An API Configuration is a combination of settings for both the Managed
                   Service and Gateways serving this API Config.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, api_config, api_config_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = apigateway.CreateApiConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if api_config is not None:
            request.api_config = api_config
        if api_config_id is not None:
            request.api_config_id = api_config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_api_config,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            apigateway.ApiConfig,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_api_config(
        self,
        request: apigateway.UpdateApiConfigRequest = None,
        *,
        api_config: apigateway.ApiConfig = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single ApiConfig.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.UpdateApiConfigRequest`):
                The request object. Request message for
                ApiGatewayService.UpdateApiConfig
            api_config (:class:`google.cloud.apigateway_v1.types.ApiConfig`):
                Required. API Config resource.
                This corresponds to the ``api_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the ApiConfig resource by the update. The
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

                The result type for the operation will be :class:`google.cloud.apigateway_v1.types.ApiConfig` An API Configuration is a combination of settings for both the Managed
                   Service and Gateways serving this API Config.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([api_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = apigateway.UpdateApiConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if api_config is not None:
            request.api_config = api_config
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_api_config,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("api_config.name", request.api_config.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            apigateway.ApiConfig,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_api_config(
        self,
        request: apigateway.DeleteApiConfigRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single ApiConfig.

        Args:
            request (:class:`google.cloud.apigateway_v1.types.DeleteApiConfigRequest`):
                The request object. Request message for
                ApiGatewayService.DeleteApiConfig
            name (:class:`str`):
                Required. Resource name of the form:
                ``projects/*/locations/global/apis/*/configs/*``

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

        request = apigateway.DeleteApiConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_api_config,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable, core_exceptions.Unknown,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=apigateway.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-api-gateway",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ApiGatewayServiceAsyncClient",)
