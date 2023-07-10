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
from google.cloud.network_services_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.network_services import NetworkServicesAsyncClient, NetworkServicesClient
from .types.common import EndpointMatcher, OperationMetadata, TrafficPortSelector
from .types.endpoint_policy import (
    CreateEndpointPolicyRequest,
    DeleteEndpointPolicyRequest,
    EndpointPolicy,
    GetEndpointPolicyRequest,
    ListEndpointPoliciesRequest,
    ListEndpointPoliciesResponse,
    UpdateEndpointPolicyRequest,
)
from .types.gateway import (
    CreateGatewayRequest,
    DeleteGatewayRequest,
    Gateway,
    GetGatewayRequest,
    ListGatewaysRequest,
    ListGatewaysResponse,
    UpdateGatewayRequest,
)
from .types.grpc_route import (
    CreateGrpcRouteRequest,
    DeleteGrpcRouteRequest,
    GetGrpcRouteRequest,
    GrpcRoute,
    ListGrpcRoutesRequest,
    ListGrpcRoutesResponse,
    UpdateGrpcRouteRequest,
)
from .types.http_route import (
    CreateHttpRouteRequest,
    DeleteHttpRouteRequest,
    GetHttpRouteRequest,
    HttpRoute,
    ListHttpRoutesRequest,
    ListHttpRoutesResponse,
    UpdateHttpRouteRequest,
)
from .types.mesh import (
    CreateMeshRequest,
    DeleteMeshRequest,
    GetMeshRequest,
    ListMeshesRequest,
    ListMeshesResponse,
    Mesh,
    UpdateMeshRequest,
)
from .types.service_binding import (
    CreateServiceBindingRequest,
    DeleteServiceBindingRequest,
    GetServiceBindingRequest,
    ListServiceBindingsRequest,
    ListServiceBindingsResponse,
    ServiceBinding,
)
from .types.tcp_route import (
    CreateTcpRouteRequest,
    DeleteTcpRouteRequest,
    GetTcpRouteRequest,
    ListTcpRoutesRequest,
    ListTcpRoutesResponse,
    TcpRoute,
    UpdateTcpRouteRequest,
)
from .types.tls_route import (
    CreateTlsRouteRequest,
    DeleteTlsRouteRequest,
    GetTlsRouteRequest,
    ListTlsRoutesRequest,
    ListTlsRoutesResponse,
    TlsRoute,
    UpdateTlsRouteRequest,
)

__all__ = (
    "NetworkServicesAsyncClient",
    "CreateEndpointPolicyRequest",
    "CreateGatewayRequest",
    "CreateGrpcRouteRequest",
    "CreateHttpRouteRequest",
    "CreateMeshRequest",
    "CreateServiceBindingRequest",
    "CreateTcpRouteRequest",
    "CreateTlsRouteRequest",
    "DeleteEndpointPolicyRequest",
    "DeleteGatewayRequest",
    "DeleteGrpcRouteRequest",
    "DeleteHttpRouteRequest",
    "DeleteMeshRequest",
    "DeleteServiceBindingRequest",
    "DeleteTcpRouteRequest",
    "DeleteTlsRouteRequest",
    "EndpointMatcher",
    "EndpointPolicy",
    "Gateway",
    "GetEndpointPolicyRequest",
    "GetGatewayRequest",
    "GetGrpcRouteRequest",
    "GetHttpRouteRequest",
    "GetMeshRequest",
    "GetServiceBindingRequest",
    "GetTcpRouteRequest",
    "GetTlsRouteRequest",
    "GrpcRoute",
    "HttpRoute",
    "ListEndpointPoliciesRequest",
    "ListEndpointPoliciesResponse",
    "ListGatewaysRequest",
    "ListGatewaysResponse",
    "ListGrpcRoutesRequest",
    "ListGrpcRoutesResponse",
    "ListHttpRoutesRequest",
    "ListHttpRoutesResponse",
    "ListMeshesRequest",
    "ListMeshesResponse",
    "ListServiceBindingsRequest",
    "ListServiceBindingsResponse",
    "ListTcpRoutesRequest",
    "ListTcpRoutesResponse",
    "ListTlsRoutesRequest",
    "ListTlsRoutesResponse",
    "Mesh",
    "NetworkServicesClient",
    "OperationMetadata",
    "ServiceBinding",
    "TcpRoute",
    "TlsRoute",
    "TrafficPortSelector",
    "UpdateEndpointPolicyRequest",
    "UpdateGatewayRequest",
    "UpdateGrpcRouteRequest",
    "UpdateHttpRouteRequest",
    "UpdateMeshRequest",
    "UpdateTcpRouteRequest",
    "UpdateTlsRouteRequest",
)
