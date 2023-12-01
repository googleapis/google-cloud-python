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
from google.cloud.netapp import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.netapp_v1.services.net_app.client import NetAppClient
from google.cloud.netapp_v1.services.net_app.async_client import NetAppAsyncClient

from google.cloud.netapp_v1.types.active_directory import ActiveDirectory
from google.cloud.netapp_v1.types.active_directory import CreateActiveDirectoryRequest
from google.cloud.netapp_v1.types.active_directory import DeleteActiveDirectoryRequest
from google.cloud.netapp_v1.types.active_directory import GetActiveDirectoryRequest
from google.cloud.netapp_v1.types.active_directory import ListActiveDirectoriesRequest
from google.cloud.netapp_v1.types.active_directory import ListActiveDirectoriesResponse
from google.cloud.netapp_v1.types.active_directory import UpdateActiveDirectoryRequest
from google.cloud.netapp_v1.types.cloud_netapp_service import OperationMetadata
from google.cloud.netapp_v1.types.common import EncryptionType
from google.cloud.netapp_v1.types.common import ServiceLevel
from google.cloud.netapp_v1.types.kms import CreateKmsConfigRequest
from google.cloud.netapp_v1.types.kms import DeleteKmsConfigRequest
from google.cloud.netapp_v1.types.kms import EncryptVolumesRequest
from google.cloud.netapp_v1.types.kms import GetKmsConfigRequest
from google.cloud.netapp_v1.types.kms import KmsConfig
from google.cloud.netapp_v1.types.kms import ListKmsConfigsRequest
from google.cloud.netapp_v1.types.kms import ListKmsConfigsResponse
from google.cloud.netapp_v1.types.kms import UpdateKmsConfigRequest
from google.cloud.netapp_v1.types.kms import VerifyKmsConfigRequest
from google.cloud.netapp_v1.types.kms import VerifyKmsConfigResponse
from google.cloud.netapp_v1.types.replication import CreateReplicationRequest
from google.cloud.netapp_v1.types.replication import DeleteReplicationRequest
from google.cloud.netapp_v1.types.replication import DestinationVolumeParameters
from google.cloud.netapp_v1.types.replication import GetReplicationRequest
from google.cloud.netapp_v1.types.replication import ListReplicationsRequest
from google.cloud.netapp_v1.types.replication import ListReplicationsResponse
from google.cloud.netapp_v1.types.replication import Replication
from google.cloud.netapp_v1.types.replication import ResumeReplicationRequest
from google.cloud.netapp_v1.types.replication import ReverseReplicationDirectionRequest
from google.cloud.netapp_v1.types.replication import StopReplicationRequest
from google.cloud.netapp_v1.types.replication import TransferStats
from google.cloud.netapp_v1.types.replication import UpdateReplicationRequest
from google.cloud.netapp_v1.types.snapshot import CreateSnapshotRequest
from google.cloud.netapp_v1.types.snapshot import DeleteSnapshotRequest
from google.cloud.netapp_v1.types.snapshot import GetSnapshotRequest
from google.cloud.netapp_v1.types.snapshot import ListSnapshotsRequest
from google.cloud.netapp_v1.types.snapshot import ListSnapshotsResponse
from google.cloud.netapp_v1.types.snapshot import Snapshot
from google.cloud.netapp_v1.types.snapshot import UpdateSnapshotRequest
from google.cloud.netapp_v1.types.storage_pool import CreateStoragePoolRequest
from google.cloud.netapp_v1.types.storage_pool import DeleteStoragePoolRequest
from google.cloud.netapp_v1.types.storage_pool import GetStoragePoolRequest
from google.cloud.netapp_v1.types.storage_pool import ListStoragePoolsRequest
from google.cloud.netapp_v1.types.storage_pool import ListStoragePoolsResponse
from google.cloud.netapp_v1.types.storage_pool import StoragePool
from google.cloud.netapp_v1.types.storage_pool import UpdateStoragePoolRequest
from google.cloud.netapp_v1.types.volume import CreateVolumeRequest
from google.cloud.netapp_v1.types.volume import DailySchedule
from google.cloud.netapp_v1.types.volume import DeleteVolumeRequest
from google.cloud.netapp_v1.types.volume import ExportPolicy
from google.cloud.netapp_v1.types.volume import GetVolumeRequest
from google.cloud.netapp_v1.types.volume import HourlySchedule
from google.cloud.netapp_v1.types.volume import ListVolumesRequest
from google.cloud.netapp_v1.types.volume import ListVolumesResponse
from google.cloud.netapp_v1.types.volume import MonthlySchedule
from google.cloud.netapp_v1.types.volume import MountOption
from google.cloud.netapp_v1.types.volume import RestoreParameters
from google.cloud.netapp_v1.types.volume import RevertVolumeRequest
from google.cloud.netapp_v1.types.volume import SimpleExportPolicyRule
from google.cloud.netapp_v1.types.volume import SnapshotPolicy
from google.cloud.netapp_v1.types.volume import UpdateVolumeRequest
from google.cloud.netapp_v1.types.volume import Volume
from google.cloud.netapp_v1.types.volume import WeeklySchedule
from google.cloud.netapp_v1.types.volume import AccessType
from google.cloud.netapp_v1.types.volume import Protocols
from google.cloud.netapp_v1.types.volume import RestrictedAction
from google.cloud.netapp_v1.types.volume import SecurityStyle
from google.cloud.netapp_v1.types.volume import SMBSettings

