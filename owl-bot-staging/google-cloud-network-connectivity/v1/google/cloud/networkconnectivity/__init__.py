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
from google.cloud.networkconnectivity import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.networkconnectivity_v1.services.cross_network_automation_service.client import CrossNetworkAutomationServiceClient
from google.cloud.networkconnectivity_v1.services.cross_network_automation_service.async_client import CrossNetworkAutomationServiceAsyncClient
from google.cloud.networkconnectivity_v1.services.data_transfer_service.client import DataTransferServiceClient
from google.cloud.networkconnectivity_v1.services.data_transfer_service.async_client import DataTransferServiceAsyncClient
from google.cloud.networkconnectivity_v1.services.hub_service.client import HubServiceClient
from google.cloud.networkconnectivity_v1.services.hub_service.async_client import HubServiceAsyncClient
from google.cloud.networkconnectivity_v1.services.internal_range_service.client import InternalRangeServiceClient
from google.cloud.networkconnectivity_v1.services.internal_range_service.async_client import InternalRangeServiceAsyncClient
from google.cloud.networkconnectivity_v1.services.policy_based_routing_service.client import PolicyBasedRoutingServiceClient
from google.cloud.networkconnectivity_v1.services.policy_based_routing_service.async_client import PolicyBasedRoutingServiceAsyncClient

