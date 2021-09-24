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

from .services.artifact_registry import ArtifactRegistryClient
from .services.artifact_registry import ArtifactRegistryAsyncClient

from .types.artifact import DockerImage
from .types.artifact import ListDockerImagesRequest
from .types.artifact import ListDockerImagesResponse
from .types.repository import GetRepositoryRequest
from .types.repository import ListRepositoriesRequest
from .types.repository import ListRepositoriesResponse
from .types.repository import Repository

__all__ = (
    "ArtifactRegistryAsyncClient",
    "ArtifactRegistryClient",
    "DockerImage",
    "GetRepositoryRequest",
    "ListDockerImagesRequest",
    "ListDockerImagesResponse",
    "ListRepositoriesRequest",
    "ListRepositoriesResponse",
    "Repository",
)
