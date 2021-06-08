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
import proto  # type: ignore

from google.analytics.data_v1alpha.types import data


__protobuf__ = proto.module(
    package="google.analytics.data.v1alpha",
    manifest={
        "Metadata",
        "RunReportRequest",
        "RunReportResponse",
        "RunPivotReportRequest",
        "RunPivotReportResponse",
        "BatchRunReportsRequest",
        "BatchRunReportsResponse",
        "BatchRunPivotReportsRequest",
        "BatchRunPivotReportsResponse",
        "GetMetadataRequest",
        "RunRealtimeReportRequest",
        "RunRealtimeReportResponse",
    },
)


class Metadata(proto.Message):
    r"""The dimensions and metrics currently accepted in reporting
    methods.

    Attributes:
        name (str):
            Resource name of this metadata.
        dimensions (Sequence[google.analytics.data_v1alpha.types.DimensionMetadata]):
            The dimension descriptions.
        metrics (Sequence[google.analytics.data_v1alpha.types.MetricMetadata]):
            The metric descriptions.
    """

    name = proto.Field(proto.STRING, number=3,)
    dimensions = proto.RepeatedField(
        proto.MESSAGE, number=1, message=data.DimensionMetadata,
    )
    metrics = proto.RepeatedField(proto.MESSAGE, number=2, message=data.MetricMetadata,)


class RunReportRequest(proto.Message):
    r"""The request to generate a report.
    Attributes:
        entity (google.analytics.data_v1alpha.types.Entity):
            A property whose events are tracked. Within a
            batch request, this entity should either be
            unspecified or consistent with the batch-level
            entity.
        dimensions (Sequence[google.analytics.data_v1alpha.types.Dimension]):
            The dimensions requested and displayed.
        metrics (Sequence[google.analytics.data_v1alpha.types.Metric]):
            The metrics requested and displayed.
        date_ranges (Sequence[google.analytics.data_v1alpha.types.DateRange]):
            Date ranges of data to read. If multiple date ranges are
            requested, each response row will contain a zero based date
            range index. If two date ranges overlap, the event data for
            the overlapping days is included in the response rows for
            both date ranges. In a cohort request, this ``dateRanges``
            must be unspecified.
        offset (int):
            The row count of the start row. The first row is counted as
            row 0.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
        limit (int):
            The number of rows to return. If unspecified, 10 rows are
            returned. If -1, all rows are returned.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
        metric_aggregations (Sequence[google.analytics.data_v1alpha.types.MetricAggregation]):
            Aggregation of metrics. Aggregated metric values will be
            shown in rows where the dimension_values are set to
            "RESERVED_(MetricAggregation)".
        dimension_filter (google.analytics.data_v1alpha.types.FilterExpression):
            The filter clause of dimensions. Dimensions
            must be requested to be used in this filter.
            Metrics cannot be used in this filter.
        metric_filter (google.analytics.data_v1alpha.types.FilterExpression):
            The filter clause of metrics. Applied at post
            aggregation phase, similar to SQL having-clause.
            Metrics must be requested to be used in this
            filter. Dimensions cannot be used in this
            filter.
        order_bys (Sequence[google.analytics.data_v1alpha.types.OrderBy]):
            Specifies how rows are ordered in the
            response.
        currency_code (str):
            A currency code in ISO4217 format, such as
            "AED", "USD", "JPY". If the field is empty, the
            report uses the entity's default currency.
        cohort_spec (google.analytics.data_v1alpha.types.CohortSpec):
            Cohort group associated with this request. If
            there is a cohort group in the request the
            'cohort' dimension must be present.
        keep_empty_rows (bool):
            If false or unspecified, each row with all
            metrics equal to 0 will not be returned. If
            true, these rows will be returned if they are
            not separately removed by a filter.
        return_property_quota (bool):
            Toggles whether to return the current state of this
            Analytics Property's quota. Quota is returned in
            `PropertyQuota <#PropertyQuota>`__.
    """

    entity = proto.Field(proto.MESSAGE, number=1, message=data.Entity,)
    dimensions = proto.RepeatedField(proto.MESSAGE, number=2, message=data.Dimension,)
    metrics = proto.RepeatedField(proto.MESSAGE, number=3, message=data.Metric,)
    date_ranges = proto.RepeatedField(proto.MESSAGE, number=4, message=data.DateRange,)
    offset = proto.Field(proto.INT64, number=5,)
    limit = proto.Field(proto.INT64, number=6,)
    metric_aggregations = proto.RepeatedField(
        proto.ENUM, number=7, enum=data.MetricAggregation,
    )
    dimension_filter = proto.Field(
        proto.MESSAGE, number=8, message=data.FilterExpression,
    )
    metric_filter = proto.Field(proto.MESSAGE, number=9, message=data.FilterExpression,)
    order_bys = proto.RepeatedField(proto.MESSAGE, number=10, message=data.OrderBy,)
    currency_code = proto.Field(proto.STRING, number=11,)
    cohort_spec = proto.Field(proto.MESSAGE, number=12, message=data.CohortSpec,)
    keep_empty_rows = proto.Field(proto.BOOL, number=13,)
    return_property_quota = proto.Field(proto.BOOL, number=14,)


