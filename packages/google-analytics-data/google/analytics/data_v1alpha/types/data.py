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


__protobuf__ = proto.module(
    package="google.analytics.data.v1alpha",
    manifest={
        "MetricAggregation",
        "MetricType",
        "DateRange",
        "Entity",
        "Dimension",
        "DimensionExpression",
        "Metric",
        "FilterExpression",
        "FilterExpressionList",
        "Filter",
        "OrderBy",
        "Pivot",
        "CohortSpec",
        "Cohort",
        "CohortsRange",
        "CohortReportSettings",
        "ResponseMetaData",
        "DimensionHeader",
        "MetricHeader",
        "PivotHeader",
        "PivotDimensionHeader",
        "Row",
        "DimensionValue",
        "MetricValue",
        "NumericValue",
        "PropertyQuota",
        "QuotaStatus",
        "DimensionMetadata",
        "MetricMetadata",
    },
)


class MetricAggregation(proto.Enum):
    r"""Represents aggregation of metrics."""
    METRIC_AGGREGATION_UNSPECIFIED = 0
    TOTAL = 1
    MINIMUM = 5
    MAXIMUM = 6
    COUNT = 4


class MetricType(proto.Enum):
    r"""A metric's value type."""
    METRIC_TYPE_UNSPECIFIED = 0
    TYPE_INTEGER = 1
    TYPE_FLOAT = 2
    TYPE_SECONDS = 4
    TYPE_MILLISECONDS = 5
    TYPE_MINUTES = 6
    TYPE_HOURS = 7
    TYPE_STANDARD = 8
    TYPE_CURRENCY = 9
    TYPE_FEET = 10
    TYPE_MILES = 11
    TYPE_METERS = 12
    TYPE_KILOMETERS = 13


class DateRange(proto.Message):
    r"""A contiguous set of days: startDate, startDate + 1, ...,
    endDate. Requests are allowed up to 4 date ranges.

    Attributes:
        start_date (str):
            The inclusive start date for the query in the format
            ``YYYY-MM-DD``. Cannot be after ``end_date``. The format
            ``NdaysAgo``, ``yesterday``, or ``today`` is also accepted,
            and in that case, the date is inferred based on the
            property's reporting time zone.
        end_date (str):
            The inclusive end date for the query in the format
            ``YYYY-MM-DD``. Cannot be before ``start_date``. The format
            ``NdaysAgo``, ``yesterday``, or ``today`` is also accepted,
            and in that case, the date is inferred based on the
            property's reporting time zone.
        name (str):
            Assigns a name to this date range. The dimension
            ``dateRange`` is valued to this name in a report response.
            If set, cannot begin with ``date_range_`` or ``RESERVED_``.
            If not set, date ranges are named by their zero based index
            in the request: ``date_range_0``, ``date_range_1``, etc.
    """

    start_date = proto.Field(proto.STRING, number=1,)
    end_date = proto.Field(proto.STRING, number=2,)
    name = proto.Field(proto.STRING, number=3,)


class Entity(proto.Message):
    r"""The unique identifier of the property whose events are
    tracked.

    Attributes:
        property_id (str):
            A Google Analytics GA4 property id. To learn more, see
            `where to find your Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.
    """

    property_id = proto.Field(proto.STRING, number=1,)


class Dimension(proto.Message):
    r"""Dimensions are attributes of your data. For example, the
    dimension city indicates the city from which an event
    originates. Dimension values in report responses are strings;
    for example, city could be "Paris" or "New York". Requests are
    allowed up to 8 dimensions.

    Attributes:
        name (str):
            The name of the dimension. See the `API
            Dimensions <https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#dimensions>`__
            for the list of dimension names.

            If ``dimensionExpression`` is specified, ``name`` can be any
            string that you would like. For example if a
            ``dimensionExpression`` concatenates ``country`` and
            ``city``, you could call that dimension ``countryAndCity``.

            Dimensions are referenced by ``name`` in
            ``dimensionFilter``, ``orderBys``, ``dimensionExpression``,
            and ``pivots``.
        dimension_expression (google.analytics.data_v1alpha.types.DimensionExpression):
            One dimension can be the result of an
            expression of multiple dimensions. For example,
            dimension "country, city": concatenate(country,
            ", ", city).
    """

    name = proto.Field(proto.STRING, number=1,)
    dimension_expression = proto.Field(
        proto.MESSAGE, number=2, message="DimensionExpression",
    )


