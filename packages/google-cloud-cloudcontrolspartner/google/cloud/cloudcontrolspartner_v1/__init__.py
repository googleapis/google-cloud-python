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
from google.cloud.cloudcontrolspartner_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_controls_partner_core import (
    CloudControlsPartnerCoreAsyncClient,
    CloudControlsPartnerCoreClient,
)
from .services.cloud_controls_partner_monitoring import (
    CloudControlsPartnerMonitoringAsyncClient,
    CloudControlsPartnerMonitoringClient,
)
from .types.access_approval_requests import (
    AccessApprovalRequest,
    AccessReason,
    ListAccessApprovalRequestsRequest,
    ListAccessApprovalRequestsResponse,
)
from .types.completion_state import CompletionState
from .types.core import OperationMetadata
from .types.customer_workloads import (
    GetWorkloadRequest,
    ListWorkloadsRequest,
    ListWorkloadsResponse,
    Workload,
    WorkloadOnboardingState,
    WorkloadOnboardingStep,
)
from .types.customers import (
    Customer,
    CustomerOnboardingState,
    CustomerOnboardingStep,
    GetCustomerRequest,
    ListCustomersRequest,
    ListCustomersResponse,
)
from .types.ekm_connections import (
    EkmConnection,
    EkmConnections,
    GetEkmConnectionsRequest,
)
from .types.partner_permissions import GetPartnerPermissionsRequest, PartnerPermissions
from .types.partners import EkmMetadata, GetPartnerRequest, Partner, Sku
from .types.violations import (
    GetViolationRequest,
    ListViolationsRequest,
    ListViolationsResponse,
    Violation,
)

__all__ = (
    "CloudControlsPartnerCoreAsyncClient",
    "CloudControlsPartnerMonitoringAsyncClient",
    "AccessApprovalRequest",
    "AccessReason",
    "CloudControlsPartnerCoreClient",
    "CloudControlsPartnerMonitoringClient",
    "CompletionState",
    "Customer",
    "CustomerOnboardingState",
    "CustomerOnboardingStep",
    "EkmConnection",
    "EkmConnections",
    "EkmMetadata",
    "GetCustomerRequest",
    "GetEkmConnectionsRequest",
    "GetPartnerPermissionsRequest",
    "GetPartnerRequest",
    "GetViolationRequest",
    "GetWorkloadRequest",
    "ListAccessApprovalRequestsRequest",
    "ListAccessApprovalRequestsResponse",
    "ListCustomersRequest",
    "ListCustomersResponse",
    "ListViolationsRequest",
    "ListViolationsResponse",
    "ListWorkloadsRequest",
    "ListWorkloadsResponse",
    "OperationMetadata",
    "Partner",
    "PartnerPermissions",
    "Sku",
    "Violation",
    "Workload",
    "WorkloadOnboardingState",
    "WorkloadOnboardingStep",
)
