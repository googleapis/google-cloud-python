# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from .services.bare_metal_solution import BareMetalSolutionClient
from .services.bare_metal_solution import BareMetalSolutionAsyncClient

from .types.baremetalsolution import CreateSnapshotSchedulePolicyRequest
from .types.baremetalsolution import CreateVolumeSnapshotRequest
from .types.baremetalsolution import DeleteSnapshotSchedulePolicyRequest
from .types.baremetalsolution import DeleteVolumeSnapshotRequest
from .types.baremetalsolution import GetInstanceRequest
from .types.baremetalsolution import GetLunRequest
from .types.baremetalsolution import GetNetworkRequest
from .types.baremetalsolution import GetSnapshotSchedulePolicyRequest
from .types.baremetalsolution import GetVolumeRequest
from .types.baremetalsolution import GetVolumeSnapshotRequest
from .types.baremetalsolution import Instance
from .types.baremetalsolution import ListInstancesRequest
from .types.baremetalsolution import ListInstancesResponse
from .types.baremetalsolution import ListLunsRequest
from .types.baremetalsolution import ListLunsResponse
from .types.baremetalsolution import ListNetworksRequest
from .types.baremetalsolution import ListNetworksResponse
from .types.baremetalsolution import ListSnapshotSchedulePoliciesRequest
from .types.baremetalsolution import ListSnapshotSchedulePoliciesResponse
from .types.baremetalsolution import ListVolumeSnapshotsRequest
from .types.baremetalsolution import ListVolumeSnapshotsResponse
from .types.baremetalsolution import ListVolumesRequest
from .types.baremetalsolution import ListVolumesResponse
from .types.baremetalsolution import Lun
from .types.baremetalsolution import Network
from .types.baremetalsolution import OperationMetadata
from .types.baremetalsolution import ResetInstanceRequest
from .types.baremetalsolution import ResetInstanceResponse
from .types.baremetalsolution import RestoreVolumeSnapshotRequest
from .types.baremetalsolution import SnapshotSchedulePolicy
from .types.baremetalsolution import UpdateSnapshotSchedulePolicyRequest
from .types.baremetalsolution import UpdateVolumeRequest
from .types.baremetalsolution import Volume
from .types.baremetalsolution import VolumeSnapshot
from .types.baremetalsolution import VRF

__all__ = (
    "BareMetalSolutionAsyncClient",
    "BareMetalSolutionClient",
    "CreateSnapshotSchedulePolicyRequest",
    "CreateVolumeSnapshotRequest",
    "DeleteSnapshotSchedulePolicyRequest",
    "DeleteVolumeSnapshotRequest",
    "GetInstanceRequest",
    "GetLunRequest",
    "GetNetworkRequest",
    "GetSnapshotSchedulePolicyRequest",
    "GetVolumeRequest",
    "GetVolumeSnapshotRequest",
    "Instance",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListLunsRequest",
    "ListLunsResponse",
    "ListNetworksRequest",
    "ListNetworksResponse",
    "ListSnapshotSchedulePoliciesRequest",
    "ListSnapshotSchedulePoliciesResponse",
    "ListVolumeSnapshotsRequest",
    "ListVolumeSnapshotsResponse",
    "ListVolumesRequest",
    "ListVolumesResponse",
    "Lun",
    "Network",
    "OperationMetadata",
    "ResetInstanceRequest",
    "ResetInstanceResponse",
    "RestoreVolumeSnapshotRequest",
    "SnapshotSchedulePolicy",
    "UpdateSnapshotSchedulePolicyRequest",
    "UpdateVolumeRequest",
    "VRF",
    "Volume",
    "VolumeSnapshot",
)
