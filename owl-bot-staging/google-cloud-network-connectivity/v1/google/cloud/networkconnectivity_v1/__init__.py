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
from google.cloud.networkconnectivity_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.hub_service import HubServiceClient
from .services.hub_service import HubServiceAsyncClient
from .services.policy_based_routing_service import PolicyBasedRoutingServiceClient
from .services.policy_based_routing_service import PolicyBasedRoutingServiceAsyncClient

from .types.common import OperationMetadata
from .types.hub import CreateHubRequest
from .types.hub import CreateSpokeRequest
from .types.hub import DeleteHubRequest
from .types.hub import DeleteSpokeRequest
from .types.hub import GetHubRequest
from .types.hub import GetSpokeRequest
from .types.hub import Hub
from .types.hub import LinkedInterconnectAttachments
from .types.hub import LinkedRouterApplianceInstances
from .types.hub import LinkedVpnTunnels
from .types.hub import ListHubsRequest
from .types.hub import ListHubsResponse
from .types.hub import ListSpokesRequest
from .types.hub import ListSpokesResponse
from .types.hub import LocationMetadata
from .types.hub import RouterApplianceInstance
from .types.hub import RoutingVPC
from .types.hub import Spoke
from .types.hub import UpdateHubRequest
from .types.hub import UpdateSpokeRequest
from .types.hub import LocationFeature
from .types.hub import State
from .types.policy_based_routing import CreatePolicyBasedRouteRequest
from .types.policy_based_routing import DeletePolicyBasedRouteRequest
from .types.policy_based_routing import GetPolicyBasedRouteRequest
from .types.policy_based_routing import ListPolicyBasedRoutesRequest
from .types.policy_based_routing import ListPolicyBasedRoutesResponse
from .types.policy_based_routing import PolicyBasedRoute

__all__ = (
    'HubServiceAsyncClient',
    'PolicyBasedRoutingServiceAsyncClient',
'CreateHubRequest',
'CreatePolicyBasedRouteRequest',
'CreateSpokeRequest',
'DeleteHubRequest',
'DeletePolicyBasedRouteRequest',
'DeleteSpokeRequest',
'GetHubRequest',
'GetPolicyBasedRouteRequest',
'GetSpokeRequest',
'Hub',
'HubServiceClient',
'LinkedInterconnectAttachments',
'LinkedRouterApplianceInstances',
'LinkedVpnTunnels',
'ListHubsRequest',
'ListHubsResponse',
'ListPolicyBasedRoutesRequest',
'ListPolicyBasedRoutesResponse',
'ListSpokesRequest',
'ListSpokesResponse',
'LocationFeature',
'LocationMetadata',
'OperationMetadata',
'PolicyBasedRoute',
'PolicyBasedRoutingServiceClient',
'RouterApplianceInstance',
'RoutingVPC',
'Spoke',
'State',
'UpdateHubRequest',
'UpdateSpokeRequest',
)
