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

from google.cloud.apigateway_v1.types import apigateway

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseApiGatewayServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ApiGatewayServiceRestInterceptor:
    """Interceptor for ApiGatewayService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ApiGatewayServiceRestTransport.

    .. code-block:: python
        class MyCustomApiGatewayServiceInterceptor(ApiGatewayServiceRestInterceptor):
            def pre_create_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_api_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_api_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_api_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_api_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_api_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_api_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_api_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_apis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_apis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_gateways(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_gateways(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_api_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_api_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ApiGatewayServiceRestTransport(interceptor=MyCustomApiGatewayServiceInterceptor())
        client = ApiGatewayServiceClient(transport=transport)


    """

    def pre_create_api(
        self, request: apigateway.CreateApiRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apigateway.CreateApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_create_api(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_create_api_config(
        self,
        request: apigateway.CreateApiConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.CreateApiConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_api_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_create_api_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_api_config

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_create_gateway(
        self,
        request: apigateway.CreateGatewayRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.CreateGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_create_gateway(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_gateway

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_api(
        self, request: apigateway.DeleteApiRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apigateway.DeleteApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_delete_api(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_api_config(
        self,
        request: apigateway.DeleteApiConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.DeleteApiConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_api_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_delete_api_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_api_config

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_gateway(
        self,
        request: apigateway.DeleteGatewayRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.DeleteGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_delete_gateway(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_gateway

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_get_api(
        self, request: apigateway.GetApiRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apigateway.GetApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_get_api(self, response: apigateway.Api) -> apigateway.Api:
        """Post-rpc interceptor for get_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_get_api_config(
        self,
        request: apigateway.GetApiConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.GetApiConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_get_api_config(
        self, response: apigateway.ApiConfig
    ) -> apigateway.ApiConfig:
        """Post-rpc interceptor for get_api_config

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_get_gateway(
        self, request: apigateway.GetGatewayRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apigateway.GetGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_get_gateway(self, response: apigateway.Gateway) -> apigateway.Gateway:
        """Post-rpc interceptor for get_gateway

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_list_api_configs(
        self,
        request: apigateway.ListApiConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.ListApiConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_api_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_list_api_configs(
        self, response: apigateway.ListApiConfigsResponse
    ) -> apigateway.ListApiConfigsResponse:
        """Post-rpc interceptor for list_api_configs

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_list_apis(
        self, request: apigateway.ListApisRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apigateway.ListApisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_apis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_list_apis(
        self, response: apigateway.ListApisResponse
    ) -> apigateway.ListApisResponse:
        """Post-rpc interceptor for list_apis

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_list_gateways(
        self,
        request: apigateway.ListGatewaysRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.ListGatewaysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_gateways

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_list_gateways(
        self, response: apigateway.ListGatewaysResponse
    ) -> apigateway.ListGatewaysResponse:
        """Post-rpc interceptor for list_gateways

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_update_api(
        self, request: apigateway.UpdateApiRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[apigateway.UpdateApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_update_api(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_api

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_update_api_config(
        self,
        request: apigateway.UpdateApiConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.UpdateApiConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_api_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_update_api_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_api_config

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response

    def pre_update_gateway(
        self,
        request: apigateway.UpdateGatewayRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apigateway.UpdateGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ApiGatewayService server.
        """
        return request, metadata

    def post_update_gateway(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_gateway

        Override in a subclass to manipulate the response
        after it is returned by the ApiGatewayService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ApiGatewayServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ApiGatewayServiceRestInterceptor


class ApiGatewayServiceRestTransport(_BaseApiGatewayServiceRestTransport):
    """REST backend synchronous transport for ApiGatewayService.

    The API Gateway Service is the interface for managing API
    Gateways.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "apigateway.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ApiGatewayServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'apigateway.googleapis.com').
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
        self._interceptor = interceptor or ApiGatewayServiceRestInterceptor()
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
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateApi(
        _BaseApiGatewayServiceRestTransport._BaseCreateApi, ApiGatewayServiceRestStub
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.CreateApi")

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
            request: apigateway.CreateApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create api method over HTTP.

            Args:
                request (~.apigateway.CreateApiRequest):
                    The request object. Request message for
                ApiGatewayService.CreateApi
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
                _BaseApiGatewayServiceRestTransport._BaseCreateApi._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_api(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseCreateApi._get_transcoded_request(
                http_options, request
            )

            body = _BaseApiGatewayServiceRestTransport._BaseCreateApi._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseCreateApi._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._CreateApi._get_response(
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
            resp = self._interceptor.post_create_api(resp)
            return resp

    class _CreateApiConfig(
        _BaseApiGatewayServiceRestTransport._BaseCreateApiConfig,
        ApiGatewayServiceRestStub,
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.CreateApiConfig")

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
            request: apigateway.CreateApiConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create api config method over HTTP.

            Args:
                request (~.apigateway.CreateApiConfigRequest):
                    The request object. Request message for
                ApiGatewayService.CreateApiConfig
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
                _BaseApiGatewayServiceRestTransport._BaseCreateApiConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_api_config(
                request, metadata
            )
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseCreateApiConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseApiGatewayServiceRestTransport._BaseCreateApiConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseCreateApiConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._CreateApiConfig._get_response(
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
            resp = self._interceptor.post_create_api_config(resp)
            return resp

    class _CreateGateway(
        _BaseApiGatewayServiceRestTransport._BaseCreateGateway,
        ApiGatewayServiceRestStub,
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.CreateGateway")

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
            request: apigateway.CreateGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create gateway method over HTTP.

            Args:
                request (~.apigateway.CreateGatewayRequest):
                    The request object. Request message for
                ApiGatewayService.CreateGateway
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
                _BaseApiGatewayServiceRestTransport._BaseCreateGateway._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_gateway(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseCreateGateway._get_transcoded_request(
                http_options, request
            )

            body = _BaseApiGatewayServiceRestTransport._BaseCreateGateway._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseCreateGateway._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._CreateGateway._get_response(
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
            resp = self._interceptor.post_create_gateway(resp)
            return resp

    class _DeleteApi(
        _BaseApiGatewayServiceRestTransport._BaseDeleteApi, ApiGatewayServiceRestStub
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.DeleteApi")

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
            request: apigateway.DeleteApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete api method over HTTP.

            Args:
                request (~.apigateway.DeleteApiRequest):
                    The request object. Request message for
                ApiGatewayService.DeleteApi
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
                _BaseApiGatewayServiceRestTransport._BaseDeleteApi._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_api(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseDeleteApi._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseDeleteApi._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._DeleteApi._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_api(resp)
            return resp

    class _DeleteApiConfig(
        _BaseApiGatewayServiceRestTransport._BaseDeleteApiConfig,
        ApiGatewayServiceRestStub,
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.DeleteApiConfig")

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
            request: apigateway.DeleteApiConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete api config method over HTTP.

            Args:
                request (~.apigateway.DeleteApiConfigRequest):
                    The request object. Request message for
                ApiGatewayService.DeleteApiConfig
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
                _BaseApiGatewayServiceRestTransport._BaseDeleteApiConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_api_config(
                request, metadata
            )
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseDeleteApiConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseDeleteApiConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._DeleteApiConfig._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_api_config(resp)
            return resp

    class _DeleteGateway(
        _BaseApiGatewayServiceRestTransport._BaseDeleteGateway,
        ApiGatewayServiceRestStub,
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.DeleteGateway")

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
            request: apigateway.DeleteGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete gateway method over HTTP.

            Args:
                request (~.apigateway.DeleteGatewayRequest):
                    The request object. Request message for
                ApiGatewayService.DeleteGateway
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
                _BaseApiGatewayServiceRestTransport._BaseDeleteGateway._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_gateway(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseDeleteGateway._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseDeleteGateway._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._DeleteGateway._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_gateway(resp)
            return resp

    class _GetApi(
        _BaseApiGatewayServiceRestTransport._BaseGetApi, ApiGatewayServiceRestStub
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.GetApi")

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
            request: apigateway.GetApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apigateway.Api:
            r"""Call the get api method over HTTP.

            Args:
                request (~.apigateway.GetApiRequest):
                    The request object. Request message for
                ApiGatewayService.GetApi
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apigateway.Api:
                    An API that can be served by one or
                more Gateways.

            """

            http_options = (
                _BaseApiGatewayServiceRestTransport._BaseGetApi._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_api(request, metadata)
            transcoded_request = (
                _BaseApiGatewayServiceRestTransport._BaseGetApi._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseApiGatewayServiceRestTransport._BaseGetApi._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._GetApi._get_response(
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
            resp = apigateway.Api()
            pb_resp = apigateway.Api.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api(resp)
            return resp

    class _GetApiConfig(
        _BaseApiGatewayServiceRestTransport._BaseGetApiConfig, ApiGatewayServiceRestStub
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.GetApiConfig")

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
            request: apigateway.GetApiConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apigateway.ApiConfig:
            r"""Call the get api config method over HTTP.

            Args:
                request (~.apigateway.GetApiConfigRequest):
                    The request object. Request message for
                ApiGatewayService.GetApiConfig
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apigateway.ApiConfig:
                    An API Configuration is a combination
                of settings for both the Managed Service
                and Gateways serving this API Config.

            """

            http_options = (
                _BaseApiGatewayServiceRestTransport._BaseGetApiConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_api_config(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseGetApiConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseGetApiConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._GetApiConfig._get_response(
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
            resp = apigateway.ApiConfig()
            pb_resp = apigateway.ApiConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api_config(resp)
            return resp

    class _GetGateway(
        _BaseApiGatewayServiceRestTransport._BaseGetGateway, ApiGatewayServiceRestStub
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.GetGateway")

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
            request: apigateway.GetGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apigateway.Gateway:
            r"""Call the get gateway method over HTTP.

            Args:
                request (~.apigateway.GetGatewayRequest):
                    The request object. Request message for
                ApiGatewayService.GetGateway
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apigateway.Gateway:
                    A Gateway is an API-aware HTTP proxy.
                It performs API-Method and/or
                API-Consumer specific actions based on
                an API Config such as authentication,
                policy enforcement, and backend
                selection.

            """

            http_options = (
                _BaseApiGatewayServiceRestTransport._BaseGetGateway._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_gateway(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseGetGateway._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseGetGateway._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._GetGateway._get_response(
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
            resp = apigateway.Gateway()
            pb_resp = apigateway.Gateway.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_gateway(resp)
            return resp

    class _ListApiConfigs(
        _BaseApiGatewayServiceRestTransport._BaseListApiConfigs,
        ApiGatewayServiceRestStub,
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.ListApiConfigs")

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
            request: apigateway.ListApiConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apigateway.ListApiConfigsResponse:
            r"""Call the list api configs method over HTTP.

            Args:
                request (~.apigateway.ListApiConfigsRequest):
                    The request object. Request message for
                ApiGatewayService.ListApiConfigs
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apigateway.ListApiConfigsResponse:
                    Response message for
                ApiGatewayService.ListApiConfigs

            """

            http_options = (
                _BaseApiGatewayServiceRestTransport._BaseListApiConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_api_configs(
                request, metadata
            )
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseListApiConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseListApiConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._ListApiConfigs._get_response(
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
            resp = apigateway.ListApiConfigsResponse()
            pb_resp = apigateway.ListApiConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_api_configs(resp)
            return resp

    class _ListApis(
        _BaseApiGatewayServiceRestTransport._BaseListApis, ApiGatewayServiceRestStub
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.ListApis")

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
            request: apigateway.ListApisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apigateway.ListApisResponse:
            r"""Call the list apis method over HTTP.

            Args:
                request (~.apigateway.ListApisRequest):
                    The request object. Request message for
                ApiGatewayService.ListApis
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apigateway.ListApisResponse:
                    Response message for
                ApiGatewayService.ListApis

            """

            http_options = (
                _BaseApiGatewayServiceRestTransport._BaseListApis._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_apis(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseListApis._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseListApis._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._ListApis._get_response(
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
            resp = apigateway.ListApisResponse()
            pb_resp = apigateway.ListApisResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_apis(resp)
            return resp

    class _ListGateways(
        _BaseApiGatewayServiceRestTransport._BaseListGateways, ApiGatewayServiceRestStub
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.ListGateways")

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
            request: apigateway.ListGatewaysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> apigateway.ListGatewaysResponse:
            r"""Call the list gateways method over HTTP.

            Args:
                request (~.apigateway.ListGatewaysRequest):
                    The request object. Request message for
                ApiGatewayService.ListGateways
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.apigateway.ListGatewaysResponse:
                    Response message for
                ApiGatewayService.ListGateways

            """

            http_options = (
                _BaseApiGatewayServiceRestTransport._BaseListGateways._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_gateways(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseListGateways._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseListGateways._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._ListGateways._get_response(
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
            resp = apigateway.ListGatewaysResponse()
            pb_resp = apigateway.ListGatewaysResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_gateways(resp)
            return resp

    class _UpdateApi(
        _BaseApiGatewayServiceRestTransport._BaseUpdateApi, ApiGatewayServiceRestStub
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.UpdateApi")

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
            request: apigateway.UpdateApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update api method over HTTP.

            Args:
                request (~.apigateway.UpdateApiRequest):
                    The request object. Request message for
                ApiGatewayService.UpdateApi
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
                _BaseApiGatewayServiceRestTransport._BaseUpdateApi._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_api(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseUpdateApi._get_transcoded_request(
                http_options, request
            )

            body = _BaseApiGatewayServiceRestTransport._BaseUpdateApi._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseUpdateApi._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._UpdateApi._get_response(
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
            resp = self._interceptor.post_update_api(resp)
            return resp

    class _UpdateApiConfig(
        _BaseApiGatewayServiceRestTransport._BaseUpdateApiConfig,
        ApiGatewayServiceRestStub,
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.UpdateApiConfig")

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
            request: apigateway.UpdateApiConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update api config method over HTTP.

            Args:
                request (~.apigateway.UpdateApiConfigRequest):
                    The request object. Request message for
                ApiGatewayService.UpdateApiConfig
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
                _BaseApiGatewayServiceRestTransport._BaseUpdateApiConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_api_config(
                request, metadata
            )
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseUpdateApiConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseApiGatewayServiceRestTransport._BaseUpdateApiConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseUpdateApiConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._UpdateApiConfig._get_response(
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
            resp = self._interceptor.post_update_api_config(resp)
            return resp

    class _UpdateGateway(
        _BaseApiGatewayServiceRestTransport._BaseUpdateGateway,
        ApiGatewayServiceRestStub,
    ):
        def __hash__(self):
            return hash("ApiGatewayServiceRestTransport.UpdateGateway")

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
            request: apigateway.UpdateGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update gateway method over HTTP.

            Args:
                request (~.apigateway.UpdateGatewayRequest):
                    The request object. Request message for
                ApiGatewayService.UpdateGateway
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
                _BaseApiGatewayServiceRestTransport._BaseUpdateGateway._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_gateway(request, metadata)
            transcoded_request = _BaseApiGatewayServiceRestTransport._BaseUpdateGateway._get_transcoded_request(
                http_options, request
            )

            body = _BaseApiGatewayServiceRestTransport._BaseUpdateGateway._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseApiGatewayServiceRestTransport._BaseUpdateGateway._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ApiGatewayServiceRestTransport._UpdateGateway._get_response(
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
            resp = self._interceptor.post_update_gateway(resp)
            return resp

    @property
    def create_api(
        self,
    ) -> Callable[[apigateway.CreateApiRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_api_config(
        self,
    ) -> Callable[[apigateway.CreateApiConfigRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApiConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_gateway(
        self,
    ) -> Callable[[apigateway.CreateGatewayRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api(
        self,
    ) -> Callable[[apigateway.DeleteApiRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api_config(
        self,
    ) -> Callable[[apigateway.DeleteApiConfigRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApiConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_gateway(
        self,
    ) -> Callable[[apigateway.DeleteGatewayRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api(self) -> Callable[[apigateway.GetApiRequest], apigateway.Api]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api_config(
        self,
    ) -> Callable[[apigateway.GetApiConfigRequest], apigateway.ApiConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApiConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_gateway(
        self,
    ) -> Callable[[apigateway.GetGatewayRequest], apigateway.Gateway]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_api_configs(
        self,
    ) -> Callable[
        [apigateway.ListApiConfigsRequest], apigateway.ListApiConfigsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApiConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_apis(
        self,
    ) -> Callable[[apigateway.ListApisRequest], apigateway.ListApisResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_gateways(
        self,
    ) -> Callable[[apigateway.ListGatewaysRequest], apigateway.ListGatewaysResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGateways(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_api(
        self,
    ) -> Callable[[apigateway.UpdateApiRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_api_config(
        self,
    ) -> Callable[[apigateway.UpdateApiConfigRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApiConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_gateway(
        self,
    ) -> Callable[[apigateway.UpdateGatewayRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ApiGatewayServiceRestTransport",)
