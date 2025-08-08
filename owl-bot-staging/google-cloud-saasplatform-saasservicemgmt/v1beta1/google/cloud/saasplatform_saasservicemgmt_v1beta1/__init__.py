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
from google.cloud.saasplatform_saasservicemgmt_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.saas_deployments import SaasDeploymentsClient
from .services.saas_deployments import SaasDeploymentsAsyncClient
from .services.saas_rollouts import SaasRolloutsClient
from .services.saas_rollouts import SaasRolloutsAsyncClient

from .types.common import Aggregate
from .types.common import Blueprint
from .types.common import UnitCondition
from .types.common import UnitOperationCondition
from .types.common import UnitVariable
from .types.common import UnitOperationErrorCategory
from .types.deployments_resources import Dependency
from .types.deployments_resources import Deprovision
from .types.deployments_resources import FromMapping
from .types.deployments_resources import Location
from .types.deployments_resources import Provision
from .types.deployments_resources import Release
from .types.deployments_resources import Saas
from .types.deployments_resources import Schedule
from .types.deployments_resources import Tenant
from .types.deployments_resources import ToMapping
from .types.deployments_resources import Unit
from .types.deployments_resources import UnitDependency
from .types.deployments_resources import UnitKind
from .types.deployments_resources import UnitOperation
from .types.deployments_resources import Upgrade
from .types.deployments_resources import VariableMapping
from .types.deployments_service import CreateReleaseRequest
from .types.deployments_service import CreateSaasRequest
from .types.deployments_service import CreateTenantRequest
from .types.deployments_service import CreateUnitKindRequest
from .types.deployments_service import CreateUnitOperationRequest
from .types.deployments_service import CreateUnitRequest
from .types.deployments_service import DeleteReleaseRequest
from .types.deployments_service import DeleteSaasRequest
from .types.deployments_service import DeleteTenantRequest
from .types.deployments_service import DeleteUnitKindRequest
from .types.deployments_service import DeleteUnitOperationRequest
from .types.deployments_service import DeleteUnitRequest
from .types.deployments_service import GetReleaseRequest
from .types.deployments_service import GetSaasRequest
from .types.deployments_service import GetTenantRequest
from .types.deployments_service import GetUnitKindRequest
from .types.deployments_service import GetUnitOperationRequest
from .types.deployments_service import GetUnitRequest
from .types.deployments_service import ListReleasesRequest
from .types.deployments_service import ListReleasesResponse
from .types.deployments_service import ListSaasRequest
from .types.deployments_service import ListSaasResponse
from .types.deployments_service import ListTenantsRequest
from .types.deployments_service import ListTenantsResponse
from .types.deployments_service import ListUnitKindsRequest
from .types.deployments_service import ListUnitKindsResponse
from .types.deployments_service import ListUnitOperationsRequest
from .types.deployments_service import ListUnitOperationsResponse
from .types.deployments_service import ListUnitsRequest
from .types.deployments_service import ListUnitsResponse
from .types.deployments_service import UpdateReleaseRequest
from .types.deployments_service import UpdateSaasRequest
from .types.deployments_service import UpdateTenantRequest
from .types.deployments_service import UpdateUnitKindRequest
from .types.deployments_service import UpdateUnitOperationRequest
from .types.deployments_service import UpdateUnitRequest
from .types.rollouts_resources import ErrorBudget
from .types.rollouts_resources import Rollout
from .types.rollouts_resources import RolloutControl
from .types.rollouts_resources import RolloutKind
from .types.rollouts_resources import RolloutStats
from .types.rollouts_resources import RolloutAction
from .types.rollouts_service import CreateRolloutKindRequest
from .types.rollouts_service import CreateRolloutRequest
from .types.rollouts_service import DeleteRolloutKindRequest
from .types.rollouts_service import DeleteRolloutRequest
from .types.rollouts_service import GetRolloutKindRequest
from .types.rollouts_service import GetRolloutRequest
from .types.rollouts_service import ListRolloutKindsRequest
from .types.rollouts_service import ListRolloutKindsResponse
from .types.rollouts_service import ListRolloutsRequest
from .types.rollouts_service import ListRolloutsResponse
from .types.rollouts_service import UpdateRolloutKindRequest
from .types.rollouts_service import UpdateRolloutRequest

__all__ = (
    'SaasDeploymentsAsyncClient',
    'SaasRolloutsAsyncClient',
'Aggregate',
'Blueprint',
'CreateReleaseRequest',
'CreateRolloutKindRequest',
'CreateRolloutRequest',
'CreateSaasRequest',
'CreateTenantRequest',
'CreateUnitKindRequest',
'CreateUnitOperationRequest',
'CreateUnitRequest',
'DeleteReleaseRequest',
'DeleteRolloutKindRequest',
'DeleteRolloutRequest',
'DeleteSaasRequest',
'DeleteTenantRequest',
'DeleteUnitKindRequest',
'DeleteUnitOperationRequest',
'DeleteUnitRequest',
'Dependency',
'Deprovision',
'ErrorBudget',
'FromMapping',
'GetReleaseRequest',
'GetRolloutKindRequest',
'GetRolloutRequest',
'GetSaasRequest',
'GetTenantRequest',
'GetUnitKindRequest',
'GetUnitOperationRequest',
'GetUnitRequest',
'ListReleasesRequest',
'ListReleasesResponse',
'ListRolloutKindsRequest',
'ListRolloutKindsResponse',
'ListRolloutsRequest',
'ListRolloutsResponse',
'ListSaasRequest',
'ListSaasResponse',
'ListTenantsRequest',
'ListTenantsResponse',
'ListUnitKindsRequest',
'ListUnitKindsResponse',
'ListUnitOperationsRequest',
'ListUnitOperationsResponse',
'ListUnitsRequest',
'ListUnitsResponse',
'Location',
'Provision',
'Release',
'Rollout',
'RolloutAction',
'RolloutControl',
'RolloutKind',
'RolloutStats',
'Saas',
'SaasDeploymentsClient',
'SaasRolloutsClient',
'Schedule',
'Tenant',
'ToMapping',
'Unit',
'UnitCondition',
'UnitDependency',
'UnitKind',
'UnitOperation',
'UnitOperationCondition',
'UnitOperationErrorCategory',
'UnitVariable',
'UpdateReleaseRequest',
'UpdateRolloutKindRequest',
'UpdateRolloutRequest',
'UpdateSaasRequest',
'UpdateTenantRequest',
'UpdateUnitKindRequest',
'UpdateUnitOperationRequest',
'UpdateUnitRequest',
'Upgrade',
'VariableMapping',
)
