# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
    AcknowledgeUserDataCollectionRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    AcknowledgeUserDataCollectionResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ApproveDisplayVideo360AdvertiserLinkProposalRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ApproveDisplayVideo360AdvertiserLinkProposalResponse,
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
    CancelDisplayVideo360AdvertiserLinkProposalRequest,
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
from google.analytics.admin_v1alpha.types.analytics_admin import CreateDataStreamRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateDisplayVideo360AdvertiserLinkProposalRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    CreateDisplayVideo360AdvertiserLinkRequest,
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
from google.analytics.admin_v1alpha.types.analytics_admin import DeleteAccountRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteConversionEventRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import DeleteDataStreamRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteDisplayVideo360AdvertiserLinkProposalRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteDisplayVideo360AdvertiserLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteFirebaseLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteGoogleAdsLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    DeleteMeasurementProtocolSecretRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import DeletePropertyRequest
from google.analytics.admin_v1alpha.types.analytics_admin import DeleteUserLinkRequest
from google.analytics.admin_v1alpha.types.analytics_admin import GetAccountRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetConversionEventRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetCustomDimensionRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetCustomMetricRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetDataRetentionSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetDataSharingSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetDataStreamRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetDisplayVideo360AdvertiserLinkProposalRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetDisplayVideo360AdvertiserLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetGlobalSiteTagRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetGoogleSignalsSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    GetMeasurementProtocolSecretRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import GetPropertyRequest
from google.analytics.admin_v1alpha.types.analytics_admin import GetUserLinkRequest
from google.analytics.admin_v1alpha.types.analytics_admin import ListAccountsRequest
from google.analytics.admin_v1alpha.types.analytics_admin import ListAccountsResponse
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAccountSummariesRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListAccountSummariesResponse,
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
from google.analytics.admin_v1alpha.types.analytics_admin import ListDataStreamsRequest
from google.analytics.admin_v1alpha.types.analytics_admin import ListDataStreamsResponse
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListDisplayVideo360AdvertiserLinkProposalsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListDisplayVideo360AdvertiserLinkProposalsResponse,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListDisplayVideo360AdvertiserLinksRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    ListDisplayVideo360AdvertiserLinksResponse,
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
    UpdateCustomDimensionRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateCustomMetricRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateDataRetentionSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import UpdateDataStreamRequest
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateDisplayVideo360AdvertiserLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateGoogleAdsLinkRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateGoogleSignalsSettingsRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import (
    UpdateMeasurementProtocolSecretRequest,
)
from google.analytics.admin_v1alpha.types.analytics_admin import UpdatePropertyRequest
from google.analytics.admin_v1alpha.types.analytics_admin import UpdateUserLinkRequest
from google.analytics.admin_v1alpha.types.resources import Account
from google.analytics.admin_v1alpha.types.resources import AccountSummary
from google.analytics.admin_v1alpha.types.resources import AuditUserLink
from google.analytics.admin_v1alpha.types.resources import ChangeHistoryChange
from google.analytics.admin_v1alpha.types.resources import ChangeHistoryEvent
from google.analytics.admin_v1alpha.types.resources import ConversionEvent
from google.analytics.admin_v1alpha.types.resources import CustomDimension
from google.analytics.admin_v1alpha.types.resources import CustomMetric
from google.analytics.admin_v1alpha.types.resources import DataRetentionSettings
from google.analytics.admin_v1alpha.types.resources import DataSharingSettings
from google.analytics.admin_v1alpha.types.resources import DataStream
from google.analytics.admin_v1alpha.types.resources import DisplayVideo360AdvertiserLink
from google.analytics.admin_v1alpha.types.resources import (
    DisplayVideo360AdvertiserLinkProposal,
)
from google.analytics.admin_v1alpha.types.resources import FirebaseLink
from google.analytics.admin_v1alpha.types.resources import GlobalSiteTag
from google.analytics.admin_v1alpha.types.resources import GoogleAdsLink
from google.analytics.admin_v1alpha.types.resources import GoogleSignalsSettings
from google.analytics.admin_v1alpha.types.resources import LinkProposalStatusDetails
from google.analytics.admin_v1alpha.types.resources import MeasurementProtocolSecret
from google.analytics.admin_v1alpha.types.resources import Property
from google.analytics.admin_v1alpha.types.resources import PropertySummary
from google.analytics.admin_v1alpha.types.resources import UserLink
from google.analytics.admin_v1alpha.types.resources import ActionType
from google.analytics.admin_v1alpha.types.resources import ActorType
from google.analytics.admin_v1alpha.types.resources import ChangeHistoryResourceType
from google.analytics.admin_v1alpha.types.resources import GoogleSignalsConsent
from google.analytics.admin_v1alpha.types.resources import GoogleSignalsState
from google.analytics.admin_v1alpha.types.resources import IndustryCategory
from google.analytics.admin_v1alpha.types.resources import LinkProposalInitiatingProduct
from google.analytics.admin_v1alpha.types.resources import LinkProposalState
from google.analytics.admin_v1alpha.types.resources import ServiceLevel

