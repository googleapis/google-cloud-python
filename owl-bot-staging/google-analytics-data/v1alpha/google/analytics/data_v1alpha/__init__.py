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
from google.analytics.data_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.alpha_analytics_data import AlphaAnalyticsDataClient
from .services.alpha_analytics_data import AlphaAnalyticsDataAsyncClient

from .types.analytics_data_api import AudienceDimension
from .types.analytics_data_api import AudienceDimensionValue
from .types.analytics_data_api import AudienceList
from .types.analytics_data_api import AudienceListMetadata
from .types.analytics_data_api import AudienceRow
from .types.analytics_data_api import CreateAudienceListRequest
from .types.analytics_data_api import CreateRecurringAudienceListRequest
from .types.analytics_data_api import CreateReportTaskRequest
from .types.analytics_data_api import GetAudienceListRequest
from .types.analytics_data_api import GetPropertyQuotasSnapshotRequest
from .types.analytics_data_api import GetRecurringAudienceListRequest
from .types.analytics_data_api import GetReportTaskRequest
from .types.analytics_data_api import ListAudienceListsRequest
from .types.analytics_data_api import ListAudienceListsResponse
from .types.analytics_data_api import ListRecurringAudienceListsRequest
from .types.analytics_data_api import ListRecurringAudienceListsResponse
from .types.analytics_data_api import ListReportTasksRequest
from .types.analytics_data_api import ListReportTasksResponse
from .types.analytics_data_api import PropertyQuotasSnapshot
from .types.analytics_data_api import QueryAudienceListRequest
from .types.analytics_data_api import QueryAudienceListResponse
from .types.analytics_data_api import QueryReportTaskRequest
from .types.analytics_data_api import QueryReportTaskResponse
from .types.analytics_data_api import RecurringAudienceList
from .types.analytics_data_api import ReportTask
from .types.analytics_data_api import ReportTaskMetadata
from .types.analytics_data_api import RunFunnelReportRequest
from .types.analytics_data_api import RunFunnelReportResponse
from .types.analytics_data_api import SheetExportAudienceListRequest
from .types.analytics_data_api import SheetExportAudienceListResponse
from .types.analytics_data_api import WebhookNotification
from .types.data import BetweenFilter
from .types.data import Cohort
from .types.data import CohortReportSettings
from .types.data import CohortSpec
from .types.data import CohortsRange
from .types.data import DateRange
from .types.data import Dimension
from .types.data import DimensionExpression
from .types.data import DimensionHeader
from .types.data import DimensionValue
from .types.data import EventSegment
from .types.data import EventSegmentConditionGroup
from .types.data import EventSegmentCriteria
from .types.data import EventSegmentExclusion
from .types.data import Filter
from .types.data import FilterExpression
from .types.data import FilterExpressionList
from .types.data import Funnel
from .types.data import FunnelBreakdown
from .types.data import FunnelEventFilter
from .types.data import FunnelFieldFilter
from .types.data import FunnelFilterExpression
from .types.data import FunnelFilterExpressionList
from .types.data import FunnelNextAction
from .types.data import FunnelParameterFilter
from .types.data import FunnelParameterFilterExpression
from .types.data import FunnelParameterFilterExpressionList
from .types.data import FunnelResponseMetadata
from .types.data import FunnelStep
from .types.data import FunnelSubReport
from .types.data import InListFilter
from .types.data import Metric
from .types.data import MetricHeader
from .types.data import MetricValue
from .types.data import NumericFilter
from .types.data import NumericValue
from .types.data import OrderBy
from .types.data import PropertyQuota
from .types.data import QuotaStatus
from .types.data import ResponseMetaData
from .types.data import Row
from .types.data import SamplingMetadata
from .types.data import Segment
from .types.data import SegmentEventFilter
from .types.data import SegmentFilter
from .types.data import SegmentFilterExpression
from .types.data import SegmentFilterExpressionList
from .types.data import SegmentFilterScoping
from .types.data import SegmentParameterFilter
from .types.data import SegmentParameterFilterExpression
from .types.data import SegmentParameterFilterExpressionList
from .types.data import SegmentParameterFilterScoping
from .types.data import SessionSegment
from .types.data import SessionSegmentConditionGroup
from .types.data import SessionSegmentCriteria
from .types.data import SessionSegmentExclusion
from .types.data import StringFilter
from .types.data import UserSegment
from .types.data import UserSegmentConditionGroup
from .types.data import UserSegmentCriteria
from .types.data import UserSegmentExclusion
from .types.data import UserSegmentSequenceGroup
from .types.data import UserSequenceStep
from .types.data import EventCriteriaScoping
from .types.data import EventExclusionDuration
from .types.data import MetricAggregation
from .types.data import MetricType
from .types.data import RestrictedMetricType
from .types.data import SamplingLevel
from .types.data import SessionCriteriaScoping
from .types.data import SessionExclusionDuration
from .types.data import UserCriteriaScoping
from .types.data import UserExclusionDuration

