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
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.network_services_v1.types import (
    endpoint_policy as gcn_endpoint_policy,
)
from google.cloud.network_services_v1.types import (
    service_binding as gcn_service_binding,
)
from google.cloud.network_services_v1.types import endpoint_policy
from google.cloud.network_services_v1.types import gateway
from google.cloud.network_services_v1.types import gateway as gcn_gateway
from google.cloud.network_services_v1.types import grpc_route
from google.cloud.network_services_v1.types import grpc_route as gcn_grpc_route
from google.cloud.network_services_v1.types import http_route
from google.cloud.network_services_v1.types import http_route as gcn_http_route
from google.cloud.network_services_v1.types import mesh
from google.cloud.network_services_v1.types import mesh as gcn_mesh
from google.cloud.network_services_v1.types import service_binding
from google.cloud.network_services_v1.types import tcp_route
from google.cloud.network_services_v1.types import tcp_route as gcn_tcp_route
from google.cloud.network_services_v1.types import tls_route
from google.cloud.network_services_v1.types import tls_route as gcn_tls_route

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import NetworkServicesTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class NetworkServicesRestInterceptor:
    """Interceptor for NetworkServices.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the NetworkServicesRestTransport.

    .. code-block:: python
        class MyCustomNetworkServicesInterceptor(NetworkServicesRestInterceptor):
            def pre_create_endpoint_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_endpoint_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_grpc_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_grpc_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_http_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_http_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_mesh(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_mesh(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_service_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_tcp_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_tcp_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_tls_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_tls_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_endpoint_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_endpoint_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_grpc_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_grpc_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_http_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_http_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_mesh(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_mesh(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_service_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_service_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_tcp_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_tcp_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_tls_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_tls_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_endpoint_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_endpoint_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_grpc_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_grpc_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_http_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_http_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_mesh(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_mesh(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_tcp_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_tcp_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_tls_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_tls_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_endpoint_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_endpoint_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_gateways(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_gateways(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_grpc_routes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_grpc_routes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_http_routes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_http_routes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_meshes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_meshes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_service_bindings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_service_bindings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_tcp_routes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_tcp_routes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_tls_routes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_tls_routes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_endpoint_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_endpoint_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_grpc_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_grpc_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_http_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_http_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_mesh(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_mesh(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_tcp_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_tcp_route(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_tls_route(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_tls_route(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = NetworkServicesRestTransport(interceptor=MyCustomNetworkServicesInterceptor())
        client = NetworkServicesClient(transport=transport)


    """

    def pre_create_endpoint_policy(
        self,
        request: gcn_endpoint_policy.CreateEndpointPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_endpoint_policy.CreateEndpointPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_endpoint_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_create_endpoint_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_endpoint_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_create_gateway(
        self,
        request: gcn_gateway.CreateGatewayRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_gateway.CreateGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_create_gateway(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_gateway

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_create_grpc_route(
        self,
        request: gcn_grpc_route.CreateGrpcRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_grpc_route.CreateGrpcRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_grpc_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_create_grpc_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_grpc_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_create_http_route(
        self,
        request: gcn_http_route.CreateHttpRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_http_route.CreateHttpRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_http_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_create_http_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_http_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_create_mesh(
        self, request: gcn_mesh.CreateMeshRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gcn_mesh.CreateMeshRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_mesh

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_create_mesh(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_mesh

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_create_service_binding(
        self,
        request: gcn_service_binding.CreateServiceBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_service_binding.CreateServiceBindingRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_service_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_create_service_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_service_binding

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_create_tcp_route(
        self,
        request: gcn_tcp_route.CreateTcpRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_tcp_route.CreateTcpRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_tcp_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_create_tcp_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_tcp_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_create_tls_route(
        self,
        request: gcn_tls_route.CreateTlsRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_tls_route.CreateTlsRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_tls_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_create_tls_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_tls_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_endpoint_policy(
        self,
        request: endpoint_policy.DeleteEndpointPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[endpoint_policy.DeleteEndpointPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_endpoint_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_endpoint_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_endpoint_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_gateway(
        self, request: gateway.DeleteGatewayRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gateway.DeleteGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_gateway(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_gateway

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_grpc_route(
        self,
        request: grpc_route.DeleteGrpcRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grpc_route.DeleteGrpcRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_grpc_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_grpc_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_grpc_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_http_route(
        self,
        request: http_route.DeleteHttpRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[http_route.DeleteHttpRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_http_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_http_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_http_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_mesh(
        self, request: mesh.DeleteMeshRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[mesh.DeleteMeshRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_mesh

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_mesh(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_mesh

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_service_binding(
        self,
        request: service_binding.DeleteServiceBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service_binding.DeleteServiceBindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_service_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_service_binding(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_service_binding

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_tcp_route(
        self,
        request: tcp_route.DeleteTcpRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[tcp_route.DeleteTcpRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_tcp_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_tcp_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_tcp_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_tls_route(
        self,
        request: tls_route.DeleteTlsRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[tls_route.DeleteTlsRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_tls_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_tls_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_tls_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_endpoint_policy(
        self,
        request: endpoint_policy.GetEndpointPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[endpoint_policy.GetEndpointPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_endpoint_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_endpoint_policy(
        self, response: endpoint_policy.EndpointPolicy
    ) -> endpoint_policy.EndpointPolicy:
        """Post-rpc interceptor for get_endpoint_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_gateway(
        self, request: gateway.GetGatewayRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gateway.GetGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_gateway(self, response: gateway.Gateway) -> gateway.Gateway:
        """Post-rpc interceptor for get_gateway

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_grpc_route(
        self,
        request: grpc_route.GetGrpcRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grpc_route.GetGrpcRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_grpc_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_grpc_route(
        self, response: grpc_route.GrpcRoute
    ) -> grpc_route.GrpcRoute:
        """Post-rpc interceptor for get_grpc_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_http_route(
        self,
        request: http_route.GetHttpRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[http_route.GetHttpRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_http_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_http_route(
        self, response: http_route.HttpRoute
    ) -> http_route.HttpRoute:
        """Post-rpc interceptor for get_http_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_mesh(
        self, request: mesh.GetMeshRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[mesh.GetMeshRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_mesh

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_mesh(self, response: mesh.Mesh) -> mesh.Mesh:
        """Post-rpc interceptor for get_mesh

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_service_binding(
        self,
        request: service_binding.GetServiceBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service_binding.GetServiceBindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_service_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_service_binding(
        self, response: service_binding.ServiceBinding
    ) -> service_binding.ServiceBinding:
        """Post-rpc interceptor for get_service_binding

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_tcp_route(
        self, request: tcp_route.GetTcpRouteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tcp_route.GetTcpRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_tcp_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_tcp_route(self, response: tcp_route.TcpRoute) -> tcp_route.TcpRoute:
        """Post-rpc interceptor for get_tcp_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_tls_route(
        self, request: tls_route.GetTlsRouteRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tls_route.GetTlsRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_tls_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_tls_route(self, response: tls_route.TlsRoute) -> tls_route.TlsRoute:
        """Post-rpc interceptor for get_tls_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_endpoint_policies(
        self,
        request: endpoint_policy.ListEndpointPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[endpoint_policy.ListEndpointPoliciesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_endpoint_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_endpoint_policies(
        self, response: endpoint_policy.ListEndpointPoliciesResponse
    ) -> endpoint_policy.ListEndpointPoliciesResponse:
        """Post-rpc interceptor for list_endpoint_policies

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_gateways(
        self, request: gateway.ListGatewaysRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gateway.ListGatewaysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_gateways

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_gateways(
        self, response: gateway.ListGatewaysResponse
    ) -> gateway.ListGatewaysResponse:
        """Post-rpc interceptor for list_gateways

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_grpc_routes(
        self,
        request: grpc_route.ListGrpcRoutesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[grpc_route.ListGrpcRoutesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_grpc_routes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_grpc_routes(
        self, response: grpc_route.ListGrpcRoutesResponse
    ) -> grpc_route.ListGrpcRoutesResponse:
        """Post-rpc interceptor for list_grpc_routes

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_http_routes(
        self,
        request: http_route.ListHttpRoutesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[http_route.ListHttpRoutesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_http_routes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_http_routes(
        self, response: http_route.ListHttpRoutesResponse
    ) -> http_route.ListHttpRoutesResponse:
        """Post-rpc interceptor for list_http_routes

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_meshes(
        self, request: mesh.ListMeshesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[mesh.ListMeshesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_meshes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_meshes(
        self, response: mesh.ListMeshesResponse
    ) -> mesh.ListMeshesResponse:
        """Post-rpc interceptor for list_meshes

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_service_bindings(
        self,
        request: service_binding.ListServiceBindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service_binding.ListServiceBindingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_service_bindings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_service_bindings(
        self, response: service_binding.ListServiceBindingsResponse
    ) -> service_binding.ListServiceBindingsResponse:
        """Post-rpc interceptor for list_service_bindings

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_tcp_routes(
        self,
        request: tcp_route.ListTcpRoutesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[tcp_route.ListTcpRoutesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_tcp_routes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_tcp_routes(
        self, response: tcp_route.ListTcpRoutesResponse
    ) -> tcp_route.ListTcpRoutesResponse:
        """Post-rpc interceptor for list_tcp_routes

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_tls_routes(
        self,
        request: tls_route.ListTlsRoutesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[tls_route.ListTlsRoutesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_tls_routes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_tls_routes(
        self, response: tls_route.ListTlsRoutesResponse
    ) -> tls_route.ListTlsRoutesResponse:
        """Post-rpc interceptor for list_tls_routes

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_update_endpoint_policy(
        self,
        request: gcn_endpoint_policy.UpdateEndpointPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcn_endpoint_policy.UpdateEndpointPolicyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_endpoint_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_update_endpoint_policy(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_endpoint_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_update_gateway(
        self,
        request: gcn_gateway.UpdateGatewayRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_gateway.UpdateGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_update_gateway(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_gateway

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_update_grpc_route(
        self,
        request: gcn_grpc_route.UpdateGrpcRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_grpc_route.UpdateGrpcRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_grpc_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_update_grpc_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_grpc_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_update_http_route(
        self,
        request: gcn_http_route.UpdateHttpRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_http_route.UpdateHttpRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_http_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_update_http_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_http_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_update_mesh(
        self, request: gcn_mesh.UpdateMeshRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gcn_mesh.UpdateMeshRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_mesh

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_update_mesh(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_mesh

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_update_tcp_route(
        self,
        request: gcn_tcp_route.UpdateTcpRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_tcp_route.UpdateTcpRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_tcp_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_update_tcp_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_tcp_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_update_tls_route(
        self,
        request: gcn_tls_route.UpdateTlsRouteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcn_tls_route.UpdateTlsRouteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_tls_route

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_update_tls_route(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_tls_route

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
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
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
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
        before they are sent to the NetworkServices server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the NetworkServices server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class NetworkServicesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: NetworkServicesRestInterceptor


class NetworkServicesRestTransport(NetworkServicesTransport):
    """REST backend transport for NetworkServices.

    Service describing handlers for resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "networkservices.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[NetworkServicesRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'networkservices.googleapis.com').
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
        self._interceptor = interceptor or NetworkServicesRestInterceptor()
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

    class _CreateEndpointPolicy(NetworkServicesRestStub):
        def __hash__(self):
            return hash("CreateEndpointPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "endpointPolicyId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_endpoint_policy.CreateEndpointPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create endpoint policy method over HTTP.

            Args:
                request (~.gcn_endpoint_policy.CreateEndpointPolicyRequest):
                    The request object. Request used with the
                CreateEndpointPolicy method.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/endpointPolicies",
                    "body": "endpoint_policy",
                },
            ]
            request, metadata = self._interceptor.pre_create_endpoint_policy(
                request, metadata
            )
            pb_request = gcn_endpoint_policy.CreateEndpointPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_create_endpoint_policy(resp)
            return resp

    class _CreateGateway(NetworkServicesRestStub):
        def __hash__(self):
            return hash("CreateGateway")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "gatewayId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_gateway.CreateGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create gateway method over HTTP.

            Args:
                request (~.gcn_gateway.CreateGatewayRequest):
                    The request object. Request used by the CreateGateway
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/gateways",
                    "body": "gateway",
                },
            ]
            request, metadata = self._interceptor.pre_create_gateway(request, metadata)
            pb_request = gcn_gateway.CreateGatewayRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_create_gateway(resp)
            return resp

    class _CreateGrpcRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("CreateGrpcRoute")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "grpcRouteId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_grpc_route.CreateGrpcRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create grpc route method over HTTP.

            Args:
                request (~.gcn_grpc_route.CreateGrpcRouteRequest):
                    The request object. Request used by the CreateGrpcRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/grpcRoutes",
                    "body": "grpc_route",
                },
            ]
            request, metadata = self._interceptor.pre_create_grpc_route(
                request, metadata
            )
            pb_request = gcn_grpc_route.CreateGrpcRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_create_grpc_route(resp)
            return resp

    class _CreateHttpRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("CreateHttpRoute")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "httpRouteId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_http_route.CreateHttpRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create http route method over HTTP.

            Args:
                request (~.gcn_http_route.CreateHttpRouteRequest):
                    The request object. Request used by the HttpRoute method.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/httpRoutes",
                    "body": "http_route",
                },
            ]
            request, metadata = self._interceptor.pre_create_http_route(
                request, metadata
            )
            pb_request = gcn_http_route.CreateHttpRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_create_http_route(resp)
            return resp

    class _CreateMesh(NetworkServicesRestStub):
        def __hash__(self):
            return hash("CreateMesh")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "meshId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_mesh.CreateMeshRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create mesh method over HTTP.

            Args:
                request (~.gcn_mesh.CreateMeshRequest):
                    The request object. Request used by the CreateMesh
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/meshes",
                    "body": "mesh",
                },
            ]
            request, metadata = self._interceptor.pre_create_mesh(request, metadata)
            pb_request = gcn_mesh.CreateMeshRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_create_mesh(resp)
            return resp

    class _CreateServiceBinding(NetworkServicesRestStub):
        def __hash__(self):
            return hash("CreateServiceBinding")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "serviceBindingId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_service_binding.CreateServiceBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create service binding method over HTTP.

            Args:
                request (~.gcn_service_binding.CreateServiceBindingRequest):
                    The request object. Request used by the ServiceBinding
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/serviceBindings",
                    "body": "service_binding",
                },
            ]
            request, metadata = self._interceptor.pre_create_service_binding(
                request, metadata
            )
            pb_request = gcn_service_binding.CreateServiceBindingRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_create_service_binding(resp)
            return resp

    class _CreateTcpRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("CreateTcpRoute")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "tcpRouteId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_tcp_route.CreateTcpRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create tcp route method over HTTP.

            Args:
                request (~.gcn_tcp_route.CreateTcpRouteRequest):
                    The request object. Request used by the TcpRoute method.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/tcpRoutes",
                    "body": "tcp_route",
                },
            ]
            request, metadata = self._interceptor.pre_create_tcp_route(
                request, metadata
            )
            pb_request = gcn_tcp_route.CreateTcpRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_create_tcp_route(resp)
            return resp

    class _CreateTlsRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("CreateTlsRoute")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "tlsRouteId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcn_tls_route.CreateTlsRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create tls route method over HTTP.

            Args:
                request (~.gcn_tls_route.CreateTlsRouteRequest):
                    The request object. Request used by the TlsRoute method.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/tlsRoutes",
                    "body": "tls_route",
                },
            ]
            request, metadata = self._interceptor.pre_create_tls_route(
                request, metadata
            )
            pb_request = gcn_tls_route.CreateTlsRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_create_tls_route(resp)
            return resp

    class _DeleteEndpointPolicy(NetworkServicesRestStub):
        def __hash__(self):
            return hash("DeleteEndpointPolicy")

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
            request: endpoint_policy.DeleteEndpointPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete endpoint policy method over HTTP.

            Args:
                request (~.endpoint_policy.DeleteEndpointPolicyRequest):
                    The request object. Request used with the
                DeleteEndpointPolicy method.
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
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/endpointPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_endpoint_policy(
                request, metadata
            )
            pb_request = endpoint_policy.DeleteEndpointPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_endpoint_policy(resp)
            return resp

    class _DeleteGateway(NetworkServicesRestStub):
        def __hash__(self):
            return hash("DeleteGateway")

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
            request: gateway.DeleteGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete gateway method over HTTP.

            Args:
                request (~.gateway.DeleteGatewayRequest):
                    The request object. Request used by the DeleteGateway
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/gateways/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_gateway(request, metadata)
            pb_request = gateway.DeleteGatewayRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_gateway(resp)
            return resp

    class _DeleteGrpcRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("DeleteGrpcRoute")

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
            request: grpc_route.DeleteGrpcRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete grpc route method over HTTP.

            Args:
                request (~.grpc_route.DeleteGrpcRouteRequest):
                    The request object. Request used by the DeleteGrpcRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/grpcRoutes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_grpc_route(
                request, metadata
            )
            pb_request = grpc_route.DeleteGrpcRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_grpc_route(resp)
            return resp

    class _DeleteHttpRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("DeleteHttpRoute")

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
            request: http_route.DeleteHttpRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete http route method over HTTP.

            Args:
                request (~.http_route.DeleteHttpRouteRequest):
                    The request object. Request used by the DeleteHttpRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/httpRoutes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_http_route(
                request, metadata
            )
            pb_request = http_route.DeleteHttpRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_http_route(resp)
            return resp

    class _DeleteMesh(NetworkServicesRestStub):
        def __hash__(self):
            return hash("DeleteMesh")

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
            request: mesh.DeleteMeshRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete mesh method over HTTP.

            Args:
                request (~.mesh.DeleteMeshRequest):
                    The request object. Request used by the DeleteMesh
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/meshes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_mesh(request, metadata)
            pb_request = mesh.DeleteMeshRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_mesh(resp)
            return resp

    class _DeleteServiceBinding(NetworkServicesRestStub):
        def __hash__(self):
            return hash("DeleteServiceBinding")

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
            request: service_binding.DeleteServiceBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete service binding method over HTTP.

            Args:
                request (~.service_binding.DeleteServiceBindingRequest):
                    The request object. Request used by the
                DeleteServiceBinding method.
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
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/serviceBindings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_service_binding(
                request, metadata
            )
            pb_request = service_binding.DeleteServiceBindingRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_service_binding(resp)
            return resp

    class _DeleteTcpRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("DeleteTcpRoute")

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
            request: tcp_route.DeleteTcpRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete tcp route method over HTTP.

            Args:
                request (~.tcp_route.DeleteTcpRouteRequest):
                    The request object. Request used by the DeleteTcpRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/tcpRoutes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_tcp_route(
                request, metadata
            )
            pb_request = tcp_route.DeleteTcpRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_tcp_route(resp)
            return resp

    class _DeleteTlsRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("DeleteTlsRoute")

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
            request: tls_route.DeleteTlsRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete tls route method over HTTP.

            Args:
                request (~.tls_route.DeleteTlsRouteRequest):
                    The request object. Request used by the DeleteTlsRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/tlsRoutes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_tls_route(
                request, metadata
            )
            pb_request = tls_route.DeleteTlsRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_tls_route(resp)
            return resp

    class _GetEndpointPolicy(NetworkServicesRestStub):
        def __hash__(self):
            return hash("GetEndpointPolicy")

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
            request: endpoint_policy.GetEndpointPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> endpoint_policy.EndpointPolicy:
            r"""Call the get endpoint policy method over HTTP.

            Args:
                request (~.endpoint_policy.GetEndpointPolicyRequest):
                    The request object. Request used with the
                GetEndpointPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.endpoint_policy.EndpointPolicy:
                    EndpointPolicy is a resource that
                helps apply desired configuration on the
                endpoints that match specific criteria.
                For example, this resource can be used
                to apply "authentication config" an all
                endpoints that serve on port 8080.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/endpointPolicies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_endpoint_policy(
                request, metadata
            )
            pb_request = endpoint_policy.GetEndpointPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = endpoint_policy.EndpointPolicy()
            pb_resp = endpoint_policy.EndpointPolicy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_endpoint_policy(resp)
            return resp

    class _GetGateway(NetworkServicesRestStub):
        def __hash__(self):
            return hash("GetGateway")

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
            request: gateway.GetGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gateway.Gateway:
            r"""Call the get gateway method over HTTP.

            Args:
                request (~.gateway.GetGatewayRequest):
                    The request object. Request used by the GetGateway
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gateway.Gateway:
                    Gateway represents the configuration
                for a proxy, typically a load balancer.
                It captures the ip:port over which the
                services are exposed by the proxy, along
                with any policy configurations. Routes
                have reference to to Gateways to dictate
                how requests should be routed by this
                Gateway.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/gateways/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_gateway(request, metadata)
            pb_request = gateway.GetGatewayRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = gateway.Gateway()
            pb_resp = gateway.Gateway.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_gateway(resp)
            return resp

    class _GetGrpcRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("GetGrpcRoute")

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
            request: grpc_route.GetGrpcRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grpc_route.GrpcRoute:
            r"""Call the get grpc route method over HTTP.

            Args:
                request (~.grpc_route.GetGrpcRouteRequest):
                    The request object. Request used by the GetGrpcRoute
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grpc_route.GrpcRoute:
                    GrpcRoute is the resource defining
                how gRPC traffic routed by a Mesh or
                Gateway resource is routed.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/grpcRoutes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_grpc_route(request, metadata)
            pb_request = grpc_route.GetGrpcRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = grpc_route.GrpcRoute()
            pb_resp = grpc_route.GrpcRoute.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_grpc_route(resp)
            return resp

    class _GetHttpRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("GetHttpRoute")

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
            request: http_route.GetHttpRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> http_route.HttpRoute:
            r"""Call the get http route method over HTTP.

            Args:
                request (~.http_route.GetHttpRouteRequest):
                    The request object. Request used by the GetHttpRoute
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.http_route.HttpRoute:
                    HttpRoute is the resource defining
                how HTTP traffic should be routed by a
                Mesh or Gateway resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/httpRoutes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_http_route(request, metadata)
            pb_request = http_route.GetHttpRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = http_route.HttpRoute()
            pb_resp = http_route.HttpRoute.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_http_route(resp)
            return resp

    class _GetMesh(NetworkServicesRestStub):
        def __hash__(self):
            return hash("GetMesh")

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
            request: mesh.GetMeshRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> mesh.Mesh:
            r"""Call the get mesh method over HTTP.

            Args:
                request (~.mesh.GetMeshRequest):
                    The request object. Request used by the GetMesh method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.mesh.Mesh:
                    Mesh represents a logical
                configuration grouping for workload to
                workload communication within a service
                mesh. Routes that point to mesh dictate
                how requests are routed within this
                logical mesh boundary.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/meshes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_mesh(request, metadata)
            pb_request = mesh.GetMeshRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = mesh.Mesh()
            pb_resp = mesh.Mesh.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_mesh(resp)
            return resp

    class _GetServiceBinding(NetworkServicesRestStub):
        def __hash__(self):
            return hash("GetServiceBinding")

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
            request: service_binding.GetServiceBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service_binding.ServiceBinding:
            r"""Call the get service binding method over HTTP.

            Args:
                request (~.service_binding.GetServiceBindingRequest):
                    The request object. Request used by the GetServiceBinding
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service_binding.ServiceBinding:
                    ServiceBinding is the resource that
                defines a Service Directory Service to
                be used in a BackendService resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/serviceBindings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_service_binding(
                request, metadata
            )
            pb_request = service_binding.GetServiceBindingRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = service_binding.ServiceBinding()
            pb_resp = service_binding.ServiceBinding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service_binding(resp)
            return resp

    class _GetTcpRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("GetTcpRoute")

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
            request: tcp_route.GetTcpRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tcp_route.TcpRoute:
            r"""Call the get tcp route method over HTTP.

            Args:
                request (~.tcp_route.GetTcpRouteRequest):
                    The request object. Request used by the GetTcpRoute
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tcp_route.TcpRoute:
                    TcpRoute is the resource defining how
                TCP traffic should be routed by a
                Mesh/Gateway resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/tcpRoutes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_tcp_route(request, metadata)
            pb_request = tcp_route.GetTcpRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = tcp_route.TcpRoute()
            pb_resp = tcp_route.TcpRoute.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_tcp_route(resp)
            return resp

    class _GetTlsRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("GetTlsRoute")

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
            request: tls_route.GetTlsRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tls_route.TlsRoute:
            r"""Call the get tls route method over HTTP.

            Args:
                request (~.tls_route.GetTlsRouteRequest):
                    The request object. Request used by the GetTlsRoute
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tls_route.TlsRoute:
                    TlsRoute defines how traffic should
                be routed based on SNI and other
                matching L3 attributes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/tlsRoutes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_tls_route(request, metadata)
            pb_request = tls_route.GetTlsRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = tls_route.TlsRoute()
            pb_resp = tls_route.TlsRoute.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_tls_route(resp)
            return resp

    class _ListEndpointPolicies(NetworkServicesRestStub):
        def __hash__(self):
            return hash("ListEndpointPolicies")

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
            request: endpoint_policy.ListEndpointPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> endpoint_policy.ListEndpointPoliciesResponse:
            r"""Call the list endpoint policies method over HTTP.

            Args:
                request (~.endpoint_policy.ListEndpointPoliciesRequest):
                    The request object. Request used with the
                ListEndpointPolicies method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.endpoint_policy.ListEndpointPoliciesResponse:
                    Response returned by the
                ListEndpointPolicies method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/endpointPolicies",
                },
            ]
            request, metadata = self._interceptor.pre_list_endpoint_policies(
                request, metadata
            )
            pb_request = endpoint_policy.ListEndpointPoliciesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = endpoint_policy.ListEndpointPoliciesResponse()
            pb_resp = endpoint_policy.ListEndpointPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_endpoint_policies(resp)
            return resp

    class _ListGateways(NetworkServicesRestStub):
        def __hash__(self):
            return hash("ListGateways")

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
            request: gateway.ListGatewaysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gateway.ListGatewaysResponse:
            r"""Call the list gateways method over HTTP.

            Args:
                request (~.gateway.ListGatewaysRequest):
                    The request object. Request used with the ListGateways
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gateway.ListGatewaysResponse:
                    Response returned by the ListGateways
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/gateways",
                },
            ]
            request, metadata = self._interceptor.pre_list_gateways(request, metadata)
            pb_request = gateway.ListGatewaysRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = gateway.ListGatewaysResponse()
            pb_resp = gateway.ListGatewaysResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_gateways(resp)
            return resp

    class _ListGrpcRoutes(NetworkServicesRestStub):
        def __hash__(self):
            return hash("ListGrpcRoutes")

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
            request: grpc_route.ListGrpcRoutesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> grpc_route.ListGrpcRoutesResponse:
            r"""Call the list grpc routes method over HTTP.

            Args:
                request (~.grpc_route.ListGrpcRoutesRequest):
                    The request object. Request used with the ListGrpcRoutes
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.grpc_route.ListGrpcRoutesResponse:
                    Response returned by the
                ListGrpcRoutes method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/grpcRoutes",
                },
            ]
            request, metadata = self._interceptor.pre_list_grpc_routes(
                request, metadata
            )
            pb_request = grpc_route.ListGrpcRoutesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = grpc_route.ListGrpcRoutesResponse()
            pb_resp = grpc_route.ListGrpcRoutesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_grpc_routes(resp)
            return resp

    class _ListHttpRoutes(NetworkServicesRestStub):
        def __hash__(self):
            return hash("ListHttpRoutes")

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
            request: http_route.ListHttpRoutesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> http_route.ListHttpRoutesResponse:
            r"""Call the list http routes method over HTTP.

            Args:
                request (~.http_route.ListHttpRoutesRequest):
                    The request object. Request used with the ListHttpRoutes
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.http_route.ListHttpRoutesResponse:
                    Response returned by the
                ListHttpRoutes method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/httpRoutes",
                },
            ]
            request, metadata = self._interceptor.pre_list_http_routes(
                request, metadata
            )
            pb_request = http_route.ListHttpRoutesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = http_route.ListHttpRoutesResponse()
            pb_resp = http_route.ListHttpRoutesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_http_routes(resp)
            return resp

    class _ListMeshes(NetworkServicesRestStub):
        def __hash__(self):
            return hash("ListMeshes")

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
            request: mesh.ListMeshesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> mesh.ListMeshesResponse:
            r"""Call the list meshes method over HTTP.

            Args:
                request (~.mesh.ListMeshesRequest):
                    The request object. Request used with the ListMeshes
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.mesh.ListMeshesResponse:
                    Response returned by the ListMeshes
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/meshes",
                },
            ]
            request, metadata = self._interceptor.pre_list_meshes(request, metadata)
            pb_request = mesh.ListMeshesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = mesh.ListMeshesResponse()
            pb_resp = mesh.ListMeshesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_meshes(resp)
            return resp

    class _ListServiceBindings(NetworkServicesRestStub):
        def __hash__(self):
            return hash("ListServiceBindings")

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
            request: service_binding.ListServiceBindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service_binding.ListServiceBindingsResponse:
            r"""Call the list service bindings method over HTTP.

            Args:
                request (~.service_binding.ListServiceBindingsRequest):
                    The request object. Request used with the
                ListServiceBindings method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service_binding.ListServiceBindingsResponse:
                    Response returned by the
                ListServiceBindings method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/serviceBindings",
                },
            ]
            request, metadata = self._interceptor.pre_list_service_bindings(
                request, metadata
            )
            pb_request = service_binding.ListServiceBindingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = service_binding.ListServiceBindingsResponse()
            pb_resp = service_binding.ListServiceBindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_service_bindings(resp)
            return resp

    class _ListTcpRoutes(NetworkServicesRestStub):
        def __hash__(self):
            return hash("ListTcpRoutes")

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
            request: tcp_route.ListTcpRoutesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tcp_route.ListTcpRoutesResponse:
            r"""Call the list tcp routes method over HTTP.

            Args:
                request (~.tcp_route.ListTcpRoutesRequest):
                    The request object. Request used with the ListTcpRoutes
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tcp_route.ListTcpRoutesResponse:
                    Response returned by the
                ListTcpRoutes method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/tcpRoutes",
                },
            ]
            request, metadata = self._interceptor.pre_list_tcp_routes(request, metadata)
            pb_request = tcp_route.ListTcpRoutesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = tcp_route.ListTcpRoutesResponse()
            pb_resp = tcp_route.ListTcpRoutesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_tcp_routes(resp)
            return resp

    class _ListTlsRoutes(NetworkServicesRestStub):
        def __hash__(self):
            return hash("ListTlsRoutes")

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
            request: tls_route.ListTlsRoutesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tls_route.ListTlsRoutesResponse:
            r"""Call the list tls routes method over HTTP.

            Args:
                request (~.tls_route.ListTlsRoutesRequest):
                    The request object. Request used with the ListTlsRoutes
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tls_route.ListTlsRoutesResponse:
                    Response returned by the
                ListTlsRoutes method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/tlsRoutes",
                },
            ]
            request, metadata = self._interceptor.pre_list_tls_routes(request, metadata)
            pb_request = tls_route.ListTlsRoutesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = tls_route.ListTlsRoutesResponse()
            pb_resp = tls_route.ListTlsRoutesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_tls_routes(resp)
            return resp

    class _UpdateEndpointPolicy(NetworkServicesRestStub):
        def __hash__(self):
            return hash("UpdateEndpointPolicy")

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
            request: gcn_endpoint_policy.UpdateEndpointPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update endpoint policy method over HTTP.

            Args:
                request (~.gcn_endpoint_policy.UpdateEndpointPolicyRequest):
                    The request object. Request used with the
                UpdateEndpointPolicy method.
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
                    "method": "patch",
                    "uri": "/v1/{endpoint_policy.name=projects/*/locations/*/endpointPolicies/*}",
                    "body": "endpoint_policy",
                },
            ]
            request, metadata = self._interceptor.pre_update_endpoint_policy(
                request, metadata
            )
            pb_request = gcn_endpoint_policy.UpdateEndpointPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_update_endpoint_policy(resp)
            return resp

    class _UpdateGateway(NetworkServicesRestStub):
        def __hash__(self):
            return hash("UpdateGateway")

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
            request: gcn_gateway.UpdateGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update gateway method over HTTP.

            Args:
                request (~.gcn_gateway.UpdateGatewayRequest):
                    The request object. Request used by the UpdateGateway
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{gateway.name=projects/*/locations/*/gateways/*}",
                    "body": "gateway",
                },
            ]
            request, metadata = self._interceptor.pre_update_gateway(request, metadata)
            pb_request = gcn_gateway.UpdateGatewayRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_update_gateway(resp)
            return resp

    class _UpdateGrpcRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("UpdateGrpcRoute")

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
            request: gcn_grpc_route.UpdateGrpcRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update grpc route method over HTTP.

            Args:
                request (~.gcn_grpc_route.UpdateGrpcRouteRequest):
                    The request object. Request used by the UpdateGrpcRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{grpc_route.name=projects/*/locations/*/grpcRoutes/*}",
                    "body": "grpc_route",
                },
            ]
            request, metadata = self._interceptor.pre_update_grpc_route(
                request, metadata
            )
            pb_request = gcn_grpc_route.UpdateGrpcRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_update_grpc_route(resp)
            return resp

    class _UpdateHttpRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("UpdateHttpRoute")

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
            request: gcn_http_route.UpdateHttpRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update http route method over HTTP.

            Args:
                request (~.gcn_http_route.UpdateHttpRouteRequest):
                    The request object. Request used by the UpdateHttpRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{http_route.name=projects/*/locations/*/httpRoutes/*}",
                    "body": "http_route",
                },
            ]
            request, metadata = self._interceptor.pre_update_http_route(
                request, metadata
            )
            pb_request = gcn_http_route.UpdateHttpRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_update_http_route(resp)
            return resp

    class _UpdateMesh(NetworkServicesRestStub):
        def __hash__(self):
            return hash("UpdateMesh")

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
            request: gcn_mesh.UpdateMeshRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update mesh method over HTTP.

            Args:
                request (~.gcn_mesh.UpdateMeshRequest):
                    The request object. Request used by the UpdateMesh
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{mesh.name=projects/*/locations/*/meshes/*}",
                    "body": "mesh",
                },
            ]
            request, metadata = self._interceptor.pre_update_mesh(request, metadata)
            pb_request = gcn_mesh.UpdateMeshRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_update_mesh(resp)
            return resp

    class _UpdateTcpRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("UpdateTcpRoute")

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
            request: gcn_tcp_route.UpdateTcpRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update tcp route method over HTTP.

            Args:
                request (~.gcn_tcp_route.UpdateTcpRouteRequest):
                    The request object. Request used by the UpdateTcpRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{tcp_route.name=projects/*/locations/*/tcpRoutes/*}",
                    "body": "tcp_route",
                },
            ]
            request, metadata = self._interceptor.pre_update_tcp_route(
                request, metadata
            )
            pb_request = gcn_tcp_route.UpdateTcpRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_update_tcp_route(resp)
            return resp

    class _UpdateTlsRoute(NetworkServicesRestStub):
        def __hash__(self):
            return hash("UpdateTlsRoute")

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
            request: gcn_tls_route.UpdateTlsRouteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update tls route method over HTTP.

            Args:
                request (~.gcn_tls_route.UpdateTlsRouteRequest):
                    The request object. Request used by the UpdateTlsRoute
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{tls_route.name=projects/*/locations/*/tlsRoutes/*}",
                    "body": "tls_route",
                },
            ]
            request, metadata = self._interceptor.pre_update_tls_route(
                request, metadata
            )
            pb_request = gcn_tls_route.UpdateTlsRouteRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = self._interceptor.post_update_tls_route(resp)
            return resp

    @property
    def create_endpoint_policy(
        self,
    ) -> Callable[
        [gcn_endpoint_policy.CreateEndpointPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEndpointPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_gateway(
        self,
    ) -> Callable[[gcn_gateway.CreateGatewayRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_grpc_route(
        self,
    ) -> Callable[[gcn_grpc_route.CreateGrpcRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGrpcRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_http_route(
        self,
    ) -> Callable[[gcn_http_route.CreateHttpRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateHttpRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_mesh(
        self,
    ) -> Callable[[gcn_mesh.CreateMeshRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMesh(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_service_binding(
        self,
    ) -> Callable[
        [gcn_service_binding.CreateServiceBindingRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateServiceBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_tcp_route(
        self,
    ) -> Callable[[gcn_tcp_route.CreateTcpRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTcpRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_tls_route(
        self,
    ) -> Callable[[gcn_tls_route.CreateTlsRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTlsRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_endpoint_policy(
        self,
    ) -> Callable[
        [endpoint_policy.DeleteEndpointPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEndpointPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_gateway(
        self,
    ) -> Callable[[gateway.DeleteGatewayRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_grpc_route(
        self,
    ) -> Callable[[grpc_route.DeleteGrpcRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGrpcRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_http_route(
        self,
    ) -> Callable[[http_route.DeleteHttpRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteHttpRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_mesh(
        self,
    ) -> Callable[[mesh.DeleteMeshRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMesh(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_service_binding(
        self,
    ) -> Callable[
        [service_binding.DeleteServiceBindingRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteServiceBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_tcp_route(
        self,
    ) -> Callable[[tcp_route.DeleteTcpRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTcpRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_tls_route(
        self,
    ) -> Callable[[tls_route.DeleteTlsRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTlsRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_endpoint_policy(
        self,
    ) -> Callable[
        [endpoint_policy.GetEndpointPolicyRequest], endpoint_policy.EndpointPolicy
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEndpointPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_gateway(self) -> Callable[[gateway.GetGatewayRequest], gateway.Gateway]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_grpc_route(
        self,
    ) -> Callable[[grpc_route.GetGrpcRouteRequest], grpc_route.GrpcRoute]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGrpcRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_http_route(
        self,
    ) -> Callable[[http_route.GetHttpRouteRequest], http_route.HttpRoute]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetHttpRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_mesh(self) -> Callable[[mesh.GetMeshRequest], mesh.Mesh]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMesh(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service_binding(
        self,
    ) -> Callable[
        [service_binding.GetServiceBindingRequest], service_binding.ServiceBinding
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetServiceBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_tcp_route(
        self,
    ) -> Callable[[tcp_route.GetTcpRouteRequest], tcp_route.TcpRoute]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTcpRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_tls_route(
        self,
    ) -> Callable[[tls_route.GetTlsRouteRequest], tls_route.TlsRoute]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTlsRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_endpoint_policies(
        self,
    ) -> Callable[
        [endpoint_policy.ListEndpointPoliciesRequest],
        endpoint_policy.ListEndpointPoliciesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEndpointPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_gateways(
        self,
    ) -> Callable[[gateway.ListGatewaysRequest], gateway.ListGatewaysResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGateways(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_grpc_routes(
        self,
    ) -> Callable[
        [grpc_route.ListGrpcRoutesRequest], grpc_route.ListGrpcRoutesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGrpcRoutes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_http_routes(
        self,
    ) -> Callable[
        [http_route.ListHttpRoutesRequest], http_route.ListHttpRoutesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListHttpRoutes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_meshes(
        self,
    ) -> Callable[[mesh.ListMeshesRequest], mesh.ListMeshesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMeshes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_service_bindings(
        self,
    ) -> Callable[
        [service_binding.ListServiceBindingsRequest],
        service_binding.ListServiceBindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServiceBindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_tcp_routes(
        self,
    ) -> Callable[[tcp_route.ListTcpRoutesRequest], tcp_route.ListTcpRoutesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTcpRoutes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_tls_routes(
        self,
    ) -> Callable[[tls_route.ListTlsRoutesRequest], tls_route.ListTlsRoutesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTlsRoutes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_endpoint_policy(
        self,
    ) -> Callable[
        [gcn_endpoint_policy.UpdateEndpointPolicyRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEndpointPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_gateway(
        self,
    ) -> Callable[[gcn_gateway.UpdateGatewayRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_grpc_route(
        self,
    ) -> Callable[[gcn_grpc_route.UpdateGrpcRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGrpcRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_http_route(
        self,
    ) -> Callable[[gcn_http_route.UpdateHttpRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateHttpRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_mesh(
        self,
    ) -> Callable[[gcn_mesh.UpdateMeshRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMesh(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_tcp_route(
        self,
    ) -> Callable[[gcn_tcp_route.UpdateTcpRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTcpRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_tls_route(
        self,
    ) -> Callable[[gcn_tls_route.UpdateTlsRouteRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTlsRoute(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(NetworkServicesRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(NetworkServicesRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(NetworkServicesRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheKeysets/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheOrigins/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheServices/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/endpointPolicies/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/serviceBindings/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/meshes/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/gateways/*}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(NetworkServicesRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheKeysets/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheOrigins/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheServices/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/endpointPolicies/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/serviceBindings/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/meshes/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/gateways/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(NetworkServicesRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheKeysets/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheOrigins/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/edgeCacheServices/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/endpointPolicies/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/serviceBindings/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/meshes/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/gateways/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(NetworkServicesRestStub):
        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(NetworkServicesRestStub):
        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(NetworkServicesRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(NetworkServicesRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("NetworkServicesRestTransport",)
