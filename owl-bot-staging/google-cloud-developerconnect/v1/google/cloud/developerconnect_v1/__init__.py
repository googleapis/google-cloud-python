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
from google.cloud.developerconnect_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.developer_connect import DeveloperConnectClient
from .services.developer_connect import DeveloperConnectAsyncClient

from .types.developer_connect import Connection
from .types.developer_connect import CreateConnectionRequest
from .types.developer_connect import CreateGitRepositoryLinkRequest
from .types.developer_connect import DeleteConnectionRequest
from .types.developer_connect import DeleteGitRepositoryLinkRequest
from .types.developer_connect import FetchGitHubInstallationsRequest
from .types.developer_connect import FetchGitHubInstallationsResponse
from .types.developer_connect import FetchGitRefsRequest
from .types.developer_connect import FetchGitRefsResponse
from .types.developer_connect import FetchLinkableGitRepositoriesRequest
from .types.developer_connect import FetchLinkableGitRepositoriesResponse
from .types.developer_connect import FetchReadTokenRequest
from .types.developer_connect import FetchReadTokenResponse
from .types.developer_connect import FetchReadWriteTokenRequest
from .types.developer_connect import FetchReadWriteTokenResponse
from .types.developer_connect import GetConnectionRequest
from .types.developer_connect import GetGitRepositoryLinkRequest
from .types.developer_connect import GitHubConfig
from .types.developer_connect import GitRepositoryLink
from .types.developer_connect import InstallationState
from .types.developer_connect import LinkableGitRepository
from .types.developer_connect import ListConnectionsRequest
from .types.developer_connect import ListConnectionsResponse
from .types.developer_connect import ListGitRepositoryLinksRequest
from .types.developer_connect import ListGitRepositoryLinksResponse
from .types.developer_connect import OAuthCredential
from .types.developer_connect import OperationMetadata
from .types.developer_connect import UpdateConnectionRequest

__all__ = (
    'DeveloperConnectAsyncClient',
'Connection',
'CreateConnectionRequest',
'CreateGitRepositoryLinkRequest',
'DeleteConnectionRequest',
'DeleteGitRepositoryLinkRequest',
'DeveloperConnectClient',
'FetchGitHubInstallationsRequest',
'FetchGitHubInstallationsResponse',
'FetchGitRefsRequest',
'FetchGitRefsResponse',
'FetchLinkableGitRepositoriesRequest',
'FetchLinkableGitRepositoriesResponse',
'FetchReadTokenRequest',
'FetchReadTokenResponse',
'FetchReadWriteTokenRequest',
'FetchReadWriteTokenResponse',
'GetConnectionRequest',
'GetGitRepositoryLinkRequest',
'GitHubConfig',
'GitRepositoryLink',
'InstallationState',
'LinkableGitRepository',
'ListConnectionsRequest',
'ListConnectionsResponse',
'ListGitRepositoryLinksRequest',
'ListGitRepositoryLinksResponse',
'OAuthCredential',
'OperationMetadata',
'UpdateConnectionRequest',
)
