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
from .config_common import (
    OSPolicyResourceCompliance,
    OSPolicyResourceConfigStep,
    OSPolicyComplianceState,
)
from .instance_os_policies_compliance import (
    GetInstanceOSPoliciesComplianceRequest,
    InstanceOSPoliciesCompliance,
    ListInstanceOSPoliciesCompliancesRequest,
    ListInstanceOSPoliciesCompliancesResponse,
)
from .inventory import (
    GetInventoryRequest,
    Inventory,
    ListInventoriesRequest,
    ListInventoriesResponse,
    InventoryView,
)
from .os_policy import (
    OSPolicy,
)
from .os_policy_assignment_reports import (
    GetOSPolicyAssignmentReportRequest,
    ListOSPolicyAssignmentReportsRequest,
    ListOSPolicyAssignmentReportsResponse,
    OSPolicyAssignmentReport,
)
from .os_policy_assignments import (
    CreateOSPolicyAssignmentRequest,
    DeleteOSPolicyAssignmentRequest,
    GetOSPolicyAssignmentRequest,
    ListOSPolicyAssignmentRevisionsRequest,
    ListOSPolicyAssignmentRevisionsResponse,
    ListOSPolicyAssignmentsRequest,
    ListOSPolicyAssignmentsResponse,
    OSPolicyAssignment,
    OSPolicyAssignmentOperationMetadata,
    UpdateOSPolicyAssignmentRequest,
)
from .osconfig_common import (
    FixedOrPercent,
)
from .vulnerability import (
    CVSSv3,
    GetVulnerabilityReportRequest,
    ListVulnerabilityReportsRequest,
    ListVulnerabilityReportsResponse,
    VulnerabilityReport,
)

__all__ = (
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
