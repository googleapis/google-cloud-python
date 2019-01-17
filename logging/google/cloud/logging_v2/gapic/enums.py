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


class LogSeverity(enum.IntEnum):
    """
    The severity of the event described in a log entry, expressed as one of
    the standard severity levels listed below. For your reference, the
    levels are assigned the listed numeric values. The effect of using
    numeric values other than those listed is undefined.

    You can filter for log entries by severity. For example, the following
    filter expression will match log entries with severities ``INFO``,
    ``NOTICE``, and ``WARNING``:

    ::

         severity > DEBUG AND severity <= WARNING

    If you are writing log entries, you should map other severity encodings
    to one of these standard levels. For example, you might map all of
    Java's FINE, FINER, and FINEST levels to ``LogSeverity.DEBUG``. You can
    preserve the original severity level in the log entry payload if you
    wish.

    Attributes:
      DEFAULT (int): (0) The log entry has no assigned severity level.
      DEBUG (int): (100) Debug or trace information.
      INFO (int): (200) Routine information, such as ongoing status or performance.
      NOTICE (int): (300) Normal but significant events, such as start up, shut down, or
      a configuration change.
      WARNING (int): (400) Warning events might cause problems.
      ERROR (int): (500) Error events are likely to cause problems.
      CRITICAL (int): (600) Critical events cause more severe problems or outages.
      ALERT (int): (700) A person must take an action immediately.
      EMERGENCY (int): (800) One or more systems are unusable.
    """

    DEFAULT = 0
    DEBUG = 100
    INFO = 200
    NOTICE = 300
    WARNING = 400
    ERROR = 500
    CRITICAL = 600
    ALERT = 700
    EMERGENCY = 800


class NullValue(enum.IntEnum):
    """
    ``NullValue`` is a singleton enumeration to represent the null value for
    the ``Value`` type union.

    The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """

    NULL_VALUE = 0


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


class LogMetric(object):
    class ApiVersion(enum.IntEnum):
        """
        Logging API version.

        Attributes:
          V2 (int): Logging API v2.
          V1 (int): Logging API v1.
        """

        V2 = 0
        V1 = 1


class LogSink(object):
    class VersionFormat(enum.IntEnum):
        """
        Available log entry formats. Log entries can be written to
        Logging in either format and can be exported in either format.
        Version 2 is the preferred format.

        Attributes:
          VERSION_FORMAT_UNSPECIFIED (int): An unspecified format version that will default to V2.
          V2 (int): ``LogEntry`` version 2 format.
          V1 (int): ``LogEntry`` version 1 format.
        """

        VERSION_FORMAT_UNSPECIFIED = 0
        V2 = 1
        V1 = 2


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
