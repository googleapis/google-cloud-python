# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from .types.storage_control import CommonLongRunningOperationMetadata
from .types.storage_control import CreateFolderRequest
from .types.storage_control import CreateManagedFolderRequest
from .types.storage_control import DeleteFolderRequest
from .types.storage_control import DeleteManagedFolderRequest
from .types.storage_control import Folder
from .types.storage_control import GetFolderRequest
from .types.storage_control import GetManagedFolderRequest
from .types.storage_control import GetStorageLayoutRequest
from .types.storage_control import ListFoldersRequest
from .types.storage_control import ListFoldersResponse
from .types.storage_control import ListManagedFoldersRequest
from .types.storage_control import ListManagedFoldersResponse
from .types.storage_control import ManagedFolder
from .types.storage_control import PendingRenameInfo
from .types.storage_control import RenameFolderMetadata
from .types.storage_control import RenameFolderRequest
from .types.storage_control import StorageLayout

__all__ = (
    'StorageControlAsyncClient',
'CommonLongRunningOperationMetadata',
'CreateFolderRequest',
'CreateManagedFolderRequest',
'DeleteFolderRequest',
'DeleteManagedFolderRequest',
'Folder',
'GetFolderRequest',
'GetManagedFolderRequest',
'GetStorageLayoutRequest',
'ListFoldersRequest',
'ListFoldersResponse',
'ListManagedFoldersRequest',
'ListManagedFoldersResponse',
'ManagedFolder',
'PendingRenameInfo',
'RenameFolderMetadata',
'RenameFolderRequest',
'StorageControlClient',
'StorageLayout',
)
