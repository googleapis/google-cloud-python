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
from google.cloud.artifactregistry import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.artifactregistry_v1.services.artifact_registry.client import ArtifactRegistryClient
from google.cloud.artifactregistry_v1.services.artifact_registry.async_client import ArtifactRegistryAsyncClient

from google.cloud.artifactregistry_v1.types.apt_artifact import AptArtifact
from google.cloud.artifactregistry_v1.types.apt_artifact import ImportAptArtifactsErrorInfo
from google.cloud.artifactregistry_v1.types.apt_artifact import ImportAptArtifactsGcsSource
from google.cloud.artifactregistry_v1.types.apt_artifact import ImportAptArtifactsMetadata
from google.cloud.artifactregistry_v1.types.apt_artifact import ImportAptArtifactsRequest
from google.cloud.artifactregistry_v1.types.apt_artifact import ImportAptArtifactsResponse
from google.cloud.artifactregistry_v1.types.artifact import DockerImage
from google.cloud.artifactregistry_v1.types.artifact import GetDockerImageRequest
from google.cloud.artifactregistry_v1.types.artifact import GetMavenArtifactRequest
from google.cloud.artifactregistry_v1.types.artifact import GetNpmPackageRequest
from google.cloud.artifactregistry_v1.types.artifact import GetPythonPackageRequest
from google.cloud.artifactregistry_v1.types.artifact import ListDockerImagesRequest
from google.cloud.artifactregistry_v1.types.artifact import ListDockerImagesResponse
from google.cloud.artifactregistry_v1.types.artifact import ListMavenArtifactsRequest
from google.cloud.artifactregistry_v1.types.artifact import ListMavenArtifactsResponse
from google.cloud.artifactregistry_v1.types.artifact import ListNpmPackagesRequest
from google.cloud.artifactregistry_v1.types.artifact import ListNpmPackagesResponse
from google.cloud.artifactregistry_v1.types.artifact import ListPythonPackagesRequest
from google.cloud.artifactregistry_v1.types.artifact import ListPythonPackagesResponse
from google.cloud.artifactregistry_v1.types.artifact import MavenArtifact
from google.cloud.artifactregistry_v1.types.artifact import NpmPackage
from google.cloud.artifactregistry_v1.types.artifact import PythonPackage
from google.cloud.artifactregistry_v1.types.file import File
from google.cloud.artifactregistry_v1.types.file import GetFileRequest
from google.cloud.artifactregistry_v1.types.file import Hash
from google.cloud.artifactregistry_v1.types.file import ListFilesRequest
from google.cloud.artifactregistry_v1.types.file import ListFilesResponse
from google.cloud.artifactregistry_v1.types.package import DeletePackageRequest
from google.cloud.artifactregistry_v1.types.package import GetPackageRequest
from google.cloud.artifactregistry_v1.types.package import ListPackagesRequest
from google.cloud.artifactregistry_v1.types.package import ListPackagesResponse
from google.cloud.artifactregistry_v1.types.package import Package
from google.cloud.artifactregistry_v1.types.repository import CleanupPolicy
from google.cloud.artifactregistry_v1.types.repository import CleanupPolicyCondition
from google.cloud.artifactregistry_v1.types.repository import CleanupPolicyMostRecentVersions
from google.cloud.artifactregistry_v1.types.repository import CreateRepositoryRequest
from google.cloud.artifactregistry_v1.types.repository import DeleteRepositoryRequest
from google.cloud.artifactregistry_v1.types.repository import GetRepositoryRequest
from google.cloud.artifactregistry_v1.types.repository import ListRepositoriesRequest
from google.cloud.artifactregistry_v1.types.repository import ListRepositoriesResponse
from google.cloud.artifactregistry_v1.types.repository import RemoteRepositoryConfig
from google.cloud.artifactregistry_v1.types.repository import Repository
from google.cloud.artifactregistry_v1.types.repository import UpdateRepositoryRequest
from google.cloud.artifactregistry_v1.types.repository import UpstreamPolicy
from google.cloud.artifactregistry_v1.types.repository import VirtualRepositoryConfig
from google.cloud.artifactregistry_v1.types.service import OperationMetadata
from google.cloud.artifactregistry_v1.types.settings import GetProjectSettingsRequest
from google.cloud.artifactregistry_v1.types.settings import ProjectSettings
from google.cloud.artifactregistry_v1.types.settings import UpdateProjectSettingsRequest
from google.cloud.artifactregistry_v1.types.tag import CreateTagRequest
from google.cloud.artifactregistry_v1.types.tag import DeleteTagRequest
from google.cloud.artifactregistry_v1.types.tag import GetTagRequest
from google.cloud.artifactregistry_v1.types.tag import ListTagsRequest
from google.cloud.artifactregistry_v1.types.tag import ListTagsResponse
from google.cloud.artifactregistry_v1.types.tag import Tag
from google.cloud.artifactregistry_v1.types.tag import UpdateTagRequest
from google.cloud.artifactregistry_v1.types.version import BatchDeleteVersionsMetadata
from google.cloud.artifactregistry_v1.types.version import BatchDeleteVersionsRequest
from google.cloud.artifactregistry_v1.types.version import DeleteVersionRequest
from google.cloud.artifactregistry_v1.types.version import GetVersionRequest
from google.cloud.artifactregistry_v1.types.version import ListVersionsRequest
from google.cloud.artifactregistry_v1.types.version import ListVersionsResponse
from google.cloud.artifactregistry_v1.types.version import Version
from google.cloud.artifactregistry_v1.types.version import VersionView
from google.cloud.artifactregistry_v1.types.vpcsc_config import GetVPCSCConfigRequest
from google.cloud.artifactregistry_v1.types.vpcsc_config import UpdateVPCSCConfigRequest
from google.cloud.artifactregistry_v1.types.vpcsc_config import VPCSCConfig
from google.cloud.artifactregistry_v1.types.yum_artifact import ImportYumArtifactsErrorInfo
from google.cloud.artifactregistry_v1.types.yum_artifact import ImportYumArtifactsGcsSource
from google.cloud.artifactregistry_v1.types.yum_artifact import ImportYumArtifactsMetadata
from google.cloud.artifactregistry_v1.types.yum_artifact import ImportYumArtifactsRequest
from google.cloud.artifactregistry_v1.types.yum_artifact import ImportYumArtifactsResponse
from google.cloud.artifactregistry_v1.types.yum_artifact import YumArtifact

