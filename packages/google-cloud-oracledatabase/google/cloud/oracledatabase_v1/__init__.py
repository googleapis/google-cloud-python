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
from google.cloud.oracledatabase_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.oracle_database import OracleDatabaseClient
from .types.autonomous_database import (
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
from .types.autonomous_database_character_set import AutonomousDatabaseCharacterSet
from .types.autonomous_db_backup import (
    AutonomousDatabaseBackup,
    AutonomousDatabaseBackupProperties,
)
from .types.autonomous_db_version import AutonomousDbVersion
from .types.common import CustomerContact
from .types.db_node import DbNode, DbNodeProperties
from .types.db_server import DbServer, DbServerProperties
from .types.db_system_shape import DbSystemShape
from .types.entitlement import CloudAccountDetails, Entitlement
from .types.exadata_infra import (
    CloudExadataInfrastructure,
    CloudExadataInfrastructureProperties,
    MaintenanceWindow,
)
from .types.gi_version import GiVersion
from .types.location_metadata import LocationMetadata
from .types.oracledatabase import (
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
    RestoreAutonomousDatabaseRequest,
)
from .types.vm_cluster import (
    CloudVmCluster,
    CloudVmClusterProperties,
    DataCollectionOptions,
)

__all__ = (
    "AllConnectionStrings",
    "AutonomousDatabase",
    "AutonomousDatabaseApex",
    "AutonomousDatabaseBackup",
    "AutonomousDatabaseBackupProperties",
    "AutonomousDatabaseCharacterSet",
    "AutonomousDatabaseConnectionStrings",
    "AutonomousDatabaseConnectionUrls",
    "AutonomousDatabaseProperties",
    "AutonomousDatabaseStandbySummary",
    "AutonomousDbVersion",
    "CloudAccountDetails",
    "CloudExadataInfrastructure",
    "CloudExadataInfrastructureProperties",
    "CloudVmCluster",
    "CloudVmClusterProperties",
    "CreateAutonomousDatabaseRequest",
    "CreateCloudExadataInfrastructureRequest",
    "CreateCloudVmClusterRequest",
    "CustomerContact",
    "DBWorkload",
    "DataCollectionOptions",
    "DatabaseConnectionStringProfile",
    "DbNode",
    "DbNodeProperties",
    "DbServer",
    "DbServerProperties",
    "DbSystemShape",
    "DeleteAutonomousDatabaseRequest",
    "DeleteCloudExadataInfrastructureRequest",
    "DeleteCloudVmClusterRequest",
    "Entitlement",
    "GenerateAutonomousDatabaseWalletRequest",
    "GenerateAutonomousDatabaseWalletResponse",
    "GenerateType",
    "GetAutonomousDatabaseRequest",
    "GetCloudExadataInfrastructureRequest",
    "GetCloudVmClusterRequest",
    "GiVersion",
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
    "LocationMetadata",
    "MaintenanceWindow",
    "OperationMetadata",
    "OperationsInsightsState",
    "OracleDatabaseClient",
    "RestoreAutonomousDatabaseRequest",
    "ScheduledOperationDetails",
    "State",
)
