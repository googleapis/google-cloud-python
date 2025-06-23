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
from google.cloud.storage_control import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.storage_control_v2.services.storage_control.client import StorageControlClient
from google.cloud.storage_control_v2.services.storage_control.async_client import StorageControlAsyncClient

from google.cloud.storage_control_v2.types.storage_control import AnywhereCache
from google.cloud.storage_control_v2.types.storage_control import CommonLongRunningOperationMetadata
from google.cloud.storage_control_v2.types.storage_control import CreateAnywhereCacheMetadata
from google.cloud.storage_control_v2.types.storage_control import CreateAnywhereCacheRequest
from google.cloud.storage_control_v2.types.storage_control import CreateFolderRequest
from google.cloud.storage_control_v2.types.storage_control import CreateManagedFolderRequest
from google.cloud.storage_control_v2.types.storage_control import DeleteFolderRequest
from google.cloud.storage_control_v2.types.storage_control import DeleteManagedFolderRequest
from google.cloud.storage_control_v2.types.storage_control import DisableAnywhereCacheRequest
from google.cloud.storage_control_v2.types.storage_control import Folder
from google.cloud.storage_control_v2.types.storage_control import GetAnywhereCacheRequest
from google.cloud.storage_control_v2.types.storage_control import GetFolderIntelligenceConfigRequest
from google.cloud.storage_control_v2.types.storage_control import GetFolderRequest
from google.cloud.storage_control_v2.types.storage_control import GetManagedFolderRequest
from google.cloud.storage_control_v2.types.storage_control import GetOrganizationIntelligenceConfigRequest
from google.cloud.storage_control_v2.types.storage_control import GetProjectIntelligenceConfigRequest
from google.cloud.storage_control_v2.types.storage_control import GetStorageLayoutRequest
from google.cloud.storage_control_v2.types.storage_control import IntelligenceConfig
from google.cloud.storage_control_v2.types.storage_control import ListAnywhereCachesRequest
from google.cloud.storage_control_v2.types.storage_control import ListAnywhereCachesResponse
from google.cloud.storage_control_v2.types.storage_control import ListFoldersRequest
from google.cloud.storage_control_v2.types.storage_control import ListFoldersResponse
from google.cloud.storage_control_v2.types.storage_control import ListManagedFoldersRequest
from google.cloud.storage_control_v2.types.storage_control import ListManagedFoldersResponse
from google.cloud.storage_control_v2.types.storage_control import ManagedFolder
from google.cloud.storage_control_v2.types.storage_control import PauseAnywhereCacheRequest
from google.cloud.storage_control_v2.types.storage_control import PendingRenameInfo
from google.cloud.storage_control_v2.types.storage_control import RenameFolderMetadata
from google.cloud.storage_control_v2.types.storage_control import RenameFolderRequest
from google.cloud.storage_control_v2.types.storage_control import ResumeAnywhereCacheRequest
from google.cloud.storage_control_v2.types.storage_control import StorageLayout
from google.cloud.storage_control_v2.types.storage_control import UpdateAnywhereCacheMetadata
from google.cloud.storage_control_v2.types.storage_control import UpdateAnywhereCacheRequest
from google.cloud.storage_control_v2.types.storage_control import UpdateFolderIntelligenceConfigRequest
from google.cloud.storage_control_v2.types.storage_control import UpdateOrganizationIntelligenceConfigRequest
from google.cloud.storage_control_v2.types.storage_control import UpdateProjectIntelligenceConfigRequest

__all__ = ('StorageControlClient',
    'StorageControlAsyncClient',
    'AnywhereCache',
    'CommonLongRunningOperationMetadata',
    'CreateAnywhereCacheMetadata',
    'CreateAnywhereCacheRequest',
    'CreateFolderRequest',
    'CreateManagedFolderRequest',
    'DeleteFolderRequest',
    'DeleteManagedFolderRequest',
    'DisableAnywhereCacheRequest',
    'Folder',
    'GetAnywhereCacheRequest',
    'GetFolderIntelligenceConfigRequest',
    'GetFolderRequest',
    'GetManagedFolderRequest',
    'GetOrganizationIntelligenceConfigRequest',
    'GetProjectIntelligenceConfigRequest',
    'GetStorageLayoutRequest',
    'IntelligenceConfig',
    'ListAnywhereCachesRequest',
    'ListAnywhereCachesResponse',
    'ListFoldersRequest',
    'ListFoldersResponse',
    'ListManagedFoldersRequest',
    'ListManagedFoldersResponse',
    'ManagedFolder',
    'PauseAnywhereCacheRequest',
    'PendingRenameInfo',
    'RenameFolderMetadata',
    'RenameFolderRequest',
    'ResumeAnywhereCacheRequest',
    'StorageLayout',
    'UpdateAnywhereCacheMetadata',
    'UpdateAnywhereCacheRequest',
    'UpdateFolderIntelligenceConfigRequest',
    'UpdateOrganizationIntelligenceConfigRequest',
    'UpdateProjectIntelligenceConfigRequest',
)
