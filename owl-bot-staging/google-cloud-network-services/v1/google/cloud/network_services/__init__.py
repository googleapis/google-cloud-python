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
from google.cloud.network_services import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.network_services_v1.services.dep_service.client import DepServiceClient
from google.cloud.network_services_v1.services.dep_service.async_client import DepServiceAsyncClient
from google.cloud.network_services_v1.services.network_services.client import NetworkServicesClient
from google.cloud.network_services_v1.services.network_services.async_client import NetworkServicesAsyncClient

from google.cloud.network_services_v1.types.common import EndpointMatcher
from google.cloud.network_services_v1.types.common import OperationMetadata
from google.cloud.network_services_v1.types.common import TrafficPortSelector
from google.cloud.network_services_v1.types.common import EnvoyHeaders
from google.cloud.network_services_v1.types.dep import AuthzExtension
from google.cloud.network_services_v1.types.dep import CreateAuthzExtensionRequest
from google.cloud.network_services_v1.types.dep import CreateLbRouteExtensionRequest
from google.cloud.network_services_v1.types.dep import CreateLbTrafficExtensionRequest
from google.cloud.network_services_v1.types.dep import DeleteAuthzExtensionRequest
from google.cloud.network_services_v1.types.dep import DeleteLbRouteExtensionRequest
from google.cloud.network_services_v1.types.dep import DeleteLbTrafficExtensionRequest
from google.cloud.network_services_v1.types.dep import ExtensionChain
from google.cloud.network_services_v1.types.dep import GetAuthzExtensionRequest
from google.cloud.network_services_v1.types.dep import GetLbRouteExtensionRequest
from google.cloud.network_services_v1.types.dep import GetLbTrafficExtensionRequest
from google.cloud.network_services_v1.types.dep import LbRouteExtension
from google.cloud.network_services_v1.types.dep import LbTrafficExtension
from google.cloud.network_services_v1.types.dep import ListAuthzExtensionsRequest
from google.cloud.network_services_v1.types.dep import ListAuthzExtensionsResponse
from google.cloud.network_services_v1.types.dep import ListLbRouteExtensionsRequest
from google.cloud.network_services_v1.types.dep import ListLbRouteExtensionsResponse
from google.cloud.network_services_v1.types.dep import ListLbTrafficExtensionsRequest
from google.cloud.network_services_v1.types.dep import ListLbTrafficExtensionsResponse
from google.cloud.network_services_v1.types.dep import UpdateAuthzExtensionRequest
from google.cloud.network_services_v1.types.dep import UpdateLbRouteExtensionRequest
from google.cloud.network_services_v1.types.dep import UpdateLbTrafficExtensionRequest
from google.cloud.network_services_v1.types.dep import EventType
from google.cloud.network_services_v1.types.dep import LoadBalancingScheme
from google.cloud.network_services_v1.types.dep import WireFormat
from google.cloud.network_services_v1.types.endpoint_policy import CreateEndpointPolicyRequest
from google.cloud.network_services_v1.types.endpoint_policy import DeleteEndpointPolicyRequest
from google.cloud.network_services_v1.types.endpoint_policy import EndpointPolicy
from google.cloud.network_services_v1.types.endpoint_policy import GetEndpointPolicyRequest
from google.cloud.network_services_v1.types.endpoint_policy import ListEndpointPoliciesRequest
from google.cloud.network_services_v1.types.endpoint_policy import ListEndpointPoliciesResponse
from google.cloud.network_services_v1.types.endpoint_policy import UpdateEndpointPolicyRequest
from google.cloud.network_services_v1.types.extensibility import CreateWasmPluginRequest
from google.cloud.network_services_v1.types.extensibility import CreateWasmPluginVersionRequest
from google.cloud.network_services_v1.types.extensibility import DeleteWasmPluginRequest
from google.cloud.network_services_v1.types.extensibility import DeleteWasmPluginVersionRequest
from google.cloud.network_services_v1.types.extensibility import GetWasmPluginRequest
from google.cloud.network_services_v1.types.extensibility import GetWasmPluginVersionRequest
from google.cloud.network_services_v1.types.extensibility import ListWasmPluginsRequest
from google.cloud.network_services_v1.types.extensibility import ListWasmPluginsResponse
from google.cloud.network_services_v1.types.extensibility import ListWasmPluginVersionsRequest
from google.cloud.network_services_v1.types.extensibility import ListWasmPluginVersionsResponse
from google.cloud.network_services_v1.types.extensibility import UpdateWasmPluginRequest
from google.cloud.network_services_v1.types.extensibility import WasmPlugin
from google.cloud.network_services_v1.types.extensibility import WasmPluginVersion
from google.cloud.network_services_v1.types.extensibility import WasmPluginView
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
from google.cloud.network_services_v1.types.route_view import GatewayRouteView
from google.cloud.network_services_v1.types.route_view import GetGatewayRouteViewRequest
from google.cloud.network_services_v1.types.route_view import GetMeshRouteViewRequest
from google.cloud.network_services_v1.types.route_view import ListGatewayRouteViewsRequest
from google.cloud.network_services_v1.types.route_view import ListGatewayRouteViewsResponse
from google.cloud.network_services_v1.types.route_view import ListMeshRouteViewsRequest
from google.cloud.network_services_v1.types.route_view import ListMeshRouteViewsResponse
from google.cloud.network_services_v1.types.route_view import MeshRouteView
from google.cloud.network_services_v1.types.service_binding import CreateServiceBindingRequest
from google.cloud.network_services_v1.types.service_binding import DeleteServiceBindingRequest
from google.cloud.network_services_v1.types.service_binding import GetServiceBindingRequest
from google.cloud.network_services_v1.types.service_binding import ListServiceBindingsRequest
from google.cloud.network_services_v1.types.service_binding import ListServiceBindingsResponse
from google.cloud.network_services_v1.types.service_binding import ServiceBinding
from google.cloud.network_services_v1.types.service_binding import UpdateServiceBindingRequest
from google.cloud.network_services_v1.types.service_lb_policy import CreateServiceLbPolicyRequest
from google.cloud.network_services_v1.types.service_lb_policy import DeleteServiceLbPolicyRequest
from google.cloud.network_services_v1.types.service_lb_policy import GetServiceLbPolicyRequest
from google.cloud.network_services_v1.types.service_lb_policy import ListServiceLbPoliciesRequest
from google.cloud.network_services_v1.types.service_lb_policy import ListServiceLbPoliciesResponse
from google.cloud.network_services_v1.types.service_lb_policy import ServiceLbPolicy
from google.cloud.network_services_v1.types.service_lb_policy import UpdateServiceLbPolicyRequest
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

