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

from google.protobuf import duration_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.monitoring.dashboard.v1",
    manifest={"Aggregation", "PickTimeSeriesFilter", "StatisticalTimeSeriesFilter",},
)


class Aggregation(proto.Message):
    r"""Describes how to combine multiple time series to provide a different
    view of the data. Aggregation of time series is done in two steps.
    First, each time series in the set is *aligned* to the same time
    interval boundaries, then the set of time series is optionally
    *reduced* in number.

    Alignment consists of applying the ``per_series_aligner`` operation
    to each time series after its data has been divided into regular
    ``alignment_period`` time intervals. This process takes *all* of the
    data points in an alignment period, applies a mathematical
    transformation such as averaging, minimum, maximum, delta, etc., and
    converts them into a single data point per period.

    Reduction is when the aligned and transformed time series can
    optionally be combined, reducing the number of time series through
    similar mathematical transformations. Reduction involves applying a
    ``cross_series_reducer`` to all the time series, optionally sorting
    the time series into subsets with ``group_by_fields``, and applying
    the reducer to each subset.

    The raw time series data can contain a huge amount of information
    from multiple sources. Alignment and reduction transforms this mass
    of data into a more manageable and representative collection of
    data, for example "the 95% latency across the average of all tasks
    in a cluster". This representative data can be more easily graphed
    and comprehended, and the individual time series data is still
    available for later drilldown. For more details, see `Filtering and
    aggregation <https://cloud.google.com/monitoring/api/v3/aggregation>`__.

    Attributes:
        alignment_period (google.protobuf.duration_pb2.Duration):
            The ``alignment_period`` specifies a time interval, in
            seconds, that is used to divide the data in all the [time
            series][google.monitoring.v3.TimeSeries] into consistent
            blocks of time. This will be done before the per-series
            aligner can be applied to the data.

            The value must be at least 60 seconds. If a per-series
            aligner other than ``ALIGN_NONE`` is specified, this field
            is required or an error is returned. If no per-series
            aligner is specified, or the aligner ``ALIGN_NONE`` is
            specified, then this field is ignored.

            The maximum value of the ``alignment_period`` is 2 years, or
            104 weeks.
        per_series_aligner (google.cloud.monitoring_dashboard_v1.types.Aggregation.Aligner):
            An ``Aligner`` describes how to bring the data points in a
            single time series into temporal alignment. Except for
            ``ALIGN_NONE``, all alignments cause all the data points in
            an ``alignment_period`` to be mathematically grouped
            together, resulting in a single data point for each
            ``alignment_period`` with end timestamp at the end of the
            period.

            Not all alignment operations may be applied to all time
            series. The valid choices depend on the ``metric_kind`` and
            ``value_type`` of the original time series. Alignment can
            change the ``metric_kind`` or the ``value_type`` of the time
            series.

            Time series data must be aligned in order to perform
            cross-time series reduction. If ``cross_series_reducer`` is
            specified, then ``per_series_aligner`` must be specified and
            not equal to ``ALIGN_NONE`` and ``alignment_period`` must be
            specified; otherwise, an error is returned.
        cross_series_reducer (google.cloud.monitoring_dashboard_v1.types.Aggregation.Reducer):
            The reduction operation to be used to combine time series
            into a single time series, where the value of each data
            point in the resulting series is a function of all the
            already aligned values in the input time series.

            Not all reducer operations can be applied to all time
            series. The valid choices depend on the ``metric_kind`` and
            the ``value_type`` of the original time series. Reduction
            can yield a time series with a different ``metric_kind`` or
            ``value_type`` than the input time series.

            Time series data must first be aligned (see
            ``per_series_aligner``) in order to perform cross-time
            series reduction. If ``cross_series_reducer`` is specified,
            then ``per_series_aligner`` must be specified, and must not
            be ``ALIGN_NONE``. An ``alignment_period`` must also be
            specified; otherwise, an error is returned.
        group_by_fields (Sequence[str]):
            The set of fields to preserve when ``cross_series_reducer``
            is specified. The ``group_by_fields`` determine how the time
            series are partitioned into subsets prior to applying the
            aggregation operation. Each subset contains time series that
            have the same value for each of the grouping fields. Each
            individual time series is a member of exactly one subset.
            The ``cross_series_reducer`` is applied to each subset of
            time series. It is not possible to reduce across different
            resource types, so this field implicitly contains
            ``resource.type``. Fields not specified in
            ``group_by_fields`` are aggregated away. If
            ``group_by_fields`` is not specified and all the time series
            have the same resource type, then the time series are
            aggregated into a single output time series. If
            ``cross_series_reducer`` is not defined, this field is
            ignored.
    """

    class Aligner(proto.Enum):
        r"""The ``Aligner`` specifies the operation that will be applied to the
        data points in each alignment period in a time series. Except for
        ``ALIGN_NONE``, which specifies that no operation be applied, each
        alignment operation replaces the set of data values in each
        alignment period with a single value: the result of applying the
        operation to the data values. An aligned time series has a single
        data value at the end of each ``alignment_period``.

        An alignment operation can change the data type of the values, too.
        For example, if you apply a counting operation to boolean values,
        the data ``value_type`` in the original time series is ``BOOLEAN``,
        but the ``value_type`` in the aligned result is ``INT64``.
        """
        ALIGN_NONE = 0
        ALIGN_DELTA = 1
        ALIGN_RATE = 2
        ALIGN_INTERPOLATE = 3
        ALIGN_NEXT_OLDER = 4
        ALIGN_MIN = 10
        ALIGN_MAX = 11
        ALIGN_MEAN = 12
        ALIGN_COUNT = 13
        ALIGN_SUM = 14
        ALIGN_STDDEV = 15
        ALIGN_COUNT_TRUE = 16
        ALIGN_COUNT_FALSE = 24
        ALIGN_FRACTION_TRUE = 17
        ALIGN_PERCENTILE_99 = 18
        ALIGN_PERCENTILE_95 = 19
        ALIGN_PERCENTILE_50 = 20
        ALIGN_PERCENTILE_05 = 21
        ALIGN_PERCENT_CHANGE = 23

    class Reducer(proto.Enum):
        r"""A Reducer operation describes how to aggregate data points
        from multiple time series into a single time series, where the
        value of each data point in the resulting series is a function
        of all the already aligned values in the input time series.
        """
        REDUCE_NONE = 0
        REDUCE_MEAN = 1
        REDUCE_MIN = 2
        REDUCE_MAX = 3
        REDUCE_SUM = 4
        REDUCE_STDDEV = 5
        REDUCE_COUNT = 6
        REDUCE_COUNT_TRUE = 7
        REDUCE_COUNT_FALSE = 15
        REDUCE_FRACTION_TRUE = 8
        REDUCE_PERCENTILE_99 = 9
        REDUCE_PERCENTILE_95 = 10
        REDUCE_PERCENTILE_50 = 11
        REDUCE_PERCENTILE_05 = 12

    alignment_period = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )
    per_series_aligner = proto.Field(proto.ENUM, number=2, enum=Aligner,)
    cross_series_reducer = proto.Field(proto.ENUM, number=4, enum=Reducer,)
    group_by_fields = proto.RepeatedField(proto.STRING, number=5,)


