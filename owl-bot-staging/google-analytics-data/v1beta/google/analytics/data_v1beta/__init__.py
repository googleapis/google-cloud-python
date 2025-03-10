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
from google.analytics.data_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.beta_analytics_data import BetaAnalyticsDataClient
from .services.beta_analytics_data import BetaAnalyticsDataAsyncClient

from .types.analytics_data_api import AudienceDimension
from .types.analytics_data_api import AudienceDimensionValue
from .types.analytics_data_api import AudienceExport
from .types.analytics_data_api import AudienceExportMetadata
from .types.analytics_data_api import AudienceRow
from .types.analytics_data_api import BatchRunPivotReportsRequest
from .types.analytics_data_api import BatchRunPivotReportsResponse
from .types.analytics_data_api import BatchRunReportsRequest
from .types.analytics_data_api import BatchRunReportsResponse
from .types.analytics_data_api import CheckCompatibilityRequest
from .types.analytics_data_api import CheckCompatibilityResponse
from .types.analytics_data_api import CreateAudienceExportRequest
from .types.analytics_data_api import GetAudienceExportRequest
from .types.analytics_data_api import GetMetadataRequest
from .types.analytics_data_api import ListAudienceExportsRequest
from .types.analytics_data_api import ListAudienceExportsResponse
from .types.analytics_data_api import Metadata
from .types.analytics_data_api import QueryAudienceExportRequest
from .types.analytics_data_api import QueryAudienceExportResponse
from .types.analytics_data_api import RunPivotReportRequest
from .types.analytics_data_api import RunPivotReportResponse
from .types.analytics_data_api import RunRealtimeReportRequest
from .types.analytics_data_api import RunRealtimeReportResponse
from .types.analytics_data_api import RunReportRequest
from .types.analytics_data_api import RunReportResponse
from .types.data import Cohort
from .types.data import CohortReportSettings
from .types.data import CohortSpec
from .types.data import CohortsRange
from .types.data import Comparison
from .types.data import ComparisonMetadata
from .types.data import DateRange
from .types.data import Dimension
from .types.data import DimensionCompatibility
from .types.data import DimensionExpression
from .types.data import DimensionHeader
from .types.data import DimensionMetadata
from .types.data import DimensionValue
from .types.data import Filter
from .types.data import FilterExpression
from .types.data import FilterExpressionList
from .types.data import Metric
from .types.data import MetricCompatibility
from .types.data import MetricHeader
from .types.data import MetricMetadata
from .types.data import MetricValue
from .types.data import MinuteRange
from .types.data import NumericValue
from .types.data import OrderBy
from .types.data import Pivot
from .types.data import PivotDimensionHeader
from .types.data import PivotHeader
from .types.data import PropertyQuota
from .types.data import QuotaStatus
from .types.data import ResponseMetaData
from .types.data import Row
from .types.data import SamplingMetadata
from .types.data import Compatibility
from .types.data import MetricAggregation
from .types.data import MetricType
from .types.data import RestrictedMetricType

__all__ = (
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
'BetaAnalyticsDataClient',
'CheckCompatibilityRequest',
'CheckCompatibilityResponse',
'Cohort',
'CohortReportSettings',
'CohortSpec',
'CohortsRange',
'Comparison',
'ComparisonMetadata',
'Compatibility',
'CreateAudienceExportRequest',
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
'GetAudienceExportRequest',
'GetMetadataRequest',
'ListAudienceExportsRequest',
'ListAudienceExportsResponse',
'Metadata',
'Metric',
'MetricAggregation',
'MetricCompatibility',
'MetricHeader',
'MetricMetadata',
'MetricType',
'MetricValue',
'MinuteRange',
'NumericValue',
'OrderBy',
'Pivot',
'PivotDimensionHeader',
'PivotHeader',
'PropertyQuota',
'QueryAudienceExportRequest',
'QueryAudienceExportResponse',
'QuotaStatus',
'ResponseMetaData',
'RestrictedMetricType',
'Row',
'RunPivotReportRequest',
'RunPivotReportResponse',
'RunRealtimeReportRequest',
'RunRealtimeReportResponse',
'RunReportRequest',
'RunReportResponse',
'SamplingMetadata',
)
