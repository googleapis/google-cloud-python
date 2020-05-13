# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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


class CalendarPeriod(enum.IntEnum):
    """
    A ``CalendarPeriod`` represents the abstract concept of a time
    period that has a canonical start. Grammatically, "the start of the
    current ``CalendarPeriod``." All calendar times begin at midnight UTC.

    Attributes:
      CALENDAR_PERIOD_UNSPECIFIED (int): Undefined period, raises an error.
      DAY (int): A day.
      WEEK (int): A week. Weeks begin on Monday, following `ISO
      8601 <https://en.wikipedia.org/wiki/ISO_week_date>`__.
      FORTNIGHT (int): A fortnight. The first calendar fortnight of the year begins at the
      start of week 1 according to `ISO
      8601 <https://en.wikipedia.org/wiki/ISO_week_date>`__.
      MONTH (int): A month.
      QUARTER (int): A quarter. Quarters start on dates 1-Jan, 1-Apr, 1-Jul, and 1-Oct of each
      year.
      HALF (int): A half-year. Half-years start on dates 1-Jan and 1-Jul.
      YEAR (int): A year.
    """

    CALENDAR_PERIOD_UNSPECIFIED = 0
    DAY = 1
    WEEK = 2
    FORTNIGHT = 3
    MONTH = 4
    QUARTER = 5
    HALF = 6
    YEAR = 7


class ComparisonType(enum.IntEnum):
    """
    Specifies an ordering relationship on two arguments, called ``left``
    and ``right``.

    Attributes:
      COMPARISON_UNSPECIFIED (int): No ordering relationship is specified.
      COMPARISON_GT (int): True if the left argument is greater than the right argument.
      COMPARISON_GE (int): True if the left argument is greater than or equal to the right argument.
      COMPARISON_LT (int): True if the left argument is less than the right argument.
      COMPARISON_LE (int): True if the left argument is less than or equal to the right argument.
      COMPARISON_EQ (int): True if the left argument is equal to the right argument.
      COMPARISON_NE (int): True if the left argument is not equal to the right argument.
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
      DEPRECATED (int): Deprecated features are scheduled to be shut down and removed. For
      more information, see the “Deprecation Policy” section of our `Terms of
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
    ``NullValue`` is a singleton enumeration to represent the null value
    for the ``Value`` type union.

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
      SERVICE_TIER_BASIC (int): The Stackdriver Basic tier, a free tier of service that provides
      basic features, a moderate allotment of logs, and access to built-in
      metrics. A number of features are not available in this tier. For more
      details, see `the service tiers
      documentation <https://cloud.google.com/monitoring/workspaces/tiers>`__.
      SERVICE_TIER_PREMIUM (int): The Stackdriver Premium tier, a higher, more expensive tier of
      service that provides access to all Stackdriver features, lets you use
      Stackdriver with AWS accounts, and has a larger allotments for logs and
      metrics. For more details, see `the service tiers
      documentation <https://cloud.google.com/monitoring/workspaces/tiers>`__.
    """

    SERVICE_TIER_UNSPECIFIED = 0
    SERVICE_TIER_BASIC = 1
    SERVICE_TIER_PREMIUM = 2