__all__ = ('NetAppClient',
    'NetAppAsyncClient',
    'ActiveDirectory',
    'CreateActiveDirectoryRequest',
    'DeleteActiveDirectoryRequest',
    'GetActiveDirectoryRequest',
    'ListActiveDirectoriesRequest',
    'ListActiveDirectoriesResponse',
    'UpdateActiveDirectoryRequest',
    'OperationMetadata',
    'EncryptionType',
    'ServiceLevel',
    'CreateKmsConfigRequest',
    'DeleteKmsConfigRequest',
    'EncryptVolumesRequest',
    'GetKmsConfigRequest',
    'KmsConfig',
    'ListKmsConfigsRequest',
    'ListKmsConfigsResponse',
    'UpdateKmsConfigRequest',
    'VerifyKmsConfigRequest',
    'VerifyKmsConfigResponse',
    'CreateReplicationRequest',
    'DeleteReplicationRequest',
    'DestinationVolumeParameters',
    'GetReplicationRequest',
    'ListReplicationsRequest',
    'ListReplicationsResponse',
    'Replication',
    'ResumeReplicationRequest',
    'ReverseReplicationDirectionRequest',
    'StopReplicationRequest',
    'TransferStats',
    'UpdateReplicationRequest',
    'CreateSnapshotRequest',
    'DeleteSnapshotRequest',
    'GetSnapshotRequest',
    'ListSnapshotsRequest',
    'ListSnapshotsResponse',
    'Snapshot',
    'UpdateSnapshotRequest',
    'CreateStoragePoolRequest',
    'DeleteStoragePoolRequest',
    'GetStoragePoolRequest',
    'ListStoragePoolsRequest',
    'ListStoragePoolsResponse',
    'StoragePool',
    'UpdateStoragePoolRequest',
    'CreateVolumeRequest',
    'DailySchedule',
    'DeleteVolumeRequest',
    'ExportPolicy',
    'GetVolumeRequest',
    'HourlySchedule',
    'ListVolumesRequest',
    'ListVolumesResponse',
    'MonthlySchedule',
    'MountOption',
    'RestoreParameters',
    'RevertVolumeRequest',
    'SimpleExportPolicyRule',
    'SnapshotPolicy',
    'UpdateVolumeRequest',
    'Volume',
    'WeeklySchedule',
    'AccessType',
    'Protocols',
    'RestrictedAction',
    'SecurityStyle',
    'SMBSettings',
)
