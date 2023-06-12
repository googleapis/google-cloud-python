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
from google.cloud.alloydb import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.alloydb_v1beta.services.alloy_db_admin.client import AlloyDBAdminClient
from google.cloud.alloydb_v1beta.services.alloy_db_admin.async_client import AlloyDBAdminAsyncClient

from google.cloud.alloydb_v1beta.types.resources import AutomatedBackupPolicy
from google.cloud.alloydb_v1beta.types.resources import Backup
from google.cloud.alloydb_v1beta.types.resources import BackupSource
from google.cloud.alloydb_v1beta.types.resources import Cluster
from google.cloud.alloydb_v1beta.types.resources import ConnectionInfo
from google.cloud.alloydb_v1beta.types.resources import ContinuousBackupConfig
from google.cloud.alloydb_v1beta.types.resources import ContinuousBackupInfo
from google.cloud.alloydb_v1beta.types.resources import ContinuousBackupSource
from google.cloud.alloydb_v1beta.types.resources import EncryptionConfig
from google.cloud.alloydb_v1beta.types.resources import EncryptionInfo
from google.cloud.alloydb_v1beta.types.resources import Instance
from google.cloud.alloydb_v1beta.types.resources import MigrationSource
from google.cloud.alloydb_v1beta.types.resources import SslConfig
from google.cloud.alloydb_v1beta.types.resources import SupportedDatabaseFlag
from google.cloud.alloydb_v1beta.types.resources import UserPassword
from google.cloud.alloydb_v1beta.types.resources import DatabaseVersion
from google.cloud.alloydb_v1beta.types.resources import InstanceView
from google.cloud.alloydb_v1beta.types.service import BatchCreateInstancesMetadata
from google.cloud.alloydb_v1beta.types.service import BatchCreateInstancesRequest
from google.cloud.alloydb_v1beta.types.service import BatchCreateInstancesResponse
from google.cloud.alloydb_v1beta.types.service import BatchCreateInstanceStatus
from google.cloud.alloydb_v1beta.types.service import CreateBackupRequest
from google.cloud.alloydb_v1beta.types.service import CreateClusterRequest
from google.cloud.alloydb_v1beta.types.service import CreateInstanceRequest
from google.cloud.alloydb_v1beta.types.service import CreateInstanceRequests
from google.cloud.alloydb_v1beta.types.service import CreateSecondaryClusterRequest
from google.cloud.alloydb_v1beta.types.service import CreateSecondaryInstanceRequest
from google.cloud.alloydb_v1beta.types.service import DeleteBackupRequest
from google.cloud.alloydb_v1beta.types.service import DeleteClusterRequest
from google.cloud.alloydb_v1beta.types.service import DeleteInstanceRequest
from google.cloud.alloydb_v1beta.types.service import FailoverInstanceRequest
from google.cloud.alloydb_v1beta.types.service import GenerateClientCertificateRequest
from google.cloud.alloydb_v1beta.types.service import GenerateClientCertificateResponse
from google.cloud.alloydb_v1beta.types.service import GetBackupRequest
from google.cloud.alloydb_v1beta.types.service import GetClusterRequest
from google.cloud.alloydb_v1beta.types.service import GetConnectionInfoRequest
from google.cloud.alloydb_v1beta.types.service import GetInstanceRequest
from google.cloud.alloydb_v1beta.types.service import ListBackupsRequest
from google.cloud.alloydb_v1beta.types.service import ListBackupsResponse
from google.cloud.alloydb_v1beta.types.service import ListClustersRequest
from google.cloud.alloydb_v1beta.types.service import ListClustersResponse
from google.cloud.alloydb_v1beta.types.service import ListInstancesRequest
from google.cloud.alloydb_v1beta.types.service import ListInstancesResponse
from google.cloud.alloydb_v1beta.types.service import ListSupportedDatabaseFlagsRequest
from google.cloud.alloydb_v1beta.types.service import ListSupportedDatabaseFlagsResponse
from google.cloud.alloydb_v1beta.types.service import OperationMetadata
from google.cloud.alloydb_v1beta.types.service import PromoteClusterRequest
from google.cloud.alloydb_v1beta.types.service import RestartInstanceRequest
from google.cloud.alloydb_v1beta.types.service import RestoreClusterRequest
from google.cloud.alloydb_v1beta.types.service import UpdateBackupRequest
from google.cloud.alloydb_v1beta.types.service import UpdateClusterRequest
from google.cloud.alloydb_v1beta.types.service import UpdateInstanceRequest

__all__ = ('AlloyDBAdminClient',
    'AlloyDBAdminAsyncClient',
    'AutomatedBackupPolicy',
    'Backup',
    'BackupSource',
    'Cluster',
    'ConnectionInfo',
    'ContinuousBackupConfig',
    'ContinuousBackupInfo',
    'ContinuousBackupSource',
    'EncryptionConfig',
    'EncryptionInfo',
    'Instance',
    'MigrationSource',
    'SslConfig',
    'SupportedDatabaseFlag',
    'UserPassword',
    'DatabaseVersion',
    'InstanceView',
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
    'DeleteBackupRequest',
    'DeleteClusterRequest',
    'DeleteInstanceRequest',
    'FailoverInstanceRequest',
    'GenerateClientCertificateRequest',
    'GenerateClientCertificateResponse',
    'GetBackupRequest',
    'GetClusterRequest',
    'GetConnectionInfoRequest',
    'GetInstanceRequest',
    'ListBackupsRequest',
    'ListBackupsResponse',
    'ListClustersRequest',
    'ListClustersResponse',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'ListSupportedDatabaseFlagsRequest',
    'ListSupportedDatabaseFlagsResponse',
    'OperationMetadata',
    'PromoteClusterRequest',
    'RestartInstanceRequest',
    'RestoreClusterRequest',
    'UpdateBackupRequest',
    'UpdateClusterRequest',
    'UpdateInstanceRequest',
)
