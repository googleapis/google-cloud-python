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
from google.cloud.apigee_registry_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.provisioning import ProvisioningAsyncClient, ProvisioningClient
from .services.registry import RegistryAsyncClient, RegistryClient
from .types.provisioning_service import (
    CreateInstanceRequest,
    DeleteInstanceRequest,
    GetInstanceRequest,
    Instance,
    OperationMetadata,
)
from .types.registry_models import Api, ApiDeployment, ApiSpec, ApiVersion, Artifact
from .types.registry_service import (
    CreateApiDeploymentRequest,
    CreateApiRequest,
    CreateApiSpecRequest,
    CreateApiVersionRequest,
    CreateArtifactRequest,
    DeleteApiDeploymentRequest,
    DeleteApiDeploymentRevisionRequest,
    DeleteApiRequest,
    DeleteApiSpecRequest,
    DeleteApiSpecRevisionRequest,
    DeleteApiVersionRequest,
    DeleteArtifactRequest,
    GetApiDeploymentRequest,
    GetApiRequest,
    GetApiSpecContentsRequest,
    GetApiSpecRequest,
    GetApiVersionRequest,
    GetArtifactContentsRequest,
    GetArtifactRequest,
    ListApiDeploymentRevisionsRequest,
    ListApiDeploymentRevisionsResponse,
    ListApiDeploymentsRequest,
    ListApiDeploymentsResponse,
    ListApiSpecRevisionsRequest,
    ListApiSpecRevisionsResponse,
    ListApiSpecsRequest,
    ListApiSpecsResponse,
    ListApisRequest,
    ListApisResponse,
    ListApiVersionsRequest,
    ListApiVersionsResponse,
    ListArtifactsRequest,
    ListArtifactsResponse,
    ReplaceArtifactRequest,
    RollbackApiDeploymentRequest,
    RollbackApiSpecRequest,
    TagApiDeploymentRevisionRequest,
    TagApiSpecRevisionRequest,
    UpdateApiDeploymentRequest,
    UpdateApiRequest,
    UpdateApiSpecRequest,
    UpdateApiVersionRequest,
)

__all__ = (
    "ProvisioningAsyncClient",
    "RegistryAsyncClient",
    "Api",
    "ApiDeployment",
    "ApiSpec",
    "ApiVersion",
    "Artifact",
    "CreateApiDeploymentRequest",
    "CreateApiRequest",
    "CreateApiSpecRequest",
    "CreateApiVersionRequest",
    "CreateArtifactRequest",
    "CreateInstanceRequest",
    "DeleteApiDeploymentRequest",
    "DeleteApiDeploymentRevisionRequest",
    "DeleteApiRequest",
    "DeleteApiSpecRequest",
    "DeleteApiSpecRevisionRequest",
    "DeleteApiVersionRequest",
    "DeleteArtifactRequest",
    "DeleteInstanceRequest",
    "GetApiDeploymentRequest",
    "GetApiRequest",
    "GetApiSpecContentsRequest",
    "GetApiSpecRequest",
    "GetApiVersionRequest",
    "GetArtifactContentsRequest",
    "GetArtifactRequest",
    "GetInstanceRequest",
    "Instance",
    "ListApiDeploymentRevisionsRequest",
    "ListApiDeploymentRevisionsResponse",
    "ListApiDeploymentsRequest",
    "ListApiDeploymentsResponse",
    "ListApiSpecRevisionsRequest",
    "ListApiSpecRevisionsResponse",
    "ListApiSpecsRequest",
    "ListApiSpecsResponse",
    "ListApiVersionsRequest",
    "ListApiVersionsResponse",
    "ListApisRequest",
    "ListApisResponse",
    "ListArtifactsRequest",
    "ListArtifactsResponse",
    "OperationMetadata",
    "ProvisioningClient",
    "RegistryClient",
    "ReplaceArtifactRequest",
    "RollbackApiDeploymentRequest",
    "RollbackApiSpecRequest",
    "TagApiDeploymentRevisionRequest",
    "TagApiSpecRevisionRequest",
    "UpdateApiDeploymentRequest",
    "UpdateApiRequest",
    "UpdateApiSpecRequest",
    "UpdateApiVersionRequest",
)
