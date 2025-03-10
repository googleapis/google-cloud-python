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
from google.cloud.iam_admin import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.iam_admin_v1.services.iam.client import IAMClient
from google.cloud.iam_admin_v1.services.iam.async_client import IAMAsyncClient

from google.cloud.iam_admin_v1.types.audit_data import AuditData
from google.cloud.iam_admin_v1.types.iam import CreateRoleRequest
from google.cloud.iam_admin_v1.types.iam import CreateServiceAccountKeyRequest
from google.cloud.iam_admin_v1.types.iam import CreateServiceAccountRequest
from google.cloud.iam_admin_v1.types.iam import DeleteRoleRequest
from google.cloud.iam_admin_v1.types.iam import DeleteServiceAccountKeyRequest
from google.cloud.iam_admin_v1.types.iam import DeleteServiceAccountRequest
from google.cloud.iam_admin_v1.types.iam import DisableServiceAccountKeyRequest
from google.cloud.iam_admin_v1.types.iam import DisableServiceAccountRequest
from google.cloud.iam_admin_v1.types.iam import EnableServiceAccountKeyRequest
from google.cloud.iam_admin_v1.types.iam import EnableServiceAccountRequest
from google.cloud.iam_admin_v1.types.iam import GetRoleRequest
from google.cloud.iam_admin_v1.types.iam import GetServiceAccountKeyRequest
from google.cloud.iam_admin_v1.types.iam import GetServiceAccountRequest
from google.cloud.iam_admin_v1.types.iam import LintPolicyRequest
from google.cloud.iam_admin_v1.types.iam import LintPolicyResponse
from google.cloud.iam_admin_v1.types.iam import LintResult
from google.cloud.iam_admin_v1.types.iam import ListRolesRequest
from google.cloud.iam_admin_v1.types.iam import ListRolesResponse
from google.cloud.iam_admin_v1.types.iam import ListServiceAccountKeysRequest
from google.cloud.iam_admin_v1.types.iam import ListServiceAccountKeysResponse
from google.cloud.iam_admin_v1.types.iam import ListServiceAccountsRequest
from google.cloud.iam_admin_v1.types.iam import ListServiceAccountsResponse
from google.cloud.iam_admin_v1.types.iam import PatchServiceAccountRequest
from google.cloud.iam_admin_v1.types.iam import Permission
from google.cloud.iam_admin_v1.types.iam import QueryAuditableServicesRequest
from google.cloud.iam_admin_v1.types.iam import QueryAuditableServicesResponse
from google.cloud.iam_admin_v1.types.iam import QueryGrantableRolesRequest
from google.cloud.iam_admin_v1.types.iam import QueryGrantableRolesResponse
from google.cloud.iam_admin_v1.types.iam import QueryTestablePermissionsRequest
from google.cloud.iam_admin_v1.types.iam import QueryTestablePermissionsResponse
from google.cloud.iam_admin_v1.types.iam import Role
from google.cloud.iam_admin_v1.types.iam import ServiceAccount
from google.cloud.iam_admin_v1.types.iam import ServiceAccountKey
from google.cloud.iam_admin_v1.types.iam import SignBlobRequest
from google.cloud.iam_admin_v1.types.iam import SignBlobResponse
from google.cloud.iam_admin_v1.types.iam import SignJwtRequest
from google.cloud.iam_admin_v1.types.iam import SignJwtResponse
from google.cloud.iam_admin_v1.types.iam import UndeleteRoleRequest
from google.cloud.iam_admin_v1.types.iam import UndeleteServiceAccountRequest
from google.cloud.iam_admin_v1.types.iam import UndeleteServiceAccountResponse
from google.cloud.iam_admin_v1.types.iam import UpdateRoleRequest
from google.cloud.iam_admin_v1.types.iam import UploadServiceAccountKeyRequest
from google.cloud.iam_admin_v1.types.iam import RoleView
from google.cloud.iam_admin_v1.types.iam import ServiceAccountKeyAlgorithm
from google.cloud.iam_admin_v1.types.iam import ServiceAccountKeyOrigin
from google.cloud.iam_admin_v1.types.iam import ServiceAccountPrivateKeyType
from google.cloud.iam_admin_v1.types.iam import ServiceAccountPublicKeyType

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