class RunReportResponse(proto.Message):
    r"""The response report table corresponding to a request.
    Attributes:
        dimension_headers (Sequence[google.analytics.data_v1alpha.types.DimensionHeader]):
            Describes dimension columns. The number of
            DimensionHeaders and ordering of
            DimensionHeaders matches the dimensions present
            in rows.
        metric_headers (Sequence[google.analytics.data_v1alpha.types.MetricHeader]):
            Describes metric columns. The number of
            MetricHeaders and ordering of MetricHeaders
            matches the metrics present in rows.
        rows (Sequence[google.analytics.data_v1alpha.types.Row]):
            Rows of dimension value combinations and
            metric values in the report.
        totals (Sequence[google.analytics.data_v1alpha.types.Row]):
            If requested, the totaled values of metrics.
        maximums (Sequence[google.analytics.data_v1alpha.types.Row]):
            If requested, the maximum values of metrics.
        minimums (Sequence[google.analytics.data_v1alpha.types.Row]):
            If requested, the minimum values of metrics.
        row_count (int):
            The total number of rows in the query result, regardless of
            the number of rows returned in the response. For example if
            a query returns 175 rows and includes limit = 50 in the API
            request, the response will contain row_count = 175 but only
            50 rows.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
        metadata (google.analytics.data_v1alpha.types.ResponseMetaData):
            Metadata for the report.
        property_quota (google.analytics.data_v1alpha.types.PropertyQuota):
            This Analytics Property's quota state
            including this request.
    """

    dimension_headers = proto.RepeatedField(
        proto.MESSAGE, number=11, message=data.DimensionHeader,
    )
    metric_headers = proto.RepeatedField(
        proto.MESSAGE, number=1, message=data.MetricHeader,
    )
    rows = proto.RepeatedField(proto.MESSAGE, number=2, message=data.Row,)
    totals = proto.RepeatedField(proto.MESSAGE, number=8, message=data.Row,)
    maximums = proto.RepeatedField(proto.MESSAGE, number=9, message=data.Row,)
    minimums = proto.RepeatedField(proto.MESSAGE, number=10, message=data.Row,)
    row_count = proto.Field(proto.INT32, number=12,)
    metadata = proto.Field(proto.MESSAGE, number=6, message=data.ResponseMetaData,)
    property_quota = proto.Field(proto.MESSAGE, number=7, message=data.PropertyQuota,)


