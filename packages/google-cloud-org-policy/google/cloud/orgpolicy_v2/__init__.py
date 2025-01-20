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


from .services.org_policy import OrgPolicyAsyncClient, OrgPolicyClient
from .types.constraint import Constraint, CustomConstraint
from .types.orgpolicy import (
    AlternatePolicySpec,
    CreateCustomConstraintRequest,
    CreatePolicyRequest,
    DeleteCustomConstraintRequest,
    DeletePolicyRequest,
    GetCustomConstraintRequest,
    GetEffectivePolicyRequest,
    GetPolicyRequest,
    ListConstraintsRequest,
    ListConstraintsResponse,
    ListCustomConstraintsRequest,
    ListCustomConstraintsResponse,
    ListPoliciesRequest,
    ListPoliciesResponse,
    Policy,
    PolicySpec,
    UpdateCustomConstraintRequest,
    UpdatePolicyRequest,
)

__all__ = (
    "OrgPolicyAsyncClient",
    "AlternatePolicySpec",
    "Constraint",
    "CreateCustomConstraintRequest",
    "CreatePolicyRequest",
    "CustomConstraint",
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
    "OrgPolicyClient",
    "Policy",
    "PolicySpec",
    "UpdateCustomConstraintRequest",
    "UpdatePolicyRequest",
)
