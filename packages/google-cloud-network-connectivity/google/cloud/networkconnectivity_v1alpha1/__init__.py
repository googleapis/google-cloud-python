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
from google.cloud.networkconnectivity_v1alpha1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.hub_service import HubServiceAsyncClient, HubServiceClient
from .types.common import OperationMetadata
from .types.hub import (
    CreateHubRequest,
    CreateSpokeRequest,
    DeleteHubRequest,
    DeleteSpokeRequest,
    GetHubRequest,
    GetSpokeRequest,
    Hub,
    ListHubsRequest,
    ListHubsResponse,
    ListSpokesRequest,
    ListSpokesResponse,
    RouterApplianceInstance,
    Spoke,
    State,
    UpdateHubRequest,
    UpdateSpokeRequest,
)

__all__ = (
    "HubServiceAsyncClient",
    "CreateHubRequest",
    "CreateSpokeRequest",
    "DeleteHubRequest",
    "DeleteSpokeRequest",
    "GetHubRequest",
    "GetSpokeRequest",
    "Hub",
    "HubServiceClient",
    "ListHubsRequest",
    "ListHubsResponse",
    "ListSpokesRequest",
    "ListSpokesResponse",
    "OperationMetadata",
    "RouterApplianceInstance",
    "Spoke",
    "State",
    "UpdateHubRequest",
    "UpdateSpokeRequest",
)