__all__ = ('DepServiceClient',
    'DepServiceAsyncClient',
    'NetworkServicesClient',
    'NetworkServicesAsyncClient',
    'EndpointMatcher',
    'OperationMetadata',
    'TrafficPortSelector',
    'EnvoyHeaders',
    'AuthzExtension',
    'CreateAuthzExtensionRequest',
    'CreateLbRouteExtensionRequest',
    'CreateLbTrafficExtensionRequest',
    'DeleteAuthzExtensionRequest',
    'DeleteLbRouteExtensionRequest',
    'DeleteLbTrafficExtensionRequest',
    'ExtensionChain',
    'GetAuthzExtensionRequest',
    'GetLbRouteExtensionRequest',
    'GetLbTrafficExtensionRequest',
    'LbRouteExtension',
    'LbTrafficExtension',
    'ListAuthzExtensionsRequest',
    'ListAuthzExtensionsResponse',
    'ListLbRouteExtensionsRequest',
    'ListLbRouteExtensionsResponse',
    'ListLbTrafficExtensionsRequest',
    'ListLbTrafficExtensionsResponse',
    'UpdateAuthzExtensionRequest',
    'UpdateLbRouteExtensionRequest',
    'UpdateLbTrafficExtensionRequest',
    'EventType',
    'LoadBalancingScheme',
    'WireFormat',
    'CreateEndpointPolicyRequest',
    'DeleteEndpointPolicyRequest',
    'EndpointPolicy',
    'GetEndpointPolicyRequest',
    'ListEndpointPoliciesRequest',
    'ListEndpointPoliciesResponse',
    'UpdateEndpointPolicyRequest',
    'CreateWasmPluginRequest',
    'CreateWasmPluginVersionRequest',
    'DeleteWasmPluginRequest',
    'DeleteWasmPluginVersionRequest',
    'GetWasmPluginRequest',
    'GetWasmPluginVersionRequest',
    'ListWasmPluginsRequest',
    'ListWasmPluginsResponse',
    'ListWasmPluginVersionsRequest',
    'ListWasmPluginVersionsResponse',
    'UpdateWasmPluginRequest',
    'WasmPlugin',
    'WasmPluginVersion',
    'WasmPluginView',
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
    'GatewayRouteView',
    'GetGatewayRouteViewRequest',
    'GetMeshRouteViewRequest',
    'ListGatewayRouteViewsRequest',
    'ListGatewayRouteViewsResponse',
    'ListMeshRouteViewsRequest',
    'ListMeshRouteViewsResponse',
    'MeshRouteView',
    'CreateServiceBindingRequest',
    'DeleteServiceBindingRequest',
    'GetServiceBindingRequest',
    'ListServiceBindingsRequest',
    'ListServiceBindingsResponse',
    'ServiceBinding',
    'UpdateServiceBindingRequest',
    'CreateServiceLbPolicyRequest',
    'DeleteServiceLbPolicyRequest',
    'GetServiceLbPolicyRequest',
    'ListServiceLbPoliciesRequest',
    'ListServiceLbPoliciesResponse',
    'ServiceLbPolicy',
    'UpdateServiceLbPolicyRequest',
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
