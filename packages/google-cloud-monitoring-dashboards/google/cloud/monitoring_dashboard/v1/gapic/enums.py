# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class SparkChartType(enum.IntEnum):
    """
    Defines the possible types of spark chart supported by the
    ``Scorecard``.

    Attributes:
      SPARK_CHART_TYPE_UNSPECIFIED (int): Not allowed in well-formed requests.
      SPARK_LINE (int): The sparkline will be rendered as a small line chart.
      SPARK_BAR (int): The sparkbar will be rendered as a small bar chart.
    """

    SPARK_CHART_TYPE_UNSPECIFIED = 0
    SPARK_LINE = 1
    SPARK_BAR = 2


class Aggregation(object):
    class Aligner(enum.IntEnum):
        """
        The Aligner describes how to bring the data points in a single
        time series into temporal alignment.

        Attributes:
          ALIGN_NONE (int): No alignment. Raw data is returned. Not valid if cross-time
          series reduction is requested. The value type of the result is
          the same as the value type of the input.
          ALIGN_DELTA (int): Align and convert to delta metric type. This alignment is valid for
          cumulative metrics and delta metrics. Aligning an existing delta metric
          to a delta metric requires that the alignment period be increased. The
          value type of the result is the same as the value type of the input.

          One can think of this aligner as a rate but without time units; that is,
          the output is conceptually (second_point - first_point).
          ALIGN_RATE (int): Align and convert to a rate. This alignment is valid for cumulative
          metrics and delta metrics with numeric values. The output is a gauge
          metric with value type ``DOUBLE``.

          One can think of this aligner as conceptually providing the slope of the
          line that passes through the value at the start and end of the window.
          In other words, this is conceptually ((y1 - y0)/(t1 - t0)), and the
          output unit is one that has a "/time" dimension.

          If, by rate, you are looking for percentage change, see the
          ``ALIGN_PERCENT_CHANGE`` aligner option.
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
          ALIGN_MEAN (int): Align time series via aggregation. The resulting data point in the
          alignment period is the average or arithmetic mean of all data points in
          the period. This alignment is valid for gauge and delta metrics with
          numeric values. The value type of the output is ``DOUBLE``.
          ALIGN_COUNT (int): Align time series via aggregation. The resulting data point in the
          alignment period is the count of all data points in the period. This
          alignment is valid for gauge and delta metrics with numeric or Boolean
          values. The value type of the output is ``INT64``.
          ALIGN_SUM (int): Align time series via aggregation. The resulting data point in
          the alignment period is the sum of all data points in the
          period. This alignment is valid for gauge and delta metrics with numeric
          and distribution values. The value type of the output is the
          same as the value type of the input.
          ALIGN_STDDEV (int): Align time series via aggregation. The resulting data point in the
          alignment period is the standard deviation of all data points in the
          period. This alignment is valid for gauge and delta metrics with numeric
          values. The value type of the output is ``DOUBLE``.
          ALIGN_COUNT_TRUE (int): Align time series via aggregation. The resulting data point in the
          alignment period is the count of True-valued data points in the period.
          This alignment is valid for gauge metrics with Boolean values. The value
          type of the output is ``INT64``.
          ALIGN_COUNT_FALSE (int): Align time series via aggregation. The resulting data point in the
          alignment period is the count of False-valued data points in the period.
          This alignment is valid for gauge metrics with Boolean values. The value
          type of the output is ``INT64``.
          ALIGN_FRACTION_TRUE (int): Align time series via aggregation. The resulting data point in the
          alignment period is the fraction of True-valued data points in the
          period. This alignment is valid for gauge metrics with Boolean values.
          The output value is in the range [0, 1] and has value type ``DOUBLE``.
          ALIGN_PERCENTILE_99 (int): Align time series via aggregation. The resulting data point in the
          alignment period is the 99th percentile of all data points in the
          period. This alignment is valid for gauge and delta metrics with
          distribution values. The output is a gauge metric with value type
          ``DOUBLE``.
          ALIGN_PERCENTILE_95 (int): Align time series via aggregation. The resulting data point in the
          alignment period is the 95th percentile of all data points in the
          period. This alignment is valid for gauge and delta metrics with
          distribution values. The output is a gauge metric with value type
          ``DOUBLE``.
          ALIGN_PERCENTILE_50 (int): Align time series via aggregation. The resulting data point in the
          alignment period is the 50th percentile of all data points in the
          period. This alignment is valid for gauge and delta metrics with
          distribution values. The output is a gauge metric with value type
          ``DOUBLE``.
          ALIGN_PERCENTILE_05 (int): Align time series via aggregation. The resulting data point in the
          alignment period is the 5th percentile of all data points in the period.
          This alignment is valid for gauge and delta metrics with distribution
          values. The output is a gauge metric with value type ``DOUBLE``.
          ALIGN_PERCENT_CHANGE (int): Align and convert to a percentage change. This alignment is valid
          for gauge and delta metrics with numeric values. This alignment
          conceptually computes the equivalent of "((current -
          previous)/previous)*100" where previous value is determined based on the
          alignmentPeriod. In the event that previous is 0 the calculated value is
          infinity with the exception that if both (current - previous) and
          previous are 0 the calculated value is 0. A 10 minute moving mean is
          computed at each point of the time window prior to the above calculation
          to smooth the metric and prevent false positives from very short lived
          spikes. Only applicable for data that is >= 0. Any values < 0 are
          treated as no data. While delta metrics are accepted by this alignment
          special care should be taken that the values for the metric will always
          be positive. The output is a gauge metric with value type ``DOUBLE``.
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

    class Reducer(enum.IntEnum):
        """
        A Reducer describes how to aggregate data points from multiple
        time series into a single time series.

        Attributes:
          REDUCE_NONE (int): No cross-time series reduction. The output of the aligner is
          returned.
          REDUCE_MEAN (int): Reduce by computing the mean across time series for each alignment
          period. This reducer is valid for delta and gauge metrics with numeric
          or distribution values. The value type of the output is ``DOUBLE``.
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
          REDUCE_STDDEV (int): Reduce by computing the standard deviation across time series for
          each alignment period. This reducer is valid for delta and gauge metrics
          with numeric or distribution values. The value type of the output is
          ``DOUBLE``.
          REDUCE_COUNT (int): Reduce by computing the count of data points across time series for
          each alignment period. This reducer is valid for delta and gauge metrics
          of numeric, Boolean, distribution, and string value type. The value type
          of the output is ``INT64``.
          REDUCE_COUNT_TRUE (int): Reduce by computing the count of True-valued data points across time
          series for each alignment period. This reducer is valid for delta and
          gauge metrics of Boolean value type. The value type of the output is
          ``INT64``.
          REDUCE_COUNT_FALSE (int): Reduce by computing the count of False-valued data points across
          time series for each alignment period. This reducer is valid for delta
          and gauge metrics of Boolean value type. The value type of the output is
          ``INT64``.
          REDUCE_FRACTION_TRUE (int): Reduce by computing the fraction of True-valued data points across
          time series for each alignment period. This reducer is valid for delta
          and gauge metrics of Boolean value type. The output value is in the
          range [0, 1] and has value type ``DOUBLE``.
          REDUCE_PERCENTILE_99 (int): Reduce by computing 99th percentile of data points across time
          series for each alignment period. This reducer is valid for gauge and
          delta metrics of numeric and distribution type. The value of the output
          is ``DOUBLE``
          REDUCE_PERCENTILE_95 (int): Reduce by computing 95th percentile of data points across time
          series for each alignment period. This reducer is valid for gauge and
          delta metrics of numeric and distribution type. The value of the output
          is ``DOUBLE``
          REDUCE_PERCENTILE_50 (int): Reduce by computing 50th percentile of data points across time
          series for each alignment period. This reducer is valid for gauge and
          delta metrics of numeric and distribution type. The value of the output
          is ``DOUBLE``
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
        REDUCE_COUNT_FALSE = 15
        REDUCE_FRACTION_TRUE = 8
        REDUCE_PERCENTILE_99 = 9
        REDUCE_PERCENTILE_95 = 10
        REDUCE_PERCENTILE_50 = 11
        REDUCE_PERCENTILE_05 = 12


