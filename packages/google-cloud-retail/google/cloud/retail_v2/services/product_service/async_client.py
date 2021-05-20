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
from google.cloud.retail_v2.types import common
from google.cloud.retail_v2.types import import_config
from google.cloud.retail_v2.types import product
from google.cloud.retail_v2.types import product as gcr_product
from google.cloud.retail_v2.types import product_service
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from .transports.base import ProductServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ProductServiceGrpcAsyncIOTransport
from .client import ProductServiceClient


class ProductServiceAsyncClient:
    """Service for ingesting [Product][google.cloud.retail.v2.Product]
    information of the customer's website.
    """

    _client: ProductServiceClient

    DEFAULT_ENDPOINT = ProductServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ProductServiceClient.DEFAULT_MTLS_ENDPOINT

    branch_path = staticmethod(ProductServiceClient.branch_path)
    parse_branch_path = staticmethod(ProductServiceClient.parse_branch_path)
    product_path = staticmethod(ProductServiceClient.product_path)
    parse_product_path = staticmethod(ProductServiceClient.parse_product_path)
    common_billing_account_path = staticmethod(
        ProductServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ProductServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ProductServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ProductServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ProductServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ProductServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ProductServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ProductServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ProductServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ProductServiceClient.parse_common_location_path
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
            ProductServiceAsyncClient: The constructed client.
        """
        return ProductServiceClient.from_service_account_info.__func__(ProductServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ProductServiceAsyncClient: The constructed client.
        """
        return ProductServiceClient.from_service_account_file.__func__(ProductServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ProductServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ProductServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ProductServiceClient).get_transport_class, type(ProductServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ProductServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the product service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ProductServiceTransport]): The
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
        self._client = ProductServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_product(
        self,
        request: product_service.CreateProductRequest = None,
        *,
        parent: str = None,
        product: gcr_product.Product = None,
        product_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_product.Product:
        r"""Creates a [Product][google.cloud.retail.v2.Product].

        Args:
            request (:class:`google.cloud.retail_v2.types.CreateProductRequest`):
                The request object. Request message for
                [CreateProduct][] method.
            parent (:class:`str`):
                Required. The parent catalog resource name, such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            product (:class:`google.cloud.retail_v2.types.Product`):
                Required. The [Product][google.cloud.retail.v2.Product]
                to create.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            product_id (:class:`str`):
                Required. The ID to use for the
                [Product][google.cloud.retail.v2.Product], which will
                become the final component of the
                [Product.name][google.cloud.retail.v2.Product.name].

                If the caller does not have permission to create the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                This field must be unique among all
                [Product][google.cloud.retail.v2.Product]s with the same
                [parent][google.cloud.retail.v2.CreateProductRequest.parent].
                Otherwise, an ALREADY_EXISTS error is returned.

                This field must be a UTF-8 encoded string with a length
                limit of 128 characters. Otherwise, an INVALID_ARGUMENT
                error is returned.

                This corresponds to the ``product_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, product, product_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = product_service.CreateProductRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if product is not None:
            request.product = product
        if product_id is not None:
            request.product_id = product_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_product,
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

    async def get_product(
        self,
        request: product_service.GetProductRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product.Product:
        r"""Gets a [Product][google.cloud.retail.v2.Product].

        Args:
            request (:class:`google.cloud.retail_v2.types.GetProductRequest`):
                The request object. Request message for [GetProduct][]
                method.
            name (:class:`str`):
                Required. Full resource name of
                [Product][google.cloud.retail.v2.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to access the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                If the requested
                [Product][google.cloud.retail.v2.Product] does not
                exist, a NOT_FOUND error is returned.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

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

        request = product_service.GetProductRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_product,
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

    async def update_product(
        self,
        request: product_service.UpdateProductRequest = None,
        *,
        product: gcr_product.Product = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_product.Product:
        r"""Updates a [Product][google.cloud.retail.v2.Product].

        Args:
            request (:class:`google.cloud.retail_v2.types.UpdateProductRequest`):
                The request object. Request message for
                [UpdateProduct][] method.
            product (:class:`google.cloud.retail_v2.types.Product`):
                Required. The product to update/create.

                If the caller does not have permission to update the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                If the [Product][google.cloud.retail.v2.Product] to
                update does not exist, a NOT_FOUND error is returned.

                This corresponds to the ``product`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Indicates which fields in the provided
                [Product][google.cloud.retail.v2.Product] to update. The
                immutable and output only fields are NOT supported. If
                not set, all supported fields (the fields that are
                neither immutable nor output only) are updated.

                If an unsupported or unknown field is provided, an
                INVALID_ARGUMENT error is returned.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.Product:
                Product captures all metadata
                information of items to be recommended
                or searched.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([product, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = product_service.UpdateProductRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if product is not None:
            request.product = product
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_product,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("product.name", request.product.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_product(
        self,
        request: product_service.DeleteProductRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a [Product][google.cloud.retail.v2.Product].

        Args:
            request (:class:`google.cloud.retail_v2.types.DeleteProductRequest`):
                The request object. Request message for
                [DeleteProduct][] method.
            name (:class:`str`):
                Required. Full resource name of
                [Product][google.cloud.retail.v2.Product], such as
                ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

                If the caller does not have permission to delete the
                [Product][google.cloud.retail.v2.Product], regardless of
                whether or not it exists, a PERMISSION_DENIED error is
                returned.

                If the [Product][google.cloud.retail.v2.Product] to
                delete does not exist, a NOT_FOUND error is returned.

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

        request = product_service.DeleteProductRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_product,
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

    async def import_products(
        self,
        request: import_config.ImportProductsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Bulk import of multiple
        [Product][google.cloud.retail.v2.Product]s.

        Request processing may be synchronous. No partial updating is
        supported. Non-existing items are created.

        Note that it is possible for a subset of the
        [Product][google.cloud.retail.v2.Product]s to be successfully
        updated.

        Args:
            request (:class:`google.cloud.retail_v2.types.ImportProductsRequest`):
                The request object. Request message for Import methods.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2.types.ImportProductsResponse` Response of the
                   [ImportProductsRequest][google.cloud.retail.v2.ImportProductsRequest].
                   If the long running operation is done, then this
                   message is returned by the
                   google.longrunning.Operations.response field if the
                   operation was successful.

        """
        # Create or coerce a protobuf request object.
        request = import_config.ImportProductsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_products,
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
            import_config.ImportProductsResponse,
            metadata_type=import_config.ImportMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-retail",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ProductServiceAsyncClient",)
