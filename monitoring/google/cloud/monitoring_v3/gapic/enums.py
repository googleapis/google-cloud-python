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


class ComparisonType(enum.IntEnum):
    """
    Specifies an ordering relationship on two arguments, here called left and
    right.

    Attributes:
      COMPARISON_UNSPECIFIED (int): No ordering relationship is specified.
      COMPARISON_GT (int): The left argument is greater than the right argument.
      COMPARISON_GE (int): The left argument is greater than or equal to the right argument.
      COMPARISON_LT (int): The left argument is less than the right argument.
      COMPARISON_LE (int): The left argument is less than or equal to the right argument.
      COMPARISON_EQ (int): The left argument is equal to the right argument.
      COMPARISON_NE (int): The left argument is not equal to the right argument.
    """

    COMPARISON_UNSPECIFIED = 0
    COMPARISON_GT = 1
    COMPARISON_GE = 2
    COMPARISON_LT = 3
    COMPARISON_LE = 4
    COMPARISON_EQ = 5
    COMPARISON_NE = 6


class GroupResourceType(enum.IntEnum):
    """
    The supported resource types that can be used as values of
    ``group_resource.resource_type``. ``INSTANCE`` includes ``gce_instance``
    and ``aws_ec2_instance`` resource types. The resource types ``gae_app``
    and ``uptime_url`` are not valid here because group checks on App Engine
    modules and URLs are not allowed.

    Attributes:
      RESOURCE_TYPE_UNSPECIFIED (int): Default value (not valid).
      INSTANCE (int): A group of instances from Google Cloud Platform (GCP) or
      Amazon Web Services (AWS).
      AWS_ELB_LOAD_BALANCER (int): A group of Amazon ELB load balancers.
    """

    RESOURCE_TYPE_UNSPECIFIED = 0
    INSTANCE = 1
    AWS_ELB_LOAD_BALANCER = 2


class LaunchStage(enum.IntEnum):
    """
    The launch stage as defined by `Google Cloud Platform Launch
    Stages <http://cloud.google.com/terms/launch-stages>`__.

    Attributes:
      LAUNCH_STAGE_UNSPECIFIED (int): Do not use this default value.
      EARLY_ACCESS (int): Early Access features are limited to a closed group of testers. To use
      these features, you must sign up in advance and sign a Trusted Tester
      agreement (which includes confidentiality provisions). These features may
      be unstable, changed in backward-incompatible ways, and are not
      guaranteed to be released.
      ALPHA (int): Alpha is a limited availability test for releases before they are cleared
      for widespread use. By Alpha, all significant design issues are resolved
      and we are in the process of verifying functionality. Alpha customers
      need to apply for access, agree to applicable terms, and have their
      projects whitelisted. Alpha releases don’t have to be feature complete,
      no SLAs are provided, and there are no technical support obligations, but
      they will be far enough along that customers can actually use them in
      test environments or for limited-use tests -- just like they would in
      normal production cases.
      BETA (int): Beta is the point at which we are ready to open a release for any
      customer to use. There are no SLA or technical support obligations in a
      Beta release. Products will be complete from a feature perspective, but
      may have some open outstanding issues. Beta releases are suitable for
      limited production use cases.
      GA (int): GA features are open to all developers and are considered stable and
      fully qualified for production use.
      DEPRECATED (int): Deprecated features are scheduled to be shut down and removed. For more
      information, see the “Deprecation Policy” section of our `Terms of
      Service <https://cloud.google.com/terms/>`__ and the `Google Cloud
      Platform Subject to the Deprecation
      Policy <https://cloud.google.com/terms/deprecation>`__ documentation.
    """

    LAUNCH_STAGE_UNSPECIFIED = 0
    EARLY_ACCESS = 1
    ALPHA = 2
    BETA = 3
    GA = 4
    DEPRECATED = 5


class NullValue(enum.IntEnum):
    """
    ``NullValue`` is a singleton enumeration to represent the null value for
    the ``Value`` type union.

    The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """

    NULL_VALUE = 0


class ServiceTier(enum.IntEnum):
    """
    The tier of service for a Workspace. Please see the `service tiers
    documentation <https://cloud.google.com/monitoring/workspaces/tiers>`__
    for more details.

    Attributes:
      SERVICE_TIER_UNSPECIFIED (int): An invalid sentinel value, used to indicate that a tier has not
      been provided explicitly.
      SERVICE_TIER_BASIC (int): The Stackdriver Basic tier, a free tier of service that provides basic
      features, a moderate allotment of logs, and access to built-in metrics.
      A number of features are not available in this tier. For more details,
      see `the service tiers
      documentation <https://cloud.google.com/monitoring/workspaces/tiers>`__.
      SERVICE_TIER_PREMIUM (int): The Stackdriver Premium tier, a higher, more expensive tier of service
      that provides access to all Stackdriver features, lets you use
      Stackdriver with AWS accounts, and has a larger allotments for logs and
      metrics. For more details, see `the service tiers
      documentation <https://cloud.google.com/monitoring/workspaces/tiers>`__.
    """

    SERVICE_TIER_UNSPECIFIED = 0
    SERVICE_TIER_BASIC = 1
    SERVICE_TIER_PREMIUM = 2