class ChartOptions(object):
    class Mode(enum.IntEnum):
        """
        Chart mode options.

        Attributes:
          MODE_UNSPECIFIED (int): Mode is unspecified. The view will default to ``COLOR``.
          COLOR (int): The chart distinguishes data series using different color. Line
          colors may get reused when there are many lines in the chart.
          X_RAY (int): The chart uses the Stackdriver x-ray mode, in which each
          data set is plotted using the same semi-transparent color.
          STATS (int): The chart displays statistics such as average, median, 95th percentile,
          and more.
        """

        MODE_UNSPECIFIED = 0
        COLOR = 1
        X_RAY = 2
        STATS = 3


class PickTimeSeriesFilter(object):
    class Direction(enum.IntEnum):
        """
        Describes the ranking directions.

        Attributes:
          DIRECTION_UNSPECIFIED (int): Not allowed in well-formed requests.
          TOP (int): Pass the highest ranking inputs.
          BOTTOM (int): Pass the lowest ranking inputs.
        """

        DIRECTION_UNSPECIFIED = 0
        TOP = 1
        BOTTOM = 2

    class Method(enum.IntEnum):
        """
        The value reducers that can be applied to a PickTimeSeriesFilter.

        Attributes:
          METHOD_UNSPECIFIED (int): Not allowed in well-formed requests.
          METHOD_MEAN (int): Select the mean of all values.
          METHOD_MAX (int): Select the maximum value.
          METHOD_MIN (int): Select the minimum value.
          METHOD_SUM (int): Compute the sum of all values.
          METHOD_LATEST (int): Select the most recent value.
        """

        METHOD_UNSPECIFIED = 0
        METHOD_MEAN = 1
        METHOD_MAX = 2
        METHOD_MIN = 3
        METHOD_SUM = 4
        METHOD_LATEST = 5


