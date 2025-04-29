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
from google.cloud.oracledatabase import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.oracledatabase_v1.services.oracle_database.async_client import (
    OracleDatabaseAsyncClient,
)
from google.cloud.oracledatabase_v1.services.oracle_database.client import (
    OracleDatabaseClient,
)
from google.cloud.oracledatabase_v1.types.autonomous_database import (
    AllConnectionStrings,
    AutonomousDatabase,
    AutonomousDatabaseApex,
    AutonomousDatabaseConnectionStrings,
    AutonomousDatabaseConnectionUrls,
    AutonomousDatabaseProperties,
    AutonomousDatabaseStandbySummary,
    DatabaseConnectionStringProfile,
    DBWorkload,
    GenerateType,
    OperationsInsightsState,
    ScheduledOperationDetails,
    State,
)
from google.cloud.oracledatabase_v1.types.autonomous_database_character_set import (
    AutonomousDatabaseCharacterSet,
)
from google.cloud.oracledatabase_v1.types.autonomous_db_backup import (
    AutonomousDatabaseBackup,
    AutonomousDatabaseBackupProperties,
)
from google.cloud.oracledatabase_v1.types.autonomous_db_version import (
    AutonomousDbVersion,
)
from google.cloud.oracledatabase_v1.types.common import CustomerContact
from google.cloud.oracledatabase_v1.types.db_node import DbNode, DbNodeProperties
from google.cloud.oracledatabase_v1.types.db_server import DbServer, DbServerProperties
from google.cloud.oracledatabase_v1.types.db_system_shape import DbSystemShape
from google.cloud.oracledatabase_v1.types.entitlement import (
    CloudAccountDetails,
    Entitlement,
)
from google.cloud.oracledatabase_v1.types.exadata_infra import (
    CloudExadataInfrastructure,
    CloudExadataInfrastructureProperties,
    MaintenanceWindow,
)
from google.cloud.oracledatabase_v1.types.gi_version import GiVersion
from google.cloud.oracledatabase_v1.types.location_metadata import LocationMetadata
from google.cloud.oracledatabase_v1.types.oracledatabase import (
    CreateAutonomousDatabaseRequest,
    CreateCloudExadataInfrastructureRequest,
    CreateCloudVmClusterRequest,
    DeleteAutonomousDatabaseRequest,
    DeleteCloudExadataInfrastructureRequest,
    DeleteCloudVmClusterRequest,
    GenerateAutonomousDatabaseWalletRequest,
    GenerateAutonomousDatabaseWalletResponse,
    GetAutonomousDatabaseRequest,
    GetCloudExadataInfrastructureRequest,
    GetCloudVmClusterRequest,
    ListAutonomousDatabaseBackupsRequest,
    ListAutonomousDatabaseBackupsResponse,
    ListAutonomousDatabaseCharacterSetsRequest,
    ListAutonomousDatabaseCharacterSetsResponse,
    ListAutonomousDatabasesRequest,
    ListAutonomousDatabasesResponse,
    ListAutonomousDbVersionsRequest,
    ListAutonomousDbVersionsResponse,
    ListCloudExadataInfrastructuresRequest,
    ListCloudExadataInfrastructuresResponse,
    ListCloudVmClustersRequest,
    ListCloudVmClustersResponse,
    ListDbNodesRequest,
    ListDbNodesResponse,
    ListDbServersRequest,
    ListDbServersResponse,
    ListDbSystemShapesRequest,
    ListDbSystemShapesResponse,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    ListGiVersionsRequest,
    ListGiVersionsResponse,
    OperationMetadata,
    RestartAutonomousDatabaseRequest,
    RestoreAutonomousDatabaseRequest,
    StartAutonomousDatabaseRequest,
    StopAutonomousDatabaseRequest,
)
from google.cloud.oracledatabase_v1.types.vm_cluster import (
    CloudVmCluster,
    CloudVmClusterProperties,
    DataCollectionOptions,
)

__all__ = (
    "OracleDatabaseClient",
    "OracleDatabaseAsyncClient",
    "AllConnectionStrings",
    "AutonomousDatabase",
    "AutonomousDatabaseApex",
    "AutonomousDatabaseConnectionStrings",
    "AutonomousDatabaseConnectionUrls",
    "AutonomousDatabaseProperties",
    "AutonomousDatabaseStandbySummary",
    "DatabaseConnectionStringProfile",
    "ScheduledOperationDetails",
    "DBWorkload",
    "GenerateType",
    "OperationsInsightsState",
    "State",
    "AutonomousDatabaseCharacterSet",
    "AutonomousDatabaseBackup",
    "AutonomousDatabaseBackupProperties",
    "AutonomousDbVersion",
    "CustomerContact",
    "DbNode",
    "DbNodeProperties",
    "DbServer",
    "DbServerProperties",
    "DbSystemShape",
    "CloudAccountDetails",
    "Entitlement",
    "CloudExadataInfrastructure",
    "CloudExadataInfrastructureProperties",
    "MaintenanceWindow",
    "GiVersion",
    "LocationMetadata",
    "CreateAutonomousDatabaseRequest",
    "CreateCloudExadataInfrastructureRequest",
    "CreateCloudVmClusterRequest",
    "DeleteAutonomousDatabaseRequest",
    "DeleteCloudExadataInfrastructureRequest",
    "DeleteCloudVmClusterRequest",
    "GenerateAutonomousDatabaseWalletRequest",
    "GenerateAutonomousDatabaseWalletResponse",
    "GetAutonomousDatabaseRequest",
    "GetCloudExadataInfrastructureRequest",
    "GetCloudVmClusterRequest",
    "ListAutonomousDatabaseBackupsRequest",
    "ListAutonomousDatabaseBackupsResponse",
    "ListAutonomousDatabaseCharacterSetsRequest",
    "ListAutonomousDatabaseCharacterSetsResponse",
    "ListAutonomousDatabasesRequest",
    "ListAutonomousDatabasesResponse",
    "ListAutonomousDbVersionsRequest",
    "ListAutonomousDbVersionsResponse",
    "ListCloudExadataInfrastructuresRequest",
    "ListCloudExadataInfrastructuresResponse",
    "ListCloudVmClustersRequest",
    "ListCloudVmClustersResponse",
    "ListDbNodesRequest",
    "ListDbNodesResponse",
    "ListDbServersRequest",
    "ListDbServersResponse",
    "ListDbSystemShapesRequest",
    "ListDbSystemShapesResponse",
    "ListEntitlementsRequest",
    "ListEntitlementsResponse",
    "ListGiVersionsRequest",
    "ListGiVersionsResponse",
    "OperationMetadata",
    "RestartAutonomousDatabaseRequest",
    "RestoreAutonomousDatabaseRequest",
    "StartAutonomousDatabaseRequest",
    "StopAutonomousDatabaseRequest",
    "CloudVmCluster",
    "CloudVmClusterProperties",
    "DataCollectionOptions",
)
