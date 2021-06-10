# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.resourcemanager_v3.services.folders.client import FoldersClient
from google.cloud.resourcemanager_v3.services.folders.async_client import (
    FoldersAsyncClient,
)
from google.cloud.resourcemanager_v3.services.organizations.client import (
    OrganizationsClient,
)
from google.cloud.resourcemanager_v3.services.organizations.async_client import (
    OrganizationsAsyncClient,
)
from google.cloud.resourcemanager_v3.services.projects.client import ProjectsClient
from google.cloud.resourcemanager_v3.services.projects.async_client import (
    ProjectsAsyncClient,
)
from google.cloud.resourcemanager_v3.services.tag_bindings.client import (
    TagBindingsClient,
)
from google.cloud.resourcemanager_v3.services.tag_bindings.async_client import (
    TagBindingsAsyncClient,
)
from google.cloud.resourcemanager_v3.services.tag_keys.client import TagKeysClient
from google.cloud.resourcemanager_v3.services.tag_keys.async_client import (
    TagKeysAsyncClient,
)
from google.cloud.resourcemanager_v3.services.tag_values.client import TagValuesClient
from google.cloud.resourcemanager_v3.services.tag_values.async_client import (
    TagValuesAsyncClient,
)

from google.cloud.resourcemanager_v3.types.folders import CreateFolderMetadata
from google.cloud.resourcemanager_v3.types.folders import CreateFolderRequest
from google.cloud.resourcemanager_v3.types.folders import DeleteFolderMetadata
from google.cloud.resourcemanager_v3.types.folders import DeleteFolderRequest
from google.cloud.resourcemanager_v3.types.folders import Folder
from google.cloud.resourcemanager_v3.types.folders import GetFolderRequest
from google.cloud.resourcemanager_v3.types.folders import ListFoldersRequest
from google.cloud.resourcemanager_v3.types.folders import ListFoldersResponse
from google.cloud.resourcemanager_v3.types.folders import MoveFolderMetadata
from google.cloud.resourcemanager_v3.types.folders import MoveFolderRequest
from google.cloud.resourcemanager_v3.types.folders import SearchFoldersRequest
from google.cloud.resourcemanager_v3.types.folders import SearchFoldersResponse
from google.cloud.resourcemanager_v3.types.folders import UndeleteFolderMetadata
from google.cloud.resourcemanager_v3.types.folders import UndeleteFolderRequest
from google.cloud.resourcemanager_v3.types.folders import UpdateFolderMetadata
from google.cloud.resourcemanager_v3.types.folders import UpdateFolderRequest
from google.cloud.resourcemanager_v3.types.organizations import (
    DeleteOrganizationMetadata,
)
from google.cloud.resourcemanager_v3.types.organizations import GetOrganizationRequest
from google.cloud.resourcemanager_v3.types.organizations import Organization
from google.cloud.resourcemanager_v3.types.organizations import (
    SearchOrganizationsRequest,
)
from google.cloud.resourcemanager_v3.types.organizations import (
    SearchOrganizationsResponse,
)
from google.cloud.resourcemanager_v3.types.organizations import (
    UndeleteOrganizationMetadata,
)
from google.cloud.resourcemanager_v3.types.projects import CreateProjectMetadata
from google.cloud.resourcemanager_v3.types.projects import CreateProjectRequest
from google.cloud.resourcemanager_v3.types.projects import DeleteProjectMetadata
from google.cloud.resourcemanager_v3.types.projects import DeleteProjectRequest
from google.cloud.resourcemanager_v3.types.projects import GetProjectRequest
from google.cloud.resourcemanager_v3.types.projects import ListProjectsRequest
from google.cloud.resourcemanager_v3.types.projects import ListProjectsResponse
from google.cloud.resourcemanager_v3.types.projects import MoveProjectMetadata
from google.cloud.resourcemanager_v3.types.projects import MoveProjectRequest
from google.cloud.resourcemanager_v3.types.projects import Project
from google.cloud.resourcemanager_v3.types.projects import SearchProjectsRequest
from google.cloud.resourcemanager_v3.types.projects import SearchProjectsResponse
from google.cloud.resourcemanager_v3.types.projects import UndeleteProjectMetadata
from google.cloud.resourcemanager_v3.types.projects import UndeleteProjectRequest
from google.cloud.resourcemanager_v3.types.projects import UpdateProjectMetadata
from google.cloud.resourcemanager_v3.types.projects import UpdateProjectRequest
from google.cloud.resourcemanager_v3.types.tag_bindings import CreateTagBindingMetadata
from google.cloud.resourcemanager_v3.types.tag_bindings import CreateTagBindingRequest
from google.cloud.resourcemanager_v3.types.tag_bindings import DeleteTagBindingMetadata
from google.cloud.resourcemanager_v3.types.tag_bindings import DeleteTagBindingRequest
from google.cloud.resourcemanager_v3.types.tag_bindings import ListTagBindingsRequest
from google.cloud.resourcemanager_v3.types.tag_bindings import ListTagBindingsResponse
from google.cloud.resourcemanager_v3.types.tag_bindings import TagBinding
from google.cloud.resourcemanager_v3.types.tag_keys import CreateTagKeyMetadata
from google.cloud.resourcemanager_v3.types.tag_keys import CreateTagKeyRequest
from google.cloud.resourcemanager_v3.types.tag_keys import DeleteTagKeyMetadata
from google.cloud.resourcemanager_v3.types.tag_keys import DeleteTagKeyRequest
from google.cloud.resourcemanager_v3.types.tag_keys import GetTagKeyRequest
from google.cloud.resourcemanager_v3.types.tag_keys import ListTagKeysRequest
from google.cloud.resourcemanager_v3.types.tag_keys import ListTagKeysResponse
from google.cloud.resourcemanager_v3.types.tag_keys import TagKey
from google.cloud.resourcemanager_v3.types.tag_keys import UpdateTagKeyMetadata
from google.cloud.resourcemanager_v3.types.tag_keys import UpdateTagKeyRequest
from google.cloud.resourcemanager_v3.types.tag_values import CreateTagValueMetadata
from google.cloud.resourcemanager_v3.types.tag_values import CreateTagValueRequest
from google.cloud.resourcemanager_v3.types.tag_values import DeleteTagValueMetadata
from google.cloud.resourcemanager_v3.types.tag_values import DeleteTagValueRequest
from google.cloud.resourcemanager_v3.types.tag_values import GetTagValueRequest
from google.cloud.resourcemanager_v3.types.tag_values import ListTagValuesRequest
from google.cloud.resourcemanager_v3.types.tag_values import ListTagValuesResponse
from google.cloud.resourcemanager_v3.types.tag_values import TagValue
from google.cloud.resourcemanager_v3.types.tag_values import UpdateTagValueMetadata
from google.cloud.resourcemanager_v3.types.tag_values import UpdateTagValueRequest

