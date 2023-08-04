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


from .services.net_app import NetAppAsyncClient, NetAppClient
from .types.active_directory import (
    ActiveDirectory,
    CreateActiveDirectoryRequest,
    DeleteActiveDirectoryRequest,
    GetActiveDirectoryRequest,
    ListActiveDirectoriesRequest,
    ListActiveDirectoriesResponse,
    UpdateActiveDirectoryRequest,
)
from .types.cloud_netapp_service import OperationMetadata
from .types.common import EncryptionType, ServiceLevel
from .types.kms import (
    CreateKmsConfigRequest,
    DeleteKmsConfigRequest,
    EncryptVolumesRequest,
    GetKmsConfigRequest,
    KmsConfig,
    ListKmsConfigsRequest,
    ListKmsConfigsResponse,
    UpdateKmsConfigRequest,
    VerifyKmsConfigRequest,
    VerifyKmsConfigResponse,
)
from .types.replication import (
    CreateReplicationRequest,
    DeleteReplicationRequest,
    DestinationVolumeParameters,
    GetReplicationRequest,
    ListReplicationsRequest,
    ListReplicationsResponse,
    Replication,
    ResumeReplicationRequest,
    ReverseReplicationDirectionRequest,
    StopReplicationRequest,
    TransferStats,
    UpdateReplicationRequest,
)
from .types.snapshot import (
    CreateSnapshotRequest,
    DeleteSnapshotRequest,
    GetSnapshotRequest,
    ListSnapshotsRequest,
    ListSnapshotsResponse,
    Snapshot,
    UpdateSnapshotRequest,
)
from .types.storage_pool import (
    CreateStoragePoolRequest,
    DeleteStoragePoolRequest,
    GetStoragePoolRequest,
    ListStoragePoolsRequest,
    ListStoragePoolsResponse,
    StoragePool,
    UpdateStoragePoolRequest,
)
from .types.volume import (
    AccessType,
    CreateVolumeRequest,
    DailySchedule,
    DeleteVolumeRequest,
    ExportPolicy,
    GetVolumeRequest,
    HourlySchedule,
    ListVolumesRequest,
    ListVolumesResponse,
    MonthlySchedule,
    MountOption,
    Protocols,
    RestoreParameters,
    RestrictedAction,
    RevertVolumeRequest,
    SecurityStyle,
    SimpleExportPolicyRule,
    SMBSettings,
    SnapshotPolicy,
    UpdateVolumeRequest,
    Volume,
    WeeklySchedule,
)

__all__ = (
    "NetAppAsyncClient",
    "AccessType",
    "ActiveDirectory",
    "CreateActiveDirectoryRequest",
    "CreateKmsConfigRequest",
    "CreateReplicationRequest",
    "CreateSnapshotRequest",
    "CreateStoragePoolRequest",
    "CreateVolumeRequest",
    "DailySchedule",
    "DeleteActiveDirectoryRequest",
    "DeleteKmsConfigRequest",
    "DeleteReplicationRequest",
    "DeleteSnapshotRequest",
    "DeleteStoragePoolRequest",
    "DeleteVolumeRequest",
    "DestinationVolumeParameters",
    "EncryptVolumesRequest",
    "EncryptionType",
    "ExportPolicy",
    "GetActiveDirectoryRequest",
    "GetKmsConfigRequest",
    "GetReplicationRequest",
    "GetSnapshotRequest",
    "GetStoragePoolRequest",
    "GetVolumeRequest",
    "HourlySchedule",
    "KmsConfig",
    "ListActiveDirectoriesRequest",
    "ListActiveDirectoriesResponse",
    "ListKmsConfigsRequest",
    "ListKmsConfigsResponse",
    "ListReplicationsRequest",
    "ListReplicationsResponse",
    "ListSnapshotsRequest",
    "ListSnapshotsResponse",
    "ListStoragePoolsRequest",
    "ListStoragePoolsResponse",
    "ListVolumesRequest",
    "ListVolumesResponse",
    "MonthlySchedule",
    "MountOption",
    "NetAppClient",
    "OperationMetadata",
    "Protocols",
    "Replication",
    "RestoreParameters",
    "RestrictedAction",
    "ResumeReplicationRequest",
    "ReverseReplicationDirectionRequest",
    "RevertVolumeRequest",
    "SMBSettings",
    "SecurityStyle",
    "ServiceLevel",
    "SimpleExportPolicyRule",
    "Snapshot",
    "SnapshotPolicy",
    "StopReplicationRequest",
    "StoragePool",
    "TransferStats",
    "UpdateActiveDirectoryRequest",
    "UpdateKmsConfigRequest",
    "UpdateReplicationRequest",
    "UpdateSnapshotRequest",
    "UpdateStoragePoolRequest",
    "UpdateVolumeRequest",
    "VerifyKmsConfigRequest",
    "VerifyKmsConfigResponse",
    "Volume",
    "WeeklySchedule",
)
