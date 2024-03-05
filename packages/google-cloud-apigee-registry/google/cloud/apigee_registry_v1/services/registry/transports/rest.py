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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.api import httpbody_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.apigee_registry_v1.types import registry_models, registry_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import RegistryTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class RegistryRestInterceptor:
    """Interceptor for Registry.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RegistryRestTransport.

    .. code-block:: python
        class MyCustomRegistryInterceptor(RegistryRestInterceptor):
            def pre_create_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_api_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_api_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_api_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_api_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_api_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_api_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_artifact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_artifact(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_api_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_api_deployment_revision(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_api_deployment_revision(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_api_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_api_spec_revision(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_api_spec_revision(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_api_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_artifact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_api_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_api_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_api_spec_contents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api_spec_contents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_api_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_api_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_artifact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_artifact(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_artifact_contents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_artifact_contents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_api_deployment_revisions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_api_deployment_revisions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_api_deployments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_api_deployments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_apis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_apis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_api_spec_revisions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_api_spec_revisions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_api_specs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_api_specs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_api_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_api_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_artifacts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_artifacts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_replace_artifact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_replace_artifact(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rollback_api_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rollback_api_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rollback_api_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rollback_api_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_tag_api_deployment_revision(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_tag_api_deployment_revision(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_tag_api_spec_revision(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_tag_api_spec_revision(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_api(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_api(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_api_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_api_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_api_spec(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_api_spec(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_api_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_api_version(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RegistryRestTransport(interceptor=MyCustomRegistryInterceptor())
        client = RegistryClient(transport=transport)


    """

    def pre_create_api(
        self,
        request: registry_service.CreateApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.CreateApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_api(self, response: registry_models.Api) -> registry_models.Api:
        """Post-rpc interceptor for create_api

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_create_api_deployment(
        self,
        request: registry_service.CreateApiDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.CreateApiDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_api_deployment(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for create_api_deployment

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_create_api_spec(
        self,
        request: registry_service.CreateApiSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.CreateApiSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_api_spec(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for create_api_spec

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_create_api_version(
        self,
        request: registry_service.CreateApiVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.CreateApiVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_api_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_api_version(
        self, response: registry_models.ApiVersion
    ) -> registry_models.ApiVersion:
        """Post-rpc interceptor for create_api_version

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_create_artifact(
        self,
        request: registry_service.CreateArtifactRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.CreateArtifactRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_artifact(
        self, response: registry_models.Artifact
    ) -> registry_models.Artifact:
        """Post-rpc interceptor for create_artifact

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_delete_api(
        self,
        request: registry_service.DeleteApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.DeleteApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_delete_api_deployment(
        self,
        request: registry_service.DeleteApiDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.DeleteApiDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_delete_api_deployment_revision(
        self,
        request: registry_service.DeleteApiDeploymentRevisionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        registry_service.DeleteApiDeploymentRevisionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_api_deployment_revision

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_delete_api_deployment_revision(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for delete_api_deployment_revision

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_delete_api_spec(
        self,
        request: registry_service.DeleteApiSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.DeleteApiSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_delete_api_spec_revision(
        self,
        request: registry_service.DeleteApiSpecRevisionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        registry_service.DeleteApiSpecRevisionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_api_spec_revision

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_delete_api_spec_revision(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for delete_api_spec_revision

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_delete_api_version(
        self,
        request: registry_service.DeleteApiVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.DeleteApiVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_api_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_delete_artifact(
        self,
        request: registry_service.DeleteArtifactRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.DeleteArtifactRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_get_api(
        self,
        request: registry_service.GetApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.GetApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api(self, response: registry_models.Api) -> registry_models.Api:
        """Post-rpc interceptor for get_api

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_get_api_deployment(
        self,
        request: registry_service.GetApiDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.GetApiDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api_deployment(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for get_api_deployment

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_get_api_spec(
        self,
        request: registry_service.GetApiSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.GetApiSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api_spec(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for get_api_spec

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_get_api_spec_contents(
        self,
        request: registry_service.GetApiSpecContentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.GetApiSpecContentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api_spec_contents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api_spec_contents(
        self, response: httpbody_pb2.HttpBody
    ) -> httpbody_pb2.HttpBody:
        """Post-rpc interceptor for get_api_spec_contents

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_get_api_version(
        self,
        request: registry_service.GetApiVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.GetApiVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_api_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api_version(
        self, response: registry_models.ApiVersion
    ) -> registry_models.ApiVersion:
        """Post-rpc interceptor for get_api_version

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_get_artifact(
        self,
        request: registry_service.GetArtifactRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.GetArtifactRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_artifact(
        self, response: registry_models.Artifact
    ) -> registry_models.Artifact:
        """Post-rpc interceptor for get_artifact

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_get_artifact_contents(
        self,
        request: registry_service.GetArtifactContentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.GetArtifactContentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_artifact_contents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_artifact_contents(
        self, response: httpbody_pb2.HttpBody
    ) -> httpbody_pb2.HttpBody:
        """Post-rpc interceptor for get_artifact_contents

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_list_api_deployment_revisions(
        self,
        request: registry_service.ListApiDeploymentRevisionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        registry_service.ListApiDeploymentRevisionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_api_deployment_revisions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_deployment_revisions(
        self, response: registry_service.ListApiDeploymentRevisionsResponse
    ) -> registry_service.ListApiDeploymentRevisionsResponse:
        """Post-rpc interceptor for list_api_deployment_revisions

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_list_api_deployments(
        self,
        request: registry_service.ListApiDeploymentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.ListApiDeploymentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_api_deployments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_deployments(
        self, response: registry_service.ListApiDeploymentsResponse
    ) -> registry_service.ListApiDeploymentsResponse:
        """Post-rpc interceptor for list_api_deployments

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_list_apis(
        self,
        request: registry_service.ListApisRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.ListApisRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_apis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_apis(
        self, response: registry_service.ListApisResponse
    ) -> registry_service.ListApisResponse:
        """Post-rpc interceptor for list_apis

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_list_api_spec_revisions(
        self,
        request: registry_service.ListApiSpecRevisionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.ListApiSpecRevisionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_api_spec_revisions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_spec_revisions(
        self, response: registry_service.ListApiSpecRevisionsResponse
    ) -> registry_service.ListApiSpecRevisionsResponse:
        """Post-rpc interceptor for list_api_spec_revisions

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_list_api_specs(
        self,
        request: registry_service.ListApiSpecsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.ListApiSpecsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_api_specs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_specs(
        self, response: registry_service.ListApiSpecsResponse
    ) -> registry_service.ListApiSpecsResponse:
        """Post-rpc interceptor for list_api_specs

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_list_api_versions(
        self,
        request: registry_service.ListApiVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.ListApiVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_api_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_versions(
        self, response: registry_service.ListApiVersionsResponse
    ) -> registry_service.ListApiVersionsResponse:
        """Post-rpc interceptor for list_api_versions

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_list_artifacts(
        self,
        request: registry_service.ListArtifactsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.ListArtifactsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_artifacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_artifacts(
        self, response: registry_service.ListArtifactsResponse
    ) -> registry_service.ListArtifactsResponse:
        """Post-rpc interceptor for list_artifacts

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_replace_artifact(
        self,
        request: registry_service.ReplaceArtifactRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.ReplaceArtifactRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for replace_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_replace_artifact(
        self, response: registry_models.Artifact
    ) -> registry_models.Artifact:
        """Post-rpc interceptor for replace_artifact

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_rollback_api_deployment(
        self,
        request: registry_service.RollbackApiDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        registry_service.RollbackApiDeploymentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for rollback_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_rollback_api_deployment(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for rollback_api_deployment

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_rollback_api_spec(
        self,
        request: registry_service.RollbackApiSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.RollbackApiSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rollback_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_rollback_api_spec(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for rollback_api_spec

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_tag_api_deployment_revision(
        self,
        request: registry_service.TagApiDeploymentRevisionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        registry_service.TagApiDeploymentRevisionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for tag_api_deployment_revision

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_tag_api_deployment_revision(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for tag_api_deployment_revision

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_tag_api_spec_revision(
        self,
        request: registry_service.TagApiSpecRevisionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.TagApiSpecRevisionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for tag_api_spec_revision

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_tag_api_spec_revision(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for tag_api_spec_revision

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_update_api(
        self,
        request: registry_service.UpdateApiRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.UpdateApiRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_update_api(self, response: registry_models.Api) -> registry_models.Api:
        """Post-rpc interceptor for update_api

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_update_api_deployment(
        self,
        request: registry_service.UpdateApiDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.UpdateApiDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_update_api_deployment(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for update_api_deployment

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_update_api_spec(
        self,
        request: registry_service.UpdateApiSpecRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.UpdateApiSpecRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_update_api_spec(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for update_api_spec

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_update_api_version(
        self,
        request: registry_service.UpdateApiVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[registry_service.UpdateApiVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_api_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_update_api_version(
        self, response: registry_models.ApiVersion
    ) -> registry_models.ApiVersion:
        """Post-rpc interceptor for update_api_version

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
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
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
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
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
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
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
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
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
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
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
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
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RegistryRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RegistryRestInterceptor


class RegistryRestTransport(RegistryTransport):
    """REST backend transport for Registry.

    The Registry service allows teams to manage descriptions of
    APIs.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "apigeeregistry.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RegistryRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'apigeeregistry.googleapis.com').
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or RegistryRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateApi(RegistryRestStub):
        def __hash__(self):
            return hash("CreateApi")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "apiId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: registry_service.CreateApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.Api:
            r"""Call the create api method over HTTP.

            Args:
                request (~.registry_service.CreateApiRequest):
                    The request object. Request message for CreateApi.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.Api:
                    A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/apis",
                    "body": "api",
                },
            ]
            request, metadata = self._interceptor.pre_create_api(request, metadata)
            pb_request = registry_service.CreateApiRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.Api()
            pb_resp = registry_models.Api.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_api(resp)
            return resp

    class _CreateApiDeployment(RegistryRestStub):
        def __hash__(self):
            return hash("CreateApiDeployment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "apiDeploymentId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: registry_service.CreateApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the create api deployment method over HTTP.

            Args:
                request (~.registry_service.CreateApiDeploymentRequest):
                    The request object. Request message for
                CreateApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiDeployment:
                    Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*}/deployments",
                    "body": "api_deployment",
                },
            ]
            request, metadata = self._interceptor.pre_create_api_deployment(
                request, metadata
            )
            pb_request = registry_service.CreateApiDeploymentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiDeployment()
            pb_resp = registry_models.ApiDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_api_deployment(resp)
            return resp

    class _CreateApiSpec(RegistryRestStub):
        def __hash__(self):
            return hash("CreateApiSpec")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "apiSpecId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: registry_service.CreateApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the create api spec method over HTTP.

            Args:
                request (~.registry_service.CreateApiSpecRequest):
                    The request object. Request message for CreateApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiSpec:
                    Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*}/specs",
                    "body": "api_spec",
                },
            ]
            request, metadata = self._interceptor.pre_create_api_spec(request, metadata)
            pb_request = registry_service.CreateApiSpecRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiSpec()
            pb_resp = registry_models.ApiSpec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_api_spec(resp)
            return resp

    class _CreateApiVersion(RegistryRestStub):
        def __hash__(self):
            return hash("CreateApiVersion")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "apiVersionId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: registry_service.CreateApiVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiVersion:
            r"""Call the create api version method over HTTP.

            Args:
                request (~.registry_service.CreateApiVersionRequest):
                    The request object. Request message for CreateApiVersion.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiVersion:
                    Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*}/versions",
                    "body": "api_version",
                },
            ]
            request, metadata = self._interceptor.pre_create_api_version(
                request, metadata
            )
            pb_request = registry_service.CreateApiVersionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiVersion()
            pb_resp = registry_models.ApiVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_api_version(resp)
            return resp

    class _CreateArtifact(RegistryRestStub):
        def __hash__(self):
            return hash("CreateArtifact")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "artifactId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: registry_service.CreateArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.Artifact:
            r"""Call the create artifact method over HTTP.

            Args:
                request (~.registry_service.CreateArtifactRequest):
                    The request object. Request message for CreateArtifact.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.Artifact:
                    Artifacts of resources. Artifacts are unique
                (single-value) per resource and are used to store
                metadata that is too large or numerous to be stored
                directly on the resource. Since artifacts are stored
                separately from parent resources, they should generally
                be used for metadata that is needed infrequently, i.e.,
                not for display in primary views of the resource but
                perhaps displayed or downloaded upon request. The
                ``ListArtifacts`` method allows artifacts to be quickly
                enumerated and checked for presence without downloading
                their (potentially-large) contents.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/artifacts",
                    "body": "artifact",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*}/artifacts",
                    "body": "artifact",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*}/artifacts",
                    "body": "artifact",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*/specs/*}/artifacts",
                    "body": "artifact",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/deployments/*}/artifacts",
                    "body": "artifact",
                },
            ]
            request, metadata = self._interceptor.pre_create_artifact(request, metadata)
            pb_request = registry_service.CreateArtifactRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.Artifact()
            pb_resp = registry_models.Artifact.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_artifact(resp)
            return resp

    class _DeleteApi(RegistryRestStub):
        def __hash__(self):
            return hash("DeleteApi")

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
            request: registry_service.DeleteApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete api method over HTTP.

            Args:
                request (~.registry_service.DeleteApiRequest):
                    The request object. Request message for DeleteApi.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_api(request, metadata)
            pb_request = registry_service.DeleteApiRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _DeleteApiDeployment(RegistryRestStub):
        def __hash__(self):
            return hash("DeleteApiDeployment")

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
            request: registry_service.DeleteApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete api deployment method over HTTP.

            Args:
                request (~.registry_service.DeleteApiDeploymentRequest):
                    The request object. Request message for
                DeleteApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_api_deployment(
                request, metadata
            )
            pb_request = registry_service.DeleteApiDeploymentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _DeleteApiDeploymentRevision(RegistryRestStub):
        def __hash__(self):
            return hash("DeleteApiDeploymentRevision")

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
            request: registry_service.DeleteApiDeploymentRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the delete api deployment
            revision method over HTTP.

                Args:
                    request (~.registry_service.DeleteApiDeploymentRevisionRequest):
                        The request object. Request message for
                    DeleteApiDeploymentRevision.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.registry_models.ApiDeployment:
                        Describes a service running at
                    particular address that provides a
                    particular version of an API.
                    ApiDeployments have revisions which
                    correspond to different configurations
                    of a single deployment in time. Revision
                    identifiers should be updated whenever
                    the served API spec or endpoint address
                    changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*}:deleteRevision",
                },
            ]
            request, metadata = self._interceptor.pre_delete_api_deployment_revision(
                request, metadata
            )
            pb_request = registry_service.DeleteApiDeploymentRevisionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiDeployment()
            pb_resp = registry_models.ApiDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_api_deployment_revision(resp)
            return resp

    class _DeleteApiSpec(RegistryRestStub):
        def __hash__(self):
            return hash("DeleteApiSpec")

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
            request: registry_service.DeleteApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete api spec method over HTTP.

            Args:
                request (~.registry_service.DeleteApiSpecRequest):
                    The request object. Request message for DeleteApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_api_spec(request, metadata)
            pb_request = registry_service.DeleteApiSpecRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _DeleteApiSpecRevision(RegistryRestStub):
        def __hash__(self):
            return hash("DeleteApiSpecRevision")

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
            request: registry_service.DeleteApiSpecRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the delete api spec revision method over HTTP.

            Args:
                request (~.registry_service.DeleteApiSpecRevisionRequest):
                    The request object. Request message for
                DeleteApiSpecRevision.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiSpec:
                    Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}:deleteRevision",
                },
            ]
            request, metadata = self._interceptor.pre_delete_api_spec_revision(
                request, metadata
            )
            pb_request = registry_service.DeleteApiSpecRevisionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiSpec()
            pb_resp = registry_models.ApiSpec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_api_spec_revision(resp)
            return resp

    class _DeleteApiVersion(RegistryRestStub):
        def __hash__(self):
            return hash("DeleteApiVersion")

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
            request: registry_service.DeleteApiVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete api version method over HTTP.

            Args:
                request (~.registry_service.DeleteApiVersionRequest):
                    The request object. Request message for DeleteApiVersion.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_api_version(
                request, metadata
            )
            pb_request = registry_service.DeleteApiVersionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _DeleteArtifact(RegistryRestStub):
        def __hash__(self):
            return hash("DeleteArtifact")

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
            request: registry_service.DeleteArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete artifact method over HTTP.

            Args:
                request (~.registry_service.DeleteArtifactRequest):
                    The request object. Request message for DeleteArtifact.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/artifacts/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/artifacts/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/artifacts/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*/artifacts/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*/artifacts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_artifact(request, metadata)
            pb_request = registry_service.DeleteArtifactRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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

    class _GetApi(RegistryRestStub):
        def __hash__(self):
            return hash("GetApi")

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
            request: registry_service.GetApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.Api:
            r"""Call the get api method over HTTP.

            Args:
                request (~.registry_service.GetApiRequest):
                    The request object. Request message for GetApi.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.Api:
                    A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_api(request, metadata)
            pb_request = registry_service.GetApiRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.Api()
            pb_resp = registry_models.Api.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api(resp)
            return resp

    class _GetApiDeployment(RegistryRestStub):
        def __hash__(self):
            return hash("GetApiDeployment")

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
            request: registry_service.GetApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the get api deployment method over HTTP.

            Args:
                request (~.registry_service.GetApiDeploymentRequest):
                    The request object. Request message for GetApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiDeployment:
                    Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_api_deployment(
                request, metadata
            )
            pb_request = registry_service.GetApiDeploymentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiDeployment()
            pb_resp = registry_models.ApiDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api_deployment(resp)
            return resp

    class _GetApiSpec(RegistryRestStub):
        def __hash__(self):
            return hash("GetApiSpec")

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
            request: registry_service.GetApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the get api spec method over HTTP.

            Args:
                request (~.registry_service.GetApiSpecRequest):
                    The request object. Request message for GetApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiSpec:
                    Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_api_spec(request, metadata)
            pb_request = registry_service.GetApiSpecRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiSpec()
            pb_resp = registry_models.ApiSpec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api_spec(resp)
            return resp

    class _GetApiSpecContents(RegistryRestStub):
        def __hash__(self):
            return hash("GetApiSpecContents")

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
            request: registry_service.GetApiSpecContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> httpbody_pb2.HttpBody:
            r"""Call the get api spec contents method over HTTP.

            Args:
                request (~.registry_service.GetApiSpecContentsRequest):
                    The request object. Request message for
                GetApiSpecContents.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.httpbody_pb2.HttpBody:
                    Message that represents an arbitrary HTTP body. It
                should only be used for payload formats that can't be
                represented as JSON, such as raw binary or an HTML page.

                This message can be used both in streaming and
                non-streaming API methods in the request as well as the
                response.

                It can be used as a top-level request field, which is
                convenient if one wants to extract parameters from
                either the URL or HTTP template into the request fields
                and also want access to the raw HTTP body.

                Example:

                ::

                    message GetResourceRequest {
                      // A unique request id.
                      string request_id = 1;

                      // The raw HTTP body is bound to this field.
                      google.api.HttpBody http_body = 2;

                    }

                    service ResourceService {
                      rpc GetResource(GetResourceRequest)
                        returns (google.api.HttpBody);
                      rpc UpdateResource(google.api.HttpBody)
                        returns (google.protobuf.Empty);

                    }

                Example with streaming methods:

                ::

                    service CaldavService {
                      rpc GetCalendar(stream google.api.HttpBody)
                        returns (stream google.api.HttpBody);
                      rpc UpdateCalendar(stream google.api.HttpBody)
                        returns (stream google.api.HttpBody);

                    }

                Use of this type only changes how the request and
                response bodies are handled, all other features will
                continue to work unchanged.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}:getContents",
                },
            ]
            request, metadata = self._interceptor.pre_get_api_spec_contents(
                request, metadata
            )
            pb_request = registry_service.GetApiSpecContentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = httpbody_pb2.HttpBody()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api_spec_contents(resp)
            return resp

    class _GetApiVersion(RegistryRestStub):
        def __hash__(self):
            return hash("GetApiVersion")

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
            request: registry_service.GetApiVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiVersion:
            r"""Call the get api version method over HTTP.

            Args:
                request (~.registry_service.GetApiVersionRequest):
                    The request object. Request message for GetApiVersion.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiVersion:
                    Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_api_version(request, metadata)
            pb_request = registry_service.GetApiVersionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiVersion()
            pb_resp = registry_models.ApiVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_api_version(resp)
            return resp

    class _GetArtifact(RegistryRestStub):
        def __hash__(self):
            return hash("GetArtifact")

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
            request: registry_service.GetArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.Artifact:
            r"""Call the get artifact method over HTTP.

            Args:
                request (~.registry_service.GetArtifactRequest):
                    The request object. Request message for GetArtifact.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.Artifact:
                    Artifacts of resources. Artifacts are unique
                (single-value) per resource and are used to store
                metadata that is too large or numerous to be stored
                directly on the resource. Since artifacts are stored
                separately from parent resources, they should generally
                be used for metadata that is needed infrequently, i.e.,
                not for display in primary views of the resource but
                perhaps displayed or downloaded upon request. The
                ``ListArtifacts`` method allows artifacts to be quickly
                enumerated and checked for presence without downloading
                their (potentially-large) contents.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/artifacts/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/artifacts/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/artifacts/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*/artifacts/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*/artifacts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_artifact(request, metadata)
            pb_request = registry_service.GetArtifactRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.Artifact()
            pb_resp = registry_models.Artifact.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_artifact(resp)
            return resp

    class _GetArtifactContents(RegistryRestStub):
        def __hash__(self):
            return hash("GetArtifactContents")

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
            request: registry_service.GetArtifactContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> httpbody_pb2.HttpBody:
            r"""Call the get artifact contents method over HTTP.

            Args:
                request (~.registry_service.GetArtifactContentsRequest):
                    The request object. Request message for
                GetArtifactContents.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.httpbody_pb2.HttpBody:
                    Message that represents an arbitrary HTTP body. It
                should only be used for payload formats that can't be
                represented as JSON, such as raw binary or an HTML page.

                This message can be used both in streaming and
                non-streaming API methods in the request as well as the
                response.

                It can be used as a top-level request field, which is
                convenient if one wants to extract parameters from
                either the URL or HTTP template into the request fields
                and also want access to the raw HTTP body.

                Example:

                ::

                    message GetResourceRequest {
                      // A unique request id.
                      string request_id = 1;

                      // The raw HTTP body is bound to this field.
                      google.api.HttpBody http_body = 2;

                    }

                    service ResourceService {
                      rpc GetResource(GetResourceRequest)
                        returns (google.api.HttpBody);
                      rpc UpdateResource(google.api.HttpBody)
                        returns (google.protobuf.Empty);

                    }

                Example with streaming methods:

                ::

                    service CaldavService {
                      rpc GetCalendar(stream google.api.HttpBody)
                        returns (stream google.api.HttpBody);
                      rpc UpdateCalendar(stream google.api.HttpBody)
                        returns (stream google.api.HttpBody);

                    }

                Use of this type only changes how the request and
                response bodies are handled, all other features will
                continue to work unchanged.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/artifacts/*}:getContents",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/artifacts/*}:getContents",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/artifacts/*}:getContents",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*/artifacts/*}:getContents",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*/artifacts/*}:getContents",
                },
            ]
            request, metadata = self._interceptor.pre_get_artifact_contents(
                request, metadata
            )
            pb_request = registry_service.GetArtifactContentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = httpbody_pb2.HttpBody()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_artifact_contents(resp)
            return resp

    class _ListApiDeploymentRevisions(RegistryRestStub):
        def __hash__(self):
            return hash("ListApiDeploymentRevisions")

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
            request: registry_service.ListApiDeploymentRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_service.ListApiDeploymentRevisionsResponse:
            r"""Call the list api deployment
            revisions method over HTTP.

                Args:
                    request (~.registry_service.ListApiDeploymentRevisionsRequest):
                        The request object. Request message for
                    ListApiDeploymentRevisions.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.registry_service.ListApiDeploymentRevisionsResponse:
                        Response message for
                    ListApiDeploymentRevisionsResponse.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*}:listRevisions",
                },
            ]
            request, metadata = self._interceptor.pre_list_api_deployment_revisions(
                request, metadata
            )
            pb_request = registry_service.ListApiDeploymentRevisionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_service.ListApiDeploymentRevisionsResponse()
            pb_resp = registry_service.ListApiDeploymentRevisionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_api_deployment_revisions(resp)
            return resp

    class _ListApiDeployments(RegistryRestStub):
        def __hash__(self):
            return hash("ListApiDeployments")

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
            request: registry_service.ListApiDeploymentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_service.ListApiDeploymentsResponse:
            r"""Call the list api deployments method over HTTP.

            Args:
                request (~.registry_service.ListApiDeploymentsRequest):
                    The request object. Request message for
                ListApiDeployments.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_service.ListApiDeploymentsResponse:
                    Response message for
                ListApiDeployments.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*}/deployments",
                },
            ]
            request, metadata = self._interceptor.pre_list_api_deployments(
                request, metadata
            )
            pb_request = registry_service.ListApiDeploymentsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_service.ListApiDeploymentsResponse()
            pb_resp = registry_service.ListApiDeploymentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_api_deployments(resp)
            return resp

    class _ListApis(RegistryRestStub):
        def __hash__(self):
            return hash("ListApis")

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
            request: registry_service.ListApisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_service.ListApisResponse:
            r"""Call the list apis method over HTTP.

            Args:
                request (~.registry_service.ListApisRequest):
                    The request object. Request message for ListApis.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_service.ListApisResponse:
                    Response message for ListApis.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/apis",
                },
            ]
            request, metadata = self._interceptor.pre_list_apis(request, metadata)
            pb_request = registry_service.ListApisRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_service.ListApisResponse()
            pb_resp = registry_service.ListApisResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_apis(resp)
            return resp

    class _ListApiSpecRevisions(RegistryRestStub):
        def __hash__(self):
            return hash("ListApiSpecRevisions")

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
            request: registry_service.ListApiSpecRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_service.ListApiSpecRevisionsResponse:
            r"""Call the list api spec revisions method over HTTP.

            Args:
                request (~.registry_service.ListApiSpecRevisionsRequest):
                    The request object. Request message for
                ListApiSpecRevisions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_service.ListApiSpecRevisionsResponse:
                    Response message for
                ListApiSpecRevisionsResponse.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}:listRevisions",
                },
            ]
            request, metadata = self._interceptor.pre_list_api_spec_revisions(
                request, metadata
            )
            pb_request = registry_service.ListApiSpecRevisionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_service.ListApiSpecRevisionsResponse()
            pb_resp = registry_service.ListApiSpecRevisionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_api_spec_revisions(resp)
            return resp

    class _ListApiSpecs(RegistryRestStub):
        def __hash__(self):
            return hash("ListApiSpecs")

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
            request: registry_service.ListApiSpecsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_service.ListApiSpecsResponse:
            r"""Call the list api specs method over HTTP.

            Args:
                request (~.registry_service.ListApiSpecsRequest):
                    The request object. Request message for ListApiSpecs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_service.ListApiSpecsResponse:
                    Response message for ListApiSpecs.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*}/specs",
                },
            ]
            request, metadata = self._interceptor.pre_list_api_specs(request, metadata)
            pb_request = registry_service.ListApiSpecsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_service.ListApiSpecsResponse()
            pb_resp = registry_service.ListApiSpecsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_api_specs(resp)
            return resp

    class _ListApiVersions(RegistryRestStub):
        def __hash__(self):
            return hash("ListApiVersions")

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
            request: registry_service.ListApiVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_service.ListApiVersionsResponse:
            r"""Call the list api versions method over HTTP.

            Args:
                request (~.registry_service.ListApiVersionsRequest):
                    The request object. Request message for ListApiVersions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_service.ListApiVersionsResponse:
                    Response message for ListApiVersions.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*}/versions",
                },
            ]
            request, metadata = self._interceptor.pre_list_api_versions(
                request, metadata
            )
            pb_request = registry_service.ListApiVersionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_service.ListApiVersionsResponse()
            pb_resp = registry_service.ListApiVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_api_versions(resp)
            return resp

    class _ListArtifacts(RegistryRestStub):
        def __hash__(self):
            return hash("ListArtifacts")

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
            request: registry_service.ListArtifactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_service.ListArtifactsResponse:
            r"""Call the list artifacts method over HTTP.

            Args:
                request (~.registry_service.ListArtifactsRequest):
                    The request object. Request message for ListArtifacts.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_service.ListArtifactsResponse:
                    Response message for ListArtifacts.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/artifacts",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*}/artifacts",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*}/artifacts",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/versions/*/specs/*}/artifacts",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/apis/*/deployments/*}/artifacts",
                },
            ]
            request, metadata = self._interceptor.pre_list_artifacts(request, metadata)
            pb_request = registry_service.ListArtifactsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_service.ListArtifactsResponse()
            pb_resp = registry_service.ListArtifactsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_artifacts(resp)
            return resp

    class _ReplaceArtifact(RegistryRestStub):
        def __hash__(self):
            return hash("ReplaceArtifact")

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
            request: registry_service.ReplaceArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.Artifact:
            r"""Call the replace artifact method over HTTP.

            Args:
                request (~.registry_service.ReplaceArtifactRequest):
                    The request object. Request message for ReplaceArtifact.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.Artifact:
                    Artifacts of resources. Artifacts are unique
                (single-value) per resource and are used to store
                metadata that is too large or numerous to be stored
                directly on the resource. Since artifacts are stored
                separately from parent resources, they should generally
                be used for metadata that is needed infrequently, i.e.,
                not for display in primary views of the resource but
                perhaps displayed or downloaded upon request. The
                ``ListArtifacts`` method allows artifacts to be quickly
                enumerated and checked for presence without downloading
                their (potentially-large) contents.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1/{artifact.name=projects/*/locations/*/artifacts/*}",
                    "body": "artifact",
                },
                {
                    "method": "put",
                    "uri": "/v1/{artifact.name=projects/*/locations/*/apis/*/artifacts/*}",
                    "body": "artifact",
                },
                {
                    "method": "put",
                    "uri": "/v1/{artifact.name=projects/*/locations/*/apis/*/versions/*/artifacts/*}",
                    "body": "artifact",
                },
                {
                    "method": "put",
                    "uri": "/v1/{artifact.name=projects/*/locations/*/apis/*/versions/*/specs/*/artifacts/*}",
                    "body": "artifact",
                },
                {
                    "method": "put",
                    "uri": "/v1/{artifact.name=projects/*/locations/*/apis/*/deployments/*/artifacts/*}",
                    "body": "artifact",
                },
            ]
            request, metadata = self._interceptor.pre_replace_artifact(
                request, metadata
            )
            pb_request = registry_service.ReplaceArtifactRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.Artifact()
            pb_resp = registry_models.Artifact.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_replace_artifact(resp)
            return resp

    class _RollbackApiDeployment(RegistryRestStub):
        def __hash__(self):
            return hash("RollbackApiDeployment")

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
            request: registry_service.RollbackApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the rollback api deployment method over HTTP.

            Args:
                request (~.registry_service.RollbackApiDeploymentRequest):
                    The request object. Request message for
                RollbackApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiDeployment:
                    Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*}:rollback",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rollback_api_deployment(
                request, metadata
            )
            pb_request = registry_service.RollbackApiDeploymentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiDeployment()
            pb_resp = registry_models.ApiDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rollback_api_deployment(resp)
            return resp

    class _RollbackApiSpec(RegistryRestStub):
        def __hash__(self):
            return hash("RollbackApiSpec")

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
            request: registry_service.RollbackApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the rollback api spec method over HTTP.

            Args:
                request (~.registry_service.RollbackApiSpecRequest):
                    The request object. Request message for RollbackApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiSpec:
                    Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}:rollback",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rollback_api_spec(
                request, metadata
            )
            pb_request = registry_service.RollbackApiSpecRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiSpec()
            pb_resp = registry_models.ApiSpec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rollback_api_spec(resp)
            return resp

    class _TagApiDeploymentRevision(RegistryRestStub):
        def __hash__(self):
            return hash("TagApiDeploymentRevision")

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
            request: registry_service.TagApiDeploymentRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the tag api deployment
            revision method over HTTP.

                Args:
                    request (~.registry_service.TagApiDeploymentRevisionRequest):
                        The request object. Request message for
                    TagApiDeploymentRevision.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.registry_models.ApiDeployment:
                        Describes a service running at
                    particular address that provides a
                    particular version of an API.
                    ApiDeployments have revisions which
                    correspond to different configurations
                    of a single deployment in time. Revision
                    identifiers should be updated whenever
                    the served API spec or endpoint address
                    changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/deployments/*}:tagRevision",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_tag_api_deployment_revision(
                request, metadata
            )
            pb_request = registry_service.TagApiDeploymentRevisionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiDeployment()
            pb_resp = registry_models.ApiDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_tag_api_deployment_revision(resp)
            return resp

    class _TagApiSpecRevision(RegistryRestStub):
        def __hash__(self):
            return hash("TagApiSpecRevision")

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
            request: registry_service.TagApiSpecRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the tag api spec revision method over HTTP.

            Args:
                request (~.registry_service.TagApiSpecRevisionRequest):
                    The request object. Request message for
                TagApiSpecRevision.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiSpec:
                    Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/apis/*/versions/*/specs/*}:tagRevision",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_tag_api_spec_revision(
                request, metadata
            )
            pb_request = registry_service.TagApiSpecRevisionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiSpec()
            pb_resp = registry_models.ApiSpec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_tag_api_spec_revision(resp)
            return resp

    class _UpdateApi(RegistryRestStub):
        def __hash__(self):
            return hash("UpdateApi")

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
            request: registry_service.UpdateApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.Api:
            r"""Call the update api method over HTTP.

            Args:
                request (~.registry_service.UpdateApiRequest):
                    The request object. Request message for UpdateApi.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.Api:
                    A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{api.name=projects/*/locations/*/apis/*}",
                    "body": "api",
                },
            ]
            request, metadata = self._interceptor.pre_update_api(request, metadata)
            pb_request = registry_service.UpdateApiRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.Api()
            pb_resp = registry_models.Api.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_api(resp)
            return resp

    class _UpdateApiDeployment(RegistryRestStub):
        def __hash__(self):
            return hash("UpdateApiDeployment")

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
            request: registry_service.UpdateApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the update api deployment method over HTTP.

            Args:
                request (~.registry_service.UpdateApiDeploymentRequest):
                    The request object. Request message for
                UpdateApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiDeployment:
                    Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{api_deployment.name=projects/*/locations/*/apis/*/deployments/*}",
                    "body": "api_deployment",
                },
            ]
            request, metadata = self._interceptor.pre_update_api_deployment(
                request, metadata
            )
            pb_request = registry_service.UpdateApiDeploymentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiDeployment()
            pb_resp = registry_models.ApiDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_api_deployment(resp)
            return resp

    class _UpdateApiSpec(RegistryRestStub):
        def __hash__(self):
            return hash("UpdateApiSpec")

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
            request: registry_service.UpdateApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the update api spec method over HTTP.

            Args:
                request (~.registry_service.UpdateApiSpecRequest):
                    The request object. Request message for UpdateApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiSpec:
                    Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{api_spec.name=projects/*/locations/*/apis/*/versions/*/specs/*}",
                    "body": "api_spec",
                },
            ]
            request, metadata = self._interceptor.pre_update_api_spec(request, metadata)
            pb_request = registry_service.UpdateApiSpecRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiSpec()
            pb_resp = registry_models.ApiSpec.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_api_spec(resp)
            return resp

    class _UpdateApiVersion(RegistryRestStub):
        def __hash__(self):
            return hash("UpdateApiVersion")

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
            request: registry_service.UpdateApiVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> registry_models.ApiVersion:
            r"""Call the update api version method over HTTP.

            Args:
                request (~.registry_service.UpdateApiVersionRequest):
                    The request object. Request message for UpdateApiVersion.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.registry_models.ApiVersion:
                    Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{api_version.name=projects/*/locations/*/apis/*/versions/*}",
                    "body": "api_version",
                },
            ]
            request, metadata = self._interceptor.pre_update_api_version(
                request, metadata
            )
            pb_request = registry_service.UpdateApiVersionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
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
            resp = registry_models.ApiVersion()
            pb_resp = registry_models.ApiVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_api_version(resp)
            return resp

    @property
    def create_api(
        self,
    ) -> Callable[[registry_service.CreateApiRequest], registry_models.Api]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_api_deployment(
        self,
    ) -> Callable[
        [registry_service.CreateApiDeploymentRequest], registry_models.ApiDeployment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApiDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_api_spec(
        self,
    ) -> Callable[[registry_service.CreateApiSpecRequest], registry_models.ApiSpec]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApiSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_api_version(
        self,
    ) -> Callable[
        [registry_service.CreateApiVersionRequest], registry_models.ApiVersion
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateApiVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_artifact(
        self,
    ) -> Callable[[registry_service.CreateArtifactRequest], registry_models.Artifact]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateArtifact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api(
        self,
    ) -> Callable[[registry_service.DeleteApiRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api_deployment(
        self,
    ) -> Callable[[registry_service.DeleteApiDeploymentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApiDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api_deployment_revision(
        self,
    ) -> Callable[
        [registry_service.DeleteApiDeploymentRevisionRequest],
        registry_models.ApiDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApiDeploymentRevision(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api_spec(
        self,
    ) -> Callable[[registry_service.DeleteApiSpecRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApiSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api_spec_revision(
        self,
    ) -> Callable[
        [registry_service.DeleteApiSpecRevisionRequest], registry_models.ApiSpec
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApiSpecRevision(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_api_version(
        self,
    ) -> Callable[[registry_service.DeleteApiVersionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteApiVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_artifact(
        self,
    ) -> Callable[[registry_service.DeleteArtifactRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteArtifact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api(
        self,
    ) -> Callable[[registry_service.GetApiRequest], registry_models.Api]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api_deployment(
        self,
    ) -> Callable[
        [registry_service.GetApiDeploymentRequest], registry_models.ApiDeployment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApiDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api_spec(
        self,
    ) -> Callable[[registry_service.GetApiSpecRequest], registry_models.ApiSpec]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApiSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api_spec_contents(
        self,
    ) -> Callable[[registry_service.GetApiSpecContentsRequest], httpbody_pb2.HttpBody]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApiSpecContents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_api_version(
        self,
    ) -> Callable[[registry_service.GetApiVersionRequest], registry_models.ApiVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetApiVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_artifact(
        self,
    ) -> Callable[[registry_service.GetArtifactRequest], registry_models.Artifact]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetArtifact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_artifact_contents(
        self,
    ) -> Callable[[registry_service.GetArtifactContentsRequest], httpbody_pb2.HttpBody]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetArtifactContents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_api_deployment_revisions(
        self,
    ) -> Callable[
        [registry_service.ListApiDeploymentRevisionsRequest],
        registry_service.ListApiDeploymentRevisionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApiDeploymentRevisions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_api_deployments(
        self,
    ) -> Callable[
        [registry_service.ListApiDeploymentsRequest],
        registry_service.ListApiDeploymentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApiDeployments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_apis(
        self,
    ) -> Callable[
        [registry_service.ListApisRequest], registry_service.ListApisResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_api_spec_revisions(
        self,
    ) -> Callable[
        [registry_service.ListApiSpecRevisionsRequest],
        registry_service.ListApiSpecRevisionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApiSpecRevisions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_api_specs(
        self,
    ) -> Callable[
        [registry_service.ListApiSpecsRequest], registry_service.ListApiSpecsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApiSpecs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_api_versions(
        self,
    ) -> Callable[
        [registry_service.ListApiVersionsRequest],
        registry_service.ListApiVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListApiVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_artifacts(
        self,
    ) -> Callable[
        [registry_service.ListArtifactsRequest], registry_service.ListArtifactsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListArtifacts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def replace_artifact(
        self,
    ) -> Callable[[registry_service.ReplaceArtifactRequest], registry_models.Artifact]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReplaceArtifact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rollback_api_deployment(
        self,
    ) -> Callable[
        [registry_service.RollbackApiDeploymentRequest], registry_models.ApiDeployment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RollbackApiDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rollback_api_spec(
        self,
    ) -> Callable[[registry_service.RollbackApiSpecRequest], registry_models.ApiSpec]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RollbackApiSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def tag_api_deployment_revision(
        self,
    ) -> Callable[
        [registry_service.TagApiDeploymentRevisionRequest],
        registry_models.ApiDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TagApiDeploymentRevision(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def tag_api_spec_revision(
        self,
    ) -> Callable[
        [registry_service.TagApiSpecRevisionRequest], registry_models.ApiSpec
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TagApiSpecRevision(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_api(
        self,
    ) -> Callable[[registry_service.UpdateApiRequest], registry_models.Api]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApi(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_api_deployment(
        self,
    ) -> Callable[
        [registry_service.UpdateApiDeploymentRequest], registry_models.ApiDeployment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApiDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_api_spec(
        self,
    ) -> Callable[[registry_service.UpdateApiSpecRequest], registry_models.ApiSpec]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApiSpec(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_api_version(
        self,
    ) -> Callable[
        [registry_service.UpdateApiVersionRequest], registry_models.ApiVersion
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateApiVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(RegistryRestStub):
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

    class _ListLocations(RegistryRestStub):
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
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(RegistryRestStub):
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
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/deployments/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/specs/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/artifacts/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/artifacts/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/artifacts/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/specs/*/artifacts/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/instances/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/runtime}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(RegistryRestStub):
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
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/deployments/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/specs/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/artifacts/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/artifacts/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/artifacts/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/specs/*/artifacts/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/instances/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/runtime}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(RegistryRestStub):
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
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/deployments/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/specs/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/artifacts/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/artifacts/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/artifacts/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/apis/*/versions/*/specs/*/artifacts/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/instances/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/runtime}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(RegistryRestStub):
        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(RegistryRestStub):
        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(RegistryRestStub):
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
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(RegistryRestStub):
        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
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

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegistryRestTransport",)
