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
from google.cloud.devtools.cloudbuild_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.repository_manager import (
    RepositoryManagerAsyncClient,
    RepositoryManagerClient,
)
from .types.cloudbuild import OperationMetadata, RunWorkflowCustomOperationMetadata
from .types.repositories import (
    BatchCreateRepositoriesRequest,
    BatchCreateRepositoriesResponse,
    BitbucketCloudConfig,
    BitbucketDataCenterConfig,
    Connection,
    CreateConnectionRequest,
    CreateRepositoryRequest,
    DeleteConnectionRequest,
    DeleteRepositoryRequest,
    FetchGitRefsRequest,
    FetchGitRefsResponse,
    FetchLinkableRepositoriesRequest,
    FetchLinkableRepositoriesResponse,
    FetchReadTokenRequest,
    FetchReadTokenResponse,
    FetchReadWriteTokenRequest,
    FetchReadWriteTokenResponse,
    GetConnectionRequest,
    GetRepositoryRequest,
    GitHubConfig,
    GitHubEnterpriseConfig,
    GitLabConfig,
    InstallationState,
    ListConnectionsRequest,
    ListConnectionsResponse,
    ListRepositoriesRequest,
    ListRepositoriesResponse,
    OAuthCredential,
    ProcessWebhookRequest,
    Repository,
    ServiceDirectoryConfig,
    UpdateConnectionRequest,
    UserCredential,
)

__all__ = (
    "RepositoryManagerAsyncClient",
    "BatchCreateRepositoriesRequest",
    "BatchCreateRepositoriesResponse",
    "BitbucketCloudConfig",
    "BitbucketDataCenterConfig",
    "Connection",
    "CreateConnectionRequest",
    "CreateRepositoryRequest",
    "DeleteConnectionRequest",
    "DeleteRepositoryRequest",
    "FetchGitRefsRequest",
    "FetchGitRefsResponse",
    "FetchLinkableRepositoriesRequest",
    "FetchLinkableRepositoriesResponse",
    "FetchReadTokenRequest",
    "FetchReadTokenResponse",
    "FetchReadWriteTokenRequest",
    "FetchReadWriteTokenResponse",
    "GetConnectionRequest",
    "GetRepositoryRequest",
    "GitHubConfig",
    "GitHubEnterpriseConfig",
    "GitLabConfig",
    "InstallationState",
    "ListConnectionsRequest",
    "ListConnectionsResponse",
    "ListRepositoriesRequest",
    "ListRepositoriesResponse",
    "OAuthCredential",
    "OperationMetadata",
    "ProcessWebhookRequest",
    "Repository",
    "RepositoryManagerClient",
    "RunWorkflowCustomOperationMetadata",
    "ServiceDirectoryConfig",
    "UpdateConnectionRequest",
    "UserCredential",
)