class UptimeCheckRegion(enum.IntEnum):
    """
    The regions from which an uptime check can be run.

    Attributes:
      REGION_UNSPECIFIED (int): Default value if no region is specified. Will result in uptime checks
      running from all regions.
      USA (int): Allows checks to run from locations within the United States of America.
      EUROPE (int): Allows checks to run from locations within the continent of Europe.
      SOUTH_AMERICA (int): Allows checks to run from locations within the continent of South
      America.
      ASIA_PACIFIC (int): Allows checks to run from locations within the Asia Pacific area (ex:
      Singapore).
    """

    REGION_UNSPECIFIED = 0
    USA = 1
    EUROPE = 2
    SOUTH_AMERICA = 3
    ASIA_PACIFIC = 4


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
          the output is conceptually (second\_point - first\_point).
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
          ALIGN_PERCENT_CHANGE (int): Align and convert to a percentage change. This alignment is valid for
          gauge and delta metrics with numeric values. This alignment conceptually
          computes the equivalent of "((current - previous)/previous)\*100" where
          previous value is determined based on the alignmentPeriod. In the event
          that previous is 0 the calculated value is infinity with the exception
          that if both (current - previous) and previous are 0 the calculated
          value is 0. A 10 minute moving mean is computed at each point of the
          time window prior to the above calculation to smooth the metric and
          prevent false positives from very short lived spikes. Only applicable
          for data that is >= 0. Any values < 0 are treated as no data. While
          delta metrics are accepted by this alignment special care should be
          taken that the values for the metric will always be positive. The output
          is a gauge metric with value type ``DOUBLE``.
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
          REDUCE_STDDEV (int): Reduce by computing the standard deviation across time series for each
          alignment period. This reducer is valid for delta and gauge metrics with
          numeric or distribution values. The value type of the output is
          ``DOUBLE``.
          REDUCE_COUNT (int): Reduce by computing the count of data points across time series for each
          alignment period. This reducer is valid for delta and gauge metrics of
          numeric, Boolean, distribution, and string value type. The value type of
          the output is ``INT64``.
          REDUCE_COUNT_TRUE (int): Reduce by computing the count of True-valued data points across time
          series for each alignment period. This reducer is valid for delta and
          gauge metrics of Boolean value type. The value type of the output is
          ``INT64``.
          REDUCE_COUNT_FALSE (int): Reduce by computing the count of False-valued data points across time
          series for each alignment period. This reducer is valid for delta and
          gauge metrics of Boolean value type. The value type of the output is
          ``INT64``.
          REDUCE_FRACTION_TRUE (int): Reduce by computing the fraction of True-valued data points across time
          series for each alignment period. This reducer is valid for delta and
          gauge metrics of Boolean value type. The output value is in the range
          [0, 1] and has value type ``DOUBLE``.
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
          REDUCE_PERCENTILE_05 (int): Reduce by computing 5th percentile of data points across time series for
          each alignment period. This reducer is valid for gauge and delta metrics
          of numeric and distribution type. The value of the output is ``DOUBLE``
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


class AlertPolicy(object):
    class ConditionCombinerType(enum.IntEnum):
        """
        Operators for combining conditions.

        Attributes:
          COMBINE_UNSPECIFIED (int): An unspecified combiner.
          AND (int): Combine conditions using the logical ``AND`` operator. An incident is
          created only if all conditions are met simultaneously. This combiner is
          satisfied if all conditions are met, even if they are met on completely
          different resources.
          OR (int): Combine conditions using the logical ``OR`` operator. An incident is
          created if any of the listed conditions is met.
          AND_WITH_MATCHING_RESOURCE (int): Combine conditions using logical ``AND`` operator, but unlike the
          regular ``AND`` option, an incident is created only if all conditions
          are met simultaneously on at least one resource.
        """

        COMBINE_UNSPECIFIED = 0
        AND = 1
        OR = 2
        AND_WITH_MATCHING_RESOURCE = 3


class LabelDescriptor(object):
    class ValueType(enum.IntEnum):
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


class ListTimeSeriesRequest(object):
    class TimeSeriesView(enum.IntEnum):
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


class MetricDescriptor(object):
    class MetricKind(enum.IntEnum):
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

    class ValueType(enum.IntEnum):
        """
        The value type of a metric.

        Attributes:
          VALUE_TYPE_UNSPECIFIED (int): Do not use this default value.
          BOOL (int): The value is a boolean. This value type can be used only if the metric
          kind is ``GAUGE``.
          INT64 (int): The value is a signed 64-bit integer.
          DOUBLE (int): The value is a double precision floating point number.
          STRING (int): The value is a text string. This value type can be used only if the
          metric kind is ``GAUGE``.
          DISTRIBUTION (int): The value is a ``Distribution``.
          MONEY (int): The value is money.
        """

        VALUE_TYPE_UNSPECIFIED = 0
        BOOL = 1
        INT64 = 2
        DOUBLE = 3
        STRING = 4
        DISTRIBUTION = 5
        MONEY = 6


class NotificationChannel(object):
    class VerificationStatus(enum.IntEnum):
        """
        Indicates whether the channel has been verified or not. It is illegal to
        specify this field in a ``CreateNotificationChannel`` or an
        ``UpdateNotificationChannel`` operation.

        Attributes:
          VERIFICATION_STATUS_UNSPECIFIED (int): Sentinel value used to indicate that the state is unknown, omitted, or
          is not applicable (as in the case of channels that neither support
          nor require verification in order to function).
          UNVERIFIED (int): The channel has yet to be verified and requires verification to function.
          Note that this state also applies to the case where the verification
          process has been initiated by sending a verification code but where
          the verification code has not been submitted to complete the process.
          VERIFIED (int): It has been proven that notifications can be received on this
          notification channel and that someone on the project has access
          to messages that are delivered to that channel.
        """

        VERIFICATION_STATUS_UNSPECIFIED = 0
        UNVERIFIED = 1
        VERIFIED = 2