class DimensionExpression(proto.Message):
    r"""Used to express a dimension which is the result of a formula of
    multiple dimensions. Example usages:

    1) lower_case(dimension)
    2) concatenate(dimension1, symbol, dimension2).

    Attributes:
        lower_case (google.analytics.data_v1alpha.types.DimensionExpression.CaseExpression):
            Used to convert a dimension value to lower
            case.
        upper_case (google.analytics.data_v1alpha.types.DimensionExpression.CaseExpression):
            Used to convert a dimension value to upper
            case.
        concatenate (google.analytics.data_v1alpha.types.DimensionExpression.ConcatenateExpression):
            Used to combine dimension values to a single
            dimension. For example, dimension "country,
            city": concatenate(country, ", ", city).
    """

    class CaseExpression(proto.Message):
        r"""Used to convert a dimension value to a single case.
        Attributes:
            dimension_name (str):
                Name of a dimension. The name must refer back
                to a name in dimensions field of the request.
        """

        dimension_name = proto.Field(proto.STRING, number=1,)

    class ConcatenateExpression(proto.Message):
        r"""Used to combine dimension values to a single dimension.
        Attributes:
            dimension_names (Sequence[str]):
                Names of dimensions. The names must refer
                back to names in the dimensions field of the
                request.
            delimiter (str):
                The delimiter placed between dimension names.

                Delimiters are often single characters such as "|" or ","
                but can be longer strings. If a dimension value contains the
                delimiter, both will be present in response with no
                distinction. For example if dimension 1 value = "US,FR",
                dimension 2 value = "JP", and delimiter = ",", then the
                response will contain "US,FR,JP".
        """

        dimension_names = proto.RepeatedField(proto.STRING, number=1,)
        delimiter = proto.Field(proto.STRING, number=2,)

    lower_case = proto.Field(
        proto.MESSAGE, number=4, oneof="one_expression", message=CaseExpression,
    )
    upper_case = proto.Field(
        proto.MESSAGE, number=5, oneof="one_expression", message=CaseExpression,
    )
    concatenate = proto.Field(
        proto.MESSAGE, number=6, oneof="one_expression", message=ConcatenateExpression,
    )


class Metric(proto.Message):
    r"""The quantitative measurements of a report. For example, the metric
    ``eventCount`` is the total number of events. Requests are allowed
    up to 10 metrics.

    Attributes:
        name (str):
            The name of the metric. See the `API
            Metrics <https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#metrics>`__
            for the list of metric names.

            If ``expression`` is specified, ``name`` can be any string
            that you would like. For example if ``expression`` is
            ``screenPageViews/sessions``, you could call that metric's
            name = ``viewsPerSession``.

            Metrics are referenced by ``name`` in ``metricFilter``,
            ``orderBys``, and metric ``expression``.
        expression (str):
            A mathematical expression for derived metrics. For example,
            the metric Event count per user is
            ``eventCount/totalUsers``.
        invisible (bool):
            Indicates if a metric is invisible in the report response.
            If a metric is invisible, the metric will not produce a
            column in the response, but can be used in ``metricFilter``,
            ``orderBys``, or a metric ``expression``.
    """

    name = proto.Field(proto.STRING, number=1,)
    expression = proto.Field(proto.STRING, number=2,)
    invisible = proto.Field(proto.BOOL, number=3,)


class FilterExpression(proto.Message):
    r"""To express dimension or metric filters.
    The fields in the same FilterExpression need to be either all
    dimensions or all metrics.

    Attributes:
        and_group (google.analytics.data_v1alpha.types.FilterExpressionList):
            The FilterExpressions in and_group have an AND relationship.
        or_group (google.analytics.data_v1alpha.types.FilterExpressionList):
            The FilterExpressions in or_group have an OR relationship.
        not_expression (google.analytics.data_v1alpha.types.FilterExpression):
            The FilterExpression is NOT of not_expression.
        filter (google.analytics.data_v1alpha.types.Filter):
            A primitive filter.
            All fields in filter in same FilterExpression
            needs to be either all dimensions or metrics.
    """

    and_group = proto.Field(
        proto.MESSAGE, number=1, oneof="expr", message="FilterExpressionList",
    )
    or_group = proto.Field(
        proto.MESSAGE, number=2, oneof="expr", message="FilterExpressionList",
    )
    not_expression = proto.Field(
        proto.MESSAGE, number=3, oneof="expr", message="FilterExpression",
    )
    filter = proto.Field(proto.MESSAGE, number=4, oneof="expr", message="Filter",)


