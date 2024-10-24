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
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.retail_v2alpha.types import export_config, import_config
from google.cloud.retail_v2alpha.types import product
from google.cloud.retail_v2alpha.types import product as gcr_product
from google.cloud.retail_v2alpha.types import product_service, purge_config

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseProductServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ProductServiceRestInterceptor:
    """Interceptor for ProductService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ProductServiceRestTransport.

    .. code-block:: python
        class MyCustomProductServiceInterceptor(ProductServiceRestInterceptor):
            def pre_add_fulfillment_places(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_fulfillment_places(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_add_local_inventories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_local_inventories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_product(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_product(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_product(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_export_products(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_products(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_product(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_product(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_products(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_products(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_products(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_products(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_purge_products(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_purge_products(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_fulfillment_places(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_fulfillment_places(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_local_inventories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_local_inventories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_inventory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_inventory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_product(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_product(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ProductServiceRestTransport(interceptor=MyCustomProductServiceInterceptor())
        client = ProductServiceClient(transport=transport)


    """

    def pre_add_fulfillment_places(
        self,
        request: product_service.AddFulfillmentPlacesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_service.AddFulfillmentPlacesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_fulfillment_places

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_add_fulfillment_places(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for add_fulfillment_places

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_add_local_inventories(
        self,
        request: product_service.AddLocalInventoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_service.AddLocalInventoriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_local_inventories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_add_local_inventories(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for add_local_inventories

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_create_product(
        self,
        request: product_service.CreateProductRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_service.CreateProductRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_product

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_create_product(self, response: gcr_product.Product) -> gcr_product.Product:
        """Post-rpc interceptor for create_product

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_product(
        self,
        request: product_service.DeleteProductRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_service.DeleteProductRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_product

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def pre_export_products(
        self,
        request: export_config.ExportProductsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[export_config.ExportProductsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for export_products

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_export_products(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_products

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_get_product(
        self,
        request: product_service.GetProductRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_service.GetProductRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_product

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_get_product(self, response: product.Product) -> product.Product:
        """Post-rpc interceptor for get_product

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_import_products(
        self,
        request: import_config.ImportProductsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[import_config.ImportProductsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_products

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_import_products(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_products

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_list_products(
        self,
        request: product_service.ListProductsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_service.ListProductsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_products

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_list_products(
        self, response: product_service.ListProductsResponse
    ) -> product_service.ListProductsResponse:
        """Post-rpc interceptor for list_products

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_purge_products(
        self,
        request: purge_config.PurgeProductsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[purge_config.PurgeProductsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for purge_products

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_purge_products(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for purge_products

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_remove_fulfillment_places(
        self,
        request: product_service.RemoveFulfillmentPlacesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_service.RemoveFulfillmentPlacesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for remove_fulfillment_places

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_remove_fulfillment_places(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for remove_fulfillment_places

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_remove_local_inventories(
        self,
        request: product_service.RemoveLocalInventoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_service.RemoveLocalInventoriesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for remove_local_inventories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_remove_local_inventories(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for remove_local_inventories

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_set_inventory(
        self,
        request: product_service.SetInventoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_service.SetInventoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_inventory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_set_inventory(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for set_inventory

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_update_product(
        self,
        request: product_service.UpdateProductRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_service.UpdateProductRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_product

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_update_product(self, response: gcr_product.Product) -> gcr_product.Product:
        """Post-rpc interceptor for update_product

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
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
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ProductService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ProductServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ProductServiceRestInterceptor


class ProductServiceRestTransport(_BaseProductServiceRestTransport):
    """REST backend synchronous transport for ProductService.

    Service for ingesting [Product][google.cloud.retail.v2alpha.Product]
    information of the customer's website.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "retail.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ProductServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'retail.googleapis.com').
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
        self._interceptor = interceptor or ProductServiceRestInterceptor()
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
                        "uri": "/v2alpha/{name=projects/*/locations/*/catalogs/*/branches/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/catalogs/*/branches/*/places/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/catalogs/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*/catalogs/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*/locations/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v2alpha/{name=projects/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2alpha",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _AddFulfillmentPlaces(
        _BaseProductServiceRestTransport._BaseAddFulfillmentPlaces,
        ProductServiceRestStub,
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.AddFulfillmentPlaces")

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
            request: product_service.AddFulfillmentPlacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the add fulfillment places method over HTTP.

            Args:
                request (~.product_service.AddFulfillmentPlacesRequest):
                    The request object. Request message for
                [ProductService.AddFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.AddFulfillmentPlaces]
                method.
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
                _BaseProductServiceRestTransport._BaseAddFulfillmentPlaces._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_fulfillment_places(
                request, metadata
            )
            transcoded_request = _BaseProductServiceRestTransport._BaseAddFulfillmentPlaces._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseAddFulfillmentPlaces._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseAddFulfillmentPlaces._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._AddFulfillmentPlaces._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_add_fulfillment_places(resp)
            return resp

    class _AddLocalInventories(
        _BaseProductServiceRestTransport._BaseAddLocalInventories,
        ProductServiceRestStub,
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.AddLocalInventories")

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
            request: product_service.AddLocalInventoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the add local inventories method over HTTP.

            Args:
                request (~.product_service.AddLocalInventoriesRequest):
                    The request object. Request message for
                [ProductService.AddLocalInventories][google.cloud.retail.v2alpha.ProductService.AddLocalInventories]
                method.
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
                _BaseProductServiceRestTransport._BaseAddLocalInventories._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_local_inventories(
                request, metadata
            )
            transcoded_request = _BaseProductServiceRestTransport._BaseAddLocalInventories._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseAddLocalInventories._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseAddLocalInventories._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._AddLocalInventories._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_add_local_inventories(resp)
            return resp

    class _CreateProduct(
        _BaseProductServiceRestTransport._BaseCreateProduct, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.CreateProduct")

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
            request: product_service.CreateProductRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcr_product.Product:
            r"""Call the create product method over HTTP.

            Args:
                request (~.product_service.CreateProductRequest):
                    The request object. Request message for
                [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcr_product.Product:
                    Product captures all metadata
                information of items to be recommended
                or searched.

            """

            http_options = (
                _BaseProductServiceRestTransport._BaseCreateProduct._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_product(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseCreateProduct._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseCreateProduct._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseCreateProduct._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._CreateProduct._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcr_product.Product()
            pb_resp = gcr_product.Product.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_product(resp)
            return resp

    class _DeleteProduct(
        _BaseProductServiceRestTransport._BaseDeleteProduct, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.DeleteProduct")

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
            request: product_service.DeleteProductRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete product method over HTTP.

            Args:
                request (~.product_service.DeleteProductRequest):
                    The request object. Request message for
                [ProductService.DeleteProduct][google.cloud.retail.v2alpha.ProductService.DeleteProduct]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseProductServiceRestTransport._BaseDeleteProduct._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_product(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseDeleteProduct._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseDeleteProduct._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._DeleteProduct._get_response(
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

    class _ExportProducts(
        _BaseProductServiceRestTransport._BaseExportProducts, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.ExportProducts")

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
            request: export_config.ExportProductsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export products method over HTTP.

            Args:
                request (~.export_config.ExportProductsRequest):
                    The request object. Request message for ExportProducts
                method.
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
                _BaseProductServiceRestTransport._BaseExportProducts._get_http_options()
            )
            request, metadata = self._interceptor.pre_export_products(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseExportProducts._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseExportProducts._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseExportProducts._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._ExportProducts._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_export_products(resp)
            return resp

    class _GetProduct(
        _BaseProductServiceRestTransport._BaseGetProduct, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.GetProduct")

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
            request: product_service.GetProductRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product.Product:
            r"""Call the get product method over HTTP.

            Args:
                request (~.product_service.GetProductRequest):
                    The request object. Request message for
                [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product.Product:
                    Product captures all metadata
                information of items to be recommended
                or searched.

            """

            http_options = (
                _BaseProductServiceRestTransport._BaseGetProduct._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_product(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseGetProduct._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseProductServiceRestTransport._BaseGetProduct._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ProductServiceRestTransport._GetProduct._get_response(
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
            resp = product.Product()
            pb_resp = product.Product.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_product(resp)
            return resp

    class _ImportProducts(
        _BaseProductServiceRestTransport._BaseImportProducts, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.ImportProducts")

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
            request: import_config.ImportProductsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import products method over HTTP.

            Args:
                request (~.import_config.ImportProductsRequest):
                    The request object. Request message for Import methods.
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
                _BaseProductServiceRestTransport._BaseImportProducts._get_http_options()
            )
            request, metadata = self._interceptor.pre_import_products(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseImportProducts._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseImportProducts._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseImportProducts._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._ImportProducts._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_products(resp)
            return resp

    class _ListProducts(
        _BaseProductServiceRestTransport._BaseListProducts, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.ListProducts")

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
            request: product_service.ListProductsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_service.ListProductsResponse:
            r"""Call the list products method over HTTP.

            Args:
                request (~.product_service.ListProductsRequest):
                    The request object. Request message for
                [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_service.ListProductsResponse:
                    Response message for
                [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts]
                method.

            """

            http_options = (
                _BaseProductServiceRestTransport._BaseListProducts._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_products(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseListProducts._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseListProducts._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._ListProducts._get_response(
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
            resp = product_service.ListProductsResponse()
            pb_resp = product_service.ListProductsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_products(resp)
            return resp

    class _PurgeProducts(
        _BaseProductServiceRestTransport._BasePurgeProducts, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.PurgeProducts")

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
            request: purge_config.PurgeProductsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the purge products method over HTTP.

            Args:
                request (~.purge_config.PurgeProductsRequest):
                    The request object. Request message for PurgeProducts
                method.
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
                _BaseProductServiceRestTransport._BasePurgeProducts._get_http_options()
            )
            request, metadata = self._interceptor.pre_purge_products(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BasePurgeProducts._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BasePurgeProducts._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BasePurgeProducts._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._PurgeProducts._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_purge_products(resp)
            return resp

    class _RemoveFulfillmentPlaces(
        _BaseProductServiceRestTransport._BaseRemoveFulfillmentPlaces,
        ProductServiceRestStub,
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.RemoveFulfillmentPlaces")

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
            request: product_service.RemoveFulfillmentPlacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the remove fulfillment places method over HTTP.

            Args:
                request (~.product_service.RemoveFulfillmentPlacesRequest):
                    The request object. Request message for
                [ProductService.RemoveFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.RemoveFulfillmentPlaces]
                method.
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
                _BaseProductServiceRestTransport._BaseRemoveFulfillmentPlaces._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_fulfillment_places(
                request, metadata
            )
            transcoded_request = _BaseProductServiceRestTransport._BaseRemoveFulfillmentPlaces._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseRemoveFulfillmentPlaces._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseRemoveFulfillmentPlaces._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ProductServiceRestTransport._RemoveFulfillmentPlaces._get_response(
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
            resp = self._interceptor.post_remove_fulfillment_places(resp)
            return resp

    class _RemoveLocalInventories(
        _BaseProductServiceRestTransport._BaseRemoveLocalInventories,
        ProductServiceRestStub,
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.RemoveLocalInventories")

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
            request: product_service.RemoveLocalInventoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the remove local inventories method over HTTP.

            Args:
                request (~.product_service.RemoveLocalInventoriesRequest):
                    The request object. Request message for
                [ProductService.RemoveLocalInventories][google.cloud.retail.v2alpha.ProductService.RemoveLocalInventories]
                method.
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
                _BaseProductServiceRestTransport._BaseRemoveLocalInventories._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_local_inventories(
                request, metadata
            )
            transcoded_request = _BaseProductServiceRestTransport._BaseRemoveLocalInventories._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseRemoveLocalInventories._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseRemoveLocalInventories._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ProductServiceRestTransport._RemoveLocalInventories._get_response(
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
            resp = self._interceptor.post_remove_local_inventories(resp)
            return resp

    class _SetInventory(
        _BaseProductServiceRestTransport._BaseSetInventory, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.SetInventory")

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
            request: product_service.SetInventoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the set inventory method over HTTP.

            Args:
                request (~.product_service.SetInventoryRequest):
                    The request object. Request message for
                [ProductService.SetInventory][google.cloud.retail.v2alpha.ProductService.SetInventory]
                method.
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
                _BaseProductServiceRestTransport._BaseSetInventory._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_inventory(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseSetInventory._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseSetInventory._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseSetInventory._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._SetInventory._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_inventory(resp)
            return resp

    class _UpdateProduct(
        _BaseProductServiceRestTransport._BaseUpdateProduct, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.UpdateProduct")

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
            request: product_service.UpdateProductRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcr_product.Product:
            r"""Call the update product method over HTTP.

            Args:
                request (~.product_service.UpdateProductRequest):
                    The request object. Request message for
                [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcr_product.Product:
                    Product captures all metadata
                information of items to be recommended
                or searched.

            """

            http_options = (
                _BaseProductServiceRestTransport._BaseUpdateProduct._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_product(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseUpdateProduct._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductServiceRestTransport._BaseUpdateProduct._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseUpdateProduct._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._UpdateProduct._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcr_product.Product()
            pb_resp = gcr_product.Product.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_product(resp)
            return resp

    @property
    def add_fulfillment_places(
        self,
    ) -> Callable[
        [product_service.AddFulfillmentPlacesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddFulfillmentPlaces(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def add_local_inventories(
        self,
    ) -> Callable[
        [product_service.AddLocalInventoriesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddLocalInventories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_product(
        self,
    ) -> Callable[[product_service.CreateProductRequest], gcr_product.Product]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProduct(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_product(
        self,
    ) -> Callable[[product_service.DeleteProductRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProduct(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_products(
        self,
    ) -> Callable[[export_config.ExportProductsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportProducts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_product(
        self,
    ) -> Callable[[product_service.GetProductRequest], product.Product]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProduct(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_products(
        self,
    ) -> Callable[[import_config.ImportProductsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportProducts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_products(
        self,
    ) -> Callable[
        [product_service.ListProductsRequest], product_service.ListProductsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProducts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def purge_products(
        self,
    ) -> Callable[[purge_config.PurgeProductsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PurgeProducts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_fulfillment_places(
        self,
    ) -> Callable[
        [product_service.RemoveFulfillmentPlacesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveFulfillmentPlaces(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_local_inventories(
        self,
    ) -> Callable[
        [product_service.RemoveLocalInventoriesRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveLocalInventories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_inventory(
        self,
    ) -> Callable[[product_service.SetInventoryRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetInventory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_product(
        self,
    ) -> Callable[[product_service.UpdateProductRequest], gcr_product.Product]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProduct(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseProductServiceRestTransport._BaseGetOperation, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.GetOperation")

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
                _BaseProductServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._GetOperation._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseProductServiceRestTransport._BaseListOperations, ProductServiceRestStub
    ):
        def __hash__(self):
            return hash("ProductServiceRestTransport.ListOperations")

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
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseProductServiceRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseProductServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseProductServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ProductServiceRestTransport._ListOperations._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ProductServiceRestTransport",)