class RunPivotReportRequest(proto.Message):
    r"""The request to generate a pivot report.
    Attributes:
        entity (google.analytics.data_v1alpha.types.Entity):
            A property whose events are tracked. Within a
            batch request, this entity should either be
            unspecified or consistent with the batch-level
            entity.
        dimensions (Sequence[google.analytics.data_v1alpha.types.Dimension]):
            The dimensions requested. All defined dimensions must be
            used by one of the following: dimension_expression,
            dimension_filter, pivots, order_bys.
        metrics (Sequence[google.analytics.data_v1alpha.types.Metric]):
            The metrics requested, at least one metric needs to be
            specified. All defined metrics must be used by one of the
            following: metric_expression, metric_filter, order_bys.
        dimension_filter (google.analytics.data_v1alpha.types.FilterExpression):
            The filter clause of dimensions. Dimensions
            must be requested to be used in this filter.
            Metrics cannot be used in this filter.
        metric_filter (google.analytics.data_v1alpha.types.FilterExpression):
            The filter clause of metrics. Applied at post
            aggregation phase, similar to SQL having-clause.
            Metrics must be requested to be used in this
            filter. Dimensions cannot be used in this
            filter.
        pivots (Sequence[google.analytics.data_v1alpha.types.Pivot]):
            Describes the visual format of the report's
            dimensions in columns or rows. The union of the
            fieldNames (dimension names) in all pivots must
            be a subset of dimension names defined in
            Dimensions. No two pivots can share a dimension.
            A dimension is only visible if it appears in a
            pivot.
        date_ranges (Sequence[google.analytics.data_v1alpha.types.DateRange]):
            The date range to retrieve event data for the report. If
            multiple date ranges are specified, event data from each
            date range is used in the report. A special dimension with
            field name "dateRange" can be included in a Pivot's field
            names; if included, the report compares between date ranges.
            In a cohort request, this ``dateRanges`` must be
            unspecified.
        currency_code (str):
            A currency code in ISO4217 format, such as
            "AED", "USD", "JPY". If the field is empty, the
            report uses the entity's default currency.
        cohort_spec (google.analytics.data_v1alpha.types.CohortSpec):
            Cohort group associated with this request. If
            there is a cohort group in the request the
            'cohort' dimension must be present.
        keep_empty_rows (bool):
            If false or unspecified, each row with all
            metrics equal to 0 will not be returned. If
            true, these rows will be returned if they are
            not separately removed by a filter.
        return_property_quota (bool):
            Toggles whether to return the current state of this
            Analytics Property's quota. Quota is returned in
            `PropertyQuota <#PropertyQuota>`__.
    """

    entity = proto.Field(proto.MESSAGE, number=1, message=data.Entity,)
    dimensions = proto.RepeatedField(proto.MESSAGE, number=2, message=data.Dimension,)
    metrics = proto.RepeatedField(proto.MESSAGE, number=3, message=data.Metric,)
    dimension_filter = proto.Field(
        proto.MESSAGE, number=4, message=data.FilterExpression,
    )
    metric_filter = proto.Field(proto.MESSAGE, number=5, message=data.FilterExpression,)
    pivots = proto.RepeatedField(proto.MESSAGE, number=6, message=data.Pivot,)
    date_ranges = proto.RepeatedField(proto.MESSAGE, number=7, message=data.DateRange,)
    currency_code = proto.Field(proto.STRING, number=8,)
    cohort_spec = proto.Field(proto.MESSAGE, number=9, message=data.CohortSpec,)
    keep_empty_rows = proto.Field(proto.BOOL, number=10,)
    return_property_quota = proto.Field(proto.BOOL, number=11,)


class RunPivotReportResponse(proto.Message):
    r"""The response pivot report table corresponding to a pivot
    request.

    Attributes:
        pivot_headers (Sequence[google.analytics.data_v1alpha.types.PivotHeader]):
            Summarizes the columns and rows created by a pivot. Each
            pivot in the request produces one header in the response. If
            we have a request like this:

            ::

                "pivots": [{
                  "fieldNames": ["country",
                    "city"]
                },
                {
                  "fieldNames": "eventName"
                }]

            We will have the following ``pivotHeaders`` in the response:

            ::

                "pivotHeaders" : [{
                  "dimensionHeaders": [{
                    "dimensionValues": [
                       { "value": "United Kingdom" },
                       { "value": "London" }
                     ]
                  },
                  {
                    "dimensionValues": [
                    { "value": "Japan" },
                    { "value": "Osaka" }
                    ]
                  }]
                },
                {
                  "dimensionHeaders": [{
                    "dimensionValues": [{ "value": "session_start" }]
                  },
                  {
                    "dimensionValues": [{ "value": "scroll" }]
                  }]
                }]
        dimension_headers (Sequence[google.analytics.data_v1alpha.types.DimensionHeader]):
            Describes dimension columns. The number of
            DimensionHeaders and ordering of
            DimensionHeaders matches the dimensions present
            in rows.
        metric_headers (Sequence[google.analytics.data_v1alpha.types.MetricHeader]):
            Describes metric columns. The number of
            MetricHeaders and ordering of MetricHeaders
            matches the metrics present in rows.
        rows (Sequence[google.analytics.data_v1alpha.types.Row]):
            Rows of dimension value combinations and
            metric values in the report.
        aggregates (Sequence[google.analytics.data_v1alpha.types.Row]):
            Aggregation of metric values. Can be totals, minimums, or
            maximums. The returned aggregations are controlled by the
            metric_aggregations in the pivot. The type of aggregation
            returned in each row is shown by the dimension_values which
            are set to "RESERVED\_".
        metadata (google.analytics.data_v1alpha.types.ResponseMetaData):
            Metadata for the report.
        property_quota (google.analytics.data_v1alpha.types.PropertyQuota):
            This Analytics Property's quota state
            including this request.
    """

    pivot_headers = proto.RepeatedField(
        proto.MESSAGE, number=1, message=data.PivotHeader,
    )
    dimension_headers = proto.RepeatedField(
        proto.MESSAGE, number=7, message=data.DimensionHeader,
    )
    metric_headers = proto.RepeatedField(
        proto.MESSAGE, number=2, message=data.MetricHeader,
    )
    rows = proto.RepeatedField(proto.MESSAGE, number=3, message=data.Row,)
    aggregates = proto.RepeatedField(proto.MESSAGE, number=4, message=data.Row,)
    metadata = proto.Field(proto.MESSAGE, number=5, message=data.ResponseMetaData,)
    property_quota = proto.Field(proto.MESSAGE, number=6, message=data.PropertyQuota,)


