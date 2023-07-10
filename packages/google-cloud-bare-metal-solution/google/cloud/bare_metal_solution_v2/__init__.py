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
from google.cloud.bare_metal_solution_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.bare_metal_solution import (
    BareMetalSolutionAsyncClient,
    BareMetalSolutionClient,
)
from .types.baremetalsolution import OperationMetadata, ResetInstanceResponse
from .types.instance import (
    DetachLunRequest,
    GetInstanceRequest,
    Instance,
    ListInstancesRequest,
    ListInstancesResponse,
    ResetInstanceRequest,
    ServerNetworkTemplate,
    StartInstanceRequest,
    StartInstanceResponse,
    StopInstanceRequest,
    StopInstanceResponse,
    UpdateInstanceRequest,
)
from .types.lun import GetLunRequest, ListLunsRequest, ListLunsResponse, Lun
from .types.network import (
    VRF,
    GetNetworkRequest,
    ListNetworksRequest,
    ListNetworksResponse,
    ListNetworkUsageRequest,
    ListNetworkUsageResponse,
    LogicalInterface,
    Network,
    NetworkAddressReservation,
    NetworkUsage,
    UpdateNetworkRequest,
)
from .types.nfs_share import (
    GetNfsShareRequest,
    ListNfsSharesRequest,
    ListNfsSharesResponse,
    NfsShare,
    UpdateNfsShareRequest,
)
from .types.volume import (
    GetVolumeRequest,
    ListVolumesRequest,
    ListVolumesResponse,
    ResizeVolumeRequest,
    UpdateVolumeRequest,
    Volume,
)

__all__ = (
    "BareMetalSolutionAsyncClient",
    "BareMetalSolutionClient",
    "DetachLunRequest",
    "GetInstanceRequest",
    "GetLunRequest",
    "GetNetworkRequest",
    "GetNfsShareRequest",
    "GetVolumeRequest",
    "Instance",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListLunsRequest",
    "ListLunsResponse",
    "ListNetworkUsageRequest",
    "ListNetworkUsageResponse",
    "ListNetworksRequest",
    "ListNetworksResponse",
    "ListNfsSharesRequest",
    "ListNfsSharesResponse",
    "ListVolumesRequest",
    "ListVolumesResponse",
    "LogicalInterface",
    "Lun",
    "Network",
    "NetworkAddressReservation",
    "NetworkUsage",
    "NfsShare",
    "OperationMetadata",
    "ResetInstanceRequest",
    "ResetInstanceResponse",
    "ResizeVolumeRequest",
    "ServerNetworkTemplate",
    "StartInstanceRequest",
    "StartInstanceResponse",
    "StopInstanceRequest",
    "StopInstanceResponse",
    "UpdateInstanceRequest",
    "UpdateNetworkRequest",
    "UpdateNfsShareRequest",
    "UpdateVolumeRequest",
    "VRF",
    "Volume",
)
