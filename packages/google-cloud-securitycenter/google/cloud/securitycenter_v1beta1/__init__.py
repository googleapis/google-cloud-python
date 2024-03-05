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
from google.cloud.securitycenter_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.security_center import SecurityCenterAsyncClient, SecurityCenterClient
from .types.asset import Asset
from .types.finding import Finding
from .types.organization_settings import OrganizationSettings
from .types.run_asset_discovery_response import RunAssetDiscoveryResponse
from .types.security_marks import SecurityMarks
from .types.securitycenter_service import (
    CreateFindingRequest,
    CreateSourceRequest,
    GetOrganizationSettingsRequest,
    GetSourceRequest,
    GroupAssetsRequest,
    GroupAssetsResponse,
    GroupFindingsRequest,
    GroupFindingsResponse,
    GroupResult,
    ListAssetsRequest,
    ListAssetsResponse,
    ListFindingsRequest,
    ListFindingsResponse,
    ListSourcesRequest,
    ListSourcesResponse,
    RunAssetDiscoveryRequest,
    SetFindingStateRequest,
    UpdateFindingRequest,
    UpdateOrganizationSettingsRequest,
    UpdateSecurityMarksRequest,
    UpdateSourceRequest,
)
from .types.source import Source

__all__ = (
    "SecurityCenterAsyncClient",
    "Asset",
    "CreateFindingRequest",
    "CreateSourceRequest",
    "Finding",
    "GetOrganizationSettingsRequest",
    "GetSourceRequest",
    "GroupAssetsRequest",
    "GroupAssetsResponse",
    "GroupFindingsRequest",
    "GroupFindingsResponse",
    "GroupResult",
    "ListAssetsRequest",
    "ListAssetsResponse",
    "ListFindingsRequest",
    "ListFindingsResponse",
    "ListSourcesRequest",
    "ListSourcesResponse",
    "OrganizationSettings",
    "RunAssetDiscoveryRequest",
    "RunAssetDiscoveryResponse",
    "SecurityCenterClient",
    "SecurityMarks",
    "SetFindingStateRequest",
    "Source",
    "UpdateFindingRequest",
    "UpdateOrganizationSettingsRequest",
    "UpdateSecurityMarksRequest",
    "UpdateSourceRequest",
)
