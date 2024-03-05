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
from google.cloud.securesourcemanager import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.securesourcemanager_v1.services.secure_source_manager.async_client import (
    SecureSourceManagerAsyncClient,
)
from google.cloud.securesourcemanager_v1.services.secure_source_manager.client import (
    SecureSourceManagerClient,
)
from google.cloud.securesourcemanager_v1.types.secure_source_manager import (
    CreateInstanceRequest,
    CreateRepositoryRequest,
    DeleteInstanceRequest,
    DeleteRepositoryRequest,
    GetInstanceRequest,
    GetRepositoryRequest,
    Instance,
    ListInstancesRequest,
    ListInstancesResponse,
    ListRepositoriesRequest,
    ListRepositoriesResponse,
    OperationMetadata,
    Repository,
)

__all__ = (
    "SecureSourceManagerClient",
    "SecureSourceManagerAsyncClient",
    "CreateInstanceRequest",
    "CreateRepositoryRequest",
    "DeleteInstanceRequest",
    "DeleteRepositoryRequest",
    "GetInstanceRequest",
    "GetRepositoryRequest",
    "Instance",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListRepositoriesRequest",
    "ListRepositoriesResponse",
    "OperationMetadata",
    "Repository",
)
