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
from google.cloud.network_services import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.network_services_v1.services.dep_service.async_client import (
    DepServiceAsyncClient,
)
from google.cloud.network_services_v1.services.dep_service.client import (
    DepServiceClient,
)
from google.cloud.network_services_v1.services.network_services.async_client import (
    NetworkServicesAsyncClient,
)
from google.cloud.network_services_v1.services.network_services.client import (
    NetworkServicesClient,
)
from google.cloud.network_services_v1.types.common import (
    EndpointMatcher,
    OperationMetadata,
    TrafficPortSelector,
)
from google.cloud.network_services_v1.types.dep import (
    CreateLbRouteExtensionRequest,
    CreateLbTrafficExtensionRequest,
    DeleteLbRouteExtensionRequest,
    DeleteLbTrafficExtensionRequest,
    EventType,
    ExtensionChain,
    GetLbRouteExtensionRequest,
    GetLbTrafficExtensionRequest,
    LbRouteExtension,
    LbTrafficExtension,
    ListLbRouteExtensionsRequest,
    ListLbRouteExtensionsResponse,
    ListLbTrafficExtensionsRequest,
    ListLbTrafficExtensionsResponse,
    LoadBalancingScheme,
    UpdateLbRouteExtensionRequest,
    UpdateLbTrafficExtensionRequest,
)
from google.cloud.network_services_v1.types.endpoint_policy import (
    CreateEndpointPolicyRequest,
    DeleteEndpointPolicyRequest,
    EndpointPolicy,
    GetEndpointPolicyRequest,
    ListEndpointPoliciesRequest,
    ListEndpointPoliciesResponse,
    UpdateEndpointPolicyRequest,
)
from google.cloud.network_services_v1.types.gateway import (
    CreateGatewayRequest,
    DeleteGatewayRequest,
    Gateway,
    GetGatewayRequest,
    ListGatewaysRequest,
    ListGatewaysResponse,
    UpdateGatewayRequest,
)
from google.cloud.network_services_v1.types.grpc_route import (
    CreateGrpcRouteRequest,
    DeleteGrpcRouteRequest,
    GetGrpcRouteRequest,
    GrpcRoute,
    ListGrpcRoutesRequest,
    ListGrpcRoutesResponse,
    UpdateGrpcRouteRequest,
)
from google.cloud.network_services_v1.types.http_route import (
    CreateHttpRouteRequest,
    DeleteHttpRouteRequest,
    GetHttpRouteRequest,
    HttpRoute,
    ListHttpRoutesRequest,
    ListHttpRoutesResponse,
    UpdateHttpRouteRequest,
)
from google.cloud.network_services_v1.types.mesh import (
    CreateMeshRequest,
    DeleteMeshRequest,
    GetMeshRequest,
    ListMeshesRequest,
    ListMeshesResponse,
    Mesh,
    UpdateMeshRequest,
)
from google.cloud.network_services_v1.types.service_binding import (
    CreateServiceBindingRequest,
    DeleteServiceBindingRequest,
    GetServiceBindingRequest,
    ListServiceBindingsRequest,
    ListServiceBindingsResponse,
    ServiceBinding,
)
from google.cloud.network_services_v1.types.tcp_route import (
    CreateTcpRouteRequest,
    DeleteTcpRouteRequest,
    GetTcpRouteRequest,
    ListTcpRoutesRequest,
    ListTcpRoutesResponse,
    TcpRoute,
    UpdateTcpRouteRequest,
)
from google.cloud.network_services_v1.types.tls_route import (
    CreateTlsRouteRequest,
    DeleteTlsRouteRequest,
    GetTlsRouteRequest,
    ListTlsRoutesRequest,
    ListTlsRoutesResponse,
    TlsRoute,
    UpdateTlsRouteRequest,
)

__all__ = (
    "DepServiceClient",
    "DepServiceAsyncClient",
    "NetworkServicesClient",
    "NetworkServicesAsyncClient",
    "EndpointMatcher",
    "OperationMetadata",
    "TrafficPortSelector",
    "CreateLbRouteExtensionRequest",
    "CreateLbTrafficExtensionRequest",
    "DeleteLbRouteExtensionRequest",
    "DeleteLbTrafficExtensionRequest",
    "ExtensionChain",
    "GetLbRouteExtensionRequest",
    "GetLbTrafficExtensionRequest",
    "LbRouteExtension",
    "LbTrafficExtension",
    "ListLbRouteExtensionsRequest",
    "ListLbRouteExtensionsResponse",
    "ListLbTrafficExtensionsRequest",
    "ListLbTrafficExtensionsResponse",
    "UpdateLbRouteExtensionRequest",
    "UpdateLbTrafficExtensionRequest",
    "EventType",
    "LoadBalancingScheme",
    "CreateEndpointPolicyRequest",
    "DeleteEndpointPolicyRequest",
    "EndpointPolicy",
    "GetEndpointPolicyRequest",
    "ListEndpointPoliciesRequest",
    "ListEndpointPoliciesResponse",
    "UpdateEndpointPolicyRequest",
    "CreateGatewayRequest",
    "DeleteGatewayRequest",
    "Gateway",
    "GetGatewayRequest",
    "ListGatewaysRequest",
    "ListGatewaysResponse",
    "UpdateGatewayRequest",
    "CreateGrpcRouteRequest",
    "DeleteGrpcRouteRequest",
    "GetGrpcRouteRequest",
    "GrpcRoute",
    "ListGrpcRoutesRequest",
    "ListGrpcRoutesResponse",
    "UpdateGrpcRouteRequest",
    "CreateHttpRouteRequest",
    "DeleteHttpRouteRequest",
    "GetHttpRouteRequest",
    "HttpRoute",
    "ListHttpRoutesRequest",
    "ListHttpRoutesResponse",
    "UpdateHttpRouteRequest",
    "CreateMeshRequest",
    "DeleteMeshRequest",
    "GetMeshRequest",
    "ListMeshesRequest",
    "ListMeshesResponse",
    "Mesh",
    "UpdateMeshRequest",
    "CreateServiceBindingRequest",
    "DeleteServiceBindingRequest",
    "GetServiceBindingRequest",
    "ListServiceBindingsRequest",
    "ListServiceBindingsResponse",
    "ServiceBinding",
    "CreateTcpRouteRequest",
    "DeleteTcpRouteRequest",
    "GetTcpRouteRequest",
    "ListTcpRoutesRequest",
    "ListTcpRoutesResponse",
    "TcpRoute",
    "UpdateTcpRouteRequest",
    "CreateTlsRouteRequest",
    "DeleteTlsRouteRequest",
    "GetTlsRouteRequest",
    "ListTlsRoutesRequest",
    "ListTlsRoutesResponse",
    "TlsRoute",
    "UpdateTlsRouteRequest",
)
