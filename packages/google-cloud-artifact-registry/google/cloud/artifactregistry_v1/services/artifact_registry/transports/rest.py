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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.artifactregistry_v1.types import apt_artifact, artifact, file, package
from google.cloud.artifactregistry_v1.types import vpcsc_config as gda_vpcsc_config
from google.cloud.artifactregistry_v1.types import repository
from google.cloud.artifactregistry_v1.types import repository as gda_repository
from google.cloud.artifactregistry_v1.types import settings
from google.cloud.artifactregistry_v1.types import tag
from google.cloud.artifactregistry_v1.types import tag as gda_tag
from google.cloud.artifactregistry_v1.types import version
from google.cloud.artifactregistry_v1.types import vpcsc_config
from google.cloud.artifactregistry_v1.types import yum_artifact

from .base import ArtifactRegistryTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ArtifactRegistryRestInterceptor:
    """Interceptor for ArtifactRegistry.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ArtifactRegistryRestTransport.

    .. code-block:: python
        class MyCustomArtifactRegistryInterceptor(ArtifactRegistryRestInterceptor):
            def pre_create_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_tag(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_tag(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_package(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_package(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_tag(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_docker_image(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_docker_image(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_maven_artifact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_maven_artifact(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_npm_package(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_npm_package(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_package(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_package(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_project_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_project_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_python_package(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_python_package(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_tag(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_tag(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_vpcsc_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_vpcsc_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_apt_artifacts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_apt_artifacts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_yum_artifacts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_yum_artifacts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_docker_images(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_docker_images(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_files(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_files(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_maven_artifacts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_maven_artifacts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_npm_packages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_npm_packages(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_packages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_packages(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_python_packages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_python_packages(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_repositories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_repositories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_tags(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_tags(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_project_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_project_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_tag(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_tag(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_vpcsc_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_vpcsc_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ArtifactRegistryRestTransport(interceptor=MyCustomArtifactRegistryInterceptor())
        client = ArtifactRegistryClient(transport=transport)


    """

    def pre_create_repository(
        self,
        request: gda_repository.CreateRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gda_repository.CreateRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_create_repository(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_repository

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_create_tag(
        self, request: gda_tag.CreateTagRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gda_tag.CreateTagRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_tag

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_create_tag(self, response: gda_tag.Tag) -> gda_tag.Tag:
        """Post-rpc interceptor for create_tag

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_delete_package(
        self, request: package.DeletePackageRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[package.DeletePackageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_package

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_delete_package(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_package

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_delete_repository(
        self,
        request: repository.DeleteRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repository.DeleteRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_delete_repository(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_repository

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_delete_tag(
        self, request: tag.DeleteTagRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tag.DeleteTagRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_tag

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def pre_delete_version(
        self, request: version.DeleteVersionRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[version.DeleteVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_delete_version(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_version

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_docker_image(
        self,
        request: artifact.GetDockerImageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[artifact.GetDockerImageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_docker_image

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_docker_image(
        self, response: artifact.DockerImage
    ) -> artifact.DockerImage:
        """Post-rpc interceptor for get_docker_image

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_file(
        self, request: file.GetFileRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[file.GetFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_file(self, response: file.File) -> file.File:
        """Post-rpc interceptor for get_file

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_maven_artifact(
        self,
        request: artifact.GetMavenArtifactRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[artifact.GetMavenArtifactRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_maven_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_maven_artifact(
        self, response: artifact.MavenArtifact
    ) -> artifact.MavenArtifact:
        """Post-rpc interceptor for get_maven_artifact

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_npm_package(
        self,
        request: artifact.GetNpmPackageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[artifact.GetNpmPackageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_npm_package

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_npm_package(
        self, response: artifact.NpmPackage
    ) -> artifact.NpmPackage:
        """Post-rpc interceptor for get_npm_package

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_package(
        self, request: package.GetPackageRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[package.GetPackageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_package

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_package(self, response: package.Package) -> package.Package:
        """Post-rpc interceptor for get_package

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_project_settings(
        self,
        request: settings.GetProjectSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[settings.GetProjectSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_project_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_project_settings(
        self, response: settings.ProjectSettings
    ) -> settings.ProjectSettings:
        """Post-rpc interceptor for get_project_settings

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_python_package(
        self,
        request: artifact.GetPythonPackageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[artifact.GetPythonPackageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_python_package

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_python_package(
        self, response: artifact.PythonPackage
    ) -> artifact.PythonPackage:
        """Post-rpc interceptor for get_python_package

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_repository(
        self,
        request: repository.GetRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repository.GetRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_repository(
        self, response: repository.Repository
    ) -> repository.Repository:
        """Post-rpc interceptor for get_repository

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_tag(
        self, request: tag.GetTagRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tag.GetTagRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_tag

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_tag(self, response: tag.Tag) -> tag.Tag:
        """Post-rpc interceptor for get_tag

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_version(
        self, request: version.GetVersionRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[version.GetVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_version(self, response: version.Version) -> version.Version:
        """Post-rpc interceptor for get_version

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_vpcsc_config(
        self,
        request: vpcsc_config.GetVPCSCConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vpcsc_config.GetVPCSCConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_vpcsc_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_vpcsc_config(
        self, response: vpcsc_config.VPCSCConfig
    ) -> vpcsc_config.VPCSCConfig:
        """Post-rpc interceptor for get_vpcsc_config

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_import_apt_artifacts(
        self,
        request: apt_artifact.ImportAptArtifactsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[apt_artifact.ImportAptArtifactsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_apt_artifacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_import_apt_artifacts(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_apt_artifacts

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_import_yum_artifacts(
        self,
        request: yum_artifact.ImportYumArtifactsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[yum_artifact.ImportYumArtifactsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_yum_artifacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_import_yum_artifacts(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_yum_artifacts

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_docker_images(
        self,
        request: artifact.ListDockerImagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[artifact.ListDockerImagesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_docker_images

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_docker_images(
        self, response: artifact.ListDockerImagesResponse
    ) -> artifact.ListDockerImagesResponse:
        """Post-rpc interceptor for list_docker_images

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_files(
        self, request: file.ListFilesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[file.ListFilesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_files

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_files(
        self, response: file.ListFilesResponse
    ) -> file.ListFilesResponse:
        """Post-rpc interceptor for list_files

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_maven_artifacts(
        self,
        request: artifact.ListMavenArtifactsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[artifact.ListMavenArtifactsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_maven_artifacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_maven_artifacts(
        self, response: artifact.ListMavenArtifactsResponse
    ) -> artifact.ListMavenArtifactsResponse:
        """Post-rpc interceptor for list_maven_artifacts

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_npm_packages(
        self,
        request: artifact.ListNpmPackagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[artifact.ListNpmPackagesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_npm_packages

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_npm_packages(
        self, response: artifact.ListNpmPackagesResponse
    ) -> artifact.ListNpmPackagesResponse:
        """Post-rpc interceptor for list_npm_packages

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_packages(
        self, request: package.ListPackagesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[package.ListPackagesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_packages

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_packages(
        self, response: package.ListPackagesResponse
    ) -> package.ListPackagesResponse:
        """Post-rpc interceptor for list_packages

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_python_packages(
        self,
        request: artifact.ListPythonPackagesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[artifact.ListPythonPackagesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_python_packages

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_python_packages(
        self, response: artifact.ListPythonPackagesResponse
    ) -> artifact.ListPythonPackagesResponse:
        """Post-rpc interceptor for list_python_packages

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_repositories(
        self,
        request: repository.ListRepositoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[repository.ListRepositoriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_repositories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_repositories(
        self, response: repository.ListRepositoriesResponse
    ) -> repository.ListRepositoriesResponse:
        """Post-rpc interceptor for list_repositories

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_tags(
        self, request: tag.ListTagsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[tag.ListTagsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_tags

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_tags(self, response: tag.ListTagsResponse) -> tag.ListTagsResponse:
        """Post-rpc interceptor for list_tags

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_versions(
        self, request: version.ListVersionsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[version.ListVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_versions(
        self, response: version.ListVersionsResponse
    ) -> version.ListVersionsResponse:
        """Post-rpc interceptor for list_versions

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_update_project_settings(
        self,
        request: settings.UpdateProjectSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[settings.UpdateProjectSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_project_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_update_project_settings(
        self, response: settings.ProjectSettings
    ) -> settings.ProjectSettings:
        """Post-rpc interceptor for update_project_settings

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_update_repository(
        self,
        request: gda_repository.UpdateRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gda_repository.UpdateRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_update_repository(
        self, response: gda_repository.Repository
    ) -> gda_repository.Repository:
        """Post-rpc interceptor for update_repository

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_update_tag(
        self, request: gda_tag.UpdateTagRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gda_tag.UpdateTagRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_tag

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_update_tag(self, response: gda_tag.Tag) -> gda_tag.Tag:
        """Post-rpc interceptor for update_tag

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_update_vpcsc_config(
        self,
        request: gda_vpcsc_config.UpdateVPCSCConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gda_vpcsc_config.UpdateVPCSCConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_vpcsc_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_update_vpcsc_config(
        self, response: gda_vpcsc_config.VPCSCConfig
    ) -> gda_vpcsc_config.VPCSCConfig:
        """Post-rpc interceptor for update_vpcsc_config

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ArtifactRegistry server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ArtifactRegistry server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ArtifactRegistryRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ArtifactRegistryRestInterceptor


class ArtifactRegistryRestTransport(ArtifactRegistryTransport):
    """REST backend transport for ArtifactRegistry.

    The Artifact Registry API service.

    Artifact Registry is an artifact management system for storing
    artifacts from different package management systems.

    The resources managed by this API are:

    -  Repositories, which group packages and their data.
    -  Packages, which group versions and their tags.
    -  Versions, which are specific forms of a package.
    -  Tags, which represent alternative names for versions.
    -  Files, which contain content and are optionally associated with a
       Package or Version.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "artifactregistry.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ArtifactRegistryRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ArtifactRegistryRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateRepository(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("CreateRepository")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gda_repository.CreateRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create repository method over HTTP.

            Args:
                request (~.gda_repository.CreateRepositoryRequest):
                    The request object. The request to create a new
                repository.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/repositories",
                    "body": "repository",
                },
            ]
            request, metadata = self._interceptor.pre_create_repository(
                request, metadata
            )
            pb_request = gda_repository.CreateRepositoryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_repository(resp)
            return resp

    class _CreateTag(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("CreateTag")

        def __call__(
            self,
            request: gda_tag.CreateTagRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gda_tag.Tag:
            r"""Call the create tag method over HTTP.

            Args:
                request (~.gda_tag.CreateTagRequest):
                    The request object. The request to create a new tag.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gda_tag.Tag:
                    Tags point to a version and represent
                an alternative name that can be used to
                access the version.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*/packages/*}/tags",
                    "body": "tag",
                },
            ]
            request, metadata = self._interceptor.pre_create_tag(request, metadata)
            pb_request = gda_tag.CreateTagRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gda_tag.Tag()
            pb_resp = gda_tag.Tag.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_tag(resp)
            return resp

    class _DeletePackage(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("DeletePackage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: package.DeletePackageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete package method over HTTP.

            Args:
                request (~.package.DeletePackageRequest):
                    The request object. The request to delete a package.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/packages/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_package(request, metadata)
            pb_request = package.DeletePackageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_package(resp)
            return resp

    class _DeleteRepository(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("DeleteRepository")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: repository.DeleteRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete repository method over HTTP.

            Args:
                request (~.repository.DeleteRepositoryRequest):
                    The request object. The request to delete a repository.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_repository(
                request, metadata
            )
            pb_request = repository.DeleteRepositoryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_repository(resp)
            return resp

    class _DeleteTag(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("DeleteTag")

        def __call__(
            self,
            request: tag.DeleteTagRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete tag method over HTTP.

            Args:
                request (~.tag.DeleteTagRequest):
                    The request object. The request to delete a tag.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/packages/*/tags/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_tag(request, metadata)
            pb_request = tag.DeleteTagRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteVersion(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("DeleteVersion")

        def __call__(
            self,
            request: version.DeleteVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete version method over HTTP.

            Args:
                request (~.version.DeleteVersionRequest):
                    The request object. The request to delete a version.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/packages/*/versions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_version(request, metadata)
            pb_request = version.DeleteVersionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_version(resp)
            return resp

    class _GetDockerImage(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetDockerImage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: artifact.GetDockerImageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> artifact.DockerImage:
            r"""Call the get docker image method over HTTP.

            Args:
                request (~.artifact.GetDockerImageRequest):
                    The request object. The request to get docker images.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.artifact.DockerImage:
                    DockerImage represents a docker artifact. The following
                fields are returned as untyped metadata in the Version
                resource, using camelcase keys (i.e.
                metadata.imageSizeBytes):

                -  imageSizeBytes
                -  mediaType
                -  buildTime

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/dockerImages/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_docker_image(
                request, metadata
            )
            pb_request = artifact.GetDockerImageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = artifact.DockerImage()
            pb_resp = artifact.DockerImage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_docker_image(resp)
            return resp

    class _GetFile(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetFile")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: file.GetFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> file.File:
            r"""Call the get file method over HTTP.

            Args:
                request (~.file.GetFileRequest):
                    The request object. The request to retrieve a file.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.file.File:
                    Files store content that is
                potentially associated with Packages or
                Versions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/files/**}",
                },
            ]
            request, metadata = self._interceptor.pre_get_file(request, metadata)
            pb_request = file.GetFileRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = file.File()
            pb_resp = file.File.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_file(resp)
            return resp

    class _GetIamPolicy(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetIamPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.GetIamPolicyRequest):
                    The request object. Request message for ``GetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": [
                            "user:eve@example.com"
                          ],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ],
                      "etag": "BwWWja0YfJA=",
                      "version": 3
                    }

                **YAML example:**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                    etag: BwWWja0YfJA=
                    version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/repositories/*}:getIamPolicy",
                },
            ]
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            pb_request = request
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetMavenArtifact(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetMavenArtifact")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: artifact.GetMavenArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> artifact.MavenArtifact:
            r"""Call the get maven artifact method over HTTP.

            Args:
                request (~.artifact.GetMavenArtifactRequest):
                    The request object. The request to get maven artifacts.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.artifact.MavenArtifact:
                    MavenArtifact represents a maven
                artifact.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/mavenArtifacts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_maven_artifact(
                request, metadata
            )
            pb_request = artifact.GetMavenArtifactRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = artifact.MavenArtifact()
            pb_resp = artifact.MavenArtifact.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_maven_artifact(resp)
            return resp

    class _GetNpmPackage(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetNpmPackage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: artifact.GetNpmPackageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> artifact.NpmPackage:
            r"""Call the get npm package method over HTTP.

            Args:
                request (~.artifact.GetNpmPackageRequest):
                    The request object. The request to get npm packages.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.artifact.NpmPackage:
                    NpmPackage represents an npm
                artifact.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/npmPackages/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_npm_package(request, metadata)
            pb_request = artifact.GetNpmPackageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = artifact.NpmPackage()
            pb_resp = artifact.NpmPackage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_npm_package(resp)
            return resp

    class _GetPackage(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetPackage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: package.GetPackageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> package.Package:
            r"""Call the get package method over HTTP.

            Args:
                request (~.package.GetPackageRequest):
                    The request object. The request to retrieve a package.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.package.Package:
                    Packages are named collections of
                versions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/packages/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_package(request, metadata)
            pb_request = package.GetPackageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = package.Package()
            pb_resp = package.Package.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_package(resp)
            return resp

    class _GetProjectSettings(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetProjectSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: settings.GetProjectSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> settings.ProjectSettings:
            r"""Call the get project settings method over HTTP.

            Args:
                request (~.settings.GetProjectSettingsRequest):
                    The request object. Gets the redirection status for a
                project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.settings.ProjectSettings:
                    The Artifact Registry settings that
                apply to a Project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/projectSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_get_project_settings(
                request, metadata
            )
            pb_request = settings.GetProjectSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = settings.ProjectSettings()
            pb_resp = settings.ProjectSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_project_settings(resp)
            return resp

    class _GetPythonPackage(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetPythonPackage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: artifact.GetPythonPackageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> artifact.PythonPackage:
            r"""Call the get python package method over HTTP.

            Args:
                request (~.artifact.GetPythonPackageRequest):
                    The request object. The request to get python packages.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.artifact.PythonPackage:
                    PythonPackage represents a python
                artifact.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/pythonPackages/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_python_package(
                request, metadata
            )
            pb_request = artifact.GetPythonPackageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = artifact.PythonPackage()
            pb_resp = artifact.PythonPackage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_python_package(resp)
            return resp

    class _GetRepository(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetRepository")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: repository.GetRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repository.Repository:
            r"""Call the get repository method over HTTP.

            Args:
                request (~.repository.GetRepositoryRequest):
                    The request object. The request to retrieve a repository.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repository.Repository:
                    A Repository for storing artifacts
                with a specific format.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_repository(request, metadata)
            pb_request = repository.GetRepositoryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = repository.Repository()
            pb_resp = repository.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_repository(resp)
            return resp

    class _GetTag(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetTag")

        def __call__(
            self,
            request: tag.GetTagRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tag.Tag:
            r"""Call the get tag method over HTTP.

            Args:
                request (~.tag.GetTagRequest):
                    The request object. The request to retrieve a tag.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tag.Tag:
                    Tags point to a version and represent
                an alternative name that can be used to
                access the version.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/packages/*/tags/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_tag(request, metadata)
            pb_request = tag.GetTagRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tag.Tag()
            pb_resp = tag.Tag.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_tag(resp)
            return resp

    class _GetVersion(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetVersion")

        def __call__(
            self,
            request: version.GetVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> version.Version:
            r"""Call the get version method over HTTP.

            Args:
                request (~.version.GetVersionRequest):
                    The request object. The request to retrieve a version.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.version.Version:
                    The body of a version resource. A
                version resource represents a collection
                of components, such as files and other
                data. This may correspond to a version
                in many package management schemes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/repositories/*/packages/*/versions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_version(request, metadata)
            pb_request = version.GetVersionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = version.Version()
            pb_resp = version.Version.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_version(resp)
            return resp

    class _GetVPCSCConfig(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("GetVPCSCConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: vpcsc_config.GetVPCSCConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vpcsc_config.VPCSCConfig:
            r"""Call the get vpcsc config method over HTTP.

            Args:
                request (~.vpcsc_config.GetVPCSCConfigRequest):
                    The request object. Gets the VPC SC config for a project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vpcsc_config.VPCSCConfig:
                    The Artifact Registry VPC SC config
                that apply to a Project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/vpcscConfig}",
                },
            ]
            request, metadata = self._interceptor.pre_get_vpcsc_config(
                request, metadata
            )
            pb_request = vpcsc_config.GetVPCSCConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = vpcsc_config.VPCSCConfig()
            pb_resp = vpcsc_config.VPCSCConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_vpcsc_config(resp)
            return resp

    class _ImportAptArtifacts(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ImportAptArtifacts")

        def __call__(
            self,
            request: apt_artifact.ImportAptArtifactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import apt artifacts method over HTTP.

            Args:
                request (~.apt_artifact.ImportAptArtifactsRequest):
                    The request object. The request to import new apt
                artifacts.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*}/aptArtifacts:import",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_import_apt_artifacts(
                request, metadata
            )
            pb_request = apt_artifact.ImportAptArtifactsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_apt_artifacts(resp)
            return resp

    class _ImportYumArtifacts(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ImportYumArtifacts")

        def __call__(
            self,
            request: yum_artifact.ImportYumArtifactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import yum artifacts method over HTTP.

            Args:
                request (~.yum_artifact.ImportYumArtifactsRequest):
                    The request object. The request to import new yum
                artifacts.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*}/yumArtifacts:import",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_import_yum_artifacts(
                request, metadata
            )
            pb_request = yum_artifact.ImportYumArtifactsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_yum_artifacts(resp)
            return resp

    class _ListDockerImages(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListDockerImages")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: artifact.ListDockerImagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> artifact.ListDockerImagesResponse:
            r"""Call the list docker images method over HTTP.

            Args:
                request (~.artifact.ListDockerImagesRequest):
                    The request object. The request to list docker images.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.artifact.ListDockerImagesResponse:
                    The response from listing docker
                images.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*}/dockerImages",
                },
            ]
            request, metadata = self._interceptor.pre_list_docker_images(
                request, metadata
            )
            pb_request = artifact.ListDockerImagesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = artifact.ListDockerImagesResponse()
            pb_resp = artifact.ListDockerImagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_docker_images(resp)
            return resp

    class _ListFiles(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListFiles")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: file.ListFilesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> file.ListFilesResponse:
            r"""Call the list files method over HTTP.

            Args:
                request (~.file.ListFilesRequest):
                    The request object. The request to list files.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.file.ListFilesResponse:
                    The response from listing files.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*}/files",
                },
            ]
            request, metadata = self._interceptor.pre_list_files(request, metadata)
            pb_request = file.ListFilesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = file.ListFilesResponse()
            pb_resp = file.ListFilesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_files(resp)
            return resp

    class _ListMavenArtifacts(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListMavenArtifacts")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: artifact.ListMavenArtifactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> artifact.ListMavenArtifactsResponse:
            r"""Call the list maven artifacts method over HTTP.

            Args:
                request (~.artifact.ListMavenArtifactsRequest):
                    The request object. The request to list maven artifacts.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.artifact.ListMavenArtifactsResponse:
                    The response from listing maven
                artifacts.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*}/mavenArtifacts",
                },
            ]
            request, metadata = self._interceptor.pre_list_maven_artifacts(
                request, metadata
            )
            pb_request = artifact.ListMavenArtifactsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = artifact.ListMavenArtifactsResponse()
            pb_resp = artifact.ListMavenArtifactsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_maven_artifacts(resp)
            return resp

    class _ListNpmPackages(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListNpmPackages")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: artifact.ListNpmPackagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> artifact.ListNpmPackagesResponse:
            r"""Call the list npm packages method over HTTP.

            Args:
                request (~.artifact.ListNpmPackagesRequest):
                    The request object. The request to list npm packages.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.artifact.ListNpmPackagesResponse:
                    The response from listing npm
                packages.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*}/npmPackages",
                },
            ]
            request, metadata = self._interceptor.pre_list_npm_packages(
                request, metadata
            )
            pb_request = artifact.ListNpmPackagesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = artifact.ListNpmPackagesResponse()
            pb_resp = artifact.ListNpmPackagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_npm_packages(resp)
            return resp

    class _ListPackages(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListPackages")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: package.ListPackagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> package.ListPackagesResponse:
            r"""Call the list packages method over HTTP.

            Args:
                request (~.package.ListPackagesRequest):
                    The request object. The request to list packages.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.package.ListPackagesResponse:
                    The response from listing packages.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*}/packages",
                },
            ]
            request, metadata = self._interceptor.pre_list_packages(request, metadata)
            pb_request = package.ListPackagesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = package.ListPackagesResponse()
            pb_resp = package.ListPackagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_packages(resp)
            return resp

    class _ListPythonPackages(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListPythonPackages")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: artifact.ListPythonPackagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> artifact.ListPythonPackagesResponse:
            r"""Call the list python packages method over HTTP.

            Args:
                request (~.artifact.ListPythonPackagesRequest):
                    The request object. The request to list python packages.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.artifact.ListPythonPackagesResponse:
                    The response from listing python
                packages.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*}/pythonPackages",
                },
            ]
            request, metadata = self._interceptor.pre_list_python_packages(
                request, metadata
            )
            pb_request = artifact.ListPythonPackagesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = artifact.ListPythonPackagesResponse()
            pb_resp = artifact.ListPythonPackagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_python_packages(resp)
            return resp

    class _ListRepositories(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListRepositories")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: repository.ListRepositoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> repository.ListRepositoriesResponse:
            r"""Call the list repositories method over HTTP.

            Args:
                request (~.repository.ListRepositoriesRequest):
                    The request object. The request to list repositories.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.repository.ListRepositoriesResponse:
                    The response from listing
                repositories.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/repositories",
                },
            ]
            request, metadata = self._interceptor.pre_list_repositories(
                request, metadata
            )
            pb_request = repository.ListRepositoriesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = repository.ListRepositoriesResponse()
            pb_resp = repository.ListRepositoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_repositories(resp)
            return resp

    class _ListTags(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListTags")

        def __call__(
            self,
            request: tag.ListTagsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tag.ListTagsResponse:
            r"""Call the list tags method over HTTP.

            Args:
                request (~.tag.ListTagsRequest):
                    The request object. The request to list tags.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tag.ListTagsResponse:
                    The response from listing tags.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*/packages/*}/tags",
                },
            ]
            request, metadata = self._interceptor.pre_list_tags(request, metadata)
            pb_request = tag.ListTagsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = tag.ListTagsResponse()
            pb_resp = tag.ListTagsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_tags(resp)
            return resp

    class _ListVersions(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("ListVersions")

        def __call__(
            self,
            request: version.ListVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> version.ListVersionsResponse:
            r"""Call the list versions method over HTTP.

            Args:
                request (~.version.ListVersionsRequest):
                    The request object. The request to list versions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.version.ListVersionsResponse:
                    The response from listing versions.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/repositories/*/packages/*}/versions",
                },
            ]
            request, metadata = self._interceptor.pre_list_versions(request, metadata)
            pb_request = version.ListVersionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = version.ListVersionsResponse()
            pb_resp = version.ListVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_versions(resp)
            return resp

    class _SetIamPolicy(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("SetIamPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.SetIamPolicyRequest):
                    The request object. Request message for ``SetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": [
                            "user:eve@example.com"
                          ],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ],
                      "etag": "BwWWja0YfJA=",
                      "version": 3
                    }

                **YAML example:**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                    etag: BwWWja0YfJA=
                    version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/repositories/*}:setIamPolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            pb_request = request
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _TestIamPermissions(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("TestIamPermissions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.iam_policy_pb2.TestIamPermissionsRequest):
                    The request object. Request message for ``TestIamPermissions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.iam_policy_pb2.TestIamPermissionsResponse:
                    Response message for ``TestIamPermissions`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/repositories/*}:testIamPermissions",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            pb_request = request
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    class _UpdateProjectSettings(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("UpdateProjectSettings")

        def __call__(
            self,
            request: settings.UpdateProjectSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> settings.ProjectSettings:
            r"""Call the update project settings method over HTTP.

            Args:
                request (~.settings.UpdateProjectSettingsRequest):
                    The request object. Sets the settings of the project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.settings.ProjectSettings:
                    The Artifact Registry settings that
                apply to a Project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{project_settings.name=projects/*/projectSettings}",
                    "body": "project_settings",
                },
            ]
            request, metadata = self._interceptor.pre_update_project_settings(
                request, metadata
            )
            pb_request = settings.UpdateProjectSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = settings.ProjectSettings()
            pb_resp = settings.ProjectSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_project_settings(resp)
            return resp

    class _UpdateRepository(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("UpdateRepository")

        def __call__(
            self,
            request: gda_repository.UpdateRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gda_repository.Repository:
            r"""Call the update repository method over HTTP.

            Args:
                request (~.gda_repository.UpdateRepositoryRequest):
                    The request object. The request to update a repository.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gda_repository.Repository:
                    A Repository for storing artifacts
                with a specific format.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{repository.name=projects/*/locations/*/repositories/*}",
                    "body": "repository",
                },
            ]
            request, metadata = self._interceptor.pre_update_repository(
                request, metadata
            )
            pb_request = gda_repository.UpdateRepositoryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gda_repository.Repository()
            pb_resp = gda_repository.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_repository(resp)
            return resp

    class _UpdateTag(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("UpdateTag")

        def __call__(
            self,
            request: gda_tag.UpdateTagRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gda_tag.Tag:
            r"""Call the update tag method over HTTP.

            Args:
                request (~.gda_tag.UpdateTagRequest):
                    The request object. The request to create or update a
                tag.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gda_tag.Tag:
                    Tags point to a version and represent
                an alternative name that can be used to
                access the version.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{tag.name=projects/*/locations/*/repositories/*/packages/*/tags/*}",
                    "body": "tag",
                },
            ]
            request, metadata = self._interceptor.pre_update_tag(request, metadata)
            pb_request = gda_tag.UpdateTagRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gda_tag.Tag()
            pb_resp = gda_tag.Tag.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_tag(resp)
            return resp

    class _UpdateVPCSCConfig(ArtifactRegistryRestStub):
        def __hash__(self):
            return hash("UpdateVPCSCConfig")

        def __call__(
            self,
            request: gda_vpcsc_config.UpdateVPCSCConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gda_vpcsc_config.VPCSCConfig:
            r"""Call the update vpcsc config method over HTTP.

            Args:
                request (~.gda_vpcsc_config.UpdateVPCSCConfigRequest):
                    The request object. Sets the VPCSC config of the project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gda_vpcsc_config.VPCSCConfig:
                    The Artifact Registry VPC SC config
                that apply to a Project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{vpcsc_config.name=projects/*/locations/*/vpcscConfig}",
                    "body": "vpcsc_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_vpcsc_config(
                request, metadata
            )
            pb_request = gda_vpcsc_config.UpdateVPCSCConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gda_vpcsc_config.VPCSCConfig()
            pb_resp = gda_vpcsc_config.VPCSCConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_vpcsc_config(resp)
            return resp

    @property
    def create_repository(
        self,
    ) -> Callable[[gda_repository.CreateRepositoryRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_tag(self) -> Callable[[gda_tag.CreateTagRequest], gda_tag.Tag]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTag(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_package(
        self,
    ) -> Callable[[package.DeletePackageRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePackage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_repository(
        self,
    ) -> Callable[[repository.DeleteRepositoryRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_tag(self) -> Callable[[tag.DeleteTagRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTag(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_version(
        self,
    ) -> Callable[[version.DeleteVersionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_docker_image(
        self,
    ) -> Callable[[artifact.GetDockerImageRequest], artifact.DockerImage]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDockerImage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_file(self) -> Callable[[file.GetFileRequest], file.File]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_maven_artifact(
        self,
    ) -> Callable[[artifact.GetMavenArtifactRequest], artifact.MavenArtifact]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMavenArtifact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_npm_package(
        self,
    ) -> Callable[[artifact.GetNpmPackageRequest], artifact.NpmPackage]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNpmPackage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_package(self) -> Callable[[package.GetPackageRequest], package.Package]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPackage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_project_settings(
        self,
    ) -> Callable[[settings.GetProjectSettingsRequest], settings.ProjectSettings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProjectSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_python_package(
        self,
    ) -> Callable[[artifact.GetPythonPackageRequest], artifact.PythonPackage]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPythonPackage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_repository(
        self,
    ) -> Callable[[repository.GetRepositoryRequest], repository.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_tag(self) -> Callable[[tag.GetTagRequest], tag.Tag]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTag(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_version(self) -> Callable[[version.GetVersionRequest], version.Version]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_vpcsc_config(
        self,
    ) -> Callable[[vpcsc_config.GetVPCSCConfigRequest], vpcsc_config.VPCSCConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVPCSCConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_apt_artifacts(
        self,
    ) -> Callable[[apt_artifact.ImportAptArtifactsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportAptArtifacts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_yum_artifacts(
        self,
    ) -> Callable[[yum_artifact.ImportYumArtifactsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportYumArtifacts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_docker_images(
        self,
    ) -> Callable[
        [artifact.ListDockerImagesRequest], artifact.ListDockerImagesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDockerImages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_files(self) -> Callable[[file.ListFilesRequest], file.ListFilesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFiles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_maven_artifacts(
        self,
    ) -> Callable[
        [artifact.ListMavenArtifactsRequest], artifact.ListMavenArtifactsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMavenArtifacts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_npm_packages(
        self,
    ) -> Callable[[artifact.ListNpmPackagesRequest], artifact.ListNpmPackagesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNpmPackages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_packages(
        self,
    ) -> Callable[[package.ListPackagesRequest], package.ListPackagesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPackages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_python_packages(
        self,
    ) -> Callable[
        [artifact.ListPythonPackagesRequest], artifact.ListPythonPackagesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPythonPackages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_repositories(
        self,
    ) -> Callable[
        [repository.ListRepositoriesRequest], repository.ListRepositoriesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRepositories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_tags(self) -> Callable[[tag.ListTagsRequest], tag.ListTagsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTags(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_versions(
        self,
    ) -> Callable[[version.ListVersionsRequest], version.ListVersionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_project_settings(
        self,
    ) -> Callable[[settings.UpdateProjectSettingsRequest], settings.ProjectSettings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProjectSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_repository(
        self,
    ) -> Callable[[gda_repository.UpdateRepositoryRequest], gda_repository.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_tag(self) -> Callable[[gda_tag.UpdateTagRequest], gda_tag.Tag]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTag(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_vpcsc_config(
        self,
    ) -> Callable[
        [gda_vpcsc_config.UpdateVPCSCConfigRequest], gda_vpcsc_config.VPCSCConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateVPCSCConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(ArtifactRegistryRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:

            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(ArtifactRegistryRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:

            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(ArtifactRegistryRestStub):
        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:

            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ArtifactRegistryRestTransport",)
