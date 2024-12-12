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
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dataform_v1beta1.types import dataform

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDataformRestTransport

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


class DataformRestInterceptor:
    """Interceptor for Dataform.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DataformRestTransport.

    .. code-block:: python
        class MyCustomDataformInterceptor(DataformRestInterceptor):
            def pre_cancel_workflow_invocation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_commit_repository_changes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_commit_workspace_changes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_compute_repository_access_token_status(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_compute_repository_access_token_status(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_compilation_result(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_compilation_result(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_release_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_release_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_workflow_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_workflow_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_workflow_invocation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_workflow_invocation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_workspace(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_workspace(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_release_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_workflow_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_workflow_invocation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_workspace(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_fetch_file_diff(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_file_diff(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_file_git_statuses(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_file_git_statuses(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_git_ahead_behind(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_git_ahead_behind(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_remote_branches(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_remote_branches(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_repository_history(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_repository_history(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_compilation_result(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_compilation_result(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_release_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_release_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workflow_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workflow_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workflow_invocation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workflow_invocation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workspace(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workspace(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_install_npm_packages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_install_npm_packages(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_compilation_results(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_compilation_results(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_release_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_release_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_repositories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_repositories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workflow_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workflow_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workflow_invocations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workflow_invocations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workspaces(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workspaces(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_make_directory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_make_directory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_move_directory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_move_directory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_move_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_move_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_pull_git_commits(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_push_git_commits(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_query_compilation_result_actions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_compilation_result_actions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_query_directory_contents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_directory_contents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_query_repository_directory_contents(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_repository_directory_contents(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_query_workflow_invocation_actions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_workflow_invocation_actions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_read_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_read_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_read_repository_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_read_repository_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_directory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_remove_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_reset_workspace_changes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_update_release_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_release_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_workflow_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_workflow_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_write_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_write_file(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DataformRestTransport(interceptor=MyCustomDataformInterceptor())
        client = DataformClient(transport=transport)


    """

    def pre_cancel_workflow_invocation(
        self,
        request: dataform.CancelWorkflowInvocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CancelWorkflowInvocationRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for cancel_workflow_invocation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_commit_repository_changes(
        self,
        request: dataform.CommitRepositoryChangesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CommitRepositoryChangesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for commit_repository_changes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_commit_workspace_changes(
        self,
        request: dataform.CommitWorkspaceChangesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CommitWorkspaceChangesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for commit_workspace_changes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_compute_repository_access_token_status(
        self,
        request: dataform.ComputeRepositoryAccessTokenStatusRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.ComputeRepositoryAccessTokenStatusRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for compute_repository_access_token_status

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_compute_repository_access_token_status(
        self, response: dataform.ComputeRepositoryAccessTokenStatusResponse
    ) -> dataform.ComputeRepositoryAccessTokenStatusResponse:
        """Post-rpc interceptor for compute_repository_access_token_status

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_create_compilation_result(
        self,
        request: dataform.CreateCompilationResultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CreateCompilationResultRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_compilation_result

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_create_compilation_result(
        self, response: dataform.CompilationResult
    ) -> dataform.CompilationResult:
        """Post-rpc interceptor for create_compilation_result

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_create_release_config(
        self,
        request: dataform.CreateReleaseConfigRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CreateReleaseConfigRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_release_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_create_release_config(
        self, response: dataform.ReleaseConfig
    ) -> dataform.ReleaseConfig:
        """Post-rpc interceptor for create_release_config

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_create_repository(
        self,
        request: dataform.CreateRepositoryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CreateRepositoryRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_create_repository(
        self, response: dataform.Repository
    ) -> dataform.Repository:
        """Post-rpc interceptor for create_repository

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_create_workflow_config(
        self,
        request: dataform.CreateWorkflowConfigRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CreateWorkflowConfigRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_workflow_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_create_workflow_config(
        self, response: dataform.WorkflowConfig
    ) -> dataform.WorkflowConfig:
        """Post-rpc interceptor for create_workflow_config

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_create_workflow_invocation(
        self,
        request: dataform.CreateWorkflowInvocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CreateWorkflowInvocationRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_workflow_invocation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_create_workflow_invocation(
        self, response: dataform.WorkflowInvocation
    ) -> dataform.WorkflowInvocation:
        """Post-rpc interceptor for create_workflow_invocation

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_create_workspace(
        self,
        request: dataform.CreateWorkspaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.CreateWorkspaceRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_workspace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_create_workspace(self, response: dataform.Workspace) -> dataform.Workspace:
        """Post-rpc interceptor for create_workspace

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_delete_release_config(
        self,
        request: dataform.DeleteReleaseConfigRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.DeleteReleaseConfigRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_release_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_delete_repository(
        self,
        request: dataform.DeleteRepositoryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.DeleteRepositoryRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_delete_workflow_config(
        self,
        request: dataform.DeleteWorkflowConfigRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.DeleteWorkflowConfigRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_workflow_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_delete_workflow_invocation(
        self,
        request: dataform.DeleteWorkflowInvocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.DeleteWorkflowInvocationRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_workflow_invocation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_delete_workspace(
        self,
        request: dataform.DeleteWorkspaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.DeleteWorkspaceRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_workspace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_fetch_file_diff(
        self,
        request: dataform.FetchFileDiffRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.FetchFileDiffRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for fetch_file_diff

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_fetch_file_diff(
        self, response: dataform.FetchFileDiffResponse
    ) -> dataform.FetchFileDiffResponse:
        """Post-rpc interceptor for fetch_file_diff

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_file_git_statuses(
        self,
        request: dataform.FetchFileGitStatusesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.FetchFileGitStatusesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for fetch_file_git_statuses

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_fetch_file_git_statuses(
        self, response: dataform.FetchFileGitStatusesResponse
    ) -> dataform.FetchFileGitStatusesResponse:
        """Post-rpc interceptor for fetch_file_git_statuses

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_git_ahead_behind(
        self,
        request: dataform.FetchGitAheadBehindRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.FetchGitAheadBehindRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for fetch_git_ahead_behind

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_fetch_git_ahead_behind(
        self, response: dataform.FetchGitAheadBehindResponse
    ) -> dataform.FetchGitAheadBehindResponse:
        """Post-rpc interceptor for fetch_git_ahead_behind

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_remote_branches(
        self,
        request: dataform.FetchRemoteBranchesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.FetchRemoteBranchesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for fetch_remote_branches

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_fetch_remote_branches(
        self, response: dataform.FetchRemoteBranchesResponse
    ) -> dataform.FetchRemoteBranchesResponse:
        """Post-rpc interceptor for fetch_remote_branches

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_repository_history(
        self,
        request: dataform.FetchRepositoryHistoryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.FetchRepositoryHistoryRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for fetch_repository_history

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_fetch_repository_history(
        self, response: dataform.FetchRepositoryHistoryResponse
    ) -> dataform.FetchRepositoryHistoryResponse:
        """Post-rpc interceptor for fetch_repository_history

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_get_compilation_result(
        self,
        request: dataform.GetCompilationResultRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.GetCompilationResultRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_compilation_result

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_get_compilation_result(
        self, response: dataform.CompilationResult
    ) -> dataform.CompilationResult:
        """Post-rpc interceptor for get_compilation_result

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_get_release_config(
        self,
        request: dataform.GetReleaseConfigRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.GetReleaseConfigRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_release_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_get_release_config(
        self, response: dataform.ReleaseConfig
    ) -> dataform.ReleaseConfig:
        """Post-rpc interceptor for get_release_config

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_get_repository(
        self,
        request: dataform.GetRepositoryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.GetRepositoryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_get_repository(self, response: dataform.Repository) -> dataform.Repository:
        """Post-rpc interceptor for get_repository

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_get_workflow_config(
        self,
        request: dataform.GetWorkflowConfigRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.GetWorkflowConfigRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_workflow_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_get_workflow_config(
        self, response: dataform.WorkflowConfig
    ) -> dataform.WorkflowConfig:
        """Post-rpc interceptor for get_workflow_config

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_get_workflow_invocation(
        self,
        request: dataform.GetWorkflowInvocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.GetWorkflowInvocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_workflow_invocation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_get_workflow_invocation(
        self, response: dataform.WorkflowInvocation
    ) -> dataform.WorkflowInvocation:
        """Post-rpc interceptor for get_workflow_invocation

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_get_workspace(
        self,
        request: dataform.GetWorkspaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.GetWorkspaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_workspace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_get_workspace(self, response: dataform.Workspace) -> dataform.Workspace:
        """Post-rpc interceptor for get_workspace

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_install_npm_packages(
        self,
        request: dataform.InstallNpmPackagesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.InstallNpmPackagesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for install_npm_packages

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_install_npm_packages(
        self, response: dataform.InstallNpmPackagesResponse
    ) -> dataform.InstallNpmPackagesResponse:
        """Post-rpc interceptor for install_npm_packages

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_list_compilation_results(
        self,
        request: dataform.ListCompilationResultsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.ListCompilationResultsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_compilation_results

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_list_compilation_results(
        self, response: dataform.ListCompilationResultsResponse
    ) -> dataform.ListCompilationResultsResponse:
        """Post-rpc interceptor for list_compilation_results

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_list_release_configs(
        self,
        request: dataform.ListReleaseConfigsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.ListReleaseConfigsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_release_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_list_release_configs(
        self, response: dataform.ListReleaseConfigsResponse
    ) -> dataform.ListReleaseConfigsResponse:
        """Post-rpc interceptor for list_release_configs

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_list_repositories(
        self,
        request: dataform.ListRepositoriesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.ListRepositoriesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_repositories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_list_repositories(
        self, response: dataform.ListRepositoriesResponse
    ) -> dataform.ListRepositoriesResponse:
        """Post-rpc interceptor for list_repositories

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_list_workflow_configs(
        self,
        request: dataform.ListWorkflowConfigsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.ListWorkflowConfigsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_workflow_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_list_workflow_configs(
        self, response: dataform.ListWorkflowConfigsResponse
    ) -> dataform.ListWorkflowConfigsResponse:
        """Post-rpc interceptor for list_workflow_configs

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_list_workflow_invocations(
        self,
        request: dataform.ListWorkflowInvocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.ListWorkflowInvocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_workflow_invocations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_list_workflow_invocations(
        self, response: dataform.ListWorkflowInvocationsResponse
    ) -> dataform.ListWorkflowInvocationsResponse:
        """Post-rpc interceptor for list_workflow_invocations

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_list_workspaces(
        self,
        request: dataform.ListWorkspacesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.ListWorkspacesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_workspaces

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_list_workspaces(
        self, response: dataform.ListWorkspacesResponse
    ) -> dataform.ListWorkspacesResponse:
        """Post-rpc interceptor for list_workspaces

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_make_directory(
        self,
        request: dataform.MakeDirectoryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.MakeDirectoryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for make_directory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_make_directory(
        self, response: dataform.MakeDirectoryResponse
    ) -> dataform.MakeDirectoryResponse:
        """Post-rpc interceptor for make_directory

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_move_directory(
        self,
        request: dataform.MoveDirectoryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.MoveDirectoryRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for move_directory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_move_directory(
        self, response: dataform.MoveDirectoryResponse
    ) -> dataform.MoveDirectoryResponse:
        """Post-rpc interceptor for move_directory

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_move_file(
        self,
        request: dataform.MoveFileRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.MoveFileRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for move_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_move_file(
        self, response: dataform.MoveFileResponse
    ) -> dataform.MoveFileResponse:
        """Post-rpc interceptor for move_file

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_pull_git_commits(
        self,
        request: dataform.PullGitCommitsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.PullGitCommitsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for pull_git_commits

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_push_git_commits(
        self,
        request: dataform.PushGitCommitsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.PushGitCommitsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for push_git_commits

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_query_compilation_result_actions(
        self,
        request: dataform.QueryCompilationResultActionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.QueryCompilationResultActionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for query_compilation_result_actions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_query_compilation_result_actions(
        self, response: dataform.QueryCompilationResultActionsResponse
    ) -> dataform.QueryCompilationResultActionsResponse:
        """Post-rpc interceptor for query_compilation_result_actions

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_query_directory_contents(
        self,
        request: dataform.QueryDirectoryContentsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.QueryDirectoryContentsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for query_directory_contents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_query_directory_contents(
        self, response: dataform.QueryDirectoryContentsResponse
    ) -> dataform.QueryDirectoryContentsResponse:
        """Post-rpc interceptor for query_directory_contents

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_query_repository_directory_contents(
        self,
        request: dataform.QueryRepositoryDirectoryContentsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.QueryRepositoryDirectoryContentsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for query_repository_directory_contents

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_query_repository_directory_contents(
        self, response: dataform.QueryRepositoryDirectoryContentsResponse
    ) -> dataform.QueryRepositoryDirectoryContentsResponse:
        """Post-rpc interceptor for query_repository_directory_contents

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_query_workflow_invocation_actions(
        self,
        request: dataform.QueryWorkflowInvocationActionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.QueryWorkflowInvocationActionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for query_workflow_invocation_actions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_query_workflow_invocation_actions(
        self, response: dataform.QueryWorkflowInvocationActionsResponse
    ) -> dataform.QueryWorkflowInvocationActionsResponse:
        """Post-rpc interceptor for query_workflow_invocation_actions

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_read_file(
        self,
        request: dataform.ReadFileRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.ReadFileRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for read_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_read_file(
        self, response: dataform.ReadFileResponse
    ) -> dataform.ReadFileResponse:
        """Post-rpc interceptor for read_file

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_read_repository_file(
        self,
        request: dataform.ReadRepositoryFileRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.ReadRepositoryFileRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for read_repository_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_read_repository_file(
        self, response: dataform.ReadRepositoryFileResponse
    ) -> dataform.ReadRepositoryFileResponse:
        """Post-rpc interceptor for read_repository_file

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_remove_directory(
        self,
        request: dataform.RemoveDirectoryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.RemoveDirectoryRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for remove_directory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_remove_file(
        self,
        request: dataform.RemoveFileRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.RemoveFileRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for remove_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_reset_workspace_changes(
        self,
        request: dataform.ResetWorkspaceChangesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.ResetWorkspaceChangesRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for reset_workspace_changes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_update_release_config(
        self,
        request: dataform.UpdateReleaseConfigRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.UpdateReleaseConfigRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_release_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_update_release_config(
        self, response: dataform.ReleaseConfig
    ) -> dataform.ReleaseConfig:
        """Post-rpc interceptor for update_release_config

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_update_repository(
        self,
        request: dataform.UpdateRepositoryRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.UpdateRepositoryRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_update_repository(
        self, response: dataform.Repository
    ) -> dataform.Repository:
        """Post-rpc interceptor for update_repository

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_update_workflow_config(
        self,
        request: dataform.UpdateWorkflowConfigRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        dataform.UpdateWorkflowConfigRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_workflow_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_update_workflow_config(
        self, response: dataform.WorkflowConfig
    ) -> dataform.WorkflowConfig:
        """Post-rpc interceptor for update_workflow_config

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_write_file(
        self,
        request: dataform.WriteFileRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[dataform.WriteFileRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for write_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_write_file(
        self, response: dataform.WriteFileResponse
    ) -> dataform.WriteFileResponse:
        """Post-rpc interceptor for write_file

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
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
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
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
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
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
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
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
        before they are sent to the Dataform server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the Dataform server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DataformRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DataformRestInterceptor


class DataformRestTransport(_BaseDataformRestTransport):
    """REST backend synchronous transport for Dataform.

    Dataform is a service to develop, create, document, test, and
    update curated tables in BigQuery.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dataform.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DataformRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dataform.googleapis.com').
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
        self._interceptor = interceptor or DataformRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CancelWorkflowInvocation(
        _BaseDataformRestTransport._BaseCancelWorkflowInvocation, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CancelWorkflowInvocation")

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
            request: dataform.CancelWorkflowInvocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the cancel workflow
            invocation method over HTTP.

                Args:
                    request (~.dataform.CancelWorkflowInvocationRequest):
                        The request object. ``CancelWorkflowInvocation`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseCancelWorkflowInvocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_workflow_invocation(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseCancelWorkflowInvocation._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseCancelWorkflowInvocation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseCancelWorkflowInvocation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CancelWorkflowInvocation",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CancelWorkflowInvocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CancelWorkflowInvocation._get_response(
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

    class _CommitRepositoryChanges(
        _BaseDataformRestTransport._BaseCommitRepositoryChanges, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CommitRepositoryChanges")

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
            request: dataform.CommitRepositoryChangesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the commit repository changes method over HTTP.

            Args:
                request (~.dataform.CommitRepositoryChangesRequest):
                    The request object. ``CommitRepositoryChanges`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseCommitRepositoryChanges._get_http_options()
            )

            request, metadata = self._interceptor.pre_commit_repository_changes(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseCommitRepositoryChanges._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseCommitRepositoryChanges._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseCommitRepositoryChanges._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CommitRepositoryChanges",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CommitRepositoryChanges",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CommitRepositoryChanges._get_response(
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

    class _CommitWorkspaceChanges(
        _BaseDataformRestTransport._BaseCommitWorkspaceChanges, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CommitWorkspaceChanges")

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
            request: dataform.CommitWorkspaceChangesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the commit workspace changes method over HTTP.

            Args:
                request (~.dataform.CommitWorkspaceChangesRequest):
                    The request object. ``CommitWorkspaceChanges`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseCommitWorkspaceChanges._get_http_options()
            )

            request, metadata = self._interceptor.pre_commit_workspace_changes(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseCommitWorkspaceChanges._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseCommitWorkspaceChanges._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseCommitWorkspaceChanges._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CommitWorkspaceChanges",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CommitWorkspaceChanges",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CommitWorkspaceChanges._get_response(
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

    class _ComputeRepositoryAccessTokenStatus(
        _BaseDataformRestTransport._BaseComputeRepositoryAccessTokenStatus,
        DataformRestStub,
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ComputeRepositoryAccessTokenStatus")

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
            request: dataform.ComputeRepositoryAccessTokenStatusRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ComputeRepositoryAccessTokenStatusResponse:
            r"""Call the compute repository access
            token status method over HTTP.

                Args:
                    request (~.dataform.ComputeRepositoryAccessTokenStatusRequest):
                        The request object. ``ComputeRepositoryAccessTokenStatus`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.dataform.ComputeRepositoryAccessTokenStatusResponse:
                        ``ComputeRepositoryAccessTokenStatus`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseComputeRepositoryAccessTokenStatus._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_compute_repository_access_token_status(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseComputeRepositoryAccessTokenStatus._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseComputeRepositoryAccessTokenStatus._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ComputeRepositoryAccessTokenStatus",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ComputeRepositoryAccessTokenStatus",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                DataformRestTransport._ComputeRepositoryAccessTokenStatus._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataform.ComputeRepositoryAccessTokenStatusResponse()
            pb_resp = dataform.ComputeRepositoryAccessTokenStatusResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_compute_repository_access_token_status(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        dataform.ComputeRepositoryAccessTokenStatusResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.compute_repository_access_token_status",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ComputeRepositoryAccessTokenStatus",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateCompilationResult(
        _BaseDataformRestTransport._BaseCreateCompilationResult, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CreateCompilationResult")

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
            request: dataform.CreateCompilationResultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.CompilationResult:
            r"""Call the create compilation result method over HTTP.

            Args:
                request (~.dataform.CreateCompilationResultRequest):
                    The request object. ``CreateCompilationResult`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.CompilationResult:
                    Represents the result of compiling a
                Dataform project.

            """

            http_options = (
                _BaseDataformRestTransport._BaseCreateCompilationResult._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_compilation_result(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseCreateCompilationResult._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseCreateCompilationResult._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseCreateCompilationResult._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CreateCompilationResult",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateCompilationResult",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CreateCompilationResult._get_response(
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
            resp = dataform.CompilationResult()
            pb_resp = dataform.CompilationResult.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_compilation_result(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.CompilationResult.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.create_compilation_result",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateCompilationResult",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateReleaseConfig(
        _BaseDataformRestTransport._BaseCreateReleaseConfig, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CreateReleaseConfig")

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
            request: dataform.CreateReleaseConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ReleaseConfig:
            r"""Call the create release config method over HTTP.

            Args:
                request (~.dataform.CreateReleaseConfigRequest):
                    The request object. ``CreateReleaseConfig`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ReleaseConfig:
                    Represents a Dataform release
                configuration.

            """

            http_options = (
                _BaseDataformRestTransport._BaseCreateReleaseConfig._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_release_config(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseCreateReleaseConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseCreateReleaseConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseCreateReleaseConfig._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CreateReleaseConfig",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateReleaseConfig",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CreateReleaseConfig._get_response(
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
            resp = dataform.ReleaseConfig()
            pb_resp = dataform.ReleaseConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_release_config(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ReleaseConfig.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.create_release_config",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateReleaseConfig",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateRepository(
        _BaseDataformRestTransport._BaseCreateRepository, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CreateRepository")

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
            request: dataform.CreateRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.Repository:
            r"""Call the create repository method over HTTP.

            Args:
                request (~.dataform.CreateRepositoryRequest):
                    The request object. ``CreateRepository`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.Repository:
                    Represents a Dataform Git repository.
            """

            http_options = (
                _BaseDataformRestTransport._BaseCreateRepository._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_repository(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseCreateRepository._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseDataformRestTransport._BaseCreateRepository._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseCreateRepository._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CreateRepository",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateRepository",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CreateRepository._get_response(
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
            resp = dataform.Repository()
            pb_resp = dataform.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_repository(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.Repository.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.create_repository",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateRepository",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateWorkflowConfig(
        _BaseDataformRestTransport._BaseCreateWorkflowConfig, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CreateWorkflowConfig")

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
            request: dataform.CreateWorkflowConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.WorkflowConfig:
            r"""Call the create workflow config method over HTTP.

            Args:
                request (~.dataform.CreateWorkflowConfigRequest):
                    The request object. ``CreateWorkflowConfig`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.WorkflowConfig:
                    Represents a Dataform workflow
                configuration.

            """

            http_options = (
                _BaseDataformRestTransport._BaseCreateWorkflowConfig._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_workflow_config(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseCreateWorkflowConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseCreateWorkflowConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseCreateWorkflowConfig._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CreateWorkflowConfig",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateWorkflowConfig",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CreateWorkflowConfig._get_response(
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
            resp = dataform.WorkflowConfig()
            pb_resp = dataform.WorkflowConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_workflow_config(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.WorkflowConfig.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.create_workflow_config",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateWorkflowConfig",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateWorkflowInvocation(
        _BaseDataformRestTransport._BaseCreateWorkflowInvocation, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CreateWorkflowInvocation")

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
            request: dataform.CreateWorkflowInvocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.WorkflowInvocation:
            r"""Call the create workflow
            invocation method over HTTP.

                Args:
                    request (~.dataform.CreateWorkflowInvocationRequest):
                        The request object. ``CreateWorkflowInvocation`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.dataform.WorkflowInvocation:
                        Represents a single invocation of a
                    compilation result.

            """

            http_options = (
                _BaseDataformRestTransport._BaseCreateWorkflowInvocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_workflow_invocation(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseCreateWorkflowInvocation._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseCreateWorkflowInvocation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseCreateWorkflowInvocation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CreateWorkflowInvocation",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateWorkflowInvocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CreateWorkflowInvocation._get_response(
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
            resp = dataform.WorkflowInvocation()
            pb_resp = dataform.WorkflowInvocation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_workflow_invocation(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.WorkflowInvocation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.create_workflow_invocation",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateWorkflowInvocation",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateWorkspace(
        _BaseDataformRestTransport._BaseCreateWorkspace, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.CreateWorkspace")

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
            request: dataform.CreateWorkspaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.Workspace:
            r"""Call the create workspace method over HTTP.

            Args:
                request (~.dataform.CreateWorkspaceRequest):
                    The request object. ``CreateWorkspace`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.Workspace:
                    Represents a Dataform Git workspace.
            """

            http_options = (
                _BaseDataformRestTransport._BaseCreateWorkspace._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_workspace(
                request, metadata
            )
            transcoded_request = (
                _BaseDataformRestTransport._BaseCreateWorkspace._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseDataformRestTransport._BaseCreateWorkspace._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseCreateWorkspace._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.CreateWorkspace",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateWorkspace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._CreateWorkspace._get_response(
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
            resp = dataform.Workspace()
            pb_resp = dataform.Workspace.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_workspace(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.Workspace.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.create_workspace",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "CreateWorkspace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteReleaseConfig(
        _BaseDataformRestTransport._BaseDeleteReleaseConfig, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.DeleteReleaseConfig")

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
            request: dataform.DeleteReleaseConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete release config method over HTTP.

            Args:
                request (~.dataform.DeleteReleaseConfigRequest):
                    The request object. ``DeleteReleaseConfig`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseDeleteReleaseConfig._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_release_config(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseDeleteReleaseConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseDeleteReleaseConfig._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.DeleteReleaseConfig",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "DeleteReleaseConfig",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._DeleteReleaseConfig._get_response(
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

    class _DeleteRepository(
        _BaseDataformRestTransport._BaseDeleteRepository, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.DeleteRepository")

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
            request: dataform.DeleteRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete repository method over HTTP.

            Args:
                request (~.dataform.DeleteRepositoryRequest):
                    The request object. ``DeleteRepository`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseDeleteRepository._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_repository(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseDeleteRepository._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseDeleteRepository._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.DeleteRepository",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "DeleteRepository",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._DeleteRepository._get_response(
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

    class _DeleteWorkflowConfig(
        _BaseDataformRestTransport._BaseDeleteWorkflowConfig, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.DeleteWorkflowConfig")

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
            request: dataform.DeleteWorkflowConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete workflow config method over HTTP.

            Args:
                request (~.dataform.DeleteWorkflowConfigRequest):
                    The request object. ``DeleteWorkflowConfig`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseDeleteWorkflowConfig._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_workflow_config(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseDeleteWorkflowConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseDeleteWorkflowConfig._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.DeleteWorkflowConfig",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "DeleteWorkflowConfig",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._DeleteWorkflowConfig._get_response(
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

    class _DeleteWorkflowInvocation(
        _BaseDataformRestTransport._BaseDeleteWorkflowInvocation, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.DeleteWorkflowInvocation")

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
            request: dataform.DeleteWorkflowInvocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete workflow
            invocation method over HTTP.

                Args:
                    request (~.dataform.DeleteWorkflowInvocationRequest):
                        The request object. ``DeleteWorkflowInvocation`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseDeleteWorkflowInvocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_workflow_invocation(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseDeleteWorkflowInvocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseDeleteWorkflowInvocation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.DeleteWorkflowInvocation",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "DeleteWorkflowInvocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._DeleteWorkflowInvocation._get_response(
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

    class _DeleteWorkspace(
        _BaseDataformRestTransport._BaseDeleteWorkspace, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.DeleteWorkspace")

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
            request: dataform.DeleteWorkspaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete workspace method over HTTP.

            Args:
                request (~.dataform.DeleteWorkspaceRequest):
                    The request object. ``DeleteWorkspace`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseDeleteWorkspace._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_workspace(
                request, metadata
            )
            transcoded_request = (
                _BaseDataformRestTransport._BaseDeleteWorkspace._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseDeleteWorkspace._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.DeleteWorkspace",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "DeleteWorkspace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._DeleteWorkspace._get_response(
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

    class _FetchFileDiff(
        _BaseDataformRestTransport._BaseFetchFileDiff, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.FetchFileDiff")

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
            request: dataform.FetchFileDiffRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.FetchFileDiffResponse:
            r"""Call the fetch file diff method over HTTP.

            Args:
                request (~.dataform.FetchFileDiffRequest):
                    The request object. ``FetchFileDiff`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.FetchFileDiffResponse:
                    ``FetchFileDiff`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseFetchFileDiff._get_http_options()
            )

            request, metadata = self._interceptor.pre_fetch_file_diff(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseFetchFileDiff._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseFetchFileDiff._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.FetchFileDiff",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchFileDiff",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._FetchFileDiff._get_response(
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
            resp = dataform.FetchFileDiffResponse()
            pb_resp = dataform.FetchFileDiffResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_fetch_file_diff(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.FetchFileDiffResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.fetch_file_diff",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchFileDiff",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _FetchFileGitStatuses(
        _BaseDataformRestTransport._BaseFetchFileGitStatuses, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.FetchFileGitStatuses")

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
            request: dataform.FetchFileGitStatusesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.FetchFileGitStatusesResponse:
            r"""Call the fetch file git statuses method over HTTP.

            Args:
                request (~.dataform.FetchFileGitStatusesRequest):
                    The request object. ``FetchFileGitStatuses`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.FetchFileGitStatusesResponse:
                    ``FetchFileGitStatuses`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseFetchFileGitStatuses._get_http_options()
            )

            request, metadata = self._interceptor.pre_fetch_file_git_statuses(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseFetchFileGitStatuses._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseFetchFileGitStatuses._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.FetchFileGitStatuses",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchFileGitStatuses",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._FetchFileGitStatuses._get_response(
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
            resp = dataform.FetchFileGitStatusesResponse()
            pb_resp = dataform.FetchFileGitStatusesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_fetch_file_git_statuses(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.FetchFileGitStatusesResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.fetch_file_git_statuses",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchFileGitStatuses",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _FetchGitAheadBehind(
        _BaseDataformRestTransport._BaseFetchGitAheadBehind, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.FetchGitAheadBehind")

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
            request: dataform.FetchGitAheadBehindRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.FetchGitAheadBehindResponse:
            r"""Call the fetch git ahead behind method over HTTP.

            Args:
                request (~.dataform.FetchGitAheadBehindRequest):
                    The request object. ``FetchGitAheadBehind`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.FetchGitAheadBehindResponse:
                    ``FetchGitAheadBehind`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseFetchGitAheadBehind._get_http_options()
            )

            request, metadata = self._interceptor.pre_fetch_git_ahead_behind(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseFetchGitAheadBehind._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseFetchGitAheadBehind._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.FetchGitAheadBehind",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchGitAheadBehind",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._FetchGitAheadBehind._get_response(
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
            resp = dataform.FetchGitAheadBehindResponse()
            pb_resp = dataform.FetchGitAheadBehindResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_fetch_git_ahead_behind(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.FetchGitAheadBehindResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.fetch_git_ahead_behind",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchGitAheadBehind",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _FetchRemoteBranches(
        _BaseDataformRestTransport._BaseFetchRemoteBranches, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.FetchRemoteBranches")

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
            request: dataform.FetchRemoteBranchesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.FetchRemoteBranchesResponse:
            r"""Call the fetch remote branches method over HTTP.

            Args:
                request (~.dataform.FetchRemoteBranchesRequest):
                    The request object. ``FetchRemoteBranches`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.FetchRemoteBranchesResponse:
                    ``FetchRemoteBranches`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseFetchRemoteBranches._get_http_options()
            )

            request, metadata = self._interceptor.pre_fetch_remote_branches(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseFetchRemoteBranches._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseFetchRemoteBranches._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.FetchRemoteBranches",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchRemoteBranches",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._FetchRemoteBranches._get_response(
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
            resp = dataform.FetchRemoteBranchesResponse()
            pb_resp = dataform.FetchRemoteBranchesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_fetch_remote_branches(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.FetchRemoteBranchesResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.fetch_remote_branches",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchRemoteBranches",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _FetchRepositoryHistory(
        _BaseDataformRestTransport._BaseFetchRepositoryHistory, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.FetchRepositoryHistory")

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
            request: dataform.FetchRepositoryHistoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.FetchRepositoryHistoryResponse:
            r"""Call the fetch repository history method over HTTP.

            Args:
                request (~.dataform.FetchRepositoryHistoryRequest):
                    The request object. ``FetchRepositoryHistory`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.FetchRepositoryHistoryResponse:
                    ``FetchRepositoryHistory`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseFetchRepositoryHistory._get_http_options()
            )

            request, metadata = self._interceptor.pre_fetch_repository_history(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseFetchRepositoryHistory._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseFetchRepositoryHistory._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.FetchRepositoryHistory",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchRepositoryHistory",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._FetchRepositoryHistory._get_response(
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
            resp = dataform.FetchRepositoryHistoryResponse()
            pb_resp = dataform.FetchRepositoryHistoryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_fetch_repository_history(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.FetchRepositoryHistoryResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.fetch_repository_history",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "FetchRepositoryHistory",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetCompilationResult(
        _BaseDataformRestTransport._BaseGetCompilationResult, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.GetCompilationResult")

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
            request: dataform.GetCompilationResultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.CompilationResult:
            r"""Call the get compilation result method over HTTP.

            Args:
                request (~.dataform.GetCompilationResultRequest):
                    The request object. ``GetCompilationResult`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.CompilationResult:
                    Represents the result of compiling a
                Dataform project.

            """

            http_options = (
                _BaseDataformRestTransport._BaseGetCompilationResult._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_compilation_result(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseGetCompilationResult._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseGetCompilationResult._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.GetCompilationResult",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetCompilationResult",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._GetCompilationResult._get_response(
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
            resp = dataform.CompilationResult()
            pb_resp = dataform.CompilationResult.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_compilation_result(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.CompilationResult.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.get_compilation_result",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetCompilationResult",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetReleaseConfig(
        _BaseDataformRestTransport._BaseGetReleaseConfig, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.GetReleaseConfig")

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
            request: dataform.GetReleaseConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ReleaseConfig:
            r"""Call the get release config method over HTTP.

            Args:
                request (~.dataform.GetReleaseConfigRequest):
                    The request object. ``GetReleaseConfig`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ReleaseConfig:
                    Represents a Dataform release
                configuration.

            """

            http_options = (
                _BaseDataformRestTransport._BaseGetReleaseConfig._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_release_config(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseGetReleaseConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseGetReleaseConfig._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.GetReleaseConfig",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetReleaseConfig",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._GetReleaseConfig._get_response(
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
            resp = dataform.ReleaseConfig()
            pb_resp = dataform.ReleaseConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_release_config(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ReleaseConfig.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.get_release_config",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetReleaseConfig",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetRepository(
        _BaseDataformRestTransport._BaseGetRepository, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.GetRepository")

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
            request: dataform.GetRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.Repository:
            r"""Call the get repository method over HTTP.

            Args:
                request (~.dataform.GetRepositoryRequest):
                    The request object. ``GetRepository`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.Repository:
                    Represents a Dataform Git repository.
            """

            http_options = (
                _BaseDataformRestTransport._BaseGetRepository._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_repository(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseGetRepository._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseGetRepository._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.GetRepository",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetRepository",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._GetRepository._get_response(
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
            resp = dataform.Repository()
            pb_resp = dataform.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_repository(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.Repository.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.get_repository",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetRepository",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetWorkflowConfig(
        _BaseDataformRestTransport._BaseGetWorkflowConfig, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.GetWorkflowConfig")

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
            request: dataform.GetWorkflowConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.WorkflowConfig:
            r"""Call the get workflow config method over HTTP.

            Args:
                request (~.dataform.GetWorkflowConfigRequest):
                    The request object. ``GetWorkflowConfig`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.WorkflowConfig:
                    Represents a Dataform workflow
                configuration.

            """

            http_options = (
                _BaseDataformRestTransport._BaseGetWorkflowConfig._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_workflow_config(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseGetWorkflowConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseGetWorkflowConfig._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.GetWorkflowConfig",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetWorkflowConfig",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._GetWorkflowConfig._get_response(
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
            resp = dataform.WorkflowConfig()
            pb_resp = dataform.WorkflowConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_workflow_config(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.WorkflowConfig.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.get_workflow_config",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetWorkflowConfig",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetWorkflowInvocation(
        _BaseDataformRestTransport._BaseGetWorkflowInvocation, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.GetWorkflowInvocation")

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
            request: dataform.GetWorkflowInvocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.WorkflowInvocation:
            r"""Call the get workflow invocation method over HTTP.

            Args:
                request (~.dataform.GetWorkflowInvocationRequest):
                    The request object. ``GetWorkflowInvocation`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.WorkflowInvocation:
                    Represents a single invocation of a
                compilation result.

            """

            http_options = (
                _BaseDataformRestTransport._BaseGetWorkflowInvocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_workflow_invocation(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseGetWorkflowInvocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseGetWorkflowInvocation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.GetWorkflowInvocation",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetWorkflowInvocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._GetWorkflowInvocation._get_response(
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
            resp = dataform.WorkflowInvocation()
            pb_resp = dataform.WorkflowInvocation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_workflow_invocation(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.WorkflowInvocation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.get_workflow_invocation",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetWorkflowInvocation",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetWorkspace(_BaseDataformRestTransport._BaseGetWorkspace, DataformRestStub):
        def __hash__(self):
            return hash("DataformRestTransport.GetWorkspace")

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
            request: dataform.GetWorkspaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.Workspace:
            r"""Call the get workspace method over HTTP.

            Args:
                request (~.dataform.GetWorkspaceRequest):
                    The request object. ``GetWorkspace`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.Workspace:
                    Represents a Dataform Git workspace.
            """

            http_options = (
                _BaseDataformRestTransport._BaseGetWorkspace._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_workspace(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseGetWorkspace._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseGetWorkspace._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.GetWorkspace",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetWorkspace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._GetWorkspace._get_response(
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
            resp = dataform.Workspace()
            pb_resp = dataform.Workspace.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_workspace(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.Workspace.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.get_workspace",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetWorkspace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _InstallNpmPackages(
        _BaseDataformRestTransport._BaseInstallNpmPackages, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.InstallNpmPackages")

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
            request: dataform.InstallNpmPackagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.InstallNpmPackagesResponse:
            r"""Call the install npm packages method over HTTP.

            Args:
                request (~.dataform.InstallNpmPackagesRequest):
                    The request object. ``InstallNpmPackages`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.InstallNpmPackagesResponse:
                    ``InstallNpmPackages`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseInstallNpmPackages._get_http_options()
            )

            request, metadata = self._interceptor.pre_install_npm_packages(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseInstallNpmPackages._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseInstallNpmPackages._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseInstallNpmPackages._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.InstallNpmPackages",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "InstallNpmPackages",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._InstallNpmPackages._get_response(
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
            resp = dataform.InstallNpmPackagesResponse()
            pb_resp = dataform.InstallNpmPackagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_install_npm_packages(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.InstallNpmPackagesResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.install_npm_packages",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "InstallNpmPackages",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListCompilationResults(
        _BaseDataformRestTransport._BaseListCompilationResults, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ListCompilationResults")

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
            request: dataform.ListCompilationResultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ListCompilationResultsResponse:
            r"""Call the list compilation results method over HTTP.

            Args:
                request (~.dataform.ListCompilationResultsRequest):
                    The request object. ``ListCompilationResults`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ListCompilationResultsResponse:
                    ``ListCompilationResults`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseListCompilationResults._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_compilation_results(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseListCompilationResults._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseListCompilationResults._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ListCompilationResults",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListCompilationResults",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ListCompilationResults._get_response(
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
            resp = dataform.ListCompilationResultsResponse()
            pb_resp = dataform.ListCompilationResultsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_compilation_results(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ListCompilationResultsResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.list_compilation_results",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListCompilationResults",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListReleaseConfigs(
        _BaseDataformRestTransport._BaseListReleaseConfigs, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ListReleaseConfigs")

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
            request: dataform.ListReleaseConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ListReleaseConfigsResponse:
            r"""Call the list release configs method over HTTP.

            Args:
                request (~.dataform.ListReleaseConfigsRequest):
                    The request object. ``ListReleaseConfigs`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ListReleaseConfigsResponse:
                    ``ListReleaseConfigs`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseListReleaseConfigs._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_release_configs(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseListReleaseConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseListReleaseConfigs._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ListReleaseConfigs",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListReleaseConfigs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ListReleaseConfigs._get_response(
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
            resp = dataform.ListReleaseConfigsResponse()
            pb_resp = dataform.ListReleaseConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_release_configs(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ListReleaseConfigsResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.list_release_configs",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListReleaseConfigs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListRepositories(
        _BaseDataformRestTransport._BaseListRepositories, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ListRepositories")

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
            request: dataform.ListRepositoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ListRepositoriesResponse:
            r"""Call the list repositories method over HTTP.

            Args:
                request (~.dataform.ListRepositoriesRequest):
                    The request object. ``ListRepositories`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ListRepositoriesResponse:
                    ``ListRepositories`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseListRepositories._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_repositories(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseListRepositories._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseListRepositories._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ListRepositories",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListRepositories",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ListRepositories._get_response(
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
            resp = dataform.ListRepositoriesResponse()
            pb_resp = dataform.ListRepositoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_repositories(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ListRepositoriesResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.list_repositories",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListRepositories",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListWorkflowConfigs(
        _BaseDataformRestTransport._BaseListWorkflowConfigs, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ListWorkflowConfigs")

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
            request: dataform.ListWorkflowConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ListWorkflowConfigsResponse:
            r"""Call the list workflow configs method over HTTP.

            Args:
                request (~.dataform.ListWorkflowConfigsRequest):
                    The request object. ``ListWorkflowConfigs`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ListWorkflowConfigsResponse:
                    ``ListWorkflowConfigs`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseListWorkflowConfigs._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_workflow_configs(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseListWorkflowConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseListWorkflowConfigs._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ListWorkflowConfigs",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListWorkflowConfigs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ListWorkflowConfigs._get_response(
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
            resp = dataform.ListWorkflowConfigsResponse()
            pb_resp = dataform.ListWorkflowConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_workflow_configs(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ListWorkflowConfigsResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.list_workflow_configs",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListWorkflowConfigs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListWorkflowInvocations(
        _BaseDataformRestTransport._BaseListWorkflowInvocations, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ListWorkflowInvocations")

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
            request: dataform.ListWorkflowInvocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ListWorkflowInvocationsResponse:
            r"""Call the list workflow invocations method over HTTP.

            Args:
                request (~.dataform.ListWorkflowInvocationsRequest):
                    The request object. ``ListWorkflowInvocations`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ListWorkflowInvocationsResponse:
                    ``ListWorkflowInvocations`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseListWorkflowInvocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_workflow_invocations(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseListWorkflowInvocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseListWorkflowInvocations._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ListWorkflowInvocations",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListWorkflowInvocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ListWorkflowInvocations._get_response(
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
            resp = dataform.ListWorkflowInvocationsResponse()
            pb_resp = dataform.ListWorkflowInvocationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_workflow_invocations(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ListWorkflowInvocationsResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.list_workflow_invocations",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListWorkflowInvocations",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListWorkspaces(
        _BaseDataformRestTransport._BaseListWorkspaces, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ListWorkspaces")

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
            request: dataform.ListWorkspacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ListWorkspacesResponse:
            r"""Call the list workspaces method over HTTP.

            Args:
                request (~.dataform.ListWorkspacesRequest):
                    The request object. ``ListWorkspaces`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ListWorkspacesResponse:
                    ``ListWorkspaces`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseListWorkspaces._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_workspaces(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseListWorkspaces._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseListWorkspaces._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ListWorkspaces",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListWorkspaces",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ListWorkspaces._get_response(
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
            resp = dataform.ListWorkspacesResponse()
            pb_resp = dataform.ListWorkspacesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_workspaces(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ListWorkspacesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.list_workspaces",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListWorkspaces",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _MakeDirectory(
        _BaseDataformRestTransport._BaseMakeDirectory, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.MakeDirectory")

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
            request: dataform.MakeDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.MakeDirectoryResponse:
            r"""Call the make directory method over HTTP.

            Args:
                request (~.dataform.MakeDirectoryRequest):
                    The request object. ``MakeDirectory`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.MakeDirectoryResponse:
                    ``MakeDirectory`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseMakeDirectory._get_http_options()
            )

            request, metadata = self._interceptor.pre_make_directory(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseMakeDirectory._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseDataformRestTransport._BaseMakeDirectory._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseMakeDirectory._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.MakeDirectory",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "MakeDirectory",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._MakeDirectory._get_response(
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
            resp = dataform.MakeDirectoryResponse()
            pb_resp = dataform.MakeDirectoryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_make_directory(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.MakeDirectoryResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.make_directory",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "MakeDirectory",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _MoveDirectory(
        _BaseDataformRestTransport._BaseMoveDirectory, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.MoveDirectory")

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
            request: dataform.MoveDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.MoveDirectoryResponse:
            r"""Call the move directory method over HTTP.

            Args:
                request (~.dataform.MoveDirectoryRequest):
                    The request object. ``MoveDirectory`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.MoveDirectoryResponse:
                    ``MoveDirectory`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseMoveDirectory._get_http_options()
            )

            request, metadata = self._interceptor.pre_move_directory(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseMoveDirectory._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseDataformRestTransport._BaseMoveDirectory._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseMoveDirectory._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.MoveDirectory",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "MoveDirectory",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._MoveDirectory._get_response(
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
            resp = dataform.MoveDirectoryResponse()
            pb_resp = dataform.MoveDirectoryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_move_directory(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.MoveDirectoryResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.move_directory",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "MoveDirectory",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _MoveFile(_BaseDataformRestTransport._BaseMoveFile, DataformRestStub):
        def __hash__(self):
            return hash("DataformRestTransport.MoveFile")

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
            request: dataform.MoveFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.MoveFileResponse:
            r"""Call the move file method over HTTP.

            Args:
                request (~.dataform.MoveFileRequest):
                    The request object. ``MoveFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.MoveFileResponse:
                    ``MoveFile`` response message.
            """

            http_options = _BaseDataformRestTransport._BaseMoveFile._get_http_options()

            request, metadata = self._interceptor.pre_move_file(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseMoveFile._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseDataformRestTransport._BaseMoveFile._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseMoveFile._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.MoveFile",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "MoveFile",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._MoveFile._get_response(
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
            resp = dataform.MoveFileResponse()
            pb_resp = dataform.MoveFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_move_file(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.MoveFileResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.move_file",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "MoveFile",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _PullGitCommits(
        _BaseDataformRestTransport._BasePullGitCommits, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.PullGitCommits")

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
            request: dataform.PullGitCommitsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the pull git commits method over HTTP.

            Args:
                request (~.dataform.PullGitCommitsRequest):
                    The request object. ``PullGitCommits`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BasePullGitCommits._get_http_options()
            )

            request, metadata = self._interceptor.pre_pull_git_commits(
                request, metadata
            )
            transcoded_request = (
                _BaseDataformRestTransport._BasePullGitCommits._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseDataformRestTransport._BasePullGitCommits._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BasePullGitCommits._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.PullGitCommits",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "PullGitCommits",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._PullGitCommits._get_response(
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

    class _PushGitCommits(
        _BaseDataformRestTransport._BasePushGitCommits, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.PushGitCommits")

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
            request: dataform.PushGitCommitsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the push git commits method over HTTP.

            Args:
                request (~.dataform.PushGitCommitsRequest):
                    The request object. ``PushGitCommits`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BasePushGitCommits._get_http_options()
            )

            request, metadata = self._interceptor.pre_push_git_commits(
                request, metadata
            )
            transcoded_request = (
                _BaseDataformRestTransport._BasePushGitCommits._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseDataformRestTransport._BasePushGitCommits._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BasePushGitCommits._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.PushGitCommits",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "PushGitCommits",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._PushGitCommits._get_response(
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

    class _QueryCompilationResultActions(
        _BaseDataformRestTransport._BaseQueryCompilationResultActions, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.QueryCompilationResultActions")

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
            request: dataform.QueryCompilationResultActionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.QueryCompilationResultActionsResponse:
            r"""Call the query compilation result
            actions method over HTTP.

                Args:
                    request (~.dataform.QueryCompilationResultActionsRequest):
                        The request object. ``QueryCompilationResultActions`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.dataform.QueryCompilationResultActionsResponse:
                        ``QueryCompilationResultActions`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseQueryCompilationResultActions._get_http_options()
            )

            request, metadata = self._interceptor.pre_query_compilation_result_actions(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseQueryCompilationResultActions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseQueryCompilationResultActions._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.QueryCompilationResultActions",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "QueryCompilationResultActions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                DataformRestTransport._QueryCompilationResultActions._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataform.QueryCompilationResultActionsResponse()
            pb_resp = dataform.QueryCompilationResultActionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_query_compilation_result_actions(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        dataform.QueryCompilationResultActionsResponse.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.query_compilation_result_actions",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "QueryCompilationResultActions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _QueryDirectoryContents(
        _BaseDataformRestTransport._BaseQueryDirectoryContents, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.QueryDirectoryContents")

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
            request: dataform.QueryDirectoryContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.QueryDirectoryContentsResponse:
            r"""Call the query directory contents method over HTTP.

            Args:
                request (~.dataform.QueryDirectoryContentsRequest):
                    The request object. ``QueryDirectoryContents`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.QueryDirectoryContentsResponse:
                    ``QueryDirectoryContents`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseQueryDirectoryContents._get_http_options()
            )

            request, metadata = self._interceptor.pre_query_directory_contents(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseQueryDirectoryContents._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseQueryDirectoryContents._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.QueryDirectoryContents",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "QueryDirectoryContents",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._QueryDirectoryContents._get_response(
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
            resp = dataform.QueryDirectoryContentsResponse()
            pb_resp = dataform.QueryDirectoryContentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_query_directory_contents(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.QueryDirectoryContentsResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.query_directory_contents",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "QueryDirectoryContents",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _QueryRepositoryDirectoryContents(
        _BaseDataformRestTransport._BaseQueryRepositoryDirectoryContents,
        DataformRestStub,
    ):
        def __hash__(self):
            return hash("DataformRestTransport.QueryRepositoryDirectoryContents")

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
            request: dataform.QueryRepositoryDirectoryContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.QueryRepositoryDirectoryContentsResponse:
            r"""Call the query repository
            directory contents method over HTTP.

                Args:
                    request (~.dataform.QueryRepositoryDirectoryContentsRequest):
                        The request object. ``QueryRepositoryDirectoryContents`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.dataform.QueryRepositoryDirectoryContentsResponse:
                        ``QueryRepositoryDirectoryContents`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseQueryRepositoryDirectoryContents._get_http_options()
            )

            (
                request,
                metadata,
            ) = self._interceptor.pre_query_repository_directory_contents(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseQueryRepositoryDirectoryContents._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseQueryRepositoryDirectoryContents._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.QueryRepositoryDirectoryContents",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "QueryRepositoryDirectoryContents",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                DataformRestTransport._QueryRepositoryDirectoryContents._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataform.QueryRepositoryDirectoryContentsResponse()
            pb_resp = dataform.QueryRepositoryDirectoryContentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_query_repository_directory_contents(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        dataform.QueryRepositoryDirectoryContentsResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.query_repository_directory_contents",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "QueryRepositoryDirectoryContents",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _QueryWorkflowInvocationActions(
        _BaseDataformRestTransport._BaseQueryWorkflowInvocationActions, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.QueryWorkflowInvocationActions")

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
            request: dataform.QueryWorkflowInvocationActionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.QueryWorkflowInvocationActionsResponse:
            r"""Call the query workflow invocation
            actions method over HTTP.

                Args:
                    request (~.dataform.QueryWorkflowInvocationActionsRequest):
                        The request object. ``QueryWorkflowInvocationActions`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.dataform.QueryWorkflowInvocationActionsResponse:
                        ``QueryWorkflowInvocationActions`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseQueryWorkflowInvocationActions._get_http_options()
            )

            request, metadata = self._interceptor.pre_query_workflow_invocation_actions(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseQueryWorkflowInvocationActions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseQueryWorkflowInvocationActions._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.QueryWorkflowInvocationActions",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "QueryWorkflowInvocationActions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                DataformRestTransport._QueryWorkflowInvocationActions._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = dataform.QueryWorkflowInvocationActionsResponse()
            pb_resp = dataform.QueryWorkflowInvocationActionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_query_workflow_invocation_actions(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        dataform.QueryWorkflowInvocationActionsResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.query_workflow_invocation_actions",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "QueryWorkflowInvocationActions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ReadFile(_BaseDataformRestTransport._BaseReadFile, DataformRestStub):
        def __hash__(self):
            return hash("DataformRestTransport.ReadFile")

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
            request: dataform.ReadFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ReadFileResponse:
            r"""Call the read file method over HTTP.

            Args:
                request (~.dataform.ReadFileRequest):
                    The request object. ``ReadFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ReadFileResponse:
                    ``ReadFile`` response message.
            """

            http_options = _BaseDataformRestTransport._BaseReadFile._get_http_options()

            request, metadata = self._interceptor.pre_read_file(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseReadFile._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseReadFile._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ReadFile",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ReadFile",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ReadFile._get_response(
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
            resp = dataform.ReadFileResponse()
            pb_resp = dataform.ReadFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_read_file(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ReadFileResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.read_file",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ReadFile",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ReadRepositoryFile(
        _BaseDataformRestTransport._BaseReadRepositoryFile, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ReadRepositoryFile")

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
            request: dataform.ReadRepositoryFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ReadRepositoryFileResponse:
            r"""Call the read repository file method over HTTP.

            Args:
                request (~.dataform.ReadRepositoryFileRequest):
                    The request object. ``ReadRepositoryFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ReadRepositoryFileResponse:
                    ``ReadRepositoryFile`` response message.
            """

            http_options = (
                _BaseDataformRestTransport._BaseReadRepositoryFile._get_http_options()
            )

            request, metadata = self._interceptor.pre_read_repository_file(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseReadRepositoryFile._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseReadRepositoryFile._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ReadRepositoryFile",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ReadRepositoryFile",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ReadRepositoryFile._get_response(
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
            resp = dataform.ReadRepositoryFileResponse()
            pb_resp = dataform.ReadRepositoryFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_read_repository_file(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ReadRepositoryFileResponse.to_json(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.read_repository_file",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ReadRepositoryFile",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RemoveDirectory(
        _BaseDataformRestTransport._BaseRemoveDirectory, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.RemoveDirectory")

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
            request: dataform.RemoveDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the remove directory method over HTTP.

            Args:
                request (~.dataform.RemoveDirectoryRequest):
                    The request object. ``RemoveDirectory`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseRemoveDirectory._get_http_options()
            )

            request, metadata = self._interceptor.pre_remove_directory(
                request, metadata
            )
            transcoded_request = (
                _BaseDataformRestTransport._BaseRemoveDirectory._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseDataformRestTransport._BaseRemoveDirectory._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseRemoveDirectory._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.RemoveDirectory",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "RemoveDirectory",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._RemoveDirectory._get_response(
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

    class _RemoveFile(_BaseDataformRestTransport._BaseRemoveFile, DataformRestStub):
        def __hash__(self):
            return hash("DataformRestTransport.RemoveFile")

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
            request: dataform.RemoveFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the remove file method over HTTP.

            Args:
                request (~.dataform.RemoveFileRequest):
                    The request object. ``RemoveFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseRemoveFile._get_http_options()
            )

            request, metadata = self._interceptor.pre_remove_file(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseRemoveFile._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseDataformRestTransport._BaseRemoveFile._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseRemoveFile._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.RemoveFile",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "RemoveFile",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._RemoveFile._get_response(
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

    class _ResetWorkspaceChanges(
        _BaseDataformRestTransport._BaseResetWorkspaceChanges, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ResetWorkspaceChanges")

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
            request: dataform.ResetWorkspaceChangesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the reset workspace changes method over HTTP.

            Args:
                request (~.dataform.ResetWorkspaceChangesRequest):
                    The request object. ``ResetWorkspaceChanges`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseDataformRestTransport._BaseResetWorkspaceChanges._get_http_options()
            )

            request, metadata = self._interceptor.pre_reset_workspace_changes(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseResetWorkspaceChanges._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseResetWorkspaceChanges._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseResetWorkspaceChanges._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ResetWorkspaceChanges",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ResetWorkspaceChanges",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ResetWorkspaceChanges._get_response(
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

    class _UpdateReleaseConfig(
        _BaseDataformRestTransport._BaseUpdateReleaseConfig, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.UpdateReleaseConfig")

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
            request: dataform.UpdateReleaseConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.ReleaseConfig:
            r"""Call the update release config method over HTTP.

            Args:
                request (~.dataform.UpdateReleaseConfigRequest):
                    The request object. ``UpdateReleaseConfig`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.ReleaseConfig:
                    Represents a Dataform release
                configuration.

            """

            http_options = (
                _BaseDataformRestTransport._BaseUpdateReleaseConfig._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_release_config(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseUpdateReleaseConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseUpdateReleaseConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseUpdateReleaseConfig._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.UpdateReleaseConfig",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "UpdateReleaseConfig",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._UpdateReleaseConfig._get_response(
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
            resp = dataform.ReleaseConfig()
            pb_resp = dataform.ReleaseConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_release_config(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.ReleaseConfig.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.update_release_config",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "UpdateReleaseConfig",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateRepository(
        _BaseDataformRestTransport._BaseUpdateRepository, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.UpdateRepository")

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
            request: dataform.UpdateRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.Repository:
            r"""Call the update repository method over HTTP.

            Args:
                request (~.dataform.UpdateRepositoryRequest):
                    The request object. ``UpdateRepository`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.Repository:
                    Represents a Dataform Git repository.
            """

            http_options = (
                _BaseDataformRestTransport._BaseUpdateRepository._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_repository(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseUpdateRepository._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseDataformRestTransport._BaseUpdateRepository._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseUpdateRepository._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.UpdateRepository",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "UpdateRepository",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._UpdateRepository._get_response(
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
            resp = dataform.Repository()
            pb_resp = dataform.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_repository(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.Repository.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.update_repository",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "UpdateRepository",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateWorkflowConfig(
        _BaseDataformRestTransport._BaseUpdateWorkflowConfig, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.UpdateWorkflowConfig")

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
            request: dataform.UpdateWorkflowConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.WorkflowConfig:
            r"""Call the update workflow config method over HTTP.

            Args:
                request (~.dataform.UpdateWorkflowConfigRequest):
                    The request object. ``UpdateWorkflowConfig`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.WorkflowConfig:
                    Represents a Dataform workflow
                configuration.

            """

            http_options = (
                _BaseDataformRestTransport._BaseUpdateWorkflowConfig._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_workflow_config(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseUpdateWorkflowConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseUpdateWorkflowConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseUpdateWorkflowConfig._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.UpdateWorkflowConfig",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "UpdateWorkflowConfig",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._UpdateWorkflowConfig._get_response(
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
            resp = dataform.WorkflowConfig()
            pb_resp = dataform.WorkflowConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_workflow_config(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.WorkflowConfig.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.update_workflow_config",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "UpdateWorkflowConfig",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _WriteFile(_BaseDataformRestTransport._BaseWriteFile, DataformRestStub):
        def __hash__(self):
            return hash("DataformRestTransport.WriteFile")

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
            request: dataform.WriteFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> dataform.WriteFileResponse:
            r"""Call the write file method over HTTP.

            Args:
                request (~.dataform.WriteFileRequest):
                    The request object. ``WriteFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.dataform.WriteFileResponse:
                    ``WriteFile`` response message.
            """

            http_options = _BaseDataformRestTransport._BaseWriteFile._get_http_options()

            request, metadata = self._interceptor.pre_write_file(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseWriteFile._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseDataformRestTransport._BaseWriteFile._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseWriteFile._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.WriteFile",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "WriteFile",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._WriteFile._get_response(
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
            resp = dataform.WriteFileResponse()
            pb_resp = dataform.WriteFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_write_file(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = dataform.WriteFileResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.dataform_v1beta1.DataformClient.write_file",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "WriteFile",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def cancel_workflow_invocation(
        self,
    ) -> Callable[[dataform.CancelWorkflowInvocationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelWorkflowInvocation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def commit_repository_changes(
        self,
    ) -> Callable[[dataform.CommitRepositoryChangesRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CommitRepositoryChanges(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def commit_workspace_changes(
        self,
    ) -> Callable[[dataform.CommitWorkspaceChangesRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CommitWorkspaceChanges(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def compute_repository_access_token_status(
        self,
    ) -> Callable[
        [dataform.ComputeRepositoryAccessTokenStatusRequest],
        dataform.ComputeRepositoryAccessTokenStatusResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ComputeRepositoryAccessTokenStatus(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_compilation_result(
        self,
    ) -> Callable[
        [dataform.CreateCompilationResultRequest], dataform.CompilationResult
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCompilationResult(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_release_config(
        self,
    ) -> Callable[[dataform.CreateReleaseConfigRequest], dataform.ReleaseConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReleaseConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_repository(
        self,
    ) -> Callable[[dataform.CreateRepositoryRequest], dataform.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_workflow_config(
        self,
    ) -> Callable[[dataform.CreateWorkflowConfigRequest], dataform.WorkflowConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkflowConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_workflow_invocation(
        self,
    ) -> Callable[
        [dataform.CreateWorkflowInvocationRequest], dataform.WorkflowInvocation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkflowInvocation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_workspace(
        self,
    ) -> Callable[[dataform.CreateWorkspaceRequest], dataform.Workspace]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkspace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_release_config(
        self,
    ) -> Callable[[dataform.DeleteReleaseConfigRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteReleaseConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_repository(
        self,
    ) -> Callable[[dataform.DeleteRepositoryRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_workflow_config(
        self,
    ) -> Callable[[dataform.DeleteWorkflowConfigRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkflowConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_workflow_invocation(
        self,
    ) -> Callable[[dataform.DeleteWorkflowInvocationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkflowInvocation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_workspace(
        self,
    ) -> Callable[[dataform.DeleteWorkspaceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkspace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_file_diff(
        self,
    ) -> Callable[[dataform.FetchFileDiffRequest], dataform.FetchFileDiffResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchFileDiff(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_file_git_statuses(
        self,
    ) -> Callable[
        [dataform.FetchFileGitStatusesRequest], dataform.FetchFileGitStatusesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchFileGitStatuses(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_git_ahead_behind(
        self,
    ) -> Callable[
        [dataform.FetchGitAheadBehindRequest], dataform.FetchGitAheadBehindResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchGitAheadBehind(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_remote_branches(
        self,
    ) -> Callable[
        [dataform.FetchRemoteBranchesRequest], dataform.FetchRemoteBranchesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchRemoteBranches(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_repository_history(
        self,
    ) -> Callable[
        [dataform.FetchRepositoryHistoryRequest],
        dataform.FetchRepositoryHistoryResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchRepositoryHistory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_compilation_result(
        self,
    ) -> Callable[[dataform.GetCompilationResultRequest], dataform.CompilationResult]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCompilationResult(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_release_config(
        self,
    ) -> Callable[[dataform.GetReleaseConfigRequest], dataform.ReleaseConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReleaseConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_repository(
        self,
    ) -> Callable[[dataform.GetRepositoryRequest], dataform.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workflow_config(
        self,
    ) -> Callable[[dataform.GetWorkflowConfigRequest], dataform.WorkflowConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkflowConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workflow_invocation(
        self,
    ) -> Callable[[dataform.GetWorkflowInvocationRequest], dataform.WorkflowInvocation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkflowInvocation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workspace(
        self,
    ) -> Callable[[dataform.GetWorkspaceRequest], dataform.Workspace]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkspace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def install_npm_packages(
        self,
    ) -> Callable[
        [dataform.InstallNpmPackagesRequest], dataform.InstallNpmPackagesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InstallNpmPackages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_compilation_results(
        self,
    ) -> Callable[
        [dataform.ListCompilationResultsRequest],
        dataform.ListCompilationResultsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCompilationResults(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_release_configs(
        self,
    ) -> Callable[
        [dataform.ListReleaseConfigsRequest], dataform.ListReleaseConfigsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReleaseConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_repositories(
        self,
    ) -> Callable[
        [dataform.ListRepositoriesRequest], dataform.ListRepositoriesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRepositories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workflow_configs(
        self,
    ) -> Callable[
        [dataform.ListWorkflowConfigsRequest], dataform.ListWorkflowConfigsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkflowConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workflow_invocations(
        self,
    ) -> Callable[
        [dataform.ListWorkflowInvocationsRequest],
        dataform.ListWorkflowInvocationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkflowInvocations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workspaces(
        self,
    ) -> Callable[[dataform.ListWorkspacesRequest], dataform.ListWorkspacesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkspaces(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def make_directory(
        self,
    ) -> Callable[[dataform.MakeDirectoryRequest], dataform.MakeDirectoryResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MakeDirectory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def move_directory(
        self,
    ) -> Callable[[dataform.MoveDirectoryRequest], dataform.MoveDirectoryResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MoveDirectory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def move_file(
        self,
    ) -> Callable[[dataform.MoveFileRequest], dataform.MoveFileResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MoveFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def pull_git_commits(
        self,
    ) -> Callable[[dataform.PullGitCommitsRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PullGitCommits(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def push_git_commits(
        self,
    ) -> Callable[[dataform.PushGitCommitsRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PushGitCommits(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query_compilation_result_actions(
        self,
    ) -> Callable[
        [dataform.QueryCompilationResultActionsRequest],
        dataform.QueryCompilationResultActionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._QueryCompilationResultActions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query_directory_contents(
        self,
    ) -> Callable[
        [dataform.QueryDirectoryContentsRequest],
        dataform.QueryDirectoryContentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._QueryDirectoryContents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query_repository_directory_contents(
        self,
    ) -> Callable[
        [dataform.QueryRepositoryDirectoryContentsRequest],
        dataform.QueryRepositoryDirectoryContentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._QueryRepositoryDirectoryContents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query_workflow_invocation_actions(
        self,
    ) -> Callable[
        [dataform.QueryWorkflowInvocationActionsRequest],
        dataform.QueryWorkflowInvocationActionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._QueryWorkflowInvocationActions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def read_file(
        self,
    ) -> Callable[[dataform.ReadFileRequest], dataform.ReadFileResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReadFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def read_repository_file(
        self,
    ) -> Callable[
        [dataform.ReadRepositoryFileRequest], dataform.ReadRepositoryFileResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReadRepositoryFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_directory(
        self,
    ) -> Callable[[dataform.RemoveDirectoryRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveDirectory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_file(self) -> Callable[[dataform.RemoveFileRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reset_workspace_changes(
        self,
    ) -> Callable[[dataform.ResetWorkspaceChangesRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResetWorkspaceChanges(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_release_config(
        self,
    ) -> Callable[[dataform.UpdateReleaseConfigRequest], dataform.ReleaseConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateReleaseConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_repository(
        self,
    ) -> Callable[[dataform.UpdateRepositoryRequest], dataform.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_workflow_config(
        self,
    ) -> Callable[[dataform.UpdateWorkflowConfigRequest], dataform.WorkflowConfig]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateWorkflowConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def write_file(
        self,
    ) -> Callable[[dataform.WriteFileRequest], dataform.WriteFileResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._WriteFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseDataformRestTransport._BaseGetLocation, DataformRestStub):
        def __hash__(self):
            return hash("DataformRestTransport.GetLocation")

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
                _BaseDataformRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseGetLocation._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._GetLocation._get_response(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
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
        _BaseDataformRestTransport._BaseListLocations, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.ListLocations")

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
                _BaseDataformRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseListLocations._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._ListLocations._get_response(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(_BaseDataformRestTransport._BaseGetIamPolicy, DataformRestStub):
        def __hash__(self):
            return hash("DataformRestTransport.GetIamPolicy")

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
                _BaseDataformRestTransport._BaseGetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseGetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseGetIamPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._GetIamPolicy._get_response(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformAsyncClient.GetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "GetIamPolicy",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(_BaseDataformRestTransport._BaseSetIamPolicy, DataformRestStub):
        def __hash__(self):
            return hash("DataformRestTransport.SetIamPolicy")

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
                _BaseDataformRestTransport._BaseSetIamPolicy._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = (
                _BaseDataformRestTransport._BaseSetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseDataformRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataformRestTransport._BaseSetIamPolicy._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "SetIamPolicy",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._SetIamPolicy._get_response(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformAsyncClient.SetIamPolicy",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
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
        _BaseDataformRestTransport._BaseTestIamPermissions, DataformRestStub
    ):
        def __hash__(self):
            return hash("DataformRestTransport.TestIamPermissions")

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
                _BaseDataformRestTransport._BaseTestIamPermissions._get_http_options()
            )

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseDataformRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataformRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataformRestTransport._BaseTestIamPermissions._get_query_params_json(
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
                    f"Sending request for google.cloud.dataform_v1beta1.DataformClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "TestIamPermissions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = DataformRestTransport._TestIamPermissions._get_response(
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
                    "Received response for google.cloud.dataform_v1beta1.DataformAsyncClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.dataform.v1beta1.Dataform",
                        "rpcName": "TestIamPermissions",
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


__all__ = ("DataformRestTransport",)
