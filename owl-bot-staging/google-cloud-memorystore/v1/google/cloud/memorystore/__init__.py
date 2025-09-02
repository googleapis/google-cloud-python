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
from google.cloud.memorystore import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.memorystore_v1.services.memorystore.client import MemorystoreClient

from google.cloud.memorystore_v1.types.memorystore import AutomatedBackupConfig
from google.cloud.memorystore_v1.types.memorystore import Backup
from google.cloud.memorystore_v1.types.memorystore import BackupCollection
from google.cloud.memorystore_v1.types.memorystore import BackupFile
from google.cloud.memorystore_v1.types.memorystore import BackupInstanceRequest
from google.cloud.memorystore_v1.types.memorystore import CertificateAuthority
from google.cloud.memorystore_v1.types.memorystore import CreateInstanceRequest
from google.cloud.memorystore_v1.types.memorystore import CrossInstanceReplicationConfig
from google.cloud.memorystore_v1.types.memorystore import DeleteBackupRequest
from google.cloud.memorystore_v1.types.memorystore import DeleteInstanceRequest
from google.cloud.memorystore_v1.types.memorystore import DiscoveryEndpoint
from google.cloud.memorystore_v1.types.memorystore import ExportBackupRequest
from google.cloud.memorystore_v1.types.memorystore import GetBackupCollectionRequest
from google.cloud.memorystore_v1.types.memorystore import GetBackupRequest
from google.cloud.memorystore_v1.types.memorystore import GetCertificateAuthorityRequest
from google.cloud.memorystore_v1.types.memorystore import GetInstanceRequest
from google.cloud.memorystore_v1.types.memorystore import Instance
from google.cloud.memorystore_v1.types.memorystore import ListBackupCollectionsRequest
from google.cloud.memorystore_v1.types.memorystore import ListBackupCollectionsResponse
from google.cloud.memorystore_v1.types.memorystore import ListBackupsRequest
from google.cloud.memorystore_v1.types.memorystore import ListBackupsResponse
from google.cloud.memorystore_v1.types.memorystore import ListInstancesRequest
from google.cloud.memorystore_v1.types.memorystore import ListInstancesResponse
from google.cloud.memorystore_v1.types.memorystore import MaintenancePolicy
from google.cloud.memorystore_v1.types.memorystore import MaintenanceSchedule
from google.cloud.memorystore_v1.types.memorystore import NodeConfig
from google.cloud.memorystore_v1.types.memorystore import OperationMetadata
from google.cloud.memorystore_v1.types.memorystore import PersistenceConfig
from google.cloud.memorystore_v1.types.memorystore import PscAttachmentDetail
from google.cloud.memorystore_v1.types.memorystore import PscAutoConnection
from google.cloud.memorystore_v1.types.memorystore import PscConnection
from google.cloud.memorystore_v1.types.memorystore import RescheduleMaintenanceRequest
from google.cloud.memorystore_v1.types.memorystore import UpdateInstanceRequest
from google.cloud.memorystore_v1.types.memorystore import WeeklyMaintenanceWindow
from google.cloud.memorystore_v1.types.memorystore import ZoneDistributionConfig
from google.cloud.memorystore_v1.types.memorystore import ConnectionType
from google.cloud.memorystore_v1.types.memorystore import PscConnectionStatus

__all__ = ('MemorystoreClient',
    'AutomatedBackupConfig',
    'Backup',
    'BackupCollection',
    'BackupFile',
    'BackupInstanceRequest',
    'CertificateAuthority',
    'CreateInstanceRequest',
    'CrossInstanceReplicationConfig',
    'DeleteBackupRequest',
    'DeleteInstanceRequest',
    'DiscoveryEndpoint',
    'ExportBackupRequest',
    'GetBackupCollectionRequest',
    'GetBackupRequest',
    'GetCertificateAuthorityRequest',
    'GetInstanceRequest',
    'Instance',
    'ListBackupCollectionsRequest',
    'ListBackupCollectionsResponse',
    'ListBackupsRequest',
    'ListBackupsResponse',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'MaintenancePolicy',
    'MaintenanceSchedule',
    'NodeConfig',
    'OperationMetadata',
    'PersistenceConfig',
    'PscAttachmentDetail',
    'PscAutoConnection',
    'PscConnection',
    'RescheduleMaintenanceRequest',
    'UpdateInstanceRequest',
    'WeeklyMaintenanceWindow',
    'ZoneDistributionConfig',
    'ConnectionType',
    'PscConnectionStatus',
)