class UptimeCheckRegion(enum.IntEnum):
    """
    The regions from which an Uptime check can be run.

    Attributes:
      REGION_UNSPECIFIED (int): Default value if no region is specified. Will result in Uptime checks
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
        The ``Aligner`` specifies the operation that will be applied to the
        data points in each alignment period in a time series. Except for
        ``ALIGN_NONE``, which specifies that no operation be applied, each
        alignment operation replaces the set of data values in each alignment
        period with a single value: the result of applying the operation to the
        data values. An aligned time series has a single data value at the end
        of each ``alignment_period``.

        An alignment operation can change the data type of the values, too. For
        example, if you apply a counting operation to boolean values, the data
        ``value_type`` in the original time series is ``BOOLEAN``, but the
        ``value_type`` in the aligned result is ``INT64``.

        Attributes:
          ALIGN_NONE (int): No alignment. Raw data is returned. Not valid if cross-series
          reduction is requested. The ``value_type`` of the result is the same as
          the ``value_type`` of the input.
          ALIGN_DELTA (int): Align and convert to ``DELTA``. The output is ``delta = y1 - y0``.

          This alignment is valid for ``CUMULATIVE`` and ``DELTA`` metrics. If the
          selected alignment period results in periods with no data, then the
          aligned value for such a period is created by interpolation. The
          ``value_type`` of the aligned result is the same as the ``value_type``
          of the input.
          ALIGN_RATE (int): Align and convert to a rate. The result is computed as
          ``rate = (y1 - y0)/(t1 - t0)``, or "delta over time". Think of this
          aligner as providing the slope of the line that passes through the value
          at the start and at the end of the ``alignment_period``.

          This aligner is valid for ``CUMULATIVE`` and ``DELTA`` metrics with
          numeric values. If the selected alignment period results in periods with
          no data, then the aligned value for such a period is created by
          interpolation. The output is a ``GAUGE`` metric with ``value_type``
          ``DOUBLE``.

          If, by "rate", you mean "percentage change", see the
          ``ALIGN_PERCENT_CHANGE`` aligner instead.
          ALIGN_INTERPOLATE (int): Align by interpolating between adjacent points around the alignment
          period boundary. This aligner is valid for ``GAUGE`` metrics with
          numeric values. The ``value_type`` of the aligned result is the same as
          the ``value_type`` of the input.
          ALIGN_NEXT_OLDER (int): Align by moving the most recent data point before the end of the
          alignment period to the boundary at the end of the alignment period.
          This aligner is valid for ``GAUGE`` metrics. The ``value_type`` of the
          aligned result is the same as the ``value_type`` of the input.
          ALIGN_MIN (int): Align the time series by returning the minimum value in each
          alignment period. This aligner is valid for ``GAUGE`` and ``DELTA``
          metrics with numeric values. The ``value_type`` of the aligned result is
          the same as the ``value_type`` of the input.
          ALIGN_MAX (int): Align the time series by returning the maximum value in each
          alignment period. This aligner is valid for ``GAUGE`` and ``DELTA``
          metrics with numeric values. The ``value_type`` of the aligned result is
          the same as the ``value_type`` of the input.
          ALIGN_MEAN (int): Align the time series by returning the mean value in each alignment
          period. This aligner is valid for ``GAUGE`` and ``DELTA`` metrics with
          numeric values. The ``value_type`` of the aligned result is ``DOUBLE``.
          ALIGN_COUNT (int): Align the time series by returning the number of values in each
          alignment period. This aligner is valid for ``GAUGE`` and ``DELTA``
          metrics with numeric or Boolean values. The ``value_type`` of the
          aligned result is ``INT64``.
          ALIGN_SUM (int): Align the time series by returning the sum of the values in each
          alignment period. This aligner is valid for ``GAUGE`` and ``DELTA``
          metrics with numeric and distribution values. The ``value_type`` of the
          aligned result is the same as the ``value_type`` of the input.
          ALIGN_STDDEV (int): Align the time series by returning the standard deviation of the
          values in each alignment period. This aligner is valid for ``GAUGE`` and
          ``DELTA`` metrics with numeric values. The ``value_type`` of the output
          is ``DOUBLE``.
          ALIGN_COUNT_TRUE (int): Align the time series by returning the number of ``True`` values in
          each alignment period. This aligner is valid for ``GAUGE`` metrics with
          Boolean values. The ``value_type`` of the output is ``INT64``.
          ALIGN_COUNT_FALSE (int): Align the time series by returning the number of ``False`` values in
          each alignment period. This aligner is valid for ``GAUGE`` metrics with
          Boolean values. The ``value_type`` of the output is ``INT64``.
          ALIGN_FRACTION_TRUE (int): Align the time series by returning the ratio of the number of
          ``True`` values to the total number of values in each alignment period.
          This aligner is valid for ``GAUGE`` metrics with Boolean values. The
          output value is in the range [0.0, 1.0] and has ``value_type``
          ``DOUBLE``.
          ALIGN_PERCENTILE_99 (int): Align the time series by using `percentile
          aggregation <https://en.wikipedia.org/wiki/Percentile>`__. The resulting
          data point in each alignment period is the 99th percentile of all data
          points in the period. This aligner is valid for ``GAUGE`` and ``DELTA``
          metrics with distribution values. The output is a ``GAUGE`` metric with
          ``value_type`` ``DOUBLE``.
          ALIGN_PERCENTILE_95 (int): Align the time series by using `percentile
          aggregation <https://en.wikipedia.org/wiki/Percentile>`__. The resulting
          data point in each alignment period is the 95th percentile of all data
          points in the period. This aligner is valid for ``GAUGE`` and ``DELTA``
          metrics with distribution values. The output is a ``GAUGE`` metric with
          ``value_type`` ``DOUBLE``.
          ALIGN_PERCENTILE_50 (int): Align the time series by using `percentile
          aggregation <https://en.wikipedia.org/wiki/Percentile>`__. The resulting
          data point in each alignment period is the 50th percentile of all data
          points in the period. This aligner is valid for ``GAUGE`` and ``DELTA``
          metrics with distribution values. The output is a ``GAUGE`` metric with
          ``value_type`` ``DOUBLE``.
          ALIGN_PERCENTILE_05 (int): Align the time series by using `percentile
          aggregation <https://en.wikipedia.org/wiki/Percentile>`__. The resulting
          data point in each alignment period is the 5th percentile of all data
          points in the period. This aligner is valid for ``GAUGE`` and ``DELTA``
          metrics with distribution values. The output is a ``GAUGE`` metric with
          ``value_type`` ``DOUBLE``.
          ALIGN_PERCENT_CHANGE (int): Align and convert to a percentage change. This aligner is valid for
          ``GAUGE`` and ``DELTA`` metrics with numeric values. This alignment
          returns ``((current - previous)/previous) * 100``, where the value of
          ``previous`` is determined based on the ``alignment_period``.

          If the values of ``current`` and ``previous`` are both 0, then the
          returned value is 0. If only ``previous`` is 0, the returned value is
          infinity.

          A 10-minute moving mean is computed at each point of the alignment
          period prior to the above calculation to smooth the metric and prevent
          false positives from very short-lived spikes. The moving mean is only
          applicable for data whose values are ``>= 0``. Any values ``< 0`` are
          treated as a missing datapoint, and are ignored. While ``DELTA`` metrics
          are accepted by this alignment, special care should be taken that the
          values for the metric will always be positive. The output is a ``GAUGE``
          metric with ``value_type`` ``DOUBLE``.
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
        A Reducer operation describes how to aggregate data points from multiple
        time series into a single time series, where the value of each data point
        in the resulting series is a function of all the already aligned values in
        the input time series.

        Attributes:
          REDUCE_NONE (int): No cross-time series reduction. The output of the ``Aligner`` is
          returned.
          REDUCE_MEAN (int): Reduce by computing the mean value across time series for each
          alignment period. This reducer is valid for ``DELTA`` and ``GAUGE``
          metrics with numeric or distribution values. The ``value_type`` of the
          output is ``DOUBLE``.
          REDUCE_MIN (int): Reduce by computing the minimum value across time series for each
          alignment period. This reducer is valid for ``DELTA`` and ``GAUGE``
          metrics with numeric values. The ``value_type`` of the output is the
          same as the ``value_type`` of the input.
          REDUCE_MAX (int): Reduce by computing the maximum value across time series for each
          alignment period. This reducer is valid for ``DELTA`` and ``GAUGE``
          metrics with numeric values. The ``value_type`` of the output is the
          same as the ``value_type`` of the input.
          REDUCE_SUM (int): Reduce by computing the sum across time series for each alignment
          period. This reducer is valid for ``DELTA`` and ``GAUGE`` metrics with
          numeric and distribution values. The ``value_type`` of the output is the
          same as the ``value_type`` of the input.
          REDUCE_STDDEV (int): Reduce by computing the standard deviation across time series for
          each alignment period. This reducer is valid for ``DELTA`` and ``GAUGE``
          metrics with numeric or distribution values. The ``value_type`` of the
          output is ``DOUBLE``.
          REDUCE_COUNT (int): Reduce by computing the number of data points across time series for
          each alignment period. This reducer is valid for ``DELTA`` and ``GAUGE``
          metrics of numeric, Boolean, distribution, and string ``value_type``.
          The ``value_type`` of the output is ``INT64``.
          REDUCE_COUNT_TRUE (int): Reduce by computing the number of ``True``-valued data points across
          time series for each alignment period. This reducer is valid for
          ``DELTA`` and ``GAUGE`` metrics of Boolean ``value_type``. The
          ``value_type`` of the output is ``INT64``.
          REDUCE_COUNT_FALSE (int): Reduce by computing the number of ``False``-valued data points
          across time series for each alignment period. This reducer is valid for
          ``DELTA`` and ``GAUGE`` metrics of Boolean ``value_type``. The
          ``value_type`` of the output is ``INT64``.
          REDUCE_FRACTION_TRUE (int): Reduce by computing the ratio of the number of ``True``-valued data
          points to the total number of data points for each alignment period.
          This reducer is valid for ``DELTA`` and ``GAUGE`` metrics of Boolean
          ``value_type``. The output value is in the range [0.0, 1.0] and has
          ``value_type`` ``DOUBLE``.
          REDUCE_PERCENTILE_99 (int): Reduce by computing the `99th
          percentile <https://en.wikipedia.org/wiki/Percentile>`__ of data points
          across time series for each alignment period. This reducer is valid for
          ``GAUGE`` and ``DELTA`` metrics of numeric and distribution type. The
          value of the output is ``DOUBLE``.
          REDUCE_PERCENTILE_95 (int): Reduce by computing the `95th
          percentile <https://en.wikipedia.org/wiki/Percentile>`__ of data points
          across time series for each alignment period. This reducer is valid for
          ``GAUGE`` and ``DELTA`` metrics of numeric and distribution type. The
          value of the output is ``DOUBLE``.
          REDUCE_PERCENTILE_50 (int): Reduce by computing the `50th
          percentile <https://en.wikipedia.org/wiki/Percentile>`__ of data points
          across time series for each alignment period. This reducer is valid for
          ``GAUGE`` and ``DELTA`` metrics of numeric and distribution type. The
          value of the output is ``DOUBLE``.
          REDUCE_PERCENTILE_05 (int): Reduce by computing the `5th
          percentile <https://en.wikipedia.org/wiki/Percentile>`__ of data points
          across time series for each alignment period. This reducer is valid for
          ``GAUGE`` and ``DELTA`` metrics of numeric and distribution type. The
          value of the output is ``DOUBLE``.
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
          AND (int): Combine conditions using the logical ``AND`` operator. An incident
          is created only if all the conditions are met simultaneously. This
          combiner is satisfied if all conditions are met, even if they are met on
          completely different resources.
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


class InternalChecker(object):
    class State(enum.IntEnum):
        """
        Operational states for an internal checker.

        Attributes:
          UNSPECIFIED (int): An internal checker should never be in the unspecified state.
          CREATING (int): The checker is being created, provisioned, and configured. A checker
          in this state can be returned by ``ListInternalCheckers`` or
          ``GetInternalChecker``, as well as by examining the `long running
          Operation <https://cloud.google.com/apis/design/design_patterns#long_running_operations>`__
          that created it.
          RUNNING (int): The checker is running and available for use. A checker in this
          state can be returned by ``ListInternalCheckers`` or
          ``GetInternalChecker`` as well as by examining the `long running
          Operation <https://cloud.google.com/apis/design/design_patterns#long_running_operations>`__
          that created it. If a checker is being torn down, it is neither visible
          nor usable, so there is no "deleting" or "down" state.
        """

        UNSPECIFIED = 0
        CREATING = 1
        RUNNING = 2


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
          BOOL (int): The value is a boolean. This value type can be used only if the
          metric kind is ``GAUGE``.
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
        Indicates whether the channel has been verified or not. It is
        illegal to specify this field in a ``CreateNotificationChannel`` or an
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


class ServiceLevelObjective(object):
    class View(enum.IntEnum):
        """
        ``ServiceLevelObjective.View`` determines what form of
        ``ServiceLevelObjective`` is returned from ``GetServiceLevelObjective``,
        ``ListServiceLevelObjectives``, and
        ``ListServiceLevelObjectiveVersions`` RPCs.

        Attributes:
          VIEW_UNSPECIFIED (int): Same as FULL.
          FULL (int): Return the embedded ``ServiceLevelIndicator`` in the form in which
          it was defined. If it was defined using a ``BasicSli``, return that
          ``BasicSli``.
          EXPLICIT (int): For ``ServiceLevelIndicator``\ s using ``BasicSli`` articulation,
          instead return the ``ServiceLevelIndicator`` with its mode of
          computation fully spelled out as a ``RequestBasedSli``. For
          ``ServiceLevelIndicator``\ s using ``RequestBasedSli`` or
          ``WindowsBasedSli``, return the ``ServiceLevelIndicator`` as it was
          provided.
        """

        VIEW_UNSPECIFIED = 0
        FULL = 2
        EXPLICIT = 1


class UptimeCheckConfig(object):
    class HttpCheck(object):
        class ContentType(enum.IntEnum):
            """
            Header options corresponding to the Content-Type of the body in HTTP
            requests. Note that a ``Content-Type`` header cannot be present in the
            ``headers`` field if this field is specified.

            Attributes:
              TYPE_UNSPECIFIED (int): No content type specified. If the request method is POST, an
              unspecified content type results in a check creation rejection.
              URL_ENCODED (int): ``body`` is in URL-encoded form. Equivalent to setting the
              ``Content-Type`` to ``application/x-www-form-urlencoded`` in the HTTP
              request.
            """

            TYPE_UNSPECIFIED = 0
            URL_ENCODED = 1

        class RequestMethod(enum.IntEnum):
            """
            The HTTP request method options.

            Attributes:
              METHOD_UNSPECIFIED (int): No request method specified.
              GET (int): GET request.
              POST (int): POST request.
            """

            METHOD_UNSPECIFIED = 0
            GET = 1
            POST = 2

    class ContentMatcher(object):
        class ContentMatcherOption(enum.IntEnum):
            """
            Options to perform content matching.

            Attributes:
              CONTENT_MATCHER_OPTION_UNSPECIFIED (int): No content matcher type specified (maintained for backward
              compatibility, but deprecated for future use). Treated as
              ``CONTAINS_STRING``.
              CONTAINS_STRING (int): Selects substring matching. The match succeeds if the output
              contains the ``content`` string. This is the default value for checks
              without a ``matcher`` option, or where the value of ``matcher`` is
              ``CONTENT_MATCHER_OPTION_UNSPECIFIED``.
              NOT_CONTAINS_STRING (int): Selects negation of substring matching. The match succeeds if the
              output does *NOT* contain the ``content`` string.
              MATCHES_REGEX (int): Selects regular-expression matching. The match succeeds of the
              output matches the regular expression specified in the ``content``
              string.
              NOT_MATCHES_REGEX (int): Selects negation of regular-expression matching. The match succeeds
              if the output does *NOT* match the regular expression specified in the
              ``content`` string.
            """

            CONTENT_MATCHER_OPTION_UNSPECIFIED = 0
            CONTAINS_STRING = 1
            NOT_CONTAINS_STRING = 2
            MATCHES_REGEX = 3
            NOT_MATCHES_REGEX = 4
