# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.network_services import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.network_services_v1.services.network_services.client import NetworkServicesClient
from google.cloud.network_services_v1.services.network_services.async_client import NetworkServicesAsyncClient

from google.cloud.network_services_v1.types.common import EndpointMatcher
from google.cloud.network_services_v1.types.common import OperationMetadata
from google.cloud.network_services_v1.types.common import TrafficPortSelector
from google.cloud.network_services_v1.types.endpoint_policy import CreateEndpointPolicyRequest
from google.cloud.network_services_v1.types.endpoint_policy import DeleteEndpointPolicyRequest
from google.cloud.network_services_v1.types.endpoint_policy import EndpointPolicy
from google.cloud.network_services_v1.types.endpoint_policy import GetEndpointPolicyRequest
from google.cloud.network_services_v1.types.endpoint_policy import ListEndpointPoliciesRequest
from google.cloud.network_services_v1.types.endpoint_policy import ListEndpointPoliciesResponse
from google.cloud.network_services_v1.types.endpoint_policy import UpdateEndpointPolicyRequest
from google.cloud.network_services_v1.types.gateway import CreateGatewayRequest
from google.cloud.network_services_v1.types.gateway import DeleteGatewayRequest
from google.cloud.network_services_v1.types.gateway import Gateway
from google.cloud.network_services_v1.types.gateway import GetGatewayRequest
from google.cloud.network_services_v1.types.gateway import ListGatewaysRequest
from google.cloud.network_services_v1.types.gateway import ListGatewaysResponse
from google.cloud.network_services_v1.types.gateway import UpdateGatewayRequest
from google.cloud.network_services_v1.types.grpc_route import CreateGrpcRouteRequest
from google.cloud.network_services_v1.types.grpc_route import DeleteGrpcRouteRequest
from google.cloud.network_services_v1.types.grpc_route import GetGrpcRouteRequest
from google.cloud.network_services_v1.types.grpc_route import GrpcRoute
from google.cloud.network_services_v1.types.grpc_route import ListGrpcRoutesRequest
from google.cloud.network_services_v1.types.grpc_route import ListGrpcRoutesResponse
from google.cloud.network_services_v1.types.grpc_route import UpdateGrpcRouteRequest
from google.cloud.network_services_v1.types.http_route import CreateHttpRouteRequest
from google.cloud.network_services_v1.types.http_route import DeleteHttpRouteRequest
from google.cloud.network_services_v1.types.http_route import GetHttpRouteRequest
from google.cloud.network_services_v1.types.http_route import HttpRoute
from google.cloud.network_services_v1.types.http_route import ListHttpRoutesRequest
from google.cloud.network_services_v1.types.http_route import ListHttpRoutesResponse
from google.cloud.network_services_v1.types.http_route import UpdateHttpRouteRequest
from google.cloud.network_services_v1.types.mesh import CreateMeshRequest
from google.cloud.network_services_v1.types.mesh import DeleteMeshRequest
from google.cloud.network_services_v1.types.mesh import GetMeshRequest
from google.cloud.network_services_v1.types.mesh import ListMeshesRequest
from google.cloud.network_services_v1.types.mesh import ListMeshesResponse
from google.cloud.network_services_v1.types.mesh import Mesh
from google.cloud.network_services_v1.types.mesh import UpdateMeshRequest
from google.cloud.network_services_v1.types.service_binding import CreateServiceBindingRequest
from google.cloud.network_services_v1.types.service_binding import DeleteServiceBindingRequest
from google.cloud.network_services_v1.types.service_binding import GetServiceBindingRequest
from google.cloud.network_services_v1.types.service_binding import ListServiceBindingsRequest
from google.cloud.network_services_v1.types.service_binding import ListServiceBindingsResponse
from google.cloud.network_services_v1.types.service_binding import ServiceBinding
from google.cloud.network_services_v1.types.tcp_route import CreateTcpRouteRequest
from google.cloud.network_services_v1.types.tcp_route import DeleteTcpRouteRequest
from google.cloud.network_services_v1.types.tcp_route import GetTcpRouteRequest
from google.cloud.network_services_v1.types.tcp_route import ListTcpRoutesRequest
from google.cloud.network_services_v1.types.tcp_route import ListTcpRoutesResponse
from google.cloud.network_services_v1.types.tcp_route import TcpRoute
from google.cloud.network_services_v1.types.tcp_route import UpdateTcpRouteRequest
from google.cloud.network_services_v1.types.tls_route import CreateTlsRouteRequest
from google.cloud.network_services_v1.types.tls_route import DeleteTlsRouteRequest
from google.cloud.network_services_v1.types.tls_route import GetTlsRouteRequest
from google.cloud.network_services_v1.types.tls_route import ListTlsRoutesRequest
from google.cloud.network_services_v1.types.tls_route import ListTlsRoutesResponse
from google.cloud.network_services_v1.types.tls_route import TlsRoute
from google.cloud.network_services_v1.types.tls_route import UpdateTlsRouteRequest

__all__ = ('NetworkServicesClient',
    'NetworkServicesAsyncClient',
    'EndpointMatcher',
    'OperationMetadata',
    'TrafficPortSelector',
    'CreateEndpointPolicyRequest',
    'DeleteEndpointPolicyRequest',
    'EndpointPolicy',
    'GetEndpointPolicyRequest',
    'ListEndpointPoliciesRequest',
    'ListEndpointPoliciesResponse',
    'UpdateEndpointPolicyRequest',
    'CreateGatewayRequest',
    'DeleteGatewayRequest',
    'Gateway',
    'GetGatewayRequest',
    'ListGatewaysRequest',
    'ListGatewaysResponse',
    'UpdateGatewayRequest',
    'CreateGrpcRouteRequest',
    'DeleteGrpcRouteRequest',
    'GetGrpcRouteRequest',
    'GrpcRoute',
    'ListGrpcRoutesRequest',
    'ListGrpcRoutesResponse',
    'UpdateGrpcRouteRequest',
    'CreateHttpRouteRequest',
    'DeleteHttpRouteRequest',
    'GetHttpRouteRequest',
    'HttpRoute',
    'ListHttpRoutesRequest',
    'ListHttpRoutesResponse',
    'UpdateHttpRouteRequest',
    'CreateMeshRequest',
    'DeleteMeshRequest',
    'GetMeshRequest',
    'ListMeshesRequest',
    'ListMeshesResponse',
    'Mesh',
    'UpdateMeshRequest',
    'CreateServiceBindingRequest',
    'DeleteServiceBindingRequest',
    'GetServiceBindingRequest',
    'ListServiceBindingsRequest',
    'ListServiceBindingsResponse',
    'ServiceBinding',
    'CreateTcpRouteRequest',
    'DeleteTcpRouteRequest',
    'GetTcpRouteRequest',
    'ListTcpRoutesRequest',
    'ListTcpRoutesResponse',
    'TcpRoute',
    'UpdateTcpRouteRequest',
    'CreateTlsRouteRequest',
    'DeleteTlsRouteRequest',
    'GetTlsRouteRequest',
    'ListTlsRoutesRequest',
    'ListTlsRoutesResponse',
    'TlsRoute',
    'UpdateTlsRouteRequest',
)
