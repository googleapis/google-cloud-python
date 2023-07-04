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
from google.cloud.bare_metal_solution import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bare_metal_solution_v2.services.bare_metal_solution.client import BareMetalSolutionClient
from google.cloud.bare_metal_solution_v2.services.bare_metal_solution.async_client import BareMetalSolutionAsyncClient

from google.cloud.bare_metal_solution_v2.types.baremetalsolution import OperationMetadata
from google.cloud.bare_metal_solution_v2.types.baremetalsolution import ResetInstanceResponse
from google.cloud.bare_metal_solution_v2.types.instance import DetachLunRequest
from google.cloud.bare_metal_solution_v2.types.instance import GetInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import Instance
from google.cloud.bare_metal_solution_v2.types.instance import ListInstancesRequest
from google.cloud.bare_metal_solution_v2.types.instance import ListInstancesResponse
from google.cloud.bare_metal_solution_v2.types.instance import ResetInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import ServerNetworkTemplate
from google.cloud.bare_metal_solution_v2.types.instance import StartInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import StartInstanceResponse
from google.cloud.bare_metal_solution_v2.types.instance import StopInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import StopInstanceResponse
from google.cloud.bare_metal_solution_v2.types.instance import UpdateInstanceRequest
from google.cloud.bare_metal_solution_v2.types.lun import GetLunRequest
from google.cloud.bare_metal_solution_v2.types.lun import ListLunsRequest
from google.cloud.bare_metal_solution_v2.types.lun import ListLunsResponse
from google.cloud.bare_metal_solution_v2.types.lun import Lun
from google.cloud.bare_metal_solution_v2.types.network import GetNetworkRequest
from google.cloud.bare_metal_solution_v2.types.network import ListNetworksRequest
from google.cloud.bare_metal_solution_v2.types.network import ListNetworksResponse
from google.cloud.bare_metal_solution_v2.types.network import ListNetworkUsageRequest
from google.cloud.bare_metal_solution_v2.types.network import ListNetworkUsageResponse
from google.cloud.bare_metal_solution_v2.types.network import LogicalInterface
from google.cloud.bare_metal_solution_v2.types.network import Network
from google.cloud.bare_metal_solution_v2.types.network import NetworkAddressReservation
from google.cloud.bare_metal_solution_v2.types.network import NetworkUsage
from google.cloud.bare_metal_solution_v2.types.network import UpdateNetworkRequest
from google.cloud.bare_metal_solution_v2.types.network import VRF
from google.cloud.bare_metal_solution_v2.types.nfs_share import GetNfsShareRequest
from google.cloud.bare_metal_solution_v2.types.nfs_share import ListNfsSharesRequest
from google.cloud.bare_metal_solution_v2.types.nfs_share import ListNfsSharesResponse
from google.cloud.bare_metal_solution_v2.types.nfs_share import NfsShare
from google.cloud.bare_metal_solution_v2.types.nfs_share import UpdateNfsShareRequest
from google.cloud.bare_metal_solution_v2.types.volume import GetVolumeRequest
from google.cloud.bare_metal_solution_v2.types.volume import ListVolumesRequest
from google.cloud.bare_metal_solution_v2.types.volume import ListVolumesResponse
from google.cloud.bare_metal_solution_v2.types.volume import ResizeVolumeRequest
from google.cloud.bare_metal_solution_v2.types.volume import UpdateVolumeRequest
from google.cloud.bare_metal_solution_v2.types.volume import Volume

__all__ = ('BareMetalSolutionClient',
    'BareMetalSolutionAsyncClient',
    'OperationMetadata',
    'ResetInstanceResponse',
    'DetachLunRequest',
    'GetInstanceRequest',
    'Instance',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'ResetInstanceRequest',
    'ServerNetworkTemplate',
    'StartInstanceRequest',
    'StartInstanceResponse',
    'StopInstanceRequest',
    'StopInstanceResponse',
    'UpdateInstanceRequest',
    'GetLunRequest',
    'ListLunsRequest',
    'ListLunsResponse',
    'Lun',
    'GetNetworkRequest',
    'ListNetworksRequest',
    'ListNetworksResponse',
    'ListNetworkUsageRequest',
    'ListNetworkUsageResponse',
    'LogicalInterface',
    'Network',
    'NetworkAddressReservation',
    'NetworkUsage',
    'UpdateNetworkRequest',
    'VRF',
    'GetNfsShareRequest',
    'ListNfsSharesRequest',
    'ListNfsSharesResponse',
    'NfsShare',
    'UpdateNfsShareRequest',
    'GetVolumeRequest',
    'ListVolumesRequest',
    'ListVolumesResponse',
    'ResizeVolumeRequest',
    'UpdateVolumeRequest',
    'Volume',
)
