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
from google.cloud.accesscontextmanager import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.accesscontextmanager_v1.services.access_context_manager.async_client import (
    AccessContextManagerAsyncClient,
)
from google.cloud.accesscontextmanager_v1.services.access_context_manager.client import (
    AccessContextManagerClient,
)
from google.cloud.accesscontextmanager_v1.types.access_context_manager import (
    AccessContextManagerOperationMetadata,
    CommitServicePerimetersRequest,
    CommitServicePerimetersResponse,
    CreateAccessLevelRequest,
    CreateGcpUserAccessBindingRequest,
    CreateServicePerimeterRequest,
    DeleteAccessLevelRequest,
    DeleteAccessPolicyRequest,
    DeleteGcpUserAccessBindingRequest,
    DeleteServicePerimeterRequest,
    GcpUserAccessBindingOperationMetadata,
    GetAccessLevelRequest,
    GetAccessPolicyRequest,
    GetGcpUserAccessBindingRequest,
    GetServicePerimeterRequest,
    LevelFormat,
    ListAccessLevelsRequest,
    ListAccessLevelsResponse,
    ListAccessPoliciesRequest,
    ListAccessPoliciesResponse,
    ListGcpUserAccessBindingsRequest,
    ListGcpUserAccessBindingsResponse,
    ListServicePerimetersRequest,
    ListServicePerimetersResponse,
    ReplaceAccessLevelsRequest,
    ReplaceAccessLevelsResponse,
    ReplaceServicePerimetersRequest,
    ReplaceServicePerimetersResponse,
    UpdateAccessLevelRequest,
    UpdateAccessPolicyRequest,
    UpdateGcpUserAccessBindingRequest,
    UpdateServicePerimeterRequest,
)
from google.cloud.accesscontextmanager_v1.types.access_level import (
    AccessLevel,
    BasicLevel,
    Condition,
    CustomLevel,
    DevicePolicy,
    OsConstraint,
)
from google.cloud.accesscontextmanager_v1.types.access_policy import AccessPolicy
from google.cloud.accesscontextmanager_v1.types.gcp_user_access_binding import (
    GcpUserAccessBinding,
)
from google.cloud.accesscontextmanager_v1.types.service_perimeter import (
    ServicePerimeter,
    ServicePerimeterConfig,
)

__all__ = (
    "AccessContextManagerClient",
    "AccessContextManagerAsyncClient",
    "AccessContextManagerOperationMetadata",
    "CommitServicePerimetersRequest",
    "CommitServicePerimetersResponse",
    "CreateAccessLevelRequest",
    "CreateGcpUserAccessBindingRequest",
    "CreateServicePerimeterRequest",
    "DeleteAccessLevelRequest",
    "DeleteAccessPolicyRequest",
    "DeleteGcpUserAccessBindingRequest",
    "DeleteServicePerimeterRequest",
    "GcpUserAccessBindingOperationMetadata",
    "GetAccessLevelRequest",
    "GetAccessPolicyRequest",
    "GetGcpUserAccessBindingRequest",
    "GetServicePerimeterRequest",
    "ListAccessLevelsRequest",
    "ListAccessLevelsResponse",
    "ListAccessPoliciesRequest",
    "ListAccessPoliciesResponse",
    "ListGcpUserAccessBindingsRequest",
    "ListGcpUserAccessBindingsResponse",
    "ListServicePerimetersRequest",
    "ListServicePerimetersResponse",
    "ReplaceAccessLevelsRequest",
    "ReplaceAccessLevelsResponse",
    "ReplaceServicePerimetersRequest",
    "ReplaceServicePerimetersResponse",
    "UpdateAccessLevelRequest",
    "UpdateAccessPolicyRequest",
    "UpdateGcpUserAccessBindingRequest",
    "UpdateServicePerimeterRequest",
    "LevelFormat",
    "AccessLevel",
    "BasicLevel",
    "Condition",
    "CustomLevel",
    "DevicePolicy",
    "OsConstraint",
    "AccessPolicy",
    "GcpUserAccessBinding",
    "ServicePerimeter",
    "ServicePerimeterConfig",
)