__all__ = (
    "FoldersClient",
    "FoldersAsyncClient",
    "OrganizationsClient",
    "OrganizationsAsyncClient",
    "ProjectsClient",
    "ProjectsAsyncClient",
    "TagBindingsClient",
    "TagBindingsAsyncClient",
    "TagKeysClient",
    "TagKeysAsyncClient",
    "TagValuesClient",
    "TagValuesAsyncClient",
    "CreateFolderMetadata",
    "CreateFolderRequest",
    "DeleteFolderMetadata",
    "DeleteFolderRequest",
    "Folder",
    "GetFolderRequest",
    "ListFoldersRequest",
    "ListFoldersResponse",
    "MoveFolderMetadata",
    "MoveFolderRequest",
    "SearchFoldersRequest",
    "SearchFoldersResponse",
    "UndeleteFolderMetadata",
    "UndeleteFolderRequest",
    "UpdateFolderMetadata",
    "UpdateFolderRequest",
    "DeleteOrganizationMetadata",
    "GetOrganizationRequest",
    "Organization",
    "SearchOrganizationsRequest",
    "SearchOrganizationsResponse",
    "UndeleteOrganizationMetadata",
    "CreateProjectMetadata",
    "CreateProjectRequest",
    "DeleteProjectMetadata",
    "DeleteProjectRequest",
    "GetProjectRequest",
    "ListProjectsRequest",
    "ListProjectsResponse",
    "MoveProjectMetadata",
    "MoveProjectRequest",
    "Project",
    "SearchProjectsRequest",
    "SearchProjectsResponse",
    "UndeleteProjectMetadata",
    "UndeleteProjectRequest",
    "UpdateProjectMetadata",
    "UpdateProjectRequest",
    "CreateTagBindingMetadata",
    "CreateTagBindingRequest",
    "DeleteTagBindingMetadata",
    "DeleteTagBindingRequest",
    "ListTagBindingsRequest",
    "ListTagBindingsResponse",
    "TagBinding",
    "CreateTagKeyMetadata",
    "CreateTagKeyRequest",
    "DeleteTagKeyMetadata",
    "DeleteTagKeyRequest",
    "GetTagKeyRequest",
    "ListTagKeysRequest",
    "ListTagKeysResponse",
    "TagKey",
    "UpdateTagKeyMetadata",
    "UpdateTagKeyRequest",
    "CreateTagValueMetadata",
    "CreateTagValueRequest",
    "DeleteTagValueMetadata",
    "DeleteTagValueRequest",
    "GetTagValueRequest",
    "ListTagValuesRequest",
    "ListTagValuesResponse",
    "TagValue",
    "UpdateTagValueMetadata",
    "UpdateTagValueRequest",
)
