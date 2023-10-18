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
from google.cloud.networkconnectivity import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.networkconnectivity_v1.services.hub_service.client import HubServiceClient
from google.cloud.networkconnectivity_v1.services.hub_service.async_client import HubServiceAsyncClient
from google.cloud.networkconnectivity_v1.services.policy_based_routing_service.client import PolicyBasedRoutingServiceClient
from google.cloud.networkconnectivity_v1.services.policy_based_routing_service.async_client import PolicyBasedRoutingServiceAsyncClient

from google.cloud.networkconnectivity_v1.types.common import OperationMetadata
from google.cloud.networkconnectivity_v1.types.hub import AcceptHubSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import AcceptHubSpokeResponse
from google.cloud.networkconnectivity_v1.types.hub import CreateHubRequest
from google.cloud.networkconnectivity_v1.types.hub import CreateSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import DeleteHubRequest
from google.cloud.networkconnectivity_v1.types.hub import DeleteSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import GetGroupRequest
from google.cloud.networkconnectivity_v1.types.hub import GetHubRequest
from google.cloud.networkconnectivity_v1.types.hub import GetRouteRequest
from google.cloud.networkconnectivity_v1.types.hub import GetRouteTableRequest
from google.cloud.networkconnectivity_v1.types.hub import GetSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import Group
from google.cloud.networkconnectivity_v1.types.hub import Hub
from google.cloud.networkconnectivity_v1.types.hub import LinkedInterconnectAttachments
from google.cloud.networkconnectivity_v1.types.hub import LinkedRouterApplianceInstances
from google.cloud.networkconnectivity_v1.types.hub import LinkedVpcNetwork
from google.cloud.networkconnectivity_v1.types.hub import LinkedVpnTunnels
from google.cloud.networkconnectivity_v1.types.hub import ListGroupsRequest
from google.cloud.networkconnectivity_v1.types.hub import ListGroupsResponse
from google.cloud.networkconnectivity_v1.types.hub import ListHubSpokesRequest
from google.cloud.networkconnectivity_v1.types.hub import ListHubSpokesResponse
from google.cloud.networkconnectivity_v1.types.hub import ListHubsRequest
from google.cloud.networkconnectivity_v1.types.hub import ListHubsResponse
from google.cloud.networkconnectivity_v1.types.hub import ListRoutesRequest
from google.cloud.networkconnectivity_v1.types.hub import ListRoutesResponse
from google.cloud.networkconnectivity_v1.types.hub import ListRouteTablesRequest
from google.cloud.networkconnectivity_v1.types.hub import ListRouteTablesResponse
from google.cloud.networkconnectivity_v1.types.hub import ListSpokesRequest
from google.cloud.networkconnectivity_v1.types.hub import ListSpokesResponse
from google.cloud.networkconnectivity_v1.types.hub import LocationMetadata
from google.cloud.networkconnectivity_v1.types.hub import NextHopVpcNetwork
from google.cloud.networkconnectivity_v1.types.hub import RejectHubSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import RejectHubSpokeResponse
from google.cloud.networkconnectivity_v1.types.hub import Route
from google.cloud.networkconnectivity_v1.types.hub import RouterApplianceInstance
from google.cloud.networkconnectivity_v1.types.hub import RouteTable
from google.cloud.networkconnectivity_v1.types.hub import RoutingVPC
from google.cloud.networkconnectivity_v1.types.hub import Spoke
from google.cloud.networkconnectivity_v1.types.hub import SpokeSummary
from google.cloud.networkconnectivity_v1.types.hub import UpdateHubRequest
from google.cloud.networkconnectivity_v1.types.hub import UpdateSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import LocationFeature
from google.cloud.networkconnectivity_v1.types.hub import RouteType
from google.cloud.networkconnectivity_v1.types.hub import SpokeType
from google.cloud.networkconnectivity_v1.types.hub import State
from google.cloud.networkconnectivity_v1.types.policy_based_routing import CreatePolicyBasedRouteRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import DeletePolicyBasedRouteRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import GetPolicyBasedRouteRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import ListPolicyBasedRoutesRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import ListPolicyBasedRoutesResponse
from google.cloud.networkconnectivity_v1.types.policy_based_routing import PolicyBasedRoute

__all__ = ('HubServiceClient',
    'HubServiceAsyncClient',
    'PolicyBasedRoutingServiceClient',
    'PolicyBasedRoutingServiceAsyncClient',
    'OperationMetadata',
    'AcceptHubSpokeRequest',
    'AcceptHubSpokeResponse',
    'CreateHubRequest',
    'CreateSpokeRequest',
    'DeleteHubRequest',
    'DeleteSpokeRequest',
    'GetGroupRequest',
    'GetHubRequest',
    'GetRouteRequest',
    'GetRouteTableRequest',
    'GetSpokeRequest',
    'Group',
    'Hub',
    'LinkedInterconnectAttachments',
    'LinkedRouterApplianceInstances',
    'LinkedVpcNetwork',
    'LinkedVpnTunnels',
    'ListGroupsRequest',
    'ListGroupsResponse',
    'ListHubSpokesRequest',
    'ListHubSpokesResponse',
    'ListHubsRequest',
    'ListHubsResponse',
    'ListRoutesRequest',
    'ListRoutesResponse',
    'ListRouteTablesRequest',
    'ListRouteTablesResponse',
    'ListSpokesRequest',
    'ListSpokesResponse',
    'LocationMetadata',
    'NextHopVpcNetwork',
    'RejectHubSpokeRequest',
    'RejectHubSpokeResponse',
    'Route',
    'RouterApplianceInstance',
    'RouteTable',
    'RoutingVPC',
    'Spoke',
    'SpokeSummary',
    'UpdateHubRequest',
    'UpdateSpokeRequest',
    'LocationFeature',
    'RouteType',
    'SpokeType',
    'State',
    'CreatePolicyBasedRouteRequest',
    'DeletePolicyBasedRouteRequest',
    'GetPolicyBasedRouteRequest',
    'ListPolicyBasedRoutesRequest',
    'ListPolicyBasedRoutesResponse',
    'PolicyBasedRoute',
)
