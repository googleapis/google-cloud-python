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
from google.iam.admin import gapic_version as package_version

__version__ = package_version.__version__


from google.iam.admin_v1.services.iam.client import IAMClient
from google.iam.admin_v1.services.iam.async_client import IAMAsyncClient

from google.iam.admin_v1.types.audit_data import AuditData
from google.iam.admin_v1.types.iam import CreateRoleRequest
from google.iam.admin_v1.types.iam import CreateServiceAccountKeyRequest
from google.iam.admin_v1.types.iam import CreateServiceAccountRequest
from google.iam.admin_v1.types.iam import DeleteRoleRequest
from google.iam.admin_v1.types.iam import DeleteServiceAccountKeyRequest
from google.iam.admin_v1.types.iam import DeleteServiceAccountRequest
from google.iam.admin_v1.types.iam import DisableServiceAccountKeyRequest
from google.iam.admin_v1.types.iam import DisableServiceAccountRequest
from google.iam.admin_v1.types.iam import EnableServiceAccountKeyRequest
from google.iam.admin_v1.types.iam import EnableServiceAccountRequest
from google.iam.admin_v1.types.iam import GetRoleRequest
from google.iam.admin_v1.types.iam import GetServiceAccountKeyRequest
from google.iam.admin_v1.types.iam import GetServiceAccountRequest
from google.iam.admin_v1.types.iam import LintPolicyRequest
from google.iam.admin_v1.types.iam import LintPolicyResponse
from google.iam.admin_v1.types.iam import LintResult
from google.iam.admin_v1.types.iam import ListRolesRequest
from google.iam.admin_v1.types.iam import ListRolesResponse
from google.iam.admin_v1.types.iam import ListServiceAccountKeysRequest
from google.iam.admin_v1.types.iam import ListServiceAccountKeysResponse
from google.iam.admin_v1.types.iam import ListServiceAccountsRequest
from google.iam.admin_v1.types.iam import ListServiceAccountsResponse
from google.iam.admin_v1.types.iam import PatchServiceAccountRequest
from google.iam.admin_v1.types.iam import Permission
from google.iam.admin_v1.types.iam import QueryAuditableServicesRequest
from google.iam.admin_v1.types.iam import QueryAuditableServicesResponse
from google.iam.admin_v1.types.iam import QueryGrantableRolesRequest
from google.iam.admin_v1.types.iam import QueryGrantableRolesResponse
from google.iam.admin_v1.types.iam import QueryTestablePermissionsRequest
from google.iam.admin_v1.types.iam import QueryTestablePermissionsResponse
from google.iam.admin_v1.types.iam import Role
from google.iam.admin_v1.types.iam import ServiceAccount
from google.iam.admin_v1.types.iam import ServiceAccountKey
from google.iam.admin_v1.types.iam import SignBlobRequest
from google.iam.admin_v1.types.iam import SignBlobResponse
from google.iam.admin_v1.types.iam import SignJwtRequest
from google.iam.admin_v1.types.iam import SignJwtResponse
from google.iam.admin_v1.types.iam import UndeleteRoleRequest
from google.iam.admin_v1.types.iam import UndeleteServiceAccountRequest
from google.iam.admin_v1.types.iam import UndeleteServiceAccountResponse
from google.iam.admin_v1.types.iam import UpdateRoleRequest
from google.iam.admin_v1.types.iam import UploadServiceAccountKeyRequest
from google.iam.admin_v1.types.iam import RoleView
from google.iam.admin_v1.types.iam import ServiceAccountKeyAlgorithm
from google.iam.admin_v1.types.iam import ServiceAccountKeyOrigin
from google.iam.admin_v1.types.iam import ServiceAccountPrivateKeyType
from google.iam.admin_v1.types.iam import ServiceAccountPublicKeyType

__all__ = ('IAMClient',
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
    'ServiceAccount',
    'ServiceAccountKey',
    'SignBlobRequest',
    'SignBlobResponse',
    'SignJwtRequest',
    'SignJwtResponse',
    'UndeleteRoleRequest',
    'UndeleteServiceAccountRequest',
    'UndeleteServiceAccountResponse',
    'UpdateRoleRequest',
    'UploadServiceAccountKeyRequest',
    'RoleView',
    'ServiceAccountKeyAlgorithm',
    'ServiceAccountKeyOrigin',
    'ServiceAccountPrivateKeyType',
    'ServiceAccountPublicKeyType',
)
