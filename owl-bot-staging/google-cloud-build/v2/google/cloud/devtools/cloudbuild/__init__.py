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
from google.cloud.devtools.cloudbuild import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.devtools.cloudbuild_v2.services.repository_manager.client import RepositoryManagerClient
from google.cloud.devtools.cloudbuild_v2.services.repository_manager.async_client import RepositoryManagerAsyncClient

from google.cloud.devtools.cloudbuild_v2.types.cloudbuild import OperationMetadata
from google.cloud.devtools.cloudbuild_v2.types.cloudbuild import RunWorkflowCustomOperationMetadata
from google.cloud.devtools.cloudbuild_v2.types.repositories import BatchCreateRepositoriesRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import BatchCreateRepositoriesResponse
from google.cloud.devtools.cloudbuild_v2.types.repositories import Connection
from google.cloud.devtools.cloudbuild_v2.types.repositories import CreateConnectionRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import CreateRepositoryRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import DeleteConnectionRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import DeleteRepositoryRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import FetchGitRefsRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import FetchGitRefsResponse
from google.cloud.devtools.cloudbuild_v2.types.repositories import FetchLinkableRepositoriesRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import FetchLinkableRepositoriesResponse
from google.cloud.devtools.cloudbuild_v2.types.repositories import FetchReadTokenRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import FetchReadTokenResponse
from google.cloud.devtools.cloudbuild_v2.types.repositories import FetchReadWriteTokenRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import FetchReadWriteTokenResponse
from google.cloud.devtools.cloudbuild_v2.types.repositories import GetConnectionRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import GetRepositoryRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import GitHubConfig
from google.cloud.devtools.cloudbuild_v2.types.repositories import GitHubEnterpriseConfig
from google.cloud.devtools.cloudbuild_v2.types.repositories import GitLabConfig
from google.cloud.devtools.cloudbuild_v2.types.repositories import InstallationState
from google.cloud.devtools.cloudbuild_v2.types.repositories import ListConnectionsRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import ListConnectionsResponse
from google.cloud.devtools.cloudbuild_v2.types.repositories import ListRepositoriesRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import ListRepositoriesResponse
from google.cloud.devtools.cloudbuild_v2.types.repositories import OAuthCredential
from google.cloud.devtools.cloudbuild_v2.types.repositories import ProcessWebhookRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import Repository
from google.cloud.devtools.cloudbuild_v2.types.repositories import ServiceDirectoryConfig
from google.cloud.devtools.cloudbuild_v2.types.repositories import UpdateConnectionRequest
from google.cloud.devtools.cloudbuild_v2.types.repositories import UserCredential

__all__ = ('RepositoryManagerClient',
    'RepositoryManagerAsyncClient',
    'OperationMetadata',
    'RunWorkflowCustomOperationMetadata',
    'BatchCreateRepositoriesRequest',
    'BatchCreateRepositoriesResponse',
    'Connection',
    'CreateConnectionRequest',
    'CreateRepositoryRequest',
    'DeleteConnectionRequest',
    'DeleteRepositoryRequest',
    'FetchGitRefsRequest',
    'FetchGitRefsResponse',
    'FetchLinkableRepositoriesRequest',
    'FetchLinkableRepositoriesResponse',
    'FetchReadTokenRequest',
    'FetchReadTokenResponse',
    'FetchReadWriteTokenRequest',
    'FetchReadWriteTokenResponse',
    'GetConnectionRequest',
    'GetRepositoryRequest',
    'GitHubConfig',
    'GitHubEnterpriseConfig',
    'GitLabConfig',
    'InstallationState',
    'ListConnectionsRequest',
    'ListConnectionsResponse',
    'ListRepositoriesRequest',
    'ListRepositoriesResponse',
    'OAuthCredential',
    'ProcessWebhookRequest',
    'Repository',
    'ServiceDirectoryConfig',
    'UpdateConnectionRequest',
    'UserCredential',
)
