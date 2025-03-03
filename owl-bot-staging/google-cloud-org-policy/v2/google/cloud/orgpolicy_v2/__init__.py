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
from google.cloud.orgpolicy_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.org_policy import OrgPolicyClient
from .services.org_policy import OrgPolicyAsyncClient

from .types.constraint import Constraint
from .types.constraint import CustomConstraint
from .types.orgpolicy import AlternatePolicySpec
from .types.orgpolicy import CreateCustomConstraintRequest
from .types.orgpolicy import CreatePolicyRequest
from .types.orgpolicy import DeleteCustomConstraintRequest
from .types.orgpolicy import DeletePolicyRequest
from .types.orgpolicy import GetCustomConstraintRequest
from .types.orgpolicy import GetEffectivePolicyRequest
from .types.orgpolicy import GetPolicyRequest
from .types.orgpolicy import ListConstraintsRequest
from .types.orgpolicy import ListConstraintsResponse
from .types.orgpolicy import ListCustomConstraintsRequest
from .types.orgpolicy import ListCustomConstraintsResponse
from .types.orgpolicy import ListPoliciesRequest
from .types.orgpolicy import ListPoliciesResponse
from .types.orgpolicy import Policy
from .types.orgpolicy import PolicySpec
from .types.orgpolicy import UpdateCustomConstraintRequest
from .types.orgpolicy import UpdatePolicyRequest

__all__ = (
    'OrgPolicyAsyncClient',
'AlternatePolicySpec',
'Constraint',
'CreateCustomConstraintRequest',
'CreatePolicyRequest',
'CustomConstraint',
'DeleteCustomConstraintRequest',
'DeletePolicyRequest',
'GetCustomConstraintRequest',
'GetEffectivePolicyRequest',
'GetPolicyRequest',
'ListConstraintsRequest',
'ListConstraintsResponse',
'ListCustomConstraintsRequest',
'ListCustomConstraintsResponse',
'ListPoliciesRequest',
'ListPoliciesResponse',
'OrgPolicyClient',
'Policy',
'PolicySpec',
'UpdateCustomConstraintRequest',
'UpdatePolicyRequest',
)
