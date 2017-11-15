# Copyright 2017, Google LLC All rights reserved.
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
"""Wrappers for protocol buffer enum types."""


class LabelDescriptor(object):
    class ValueType(object):
        """
        Value types that can be used as label values.

        Attributes:
          STRING (int): A variable-length string. This is the default.
          BOOL (int): Boolean; true or false.
          INT64 (int): A 64-bit signed integer.
        """
        STRING = 0
        BOOL = 1
        INT64 = 2


class Aggregation(object):
    class Aligner(object):
        """
        The Aligner describes how to bring the data points in a single
        time series into temporal alignment.

        Attributes:
          ALIGN_NONE (int): No alignment. Raw data is returned. Not valid if cross-time
          series reduction is requested. The value type of the result is
          the same as the value type of the input.
          ALIGN_DELTA (int): Align and convert to delta metric type. This alignment is valid
          for cumulative metrics and delta metrics. Aligning an existing
          delta metric to a delta metric requires that the alignment
          period be increased. The value type of the result is the same
          as the value type of the input.
          ALIGN_RATE (int): Align and convert to a rate. This alignment is valid for
          cumulative metrics and delta metrics with numeric values. The output is a
          gauge metric with value type
          ``DOUBLE``.
          ALIGN_INTERPOLATE (int): Align by interpolating between adjacent points around the
          period boundary. This alignment is valid for gauge
          metrics with numeric values. The value type of the result is the same
          as the value type of the input.
          ALIGN_NEXT_OLDER (int): Align by shifting the oldest data point before the period
          boundary to the boundary. This alignment is valid for gauge
          metrics. The value type of the result is the same as the
          value type of the input.
          ALIGN_MIN (int): Align time series via aggregation. The resulting data point in
          the alignment period is the minimum of all data points in the
          period. This alignment is valid for gauge and delta metrics with numeric
          values. The value type of the result is the same as the value
          type of the input.
          ALIGN_MAX (int): Align time series via aggregation. The resulting data point in
          the alignment period is the maximum of all data points in the
          period. This alignment is valid for gauge and delta metrics with numeric
          values. The value type of the result is the same as the value
          type of the input.
          ALIGN_MEAN (int): Align time series via aggregation. The resulting data point in
          the alignment period is the average or arithmetic mean of all
          data points in the period. This alignment is valid for gauge and delta
          metrics with numeric values. The value type of the output is
          ``DOUBLE``.
          ALIGN_COUNT (int): Align time series via aggregation. The resulting data point in
          the alignment period is the count of all data points in the
          period. This alignment is valid for gauge and delta metrics with numeric
          or Boolean values. The value type of the output is
          ``INT64``.
          ALIGN_SUM (int): Align time series via aggregation. The resulting data point in
          the alignment period is the sum of all data points in the
          period. This alignment is valid for gauge and delta metrics with numeric
          and distribution values. The value type of the output is the
          same as the value type of the input.
          ALIGN_STDDEV (int): Align time series via aggregation. The resulting data point in
          the alignment period is the standard deviation of all data
          points in the period. This alignment is valid for gauge and delta metrics
          with numeric values. The value type of the output is
          ``DOUBLE``.
          ALIGN_COUNT_TRUE (int): Align time series via aggregation. The resulting data point in
          the alignment period is the count of True-valued data points in the
          period. This alignment is valid for gauge metrics with
          Boolean values. The value type of the output is
          ``INT64``.
          ALIGN_FRACTION_TRUE (int): Align time series via aggregation. The resulting data point in
          the alignment period is the fraction of True-valued data points in the
          period. This alignment is valid for gauge metrics with Boolean values.
          The output value is in the range [0, 1] and has value type
          ``DOUBLE``.
          ALIGN_PERCENTILE_99 (int): Align time series via aggregation. The resulting data point in
          the alignment period is the 99th percentile of all data
          points in the period. This alignment is valid for gauge and delta metrics
          with distribution values. The output is a gauge metric with value type
          ``DOUBLE``.
          ALIGN_PERCENTILE_95 (int): Align time series via aggregation. The resulting data point in
          the alignment period is the 95th percentile of all data
          points in the period. This alignment is valid for gauge and delta metrics
          with distribution values. The output is a gauge metric with value type
          ``DOUBLE``.
          ALIGN_PERCENTILE_50 (int): Align time series via aggregation. The resulting data point in
          the alignment period is the 50th percentile of all data
          points in the period. This alignment is valid for gauge and delta metrics
          with distribution values. The output is a gauge metric with value type
          ``DOUBLE``.
          ALIGN_PERCENTILE_05 (int): Align time series via aggregation. The resulting data point in
          the alignment period is the 5th percentile of all data
          points in the period. This alignment is valid for gauge and delta metrics
          with distribution values. The output is a gauge metric with value type
          ``DOUBLE``.
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
        ALIGN_FRACTION_TRUE = 17
        ALIGN_PERCENTILE_99 = 18
        ALIGN_PERCENTILE_95 = 19
        ALIGN_PERCENTILE_50 = 20
        ALIGN_PERCENTILE_05 = 21

    class Reducer(object):
        """
        A Reducer describes how to aggregate data points from multiple
        time series into a single time series.

        Attributes:
          REDUCE_NONE (int): No cross-time series reduction. The output of the aligner is
          returned.
          REDUCE_MEAN (int): Reduce by computing the mean across time series for each
          alignment period. This reducer is valid for delta and
          gauge metrics with numeric or distribution values. The value type of the
          output is ``DOUBLE``.
          REDUCE_MIN (int): Reduce by computing the minimum across time series for each
          alignment period. This reducer is valid for delta and
          gauge metrics with numeric values. The value type of the output
          is the same as the value type of the input.
          REDUCE_MAX (int): Reduce by computing the maximum across time series for each
          alignment period. This reducer is valid for delta and
          gauge metrics with numeric values. The value type of the output
          is the same as the value type of the input.
          REDUCE_SUM (int): Reduce by computing the sum across time series for each
          alignment period. This reducer is valid for delta and
          gauge metrics with numeric and distribution values. The value type of
          the output is the same as the value type of the input.
          REDUCE_STDDEV (int): Reduce by computing the standard deviation across time series
          for each alignment period. This reducer is valid for delta
          and gauge metrics with numeric or distribution values. The value type of
          the output is ``DOUBLE``.
          REDUCE_COUNT (int): Reduce by computing the count of data points across time series
          for each alignment period. This reducer is valid for delta
          and gauge metrics of numeric, Boolean, distribution, and string value
          type. The value type of the output is
          ``INT64``.
          REDUCE_COUNT_TRUE (int): Reduce by computing the count of True-valued data points across time
          series for each alignment period. This reducer is valid for delta
          and gauge metrics of Boolean value type. The value type of
          the output is ``INT64``.
          REDUCE_FRACTION_TRUE (int): Reduce by computing the fraction of True-valued data points across time
          series for each alignment period. This reducer is valid for delta
          and gauge metrics of Boolean value type. The output value is in the
          range [0, 1] and has value type
          ``DOUBLE``.
          REDUCE_PERCENTILE_99 (int): Reduce by computing 99th percentile of data points across time series
          for each alignment period. This reducer is valid for gauge and delta
          metrics of numeric and distribution type. The value of the output is
          ``DOUBLE``
          REDUCE_PERCENTILE_95 (int): Reduce by computing 95th percentile of data points across time series
          for each alignment period. This reducer is valid for gauge and delta
          metrics of numeric and distribution type. The value of the output is
          ``DOUBLE``
          REDUCE_PERCENTILE_50 (int): Reduce by computing 50th percentile of data points across time series
          for each alignment period. This reducer is valid for gauge and delta
          metrics of numeric and distribution type. The value of the output is
          ``DOUBLE``
          REDUCE_PERCENTILE_05 (int): Reduce by computing 5th percentile of data points across time series
          for each alignment period. This reducer is valid for gauge and delta
          metrics of numeric and distribution type. The value of the output is
          ``DOUBLE``
        """
        REDUCE_NONE = 0
        REDUCE_MEAN = 1
        REDUCE_MIN = 2
        REDUCE_MAX = 3
        REDUCE_SUM = 4
        REDUCE_STDDEV = 5
        REDUCE_COUNT = 6
        REDUCE_COUNT_TRUE = 7
        REDUCE_FRACTION_TRUE = 8
        REDUCE_PERCENTILE_99 = 9
        REDUCE_PERCENTILE_95 = 10
        REDUCE_PERCENTILE_50 = 11
        REDUCE_PERCENTILE_05 = 12


class MetricDescriptor(object):
    class MetricKind(object):
        """
        The kind of measurement. It describes how the data is reported.

        Attributes:
          METRIC_KIND_UNSPECIFIED (int): Do not use this default value.
          GAUGE (int): An instantaneous measurement of a value.
          DELTA (int): The change in a value during a time interval.
          CUMULATIVE (int): A value accumulated over a time interval.  Cumulative
          measurements in a time series should have the same start time
          and increasing end times, until an event resets the cumulative
          value to zero and sets a new start time for the following
          points.
        """
        METRIC_KIND_UNSPECIFIED = 0
        GAUGE = 1
        DELTA = 2
        CUMULATIVE = 3

    class ValueType(object):
        """
        The value type of a metric.

        Attributes:
          VALUE_TYPE_UNSPECIFIED (int): Do not use this default value.
          BOOL (int): The value is a boolean.
          This value type can be used only if the metric kind is ``GAUGE``.
          INT64 (int): The value is a signed 64-bit integer.
          DOUBLE (int): The value is a double precision floating point number.
          STRING (int): The value is a text string.
          This value type can be used only if the metric kind is ``GAUGE``.
          DISTRIBUTION (int): The value is a ````Distribution````.
          MONEY (int): The value is money.
        """
        VALUE_TYPE_UNSPECIFIED = 0
        BOOL = 1
        INT64 = 2
        DOUBLE = 3
        STRING = 4
        DISTRIBUTION = 5
        MONEY = 6


class ListTimeSeriesRequest(object):
    class TimeSeriesView(object):
        """
        Controls which fields are returned by ``ListTimeSeries``.

        Attributes:
          FULL (int): Returns the identity of the metric(s), the time series,
          and the time series data.
          HEADERS (int): Returns the identity of the metric and the time series resource,
          but not the time series data.
        """
        FULL = 0
        HEADERS = 1
