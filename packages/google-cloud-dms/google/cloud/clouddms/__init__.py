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

from google.cloud.clouddms_v1.services.data_migration_service.async_client import (
    DataMigrationServiceAsyncClient,
)
from google.cloud.clouddms_v1.services.data_migration_service.client import (
    DataMigrationServiceClient,
)
from google.cloud.clouddms_v1.types.clouddms import (
    CreateConnectionProfileRequest,
    CreateMigrationJobRequest,
    DeleteConnectionProfileRequest,
    DeleteMigrationJobRequest,
    GenerateSshScriptRequest,
    GetConnectionProfileRequest,
    GetMigrationJobRequest,
    ListConnectionProfilesRequest,
    ListConnectionProfilesResponse,
    ListMigrationJobsRequest,
    ListMigrationJobsResponse,
    OperationMetadata,
    PromoteMigrationJobRequest,
    RestartMigrationJobRequest,
    ResumeMigrationJobRequest,
    SshScript,
    StartMigrationJobRequest,
    StopMigrationJobRequest,
    UpdateConnectionProfileRequest,
    UpdateMigrationJobRequest,
    VerifyMigrationJobRequest,
    VmCreationConfig,
    VmSelectionConfig,
)
from google.cloud.clouddms_v1.types.clouddms_resources import (
    CloudSqlConnectionProfile,
    CloudSqlSettings,
    ConnectionProfile,
    DatabaseEngine,
    DatabaseProvider,
    DatabaseType,
    MigrationJob,
    MigrationJobVerificationError,
    MySqlConnectionProfile,
    PostgreSqlConnectionProfile,
    ReverseSshConnectivity,
    SqlAclEntry,
    SqlIpConfig,
    SslConfig,
    StaticIpConnectivity,
    VpcPeeringConnectivity,
)

__all__ = (
    "DataMigrationServiceClient",
    "DataMigrationServiceAsyncClient",
    "CreateConnectionProfileRequest",
    "CreateMigrationJobRequest",
    "DeleteConnectionProfileRequest",
    "DeleteMigrationJobRequest",
    "GenerateSshScriptRequest",
    "GetConnectionProfileRequest",
    "GetMigrationJobRequest",
    "ListConnectionProfilesRequest",
    "ListConnectionProfilesResponse",
    "ListMigrationJobsRequest",
    "ListMigrationJobsResponse",
    "OperationMetadata",
    "PromoteMigrationJobRequest",
    "RestartMigrationJobRequest",
    "ResumeMigrationJobRequest",
    "SshScript",
    "StartMigrationJobRequest",
    "StopMigrationJobRequest",
    "UpdateConnectionProfileRequest",
    "UpdateMigrationJobRequest",
    "VerifyMigrationJobRequest",
    "VmCreationConfig",
    "VmSelectionConfig",
    "CloudSqlConnectionProfile",
    "CloudSqlSettings",
    "ConnectionProfile",
    "DatabaseType",
    "MigrationJob",
    "MigrationJobVerificationError",
    "MySqlConnectionProfile",
    "PostgreSqlConnectionProfile",
    "ReverseSshConnectivity",
    "SqlAclEntry",
    "SqlIpConfig",
    "SslConfig",
    "StaticIpConnectivity",
    "VpcPeeringConnectivity",
    "DatabaseEngine",
    "DatabaseProvider",
)
