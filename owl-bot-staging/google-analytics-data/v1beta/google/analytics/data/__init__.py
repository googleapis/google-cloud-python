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
from google.analytics.data import gapic_version as package_version

__version__ = package_version.__version__


from google.analytics.data_v1beta.services.beta_analytics_data.client import BetaAnalyticsDataClient
from google.analytics.data_v1beta.services.beta_analytics_data.async_client import BetaAnalyticsDataAsyncClient

from google.analytics.data_v1beta.types.analytics_data_api import AudienceDimension
from google.analytics.data_v1beta.types.analytics_data_api import AudienceDimensionValue
from google.analytics.data_v1beta.types.analytics_data_api import AudienceExport
from google.analytics.data_v1beta.types.analytics_data_api import AudienceExportMetadata
from google.analytics.data_v1beta.types.analytics_data_api import AudienceRow
from google.analytics.data_v1beta.types.analytics_data_api import BatchRunPivotReportsRequest
from google.analytics.data_v1beta.types.analytics_data_api import BatchRunPivotReportsResponse
from google.analytics.data_v1beta.types.analytics_data_api import BatchRunReportsRequest
from google.analytics.data_v1beta.types.analytics_data_api import BatchRunReportsResponse
from google.analytics.data_v1beta.types.analytics_data_api import CheckCompatibilityRequest
from google.analytics.data_v1beta.types.analytics_data_api import CheckCompatibilityResponse
from google.analytics.data_v1beta.types.analytics_data_api import CreateAudienceExportRequest
from google.analytics.data_v1beta.types.analytics_data_api import GetAudienceExportRequest
from google.analytics.data_v1beta.types.analytics_data_api import GetMetadataRequest
from google.analytics.data_v1beta.types.analytics_data_api import ListAudienceExportsRequest
from google.analytics.data_v1beta.types.analytics_data_api import ListAudienceExportsResponse
from google.analytics.data_v1beta.types.analytics_data_api import Metadata
from google.analytics.data_v1beta.types.analytics_data_api import QueryAudienceExportRequest
from google.analytics.data_v1beta.types.analytics_data_api import QueryAudienceExportResponse
from google.analytics.data_v1beta.types.analytics_data_api import RunPivotReportRequest
from google.analytics.data_v1beta.types.analytics_data_api import RunPivotReportResponse
from google.analytics.data_v1beta.types.analytics_data_api import RunRealtimeReportRequest
from google.analytics.data_v1beta.types.analytics_data_api import RunRealtimeReportResponse
from google.analytics.data_v1beta.types.analytics_data_api import RunReportRequest
from google.analytics.data_v1beta.types.analytics_data_api import RunReportResponse
from google.analytics.data_v1beta.types.data import Cohort
from google.analytics.data_v1beta.types.data import CohortReportSettings
from google.analytics.data_v1beta.types.data import CohortSpec
from google.analytics.data_v1beta.types.data import CohortsRange
from google.analytics.data_v1beta.types.data import Comparison
from google.analytics.data_v1beta.types.data import ComparisonMetadata
from google.analytics.data_v1beta.types.data import DateRange
from google.analytics.data_v1beta.types.data import Dimension
from google.analytics.data_v1beta.types.data import DimensionCompatibility
from google.analytics.data_v1beta.types.data import DimensionExpression
from google.analytics.data_v1beta.types.data import DimensionHeader
from google.analytics.data_v1beta.types.data import DimensionMetadata
from google.analytics.data_v1beta.types.data import DimensionValue
from google.analytics.data_v1beta.types.data import Filter
from google.analytics.data_v1beta.types.data import FilterExpression
from google.analytics.data_v1beta.types.data import FilterExpressionList
from google.analytics.data_v1beta.types.data import Metric
from google.analytics.data_v1beta.types.data import MetricCompatibility
from google.analytics.data_v1beta.types.data import MetricHeader
from google.analytics.data_v1beta.types.data import MetricMetadata
from google.analytics.data_v1beta.types.data import MetricValue
from google.analytics.data_v1beta.types.data import MinuteRange
from google.analytics.data_v1beta.types.data import NumericValue
from google.analytics.data_v1beta.types.data import OrderBy
from google.analytics.data_v1beta.types.data import Pivot
from google.analytics.data_v1beta.types.data import PivotDimensionHeader
from google.analytics.data_v1beta.types.data import PivotHeader
from google.analytics.data_v1beta.types.data import PropertyQuota
from google.analytics.data_v1beta.types.data import QuotaStatus
from google.analytics.data_v1beta.types.data import ResponseMetaData
from google.analytics.data_v1beta.types.data import Row
from google.analytics.data_v1beta.types.data import SamplingMetadata
from google.analytics.data_v1beta.types.data import Compatibility
from google.analytics.data_v1beta.types.data import MetricAggregation
from google.analytics.data_v1beta.types.data import MetricType
from google.analytics.data_v1beta.types.data import RestrictedMetricType

__all__ = ('BetaAnalyticsDataClient',
    'BetaAnalyticsDataAsyncClient',
    'AudienceDimension',
    'AudienceDimensionValue',
    'AudienceExport',
    'AudienceExportMetadata',
    'AudienceRow',
    'BatchRunPivotReportsRequest',
    'BatchRunPivotReportsResponse',
    'BatchRunReportsRequest',
    'BatchRunReportsResponse',
    'CheckCompatibilityRequest',
    'CheckCompatibilityResponse',
    'CreateAudienceExportRequest',
    'GetAudienceExportRequest',
    'GetMetadataRequest',
    'ListAudienceExportsRequest',
    'ListAudienceExportsResponse',
    'Metadata',
    'QueryAudienceExportRequest',
    'QueryAudienceExportResponse',
    'RunPivotReportRequest',
    'RunPivotReportResponse',
    'RunRealtimeReportRequest',
    'RunRealtimeReportResponse',
    'RunReportRequest',
    'RunReportResponse',
    'Cohort',
    'CohortReportSettings',
    'CohortSpec',
    'CohortsRange',
    'Comparison',
    'ComparisonMetadata',
    'DateRange',
    'Dimension',
    'DimensionCompatibility',
    'DimensionExpression',
    'DimensionHeader',
    'DimensionMetadata',
    'DimensionValue',
    'Filter',
    'FilterExpression',
    'FilterExpressionList',
    'Metric',
    'MetricCompatibility',
    'MetricHeader',
    'MetricMetadata',
    'MetricValue',
    'MinuteRange',
    'NumericValue',
    'OrderBy',
    'Pivot',
    'PivotDimensionHeader',
    'PivotHeader',
    'PropertyQuota',
    'QuotaStatus',
    'ResponseMetaData',
    'Row',
    'SamplingMetadata',
    'Compatibility',
    'MetricAggregation',
    'MetricType',
    'RestrictedMetricType',
)
