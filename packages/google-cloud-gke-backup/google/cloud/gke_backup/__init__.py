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
from google.cloud.gke_backup import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.gke_backup_v1.services.backup_for_gke.async_client import (
    BackupForGKEAsyncClient,
)
from google.cloud.gke_backup_v1.services.backup_for_gke.client import BackupForGKEClient
from google.cloud.gke_backup_v1.types.backup import Backup
from google.cloud.gke_backup_v1.types.backup_plan import BackupPlan
from google.cloud.gke_backup_v1.types.common import (
    EncryptionKey,
    NamespacedName,
    NamespacedNames,
    Namespaces,
)
from google.cloud.gke_backup_v1.types.gkebackup import (
    CreateBackupPlanRequest,
    CreateBackupRequest,
    CreateRestorePlanRequest,
    CreateRestoreRequest,
    DeleteBackupPlanRequest,
    DeleteBackupRequest,
    DeleteRestorePlanRequest,
    DeleteRestoreRequest,
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
from google.cloud.gke_backup_v1.types.restore import Restore, RestoreConfig
from google.cloud.gke_backup_v1.types.restore_plan import RestorePlan
from google.cloud.gke_backup_v1.types.volume import VolumeBackup, VolumeRestore

__all__ = (
    "BackupForGKEClient",
    "BackupForGKEAsyncClient",
    "Backup",
    "BackupPlan",
    "EncryptionKey",
    "NamespacedName",
    "NamespacedNames",
    "Namespaces",
    "CreateBackupPlanRequest",
    "CreateBackupRequest",
    "CreateRestorePlanRequest",
    "CreateRestoreRequest",
    "DeleteBackupPlanRequest",
    "DeleteBackupRequest",
    "DeleteRestorePlanRequest",
    "DeleteRestoreRequest",
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
    "OperationMetadata",
    "UpdateBackupPlanRequest",
    "UpdateBackupRequest",
    "UpdateRestorePlanRequest",
    "UpdateRestoreRequest",
    "Restore",
    "RestoreConfig",
    "RestorePlan",
    "VolumeBackup",
    "VolumeRestore",
)