class BatchRunReportsRequest(proto.Message):
    r"""The batch request containing multiple report requests.
    Attributes:
        entity (google.analytics.data_v1alpha.types.Entity):
            A property whose events are tracked. This
            entity must be specified for the batch. The
            entity within RunReportRequest may either be
            unspecified or consistent with this entity.
        requests (Sequence[google.analytics.data_v1alpha.types.RunReportRequest]):
            Individual requests. Each request has a
            separate report response. Each batch request is
            allowed up to 5 requests.
    """

    entity = proto.Field(proto.MESSAGE, number=1, message=data.Entity,)
    requests = proto.RepeatedField(proto.MESSAGE, number=2, message="RunReportRequest",)


class BatchRunReportsResponse(proto.Message):
    r"""The batch response containing multiple reports.
    Attributes:
        reports (Sequence[google.analytics.data_v1alpha.types.RunReportResponse]):
            Individual responses. Each response has a
            separate report request.
    """

    reports = proto.RepeatedField(proto.MESSAGE, number=1, message="RunReportResponse",)


class BatchRunPivotReportsRequest(proto.Message):
    r"""The batch request containing multiple pivot report requests.
    Attributes:
        entity (google.analytics.data_v1alpha.types.Entity):
            A property whose events are tracked. This
            entity must be specified for the batch. The
            entity within RunPivotReportRequest may either
            be unspecified or consistent with this entity.
        requests (Sequence[google.analytics.data_v1alpha.types.RunPivotReportRequest]):
            Individual requests. Each request has a
            separate pivot report response. Each batch
            request is allowed up to 5 requests.
    """

    entity = proto.Field(proto.MESSAGE, number=1, message=data.Entity,)
    requests = proto.RepeatedField(
        proto.MESSAGE, number=2, message="RunPivotReportRequest",
    )


class BatchRunPivotReportsResponse(proto.Message):
    r"""The batch response containing multiple pivot reports.
    Attributes:
        pivot_reports (Sequence[google.analytics.data_v1alpha.types.RunPivotReportResponse]):
            Individual responses. Each response has a
            separate pivot report request.
    """

    pivot_reports = proto.RepeatedField(
        proto.MESSAGE, number=1, message="RunPivotReportResponse",
    )


class GetMetadataRequest(proto.Message):
    r"""Request for a property's dimension and metric metadata.
    Attributes:
        name (str):
            Required. The resource name of the metadata to retrieve.
            This name field is specified in the URL path and not URL
            parameters. Property is a numeric Google Analytics GA4
            Property identifier. To learn more, see `where to find your
            Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.

            Example: properties/1234/metadata

            Set the Property ID to 0 for dimensions and metrics common
            to all properties. In this special mode, this method will
            not return custom dimensions and metrics.
    """

    name = proto.Field(proto.STRING, number=1,)


