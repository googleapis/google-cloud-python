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
from .types.attachment import (
    Attachment,
    CreateAttachmentRequest,
    DeleteAttachmentRequest,
    GetAttachmentRequest,
    ListAttachmentsRequest,
    ListAttachmentsResponse,
)
from .types.file import (
    DeleteFileRequest,
    File,
    GetFileRequest,
    Hash,
    ListFilesRequest,
    ListFilesResponse,
    UpdateFileRequest,
)
from .types.generic import GenericArtifact
from .types.go import GoModule
from .types.kfp_artifact import KfpArtifact
from .types.package import (
    DeletePackageRequest,
    GetPackageRequest,
    ListPackagesRequest,
    ListPackagesResponse,
    Package,
    UpdatePackageRequest,
)
from .types.repository import (
    CleanupPolicy,
    CleanupPolicyCondition,
    CleanupPolicyMostRecentVersions,
    CreateRepositoryRequest,
    DeleteRepositoryRequest,
    GetRepositoryRequest,
    ListRepositoriesRequest,
    ListRepositoriesResponse,
    RemoteRepositoryConfig,
    Repository,
    UpdateRepositoryRequest,
    UpstreamPolicy,
    VirtualRepositoryConfig,
)
from .types.rule import (
    CreateRuleRequest,
    DeleteRuleRequest,
    GetRuleRequest,
    ListRulesRequest,
    ListRulesResponse,
    Rule,
    UpdateRuleRequest,
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
    BatchDeleteVersionsRequest,
    DeleteVersionRequest,
    GetVersionRequest,
    ListVersionsRequest,
    ListVersionsResponse,
    UpdateVersionRequest,
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
    "Attachment",
    "BatchDeleteVersionsMetadata",
    "BatchDeleteVersionsRequest",
    "CleanupPolicy",
    "CleanupPolicyCondition",
    "CleanupPolicyMostRecentVersions",
    "CreateAttachmentRequest",
    "CreateRepositoryRequest",
    "CreateRuleRequest",
    "CreateTagRequest",
    "DeleteAttachmentRequest",
    "DeleteFileRequest",
    "DeletePackageRequest",
    "DeleteRepositoryRequest",
    "DeleteRuleRequest",
    "DeleteTagRequest",
    "DeleteVersionRequest",
    "DockerImage",
    "File",
    "GenericArtifact",
    "GetAttachmentRequest",
    "GetDockerImageRequest",
    "GetFileRequest",
    "GetMavenArtifactRequest",
    "GetNpmPackageRequest",
    "GetPackageRequest",
    "GetProjectSettingsRequest",
    "GetPythonPackageRequest",
    "GetRepositoryRequest",
    "GetRuleRequest",
    "GetTagRequest",
    "GetVPCSCConfigRequest",
    "GetVersionRequest",
    "GoModule",
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
    "KfpArtifact",
    "ListAttachmentsRequest",
    "ListAttachmentsResponse",
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
    "ListRulesRequest",
    "ListRulesResponse",
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
    "RemoteRepositoryConfig",
    "Repository",
    "Rule",
    "Tag",
    "UpdateFileRequest",
    "UpdatePackageRequest",
    "UpdateProjectSettingsRequest",
    "UpdateRepositoryRequest",
    "UpdateRuleRequest",
    "UpdateTagRequest",
    "UpdateVPCSCConfigRequest",
    "UpdateVersionRequest",
    "UpstreamPolicy",
    "VPCSCConfig",
    "Version",
    "VersionView",
    "VirtualRepositoryConfig",
    "YumArtifact",
)
