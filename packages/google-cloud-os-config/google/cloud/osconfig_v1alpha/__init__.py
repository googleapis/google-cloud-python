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
from google.cloud.osconfig_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.os_config_zonal_service import (
    OsConfigZonalServiceAsyncClient,
    OsConfigZonalServiceClient,
)
from .types.config_common import (
    OSPolicyComplianceState,
    OSPolicyResourceCompliance,
    OSPolicyResourceConfigStep,
)
from .types.instance_os_policies_compliance import (
    GetInstanceOSPoliciesComplianceRequest,
    InstanceOSPoliciesCompliance,
    ListInstanceOSPoliciesCompliancesRequest,
    ListInstanceOSPoliciesCompliancesResponse,
)
from .types.inventory import (
    GetInventoryRequest,
    Inventory,
    InventoryView,
    ListInventoriesRequest,
    ListInventoriesResponse,
)
from .types.os_policy import OSPolicy
from .types.os_policy_assignment_reports import (
    GetOSPolicyAssignmentReportRequest,
    ListOSPolicyAssignmentReportsRequest,
    ListOSPolicyAssignmentReportsResponse,
    OSPolicyAssignmentReport,
)
from .types.os_policy_assignments import (
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
from .types.osconfig_common import FixedOrPercent
from .types.vulnerability import (
    CVSSv3,
    GetVulnerabilityReportRequest,
    ListVulnerabilityReportsRequest,
    ListVulnerabilityReportsResponse,
    VulnerabilityReport,
)

__all__ = (
    "OsConfigZonalServiceAsyncClient",
    "CVSSv3",
    "CreateOSPolicyAssignmentRequest",
    "DeleteOSPolicyAssignmentRequest",
    "FixedOrPercent",
    "GetInstanceOSPoliciesComplianceRequest",
    "GetInventoryRequest",
    "GetOSPolicyAssignmentReportRequest",
    "GetOSPolicyAssignmentRequest",
    "GetVulnerabilityReportRequest",
    "InstanceOSPoliciesCompliance",
    "Inventory",
    "InventoryView",
    "ListInstanceOSPoliciesCompliancesRequest",
    "ListInstanceOSPoliciesCompliancesResponse",
    "ListInventoriesRequest",
    "ListInventoriesResponse",
    "ListOSPolicyAssignmentReportsRequest",
    "ListOSPolicyAssignmentReportsResponse",
    "ListOSPolicyAssignmentRevisionsRequest",
    "ListOSPolicyAssignmentRevisionsResponse",
    "ListOSPolicyAssignmentsRequest",
    "ListOSPolicyAssignmentsResponse",
    "ListVulnerabilityReportsRequest",
    "ListVulnerabilityReportsResponse",
    "OSPolicy",
    "OSPolicyAssignment",
    "OSPolicyAssignmentOperationMetadata",
    "OSPolicyAssignmentReport",
    "OSPolicyComplianceState",
    "OSPolicyResourceCompliance",
    "OSPolicyResourceConfigStep",
    "OsConfigZonalServiceClient",
    "UpdateOSPolicyAssignmentRequest",
    "VulnerabilityReport",
)
