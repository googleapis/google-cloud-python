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

from google.analytics.data_v1beta.types import data


__protobuf__ = proto.module(
    package="google.analytics.data.v1beta",
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
        dimensions (Sequence[google.analytics.data_v1beta.types.DimensionMetadata]):
            The dimension descriptions.
        metrics (Sequence[google.analytics.data_v1beta.types.MetricMetadata]):
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
        property (str):
            A Google Analytics GA4 property identifier whose events are
            tracked. Specified in the URL path and not the body. To
            learn more, see `where to find your Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.
            Within a batch request, this property should either be
            unspecified or consistent with the batch-level property.

            Example: properties/1234
        dimensions (Sequence[google.analytics.data_v1beta.types.Dimension]):
            The dimensions requested and displayed.
        metrics (Sequence[google.analytics.data_v1beta.types.Metric]):
            The metrics requested and displayed.
        date_ranges (Sequence[google.analytics.data_v1beta.types.DateRange]):
            Date ranges of data to read. If multiple date ranges are
            requested, each response row will contain a zero based date
            range index. If two date ranges overlap, the event data for
            the overlapping days is included in the response rows for
            both date ranges. In a cohort request, this ``dateRanges``
            must be unspecified.
        dimension_filter (google.analytics.data_v1beta.types.FilterExpression):
            The filter clause of dimensions. Dimensions
            must be requested to be used in this filter.
            Metrics cannot be used in this filter.
        metric_filter (google.analytics.data_v1beta.types.FilterExpression):
            The filter clause of metrics. Applied at post
            aggregation phase, similar to SQL having-clause.
            Metrics must be requested to be used in this
            filter. Dimensions cannot be used in this
            filter.
        offset (int):
            The row count of the start row. The first row is counted as
            row 0.

            When paging, the first request does not specify offset; or
            equivalently, sets offset to 0; the first request returns
            the first ``limit`` of rows. The second request sets offset
            to the ``limit`` of the first request; the second request
            returns the second ``limit`` of rows.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
        limit (int):
            The number of rows to return. If unspecified, 10,000 rows
            are returned. The API returns a maximum of 100,000 rows per
            request, no matter how many you ask for. ``limit`` must be
            positive.

            The API can also return fewer rows than the requested
            ``limit``, if there aren't as many dimension values as the
            ``limit``. For instance, there are fewer than 300 possible
            values for the dimension ``country``, so when reporting on
            only ``country``, you can't get more than 300 rows, even if
            you set ``limit`` to a higher value.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
        metric_aggregations (Sequence[google.analytics.data_v1beta.types.MetricAggregation]):
            Aggregation of metrics. Aggregated metric values will be
            shown in rows where the dimension_values are set to
            "RESERVED_(MetricAggregation)".
        order_bys (Sequence[google.analytics.data_v1beta.types.OrderBy]):
            Specifies how rows are ordered in the
            response.
        currency_code (str):
            A currency code in ISO4217 format, such as
            "AED", "USD", "JPY". If the field is empty, the
            report uses the property's default currency.
        cohort_spec (google.analytics.data_v1beta.types.CohortSpec):
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

    property = proto.Field(proto.STRING, number=1,)
    dimensions = proto.RepeatedField(proto.MESSAGE, number=2, message=data.Dimension,)
    metrics = proto.RepeatedField(proto.MESSAGE, number=3, message=data.Metric,)
    date_ranges = proto.RepeatedField(proto.MESSAGE, number=4, message=data.DateRange,)
    dimension_filter = proto.Field(
        proto.MESSAGE, number=5, message=data.FilterExpression,
    )
    metric_filter = proto.Field(proto.MESSAGE, number=6, message=data.FilterExpression,)
    offset = proto.Field(proto.INT64, number=7,)
    limit = proto.Field(proto.INT64, number=8,)
    metric_aggregations = proto.RepeatedField(
        proto.ENUM, number=9, enum=data.MetricAggregation,
    )
    order_bys = proto.RepeatedField(proto.MESSAGE, number=10, message=data.OrderBy,)
    currency_code = proto.Field(proto.STRING, number=11,)
    cohort_spec = proto.Field(proto.MESSAGE, number=12, message=data.CohortSpec,)
    keep_empty_rows = proto.Field(proto.BOOL, number=13,)
    return_property_quota = proto.Field(proto.BOOL, number=14,)


class RunReportResponse(proto.Message):
    r"""The response report table corresponding to a request.
    Attributes:
        dimension_headers (Sequence[google.analytics.data_v1beta.types.DimensionHeader]):
            Describes dimension columns. The number of
            DimensionHeaders and ordering of
            DimensionHeaders matches the dimensions present
            in rows.
        metric_headers (Sequence[google.analytics.data_v1beta.types.MetricHeader]):
            Describes metric columns. The number of
            MetricHeaders and ordering of MetricHeaders
            matches the metrics present in rows.
        rows (Sequence[google.analytics.data_v1beta.types.Row]):
            Rows of dimension value combinations and
            metric values in the report.
        totals (Sequence[google.analytics.data_v1beta.types.Row]):
            If requested, the totaled values of metrics.
        maximums (Sequence[google.analytics.data_v1beta.types.Row]):
            If requested, the maximum values of metrics.
        minimums (Sequence[google.analytics.data_v1beta.types.Row]):
            If requested, the minimum values of metrics.
        row_count (int):
            The total number of rows in the query result. ``rowCount``
            is independent of the number of rows returned in the
            response, the ``limit`` request parameter, and the
            ``offset`` request parameter. For example if a query returns
            175 rows and includes ``limit`` of 50 in the API request,
            the response will contain ``rowCount`` of 175 but only 50
            rows.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
        metadata (google.analytics.data_v1beta.types.ResponseMetaData):
            Metadata for the report.
        property_quota (google.analytics.data_v1beta.types.PropertyQuota):
            This Analytics Property's quota state
            including this request.
        kind (str):
            Identifies what kind of resource this message is. This
            ``kind`` is always the fixed string
            "analyticsData#runReport". Useful to distinguish between
            response types in JSON.
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
    metadata = proto.Field(proto.MESSAGE, number=8, message=data.ResponseMetaData,)
    property_quota = proto.Field(proto.MESSAGE, number=9, message=data.PropertyQuota,)
    kind = proto.Field(proto.STRING, number=10,)


class RunPivotReportRequest(proto.Message):
    r"""The request to generate a pivot report.
    Attributes:
        property (str):
            A Google Analytics GA4 property identifier whose events are
            tracked. Specified in the URL path and not the body. To
            learn more, see `where to find your Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.
            Within a batch request, this property should either be
            unspecified or consistent with the batch-level property.

            Example: properties/1234
        dimensions (Sequence[google.analytics.data_v1beta.types.Dimension]):
            The dimensions requested. All defined dimensions must be
            used by one of the following: dimension_expression,
            dimension_filter, pivots, order_bys.
        metrics (Sequence[google.analytics.data_v1beta.types.Metric]):
            The metrics requested, at least one metric needs to be
            specified. All defined metrics must be used by one of the
            following: metric_expression, metric_filter, order_bys.
        date_ranges (Sequence[google.analytics.data_v1beta.types.DateRange]):
            The date range to retrieve event data for the report. If
            multiple date ranges are specified, event data from each
            date range is used in the report. A special dimension with
            field name "dateRange" can be included in a Pivot's field
            names; if included, the report compares between date ranges.
            In a cohort request, this ``dateRanges`` must be
            unspecified.
        pivots (Sequence[google.analytics.data_v1beta.types.Pivot]):
            Describes the visual format of the report's
            dimensions in columns or rows. The union of the
            fieldNames (dimension names) in all pivots must
            be a subset of dimension names defined in
            Dimensions. No two pivots can share a dimension.
            A dimension is only visible if it appears in a
            pivot.
        dimension_filter (google.analytics.data_v1beta.types.FilterExpression):
            The filter clause of dimensions. Dimensions
            must be requested to be used in this filter.
            Metrics cannot be used in this filter.
        metric_filter (google.analytics.data_v1beta.types.FilterExpression):
            The filter clause of metrics. Applied at post
            aggregation phase, similar to SQL having-clause.
            Metrics must be requested to be used in this
            filter. Dimensions cannot be used in this
            filter.
        currency_code (str):
            A currency code in ISO4217 format, such as
            "AED", "USD", "JPY". If the field is empty, the
            report uses the property's default currency.
        cohort_spec (google.analytics.data_v1beta.types.CohortSpec):
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

    property = proto.Field(proto.STRING, number=1,)
    dimensions = proto.RepeatedField(proto.MESSAGE, number=2, message=data.Dimension,)
    metrics = proto.RepeatedField(proto.MESSAGE, number=3, message=data.Metric,)
    date_ranges = proto.RepeatedField(proto.MESSAGE, number=4, message=data.DateRange,)
    pivots = proto.RepeatedField(proto.MESSAGE, number=5, message=data.Pivot,)
    dimension_filter = proto.Field(
        proto.MESSAGE, number=6, message=data.FilterExpression,
    )
    metric_filter = proto.Field(proto.MESSAGE, number=7, message=data.FilterExpression,)
    currency_code = proto.Field(proto.STRING, number=8,)
    cohort_spec = proto.Field(proto.MESSAGE, number=9, message=data.CohortSpec,)
    keep_empty_rows = proto.Field(proto.BOOL, number=10,)
    return_property_quota = proto.Field(proto.BOOL, number=11,)


class RunPivotReportResponse(proto.Message):
    r"""The response pivot report table corresponding to a pivot
    request.

    Attributes:
        pivot_headers (Sequence[google.analytics.data_v1beta.types.PivotHeader]):
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
        dimension_headers (Sequence[google.analytics.data_v1beta.types.DimensionHeader]):
            Describes dimension columns. The number of
            DimensionHeaders and ordering of
            DimensionHeaders matches the dimensions present
            in rows.
        metric_headers (Sequence[google.analytics.data_v1beta.types.MetricHeader]):
            Describes metric columns. The number of
            MetricHeaders and ordering of MetricHeaders
            matches the metrics present in rows.
        rows (Sequence[google.analytics.data_v1beta.types.Row]):
            Rows of dimension value combinations and
            metric values in the report.
        aggregates (Sequence[google.analytics.data_v1beta.types.Row]):
            Aggregation of metric values. Can be totals, minimums, or
            maximums. The returned aggregations are controlled by the
            metric_aggregations in the pivot. The type of aggregation
            returned in each row is shown by the dimension_values which
            are set to "RESERVED\_".
        metadata (google.analytics.data_v1beta.types.ResponseMetaData):
            Metadata for the report.
        property_quota (google.analytics.data_v1beta.types.PropertyQuota):
            This Analytics Property's quota state
            including this request.
        kind (str):
            Identifies what kind of resource this message is. This
            ``kind`` is always the fixed string
            "analyticsData#runPivotReport". Useful to distinguish
            between response types in JSON.
    """

    pivot_headers = proto.RepeatedField(
        proto.MESSAGE, number=1, message=data.PivotHeader,
    )
    dimension_headers = proto.RepeatedField(
        proto.MESSAGE, number=2, message=data.DimensionHeader,
    )
    metric_headers = proto.RepeatedField(
        proto.MESSAGE, number=3, message=data.MetricHeader,
    )
    rows = proto.RepeatedField(proto.MESSAGE, number=4, message=data.Row,)
    aggregates = proto.RepeatedField(proto.MESSAGE, number=5, message=data.Row,)
    metadata = proto.Field(proto.MESSAGE, number=6, message=data.ResponseMetaData,)
    property_quota = proto.Field(proto.MESSAGE, number=7, message=data.PropertyQuota,)
    kind = proto.Field(proto.STRING, number=8,)


class BatchRunReportsRequest(proto.Message):
    r"""The batch request containing multiple report requests.
    Attributes:
        property (str):
            A Google Analytics GA4 property identifier whose events are
            tracked. Specified in the URL path and not the body. To
            learn more, see `where to find your Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.
            This property must be specified for the batch. The property
            within RunReportRequest may either be unspecified or
            consistent with this property.

            Example: properties/1234
        requests (Sequence[google.analytics.data_v1beta.types.RunReportRequest]):
            Individual requests. Each request has a
            separate report response. Each batch request is
            allowed up to 5 requests.
    """

    property = proto.Field(proto.STRING, number=1,)
    requests = proto.RepeatedField(proto.MESSAGE, number=2, message="RunReportRequest",)


class BatchRunReportsResponse(proto.Message):
    r"""The batch response containing multiple reports.
    Attributes:
        reports (Sequence[google.analytics.data_v1beta.types.RunReportResponse]):
            Individual responses. Each response has a
            separate report request.
        kind (str):
            Identifies what kind of resource this message is. This
            ``kind`` is always the fixed string
            "analyticsData#batchRunReports". Useful to distinguish
            between response types in JSON.
    """

    reports = proto.RepeatedField(proto.MESSAGE, number=1, message="RunReportResponse",)
    kind = proto.Field(proto.STRING, number=2,)


class BatchRunPivotReportsRequest(proto.Message):
    r"""The batch request containing multiple pivot report requests.
    Attributes:
        property (str):
            A Google Analytics GA4 property identifier whose events are
            tracked. Specified in the URL path and not the body. To
            learn more, see `where to find your Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.
            This property must be specified for the batch. The property
            within RunPivotReportRequest may either be unspecified or
            consistent with this property.

            Example: properties/1234
        requests (Sequence[google.analytics.data_v1beta.types.RunPivotReportRequest]):
            Individual requests. Each request has a
            separate pivot report response. Each batch
            request is allowed up to 5 requests.
    """

    property = proto.Field(proto.STRING, number=1,)
    requests = proto.RepeatedField(
        proto.MESSAGE, number=2, message="RunPivotReportRequest",
    )


class BatchRunPivotReportsResponse(proto.Message):
    r"""The batch response containing multiple pivot reports.
    Attributes:
        pivot_reports (Sequence[google.analytics.data_v1beta.types.RunPivotReportResponse]):
            Individual responses. Each response has a
            separate pivot report request.
        kind (str):
            Identifies what kind of resource this message is. This
            ``kind`` is always the fixed string
            "analyticsData#batchRunPivotReports". Useful to distinguish
            between response types in JSON.
    """

    pivot_reports = proto.RepeatedField(
        proto.MESSAGE, number=1, message="RunPivotReportResponse",
    )
    kind = proto.Field(proto.STRING, number=2,)


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
        dimensions (Sequence[google.analytics.data_v1beta.types.Dimension]):
            The dimensions requested and displayed.
        metrics (Sequence[google.analytics.data_v1beta.types.Metric]):
            The metrics requested and displayed.
        dimension_filter (google.analytics.data_v1beta.types.FilterExpression):
            The filter clause of dimensions. Dimensions
            must be requested to be used in this filter.
            Metrics cannot be used in this filter.
        metric_filter (google.analytics.data_v1beta.types.FilterExpression):
            The filter clause of metrics. Applied at post
            aggregation phase, similar to SQL having-clause.
            Metrics must be requested to be used in this
            filter. Dimensions cannot be used in this
            filter.
        limit (int):
            The number of rows to return. If unspecified, 10,000 rows
            are returned. The API returns a maximum of 100,000 rows per
            request, no matter how many you ask for. ``limit`` must be
            positive.

            The API can also return fewer rows than the requested
            ``limit``, if there aren't as many dimension values as the
            ``limit``. For instance, there are fewer than 300 possible
            values for the dimension ``country``, so when reporting on
            only ``country``, you can't get more than 300 rows, even if
            you set ``limit`` to a higher value.
        metric_aggregations (Sequence[google.analytics.data_v1beta.types.MetricAggregation]):
            Aggregation of metrics. Aggregated metric values will be
            shown in rows where the dimension_values are set to
            "RESERVED_(MetricAggregation)".
        order_bys (Sequence[google.analytics.data_v1beta.types.OrderBy]):
            Specifies how rows are ordered in the
            response.
        return_property_quota (bool):
            Toggles whether to return the current state of this
            Analytics Property's Realtime quota. Quota is returned in
            `PropertyQuota <#PropertyQuota>`__.
        minute_ranges (Sequence[google.analytics.data_v1beta.types.MinuteRange]):
            The minute ranges of event data to read. If
            unspecified, one minute range for the last 30
            minutes will be used. If multiple minute ranges
            are requested, each response row will contain a
            zero based minute range index. If two minute
            ranges overlap, the event data for the
            overlapping minutes is included in the response
            rows for both minute ranges.
    """

    property = proto.Field(proto.STRING, number=1,)
    dimensions = proto.RepeatedField(proto.MESSAGE, number=2, message=data.Dimension,)
    metrics = proto.RepeatedField(proto.MESSAGE, number=3, message=data.Metric,)
    dimension_filter = proto.Field(
        proto.MESSAGE, number=4, message=data.FilterExpression,
    )
    metric_filter = proto.Field(proto.MESSAGE, number=5, message=data.FilterExpression,)
    limit = proto.Field(proto.INT64, number=6,)
    metric_aggregations = proto.RepeatedField(
        proto.ENUM, number=7, enum=data.MetricAggregation,
    )
    order_bys = proto.RepeatedField(proto.MESSAGE, number=8, message=data.OrderBy,)
    return_property_quota = proto.Field(proto.BOOL, number=9,)
    minute_ranges = proto.RepeatedField(
        proto.MESSAGE, number=10, message=data.MinuteRange,
    )


class RunRealtimeReportResponse(proto.Message):
    r"""The response realtime report table corresponding to a
    request.

    Attributes:
        dimension_headers (Sequence[google.analytics.data_v1beta.types.DimensionHeader]):
            Describes dimension columns. The number of
            DimensionHeaders and ordering of
            DimensionHeaders matches the dimensions present
            in rows.
        metric_headers (Sequence[google.analytics.data_v1beta.types.MetricHeader]):
            Describes metric columns. The number of
            MetricHeaders and ordering of MetricHeaders
            matches the metrics present in rows.
        rows (Sequence[google.analytics.data_v1beta.types.Row]):
            Rows of dimension value combinations and
            metric values in the report.
        totals (Sequence[google.analytics.data_v1beta.types.Row]):
            If requested, the totaled values of metrics.
        maximums (Sequence[google.analytics.data_v1beta.types.Row]):
            If requested, the maximum values of metrics.
        minimums (Sequence[google.analytics.data_v1beta.types.Row]):
            If requested, the minimum values of metrics.
        row_count (int):
            The total number of rows in the query result. ``rowCount``
            is independent of the number of rows returned in the
            response and the ``limit`` request parameter. For example if
            a query returns 175 rows and includes ``limit`` of 50 in the
            API request, the response will contain ``rowCount`` of 175
            but only 50 rows.
        property_quota (google.analytics.data_v1beta.types.PropertyQuota):
            This Analytics Property's Realtime quota
            state including this request.
        kind (str):
            Identifies what kind of resource this message is. This
            ``kind`` is always the fixed string
            "analyticsData#runRealtimeReport". Useful to distinguish
            between response types in JSON.
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
    kind = proto.Field(proto.STRING, number=9,)


__all__ = tuple(sorted(__protobuf__.manifest))
