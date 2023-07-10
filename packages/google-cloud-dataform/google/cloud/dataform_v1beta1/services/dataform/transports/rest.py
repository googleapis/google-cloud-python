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
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.dataform_v1beta1.types import dataform

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import DataformTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
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

            def pre_commit_workspace_changes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_create_compilation_result(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_compilation_result(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_repository(self, response):
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

            def pre_delete_repository(self, request, metadata):
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

            def pre_get_compilation_result(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_compilation_result(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_repository(self, response):
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

            def pre_list_repositories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_repositories(self, response):
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

            def pre_remove_directory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_remove_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_reset_workspace_changes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_update_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_repository(self, response):
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.CancelWorkflowInvocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_workflow_invocation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_commit_workspace_changes(
        self,
        request: dataform.CommitWorkspaceChangesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.CommitWorkspaceChangesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for commit_workspace_changes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_create_compilation_result(
        self,
        request: dataform.CreateCompilationResultRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.CreateCompilationResultRequest, Sequence[Tuple[str, str]]]:
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

    def pre_create_repository(
        self,
        request: dataform.CreateRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.CreateRepositoryRequest, Sequence[Tuple[str, str]]]:
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

    def pre_create_workflow_invocation(
        self,
        request: dataform.CreateWorkflowInvocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.CreateWorkflowInvocationRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.CreateWorkspaceRequest, Sequence[Tuple[str, str]]]:
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

    def pre_delete_repository(
        self,
        request: dataform.DeleteRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.DeleteRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_delete_workflow_invocation(
        self,
        request: dataform.DeleteWorkflowInvocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.DeleteWorkflowInvocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_workflow_invocation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_delete_workspace(
        self,
        request: dataform.DeleteWorkspaceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.DeleteWorkspaceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_workspace

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_fetch_file_diff(
        self,
        request: dataform.FetchFileDiffRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.FetchFileDiffRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.FetchFileGitStatusesRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.FetchGitAheadBehindRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.FetchRemoteBranchesRequest, Sequence[Tuple[str, str]]]:
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

    def pre_get_compilation_result(
        self,
        request: dataform.GetCompilationResultRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.GetCompilationResultRequest, Sequence[Tuple[str, str]]]:
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

    def pre_get_repository(
        self,
        request: dataform.GetRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.GetRepositoryRequest, Sequence[Tuple[str, str]]]:
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

    def pre_get_workflow_invocation(
        self,
        request: dataform.GetWorkflowInvocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.GetWorkflowInvocationRequest, Sequence[Tuple[str, str]]]:
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
        self, request: dataform.GetWorkspaceRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[dataform.GetWorkspaceRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.InstallNpmPackagesRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.ListCompilationResultsRequest, Sequence[Tuple[str, str]]]:
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

    def pre_list_repositories(
        self,
        request: dataform.ListRepositoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.ListRepositoriesRequest, Sequence[Tuple[str, str]]]:
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

    def pre_list_workflow_invocations(
        self,
        request: dataform.ListWorkflowInvocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.ListWorkflowInvocationsRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.ListWorkspacesRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.MakeDirectoryRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.MoveDirectoryRequest, Sequence[Tuple[str, str]]]:
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
        self, request: dataform.MoveFileRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[dataform.MoveFileRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.PullGitCommitsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for pull_git_commits

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_push_git_commits(
        self,
        request: dataform.PushGitCommitsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.PushGitCommitsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for push_git_commits

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_query_compilation_result_actions(
        self,
        request: dataform.QueryCompilationResultActionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        dataform.QueryCompilationResultActionsRequest, Sequence[Tuple[str, str]]
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.QueryDirectoryContentsRequest, Sequence[Tuple[str, str]]]:
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

    def pre_query_workflow_invocation_actions(
        self,
        request: dataform.QueryWorkflowInvocationActionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        dataform.QueryWorkflowInvocationActionsRequest, Sequence[Tuple[str, str]]
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
        self, request: dataform.ReadFileRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[dataform.ReadFileRequest, Sequence[Tuple[str, str]]]:
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

    def pre_remove_directory(
        self,
        request: dataform.RemoveDirectoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.RemoveDirectoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_directory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_remove_file(
        self, request: dataform.RemoveFileRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[dataform.RemoveFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_reset_workspace_changes(
        self,
        request: dataform.ResetWorkspaceChangesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.ResetWorkspaceChangesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for reset_workspace_changes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Dataform server.
        """
        return request, metadata

    def pre_update_repository(
        self,
        request: dataform.UpdateRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[dataform.UpdateRepositoryRequest, Sequence[Tuple[str, str]]]:
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

    def pre_write_file(
        self, request: dataform.WriteFileRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[dataform.WriteFileRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
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
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
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


@dataclasses.dataclass
class DataformRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DataformRestInterceptor


class DataformRestTransport(DataformTransport):
    """REST backend transport for Dataform.

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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or DataformRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CancelWorkflowInvocation(DataformRestStub):
        def __hash__(self):
            return hash("CancelWorkflowInvocation")

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
            request: dataform.CancelWorkflowInvocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the cancel workflow
            invocation method over HTTP.

                Args:
                    request (~.dataform.CancelWorkflowInvocationRequest):
                        The request object. ``CancelWorkflowInvocation`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workflowInvocations/*}:cancel",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_cancel_workflow_invocation(
                request, metadata
            )
            pb_request = dataform.CancelWorkflowInvocationRequest.pb(request)
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

    class _CommitWorkspaceChanges(DataformRestStub):
        def __hash__(self):
            return hash("CommitWorkspaceChanges")

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
            request: dataform.CommitWorkspaceChangesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the commit workspace changes method over HTTP.

            Args:
                request (~.dataform.CommitWorkspaceChangesRequest):
                    The request object. ``CommitWorkspaceChanges`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}:commit",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_commit_workspace_changes(
                request, metadata
            )
            pb_request = dataform.CommitWorkspaceChangesRequest.pb(request)
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

    class _CreateCompilationResult(DataformRestStub):
        def __hash__(self):
            return hash("CreateCompilationResult")

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
            request: dataform.CreateCompilationResultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.CompilationResult:
            r"""Call the create compilation result method over HTTP.

            Args:
                request (~.dataform.CreateCompilationResultRequest):
                    The request object. ``CreateCompilationResult`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.CompilationResult:
                    Represents the result of compiling a
                Dataform project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{parent=projects/*/locations/*/repositories/*}/compilationResults",
                    "body": "compilation_result",
                },
            ]
            request, metadata = self._interceptor.pre_create_compilation_result(
                request, metadata
            )
            pb_request = dataform.CreateCompilationResultRequest.pb(request)
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
            resp = dataform.CompilationResult()
            pb_resp = dataform.CompilationResult.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_compilation_result(resp)
            return resp

    class _CreateRepository(DataformRestStub):
        def __hash__(self):
            return hash("CreateRepository")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "repositoryId": "",
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
            request: dataform.CreateRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.Repository:
            r"""Call the create repository method over HTTP.

            Args:
                request (~.dataform.CreateRepositoryRequest):
                    The request object. ``CreateRepository`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.Repository:
                    Represents a Dataform Git repository.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{parent=projects/*/locations/*}/repositories",
                    "body": "repository",
                },
            ]
            request, metadata = self._interceptor.pre_create_repository(
                request, metadata
            )
            pb_request = dataform.CreateRepositoryRequest.pb(request)
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
            resp = dataform.Repository()
            pb_resp = dataform.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_repository(resp)
            return resp

    class _CreateWorkflowInvocation(DataformRestStub):
        def __hash__(self):
            return hash("CreateWorkflowInvocation")

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
            request: dataform.CreateWorkflowInvocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.WorkflowInvocation:
            r"""Call the create workflow
            invocation method over HTTP.

                Args:
                    request (~.dataform.CreateWorkflowInvocationRequest):
                        The request object. ``CreateWorkflowInvocation`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.dataform.WorkflowInvocation:
                        Represents a single invocation of a
                    compilation result.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{parent=projects/*/locations/*/repositories/*}/workflowInvocations",
                    "body": "workflow_invocation",
                },
            ]
            request, metadata = self._interceptor.pre_create_workflow_invocation(
                request, metadata
            )
            pb_request = dataform.CreateWorkflowInvocationRequest.pb(request)
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
            resp = dataform.WorkflowInvocation()
            pb_resp = dataform.WorkflowInvocation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_workflow_invocation(resp)
            return resp

    class _CreateWorkspace(DataformRestStub):
        def __hash__(self):
            return hash("CreateWorkspace")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "workspaceId": "",
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
            request: dataform.CreateWorkspaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.Workspace:
            r"""Call the create workspace method over HTTP.

            Args:
                request (~.dataform.CreateWorkspaceRequest):
                    The request object. ``CreateWorkspace`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.Workspace:
                    Represents a Dataform Git workspace.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{parent=projects/*/locations/*/repositories/*}/workspaces",
                    "body": "workspace",
                },
            ]
            request, metadata = self._interceptor.pre_create_workspace(
                request, metadata
            )
            pb_request = dataform.CreateWorkspaceRequest.pb(request)
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
            resp = dataform.Workspace()
            pb_resp = dataform.Workspace.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_workspace(resp)
            return resp

    class _DeleteRepository(DataformRestStub):
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
            request: dataform.DeleteRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete repository method over HTTP.

            Args:
                request (~.dataform.DeleteRepositoryRequest):
                    The request object. ``DeleteRepository`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_repository(
                request, metadata
            )
            pb_request = dataform.DeleteRepositoryRequest.pb(request)
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

    class _DeleteWorkflowInvocation(DataformRestStub):
        def __hash__(self):
            return hash("DeleteWorkflowInvocation")

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
            request: dataform.DeleteWorkflowInvocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete workflow
            invocation method over HTTP.

                Args:
                    request (~.dataform.DeleteWorkflowInvocationRequest):
                        The request object. ``DeleteWorkflowInvocation`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workflowInvocations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_workflow_invocation(
                request, metadata
            )
            pb_request = dataform.DeleteWorkflowInvocationRequest.pb(request)
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

    class _DeleteWorkspace(DataformRestStub):
        def __hash__(self):
            return hash("DeleteWorkspace")

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
            request: dataform.DeleteWorkspaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete workspace method over HTTP.

            Args:
                request (~.dataform.DeleteWorkspaceRequest):
                    The request object. ``DeleteWorkspace`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_workspace(
                request, metadata
            )
            pb_request = dataform.DeleteWorkspaceRequest.pb(request)
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

    class _FetchFileDiff(DataformRestStub):
        def __hash__(self):
            return hash("FetchFileDiff")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "path": "",
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
            request: dataform.FetchFileDiffRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.FetchFileDiffResponse:
            r"""Call the fetch file diff method over HTTP.

            Args:
                request (~.dataform.FetchFileDiffRequest):
                    The request object. ``FetchFileDiff`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.FetchFileDiffResponse:
                    ``FetchFileDiff`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:fetchFileDiff",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_file_diff(request, metadata)
            pb_request = dataform.FetchFileDiffRequest.pb(request)
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
            resp = dataform.FetchFileDiffResponse()
            pb_resp = dataform.FetchFileDiffResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_file_diff(resp)
            return resp

    class _FetchFileGitStatuses(DataformRestStub):
        def __hash__(self):
            return hash("FetchFileGitStatuses")

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
            request: dataform.FetchFileGitStatusesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.FetchFileGitStatusesResponse:
            r"""Call the fetch file git statuses method over HTTP.

            Args:
                request (~.dataform.FetchFileGitStatusesRequest):
                    The request object. ``FetchFileGitStatuses`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.FetchFileGitStatusesResponse:
                    ``FetchFileGitStatuses`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}:fetchFileGitStatuses",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_file_git_statuses(
                request, metadata
            )
            pb_request = dataform.FetchFileGitStatusesRequest.pb(request)
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
            resp = dataform.FetchFileGitStatusesResponse()
            pb_resp = dataform.FetchFileGitStatusesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_file_git_statuses(resp)
            return resp

    class _FetchGitAheadBehind(DataformRestStub):
        def __hash__(self):
            return hash("FetchGitAheadBehind")

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
            request: dataform.FetchGitAheadBehindRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.FetchGitAheadBehindResponse:
            r"""Call the fetch git ahead behind method over HTTP.

            Args:
                request (~.dataform.FetchGitAheadBehindRequest):
                    The request object. ``FetchGitAheadBehind`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.FetchGitAheadBehindResponse:
                    ``FetchGitAheadBehind`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}:fetchGitAheadBehind",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_git_ahead_behind(
                request, metadata
            )
            pb_request = dataform.FetchGitAheadBehindRequest.pb(request)
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
            resp = dataform.FetchGitAheadBehindResponse()
            pb_resp = dataform.FetchGitAheadBehindResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_git_ahead_behind(resp)
            return resp

    class _FetchRemoteBranches(DataformRestStub):
        def __hash__(self):
            return hash("FetchRemoteBranches")

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
            request: dataform.FetchRemoteBranchesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.FetchRemoteBranchesResponse:
            r"""Call the fetch remote branches method over HTTP.

            Args:
                request (~.dataform.FetchRemoteBranchesRequest):
                    The request object. ``FetchRemoteBranches`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.FetchRemoteBranchesResponse:
                    ``FetchRemoteBranches`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*}:fetchRemoteBranches",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_remote_branches(
                request, metadata
            )
            pb_request = dataform.FetchRemoteBranchesRequest.pb(request)
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
            resp = dataform.FetchRemoteBranchesResponse()
            pb_resp = dataform.FetchRemoteBranchesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_remote_branches(resp)
            return resp

    class _GetCompilationResult(DataformRestStub):
        def __hash__(self):
            return hash("GetCompilationResult")

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
            request: dataform.GetCompilationResultRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.CompilationResult:
            r"""Call the get compilation result method over HTTP.

            Args:
                request (~.dataform.GetCompilationResultRequest):
                    The request object. ``GetCompilationResult`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.CompilationResult:
                    Represents the result of compiling a
                Dataform project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/compilationResults/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_compilation_result(
                request, metadata
            )
            pb_request = dataform.GetCompilationResultRequest.pb(request)
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
            resp = dataform.CompilationResult()
            pb_resp = dataform.CompilationResult.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_compilation_result(resp)
            return resp

    class _GetRepository(DataformRestStub):
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
            request: dataform.GetRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.Repository:
            r"""Call the get repository method over HTTP.

            Args:
                request (~.dataform.GetRepositoryRequest):
                    The request object. ``GetRepository`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.Repository:
                    Represents a Dataform Git repository.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_repository(request, metadata)
            pb_request = dataform.GetRepositoryRequest.pb(request)
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
            resp = dataform.Repository()
            pb_resp = dataform.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_repository(resp)
            return resp

    class _GetWorkflowInvocation(DataformRestStub):
        def __hash__(self):
            return hash("GetWorkflowInvocation")

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
            request: dataform.GetWorkflowInvocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.WorkflowInvocation:
            r"""Call the get workflow invocation method over HTTP.

            Args:
                request (~.dataform.GetWorkflowInvocationRequest):
                    The request object. ``GetWorkflowInvocation`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.WorkflowInvocation:
                    Represents a single invocation of a
                compilation result.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workflowInvocations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_workflow_invocation(
                request, metadata
            )
            pb_request = dataform.GetWorkflowInvocationRequest.pb(request)
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
            resp = dataform.WorkflowInvocation()
            pb_resp = dataform.WorkflowInvocation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_workflow_invocation(resp)
            return resp

    class _GetWorkspace(DataformRestStub):
        def __hash__(self):
            return hash("GetWorkspace")

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
            request: dataform.GetWorkspaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.Workspace:
            r"""Call the get workspace method over HTTP.

            Args:
                request (~.dataform.GetWorkspaceRequest):
                    The request object. ``GetWorkspace`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.Workspace:
                    Represents a Dataform Git workspace.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_workspace(request, metadata)
            pb_request = dataform.GetWorkspaceRequest.pb(request)
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
            resp = dataform.Workspace()
            pb_resp = dataform.Workspace.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_workspace(resp)
            return resp

    class _InstallNpmPackages(DataformRestStub):
        def __hash__(self):
            return hash("InstallNpmPackages")

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
            request: dataform.InstallNpmPackagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.InstallNpmPackagesResponse:
            r"""Call the install npm packages method over HTTP.

            Args:
                request (~.dataform.InstallNpmPackagesRequest):
                    The request object. ``InstallNpmPackages`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.InstallNpmPackagesResponse:
                    ``InstallNpmPackages`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:installNpmPackages",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_install_npm_packages(
                request, metadata
            )
            pb_request = dataform.InstallNpmPackagesRequest.pb(request)
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
            resp = dataform.InstallNpmPackagesResponse()
            pb_resp = dataform.InstallNpmPackagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_install_npm_packages(resp)
            return resp

    class _ListCompilationResults(DataformRestStub):
        def __hash__(self):
            return hash("ListCompilationResults")

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
            request: dataform.ListCompilationResultsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.ListCompilationResultsResponse:
            r"""Call the list compilation results method over HTTP.

            Args:
                request (~.dataform.ListCompilationResultsRequest):
                    The request object. ``ListCompilationResults`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.ListCompilationResultsResponse:
                    ``ListCompilationResults`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=projects/*/locations/*/repositories/*}/compilationResults",
                },
            ]
            request, metadata = self._interceptor.pre_list_compilation_results(
                request, metadata
            )
            pb_request = dataform.ListCompilationResultsRequest.pb(request)
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
            resp = dataform.ListCompilationResultsResponse()
            pb_resp = dataform.ListCompilationResultsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_compilation_results(resp)
            return resp

    class _ListRepositories(DataformRestStub):
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
            request: dataform.ListRepositoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.ListRepositoriesResponse:
            r"""Call the list repositories method over HTTP.

            Args:
                request (~.dataform.ListRepositoriesRequest):
                    The request object. ``ListRepositories`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.ListRepositoriesResponse:
                    ``ListRepositories`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=projects/*/locations/*}/repositories",
                },
            ]
            request, metadata = self._interceptor.pre_list_repositories(
                request, metadata
            )
            pb_request = dataform.ListRepositoriesRequest.pb(request)
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
            resp = dataform.ListRepositoriesResponse()
            pb_resp = dataform.ListRepositoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_repositories(resp)
            return resp

    class _ListWorkflowInvocations(DataformRestStub):
        def __hash__(self):
            return hash("ListWorkflowInvocations")

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
            request: dataform.ListWorkflowInvocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.ListWorkflowInvocationsResponse:
            r"""Call the list workflow invocations method over HTTP.

            Args:
                request (~.dataform.ListWorkflowInvocationsRequest):
                    The request object. ``ListWorkflowInvocations`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.ListWorkflowInvocationsResponse:
                    ``ListWorkflowInvocations`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=projects/*/locations/*/repositories/*}/workflowInvocations",
                },
            ]
            request, metadata = self._interceptor.pre_list_workflow_invocations(
                request, metadata
            )
            pb_request = dataform.ListWorkflowInvocationsRequest.pb(request)
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
            resp = dataform.ListWorkflowInvocationsResponse()
            pb_resp = dataform.ListWorkflowInvocationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_workflow_invocations(resp)
            return resp

    class _ListWorkspaces(DataformRestStub):
        def __hash__(self):
            return hash("ListWorkspaces")

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
            request: dataform.ListWorkspacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.ListWorkspacesResponse:
            r"""Call the list workspaces method over HTTP.

            Args:
                request (~.dataform.ListWorkspacesRequest):
                    The request object. ``ListWorkspaces`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.ListWorkspacesResponse:
                    ``ListWorkspaces`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{parent=projects/*/locations/*/repositories/*}/workspaces",
                },
            ]
            request, metadata = self._interceptor.pre_list_workspaces(request, metadata)
            pb_request = dataform.ListWorkspacesRequest.pb(request)
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
            resp = dataform.ListWorkspacesResponse()
            pb_resp = dataform.ListWorkspacesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_workspaces(resp)
            return resp

    class _MakeDirectory(DataformRestStub):
        def __hash__(self):
            return hash("MakeDirectory")

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
            request: dataform.MakeDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.MakeDirectoryResponse:
            r"""Call the make directory method over HTTP.

            Args:
                request (~.dataform.MakeDirectoryRequest):
                    The request object. ``MakeDirectory`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.MakeDirectoryResponse:
                    ``MakeDirectory`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:makeDirectory",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_make_directory(request, metadata)
            pb_request = dataform.MakeDirectoryRequest.pb(request)
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
            resp = dataform.MakeDirectoryResponse()
            pb_resp = dataform.MakeDirectoryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_make_directory(resp)
            return resp

    class _MoveDirectory(DataformRestStub):
        def __hash__(self):
            return hash("MoveDirectory")

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
            request: dataform.MoveDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.MoveDirectoryResponse:
            r"""Call the move directory method over HTTP.

            Args:
                request (~.dataform.MoveDirectoryRequest):
                    The request object. ``MoveDirectory`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.MoveDirectoryResponse:
                    ``MoveDirectory`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:moveDirectory",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_move_directory(request, metadata)
            pb_request = dataform.MoveDirectoryRequest.pb(request)
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
            resp = dataform.MoveDirectoryResponse()
            pb_resp = dataform.MoveDirectoryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_move_directory(resp)
            return resp

    class _MoveFile(DataformRestStub):
        def __hash__(self):
            return hash("MoveFile")

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
            request: dataform.MoveFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.MoveFileResponse:
            r"""Call the move file method over HTTP.

            Args:
                request (~.dataform.MoveFileRequest):
                    The request object. ``MoveFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.MoveFileResponse:
                    ``MoveFile`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:moveFile",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_move_file(request, metadata)
            pb_request = dataform.MoveFileRequest.pb(request)
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
            resp = dataform.MoveFileResponse()
            pb_resp = dataform.MoveFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_move_file(resp)
            return resp

    class _PullGitCommits(DataformRestStub):
        def __hash__(self):
            return hash("PullGitCommits")

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
            request: dataform.PullGitCommitsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the pull git commits method over HTTP.

            Args:
                request (~.dataform.PullGitCommitsRequest):
                    The request object. ``PullGitCommits`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}:pull",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_pull_git_commits(
                request, metadata
            )
            pb_request = dataform.PullGitCommitsRequest.pb(request)
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

    class _PushGitCommits(DataformRestStub):
        def __hash__(self):
            return hash("PushGitCommits")

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
            request: dataform.PushGitCommitsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the push git commits method over HTTP.

            Args:
                request (~.dataform.PushGitCommitsRequest):
                    The request object. ``PushGitCommits`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}:push",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_push_git_commits(
                request, metadata
            )
            pb_request = dataform.PushGitCommitsRequest.pb(request)
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

    class _QueryCompilationResultActions(DataformRestStub):
        def __hash__(self):
            return hash("QueryCompilationResultActions")

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
            request: dataform.QueryCompilationResultActionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.QueryCompilationResultActionsResponse:
            r"""Call the query compilation result
            actions method over HTTP.

                Args:
                    request (~.dataform.QueryCompilationResultActionsRequest):
                        The request object. ``QueryCompilationResultActions`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.dataform.QueryCompilationResultActionsResponse:
                        ``QueryCompilationResultActions`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/compilationResults/*}:query",
                },
            ]
            request, metadata = self._interceptor.pre_query_compilation_result_actions(
                request, metadata
            )
            pb_request = dataform.QueryCompilationResultActionsRequest.pb(request)
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
            resp = dataform.QueryCompilationResultActionsResponse()
            pb_resp = dataform.QueryCompilationResultActionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_query_compilation_result_actions(resp)
            return resp

    class _QueryDirectoryContents(DataformRestStub):
        def __hash__(self):
            return hash("QueryDirectoryContents")

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
            request: dataform.QueryDirectoryContentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.QueryDirectoryContentsResponse:
            r"""Call the query directory contents method over HTTP.

            Args:
                request (~.dataform.QueryDirectoryContentsRequest):
                    The request object. ``QueryDirectoryContents`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.QueryDirectoryContentsResponse:
                    ``QueryDirectoryContents`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:queryDirectoryContents",
                },
            ]
            request, metadata = self._interceptor.pre_query_directory_contents(
                request, metadata
            )
            pb_request = dataform.QueryDirectoryContentsRequest.pb(request)
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
            resp = dataform.QueryDirectoryContentsResponse()
            pb_resp = dataform.QueryDirectoryContentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_query_directory_contents(resp)
            return resp

    class _QueryWorkflowInvocationActions(DataformRestStub):
        def __hash__(self):
            return hash("QueryWorkflowInvocationActions")

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
            request: dataform.QueryWorkflowInvocationActionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.QueryWorkflowInvocationActionsResponse:
            r"""Call the query workflow invocation
            actions method over HTTP.

                Args:
                    request (~.dataform.QueryWorkflowInvocationActionsRequest):
                        The request object. ``QueryWorkflowInvocationActions`` request message.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.dataform.QueryWorkflowInvocationActionsResponse:
                        ``QueryWorkflowInvocationActions`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workflowInvocations/*}:query",
                },
            ]
            request, metadata = self._interceptor.pre_query_workflow_invocation_actions(
                request, metadata
            )
            pb_request = dataform.QueryWorkflowInvocationActionsRequest.pb(request)
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
            resp = dataform.QueryWorkflowInvocationActionsResponse()
            pb_resp = dataform.QueryWorkflowInvocationActionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_query_workflow_invocation_actions(resp)
            return resp

    class _ReadFile(DataformRestStub):
        def __hash__(self):
            return hash("ReadFile")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "path": "",
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
            request: dataform.ReadFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.ReadFileResponse:
            r"""Call the read file method over HTTP.

            Args:
                request (~.dataform.ReadFileRequest):
                    The request object. ``ReadFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.ReadFileResponse:
                    ``ReadFile`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:readFile",
                },
            ]
            request, metadata = self._interceptor.pre_read_file(request, metadata)
            pb_request = dataform.ReadFileRequest.pb(request)
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
            resp = dataform.ReadFileResponse()
            pb_resp = dataform.ReadFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_read_file(resp)
            return resp

    class _RemoveDirectory(DataformRestStub):
        def __hash__(self):
            return hash("RemoveDirectory")

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
            request: dataform.RemoveDirectoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the remove directory method over HTTP.

            Args:
                request (~.dataform.RemoveDirectoryRequest):
                    The request object. ``RemoveDirectory`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:removeDirectory",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_remove_directory(
                request, metadata
            )
            pb_request = dataform.RemoveDirectoryRequest.pb(request)
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

    class _RemoveFile(DataformRestStub):
        def __hash__(self):
            return hash("RemoveFile")

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
            request: dataform.RemoveFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the remove file method over HTTP.

            Args:
                request (~.dataform.RemoveFileRequest):
                    The request object. ``RemoveFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:removeFile",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_remove_file(request, metadata)
            pb_request = dataform.RemoveFileRequest.pb(request)
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

    class _ResetWorkspaceChanges(DataformRestStub):
        def __hash__(self):
            return hash("ResetWorkspaceChanges")

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
            request: dataform.ResetWorkspaceChangesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the reset workspace changes method over HTTP.

            Args:
                request (~.dataform.ResetWorkspaceChangesRequest):
                    The request object. ``ResetWorkspaceChanges`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}:reset",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_reset_workspace_changes(
                request, metadata
            )
            pb_request = dataform.ResetWorkspaceChangesRequest.pb(request)
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

    class _UpdateRepository(DataformRestStub):
        def __hash__(self):
            return hash("UpdateRepository")

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
            request: dataform.UpdateRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.Repository:
            r"""Call the update repository method over HTTP.

            Args:
                request (~.dataform.UpdateRepositoryRequest):
                    The request object. ``UpdateRepository`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.Repository:
                    Represents a Dataform Git repository.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta1/{repository.name=projects/*/locations/*/repositories/*}",
                    "body": "repository",
                },
            ]
            request, metadata = self._interceptor.pre_update_repository(
                request, metadata
            )
            pb_request = dataform.UpdateRepositoryRequest.pb(request)
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
            resp = dataform.Repository()
            pb_resp = dataform.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_repository(resp)
            return resp

    class _WriteFile(DataformRestStub):
        def __hash__(self):
            return hash("WriteFile")

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
            request: dataform.WriteFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> dataform.WriteFileResponse:
            r"""Call the write file method over HTTP.

            Args:
                request (~.dataform.WriteFileRequest):
                    The request object. ``WriteFile`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.dataform.WriteFileResponse:
                    ``WriteFile`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{workspace=projects/*/locations/*/repositories/*/workspaces/*}:writeFile",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_write_file(request, metadata)
            pb_request = dataform.WriteFileRequest.pb(request)
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
            resp = dataform.WriteFileResponse()
            pb_resp = dataform.WriteFileResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_write_file(resp)
            return resp

    @property
    def cancel_workflow_invocation(
        self,
    ) -> Callable[[dataform.CancelWorkflowInvocationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelWorkflowInvocation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def commit_workspace_changes(
        self,
    ) -> Callable[[dataform.CommitWorkspaceChangesRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CommitWorkspaceChanges(self._session, self._host, self._interceptor)  # type: ignore

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
    def create_repository(
        self,
    ) -> Callable[[dataform.CreateRepositoryRequest], dataform.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRepository(self._session, self._host, self._interceptor)  # type: ignore

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
    def delete_repository(
        self,
    ) -> Callable[[dataform.DeleteRepositoryRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRepository(self._session, self._host, self._interceptor)  # type: ignore

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
    def get_compilation_result(
        self,
    ) -> Callable[[dataform.GetCompilationResultRequest], dataform.CompilationResult]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCompilationResult(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_repository(
        self,
    ) -> Callable[[dataform.GetRepositoryRequest], dataform.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRepository(self._session, self._host, self._interceptor)  # type: ignore

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
    def list_repositories(
        self,
    ) -> Callable[
        [dataform.ListRepositoriesRequest], dataform.ListRepositoriesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRepositories(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_repository(
        self,
    ) -> Callable[[dataform.UpdateRepositoryRequest], dataform.Repository]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRepository(self._session, self._host, self._interceptor)  # type: ignore

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

    class _GetLocation(DataformRestStub):
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
                    "uri": "/v1beta1/{name=projects/*/locations/*}",
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

    class _ListLocations(DataformRestStub):
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
                    "uri": "/v1beta1/{name=projects/*}/locations",
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DataformRestTransport",)
