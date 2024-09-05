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
from google.ads.marketingplatform_admin_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.marketingplatform_admin_service import (
    MarketingplatformAdminServiceAsyncClient,
    MarketingplatformAdminServiceClient,
)
from .types.marketingplatform_admin import (
    AnalyticsServiceLevel,
    CreateAnalyticsAccountLinkRequest,
    DeleteAnalyticsAccountLinkRequest,
    GetOrganizationRequest,
    ListAnalyticsAccountLinksRequest,
    ListAnalyticsAccountLinksResponse,
    SetPropertyServiceLevelRequest,
    SetPropertyServiceLevelResponse,
)
from .types.resources import AnalyticsAccountLink, LinkVerificationState, Organization

__all__ = (
    "MarketingplatformAdminServiceAsyncClient",
    "AnalyticsAccountLink",
    "AnalyticsServiceLevel",
    "CreateAnalyticsAccountLinkRequest",
    "DeleteAnalyticsAccountLinkRequest",
    "GetOrganizationRequest",
    "LinkVerificationState",
    "ListAnalyticsAccountLinksRequest",
    "ListAnalyticsAccountLinksResponse",
    "MarketingplatformAdminServiceClient",
    "Organization",
    "SetPropertyServiceLevelRequest",
    "SetPropertyServiceLevelResponse",
)
