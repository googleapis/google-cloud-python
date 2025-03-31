# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.iam import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.iam_v3beta.services.policy_bindings.client import PolicyBindingsClient
from google.cloud.iam_v3beta.services.policy_bindings.async_client import PolicyBindingsAsyncClient
from google.cloud.iam_v3beta.services.principal_access_boundary_policies.client import PrincipalAccessBoundaryPoliciesClient
from google.cloud.iam_v3beta.services.principal_access_boundary_policies.async_client import PrincipalAccessBoundaryPoliciesAsyncClient

from google.cloud.iam_v3beta.types.operation_metadata import OperationMetadata
from google.cloud.iam_v3beta.types.policy_binding_resources import PolicyBinding
from google.cloud.iam_v3beta.types.policy_bindings_service import CreatePolicyBindingRequest
from google.cloud.iam_v3beta.types.policy_bindings_service import DeletePolicyBindingRequest
from google.cloud.iam_v3beta.types.policy_bindings_service import GetPolicyBindingRequest
from google.cloud.iam_v3beta.types.policy_bindings_service import ListPolicyBindingsRequest
from google.cloud.iam_v3beta.types.policy_bindings_service import ListPolicyBindingsResponse
from google.cloud.iam_v3beta.types.policy_bindings_service import SearchTargetPolicyBindingsRequest
from google.cloud.iam_v3beta.types.policy_bindings_service import SearchTargetPolicyBindingsResponse
from google.cloud.iam_v3beta.types.policy_bindings_service import UpdatePolicyBindingRequest
from google.cloud.iam_v3beta.types.principal_access_boundary_policies_service import CreatePrincipalAccessBoundaryPolicyRequest
from google.cloud.iam_v3beta.types.principal_access_boundary_policies_service import DeletePrincipalAccessBoundaryPolicyRequest
from google.cloud.iam_v3beta.types.principal_access_boundary_policies_service import GetPrincipalAccessBoundaryPolicyRequest
from google.cloud.iam_v3beta.types.principal_access_boundary_policies_service import ListPrincipalAccessBoundaryPoliciesRequest
from google.cloud.iam_v3beta.types.principal_access_boundary_policies_service import ListPrincipalAccessBoundaryPoliciesResponse
from google.cloud.iam_v3beta.types.principal_access_boundary_policies_service import SearchPrincipalAccessBoundaryPolicyBindingsRequest
from google.cloud.iam_v3beta.types.principal_access_boundary_policies_service import SearchPrincipalAccessBoundaryPolicyBindingsResponse
from google.cloud.iam_v3beta.types.principal_access_boundary_policies_service import UpdatePrincipalAccessBoundaryPolicyRequest
from google.cloud.iam_v3beta.types.principal_access_boundary_policy_resources import PrincipalAccessBoundaryPolicy
from google.cloud.iam_v3beta.types.principal_access_boundary_policy_resources import PrincipalAccessBoundaryPolicyDetails
from google.cloud.iam_v3beta.types.principal_access_boundary_policy_resources import PrincipalAccessBoundaryPolicyRule

__all__ = ('PolicyBindingsClient',
    'PolicyBindingsAsyncClient',
    'PrincipalAccessBoundaryPoliciesClient',
    'PrincipalAccessBoundaryPoliciesAsyncClient',
    'OperationMetadata',
    'PolicyBinding',
    'CreatePolicyBindingRequest',
    'DeletePolicyBindingRequest',
    'GetPolicyBindingRequest',
    'ListPolicyBindingsRequest',
    'ListPolicyBindingsResponse',
    'SearchTargetPolicyBindingsRequest',
    'SearchTargetPolicyBindingsResponse',
    'UpdatePolicyBindingRequest',
    'CreatePrincipalAccessBoundaryPolicyRequest',
    'DeletePrincipalAccessBoundaryPolicyRequest',
    'GetPrincipalAccessBoundaryPolicyRequest',
    'ListPrincipalAccessBoundaryPoliciesRequest',
    'ListPrincipalAccessBoundaryPoliciesResponse',
    'SearchPrincipalAccessBoundaryPolicyBindingsRequest',
    'SearchPrincipalAccessBoundaryPolicyBindingsResponse',
    'UpdatePrincipalAccessBoundaryPolicyRequest',
    'PrincipalAccessBoundaryPolicy',
    'PrincipalAccessBoundaryPolicyDetails',
    'PrincipalAccessBoundaryPolicyRule',
)
