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

from google.cloud.artifactregistry_v1.services.artifact_registry.client import (
    ArtifactRegistryClient,
)
from google.cloud.artifactregistry_v1.services.artifact_registry.async_client import (
    ArtifactRegistryAsyncClient,
)

from google.cloud.artifactregistry_v1.types.artifact import DockerImage
from google.cloud.artifactregistry_v1.types.artifact import ListDockerImagesRequest
from google.cloud.artifactregistry_v1.types.artifact import ListDockerImagesResponse
from google.cloud.artifactregistry_v1.types.repository import GetRepositoryRequest
from google.cloud.artifactregistry_v1.types.repository import ListRepositoriesRequest
from google.cloud.artifactregistry_v1.types.repository import ListRepositoriesResponse
from google.cloud.artifactregistry_v1.types.repository import Repository

__all__ = (
    "ArtifactRegistryClient",
    "ArtifactRegistryAsyncClient",
    "DockerImage",
    "ListDockerImagesRequest",
    "ListDockerImagesResponse",
    "GetRepositoryRequest",
    "ListRepositoriesRequest",
    "ListRepositoriesResponse",
    "Repository",
)
