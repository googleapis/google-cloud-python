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
from google.cloud.network_services_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.dep_service import DepServiceClient
from .services.dep_service import DepServiceAsyncClient
from .services.network_services import NetworkServicesClient
from .services.network_services import NetworkServicesAsyncClient

from .types.common import EndpointMatcher
from .types.common import OperationMetadata
from .types.common import TrafficPortSelector
from .types.dep import CreateLbRouteExtensionRequest
from .types.dep import CreateLbTrafficExtensionRequest
from .types.dep import DeleteLbRouteExtensionRequest
from .types.dep import DeleteLbTrafficExtensionRequest
from .types.dep import ExtensionChain
from .types.dep import GetLbRouteExtensionRequest
from .types.dep import GetLbTrafficExtensionRequest
from .types.dep import LbRouteExtension
from .types.dep import LbTrafficExtension
from .types.dep import ListLbRouteExtensionsRequest
from .types.dep import ListLbRouteExtensionsResponse
from .types.dep import ListLbTrafficExtensionsRequest
from .types.dep import ListLbTrafficExtensionsResponse
from .types.dep import UpdateLbRouteExtensionRequest
from .types.dep import UpdateLbTrafficExtensionRequest
from .types.dep import EventType
from .types.dep import LoadBalancingScheme
from .types.endpoint_policy import CreateEndpointPolicyRequest
from .types.endpoint_policy import DeleteEndpointPolicyRequest
from .types.endpoint_policy import EndpointPolicy
from .types.endpoint_policy import GetEndpointPolicyRequest
from .types.endpoint_policy import ListEndpointPoliciesRequest
from .types.endpoint_policy import ListEndpointPoliciesResponse
from .types.endpoint_policy import UpdateEndpointPolicyRequest
from .types.gateway import CreateGatewayRequest
from .types.gateway import DeleteGatewayRequest
from .types.gateway import Gateway
from .types.gateway import GetGatewayRequest
from .types.gateway import ListGatewaysRequest
from .types.gateway import ListGatewaysResponse
from .types.gateway import UpdateGatewayRequest
from .types.grpc_route import CreateGrpcRouteRequest
from .types.grpc_route import DeleteGrpcRouteRequest
from .types.grpc_route import GetGrpcRouteRequest
from .types.grpc_route import GrpcRoute
from .types.grpc_route import ListGrpcRoutesRequest
from .types.grpc_route import ListGrpcRoutesResponse
from .types.grpc_route import UpdateGrpcRouteRequest
from .types.http_route import CreateHttpRouteRequest
from .types.http_route import DeleteHttpRouteRequest
from .types.http_route import GetHttpRouteRequest
from .types.http_route import HttpRoute
from .types.http_route import ListHttpRoutesRequest
from .types.http_route import ListHttpRoutesResponse
from .types.http_route import UpdateHttpRouteRequest
from .types.mesh import CreateMeshRequest
from .types.mesh import DeleteMeshRequest
from .types.mesh import GetMeshRequest
from .types.mesh import ListMeshesRequest
from .types.mesh import ListMeshesResponse
from .types.mesh import Mesh
from .types.mesh import UpdateMeshRequest
from .types.service_binding import CreateServiceBindingRequest
from .types.service_binding import DeleteServiceBindingRequest
from .types.service_binding import GetServiceBindingRequest
from .types.service_binding import ListServiceBindingsRequest
from .types.service_binding import ListServiceBindingsResponse
from .types.service_binding import ServiceBinding
from .types.tcp_route import CreateTcpRouteRequest
from .types.tcp_route import DeleteTcpRouteRequest
from .types.tcp_route import GetTcpRouteRequest
from .types.tcp_route import ListTcpRoutesRequest
from .types.tcp_route import ListTcpRoutesResponse
from .types.tcp_route import TcpRoute
from .types.tcp_route import UpdateTcpRouteRequest
from .types.tls_route import CreateTlsRouteRequest
from .types.tls_route import DeleteTlsRouteRequest
from .types.tls_route import GetTlsRouteRequest
from .types.tls_route import ListTlsRoutesRequest
from .types.tls_route import ListTlsRoutesResponse
from .types.tls_route import TlsRoute
from .types.tls_route import UpdateTlsRouteRequest

__all__ = (
    'DepServiceAsyncClient',
    'NetworkServicesAsyncClient',
'CreateEndpointPolicyRequest',
'CreateGatewayRequest',
'CreateGrpcRouteRequest',
'CreateHttpRouteRequest',
'CreateLbRouteExtensionRequest',
'CreateLbTrafficExtensionRequest',
'CreateMeshRequest',
'CreateServiceBindingRequest',
'CreateTcpRouteRequest',
'CreateTlsRouteRequest',
'DeleteEndpointPolicyRequest',
'DeleteGatewayRequest',
'DeleteGrpcRouteRequest',
'DeleteHttpRouteRequest',
'DeleteLbRouteExtensionRequest',
'DeleteLbTrafficExtensionRequest',
'DeleteMeshRequest',
'DeleteServiceBindingRequest',
'DeleteTcpRouteRequest',
'DeleteTlsRouteRequest',
'DepServiceClient',
'EndpointMatcher',
'EndpointPolicy',
'EventType',
'ExtensionChain',
'Gateway',
'GetEndpointPolicyRequest',
'GetGatewayRequest',
'GetGrpcRouteRequest',
'GetHttpRouteRequest',
'GetLbRouteExtensionRequest',
'GetLbTrafficExtensionRequest',
'GetMeshRequest',
'GetServiceBindingRequest',
'GetTcpRouteRequest',
'GetTlsRouteRequest',
'GrpcRoute',
'HttpRoute',
'LbRouteExtension',
'LbTrafficExtension',
'ListEndpointPoliciesRequest',
'ListEndpointPoliciesResponse',
'ListGatewaysRequest',
'ListGatewaysResponse',
'ListGrpcRoutesRequest',
'ListGrpcRoutesResponse',
'ListHttpRoutesRequest',
'ListHttpRoutesResponse',
'ListLbRouteExtensionsRequest',
'ListLbRouteExtensionsResponse',
'ListLbTrafficExtensionsRequest',
'ListLbTrafficExtensionsResponse',
'ListMeshesRequest',
'ListMeshesResponse',
'ListServiceBindingsRequest',
'ListServiceBindingsResponse',
'ListTcpRoutesRequest',
'ListTcpRoutesResponse',
'ListTlsRoutesRequest',
'ListTlsRoutesResponse',
'LoadBalancingScheme',
'Mesh',
'NetworkServicesClient',
'OperationMetadata',
'ServiceBinding',
'TcpRoute',
'TlsRoute',
'TrafficPortSelector',
'UpdateEndpointPolicyRequest',
'UpdateGatewayRequest',
'UpdateGrpcRouteRequest',
'UpdateHttpRouteRequest',
'UpdateLbRouteExtensionRequest',
'UpdateLbTrafficExtensionRequest',
'UpdateMeshRequest',
'UpdateTcpRouteRequest',
'UpdateTlsRouteRequest',
)