class PickTimeSeriesFilter(proto.Message):
    r"""Describes a ranking-based time series filter. Each input time series
    is ranked with an aligner. The filter will allow up to
    ``num_time_series`` time series to pass through it, selecting them
    based on the relative ranking.

    For example, if ``ranking_method`` is
    ``METHOD_MEAN``,\ ``direction`` is ``BOTTOM``, and
    ``num_time_series`` is 3, then the 3 times series with the lowest
    mean values will pass through the filter.

    Attributes:
        ranking_method (google.cloud.monitoring_dashboard_v1.types.PickTimeSeriesFilter.Method):
            ``ranking_method`` is applied to each time series
            independently to produce the value which will be used to
            compare the time series to other time series.
        num_time_series (int):
            How many time series to allow to pass through
            the filter.
        direction (google.cloud.monitoring_dashboard_v1.types.PickTimeSeriesFilter.Direction):
            How to use the ranking to select time series
            that pass through the filter.
    """

    class Method(proto.Enum):
        r"""The value reducers that can be applied to a
        ``PickTimeSeriesFilter``.
        """
        METHOD_UNSPECIFIED = 0
        METHOD_MEAN = 1
        METHOD_MAX = 2
        METHOD_MIN = 3
        METHOD_SUM = 4
        METHOD_LATEST = 5

    class Direction(proto.Enum):
        r"""Describes the ranking directions."""
        DIRECTION_UNSPECIFIED = 0
        TOP = 1
        BOTTOM = 2

    ranking_method = proto.Field(proto.ENUM, number=1, enum=Method,)
    num_time_series = proto.Field(proto.INT32, number=2,)
    direction = proto.Field(proto.ENUM, number=3, enum=Direction,)


class StatisticalTimeSeriesFilter(proto.Message):
    r"""A filter that ranks streams based on their statistical
    relation to other streams in a request.
    Note: This field is deprecated and completely ignored by the
    API.

    Attributes:
        ranking_method (google.cloud.monitoring_dashboard_v1.types.StatisticalTimeSeriesFilter.Method):
            ``rankingMethod`` is applied to a set of time series, and
            then the produced value for each individual time series is
            used to compare a given time series to others. These are
            methods that cannot be applied stream-by-stream, but rather
            require the full context of a request to evaluate time
            series.
        num_time_series (int):
            How many time series to output.
    """

    class Method(proto.Enum):
        r"""The filter methods that can be applied to a stream."""
        METHOD_UNSPECIFIED = 0
        METHOD_CLUSTER_OUTLIER = 1

    ranking_method = proto.Field(proto.ENUM, number=1, enum=Method,)
    num_time_series = proto.Field(proto.INT32, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
