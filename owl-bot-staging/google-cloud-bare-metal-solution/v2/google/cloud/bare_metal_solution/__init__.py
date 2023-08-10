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


from google.cloud.bare_metal_solution_v2.services.bare_metal_solution.client import BareMetalSolutionClient
from google.cloud.bare_metal_solution_v2.services.bare_metal_solution.async_client import BareMetalSolutionAsyncClient

from google.cloud.bare_metal_solution_v2.types.common import OperationMetadata
from google.cloud.bare_metal_solution_v2.types.common import VolumePerformanceTier
from google.cloud.bare_metal_solution_v2.types.common import WorkloadProfile
from google.cloud.bare_metal_solution_v2.types.instance import DetachLunRequest
from google.cloud.bare_metal_solution_v2.types.instance import DisableInteractiveSerialConsoleRequest
from google.cloud.bare_metal_solution_v2.types.instance import DisableInteractiveSerialConsoleResponse
from google.cloud.bare_metal_solution_v2.types.instance import EnableInteractiveSerialConsoleRequest
from google.cloud.bare_metal_solution_v2.types.instance import EnableInteractiveSerialConsoleResponse
from google.cloud.bare_metal_solution_v2.types.instance import GetInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import Instance
from google.cloud.bare_metal_solution_v2.types.instance import ListInstancesRequest
from google.cloud.bare_metal_solution_v2.types.instance import ListInstancesResponse
from google.cloud.bare_metal_solution_v2.types.instance import RenameInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import ResetInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import ResetInstanceResponse
from google.cloud.bare_metal_solution_v2.types.instance import StartInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import StartInstanceResponse
from google.cloud.bare_metal_solution_v2.types.instance import StopInstanceRequest
from google.cloud.bare_metal_solution_v2.types.instance import StopInstanceResponse
from google.cloud.bare_metal_solution_v2.types.instance import UpdateInstanceRequest
from google.cloud.bare_metal_solution_v2.types.lun import EvictLunRequest
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
from google.cloud.bare_metal_solution_v2.types.network import NetworkMountPoint
from google.cloud.bare_metal_solution_v2.types.network import NetworkUsage
from google.cloud.bare_metal_solution_v2.types.network import RenameNetworkRequest
from google.cloud.bare_metal_solution_v2.types.network import UpdateNetworkRequest
from google.cloud.bare_metal_solution_v2.types.network import VRF
from google.cloud.bare_metal_solution_v2.types.nfs_share import CreateNfsShareRequest
from google.cloud.bare_metal_solution_v2.types.nfs_share import DeleteNfsShareRequest
from google.cloud.bare_metal_solution_v2.types.nfs_share import GetNfsShareRequest
from google.cloud.bare_metal_solution_v2.types.nfs_share import ListNfsSharesRequest
from google.cloud.bare_metal_solution_v2.types.nfs_share import ListNfsSharesResponse
from google.cloud.bare_metal_solution_v2.types.nfs_share import NfsShare
from google.cloud.bare_metal_solution_v2.types.nfs_share import RenameNfsShareRequest
from google.cloud.bare_metal_solution_v2.types.nfs_share import UpdateNfsShareRequest
from google.cloud.bare_metal_solution_v2.types.osimage import ListOSImagesRequest
from google.cloud.bare_metal_solution_v2.types.osimage import ListOSImagesResponse
from google.cloud.bare_metal_solution_v2.types.osimage import OSImage
from google.cloud.bare_metal_solution_v2.types.provisioning import CreateProvisioningConfigRequest
from google.cloud.bare_metal_solution_v2.types.provisioning import GetProvisioningConfigRequest
from google.cloud.bare_metal_solution_v2.types.provisioning import InstanceConfig
from google.cloud.bare_metal_solution_v2.types.provisioning import InstanceQuota
from google.cloud.bare_metal_solution_v2.types.provisioning import ListProvisioningQuotasRequest
from google.cloud.bare_metal_solution_v2.types.provisioning import ListProvisioningQuotasResponse
from google.cloud.bare_metal_solution_v2.types.provisioning import NetworkConfig
from google.cloud.bare_metal_solution_v2.types.provisioning import ProvisioningConfig
from google.cloud.bare_metal_solution_v2.types.provisioning import ProvisioningQuota
from google.cloud.bare_metal_solution_v2.types.provisioning import ServerNetworkTemplate
from google.cloud.bare_metal_solution_v2.types.provisioning import SubmitProvisioningConfigRequest
from google.cloud.bare_metal_solution_v2.types.provisioning import SubmitProvisioningConfigResponse
from google.cloud.bare_metal_solution_v2.types.provisioning import UpdateProvisioningConfigRequest
from google.cloud.bare_metal_solution_v2.types.provisioning import VolumeConfig
from google.cloud.bare_metal_solution_v2.types.ssh_key import CreateSSHKeyRequest
from google.cloud.bare_metal_solution_v2.types.ssh_key import DeleteSSHKeyRequest
from google.cloud.bare_metal_solution_v2.types.ssh_key import ListSSHKeysRequest
from google.cloud.bare_metal_solution_v2.types.ssh_key import ListSSHKeysResponse
from google.cloud.bare_metal_solution_v2.types.ssh_key import SSHKey
from google.cloud.bare_metal_solution_v2.types.volume import EvictVolumeRequest
from google.cloud.bare_metal_solution_v2.types.volume import GetVolumeRequest
from google.cloud.bare_metal_solution_v2.types.volume import ListVolumesRequest
from google.cloud.bare_metal_solution_v2.types.volume import ListVolumesResponse
from google.cloud.bare_metal_solution_v2.types.volume import RenameVolumeRequest
from google.cloud.bare_metal_solution_v2.types.volume import ResizeVolumeRequest
from google.cloud.bare_metal_solution_v2.types.volume import UpdateVolumeRequest
from google.cloud.bare_metal_solution_v2.types.volume import Volume
from google.cloud.bare_metal_solution_v2.types.volume_snapshot import CreateVolumeSnapshotRequest
from google.cloud.bare_metal_solution_v2.types.volume_snapshot import DeleteVolumeSnapshotRequest
from google.cloud.bare_metal_solution_v2.types.volume_snapshot import GetVolumeSnapshotRequest
from google.cloud.bare_metal_solution_v2.types.volume_snapshot import ListVolumeSnapshotsRequest
from google.cloud.bare_metal_solution_v2.types.volume_snapshot import ListVolumeSnapshotsResponse
from google.cloud.bare_metal_solution_v2.types.volume_snapshot import RestoreVolumeSnapshotRequest
from google.cloud.bare_metal_solution_v2.types.volume_snapshot import VolumeSnapshot

