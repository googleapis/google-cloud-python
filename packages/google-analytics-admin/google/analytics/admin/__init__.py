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

from google.analytics.admin_v1alpha.services.analytics_admin_service.client import (
    AnalyticsAdminServiceClient,
)
from google.analytics.admin_v1alpha.services.analytics_admin_service.async_client import (
    AnalyticsAdminServiceAsyncClient,
)

from google.analytics.admin_v1alpha.types.analytics_admin import (
    ArchiveCustomDimensionRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ArchiveCustomMetricRequest,
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
    CreateConversionEventRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateCustomDimensionRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateCustomMetricRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateFirebaseLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateGoogleAdsLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateMeasurementProtocolSecretRequest,
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
    DeleteConversionEventRequest,
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
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteMeasurementProtocolSecretRequest,
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
    GetConversionEventRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetCustomDimensionRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetCustomMetricRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetDataSharingSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetEnhancedMeasurementSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetGlobalSiteTagRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetGoogleSignalsSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetIosAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetMeasurementProtocolSecretRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetPropertyRequest
from google.analytics.admin_v1alpha.types.analytics_admin import GetUserLinkRequest
from google.analytics.admin_v1alpha.types.analytics_admin import GetWebDataStreamRequest
from google.analytics.admin_v1alpha.types.analytics_admin import ListAccountsRequest
from google.analytics.admin_v1alpha.types.analytics_admin import ListAccountsResponse
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAccountSummariesRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAccountSummariesResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAndroidAppDataStreamsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAndroidAppDataStreamsResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListConversionEventsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListConversionEventsResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListCustomDimensionsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListCustomDimensionsResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListCustomMetricsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListCustomMetricsResponse,
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
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListMeasurementProtocolSecretsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListMeasurementProtocolSecretsResponse,
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
from google.analytics.admin_v1alpha.types.analytics_admin import (
    SearchChangeHistoryEventsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    SearchChangeHistoryEventsResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import UpdateAccountRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateAndroidAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateCustomDimensionRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateCustomMetricRequest,
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
    UpdateGoogleSignalsSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateIosAppDataStreamRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateMeasurementProtocolSecretRequest,
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
from google.analytics.admin_v1alpha.types.resources import ChangeHistoryChange
from google.analytics.admin_v1alpha.types.resources import ChangeHistoryEvent
from google.analytics.admin_v1alpha.types.resources import ConversionEvent
from google.analytics.admin_v1alpha.types.resources import CustomDimension
from google.analytics.admin_v1alpha.types.resources import CustomMetric
from google.analytics.admin_v1alpha.types.resources import DataSharingSettings
from google.analytics.admin_v1alpha.types.resources import EnhancedMeasurementSettings
from google.analytics.admin_v1alpha.types.resources import FirebaseLink
from google.analytics.admin_v1alpha.types.resources import GlobalSiteTag
from google.analytics.admin_v1alpha.types.resources import GoogleAdsLink
from google.analytics.admin_v1alpha.types.resources import GoogleSignalsSettings
from google.analytics.admin_v1alpha.types.resources import IosAppDataStream
from google.analytics.admin_v1alpha.types.resources import MeasurementProtocolSecret
from google.analytics.admin_v1alpha.types.resources import Property
from google.analytics.admin_v1alpha.types.resources import PropertySummary
from google.analytics.admin_v1alpha.types.resources import UserLink
from google.analytics.admin_v1alpha.types.resources import WebDataStream
from google.analytics.admin_v1alpha.types.resources import ActionType
from google.analytics.admin_v1alpha.types.resources import ActorType
from google.analytics.admin_v1alpha.types.resources import ChangeHistoryResourceType
from google.analytics.admin_v1alpha.types.resources import GoogleSignalsConsent
from google.analytics.admin_v1alpha.types.resources import GoogleSignalsState
from google.analytics.admin_v1alpha.types.resources import IndustryCategory
from google.analytics.admin_v1alpha.types.resources import MaximumUserAccess

__all__ = (
    "AnalyticsAdminServiceClient",
    "AnalyticsAdminServiceAsyncClient",
    "ArchiveCustomDimensionRequest",
    "ArchiveCustomMetricRequest",
    "AuditUserLinksRequest",
    "AuditUserLinksResponse",
    "BatchCreateUserLinksRequest",
    "BatchCreateUserLinksResponse",
    "BatchDeleteUserLinksRequest",
    "BatchGetUserLinksRequest",
    "BatchGetUserLinksResponse",
    "BatchUpdateUserLinksRequest",
    "BatchUpdateUserLinksResponse",
    "CreateConversionEventRequest",
    "CreateCustomDimensionRequest",
    "CreateCustomMetricRequest",
    "CreateFirebaseLinkRequest",
    "CreateGoogleAdsLinkRequest",
    "CreateMeasurementProtocolSecretRequest",
    "CreatePropertyRequest",
    "CreateUserLinkRequest",
    "CreateWebDataStreamRequest",
    "DeleteAccountRequest",
    "DeleteAndroidAppDataStreamRequest",
    "DeleteConversionEventRequest",
    "DeleteFirebaseLinkRequest",
    "DeleteGoogleAdsLinkRequest",
    "DeleteIosAppDataStreamRequest",
    "DeleteMeasurementProtocolSecretRequest",
    "DeletePropertyRequest",
    "DeleteUserLinkRequest",
    "DeleteWebDataStreamRequest",
    "GetAccountRequest",
    "GetAndroidAppDataStreamRequest",
    "GetConversionEventRequest",
    "GetCustomDimensionRequest",
    "GetCustomMetricRequest",
    "GetDataSharingSettingsRequest",
    "GetEnhancedMeasurementSettingsRequest",
    "GetGlobalSiteTagRequest",
    "GetGoogleSignalsSettingsRequest",
    "GetIosAppDataStreamRequest",
    "GetMeasurementProtocolSecretRequest",
    "GetPropertyRequest",
    "GetUserLinkRequest",
    "GetWebDataStreamRequest",
    "ListAccountsRequest",
    "ListAccountsResponse",
    "ListAccountSummariesRequest",
    "ListAccountSummariesResponse",
    "ListAndroidAppDataStreamsRequest",
    "ListAndroidAppDataStreamsResponse",
    "ListConversionEventsRequest",
    "ListConversionEventsResponse",
    "ListCustomDimensionsRequest",
    "ListCustomDimensionsResponse",
    "ListCustomMetricsRequest",
    "ListCustomMetricsResponse",
    "ListFirebaseLinksRequest",
    "ListFirebaseLinksResponse",
    "ListGoogleAdsLinksRequest",
    "ListGoogleAdsLinksResponse",
    "ListIosAppDataStreamsRequest",
    "ListIosAppDataStreamsResponse",
    "ListMeasurementProtocolSecretsRequest",
    "ListMeasurementProtocolSecretsResponse",
    "ListPropertiesRequest",
    "ListPropertiesResponse",
    "ListUserLinksRequest",
    "ListUserLinksResponse",
    "ListWebDataStreamsRequest",
    "ListWebDataStreamsResponse",
    "ProvisionAccountTicketRequest",
    "ProvisionAccountTicketResponse",
    "SearchChangeHistoryEventsRequest",
    "SearchChangeHistoryEventsResponse",
    "UpdateAccountRequest",
    "UpdateAndroidAppDataStreamRequest",
    "UpdateCustomDimensionRequest",
    "UpdateCustomMetricRequest",
    "UpdateEnhancedMeasurementSettingsRequest",
    "UpdateFirebaseLinkRequest",
    "UpdateGoogleAdsLinkRequest",
    "UpdateGoogleSignalsSettingsRequest",
    "UpdateIosAppDataStreamRequest",
    "UpdateMeasurementProtocolSecretRequest",
    "UpdatePropertyRequest",
    "UpdateUserLinkRequest",
    "UpdateWebDataStreamRequest",
    "Account",
    "AccountSummary",
    "AndroidAppDataStream",
    "AuditUserLink",
    "ChangeHistoryChange",
    "ChangeHistoryEvent",
    "ConversionEvent",
    "CustomDimension",
    "CustomMetric",
    "DataSharingSettings",
    "EnhancedMeasurementSettings",
    "FirebaseLink",
    "GlobalSiteTag",
    "GoogleAdsLink",
    "GoogleSignalsSettings",
    "IosAppDataStream",
    "MeasurementProtocolSecret",
    "Property",
    "PropertySummary",
    "UserLink",
    "WebDataStream",
    "ActionType",
    "ActorType",
    "ChangeHistoryResourceType",
    "GoogleSignalsConsent",
    "GoogleSignalsState",
    "IndustryCategory",
    "MaximumUserAccess",
)
