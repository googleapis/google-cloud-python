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

from .services.folders import FoldersAsyncClient, FoldersClient
from .services.organizations import OrganizationsAsyncClient, OrganizationsClient
from .services.projects import ProjectsAsyncClient, ProjectsClient
from .services.tag_bindings import TagBindingsAsyncClient, TagBindingsClient
from .services.tag_keys import TagKeysAsyncClient, TagKeysClient
from .services.tag_values import TagValuesAsyncClient, TagValuesClient
from .types.folders import (
    CreateFolderMetadata,
    CreateFolderRequest,
    DeleteFolderMetadata,
    DeleteFolderRequest,
    Folder,
    GetFolderRequest,
    ListFoldersRequest,
    ListFoldersResponse,
    MoveFolderMetadata,
    MoveFolderRequest,
    SearchFoldersRequest,
    SearchFoldersResponse,
    UndeleteFolderMetadata,
    UndeleteFolderRequest,
    UpdateFolderMetadata,
    UpdateFolderRequest,
)
from .types.organizations import (
    DeleteOrganizationMetadata,
    GetOrganizationRequest,
    Organization,
    SearchOrganizationsRequest,
    SearchOrganizationsResponse,
    UndeleteOrganizationMetadata,
)
from .types.projects import (
    CreateProjectMetadata,
    CreateProjectRequest,
    DeleteProjectMetadata,
    DeleteProjectRequest,
    GetProjectRequest,
    ListProjectsRequest,
    ListProjectsResponse,
    MoveProjectMetadata,
    MoveProjectRequest,
    Project,
    SearchProjectsRequest,
    SearchProjectsResponse,
    UndeleteProjectMetadata,
    UndeleteProjectRequest,
    UpdateProjectMetadata,
    UpdateProjectRequest,
)
from .types.tag_bindings import (
    CreateTagBindingMetadata,
    CreateTagBindingRequest,
    DeleteTagBindingMetadata,
    DeleteTagBindingRequest,
    ListTagBindingsRequest,
    ListTagBindingsResponse,
    TagBinding,
)
from .types.tag_keys import (
    CreateTagKeyMetadata,
    CreateTagKeyRequest,
    DeleteTagKeyMetadata,
    DeleteTagKeyRequest,
    GetTagKeyRequest,
    ListTagKeysRequest,
    ListTagKeysResponse,
    TagKey,
    UpdateTagKeyMetadata,
    UpdateTagKeyRequest,
)
from .types.tag_values import (
    CreateTagValueMetadata,
    CreateTagValueRequest,
    DeleteTagValueMetadata,
    DeleteTagValueRequest,
    GetTagValueRequest,
    ListTagValuesRequest,
    ListTagValuesResponse,
    TagValue,
    UpdateTagValueMetadata,
    UpdateTagValueRequest,
)

__all__ = (
    "FoldersAsyncClient",
    "OrganizationsAsyncClient",
    "ProjectsAsyncClient",
    "TagBindingsAsyncClient",
    "TagKeysAsyncClient",
    "TagValuesAsyncClient",
    "CreateFolderMetadata",
    "CreateFolderRequest",
    "CreateProjectMetadata",
    "CreateProjectRequest",
    "CreateTagBindingMetadata",
    "CreateTagBindingRequest",
    "CreateTagKeyMetadata",
    "CreateTagKeyRequest",
    "CreateTagValueMetadata",
    "CreateTagValueRequest",
    "DeleteFolderMetadata",
    "DeleteFolderRequest",
    "DeleteOrganizationMetadata",
    "DeleteProjectMetadata",
    "DeleteProjectRequest",
    "DeleteTagBindingMetadata",
    "DeleteTagBindingRequest",
    "DeleteTagKeyMetadata",
    "DeleteTagKeyRequest",
    "DeleteTagValueMetadata",
    "DeleteTagValueRequest",
    "Folder",
    "FoldersClient",
    "GetFolderRequest",
    "GetOrganizationRequest",
    "GetProjectRequest",
    "GetTagKeyRequest",
    "GetTagValueRequest",
    "ListFoldersRequest",
    "ListFoldersResponse",
    "ListProjectsRequest",
    "ListProjectsResponse",
    "ListTagBindingsRequest",
    "ListTagBindingsResponse",
    "ListTagKeysRequest",
    "ListTagKeysResponse",
    "ListTagValuesRequest",
    "ListTagValuesResponse",
    "MoveFolderMetadata",
    "MoveFolderRequest",
    "MoveProjectMetadata",
    "MoveProjectRequest",
    "Organization",
    "OrganizationsClient",
    "Project",
    "ProjectsClient",
    "SearchFoldersRequest",
    "SearchFoldersResponse",
    "SearchOrganizationsRequest",
    "SearchOrganizationsResponse",
    "SearchProjectsRequest",
    "SearchProjectsResponse",
    "TagBinding",
    "TagBindingsClient",
    "TagKey",
    "TagKeysClient",
    "TagValue",
    "TagValuesClient",
    "UndeleteFolderMetadata",
    "UndeleteFolderRequest",
    "UndeleteOrganizationMetadata",
    "UndeleteProjectMetadata",
    "UndeleteProjectRequest",
    "UpdateFolderMetadata",
    "UpdateFolderRequest",
    "UpdateProjectMetadata",
    "UpdateProjectRequest",
    "UpdateTagKeyMetadata",
    "UpdateTagKeyRequest",
    "UpdateTagValueMetadata",
    "UpdateTagValueRequest",
)
