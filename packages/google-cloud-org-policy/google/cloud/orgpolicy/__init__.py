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
from google.cloud.orgpolicy import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.orgpolicy_v2.services.org_policy.client import OrgPolicyClient
from google.cloud.orgpolicy_v2.services.org_policy.async_client import (
    OrgPolicyAsyncClient,
)

from google.cloud.orgpolicy_v2.types.constraint import Constraint
from google.cloud.orgpolicy_v2.types.constraint import CustomConstraint
from google.cloud.orgpolicy_v2.types.orgpolicy import AlternatePolicySpec
from google.cloud.orgpolicy_v2.types.orgpolicy import CreateCustomConstraintRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import CreatePolicyRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import DeleteCustomConstraintRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import DeletePolicyRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import GetCustomConstraintRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import GetEffectivePolicyRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import GetPolicyRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import ListConstraintsRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import ListConstraintsResponse
from google.cloud.orgpolicy_v2.types.orgpolicy import ListCustomConstraintsRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import ListCustomConstraintsResponse
from google.cloud.orgpolicy_v2.types.orgpolicy import ListPoliciesRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import ListPoliciesResponse
from google.cloud.orgpolicy_v2.types.orgpolicy import Policy
from google.cloud.orgpolicy_v2.types.orgpolicy import PolicySpec
from google.cloud.orgpolicy_v2.types.orgpolicy import UpdateCustomConstraintRequest
from google.cloud.orgpolicy_v2.types.orgpolicy import UpdatePolicyRequest

__all__ = (
    "OrgPolicyClient",
    "OrgPolicyAsyncClient",
    "Constraint",
    "CustomConstraint",
    "AlternatePolicySpec",
    "CreateCustomConstraintRequest",
    "CreatePolicyRequest",
    "DeleteCustomConstraintRequest",
    "DeletePolicyRequest",
    "GetCustomConstraintRequest",
    "GetEffectivePolicyRequest",
    "GetPolicyRequest",
    "ListConstraintsRequest",
    "ListConstraintsResponse",
    "ListCustomConstraintsRequest",
    "ListCustomConstraintsResponse",
    "ListPoliciesRequest",
    "ListPoliciesResponse",
    "Policy",
    "PolicySpec",
    "UpdateCustomConstraintRequest",
    "UpdatePolicyRequest",
)
