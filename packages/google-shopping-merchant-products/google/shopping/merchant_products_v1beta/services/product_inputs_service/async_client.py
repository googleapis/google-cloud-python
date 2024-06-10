# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.shopping.merchant_products_v1beta import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.shopping.type.types import types

from google.shopping.merchant_products_v1beta.types import (
    productinputs,
    products_common,
)

from .client import ProductInputsServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, ProductInputsServiceTransport
from .transports.grpc_asyncio import ProductInputsServiceGrpcAsyncIOTransport


class ProductInputsServiceAsyncClient:
    """Service to use ProductInput resource.
    This service works for products with online channel only.
    """

    _client: ProductInputsServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = ProductInputsServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ProductInputsServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = ProductInputsServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = ProductInputsServiceClient._DEFAULT_UNIVERSE

    product_path = staticmethod(ProductInputsServiceClient.product_path)
    parse_product_path = staticmethod(ProductInputsServiceClient.parse_product_path)
    product_input_path = staticmethod(ProductInputsServiceClient.product_input_path)
    parse_product_input_path = staticmethod(
        ProductInputsServiceClient.parse_product_input_path
    )
    common_billing_account_path = staticmethod(
        ProductInputsServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ProductInputsServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ProductInputsServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ProductInputsServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ProductInputsServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ProductInputsServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ProductInputsServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ProductInputsServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ProductInputsServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ProductInputsServiceClient.parse_common_location_path
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
            ProductInputsServiceAsyncClient: The constructed client.
        """
        return ProductInputsServiceClient.from_service_account_info.__func__(ProductInputsServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ProductInputsServiceAsyncClient: The constructed client.
        """
        return ProductInputsServiceClient.from_service_account_file.__func__(ProductInputsServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        default mTLS endpoint; if the environment variable is "never", use the default API
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
        return ProductInputsServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ProductInputsServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ProductInputsServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = functools.partial(
        type(ProductInputsServiceClient).get_transport_class,
        type(ProductInputsServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                ProductInputsServiceTransport,
                Callable[..., ProductInputsServiceTransport],
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the product inputs service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ProductInputsServiceTransport,Callable[..., ProductInputsServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ProductInputsServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = ProductInputsServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def insert_product_input(
        self,
        request: Optional[Union[productinputs.InsertProductInputRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> productinputs.ProductInput:
        r"""Uploads a product input to your Merchant Center
        account. If an input with the same contentLanguage,
        offerId, and dataSource already exists, this method
        replaces that entry.

        After inserting, updating, or deleting a product input,
        it may take several minutes before the processed product
        can be retrieved.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_products_v1beta

            async def sample_insert_product_input():
                # Create a client
                client = merchant_products_v1beta.ProductInputsServiceAsyncClient()

                # Initialize request argument(s)
                product_input = merchant_products_v1beta.ProductInput()
                product_input.channel = "LOCAL"
                product_input.offer_id = "offer_id_value"
                product_input.content_language = "content_language_value"
                product_input.feed_label = "feed_label_value"

                request = merchant_products_v1beta.InsertProductInputRequest(
                    parent="parent_value",
                    product_input=product_input,
                    data_source="data_source_value",
                )

                # Make the request
                response = await client.insert_product_input(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_products_v1beta.types.InsertProductInputRequest, dict]]):
                The request object. Request message for the
                InsertProductInput method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_products_v1beta.types.ProductInput:
                This resource represents input data you submit for a product, not the
                   processed product that you see in Merchant Center, in
                   Shopping ads, or across Google surfaces. Product
                   inputs, rules and supplemental data source data are
                   combined to create the processed
                   [product][google.shopping.content.bundles.Products.Product].

                   Required product input attributes to pass data
                   validation checks are primarily defined in the
                   [Products Data
                   Specification](\ https://support.google.com/merchants/answer/188494).

                   The following attributes are required:
                   [feedLabel][google.shopping.content.bundles.Products.feed_label],
                   [contentLanguage][google.shopping.content.bundles.Products.content_language]
                   and
                   [offerId][google.shopping.content.bundles.Products.offer_id].

                   After inserting, updating, or deleting a product
                   input, it may take several minutes before the
                   processed product can be retrieved.

                   All fields in the product input and its sub-messages
                   match the English name of their corresponding
                   attribute in the vertical spec with [some
                   exceptions](\ https://support.google.com/merchants/answer/7052112).

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, productinputs.InsertProductInputRequest):
            request = productinputs.InsertProductInputRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.insert_product_input
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_product_input(
        self,
        request: Optional[Union[productinputs.DeleteProductInputRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a product input from your Merchant Center
        account.
        After inserting, updating, or deleting a product input,
        it may take several minutes before the processed product
        can be retrieved.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_products_v1beta

            async def sample_delete_product_input():
                # Create a client
                client = merchant_products_v1beta.ProductInputsServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_products_v1beta.DeleteProductInputRequest(
                    name="name_value",
                    data_source="data_source_value",
                )

                # Make the request
                await client.delete_product_input(request=request)

        Args:
            request (Optional[Union[google.shopping.merchant_products_v1beta.types.DeleteProductInputRequest, dict]]):
                The request object. Request message for the
                DeleteProductInput method.
            name (:class:`str`):
                Required. The name of the product
                input resource to delete. Format:
                accounts/{account}/productInputs/{product}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, productinputs.DeleteProductInputRequest):
            request = productinputs.DeleteProductInputRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.delete_product_input
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def __aenter__(self) -> "ProductInputsServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ProductInputsServiceAsyncClient",)
