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

from .services.analytics_admin_service import AnalyticsAdminServiceClient
from .types.analytics_admin import AuditUserLinksRequest
from .types.analytics_admin import AuditUserLinksResponse
from .types.analytics_admin import BatchCreateUserLinksRequest
from .types.analytics_admin import BatchCreateUserLinksResponse
from .types.analytics_admin import BatchDeleteUserLinksRequest
from .types.analytics_admin import BatchGetUserLinksRequest
from .types.analytics_admin import BatchGetUserLinksResponse
from .types.analytics_admin import BatchUpdateUserLinksRequest
from .types.analytics_admin import BatchUpdateUserLinksResponse
from .types.analytics_admin import CreateAndroidAppDataStreamRequest
from .types.analytics_admin import CreateFirebaseLinkRequest
from .types.analytics_admin import CreateGoogleAdsLinkRequest
from .types.analytics_admin import CreateIosAppDataStreamRequest
from .types.analytics_admin import CreatePropertyRequest
from .types.analytics_admin import CreateUserLinkRequest
from .types.analytics_admin import CreateWebDataStreamRequest
from .types.analytics_admin import DeleteAccountRequest
from .types.analytics_admin import DeleteAndroidAppDataStreamRequest
from .types.analytics_admin import DeleteFirebaseLinkRequest
from .types.analytics_admin import DeleteGoogleAdsLinkRequest
from .types.analytics_admin import DeleteIosAppDataStreamRequest
from .types.analytics_admin import DeletePropertyRequest
from .types.analytics_admin import DeleteUserLinkRequest
from .types.analytics_admin import DeleteWebDataStreamRequest
from .types.analytics_admin import GetAccountRequest
from .types.analytics_admin import GetAndroidAppDataStreamRequest
from .types.analytics_admin import GetDataSharingSettingsRequest
from .types.analytics_admin import GetEnhancedMeasurementSettingsRequest
from .types.analytics_admin import GetGlobalSiteTagRequest
from .types.analytics_admin import GetIosAppDataStreamRequest
from .types.analytics_admin import GetPropertyRequest
from .types.analytics_admin import GetUserLinkRequest
from .types.analytics_admin import GetWebDataStreamRequest
from .types.analytics_admin import ListAccountSummariesRequest
from .types.analytics_admin import ListAccountSummariesResponse
from .types.analytics_admin import ListAccountsRequest
from .types.analytics_admin import ListAccountsResponse
from .types.analytics_admin import ListAndroidAppDataStreamsRequest
from .types.analytics_admin import ListAndroidAppDataStreamsResponse
from .types.analytics_admin import ListFirebaseLinksRequest
from .types.analytics_admin import ListFirebaseLinksResponse
from .types.analytics_admin import ListGoogleAdsLinksRequest
from .types.analytics_admin import ListGoogleAdsLinksResponse
from .types.analytics_admin import ListIosAppDataStreamsRequest
from .types.analytics_admin import ListIosAppDataStreamsResponse
from .types.analytics_admin import ListPropertiesRequest
from .types.analytics_admin import ListPropertiesResponse
from .types.analytics_admin import ListUserLinksRequest
from .types.analytics_admin import ListUserLinksResponse
from .types.analytics_admin import ListWebDataStreamsRequest
from .types.analytics_admin import ListWebDataStreamsResponse
from .types.analytics_admin import ProvisionAccountTicketRequest
from .types.analytics_admin import ProvisionAccountTicketResponse
from .types.analytics_admin import UpdateAccountRequest
from .types.analytics_admin import UpdateAndroidAppDataStreamRequest
from .types.analytics_admin import UpdateEnhancedMeasurementSettingsRequest
from .types.analytics_admin import UpdateFirebaseLinkRequest
from .types.analytics_admin import UpdateGoogleAdsLinkRequest
from .types.analytics_admin import UpdateIosAppDataStreamRequest
from .types.analytics_admin import UpdatePropertyRequest
from .types.analytics_admin import UpdateUserLinkRequest
from .types.analytics_admin import UpdateWebDataStreamRequest
from .types.resources import Account
from .types.resources import AccountSummary
from .types.resources import AndroidAppDataStream
from .types.resources import AuditUserLink
from .types.resources import DataSharingSettings
from .types.resources import EnhancedMeasurementSettings
from .types.resources import FirebaseLink
from .types.resources import GlobalSiteTag
from .types.resources import GoogleAdsLink
from .types.resources import IndustryCategory
from .types.resources import IosAppDataStream
from .types.resources import MaximumUserAccess
from .types.resources import Property
from .types.resources import PropertySummary
from .types.resources import UserLink
from .types.resources import WebDataStream


__all__ = (
    "Account",
    "AccountSummary",
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
    "AnalyticsAdminServiceClient",
)
