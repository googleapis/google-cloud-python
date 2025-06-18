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
from google.cloud.alloydb_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.alloy_db_admin import AlloyDBAdminClient
from .services.alloy_db_admin import AlloyDBAdminAsyncClient
from .services.alloy_dbcsql_admin import AlloyDBCSQLAdminClient
from .services.alloy_dbcsql_admin import AlloyDBCSQLAdminAsyncClient

from .types.csql_resources import CloudSQLBackupRunSource
from .types.csql_service import RestoreFromCloudSQLRequest
from .types.data_model import SqlResult
from .types.data_model import SqlResultColumn
from .types.data_model import SqlResultRow
from .types.data_model import SqlResultValue
from .types.gemini import GCAInstanceConfig
from .types.gemini import GeminiClusterConfig
from .types.gemini import GeminiInstanceConfig
from .types.gemini import GCAEntitlementType
from .types.resources import AutomatedBackupPolicy
from .types.resources import Backup
from .types.resources import BackupSource
from .types.resources import Cluster
from .types.resources import ConnectionInfo
from .types.resources import ContinuousBackupConfig
from .types.resources import ContinuousBackupInfo
from .types.resources import ContinuousBackupSource
from .types.resources import Database
from .types.resources import EncryptionConfig
from .types.resources import EncryptionInfo
from .types.resources import Instance
from .types.resources import MaintenanceSchedule
from .types.resources import MaintenanceUpdatePolicy
from .types.resources import MigrationSource
from .types.resources import SslConfig
from .types.resources import SupportedDatabaseFlag
from .types.resources import User
from .types.resources import UserPassword
from .types.resources import ClusterView
from .types.resources import DatabaseVersion
from .types.resources import InstanceView
from .types.resources import SubscriptionType
from .types.service import BatchCreateInstancesMetadata
from .types.service import BatchCreateInstancesRequest
from .types.service import BatchCreateInstancesResponse
from .types.service import BatchCreateInstanceStatus
from .types.service import CreateBackupRequest
from .types.service import CreateClusterRequest
from .types.service import CreateInstanceRequest
from .types.service import CreateInstanceRequests
from .types.service import CreateSecondaryClusterRequest
from .types.service import CreateSecondaryInstanceRequest
from .types.service import CreateUserRequest
from .types.service import DeleteBackupRequest
from .types.service import DeleteClusterRequest
from .types.service import DeleteInstanceRequest
from .types.service import DeleteUserRequest
from .types.service import ExecuteSqlMetadata
from .types.service import ExecuteSqlRequest
from .types.service import ExecuteSqlResponse
from .types.service import ExportClusterRequest
from .types.service import ExportClusterResponse
from .types.service import FailoverInstanceRequest
from .types.service import GcsDestination
from .types.service import GenerateClientCertificateRequest
from .types.service import GenerateClientCertificateResponse
from .types.service import GetBackupRequest
from .types.service import GetClusterRequest
from .types.service import GetConnectionInfoRequest
from .types.service import GetInstanceRequest
from .types.service import GetUserRequest
from .types.service import ImportClusterRequest
from .types.service import ImportClusterResponse
from .types.service import InjectFaultRequest
from .types.service import ListBackupsRequest
from .types.service import ListBackupsResponse
from .types.service import ListClustersRequest
from .types.service import ListClustersResponse
from .types.service import ListDatabasesRequest
from .types.service import ListDatabasesResponse
from .types.service import ListInstancesRequest
from .types.service import ListInstancesResponse
from .types.service import ListSupportedDatabaseFlagsRequest
from .types.service import ListSupportedDatabaseFlagsResponse
from .types.service import ListUsersRequest
from .types.service import ListUsersResponse
from .types.service import OperationMetadata
from .types.service import PromoteClusterRequest
from .types.service import PromoteClusterStatus
from .types.service import RestartInstanceRequest
from .types.service import RestoreClusterRequest
from .types.service import SwitchoverClusterRequest
from .types.service import UpdateBackupRequest
from .types.service import UpdateClusterRequest
from .types.service import UpdateInstanceRequest
from .types.service import UpdateUserRequest
from .types.service import UpgradeClusterRequest
from .types.service import UpgradeClusterResponse
from .types.service import UpgradeClusterStatus

__all__ = (
    'AlloyDBAdminAsyncClient',
    'AlloyDBCSQLAdminAsyncClient',
'AlloyDBAdminClient',
'AlloyDBCSQLAdminClient',
'AutomatedBackupPolicy',
'Backup',
'BackupSource',
'BatchCreateInstanceStatus',
'BatchCreateInstancesMetadata',
'BatchCreateInstancesRequest',
'BatchCreateInstancesResponse',
'CloudSQLBackupRunSource',
'Cluster',
'ClusterView',
'ConnectionInfo',
'ContinuousBackupConfig',
'ContinuousBackupInfo',
'ContinuousBackupSource',
'CreateBackupRequest',
'CreateClusterRequest',
'CreateInstanceRequest',
'CreateInstanceRequests',
'CreateSecondaryClusterRequest',
'CreateSecondaryInstanceRequest',
'CreateUserRequest',
'Database',
'DatabaseVersion',
'DeleteBackupRequest',
'DeleteClusterRequest',
'DeleteInstanceRequest',
'DeleteUserRequest',
'EncryptionConfig',
'EncryptionInfo',
'ExecuteSqlMetadata',
'ExecuteSqlRequest',
'ExecuteSqlResponse',
'ExportClusterRequest',
'ExportClusterResponse',
'FailoverInstanceRequest',
'GCAEntitlementType',
'GCAInstanceConfig',
'GcsDestination',
'GeminiClusterConfig',
'GeminiInstanceConfig',
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
'Instance',
'InstanceView',
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
'MaintenanceSchedule',
'MaintenanceUpdatePolicy',
'MigrationSource',
'OperationMetadata',
'PromoteClusterRequest',
'PromoteClusterStatus',
'RestartInstanceRequest',
'RestoreClusterRequest',
'RestoreFromCloudSQLRequest',
'SqlResult',
'SqlResultColumn',
'SqlResultRow',
'SqlResultValue',
'SslConfig',
'SubscriptionType',
'SupportedDatabaseFlag',
'SwitchoverClusterRequest',
'UpdateBackupRequest',
'UpdateClusterRequest',
'UpdateInstanceRequest',
'UpdateUserRequest',
'UpgradeClusterRequest',
'UpgradeClusterResponse',
'UpgradeClusterStatus',
'User',
'UserPassword',
)
