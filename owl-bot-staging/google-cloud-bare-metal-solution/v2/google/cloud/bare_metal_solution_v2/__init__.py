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


from .services.bare_metal_solution import BareMetalSolutionClient
from .services.bare_metal_solution import BareMetalSolutionAsyncClient

from .types.baremetalsolution import OperationMetadata
from .types.baremetalsolution import ResetInstanceResponse
from .types.common import VolumePerformanceTier
from .types.common import WorkloadProfile
from .types.instance import DetachLunRequest
from .types.instance import DisableInteractiveSerialConsoleRequest
from .types.instance import DisableInteractiveSerialConsoleResponse
from .types.instance import EnableInteractiveSerialConsoleRequest
from .types.instance import EnableInteractiveSerialConsoleResponse
from .types.instance import GetInstanceRequest
from .types.instance import Instance
from .types.instance import ListInstancesRequest
from .types.instance import ListInstancesResponse
from .types.instance import RenameInstanceRequest
from .types.instance import ResetInstanceRequest
from .types.instance import ServerNetworkTemplate
from .types.instance import StartInstanceRequest
from .types.instance import StartInstanceResponse
from .types.instance import StopInstanceRequest
from .types.instance import StopInstanceResponse
from .types.instance import UpdateInstanceRequest
from .types.lun import EvictLunRequest
from .types.lun import GetLunRequest
from .types.lun import ListLunsRequest
from .types.lun import ListLunsResponse
from .types.lun import Lun
from .types.network import GetNetworkRequest
from .types.network import ListNetworksRequest
from .types.network import ListNetworksResponse
from .types.network import ListNetworkUsageRequest
from .types.network import ListNetworkUsageResponse
from .types.network import LogicalInterface
from .types.network import Network
from .types.network import NetworkAddressReservation
from .types.network import NetworkMountPoint
from .types.network import NetworkUsage
from .types.network import RenameNetworkRequest
from .types.network import UpdateNetworkRequest
from .types.network import VRF
from .types.nfs_share import CreateNfsShareRequest
from .types.nfs_share import DeleteNfsShareRequest
from .types.nfs_share import GetNfsShareRequest
from .types.nfs_share import ListNfsSharesRequest
from .types.nfs_share import ListNfsSharesResponse
from .types.nfs_share import NfsShare
from .types.nfs_share import RenameNfsShareRequest
from .types.nfs_share import UpdateNfsShareRequest
from .types.osimage import ListOSImagesRequest
from .types.osimage import ListOSImagesResponse
from .types.osimage import OSImage
from .types.provisioning import CreateProvisioningConfigRequest
from .types.provisioning import GetProvisioningConfigRequest
from .types.provisioning import InstanceConfig
from .types.provisioning import InstanceQuota
from .types.provisioning import ListProvisioningQuotasRequest
from .types.provisioning import ListProvisioningQuotasResponse
from .types.provisioning import NetworkConfig
from .types.provisioning import ProvisioningConfig
from .types.provisioning import ProvisioningQuota
from .types.provisioning import SubmitProvisioningConfigRequest
from .types.provisioning import SubmitProvisioningConfigResponse
from .types.provisioning import UpdateProvisioningConfigRequest
from .types.provisioning import VolumeConfig
from .types.ssh_key import CreateSSHKeyRequest
from .types.ssh_key import DeleteSSHKeyRequest
from .types.ssh_key import ListSSHKeysRequest
from .types.ssh_key import ListSSHKeysResponse
from .types.ssh_key import SSHKey
from .types.volume import EvictVolumeRequest
from .types.volume import GetVolumeRequest
from .types.volume import ListVolumesRequest
from .types.volume import ListVolumesResponse
from .types.volume import RenameVolumeRequest
from .types.volume import ResizeVolumeRequest
from .types.volume import UpdateVolumeRequest
from .types.volume import Volume
from .types.volume_snapshot import CreateVolumeSnapshotRequest
from .types.volume_snapshot import DeleteVolumeSnapshotRequest
from .types.volume_snapshot import GetVolumeSnapshotRequest
from .types.volume_snapshot import ListVolumeSnapshotsRequest
from .types.volume_snapshot import ListVolumeSnapshotsResponse
from .types.volume_snapshot import RestoreVolumeSnapshotRequest
from .types.volume_snapshot import VolumeSnapshot

__all__ = (
    'BareMetalSolutionAsyncClient',
'BareMetalSolutionClient',
'CreateNfsShareRequest',
'CreateProvisioningConfigRequest',
'CreateSSHKeyRequest',
'CreateVolumeSnapshotRequest',
'DeleteNfsShareRequest',
'DeleteSSHKeyRequest',
'DeleteVolumeSnapshotRequest',
'DetachLunRequest',
'DisableInteractiveSerialConsoleRequest',
'DisableInteractiveSerialConsoleResponse',
'EnableInteractiveSerialConsoleRequest',
'EnableInteractiveSerialConsoleResponse',
'EvictLunRequest',
'EvictVolumeRequest',
'GetInstanceRequest',
'GetLunRequest',
'GetNetworkRequest',
'GetNfsShareRequest',
'GetProvisioningConfigRequest',
'GetVolumeRequest',
'GetVolumeSnapshotRequest',
'Instance',
'InstanceConfig',
'InstanceQuota',
'ListInstancesRequest',
'ListInstancesResponse',
'ListLunsRequest',
'ListLunsResponse',
'ListNetworkUsageRequest',
'ListNetworkUsageResponse',
'ListNetworksRequest',
'ListNetworksResponse',
'ListNfsSharesRequest',
'ListNfsSharesResponse',
'ListOSImagesRequest',
'ListOSImagesResponse',
'ListProvisioningQuotasRequest',
'ListProvisioningQuotasResponse',
'ListSSHKeysRequest',
'ListSSHKeysResponse',
'ListVolumeSnapshotsRequest',
'ListVolumeSnapshotsResponse',
'ListVolumesRequest',
'ListVolumesResponse',
'LogicalInterface',
'Lun',
'Network',
'NetworkAddressReservation',
'NetworkConfig',
'NetworkMountPoint',
'NetworkUsage',
'NfsShare',
'OSImage',
'OperationMetadata',
'ProvisioningConfig',
'ProvisioningQuota',
'RenameInstanceRequest',
'RenameNetworkRequest',
'RenameNfsShareRequest',
'RenameVolumeRequest',
'ResetInstanceRequest',
'ResetInstanceResponse',
'ResizeVolumeRequest',
'RestoreVolumeSnapshotRequest',
'SSHKey',
'ServerNetworkTemplate',
'StartInstanceRequest',
'StartInstanceResponse',
'StopInstanceRequest',
'StopInstanceResponse',
'SubmitProvisioningConfigRequest',
'SubmitProvisioningConfigResponse',
'UpdateInstanceRequest',
'UpdateNetworkRequest',
'UpdateNfsShareRequest',
'UpdateProvisioningConfigRequest',
'UpdateVolumeRequest',
'VRF',
'Volume',
'VolumeConfig',
'VolumePerformanceTier',
'VolumeSnapshot',
'WorkloadProfile',
)
