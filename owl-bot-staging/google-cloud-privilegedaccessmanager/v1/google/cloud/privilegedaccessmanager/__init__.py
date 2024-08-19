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
from google.cloud.privilegedaccessmanager import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.privilegedaccessmanager_v1.services.privileged_access_manager.client import PrivilegedAccessManagerClient
from google.cloud.privilegedaccessmanager_v1.services.privileged_access_manager.async_client import PrivilegedAccessManagerAsyncClient

from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import AccessControlEntry
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import ApprovalWorkflow
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import ApproveGrantRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import CheckOnboardingStatusRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import CheckOnboardingStatusResponse
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import CreateEntitlementRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import CreateGrantRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import DeleteEntitlementRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import DenyGrantRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import Entitlement
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import GetEntitlementRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import GetGrantRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import Grant
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import Justification
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import ListEntitlementsRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import ListEntitlementsResponse
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import ListGrantsRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import ListGrantsResponse
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import ManualApprovals
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import OperationMetadata
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import PrivilegedAccess
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import RevokeGrantRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import SearchEntitlementsRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import SearchEntitlementsResponse
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import SearchGrantsRequest
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import SearchGrantsResponse
from google.cloud.privilegedaccessmanager_v1.types.privilegedaccessmanager import UpdateEntitlementRequest

__all__ = ('PrivilegedAccessManagerClient',
    'PrivilegedAccessManagerAsyncClient',
    'AccessControlEntry',
    'ApprovalWorkflow',
    'ApproveGrantRequest',
    'CheckOnboardingStatusRequest',
    'CheckOnboardingStatusResponse',
    'CreateEntitlementRequest',
    'CreateGrantRequest',
    'DeleteEntitlementRequest',
    'DenyGrantRequest',
    'Entitlement',
    'GetEntitlementRequest',
    'GetGrantRequest',
    'Grant',
    'Justification',
    'ListEntitlementsRequest',
    'ListEntitlementsResponse',
    'ListGrantsRequest',
    'ListGrantsResponse',
    'ManualApprovals',
    'OperationMetadata',
    'PrivilegedAccess',
    'RevokeGrantRequest',
    'SearchEntitlementsRequest',
    'SearchEntitlementsResponse',
    'SearchGrantsRequest',
    'SearchGrantsResponse',
    'UpdateEntitlementRequest',
)
