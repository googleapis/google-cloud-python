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
from google.cloud.cloudcontrolspartner import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.cloudcontrolspartner_v1beta.services.cloud_controls_partner_core.client import CloudControlsPartnerCoreClient
from google.cloud.cloudcontrolspartner_v1beta.services.cloud_controls_partner_core.async_client import CloudControlsPartnerCoreAsyncClient
from google.cloud.cloudcontrolspartner_v1beta.services.cloud_controls_partner_monitoring.client import CloudControlsPartnerMonitoringClient
from google.cloud.cloudcontrolspartner_v1beta.services.cloud_controls_partner_monitoring.async_client import CloudControlsPartnerMonitoringAsyncClient

from google.cloud.cloudcontrolspartner_v1beta.types.access_approval_requests import AccessApprovalRequest
from google.cloud.cloudcontrolspartner_v1beta.types.access_approval_requests import AccessReason
from google.cloud.cloudcontrolspartner_v1beta.types.access_approval_requests import ListAccessApprovalRequestsRequest
from google.cloud.cloudcontrolspartner_v1beta.types.access_approval_requests import ListAccessApprovalRequestsResponse
from google.cloud.cloudcontrolspartner_v1beta.types.completion_state import CompletionState
from google.cloud.cloudcontrolspartner_v1beta.types.core import OperationMetadata
from google.cloud.cloudcontrolspartner_v1beta.types.customer_workloads import GetWorkloadRequest
from google.cloud.cloudcontrolspartner_v1beta.types.customer_workloads import ListWorkloadsRequest
from google.cloud.cloudcontrolspartner_v1beta.types.customer_workloads import ListWorkloadsResponse
from google.cloud.cloudcontrolspartner_v1beta.types.customer_workloads import Workload
from google.cloud.cloudcontrolspartner_v1beta.types.customer_workloads import WorkloadOnboardingState
from google.cloud.cloudcontrolspartner_v1beta.types.customer_workloads import WorkloadOnboardingStep
from google.cloud.cloudcontrolspartner_v1beta.types.customers import Customer
from google.cloud.cloudcontrolspartner_v1beta.types.customers import CustomerOnboardingState
from google.cloud.cloudcontrolspartner_v1beta.types.customers import CustomerOnboardingStep
from google.cloud.cloudcontrolspartner_v1beta.types.customers import GetCustomerRequest
from google.cloud.cloudcontrolspartner_v1beta.types.customers import ListCustomersRequest
from google.cloud.cloudcontrolspartner_v1beta.types.customers import ListCustomersResponse
from google.cloud.cloudcontrolspartner_v1beta.types.ekm_connections import EkmConnection
from google.cloud.cloudcontrolspartner_v1beta.types.ekm_connections import EkmConnections
from google.cloud.cloudcontrolspartner_v1beta.types.ekm_connections import GetEkmConnectionsRequest
from google.cloud.cloudcontrolspartner_v1beta.types.partner_permissions import GetPartnerPermissionsRequest
from google.cloud.cloudcontrolspartner_v1beta.types.partner_permissions import PartnerPermissions
from google.cloud.cloudcontrolspartner_v1beta.types.partners import EkmMetadata
from google.cloud.cloudcontrolspartner_v1beta.types.partners import GetPartnerRequest
from google.cloud.cloudcontrolspartner_v1beta.types.partners import Partner
from google.cloud.cloudcontrolspartner_v1beta.types.partners import Sku
from google.cloud.cloudcontrolspartner_v1beta.types.violations import GetViolationRequest
from google.cloud.cloudcontrolspartner_v1beta.types.violations import ListViolationsRequest
from google.cloud.cloudcontrolspartner_v1beta.types.violations import ListViolationsResponse
from google.cloud.cloudcontrolspartner_v1beta.types.violations import Violation

__all__ = ('CloudControlsPartnerCoreClient',
    'CloudControlsPartnerCoreAsyncClient',
    'CloudControlsPartnerMonitoringClient',
    'CloudControlsPartnerMonitoringAsyncClient',
    'AccessApprovalRequest',
    'AccessReason',
    'ListAccessApprovalRequestsRequest',
    'ListAccessApprovalRequestsResponse',
    'CompletionState',
    'OperationMetadata',
    'GetWorkloadRequest',
    'ListWorkloadsRequest',
    'ListWorkloadsResponse',
    'Workload',
    'WorkloadOnboardingState',
    'WorkloadOnboardingStep',
    'Customer',
    'CustomerOnboardingState',
    'CustomerOnboardingStep',
    'GetCustomerRequest',
    'ListCustomersRequest',
    'ListCustomersResponse',
    'EkmConnection',
    'EkmConnections',
    'GetEkmConnectionsRequest',
    'GetPartnerPermissionsRequest',
    'PartnerPermissions',
    'EkmMetadata',
    'GetPartnerRequest',
    'Partner',
    'Sku',
    'GetViolationRequest',
    'ListViolationsRequest',
    'ListViolationsResponse',
    'Violation',
)
