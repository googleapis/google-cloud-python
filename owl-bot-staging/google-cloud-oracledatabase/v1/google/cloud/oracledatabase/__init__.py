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


from google.cloud.oracledatabase_v1.services.oracle_database.client import OracleDatabaseClient
from google.cloud.oracledatabase_v1.services.oracle_database.async_client import OracleDatabaseAsyncClient

from google.cloud.oracledatabase_v1.types.autonomous_database import AllConnectionStrings
from google.cloud.oracledatabase_v1.types.autonomous_database import AutonomousDatabase
from google.cloud.oracledatabase_v1.types.autonomous_database import AutonomousDatabaseApex
from google.cloud.oracledatabase_v1.types.autonomous_database import AutonomousDatabaseConnectionStrings
from google.cloud.oracledatabase_v1.types.autonomous_database import AutonomousDatabaseConnectionUrls
from google.cloud.oracledatabase_v1.types.autonomous_database import AutonomousDatabaseProperties
from google.cloud.oracledatabase_v1.types.autonomous_database import AutonomousDatabaseStandbySummary
from google.cloud.oracledatabase_v1.types.autonomous_database import DatabaseConnectionStringProfile
from google.cloud.oracledatabase_v1.types.autonomous_database import ScheduledOperationDetails
from google.cloud.oracledatabase_v1.types.autonomous_database import DBWorkload
from google.cloud.oracledatabase_v1.types.autonomous_database import GenerateType
from google.cloud.oracledatabase_v1.types.autonomous_database import OperationsInsightsState
from google.cloud.oracledatabase_v1.types.autonomous_database import State
from google.cloud.oracledatabase_v1.types.autonomous_database_character_set import AutonomousDatabaseCharacterSet
from google.cloud.oracledatabase_v1.types.autonomous_db_backup import AutonomousDatabaseBackup
from google.cloud.oracledatabase_v1.types.autonomous_db_backup import AutonomousDatabaseBackupProperties
from google.cloud.oracledatabase_v1.types.autonomous_db_version import AutonomousDbVersion
from google.cloud.oracledatabase_v1.types.common import CustomerContact
from google.cloud.oracledatabase_v1.types.db_node import DbNode
from google.cloud.oracledatabase_v1.types.db_node import DbNodeProperties
from google.cloud.oracledatabase_v1.types.db_server import DbServer
from google.cloud.oracledatabase_v1.types.db_server import DbServerProperties
from google.cloud.oracledatabase_v1.types.db_system_shape import DbSystemShape
from google.cloud.oracledatabase_v1.types.entitlement import CloudAccountDetails
from google.cloud.oracledatabase_v1.types.entitlement import Entitlement
from google.cloud.oracledatabase_v1.types.exadata_infra import CloudExadataInfrastructure
from google.cloud.oracledatabase_v1.types.exadata_infra import CloudExadataInfrastructureProperties
from google.cloud.oracledatabase_v1.types.exadata_infra import MaintenanceWindow
from google.cloud.oracledatabase_v1.types.gi_version import GiVersion
from google.cloud.oracledatabase_v1.types.location_metadata import LocationMetadata
from google.cloud.oracledatabase_v1.types.oracledatabase import CreateAutonomousDatabaseRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import CreateCloudExadataInfrastructureRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import CreateCloudVmClusterRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import DeleteAutonomousDatabaseRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import DeleteCloudExadataInfrastructureRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import DeleteCloudVmClusterRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import GenerateAutonomousDatabaseWalletRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import GenerateAutonomousDatabaseWalletResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import GetAutonomousDatabaseRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import GetCloudExadataInfrastructureRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import GetCloudVmClusterRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListAutonomousDatabaseBackupsRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListAutonomousDatabaseBackupsResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListAutonomousDatabaseCharacterSetsRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListAutonomousDatabaseCharacterSetsResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListAutonomousDatabasesRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListAutonomousDatabasesResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListAutonomousDbVersionsRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListAutonomousDbVersionsResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListCloudExadataInfrastructuresRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListCloudExadataInfrastructuresResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListCloudVmClustersRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListCloudVmClustersResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListDbNodesRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListDbNodesResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListDbServersRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListDbServersResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListDbSystemShapesRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListDbSystemShapesResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListEntitlementsRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListEntitlementsResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import ListGiVersionsRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import ListGiVersionsResponse
from google.cloud.oracledatabase_v1.types.oracledatabase import OperationMetadata
from google.cloud.oracledatabase_v1.types.oracledatabase import RestartAutonomousDatabaseRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import RestoreAutonomousDatabaseRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import StartAutonomousDatabaseRequest
from google.cloud.oracledatabase_v1.types.oracledatabase import StopAutonomousDatabaseRequest
from google.cloud.oracledatabase_v1.types.vm_cluster import CloudVmCluster
from google.cloud.oracledatabase_v1.types.vm_cluster import CloudVmClusterProperties
from google.cloud.oracledatabase_v1.types.vm_cluster import DataCollectionOptions

