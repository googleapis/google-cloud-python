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
from google.cloud.networkconnectivity import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.networkconnectivity_v1.services.hub_service.async_client import (
    HubServiceAsyncClient,
)
from google.cloud.networkconnectivity_v1.services.hub_service.client import (
    HubServiceClient,
)
from google.cloud.networkconnectivity_v1.services.policy_based_routing_service.async_client import (
    PolicyBasedRoutingServiceAsyncClient,
)
from google.cloud.networkconnectivity_v1.services.policy_based_routing_service.client import (
    PolicyBasedRoutingServiceClient,
)
from google.cloud.networkconnectivity_v1.types.common import OperationMetadata
from google.cloud.networkconnectivity_v1.types.hub import (
    AcceptHubSpokeRequest,
    AcceptHubSpokeResponse,
    CreateHubRequest,
    CreateSpokeRequest,
    DeleteHubRequest,
    DeleteSpokeRequest,
    GetGroupRequest,
    GetHubRequest,
    GetRouteRequest,
    GetRouteTableRequest,
    GetSpokeRequest,
    Group,
    Hub,
    LinkedInterconnectAttachments,
    LinkedRouterApplianceInstances,
    LinkedVpcNetwork,
    LinkedVpnTunnels,
    ListGroupsRequest,
    ListGroupsResponse,
    ListHubSpokesRequest,
    ListHubSpokesResponse,
    ListHubsRequest,
    ListHubsResponse,
    ListRoutesRequest,
    ListRoutesResponse,
    ListRouteTablesRequest,
    ListRouteTablesResponse,
    ListSpokesRequest,
    ListSpokesResponse,
    LocationFeature,
    LocationMetadata,
    NextHopVpcNetwork,
    RejectHubSpokeRequest,
    RejectHubSpokeResponse,
    Route,
    RouterApplianceInstance,
    RouteTable,
    RouteType,
    RoutingVPC,
    Spoke,
    SpokeSummary,
    SpokeType,
    State,
    UpdateHubRequest,
    UpdateSpokeRequest,
)
from google.cloud.networkconnectivity_v1.types.policy_based_routing import (
    CreatePolicyBasedRouteRequest,
    DeletePolicyBasedRouteRequest,
    GetPolicyBasedRouteRequest,
    ListPolicyBasedRoutesRequest,
    ListPolicyBasedRoutesResponse,
    PolicyBasedRoute,
)

__all__ = (
    "HubServiceClient",
    "HubServiceAsyncClient",
    "PolicyBasedRoutingServiceClient",
    "PolicyBasedRoutingServiceAsyncClient",
    "OperationMetadata",
    "AcceptHubSpokeRequest",
    "AcceptHubSpokeResponse",
    "CreateHubRequest",
    "CreateSpokeRequest",
    "DeleteHubRequest",
    "DeleteSpokeRequest",
    "GetGroupRequest",
    "GetHubRequest",
    "GetRouteRequest",
    "GetRouteTableRequest",
    "GetSpokeRequest",
    "Group",
    "Hub",
    "LinkedInterconnectAttachments",
    "LinkedRouterApplianceInstances",
    "LinkedVpcNetwork",
    "LinkedVpnTunnels",
    "ListGroupsRequest",
    "ListGroupsResponse",
    "ListHubSpokesRequest",
    "ListHubSpokesResponse",
    "ListHubsRequest",
    "ListHubsResponse",
    "ListRoutesRequest",
    "ListRoutesResponse",
    "ListRouteTablesRequest",
    "ListRouteTablesResponse",
    "ListSpokesRequest",
    "ListSpokesResponse",
    "LocationMetadata",
    "NextHopVpcNetwork",
    "RejectHubSpokeRequest",
    "RejectHubSpokeResponse",
    "Route",
    "RouterApplianceInstance",
    "RouteTable",
    "RoutingVPC",
    "Spoke",
    "SpokeSummary",
    "UpdateHubRequest",
    "UpdateSpokeRequest",
    "LocationFeature",
    "RouteType",
    "SpokeType",
    "State",
    "CreatePolicyBasedRouteRequest",
    "DeletePolicyBasedRouteRequest",
    "GetPolicyBasedRouteRequest",
    "ListPolicyBasedRoutesRequest",
    "ListPolicyBasedRoutesResponse",
    "PolicyBasedRoute",
)
