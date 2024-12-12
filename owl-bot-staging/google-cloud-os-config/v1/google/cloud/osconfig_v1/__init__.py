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
from google.cloud.osconfig_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.os_config_service import OsConfigServiceClient
from .services.os_config_service import OsConfigServiceAsyncClient
from .services.os_config_zonal_service import OsConfigZonalServiceClient
from .services.os_config_zonal_service import OsConfigZonalServiceAsyncClient

from .types.inventory import GetInventoryRequest
from .types.inventory import Inventory
from .types.inventory import ListInventoriesRequest
from .types.inventory import ListInventoriesResponse
from .types.inventory import InventoryView
from .types.os_policy import OSPolicy
from .types.os_policy_assignment_reports import GetOSPolicyAssignmentReportRequest
from .types.os_policy_assignment_reports import ListOSPolicyAssignmentReportsRequest
from .types.os_policy_assignment_reports import ListOSPolicyAssignmentReportsResponse
from .types.os_policy_assignment_reports import OSPolicyAssignmentReport
from .types.os_policy_assignments import CreateOSPolicyAssignmentRequest
from .types.os_policy_assignments import DeleteOSPolicyAssignmentRequest
from .types.os_policy_assignments import GetOSPolicyAssignmentRequest
from .types.os_policy_assignments import ListOSPolicyAssignmentRevisionsRequest
from .types.os_policy_assignments import ListOSPolicyAssignmentRevisionsResponse
from .types.os_policy_assignments import ListOSPolicyAssignmentsRequest
from .types.os_policy_assignments import ListOSPolicyAssignmentsResponse
from .types.os_policy_assignments import OSPolicyAssignment
from .types.os_policy_assignments import OSPolicyAssignmentOperationMetadata
from .types.os_policy_assignments import UpdateOSPolicyAssignmentRequest
from .types.osconfig_common import FixedOrPercent
from .types.patch_deployments import CreatePatchDeploymentRequest
from .types.patch_deployments import DeletePatchDeploymentRequest
from .types.patch_deployments import GetPatchDeploymentRequest
from .types.patch_deployments import ListPatchDeploymentsRequest
from .types.patch_deployments import ListPatchDeploymentsResponse
from .types.patch_deployments import MonthlySchedule
from .types.patch_deployments import OneTimeSchedule
from .types.patch_deployments import PatchDeployment
from .types.patch_deployments import PausePatchDeploymentRequest
from .types.patch_deployments import RecurringSchedule
from .types.patch_deployments import ResumePatchDeploymentRequest
from .types.patch_deployments import UpdatePatchDeploymentRequest
from .types.patch_deployments import WeekDayOfMonth
from .types.patch_deployments import WeeklySchedule
from .types.patch_jobs import AptSettings
from .types.patch_jobs import CancelPatchJobRequest
from .types.patch_jobs import ExecStep
from .types.patch_jobs import ExecStepConfig
from .types.patch_jobs import ExecutePatchJobRequest
from .types.patch_jobs import GcsObject
from .types.patch_jobs import GetPatchJobRequest
from .types.patch_jobs import GooSettings
from .types.patch_jobs import Instance
from .types.patch_jobs import ListPatchJobInstanceDetailsRequest
from .types.patch_jobs import ListPatchJobInstanceDetailsResponse
from .types.patch_jobs import ListPatchJobsRequest
from .types.patch_jobs import ListPatchJobsResponse
from .types.patch_jobs import PatchConfig
from .types.patch_jobs import PatchInstanceFilter
from .types.patch_jobs import PatchJob
from .types.patch_jobs import PatchJobInstanceDetails
from .types.patch_jobs import PatchRollout
from .types.patch_jobs import WindowsUpdateSettings
from .types.patch_jobs import YumSettings
from .types.patch_jobs import ZypperSettings
from .types.vulnerability import CVSSv3
from .types.vulnerability import GetVulnerabilityReportRequest
from .types.vulnerability import ListVulnerabilityReportsRequest
from .types.vulnerability import ListVulnerabilityReportsResponse
from .types.vulnerability import VulnerabilityReport

__all__ = (
    'OsConfigServiceAsyncClient',
    'OsConfigZonalServiceAsyncClient',
'AptSettings',
'CVSSv3',
'CancelPatchJobRequest',
'CreateOSPolicyAssignmentRequest',
'CreatePatchDeploymentRequest',
'DeleteOSPolicyAssignmentRequest',
'DeletePatchDeploymentRequest',
'ExecStep',
'ExecStepConfig',
'ExecutePatchJobRequest',
'FixedOrPercent',
'GcsObject',
'GetInventoryRequest',
'GetOSPolicyAssignmentReportRequest',
'GetOSPolicyAssignmentRequest',
'GetPatchDeploymentRequest',
'GetPatchJobRequest',
'GetVulnerabilityReportRequest',
'GooSettings',
'Instance',
'Inventory',
'InventoryView',
'ListInventoriesRequest',
'ListInventoriesResponse',
'ListOSPolicyAssignmentReportsRequest',
'ListOSPolicyAssignmentReportsResponse',
'ListOSPolicyAssignmentRevisionsRequest',
'ListOSPolicyAssignmentRevisionsResponse',
'ListOSPolicyAssignmentsRequest',
'ListOSPolicyAssignmentsResponse',
'ListPatchDeploymentsRequest',
'ListPatchDeploymentsResponse',
'ListPatchJobInstanceDetailsRequest',
'ListPatchJobInstanceDetailsResponse',
'ListPatchJobsRequest',
'ListPatchJobsResponse',
'ListVulnerabilityReportsRequest',
'ListVulnerabilityReportsResponse',
'MonthlySchedule',
'OSPolicy',
'OSPolicyAssignment',
'OSPolicyAssignmentOperationMetadata',
'OSPolicyAssignmentReport',
'OneTimeSchedule',
'OsConfigServiceClient',
'OsConfigZonalServiceClient',
'PatchConfig',
'PatchDeployment',
'PatchInstanceFilter',
'PatchJob',
'PatchJobInstanceDetails',
'PatchRollout',
'PausePatchDeploymentRequest',
'RecurringSchedule',
'ResumePatchDeploymentRequest',
'UpdateOSPolicyAssignmentRequest',
'UpdatePatchDeploymentRequest',
'VulnerabilityReport',
'WeekDayOfMonth',
'WeeklySchedule',
'WindowsUpdateSettings',
'YumSettings',
'ZypperSettings',
)