class FilterExpressionList(proto.Message):
    r"""A list of filter expressions.
    Attributes:
        expressions (Sequence[google.analytics.data_v1alpha.types.FilterExpression]):
            A list of filter expressions.
    """

    expressions = proto.RepeatedField(
        proto.MESSAGE, number=1, message="FilterExpression",
    )


class Filter(proto.Message):
    r"""An expression to filter dimension or metric values.
    Attributes:
        field_name (str):
            The dimension name or metric name. Must be a
            name defined in dimensions or metrics.
        null_filter (bool):
            A filter for null values. If True, a null
            dimension value is matched by this filter. Null
            filter is commonly used inside a NOT filter
            expression. For example, a NOT expression of a
            null filter removes rows when a dimension is
            null.
        string_filter (google.analytics.data_v1alpha.types.Filter.StringFilter):
            Strings related filter.
        in_list_filter (google.analytics.data_v1alpha.types.Filter.InListFilter):
            A filter for in list values.
        numeric_filter (google.analytics.data_v1alpha.types.Filter.NumericFilter):
            A filter for numeric or date values.
        between_filter (google.analytics.data_v1alpha.types.Filter.BetweenFilter):
            A filter for two values.
    """

    class StringFilter(proto.Message):
        r"""The filter for string
        Attributes:
            match_type (google.analytics.data_v1alpha.types.Filter.StringFilter.MatchType):
                The match type for this filter.
            value (str):
                The string value used for the matching.
            case_sensitive (bool):
                If true, the string value is case sensitive.
        """

        class MatchType(proto.Enum):
            r"""The match type of a string filter"""
            MATCH_TYPE_UNSPECIFIED = 0
            EXACT = 1
            BEGINS_WITH = 2
            ENDS_WITH = 3
            CONTAINS = 4
            FULL_REGEXP = 5
            PARTIAL_REGEXP = 6

        match_type = proto.Field(
            proto.ENUM, number=1, enum="Filter.StringFilter.MatchType",
        )
        value = proto.Field(proto.STRING, number=2,)
        case_sensitive = proto.Field(proto.BOOL, number=3,)

    class InListFilter(proto.Message):
        r"""The result needs to be in a list of string values.
        Attributes:
            values (Sequence[str]):
                The list of string values.
                Must be non-empty.
            case_sensitive (bool):
                If true, the string value is case sensitive.
        """

        values = proto.RepeatedField(proto.STRING, number=1,)
        case_sensitive = proto.Field(proto.BOOL, number=2,)

    class NumericFilter(proto.Message):
        r"""Filters for numeric or date values.
        Attributes:
            operation (google.analytics.data_v1alpha.types.Filter.NumericFilter.Operation):
                The operation type for this filter.
            value (google.analytics.data_v1alpha.types.NumericValue):
                A numeric value or a date value.
        """

        class Operation(proto.Enum):
            r"""The operation applied to a numeric filter"""
            OPERATION_UNSPECIFIED = 0
            EQUAL = 1
            LESS_THAN = 2
            LESS_THAN_OR_EQUAL = 3
            GREATER_THAN = 4
            GREATER_THAN_OR_EQUAL = 5

        operation = proto.Field(
            proto.ENUM, number=1, enum="Filter.NumericFilter.Operation",
        )
        value = proto.Field(proto.MESSAGE, number=2, message="NumericValue",)

    class BetweenFilter(proto.Message):
        r"""To express that the result needs to be between two numbers
        (inclusive).

        Attributes:
            from_value (google.analytics.data_v1alpha.types.NumericValue):
                Begins with this number.
            to_value (google.analytics.data_v1alpha.types.NumericValue):
                Ends with this number.
        """

        from_value = proto.Field(proto.MESSAGE, number=1, message="NumericValue",)
        to_value = proto.Field(proto.MESSAGE, number=2, message="NumericValue",)

    field_name = proto.Field(proto.STRING, number=1,)
    null_filter = proto.Field(proto.BOOL, number=2, oneof="one_filter",)
    string_filter = proto.Field(
        proto.MESSAGE, number=3, oneof="one_filter", message=StringFilter,
    )
    in_list_filter = proto.Field(
        proto.MESSAGE, number=4, oneof="one_filter", message=InListFilter,
    )
    numeric_filter = proto.Field(
        proto.MESSAGE, number=5, oneof="one_filter", message=NumericFilter,
    )
    between_filter = proto.Field(
        proto.MESSAGE, number=6, oneof="one_filter", message=BetweenFilter,
    )


