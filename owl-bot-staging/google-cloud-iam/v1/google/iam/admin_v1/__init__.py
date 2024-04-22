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
from google.iam.admin_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.iam import IAMClient
from .services.iam import IAMAsyncClient

from .types.audit_data import AuditData
from .types.iam import CreateRoleRequest
from .types.iam import CreateServiceAccountKeyRequest
from .types.iam import CreateServiceAccountRequest
from .types.iam import DeleteRoleRequest
from .types.iam import DeleteServiceAccountKeyRequest
from .types.iam import DeleteServiceAccountRequest
from .types.iam import DisableServiceAccountKeyRequest
from .types.iam import DisableServiceAccountRequest
from .types.iam import EnableServiceAccountKeyRequest
from .types.iam import EnableServiceAccountRequest
from .types.iam import GetRoleRequest
from .types.iam import GetServiceAccountKeyRequest
from .types.iam import GetServiceAccountRequest
from .types.iam import LintPolicyRequest
from .types.iam import LintPolicyResponse
from .types.iam import LintResult
from .types.iam import ListRolesRequest
from .types.iam import ListRolesResponse
from .types.iam import ListServiceAccountKeysRequest
from .types.iam import ListServiceAccountKeysResponse
from .types.iam import ListServiceAccountsRequest
from .types.iam import ListServiceAccountsResponse
from .types.iam import PatchServiceAccountRequest
from .types.iam import Permission
from .types.iam import QueryAuditableServicesRequest
from .types.iam import QueryAuditableServicesResponse
from .types.iam import QueryGrantableRolesRequest
from .types.iam import QueryGrantableRolesResponse
from .types.iam import QueryTestablePermissionsRequest
from .types.iam import QueryTestablePermissionsResponse
from .types.iam import Role
from .types.iam import ServiceAccount
from .types.iam import ServiceAccountKey
from .types.iam import SignBlobRequest
from .types.iam import SignBlobResponse
from .types.iam import SignJwtRequest
from .types.iam import SignJwtResponse
from .types.iam import UndeleteRoleRequest
from .types.iam import UndeleteServiceAccountRequest
from .types.iam import UndeleteServiceAccountResponse
from .types.iam import UpdateRoleRequest
from .types.iam import UploadServiceAccountKeyRequest
from .types.iam import RoleView
from .types.iam import ServiceAccountKeyAlgorithm
from .types.iam import ServiceAccountKeyOrigin
from .types.iam import ServiceAccountPrivateKeyType
from .types.iam import ServiceAccountPublicKeyType

__all__ = (
    'IAMAsyncClient',
'AuditData',
'CreateRoleRequest',
'CreateServiceAccountKeyRequest',
'CreateServiceAccountRequest',
'DeleteRoleRequest',
'DeleteServiceAccountKeyRequest',
'DeleteServiceAccountRequest',
'DisableServiceAccountKeyRequest',
'DisableServiceAccountRequest',
'EnableServiceAccountKeyRequest',
'EnableServiceAccountRequest',
'GetRoleRequest',
'GetServiceAccountKeyRequest',
'GetServiceAccountRequest',
'IAMClient',
'LintPolicyRequest',
'LintPolicyResponse',
'LintResult',
'ListRolesRequest',
'ListRolesResponse',
'ListServiceAccountKeysRequest',
'ListServiceAccountKeysResponse',
'ListServiceAccountsRequest',
'ListServiceAccountsResponse',
'PatchServiceAccountRequest',
'Permission',
'QueryAuditableServicesRequest',
'QueryAuditableServicesResponse',
'QueryGrantableRolesRequest',
'QueryGrantableRolesResponse',
'QueryTestablePermissionsRequest',
'QueryTestablePermissionsResponse',
'Role',
'RoleView',
'ServiceAccount',
'ServiceAccountKey',
'ServiceAccountKeyAlgorithm',
'ServiceAccountKeyOrigin',
'ServiceAccountPrivateKeyType',
'ServiceAccountPublicKeyType',
'SignBlobRequest',
'SignBlobResponse',
'SignJwtRequest',
'SignJwtResponse',
'UndeleteRoleRequest',
'UndeleteServiceAccountRequest',
'UndeleteServiceAccountResponse',
'UpdateRoleRequest',
'UploadServiceAccountKeyRequest',
)
