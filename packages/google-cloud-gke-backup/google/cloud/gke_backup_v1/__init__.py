# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from .types.backup_plan import BackupPlan, ExclusionWindow, RpoConfig
from .types.common import (
    EncryptionKey,
    NamespacedName,
    NamespacedNames,
    Namespaces,
    VolumeTypeEnum,
)
from .types.gkebackup import (
    CreateBackupPlanRequest,
    CreateBackupRequest,
    CreateRestorePlanRequest,
    CreateRestoreRequest,
    DeleteBackupPlanRequest,
    DeleteBackupRequest,
    DeleteRestorePlanRequest,
    DeleteRestoreRequest,
    GetBackupIndexDownloadUrlRequest,
    GetBackupIndexDownloadUrlResponse,
    GetBackupPlanRequest,
    GetBackupRequest,
    GetRestorePlanRequest,
    GetRestoreRequest,
    GetVolumeBackupRequest,
    GetVolumeRestoreRequest,
    ListBackupPlansRequest,
    ListBackupPlansResponse,
    ListBackupsRequest,
    ListBackupsResponse,
    ListRestorePlansRequest,
    ListRestorePlansResponse,
    ListRestoresRequest,
    ListRestoresResponse,
    ListVolumeBackupsRequest,
    ListVolumeBackupsResponse,
    ListVolumeRestoresRequest,
    ListVolumeRestoresResponse,
    OperationMetadata,
    UpdateBackupPlanRequest,
    UpdateBackupRequest,
    UpdateRestorePlanRequest,
    UpdateRestoreRequest,
)
from .types.restore import (
    ResourceSelector,
    Restore,
    RestoreConfig,
    VolumeDataRestorePolicyOverride,
)
from .types.restore_plan import RestorePlan
from .types.volume import VolumeBackup, VolumeRestore

__all__ = (
    "BackupForGKEAsyncClient",
    "Backup",
    "BackupForGKEClient",
    "BackupPlan",
    "CreateBackupPlanRequest",
    "CreateBackupRequest",
    "CreateRestorePlanRequest",
    "CreateRestoreRequest",
    "DeleteBackupPlanRequest",
    "DeleteBackupRequest",
    "DeleteRestorePlanRequest",
    "DeleteRestoreRequest",
    "EncryptionKey",
    "ExclusionWindow",
    "GetBackupIndexDownloadUrlRequest",
    "GetBackupIndexDownloadUrlResponse",
    "GetBackupPlanRequest",
    "GetBackupRequest",
    "GetRestorePlanRequest",
    "GetRestoreRequest",
    "GetVolumeBackupRequest",
    "GetVolumeRestoreRequest",
    "ListBackupPlansRequest",
    "ListBackupPlansResponse",
    "ListBackupsRequest",
    "ListBackupsResponse",
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
    "RestoreConfig",
    "RestorePlan",
    "RpoConfig",
    "UpdateBackupPlanRequest",
    "UpdateBackupRequest",
    "UpdateRestorePlanRequest",
    "UpdateRestoreRequest",
    "VolumeBackup",
    "VolumeDataRestorePolicyOverride",
    "VolumeRestore",
    "VolumeTypeEnum",
)
