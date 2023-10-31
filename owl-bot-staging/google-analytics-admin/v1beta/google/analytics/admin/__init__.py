# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.analytics.admin import gapic_version as package_version

__version__ = package_version.__version__


from google.analytics.admin_v1beta.services.analytics_admin_service.client import AnalyticsAdminServiceClient
from google.analytics.admin_v1beta.services.analytics_admin_service.async_client import AnalyticsAdminServiceAsyncClient

from google.analytics.admin_v1beta.types.access_report import AccessBetweenFilter
from google.analytics.admin_v1beta.types.access_report import AccessDateRange
from google.analytics.admin_v1beta.types.access_report import AccessDimension
from google.analytics.admin_v1beta.types.access_report import AccessDimensionHeader
from google.analytics.admin_v1beta.types.access_report import AccessDimensionValue
from google.analytics.admin_v1beta.types.access_report import AccessFilter
from google.analytics.admin_v1beta.types.access_report import AccessFilterExpression
from google.analytics.admin_v1beta.types.access_report import AccessFilterExpressionList
from google.analytics.admin_v1beta.types.access_report import AccessInListFilter
from google.analytics.admin_v1beta.types.access_report import AccessMetric
from google.analytics.admin_v1beta.types.access_report import AccessMetricHeader
from google.analytics.admin_v1beta.types.access_report import AccessMetricValue
from google.analytics.admin_v1beta.types.access_report import AccessNumericFilter
from google.analytics.admin_v1beta.types.access_report import AccessOrderBy
from google.analytics.admin_v1beta.types.access_report import AccessQuota
from google.analytics.admin_v1beta.types.access_report import AccessQuotaStatus
from google.analytics.admin_v1beta.types.access_report import AccessRow
from google.analytics.admin_v1beta.types.access_report import AccessStringFilter
from google.analytics.admin_v1beta.types.access_report import NumericValue
from google.analytics.admin_v1beta.types.analytics_admin import AcknowledgeUserDataCollectionRequest
from google.analytics.admin_v1beta.types.analytics_admin import AcknowledgeUserDataCollectionResponse
from google.analytics.admin_v1beta.types.analytics_admin import ArchiveCustomDimensionRequest
from google.analytics.admin_v1beta.types.analytics_admin import ArchiveCustomMetricRequest
from google.analytics.admin_v1beta.types.analytics_admin import CreateConversionEventRequest
from google.analytics.admin_v1beta.types.analytics_admin import CreateCustomDimensionRequest
from google.analytics.admin_v1beta.types.analytics_admin import CreateCustomMetricRequest
from google.analytics.admin_v1beta.types.analytics_admin import CreateDataStreamRequest
from google.analytics.admin_v1beta.types.analytics_admin import CreateFirebaseLinkRequest
from google.analytics.admin_v1beta.types.analytics_admin import CreateGoogleAdsLinkRequest
from google.analytics.admin_v1beta.types.analytics_admin import CreateMeasurementProtocolSecretRequest
from google.analytics.admin_v1beta.types.analytics_admin import CreatePropertyRequest
from google.analytics.admin_v1beta.types.analytics_admin import DeleteAccountRequest
from google.analytics.admin_v1beta.types.analytics_admin import DeleteConversionEventRequest
from google.analytics.admin_v1beta.types.analytics_admin import DeleteDataStreamRequest
from google.analytics.admin_v1beta.types.analytics_admin import DeleteFirebaseLinkRequest
from google.analytics.admin_v1beta.types.analytics_admin import DeleteGoogleAdsLinkRequest
from google.analytics.admin_v1beta.types.analytics_admin import DeleteMeasurementProtocolSecretRequest
from google.analytics.admin_v1beta.types.analytics_admin import DeletePropertyRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetAccountRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetConversionEventRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetCustomDimensionRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetCustomMetricRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetDataRetentionSettingsRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetDataSharingSettingsRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetDataStreamRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetMeasurementProtocolSecretRequest
from google.analytics.admin_v1beta.types.analytics_admin import GetPropertyRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListAccountsRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListAccountsResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListAccountSummariesRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListAccountSummariesResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListConversionEventsRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListConversionEventsResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListCustomDimensionsRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListCustomDimensionsResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListCustomMetricsRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListCustomMetricsResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListDataStreamsRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListDataStreamsResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListFirebaseLinksRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListFirebaseLinksResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListGoogleAdsLinksRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListGoogleAdsLinksResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListMeasurementProtocolSecretsRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListMeasurementProtocolSecretsResponse
from google.analytics.admin_v1beta.types.analytics_admin import ListPropertiesRequest
from google.analytics.admin_v1beta.types.analytics_admin import ListPropertiesResponse
from google.analytics.admin_v1beta.types.analytics_admin import ProvisionAccountTicketRequest
from google.analytics.admin_v1beta.types.analytics_admin import ProvisionAccountTicketResponse
from google.analytics.admin_v1beta.types.analytics_admin import RunAccessReportRequest
from google.analytics.admin_v1beta.types.analytics_admin import RunAccessReportResponse
from google.analytics.admin_v1beta.types.analytics_admin import SearchChangeHistoryEventsRequest
from google.analytics.admin_v1beta.types.analytics_admin import SearchChangeHistoryEventsResponse
from google.analytics.admin_v1beta.types.analytics_admin import UpdateAccountRequest
from google.analytics.admin_v1beta.types.analytics_admin import UpdateConversionEventRequest
from google.analytics.admin_v1beta.types.analytics_admin import UpdateCustomDimensionRequest
from google.analytics.admin_v1beta.types.analytics_admin import UpdateCustomMetricRequest
from google.analytics.admin_v1beta.types.analytics_admin import UpdateDataRetentionSettingsRequest
from google.analytics.admin_v1beta.types.analytics_admin import UpdateDataStreamRequest
from google.analytics.admin_v1beta.types.analytics_admin import UpdateGoogleAdsLinkRequest
from google.analytics.admin_v1beta.types.analytics_admin import UpdateMeasurementProtocolSecretRequest
from google.analytics.admin_v1beta.types.analytics_admin import UpdatePropertyRequest
from google.analytics.admin_v1beta.types.resources import Account
from google.analytics.admin_v1beta.types.resources import AccountSummary
from google.analytics.admin_v1beta.types.resources import ChangeHistoryChange
from google.analytics.admin_v1beta.types.resources import ChangeHistoryEvent
from google.analytics.admin_v1beta.types.resources import ConversionEvent
from google.analytics.admin_v1beta.types.resources import CustomDimension
from google.analytics.admin_v1beta.types.resources import CustomMetric
from google.analytics.admin_v1beta.types.resources import DataRetentionSettings
from google.analytics.admin_v1beta.types.resources import DataSharingSettings
from google.analytics.admin_v1beta.types.resources import DataStream
from google.analytics.admin_v1beta.types.resources import FirebaseLink
from google.analytics.admin_v1beta.types.resources import GoogleAdsLink
from google.analytics.admin_v1beta.types.resources import MeasurementProtocolSecret
from google.analytics.admin_v1beta.types.resources import Property
from google.analytics.admin_v1beta.types.resources import PropertySummary
from google.analytics.admin_v1beta.types.resources import ActionType
from google.analytics.admin_v1beta.types.resources import ActorType
from google.analytics.admin_v1beta.types.resources import ChangeHistoryResourceType
from google.analytics.admin_v1beta.types.resources import IndustryCategory
from google.analytics.admin_v1beta.types.resources import PropertyType
from google.analytics.admin_v1beta.types.resources import ServiceLevel

