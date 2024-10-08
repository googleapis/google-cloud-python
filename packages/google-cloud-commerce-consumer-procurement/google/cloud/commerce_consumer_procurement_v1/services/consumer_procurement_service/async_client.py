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

from google.cloud.commerce_consumer_procurement_v1 import (
    gapic_version as package_version,
)

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.commerce_consumer_procurement_v1.services.consumer_procurement_service import (
    pagers,
)
from google.cloud.commerce_consumer_procurement_v1.types import (
    order,
    procurement_service,
)

from .client import ConsumerProcurementServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, ConsumerProcurementServiceTransport
from .transports.grpc_asyncio import ConsumerProcurementServiceGrpcAsyncIOTransport


class ConsumerProcurementServiceAsyncClient:
    """ConsumerProcurementService allows customers to make purchases of
    products served by the Cloud Commerce platform.

    When purchases are made, the
    [ConsumerProcurementService][google.cloud.commerce.consumer.procurement.v1.ConsumerProcurementService]
    programs the appropriate backends, including both Google's own
    infrastructure, as well as third-party systems, and to enable
    billing setup for charging for the procured item.
    """

    _client: ConsumerProcurementServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = ConsumerProcurementServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ConsumerProcurementServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = (
        ConsumerProcurementServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    )
    _DEFAULT_UNIVERSE = ConsumerProcurementServiceClient._DEFAULT_UNIVERSE

    offer_path = staticmethod(ConsumerProcurementServiceClient.offer_path)
    parse_offer_path = staticmethod(ConsumerProcurementServiceClient.parse_offer_path)
    order_path = staticmethod(ConsumerProcurementServiceClient.order_path)
    parse_order_path = staticmethod(ConsumerProcurementServiceClient.parse_order_path)
    common_billing_account_path = staticmethod(
        ConsumerProcurementServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ConsumerProcurementServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(
        ConsumerProcurementServiceClient.common_folder_path
    )
    parse_common_folder_path = staticmethod(
        ConsumerProcurementServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ConsumerProcurementServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ConsumerProcurementServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        ConsumerProcurementServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        ConsumerProcurementServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        ConsumerProcurementServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        ConsumerProcurementServiceClient.parse_common_location_path
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
            ConsumerProcurementServiceAsyncClient: The constructed client.
        """
        return ConsumerProcurementServiceClient.from_service_account_info.__func__(ConsumerProcurementServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ConsumerProcurementServiceAsyncClient: The constructed client.
        """
        return ConsumerProcurementServiceClient.from_service_account_file.__func__(ConsumerProcurementServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return ConsumerProcurementServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ConsumerProcurementServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ConsumerProcurementServiceTransport: The transport used by the client instance.
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

    get_transport_class = ConsumerProcurementServiceClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                ConsumerProcurementServiceTransport,
                Callable[..., ConsumerProcurementServiceTransport],
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the consumer procurement service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ConsumerProcurementServiceTransport,Callable[..., ConsumerProcurementServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ConsumerProcurementServiceTransport constructor.
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
        self._client = ConsumerProcurementServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def place_order(
        self,
        request: Optional[Union[procurement_service.PlaceOrderRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new
        [Order][google.cloud.commerce.consumer.procurement.v1.Order].

        This API only supports GCP spend-based committed use discounts
        specified by GCP documentation.

        The returned long-running operation is in-progress until the
        backend completes the creation of the resource. Once completed,
        the order is in
        [OrderState.ORDER_STATE_ACTIVE][google.cloud.commerce.consumer.procurement.v1.OrderState.ORDER_STATE_ACTIVE].
        In case of failure, the order resource will be removed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import commerce_consumer_procurement_v1

            async def sample_place_order():
                # Create a client
                client = commerce_consumer_procurement_v1.ConsumerProcurementServiceAsyncClient()

                # Initialize request argument(s)
                request = commerce_consumer_procurement_v1.PlaceOrderRequest(
                    parent="parent_value",
                    display_name="display_name_value",
                )

                # Make the request
                operation = client.place_order(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.commerce_consumer_procurement_v1.types.PlaceOrderRequest, dict]]):
                The request object. Request message for
                [ConsumerProcurementService.PlaceOrder][google.cloud.commerce.consumer.procurement.v1.ConsumerProcurementService.PlaceOrder].
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.commerce_consumer_procurement_v1.types.Order` Represents a purchase made by a customer on Cloud Marketplace.
                   Creating an order makes sure that both the Google
                   backend systems as well as external service
                   provider's systems (if needed) allow use of purchased
                   products and ensures the appropriate billing events
                   occur.

                   An Order can be made against one Product with
                   multiple add-ons (optional) or one Quote which might
                   reference multiple products.

                   Customers typically choose a price plan for each
                   Product purchased when they create an order and can
                   change their plan later, if the product allows.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, procurement_service.PlaceOrderRequest):
            request = procurement_service.PlaceOrderRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.place_order
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            order.Order,
            metadata_type=procurement_service.PlaceOrderMetadata,
        )

        # Done; return the response.
        return response

    async def get_order(
        self,
        request: Optional[Union[procurement_service.GetOrderRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> order.Order:
        r"""Returns the requested
        [Order][google.cloud.commerce.consumer.procurement.v1.Order]
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import commerce_consumer_procurement_v1

            async def sample_get_order():
                # Create a client
                client = commerce_consumer_procurement_v1.ConsumerProcurementServiceAsyncClient()

                # Initialize request argument(s)
                request = commerce_consumer_procurement_v1.GetOrderRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_order(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.commerce_consumer_procurement_v1.types.GetOrderRequest, dict]]):
                The request object. Request message for
                [ConsumerProcurementService.GetOrder][google.cloud.commerce.consumer.procurement.v1.ConsumerProcurementService.GetOrder]
            name (:class:`str`):
                Required. The name of the order to
                retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.commerce_consumer_procurement_v1.types.Order:
                Represents a purchase made by a
                customer on Cloud Marketplace. Creating
                an order makes sure that both the Google
                backend systems as well as external
                service provider's systems (if needed)
                allow use of purchased products and
                ensures the appropriate billing events
                occur.

                An Order can be made against one Product
                with multiple add-ons (optional) or one
                Quote which might reference multiple
                products.

                Customers typically choose a price plan
                for each Product purchased when they
                create an order and can change their
                plan later, if the product allows.

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
        if not isinstance(request, procurement_service.GetOrderRequest):
            request = procurement_service.GetOrderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_order
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    async def list_orders(
        self,
        request: Optional[Union[procurement_service.ListOrdersRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListOrdersAsyncPager:
        r"""Lists
        [Order][google.cloud.commerce.consumer.procurement.v1.Order]
        resources that the user has access to, within the scope of the
        parent resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import commerce_consumer_procurement_v1

            async def sample_list_orders():
                # Create a client
                client = commerce_consumer_procurement_v1.ConsumerProcurementServiceAsyncClient()

                # Initialize request argument(s)
                request = commerce_consumer_procurement_v1.ListOrdersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_orders(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.commerce_consumer_procurement_v1.types.ListOrdersRequest, dict]]):
                The request object. Request message for
                [ConsumerProcurementService.ListOrders][google.cloud.commerce.consumer.procurement.v1.ConsumerProcurementService.ListOrders].
            parent (:class:`str`):
                Required. The parent resource to query for orders. This
                field has the form
                ``billingAccounts/{billing-account-id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.commerce_consumer_procurement_v1.services.consumer_procurement_service.pagers.ListOrdersAsyncPager:
                Response message for
                   [ConsumerProcurementService.ListOrders][google.cloud.commerce.consumer.procurement.v1.ConsumerProcurementService.ListOrders].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, procurement_service.ListOrdersRequest):
            request = procurement_service.ListOrdersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_orders
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListOrdersAsyncPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def modify_order(
        self,
        request: Optional[Union[procurement_service.ModifyOrderRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Modifies an existing
        [Order][google.cloud.commerce.consumer.procurement.v1.Order]
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import commerce_consumer_procurement_v1

            async def sample_modify_order():
                # Create a client
                client = commerce_consumer_procurement_v1.ConsumerProcurementServiceAsyncClient()

                # Initialize request argument(s)
                request = commerce_consumer_procurement_v1.ModifyOrderRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.modify_order(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.commerce_consumer_procurement_v1.types.ModifyOrderRequest, dict]]):
                The request object. Request message for
                [ConsumerProcurementService.ModifyOrder][google.cloud.commerce.consumer.procurement.v1.ConsumerProcurementService.ModifyOrder].
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.commerce_consumer_procurement_v1.types.Order` Represents a purchase made by a customer on Cloud Marketplace.
                   Creating an order makes sure that both the Google
                   backend systems as well as external service
                   provider's systems (if needed) allow use of purchased
                   products and ensures the appropriate billing events
                   occur.

                   An Order can be made against one Product with
                   multiple add-ons (optional) or one Quote which might
                   reference multiple products.

                   Customers typically choose a price plan for each
                   Product purchased when they create an order and can
                   change their plan later, if the product allows.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, procurement_service.ModifyOrderRequest):
            request = procurement_service.ModifyOrderRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.modify_order
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            order.Order,
            metadata_type=procurement_service.ModifyOrderMetadata,
        )

        # Done; return the response.
        return response

    async def cancel_order(
        self,
        request: Optional[Union[procurement_service.CancelOrderRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Cancels an existing
        [Order][google.cloud.commerce.consumer.procurement.v1.Order].
        Every product procured in the Order will be cancelled.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import commerce_consumer_procurement_v1

            async def sample_cancel_order():
                # Create a client
                client = commerce_consumer_procurement_v1.ConsumerProcurementServiceAsyncClient()

                # Initialize request argument(s)
                request = commerce_consumer_procurement_v1.CancelOrderRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.cancel_order(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.commerce_consumer_procurement_v1.types.CancelOrderRequest, dict]]):
                The request object. Request message for
                [ConsumerProcurementService.CancelOrder][google.cloud.commerce.consumer.procurement.v1.ConsumerProcurementService.CancelOrder].
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.commerce_consumer_procurement_v1.types.Order` Represents a purchase made by a customer on Cloud Marketplace.
                   Creating an order makes sure that both the Google
                   backend systems as well as external service
                   provider's systems (if needed) allow use of purchased
                   products and ensures the appropriate billing events
                   occur.

                   An Order can be made against one Product with
                   multiple add-ons (optional) or one Quote which might
                   reference multiple products.

                   Customers typically choose a price plan for each
                   Product purchased when they create an order and can
                   change their plan later, if the product allows.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, procurement_service.CancelOrderRequest):
            request = procurement_service.CancelOrderRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.cancel_order
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            order.Order,
            metadata_type=procurement_service.CancelOrderMetadata,
        )

        # Done; return the response.
        return response

    async def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    async def __aenter__(self) -> "ConsumerProcurementServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ConsumerProcurementServiceAsyncClient",)
