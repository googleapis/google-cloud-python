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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.analytics.data_v1alpha.types import data

__protobuf__ = proto.module(
    package="google.analytics.data.v1alpha",
    manifest={
        "RunFunnelReportRequest",
        "RunFunnelReportResponse",
    },
)


class RunFunnelReportRequest(proto.Message):
    r"""The request for a funnel report.

    Attributes:
        property (str):
            A Google Analytics GA4 property identifier whose events are
            tracked. Specified in the URL path and not the body. To
            learn more, see `where to find your Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.
            Within a batch request, this property should either be
            unspecified or consistent with the batch-level property.

            Example: properties/1234
        date_ranges (MutableSequence[google.analytics.data_v1alpha.types.DateRange]):
            Date ranges of data to read. If multiple date
            ranges are requested, each response row will
            contain a zero based date range index. If two
            date ranges overlap, the event data for the
            overlapping days is included in the response
            rows for both date ranges.
        funnel (google.analytics.data_v1alpha.types.Funnel):
            The configuration of this request's funnel.
            This funnel configuration is required.
        funnel_breakdown (google.analytics.data_v1alpha.types.FunnelBreakdown):
            If specified, this breakdown adds a dimension to the funnel
            table sub report response. This breakdown dimension expands
            each funnel step to the unique values of the breakdown
            dimension. For example, a breakdown by the
            ``deviceCategory`` dimension will create rows for
            ``mobile``, ``tablet``, ``desktop``, and the total.
        funnel_next_action (google.analytics.data_v1alpha.types.FunnelNextAction):
            If specified, next action adds a dimension to the funnel
            visualization sub report response. This next action
            dimension expands each funnel step to the unique values of
            the next action. For example a next action of the
            ``eventName`` dimension will create rows for several events
            (i.e. ``session_start`` & ``click``) and the total.

            Next action only supports ``eventName`` and most Page /
            Screen dimensions like ``pageTitle`` and ``pagePath``.
        funnel_visualization_type (google.analytics.data_v1alpha.types.RunFunnelReportRequest.FunnelVisualizationType):
            The funnel visualization type controls the dimensions
            present in the funnel visualization sub report response. If
            not specified, ``STANDARD_FUNNEL`` is used.
        segments (MutableSequence[google.analytics.data_v1alpha.types.Segment]):
            The configurations of segments. Segments are
            subsets of a property's data. In a funnel report
            with segments, the funnel is evaluated in each
            segment.
            Each segment specified in this request
            produces a separate row in the response; in the
            response, each segment identified by its name.

            The segments parameter is optional. Requests are
            limited to 4 segments.
        limit (int):
            The number of rows to return. If unspecified, 10,000 rows
            are returned. The API returns a maximum of 100,000 rows per
            request, no matter how many you ask for. ``limit`` must be
            positive.

            The API can also return fewer rows than the requested
            ``limit``, if there aren't as many dimension values as the
            ``limit``.
        dimension_filter (google.analytics.data_v1alpha.types.FilterExpression):
            Dimension filters allow you to ask for only specific
            dimension values in the report. To learn more, see `Creating
            a Report: Dimension
            Filters <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#dimension_filters>`__
            for examples. Metrics cannot be used in this filter.
        return_property_quota (bool):
            Toggles whether to return the current state of this
            Analytics Property's quota. Quota is returned in
            `PropertyQuota <#PropertyQuota>`__.
    """

    class FunnelVisualizationType(proto.Enum):
        r"""Controls the dimensions present in the funnel visualization
        sub report response.
        """
        FUNNEL_VISUALIZATION_TYPE_UNSPECIFIED = 0
        STANDARD_FUNNEL = 1
        TRENDED_FUNNEL = 2

    property: str = proto.Field(
        proto.STRING,
        number=1,
    )
    date_ranges: MutableSequence[data.DateRange] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=data.DateRange,
    )
    funnel: data.Funnel = proto.Field(
        proto.MESSAGE,
        number=3,
        message=data.Funnel,
    )
    funnel_breakdown: data.FunnelBreakdown = proto.Field(
        proto.MESSAGE,
        number=4,
        message=data.FunnelBreakdown,
    )
    funnel_next_action: data.FunnelNextAction = proto.Field(
        proto.MESSAGE,
        number=5,
        message=data.FunnelNextAction,
    )
    funnel_visualization_type: FunnelVisualizationType = proto.Field(
        proto.ENUM,
        number=6,
        enum=FunnelVisualizationType,
    )
    segments: MutableSequence[data.Segment] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=data.Segment,
    )
    limit: int = proto.Field(
        proto.INT64,
        number=9,
    )
    dimension_filter: data.FilterExpression = proto.Field(
        proto.MESSAGE,
        number=10,
        message=data.FilterExpression,
    )
    return_property_quota: bool = proto.Field(
        proto.BOOL,
        number=12,
    )


class RunFunnelReportResponse(proto.Message):
    r"""The funnel report response contains two sub reports. The two
    sub reports are different combinations of dimensions and
    metrics.

    Attributes:
        funnel_table (google.analytics.data_v1alpha.types.FunnelSubReport):
            The funnel table is a report with the funnel
            step, segment, breakdown dimension, active
            users, completion rate, abandonments, and
            abandonments rate.

            The segment dimension is only present in this
            response if a segment was requested. The
            breakdown dimension is only present in this
            response if it was requested.
        funnel_visualization (google.analytics.data_v1alpha.types.FunnelSubReport):
            The funnel visualization is a report with the funnel step,
            segment, date, next action dimension, and active users.

            The segment dimension is only present in this response if a
            segment was requested. The date dimension is only present in
            this response if it was requested via the ``TRENDED_FUNNEL``
            funnel type. The next action dimension is only present in
            the response if it was requested.
        property_quota (google.analytics.data_v1alpha.types.PropertyQuota):
            This Analytics Property's quota state
            including this request.
        kind (str):
            Identifies what kind of resource this message is. This
            ``kind`` is always the fixed string
            "analyticsData#runFunnelReport". Useful to distinguish
            between response types in JSON.
    """

    funnel_table: data.FunnelSubReport = proto.Field(
        proto.MESSAGE,
        number=1,
        message=data.FunnelSubReport,
    )
    funnel_visualization: data.FunnelSubReport = proto.Field(
        proto.MESSAGE,
        number=2,
        message=data.FunnelSubReport,
    )
    property_quota: data.PropertyQuota = proto.Field(
        proto.MESSAGE,
        number=3,
        message=data.PropertyQuota,
    )
    kind: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
