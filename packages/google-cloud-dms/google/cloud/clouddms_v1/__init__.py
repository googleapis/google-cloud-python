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

from .services.data_migration_service import (
    DataMigrationServiceAsyncClient,
    DataMigrationServiceClient,
)
from .types.clouddms import (
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
from .types.clouddms_resources import (
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
    "DataMigrationServiceAsyncClient",
    "CloudSqlConnectionProfile",
    "CloudSqlSettings",
    "ConnectionProfile",
    "CreateConnectionProfileRequest",
    "CreateMigrationJobRequest",
    "DataMigrationServiceClient",
    "DatabaseEngine",
    "DatabaseProvider",
    "DatabaseType",
    "DeleteConnectionProfileRequest",
    "DeleteMigrationJobRequest",
    "GenerateSshScriptRequest",
    "GetConnectionProfileRequest",
    "GetMigrationJobRequest",
    "ListConnectionProfilesRequest",
    "ListConnectionProfilesResponse",
    "ListMigrationJobsRequest",
    "ListMigrationJobsResponse",
    "MigrationJob",
    "MigrationJobVerificationError",
    "MySqlConnectionProfile",
    "OperationMetadata",
    "PostgreSqlConnectionProfile",
    "PromoteMigrationJobRequest",
    "RestartMigrationJobRequest",
    "ResumeMigrationJobRequest",
    "ReverseSshConnectivity",
    "SqlAclEntry",
    "SqlIpConfig",
    "SshScript",
    "SslConfig",
    "StartMigrationJobRequest",
    "StaticIpConnectivity",
    "StopMigrationJobRequest",
    "UpdateConnectionProfileRequest",
    "UpdateMigrationJobRequest",
    "VerifyMigrationJobRequest",
    "VmCreationConfig",
    "VmSelectionConfig",
    "VpcPeeringConnectivity",
)
