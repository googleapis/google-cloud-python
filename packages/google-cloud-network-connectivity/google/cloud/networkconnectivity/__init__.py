# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.networkconnectivity_v1alpha1.services.hub_service.client import (
    HubServiceClient,
)
from google.cloud.networkconnectivity_v1alpha1.services.hub_service.async_client import (
    HubServiceAsyncClient,
)

from google.cloud.networkconnectivity_v1alpha1.types.common import OperationMetadata
from google.cloud.networkconnectivity_v1alpha1.types.hub import CreateHubRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import CreateSpokeRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import DeleteHubRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import DeleteSpokeRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import GetHubRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import GetSpokeRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import Hub
from google.cloud.networkconnectivity_v1alpha1.types.hub import ListHubsRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import ListHubsResponse
from google.cloud.networkconnectivity_v1alpha1.types.hub import ListSpokesRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import ListSpokesResponse
from google.cloud.networkconnectivity_v1alpha1.types.hub import RouterApplianceInstance
from google.cloud.networkconnectivity_v1alpha1.types.hub import Spoke
from google.cloud.networkconnectivity_v1alpha1.types.hub import UpdateHubRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import UpdateSpokeRequest
from google.cloud.networkconnectivity_v1alpha1.types.hub import State

__all__ = (
    "HubServiceClient",
    "HubServiceAsyncClient",
    "OperationMetadata",
    "CreateHubRequest",
    "CreateSpokeRequest",
    "DeleteHubRequest",
    "DeleteSpokeRequest",
    "GetHubRequest",
    "GetSpokeRequest",
    "Hub",
    "ListHubsRequest",
    "ListHubsResponse",
    "ListSpokesRequest",
    "ListSpokesResponse",
    "RouterApplianceInstance",
    "Spoke",
    "UpdateHubRequest",
    "UpdateSpokeRequest",
    "State",
)
