# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.iam_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.policies import PoliciesClient
from .services.policies import PoliciesAsyncClient

from .types.deny import DenyRule
from .types.policy import CreatePolicyRequest
from .types.policy import DeletePolicyRequest
from .types.policy import GetPolicyRequest
from .types.policy import ListPoliciesRequest
from .types.policy import ListPoliciesResponse
from .types.policy import Policy
from .types.policy import PolicyOperationMetadata
from .types.policy import PolicyRule
from .types.policy import UpdatePolicyRequest

__all__ = (
    'PoliciesAsyncClient',
'CreatePolicyRequest',
'DeletePolicyRequest',
'DenyRule',
'GetPolicyRequest',
'ListPoliciesRequest',
'ListPoliciesResponse',
'PoliciesClient',
'Policy',
'PolicyOperationMetadata',
'PolicyRule',
'UpdatePolicyRequest',
)
