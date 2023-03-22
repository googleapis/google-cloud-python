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
from google.cloud.alloydb_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.alloy_db_admin import AlloyDBAdminClient
from .services.alloy_db_admin import AlloyDBAdminAsyncClient

from .types.resources import AutomatedBackupPolicy
from .types.resources import Backup
from .types.resources import BackupSource
from .types.resources import Cluster
from .types.resources import ConnectionInfo
from .types.resources import ContinuousBackupConfig
from .types.resources import ContinuousBackupInfo
from .types.resources import ContinuousBackupSource
from .types.resources import EncryptionConfig
from .types.resources import EncryptionInfo
from .types.resources import Instance
from .types.resources import MigrationSource
from .types.resources import SslConfig
from .types.resources import SupportedDatabaseFlag
from .types.resources import UserPassword
from .types.resources import DatabaseVersion
from .types.resources import InstanceView
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
from .types.service import DeleteBackupRequest
from .types.service import DeleteClusterRequest
from .types.service import DeleteInstanceRequest
from .types.service import FailoverInstanceRequest
from .types.service import GenerateClientCertificateRequest
from .types.service import GenerateClientCertificateResponse
from .types.service import GetBackupRequest
from .types.service import GetClusterRequest
from .types.service import GetConnectionInfoRequest
from .types.service import GetInstanceRequest
from .types.service import ListBackupsRequest
from .types.service import ListBackupsResponse
from .types.service import ListClustersRequest
from .types.service import ListClustersResponse
from .types.service import ListInstancesRequest
from .types.service import ListInstancesResponse
from .types.service import ListSupportedDatabaseFlagsRequest
from .types.service import ListSupportedDatabaseFlagsResponse
from .types.service import OperationMetadata
from .types.service import PromoteClusterRequest
from .types.service import RestartInstanceRequest
from .types.service import RestoreClusterRequest
from .types.service import UpdateBackupRequest
from .types.service import UpdateClusterRequest
from .types.service import UpdateInstanceRequest

__all__ = (
    'AlloyDBAdminAsyncClient',
'AlloyDBAdminClient',
'AutomatedBackupPolicy',
'Backup',
'BackupSource',
'BatchCreateInstanceStatus',
'BatchCreateInstancesMetadata',
'BatchCreateInstancesRequest',
'BatchCreateInstancesResponse',
'Cluster',
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
'DatabaseVersion',
'DeleteBackupRequest',
'DeleteClusterRequest',
'DeleteInstanceRequest',
'EncryptionConfig',
'EncryptionInfo',
'FailoverInstanceRequest',
'GenerateClientCertificateRequest',
'GenerateClientCertificateResponse',
'GetBackupRequest',
'GetClusterRequest',
'GetConnectionInfoRequest',
'GetInstanceRequest',
'Instance',
'InstanceView',
'ListBackupsRequest',
'ListBackupsResponse',
'ListClustersRequest',
'ListClustersResponse',
'ListInstancesRequest',
'ListInstancesResponse',
'ListSupportedDatabaseFlagsRequest',
'ListSupportedDatabaseFlagsResponse',
'MigrationSource',
'OperationMetadata',
'PromoteClusterRequest',
'RestartInstanceRequest',
'RestoreClusterRequest',
'SslConfig',
'SupportedDatabaseFlag',
'UpdateBackupRequest',
'UpdateClusterRequest',
'UpdateInstanceRequest',
'UserPassword',
)