class OrderBy(proto.Message):
    r"""The sort options.
    Attributes:
        metric (google.analytics.data_v1alpha.types.OrderBy.MetricOrderBy):
            Sorts results by a metric's values.
        dimension (google.analytics.data_v1alpha.types.OrderBy.DimensionOrderBy):
            Sorts results by a dimension's values.
        pivot (google.analytics.data_v1alpha.types.OrderBy.PivotOrderBy):
            Sorts results by a metric's values within a
            pivot column group.
        desc (bool):
            If true, sorts by descending order.
    """

    class MetricOrderBy(proto.Message):
        r"""Sorts by metric values.
        Attributes:
            metric_name (str):
                A metric name in the request to order by.
        """

        metric_name = proto.Field(proto.STRING, number=1,)

    class DimensionOrderBy(proto.Message):
        r"""Sorts by dimension values.
        Attributes:
            dimension_name (str):
                A dimension name in the request to order by.
            order_type (google.analytics.data_v1alpha.types.OrderBy.DimensionOrderBy.OrderType):
                Controls the rule for dimension value
                ordering.
        """

        class OrderType(proto.Enum):
            r"""Rule to order the string dimension values by."""
            ORDER_TYPE_UNSPECIFIED = 0
            ALPHANUMERIC = 1
            CASE_INSENSITIVE_ALPHANUMERIC = 2
            NUMERIC = 3

        dimension_name = proto.Field(proto.STRING, number=1,)
        order_type = proto.Field(
            proto.ENUM, number=2, enum="OrderBy.DimensionOrderBy.OrderType",
        )

    class PivotOrderBy(proto.Message):
        r"""Sorts by a pivot column group.
        Attributes:
            metric_name (str):
                In the response to order by, order rows by
                this column. Must be a metric name from the
                request.
            pivot_selections (Sequence[google.analytics.data_v1alpha.types.OrderBy.PivotOrderBy.PivotSelection]):
                Used to select a dimension name and value
                pivot. If multiple pivot selections are given,
                the sort occurs on rows where all pivot
                selection dimension name and value pairs match
                the row's dimension name and value pair.
        """

        class PivotSelection(proto.Message):
            r"""A pair of dimension names and values. Rows with this dimension pivot
            pair are ordered by the metric's value.

            For example if pivots = {{"browser", "Chrome"}} and metric_name =
            "Sessions", then the rows will be sorted based on Sessions in
            Chrome.

            ::

                ---------|----------|----------------|----------|----------------
                         |  Chrome  |    Chrome      |  Safari  |     Safari
                ---------|----------|----------------|----------|----------------
                 Country | Sessions | Pages/Sessions | Sessions | Pages/Sessions
                ---------|----------|----------------|----------|----------------
                    US   |    2     |       2        |     3    |        1
                ---------|----------|----------------|----------|----------------
                  Canada |    3     |       1        |     4    |        1
                ---------|----------|----------------|----------|----------------

            Attributes:
                dimension_name (str):
                    Must be a dimension name from the request.
                dimension_value (str):
                    Order by only when the named dimension is
                    this value.
            """

            dimension_name = proto.Field(proto.STRING, number=1,)
            dimension_value = proto.Field(proto.STRING, number=2,)

        metric_name = proto.Field(proto.STRING, number=1,)
        pivot_selections = proto.RepeatedField(
            proto.MESSAGE, number=2, message="OrderBy.PivotOrderBy.PivotSelection",
        )

    metric = proto.Field(
        proto.MESSAGE, number=1, oneof="one_order_by", message=MetricOrderBy,
    )
    dimension = proto.Field(
        proto.MESSAGE, number=2, oneof="one_order_by", message=DimensionOrderBy,
    )
    pivot = proto.Field(
        proto.MESSAGE, number=3, oneof="one_order_by", message=PivotOrderBy,
    )
    desc = proto.Field(proto.BOOL, number=4,)


