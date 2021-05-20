# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from .services.artifact_registry import ArtifactRegistryClient
from .services.artifact_registry import ArtifactRegistryAsyncClient

from .types.file import File
from .types.file import GetFileRequest
from .types.file import Hash
from .types.file import ListFilesRequest
from .types.file import ListFilesResponse
from .types.package import DeletePackageRequest
from .types.package import GetPackageRequest
from .types.package import ListPackagesRequest
from .types.package import ListPackagesResponse
from .types.package import Package
from .types.repository import CreateRepositoryRequest
from .types.repository import DeleteRepositoryRequest
from .types.repository import GetRepositoryRequest
from .types.repository import ListRepositoriesRequest
from .types.repository import ListRepositoriesResponse
from .types.repository import Repository
from .types.repository import UpdateRepositoryRequest
from .types.service import OperationMetadata
from .types.tag import CreateTagRequest
from .types.tag import DeleteTagRequest
from .types.tag import GetTagRequest
from .types.tag import ListTagsRequest
from .types.tag import ListTagsResponse
from .types.tag import Tag
from .types.tag import UpdateTagRequest
from .types.version import DeleteVersionRequest
from .types.version import GetVersionRequest
from .types.version import ListVersionsRequest
from .types.version import ListVersionsResponse
from .types.version import Version
from .types.version import VersionView

__all__ = (
    "ArtifactRegistryAsyncClient",
    "ArtifactRegistryClient",
    "CreateRepositoryRequest",
    "CreateTagRequest",
    "DeletePackageRequest",
    "DeleteRepositoryRequest",
    "DeleteTagRequest",
    "DeleteVersionRequest",
    "File",
    "GetFileRequest",
    "GetPackageRequest",
    "GetRepositoryRequest",
    "GetTagRequest",
    "GetVersionRequest",
    "Hash",
    "ListFilesRequest",
    "ListFilesResponse",
    "ListPackagesRequest",
    "ListPackagesResponse",
    "ListRepositoriesRequest",
    "ListRepositoriesResponse",
    "ListTagsRequest",
    "ListTagsResponse",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "OperationMetadata",
    "Package",
    "Repository",
    "Tag",
    "UpdateRepositoryRequest",
    "UpdateTagRequest",
    "Version",
    "VersionView",
)
