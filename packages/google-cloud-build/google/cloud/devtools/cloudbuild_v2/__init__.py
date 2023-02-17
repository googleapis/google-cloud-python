# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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


from .services.repository_manager import RepositoryManagerClient
from .services.repository_manager import RepositoryManagerAsyncClient

from .types.cloudbuild import OperationMetadata
from .types.cloudbuild import RunWorkflowCustomOperationMetadata
from .types.repositories import BatchCreateRepositoriesRequest
from .types.repositories import BatchCreateRepositoriesResponse
from .types.repositories import Connection
from .types.repositories import CreateConnectionRequest
from .types.repositories import CreateRepositoryRequest
from .types.repositories import DeleteConnectionRequest
from .types.repositories import DeleteRepositoryRequest
from .types.repositories import FetchLinkableRepositoriesRequest
from .types.repositories import FetchLinkableRepositoriesResponse
from .types.repositories import FetchReadTokenRequest
from .types.repositories import FetchReadTokenResponse
from .types.repositories import FetchReadWriteTokenRequest
from .types.repositories import FetchReadWriteTokenResponse
from .types.repositories import GetConnectionRequest
from .types.repositories import GetRepositoryRequest
from .types.repositories import GitHubConfig
from .types.repositories import GitHubEnterpriseConfig
from .types.repositories import InstallationState
from .types.repositories import ListConnectionsRequest
from .types.repositories import ListConnectionsResponse
from .types.repositories import ListRepositoriesRequest
from .types.repositories import ListRepositoriesResponse
from .types.repositories import OAuthCredential
from .types.repositories import Repository
from .types.repositories import ServiceDirectoryConfig
from .types.repositories import UpdateConnectionRequest

__all__ = (
    "RepositoryManagerAsyncClient",
    "BatchCreateRepositoriesRequest",
    "BatchCreateRepositoriesResponse",
    "Connection",
    "CreateConnectionRequest",
    "CreateRepositoryRequest",
    "DeleteConnectionRequest",
    "DeleteRepositoryRequest",
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
    "InstallationState",
    "ListConnectionsRequest",
    "ListConnectionsResponse",
    "ListRepositoriesRequest",
    "ListRepositoriesResponse",
    "OAuthCredential",
    "OperationMetadata",
    "Repository",
    "RepositoryManagerClient",
    "RunWorkflowCustomOperationMetadata",
    "ServiceDirectoryConfig",
    "UpdateConnectionRequest",
)
