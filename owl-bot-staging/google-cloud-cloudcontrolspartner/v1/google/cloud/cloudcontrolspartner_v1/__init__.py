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


from .services.cloud_controls_partner_core import CloudControlsPartnerCoreClient
from .services.cloud_controls_partner_core import CloudControlsPartnerCoreAsyncClient
from .services.cloud_controls_partner_monitoring import CloudControlsPartnerMonitoringClient
from .services.cloud_controls_partner_monitoring import CloudControlsPartnerMonitoringAsyncClient

from .types.access_approval_requests import AccessApprovalRequest
from .types.access_approval_requests import AccessReason
from .types.access_approval_requests import ListAccessApprovalRequestsRequest
from .types.access_approval_requests import ListAccessApprovalRequestsResponse
from .types.completion_state import CompletionState
from .types.core import OperationMetadata
from .types.customer_workloads import GetWorkloadRequest
from .types.customer_workloads import ListWorkloadsRequest
from .types.customer_workloads import ListWorkloadsResponse
from .types.customer_workloads import Workload
from .types.customer_workloads import WorkloadOnboardingState
from .types.customer_workloads import WorkloadOnboardingStep
from .types.customers import Customer
from .types.customers import CustomerOnboardingState
from .types.customers import CustomerOnboardingStep
from .types.customers import GetCustomerRequest
from .types.customers import ListCustomersRequest
from .types.customers import ListCustomersResponse
from .types.ekm_connections import EkmConnection
from .types.ekm_connections import EkmConnections
from .types.ekm_connections import GetEkmConnectionsRequest
from .types.partner_permissions import GetPartnerPermissionsRequest
from .types.partner_permissions import PartnerPermissions
from .types.partners import EkmMetadata
from .types.partners import GetPartnerRequest
from .types.partners import Partner
from .types.partners import Sku
from .types.violations import GetViolationRequest
from .types.violations import ListViolationsRequest
from .types.violations import ListViolationsResponse
from .types.violations import Violation

__all__ = (
    'CloudControlsPartnerCoreAsyncClient',
    'CloudControlsPartnerMonitoringAsyncClient',
'AccessApprovalRequest',
'AccessReason',
'CloudControlsPartnerCoreClient',
'CloudControlsPartnerMonitoringClient',
'CompletionState',
'Customer',
'CustomerOnboardingState',
'CustomerOnboardingStep',
'EkmConnection',
'EkmConnections',
'EkmMetadata',
'GetCustomerRequest',
'GetEkmConnectionsRequest',
'GetPartnerPermissionsRequest',
'GetPartnerRequest',
'GetViolationRequest',
'GetWorkloadRequest',
'ListAccessApprovalRequestsRequest',
'ListAccessApprovalRequestsResponse',
'ListCustomersRequest',
'ListCustomersResponse',
'ListViolationsRequest',
'ListViolationsResponse',
'ListWorkloadsRequest',
'ListWorkloadsResponse',
'OperationMetadata',
'Partner',
'PartnerPermissions',
'Sku',
'Violation',
'Workload',
'WorkloadOnboardingState',
'WorkloadOnboardingStep',
)
