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
from google.cloud.kms_inventory_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.key_dashboard_service import KeyDashboardServiceClient
from .services.key_dashboard_service import KeyDashboardServiceAsyncClient
from .services.key_tracking_service import KeyTrackingServiceClient
from .services.key_tracking_service import KeyTrackingServiceAsyncClient

from .types.key_dashboard_service import ListCryptoKeysRequest
from .types.key_dashboard_service import ListCryptoKeysResponse
from .types.key_tracking_service import GetProtectedResourcesSummaryRequest
from .types.key_tracking_service import ProtectedResource
from .types.key_tracking_service import ProtectedResourcesSummary
from .types.key_tracking_service import SearchProtectedResourcesRequest
from .types.key_tracking_service import SearchProtectedResourcesResponse

__all__ = (
    'KeyDashboardServiceAsyncClient',
    'KeyTrackingServiceAsyncClient',
'GetProtectedResourcesSummaryRequest',
'KeyDashboardServiceClient',
'KeyTrackingServiceClient',
'ListCryptoKeysRequest',
'ListCryptoKeysResponse',
'ProtectedResource',
'ProtectedResourcesSummary',
'SearchProtectedResourcesRequest',
'SearchProtectedResourcesResponse',
)
