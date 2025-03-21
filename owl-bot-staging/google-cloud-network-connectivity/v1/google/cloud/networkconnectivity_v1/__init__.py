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
from google.cloud.networkconnectivity_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cross_network_automation_service import CrossNetworkAutomationServiceClient
from .services.cross_network_automation_service import CrossNetworkAutomationServiceAsyncClient
from .services.hub_service import HubServiceClient
from .services.hub_service import HubServiceAsyncClient
from .services.policy_based_routing_service import PolicyBasedRoutingServiceClient
from .services.policy_based_routing_service import PolicyBasedRoutingServiceAsyncClient

from .types.common import OperationMetadata
from .types.cross_network_automation import CreateServiceConnectionMapRequest
from .types.cross_network_automation import CreateServiceConnectionPolicyRequest
from .types.cross_network_automation import CreateServiceConnectionTokenRequest
from .types.cross_network_automation import DeleteServiceClassRequest
from .types.cross_network_automation import DeleteServiceConnectionMapRequest
from .types.cross_network_automation import DeleteServiceConnectionPolicyRequest
from .types.cross_network_automation import DeleteServiceConnectionTokenRequest
from .types.cross_network_automation import GetServiceClassRequest
from .types.cross_network_automation import GetServiceConnectionMapRequest
from .types.cross_network_automation import GetServiceConnectionPolicyRequest
from .types.cross_network_automation import GetServiceConnectionTokenRequest
from .types.cross_network_automation import ListServiceClassesRequest
from .types.cross_network_automation import ListServiceClassesResponse
from .types.cross_network_automation import ListServiceConnectionMapsRequest
from .types.cross_network_automation import ListServiceConnectionMapsResponse
from .types.cross_network_automation import ListServiceConnectionPoliciesRequest
from .types.cross_network_automation import ListServiceConnectionPoliciesResponse
from .types.cross_network_automation import ListServiceConnectionTokensRequest
from .types.cross_network_automation import ListServiceConnectionTokensResponse
from .types.cross_network_automation import ServiceClass
from .types.cross_network_automation import ServiceConnectionMap
from .types.cross_network_automation import ServiceConnectionPolicy
from .types.cross_network_automation import ServiceConnectionToken
from .types.cross_network_automation import UpdateServiceClassRequest
from .types.cross_network_automation import UpdateServiceConnectionMapRequest
from .types.cross_network_automation import UpdateServiceConnectionPolicyRequest
from .types.cross_network_automation import ConnectionErrorType
from .types.cross_network_automation import Infrastructure
from .types.cross_network_automation import IPVersion
from .types.hub import AcceptHubSpokeRequest
from .types.hub import AcceptHubSpokeResponse
from .types.hub import AcceptSpokeUpdateRequest
from .types.hub import AcceptSpokeUpdateResponse
from .types.hub import AutoAccept
from .types.hub import CreateHubRequest
from .types.hub import CreateSpokeRequest
from .types.hub import DeleteHubRequest
from .types.hub import DeleteSpokeRequest
from .types.hub import GetGroupRequest
from .types.hub import GetHubRequest
from .types.hub import GetRouteRequest
from .types.hub import GetRouteTableRequest
from .types.hub import GetSpokeRequest
from .types.hub import Group
from .types.hub import Hub
from .types.hub import HubStatusEntry
from .types.hub import LinkedInterconnectAttachments
from .types.hub import LinkedProducerVpcNetwork
from .types.hub import LinkedRouterApplianceInstances
from .types.hub import LinkedVpcNetwork
from .types.hub import LinkedVpnTunnels
from .types.hub import ListGroupsRequest
from .types.hub import ListGroupsResponse
from .types.hub import ListHubSpokesRequest
from .types.hub import ListHubSpokesResponse
from .types.hub import ListHubsRequest
from .types.hub import ListHubsResponse
from .types.hub import ListRoutesRequest
from .types.hub import ListRoutesResponse
from .types.hub import ListRouteTablesRequest
from .types.hub import ListRouteTablesResponse
from .types.hub import ListSpokesRequest
from .types.hub import ListSpokesResponse
from .types.hub import LocationMetadata
from .types.hub import NextHopInterconnectAttachment
from .types.hub import NextHopRouterApplianceInstance
from .types.hub import NextHopVpcNetwork
from .types.hub import NextHopVPNTunnel
from .types.hub import PscPropagationStatus
from .types.hub import QueryHubStatusRequest
from .types.hub import QueryHubStatusResponse
from .types.hub import RejectHubSpokeRequest
from .types.hub import RejectHubSpokeResponse
from .types.hub import RejectSpokeUpdateRequest
from .types.hub import RejectSpokeUpdateResponse
from .types.hub import Route
from .types.hub import RouterApplianceInstance
from .types.hub import RouteTable
from .types.hub import RoutingVPC
from .types.hub import Spoke
from .types.hub import SpokeSummary
from .types.hub import UpdateGroupRequest
from .types.hub import UpdateHubRequest
from .types.hub import UpdateSpokeRequest
from .types.hub import LocationFeature
from .types.hub import PolicyMode
from .types.hub import PresetTopology
from .types.hub import RouteType
from .types.hub import SpokeType
from .types.hub import State
from .types.policy_based_routing import CreatePolicyBasedRouteRequest
from .types.policy_based_routing import DeletePolicyBasedRouteRequest
from .types.policy_based_routing import GetPolicyBasedRouteRequest
from .types.policy_based_routing import ListPolicyBasedRoutesRequest
from .types.policy_based_routing import ListPolicyBasedRoutesResponse
from .types.policy_based_routing import PolicyBasedRoute