class StatisticalTimeSeriesFilter(object):
    class Method(enum.IntEnum):
        """
        The filter methods that can be applied to a stream.

        Attributes:
          METHOD_UNSPECIFIED (int): Not allowed in well-formed requests.
          METHOD_CLUSTER_OUTLIER (int): Compute the outlier score of each stream.
        """

        METHOD_UNSPECIFIED = 0
        METHOD_CLUSTER_OUTLIER = 1


class Text(object):
    class Format(enum.IntEnum):
        """
        The format type of the text content.

        Attributes:
          FORMAT_UNSPECIFIED (int): Format is unspecified. Defaults to MARKDOWN.
          MARKDOWN (int): The text contains Markdown formatting.
          RAW (int): The text contains no special formatting.
        """

        FORMAT_UNSPECIFIED = 0
        MARKDOWN = 1
        RAW = 2


class Threshold(object):
    class Color(enum.IntEnum):
        """
        The color suggests an interpretation to the viewer when actual values cross
        the threshold. Comments on each color provide UX guidance on how users can
        be expected to interpret a given state color.

        Attributes:
          COLOR_UNSPECIFIED (int): Color is unspecified. Not allowed in well-formed requests.
          YELLOW (int): Crossing the threshold is "concerning" behavior.
          RED (int): Crossing the threshold is "emergency" behavior.
        """

        COLOR_UNSPECIFIED = 0
        YELLOW = 4
        RED = 6

    class Direction(enum.IntEnum):
        """
        Whether the threshold is considered crossed by an actual value above or
        below its threshold value.

        Attributes:
          DIRECTION_UNSPECIFIED (int): Not allowed in well-formed requests.
          ABOVE (int): The threshold will be considered crossed if the actual value is above
          the threshold value.
          BELOW (int): The threshold will be considered crossed if the actual value is below
          the threshold value.
        """

        DIRECTION_UNSPECIFIED = 0
        ABOVE = 1
        BELOW = 2


class XyChart(object):
    class DataSet(object):
        class PlotType(enum.IntEnum):
            """
            The types of plotting strategies for data sets.

            Attributes:
              PLOT_TYPE_UNSPECIFIED (int): Plot type is unspecified. The view will default to ``LINE``.
              LINE (int): The data is plotted as a set of lines (one line per series).
              STACKED_AREA (int): The data is plotted as a set of filled areas (one area per series),
              with the areas stacked vertically (the base of each area is the top of
              its predecessor, and the base of the first area is the X axis). Since
              the areas do not overlap, each is filled with a different opaque color.
              STACKED_BAR (int): The data is plotted as a set of rectangular boxes (one box per series),
              with the boxes stacked vertically (the base of each box is the top of
              its predecessor, and the base of the first box is the X axis). Since
              the boxes do not overlap, each is filled with a different opaque color.
              HEATMAP (int): The data is plotted as a heatmap. The series being plotted must have
              a ``DISTRIBUTION`` value type. The value of each bucket in the
              distribution is displayed as a color. This type is not currently
              available in the Stackdriver Monitoring application.
            """

            PLOT_TYPE_UNSPECIFIED = 0
            LINE = 1
            STACKED_AREA = 2
            STACKED_BAR = 3
            HEATMAP = 4

    class Axis(object):
        class Scale(enum.IntEnum):
            """
            Types of scales used in axes.

            Attributes:
              SCALE_UNSPECIFIED (int): Scale is unspecified. The view will default to ``LINEAR``.
              LINEAR (int): Linear scale.
              LOG10 (int): Logarithmic scale (base 10).
            """

            SCALE_UNSPECIFIED = 0
            LINEAR = 1
            LOG10 = 2
