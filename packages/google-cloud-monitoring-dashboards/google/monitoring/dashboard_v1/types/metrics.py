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

from google.monitoring.dashboard_v1.types import common

__protobuf__ = proto.module(
    package="google.monitoring.dashboard.v1",
    manifest={
        "SparkChartType",
        "TimeSeriesQuery",
        "TimeSeriesFilter",
        "TimeSeriesFilterRatio",
        "Threshold",
    },
)


class SparkChartType(proto.Enum):
    r"""Defines the possible types of spark chart supported by the
    ``Scorecard``.
    """
    SPARK_CHART_TYPE_UNSPECIFIED = 0
    SPARK_LINE = 1
    SPARK_BAR = 2


class TimeSeriesQuery(proto.Message):
    r"""TimeSeriesQuery collects the set of supported methods for
    querying time series data from the Stackdriver metrics API.

    Attributes:
        time_series_filter (~.metrics.TimeSeriesFilter):
            Filter parameters to fetch time series.
        time_series_filter_ratio (~.metrics.TimeSeriesFilterRatio):
            Parameters to fetch a ratio between two time
            series filters.
        time_series_query_language (str):
            A query used to fetch time series.
        unit_override (str):
            The unit of data contained in fetched time series. If
            non-empty, this unit will override any unit that accompanies
            fetched data. The format is the same as the
            ```unit`` <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.metricDescriptors>`__
            field in ``MetricDescriptor``.
    """

    time_series_filter = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="source",
        message="TimeSeriesFilter",
    )

    time_series_filter_ratio = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source",
        message="TimeSeriesFilterRatio",
    )

    time_series_query_language = proto.Field(proto.STRING, number=3, oneof="source")

    unit_override = proto.Field(proto.STRING, number=5)


class TimeSeriesFilter(proto.Message):
    r"""A filter that defines a subset of time series data that is displayed
    in a widget. Time series data is fetched using the
    ```ListTimeSeries`` <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list>`__
    method.

    Attributes:
        filter (str):
            Required. The `monitoring
            filter <https://cloud.google.com/monitoring/api/v3/filters>`__
            that identifies the metric types, resources, and projects to
            query.
        aggregation (~.common.Aggregation):
            By default, the raw time series data is
            returned. Use this field to combine multiple
            time series for different views of the data.
        secondary_aggregation (~.common.Aggregation):
            Apply a second aggregation after ``aggregation`` is applied.
        pick_time_series_filter (~.common.PickTimeSeriesFilter):
            Ranking based time series filter.
        statistical_time_series_filter (~.common.StatisticalTimeSeriesFilter):
            Statistics based time series filter.
            Note: This field is deprecated and completely
            ignored by the API.
    """

    filter = proto.Field(proto.STRING, number=1)

    aggregation = proto.Field(
        proto.MESSAGE,
        number=2,
        message=common.Aggregation,
    )

    secondary_aggregation = proto.Field(
        proto.MESSAGE,
        number=3,
        message=common.Aggregation,
    )

    pick_time_series_filter = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="output_filter",
        message=common.PickTimeSeriesFilter,
    )

    statistical_time_series_filter = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="output_filter",
        message=common.StatisticalTimeSeriesFilter,
    )


class TimeSeriesFilterRatio(proto.Message):
    r"""A pair of time series filters that define a ratio
    computation. The output time series is the pair-wise division of
    each aligned element from the numerator and denominator time
    series.

    Attributes:
        numerator (~.metrics.TimeSeriesFilterRatio.RatioPart):
            The numerator of the ratio.
        denominator (~.metrics.TimeSeriesFilterRatio.RatioPart):
            The denominator of the ratio.
        secondary_aggregation (~.common.Aggregation):
            Apply a second aggregation after the ratio is
            computed.
        pick_time_series_filter (~.common.PickTimeSeriesFilter):
            Ranking based time series filter.
        statistical_time_series_filter (~.common.StatisticalTimeSeriesFilter):
            Statistics based time series filter.
            Note: This field is deprecated and completely
            ignored by the API.
    """

    class RatioPart(proto.Message):
        r"""Describes a query to build the numerator or denominator of a
        TimeSeriesFilterRatio.

        Attributes:
            filter (str):
                Required. The `monitoring
                filter <https://cloud.google.com/monitoring/api/v3/filters>`__
                that identifies the metric types, resources, and projects to
                query.
            aggregation (~.common.Aggregation):
                By default, the raw time series data is
                returned. Use this field to combine multiple
                time series for different views of the data.
        """

        filter = proto.Field(proto.STRING, number=1)

        aggregation = proto.Field(
            proto.MESSAGE,
            number=2,
            message=common.Aggregation,
        )

    numerator = proto.Field(
        proto.MESSAGE,
        number=1,
        message=RatioPart,
    )

    denominator = proto.Field(
        proto.MESSAGE,
        number=2,
        message=RatioPart,
    )

    secondary_aggregation = proto.Field(
        proto.MESSAGE,
        number=3,
        message=common.Aggregation,
    )

    pick_time_series_filter = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="output_filter",
        message=common.PickTimeSeriesFilter,
    )

    statistical_time_series_filter = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="output_filter",
        message=common.StatisticalTimeSeriesFilter,
    )


class Threshold(proto.Message):
    r"""Defines a threshold for categorizing time series values.

    Attributes:
        label (str):
            A label for the threshold.
        value (float):
            The value of the threshold. The value should
            be defined in the native scale of the metric.
        color (~.metrics.Threshold.Color):
            The state color for this threshold. Color is
            not allowed in a XyChart.
        direction (~.metrics.Threshold.Direction):
            The direction for the current threshold.
            Direction is not allowed in a XyChart.
    """

    class Color(proto.Enum):
        r"""The color suggests an interpretation to the viewer when
        actual values cross the threshold. Comments on each color
        provide UX guidance on how users can be expected to interpret a
        given state color.
        """
        COLOR_UNSPECIFIED = 0
        YELLOW = 4
        RED = 6

    class Direction(proto.Enum):
        r"""Whether the threshold is considered crossed by an actual
        value above or below its threshold value.
        """
        DIRECTION_UNSPECIFIED = 0
        ABOVE = 1
        BELOW = 2

    label = proto.Field(proto.STRING, number=1)

    value = proto.Field(proto.DOUBLE, number=2)

    color = proto.Field(
        proto.ENUM,
        number=3,
        enum=Color,
    )

    direction = proto.Field(
        proto.ENUM,
        number=4,
        enum=Direction,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
