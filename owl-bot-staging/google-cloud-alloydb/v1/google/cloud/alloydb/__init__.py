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
from google.cloud.alloydb import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.alloydb_v1.services.alloy_db_admin.client import AlloyDBAdminClient
from google.cloud.alloydb_v1.services.alloy_db_admin.async_client import AlloyDBAdminAsyncClient
from google.cloud.alloydb_v1.services.alloy_dbcsql_admin.client import AlloyDBCSQLAdminClient
from google.cloud.alloydb_v1.services.alloy_dbcsql_admin.async_client import AlloyDBCSQLAdminAsyncClient

from google.cloud.alloydb_v1.types.csql_resources import CloudSQLBackupRunSource
from google.cloud.alloydb_v1.types.csql_service import RestoreFromCloudSQLRequest
from google.cloud.alloydb_v1.types.data_model import SqlResult
from google.cloud.alloydb_v1.types.data_model import SqlResultColumn
from google.cloud.alloydb_v1.types.data_model import SqlResultRow
from google.cloud.alloydb_v1.types.data_model import SqlResultValue
from google.cloud.alloydb_v1.types.resources import AutomatedBackupPolicy
from google.cloud.alloydb_v1.types.resources import Backup
from google.cloud.alloydb_v1.types.resources import BackupSource
from google.cloud.alloydb_v1.types.resources import Cluster
from google.cloud.alloydb_v1.types.resources import ConnectionInfo
from google.cloud.alloydb_v1.types.resources import ContinuousBackupConfig
from google.cloud.alloydb_v1.types.resources import ContinuousBackupInfo
from google.cloud.alloydb_v1.types.resources import ContinuousBackupSource
from google.cloud.alloydb_v1.types.resources import Database
from google.cloud.alloydb_v1.types.resources import EncryptionConfig
from google.cloud.alloydb_v1.types.resources import EncryptionInfo
from google.cloud.alloydb_v1.types.resources import Instance
from google.cloud.alloydb_v1.types.resources import MaintenanceSchedule
from google.cloud.alloydb_v1.types.resources import MaintenanceUpdatePolicy
from google.cloud.alloydb_v1.types.resources import MigrationSource
from google.cloud.alloydb_v1.types.resources import SslConfig
from google.cloud.alloydb_v1.types.resources import SupportedDatabaseFlag
from google.cloud.alloydb_v1.types.resources import User
from google.cloud.alloydb_v1.types.resources import UserPassword
from google.cloud.alloydb_v1.types.resources import ClusterView
from google.cloud.alloydb_v1.types.resources import DatabaseVersion
from google.cloud.alloydb_v1.types.resources import InstanceView
from google.cloud.alloydb_v1.types.resources import SubscriptionType
from google.cloud.alloydb_v1.types.service import BatchCreateInstancesMetadata
from google.cloud.alloydb_v1.types.service import BatchCreateInstancesRequest
from google.cloud.alloydb_v1.types.service import BatchCreateInstancesResponse
from google.cloud.alloydb_v1.types.service import BatchCreateInstanceStatus
from google.cloud.alloydb_v1.types.service import CreateBackupRequest
from google.cloud.alloydb_v1.types.service import CreateClusterRequest
from google.cloud.alloydb_v1.types.service import CreateInstanceRequest
from google.cloud.alloydb_v1.types.service import CreateInstanceRequests
from google.cloud.alloydb_v1.types.service import CreateSecondaryClusterRequest
from google.cloud.alloydb_v1.types.service import CreateSecondaryInstanceRequest
from google.cloud.alloydb_v1.types.service import CreateUserRequest
from google.cloud.alloydb_v1.types.service import DeleteBackupRequest
from google.cloud.alloydb_v1.types.service import DeleteClusterRequest
from google.cloud.alloydb_v1.types.service import DeleteInstanceRequest
from google.cloud.alloydb_v1.types.service import DeleteUserRequest
from google.cloud.alloydb_v1.types.service import ExecuteSqlMetadata
from google.cloud.alloydb_v1.types.service import ExecuteSqlRequest
from google.cloud.alloydb_v1.types.service import ExecuteSqlResponse
from google.cloud.alloydb_v1.types.service import ExportClusterRequest
from google.cloud.alloydb_v1.types.service import ExportClusterResponse
from google.cloud.alloydb_v1.types.service import FailoverInstanceRequest
from google.cloud.alloydb_v1.types.service import GcsDestination
from google.cloud.alloydb_v1.types.service import GenerateClientCertificateRequest
from google.cloud.alloydb_v1.types.service import GenerateClientCertificateResponse
from google.cloud.alloydb_v1.types.service import GetBackupRequest
from google.cloud.alloydb_v1.types.service import GetClusterRequest
from google.cloud.alloydb_v1.types.service import GetConnectionInfoRequest
from google.cloud.alloydb_v1.types.service import GetInstanceRequest
from google.cloud.alloydb_v1.types.service import GetUserRequest
from google.cloud.alloydb_v1.types.service import ImportClusterRequest
from google.cloud.alloydb_v1.types.service import ImportClusterResponse
from google.cloud.alloydb_v1.types.service import InjectFaultRequest
from google.cloud.alloydb_v1.types.service import ListBackupsRequest
from google.cloud.alloydb_v1.types.service import ListBackupsResponse
from google.cloud.alloydb_v1.types.service import ListClustersRequest
from google.cloud.alloydb_v1.types.service import ListClustersResponse
from google.cloud.alloydb_v1.types.service import ListDatabasesRequest
from google.cloud.alloydb_v1.types.service import ListDatabasesResponse
from google.cloud.alloydb_v1.types.service import ListInstancesRequest
from google.cloud.alloydb_v1.types.service import ListInstancesResponse
from google.cloud.alloydb_v1.types.service import ListSupportedDatabaseFlagsRequest
from google.cloud.alloydb_v1.types.service import ListSupportedDatabaseFlagsResponse
from google.cloud.alloydb_v1.types.service import ListUsersRequest
from google.cloud.alloydb_v1.types.service import ListUsersResponse
from google.cloud.alloydb_v1.types.service import OperationMetadata
from google.cloud.alloydb_v1.types.service import PromoteClusterRequest
from google.cloud.alloydb_v1.types.service import RestartInstanceRequest
from google.cloud.alloydb_v1.types.service import RestoreClusterRequest
from google.cloud.alloydb_v1.types.service import SwitchoverClusterRequest
from google.cloud.alloydb_v1.types.service import UpdateBackupRequest
from google.cloud.alloydb_v1.types.service import UpdateClusterRequest
from google.cloud.alloydb_v1.types.service import UpdateInstanceRequest
from google.cloud.alloydb_v1.types.service import UpdateUserRequest
from google.cloud.alloydb_v1.types.service import UpgradeClusterRequest
from google.cloud.alloydb_v1.types.service import UpgradeClusterResponse
from google.cloud.alloydb_v1.types.service import UpgradeClusterStatus

