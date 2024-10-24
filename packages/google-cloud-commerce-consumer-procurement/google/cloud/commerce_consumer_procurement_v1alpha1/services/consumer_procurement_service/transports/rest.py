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

import dataclasses
import json  # type: ignore
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.commerce_consumer_procurement_v1alpha1.types import (
    order,
    procurement_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseConsumerProcurementServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ConsumerProcurementServiceRestInterceptor:
    """Interceptor for ConsumerProcurementService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ConsumerProcurementServiceRestTransport.

    .. code-block:: python
        class MyCustomConsumerProcurementServiceInterceptor(ConsumerProcurementServiceRestInterceptor):
            def pre_get_order(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_order(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_orders(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_orders(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_place_order(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_place_order(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ConsumerProcurementServiceRestTransport(interceptor=MyCustomConsumerProcurementServiceInterceptor())
        client = ConsumerProcurementServiceClient(transport=transport)


    """

    def pre_get_order(
        self,
        request: procurement_service.GetOrderRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[procurement_service.GetOrderRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_order

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConsumerProcurementService server.
        """
        return request, metadata

    def post_get_order(self, response: order.Order) -> order.Order:
        """Post-rpc interceptor for get_order

        Override in a subclass to manipulate the response
        after it is returned by the ConsumerProcurementService server but before
        it is returned to user code.
        """
        return response

    def pre_list_orders(
        self,
        request: procurement_service.ListOrdersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[procurement_service.ListOrdersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_orders

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConsumerProcurementService server.
        """
        return request, metadata

    def post_list_orders(
        self, response: procurement_service.ListOrdersResponse
    ) -> procurement_service.ListOrdersResponse:
        """Post-rpc interceptor for list_orders

        Override in a subclass to manipulate the response
        after it is returned by the ConsumerProcurementService server but before
        it is returned to user code.
        """
        return response

    def pre_place_order(
        self,
        request: procurement_service.PlaceOrderRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[procurement_service.PlaceOrderRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for place_order

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConsumerProcurementService server.
        """
        return request, metadata

    def post_place_order(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for place_order

        Override in a subclass to manipulate the response
        after it is returned by the ConsumerProcurementService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConsumerProcurementService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ConsumerProcurementService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ConsumerProcurementServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ConsumerProcurementServiceRestInterceptor


class ConsumerProcurementServiceRestTransport(
    _BaseConsumerProcurementServiceRestTransport
):
    """REST backend synchronous transport for ConsumerProcurementService.

    ConsumerProcurementService allows customers to make purchases of
    products served by the Cloud Commerce platform.

    When purchases are made, the
    [ConsumerProcurementService][google.cloud.commerce.consumer.procurement.v1alpha1.ConsumerProcurementService]
    programs the appropriate backends, including both Google's own
    infrastructure, as well as third-party systems, and to enable
    billing setup for charging for the procured item.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudcommerceconsumerprocurement.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ConsumerProcurementServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudcommerceconsumerprocurement.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ConsumerProcurementServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1alpha1/{name=billingAccounts/*/orders/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha1/{name=billingAccounts/*/orders/*/orderAttributions/*/operations/*}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1alpha1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _GetOrder(
        _BaseConsumerProcurementServiceRestTransport._BaseGetOrder,
        ConsumerProcurementServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConsumerProcurementServiceRestTransport.GetOrder")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: procurement_service.GetOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> order.Order:
            r"""Call the get order method over HTTP.

            Args:
                request (~.procurement_service.GetOrderRequest):
                    The request object. Request message for
                [ConsumerProcurementService.GetOrder][google.cloud.commerce.consumer.procurement.v1alpha1.ConsumerProcurementService.GetOrder]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.order.Order:
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

            http_options = (
                _BaseConsumerProcurementServiceRestTransport._BaseGetOrder._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_order(request, metadata)
            transcoded_request = _BaseConsumerProcurementServiceRestTransport._BaseGetOrder._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConsumerProcurementServiceRestTransport._BaseGetOrder._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConsumerProcurementServiceRestTransport._GetOrder._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = order.Order()
            pb_resp = order.Order.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_order(resp)
            return resp

    class _ListOrders(
        _BaseConsumerProcurementServiceRestTransport._BaseListOrders,
        ConsumerProcurementServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConsumerProcurementServiceRestTransport.ListOrders")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: procurement_service.ListOrdersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> procurement_service.ListOrdersResponse:
            r"""Call the list orders method over HTTP.

            Args:
                request (~.procurement_service.ListOrdersRequest):
                    The request object. Request message for
                [ConsumerProcurementService.ListOrders][google.cloud.commerce.consumer.procurement.v1alpha1.ConsumerProcurementService.ListOrders].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.procurement_service.ListOrdersResponse:
                    Response message for
                [ConsumerProcurementService.ListOrders][google.cloud.commerce.consumer.procurement.v1alpha1.ConsumerProcurementService.ListOrders].

            """

            http_options = (
                _BaseConsumerProcurementServiceRestTransport._BaseListOrders._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_orders(request, metadata)
            transcoded_request = _BaseConsumerProcurementServiceRestTransport._BaseListOrders._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConsumerProcurementServiceRestTransport._BaseListOrders._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConsumerProcurementServiceRestTransport._ListOrders._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = procurement_service.ListOrdersResponse()
            pb_resp = procurement_service.ListOrdersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_orders(resp)
            return resp

    class _PlaceOrder(
        _BaseConsumerProcurementServiceRestTransport._BasePlaceOrder,
        ConsumerProcurementServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConsumerProcurementServiceRestTransport.PlaceOrder")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: procurement_service.PlaceOrderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the place order method over HTTP.

            Args:
                request (~.procurement_service.PlaceOrderRequest):
                    The request object. Request message for
                [ConsumerProcurementService.PlaceOrder][google.cloud.commerce.consumer.procurement.v1alpha1.ConsumerProcurementService.PlaceOrder].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseConsumerProcurementServiceRestTransport._BasePlaceOrder._get_http_options()
            )
            request, metadata = self._interceptor.pre_place_order(request, metadata)
            transcoded_request = _BaseConsumerProcurementServiceRestTransport._BasePlaceOrder._get_transcoded_request(
                http_options, request
            )

            body = _BaseConsumerProcurementServiceRestTransport._BasePlaceOrder._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseConsumerProcurementServiceRestTransport._BasePlaceOrder._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConsumerProcurementServiceRestTransport._PlaceOrder._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_place_order(resp)
            return resp

    @property
    def get_order(self) -> Callable[[procurement_service.GetOrderRequest], order.Order]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOrder(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_orders(
        self,
    ) -> Callable[
        [procurement_service.ListOrdersRequest], procurement_service.ListOrdersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOrders(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def place_order(
        self,
    ) -> Callable[[procurement_service.PlaceOrderRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PlaceOrder(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseConsumerProcurementServiceRestTransport._BaseGetOperation,
        ConsumerProcurementServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConsumerProcurementServiceRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseConsumerProcurementServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseConsumerProcurementServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConsumerProcurementServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConsumerProcurementServiceRestTransport._GetOperation._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ConsumerProcurementServiceRestTransport",)
