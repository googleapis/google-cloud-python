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

from google.analytics.admin_v1alpha.services.analytics_admin_service.async_client import (
    AnalyticsAdminServiceAsyncClient,
)
from google.analytics.admin_v1alpha.services.analytics_admin_service.client import (
    AnalyticsAdminServiceClient,
)
from google.analytics.admin_v1alpha.types.analytics_admin import AuditUserLinksRequest
from google.analytics.admin_v1alpha.types.analytics_admin import AuditUserLinksResponse
from google.analytics.admin_v1alpha.types.analytics_admin import (
    BatchCreateUserLinksRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    BatchCreateUserLinksResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    BatchDeleteUserLinksRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    BatchGetUserLinksRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    BatchGetUserLinksResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    BatchUpdateUserLinksRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    BatchUpdateUserLinksResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateAndroidAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateFirebaseLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateGoogleAdsLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateIosAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import CreatePropertyRequest
from google.analytics.admin_v1alpha.types.analytics_admin import CreateUserLinkRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateWebDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import DeleteAccountRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteAndroidAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteFirebaseLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteGoogleAdsLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteIosAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import DeletePropertyRequest
from google.analytics.admin_v1alpha.types.analytics_admin import DeleteUserLinkRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteWebDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetAccountRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetAndroidAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetDataSharingSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetEnhancedMeasurementSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetGlobalSiteTagRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetIosAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetPropertyRequest
from google.analytics.admin_v1alpha.types.analytics_admin import GetUserLinkRequest
from google.analytics.admin_v1alpha.types.analytics_admin import GetWebDataStreamRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAccountSummariesRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAccountSummariesResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import ListAccountsRequest
from google.analytics.admin_v1alpha.types.analytics_admin import ListAccountsResponse
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAndroidAppDataStreamsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAndroidAppDataStreamsResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListFirebaseLinksRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListFirebaseLinksResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListGoogleAdsLinksRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListGoogleAdsLinksResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListIosAppDataStreamsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListIosAppDataStreamsResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import ListPropertiesRequest
from google.analytics.admin_v1alpha.types.analytics_admin import ListPropertiesResponse
from google.analytics.admin_v1alpha.types.analytics_admin import ListUserLinksRequest
from google.analytics.admin_v1alpha.types.analytics_admin import ListUserLinksResponse
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListWebDataStreamsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListWebDataStreamsResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ProvisionAccountTicketRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ProvisionAccountTicketResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import UpdateAccountRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateAndroidAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateEnhancedMeasurementSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateFirebaseLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateGoogleAdsLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateIosAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import UpdatePropertyRequest
from google.analytics.admin_v1alpha.types.analytics_admin import UpdateUserLinkRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateWebDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.resources import Account
from google.analytics.admin_v1alpha.types.resources import AccountSummary
from google.analytics.admin_v1alpha.types.resources import AndroidAppDataStream
from google.analytics.admin_v1alpha.types.resources import AuditUserLink
from google.analytics.admin_v1alpha.types.resources import DataSharingSettings
from google.analytics.admin_v1alpha.types.resources import EnhancedMeasurementSettings
from google.analytics.admin_v1alpha.types.resources import FirebaseLink
from google.analytics.admin_v1alpha.types.resources import GlobalSiteTag
from google.analytics.admin_v1alpha.types.resources import GoogleAdsLink
from google.analytics.admin_v1alpha.types.resources import IndustryCategory
from google.analytics.admin_v1alpha.types.resources import IosAppDataStream
from google.analytics.admin_v1alpha.types.resources import MaximumUserAccess
from google.analytics.admin_v1alpha.types.resources import Property
from google.analytics.admin_v1alpha.types.resources import PropertySummary
from google.analytics.admin_v1alpha.types.resources import UserLink
from google.analytics.admin_v1alpha.types.resources import WebDataStream

__all__ = (
    "Account",
    "AccountSummary",
    "AnalyticsAdminServiceAsyncClient",
    "AnalyticsAdminServiceClient",
    "AndroidAppDataStream",
    "AuditUserLink",
    "AuditUserLinksRequest",
    "AuditUserLinksResponse",
    "BatchCreateUserLinksRequest",
    "BatchCreateUserLinksResponse",
    "BatchDeleteUserLinksRequest",
    "BatchGetUserLinksRequest",
    "BatchGetUserLinksResponse",
    "BatchUpdateUserLinksRequest",
    "BatchUpdateUserLinksResponse",
    "CreateAndroidAppDataStreamRequest",
    "CreateFirebaseLinkRequest",
    "CreateGoogleAdsLinkRequest",
    "CreateIosAppDataStreamRequest",
    "CreatePropertyRequest",
    "CreateUserLinkRequest",
    "CreateWebDataStreamRequest",
    "DataSharingSettings",
    "DeleteAccountRequest",
    "DeleteAndroidAppDataStreamRequest",
    "DeleteFirebaseLinkRequest",
    "DeleteGoogleAdsLinkRequest",
    "DeleteIosAppDataStreamRequest",
    "DeletePropertyRequest",
    "DeleteUserLinkRequest",
    "DeleteWebDataStreamRequest",
    "EnhancedMeasurementSettings",
    "FirebaseLink",
    "GetAccountRequest",
    "GetAndroidAppDataStreamRequest",
    "GetDataSharingSettingsRequest",
    "GetEnhancedMeasurementSettingsRequest",
    "GetGlobalSiteTagRequest",
    "GetIosAppDataStreamRequest",
    "GetPropertyRequest",
    "GetUserLinkRequest",
    "GetWebDataStreamRequest",
    "GlobalSiteTag",
    "GoogleAdsLink",
    "IndustryCategory",
    "IosAppDataStream",
    "ListAccountSummariesRequest",
    "ListAccountSummariesResponse",
    "ListAccountsRequest",
    "ListAccountsResponse",
    "ListAndroidAppDataStreamsRequest",
    "ListAndroidAppDataStreamsResponse",
    "ListFirebaseLinksRequest",
    "ListFirebaseLinksResponse",
    "ListGoogleAdsLinksRequest",
    "ListGoogleAdsLinksResponse",
    "ListIosAppDataStreamsRequest",
    "ListIosAppDataStreamsResponse",
    "ListPropertiesRequest",
    "ListPropertiesResponse",
    "ListUserLinksRequest",
    "ListUserLinksResponse",
    "ListWebDataStreamsRequest",
    "ListWebDataStreamsResponse",
    "MaximumUserAccess",
    "Property",
    "PropertySummary",
    "ProvisionAccountTicketRequest",
    "ProvisionAccountTicketResponse",
    "UpdateAccountRequest",
    "UpdateAndroidAppDataStreamRequest",
    "UpdateEnhancedMeasurementSettingsRequest",
    "UpdateFirebaseLinkRequest",
    "UpdateGoogleAdsLinkRequest",
    "UpdateIosAppDataStreamRequest",
    "UpdatePropertyRequest",
    "UpdateUserLinkRequest",
    "UpdateWebDataStreamRequest",
    "UserLink",
    "WebDataStream",
)
