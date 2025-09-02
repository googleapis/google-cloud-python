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
from google.cloud.securesourcemanager import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.securesourcemanager_v1.services.secure_source_manager.client import SecureSourceManagerClient
from google.cloud.securesourcemanager_v1.services.secure_source_manager.async_client import SecureSourceManagerAsyncClient

from google.cloud.securesourcemanager_v1.types.secure_source_manager import BatchCreatePullRequestCommentsRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import BatchCreatePullRequestCommentsResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import BranchRule
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CloseIssueRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ClosePullRequestRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CreateBranchRuleRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CreateHookRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CreateInstanceRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CreateIssueCommentRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CreateIssueRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CreatePullRequestCommentRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CreatePullRequestRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import CreateRepositoryRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import DeleteBranchRuleRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import DeleteHookRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import DeleteInstanceRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import DeleteIssueCommentRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import DeleteIssueRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import DeletePullRequestCommentRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import DeleteRepositoryRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import FetchBlobRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import FetchBlobResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import FetchTreeRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import FetchTreeResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import FileDiff
from google.cloud.securesourcemanager_v1.types.secure_source_manager import GetBranchRuleRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import GetHookRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import GetInstanceRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import GetIssueCommentRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import GetIssueRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import GetPullRequestCommentRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import GetPullRequestRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import GetRepositoryRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import Hook
from google.cloud.securesourcemanager_v1.types.secure_source_manager import Instance
from google.cloud.securesourcemanager_v1.types.secure_source_manager import Issue
from google.cloud.securesourcemanager_v1.types.secure_source_manager import IssueComment
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListBranchRulesRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListBranchRulesResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListHooksRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListHooksResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListInstancesRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListInstancesResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListIssueCommentsRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListIssueCommentsResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListIssuesRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListIssuesResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListPullRequestCommentsRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListPullRequestCommentsResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListPullRequestFileDiffsRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListPullRequestFileDiffsResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListPullRequestsRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListPullRequestsResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListRepositoriesRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ListRepositoriesResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import MergePullRequestRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import OpenIssueRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import OpenPullRequestRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import OperationMetadata
from google.cloud.securesourcemanager_v1.types.secure_source_manager import PullRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import PullRequestComment
from google.cloud.securesourcemanager_v1.types.secure_source_manager import Repository
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ResolvePullRequestCommentsRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import ResolvePullRequestCommentsResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import TreeEntry
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UnresolvePullRequestCommentsRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UnresolvePullRequestCommentsResponse
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UpdateBranchRuleRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UpdateHookRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UpdateIssueCommentRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UpdateIssueRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UpdatePullRequestCommentRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UpdatePullRequestRequest
from google.cloud.securesourcemanager_v1.types.secure_source_manager import UpdateRepositoryRequest

__all__ = ('SecureSourceManagerClient',
    'SecureSourceManagerAsyncClient',
    'BatchCreatePullRequestCommentsRequest',
    'BatchCreatePullRequestCommentsResponse',
    'BranchRule',
    'CloseIssueRequest',
    'ClosePullRequestRequest',
    'CreateBranchRuleRequest',
    'CreateHookRequest',
    'CreateInstanceRequest',
    'CreateIssueCommentRequest',
    'CreateIssueRequest',
    'CreatePullRequestCommentRequest',
    'CreatePullRequestRequest',
    'CreateRepositoryRequest',
    'DeleteBranchRuleRequest',
    'DeleteHookRequest',
    'DeleteInstanceRequest',
    'DeleteIssueCommentRequest',
    'DeleteIssueRequest',
    'DeletePullRequestCommentRequest',
    'DeleteRepositoryRequest',
    'FetchBlobRequest',
    'FetchBlobResponse',
    'FetchTreeRequest',
    'FetchTreeResponse',
    'FileDiff',
    'GetBranchRuleRequest',
    'GetHookRequest',
    'GetInstanceRequest',
    'GetIssueCommentRequest',
    'GetIssueRequest',
    'GetPullRequestCommentRequest',
    'GetPullRequestRequest',
    'GetRepositoryRequest',
    'Hook',
    'Instance',
    'Issue',
    'IssueComment',
    'ListBranchRulesRequest',
    'ListBranchRulesResponse',
    'ListHooksRequest',
    'ListHooksResponse',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'ListIssueCommentsRequest',
    'ListIssueCommentsResponse',
    'ListIssuesRequest',
    'ListIssuesResponse',
    'ListPullRequestCommentsRequest',
    'ListPullRequestCommentsResponse',
    'ListPullRequestFileDiffsRequest',
    'ListPullRequestFileDiffsResponse',
    'ListPullRequestsRequest',
    'ListPullRequestsResponse',
    'ListRepositoriesRequest',
    'ListRepositoriesResponse',
    'MergePullRequestRequest',
    'OpenIssueRequest',
    'OpenPullRequestRequest',
    'OperationMetadata',
    'PullRequest',
    'PullRequestComment',
    'Repository',
    'ResolvePullRequestCommentsRequest',
    'ResolvePullRequestCommentsResponse',
    'TreeEntry',
    'UnresolvePullRequestCommentsRequest',
    'UnresolvePullRequestCommentsResponse',
    'UpdateBranchRuleRequest',
    'UpdateHookRequest',
    'UpdateIssueCommentRequest',
    'UpdateIssueRequest',
    'UpdatePullRequestCommentRequest',
    'UpdatePullRequestRequest',
    'UpdateRepositoryRequest',
)