__all__ = ('ArtifactRegistryClient',
    'ArtifactRegistryAsyncClient',
    'AptArtifact',
    'ImportAptArtifactsErrorInfo',
    'ImportAptArtifactsGcsSource',
    'ImportAptArtifactsMetadata',
    'ImportAptArtifactsRequest',
    'ImportAptArtifactsResponse',
    'DockerImage',
    'GetDockerImageRequest',
    'GetMavenArtifactRequest',
    'GetNpmPackageRequest',
    'GetPythonPackageRequest',
    'ListDockerImagesRequest',
    'ListDockerImagesResponse',
    'ListMavenArtifactsRequest',
    'ListMavenArtifactsResponse',
    'ListNpmPackagesRequest',
    'ListNpmPackagesResponse',
    'ListPythonPackagesRequest',
    'ListPythonPackagesResponse',
    'MavenArtifact',
    'NpmPackage',
    'PythonPackage',
    'File',
    'GetFileRequest',
    'Hash',
    'ListFilesRequest',
    'ListFilesResponse',
    'DeletePackageRequest',
    'GetPackageRequest',
    'ListPackagesRequest',
    'ListPackagesResponse',
    'Package',
    'CleanupPolicy',
    'CleanupPolicyCondition',
    'CleanupPolicyMostRecentVersions',
    'CreateRepositoryRequest',
    'DeleteRepositoryRequest',
    'GetRepositoryRequest',
    'ListRepositoriesRequest',
    'ListRepositoriesResponse',
    'RemoteRepositoryConfig',
    'Repository',
    'UpdateRepositoryRequest',
    'UpstreamPolicy',
    'VirtualRepositoryConfig',
    'OperationMetadata',
    'GetProjectSettingsRequest',
    'ProjectSettings',
    'UpdateProjectSettingsRequest',
    'CreateTagRequest',
    'DeleteTagRequest',
    'GetTagRequest',
    'ListTagsRequest',
    'ListTagsResponse',
    'Tag',
    'UpdateTagRequest',
    'BatchDeleteVersionsMetadata',
    'BatchDeleteVersionsRequest',
    'DeleteVersionRequest',
    'GetVersionRequest',
    'ListVersionsRequest',
    'ListVersionsResponse',
    'Version',
    'VersionView',
    'GetVPCSCConfigRequest',
    'UpdateVPCSCConfigRequest',
    'VPCSCConfig',
    'ImportYumArtifactsErrorInfo',
    'ImportYumArtifactsGcsSource',
    'ImportYumArtifactsMetadata',
    'ImportYumArtifactsRequest',
    'ImportYumArtifactsResponse',
    'YumArtifact',
)
