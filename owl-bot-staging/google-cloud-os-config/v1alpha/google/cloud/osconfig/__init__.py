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
from google.cloud.osconfig import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.osconfig_v1alpha.services.os_config_zonal_service.client import OsConfigZonalServiceClient
from google.cloud.osconfig_v1alpha.services.os_config_zonal_service.async_client import OsConfigZonalServiceAsyncClient

from google.cloud.osconfig_v1alpha.types.config_common import OSPolicyResourceCompliance
from google.cloud.osconfig_v1alpha.types.config_common import OSPolicyResourceConfigStep
from google.cloud.osconfig_v1alpha.types.config_common import OSPolicyComplianceState
from google.cloud.osconfig_v1alpha.types.instance_os_policies_compliance import GetInstanceOSPoliciesComplianceRequest
from google.cloud.osconfig_v1alpha.types.instance_os_policies_compliance import InstanceOSPoliciesCompliance
from google.cloud.osconfig_v1alpha.types.instance_os_policies_compliance import ListInstanceOSPoliciesCompliancesRequest
from google.cloud.osconfig_v1alpha.types.instance_os_policies_compliance import ListInstanceOSPoliciesCompliancesResponse
from google.cloud.osconfig_v1alpha.types.inventory import GetInventoryRequest
from google.cloud.osconfig_v1alpha.types.inventory import Inventory
from google.cloud.osconfig_v1alpha.types.inventory import ListInventoriesRequest
from google.cloud.osconfig_v1alpha.types.inventory import ListInventoriesResponse
from google.cloud.osconfig_v1alpha.types.inventory import InventoryView
from google.cloud.osconfig_v1alpha.types.os_policy import OSPolicy
from google.cloud.osconfig_v1alpha.types.os_policy_assignment_reports import GetOSPolicyAssignmentReportRequest
from google.cloud.osconfig_v1alpha.types.os_policy_assignment_reports import ListOSPolicyAssignmentReportsRequest
from google.cloud.osconfig_v1alpha.types.os_policy_assignment_reports import ListOSPolicyAssignmentReportsResponse
from google.cloud.osconfig_v1alpha.types.os_policy_assignment_reports import OSPolicyAssignmentReport
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import CreateOSPolicyAssignmentRequest
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import DeleteOSPolicyAssignmentRequest
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import GetOSPolicyAssignmentRequest
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import ListOSPolicyAssignmentRevisionsRequest
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import ListOSPolicyAssignmentRevisionsResponse
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import ListOSPolicyAssignmentsRequest
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import ListOSPolicyAssignmentsResponse
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import OSPolicyAssignment
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import OSPolicyAssignmentOperationMetadata
from google.cloud.osconfig_v1alpha.types.os_policy_assignments import UpdateOSPolicyAssignmentRequest
from google.cloud.osconfig_v1alpha.types.osconfig_common import FixedOrPercent
from google.cloud.osconfig_v1alpha.types.vulnerability import CVSSv3
from google.cloud.osconfig_v1alpha.types.vulnerability import GetVulnerabilityReportRequest
from google.cloud.osconfig_v1alpha.types.vulnerability import ListVulnerabilityReportsRequest
from google.cloud.osconfig_v1alpha.types.vulnerability import ListVulnerabilityReportsResponse
from google.cloud.osconfig_v1alpha.types.vulnerability import VulnerabilityReport

__all__ = ('OsConfigZonalServiceClient',
    'OsConfigZonalServiceAsyncClient',
    'OSPolicyResourceCompliance',
    'OSPolicyResourceConfigStep',
    'OSPolicyComplianceState',
    'GetInstanceOSPoliciesComplianceRequest',
    'InstanceOSPoliciesCompliance',
    'ListInstanceOSPoliciesCompliancesRequest',
    'ListInstanceOSPoliciesCompliancesResponse',
    'GetInventoryRequest',
    'Inventory',
    'ListInventoriesRequest',
    'ListInventoriesResponse',
    'InventoryView',
    'OSPolicy',
    'GetOSPolicyAssignmentReportRequest',
    'ListOSPolicyAssignmentReportsRequest',
    'ListOSPolicyAssignmentReportsResponse',
    'OSPolicyAssignmentReport',
    'CreateOSPolicyAssignmentRequest',
    'DeleteOSPolicyAssignmentRequest',
    'GetOSPolicyAssignmentRequest',
    'ListOSPolicyAssignmentRevisionsRequest',
    'ListOSPolicyAssignmentRevisionsResponse',
    'ListOSPolicyAssignmentsRequest',
    'ListOSPolicyAssignmentsResponse',
    'OSPolicyAssignment',
    'OSPolicyAssignmentOperationMetadata',
    'UpdateOSPolicyAssignmentRequest',
    'FixedOrPercent',
    'CVSSv3',
    'GetVulnerabilityReportRequest',
    'ListVulnerabilityReportsRequest',
    'ListVulnerabilityReportsResponse',
    'VulnerabilityReport',
)