class Pivot(proto.Message):
    r"""Describes the visible dimension columns and rows in the
    report response.

    Attributes:
        field_names (Sequence[str]):
            Dimension names for visible columns in the
            report response. Including "dateRange" produces
            a date range column; for each row in the
            response, dimension values in the date range
            column will indicate the corresponding date
            range from the request.
        order_bys (Sequence[google.analytics.data_v1alpha.types.OrderBy]):
            Specifies how dimensions are ordered in the pivot. In the
            first Pivot, the OrderBys determine Row and
            PivotDimensionHeader ordering; in subsequent Pivots, the
            OrderBys determine only PivotDimensionHeader ordering.
            Dimensions specified in these OrderBys must be a subset of
            Pivot.field_names.
        offset (int):
            The row count of the start row. The first row
            is counted as row 0.
        limit (int):
            The number of rows to return in this pivot.
            If unspecified, 10 rows are returned. If -1, all
            rows are returned.
        metric_aggregations (Sequence[google.analytics.data_v1alpha.types.MetricAggregation]):
            Aggregate the metrics by dimensions in this pivot using the
            specified metric_aggregations.
    """

    field_names = proto.RepeatedField(proto.STRING, number=1,)
    order_bys = proto.RepeatedField(proto.MESSAGE, number=2, message="OrderBy",)
    offset = proto.Field(proto.INT64, number=3,)
    limit = proto.Field(proto.INT64, number=4,)
    metric_aggregations = proto.RepeatedField(
        proto.ENUM, number=5, enum="MetricAggregation",
    )


class CohortSpec(proto.Message):
    r"""Specification of cohorts for a cohort report. Cohort reports can be
    used for example to create a time series of user retention for the
    cohort. For example, you could select the cohort of users that were
    acquired in the first week of September and follow that cohort for
    the next six weeks. Selecting the users acquired in the first week
    of September cohort is specified in the ``cohort`` object. Following
    that cohort for the next six weeks is specified in the
    ``cohortsRange`` object.

    The report response could show a weekly time series where say your
    app has retained 60% of this cohort after three weeks and 25% of
    this cohort after six weeks. These two percentages can be calculated
    by the metric ``cohortActiveUsers/cohortTotalUsers`` and will be
    separate rows in the report.

    Attributes:
        cohorts (Sequence[google.analytics.data_v1alpha.types.Cohort]):
            Defines the selection criteria to group users
            into cohorts.
            Most cohort reports define only a single cohort.
            If multiple cohorts are specified, each cohort
            can be recognized in the report by their name.
        cohorts_range (google.analytics.data_v1alpha.types.CohortsRange):
            Cohort reports follow cohorts over an
            extended reporting date range. This range
            specifies an offset duration to follow the
            cohorts over.
        cohort_report_settings (google.analytics.data_v1alpha.types.CohortReportSettings):
            Optional settings for a cohort report.
    """

    cohorts = proto.RepeatedField(proto.MESSAGE, number=1, message="Cohort",)
    cohorts_range = proto.Field(proto.MESSAGE, number=2, message="CohortsRange",)
    cohort_report_settings = proto.Field(
        proto.MESSAGE, number=3, message="CohortReportSettings",
    )


