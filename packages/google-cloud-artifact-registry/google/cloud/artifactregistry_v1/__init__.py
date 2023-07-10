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
from google.cloud.artifactregistry_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.artifact_registry import (
    ArtifactRegistryAsyncClient,
    ArtifactRegistryClient,
)
from .types.apt_artifact import (
    AptArtifact,
    ImportAptArtifactsErrorInfo,
    ImportAptArtifactsGcsSource,
    ImportAptArtifactsMetadata,
    ImportAptArtifactsRequest,
    ImportAptArtifactsResponse,
)
from .types.artifact import (
    DockerImage,
    GetDockerImageRequest,
    GetMavenArtifactRequest,
    GetNpmPackageRequest,
    GetPythonPackageRequest,
    ListDockerImagesRequest,
    ListDockerImagesResponse,
    ListMavenArtifactsRequest,
    ListMavenArtifactsResponse,
    ListNpmPackagesRequest,
    ListNpmPackagesResponse,
    ListPythonPackagesRequest,
    ListPythonPackagesResponse,
    MavenArtifact,
    NpmPackage,
    PythonPackage,
)
from .types.file import File, GetFileRequest, Hash, ListFilesRequest, ListFilesResponse
from .types.package import (
    DeletePackageRequest,
    GetPackageRequest,
    ListPackagesRequest,
    ListPackagesResponse,
    Package,
)
from .types.repository import (
    CreateRepositoryRequest,
    DeleteRepositoryRequest,
    GetRepositoryRequest,
    ListRepositoriesRequest,
    ListRepositoriesResponse,
    Repository,
    UpdateRepositoryRequest,
)
from .types.service import OperationMetadata
from .types.settings import (
    GetProjectSettingsRequest,
    ProjectSettings,
    UpdateProjectSettingsRequest,
)
from .types.tag import (
    CreateTagRequest,
    DeleteTagRequest,
    GetTagRequest,
    ListTagsRequest,
    ListTagsResponse,
    Tag,
    UpdateTagRequest,
)
from .types.version import (
    BatchDeleteVersionsMetadata,
    DeleteVersionRequest,
    GetVersionRequest,
    ListVersionsRequest,
    ListVersionsResponse,
    Version,
    VersionView,
)
from .types.vpcsc_config import (
    GetVPCSCConfigRequest,
    UpdateVPCSCConfigRequest,
    VPCSCConfig,
)
from .types.yum_artifact import (
    ImportYumArtifactsErrorInfo,
    ImportYumArtifactsGcsSource,
    ImportYumArtifactsMetadata,
    ImportYumArtifactsRequest,
    ImportYumArtifactsResponse,
    YumArtifact,
)

__all__ = (
    "ArtifactRegistryAsyncClient",
    "AptArtifact",
    "ArtifactRegistryClient",
    "BatchDeleteVersionsMetadata",
    "CreateRepositoryRequest",
    "CreateTagRequest",
    "DeletePackageRequest",
    "DeleteRepositoryRequest",
    "DeleteTagRequest",
    "DeleteVersionRequest",
    "DockerImage",
    "File",
    "GetDockerImageRequest",
    "GetFileRequest",
    "GetMavenArtifactRequest",
    "GetNpmPackageRequest",
    "GetPackageRequest",
    "GetProjectSettingsRequest",
    "GetPythonPackageRequest",
    "GetRepositoryRequest",
    "GetTagRequest",
    "GetVPCSCConfigRequest",
    "GetVersionRequest",
    "Hash",
    "ImportAptArtifactsErrorInfo",
    "ImportAptArtifactsGcsSource",
    "ImportAptArtifactsMetadata",
    "ImportAptArtifactsRequest",
    "ImportAptArtifactsResponse",
    "ImportYumArtifactsErrorInfo",
    "ImportYumArtifactsGcsSource",
    "ImportYumArtifactsMetadata",
    "ImportYumArtifactsRequest",
    "ImportYumArtifactsResponse",
    "ListDockerImagesRequest",
    "ListDockerImagesResponse",
    "ListFilesRequest",
    "ListFilesResponse",
    "ListMavenArtifactsRequest",
    "ListMavenArtifactsResponse",
    "ListNpmPackagesRequest",
    "ListNpmPackagesResponse",
    "ListPackagesRequest",
    "ListPackagesResponse",
    "ListPythonPackagesRequest",
    "ListPythonPackagesResponse",
    "ListRepositoriesRequest",
    "ListRepositoriesResponse",
    "ListTagsRequest",
    "ListTagsResponse",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "MavenArtifact",
    "NpmPackage",
    "OperationMetadata",
    "Package",
    "ProjectSettings",
    "PythonPackage",
    "Repository",
    "Tag",
    "UpdateProjectSettingsRequest",
    "UpdateRepositoryRequest",
    "UpdateTagRequest",
    "UpdateVPCSCConfigRequest",
    "VPCSCConfig",
    "Version",
    "VersionView",
    "YumArtifact",
)
