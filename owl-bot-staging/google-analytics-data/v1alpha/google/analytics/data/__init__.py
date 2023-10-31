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
from google.analytics.data import gapic_version as package_version

__version__ = package_version.__version__


from google.analytics.data_v1alpha.services.alpha_analytics_data.client import AlphaAnalyticsDataClient
from google.analytics.data_v1alpha.services.alpha_analytics_data.async_client import AlphaAnalyticsDataAsyncClient

from google.analytics.data_v1alpha.types.analytics_data_api import AudienceDimension
from google.analytics.data_v1alpha.types.analytics_data_api import AudienceDimensionValue
from google.analytics.data_v1alpha.types.analytics_data_api import AudienceList
from google.analytics.data_v1alpha.types.analytics_data_api import AudienceListMetadata
from google.analytics.data_v1alpha.types.analytics_data_api import AudienceRow
from google.analytics.data_v1alpha.types.analytics_data_api import CreateAudienceListRequest
from google.analytics.data_v1alpha.types.analytics_data_api import GetAudienceListRequest
from google.analytics.data_v1alpha.types.analytics_data_api import ListAudienceListsRequest
from google.analytics.data_v1alpha.types.analytics_data_api import ListAudienceListsResponse
from google.analytics.data_v1alpha.types.analytics_data_api import QueryAudienceListRequest
from google.analytics.data_v1alpha.types.analytics_data_api import QueryAudienceListResponse
from google.analytics.data_v1alpha.types.analytics_data_api import RunFunnelReportRequest
from google.analytics.data_v1alpha.types.analytics_data_api import RunFunnelReportResponse
from google.analytics.data_v1alpha.types.data import BetweenFilter
from google.analytics.data_v1alpha.types.data import DateRange
from google.analytics.data_v1alpha.types.data import Dimension
from google.analytics.data_v1alpha.types.data import DimensionExpression
from google.analytics.data_v1alpha.types.data import DimensionHeader
from google.analytics.data_v1alpha.types.data import DimensionValue
from google.analytics.data_v1alpha.types.data import EventSegment
from google.analytics.data_v1alpha.types.data import EventSegmentConditionGroup
from google.analytics.data_v1alpha.types.data import EventSegmentCriteria
from google.analytics.data_v1alpha.types.data import EventSegmentExclusion
from google.analytics.data_v1alpha.types.data import Filter
from google.analytics.data_v1alpha.types.data import FilterExpression
from google.analytics.data_v1alpha.types.data import FilterExpressionList
from google.analytics.data_v1alpha.types.data import Funnel
from google.analytics.data_v1alpha.types.data import FunnelBreakdown
from google.analytics.data_v1alpha.types.data import FunnelEventFilter
from google.analytics.data_v1alpha.types.data import FunnelFieldFilter
from google.analytics.data_v1alpha.types.data import FunnelFilterExpression
from google.analytics.data_v1alpha.types.data import FunnelFilterExpressionList
from google.analytics.data_v1alpha.types.data import FunnelNextAction
from google.analytics.data_v1alpha.types.data import FunnelParameterFilter
from google.analytics.data_v1alpha.types.data import FunnelParameterFilterExpression
from google.analytics.data_v1alpha.types.data import FunnelParameterFilterExpressionList
from google.analytics.data_v1alpha.types.data import FunnelResponseMetadata
from google.analytics.data_v1alpha.types.data import FunnelStep
from google.analytics.data_v1alpha.types.data import FunnelSubReport
from google.analytics.data_v1alpha.types.data import InListFilter
from google.analytics.data_v1alpha.types.data import MetricHeader
from google.analytics.data_v1alpha.types.data import MetricValue
from google.analytics.data_v1alpha.types.data import NumericFilter
from google.analytics.data_v1alpha.types.data import NumericValue
from google.analytics.data_v1alpha.types.data import PropertyQuota
from google.analytics.data_v1alpha.types.data import QuotaStatus
from google.analytics.data_v1alpha.types.data import Row
from google.analytics.data_v1alpha.types.data import SamplingMetadata
from google.analytics.data_v1alpha.types.data import Segment
from google.analytics.data_v1alpha.types.data import SegmentEventFilter
from google.analytics.data_v1alpha.types.data import SegmentFilter
from google.analytics.data_v1alpha.types.data import SegmentFilterExpression
from google.analytics.data_v1alpha.types.data import SegmentFilterExpressionList
from google.analytics.data_v1alpha.types.data import SegmentFilterScoping
from google.analytics.data_v1alpha.types.data import SegmentParameterFilter
from google.analytics.data_v1alpha.types.data import SegmentParameterFilterExpression
from google.analytics.data_v1alpha.types.data import SegmentParameterFilterExpressionList
from google.analytics.data_v1alpha.types.data import SegmentParameterFilterScoping
from google.analytics.data_v1alpha.types.data import SessionSegment
from google.analytics.data_v1alpha.types.data import SessionSegmentConditionGroup
from google.analytics.data_v1alpha.types.data import SessionSegmentCriteria
from google.analytics.data_v1alpha.types.data import SessionSegmentExclusion
from google.analytics.data_v1alpha.types.data import StringFilter
from google.analytics.data_v1alpha.types.data import UserSegment
from google.analytics.data_v1alpha.types.data import UserSegmentConditionGroup
from google.analytics.data_v1alpha.types.data import UserSegmentCriteria
from google.analytics.data_v1alpha.types.data import UserSegmentExclusion
from google.analytics.data_v1alpha.types.data import UserSegmentSequenceGroup
from google.analytics.data_v1alpha.types.data import UserSequenceStep
from google.analytics.data_v1alpha.types.data import EventCriteriaScoping
from google.analytics.data_v1alpha.types.data import EventExclusionDuration
from google.analytics.data_v1alpha.types.data import MetricType
from google.analytics.data_v1alpha.types.data import SessionCriteriaScoping
from google.analytics.data_v1alpha.types.data import SessionExclusionDuration
from google.analytics.data_v1alpha.types.data import UserCriteriaScoping
from google.analytics.data_v1alpha.types.data import UserExclusionDuration

__all__ = ('AlphaAnalyticsDataClient',
    'AlphaAnalyticsDataAsyncClient',
    'AudienceDimension',
    'AudienceDimensionValue',
    'AudienceList',
    'AudienceListMetadata',
    'AudienceRow',
    'CreateAudienceListRequest',
    'GetAudienceListRequest',
    'ListAudienceListsRequest',
    'ListAudienceListsResponse',
    'QueryAudienceListRequest',
    'QueryAudienceListResponse',
    'RunFunnelReportRequest',
    'RunFunnelReportResponse',
    'BetweenFilter',
    'DateRange',
    'Dimension',
    'DimensionExpression',
    'DimensionHeader',
    'DimensionValue',
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
    'InListFilter',
    'MetricHeader',
    'MetricValue',
    'NumericFilter',
    'NumericValue',
    'PropertyQuota',
    'QuotaStatus',
    'Row',
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
    'SessionSegment',
    'SessionSegmentConditionGroup',
    'SessionSegmentCriteria',
    'SessionSegmentExclusion',
    'StringFilter',
    'UserSegment',
    'UserSegmentConditionGroup',
    'UserSegmentCriteria',
    'UserSegmentExclusion',
    'UserSegmentSequenceGroup',
    'UserSequenceStep',
    'EventCriteriaScoping',
    'EventExclusionDuration',
    'MetricType',
    'SessionCriteriaScoping',
    'SessionExclusionDuration',
    'UserCriteriaScoping',
    'UserExclusionDuration',
)
