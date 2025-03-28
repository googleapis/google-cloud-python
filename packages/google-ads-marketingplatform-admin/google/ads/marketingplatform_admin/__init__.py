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
from google.ads.marketingplatform_admin import gapic_version as package_version

__version__ = package_version.__version__


from google.ads.marketingplatform_admin_v1alpha.services.marketingplatform_admin_service.async_client import (
    MarketingplatformAdminServiceAsyncClient,
)
from google.ads.marketingplatform_admin_v1alpha.services.marketingplatform_admin_service.client import (
    MarketingplatformAdminServiceClient,
)
from google.ads.marketingplatform_admin_v1alpha.types.marketingplatform_admin import (
    AnalyticsServiceLevel,
    CreateAnalyticsAccountLinkRequest,
    DeleteAnalyticsAccountLinkRequest,
    GetOrganizationRequest,
    ListAnalyticsAccountLinksRequest,
    ListAnalyticsAccountLinksResponse,
    SetPropertyServiceLevelRequest,
    SetPropertyServiceLevelResponse,
)
from google.ads.marketingplatform_admin_v1alpha.types.resources import (
    AnalyticsAccountLink,
    LinkVerificationState,
    Organization,
)

__all__ = (
    "MarketingplatformAdminServiceClient",
    "MarketingplatformAdminServiceAsyncClient",
    "CreateAnalyticsAccountLinkRequest",
    "DeleteAnalyticsAccountLinkRequest",
    "GetOrganizationRequest",
    "ListAnalyticsAccountLinksRequest",
    "ListAnalyticsAccountLinksResponse",
    "SetPropertyServiceLevelRequest",
    "SetPropertyServiceLevelResponse",
    "AnalyticsServiceLevel",
    "AnalyticsAccountLink",
    "Organization",
    "LinkVerificationState",
)