from google.cloud.networkconnectivity_v1.types.common import OperationMetadata
from google.cloud.networkconnectivity_v1.types.cross_network_automation import CreateServiceConnectionMapRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import CreateServiceConnectionPolicyRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import CreateServiceConnectionTokenRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import DeleteServiceClassRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import DeleteServiceConnectionMapRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import DeleteServiceConnectionPolicyRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import DeleteServiceConnectionTokenRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import GetServiceClassRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import GetServiceConnectionMapRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import GetServiceConnectionPolicyRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import GetServiceConnectionTokenRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ListServiceClassesRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ListServiceClassesResponse
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ListServiceConnectionMapsRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ListServiceConnectionMapsResponse
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ListServiceConnectionPoliciesRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ListServiceConnectionPoliciesResponse
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ListServiceConnectionTokensRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ListServiceConnectionTokensResponse
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ServiceClass
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ServiceConnectionMap
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ServiceConnectionPolicy
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ServiceConnectionToken
from google.cloud.networkconnectivity_v1.types.cross_network_automation import UpdateServiceClassRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import UpdateServiceConnectionMapRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import UpdateServiceConnectionPolicyRequest
from google.cloud.networkconnectivity_v1.types.cross_network_automation import ConnectionErrorType
from google.cloud.networkconnectivity_v1.types.cross_network_automation import Infrastructure
from google.cloud.networkconnectivity_v1.types.cross_network_automation import IPVersion
from google.cloud.networkconnectivity_v1.types.data_transfer import CreateDestinationRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import CreateMulticloudDataTransferConfigRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import DeleteDestinationRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import DeleteMulticloudDataTransferConfigRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import Destination
from google.cloud.networkconnectivity_v1.types.data_transfer import GetDestinationRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import GetMulticloudDataTransferConfigRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import GetMulticloudDataTransferSupportedServiceRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import ListDestinationsRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import ListDestinationsResponse
from google.cloud.networkconnectivity_v1.types.data_transfer import ListMulticloudDataTransferConfigsRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import ListMulticloudDataTransferConfigsResponse
from google.cloud.networkconnectivity_v1.types.data_transfer import ListMulticloudDataTransferSupportedServicesRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import ListMulticloudDataTransferSupportedServicesResponse
from google.cloud.networkconnectivity_v1.types.data_transfer import MulticloudDataTransferConfig
from google.cloud.networkconnectivity_v1.types.data_transfer import MulticloudDataTransferSupportedService
from google.cloud.networkconnectivity_v1.types.data_transfer import ServiceConfig
from google.cloud.networkconnectivity_v1.types.data_transfer import StateTimeline
from google.cloud.networkconnectivity_v1.types.data_transfer import UpdateDestinationRequest
from google.cloud.networkconnectivity_v1.types.data_transfer import UpdateMulticloudDataTransferConfigRequest
from google.cloud.networkconnectivity_v1.types.hub import AcceptHubSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import AcceptHubSpokeResponse
from google.cloud.networkconnectivity_v1.types.hub import AcceptSpokeUpdateRequest
from google.cloud.networkconnectivity_v1.types.hub import AcceptSpokeUpdateResponse
from google.cloud.networkconnectivity_v1.types.hub import AutoAccept
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
from google.cloud.networkconnectivity_v1.types.hub import HubStatusEntry
from google.cloud.networkconnectivity_v1.types.hub import LinkedInterconnectAttachments
from google.cloud.networkconnectivity_v1.types.hub import LinkedProducerVpcNetwork
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
from google.cloud.networkconnectivity_v1.types.hub import NextHopInterconnectAttachment
from google.cloud.networkconnectivity_v1.types.hub import NextHopRouterApplianceInstance
from google.cloud.networkconnectivity_v1.types.hub import NextHopVpcNetwork
from google.cloud.networkconnectivity_v1.types.hub import NextHopVPNTunnel
from google.cloud.networkconnectivity_v1.types.hub import PscPropagationStatus
from google.cloud.networkconnectivity_v1.types.hub import QueryHubStatusRequest
from google.cloud.networkconnectivity_v1.types.hub import QueryHubStatusResponse
from google.cloud.networkconnectivity_v1.types.hub import RejectHubSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import RejectHubSpokeResponse
from google.cloud.networkconnectivity_v1.types.hub import RejectSpokeUpdateRequest
from google.cloud.networkconnectivity_v1.types.hub import RejectSpokeUpdateResponse
from google.cloud.networkconnectivity_v1.types.hub import Route
from google.cloud.networkconnectivity_v1.types.hub import RouterApplianceInstance
from google.cloud.networkconnectivity_v1.types.hub import RouteTable
from google.cloud.networkconnectivity_v1.types.hub import RoutingVPC
from google.cloud.networkconnectivity_v1.types.hub import Spoke
from google.cloud.networkconnectivity_v1.types.hub import SpokeSummary
from google.cloud.networkconnectivity_v1.types.hub import UpdateGroupRequest
from google.cloud.networkconnectivity_v1.types.hub import UpdateHubRequest
from google.cloud.networkconnectivity_v1.types.hub import UpdateSpokeRequest
from google.cloud.networkconnectivity_v1.types.hub import LocationFeature
from google.cloud.networkconnectivity_v1.types.hub import PolicyMode
from google.cloud.networkconnectivity_v1.types.hub import PresetTopology
from google.cloud.networkconnectivity_v1.types.hub import RouteType
from google.cloud.networkconnectivity_v1.types.hub import SpokeType
from google.cloud.networkconnectivity_v1.types.hub import State
from google.cloud.networkconnectivity_v1.types.internal_range import CreateInternalRangeRequest
from google.cloud.networkconnectivity_v1.types.internal_range import DeleteInternalRangeRequest
from google.cloud.networkconnectivity_v1.types.internal_range import GetInternalRangeRequest
from google.cloud.networkconnectivity_v1.types.internal_range import InternalRange
from google.cloud.networkconnectivity_v1.types.internal_range import ListInternalRangesRequest
from google.cloud.networkconnectivity_v1.types.internal_range import ListInternalRangesResponse
from google.cloud.networkconnectivity_v1.types.internal_range import UpdateInternalRangeRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import CreatePolicyBasedRouteRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import DeletePolicyBasedRouteRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import GetPolicyBasedRouteRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import ListPolicyBasedRoutesRequest
from google.cloud.networkconnectivity_v1.types.policy_based_routing import ListPolicyBasedRoutesResponse
from google.cloud.networkconnectivity_v1.types.policy_based_routing import PolicyBasedRoute

