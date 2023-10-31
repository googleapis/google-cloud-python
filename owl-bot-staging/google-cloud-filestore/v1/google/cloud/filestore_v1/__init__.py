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
from google.cloud.filestore_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_filestore_manager import CloudFilestoreManagerClient
from .services.cloud_filestore_manager import CloudFilestoreManagerAsyncClient

from .types.cloud_filestore_service import Backup
from .types.cloud_filestore_service import CreateBackupRequest
from .types.cloud_filestore_service import CreateInstanceRequest
from .types.cloud_filestore_service import CreateSnapshotRequest
from .types.cloud_filestore_service import DeleteBackupRequest
from .types.cloud_filestore_service import DeleteInstanceRequest
from .types.cloud_filestore_service import DeleteSnapshotRequest
from .types.cloud_filestore_service import FileShareConfig
from .types.cloud_filestore_service import GetBackupRequest
from .types.cloud_filestore_service import GetInstanceRequest
from .types.cloud_filestore_service import GetSnapshotRequest
from .types.cloud_filestore_service import Instance
from .types.cloud_filestore_service import ListBackupsRequest
from .types.cloud_filestore_service import ListBackupsResponse
from .types.cloud_filestore_service import ListInstancesRequest
from .types.cloud_filestore_service import ListInstancesResponse
from .types.cloud_filestore_service import ListSnapshotsRequest
from .types.cloud_filestore_service import ListSnapshotsResponse
from .types.cloud_filestore_service import NetworkConfig
from .types.cloud_filestore_service import NfsExportOptions
from .types.cloud_filestore_service import RestoreInstanceRequest
from .types.cloud_filestore_service import Snapshot
from .types.cloud_filestore_service import UpdateBackupRequest
from .types.cloud_filestore_service import UpdateInstanceRequest
from .types.cloud_filestore_service import UpdateSnapshotRequest

__all__ = (
    'CloudFilestoreManagerAsyncClient',
'Backup',
'CloudFilestoreManagerClient',
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
