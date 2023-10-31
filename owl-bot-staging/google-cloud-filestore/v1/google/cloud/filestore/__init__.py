# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.filestore import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.filestore_v1.services.cloud_filestore_manager.client import CloudFilestoreManagerClient
from google.cloud.filestore_v1.services.cloud_filestore_manager.async_client import CloudFilestoreManagerAsyncClient

from google.cloud.filestore_v1.types.cloud_filestore_service import Backup
from google.cloud.filestore_v1.types.cloud_filestore_service import CreateBackupRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import CreateInstanceRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import CreateSnapshotRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import DeleteBackupRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import DeleteInstanceRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import DeleteSnapshotRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import FileShareConfig
from google.cloud.filestore_v1.types.cloud_filestore_service import GetBackupRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import GetInstanceRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import GetSnapshotRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import Instance
from google.cloud.filestore_v1.types.cloud_filestore_service import ListBackupsRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import ListBackupsResponse
from google.cloud.filestore_v1.types.cloud_filestore_service import ListInstancesRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import ListInstancesResponse
from google.cloud.filestore_v1.types.cloud_filestore_service import ListSnapshotsRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import ListSnapshotsResponse
from google.cloud.filestore_v1.types.cloud_filestore_service import NetworkConfig
from google.cloud.filestore_v1.types.cloud_filestore_service import NfsExportOptions
from google.cloud.filestore_v1.types.cloud_filestore_service import RestoreInstanceRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import Snapshot
from google.cloud.filestore_v1.types.cloud_filestore_service import UpdateBackupRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import UpdateInstanceRequest
from google.cloud.filestore_v1.types.cloud_filestore_service import UpdateSnapshotRequest

__all__ = ('CloudFilestoreManagerClient',
    'CloudFilestoreManagerAsyncClient',
    'Backup',
    'CreateBackupRequest',
    'CreateInstanceRequest',
    'CreateSnapshotRequest',
    'DeleteBackupRequest',
    'DeleteInstanceRequest',
    'DeleteSnapshotRequest',
    'FileShareConfig',
    'GetBackupRequest',
    'GetInstanceRequest',
    'GetSnapshotRequest',
    'Instance',
    'ListBackupsRequest',
    'ListBackupsResponse',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'ListSnapshotsRequest',
    'ListSnapshotsResponse',
    'NetworkConfig',
    'NfsExportOptions',
    'RestoreInstanceRequest',
    'Snapshot',
    'UpdateBackupRequest',
    'UpdateInstanceRequest',
    'UpdateSnapshotRequest',
)
