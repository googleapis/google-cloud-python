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
from google.cloud.alloydb_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.alloy_db_admin import AlloyDBAdminAsyncClient, AlloyDBAdminClient
from .types.resources import (
    AutomatedBackupPolicy,
    Backup,
    BackupSource,
    Cluster,
    ConnectionInfo,
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
    CreateSecondaryClusterRequest,
    CreateSecondaryInstanceRequest,
    DeleteBackupRequest,
    DeleteClusterRequest,
    DeleteInstanceRequest,
    FailoverInstanceRequest,
    GenerateClientCertificateRequest,
    GenerateClientCertificateResponse,
    GetBackupRequest,
    GetClusterRequest,
    GetConnectionInfoRequest,
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
    PromoteClusterRequest,
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
    "ConnectionInfo",
    "ContinuousBackupConfig",
    "ContinuousBackupInfo",
    "ContinuousBackupSource",
    "CreateBackupRequest",
    "CreateClusterRequest",
    "CreateInstanceRequest",
    "CreateInstanceRequests",
    "CreateSecondaryClusterRequest",
    "CreateSecondaryInstanceRequest",
    "DatabaseVersion",
    "DeleteBackupRequest",
    "DeleteClusterRequest",
    "DeleteInstanceRequest",
    "EncryptionConfig",
    "EncryptionInfo",
    "FailoverInstanceRequest",
    "GenerateClientCertificateRequest",
    "GenerateClientCertificateResponse",
    "GetBackupRequest",
    "GetClusterRequest",
    "GetConnectionInfoRequest",
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
    "PromoteClusterRequest",
    "RestartInstanceRequest",
    "RestoreClusterRequest",
    "SslConfig",
    "SupportedDatabaseFlag",
    "UpdateBackupRequest",
    "UpdateClusterRequest",
    "UpdateInstanceRequest",
    "UserPassword",
)