__all__ = (
    'AlphaAnalyticsDataAsyncClient',
'AlphaAnalyticsDataClient',
'AudienceDimension',
'AudienceDimensionValue',
'AudienceList',
'AudienceListMetadata',
'AudienceRow',
'BetweenFilter',
'Cohort',
'CohortReportSettings',
'CohortSpec',
'CohortsRange',
'CreateAudienceListRequest',
'CreateRecurringAudienceListRequest',
'CreateReportTaskRequest',
'DateRange',
'Dimension',
'DimensionExpression',
'DimensionHeader',
'DimensionValue',
'EventCriteriaScoping',
'EventExclusionDuration',
'EventSegment',
'EventSegmentConditionGroup',
'EventSegmentCriteria',
'EventSegmentExclusion',
'Filter',
'FilterExpression',
'FilterExpressionList',
'Funnel',
'FunnelBreakdown',
'FunnelEventFilter',
'FunnelFieldFilter',
'FunnelFilterExpression',
'FunnelFilterExpressionList',
'FunnelNextAction',
'FunnelParameterFilter',
'FunnelParameterFilterExpression',
'FunnelParameterFilterExpressionList',
'FunnelResponseMetadata',
'FunnelStep',
'FunnelSubReport',
'GetAudienceListRequest',
'GetPropertyQuotasSnapshotRequest',
'GetRecurringAudienceListRequest',
'GetReportTaskRequest',
'InListFilter',
'ListAudienceListsRequest',
'ListAudienceListsResponse',
'ListRecurringAudienceListsRequest',
'ListRecurringAudienceListsResponse',
'ListReportTasksRequest',
'ListReportTasksResponse',
'Metric',
'MetricAggregation',
'MetricHeader',
'MetricType',
'MetricValue',
'NumericFilter',
'NumericValue',
'OrderBy',
'PropertyQuota',
'PropertyQuotasSnapshot',
'QueryAudienceListRequest',
'QueryAudienceListResponse',
'QueryReportTaskRequest',
'QueryReportTaskResponse',
'QuotaStatus',
'RecurringAudienceList',
'ReportTask',
'ReportTaskMetadata',
'ResponseMetaData',
'RestrictedMetricType',
'Row',
'RunFunnelReportRequest',
'RunFunnelReportResponse',
'SamplingLevel',
'SamplingMetadata',
'Segment',
'SegmentEventFilter',
'SegmentFilter',
'SegmentFilterExpression',
'SegmentFilterExpressionList',
'SegmentFilterScoping',
'SegmentParameterFilter',
'SegmentParameterFilterExpression',
'SegmentParameterFilterExpressionList',
'SegmentParameterFilterScoping',
'SessionCriteriaScoping',
'SessionExclusionDuration',
'SessionSegment',
'SessionSegmentConditionGroup',
'SessionSegmentCriteria',
'SessionSegmentExclusion',
'SheetExportAudienceListRequest',
'SheetExportAudienceListResponse',
'StringFilter',
'UserCriteriaScoping',
'UserExclusionDuration',
'UserSegment',
'UserSegmentConditionGroup',
'UserSegmentCriteria',
'UserSegmentExclusion',
'UserSegmentSequenceGroup',
'UserSequenceStep',
'WebhookNotification',
)
