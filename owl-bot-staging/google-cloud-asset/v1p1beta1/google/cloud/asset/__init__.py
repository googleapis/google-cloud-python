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
from google.cloud.asset import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.asset_v1p1beta1.services.asset_service.client import AssetServiceClient
from google.cloud.asset_v1p1beta1.services.asset_service.async_client import AssetServiceAsyncClient

from google.cloud.asset_v1p1beta1.types.asset_service import SearchAllIamPoliciesRequest
from google.cloud.asset_v1p1beta1.types.asset_service import SearchAllIamPoliciesResponse
from google.cloud.asset_v1p1beta1.types.asset_service import SearchAllResourcesRequest
from google.cloud.asset_v1p1beta1.types.asset_service import SearchAllResourcesResponse
from google.cloud.asset_v1p1beta1.types.assets import IamPolicySearchResult
from google.cloud.asset_v1p1beta1.types.assets import Permissions
from google.cloud.asset_v1p1beta1.types.assets import StandardResourceMetadata

__all__ = ('AssetServiceClient',
    'AssetServiceAsyncClient',
    'SearchAllIamPoliciesRequest',
    'SearchAllIamPoliciesResponse',
    'SearchAllResourcesRequest',
    'SearchAllResourcesResponse',
    'IamPolicySearchResult',
    'Permissions',
    'StandardResourceMetadata',
)