class Cohort(proto.Message):
    r"""Defines a cohort selection criteria. A cohort is a group of users
    who share a common characteristic. For example, users with the same
    ``firstTouchDate`` belong to the same cohort.

    Attributes:
        name (str):
            Assigns a name to this cohort. The dimension ``cohort`` is
            valued to this name in a report response. If set, cannot
            begin with ``cohort_`` or ``RESERVED_``. If not set, cohorts
            are named by their zero based index ``cohort_0``,
            ``cohort_1``, etc.
        dimension (str):
            Dimension used by the cohort. Required and only supports
            ``firstTouchDate``.
        date_range (google.analytics.data_v1alpha.types.DateRange):
            The cohort selects users whose first touch date is between
            start date and end date defined in the ``dateRange``. This
            ``dateRange`` does not specify the full date range of event
            data that is present in a cohort report. In a cohort report,
            this ``dateRange`` is extended by the granularity and offset
            present in the ``cohortsRange``; event data for the extended
            reporting date range is present in a cohort report.

            In a cohort request, this ``dateRange`` is required and the
            ``dateRanges`` in the ``RunReportRequest`` or
            ``RunPivotReportRequest`` must be unspecified.

            This ``dateRange`` should generally be aligned with the
            cohort's granularity. If ``CohortsRange`` uses daily
            granularity, this ``dateRange`` can be a single day. If
            ``CohortsRange`` uses weekly granularity, this ``dateRange``
            can be aligned to a week boundary, starting at Sunday and
            ending Saturday. If ``CohortsRange`` uses monthly
            granularity, this ``dateRange`` can be aligned to a month,
            starting at the first and ending on the last day of the
            month.
    """

    name = proto.Field(proto.STRING, number=1,)
    dimension = proto.Field(proto.STRING, number=2,)
    date_range = proto.Field(proto.MESSAGE, number=3, message="DateRange",)


class CohortsRange(proto.Message):
    r"""Configures the extended reporting date range for a cohort
    report. Specifies an offset duration to follow the cohorts over.

    Attributes:
        granularity (google.analytics.data_v1alpha.types.CohortsRange.Granularity):
            The granularity used to interpret the ``startOffset`` and
            ``endOffset`` for the extended reporting date range for a
            cohort report.
        start_offset (int):
            ``startOffset`` specifies the start date of the extended
            reporting date range for a cohort report. ``startOffset`` is
            commonly set to 0 so that reports contain data from the
            acquisition of the cohort forward.

            If ``granularity`` is ``DAILY``, the ``startDate`` of the
            extended reporting date range is ``startDate`` of the cohort
            plus ``startOffset`` days.

            If ``granularity`` is ``WEEKLY``, the ``startDate`` of the
            extended reporting date range is ``startDate`` of the cohort
            plus ``startOffset * 7`` days.

            If ``granularity`` is ``MONTHLY``, the ``startDate`` of the
            extended reporting date range is ``startDate`` of the cohort
            plus ``startOffset * 30`` days.
        end_offset (int):
            ``endOffset`` specifies the end date of the extended
            reporting date range for a cohort report. ``endOffset`` can
            be any positive integer but is commonly set to 5 to 10 so
            that reports contain data on the cohort for the next several
            granularity time periods.

            If ``granularity`` is ``DAILY``, the ``endDate`` of the
            extended reporting date range is ``endDate`` of the cohort
            plus ``endOffset`` days.

            If ``granularity`` is ``WEEKLY``, the ``endDate`` of the
            extended reporting date range is ``endDate`` of the cohort
            plus ``endOffset * 7`` days.

            If ``granularity`` is ``MONTHLY``, the ``endDate`` of the
            extended reporting date range is ``endDate`` of the cohort
            plus ``endOffset * 30`` days.
    """

    class Granularity(proto.Enum):
        r"""The granularity used to interpret the ``startOffset`` and
        ``endOffset`` for the extended reporting date range for a cohort
        report.
        """
        GRANULARITY_UNSPECIFIED = 0
        DAILY = 1
        WEEKLY = 2
        MONTHLY = 3

    granularity = proto.Field(proto.ENUM, number=1, enum=Granularity,)
    start_offset = proto.Field(proto.INT32, number=2,)
    end_offset = proto.Field(proto.INT32, number=3,)


class CohortReportSettings(proto.Message):
    r"""Optional settings of a cohort report.
    Attributes:
        accumulate (bool):
            If true, accumulates the result from first touch day to the
            end day. Not supported in ``RunReportRequest``.
    """

    accumulate = proto.Field(proto.BOOL, number=1,)


class ResponseMetaData(proto.Message):
    r"""Response's metadata carrying additional information about the
    report content.

    Attributes:
        data_loss_from_other_row (bool):
            If true, indicates some buckets of dimension
            combinations are rolled into "(other)" row. This
            can happen for high cardinality reports.
    """

    data_loss_from_other_row = proto.Field(proto.BOOL, number=3,)