__all__ = ('BareMetalSolutionClient',
    'BareMetalSolutionAsyncClient',
    'OperationMetadata',
    'VolumePerformanceTier',
    'WorkloadProfile',
    'DetachLunRequest',
    'DisableInteractiveSerialConsoleRequest',
    'DisableInteractiveSerialConsoleResponse',
    'EnableInteractiveSerialConsoleRequest',
    'EnableInteractiveSerialConsoleResponse',
    'GetInstanceRequest',
    'Instance',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'RenameInstanceRequest',
    'ResetInstanceRequest',
    'ResetInstanceResponse',
    'StartInstanceRequest',
    'StartInstanceResponse',
    'StopInstanceRequest',
    'StopInstanceResponse',
    'UpdateInstanceRequest',
    'EvictLunRequest',
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
    'NetworkMountPoint',
    'NetworkUsage',
    'RenameNetworkRequest',
    'UpdateNetworkRequest',
    'VRF',
    'CreateNfsShareRequest',
    'DeleteNfsShareRequest',
    'GetNfsShareRequest',
    'ListNfsSharesRequest',
    'ListNfsSharesResponse',
    'NfsShare',
    'RenameNfsShareRequest',
    'UpdateNfsShareRequest',
    'ListOSImagesRequest',
    'ListOSImagesResponse',
    'OSImage',
    'CreateProvisioningConfigRequest',
    'GetProvisioningConfigRequest',
    'InstanceConfig',
    'InstanceQuota',
    'ListProvisioningQuotasRequest',
    'ListProvisioningQuotasResponse',
    'NetworkConfig',
    'ProvisioningConfig',
    'ProvisioningQuota',
    'ServerNetworkTemplate',
    'SubmitProvisioningConfigRequest',
    'SubmitProvisioningConfigResponse',
    'UpdateProvisioningConfigRequest',
    'VolumeConfig',
    'CreateSSHKeyRequest',
    'DeleteSSHKeyRequest',
    'ListSSHKeysRequest',
    'ListSSHKeysResponse',
    'SSHKey',
    'EvictVolumeRequest',
    'GetVolumeRequest',
    'ListVolumesRequest',
    'ListVolumesResponse',
    'RenameVolumeRequest',
    'ResizeVolumeRequest',
    'UpdateVolumeRequest',
    'Volume',
    'CreateVolumeSnapshotRequest',
    'DeleteVolumeSnapshotRequest',
    'GetVolumeSnapshotRequest',
    'ListVolumeSnapshotsRequest',
    'ListVolumeSnapshotsResponse',
    'RestoreVolumeSnapshotRequest',
    'VolumeSnapshot',
)
