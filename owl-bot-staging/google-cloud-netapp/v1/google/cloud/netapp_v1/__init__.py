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
from google.cloud.netapp_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.net_app import NetAppClient
from .services.net_app import NetAppAsyncClient

from .types.active_directory import ActiveDirectory
from .types.active_directory import CreateActiveDirectoryRequest
from .types.active_directory import DeleteActiveDirectoryRequest
from .types.active_directory import GetActiveDirectoryRequest
from .types.active_directory import ListActiveDirectoriesRequest
from .types.active_directory import ListActiveDirectoriesResponse
from .types.active_directory import UpdateActiveDirectoryRequest
from .types.cloud_netapp_service import OperationMetadata
from .types.common import EncryptionType
from .types.common import ServiceLevel
from .types.kms import CreateKmsConfigRequest
from .types.kms import DeleteKmsConfigRequest
from .types.kms import EncryptVolumesRequest
from .types.kms import GetKmsConfigRequest
from .types.kms import KmsConfig
from .types.kms import ListKmsConfigsRequest
from .types.kms import ListKmsConfigsResponse
from .types.kms import UpdateKmsConfigRequest
from .types.kms import VerifyKmsConfigRequest
from .types.kms import VerifyKmsConfigResponse
from .types.replication import CreateReplicationRequest
from .types.replication import DeleteReplicationRequest
from .types.replication import DestinationVolumeParameters
from .types.replication import GetReplicationRequest
from .types.replication import ListReplicationsRequest
from .types.replication import ListReplicationsResponse
from .types.replication import Replication
from .types.replication import ResumeReplicationRequest
from .types.replication import ReverseReplicationDirectionRequest
from .types.replication import StopReplicationRequest
from .types.replication import TransferStats
from .types.replication import UpdateReplicationRequest
from .types.snapshot import CreateSnapshotRequest
from .types.snapshot import DeleteSnapshotRequest
from .types.snapshot import GetSnapshotRequest
from .types.snapshot import ListSnapshotsRequest
from .types.snapshot import ListSnapshotsResponse
from .types.snapshot import Snapshot
from .types.snapshot import UpdateSnapshotRequest
from .types.storage_pool import CreateStoragePoolRequest
from .types.storage_pool import DeleteStoragePoolRequest
from .types.storage_pool import GetStoragePoolRequest
from .types.storage_pool import ListStoragePoolsRequest
from .types.storage_pool import ListStoragePoolsResponse
from .types.storage_pool import StoragePool
from .types.storage_pool import UpdateStoragePoolRequest
from .types.volume import CreateVolumeRequest
from .types.volume import DailySchedule
from .types.volume import DeleteVolumeRequest
from .types.volume import ExportPolicy
from .types.volume import GetVolumeRequest
from .types.volume import HourlySchedule
from .types.volume import ListVolumesRequest
from .types.volume import ListVolumesResponse
from .types.volume import MonthlySchedule
from .types.volume import MountOption
from .types.volume import RestoreParameters
from .types.volume import RevertVolumeRequest
from .types.volume import SimpleExportPolicyRule
from .types.volume import SnapshotPolicy
from .types.volume import UpdateVolumeRequest
from .types.volume import Volume
from .types.volume import WeeklySchedule
from .types.volume import AccessType
from .types.volume import Protocols
from .types.volume import RestrictedAction
from .types.volume import SecurityStyle
from .types.volume import SMBSettings

__all__ = (
    'NetAppAsyncClient',
'AccessType',
'ActiveDirectory',
'CreateActiveDirectoryRequest',
'CreateKmsConfigRequest',
'CreateReplicationRequest',
'CreateSnapshotRequest',
'CreateStoragePoolRequest',
'CreateVolumeRequest',
'DailySchedule',
'DeleteActiveDirectoryRequest',
'DeleteKmsConfigRequest',
'DeleteReplicationRequest',
'DeleteSnapshotRequest',
'DeleteStoragePoolRequest',
'DeleteVolumeRequest',
'DestinationVolumeParameters',
'EncryptVolumesRequest',
'EncryptionType',
'ExportPolicy',
'GetActiveDirectoryRequest',
'GetKmsConfigRequest',
'GetReplicationRequest',
'GetSnapshotRequest',
'GetStoragePoolRequest',
'GetVolumeRequest',
'HourlySchedule',
'KmsConfig',
'ListActiveDirectoriesRequest',
'ListActiveDirectoriesResponse',
'ListKmsConfigsRequest',
'ListKmsConfigsResponse',
'ListReplicationsRequest',
'ListReplicationsResponse',
'ListSnapshotsRequest',
'ListSnapshotsResponse',
'ListStoragePoolsRequest',
'ListStoragePoolsResponse',
'ListVolumesRequest',
'ListVolumesResponse',
'MonthlySchedule',
'MountOption',
'NetAppClient',
'OperationMetadata',
'Protocols',
'Replication',
'RestoreParameters',
'RestrictedAction',
'ResumeReplicationRequest',
'ReverseReplicationDirectionRequest',
'RevertVolumeRequest',
'SMBSettings',
'SecurityStyle',
'ServiceLevel',
'SimpleExportPolicyRule',
'Snapshot',
'SnapshotPolicy',
'StopReplicationRequest',
'StoragePool',
'TransferStats',
'UpdateActiveDirectoryRequest',
'UpdateKmsConfigRequest',
'UpdateReplicationRequest',
'UpdateSnapshotRequest',
'UpdateStoragePoolRequest',
'UpdateVolumeRequest',
'VerifyKmsConfigRequest',
'VerifyKmsConfigResponse',
'Volume',
'WeeklySchedule',
)
