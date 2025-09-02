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


from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.client import SaasDeploymentsClient
from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_deployments.async_client import SaasDeploymentsAsyncClient
from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_rollouts.client import SaasRolloutsClient
from google.cloud.saasplatform_saasservicemgmt_v1beta1.services.saas_rollouts.async_client import SaasRolloutsAsyncClient

from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.common import Aggregate
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.common import Blueprint
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.common import UnitCondition
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.common import UnitOperationCondition
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.common import UnitVariable
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.common import UnitOperationErrorCategory
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Dependency
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Deprovision
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import FromMapping
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Location
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Provision
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Release
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Saas
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Schedule
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Tenant
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import ToMapping
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Unit
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import UnitDependency
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import UnitKind
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import UnitOperation
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import Upgrade
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_resources import VariableMapping
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import CreateReleaseRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import CreateSaasRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import CreateTenantRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import CreateUnitKindRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import CreateUnitOperationRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import CreateUnitRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import DeleteReleaseRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import DeleteSaasRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import DeleteTenantRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import DeleteUnitKindRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import DeleteUnitOperationRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import DeleteUnitRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import GetReleaseRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import GetSaasRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import GetTenantRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import GetUnitKindRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import GetUnitOperationRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import GetUnitRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListReleasesRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListReleasesResponse
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListSaasRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListSaasResponse
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListTenantsRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListTenantsResponse
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListUnitKindsRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListUnitKindsResponse
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListUnitOperationsRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListUnitOperationsResponse
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListUnitsRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import ListUnitsResponse
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import UpdateReleaseRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import UpdateSaasRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import UpdateTenantRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import UpdateUnitKindRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import UpdateUnitOperationRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.deployments_service import UpdateUnitRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_resources import ErrorBudget
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_resources import Rollout
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_resources import RolloutControl
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_resources import RolloutKind
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_resources import RolloutStats
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_resources import RolloutAction
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import CreateRolloutKindRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import CreateRolloutRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import DeleteRolloutKindRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import DeleteRolloutRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import GetRolloutKindRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import GetRolloutRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import ListRolloutKindsRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import ListRolloutKindsResponse
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import ListRolloutsRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import ListRolloutsResponse
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import UpdateRolloutKindRequest
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types.rollouts_service import UpdateRolloutRequest

__all__ = ('SaasDeploymentsClient',
    'SaasDeploymentsAsyncClient',
    'SaasRolloutsClient',
    'SaasRolloutsAsyncClient',
    'Aggregate',
    'Blueprint',
    'UnitCondition',
    'UnitOperationCondition',
    'UnitVariable',
    'UnitOperationErrorCategory',
    'Dependency',
    'Deprovision',
    'FromMapping',
    'Location',
    'Provision',
    'Release',
    'Saas',
    'Schedule',
    'Tenant',
    'ToMapping',
    'Unit',
    'UnitDependency',
    'UnitKind',
    'UnitOperation',
    'Upgrade',
    'VariableMapping',
    'CreateReleaseRequest',
    'CreateSaasRequest',
    'CreateTenantRequest',
    'CreateUnitKindRequest',
    'CreateUnitOperationRequest',
    'CreateUnitRequest',
    'DeleteReleaseRequest',
    'DeleteSaasRequest',
    'DeleteTenantRequest',
    'DeleteUnitKindRequest',
    'DeleteUnitOperationRequest',
    'DeleteUnitRequest',
    'GetReleaseRequest',
    'GetSaasRequest',
    'GetTenantRequest',
    'GetUnitKindRequest',
    'GetUnitOperationRequest',
    'GetUnitRequest',
    'ListReleasesRequest',
    'ListReleasesResponse',
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
    'UpdateReleaseRequest',
    'UpdateSaasRequest',
    'UpdateTenantRequest',
    'UpdateUnitKindRequest',
    'UpdateUnitOperationRequest',
    'UpdateUnitRequest',
    'ErrorBudget',
    'Rollout',
    'RolloutControl',
    'RolloutKind',
    'RolloutStats',
    'RolloutAction',
    'CreateRolloutKindRequest',
    'CreateRolloutRequest',
    'DeleteRolloutKindRequest',
    'DeleteRolloutRequest',
    'GetRolloutKindRequest',
    'GetRolloutRequest',
    'ListRolloutKindsRequest',
    'ListRolloutKindsResponse',
    'ListRolloutsRequest',
    'ListRolloutsResponse',
    'UpdateRolloutKindRequest',
    'UpdateRolloutRequest',
)
