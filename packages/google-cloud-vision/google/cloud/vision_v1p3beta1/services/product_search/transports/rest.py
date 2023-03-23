# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.api_core import operations_v1
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.vision_v1p3beta1.types import product_search_service
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from .base import (
    ProductSearchTransport,
    DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO,
)


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ProductSearchRestInterceptor:
    """Interceptor for ProductSearch.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ProductSearchRestTransport.

    .. code-block:: python
        class MyCustomProductSearchInterceptor(ProductSearchRestInterceptor):
            def pre_add_product_to_product_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_create_product(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_product(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_product_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_product_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_reference_image(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_reference_image(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_product(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_product_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_reference_image(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_product(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_product(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_product_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_product_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_reference_image(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_reference_image(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_product_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_product_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_products(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_products(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_product_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_product_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_products_in_product_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_products_in_product_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_reference_images(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_reference_images(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_product_from_product_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_update_product(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_product(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_product_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_product_set(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ProductSearchRestTransport(interceptor=MyCustomProductSearchInterceptor())
        client = ProductSearchClient(transport=transport)


    """

    def pre_add_product_to_product_set(
        self,
        request: product_search_service.AddProductToProductSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.AddProductToProductSetRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for add_product_to_product_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def pre_create_product(
        self,
        request: product_search_service.CreateProductRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_search_service.CreateProductRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_product

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_create_product(
        self, response: product_search_service.Product
    ) -> product_search_service.Product:
        """Post-rpc interceptor for create_product

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_create_product_set(
        self,
        request: product_search_service.CreateProductSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.CreateProductSetRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_product_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_create_product_set(
        self, response: product_search_service.ProductSet
    ) -> product_search_service.ProductSet:
        """Post-rpc interceptor for create_product_set

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_create_reference_image(
        self,
        request: product_search_service.CreateReferenceImageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.CreateReferenceImageRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_reference_image

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_create_reference_image(
        self, response: product_search_service.ReferenceImage
    ) -> product_search_service.ReferenceImage:
        """Post-rpc interceptor for create_reference_image

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_delete_product(
        self,
        request: product_search_service.DeleteProductRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_search_service.DeleteProductRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_product

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def pre_delete_product_set(
        self,
        request: product_search_service.DeleteProductSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.DeleteProductSetRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_product_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def pre_delete_reference_image(
        self,
        request: product_search_service.DeleteReferenceImageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.DeleteReferenceImageRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_reference_image

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def pre_get_product(
        self,
        request: product_search_service.GetProductRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_search_service.GetProductRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_product

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_get_product(
        self, response: product_search_service.Product
    ) -> product_search_service.Product:
        """Post-rpc interceptor for get_product

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_get_product_set(
        self,
        request: product_search_service.GetProductSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_search_service.GetProductSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_product_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_get_product_set(
        self, response: product_search_service.ProductSet
    ) -> product_search_service.ProductSet:
        """Post-rpc interceptor for get_product_set

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_get_reference_image(
        self,
        request: product_search_service.GetReferenceImageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.GetReferenceImageRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_reference_image

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_get_reference_image(
        self, response: product_search_service.ReferenceImage
    ) -> product_search_service.ReferenceImage:
        """Post-rpc interceptor for get_reference_image

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_import_product_sets(
        self,
        request: product_search_service.ImportProductSetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.ImportProductSetsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for import_product_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_import_product_sets(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_product_sets

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_list_products(
        self,
        request: product_search_service.ListProductsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_search_service.ListProductsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_products

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_list_products(
        self, response: product_search_service.ListProductsResponse
    ) -> product_search_service.ListProductsResponse:
        """Post-rpc interceptor for list_products

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_list_product_sets(
        self,
        request: product_search_service.ListProductSetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.ListProductSetsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_product_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_list_product_sets(
        self, response: product_search_service.ListProductSetsResponse
    ) -> product_search_service.ListProductSetsResponse:
        """Post-rpc interceptor for list_product_sets

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_list_products_in_product_set(
        self,
        request: product_search_service.ListProductsInProductSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.ListProductsInProductSetRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_products_in_product_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_list_products_in_product_set(
        self, response: product_search_service.ListProductsInProductSetResponse
    ) -> product_search_service.ListProductsInProductSetResponse:
        """Post-rpc interceptor for list_products_in_product_set

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_list_reference_images(
        self,
        request: product_search_service.ListReferenceImagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.ListReferenceImagesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_reference_images

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_list_reference_images(
        self, response: product_search_service.ListReferenceImagesResponse
    ) -> product_search_service.ListReferenceImagesResponse:
        """Post-rpc interceptor for list_reference_images

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_remove_product_from_product_set(
        self,
        request: product_search_service.RemoveProductFromProductSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.RemoveProductFromProductSetRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for remove_product_from_product_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def pre_update_product(
        self,
        request: product_search_service.UpdateProductRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[product_search_service.UpdateProductRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_product

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_update_product(
        self, response: product_search_service.Product
    ) -> product_search_service.Product:
        """Post-rpc interceptor for update_product

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response

    def pre_update_product_set(
        self,
        request: product_search_service.UpdateProductSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        product_search_service.UpdateProductSetRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_product_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductSearch server.
        """
        return request, metadata

    def post_update_product_set(
        self, response: product_search_service.ProductSet
    ) -> product_search_service.ProductSet:
        """Post-rpc interceptor for update_product_set

        Override in a subclass to manipulate the response
        after it is returned by the ProductSearch server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ProductSearchRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ProductSearchRestInterceptor


class ProductSearchRestTransport(ProductSearchTransport):
    """REST backend transport for ProductSearch.

    Manages Products and ProductSets of reference images for use in
    product search. It uses the following resource model:

    -  The API has a collection of
       [ProductSet][google.cloud.vision.v1p3beta1.ProductSet] resources,
       named ``projects/*/locations/*/productSets/*``, which acts as a
       way to put different products into groups to limit
       identification.

    In parallel,

    -  The API has a collection of
       [Product][google.cloud.vision.v1p3beta1.Product] resources, named
       ``projects/*/locations/*/products/*``

    -  Each [Product][google.cloud.vision.v1p3beta1.Product] has a
       collection of
       [ReferenceImage][google.cloud.vision.v1p3beta1.ReferenceImage]
       resources, named
       ``projects/*/locations/*/products/*/referenceImages/*``

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "vision.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ProductSearchRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ProductSearchRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {}

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1p3beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _AddProductToProductSet(ProductSearchRestStub):
        def __hash__(self):
            return hash("AddProductToProductSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.AddProductToProductSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the add product to product
            set method over HTTP.

                Args:
                    request (~.product_search_service.AddProductToProductSetRequest):
                        The request object. Request message for the ``AddProductToProductSet``
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/productSets/*}:addProduct",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_add_product_to_product_set(
                request, metadata
            )
            pb_request = product_search_service.AddProductToProductSetRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _CreateProduct(ProductSearchRestStub):
        def __hash__(self):
            return hash("CreateProduct")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.CreateProductRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.Product:
            r"""Call the create product method over HTTP.

            Args:
                request (~.product_search_service.CreateProductRequest):
                    The request object. Request message for the ``CreateProduct`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.Product:
                    A Product contains ReferenceImages.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1p3beta1/{parent=projects/*/locations/*}/products",
                    "body": "product",
                },
            ]
            request, metadata = self._interceptor.pre_create_product(request, metadata)
            pb_request = product_search_service.CreateProductRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.Product()
            pb_resp = product_search_service.Product.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_product(resp)
            return resp

    class _CreateProductSet(ProductSearchRestStub):
        def __hash__(self):
            return hash("CreateProductSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.CreateProductSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ProductSet:
            r"""Call the create product set method over HTTP.

            Args:
                request (~.product_search_service.CreateProductSetRequest):
                    The request object. Request message for the ``CreateProductSet`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.ProductSet:
                    A ProductSet contains Products. A
                ProductSet can contain a maximum of 1
                million reference images. If the limit
                is exceeded, periodic indexing will
                fail.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1p3beta1/{parent=projects/*/locations/*}/productSets",
                    "body": "product_set",
                },
            ]
            request, metadata = self._interceptor.pre_create_product_set(
                request, metadata
            )
            pb_request = product_search_service.CreateProductSetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ProductSet()
            pb_resp = product_search_service.ProductSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_product_set(resp)
            return resp

    class _CreateReferenceImage(ProductSearchRestStub):
        def __hash__(self):
            return hash("CreateReferenceImage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.CreateReferenceImageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ReferenceImage:
            r"""Call the create reference image method over HTTP.

            Args:
                request (~.product_search_service.CreateReferenceImageRequest):
                    The request object. Request message for the ``CreateReferenceImage`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.ReferenceImage:
                    A ``ReferenceImage`` represents a product image and its
                associated metadata, such as bounding boxes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1p3beta1/{parent=projects/*/locations/*/products/*}/referenceImages",
                    "body": "reference_image",
                },
            ]
            request, metadata = self._interceptor.pre_create_reference_image(
                request, metadata
            )
            pb_request = product_search_service.CreateReferenceImageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ReferenceImage()
            pb_resp = product_search_service.ReferenceImage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_reference_image(resp)
            return resp

    class _DeleteProduct(ProductSearchRestStub):
        def __hash__(self):
            return hash("DeleteProduct")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.DeleteProductRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete product method over HTTP.

            Args:
                request (~.product_search_service.DeleteProductRequest):
                    The request object. Request message for the ``DeleteProduct`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/products/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_product(request, metadata)
            pb_request = product_search_service.DeleteProductRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteProductSet(ProductSearchRestStub):
        def __hash__(self):
            return hash("DeleteProductSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.DeleteProductSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete product set method over HTTP.

            Args:
                request (~.product_search_service.DeleteProductSetRequest):
                    The request object. Request message for the ``DeleteProductSet`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/productSets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_product_set(
                request, metadata
            )
            pb_request = product_search_service.DeleteProductSetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteReferenceImage(ProductSearchRestStub):
        def __hash__(self):
            return hash("DeleteReferenceImage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.DeleteReferenceImageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete reference image method over HTTP.

            Args:
                request (~.product_search_service.DeleteReferenceImageRequest):
                    The request object. Request message for the ``DeleteReferenceImage`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/products/*/referenceImages/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_reference_image(
                request, metadata
            )
            pb_request = product_search_service.DeleteReferenceImageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetProduct(ProductSearchRestStub):
        def __hash__(self):
            return hash("GetProduct")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.GetProductRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.Product:
            r"""Call the get product method over HTTP.

            Args:
                request (~.product_search_service.GetProductRequest):
                    The request object. Request message for the ``GetProduct`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.Product:
                    A Product contains ReferenceImages.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/products/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_product(request, metadata)
            pb_request = product_search_service.GetProductRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.Product()
            pb_resp = product_search_service.Product.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_product(resp)
            return resp

    class _GetProductSet(ProductSearchRestStub):
        def __hash__(self):
            return hash("GetProductSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.GetProductSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ProductSet:
            r"""Call the get product set method over HTTP.

            Args:
                request (~.product_search_service.GetProductSetRequest):
                    The request object. Request message for the ``GetProductSet`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.ProductSet:
                    A ProductSet contains Products. A
                ProductSet can contain a maximum of 1
                million reference images. If the limit
                is exceeded, periodic indexing will
                fail.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/productSets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_product_set(request, metadata)
            pb_request = product_search_service.GetProductSetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ProductSet()
            pb_resp = product_search_service.ProductSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_product_set(resp)
            return resp

    class _GetReferenceImage(ProductSearchRestStub):
        def __hash__(self):
            return hash("GetReferenceImage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.GetReferenceImageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ReferenceImage:
            r"""Call the get reference image method over HTTP.

            Args:
                request (~.product_search_service.GetReferenceImageRequest):
                    The request object. Request message for the ``GetReferenceImage`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.ReferenceImage:
                    A ``ReferenceImage`` represents a product image and its
                associated metadata, such as bounding boxes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/products/*/referenceImages/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_reference_image(
                request, metadata
            )
            pb_request = product_search_service.GetReferenceImageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ReferenceImage()
            pb_resp = product_search_service.ReferenceImage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_reference_image(resp)
            return resp

    class _ImportProductSets(ProductSearchRestStub):
        def __hash__(self):
            return hash("ImportProductSets")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.ImportProductSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import product sets method over HTTP.

            Args:
                request (~.product_search_service.ImportProductSetsRequest):
                    The request object. Request message for the ``ImportProductSets`` method.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1p3beta1/{parent=projects/*/locations/*}/productSets:import",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_import_product_sets(
                request, metadata
            )
            pb_request = product_search_service.ImportProductSetsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_product_sets(resp)
            return resp

    class _ListProducts(ProductSearchRestStub):
        def __hash__(self):
            return hash("ListProducts")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.ListProductsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ListProductsResponse:
            r"""Call the list products method over HTTP.

            Args:
                request (~.product_search_service.ListProductsRequest):
                    The request object. Request message for the ``ListProducts`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.ListProductsResponse:
                    Response message for the ``ListProducts`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p3beta1/{parent=projects/*/locations/*}/products",
                },
            ]
            request, metadata = self._interceptor.pre_list_products(request, metadata)
            pb_request = product_search_service.ListProductsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ListProductsResponse()
            pb_resp = product_search_service.ListProductsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_products(resp)
            return resp

    class _ListProductSets(ProductSearchRestStub):
        def __hash__(self):
            return hash("ListProductSets")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.ListProductSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ListProductSetsResponse:
            r"""Call the list product sets method over HTTP.

            Args:
                request (~.product_search_service.ListProductSetsRequest):
                    The request object. Request message for the ``ListProductSets`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.ListProductSetsResponse:
                    Response message for the ``ListProductSets`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p3beta1/{parent=projects/*/locations/*}/productSets",
                },
            ]
            request, metadata = self._interceptor.pre_list_product_sets(
                request, metadata
            )
            pb_request = product_search_service.ListProductSetsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ListProductSetsResponse()
            pb_resp = product_search_service.ListProductSetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_product_sets(resp)
            return resp

    class _ListProductsInProductSet(ProductSearchRestStub):
        def __hash__(self):
            return hash("ListProductsInProductSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.ListProductsInProductSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ListProductsInProductSetResponse:
            r"""Call the list products in product
            set method over HTTP.

                Args:
                    request (~.product_search_service.ListProductsInProductSetRequest):
                        The request object. Request message for the ``ListProductsInProductSet``
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.product_search_service.ListProductsInProductSetResponse:
                        Response message for the ``ListProductsInProductSet``
                    method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/productSets/*}/products",
                },
            ]
            request, metadata = self._interceptor.pre_list_products_in_product_set(
                request, metadata
            )
            pb_request = product_search_service.ListProductsInProductSetRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ListProductsInProductSetResponse()
            pb_resp = product_search_service.ListProductsInProductSetResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_products_in_product_set(resp)
            return resp

    class _ListReferenceImages(ProductSearchRestStub):
        def __hash__(self):
            return hash("ListReferenceImages")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.ListReferenceImagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ListReferenceImagesResponse:
            r"""Call the list reference images method over HTTP.

            Args:
                request (~.product_search_service.ListReferenceImagesRequest):
                    The request object. Request message for the ``ListReferenceImages`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.ListReferenceImagesResponse:
                    Response message for the ``ListReferenceImages`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1p3beta1/{parent=projects/*/locations/*/products/*}/referenceImages",
                },
            ]
            request, metadata = self._interceptor.pre_list_reference_images(
                request, metadata
            )
            pb_request = product_search_service.ListReferenceImagesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ListReferenceImagesResponse()
            pb_resp = product_search_service.ListReferenceImagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_reference_images(resp)
            return resp

    class _RemoveProductFromProductSet(ProductSearchRestStub):
        def __hash__(self):
            return hash("RemoveProductFromProductSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.RemoveProductFromProductSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the remove product from
            product set method over HTTP.

                Args:
                    request (~.product_search_service.RemoveProductFromProductSetRequest):
                        The request object. Request message for the ``RemoveProductFromProductSet``
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1p3beta1/{name=projects/*/locations/*/productSets/*}:removeProduct",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_remove_product_from_product_set(
                request, metadata
            )
            pb_request = product_search_service.RemoveProductFromProductSetRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _UpdateProduct(ProductSearchRestStub):
        def __hash__(self):
            return hash("UpdateProduct")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.UpdateProductRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.Product:
            r"""Call the update product method over HTTP.

            Args:
                request (~.product_search_service.UpdateProductRequest):
                    The request object. Request message for the ``UpdateProduct`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.Product:
                    A Product contains ReferenceImages.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1p3beta1/{product.name=projects/*/locations/*/products/*}",
                    "body": "product",
                },
            ]
            request, metadata = self._interceptor.pre_update_product(request, metadata)
            pb_request = product_search_service.UpdateProductRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.Product()
            pb_resp = product_search_service.Product.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_product(resp)
            return resp

    class _UpdateProductSet(ProductSearchRestStub):
        def __hash__(self):
            return hash("UpdateProductSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: product_search_service.UpdateProductSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> product_search_service.ProductSet:
            r"""Call the update product set method over HTTP.

            Args:
                request (~.product_search_service.UpdateProductSetRequest):
                    The request object. Request message for the ``UpdateProductSet`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.product_search_service.ProductSet:
                    A ProductSet contains Products. A
                ProductSet can contain a maximum of 1
                million reference images. If the limit
                is exceeded, periodic indexing will
                fail.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1p3beta1/{product_set.name=projects/*/locations/*/productSets/*}",
                    "body": "product_set",
                },
            ]
            request, metadata = self._interceptor.pre_update_product_set(
                request, metadata
            )
            pb_request = product_search_service.UpdateProductSetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = product_search_service.ProductSet()
            pb_resp = product_search_service.ProductSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_product_set(resp)
            return resp

    @property
    def add_product_to_product_set(
        self,
    ) -> Callable[
        [product_search_service.AddProductToProductSetRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddProductToProductSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_product(
        self,
    ) -> Callable[
        [product_search_service.CreateProductRequest], product_search_service.Product
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProduct(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_product_set(
        self,
    ) -> Callable[
        [product_search_service.CreateProductSetRequest],
        product_search_service.ProductSet,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProductSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_reference_image(
        self,
    ) -> Callable[
        [product_search_service.CreateReferenceImageRequest],
        product_search_service.ReferenceImage,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReferenceImage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_product(
        self,
    ) -> Callable[[product_search_service.DeleteProductRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProduct(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_product_set(
        self,
    ) -> Callable[[product_search_service.DeleteProductSetRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProductSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_reference_image(
        self,
    ) -> Callable[
        [product_search_service.DeleteReferenceImageRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteReferenceImage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_product(
        self,
    ) -> Callable[
        [product_search_service.GetProductRequest], product_search_service.Product
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProduct(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_product_set(
        self,
    ) -> Callable[
        [product_search_service.GetProductSetRequest], product_search_service.ProductSet
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProductSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_reference_image(
        self,
    ) -> Callable[
        [product_search_service.GetReferenceImageRequest],
        product_search_service.ReferenceImage,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReferenceImage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_product_sets(
        self,
    ) -> Callable[
        [product_search_service.ImportProductSetsRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportProductSets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_products(
        self,
    ) -> Callable[
        [product_search_service.ListProductsRequest],
        product_search_service.ListProductsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProducts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_product_sets(
        self,
    ) -> Callable[
        [product_search_service.ListProductSetsRequest],
        product_search_service.ListProductSetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProductSets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_products_in_product_set(
        self,
    ) -> Callable[
        [product_search_service.ListProductsInProductSetRequest],
        product_search_service.ListProductsInProductSetResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProductsInProductSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_reference_images(
        self,
    ) -> Callable[
        [product_search_service.ListReferenceImagesRequest],
        product_search_service.ListReferenceImagesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReferenceImages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_product_from_product_set(
        self,
    ) -> Callable[
        [product_search_service.RemoveProductFromProductSetRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveProductFromProductSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_product(
        self,
    ) -> Callable[
        [product_search_service.UpdateProductRequest], product_search_service.Product
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProduct(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_product_set(
        self,
    ) -> Callable[
        [product_search_service.UpdateProductSetRequest],
        product_search_service.ProductSet,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProductSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ProductSearchRestTransport",)
