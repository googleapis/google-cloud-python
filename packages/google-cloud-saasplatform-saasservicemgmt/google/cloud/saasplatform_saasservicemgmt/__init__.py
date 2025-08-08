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
from google.cloud.saasplatform_saasservicemgmt import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.async_client import (
    SaasDeploymentsAsyncClient,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.client import (
    SaasDeploymentsClient,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_rollouts.async_client import (
    SaasRolloutsAsyncClient,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_rollouts.client import (
    SaasRolloutsClient,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.common import (
    Aggregate,
    Blueprint,
    UnitCondition,
    UnitOperationCondition,
    UnitOperationErrorCategory,
    UnitVariable,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import (
    Dependency,
    Deprovision,
    FromMapping,
    Location,
    Provision,
    Release,
    Saas,
    Schedule,
    Tenant,
    ToMapping,
    Unit,
    UnitDependency,
    UnitKind,
    UnitOperation,
    Upgrade,
    VariableMapping,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import (
    CreateReleaseRequest,
    CreateSaasRequest,
    CreateTenantRequest,
    CreateUnitKindRequest,
    CreateUnitOperationRequest,
    CreateUnitRequest,
    DeleteReleaseRequest,
    DeleteSaasRequest,
    DeleteTenantRequest,
    DeleteUnitKindRequest,
    DeleteUnitOperationRequest,
    DeleteUnitRequest,
    GetReleaseRequest,
    GetSaasRequest,
    GetTenantRequest,
    GetUnitKindRequest,
    GetUnitOperationRequest,
    GetUnitRequest,
    ListReleasesRequest,
    ListReleasesResponse,
    ListSaasRequest,
    ListSaasResponse,
    ListTenantsRequest,
    ListTenantsResponse,
    ListUnitKindsRequest,
    ListUnitKindsResponse,
    ListUnitOperationsRequest,
    ListUnitOperationsResponse,
    ListUnitsRequest,
    ListUnitsResponse,
    UpdateReleaseRequest,
    UpdateSaasRequest,
    UpdateTenantRequest,
    UpdateUnitKindRequest,
    UpdateUnitOperationRequest,
    UpdateUnitRequest,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_resources import (
    ErrorBudget,
    Rollout,
    RolloutAction,
    RolloutControl,
    RolloutKind,
    RolloutStats,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import (
    CreateRolloutKindRequest,
    CreateRolloutRequest,
    DeleteRolloutKindRequest,
    DeleteRolloutRequest,
    GetRolloutKindRequest,
    GetRolloutRequest,
    ListRolloutKindsRequest,
    ListRolloutKindsResponse,
    ListRolloutsRequest,
    ListRolloutsResponse,
    UpdateRolloutKindRequest,
    UpdateRolloutRequest,
)

__all__ = (
    "SaasDeploymentsClient",
    "SaasDeploymentsAsyncClient",
    "SaasRolloutsClient",
    "SaasRolloutsAsyncClient",
    "Aggregate",
    "Blueprint",
    "UnitCondition",
    "UnitOperationCondition",
    "UnitVariable",
    "UnitOperationErrorCategory",
    "Dependency",
    "Deprovision",
    "FromMapping",
    "Location",
    "Provision",
    "Release",
    "Saas",
    "Schedule",
    "Tenant",
    "ToMapping",
    "Unit",
    "UnitDependency",
    "UnitKind",
    "UnitOperation",
    "Upgrade",
    "VariableMapping",
    "CreateReleaseRequest",
    "CreateSaasRequest",
    "CreateTenantRequest",
    "CreateUnitKindRequest",
    "CreateUnitOperationRequest",
    "CreateUnitRequest",
    "DeleteReleaseRequest",
    "DeleteSaasRequest",
    "DeleteTenantRequest",
    "DeleteUnitKindRequest",
    "DeleteUnitOperationRequest",
    "DeleteUnitRequest",
    "GetReleaseRequest",
    "GetSaasRequest",
    "GetTenantRequest",
    "GetUnitKindRequest",
    "GetUnitOperationRequest",
    "GetUnitRequest",
    "ListReleasesRequest",
    "ListReleasesResponse",
    "ListSaasRequest",
    "ListSaasResponse",
    "ListTenantsRequest",
    "ListTenantsResponse",
    "ListUnitKindsRequest",
    "ListUnitKindsResponse",
    "ListUnitOperationsRequest",
    "ListUnitOperationsResponse",
    "ListUnitsRequest",
    "ListUnitsResponse",
    "UpdateReleaseRequest",
    "UpdateSaasRequest",
    "UpdateTenantRequest",
    "UpdateUnitKindRequest",
    "UpdateUnitOperationRequest",
    "UpdateUnitRequest",
    "ErrorBudget",
    "Rollout",
    "RolloutControl",
    "RolloutKind",
    "RolloutStats",
    "RolloutAction",
    "CreateRolloutKindRequest",
    "CreateRolloutRequest",
    "DeleteRolloutKindRequest",
    "DeleteRolloutRequest",
    "GetRolloutKindRequest",
    "GetRolloutRequest",
    "ListRolloutKindsRequest",
    "ListRolloutKindsResponse",
    "ListRolloutsRequest",
    "ListRolloutsResponse",
    "UpdateRolloutKindRequest",
    "UpdateRolloutRequest",
)