__all__ = ('OracleDatabaseClient',
    'OracleDatabaseAsyncClient',
    'AllConnectionStrings',
    'AutonomousDatabase',
    'AutonomousDatabaseApex',
    'AutonomousDatabaseConnectionStrings',
    'AutonomousDatabaseConnectionUrls',
    'AutonomousDatabaseProperties',
    'AutonomousDatabaseStandbySummary',
    'DatabaseConnectionStringProfile',
    'ScheduledOperationDetails',
    'DBWorkload',
    'GenerateType',
    'OperationsInsightsState',
    'State',
    'AutonomousDatabaseCharacterSet',
    'AutonomousDatabaseBackup',
    'AutonomousDatabaseBackupProperties',
    'AutonomousDbVersion',
    'CustomerContact',
    'DbNode',
    'DbNodeProperties',
    'DbServer',
    'DbServerProperties',
    'DbSystemShape',
    'CloudAccountDetails',
    'Entitlement',
    'CloudExadataInfrastructure',
    'CloudExadataInfrastructureProperties',
    'MaintenanceWindow',
    'GiVersion',
    'LocationMetadata',
    'CreateAutonomousDatabaseRequest',
    'CreateCloudExadataInfrastructureRequest',
    'CreateCloudVmClusterRequest',
    'DeleteAutonomousDatabaseRequest',
    'DeleteCloudExadataInfrastructureRequest',
    'DeleteCloudVmClusterRequest',
    'GenerateAutonomousDatabaseWalletRequest',
    'GenerateAutonomousDatabaseWalletResponse',
    'GetAutonomousDatabaseRequest',
    'GetCloudExadataInfrastructureRequest',
    'GetCloudVmClusterRequest',
    'ListAutonomousDatabaseBackupsRequest',
    'ListAutonomousDatabaseBackupsResponse',
    'ListAutonomousDatabaseCharacterSetsRequest',
    'ListAutonomousDatabaseCharacterSetsResponse',
    'ListAutonomousDatabasesRequest',
    'ListAutonomousDatabasesResponse',
    'ListAutonomousDbVersionsRequest',
    'ListAutonomousDbVersionsResponse',
    'ListCloudExadataInfrastructuresRequest',
    'ListCloudExadataInfrastructuresResponse',
    'ListCloudVmClustersRequest',
    'ListCloudVmClustersResponse',
    'ListDbNodesRequest',
    'ListDbNodesResponse',
    'ListDbServersRequest',
    'ListDbServersResponse',
    'ListDbSystemShapesRequest',
    'ListDbSystemShapesResponse',
    'ListEntitlementsRequest',
    'ListEntitlementsResponse',
    'ListGiVersionsRequest',
    'ListGiVersionsResponse',
    'OperationMetadata',
    'RestartAutonomousDatabaseRequest',
    'RestoreAutonomousDatabaseRequest',
    'StartAutonomousDatabaseRequest',
    'StopAutonomousDatabaseRequest',
    'CloudVmCluster',
    'CloudVmClusterProperties',
    'DataCollectionOptions',
)
