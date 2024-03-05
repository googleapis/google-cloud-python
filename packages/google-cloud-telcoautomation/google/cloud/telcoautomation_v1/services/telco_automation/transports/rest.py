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
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.telcoautomation_v1.types import telcoautomation

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import TelcoAutomationTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class TelcoAutomationRestInterceptor:
    """Interceptor for TelcoAutomation.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the TelcoAutomationRestTransport.

    .. code-block:: python
        class MyCustomTelcoAutomationInterceptor(TelcoAutomationRestInterceptor):
            def pre_apply_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_apply_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_apply_hydrated_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_apply_hydrated_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_approve_blueprint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_approve_blueprint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_compute_deployment_status(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_compute_deployment_status(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_blueprint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_blueprint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_edge_slm(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_edge_slm(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_orchestration_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_orchestration_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_blueprint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_edge_slm(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_edge_slm(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_orchestration_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_orchestration_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_discard_blueprint_changes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_discard_blueprint_changes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_discard_deployment_changes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_discard_deployment_changes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_blueprint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_blueprint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_edge_slm(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_edge_slm(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_hydrated_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_hydrated_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_orchestration_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_orchestration_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_public_blueprint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_public_blueprint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_blueprint_revisions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_blueprint_revisions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_blueprints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_blueprints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_deployment_revisions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_deployment_revisions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_deployments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_deployments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_edge_slms(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_edge_slms(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_hydrated_deployments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_hydrated_deployments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_orchestration_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_orchestration_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_public_blueprints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_public_blueprints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_propose_blueprint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_propose_blueprint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reject_blueprint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reject_blueprint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_rollback_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rollback_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_blueprint_revisions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_blueprint_revisions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_deployment_revisions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_deployment_revisions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_blueprint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_blueprint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_hydrated_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_hydrated_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = TelcoAutomationRestTransport(interceptor=MyCustomTelcoAutomationInterceptor())
        client = TelcoAutomationClient(transport=transport)


    """

    def pre_apply_deployment(
        self,
        request: telcoautomation.ApplyDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.ApplyDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for apply_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_apply_deployment(
        self, response: telcoautomation.Deployment
    ) -> telcoautomation.Deployment:
        """Post-rpc interceptor for apply_deployment

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_apply_hydrated_deployment(
        self,
        request: telcoautomation.ApplyHydratedDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.ApplyHydratedDeploymentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for apply_hydrated_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_apply_hydrated_deployment(
        self, response: telcoautomation.HydratedDeployment
    ) -> telcoautomation.HydratedDeployment:
        """Post-rpc interceptor for apply_hydrated_deployment

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_approve_blueprint(
        self,
        request: telcoautomation.ApproveBlueprintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.ApproveBlueprintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for approve_blueprint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_approve_blueprint(
        self, response: telcoautomation.Blueprint
    ) -> telcoautomation.Blueprint:
        """Post-rpc interceptor for approve_blueprint

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_compute_deployment_status(
        self,
        request: telcoautomation.ComputeDeploymentStatusRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.ComputeDeploymentStatusRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for compute_deployment_status

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_compute_deployment_status(
        self, response: telcoautomation.ComputeDeploymentStatusResponse
    ) -> telcoautomation.ComputeDeploymentStatusResponse:
        """Post-rpc interceptor for compute_deployment_status

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_create_blueprint(
        self,
        request: telcoautomation.CreateBlueprintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.CreateBlueprintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_blueprint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_create_blueprint(
        self, response: telcoautomation.Blueprint
    ) -> telcoautomation.Blueprint:
        """Post-rpc interceptor for create_blueprint

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_create_deployment(
        self,
        request: telcoautomation.CreateDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.CreateDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_create_deployment(
        self, response: telcoautomation.Deployment
    ) -> telcoautomation.Deployment:
        """Post-rpc interceptor for create_deployment

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_create_edge_slm(
        self,
        request: telcoautomation.CreateEdgeSlmRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.CreateEdgeSlmRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_edge_slm

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_create_edge_slm(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_edge_slm

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_create_orchestration_cluster(
        self,
        request: telcoautomation.CreateOrchestrationClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.CreateOrchestrationClusterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_orchestration_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_create_orchestration_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_orchestration_cluster

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_delete_blueprint(
        self,
        request: telcoautomation.DeleteBlueprintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.DeleteBlueprintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_blueprint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def pre_delete_edge_slm(
        self,
        request: telcoautomation.DeleteEdgeSlmRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.DeleteEdgeSlmRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_edge_slm

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_delete_edge_slm(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_edge_slm

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_delete_orchestration_cluster(
        self,
        request: telcoautomation.DeleteOrchestrationClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.DeleteOrchestrationClusterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_orchestration_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_delete_orchestration_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_orchestration_cluster

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_discard_blueprint_changes(
        self,
        request: telcoautomation.DiscardBlueprintChangesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.DiscardBlueprintChangesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for discard_blueprint_changes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_discard_blueprint_changes(
        self, response: telcoautomation.DiscardBlueprintChangesResponse
    ) -> telcoautomation.DiscardBlueprintChangesResponse:
        """Post-rpc interceptor for discard_blueprint_changes

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_discard_deployment_changes(
        self,
        request: telcoautomation.DiscardDeploymentChangesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.DiscardDeploymentChangesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for discard_deployment_changes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_discard_deployment_changes(
        self, response: telcoautomation.DiscardDeploymentChangesResponse
    ) -> telcoautomation.DiscardDeploymentChangesResponse:
        """Post-rpc interceptor for discard_deployment_changes

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_get_blueprint(
        self,
        request: telcoautomation.GetBlueprintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.GetBlueprintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_blueprint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_get_blueprint(
        self, response: telcoautomation.Blueprint
    ) -> telcoautomation.Blueprint:
        """Post-rpc interceptor for get_blueprint

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_get_deployment(
        self,
        request: telcoautomation.GetDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.GetDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_get_deployment(
        self, response: telcoautomation.Deployment
    ) -> telcoautomation.Deployment:
        """Post-rpc interceptor for get_deployment

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_get_edge_slm(
        self,
        request: telcoautomation.GetEdgeSlmRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.GetEdgeSlmRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_edge_slm

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_get_edge_slm(
        self, response: telcoautomation.EdgeSlm
    ) -> telcoautomation.EdgeSlm:
        """Post-rpc interceptor for get_edge_slm

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_get_hydrated_deployment(
        self,
        request: telcoautomation.GetHydratedDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.GetHydratedDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_hydrated_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_get_hydrated_deployment(
        self, response: telcoautomation.HydratedDeployment
    ) -> telcoautomation.HydratedDeployment:
        """Post-rpc interceptor for get_hydrated_deployment

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_get_orchestration_cluster(
        self,
        request: telcoautomation.GetOrchestrationClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.GetOrchestrationClusterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_orchestration_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_get_orchestration_cluster(
        self, response: telcoautomation.OrchestrationCluster
    ) -> telcoautomation.OrchestrationCluster:
        """Post-rpc interceptor for get_orchestration_cluster

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_get_public_blueprint(
        self,
        request: telcoautomation.GetPublicBlueprintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.GetPublicBlueprintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_public_blueprint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_get_public_blueprint(
        self, response: telcoautomation.PublicBlueprint
    ) -> telcoautomation.PublicBlueprint:
        """Post-rpc interceptor for get_public_blueprint

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_list_blueprint_revisions(
        self,
        request: telcoautomation.ListBlueprintRevisionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.ListBlueprintRevisionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_blueprint_revisions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_blueprint_revisions(
        self, response: telcoautomation.ListBlueprintRevisionsResponse
    ) -> telcoautomation.ListBlueprintRevisionsResponse:
        """Post-rpc interceptor for list_blueprint_revisions

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_list_blueprints(
        self,
        request: telcoautomation.ListBlueprintsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.ListBlueprintsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_blueprints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_blueprints(
        self, response: telcoautomation.ListBlueprintsResponse
    ) -> telcoautomation.ListBlueprintsResponse:
        """Post-rpc interceptor for list_blueprints

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_list_deployment_revisions(
        self,
        request: telcoautomation.ListDeploymentRevisionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.ListDeploymentRevisionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_deployment_revisions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_deployment_revisions(
        self, response: telcoautomation.ListDeploymentRevisionsResponse
    ) -> telcoautomation.ListDeploymentRevisionsResponse:
        """Post-rpc interceptor for list_deployment_revisions

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_list_deployments(
        self,
        request: telcoautomation.ListDeploymentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.ListDeploymentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_deployments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_deployments(
        self, response: telcoautomation.ListDeploymentsResponse
    ) -> telcoautomation.ListDeploymentsResponse:
        """Post-rpc interceptor for list_deployments

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_list_edge_slms(
        self,
        request: telcoautomation.ListEdgeSlmsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.ListEdgeSlmsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_edge_slms

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_edge_slms(
        self, response: telcoautomation.ListEdgeSlmsResponse
    ) -> telcoautomation.ListEdgeSlmsResponse:
        """Post-rpc interceptor for list_edge_slms

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_list_hydrated_deployments(
        self,
        request: telcoautomation.ListHydratedDeploymentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.ListHydratedDeploymentsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_hydrated_deployments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_hydrated_deployments(
        self, response: telcoautomation.ListHydratedDeploymentsResponse
    ) -> telcoautomation.ListHydratedDeploymentsResponse:
        """Post-rpc interceptor for list_hydrated_deployments

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_list_orchestration_clusters(
        self,
        request: telcoautomation.ListOrchestrationClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.ListOrchestrationClustersRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_orchestration_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_orchestration_clusters(
        self, response: telcoautomation.ListOrchestrationClustersResponse
    ) -> telcoautomation.ListOrchestrationClustersResponse:
        """Post-rpc interceptor for list_orchestration_clusters

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_list_public_blueprints(
        self,
        request: telcoautomation.ListPublicBlueprintsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.ListPublicBlueprintsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_public_blueprints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_public_blueprints(
        self, response: telcoautomation.ListPublicBlueprintsResponse
    ) -> telcoautomation.ListPublicBlueprintsResponse:
        """Post-rpc interceptor for list_public_blueprints

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_propose_blueprint(
        self,
        request: telcoautomation.ProposeBlueprintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.ProposeBlueprintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for propose_blueprint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_propose_blueprint(
        self, response: telcoautomation.Blueprint
    ) -> telcoautomation.Blueprint:
        """Post-rpc interceptor for propose_blueprint

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_reject_blueprint(
        self,
        request: telcoautomation.RejectBlueprintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.RejectBlueprintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for reject_blueprint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_reject_blueprint(
        self, response: telcoautomation.Blueprint
    ) -> telcoautomation.Blueprint:
        """Post-rpc interceptor for reject_blueprint

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_remove_deployment(
        self,
        request: telcoautomation.RemoveDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.RemoveDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def pre_rollback_deployment(
        self,
        request: telcoautomation.RollbackDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.RollbackDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rollback_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_rollback_deployment(
        self, response: telcoautomation.Deployment
    ) -> telcoautomation.Deployment:
        """Post-rpc interceptor for rollback_deployment

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_search_blueprint_revisions(
        self,
        request: telcoautomation.SearchBlueprintRevisionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.SearchBlueprintRevisionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for search_blueprint_revisions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_search_blueprint_revisions(
        self, response: telcoautomation.SearchBlueprintRevisionsResponse
    ) -> telcoautomation.SearchBlueprintRevisionsResponse:
        """Post-rpc interceptor for search_blueprint_revisions

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_search_deployment_revisions(
        self,
        request: telcoautomation.SearchDeploymentRevisionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.SearchDeploymentRevisionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for search_deployment_revisions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_search_deployment_revisions(
        self, response: telcoautomation.SearchDeploymentRevisionsResponse
    ) -> telcoautomation.SearchDeploymentRevisionsResponse:
        """Post-rpc interceptor for search_deployment_revisions

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_update_blueprint(
        self,
        request: telcoautomation.UpdateBlueprintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.UpdateBlueprintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_blueprint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_update_blueprint(
        self, response: telcoautomation.Blueprint
    ) -> telcoautomation.Blueprint:
        """Post-rpc interceptor for update_blueprint

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_update_deployment(
        self,
        request: telcoautomation.UpdateDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[telcoautomation.UpdateDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_update_deployment(
        self, response: telcoautomation.Deployment
    ) -> telcoautomation.Deployment:
        """Post-rpc interceptor for update_deployment

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response

    def pre_update_hydrated_deployment(
        self,
        request: telcoautomation.UpdateHydratedDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        telcoautomation.UpdateHydratedDeploymentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_hydrated_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_update_hydrated_deployment(
        self, response: telcoautomation.HydratedDeployment
    ) -> telcoautomation.HydratedDeployment:
        """Post-rpc interceptor for update_hydrated_deployment

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
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
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
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
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
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
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
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
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
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
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
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
        before they are sent to the TelcoAutomation server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the TelcoAutomation server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class TelcoAutomationRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: TelcoAutomationRestInterceptor


class TelcoAutomationRestTransport(TelcoAutomationTransport):
    """REST backend transport for TelcoAutomation.

    TelcoAutomation Service manages the control plane cluster
    a.k.a. Orchestration Cluster (GKE cluster with config
    controller) of TNA. It also exposes blueprint APIs which manages
    the lifecycle of blueprints that control the infrastructure
    setup (e.g GDCE clusters) and deployment of network functions.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "telcoautomation.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[TelcoAutomationRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'telcoautomation.googleapis.com').
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
        self._interceptor = interceptor or TelcoAutomationRestInterceptor()
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
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations}",
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

    class _ApplyDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ApplyDeployment")

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
            request: telcoautomation.ApplyDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Deployment:
            r"""Call the apply deployment method over HTTP.

            Args:
                request (~.telcoautomation.ApplyDeploymentRequest):
                    The request object. Request object for ``ApplyDeployment``. The resources in
                given deployment gets applied to Orchestration Cluster.
                A new revision is created when a deployment is applied.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Deployment:
                    Deployment contains a collection of
                YAML files (This collection is also
                known as package) that can to applied on
                an orchestration cluster (GKE cluster
                with TNA addons) or a workload cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:apply",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_apply_deployment(
                request, metadata
            )
            pb_request = telcoautomation.ApplyDeploymentRequest.pb(request)
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
            resp = telcoautomation.Deployment()
            pb_resp = telcoautomation.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_apply_deployment(resp)
            return resp

    class _ApplyHydratedDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ApplyHydratedDeployment")

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
            request: telcoautomation.ApplyHydratedDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.HydratedDeployment:
            r"""Call the apply hydrated deployment method over HTTP.

            Args:
                request (~.telcoautomation.ApplyHydratedDeploymentRequest):
                    The request object. Request for applying a hydrated
                deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.HydratedDeployment:
                    A collection of kubernetes yaml files
                which are deployed on a Workload
                Cluster. Hydrated Deployments are
                created by TNA intent based automation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*/hydratedDeployments/*}:apply",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_apply_hydrated_deployment(
                request, metadata
            )
            pb_request = telcoautomation.ApplyHydratedDeploymentRequest.pb(request)
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
            resp = telcoautomation.HydratedDeployment()
            pb_resp = telcoautomation.HydratedDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_apply_hydrated_deployment(resp)
            return resp

    class _ApproveBlueprint(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ApproveBlueprint")

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
            request: telcoautomation.ApproveBlueprintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Blueprint:
            r"""Call the approve blueprint method over HTTP.

            Args:
                request (~.telcoautomation.ApproveBlueprintRequest):
                    The request object. Request object for ``ApproveBlueprint``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Blueprint:
                    A Blueprint contains a collection of
                kubernetes resources in the form of YAML
                files. The file contents of a blueprint
                are collectively known as package. A
                blueprint can be
                a) imported from TNA's public catalog
                b) modified as per a user's need
                c) proposed and approved.
                On approval, a revision of blueprint is
                created which can be used to create a
                deployment on Orchestration or Workload
                Cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:approve",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_approve_blueprint(
                request, metadata
            )
            pb_request = telcoautomation.ApproveBlueprintRequest.pb(request)
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
            resp = telcoautomation.Blueprint()
            pb_resp = telcoautomation.Blueprint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_approve_blueprint(resp)
            return resp

    class _ComputeDeploymentStatus(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ComputeDeploymentStatus")

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
            request: telcoautomation.ComputeDeploymentStatusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ComputeDeploymentStatusResponse:
            r"""Call the compute deployment status method over HTTP.

            Args:
                request (~.telcoautomation.ComputeDeploymentStatusRequest):
                    The request object. Request object for ``ComputeDeploymentStatus``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.ComputeDeploymentStatusResponse:
                    Response object for ``ComputeDeploymentStatus``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:computeDeploymentStatus",
                },
            ]
            request, metadata = self._interceptor.pre_compute_deployment_status(
                request, metadata
            )
            pb_request = telcoautomation.ComputeDeploymentStatusRequest.pb(request)
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
            resp = telcoautomation.ComputeDeploymentStatusResponse()
            pb_resp = telcoautomation.ComputeDeploymentStatusResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_compute_deployment_status(resp)
            return resp

    class _CreateBlueprint(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("CreateBlueprint")

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
            request: telcoautomation.CreateBlueprintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Blueprint:
            r"""Call the create blueprint method over HTTP.

            Args:
                request (~.telcoautomation.CreateBlueprintRequest):
                    The request object. Request object for ``CreateBlueprint``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Blueprint:
                    A Blueprint contains a collection of
                kubernetes resources in the form of YAML
                files. The file contents of a blueprint
                are collectively known as package. A
                blueprint can be
                a) imported from TNA's public catalog
                b) modified as per a user's need
                c) proposed and approved.
                On approval, a revision of blueprint is
                created which can be used to create a
                deployment on Orchestration or Workload
                Cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/blueprints",
                    "body": "blueprint",
                },
            ]
            request, metadata = self._interceptor.pre_create_blueprint(
                request, metadata
            )
            pb_request = telcoautomation.CreateBlueprintRequest.pb(request)
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
            resp = telcoautomation.Blueprint()
            pb_resp = telcoautomation.Blueprint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_blueprint(resp)
            return resp

    class _CreateDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("CreateDeployment")

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
            request: telcoautomation.CreateDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Deployment:
            r"""Call the create deployment method over HTTP.

            Args:
                request (~.telcoautomation.CreateDeploymentRequest):
                    The request object. Request object for ``CreateDeployment``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Deployment:
                    Deployment contains a collection of
                YAML files (This collection is also
                known as package) that can to applied on
                an orchestration cluster (GKE cluster
                with TNA addons) or a workload cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/deployments",
                    "body": "deployment",
                },
            ]
            request, metadata = self._interceptor.pre_create_deployment(
                request, metadata
            )
            pb_request = telcoautomation.CreateDeploymentRequest.pb(request)
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
            resp = telcoautomation.Deployment()
            pb_resp = telcoautomation.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_deployment(resp)
            return resp

    class _CreateEdgeSlm(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("CreateEdgeSlm")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "edgeSlmId": "",
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
            request: telcoautomation.CreateEdgeSlmRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create edge slm method over HTTP.

            Args:
                request (~.telcoautomation.CreateEdgeSlmRequest):
                    The request object. Message for creating a EdgeSlm.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/edgeSlms",
                    "body": "edge_slm",
                },
            ]
            request, metadata = self._interceptor.pre_create_edge_slm(request, metadata)
            pb_request = telcoautomation.CreateEdgeSlmRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_edge_slm(resp)
            return resp

    class _CreateOrchestrationCluster(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("CreateOrchestrationCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "orchestrationClusterId": "",
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
            request: telcoautomation.CreateOrchestrationClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create orchestration
            cluster method over HTTP.

                Args:
                    request (~.telcoautomation.CreateOrchestrationClusterRequest):
                        The request object. Message for creating a
                    OrchestrationCluster.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/orchestrationClusters",
                    "body": "orchestration_cluster",
                },
            ]
            request, metadata = self._interceptor.pre_create_orchestration_cluster(
                request, metadata
            )
            pb_request = telcoautomation.CreateOrchestrationClusterRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_orchestration_cluster(resp)
            return resp

    class _DeleteBlueprint(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("DeleteBlueprint")

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
            request: telcoautomation.DeleteBlueprintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete blueprint method over HTTP.

            Args:
                request (~.telcoautomation.DeleteBlueprintRequest):
                    The request object. Request object for ``DeleteBlueprint``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_blueprint(
                request, metadata
            )
            pb_request = telcoautomation.DeleteBlueprintRequest.pb(request)
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

    class _DeleteEdgeSlm(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("DeleteEdgeSlm")

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
            request: telcoautomation.DeleteEdgeSlmRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete edge slm method over HTTP.

            Args:
                request (~.telcoautomation.DeleteEdgeSlmRequest):
                    The request object. Message for deleting a EdgeSlm.
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
                    "uri": "/v1/{name=projects/*/locations/*/edgeSlms/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_edge_slm(request, metadata)
            pb_request = telcoautomation.DeleteEdgeSlmRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_edge_slm(resp)
            return resp

    class _DeleteOrchestrationCluster(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("DeleteOrchestrationCluster")

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
            request: telcoautomation.DeleteOrchestrationClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete orchestration
            cluster method over HTTP.

                Args:
                    request (~.telcoautomation.DeleteOrchestrationClusterRequest):
                        The request object. Message for deleting a
                    OrchestrationCluster.
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
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_orchestration_cluster(
                request, metadata
            )
            pb_request = telcoautomation.DeleteOrchestrationClusterRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_orchestration_cluster(resp)
            return resp

    class _DiscardBlueprintChanges(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("DiscardBlueprintChanges")

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
            request: telcoautomation.DiscardBlueprintChangesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.DiscardBlueprintChangesResponse:
            r"""Call the discard blueprint changes method over HTTP.

            Args:
                request (~.telcoautomation.DiscardBlueprintChangesRequest):
                    The request object. Request object for ``DiscardBlueprintChanges``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.DiscardBlueprintChangesResponse:
                    Response object for ``DiscardBlueprintChanges``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:discard",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_discard_blueprint_changes(
                request, metadata
            )
            pb_request = telcoautomation.DiscardBlueprintChangesRequest.pb(request)
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
            resp = telcoautomation.DiscardBlueprintChangesResponse()
            pb_resp = telcoautomation.DiscardBlueprintChangesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_discard_blueprint_changes(resp)
            return resp

    class _DiscardDeploymentChanges(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("DiscardDeploymentChanges")

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
            request: telcoautomation.DiscardDeploymentChangesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.DiscardDeploymentChangesResponse:
            r"""Call the discard deployment
            changes method over HTTP.

                Args:
                    request (~.telcoautomation.DiscardDeploymentChangesRequest):
                        The request object. Request object for ``DiscardDeploymentChanges``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.telcoautomation.DiscardDeploymentChangesResponse:
                        Response object for ``DiscardDeploymentChanges``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:discard",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_discard_deployment_changes(
                request, metadata
            )
            pb_request = telcoautomation.DiscardDeploymentChangesRequest.pb(request)
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
            resp = telcoautomation.DiscardDeploymentChangesResponse()
            pb_resp = telcoautomation.DiscardDeploymentChangesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_discard_deployment_changes(resp)
            return resp

    class _GetBlueprint(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("GetBlueprint")

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
            request: telcoautomation.GetBlueprintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Blueprint:
            r"""Call the get blueprint method over HTTP.

            Args:
                request (~.telcoautomation.GetBlueprintRequest):
                    The request object. Request object for ``GetBlueprint``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Blueprint:
                    A Blueprint contains a collection of
                kubernetes resources in the form of YAML
                files. The file contents of a blueprint
                are collectively known as package. A
                blueprint can be
                a) imported from TNA's public catalog
                b) modified as per a user's need
                c) proposed and approved.
                On approval, a revision of blueprint is
                created which can be used to create a
                deployment on Orchestration or Workload
                Cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_blueprint(request, metadata)
            pb_request = telcoautomation.GetBlueprintRequest.pb(request)
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
            resp = telcoautomation.Blueprint()
            pb_resp = telcoautomation.Blueprint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_blueprint(resp)
            return resp

    class _GetDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("GetDeployment")

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
            request: telcoautomation.GetDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Deployment:
            r"""Call the get deployment method over HTTP.

            Args:
                request (~.telcoautomation.GetDeploymentRequest):
                    The request object. Request object for ``GetDeployment``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Deployment:
                    Deployment contains a collection of
                YAML files (This collection is also
                known as package) that can to applied on
                an orchestration cluster (GKE cluster
                with TNA addons) or a workload cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_deployment(request, metadata)
            pb_request = telcoautomation.GetDeploymentRequest.pb(request)
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
            resp = telcoautomation.Deployment()
            pb_resp = telcoautomation.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_deployment(resp)
            return resp

    class _GetEdgeSlm(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("GetEdgeSlm")

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
            request: telcoautomation.GetEdgeSlmRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.EdgeSlm:
            r"""Call the get edge slm method over HTTP.

            Args:
                request (~.telcoautomation.GetEdgeSlmRequest):
                    The request object. Message for getting a EdgeSlm.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.EdgeSlm:
                    EdgeSlm represents an SLM instance
                which manages the lifecycle of edge
                components installed on Workload
                clusters managed by an Orchestration
                Cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/edgeSlms/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_edge_slm(request, metadata)
            pb_request = telcoautomation.GetEdgeSlmRequest.pb(request)
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
            resp = telcoautomation.EdgeSlm()
            pb_resp = telcoautomation.EdgeSlm.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_edge_slm(resp)
            return resp

    class _GetHydratedDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("GetHydratedDeployment")

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
            request: telcoautomation.GetHydratedDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.HydratedDeployment:
            r"""Call the get hydrated deployment method over HTTP.

            Args:
                request (~.telcoautomation.GetHydratedDeploymentRequest):
                    The request object. Request object for ``GetHydratedDeployment``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.HydratedDeployment:
                    A collection of kubernetes yaml files
                which are deployed on a Workload
                Cluster. Hydrated Deployments are
                created by TNA intent based automation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*/hydratedDeployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_hydrated_deployment(
                request, metadata
            )
            pb_request = telcoautomation.GetHydratedDeploymentRequest.pb(request)
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
            resp = telcoautomation.HydratedDeployment()
            pb_resp = telcoautomation.HydratedDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_hydrated_deployment(resp)
            return resp

    class _GetOrchestrationCluster(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("GetOrchestrationCluster")

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
            request: telcoautomation.GetOrchestrationClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.OrchestrationCluster:
            r"""Call the get orchestration cluster method over HTTP.

            Args:
                request (~.telcoautomation.GetOrchestrationClusterRequest):
                    The request object. Message for getting a
                OrchestrationCluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.OrchestrationCluster:
                    Orchestration cluster represents a
                GKE cluster with config controller and
                TNA specific components installed on it.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_orchestration_cluster(
                request, metadata
            )
            pb_request = telcoautomation.GetOrchestrationClusterRequest.pb(request)
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
            resp = telcoautomation.OrchestrationCluster()
            pb_resp = telcoautomation.OrchestrationCluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_orchestration_cluster(resp)
            return resp

    class _GetPublicBlueprint(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("GetPublicBlueprint")

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
            request: telcoautomation.GetPublicBlueprintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.PublicBlueprint:
            r"""Call the get public blueprint method over HTTP.

            Args:
                request (~.telcoautomation.GetPublicBlueprintRequest):
                    The request object. Request object for ``GetPublicBlueprint``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.PublicBlueprint:
                    A Blueprint contains a collection of
                kubernetes resources in the form of YAML
                files. The file contents of a blueprint
                are collectively known as package.
                Public blueprint is a TNA provided
                blueprint that in present in TNA's
                public catalog. A user can copy the
                public blueprint to their private
                catalog for further modifications.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/publicBlueprints/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_public_blueprint(
                request, metadata
            )
            pb_request = telcoautomation.GetPublicBlueprintRequest.pb(request)
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
            resp = telcoautomation.PublicBlueprint()
            pb_resp = telcoautomation.PublicBlueprint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_public_blueprint(resp)
            return resp

    class _ListBlueprintRevisions(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ListBlueprintRevisions")

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
            request: telcoautomation.ListBlueprintRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ListBlueprintRevisionsResponse:
            r"""Call the list blueprint revisions method over HTTP.

            Args:
                request (~.telcoautomation.ListBlueprintRevisionsRequest):
                    The request object. Request object for ``ListBlueprintRevisions``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.ListBlueprintRevisionsResponse:
                    Response object for ``ListBlueprintRevisions``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:listRevisions",
                },
            ]
            request, metadata = self._interceptor.pre_list_blueprint_revisions(
                request, metadata
            )
            pb_request = telcoautomation.ListBlueprintRevisionsRequest.pb(request)
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
            resp = telcoautomation.ListBlueprintRevisionsResponse()
            pb_resp = telcoautomation.ListBlueprintRevisionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_blueprint_revisions(resp)
            return resp

    class _ListBlueprints(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ListBlueprints")

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
            request: telcoautomation.ListBlueprintsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ListBlueprintsResponse:
            r"""Call the list blueprints method over HTTP.

            Args:
                request (~.telcoautomation.ListBlueprintsRequest):
                    The request object. Request object for ``ListBlueprints``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.ListBlueprintsResponse:
                    Response object for ``ListBlueprints``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/blueprints",
                },
            ]
            request, metadata = self._interceptor.pre_list_blueprints(request, metadata)
            pb_request = telcoautomation.ListBlueprintsRequest.pb(request)
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
            resp = telcoautomation.ListBlueprintsResponse()
            pb_resp = telcoautomation.ListBlueprintsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_blueprints(resp)
            return resp

    class _ListDeploymentRevisions(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ListDeploymentRevisions")

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
            request: telcoautomation.ListDeploymentRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ListDeploymentRevisionsResponse:
            r"""Call the list deployment revisions method over HTTP.

            Args:
                request (~.telcoautomation.ListDeploymentRevisionsRequest):
                    The request object. Request for listing all revisions of
                a deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.ListDeploymentRevisionsResponse:
                    List of deployment revisions for a
                given deployment.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:listRevisions",
                },
            ]
            request, metadata = self._interceptor.pre_list_deployment_revisions(
                request, metadata
            )
            pb_request = telcoautomation.ListDeploymentRevisionsRequest.pb(request)
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
            resp = telcoautomation.ListDeploymentRevisionsResponse()
            pb_resp = telcoautomation.ListDeploymentRevisionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_deployment_revisions(resp)
            return resp

    class _ListDeployments(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ListDeployments")

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
            request: telcoautomation.ListDeploymentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ListDeploymentsResponse:
            r"""Call the list deployments method over HTTP.

            Args:
                request (~.telcoautomation.ListDeploymentsRequest):
                    The request object. Request object for ``ListDeployments``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.ListDeploymentsResponse:
                    Response object for ``ListDeployments``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/deployments",
                },
            ]
            request, metadata = self._interceptor.pre_list_deployments(
                request, metadata
            )
            pb_request = telcoautomation.ListDeploymentsRequest.pb(request)
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
            resp = telcoautomation.ListDeploymentsResponse()
            pb_resp = telcoautomation.ListDeploymentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_deployments(resp)
            return resp

    class _ListEdgeSlms(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ListEdgeSlms")

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
            request: telcoautomation.ListEdgeSlmsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ListEdgeSlmsResponse:
            r"""Call the list edge slms method over HTTP.

            Args:
                request (~.telcoautomation.ListEdgeSlmsRequest):
                    The request object. Message for requesting list of
                EdgeSlms
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.ListEdgeSlmsResponse:
                    Message for response to listing
                EdgeSlms.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/edgeSlms",
                },
            ]
            request, metadata = self._interceptor.pre_list_edge_slms(request, metadata)
            pb_request = telcoautomation.ListEdgeSlmsRequest.pb(request)
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
            resp = telcoautomation.ListEdgeSlmsResponse()
            pb_resp = telcoautomation.ListEdgeSlmsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_edge_slms(resp)
            return resp

    class _ListHydratedDeployments(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ListHydratedDeployments")

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
            request: telcoautomation.ListHydratedDeploymentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ListHydratedDeploymentsResponse:
            r"""Call the list hydrated deployments method over HTTP.

            Args:
                request (~.telcoautomation.ListHydratedDeploymentsRequest):
                    The request object. Request object for ``ListHydratedDeployments``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.ListHydratedDeploymentsResponse:
                    Response object for ``ListHydratedDeployments``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/orchestrationClusters/*/deployments/*}/hydratedDeployments",
                },
            ]
            request, metadata = self._interceptor.pre_list_hydrated_deployments(
                request, metadata
            )
            pb_request = telcoautomation.ListHydratedDeploymentsRequest.pb(request)
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
            resp = telcoautomation.ListHydratedDeploymentsResponse()
            pb_resp = telcoautomation.ListHydratedDeploymentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_hydrated_deployments(resp)
            return resp

    class _ListOrchestrationClusters(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ListOrchestrationClusters")

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
            request: telcoautomation.ListOrchestrationClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ListOrchestrationClustersResponse:
            r"""Call the list orchestration
            clusters method over HTTP.

                Args:
                    request (~.telcoautomation.ListOrchestrationClustersRequest):
                        The request object. Message for requesting list of
                    OrchestrationClusters.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.telcoautomation.ListOrchestrationClustersResponse:
                        Message for response to listing
                    OrchestrationClusters.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/orchestrationClusters",
                },
            ]
            request, metadata = self._interceptor.pre_list_orchestration_clusters(
                request, metadata
            )
            pb_request = telcoautomation.ListOrchestrationClustersRequest.pb(request)
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
            resp = telcoautomation.ListOrchestrationClustersResponse()
            pb_resp = telcoautomation.ListOrchestrationClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_orchestration_clusters(resp)
            return resp

    class _ListPublicBlueprints(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ListPublicBlueprints")

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
            request: telcoautomation.ListPublicBlueprintsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.ListPublicBlueprintsResponse:
            r"""Call the list public blueprints method over HTTP.

            Args:
                request (~.telcoautomation.ListPublicBlueprintsRequest):
                    The request object. Request object for ``ListPublicBlueprints``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.ListPublicBlueprintsResponse:
                    Response object for ``ListPublicBlueprints``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/publicBlueprints",
                },
            ]
            request, metadata = self._interceptor.pre_list_public_blueprints(
                request, metadata
            )
            pb_request = telcoautomation.ListPublicBlueprintsRequest.pb(request)
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
            resp = telcoautomation.ListPublicBlueprintsResponse()
            pb_resp = telcoautomation.ListPublicBlueprintsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_public_blueprints(resp)
            return resp

    class _ProposeBlueprint(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("ProposeBlueprint")

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
            request: telcoautomation.ProposeBlueprintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Blueprint:
            r"""Call the propose blueprint method over HTTP.

            Args:
                request (~.telcoautomation.ProposeBlueprintRequest):
                    The request object. Request object for ``ProposeBlueprint``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Blueprint:
                    A Blueprint contains a collection of
                kubernetes resources in the form of YAML
                files. The file contents of a blueprint
                are collectively known as package. A
                blueprint can be
                a) imported from TNA's public catalog
                b) modified as per a user's need
                c) proposed and approved.
                On approval, a revision of blueprint is
                created which can be used to create a
                deployment on Orchestration or Workload
                Cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:propose",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_propose_blueprint(
                request, metadata
            )
            pb_request = telcoautomation.ProposeBlueprintRequest.pb(request)
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
            resp = telcoautomation.Blueprint()
            pb_resp = telcoautomation.Blueprint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_propose_blueprint(resp)
            return resp

    class _RejectBlueprint(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("RejectBlueprint")

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
            request: telcoautomation.RejectBlueprintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Blueprint:
            r"""Call the reject blueprint method over HTTP.

            Args:
                request (~.telcoautomation.RejectBlueprintRequest):
                    The request object. Request object for ``RejectBlueprint``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Blueprint:
                    A Blueprint contains a collection of
                kubernetes resources in the form of YAML
                files. The file contents of a blueprint
                are collectively known as package. A
                blueprint can be
                a) imported from TNA's public catalog
                b) modified as per a user's need
                c) proposed and approved.
                On approval, a revision of blueprint is
                created which can be used to create a
                deployment on Orchestration or Workload
                Cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:reject",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_reject_blueprint(
                request, metadata
            )
            pb_request = telcoautomation.RejectBlueprintRequest.pb(request)
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
            resp = telcoautomation.Blueprint()
            pb_resp = telcoautomation.Blueprint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_reject_blueprint(resp)
            return resp

    class _RemoveDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("RemoveDeployment")

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
            request: telcoautomation.RemoveDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the remove deployment method over HTTP.

            Args:
                request (~.telcoautomation.RemoveDeploymentRequest):
                    The request object. Request object for ``RemoveDeployment``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:remove",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_remove_deployment(
                request, metadata
            )
            pb_request = telcoautomation.RemoveDeploymentRequest.pb(request)
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

    class _RollbackDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("RollbackDeployment")

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
            request: telcoautomation.RollbackDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Deployment:
            r"""Call the rollback deployment method over HTTP.

            Args:
                request (~.telcoautomation.RollbackDeploymentRequest):
                    The request object. Request object for ``RollbackDeployment``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Deployment:
                    Deployment contains a collection of
                YAML files (This collection is also
                known as package) that can to applied on
                an orchestration cluster (GKE cluster
                with TNA addons) or a workload cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:rollback",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rollback_deployment(
                request, metadata
            )
            pb_request = telcoautomation.RollbackDeploymentRequest.pb(request)
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
            resp = telcoautomation.Deployment()
            pb_resp = telcoautomation.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rollback_deployment(resp)
            return resp

    class _SearchBlueprintRevisions(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("SearchBlueprintRevisions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "query": "",
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
            request: telcoautomation.SearchBlueprintRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.SearchBlueprintRevisionsResponse:
            r"""Call the search blueprint
            revisions method over HTTP.

                Args:
                    request (~.telcoautomation.SearchBlueprintRevisionsRequest):
                        The request object. Request object for ``SearchBlueprintRevisions``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.telcoautomation.SearchBlueprintRevisionsResponse:
                        Response object for ``SearchBlueprintRevisions``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/blueprints:searchRevisions",
                },
            ]
            request, metadata = self._interceptor.pre_search_blueprint_revisions(
                request, metadata
            )
            pb_request = telcoautomation.SearchBlueprintRevisionsRequest.pb(request)
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
            resp = telcoautomation.SearchBlueprintRevisionsResponse()
            pb_resp = telcoautomation.SearchBlueprintRevisionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_blueprint_revisions(resp)
            return resp

    class _SearchDeploymentRevisions(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("SearchDeploymentRevisions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "query": "",
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
            request: telcoautomation.SearchDeploymentRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.SearchDeploymentRevisionsResponse:
            r"""Call the search deployment
            revisions method over HTTP.

                Args:
                    request (~.telcoautomation.SearchDeploymentRevisionsRequest):
                        The request object. Request object for ``SearchDeploymentRevisions``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.telcoautomation.SearchDeploymentRevisionsResponse:
                        Response object for ``SearchDeploymentRevisions``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/deployments:searchRevisions",
                },
            ]
            request, metadata = self._interceptor.pre_search_deployment_revisions(
                request, metadata
            )
            pb_request = telcoautomation.SearchDeploymentRevisionsRequest.pb(request)
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
            resp = telcoautomation.SearchDeploymentRevisionsResponse()
            pb_resp = telcoautomation.SearchDeploymentRevisionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_deployment_revisions(resp)
            return resp

    class _UpdateBlueprint(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("UpdateBlueprint")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: telcoautomation.UpdateBlueprintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Blueprint:
            r"""Call the update blueprint method over HTTP.

            Args:
                request (~.telcoautomation.UpdateBlueprintRequest):
                    The request object. Request object for ``UpdateBlueprint``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Blueprint:
                    A Blueprint contains a collection of
                kubernetes resources in the form of YAML
                files. The file contents of a blueprint
                are collectively known as package. A
                blueprint can be
                a) imported from TNA's public catalog
                b) modified as per a user's need
                c) proposed and approved.
                On approval, a revision of blueprint is
                created which can be used to create a
                deployment on Orchestration or Workload
                Cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{blueprint.name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}",
                    "body": "blueprint",
                },
            ]
            request, metadata = self._interceptor.pre_update_blueprint(
                request, metadata
            )
            pb_request = telcoautomation.UpdateBlueprintRequest.pb(request)
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
            resp = telcoautomation.Blueprint()
            pb_resp = telcoautomation.Blueprint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_blueprint(resp)
            return resp

    class _UpdateDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("UpdateDeployment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: telcoautomation.UpdateDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.Deployment:
            r"""Call the update deployment method over HTTP.

            Args:
                request (~.telcoautomation.UpdateDeploymentRequest):
                    The request object. Request object for ``UpdateDeployment``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.telcoautomation.Deployment:
                    Deployment contains a collection of
                YAML files (This collection is also
                known as package) that can to applied on
                an orchestration cluster (GKE cluster
                with TNA addons) or a workload cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{deployment.name=projects/*/locations/*/orchestrationClusters/*/deployments/*}",
                    "body": "deployment",
                },
            ]
            request, metadata = self._interceptor.pre_update_deployment(
                request, metadata
            )
            pb_request = telcoautomation.UpdateDeploymentRequest.pb(request)
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
            resp = telcoautomation.Deployment()
            pb_resp = telcoautomation.Deployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_deployment(resp)
            return resp

    class _UpdateHydratedDeployment(TelcoAutomationRestStub):
        def __hash__(self):
            return hash("UpdateHydratedDeployment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: telcoautomation.UpdateHydratedDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> telcoautomation.HydratedDeployment:
            r"""Call the update hydrated
            deployment method over HTTP.

                Args:
                    request (~.telcoautomation.UpdateHydratedDeploymentRequest):
                        The request object. Request object for ``UpdateHydratedDeployment``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.telcoautomation.HydratedDeployment:
                        A collection of kubernetes yaml files
                    which are deployed on a Workload
                    Cluster. Hydrated Deployments are
                    created by TNA intent based automation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{hydrated_deployment.name=projects/*/locations/*/orchestrationClusters/*/deployments/*/hydratedDeployments/*}",
                    "body": "hydrated_deployment",
                },
            ]
            request, metadata = self._interceptor.pre_update_hydrated_deployment(
                request, metadata
            )
            pb_request = telcoautomation.UpdateHydratedDeploymentRequest.pb(request)
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
            resp = telcoautomation.HydratedDeployment()
            pb_resp = telcoautomation.HydratedDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_hydrated_deployment(resp)
            return resp

    @property
    def apply_deployment(
        self,
    ) -> Callable[[telcoautomation.ApplyDeploymentRequest], telcoautomation.Deployment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApplyDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def apply_hydrated_deployment(
        self,
    ) -> Callable[
        [telcoautomation.ApplyHydratedDeploymentRequest],
        telcoautomation.HydratedDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApplyHydratedDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def approve_blueprint(
        self,
    ) -> Callable[[telcoautomation.ApproveBlueprintRequest], telcoautomation.Blueprint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApproveBlueprint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def compute_deployment_status(
        self,
    ) -> Callable[
        [telcoautomation.ComputeDeploymentStatusRequest],
        telcoautomation.ComputeDeploymentStatusResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ComputeDeploymentStatus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_blueprint(
        self,
    ) -> Callable[[telcoautomation.CreateBlueprintRequest], telcoautomation.Blueprint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBlueprint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_deployment(
        self,
    ) -> Callable[
        [telcoautomation.CreateDeploymentRequest], telcoautomation.Deployment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_edge_slm(
        self,
    ) -> Callable[[telcoautomation.CreateEdgeSlmRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEdgeSlm(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_orchestration_cluster(
        self,
    ) -> Callable[
        [telcoautomation.CreateOrchestrationClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateOrchestrationCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_blueprint(
        self,
    ) -> Callable[[telcoautomation.DeleteBlueprintRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBlueprint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_edge_slm(
        self,
    ) -> Callable[[telcoautomation.DeleteEdgeSlmRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEdgeSlm(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_orchestration_cluster(
        self,
    ) -> Callable[
        [telcoautomation.DeleteOrchestrationClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteOrchestrationCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def discard_blueprint_changes(
        self,
    ) -> Callable[
        [telcoautomation.DiscardBlueprintChangesRequest],
        telcoautomation.DiscardBlueprintChangesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DiscardBlueprintChanges(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def discard_deployment_changes(
        self,
    ) -> Callable[
        [telcoautomation.DiscardDeploymentChangesRequest],
        telcoautomation.DiscardDeploymentChangesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DiscardDeploymentChanges(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_blueprint(
        self,
    ) -> Callable[[telcoautomation.GetBlueprintRequest], telcoautomation.Blueprint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBlueprint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_deployment(
        self,
    ) -> Callable[[telcoautomation.GetDeploymentRequest], telcoautomation.Deployment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_edge_slm(
        self,
    ) -> Callable[[telcoautomation.GetEdgeSlmRequest], telcoautomation.EdgeSlm]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEdgeSlm(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_hydrated_deployment(
        self,
    ) -> Callable[
        [telcoautomation.GetHydratedDeploymentRequest],
        telcoautomation.HydratedDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetHydratedDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_orchestration_cluster(
        self,
    ) -> Callable[
        [telcoautomation.GetOrchestrationClusterRequest],
        telcoautomation.OrchestrationCluster,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOrchestrationCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_public_blueprint(
        self,
    ) -> Callable[
        [telcoautomation.GetPublicBlueprintRequest], telcoautomation.PublicBlueprint
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPublicBlueprint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_blueprint_revisions(
        self,
    ) -> Callable[
        [telcoautomation.ListBlueprintRevisionsRequest],
        telcoautomation.ListBlueprintRevisionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBlueprintRevisions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_blueprints(
        self,
    ) -> Callable[
        [telcoautomation.ListBlueprintsRequest], telcoautomation.ListBlueprintsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBlueprints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_deployment_revisions(
        self,
    ) -> Callable[
        [telcoautomation.ListDeploymentRevisionsRequest],
        telcoautomation.ListDeploymentRevisionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeploymentRevisions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_deployments(
        self,
    ) -> Callable[
        [telcoautomation.ListDeploymentsRequest],
        telcoautomation.ListDeploymentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeployments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_edge_slms(
        self,
    ) -> Callable[
        [telcoautomation.ListEdgeSlmsRequest], telcoautomation.ListEdgeSlmsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEdgeSlms(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_hydrated_deployments(
        self,
    ) -> Callable[
        [telcoautomation.ListHydratedDeploymentsRequest],
        telcoautomation.ListHydratedDeploymentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListHydratedDeployments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_orchestration_clusters(
        self,
    ) -> Callable[
        [telcoautomation.ListOrchestrationClustersRequest],
        telcoautomation.ListOrchestrationClustersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOrchestrationClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_public_blueprints(
        self,
    ) -> Callable[
        [telcoautomation.ListPublicBlueprintsRequest],
        telcoautomation.ListPublicBlueprintsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPublicBlueprints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def propose_blueprint(
        self,
    ) -> Callable[[telcoautomation.ProposeBlueprintRequest], telcoautomation.Blueprint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ProposeBlueprint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reject_blueprint(
        self,
    ) -> Callable[[telcoautomation.RejectBlueprintRequest], telcoautomation.Blueprint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RejectBlueprint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_deployment(
        self,
    ) -> Callable[[telcoautomation.RemoveDeploymentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rollback_deployment(
        self,
    ) -> Callable[
        [telcoautomation.RollbackDeploymentRequest], telcoautomation.Deployment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RollbackDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_blueprint_revisions(
        self,
    ) -> Callable[
        [telcoautomation.SearchBlueprintRevisionsRequest],
        telcoautomation.SearchBlueprintRevisionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchBlueprintRevisions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_deployment_revisions(
        self,
    ) -> Callable[
        [telcoautomation.SearchDeploymentRevisionsRequest],
        telcoautomation.SearchDeploymentRevisionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchDeploymentRevisions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_blueprint(
        self,
    ) -> Callable[[telcoautomation.UpdateBlueprintRequest], telcoautomation.Blueprint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBlueprint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_deployment(
        self,
    ) -> Callable[
        [telcoautomation.UpdateDeploymentRequest], telcoautomation.Deployment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_hydrated_deployment(
        self,
    ) -> Callable[
        [telcoautomation.UpdateHydratedDeploymentRequest],
        telcoautomation.HydratedDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateHydratedDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(TelcoAutomationRestStub):
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

    class _ListLocations(TelcoAutomationRestStub):
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
                    "uri": "/v1/{name=projects/*/locations}",
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
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(TelcoAutomationRestStub):
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

    class _DeleteOperation(TelcoAutomationRestStub):
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

    class _GetOperation(TelcoAutomationRestStub):
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

    class _ListOperations(TelcoAutomationRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations}",
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


__all__ = ("TelcoAutomationRestTransport",)