class RunRealtimeReportRequest(proto.Message):
    r"""The request to generate a realtime report.
    Attributes:
        property (str):
            A Google Analytics GA4 property identifier whose events are
            tracked. Specified in the URL path and not the body. To
            learn more, see `where to find your Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.

            Example: properties/1234
        dimensions (Sequence[google.analytics.data_v1alpha.types.Dimension]):
            The dimensions requested and displayed.
        metrics (Sequence[google.analytics.data_v1alpha.types.Metric]):
            The metrics requested and displayed.
        limit (int):
            The number of rows to return. If unspecified,
            10 rows are returned. If -1, all rows are
            returned.
        dimension_filter (google.analytics.data_v1alpha.types.FilterExpression):
            The filter clause of dimensions. Dimensions
            must be requested to be used in this filter.
            Metrics cannot be used in this filter.
        metric_filter (google.analytics.data_v1alpha.types.FilterExpression):
            The filter clause of metrics. Applied at post
            aggregation phase, similar to SQL having-clause.
            Metrics must be requested to be used in this
            filter. Dimensions cannot be used in this
            filter.
        metric_aggregations (Sequence[google.analytics.data_v1alpha.types.MetricAggregation]):
            Aggregation of metrics. Aggregated metric values will be
            shown in rows where the dimension_values are set to
            "RESERVED_(MetricAggregation)".
        order_bys (Sequence[google.analytics.data_v1alpha.types.OrderBy]):
            Specifies how rows are ordered in the
            response.
        return_property_quota (bool):
            Toggles whether to return the current state of this
            Analytics Property's Realtime quota. Quota is returned in
            `PropertyQuota <#PropertyQuota>`__.
    """

    property = proto.Field(proto.STRING, number=1,)
    dimensions = proto.RepeatedField(proto.MESSAGE, number=2, message=data.Dimension,)
    metrics = proto.RepeatedField(proto.MESSAGE, number=3, message=data.Metric,)
    limit = proto.Field(proto.INT64, number=4,)
    dimension_filter = proto.Field(
        proto.MESSAGE, number=5, message=data.FilterExpression,
    )
    metric_filter = proto.Field(proto.MESSAGE, number=6, message=data.FilterExpression,)
    metric_aggregations = proto.RepeatedField(
        proto.ENUM, number=7, enum=data.MetricAggregation,
    )
    order_bys = proto.RepeatedField(proto.MESSAGE, number=8, message=data.OrderBy,)
    return_property_quota = proto.Field(proto.BOOL, number=9,)


class RunRealtimeReportResponse(proto.Message):
    r"""The response realtime report table corresponding to a
    request.

    Attributes:
        dimension_headers (Sequence[google.analytics.data_v1alpha.types.DimensionHeader]):
            Describes dimension columns. The number of
            DimensionHeaders and ordering of
            DimensionHeaders matches the dimensions present
            in rows.
        metric_headers (Sequence[google.analytics.data_v1alpha.types.MetricHeader]):
            Describes metric columns. The number of
            MetricHeaders and ordering of MetricHeaders
            matches the metrics present in rows.
        rows (Sequence[google.analytics.data_v1alpha.types.Row]):
            Rows of dimension value combinations and
            metric values in the report.
        totals (Sequence[google.analytics.data_v1alpha.types.Row]):
            If requested, the totaled values of metrics.
        maximums (Sequence[google.analytics.data_v1alpha.types.Row]):
            If requested, the maximum values of metrics.
        minimums (Sequence[google.analytics.data_v1alpha.types.Row]):
            If requested, the minimum values of metrics.
        row_count (int):
            The total number of rows in the query result, regardless of
            the number of rows returned in the response. For example if
            a query returns 175 rows and includes limit = 50 in the API
            request, the response will contain row_count = 175 but only
            50 rows.
        property_quota (google.analytics.data_v1alpha.types.PropertyQuota):
            This Analytics Property's Realtime quota
            state including this request.
    """

    dimension_headers = proto.RepeatedField(
        proto.MESSAGE, number=1, message=data.DimensionHeader,
    )
    metric_headers = proto.RepeatedField(
        proto.MESSAGE, number=2, message=data.MetricHeader,
    )
    rows = proto.RepeatedField(proto.MESSAGE, number=3, message=data.Row,)
    totals = proto.RepeatedField(proto.MESSAGE, number=4, message=data.Row,)
    maximums = proto.RepeatedField(proto.MESSAGE, number=5, message=data.Row,)
    minimums = proto.RepeatedField(proto.MESSAGE, number=6, message=data.Row,)
    row_count = proto.Field(proto.INT32, number=7,)
    property_quota = proto.Field(proto.MESSAGE, number=8, message=data.PropertyQuota,)


__all__ = tuple(sorted(__protobuf__.manifest))
