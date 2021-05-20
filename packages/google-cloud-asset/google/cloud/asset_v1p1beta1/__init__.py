# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from .services.asset_service import AssetServiceClient
from .services.asset_service import AssetServiceAsyncClient

from .types.asset_service import SearchAllIamPoliciesRequest
from .types.asset_service import SearchAllIamPoliciesResponse
from .types.asset_service import SearchAllResourcesRequest
from .types.asset_service import SearchAllResourcesResponse
from .types.assets import IamPolicySearchResult
from .types.assets import Permissions
from .types.assets import StandardResourceMetadata

__all__ = (
    "AssetServiceAsyncClient",
    "AssetServiceClient",
    "IamPolicySearchResult",
    "Permissions",
    "SearchAllIamPoliciesRequest",
    "SearchAllIamPoliciesResponse",
    "SearchAllResourcesRequest",
    "SearchAllResourcesResponse",
    "StandardResourceMetadata",
)