class DimensionHeader(proto.Message):
    r"""Describes a dimension column in the report. Dimensions
    requested in a report produce column entries within rows and
    DimensionHeaders. However, dimensions used exclusively within
    filters or expressions do not produce columns in a report;
    correspondingly, those dimensions do not produce headers.

    Attributes:
        name (str):
            The dimension's name.
    """

    name = proto.Field(proto.STRING, number=1,)


class MetricHeader(proto.Message):
    r"""Describes a metric column in the report. Visible metrics
    requested in a report produce column entries within rows and
    MetricHeaders. However, metrics used exclusively within filters
    or expressions do not produce columns in a report;
    correspondingly, those metrics do not produce headers.

    Attributes:
        name (str):
            The metric's name.
        type_ (google.analytics.data_v1alpha.types.MetricType):
            The metric's data type.
    """

    name = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.ENUM, number=2, enum="MetricType",)


class PivotHeader(proto.Message):
    r"""Dimensions' values in a single pivot.
    Attributes:
        pivot_dimension_headers (Sequence[google.analytics.data_v1alpha.types.PivotDimensionHeader]):
            The size is the same as the cardinality of
            the corresponding dimension combinations.
        row_count (int):
            The cardinality of the pivot as if offset = 0
            and limit = -1. The total number of rows for
            this pivot's fields regardless of how the
            parameters offset and limit are specified in the
            request.
    """

    pivot_dimension_headers = proto.RepeatedField(
        proto.MESSAGE, number=1, message="PivotDimensionHeader",
    )
    row_count = proto.Field(proto.INT32, number=2,)


class PivotDimensionHeader(proto.Message):
    r"""Summarizes dimension values from a row for this pivot.
    Attributes:
        dimension_values (Sequence[google.analytics.data_v1alpha.types.DimensionValue]):
            Values of multiple dimensions in a pivot.
    """

    dimension_values = proto.RepeatedField(
        proto.MESSAGE, number=1, message="DimensionValue",
    )


class Row(proto.Message):
    r"""Report data for each row. For example if RunReportRequest contains:

    .. code:: none

       "dimensions": [
         {
           "name": "eventName"
         },
         {
           "name": "countryId"
         }
       ],
       "metrics": [
         {
           "name": "eventCount"
         }
       ]

    One row with 'in_app_purchase' as the eventName, 'JP' as the
    countryId, and 15 as the eventCount, would be:

    .. code:: none

       "dimensionValues": [
         {
           "value": "in_app_purchase"
         },
         {
           "value": "JP"
         }
       ],
       "metricValues": [
         {
           "value": "15"
         }
       ]

    Attributes:
        dimension_values (Sequence[google.analytics.data_v1alpha.types.DimensionValue]):
            List of requested dimension values. In a PivotReport,
            dimension_values are only listed for dimensions included in
            a pivot.
        metric_values (Sequence[google.analytics.data_v1alpha.types.MetricValue]):
            List of requested visible metric values.
    """

    dimension_values = proto.RepeatedField(
        proto.MESSAGE, number=1, message="DimensionValue",
    )
    metric_values = proto.RepeatedField(proto.MESSAGE, number=2, message="MetricValue",)


class DimensionValue(proto.Message):
    r"""The value of a dimension.
    Attributes:
        value (str):
            Value as a string if the dimension type is a
            string.
    """

    value = proto.Field(proto.STRING, number=1, oneof="one_value",)


class MetricValue(proto.Message):
    r"""The value of a metric.
    Attributes:
        value (str):
            Measurement value. See MetricHeader for type.
    """

    value = proto.Field(proto.STRING, number=4, oneof="one_value",)


class NumericValue(proto.Message):
    r"""To represent a number.
    Attributes:
        int64_value (int):
            Integer value
        double_value (float):
            Double value
    """

    int64_value = proto.Field(proto.INT64, number=1, oneof="one_value",)
    double_value = proto.Field(proto.DOUBLE, number=2, oneof="one_value",)


