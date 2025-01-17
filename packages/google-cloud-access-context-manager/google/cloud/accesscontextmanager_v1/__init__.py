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
from google.cloud.accesscontextmanager_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.access_context_manager import (
    AccessContextManagerAsyncClient,
    AccessContextManagerClient,
)
from .types.access_context_manager import (
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
from .types.access_level import (
    AccessLevel,
    BasicLevel,
    Condition,
    CustomLevel,
    DevicePolicy,
    OsConstraint,
)
from .types.access_policy import AccessPolicy
from .types.gcp_user_access_binding import GcpUserAccessBinding
from .types.service_perimeter import ServicePerimeter, ServicePerimeterConfig

__all__ = (
    "AccessContextManagerAsyncClient",
    "AccessContextManagerClient",
    "AccessContextManagerOperationMetadata",
    "AccessLevel",
    "AccessPolicy",
    "BasicLevel",
    "CommitServicePerimetersRequest",
    "CommitServicePerimetersResponse",
    "Condition",
    "CreateAccessLevelRequest",
    "CreateGcpUserAccessBindingRequest",
    "CreateServicePerimeterRequest",
    "CustomLevel",
    "DeleteAccessLevelRequest",
    "DeleteAccessPolicyRequest",
    "DeleteGcpUserAccessBindingRequest",
    "DeleteServicePerimeterRequest",
    "DevicePolicy",
    "GcpUserAccessBinding",
    "GcpUserAccessBindingOperationMetadata",
    "GetAccessLevelRequest",
    "GetAccessPolicyRequest",
    "GetGcpUserAccessBindingRequest",
    "GetServicePerimeterRequest",
    "LevelFormat",
    "ListAccessLevelsRequest",
    "ListAccessLevelsResponse",
    "ListAccessPoliciesRequest",
    "ListAccessPoliciesResponse",
    "ListGcpUserAccessBindingsRequest",
    "ListGcpUserAccessBindingsResponse",
    "ListServicePerimetersRequest",
    "ListServicePerimetersResponse",
    "OsConstraint",
    "ReplaceAccessLevelsRequest",
    "ReplaceAccessLevelsResponse",
    "ReplaceServicePerimetersRequest",
    "ReplaceServicePerimetersResponse",
    "ServicePerimeter",
    "ServicePerimeterConfig",
    "UpdateAccessLevelRequest",
    "UpdateAccessPolicyRequest",
    "UpdateGcpUserAccessBindingRequest",
    "UpdateServicePerimeterRequest",
)
