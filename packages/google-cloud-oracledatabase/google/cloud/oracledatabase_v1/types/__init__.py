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
from .autonomous_database import (
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
from .autonomous_database_character_set import AutonomousDatabaseCharacterSet
from .autonomous_db_backup import (
    AutonomousDatabaseBackup,
    AutonomousDatabaseBackupProperties,
)
from .autonomous_db_version import AutonomousDbVersion
from .common import CustomerContact
from .db_node import DbNode, DbNodeProperties
from .db_server import DbServer, DbServerProperties
from .db_system_shape import DbSystemShape
from .entitlement import CloudAccountDetails, Entitlement
from .exadata_infra import (
    CloudExadataInfrastructure,
    CloudExadataInfrastructureProperties,
    MaintenanceWindow,
)
from .gi_version import GiVersion
from .location_metadata import LocationMetadata
from .oracledatabase import (
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
from .vm_cluster import CloudVmCluster, CloudVmClusterProperties, DataCollectionOptions

__all__ = (
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
