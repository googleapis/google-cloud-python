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
from google.cloud.storage_control_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.storage_control import StorageControlClient
from .services.storage_control import StorageControlAsyncClient

from .types.storage_control import AnywhereCache
from .types.storage_control import CommonLongRunningOperationMetadata
from .types.storage_control import CreateAnywhereCacheMetadata
from .types.storage_control import CreateAnywhereCacheRequest
from .types.storage_control import CreateFolderRequest
from .types.storage_control import CreateManagedFolderRequest
from .types.storage_control import DeleteFolderRequest
from .types.storage_control import DeleteManagedFolderRequest
from .types.storage_control import DisableAnywhereCacheRequest
from .types.storage_control import Folder
from .types.storage_control import GetAnywhereCacheRequest
from .types.storage_control import GetFolderIntelligenceConfigRequest
from .types.storage_control import GetFolderRequest
from .types.storage_control import GetManagedFolderRequest
from .types.storage_control import GetOrganizationIntelligenceConfigRequest
from .types.storage_control import GetProjectIntelligenceConfigRequest
from .types.storage_control import GetStorageLayoutRequest
from .types.storage_control import IntelligenceConfig
from .types.storage_control import ListAnywhereCachesRequest
from .types.storage_control import ListAnywhereCachesResponse
from .types.storage_control import ListFoldersRequest
from .types.storage_control import ListFoldersResponse
from .types.storage_control import ListManagedFoldersRequest
from .types.storage_control import ListManagedFoldersResponse
from .types.storage_control import ManagedFolder
from .types.storage_control import PauseAnywhereCacheRequest
from .types.storage_control import PendingRenameInfo
from .types.storage_control import RenameFolderMetadata
from .types.storage_control import RenameFolderRequest
from .types.storage_control import ResumeAnywhereCacheRequest
from .types.storage_control import StorageLayout
from .types.storage_control import UpdateAnywhereCacheMetadata
from .types.storage_control import UpdateAnywhereCacheRequest
from .types.storage_control import UpdateFolderIntelligenceConfigRequest
from .types.storage_control import UpdateOrganizationIntelligenceConfigRequest
from .types.storage_control import UpdateProjectIntelligenceConfigRequest

__all__ = (
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
'StorageControlClient',
'StorageLayout',
'UpdateAnywhereCacheMetadata',
'UpdateAnywhereCacheRequest',
'UpdateFolderIntelligenceConfigRequest',
'UpdateOrganizationIntelligenceConfigRequest',
'UpdateProjectIntelligenceConfigRequest',
)
