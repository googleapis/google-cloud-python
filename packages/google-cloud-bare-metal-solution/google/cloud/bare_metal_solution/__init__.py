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
from google.cloud.bare_metal_solution import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bare_metal_solution_v2.services.bare_metal_solution.async_client import (
    BareMetalSolutionAsyncClient,
)
from google.cloud.bare_metal_solution_v2.services.bare_metal_solution.client import (
    BareMetalSolutionClient,
)
from google.cloud.bare_metal_solution_v2.types.baremetalsolution import (
    OperationMetadata,
    ResetInstanceResponse,
)
from google.cloud.bare_metal_solution_v2.types.instance import (
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
from google.cloud.bare_metal_solution_v2.types.lun import (
    GetLunRequest,
    ListLunsRequest,
    ListLunsResponse,
    Lun,
)
from google.cloud.bare_metal_solution_v2.types.network import (
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
from google.cloud.bare_metal_solution_v2.types.nfs_share import (
    GetNfsShareRequest,
    ListNfsSharesRequest,
    ListNfsSharesResponse,
    NfsShare,
    UpdateNfsShareRequest,
)
from google.cloud.bare_metal_solution_v2.types.volume import (
    GetVolumeRequest,
    ListVolumesRequest,
    ListVolumesResponse,
    ResizeVolumeRequest,
    UpdateVolumeRequest,
    Volume,
)

__all__ = (
    "BareMetalSolutionClient",
    "BareMetalSolutionAsyncClient",
    "OperationMetadata",
    "ResetInstanceResponse",
    "DetachLunRequest",
    "GetInstanceRequest",
    "Instance",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ResetInstanceRequest",
    "ServerNetworkTemplate",
    "StartInstanceRequest",
    "StartInstanceResponse",
    "StopInstanceRequest",
    "StopInstanceResponse",
    "UpdateInstanceRequest",
    "GetLunRequest",
    "ListLunsRequest",
    "ListLunsResponse",
    "Lun",
    "GetNetworkRequest",
    "ListNetworksRequest",
    "ListNetworksResponse",
    "ListNetworkUsageRequest",
    "ListNetworkUsageResponse",
    "LogicalInterface",
    "Network",
    "NetworkAddressReservation",
    "NetworkUsage",
    "UpdateNetworkRequest",
    "VRF",
    "GetNfsShareRequest",
    "ListNfsSharesRequest",
    "ListNfsSharesResponse",
    "NfsShare",
    "UpdateNfsShareRequest",
    "GetVolumeRequest",
    "ListVolumesRequest",
    "ListVolumesResponse",
    "ResizeVolumeRequest",
    "UpdateVolumeRequest",
    "Volume",
)