__all__ = (
    "AnalyticsAdminServiceClient",
    "AnalyticsAdminServiceAsyncClient",
    "AcknowledgeUserDataCollectionRequest",
    "AcknowledgeUserDataCollectionResponse",
    "ApproveDisplayVideo360AdvertiserLinkProposalRequest",
    "ApproveDisplayVideo360AdvertiserLinkProposalResponse",
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
    "CancelDisplayVideo360AdvertiserLinkProposalRequest",
    "CreateConversionEventRequest",
    "CreateCustomDimensionRequest",
    "CreateCustomMetricRequest",
    "CreateDataStreamRequest",
    "CreateDisplayVideo360AdvertiserLinkProposalRequest",
    "CreateDisplayVideo360AdvertiserLinkRequest",
    "CreateFirebaseLinkRequest",
    "CreateGoogleAdsLinkRequest",
    "CreateMeasurementProtocolSecretRequest",
    "CreatePropertyRequest",
    "CreateUserLinkRequest",
    "DeleteAccountRequest",
    "DeleteConversionEventRequest",
    "DeleteDataStreamRequest",
    "DeleteDisplayVideo360AdvertiserLinkProposalRequest",
    "DeleteDisplayVideo360AdvertiserLinkRequest",
    "DeleteFirebaseLinkRequest",
    "DeleteGoogleAdsLinkRequest",
    "DeleteMeasurementProtocolSecretRequest",
    "DeletePropertyRequest",
    "DeleteUserLinkRequest",
    "GetAccountRequest",
    "GetConversionEventRequest",
    "GetCustomDimensionRequest",
    "GetCustomMetricRequest",
    "GetDataRetentionSettingsRequest",
    "GetDataSharingSettingsRequest",
    "GetDataStreamRequest",
    "GetDisplayVideo360AdvertiserLinkProposalRequest",
    "GetDisplayVideo360AdvertiserLinkRequest",
    "GetGlobalSiteTagRequest",
    "GetGoogleSignalsSettingsRequest",
    "GetMeasurementProtocolSecretRequest",
    "GetPropertyRequest",
    "GetUserLinkRequest",
    "ListAccountsRequest",
    "ListAccountsResponse",
    "ListAccountSummariesRequest",
    "ListAccountSummariesResponse",
    "ListConversionEventsRequest",
    "ListConversionEventsResponse",
    "ListCustomDimensionsRequest",
    "ListCustomDimensionsResponse",
    "ListCustomMetricsRequest",
    "ListCustomMetricsResponse",
    "ListDataStreamsRequest",
    "ListDataStreamsResponse",
    "ListDisplayVideo360AdvertiserLinkProposalsRequest",
    "ListDisplayVideo360AdvertiserLinkProposalsResponse",
    "ListDisplayVideo360AdvertiserLinksRequest",
    "ListDisplayVideo360AdvertiserLinksResponse",
    "ListFirebaseLinksRequest",
    "ListFirebaseLinksResponse",
    "ListGoogleAdsLinksRequest",
    "ListGoogleAdsLinksResponse",
    "ListMeasurementProtocolSecretsRequest",
    "ListMeasurementProtocolSecretsResponse",
    "ListPropertiesRequest",
    "ListPropertiesResponse",
    "ListUserLinksRequest",
    "ListUserLinksResponse",
    "ProvisionAccountTicketRequest",
    "ProvisionAccountTicketResponse",
    "SearchChangeHistoryEventsRequest",
    "SearchChangeHistoryEventsResponse",
    "UpdateAccountRequest",
    "UpdateCustomDimensionRequest",
    "UpdateCustomMetricRequest",
    "UpdateDataRetentionSettingsRequest",
    "UpdateDataStreamRequest",
    "UpdateDisplayVideo360AdvertiserLinkRequest",
    "UpdateGoogleAdsLinkRequest",
    "UpdateGoogleSignalsSettingsRequest",
    "UpdateMeasurementProtocolSecretRequest",
    "UpdatePropertyRequest",
    "UpdateUserLinkRequest",
    "Account",
    "AccountSummary",
    "AuditUserLink",
    "ChangeHistoryChange",
    "ChangeHistoryEvent",
    "ConversionEvent",
    "CustomDimension",
    "CustomMetric",
    "DataRetentionSettings",
    "DataSharingSettings",
    "DataStream",
    "DisplayVideo360AdvertiserLink",
    "DisplayVideo360AdvertiserLinkProposal",
    "FirebaseLink",
    "GlobalSiteTag",
    "GoogleAdsLink",
    "GoogleSignalsSettings",
    "LinkProposalStatusDetails",
    "MeasurementProtocolSecret",
    "Property",
    "PropertySummary",
    "UserLink",
    "ActionType",
    "ActorType",
    "ChangeHistoryResourceType",
    "GoogleSignalsConsent",
    "GoogleSignalsState",
    "IndustryCategory",
    "LinkProposalInitiatingProduct",
    "LinkProposalState",
    "ServiceLevel",
)