__all__ = ('AnalyticsAdminServiceClient',
    'AnalyticsAdminServiceAsyncClient',
    'AccessBetweenFilter',
    'AccessDateRange',
    'AccessDimension',
    'AccessDimensionHeader',
    'AccessDimensionValue',
    'AccessFilter',
    'AccessFilterExpression',
    'AccessFilterExpressionList',
    'AccessInListFilter',
    'AccessMetric',
    'AccessMetricHeader',
    'AccessMetricValue',
    'AccessNumericFilter',
    'AccessOrderBy',
    'AccessQuota',
    'AccessQuotaStatus',
    'AccessRow',
    'AccessStringFilter',
    'NumericValue',
    'AcknowledgeUserDataCollectionRequest',
    'AcknowledgeUserDataCollectionResponse',
    'ArchiveCustomDimensionRequest',
    'ArchiveCustomMetricRequest',
    'CreateConversionEventRequest',
    'CreateCustomDimensionRequest',
    'CreateCustomMetricRequest',
    'CreateDataStreamRequest',
    'CreateFirebaseLinkRequest',
    'CreateGoogleAdsLinkRequest',
    'CreateMeasurementProtocolSecretRequest',
    'CreatePropertyRequest',
    'DeleteAccountRequest',
    'DeleteConversionEventRequest',
    'DeleteDataStreamRequest',
    'DeleteFirebaseLinkRequest',
    'DeleteGoogleAdsLinkRequest',
    'DeleteMeasurementProtocolSecretRequest',
    'DeletePropertyRequest',
    'GetAccountRequest',
    'GetConversionEventRequest',
    'GetCustomDimensionRequest',
    'GetCustomMetricRequest',
    'GetDataRetentionSettingsRequest',
    'GetDataSharingSettingsRequest',
    'GetDataStreamRequest',
    'GetMeasurementProtocolSecretRequest',
    'GetPropertyRequest',
    'ListAccountsRequest',
    'ListAccountsResponse',
    'ListAccountSummariesRequest',
    'ListAccountSummariesResponse',
    'ListConversionEventsRequest',
    'ListConversionEventsResponse',
    'ListCustomDimensionsRequest',
    'ListCustomDimensionsResponse',
    'ListCustomMetricsRequest',
    'ListCustomMetricsResponse',
    'ListDataStreamsRequest',
    'ListDataStreamsResponse',
    'ListFirebaseLinksRequest',
    'ListFirebaseLinksResponse',
    'ListGoogleAdsLinksRequest',
    'ListGoogleAdsLinksResponse',
    'ListMeasurementProtocolSecretsRequest',
    'ListMeasurementProtocolSecretsResponse',
    'ListPropertiesRequest',
    'ListPropertiesResponse',
    'ProvisionAccountTicketRequest',
    'ProvisionAccountTicketResponse',
    'RunAccessReportRequest',
    'RunAccessReportResponse',
    'SearchChangeHistoryEventsRequest',
    'SearchChangeHistoryEventsResponse',
    'UpdateAccountRequest',
    'UpdateConversionEventRequest',
    'UpdateCustomDimensionRequest',
    'UpdateCustomMetricRequest',
    'UpdateDataRetentionSettingsRequest',
    'UpdateDataStreamRequest',
    'UpdateGoogleAdsLinkRequest',
    'UpdateMeasurementProtocolSecretRequest',
    'UpdatePropertyRequest',
    'Account',
    'AccountSummary',
    'ChangeHistoryChange',
    'ChangeHistoryEvent',
    'ConversionEvent',
    'CustomDimension',
    'CustomMetric',
    'DataRetentionSettings',
    'DataSharingSettings',
    'DataStream',
    'FirebaseLink',
    'GoogleAdsLink',
    'MeasurementProtocolSecret',
    'Property',
    'PropertySummary',
    'ActionType',
    'ActorType',
    'ChangeHistoryResourceType',
    'IndustryCategory',
    'PropertyType',
    'ServiceLevel',
)
