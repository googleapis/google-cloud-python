# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from .types.common import EnvoyHeaders
from .types.dep import AuthzExtension
from .types.dep import CreateAuthzExtensionRequest
from .types.dep import CreateLbRouteExtensionRequest
from .types.dep import CreateLbTrafficExtensionRequest
from .types.dep import DeleteAuthzExtensionRequest
from .types.dep import DeleteLbRouteExtensionRequest
from .types.dep import DeleteLbTrafficExtensionRequest
from .types.dep import ExtensionChain
from .types.dep import GetAuthzExtensionRequest
from .types.dep import GetLbRouteExtensionRequest
from .types.dep import GetLbTrafficExtensionRequest
from .types.dep import LbRouteExtension
from .types.dep import LbTrafficExtension
from .types.dep import ListAuthzExtensionsRequest
from .types.dep import ListAuthzExtensionsResponse
from .types.dep import ListLbRouteExtensionsRequest
from .types.dep import ListLbRouteExtensionsResponse
from .types.dep import ListLbTrafficExtensionsRequest
from .types.dep import ListLbTrafficExtensionsResponse
from .types.dep import UpdateAuthzExtensionRequest
from .types.dep import UpdateLbRouteExtensionRequest
from .types.dep import UpdateLbTrafficExtensionRequest
from .types.dep import EventType
from .types.dep import LoadBalancingScheme
from .types.dep import WireFormat
from .types.endpoint_policy import CreateEndpointPolicyRequest
from .types.endpoint_policy import DeleteEndpointPolicyRequest
from .types.endpoint_policy import EndpointPolicy
from .types.endpoint_policy import GetEndpointPolicyRequest
from .types.endpoint_policy import ListEndpointPoliciesRequest
from .types.endpoint_policy import ListEndpointPoliciesResponse
from .types.endpoint_policy import UpdateEndpointPolicyRequest
from .types.extensibility import CreateWasmPluginRequest
from .types.extensibility import CreateWasmPluginVersionRequest
from .types.extensibility import DeleteWasmPluginRequest
from .types.extensibility import DeleteWasmPluginVersionRequest
from .types.extensibility import GetWasmPluginRequest
from .types.extensibility import GetWasmPluginVersionRequest
from .types.extensibility import ListWasmPluginsRequest
from .types.extensibility import ListWasmPluginsResponse
from .types.extensibility import ListWasmPluginVersionsRequest
from .types.extensibility import ListWasmPluginVersionsResponse
from .types.extensibility import UpdateWasmPluginRequest
from .types.extensibility import WasmPlugin
from .types.extensibility import WasmPluginVersion
from .types.extensibility import WasmPluginView
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
from .types.route_view import GatewayRouteView
from .types.route_view import GetGatewayRouteViewRequest
from .types.route_view import GetMeshRouteViewRequest
from .types.route_view import ListGatewayRouteViewsRequest
from .types.route_view import ListGatewayRouteViewsResponse
from .types.route_view import ListMeshRouteViewsRequest
from .types.route_view import ListMeshRouteViewsResponse
from .types.route_view import MeshRouteView
from .types.service_binding import CreateServiceBindingRequest
from .types.service_binding import DeleteServiceBindingRequest
from .types.service_binding import GetServiceBindingRequest
from .types.service_binding import ListServiceBindingsRequest
from .types.service_binding import ListServiceBindingsResponse
from .types.service_binding import ServiceBinding
from .types.service_binding import UpdateServiceBindingRequest
from .types.service_lb_policy import CreateServiceLbPolicyRequest
from .types.service_lb_policy import DeleteServiceLbPolicyRequest
from .types.service_lb_policy import GetServiceLbPolicyRequest
from .types.service_lb_policy import ListServiceLbPoliciesRequest
from .types.service_lb_policy import ListServiceLbPoliciesResponse
from .types.service_lb_policy import ServiceLbPolicy
from .types.service_lb_policy import UpdateServiceLbPolicyRequest
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
'AuthzExtension',
'CreateAuthzExtensionRequest',
'CreateEndpointPolicyRequest',
'CreateGatewayRequest',
'CreateGrpcRouteRequest',
'CreateHttpRouteRequest',
'CreateLbRouteExtensionRequest',
'CreateLbTrafficExtensionRequest',
'CreateMeshRequest',
'CreateServiceBindingRequest',
'CreateServiceLbPolicyRequest',
'CreateTcpRouteRequest',
'CreateTlsRouteRequest',
'CreateWasmPluginRequest',
'CreateWasmPluginVersionRequest',
'DeleteAuthzExtensionRequest',
'DeleteEndpointPolicyRequest',
'DeleteGatewayRequest',
'DeleteGrpcRouteRequest',
'DeleteHttpRouteRequest',
'DeleteLbRouteExtensionRequest',
'DeleteLbTrafficExtensionRequest',
'DeleteMeshRequest',
'DeleteServiceBindingRequest',
'DeleteServiceLbPolicyRequest',
'DeleteTcpRouteRequest',
'DeleteTlsRouteRequest',
'DeleteWasmPluginRequest',
'DeleteWasmPluginVersionRequest',
'DepServiceClient',
'EndpointMatcher',
'EndpointPolicy',
'EnvoyHeaders',
'EventType',
'ExtensionChain',
'Gateway',
'GatewayRouteView',
'GetAuthzExtensionRequest',
'GetEndpointPolicyRequest',
'GetGatewayRequest',
'GetGatewayRouteViewRequest',
'GetGrpcRouteRequest',
'GetHttpRouteRequest',
'GetLbRouteExtensionRequest',
'GetLbTrafficExtensionRequest',
'GetMeshRequest',
'GetMeshRouteViewRequest',
'GetServiceBindingRequest',
'GetServiceLbPolicyRequest',
'GetTcpRouteRequest',
'GetTlsRouteRequest',
'GetWasmPluginRequest',
'GetWasmPluginVersionRequest',
'GrpcRoute',
'HttpRoute',
'LbRouteExtension',
'LbTrafficExtension',
'ListAuthzExtensionsRequest',
'ListAuthzExtensionsResponse',
'ListEndpointPoliciesRequest',
'ListEndpointPoliciesResponse',
'ListGatewayRouteViewsRequest',
'ListGatewayRouteViewsResponse',
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
'ListMeshRouteViewsRequest',
'ListMeshRouteViewsResponse',
'ListMeshesRequest',
'ListMeshesResponse',
'ListServiceBindingsRequest',
'ListServiceBindingsResponse',
'ListServiceLbPoliciesRequest',
'ListServiceLbPoliciesResponse',
'ListTcpRoutesRequest',
'ListTcpRoutesResponse',
'ListTlsRoutesRequest',
'ListTlsRoutesResponse',
'ListWasmPluginVersionsRequest',
'ListWasmPluginVersionsResponse',
'ListWasmPluginsRequest',
'ListWasmPluginsResponse',
'LoadBalancingScheme',
'Mesh',
'MeshRouteView',
'NetworkServicesClient',
'OperationMetadata',
'ServiceBinding',
'ServiceLbPolicy',
'TcpRoute',
'TlsRoute',
'TrafficPortSelector',
'UpdateAuthzExtensionRequest',
'UpdateEndpointPolicyRequest',
'UpdateGatewayRequest',
'UpdateGrpcRouteRequest',
'UpdateHttpRouteRequest',
'UpdateLbRouteExtensionRequest',
'UpdateLbTrafficExtensionRequest',
'UpdateMeshRequest',
'UpdateServiceBindingRequest',
'UpdateServiceLbPolicyRequest',
'UpdateTcpRouteRequest',
'UpdateTlsRouteRequest',
'UpdateWasmPluginRequest',
'WasmPlugin',
'WasmPluginVersion',
'WasmPluginView',
'WireFormat',
)
