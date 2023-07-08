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
from google.cloud.apigee_registry import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.apigee_registry_v1.services.provisioning.async_client import (
    ProvisioningAsyncClient,
)
from google.cloud.apigee_registry_v1.services.provisioning.client import (
    ProvisioningClient,
)
from google.cloud.apigee_registry_v1.services.registry.async_client import (
    RegistryAsyncClient,
)
from google.cloud.apigee_registry_v1.services.registry.client import RegistryClient
from google.cloud.apigee_registry_v1.types.provisioning_service import (
    CreateInstanceRequest,
    DeleteInstanceRequest,
    GetInstanceRequest,
    Instance,
    OperationMetadata,
)
from google.cloud.apigee_registry_v1.types.registry_models import (
    Api,
    ApiDeployment,
    ApiSpec,
    ApiVersion,
    Artifact,
)
from google.cloud.apigee_registry_v1.types.registry_service import (
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
    "ProvisioningClient",
    "ProvisioningAsyncClient",
    "RegistryClient",
    "RegistryAsyncClient",
    "CreateInstanceRequest",
    "DeleteInstanceRequest",
    "GetInstanceRequest",
    "Instance",
    "OperationMetadata",
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
    "DeleteApiDeploymentRequest",
    "DeleteApiDeploymentRevisionRequest",
    "DeleteApiRequest",
    "DeleteApiSpecRequest",
    "DeleteApiSpecRevisionRequest",
    "DeleteApiVersionRequest",
    "DeleteArtifactRequest",
    "GetApiDeploymentRequest",
    "GetApiRequest",
    "GetApiSpecContentsRequest",
    "GetApiSpecRequest",
    "GetApiVersionRequest",
    "GetArtifactContentsRequest",
    "GetArtifactRequest",
    "ListApiDeploymentRevisionsRequest",
    "ListApiDeploymentRevisionsResponse",
    "ListApiDeploymentsRequest",
    "ListApiDeploymentsResponse",
    "ListApiSpecRevisionsRequest",
    "ListApiSpecRevisionsResponse",
    "ListApiSpecsRequest",
    "ListApiSpecsResponse",
    "ListApisRequest",
    "ListApisResponse",
    "ListApiVersionsRequest",
    "ListApiVersionsResponse",
    "ListArtifactsRequest",
    "ListArtifactsResponse",
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