__all__ = (
    'CrossNetworkAutomationServiceAsyncClient',
    'HubServiceAsyncClient',
    'PolicyBasedRoutingServiceAsyncClient',
'AcceptHubSpokeRequest',
'AcceptHubSpokeResponse',
'AcceptSpokeUpdateRequest',
'AcceptSpokeUpdateResponse',
'AutoAccept',
'ConnectionErrorType',
'CreateHubRequest',
'CreatePolicyBasedRouteRequest',
'CreateServiceConnectionMapRequest',
'CreateServiceConnectionPolicyRequest',
'CreateServiceConnectionTokenRequest',
'CreateSpokeRequest',
'CrossNetworkAutomationServiceClient',
'DeleteHubRequest',
'DeletePolicyBasedRouteRequest',
'DeleteServiceClassRequest',
'DeleteServiceConnectionMapRequest',
'DeleteServiceConnectionPolicyRequest',
'DeleteServiceConnectionTokenRequest',
'DeleteSpokeRequest',
'GetGroupRequest',
'GetHubRequest',
'GetPolicyBasedRouteRequest',
'GetRouteRequest',
'GetRouteTableRequest',
'GetServiceClassRequest',
'GetServiceConnectionMapRequest',
'GetServiceConnectionPolicyRequest',
'GetServiceConnectionTokenRequest',
'GetSpokeRequest',
'Group',
'Hub',
'HubServiceClient',
'HubStatusEntry',
'IPVersion',
'Infrastructure',
'LinkedInterconnectAttachments',
'LinkedProducerVpcNetwork',
'LinkedRouterApplianceInstances',
'LinkedVpcNetwork',
'LinkedVpnTunnels',
'ListGroupsRequest',
'ListGroupsResponse',
'ListHubSpokesRequest',
'ListHubSpokesResponse',
'ListHubsRequest',
'ListHubsResponse',
'ListPolicyBasedRoutesRequest',
'ListPolicyBasedRoutesResponse',
'ListRouteTablesRequest',
'ListRouteTablesResponse',
'ListRoutesRequest',
'ListRoutesResponse',
'ListServiceClassesRequest',
'ListServiceClassesResponse',
'ListServiceConnectionMapsRequest',
'ListServiceConnectionMapsResponse',
'ListServiceConnectionPoliciesRequest',
'ListServiceConnectionPoliciesResponse',
'ListServiceConnectionTokensRequest',
'ListServiceConnectionTokensResponse',
'ListSpokesRequest',
'ListSpokesResponse',
'LocationFeature',
'LocationMetadata',
'NextHopInterconnectAttachment',
'NextHopRouterApplianceInstance',
'NextHopVPNTunnel',
'NextHopVpcNetwork',
'OperationMetadata',
'PolicyBasedRoute',
'PolicyBasedRoutingServiceClient',
'PolicyMode',
'PresetTopology',
'PscPropagationStatus',
'QueryHubStatusRequest',
'QueryHubStatusResponse',
'RejectHubSpokeRequest',
'RejectHubSpokeResponse',
'RejectSpokeUpdateRequest',
'RejectSpokeUpdateResponse',
'Route',
'RouteTable',
'RouteType',
'RouterApplianceInstance',
'RoutingVPC',
'ServiceClass',
'ServiceConnectionMap',
'ServiceConnectionPolicy',
'ServiceConnectionToken',
'Spoke',
'SpokeSummary',
'SpokeType',
'State',
'UpdateGroupRequest',
'UpdateHubRequest',
'UpdateServiceClassRequest',
'UpdateServiceConnectionMapRequest',
'UpdateServiceConnectionPolicyRequest',
'UpdateSpokeRequest',
)
