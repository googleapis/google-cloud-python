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

from google.cloud.artifactregistry_v1.services.artifact_registry.async_client import (
    ArtifactRegistryAsyncClient,
)
from google.cloud.artifactregistry_v1.services.artifact_registry.client import (
    ArtifactRegistryClient,
)
from google.cloud.artifactregistry_v1.types.apt_artifact import (
    AptArtifact,
    ImportAptArtifactsErrorInfo,
    ImportAptArtifactsGcsSource,
    ImportAptArtifactsMetadata,
    ImportAptArtifactsRequest,
    ImportAptArtifactsResponse,
)
from google.cloud.artifactregistry_v1.types.artifact import (
    DockerImage,
    GetDockerImageRequest,
    ListDockerImagesRequest,
    ListDockerImagesResponse,
)
from google.cloud.artifactregistry_v1.types.file import (
    File,
    GetFileRequest,
    Hash,
    ListFilesRequest,
    ListFilesResponse,
)
from google.cloud.artifactregistry_v1.types.package import (
    DeletePackageRequest,
    GetPackageRequest,
    ListPackagesRequest,
    ListPackagesResponse,
    Package,
)
from google.cloud.artifactregistry_v1.types.repository import (
    CreateRepositoryRequest,
    DeleteRepositoryRequest,
    GetRepositoryRequest,
    ListRepositoriesRequest,
    ListRepositoriesResponse,
    Repository,
    UpdateRepositoryRequest,
)
from google.cloud.artifactregistry_v1.types.service import OperationMetadata
from google.cloud.artifactregistry_v1.types.settings import (
    GetProjectSettingsRequest,
    ProjectSettings,
    UpdateProjectSettingsRequest,
)
from google.cloud.artifactregistry_v1.types.tag import (
    CreateTagRequest,
    DeleteTagRequest,
    GetTagRequest,
    ListTagsRequest,
    ListTagsResponse,
    Tag,
    UpdateTagRequest,
)
from google.cloud.artifactregistry_v1.types.version import (
    DeleteVersionRequest,
    GetVersionRequest,
    ListVersionsRequest,
    ListVersionsResponse,
    Version,
    VersionView,
)
from google.cloud.artifactregistry_v1.types.yum_artifact import (
    ImportYumArtifactsErrorInfo,
    ImportYumArtifactsGcsSource,
    ImportYumArtifactsMetadata,
    ImportYumArtifactsRequest,
    ImportYumArtifactsResponse,
    YumArtifact,
)

__all__ = (
    "ArtifactRegistryClient",
    "ArtifactRegistryAsyncClient",
    "AptArtifact",
    "ImportAptArtifactsErrorInfo",
    "ImportAptArtifactsGcsSource",
    "ImportAptArtifactsMetadata",
    "ImportAptArtifactsRequest",
    "ImportAptArtifactsResponse",
    "DockerImage",
    "GetDockerImageRequest",
    "ListDockerImagesRequest",
    "ListDockerImagesResponse",
    "File",
    "GetFileRequest",
    "Hash",
    "ListFilesRequest",
    "ListFilesResponse",
    "DeletePackageRequest",
    "GetPackageRequest",
    "ListPackagesRequest",
    "ListPackagesResponse",
    "Package",
    "CreateRepositoryRequest",
    "DeleteRepositoryRequest",
    "GetRepositoryRequest",
    "ListRepositoriesRequest",
    "ListRepositoriesResponse",
    "Repository",
    "UpdateRepositoryRequest",
    "OperationMetadata",
    "GetProjectSettingsRequest",
    "ProjectSettings",
    "UpdateProjectSettingsRequest",
    "CreateTagRequest",
    "DeleteTagRequest",
    "GetTagRequest",
    "ListTagsRequest",
    "ListTagsResponse",
    "Tag",
    "UpdateTagRequest",
    "DeleteVersionRequest",
    "GetVersionRequest",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "Version",
    "VersionView",
    "ImportYumArtifactsErrorInfo",
    "ImportYumArtifactsGcsSource",
    "ImportYumArtifactsMetadata",
    "ImportYumArtifactsRequest",
    "ImportYumArtifactsResponse",
    "YumArtifact",
)
