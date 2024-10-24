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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.shopping.merchant_products_v1beta.types import productinputs

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseProductInputsServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ProductInputsServiceRestInterceptor:
    """Interceptor for ProductInputsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ProductInputsServiceRestTransport.

    .. code-block:: python
        class MyCustomProductInputsServiceInterceptor(ProductInputsServiceRestInterceptor):
            def pre_delete_product_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_insert_product_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert_product_input(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ProductInputsServiceRestTransport(interceptor=MyCustomProductInputsServiceInterceptor())
        client = ProductInputsServiceClient(transport=transport)


    """

    def pre_delete_product_input(
        self,
        request: productinputs.DeleteProductInputRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[productinputs.DeleteProductInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_product_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductInputsService server.
        """
        return request, metadata

    def pre_insert_product_input(
        self,
        request: productinputs.InsertProductInputRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[productinputs.InsertProductInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert_product_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ProductInputsService server.
        """
        return request, metadata

    def post_insert_product_input(
        self, response: productinputs.ProductInput
    ) -> productinputs.ProductInput:
        """Post-rpc interceptor for insert_product_input

        Override in a subclass to manipulate the response
        after it is returned by the ProductInputsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ProductInputsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ProductInputsServiceRestInterceptor


class ProductInputsServiceRestTransport(_BaseProductInputsServiceRestTransport):
    """REST backend synchronous transport for ProductInputsService.

    Service to use ProductInput resource.
    This service works for products with online channel only.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "merchantapi.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ProductInputsServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'merchantapi.googleapis.com').
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ProductInputsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _DeleteProductInput(
        _BaseProductInputsServiceRestTransport._BaseDeleteProductInput,
        ProductInputsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ProductInputsServiceRestTransport.DeleteProductInput")

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
            request: productinputs.DeleteProductInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete product input method over HTTP.

            Args:
                request (~.productinputs.DeleteProductInputRequest):
                    The request object. Request message for the
                DeleteProductInput method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseProductInputsServiceRestTransport._BaseDeleteProductInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_product_input(
                request, metadata
            )
            transcoded_request = _BaseProductInputsServiceRestTransport._BaseDeleteProductInput._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseProductInputsServiceRestTransport._BaseDeleteProductInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ProductInputsServiceRestTransport._DeleteProductInput._get_response(
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

    class _InsertProductInput(
        _BaseProductInputsServiceRestTransport._BaseInsertProductInput,
        ProductInputsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ProductInputsServiceRestTransport.InsertProductInput")

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
            request: productinputs.InsertProductInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> productinputs.ProductInput:
            r"""Call the insert product input method over HTTP.

            Args:
                request (~.productinputs.InsertProductInputRequest):
                    The request object. Request message for the
                InsertProductInput method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.productinputs.ProductInput:
                    This resource represents input data you submit for a
                product, not the processed product that you see in
                Merchant Center, in Shopping ads, or across Google
                surfaces. Product inputs, rules and supplemental data
                source data are combined to create the processed
                [product][google.shopping.content.bundles.Products.Product].

                Required product input attributes to pass data
                validation checks are primarily defined in the `Products
                Data
                Specification <https://support.google.com/merchants/answer/188494>`__.

                The following attributes are required:
                [feedLabel][google.shopping.content.bundles.Products.feed_label],
                [contentLanguage][google.shopping.content.bundles.Products.content_language]
                and
                [offerId][google.shopping.content.bundles.Products.offer_id].

                After inserting, updating, or deleting a product input,
                it may take several minutes before the processed product
                can be retrieved.

                All fields in the product input and its sub-messages
                match the English name of their corresponding attribute
                in the vertical spec with `some
                exceptions <https://support.google.com/merchants/answer/7052112>`__.

            """

            http_options = (
                _BaseProductInputsServiceRestTransport._BaseInsertProductInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert_product_input(
                request, metadata
            )
            transcoded_request = _BaseProductInputsServiceRestTransport._BaseInsertProductInput._get_transcoded_request(
                http_options, request
            )

            body = _BaseProductInputsServiceRestTransport._BaseInsertProductInput._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseProductInputsServiceRestTransport._BaseInsertProductInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ProductInputsServiceRestTransport._InsertProductInput._get_response(
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
            resp = productinputs.ProductInput()
            pb_resp = productinputs.ProductInput.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_insert_product_input(resp)
            return resp

    @property
    def delete_product_input(
        self,
    ) -> Callable[[productinputs.DeleteProductInputRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProductInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert_product_input(
        self,
    ) -> Callable[
        [productinputs.InsertProductInputRequest], productinputs.ProductInput
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InsertProductInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ProductInputsServiceRestTransport",)
