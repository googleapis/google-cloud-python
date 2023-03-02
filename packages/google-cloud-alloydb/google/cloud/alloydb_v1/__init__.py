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
from google.cloud.alloydb_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.alloy_db_admin import AlloyDBAdminAsyncClient, AlloyDBAdminClient
from .types.resources import (
    AutomatedBackupPolicy,
    Backup,
    BackupSource,
    Cluster,
    DatabaseVersion,
    EncryptionConfig,
    EncryptionInfo,
    Instance,
    InstanceView,
    MigrationSource,
    SslConfig,
    SupportedDatabaseFlag,
    UserPassword,
)
from .types.service import (
    BatchCreateInstancesMetadata,
    BatchCreateInstancesRequest,
    BatchCreateInstancesResponse,
    BatchCreateInstanceStatus,
    CreateBackupRequest,
    CreateClusterRequest,
    CreateInstanceRequest,
    CreateInstanceRequests,
    DeleteBackupRequest,
    DeleteClusterRequest,
    DeleteInstanceRequest,
    FailoverInstanceRequest,
    GetBackupRequest,
    GetClusterRequest,
    GetInstanceRequest,
    ListBackupsRequest,
    ListBackupsResponse,
    ListClustersRequest,
    ListClustersResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    ListSupportedDatabaseFlagsRequest,
    ListSupportedDatabaseFlagsResponse,
    OperationMetadata,
    RestartInstanceRequest,
    RestoreClusterRequest,
    UpdateBackupRequest,
    UpdateClusterRequest,
    UpdateInstanceRequest,
)

__all__ = (
    "AlloyDBAdminAsyncClient",
    "AlloyDBAdminClient",
    "AutomatedBackupPolicy",
    "Backup",
    "BackupSource",
    "BatchCreateInstanceStatus",
    "BatchCreateInstancesMetadata",
    "BatchCreateInstancesRequest",
    "BatchCreateInstancesResponse",
    "Cluster",
    "CreateBackupRequest",
    "CreateClusterRequest",
    "CreateInstanceRequest",
    "CreateInstanceRequests",
    "DatabaseVersion",
    "DeleteBackupRequest",
    "DeleteClusterRequest",
    "DeleteInstanceRequest",
    "EncryptionConfig",
    "EncryptionInfo",
    "FailoverInstanceRequest",
    "GetBackupRequest",
    "GetClusterRequest",
    "GetInstanceRequest",
    "Instance",
    "InstanceView",
    "ListBackupsRequest",
    "ListBackupsResponse",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListSupportedDatabaseFlagsRequest",
    "ListSupportedDatabaseFlagsResponse",
    "MigrationSource",
    "OperationMetadata",
    "RestartInstanceRequest",
    "RestoreClusterRequest",
    "SslConfig",
    "SupportedDatabaseFlag",
    "UpdateBackupRequest",
    "UpdateClusterRequest",
    "UpdateInstanceRequest",
    "UserPassword",
)
