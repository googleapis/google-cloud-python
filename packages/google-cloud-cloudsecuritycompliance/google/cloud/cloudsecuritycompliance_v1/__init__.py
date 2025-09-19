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
from google.cloud.cloudsecuritycompliance_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.config import ConfigAsyncClient, ConfigClient
from .services.deployment import DeploymentAsyncClient, DeploymentClient
from .types.common import (
    AllowedValues,
    AttributeSubstitutionRule,
    CELExpression,
    CloudControl,
    CloudControlCategory,
    CloudControlDetails,
    CloudProvider,
    EnforcementMode,
    Framework,
    FrameworkCategory,
    FrameworkReference,
    IntRange,
    OperationMetadata,
    Parameter,
    ParameterSpec,
    ParameterSubstitutionRule,
    ParamValue,
    PlaceholderSubstitutionRule,
    RegexpPattern,
    Rule,
    RuleActionType,
    Severity,
    StringList,
    TargetResourceType,
    Validation,
)
from .types.config import (
    CreateCloudControlRequest,
    CreateFrameworkRequest,
    DeleteCloudControlRequest,
    DeleteFrameworkRequest,
    GetCloudControlRequest,
    GetFrameworkRequest,
    ListCloudControlsRequest,
    ListCloudControlsResponse,
    ListFrameworksRequest,
    ListFrameworksResponse,
    UpdateCloudControlRequest,
    UpdateFrameworkRequest,
)
from .types.deployment import (
    CloudControlDeployment,
    CloudControlDeploymentReference,
    CloudControlMetadata,
    CreateFrameworkDeploymentRequest,
    DeleteFrameworkDeploymentRequest,
    DeploymentState,
    FolderCreationConfig,
    FrameworkDeployment,
    FrameworkDeploymentReference,
    GetCloudControlDeploymentRequest,
    GetFrameworkDeploymentRequest,
    ListCloudControlDeploymentsRequest,
    ListCloudControlDeploymentsResponse,
    ListFrameworkDeploymentsRequest,
    ListFrameworkDeploymentsResponse,
    ProjectCreationConfig,
    TargetResourceConfig,
    TargetResourceCreationConfig,
)

__all__ = (
    "ConfigAsyncClient",
    "DeploymentAsyncClient",
    "AllowedValues",
    "AttributeSubstitutionRule",
    "CELExpression",
    "CloudControl",
    "CloudControlCategory",
    "CloudControlDeployment",
    "CloudControlDeploymentReference",
    "CloudControlDetails",
    "CloudControlMetadata",
    "CloudProvider",
    "ConfigClient",
    "CreateCloudControlRequest",
    "CreateFrameworkDeploymentRequest",
    "CreateFrameworkRequest",
    "DeleteCloudControlRequest",
    "DeleteFrameworkDeploymentRequest",
    "DeleteFrameworkRequest",
    "DeploymentClient",
    "DeploymentState",
    "EnforcementMode",
    "FolderCreationConfig",
    "Framework",
    "FrameworkCategory",
    "FrameworkDeployment",
    "FrameworkDeploymentReference",
    "FrameworkReference",
    "GetCloudControlDeploymentRequest",
    "GetCloudControlRequest",
    "GetFrameworkDeploymentRequest",
    "GetFrameworkRequest",
    "IntRange",
    "ListCloudControlDeploymentsRequest",
    "ListCloudControlDeploymentsResponse",
    "ListCloudControlsRequest",
    "ListCloudControlsResponse",
    "ListFrameworkDeploymentsRequest",
    "ListFrameworkDeploymentsResponse",
    "ListFrameworksRequest",
    "ListFrameworksResponse",
    "OperationMetadata",
    "ParamValue",
    "Parameter",
    "ParameterSpec",
    "ParameterSubstitutionRule",
    "PlaceholderSubstitutionRule",
    "ProjectCreationConfig",
    "RegexpPattern",
    "Rule",
    "RuleActionType",
    "Severity",
    "StringList",
    "TargetResourceConfig",
    "TargetResourceCreationConfig",
    "TargetResourceType",
    "UpdateCloudControlRequest",
    "UpdateFrameworkRequest",
    "Validation",
)
