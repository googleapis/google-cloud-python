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
from google.cloud.securesourcemanager_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.secure_source_manager import SecureSourceManagerClient
from .services.secure_source_manager import SecureSourceManagerAsyncClient

from .types.secure_source_manager import BatchCreatePullRequestCommentsRequest
from .types.secure_source_manager import BatchCreatePullRequestCommentsResponse
from .types.secure_source_manager import BranchRule
from .types.secure_source_manager import CloseIssueRequest
from .types.secure_source_manager import ClosePullRequestRequest
from .types.secure_source_manager import CreateBranchRuleRequest
from .types.secure_source_manager import CreateHookRequest
from .types.secure_source_manager import CreateInstanceRequest
from .types.secure_source_manager import CreateIssueCommentRequest
from .types.secure_source_manager import CreateIssueRequest
from .types.secure_source_manager import CreatePullRequestCommentRequest
from .types.secure_source_manager import CreatePullRequestRequest
from .types.secure_source_manager import CreateRepositoryRequest
from .types.secure_source_manager import DeleteBranchRuleRequest
from .types.secure_source_manager import DeleteHookRequest
from .types.secure_source_manager import DeleteInstanceRequest
from .types.secure_source_manager import DeleteIssueCommentRequest
from .types.secure_source_manager import DeleteIssueRequest
from .types.secure_source_manager import DeletePullRequestCommentRequest
from .types.secure_source_manager import DeleteRepositoryRequest
from .types.secure_source_manager import FetchBlobRequest
from .types.secure_source_manager import FetchBlobResponse
from .types.secure_source_manager import FetchTreeRequest
from .types.secure_source_manager import FetchTreeResponse
from .types.secure_source_manager import FileDiff
from .types.secure_source_manager import GetBranchRuleRequest
from .types.secure_source_manager import GetHookRequest
from .types.secure_source_manager import GetInstanceRequest
from .types.secure_source_manager import GetIssueCommentRequest
from .types.secure_source_manager import GetIssueRequest
from .types.secure_source_manager import GetPullRequestCommentRequest
from .types.secure_source_manager import GetPullRequestRequest
from .types.secure_source_manager import GetRepositoryRequest
from .types.secure_source_manager import Hook
from .types.secure_source_manager import Instance
from .types.secure_source_manager import Issue
from .types.secure_source_manager import IssueComment
from .types.secure_source_manager import ListBranchRulesRequest
from .types.secure_source_manager import ListBranchRulesResponse
from .types.secure_source_manager import ListHooksRequest
from .types.secure_source_manager import ListHooksResponse
from .types.secure_source_manager import ListInstancesRequest
from .types.secure_source_manager import ListInstancesResponse
from .types.secure_source_manager import ListIssueCommentsRequest
from .types.secure_source_manager import ListIssueCommentsResponse
from .types.secure_source_manager import ListIssuesRequest
from .types.secure_source_manager import ListIssuesResponse
from .types.secure_source_manager import ListPullRequestCommentsRequest
from .types.secure_source_manager import ListPullRequestCommentsResponse
from .types.secure_source_manager import ListPullRequestFileDiffsRequest
from .types.secure_source_manager import ListPullRequestFileDiffsResponse
from .types.secure_source_manager import ListPullRequestsRequest
from .types.secure_source_manager import ListPullRequestsResponse
from .types.secure_source_manager import ListRepositoriesRequest
from .types.secure_source_manager import ListRepositoriesResponse
from .types.secure_source_manager import MergePullRequestRequest
from .types.secure_source_manager import OpenIssueRequest
from .types.secure_source_manager import OpenPullRequestRequest
from .types.secure_source_manager import OperationMetadata
from .types.secure_source_manager import PullRequest
from .types.secure_source_manager import PullRequestComment
from .types.secure_source_manager import Repository
from .types.secure_source_manager import ResolvePullRequestCommentsRequest
from .types.secure_source_manager import ResolvePullRequestCommentsResponse
from .types.secure_source_manager import TreeEntry
from .types.secure_source_manager import UnresolvePullRequestCommentsRequest
from .types.secure_source_manager import UnresolvePullRequestCommentsResponse
from .types.secure_source_manager import UpdateBranchRuleRequest
from .types.secure_source_manager import UpdateHookRequest
from .types.secure_source_manager import UpdateIssueCommentRequest
from .types.secure_source_manager import UpdateIssueRequest
from .types.secure_source_manager import UpdatePullRequestCommentRequest
from .types.secure_source_manager import UpdatePullRequestRequest
from .types.secure_source_manager import UpdateRepositoryRequest

__all__ = (
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
'SecureSourceManagerClient',
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
