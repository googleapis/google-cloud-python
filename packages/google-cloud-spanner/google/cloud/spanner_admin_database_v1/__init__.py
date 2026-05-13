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
import sys

import google.api_core as api_core

from google.cloud.spanner_admin_database_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.database_admin import DatabaseAdminAsyncClient, DatabaseAdminClient
from .types.backup import (
    Backup,
    BackupInfo,
    BackupInstancePartition,
    CopyBackupEncryptionConfig,
    CopyBackupMetadata,
    CopyBackupRequest,
    CreateBackupEncryptionConfig,
    CreateBackupMetadata,
    CreateBackupRequest,
    DeleteBackupRequest,
    FullBackupSpec,
    GetBackupRequest,
    IncrementalBackupSpec,
    ListBackupOperationsRequest,
    ListBackupOperationsResponse,
    ListBackupsRequest,
    ListBackupsResponse,
    UpdateBackupRequest,
)
from .types.backup_schedule import (
    BackupSchedule,
    BackupScheduleSpec,
    CreateBackupScheduleRequest,
    CrontabSpec,
    DeleteBackupScheduleRequest,
    GetBackupScheduleRequest,
    ListBackupSchedulesRequest,
    ListBackupSchedulesResponse,
    UpdateBackupScheduleRequest,
)
from .types.common import (
    DatabaseDialect,
    EncryptionConfig,
    EncryptionInfo,
    OperationProgress,
)
from .types.spanner_database_admin import (
    AddSplitPointsRequest,
    AddSplitPointsResponse,
    CreateDatabaseMetadata,
    CreateDatabaseRequest,
    Database,
    DatabaseRole,
    DdlStatementActionInfo,
    DropDatabaseRequest,
    GetDatabaseDdlRequest,
    GetDatabaseDdlResponse,
    GetDatabaseRequest,
    InternalUpdateGraphOperationRequest,
    InternalUpdateGraphOperationResponse,
    ListDatabaseOperationsRequest,
    ListDatabaseOperationsResponse,
    ListDatabaseRolesRequest,
    ListDatabaseRolesResponse,
    ListDatabasesRequest,
    ListDatabasesResponse,
    OptimizeRestoredDatabaseMetadata,
    RestoreDatabaseEncryptionConfig,
    RestoreDatabaseMetadata,
    RestoreDatabaseRequest,
    RestoreInfo,
    RestoreSourceType,
    SplitPoints,
    UpdateDatabaseDdlMetadata,
    UpdateDatabaseDdlRequest,
    UpdateDatabaseMetadata,
    UpdateDatabaseRequest,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.spanner_admin_database_v1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.spanner_admin_database_v1")  # type: ignore
else:  # pragma: NO COVER
    import warnings

    _py_version_str = sys.version.split()[0]
    # version-scanner: ignore-next-line
    if sys.version_info < (3, 10):
        warnings.warn(
            "You are using a non-supported Python version "
            + f"({_py_version_str}).  Google will not post any further "
            + "updates to google.cloud.spanner_admin_database_v1 supporting this Python version. "
            + "Please upgrade to the latest Python version, or at "
            + "least to Python 3.10, and then update google.cloud.spanner_admin_database_v1.",
            FutureWarning,
        )

__all__ = (
    "DatabaseAdminAsyncClient",
    "AddSplitPointsRequest",
    "AddSplitPointsResponse",
    "Backup",
    "BackupInfo",
    "BackupInstancePartition",
    "BackupSchedule",
    "BackupScheduleSpec",
    "CopyBackupEncryptionConfig",
    "CopyBackupMetadata",
    "CopyBackupRequest",
    "CreateBackupEncryptionConfig",
    "CreateBackupMetadata",
    "CreateBackupRequest",
    "CreateBackupScheduleRequest",
    "CreateDatabaseMetadata",
    "CreateDatabaseRequest",
    "CrontabSpec",
    "Database",
    "DatabaseAdminClient",
    "DatabaseDialect",
    "DatabaseRole",
    "DdlStatementActionInfo",
    "DeleteBackupRequest",
    "DeleteBackupScheduleRequest",
    "DropDatabaseRequest",
    "EncryptionConfig",
    "EncryptionInfo",
    "FullBackupSpec",
    "GetBackupRequest",
    "GetBackupScheduleRequest",
    "GetDatabaseDdlRequest",
    "GetDatabaseDdlResponse",
    "GetDatabaseRequest",
    "IncrementalBackupSpec",
    "InternalUpdateGraphOperationRequest",
    "InternalUpdateGraphOperationResponse",
    "ListBackupOperationsRequest",
    "ListBackupOperationsResponse",
    "ListBackupSchedulesRequest",
    "ListBackupSchedulesResponse",
    "ListBackupsRequest",
    "ListBackupsResponse",
    "ListDatabaseOperationsRequest",
    "ListDatabaseOperationsResponse",
    "ListDatabaseRolesRequest",
    "ListDatabaseRolesResponse",
    "ListDatabasesRequest",
    "ListDatabasesResponse",
    "OperationProgress",
    "OptimizeRestoredDatabaseMetadata",
    "RestoreDatabaseEncryptionConfig",
    "RestoreDatabaseMetadata",
    "RestoreDatabaseRequest",
    "RestoreInfo",
    "RestoreSourceType",
    "SplitPoints",
    "UpdateBackupRequest",
    "UpdateBackupScheduleRequest",
    "UpdateDatabaseDdlMetadata",
    "UpdateDatabaseDdlRequest",
    "UpdateDatabaseMetadata",
    "UpdateDatabaseRequest",
)
