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
from google.cloud.iam_v3beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.policy_bindings import PolicyBindingsClient
from .services.policy_bindings import PolicyBindingsAsyncClient
from .services.principal_access_boundary_policies import PrincipalAccessBoundaryPoliciesClient
from .services.principal_access_boundary_policies import PrincipalAccessBoundaryPoliciesAsyncClient

from .types.operation_metadata import OperationMetadata
from .types.policy_binding_resources import PolicyBinding
from .types.policy_bindings_service import CreatePolicyBindingRequest
from .types.policy_bindings_service import DeletePolicyBindingRequest
from .types.policy_bindings_service import GetPolicyBindingRequest
from .types.policy_bindings_service import ListPolicyBindingsRequest
from .types.policy_bindings_service import ListPolicyBindingsResponse
from .types.policy_bindings_service import SearchTargetPolicyBindingsRequest
from .types.policy_bindings_service import SearchTargetPolicyBindingsResponse
from .types.policy_bindings_service import UpdatePolicyBindingRequest
from .types.principal_access_boundary_policies_service import CreatePrincipalAccessBoundaryPolicyRequest
from .types.principal_access_boundary_policies_service import DeletePrincipalAccessBoundaryPolicyRequest
from .types.principal_access_boundary_policies_service import GetPrincipalAccessBoundaryPolicyRequest
from .types.principal_access_boundary_policies_service import ListPrincipalAccessBoundaryPoliciesRequest
from .types.principal_access_boundary_policies_service import ListPrincipalAccessBoundaryPoliciesResponse
from .types.principal_access_boundary_policies_service import SearchPrincipalAccessBoundaryPolicyBindingsRequest
from .types.principal_access_boundary_policies_service import SearchPrincipalAccessBoundaryPolicyBindingsResponse
from .types.principal_access_boundary_policies_service import UpdatePrincipalAccessBoundaryPolicyRequest
from .types.principal_access_boundary_policy_resources import PrincipalAccessBoundaryPolicy
from .types.principal_access_boundary_policy_resources import PrincipalAccessBoundaryPolicyDetails
from .types.principal_access_boundary_policy_resources import PrincipalAccessBoundaryPolicyRule

__all__ = (
    'PolicyBindingsAsyncClient',
    'PrincipalAccessBoundaryPoliciesAsyncClient',
'CreatePolicyBindingRequest',
'CreatePrincipalAccessBoundaryPolicyRequest',
'DeletePolicyBindingRequest',
'DeletePrincipalAccessBoundaryPolicyRequest',
'GetPolicyBindingRequest',
'GetPrincipalAccessBoundaryPolicyRequest',
'ListPolicyBindingsRequest',
'ListPolicyBindingsResponse',
'ListPrincipalAccessBoundaryPoliciesRequest',
'ListPrincipalAccessBoundaryPoliciesResponse',
'OperationMetadata',
'PolicyBinding',
'PolicyBindingsClient',
'PrincipalAccessBoundaryPoliciesClient',
'PrincipalAccessBoundaryPolicy',
'PrincipalAccessBoundaryPolicyDetails',
'PrincipalAccessBoundaryPolicyRule',
'SearchPrincipalAccessBoundaryPolicyBindingsRequest',
'SearchPrincipalAccessBoundaryPolicyBindingsResponse',
'SearchTargetPolicyBindingsRequest',
'SearchTargetPolicyBindingsResponse',
'UpdatePolicyBindingRequest',
'UpdatePrincipalAccessBoundaryPolicyRequest',
)
