# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from .services.os_config_zonal_service import OsConfigZonalServiceClient
from .services.os_config_zonal_service import OsConfigZonalServiceAsyncClient

from .types.config_common import OSPolicyResourceCompliance
from .types.config_common import OSPolicyResourceConfigStep
from .types.config_common import OSPolicyComplianceState
from .types.instance_os_policies_compliance import (
    GetInstanceOSPoliciesComplianceRequest,
)
from .types.instance_os_policies_compliance import InstanceOSPoliciesCompliance
from .types.instance_os_policies_compliance import (
    ListInstanceOSPoliciesCompliancesRequest,
)
from .types.instance_os_policies_compliance import (
    ListInstanceOSPoliciesCompliancesResponse,
)
from .types.inventory import GetInventoryRequest
from .types.inventory import Inventory
from .types.inventory import ListInventoriesRequest
from .types.inventory import ListInventoriesResponse
from .types.inventory import InventoryView
from .types.os_policy import OSPolicy
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
from .types.vulnerability import CVSSv3
from .types.vulnerability import GetVulnerabilityReportRequest
from .types.vulnerability import ListVulnerabilityReportsRequest
from .types.vulnerability import ListVulnerabilityReportsResponse
from .types.vulnerability import VulnerabilityReport

__all__ = (
    "OsConfigZonalServiceAsyncClient",
    "CVSSv3",
    "CreateOSPolicyAssignmentRequest",
    "DeleteOSPolicyAssignmentRequest",
    "FixedOrPercent",
    "GetInstanceOSPoliciesComplianceRequest",
    "GetInventoryRequest",
    "GetOSPolicyAssignmentRequest",
    "GetVulnerabilityReportRequest",
    "InstanceOSPoliciesCompliance",
    "Inventory",
    "InventoryView",
    "ListInstanceOSPoliciesCompliancesRequest",
    "ListInstanceOSPoliciesCompliancesResponse",
    "ListInventoriesRequest",
    "ListInventoriesResponse",
    "ListOSPolicyAssignmentRevisionsRequest",
    "ListOSPolicyAssignmentRevisionsResponse",
    "ListOSPolicyAssignmentsRequest",
    "ListOSPolicyAssignmentsResponse",
    "ListVulnerabilityReportsRequest",
    "ListVulnerabilityReportsResponse",
    "OSPolicy",
    "OSPolicyAssignment",
    "OSPolicyAssignmentOperationMetadata",
    "OSPolicyComplianceState",
    "OSPolicyResourceCompliance",
    "OSPolicyResourceConfigStep",
    "OsConfigZonalServiceClient",
    "UpdateOSPolicyAssignmentRequest",
    "VulnerabilityReport",
)
