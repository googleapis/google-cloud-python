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

from google.cloud.clouddms_v1.services.data_migration_service.client import (
    DataMigrationServiceClient,
)
from google.cloud.clouddms_v1.services.data_migration_service.async_client import (
    DataMigrationServiceAsyncClient,
)

from google.cloud.clouddms_v1.types.clouddms import CreateConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import CreateMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import DeleteMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import GenerateSshScriptRequest
from google.cloud.clouddms_v1.types.clouddms import GetConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import GetMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import ListConnectionProfilesRequest
from google.cloud.clouddms_v1.types.clouddms import ListConnectionProfilesResponse
from google.cloud.clouddms_v1.types.clouddms import ListMigrationJobsRequest
from google.cloud.clouddms_v1.types.clouddms import ListMigrationJobsResponse
from google.cloud.clouddms_v1.types.clouddms import OperationMetadata
from google.cloud.clouddms_v1.types.clouddms import PromoteMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import RestartMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import ResumeMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import SshScript
from google.cloud.clouddms_v1.types.clouddms import StartMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import StopMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import UpdateConnectionProfileRequest
from google.cloud.clouddms_v1.types.clouddms import UpdateMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import VerifyMigrationJobRequest
from google.cloud.clouddms_v1.types.clouddms import VmCreationConfig
from google.cloud.clouddms_v1.types.clouddms import VmSelectionConfig
from google.cloud.clouddms_v1.types.clouddms_resources import CloudSqlConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import CloudSqlSettings
from google.cloud.clouddms_v1.types.clouddms_resources import ConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import DatabaseType
from google.cloud.clouddms_v1.types.clouddms_resources import MigrationJob
from google.cloud.clouddms_v1.types.clouddms_resources import (
    MigrationJobVerificationError,
)
from google.cloud.clouddms_v1.types.clouddms_resources import MySqlConnectionProfile
from google.cloud.clouddms_v1.types.clouddms_resources import (
    PostgreSqlConnectionProfile,
)
from google.cloud.clouddms_v1.types.clouddms_resources import ReverseSshConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import SqlAclEntry
from google.cloud.clouddms_v1.types.clouddms_resources import SqlIpConfig
from google.cloud.clouddms_v1.types.clouddms_resources import SslConfig
from google.cloud.clouddms_v1.types.clouddms_resources import StaticIpConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import VpcPeeringConnectivity
from google.cloud.clouddms_v1.types.clouddms_resources import DatabaseEngine
from google.cloud.clouddms_v1.types.clouddms_resources import DatabaseProvider

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