__all__ = ('AlloyDBAdminClient',
    'AlloyDBAdminAsyncClient',
    'AlloyDBCSQLAdminClient',
    'AlloyDBCSQLAdminAsyncClient',
    'CloudSQLBackupRunSource',
    'RestoreFromCloudSQLRequest',
    'SqlResult',
    'SqlResultColumn',
    'SqlResultRow',
    'SqlResultValue',
    'AutomatedBackupPolicy',
    'Backup',
    'BackupSource',
    'Cluster',
    'ConnectionInfo',
    'ContinuousBackupConfig',
    'ContinuousBackupInfo',
    'ContinuousBackupSource',
    'Database',
    'EncryptionConfig',
    'EncryptionInfo',
    'Instance',
    'MaintenanceSchedule',
    'MaintenanceUpdatePolicy',
    'MigrationSource',
    'SslConfig',
    'SupportedDatabaseFlag',
    'User',
    'UserPassword',
    'ClusterView',
    'DatabaseVersion',
    'InstanceView',
    'SubscriptionType',
    'BatchCreateInstancesMetadata',
    'BatchCreateInstancesRequest',
    'BatchCreateInstancesResponse',
    'BatchCreateInstanceStatus',
    'CreateBackupRequest',
    'CreateClusterRequest',
    'CreateInstanceRequest',
    'CreateInstanceRequests',
    'CreateSecondaryClusterRequest',
    'CreateSecondaryInstanceRequest',
    'CreateUserRequest',
    'DeleteBackupRequest',
    'DeleteClusterRequest',
    'DeleteInstanceRequest',
    'DeleteUserRequest',
    'ExecuteSqlMetadata',
    'ExecuteSqlRequest',
    'ExecuteSqlResponse',
    'ExportClusterRequest',
    'ExportClusterResponse',
    'FailoverInstanceRequest',
    'GcsDestination',
    'GenerateClientCertificateRequest',
    'GenerateClientCertificateResponse',
    'GetBackupRequest',
    'GetClusterRequest',
    'GetConnectionInfoRequest',
    'GetInstanceRequest',
    'GetUserRequest',
    'ImportClusterRequest',
    'ImportClusterResponse',
    'InjectFaultRequest',
    'ListBackupsRequest',
    'ListBackupsResponse',
    'ListClustersRequest',
    'ListClustersResponse',
    'ListDatabasesRequest',
    'ListDatabasesResponse',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'ListSupportedDatabaseFlagsRequest',
    'ListSupportedDatabaseFlagsResponse',
    'ListUsersRequest',
    'ListUsersResponse',
    'OperationMetadata',
    'PromoteClusterRequest',
    'RestartInstanceRequest',
    'RestoreClusterRequest',
    'SwitchoverClusterRequest',
    'UpdateBackupRequest',
    'UpdateClusterRequest',
    'UpdateInstanceRequest',
    'UpdateUserRequest',
    'UpgradeClusterRequest',
    'UpgradeClusterResponse',
    'UpgradeClusterStatus',
)