class PropertyQuota(proto.Message):
    r"""Current state of all quotas for this Analytics Property. If
    any quota for a property is exhausted, all requests to that
    property will return Resource Exhausted errors.

    Attributes:
        tokens_per_day (google.analytics.data_v1alpha.types.QuotaStatus):
            Standard Analytics Properties can use up to
            25,000 tokens per day; Analytics 360 Properties
            can use 250,000 tokens per day. Most requests
            consume fewer than 10 tokens.
        tokens_per_hour (google.analytics.data_v1alpha.types.QuotaStatus):
            Standard Analytics Properties can use up to
            5,000 tokens per day; Analytics 360 Properties
            can use 50,000 tokens per day. An API request
            consumes a single number of tokens, and that
            number is deducted from both the hourly and
            daily quotas.
        concurrent_requests (google.analytics.data_v1alpha.types.QuotaStatus):
            Standard Analytics Properties can send up to
            10 concurrent requests; Analytics 360 Properties
            can use up to 50 concurrent requests.
        server_errors_per_project_per_hour (google.analytics.data_v1alpha.types.QuotaStatus):
            Standard Analytics Properties and cloud
            project pairs can have up to 10 server errors
            per hour; Analytics 360 Properties and cloud
            project pairs can have up to 50 server errors
            per hour.
    """

    tokens_per_day = proto.Field(proto.MESSAGE, number=1, message="QuotaStatus",)
    tokens_per_hour = proto.Field(proto.MESSAGE, number=2, message="QuotaStatus",)
    concurrent_requests = proto.Field(proto.MESSAGE, number=3, message="QuotaStatus",)
    server_errors_per_project_per_hour = proto.Field(
        proto.MESSAGE, number=4, message="QuotaStatus",
    )


class QuotaStatus(proto.Message):
    r"""Current state for a particular quota group.
    Attributes:
        consumed (int):
            Quota consumed by this request.
        remaining (int):
            Quota remaining after this request.
    """

    consumed = proto.Field(proto.INT32, number=1,)
    remaining = proto.Field(proto.INT32, number=2,)


class DimensionMetadata(proto.Message):
    r"""Explains a dimension.
    Attributes:
        api_name (str):
            This dimension's name. Useable in
            `Dimension <#Dimension>`__'s ``name``. For example,
            ``eventName``.
        ui_name (str):
            This dimension's name within the Google Analytics user
            interface. For example, ``Event name``.
        description (str):
            Description of how this dimension is used and
            calculated.
        deprecated_api_names (Sequence[str]):
            Still usable but deprecated names for this dimension. If
            populated, this dimension is available by either ``apiName``
            or one of ``deprecatedApiNames`` for a period of time. After
            the deprecation period, the dimension will be available only
            by ``apiName``.
        custom_definition (bool):
            True if the dimension is a custom dimension
            for this property.
    """

    api_name = proto.Field(proto.STRING, number=1,)
    ui_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    deprecated_api_names = proto.RepeatedField(proto.STRING, number=4,)
    custom_definition = proto.Field(proto.BOOL, number=5,)


class MetricMetadata(proto.Message):
    r"""Explains a metric.
    Attributes:
        api_name (str):
            A metric name. Useable in `Metric <#Metric>`__'s ``name``.
            For example, ``eventCount``.
        ui_name (str):
            This metric's name within the Google Analytics user
            interface. For example, ``Event count``.
        description (str):
            Description of how this metric is used and
            calculated.
        deprecated_api_names (Sequence[str]):
            Still usable but deprecated names for this metric. If
            populated, this metric is available by either ``apiName`` or
            one of ``deprecatedApiNames`` for a period of time. After
            the deprecation period, the metric will be available only by
            ``apiName``.
        type_ (google.analytics.data_v1alpha.types.MetricType):
            The type of this metric.
        expression (str):
            The mathematical expression for this derived metric. Can be
            used in `Metric <#Metric>`__'s ``expression`` field for
            equivalent reports. Most metrics are not expressions, and
            for non-expressions, this field is empty.
        custom_definition (bool):
            True if the metric is a custom metric for
            this property.
    """

    api_name = proto.Field(proto.STRING, number=1,)
    ui_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    deprecated_api_names = proto.RepeatedField(proto.STRING, number=4,)
    type_ = proto.Field(proto.ENUM, number=5, enum="MetricType",)
    expression = proto.Field(proto.STRING, number=6,)
    custom_definition = proto.Field(proto.BOOL, number=7,)


__all__ = tuple(sorted(__protobuf__.manifest))
