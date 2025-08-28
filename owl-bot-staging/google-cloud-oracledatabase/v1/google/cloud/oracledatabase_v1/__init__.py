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
from google.cloud.oracledatabase_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.oracle_database import OracleDatabaseClient
from .services.oracle_database import OracleDatabaseAsyncClient

from .types.autonomous_database import AllConnectionStrings
from .types.autonomous_database import AutonomousDatabase
from .types.autonomous_database import AutonomousDatabaseApex
from .types.autonomous_database import AutonomousDatabaseConnectionStrings
from .types.autonomous_database import AutonomousDatabaseConnectionUrls
from .types.autonomous_database import AutonomousDatabaseProperties
from .types.autonomous_database import AutonomousDatabaseStandbySummary
from .types.autonomous_database import DatabaseConnectionStringProfile
from .types.autonomous_database import ScheduledOperationDetails
from .types.autonomous_database import DBWorkload
from .types.autonomous_database import GenerateType
from .types.autonomous_database import OperationsInsightsState
from .types.autonomous_database import State
from .types.autonomous_database_character_set import AutonomousDatabaseCharacterSet
from .types.autonomous_db_backup import AutonomousDatabaseBackup
from .types.autonomous_db_backup import AutonomousDatabaseBackupProperties
from .types.autonomous_db_version import AutonomousDbVersion
from .types.common import CustomerContact
from .types.db_node import DbNode
from .types.db_node import DbNodeProperties
from .types.db_server import DbServer
from .types.db_server import DbServerProperties
from .types.db_system_shape import DbSystemShape
from .types.entitlement import CloudAccountDetails
from .types.entitlement import Entitlement
from .types.exadata_infra import CloudExadataInfrastructure
from .types.exadata_infra import CloudExadataInfrastructureProperties
from .types.exadata_infra import MaintenanceWindow
from .types.gi_version import GiVersion
from .types.location_metadata import LocationMetadata
from .types.oracledatabase import CreateAutonomousDatabaseRequest
from .types.oracledatabase import CreateCloudExadataInfrastructureRequest
from .types.oracledatabase import CreateCloudVmClusterRequest
from .types.oracledatabase import DeleteAutonomousDatabaseRequest
from .types.oracledatabase import DeleteCloudExadataInfrastructureRequest
from .types.oracledatabase import DeleteCloudVmClusterRequest
from .types.oracledatabase import GenerateAutonomousDatabaseWalletRequest
from .types.oracledatabase import GenerateAutonomousDatabaseWalletResponse
from .types.oracledatabase import GetAutonomousDatabaseRequest
from .types.oracledatabase import GetCloudExadataInfrastructureRequest
from .types.oracledatabase import GetCloudVmClusterRequest
from .types.oracledatabase import ListAutonomousDatabaseBackupsRequest
from .types.oracledatabase import ListAutonomousDatabaseBackupsResponse
from .types.oracledatabase import ListAutonomousDatabaseCharacterSetsRequest
from .types.oracledatabase import ListAutonomousDatabaseCharacterSetsResponse
from .types.oracledatabase import ListAutonomousDatabasesRequest
from .types.oracledatabase import ListAutonomousDatabasesResponse
from .types.oracledatabase import ListAutonomousDbVersionsRequest
from .types.oracledatabase import ListAutonomousDbVersionsResponse
from .types.oracledatabase import ListCloudExadataInfrastructuresRequest
from .types.oracledatabase import ListCloudExadataInfrastructuresResponse
from .types.oracledatabase import ListCloudVmClustersRequest
from .types.oracledatabase import ListCloudVmClustersResponse
from .types.oracledatabase import ListDbNodesRequest
from .types.oracledatabase import ListDbNodesResponse
from .types.oracledatabase import ListDbServersRequest
from .types.oracledatabase import ListDbServersResponse
from .types.oracledatabase import ListDbSystemShapesRequest
from .types.oracledatabase import ListDbSystemShapesResponse
from .types.oracledatabase import ListEntitlementsRequest
from .types.oracledatabase import ListEntitlementsResponse
from .types.oracledatabase import ListGiVersionsRequest
from .types.oracledatabase import ListGiVersionsResponse
from .types.oracledatabase import OperationMetadata
from .types.oracledatabase import RestartAutonomousDatabaseRequest
from .types.oracledatabase import RestoreAutonomousDatabaseRequest
from .types.oracledatabase import StartAutonomousDatabaseRequest
from .types.oracledatabase import StopAutonomousDatabaseRequest
from .types.vm_cluster import CloudVmCluster
from .types.vm_cluster import CloudVmClusterProperties
from .types.vm_cluster import DataCollectionOptions

__all__ = (
    'OracleDatabaseAsyncClient',
'AllConnectionStrings',
'AutonomousDatabase',
'AutonomousDatabaseApex',
'AutonomousDatabaseBackup',
'AutonomousDatabaseBackupProperties',
'AutonomousDatabaseCharacterSet',
'AutonomousDatabaseConnectionStrings',
'AutonomousDatabaseConnectionUrls',
'AutonomousDatabaseProperties',
'AutonomousDatabaseStandbySummary',
'AutonomousDbVersion',
'CloudAccountDetails',
'CloudExadataInfrastructure',
'CloudExadataInfrastructureProperties',
'CloudVmCluster',
'CloudVmClusterProperties',
'CreateAutonomousDatabaseRequest',
'CreateCloudExadataInfrastructureRequest',
'CreateCloudVmClusterRequest',
'CustomerContact',
'DBWorkload',
'DataCollectionOptions',
'DatabaseConnectionStringProfile',
'DbNode',
'DbNodeProperties',
'DbServer',
'DbServerProperties',
'DbSystemShape',
'DeleteAutonomousDatabaseRequest',
'DeleteCloudExadataInfrastructureRequest',
'DeleteCloudVmClusterRequest',
'Entitlement',
'GenerateAutonomousDatabaseWalletRequest',
'GenerateAutonomousDatabaseWalletResponse',
'GenerateType',
'GetAutonomousDatabaseRequest',
'GetCloudExadataInfrastructureRequest',
'GetCloudVmClusterRequest',
'GiVersion',
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
'LocationMetadata',
'MaintenanceWindow',
'OperationMetadata',
'OperationsInsightsState',
'OracleDatabaseClient',
'RestartAutonomousDatabaseRequest',
'RestoreAutonomousDatabaseRequest',
'ScheduledOperationDetails',
'StartAutonomousDatabaseRequest',
'State',
'StopAutonomousDatabaseRequest',
)
