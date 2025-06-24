# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.gke_backup_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.backup_for_gke import BackupForGKEAsyncClient, BackupForGKEClient
from .types.backup import Backup
from .types.backup_channel import BackupChannel
from .types.backup_plan import BackupPlan, ExclusionWindow, RpoConfig
from .types.backup_plan_binding import BackupPlanBinding
from .types.common import (
    EncryptionKey,
    NamespacedName,
    NamespacedNames,
    Namespaces,
    VolumeTypeEnum,
)
from .types.gkebackup import (
    CreateBackupChannelRequest,
    CreateBackupPlanRequest,
    CreateBackupRequest,
    CreateRestoreChannelRequest,
    CreateRestorePlanRequest,
    CreateRestoreRequest,
    DeleteBackupChannelRequest,
    DeleteBackupPlanRequest,
    DeleteBackupRequest,
    DeleteRestoreChannelRequest,
    DeleteRestorePlanRequest,
    DeleteRestoreRequest,
    GetBackupChannelRequest,
    GetBackupIndexDownloadUrlRequest,
    GetBackupIndexDownloadUrlResponse,
    GetBackupPlanBindingRequest,
    GetBackupPlanRequest,
    GetBackupRequest,
    GetRestoreChannelRequest,
    GetRestorePlanBindingRequest,
    GetRestorePlanRequest,
    GetRestoreRequest,
    GetVolumeBackupRequest,
    GetVolumeRestoreRequest,
    ListBackupChannelsRequest,
    ListBackupChannelsResponse,
    ListBackupPlanBindingsRequest,
    ListBackupPlanBindingsResponse,
    ListBackupPlansRequest,
    ListBackupPlansResponse,
    ListBackupsRequest,
    ListBackupsResponse,
    ListRestoreChannelsRequest,
    ListRestoreChannelsResponse,
    ListRestorePlanBindingsRequest,
    ListRestorePlanBindingsResponse,
    ListRestorePlansRequest,
    ListRestorePlansResponse,
    ListRestoresRequest,
    ListRestoresResponse,
    ListVolumeBackupsRequest,
    ListVolumeBackupsResponse,
    ListVolumeRestoresRequest,
    ListVolumeRestoresResponse,
    OperationMetadata,
    UpdateBackupChannelRequest,
    UpdateBackupPlanRequest,
    UpdateBackupRequest,
    UpdateRestoreChannelRequest,
    UpdateRestorePlanRequest,
    UpdateRestoreRequest,
)
from .types.restore import (
    ResourceSelector,
    Restore,
    RestoreConfig,
    VolumeDataRestorePolicyOverride,
)
from .types.restore_channel import RestoreChannel
from .types.restore_plan import RestorePlan
from .types.restore_plan_binding import RestorePlanBinding
from .types.volume import VolumeBackup, VolumeRestore

__all__ = (
    "BackupForGKEAsyncClient",
    "Backup",
    "BackupChannel",
    "BackupForGKEClient",
    "BackupPlan",
    "BackupPlanBinding",
    "CreateBackupChannelRequest",
    "CreateBackupPlanRequest",
    "CreateBackupRequest",
    "CreateRestoreChannelRequest",
    "CreateRestorePlanRequest",
    "CreateRestoreRequest",
    "DeleteBackupChannelRequest",
    "DeleteBackupPlanRequest",
    "DeleteBackupRequest",
    "DeleteRestoreChannelRequest",
    "DeleteRestorePlanRequest",
    "DeleteRestoreRequest",
    "EncryptionKey",
    "ExclusionWindow",
    "GetBackupChannelRequest",
    "GetBackupIndexDownloadUrlRequest",
    "GetBackupIndexDownloadUrlResponse",
    "GetBackupPlanBindingRequest",
    "GetBackupPlanRequest",
    "GetBackupRequest",
    "GetRestoreChannelRequest",
    "GetRestorePlanBindingRequest",
    "GetRestorePlanRequest",
    "GetRestoreRequest",
    "GetVolumeBackupRequest",
    "GetVolumeRestoreRequest",
    "ListBackupChannelsRequest",
    "ListBackupChannelsResponse",
    "ListBackupPlanBindingsRequest",
    "ListBackupPlanBindingsResponse",
    "ListBackupPlansRequest",
    "ListBackupPlansResponse",
    "ListBackupsRequest",
    "ListBackupsResponse",
    "ListRestoreChannelsRequest",
    "ListRestoreChannelsResponse",
    "ListRestorePlanBindingsRequest",
    "ListRestorePlanBindingsResponse",
    "ListRestorePlansRequest",
    "ListRestorePlansResponse",
    "ListRestoresRequest",
    "ListRestoresResponse",
    "ListVolumeBackupsRequest",
    "ListVolumeBackupsResponse",
    "ListVolumeRestoresRequest",
    "ListVolumeRestoresResponse",
    "NamespacedName",
    "NamespacedNames",
    "Namespaces",
    "OperationMetadata",
    "ResourceSelector",
    "Restore",
    "RestoreChannel",
    "RestoreConfig",
    "RestorePlan",
    "RestorePlanBinding",
    "RpoConfig",
    "UpdateBackupChannelRequest",
    "UpdateBackupPlanRequest",
    "UpdateBackupRequest",
    "UpdateRestoreChannelRequest",
    "UpdateRestorePlanRequest",
    "UpdateRestoreRequest",
    "VolumeBackup",
    "VolumeDataRestorePolicyOverride",
    "VolumeRestore",
    "VolumeTypeEnum",
)
