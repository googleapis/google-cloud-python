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


from .services.artifact_registry import ArtifactRegistryClient
from .services.artifact_registry import ArtifactRegistryAsyncClient

from .types.apt_artifact import AptArtifact
from .types.apt_artifact import ImportAptArtifactsErrorInfo
from .types.apt_artifact import ImportAptArtifactsGcsSource
from .types.apt_artifact import ImportAptArtifactsMetadata
from .types.apt_artifact import ImportAptArtifactsRequest
from .types.apt_artifact import ImportAptArtifactsResponse
from .types.artifact import DockerImage
from .types.artifact import GetDockerImageRequest
from .types.artifact import GetMavenArtifactRequest
from .types.artifact import GetNpmPackageRequest
from .types.artifact import GetPythonPackageRequest
from .types.artifact import ListDockerImagesRequest
from .types.artifact import ListDockerImagesResponse
from .types.artifact import ListMavenArtifactsRequest
from .types.artifact import ListMavenArtifactsResponse
from .types.artifact import ListNpmPackagesRequest
from .types.artifact import ListNpmPackagesResponse
from .types.artifact import ListPythonPackagesRequest
from .types.artifact import ListPythonPackagesResponse
from .types.artifact import MavenArtifact
from .types.artifact import NpmPackage
from .types.artifact import PythonPackage
from .types.attachment import Attachment
from .types.attachment import CreateAttachmentRequest
from .types.attachment import DeleteAttachmentRequest
from .types.attachment import GetAttachmentRequest
from .types.attachment import ListAttachmentsRequest
from .types.attachment import ListAttachmentsResponse
from .types.file import DeleteFileRequest
from .types.file import File
from .types.file import GetFileRequest
from .types.file import Hash
from .types.file import ListFilesRequest
from .types.file import ListFilesResponse
from .types.file import UpdateFileRequest
from .types.generic import GenericArtifact
from .types.go import GoModule
from .types.kfp_artifact import KfpArtifact
from .types.package import DeletePackageRequest
from .types.package import GetPackageRequest
from .types.package import ListPackagesRequest
from .types.package import ListPackagesResponse
from .types.package import Package
from .types.package import UpdatePackageRequest
from .types.repository import CleanupPolicy
from .types.repository import CleanupPolicyCondition
from .types.repository import CleanupPolicyMostRecentVersions
from .types.repository import CreateRepositoryRequest
from .types.repository import DeleteRepositoryRequest
from .types.repository import GetRepositoryRequest
from .types.repository import ListRepositoriesRequest
from .types.repository import ListRepositoriesResponse
from .types.repository import RemoteRepositoryConfig
from .types.repository import Repository
from .types.repository import UpdateRepositoryRequest
from .types.repository import UpstreamPolicy
from .types.repository import VirtualRepositoryConfig
from .types.rule import CreateRuleRequest
from .types.rule import DeleteRuleRequest
from .types.rule import GetRuleRequest
from .types.rule import ListRulesRequest
from .types.rule import ListRulesResponse
from .types.rule import Rule
from .types.rule import UpdateRuleRequest
from .types.service import OperationMetadata
from .types.settings import GetProjectSettingsRequest
from .types.settings import ProjectSettings
from .types.settings import UpdateProjectSettingsRequest
from .types.tag import CreateTagRequest
from .types.tag import DeleteTagRequest
from .types.tag import GetTagRequest
from .types.tag import ListTagsRequest
from .types.tag import ListTagsResponse
from .types.tag import Tag
from .types.tag import UpdateTagRequest
from .types.version import BatchDeleteVersionsMetadata
from .types.version import BatchDeleteVersionsRequest
from .types.version import DeleteVersionRequest
from .types.version import GetVersionRequest
from .types.version import ListVersionsRequest
from .types.version import ListVersionsResponse
from .types.version import UpdateVersionRequest
from .types.version import Version
from .types.version import VersionView
from .types.vpcsc_config import GetVPCSCConfigRequest
from .types.vpcsc_config import UpdateVPCSCConfigRequest
from .types.vpcsc_config import VPCSCConfig
from .types.yum_artifact import ImportYumArtifactsErrorInfo
from .types.yum_artifact import ImportYumArtifactsGcsSource
from .types.yum_artifact import ImportYumArtifactsMetadata
from .types.yum_artifact import ImportYumArtifactsRequest
from .types.yum_artifact import ImportYumArtifactsResponse
from .types.yum_artifact import YumArtifact

__all__ = (
    'ArtifactRegistryAsyncClient',
'AptArtifact',
'ArtifactRegistryClient',
'Attachment',
'BatchDeleteVersionsMetadata',
'BatchDeleteVersionsRequest',
'CleanupPolicy',
'CleanupPolicyCondition',
'CleanupPolicyMostRecentVersions',
'CreateAttachmentRequest',
'CreateRepositoryRequest',
'CreateRuleRequest',
'CreateTagRequest',
'DeleteAttachmentRequest',
'DeleteFileRequest',
'DeletePackageRequest',
'DeleteRepositoryRequest',
'DeleteRuleRequest',
'DeleteTagRequest',
'DeleteVersionRequest',
'DockerImage',
'File',
'GenericArtifact',
'GetAttachmentRequest',
'GetDockerImageRequest',
'GetFileRequest',
'GetMavenArtifactRequest',
'GetNpmPackageRequest',
'GetPackageRequest',
'GetProjectSettingsRequest',
'GetPythonPackageRequest',
'GetRepositoryRequest',
'GetRuleRequest',
'GetTagRequest',
'GetVPCSCConfigRequest',
'GetVersionRequest',
'GoModule',
'Hash',
'ImportAptArtifactsErrorInfo',
'ImportAptArtifactsGcsSource',
'ImportAptArtifactsMetadata',
'ImportAptArtifactsRequest',
'ImportAptArtifactsResponse',
'ImportYumArtifactsErrorInfo',
'ImportYumArtifactsGcsSource',
'ImportYumArtifactsMetadata',
'ImportYumArtifactsRequest',
'ImportYumArtifactsResponse',
'KfpArtifact',
'ListAttachmentsRequest',
'ListAttachmentsResponse',
'ListDockerImagesRequest',
'ListDockerImagesResponse',
'ListFilesRequest',
'ListFilesResponse',
'ListMavenArtifactsRequest',
'ListMavenArtifactsResponse',
'ListNpmPackagesRequest',
'ListNpmPackagesResponse',
'ListPackagesRequest',
'ListPackagesResponse',
'ListPythonPackagesRequest',
'ListPythonPackagesResponse',
'ListRepositoriesRequest',
'ListRepositoriesResponse',
'ListRulesRequest',
'ListRulesResponse',
'ListTagsRequest',
'ListTagsResponse',
'ListVersionsRequest',
'ListVersionsResponse',
'MavenArtifact',
'NpmPackage',
'OperationMetadata',
'Package',
'ProjectSettings',
'PythonPackage',
'RemoteRepositoryConfig',
'Repository',
'Rule',
'Tag',
'UpdateFileRequest',
'UpdatePackageRequest',
'UpdateProjectSettingsRequest',
'UpdateRepositoryRequest',
'UpdateRuleRequest',
'UpdateTagRequest',
'UpdateVPCSCConfigRequest',
'UpdateVersionRequest',
'UpstreamPolicy',
'VPCSCConfig',
'Version',
'VersionView',
'VirtualRepositoryConfig',
'YumArtifact',
)
