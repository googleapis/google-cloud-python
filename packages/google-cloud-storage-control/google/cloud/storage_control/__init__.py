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


from google.cloud.storage_control_v2.services.storage_control.async_client import (
    StorageControlAsyncClient,
)
from google.cloud.storage_control_v2.services.storage_control.client import (
    StorageControlClient,
)
from google.cloud.storage_control_v2.types.storage_control import (
    CommonLongRunningOperationMetadata,
    CreateFolderRequest,
    CreateManagedFolderRequest,
    DeleteFolderRequest,
    DeleteManagedFolderRequest,
    Folder,
    GetFolderRequest,
    GetManagedFolderRequest,
    GetStorageLayoutRequest,
    ListFoldersRequest,
    ListFoldersResponse,
    ListManagedFoldersRequest,
    ListManagedFoldersResponse,
    ManagedFolder,
    PendingRenameInfo,
    RenameFolderMetadata,
    RenameFolderRequest,
    StorageLayout,
)

__all__ = (
    "StorageControlClient",
    "StorageControlAsyncClient",
    "CommonLongRunningOperationMetadata",
    "CreateFolderRequest",
    "CreateManagedFolderRequest",
    "DeleteFolderRequest",
    "DeleteManagedFolderRequest",
    "Folder",
    "GetFolderRequest",
    "GetManagedFolderRequest",
    "GetStorageLayoutRequest",
    "ListFoldersRequest",
    "ListFoldersResponse",
    "ListManagedFoldersRequest",
    "ListManagedFoldersResponse",
    "ManagedFolder",
    "PendingRenameInfo",
    "RenameFolderMetadata",
    "RenameFolderRequest",
    "StorageLayout",
)
