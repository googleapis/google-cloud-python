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

from google.cloud.artifactregistry_v1beta2.services.artifact_registry.async_client import (
    ArtifactRegistryAsyncClient,
)
from google.cloud.artifactregistry_v1beta2.services.artifact_registry.client import (
    ArtifactRegistryClient,
)
from google.cloud.artifactregistry_v1beta2.types.file import File
from google.cloud.artifactregistry_v1beta2.types.file import GetFileRequest
from google.cloud.artifactregistry_v1beta2.types.file import Hash
from google.cloud.artifactregistry_v1beta2.types.file import ListFilesRequest
from google.cloud.artifactregistry_v1beta2.types.file import ListFilesResponse
from google.cloud.artifactregistry_v1beta2.types.package import DeletePackageRequest
from google.cloud.artifactregistry_v1beta2.types.package import GetPackageRequest
from google.cloud.artifactregistry_v1beta2.types.package import ListPackagesRequest
from google.cloud.artifactregistry_v1beta2.types.package import ListPackagesResponse
from google.cloud.artifactregistry_v1beta2.types.package import Package
from google.cloud.artifactregistry_v1beta2.types.repository import (
    CreateRepositoryRequest,
)
from google.cloud.artifactregistry_v1beta2.types.repository import (
    DeleteRepositoryRequest,
)
from google.cloud.artifactregistry_v1beta2.types.repository import GetRepositoryRequest
from google.cloud.artifactregistry_v1beta2.types.repository import (
    ListRepositoriesRequest,
)
from google.cloud.artifactregistry_v1beta2.types.repository import (
    ListRepositoriesResponse,
)
from google.cloud.artifactregistry_v1beta2.types.repository import Repository
from google.cloud.artifactregistry_v1beta2.types.repository import (
    UpdateRepositoryRequest,
)
from google.cloud.artifactregistry_v1beta2.types.service import OperationMetadata
from google.cloud.artifactregistry_v1beta2.types.tag import CreateTagRequest
from google.cloud.artifactregistry_v1beta2.types.tag import DeleteTagRequest
from google.cloud.artifactregistry_v1beta2.types.tag import GetTagRequest
from google.cloud.artifactregistry_v1beta2.types.tag import ListTagsRequest
from google.cloud.artifactregistry_v1beta2.types.tag import ListTagsResponse
from google.cloud.artifactregistry_v1beta2.types.tag import Tag
from google.cloud.artifactregistry_v1beta2.types.tag import UpdateTagRequest
from google.cloud.artifactregistry_v1beta2.types.version import DeleteVersionRequest
from google.cloud.artifactregistry_v1beta2.types.version import GetVersionRequest
from google.cloud.artifactregistry_v1beta2.types.version import ListVersionsRequest
from google.cloud.artifactregistry_v1beta2.types.version import ListVersionsResponse
from google.cloud.artifactregistry_v1beta2.types.version import Version
from google.cloud.artifactregistry_v1beta2.types.version import VersionView

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
