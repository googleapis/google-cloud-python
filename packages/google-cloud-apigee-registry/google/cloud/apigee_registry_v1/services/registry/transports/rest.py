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
import dataclasses
import json  # type: ignore
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api import httpbody_pb2  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import google.protobuf
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.apigee_registry_v1.types import registry_models, registry_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseRegistryRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.CreateApiRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_api(self, response: registry_models.Api) -> registry_models.Api:
        """Post-rpc interceptor for create_api

        DEPRECATED. Please use the `post_create_api_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_create_api` interceptor runs
        before the `post_create_api_with_metadata` interceptor.
        """
        return response

    def post_create_api_with_metadata(
        self,
        response: registry_models.Api,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.Api, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_api

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_create_api_with_metadata`
        interceptor in new development instead of the `post_create_api` interceptor.
        When both interceptors are used, this `post_create_api_with_metadata` interceptor runs after the
        `post_create_api` interceptor. The (possibly modified) response returned by
        `post_create_api` will be passed to
        `post_create_api_with_metadata`.
        """
        return response, metadata

    def pre_create_api_deployment(
        self,
        request: registry_service.CreateApiDeploymentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.CreateApiDeploymentRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_api_deployment(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for create_api_deployment

        DEPRECATED. Please use the `post_create_api_deployment_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_create_api_deployment` interceptor runs
        before the `post_create_api_deployment_with_metadata` interceptor.
        """
        return response

    def post_create_api_deployment_with_metadata(
        self,
        response: registry_models.ApiDeployment,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiDeployment, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_api_deployment

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_create_api_deployment_with_metadata`
        interceptor in new development instead of the `post_create_api_deployment` interceptor.
        When both interceptors are used, this `post_create_api_deployment_with_metadata` interceptor runs after the
        `post_create_api_deployment` interceptor. The (possibly modified) response returned by
        `post_create_api_deployment` will be passed to
        `post_create_api_deployment_with_metadata`.
        """
        return response, metadata

    def pre_create_api_spec(
        self,
        request: registry_service.CreateApiSpecRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.CreateApiSpecRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_api_spec(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for create_api_spec

        DEPRECATED. Please use the `post_create_api_spec_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_create_api_spec` interceptor runs
        before the `post_create_api_spec_with_metadata` interceptor.
        """
        return response

    def post_create_api_spec_with_metadata(
        self,
        response: registry_models.ApiSpec,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiSpec, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_api_spec

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_create_api_spec_with_metadata`
        interceptor in new development instead of the `post_create_api_spec` interceptor.
        When both interceptors are used, this `post_create_api_spec_with_metadata` interceptor runs after the
        `post_create_api_spec` interceptor. The (possibly modified) response returned by
        `post_create_api_spec` will be passed to
        `post_create_api_spec_with_metadata`.
        """
        return response, metadata

    def pre_create_api_version(
        self,
        request: registry_service.CreateApiVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.CreateApiVersionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_api_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_api_version(
        self, response: registry_models.ApiVersion
    ) -> registry_models.ApiVersion:
        """Post-rpc interceptor for create_api_version

        DEPRECATED. Please use the `post_create_api_version_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_create_api_version` interceptor runs
        before the `post_create_api_version_with_metadata` interceptor.
        """
        return response

    def post_create_api_version_with_metadata(
        self,
        response: registry_models.ApiVersion,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiVersion, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_api_version

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_create_api_version_with_metadata`
        interceptor in new development instead of the `post_create_api_version` interceptor.
        When both interceptors are used, this `post_create_api_version_with_metadata` interceptor runs after the
        `post_create_api_version` interceptor. The (possibly modified) response returned by
        `post_create_api_version` will be passed to
        `post_create_api_version_with_metadata`.
        """
        return response, metadata

    def pre_create_artifact(
        self,
        request: registry_service.CreateArtifactRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.CreateArtifactRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_create_artifact(
        self, response: registry_models.Artifact
    ) -> registry_models.Artifact:
        """Post-rpc interceptor for create_artifact

        DEPRECATED. Please use the `post_create_artifact_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_create_artifact` interceptor runs
        before the `post_create_artifact_with_metadata` interceptor.
        """
        return response

    def post_create_artifact_with_metadata(
        self,
        response: registry_models.Artifact,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.Artifact, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_artifact

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_create_artifact_with_metadata`
        interceptor in new development instead of the `post_create_artifact` interceptor.
        When both interceptors are used, this `post_create_artifact_with_metadata` interceptor runs after the
        `post_create_artifact` interceptor. The (possibly modified) response returned by
        `post_create_artifact` will be passed to
        `post_create_artifact_with_metadata`.
        """
        return response, metadata

    def pre_delete_api(
        self,
        request: registry_service.DeleteApiRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.DeleteApiRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_delete_api_deployment(
        self,
        request: registry_service.DeleteApiDeploymentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.DeleteApiDeploymentRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_delete_api_deployment_revision(
        self,
        request: registry_service.DeleteApiDeploymentRevisionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.DeleteApiDeploymentRevisionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
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

        DEPRECATED. Please use the `post_delete_api_deployment_revision_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_delete_api_deployment_revision` interceptor runs
        before the `post_delete_api_deployment_revision_with_metadata` interceptor.
        """
        return response

    def post_delete_api_deployment_revision_with_metadata(
        self,
        response: registry_models.ApiDeployment,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiDeployment, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_api_deployment_revision

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_delete_api_deployment_revision_with_metadata`
        interceptor in new development instead of the `post_delete_api_deployment_revision` interceptor.
        When both interceptors are used, this `post_delete_api_deployment_revision_with_metadata` interceptor runs after the
        `post_delete_api_deployment_revision` interceptor. The (possibly modified) response returned by
        `post_delete_api_deployment_revision` will be passed to
        `post_delete_api_deployment_revision_with_metadata`.
        """
        return response, metadata

    def pre_delete_api_spec(
        self,
        request: registry_service.DeleteApiSpecRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.DeleteApiSpecRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_delete_api_spec_revision(
        self,
        request: registry_service.DeleteApiSpecRevisionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.DeleteApiSpecRevisionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
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

        DEPRECATED. Please use the `post_delete_api_spec_revision_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_delete_api_spec_revision` interceptor runs
        before the `post_delete_api_spec_revision_with_metadata` interceptor.
        """
        return response

    def post_delete_api_spec_revision_with_metadata(
        self,
        response: registry_models.ApiSpec,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiSpec, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_api_spec_revision

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_delete_api_spec_revision_with_metadata`
        interceptor in new development instead of the `post_delete_api_spec_revision` interceptor.
        When both interceptors are used, this `post_delete_api_spec_revision_with_metadata` interceptor runs after the
        `post_delete_api_spec_revision` interceptor. The (possibly modified) response returned by
        `post_delete_api_spec_revision` will be passed to
        `post_delete_api_spec_revision_with_metadata`.
        """
        return response, metadata

    def pre_delete_api_version(
        self,
        request: registry_service.DeleteApiVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.DeleteApiVersionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_api_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_delete_artifact(
        self,
        request: registry_service.DeleteArtifactRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.DeleteArtifactRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def pre_get_api(
        self,
        request: registry_service.GetApiRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_service.GetApiRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api(self, response: registry_models.Api) -> registry_models.Api:
        """Post-rpc interceptor for get_api

        DEPRECATED. Please use the `post_get_api_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_get_api` interceptor runs
        before the `post_get_api_with_metadata` interceptor.
        """
        return response

    def post_get_api_with_metadata(
        self,
        response: registry_models.Api,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.Api, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_api

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_get_api_with_metadata`
        interceptor in new development instead of the `post_get_api` interceptor.
        When both interceptors are used, this `post_get_api_with_metadata` interceptor runs after the
        `post_get_api` interceptor. The (possibly modified) response returned by
        `post_get_api` will be passed to
        `post_get_api_with_metadata`.
        """
        return response, metadata

    def pre_get_api_deployment(
        self,
        request: registry_service.GetApiDeploymentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.GetApiDeploymentRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api_deployment(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for get_api_deployment

        DEPRECATED. Please use the `post_get_api_deployment_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_get_api_deployment` interceptor runs
        before the `post_get_api_deployment_with_metadata` interceptor.
        """
        return response

    def post_get_api_deployment_with_metadata(
        self,
        response: registry_models.ApiDeployment,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiDeployment, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_api_deployment

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_get_api_deployment_with_metadata`
        interceptor in new development instead of the `post_get_api_deployment` interceptor.
        When both interceptors are used, this `post_get_api_deployment_with_metadata` interceptor runs after the
        `post_get_api_deployment` interceptor. The (possibly modified) response returned by
        `post_get_api_deployment` will be passed to
        `post_get_api_deployment_with_metadata`.
        """
        return response, metadata

    def pre_get_api_spec(
        self,
        request: registry_service.GetApiSpecRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.GetApiSpecRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api_spec(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for get_api_spec

        DEPRECATED. Please use the `post_get_api_spec_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_get_api_spec` interceptor runs
        before the `post_get_api_spec_with_metadata` interceptor.
        """
        return response

    def post_get_api_spec_with_metadata(
        self,
        response: registry_models.ApiSpec,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiSpec, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_api_spec

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_get_api_spec_with_metadata`
        interceptor in new development instead of the `post_get_api_spec` interceptor.
        When both interceptors are used, this `post_get_api_spec_with_metadata` interceptor runs after the
        `post_get_api_spec` interceptor. The (possibly modified) response returned by
        `post_get_api_spec` will be passed to
        `post_get_api_spec_with_metadata`.
        """
        return response, metadata

    def pre_get_api_spec_contents(
        self,
        request: registry_service.GetApiSpecContentsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.GetApiSpecContentsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_api_spec_contents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api_spec_contents(
        self, response: httpbody_pb2.HttpBody
    ) -> httpbody_pb2.HttpBody:
        """Post-rpc interceptor for get_api_spec_contents

        DEPRECATED. Please use the `post_get_api_spec_contents_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_get_api_spec_contents` interceptor runs
        before the `post_get_api_spec_contents_with_metadata` interceptor.
        """
        return response

    def post_get_api_spec_contents_with_metadata(
        self,
        response: httpbody_pb2.HttpBody,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[httpbody_pb2.HttpBody, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_api_spec_contents

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_get_api_spec_contents_with_metadata`
        interceptor in new development instead of the `post_get_api_spec_contents` interceptor.
        When both interceptors are used, this `post_get_api_spec_contents_with_metadata` interceptor runs after the
        `post_get_api_spec_contents` interceptor. The (possibly modified) response returned by
        `post_get_api_spec_contents` will be passed to
        `post_get_api_spec_contents_with_metadata`.
        """
        return response, metadata

    def pre_get_api_version(
        self,
        request: registry_service.GetApiVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.GetApiVersionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_api_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_api_version(
        self, response: registry_models.ApiVersion
    ) -> registry_models.ApiVersion:
        """Post-rpc interceptor for get_api_version

        DEPRECATED. Please use the `post_get_api_version_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_get_api_version` interceptor runs
        before the `post_get_api_version_with_metadata` interceptor.
        """
        return response

    def post_get_api_version_with_metadata(
        self,
        response: registry_models.ApiVersion,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiVersion, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_api_version

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_get_api_version_with_metadata`
        interceptor in new development instead of the `post_get_api_version` interceptor.
        When both interceptors are used, this `post_get_api_version_with_metadata` interceptor runs after the
        `post_get_api_version` interceptor. The (possibly modified) response returned by
        `post_get_api_version` will be passed to
        `post_get_api_version_with_metadata`.
        """
        return response, metadata

    def pre_get_artifact(
        self,
        request: registry_service.GetArtifactRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.GetArtifactRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_artifact(
        self, response: registry_models.Artifact
    ) -> registry_models.Artifact:
        """Post-rpc interceptor for get_artifact

        DEPRECATED. Please use the `post_get_artifact_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_get_artifact` interceptor runs
        before the `post_get_artifact_with_metadata` interceptor.
        """
        return response

    def post_get_artifact_with_metadata(
        self,
        response: registry_models.Artifact,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.Artifact, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_artifact

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_get_artifact_with_metadata`
        interceptor in new development instead of the `post_get_artifact` interceptor.
        When both interceptors are used, this `post_get_artifact_with_metadata` interceptor runs after the
        `post_get_artifact` interceptor. The (possibly modified) response returned by
        `post_get_artifact` will be passed to
        `post_get_artifact_with_metadata`.
        """
        return response, metadata

    def pre_get_artifact_contents(
        self,
        request: registry_service.GetArtifactContentsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.GetArtifactContentsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_artifact_contents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_get_artifact_contents(
        self, response: httpbody_pb2.HttpBody
    ) -> httpbody_pb2.HttpBody:
        """Post-rpc interceptor for get_artifact_contents

        DEPRECATED. Please use the `post_get_artifact_contents_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_get_artifact_contents` interceptor runs
        before the `post_get_artifact_contents_with_metadata` interceptor.
        """
        return response

    def post_get_artifact_contents_with_metadata(
        self,
        response: httpbody_pb2.HttpBody,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[httpbody_pb2.HttpBody, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_artifact_contents

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_get_artifact_contents_with_metadata`
        interceptor in new development instead of the `post_get_artifact_contents` interceptor.
        When both interceptors are used, this `post_get_artifact_contents_with_metadata` interceptor runs after the
        `post_get_artifact_contents` interceptor. The (possibly modified) response returned by
        `post_get_artifact_contents` will be passed to
        `post_get_artifact_contents_with_metadata`.
        """
        return response, metadata

    def pre_list_api_deployment_revisions(
        self,
        request: registry_service.ListApiDeploymentRevisionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiDeploymentRevisionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
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

        DEPRECATED. Please use the `post_list_api_deployment_revisions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_list_api_deployment_revisions` interceptor runs
        before the `post_list_api_deployment_revisions_with_metadata` interceptor.
        """
        return response

    def post_list_api_deployment_revisions_with_metadata(
        self,
        response: registry_service.ListApiDeploymentRevisionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiDeploymentRevisionsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_api_deployment_revisions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_list_api_deployment_revisions_with_metadata`
        interceptor in new development instead of the `post_list_api_deployment_revisions` interceptor.
        When both interceptors are used, this `post_list_api_deployment_revisions_with_metadata` interceptor runs after the
        `post_list_api_deployment_revisions` interceptor. The (possibly modified) response returned by
        `post_list_api_deployment_revisions` will be passed to
        `post_list_api_deployment_revisions_with_metadata`.
        """
        return response, metadata

    def pre_list_api_deployments(
        self,
        request: registry_service.ListApiDeploymentsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiDeploymentsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_api_deployments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_deployments(
        self, response: registry_service.ListApiDeploymentsResponse
    ) -> registry_service.ListApiDeploymentsResponse:
        """Post-rpc interceptor for list_api_deployments

        DEPRECATED. Please use the `post_list_api_deployments_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_list_api_deployments` interceptor runs
        before the `post_list_api_deployments_with_metadata` interceptor.
        """
        return response

    def post_list_api_deployments_with_metadata(
        self,
        response: registry_service.ListApiDeploymentsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiDeploymentsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_api_deployments

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_list_api_deployments_with_metadata`
        interceptor in new development instead of the `post_list_api_deployments` interceptor.
        When both interceptors are used, this `post_list_api_deployments_with_metadata` interceptor runs after the
        `post_list_api_deployments` interceptor. The (possibly modified) response returned by
        `post_list_api_deployments` will be passed to
        `post_list_api_deployments_with_metadata`.
        """
        return response, metadata

    def pre_list_apis(
        self,
        request: registry_service.ListApisRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApisRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_apis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_apis(
        self, response: registry_service.ListApisResponse
    ) -> registry_service.ListApisResponse:
        """Post-rpc interceptor for list_apis

        DEPRECATED. Please use the `post_list_apis_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_list_apis` interceptor runs
        before the `post_list_apis_with_metadata` interceptor.
        """
        return response

    def post_list_apis_with_metadata(
        self,
        response: registry_service.ListApisResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApisResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_apis

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_list_apis_with_metadata`
        interceptor in new development instead of the `post_list_apis` interceptor.
        When both interceptors are used, this `post_list_apis_with_metadata` interceptor runs after the
        `post_list_apis` interceptor. The (possibly modified) response returned by
        `post_list_apis` will be passed to
        `post_list_apis_with_metadata`.
        """
        return response, metadata

    def pre_list_api_spec_revisions(
        self,
        request: registry_service.ListApiSpecRevisionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiSpecRevisionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_api_spec_revisions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_spec_revisions(
        self, response: registry_service.ListApiSpecRevisionsResponse
    ) -> registry_service.ListApiSpecRevisionsResponse:
        """Post-rpc interceptor for list_api_spec_revisions

        DEPRECATED. Please use the `post_list_api_spec_revisions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_list_api_spec_revisions` interceptor runs
        before the `post_list_api_spec_revisions_with_metadata` interceptor.
        """
        return response

    def post_list_api_spec_revisions_with_metadata(
        self,
        response: registry_service.ListApiSpecRevisionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiSpecRevisionsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_api_spec_revisions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_list_api_spec_revisions_with_metadata`
        interceptor in new development instead of the `post_list_api_spec_revisions` interceptor.
        When both interceptors are used, this `post_list_api_spec_revisions_with_metadata` interceptor runs after the
        `post_list_api_spec_revisions` interceptor. The (possibly modified) response returned by
        `post_list_api_spec_revisions` will be passed to
        `post_list_api_spec_revisions_with_metadata`.
        """
        return response, metadata

    def pre_list_api_specs(
        self,
        request: registry_service.ListApiSpecsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiSpecsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_api_specs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_specs(
        self, response: registry_service.ListApiSpecsResponse
    ) -> registry_service.ListApiSpecsResponse:
        """Post-rpc interceptor for list_api_specs

        DEPRECATED. Please use the `post_list_api_specs_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_list_api_specs` interceptor runs
        before the `post_list_api_specs_with_metadata` interceptor.
        """
        return response

    def post_list_api_specs_with_metadata(
        self,
        response: registry_service.ListApiSpecsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiSpecsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_api_specs

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_list_api_specs_with_metadata`
        interceptor in new development instead of the `post_list_api_specs` interceptor.
        When both interceptors are used, this `post_list_api_specs_with_metadata` interceptor runs after the
        `post_list_api_specs` interceptor. The (possibly modified) response returned by
        `post_list_api_specs` will be passed to
        `post_list_api_specs_with_metadata`.
        """
        return response, metadata

    def pre_list_api_versions(
        self,
        request: registry_service.ListApiVersionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiVersionsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_api_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_api_versions(
        self, response: registry_service.ListApiVersionsResponse
    ) -> registry_service.ListApiVersionsResponse:
        """Post-rpc interceptor for list_api_versions

        DEPRECATED. Please use the `post_list_api_versions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_list_api_versions` interceptor runs
        before the `post_list_api_versions_with_metadata` interceptor.
        """
        return response

    def post_list_api_versions_with_metadata(
        self,
        response: registry_service.ListApiVersionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListApiVersionsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_api_versions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_list_api_versions_with_metadata`
        interceptor in new development instead of the `post_list_api_versions` interceptor.
        When both interceptors are used, this `post_list_api_versions_with_metadata` interceptor runs after the
        `post_list_api_versions` interceptor. The (possibly modified) response returned by
        `post_list_api_versions` will be passed to
        `post_list_api_versions_with_metadata`.
        """
        return response, metadata

    def pre_list_artifacts(
        self,
        request: registry_service.ListArtifactsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListArtifactsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_artifacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_list_artifacts(
        self, response: registry_service.ListArtifactsResponse
    ) -> registry_service.ListArtifactsResponse:
        """Post-rpc interceptor for list_artifacts

        DEPRECATED. Please use the `post_list_artifacts_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_list_artifacts` interceptor runs
        before the `post_list_artifacts_with_metadata` interceptor.
        """
        return response

    def post_list_artifacts_with_metadata(
        self,
        response: registry_service.ListArtifactsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ListArtifactsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_artifacts

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_list_artifacts_with_metadata`
        interceptor in new development instead of the `post_list_artifacts` interceptor.
        When both interceptors are used, this `post_list_artifacts_with_metadata` interceptor runs after the
        `post_list_artifacts` interceptor. The (possibly modified) response returned by
        `post_list_artifacts` will be passed to
        `post_list_artifacts_with_metadata`.
        """
        return response, metadata

    def pre_replace_artifact(
        self,
        request: registry_service.ReplaceArtifactRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.ReplaceArtifactRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for replace_artifact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_replace_artifact(
        self, response: registry_models.Artifact
    ) -> registry_models.Artifact:
        """Post-rpc interceptor for replace_artifact

        DEPRECATED. Please use the `post_replace_artifact_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_replace_artifact` interceptor runs
        before the `post_replace_artifact_with_metadata` interceptor.
        """
        return response

    def post_replace_artifact_with_metadata(
        self,
        response: registry_models.Artifact,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.Artifact, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for replace_artifact

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_replace_artifact_with_metadata`
        interceptor in new development instead of the `post_replace_artifact` interceptor.
        When both interceptors are used, this `post_replace_artifact_with_metadata` interceptor runs after the
        `post_replace_artifact` interceptor. The (possibly modified) response returned by
        `post_replace_artifact` will be passed to
        `post_replace_artifact_with_metadata`.
        """
        return response, metadata

    def pre_rollback_api_deployment(
        self,
        request: registry_service.RollbackApiDeploymentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.RollbackApiDeploymentRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
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

        DEPRECATED. Please use the `post_rollback_api_deployment_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_rollback_api_deployment` interceptor runs
        before the `post_rollback_api_deployment_with_metadata` interceptor.
        """
        return response

    def post_rollback_api_deployment_with_metadata(
        self,
        response: registry_models.ApiDeployment,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiDeployment, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for rollback_api_deployment

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_rollback_api_deployment_with_metadata`
        interceptor in new development instead of the `post_rollback_api_deployment` interceptor.
        When both interceptors are used, this `post_rollback_api_deployment_with_metadata` interceptor runs after the
        `post_rollback_api_deployment` interceptor. The (possibly modified) response returned by
        `post_rollback_api_deployment` will be passed to
        `post_rollback_api_deployment_with_metadata`.
        """
        return response, metadata

    def pre_rollback_api_spec(
        self,
        request: registry_service.RollbackApiSpecRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.RollbackApiSpecRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for rollback_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_rollback_api_spec(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for rollback_api_spec

        DEPRECATED. Please use the `post_rollback_api_spec_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_rollback_api_spec` interceptor runs
        before the `post_rollback_api_spec_with_metadata` interceptor.
        """
        return response

    def post_rollback_api_spec_with_metadata(
        self,
        response: registry_models.ApiSpec,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiSpec, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for rollback_api_spec

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_rollback_api_spec_with_metadata`
        interceptor in new development instead of the `post_rollback_api_spec` interceptor.
        When both interceptors are used, this `post_rollback_api_spec_with_metadata` interceptor runs after the
        `post_rollback_api_spec` interceptor. The (possibly modified) response returned by
        `post_rollback_api_spec` will be passed to
        `post_rollback_api_spec_with_metadata`.
        """
        return response, metadata

    def pre_tag_api_deployment_revision(
        self,
        request: registry_service.TagApiDeploymentRevisionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.TagApiDeploymentRevisionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
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

        DEPRECATED. Please use the `post_tag_api_deployment_revision_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_tag_api_deployment_revision` interceptor runs
        before the `post_tag_api_deployment_revision_with_metadata` interceptor.
        """
        return response

    def post_tag_api_deployment_revision_with_metadata(
        self,
        response: registry_models.ApiDeployment,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiDeployment, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for tag_api_deployment_revision

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_tag_api_deployment_revision_with_metadata`
        interceptor in new development instead of the `post_tag_api_deployment_revision` interceptor.
        When both interceptors are used, this `post_tag_api_deployment_revision_with_metadata` interceptor runs after the
        `post_tag_api_deployment_revision` interceptor. The (possibly modified) response returned by
        `post_tag_api_deployment_revision` will be passed to
        `post_tag_api_deployment_revision_with_metadata`.
        """
        return response, metadata

    def pre_tag_api_spec_revision(
        self,
        request: registry_service.TagApiSpecRevisionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.TagApiSpecRevisionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for tag_api_spec_revision

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_tag_api_spec_revision(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for tag_api_spec_revision

        DEPRECATED. Please use the `post_tag_api_spec_revision_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_tag_api_spec_revision` interceptor runs
        before the `post_tag_api_spec_revision_with_metadata` interceptor.
        """
        return response

    def post_tag_api_spec_revision_with_metadata(
        self,
        response: registry_models.ApiSpec,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiSpec, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for tag_api_spec_revision

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_tag_api_spec_revision_with_metadata`
        interceptor in new development instead of the `post_tag_api_spec_revision` interceptor.
        When both interceptors are used, this `post_tag_api_spec_revision_with_metadata` interceptor runs after the
        `post_tag_api_spec_revision` interceptor. The (possibly modified) response returned by
        `post_tag_api_spec_revision` will be passed to
        `post_tag_api_spec_revision_with_metadata`.
        """
        return response, metadata

    def pre_update_api(
        self,
        request: registry_service.UpdateApiRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.UpdateApiRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_api

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_update_api(self, response: registry_models.Api) -> registry_models.Api:
        """Post-rpc interceptor for update_api

        DEPRECATED. Please use the `post_update_api_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_update_api` interceptor runs
        before the `post_update_api_with_metadata` interceptor.
        """
        return response

    def post_update_api_with_metadata(
        self,
        response: registry_models.Api,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.Api, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_api

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_update_api_with_metadata`
        interceptor in new development instead of the `post_update_api` interceptor.
        When both interceptors are used, this `post_update_api_with_metadata` interceptor runs after the
        `post_update_api` interceptor. The (possibly modified) response returned by
        `post_update_api` will be passed to
        `post_update_api_with_metadata`.
        """
        return response, metadata

    def pre_update_api_deployment(
        self,
        request: registry_service.UpdateApiDeploymentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.UpdateApiDeploymentRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_api_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_update_api_deployment(
        self, response: registry_models.ApiDeployment
    ) -> registry_models.ApiDeployment:
        """Post-rpc interceptor for update_api_deployment

        DEPRECATED. Please use the `post_update_api_deployment_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_update_api_deployment` interceptor runs
        before the `post_update_api_deployment_with_metadata` interceptor.
        """
        return response

    def post_update_api_deployment_with_metadata(
        self,
        response: registry_models.ApiDeployment,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiDeployment, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_api_deployment

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_update_api_deployment_with_metadata`
        interceptor in new development instead of the `post_update_api_deployment` interceptor.
        When both interceptors are used, this `post_update_api_deployment_with_metadata` interceptor runs after the
        `post_update_api_deployment` interceptor. The (possibly modified) response returned by
        `post_update_api_deployment` will be passed to
        `post_update_api_deployment_with_metadata`.
        """
        return response, metadata

    def pre_update_api_spec(
        self,
        request: registry_service.UpdateApiSpecRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.UpdateApiSpecRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_api_spec

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_update_api_spec(
        self, response: registry_models.ApiSpec
    ) -> registry_models.ApiSpec:
        """Post-rpc interceptor for update_api_spec

        DEPRECATED. Please use the `post_update_api_spec_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_update_api_spec` interceptor runs
        before the `post_update_api_spec_with_metadata` interceptor.
        """
        return response

    def post_update_api_spec_with_metadata(
        self,
        response: registry_models.ApiSpec,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiSpec, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_api_spec

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_update_api_spec_with_metadata`
        interceptor in new development instead of the `post_update_api_spec` interceptor.
        When both interceptors are used, this `post_update_api_spec_with_metadata` interceptor runs after the
        `post_update_api_spec` interceptor. The (possibly modified) response returned by
        `post_update_api_spec` will be passed to
        `post_update_api_spec_with_metadata`.
        """
        return response, metadata

    def pre_update_api_version(
        self,
        request: registry_service.UpdateApiVersionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        registry_service.UpdateApiVersionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_api_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Registry server.
        """
        return request, metadata

    def post_update_api_version(
        self, response: registry_models.ApiVersion
    ) -> registry_models.ApiVersion:
        """Post-rpc interceptor for update_api_version

        DEPRECATED. Please use the `post_update_api_version_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the Registry server but before
        it is returned to user code. This `post_update_api_version` interceptor runs
        before the `post_update_api_version_with_metadata` interceptor.
        """
        return response

    def post_update_api_version_with_metadata(
        self,
        response: registry_models.ApiVersion,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[registry_models.ApiVersion, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_api_version

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the Registry server but before it is returned to user code.

        We recommend only using this `post_update_api_version_with_metadata`
        interceptor in new development instead of the `post_update_api_version` interceptor.
        When both interceptors are used, this `post_update_api_version_with_metadata` interceptor runs after the
        `post_update_api_version` interceptor. The (possibly modified) response returned by
        `post_update_api_version` will be passed to
        `post_update_api_version_with_metadata`.
        """
        return response, metadata

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        iam_policy_pb2.TestIamPermissionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
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


class RegistryRestTransport(_BaseRegistryRestTransport):
    """REST backend synchronous transport for Registry.

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

            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided. This argument will be
                removed in the next major version of this library.
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
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or RegistryRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateApi(_BaseRegistryRestTransport._BaseCreateApi, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.CreateApi")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.CreateApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.Api:
            r"""Call the create api method over HTTP.

            Args:
                request (~.registry_service.CreateApiRequest):
                    The request object. Request message for CreateApi.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_models.Api:
                    A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

            """

            http_options = _BaseRegistryRestTransport._BaseCreateApi._get_http_options()

            request, metadata = self._interceptor.pre_create_api(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseCreateApi._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegistryRestTransport._BaseCreateApi._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseCreateApi._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.CreateApi",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateApi",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._CreateApi._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_api_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.Api.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.create_api",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateApi",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateApiDeployment(
        _BaseRegistryRestTransport._BaseCreateApiDeployment, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.CreateApiDeployment")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.CreateApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the create api deployment method over HTTP.

            Args:
                request (~.registry_service.CreateApiDeploymentRequest):
                    The request object. Request message for
                CreateApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseCreateApiDeployment._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_api_deployment(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseCreateApiDeployment._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistryRestTransport._BaseCreateApiDeployment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseCreateApiDeployment._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.CreateApiDeployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateApiDeployment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._CreateApiDeployment._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_api_deployment_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiDeployment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.create_api_deployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateApiDeployment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateApiSpec(
        _BaseRegistryRestTransport._BaseCreateApiSpec, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.CreateApiSpec")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.CreateApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the create api spec method over HTTP.

            Args:
                request (~.registry_service.CreateApiSpecRequest):
                    The request object. Request message for CreateApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseCreateApiSpec._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_api_spec(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseCreateApiSpec._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegistryRestTransport._BaseCreateApiSpec._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseCreateApiSpec._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.CreateApiSpec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateApiSpec",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._CreateApiSpec._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_api_spec_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiSpec.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.create_api_spec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateApiSpec",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateApiVersion(
        _BaseRegistryRestTransport._BaseCreateApiVersion, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.CreateApiVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.CreateApiVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiVersion:
            r"""Call the create api version method over HTTP.

            Args:
                request (~.registry_service.CreateApiVersionRequest):
                    The request object. Request message for CreateApiVersion.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_models.ApiVersion:
                    Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

            """

            http_options = (
                _BaseRegistryRestTransport._BaseCreateApiVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_api_version(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseCreateApiVersion._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseRegistryRestTransport._BaseCreateApiVersion._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseCreateApiVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.CreateApiVersion",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateApiVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._CreateApiVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_api_version_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiVersion.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.create_api_version",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateApiVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateArtifact(
        _BaseRegistryRestTransport._BaseCreateArtifact, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.CreateArtifact")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.CreateArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.Artifact:
            r"""Call the create artifact method over HTTP.

            Args:
                request (~.registry_service.CreateArtifactRequest):
                    The request object. Request message for CreateArtifact.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseCreateArtifact._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_artifact(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseCreateArtifact._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseRegistryRestTransport._BaseCreateArtifact._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseCreateArtifact._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.CreateArtifact",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateArtifact",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._CreateArtifact._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_artifact_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.Artifact.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.create_artifact",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CreateArtifact",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteApi(_BaseRegistryRestTransport._BaseDeleteApi, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.DeleteApi")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.DeleteApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete api method over HTTP.

            Args:
                request (~.registry_service.DeleteApiRequest):
                    The request object. Request message for DeleteApi.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = _BaseRegistryRestTransport._BaseDeleteApi._get_http_options()

            request, metadata = self._interceptor.pre_delete_api(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseDeleteApi._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseDeleteApi._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.DeleteApi",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteApi",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._DeleteApi._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteApiDeployment(
        _BaseRegistryRestTransport._BaseDeleteApiDeployment, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.DeleteApiDeployment")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.DeleteApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete api deployment method over HTTP.

            Args:
                request (~.registry_service.DeleteApiDeploymentRequest):
                    The request object. Request message for
                DeleteApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseDeleteApiDeployment._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_api_deployment(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseDeleteApiDeployment._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseDeleteApiDeployment._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.DeleteApiDeployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteApiDeployment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._DeleteApiDeployment._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteApiDeploymentRevision(
        _BaseRegistryRestTransport._BaseDeleteApiDeploymentRevision, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.DeleteApiDeploymentRevision")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.DeleteApiDeploymentRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseDeleteApiDeploymentRevision._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_api_deployment_revision(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseDeleteApiDeploymentRevision._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseDeleteApiDeploymentRevision._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.DeleteApiDeploymentRevision",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteApiDeploymentRevision",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._DeleteApiDeploymentRevision._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_delete_api_deployment_revision_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiDeployment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.delete_api_deployment_revision",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteApiDeploymentRevision",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteApiSpec(
        _BaseRegistryRestTransport._BaseDeleteApiSpec, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.DeleteApiSpec")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.DeleteApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete api spec method over HTTP.

            Args:
                request (~.registry_service.DeleteApiSpecRequest):
                    The request object. Request message for DeleteApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseDeleteApiSpec._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_api_spec(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseDeleteApiSpec._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseDeleteApiSpec._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.DeleteApiSpec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteApiSpec",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._DeleteApiSpec._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteApiSpecRevision(
        _BaseRegistryRestTransport._BaseDeleteApiSpecRevision, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.DeleteApiSpecRevision")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.DeleteApiSpecRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the delete api spec revision method over HTTP.

            Args:
                request (~.registry_service.DeleteApiSpecRevisionRequest):
                    The request object. Request message for
                DeleteApiSpecRevision.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseDeleteApiSpecRevision._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_api_spec_revision(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseDeleteApiSpecRevision._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseDeleteApiSpecRevision._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.DeleteApiSpecRevision",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteApiSpecRevision",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._DeleteApiSpecRevision._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_api_spec_revision_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiSpec.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.delete_api_spec_revision",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteApiSpecRevision",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteApiVersion(
        _BaseRegistryRestTransport._BaseDeleteApiVersion, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.DeleteApiVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.DeleteApiVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete api version method over HTTP.

            Args:
                request (~.registry_service.DeleteApiVersionRequest):
                    The request object. Request message for DeleteApiVersion.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseDeleteApiVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_api_version(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseDeleteApiVersion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseDeleteApiVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.DeleteApiVersion",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteApiVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._DeleteApiVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteArtifact(
        _BaseRegistryRestTransport._BaseDeleteArtifact, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.DeleteArtifact")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.DeleteArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete artifact method over HTTP.

            Args:
                request (~.registry_service.DeleteArtifactRequest):
                    The request object. Request message for DeleteArtifact.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseDeleteArtifact._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_artifact(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseDeleteArtifact._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseDeleteArtifact._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.DeleteArtifact",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteArtifact",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._DeleteArtifact._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetApi(_BaseRegistryRestTransport._BaseGetApi, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.GetApi")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.GetApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.Api:
            r"""Call the get api method over HTTP.

            Args:
                request (~.registry_service.GetApiRequest):
                    The request object. Request message for GetApi.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_models.Api:
                    A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

            """

            http_options = _BaseRegistryRestTransport._BaseGetApi._get_http_options()

            request, metadata = self._interceptor.pre_get_api(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseGetApi._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseGetApi._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetApi",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApi",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetApi._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_api_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.Api.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.get_api",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApi",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetApiDeployment(
        _BaseRegistryRestTransport._BaseGetApiDeployment, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.GetApiDeployment")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.GetApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the get api deployment method over HTTP.

            Args:
                request (~.registry_service.GetApiDeploymentRequest):
                    The request object. Request message for GetApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseGetApiDeployment._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_api_deployment(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseGetApiDeployment._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseGetApiDeployment._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetApiDeployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApiDeployment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetApiDeployment._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_api_deployment_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiDeployment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.get_api_deployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApiDeployment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetApiSpec(_BaseRegistryRestTransport._BaseGetApiSpec, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.GetApiSpec")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.GetApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the get api spec method over HTTP.

            Args:
                request (~.registry_service.GetApiSpecRequest):
                    The request object. Request message for GetApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseGetApiSpec._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_api_spec(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseGetApiSpec._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseGetApiSpec._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetApiSpec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApiSpec",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetApiSpec._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_api_spec_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiSpec.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.get_api_spec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApiSpec",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetApiSpecContents(
        _BaseRegistryRestTransport._BaseGetApiSpecContents, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.GetApiSpecContents")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.GetApiSpecContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> httpbody_pb2.HttpBody:
            r"""Call the get api spec contents method over HTTP.

            Args:
                request (~.registry_service.GetApiSpecContentsRequest):
                    The request object. Request message for
                GetApiSpecContents.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseGetApiSpecContents._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_api_spec_contents(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseGetApiSpecContents._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseGetApiSpecContents._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetApiSpecContents",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApiSpecContents",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetApiSpecContents._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_api_spec_contents_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.get_api_spec_contents",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApiSpecContents",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetApiVersion(
        _BaseRegistryRestTransport._BaseGetApiVersion, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.GetApiVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.GetApiVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiVersion:
            r"""Call the get api version method over HTTP.

            Args:
                request (~.registry_service.GetApiVersionRequest):
                    The request object. Request message for GetApiVersion.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_models.ApiVersion:
                    Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

            """

            http_options = (
                _BaseRegistryRestTransport._BaseGetApiVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_api_version(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseGetApiVersion._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseGetApiVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetApiVersion",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApiVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetApiVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_api_version_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiVersion.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.get_api_version",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetApiVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetArtifact(_BaseRegistryRestTransport._BaseGetArtifact, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.GetArtifact")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.GetArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.Artifact:
            r"""Call the get artifact method over HTTP.

            Args:
                request (~.registry_service.GetArtifactRequest):
                    The request object. Request message for GetArtifact.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseGetArtifact._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_artifact(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseGetArtifact._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseGetArtifact._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetArtifact",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetArtifact",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetArtifact._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_artifact_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.Artifact.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.get_artifact",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetArtifact",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetArtifactContents(
        _BaseRegistryRestTransport._BaseGetArtifactContents, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.GetArtifactContents")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.GetArtifactContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> httpbody_pb2.HttpBody:
            r"""Call the get artifact contents method over HTTP.

            Args:
                request (~.registry_service.GetArtifactContentsRequest):
                    The request object. Request message for
                GetArtifactContents.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseGetArtifactContents._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_artifact_contents(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseGetArtifactContents._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseGetArtifactContents._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetArtifactContents",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetArtifactContents",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetArtifactContents._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_artifact_contents_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.get_artifact_contents",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetArtifactContents",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListApiDeploymentRevisions(
        _BaseRegistryRestTransport._BaseListApiDeploymentRevisions, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.ListApiDeploymentRevisions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.ListApiDeploymentRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.registry_service.ListApiDeploymentRevisionsResponse:
                        Response message for
                    ListApiDeploymentRevisionsResponse.

            """

            http_options = (
                _BaseRegistryRestTransport._BaseListApiDeploymentRevisions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_api_deployment_revisions(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseListApiDeploymentRevisions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseListApiDeploymentRevisions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListApiDeploymentRevisions",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiDeploymentRevisions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListApiDeploymentRevisions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_list_api_deployment_revisions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        registry_service.ListApiDeploymentRevisionsResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.list_api_deployment_revisions",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiDeploymentRevisions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListApiDeployments(
        _BaseRegistryRestTransport._BaseListApiDeployments, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.ListApiDeployments")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.ListApiDeploymentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_service.ListApiDeploymentsResponse:
            r"""Call the list api deployments method over HTTP.

            Args:
                request (~.registry_service.ListApiDeploymentsRequest):
                    The request object. Request message for
                ListApiDeployments.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_service.ListApiDeploymentsResponse:
                    Response message for
                ListApiDeployments.

            """

            http_options = (
                _BaseRegistryRestTransport._BaseListApiDeployments._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_api_deployments(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseListApiDeployments._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseListApiDeployments._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListApiDeployments",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiDeployments",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListApiDeployments._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_api_deployments_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        registry_service.ListApiDeploymentsResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.list_api_deployments",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiDeployments",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListApis(_BaseRegistryRestTransport._BaseListApis, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.ListApis")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.ListApisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_service.ListApisResponse:
            r"""Call the list apis method over HTTP.

            Args:
                request (~.registry_service.ListApisRequest):
                    The request object. Request message for ListApis.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_service.ListApisResponse:
                    Response message for ListApis.
            """

            http_options = _BaseRegistryRestTransport._BaseListApis._get_http_options()

            request, metadata = self._interceptor.pre_list_apis(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseListApis._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseListApis._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListApis",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApis",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListApis._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_apis_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_service.ListApisResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.list_apis",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApis",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListApiSpecRevisions(
        _BaseRegistryRestTransport._BaseListApiSpecRevisions, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.ListApiSpecRevisions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.ListApiSpecRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_service.ListApiSpecRevisionsResponse:
            r"""Call the list api spec revisions method over HTTP.

            Args:
                request (~.registry_service.ListApiSpecRevisionsRequest):
                    The request object. Request message for
                ListApiSpecRevisions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_service.ListApiSpecRevisionsResponse:
                    Response message for
                ListApiSpecRevisionsResponse.

            """

            http_options = (
                _BaseRegistryRestTransport._BaseListApiSpecRevisions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_api_spec_revisions(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseListApiSpecRevisions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseListApiSpecRevisions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListApiSpecRevisions",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiSpecRevisions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListApiSpecRevisions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_api_spec_revisions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        registry_service.ListApiSpecRevisionsResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.list_api_spec_revisions",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiSpecRevisions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListApiSpecs(_BaseRegistryRestTransport._BaseListApiSpecs, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.ListApiSpecs")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.ListApiSpecsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_service.ListApiSpecsResponse:
            r"""Call the list api specs method over HTTP.

            Args:
                request (~.registry_service.ListApiSpecsRequest):
                    The request object. Request message for ListApiSpecs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_service.ListApiSpecsResponse:
                    Response message for ListApiSpecs.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseListApiSpecs._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_api_specs(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseListApiSpecs._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseListApiSpecs._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListApiSpecs",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiSpecs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListApiSpecs._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_api_specs_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_service.ListApiSpecsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.list_api_specs",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiSpecs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListApiVersions(
        _BaseRegistryRestTransport._BaseListApiVersions, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.ListApiVersions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.ListApiVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_service.ListApiVersionsResponse:
            r"""Call the list api versions method over HTTP.

            Args:
                request (~.registry_service.ListApiVersionsRequest):
                    The request object. Request message for ListApiVersions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_service.ListApiVersionsResponse:
                    Response message for ListApiVersions.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseListApiVersions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_api_versions(
                request, metadata
            )
            transcoded_request = (
                _BaseRegistryRestTransport._BaseListApiVersions._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseListApiVersions._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListApiVersions",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiVersions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListApiVersions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_api_versions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_service.ListApiVersionsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.list_api_versions",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListApiVersions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListArtifacts(
        _BaseRegistryRestTransport._BaseListArtifacts, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.ListArtifacts")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: registry_service.ListArtifactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_service.ListArtifactsResponse:
            r"""Call the list artifacts method over HTTP.

            Args:
                request (~.registry_service.ListArtifactsRequest):
                    The request object. Request message for ListArtifacts.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_service.ListArtifactsResponse:
                    Response message for ListArtifacts.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseListArtifacts._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_artifacts(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseListArtifacts._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseListArtifacts._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListArtifacts",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListArtifacts",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListArtifacts._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_artifacts_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_service.ListArtifactsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.list_artifacts",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListArtifacts",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ReplaceArtifact(
        _BaseRegistryRestTransport._BaseReplaceArtifact, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.ReplaceArtifact")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.ReplaceArtifactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.Artifact:
            r"""Call the replace artifact method over HTTP.

            Args:
                request (~.registry_service.ReplaceArtifactRequest):
                    The request object. Request message for ReplaceArtifact.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseReplaceArtifact._get_http_options()
            )

            request, metadata = self._interceptor.pre_replace_artifact(
                request, metadata
            )
            transcoded_request = (
                _BaseRegistryRestTransport._BaseReplaceArtifact._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseRegistryRestTransport._BaseReplaceArtifact._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseReplaceArtifact._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ReplaceArtifact",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ReplaceArtifact",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ReplaceArtifact._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_replace_artifact_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.Artifact.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.replace_artifact",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ReplaceArtifact",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RollbackApiDeployment(
        _BaseRegistryRestTransport._BaseRollbackApiDeployment, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.RollbackApiDeployment")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.RollbackApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the rollback api deployment method over HTTP.

            Args:
                request (~.registry_service.RollbackApiDeploymentRequest):
                    The request object. Request message for
                RollbackApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseRollbackApiDeployment._get_http_options()
            )

            request, metadata = self._interceptor.pre_rollback_api_deployment(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseRollbackApiDeployment._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistryRestTransport._BaseRollbackApiDeployment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseRollbackApiDeployment._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.RollbackApiDeployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "RollbackApiDeployment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._RollbackApiDeployment._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_rollback_api_deployment_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiDeployment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.rollback_api_deployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "RollbackApiDeployment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RollbackApiSpec(
        _BaseRegistryRestTransport._BaseRollbackApiSpec, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.RollbackApiSpec")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.RollbackApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the rollback api spec method over HTTP.

            Args:
                request (~.registry_service.RollbackApiSpecRequest):
                    The request object. Request message for RollbackApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseRollbackApiSpec._get_http_options()
            )

            request, metadata = self._interceptor.pre_rollback_api_spec(
                request, metadata
            )
            transcoded_request = (
                _BaseRegistryRestTransport._BaseRollbackApiSpec._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseRegistryRestTransport._BaseRollbackApiSpec._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseRollbackApiSpec._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.RollbackApiSpec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "RollbackApiSpec",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._RollbackApiSpec._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_rollback_api_spec_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiSpec.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.rollback_api_spec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "RollbackApiSpec",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _TagApiDeploymentRevision(
        _BaseRegistryRestTransport._BaseTagApiDeploymentRevision, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.TagApiDeploymentRevision")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.TagApiDeploymentRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseTagApiDeploymentRevision._get_http_options()
            )

            request, metadata = self._interceptor.pre_tag_api_deployment_revision(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseTagApiDeploymentRevision._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistryRestTransport._BaseTagApiDeploymentRevision._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseTagApiDeploymentRevision._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.TagApiDeploymentRevision",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "TagApiDeploymentRevision",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._TagApiDeploymentRevision._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_tag_api_deployment_revision_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiDeployment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.tag_api_deployment_revision",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "TagApiDeploymentRevision",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _TagApiSpecRevision(
        _BaseRegistryRestTransport._BaseTagApiSpecRevision, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.TagApiSpecRevision")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.TagApiSpecRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the tag api spec revision method over HTTP.

            Args:
                request (~.registry_service.TagApiSpecRevisionRequest):
                    The request object. Request message for
                TagApiSpecRevision.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseTagApiSpecRevision._get_http_options()
            )

            request, metadata = self._interceptor.pre_tag_api_spec_revision(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseTagApiSpecRevision._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistryRestTransport._BaseTagApiSpecRevision._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseTagApiSpecRevision._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.TagApiSpecRevision",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "TagApiSpecRevision",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._TagApiSpecRevision._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_tag_api_spec_revision_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiSpec.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.tag_api_spec_revision",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "TagApiSpecRevision",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateApi(_BaseRegistryRestTransport._BaseUpdateApi, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.UpdateApi")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.UpdateApiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.Api:
            r"""Call the update api method over HTTP.

            Args:
                request (~.registry_service.UpdateApiRequest):
                    The request object. Request message for UpdateApi.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_models.Api:
                    A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

            """

            http_options = _BaseRegistryRestTransport._BaseUpdateApi._get_http_options()

            request, metadata = self._interceptor.pre_update_api(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseUpdateApi._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegistryRestTransport._BaseUpdateApi._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseUpdateApi._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.UpdateApi",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "UpdateApi",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._UpdateApi._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_api_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.Api.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.update_api",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "UpdateApi",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateApiDeployment(
        _BaseRegistryRestTransport._BaseUpdateApiDeployment, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.UpdateApiDeployment")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.UpdateApiDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiDeployment:
            r"""Call the update api deployment method over HTTP.

            Args:
                request (~.registry_service.UpdateApiDeploymentRequest):
                    The request object. Request message for
                UpdateApiDeployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseUpdateApiDeployment._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_api_deployment(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseUpdateApiDeployment._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistryRestTransport._BaseUpdateApiDeployment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseUpdateApiDeployment._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.UpdateApiDeployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "UpdateApiDeployment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._UpdateApiDeployment._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_api_deployment_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiDeployment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.update_api_deployment",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "UpdateApiDeployment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateApiSpec(
        _BaseRegistryRestTransport._BaseUpdateApiSpec, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.UpdateApiSpec")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.UpdateApiSpecRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiSpec:
            r"""Call the update api spec method over HTTP.

            Args:
                request (~.registry_service.UpdateApiSpecRequest):
                    The request object. Request message for UpdateApiSpec.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

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

            http_options = (
                _BaseRegistryRestTransport._BaseUpdateApiSpec._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_api_spec(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseUpdateApiSpec._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegistryRestTransport._BaseUpdateApiSpec._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseUpdateApiSpec._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.UpdateApiSpec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "UpdateApiSpec",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._UpdateApiSpec._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_api_spec_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiSpec.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.update_api_spec",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "UpdateApiSpec",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateApiVersion(
        _BaseRegistryRestTransport._BaseUpdateApiVersion, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.UpdateApiVersion")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: registry_service.UpdateApiVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> registry_models.ApiVersion:
            r"""Call the update api version method over HTTP.

            Args:
                request (~.registry_service.UpdateApiVersionRequest):
                    The request object. Request message for UpdateApiVersion.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.registry_models.ApiVersion:
                    Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

            """

            http_options = (
                _BaseRegistryRestTransport._BaseUpdateApiVersion._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_api_version(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseUpdateApiVersion._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseRegistryRestTransport._BaseUpdateApiVersion._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseUpdateApiVersion._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.UpdateApiVersion",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "UpdateApiVersion",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._UpdateApiVersion._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_api_version_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = registry_models.ApiVersion.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryClient.update_api_version",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "UpdateApiVersion",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
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

    class _GetLocation(_BaseRegistryRestTransport._BaseGetLocation, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.GetLocation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetLocation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseRegistryRestTransport._BaseListLocations, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListLocations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(_BaseRegistryRestTransport._BaseGetIamPolicy, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.GetIamPolicy")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseGetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseGetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseGetIamPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetIamPolicy._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryAsyncClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetIamPolicy",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(_BaseRegistryRestTransport._BaseSetIamPolicy, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.SetIamPolicy")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseSetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseSetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseRegistryRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseSetIamPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "SetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._SetIamPolicy._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryAsyncClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "SetIamPolicy",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(
        _BaseRegistryRestTransport._BaseTestIamPermissions, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.TestIamPermissions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseTestIamPermissions._get_http_options()
            )

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseRegistryRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseRegistryRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseRegistryRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "TestIamPermissions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._TestIamPermissions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryAsyncClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "TestIamPermissions",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseRegistryRestTransport._BaseCancelOperation, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.CancelOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseRegistryRestTransport._BaseCancelOperation._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseRegistryRestTransport._BaseCancelOperation._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._CancelOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseRegistryRestTransport._BaseDeleteOperation, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.DeleteOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseDeleteOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseRegistryRestTransport._BaseDeleteOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseDeleteOperation._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._DeleteOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(_BaseRegistryRestTransport._BaseGetOperation, RegistryRestStub):
        def __hash__(self):
            return hash("RegistryRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._GetOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseRegistryRestTransport._BaseListOperations, RegistryRestStub
    ):
        def __hash__(self):
            return hash("RegistryRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseRegistryRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseRegistryRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRegistryRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.apigeeregistry_v1.RegistryClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = RegistryRestTransport._ListOperations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.apigeeregistry_v1.RegistryAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                        "rpcName": "ListOperations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RegistryRestTransport",)
