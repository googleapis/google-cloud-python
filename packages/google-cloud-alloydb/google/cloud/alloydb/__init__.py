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
from google.cloud.alloydb import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.alloydb_v1.services.alloy_db_admin.async_client import (
    AlloyDBAdminAsyncClient,
)
from google.cloud.alloydb_v1.services.alloy_db_admin.client import AlloyDBAdminClient
from google.cloud.alloydb_v1.types.resources import (
    AutomatedBackupPolicy,
    Backup,
    BackupSource,
    Cluster,
    ClusterView,
    ContinuousBackupConfig,
    ContinuousBackupInfo,
    ContinuousBackupSource,
    DatabaseVersion,
    EncryptionConfig,
    EncryptionInfo,
    Instance,
    InstanceView,
    MigrationSource,
    SslConfig,
    SupportedDatabaseFlag,
    User,
    UserPassword,
)
from google.cloud.alloydb_v1.types.service import (
    BatchCreateInstancesMetadata,
    BatchCreateInstancesRequest,
    BatchCreateInstancesResponse,
    BatchCreateInstanceStatus,
    CreateBackupRequest,
    CreateClusterRequest,
    CreateInstanceRequest,
    CreateInstanceRequests,
    CreateSecondaryClusterRequest,
    CreateSecondaryInstanceRequest,
    CreateUserRequest,
    DeleteBackupRequest,
    DeleteClusterRequest,
    DeleteInstanceRequest,
    DeleteUserRequest,
    FailoverInstanceRequest,
    GetBackupRequest,
    GetClusterRequest,
    GetInstanceRequest,
    GetUserRequest,
    InjectFaultRequest,
    ListBackupsRequest,
    ListBackupsResponse,
    ListClustersRequest,
    ListClustersResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    ListSupportedDatabaseFlagsRequest,
    ListSupportedDatabaseFlagsResponse,
    ListUsersRequest,
    ListUsersResponse,
    OperationMetadata,
    PromoteClusterRequest,
    RestartInstanceRequest,
    RestoreClusterRequest,
    UpdateBackupRequest,
    UpdateClusterRequest,
    UpdateInstanceRequest,
    UpdateUserRequest,
)

__all__ = (
    "AlloyDBAdminClient",
    "AlloyDBAdminAsyncClient",
    "AutomatedBackupPolicy",
    "Backup",
    "BackupSource",
    "Cluster",
    "ContinuousBackupConfig",
    "ContinuousBackupInfo",
    "ContinuousBackupSource",
    "EncryptionConfig",
    "EncryptionInfo",
    "Instance",
    "MigrationSource",
    "SslConfig",
    "SupportedDatabaseFlag",
    "User",
    "UserPassword",
    "ClusterView",
    "DatabaseVersion",
    "InstanceView",
    "BatchCreateInstancesMetadata",
    "BatchCreateInstancesRequest",
    "BatchCreateInstancesResponse",
    "BatchCreateInstanceStatus",
    "CreateBackupRequest",
    "CreateClusterRequest",
    "CreateInstanceRequest",
    "CreateInstanceRequests",
    "CreateSecondaryClusterRequest",
    "CreateSecondaryInstanceRequest",
    "CreateUserRequest",
    "DeleteBackupRequest",
    "DeleteClusterRequest",
    "DeleteInstanceRequest",
    "DeleteUserRequest",
    "FailoverInstanceRequest",
    "GetBackupRequest",
    "GetClusterRequest",
    "GetInstanceRequest",
    "GetUserRequest",
    "InjectFaultRequest",
    "ListBackupsRequest",
    "ListBackupsResponse",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListSupportedDatabaseFlagsRequest",
    "ListSupportedDatabaseFlagsResponse",
    "ListUsersRequest",
    "ListUsersResponse",
    "OperationMetadata",
    "PromoteClusterRequest",
    "RestartInstanceRequest",
    "RestoreClusterRequest",
    "UpdateBackupRequest",
    "UpdateClusterRequest",
    "UpdateInstanceRequest",
    "UpdateUserRequest",
)
