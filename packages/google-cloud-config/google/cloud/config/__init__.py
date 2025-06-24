# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.config import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.config_v1.services.config.async_client import ConfigAsyncClient
from google.cloud.config_v1.services.config.client import ConfigClient
from google.cloud.config_v1.types.config import (
    ApplyResults,
    CreateDeploymentRequest,
    CreatePreviewRequest,
    DeleteDeploymentRequest,
    DeletePreviewRequest,
    DeleteStatefileRequest,
    Deployment,
    DeploymentOperationMetadata,
    ExportDeploymentStatefileRequest,
    ExportLockInfoRequest,
    ExportPreviewResultRequest,
    ExportPreviewResultResponse,
    ExportRevisionStatefileRequest,
    GetDeploymentRequest,
    GetPreviewRequest,
    GetResourceRequest,
    GetRevisionRequest,
    GetTerraformVersionRequest,
    GitSource,
    ImportStatefileRequest,
    ListDeploymentsRequest,
    ListDeploymentsResponse,
    ListPreviewsRequest,
    ListPreviewsResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    ListRevisionsRequest,
    ListRevisionsResponse,
    ListTerraformVersionsRequest,
    ListTerraformVersionsResponse,
    LockDeploymentRequest,
    LockInfo,
    OperationMetadata,
    Preview,
    PreviewArtifacts,
    PreviewOperationMetadata,
    PreviewResult,
    QuotaValidation,
    Resource,
    ResourceCAIInfo,
    ResourceTerraformInfo,
    Revision,
    Statefile,
    TerraformBlueprint,
    TerraformError,
    TerraformOutput,
    TerraformVariable,
    TerraformVersion,
    UnlockDeploymentRequest,
    UpdateDeploymentRequest,
)

__all__ = (
    "ConfigClient",
    "ConfigAsyncClient",
    "ApplyResults",
    "CreateDeploymentRequest",
    "CreatePreviewRequest",
    "DeleteDeploymentRequest",
    "DeletePreviewRequest",
    "DeleteStatefileRequest",
    "Deployment",
    "DeploymentOperationMetadata",
    "ExportDeploymentStatefileRequest",
    "ExportLockInfoRequest",
    "ExportPreviewResultRequest",
    "ExportPreviewResultResponse",
    "ExportRevisionStatefileRequest",
    "GetDeploymentRequest",
    "GetPreviewRequest",
    "GetResourceRequest",
    "GetRevisionRequest",
    "GetTerraformVersionRequest",
    "GitSource",
    "ImportStatefileRequest",
    "ListDeploymentsRequest",
    "ListDeploymentsResponse",
    "ListPreviewsRequest",
    "ListPreviewsResponse",
    "ListResourcesRequest",
    "ListResourcesResponse",
    "ListRevisionsRequest",
    "ListRevisionsResponse",
    "ListTerraformVersionsRequest",
    "ListTerraformVersionsResponse",
    "LockDeploymentRequest",
    "LockInfo",
    "OperationMetadata",
    "Preview",
    "PreviewArtifacts",
    "PreviewOperationMetadata",
    "PreviewResult",
    "Resource",
    "ResourceCAIInfo",
    "ResourceTerraformInfo",
    "Revision",
    "Statefile",
    "TerraformBlueprint",
    "TerraformError",
    "TerraformOutput",
    "TerraformVariable",
    "TerraformVersion",
    "UnlockDeploymentRequest",
    "UpdateDeploymentRequest",
    "QuotaValidation",
)
