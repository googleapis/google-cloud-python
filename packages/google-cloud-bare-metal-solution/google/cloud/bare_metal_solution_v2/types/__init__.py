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
from .baremetalsolution import OperationMetadata, ResetInstanceResponse
from .instance import (
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
from .lun import GetLunRequest, ListLunsRequest, ListLunsResponse, Lun
from .network import (
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
from .nfs_share import (
    GetNfsShareRequest,
    ListNfsSharesRequest,
    ListNfsSharesResponse,
    NfsShare,
    UpdateNfsShareRequest,
)
from .volume import (
    GetVolumeRequest,
    ListVolumesRequest,
    ListVolumesResponse,
    ResizeVolumeRequest,
    UpdateVolumeRequest,
    Volume,
)

__all__ = (
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
