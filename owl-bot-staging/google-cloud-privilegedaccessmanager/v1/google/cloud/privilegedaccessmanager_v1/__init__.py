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
from google.cloud.privilegedaccessmanager_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.privileged_access_manager import PrivilegedAccessManagerClient
from .services.privileged_access_manager import PrivilegedAccessManagerAsyncClient

from .types.privilegedaccessmanager import AccessControlEntry
from .types.privilegedaccessmanager import ApprovalWorkflow
from .types.privilegedaccessmanager import ApproveGrantRequest
from .types.privilegedaccessmanager import CheckOnboardingStatusRequest
from .types.privilegedaccessmanager import CheckOnboardingStatusResponse
from .types.privilegedaccessmanager import CreateEntitlementRequest
from .types.privilegedaccessmanager import CreateGrantRequest
from .types.privilegedaccessmanager import DeleteEntitlementRequest
from .types.privilegedaccessmanager import DenyGrantRequest
from .types.privilegedaccessmanager import Entitlement
from .types.privilegedaccessmanager import GetEntitlementRequest
from .types.privilegedaccessmanager import GetGrantRequest
from .types.privilegedaccessmanager import Grant
from .types.privilegedaccessmanager import Justification
from .types.privilegedaccessmanager import ListEntitlementsRequest
from .types.privilegedaccessmanager import ListEntitlementsResponse
from .types.privilegedaccessmanager import ListGrantsRequest
from .types.privilegedaccessmanager import ListGrantsResponse
from .types.privilegedaccessmanager import ManualApprovals
from .types.privilegedaccessmanager import OperationMetadata
from .types.privilegedaccessmanager import PrivilegedAccess
from .types.privilegedaccessmanager import RevokeGrantRequest
from .types.privilegedaccessmanager import SearchEntitlementsRequest
from .types.privilegedaccessmanager import SearchEntitlementsResponse
from .types.privilegedaccessmanager import SearchGrantsRequest
from .types.privilegedaccessmanager import SearchGrantsResponse
from .types.privilegedaccessmanager import UpdateEntitlementRequest

__all__ = (
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
'PrivilegedAccessManagerClient',
'RevokeGrantRequest',
'SearchEntitlementsRequest',
'SearchEntitlementsResponse',
'SearchGrantsRequest',
'SearchGrantsResponse',
'UpdateEntitlementRequest',
)