__all__ = ('CrossNetworkAutomationServiceClient',
    'CrossNetworkAutomationServiceAsyncClient',
    'DataTransferServiceClient',
    'DataTransferServiceAsyncClient',
    'HubServiceClient',
    'HubServiceAsyncClient',
    'InternalRangeServiceClient',
    'InternalRangeServiceAsyncClient',
    'PolicyBasedRoutingServiceClient',
    'PolicyBasedRoutingServiceAsyncClient',
    'OperationMetadata',
    'CreateServiceConnectionMapRequest',
    'CreateServiceConnectionPolicyRequest',
    'CreateServiceConnectionTokenRequest',
    'DeleteServiceClassRequest',
    'DeleteServiceConnectionMapRequest',
    'DeleteServiceConnectionPolicyRequest',
    'DeleteServiceConnectionTokenRequest',
    'GetServiceClassRequest',
    'GetServiceConnectionMapRequest',
    'GetServiceConnectionPolicyRequest',
    'GetServiceConnectionTokenRequest',
    'ListServiceClassesRequest',
    'ListServiceClassesResponse',
    'ListServiceConnectionMapsRequest',
    'ListServiceConnectionMapsResponse',
    'ListServiceConnectionPoliciesRequest',
    'ListServiceConnectionPoliciesResponse',
    'ListServiceConnectionTokensRequest',
    'ListServiceConnectionTokensResponse',
    'ServiceClass',
    'ServiceConnectionMap',
    'ServiceConnectionPolicy',
    'ServiceConnectionToken',
    'UpdateServiceClassRequest',
    'UpdateServiceConnectionMapRequest',
    'UpdateServiceConnectionPolicyRequest',
    'ConnectionErrorType',
    'Infrastructure',
    'IPVersion',
    'CreateDestinationRequest',
    'CreateMulticloudDataTransferConfigRequest',
    'DeleteDestinationRequest',
    'DeleteMulticloudDataTransferConfigRequest',
    'Destination',
    'GetDestinationRequest',
    'GetMulticloudDataTransferConfigRequest',
    'GetMulticloudDataTransferSupportedServiceRequest',
    'ListDestinationsRequest',
    'ListDestinationsResponse',
    'ListMulticloudDataTransferConfigsRequest',
    'ListMulticloudDataTransferConfigsResponse',
    'ListMulticloudDataTransferSupportedServicesRequest',
    'ListMulticloudDataTransferSupportedServicesResponse',
    'MulticloudDataTransferConfig',
    'MulticloudDataTransferSupportedService',
    'ServiceConfig',
    'StateTimeline',
    'UpdateDestinationRequest',
    'UpdateMulticloudDataTransferConfigRequest',
    'AcceptHubSpokeRequest',
    'AcceptHubSpokeResponse',
    'AcceptSpokeUpdateRequest',
    'AcceptSpokeUpdateResponse',
    'AutoAccept',
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
    'HubStatusEntry',
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
    'ListRoutesRequest',
    'ListRoutesResponse',
    'ListRouteTablesRequest',
    'ListRouteTablesResponse',
    'ListSpokesRequest',
    'ListSpokesResponse',
    'LocationMetadata',
    'NextHopInterconnectAttachment',
    'NextHopRouterApplianceInstance',
    'NextHopVpcNetwork',
    'NextHopVPNTunnel',
    'PscPropagationStatus',
    'QueryHubStatusRequest',
    'QueryHubStatusResponse',
    'RejectHubSpokeRequest',
    'RejectHubSpokeResponse',
    'RejectSpokeUpdateRequest',
    'RejectSpokeUpdateResponse',
    'Route',
    'RouterApplianceInstance',
    'RouteTable',
    'RoutingVPC',
    'Spoke',
    'SpokeSummary',
    'UpdateGroupRequest',
    'UpdateHubRequest',
    'UpdateSpokeRequest',
    'LocationFeature',
    'PolicyMode',
    'PresetTopology',
    'RouteType',
    'SpokeType',
    'State',
    'CreateInternalRangeRequest',
    'DeleteInternalRangeRequest',
    'GetInternalRangeRequest',
    'InternalRange',
    'ListInternalRangesRequest',
    'ListInternalRangesResponse',
    'UpdateInternalRangeRequest',
    'CreatePolicyBasedRouteRequest',
    'DeletePolicyBasedRouteRequest',
    'GetPolicyBasedRouteRequest',
    'ListPolicyBasedRoutesRequest',
    'ListPolicyBasedRoutesResponse',
    'PolicyBasedRoute',
)
