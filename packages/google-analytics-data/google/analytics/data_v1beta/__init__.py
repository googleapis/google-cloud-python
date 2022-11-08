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
from google.analytics.data import gapic_version as package_version

__version__ = package_version.__version__


from .services.beta_analytics_data import (
    BetaAnalyticsDataAsyncClient,
    BetaAnalyticsDataClient,
)
from .types.analytics_data_api import (
    BatchRunPivotReportsRequest,
    BatchRunPivotReportsResponse,
    BatchRunReportsRequest,
    BatchRunReportsResponse,
    CheckCompatibilityRequest,
    CheckCompatibilityResponse,
    GetMetadataRequest,
    Metadata,
    RunPivotReportRequest,
    RunPivotReportResponse,
    RunRealtimeReportRequest,
    RunRealtimeReportResponse,
    RunReportRequest,
    RunReportResponse,
)
from .types.data import (
    Cohort,
    CohortReportSettings,
    CohortSpec,
    CohortsRange,
    Compatibility,
    DateRange,
    Dimension,
    DimensionCompatibility,
    DimensionExpression,
    DimensionHeader,
    DimensionMetadata,
    DimensionValue,
    Filter,
    FilterExpression,
    FilterExpressionList,
    Metric,
    MetricAggregation,
    MetricCompatibility,
    MetricHeader,
    MetricMetadata,
    MetricType,
    MetricValue,
    MinuteRange,
    NumericValue,
    OrderBy,
    Pivot,
    PivotDimensionHeader,
    PivotHeader,
    PropertyQuota,
    QuotaStatus,
    ResponseMetaData,
    RestrictedMetricType,
    Row,
)

__all__ = (
    "BetaAnalyticsDataAsyncClient",
    "BatchRunPivotReportsRequest",
    "BatchRunPivotReportsResponse",
    "BatchRunReportsRequest",
    "BatchRunReportsResponse",
    "BetaAnalyticsDataClient",
    "CheckCompatibilityRequest",
    "CheckCompatibilityResponse",
    "Cohort",
    "CohortReportSettings",
    "CohortSpec",
    "CohortsRange",
    "Compatibility",
    "DateRange",
    "Dimension",
    "DimensionCompatibility",
    "DimensionExpression",
    "DimensionHeader",
    "DimensionMetadata",
    "DimensionValue",
    "Filter",
    "FilterExpression",
    "FilterExpressionList",
    "GetMetadataRequest",
    "Metadata",
    "Metric",
    "MetricAggregation",
    "MetricCompatibility",
    "MetricHeader",
    "MetricMetadata",
    "MetricType",
    "MetricValue",
    "MinuteRange",
    "NumericValue",
    "OrderBy",
    "Pivot",
    "PivotDimensionHeader",
    "PivotHeader",
    "PropertyQuota",
    "QuotaStatus",
    "ResponseMetaData",
    "RestrictedMetricType",
    "Row",
    "RunPivotReportRequest",
    "RunPivotReportResponse",
    "RunRealtimeReportRequest",
    "RunRealtimeReportResponse",
    "RunReportRequest",
    "RunReportResponse",
)
