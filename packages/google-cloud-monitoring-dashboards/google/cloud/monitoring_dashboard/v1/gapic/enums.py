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


class SparkChartType(enum.IntEnum):
    """
    ``rankingMethod`` is applied to each time series independently to
    produce the value which will be used to compare the time series to other
    time series.

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
          ALIGN_DELTA (int): Each of the definitions above may have "options" attached. These are
          just annotations which may cause code to be generated slightly
          differently or may contain hints for code that manipulates protocol
          messages.

          Clients may define custom options as extensions of the \*Options
          messages. These extensions may not yet be known at parsing time, so the
          parser cannot store the values in them. Instead it stores them in a
          field in the \*Options message called uninterpreted_option. This field
          must have the same name across all \*Options messages. We then use this
          field to populate the extensions when we build a descriptor, at which
          point all protos have been parsed and so all extensions are known.

          Extension numbers for custom options may be chosen as follows:

          -  For options which will only be used within a single application or
             organization, or for experimental options, use field numbers 50000
             through 99999. It is up to you to ensure that you do not use the same
             number for multiple options.
          -  For options which will be published and used publicly by multiple
             independent entities, e-mail
             protobuf-global-extension-registry@google.com to reserve extension
             numbers. Simply provide your project name (e.g. Objective-C plugin)
             and your project website (if available) -- there's no need to explain
             how you intend to use them. Usually you only need one extension
             number. You can declare multiple options with only one extension
             number by putting them in a sub-message. See the Custom Options
             section of the docs for examples:
             https://developers.google.com/protocol-buffers/docs/proto#options If
             this turns out to be popular, a web service will be set up to
             automatically assign option numbers.
          ALIGN_RATE (int): A designation of a specific field behavior (required, output only,
          etc.) in protobuf messages.

          Examples:

          string name = 1 [(google.api.field_behavior) = REQUIRED]; State state =
          1 [(google.api.field_behavior) = OUTPUT_ONLY]; google.protobuf.Duration
          ttl = 1 [(google.api.field_behavior) = INPUT_ONLY];
          google.protobuf.Timestamp expire_time = 1 [(google.api.field_behavior) =
          OUTPUT_ONLY, (google.api.field_behavior) = IMMUTABLE];
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
          ALIGN_MEAN (int): Optional. The historical or future-looking state of the resource
          pattern.

          Example:

          ::

              // The InspectTemplate message originally only supported resource
              // names with organization, and project was added later.
              message InspectTemplate {
                option (google.api.resource) = {
                  type: "dlp.googleapis.com/InspectTemplate"
                  pattern:
                  "organizations/{organization}/inspectTemplates/{inspect_template}"
                  pattern: "projects/{project}/inspectTemplates/{inspect_template}"
                  history: ORIGINALLY_SINGLE_PATTERN
                };
              }
          ALIGN_COUNT (int): If there are more results than have been returned, then this field
          is set to a non-empty value. To see the additional results, use that
          value as ``pageToken`` in the next call to this method.
          ALIGN_SUM (int): Align time series via aggregation. The resulting data point in
          the alignment period is the sum of all data points in the
          period. This alignment is valid for gauge and delta metrics with numeric
          and distribution values. The value type of the output is the
          same as the value type of the input.
          ALIGN_STDDEV (int): Reduce by computing 95th percentile of data points across time
          series for each alignment period. This reducer is valid for gauge and
          delta metrics of numeric and distribution type. The value of the output
          is ``DOUBLE``
          ALIGN_COUNT_TRUE (int): ``etag`` is used for optimistic concurrency control as a way to help
          prevent simultaneous updates of a policy from overwriting each other. An
          ``etag`` is returned in the response to ``GetDashboard``, and users are
          expected to put that etag in the request to ``UpdateDashboard`` to
          ensure that their change will be applied to the same version of the
          Dashboard configuration. The field should not be passed during dashboard
          creation.
          ALIGN_COUNT_FALSE (int): Reduce by computing 50th percentile of data points across time
          series for each alignment period. This reducer is valid for gauge and
          delta metrics of numeric and distribution type. The value of the output
          is ``DOUBLE``
          ALIGN_FRACTION_TRUE (int): A generic empty message that you can re-use to avoid defining
          duplicated empty messages in your APIs. A typical example is to use it
          as the request or the response type of an API method. For instance:

          ::

              service Foo {
                rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
              }

          The JSON representation for ``Empty`` is empty JSON object ``{}``.
          ALIGN_PERCENTILE_99 (int): If set, all the classes from the .proto file are wrapped in a single
          outer class with the given name. This applies to both Proto1 (equivalent
          to the old "--one_java_file" option) and Proto2 (where a .proto always
          translates to a single class, but you may want to explicitly choose the
          class name).
          ALIGN_PERCENTILE_95 (int): Reduce by computing the fraction of True-valued data points across
          time series for each alignment period. This reducer is valid for delta
          and gauge metrics of Boolean value type. The output value is in the
          range [0, 1] and has value type ``DOUBLE``.
          ALIGN_PERCENTILE_50 (int): Reduce by computing 5th percentile of data points across time series
          for each alignment period. This reducer is valid for gauge and delta
          metrics of numeric and distribution type. The value of the output is
          ``DOUBLE``
          ALIGN_PERCENTILE_05 (int): An indicator of the behavior of a given field (for example, that a
          field is required in requests, or given as output but ignored as input).
          This **does not** change the behavior in protocol buffers itself; it
          only denotes the behavior and may affect how API tooling handles the
          field.

          Note: This enum **may** receive new values in the future.
          ALIGN_PERCENT_CHANGE (int): The ``ListDashboards`` request.
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
          REDUCE_MEAN (int): The alignment period for per-\ ``time series`` alignment. If
          present, ``alignmentPeriod`` must be at least 60 seconds. After per-time
          series alignment, each time series will contain data points only on the
          period boundaries. If ``perSeriesAligner`` is not specified or equals
          ``ALIGN_NONE``, then this field is ignored. If ``perSeriesAligner`` is
          specified and does not equal ``ALIGN_NONE``, then this field must be
          defined; otherwise an error is returned.
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
          REDUCE_STDDEV (int): Signed seconds of the span of time. Must be from -315,576,000,000 to
          +315,576,000,000 inclusive. Note: these bounds are computed from: 60
          sec/min \* 60 min/hr \* 24 hr/day \* 365.25 days/year \* 10000 years
          REDUCE_COUNT (int): Denotes a field as required. This indicates that the field **must**
          be provided as part of the request, and failure to do so will cause an
          error (usually ``INVALID_ARGUMENT``).
          REDUCE_COUNT_TRUE (int): ``FieldMask`` represents a set of symbolic field paths, for example:

          ::

              paths: "f.a"
              paths: "f.b.d"

          Here ``f`` represents a field in some root message, ``a`` and ``b``
          fields in the message found in ``f``, and ``d`` a field found in the
          message in ``f.b``.

          Field masks are used to specify a subset of fields that should be
          returned by a get operation or modified by an update operation. Field
          masks also have a custom JSON encoding (see below).

          # Field Masks in Projections

          When used in the context of a projection, a response message or
          sub-message is filtered by the API to only contain those fields as
          specified in the mask. For example, if the mask in the previous example
          is applied to a response message as follows:

          ::

              f {
                a : 22
                b {
                  d : 1
                  x : 2
                }
                y : 13
              }
              z: 8

          The result will not contain specific values for fields x,y and z (their
          value will be set to the default, and omitted in proto text output):

          ::

              f {
                a : 22
                b {
                  d : 1
                }
              }

          A repeated field is not allowed except at the last position of a paths
          string.

          If a FieldMask object is not present in a get operation, the operation
          applies to all fields (as if a FieldMask of all fields had been
          specified).

          Note that a field mask does not necessarily apply to the top-level
          response message. In case of a REST get operation, the field mask
          applies directly to the response, but in case of a REST list operation,
          the mask instead applies to each individual message in the returned
          resource list. In case of a REST custom method, other definitions may be
          used. Where the mask applies will be clearly documented together with
          its declaration in the API. In any case, the effect on the returned
          resource/resources is required behavior for APIs.

          # Field Masks in Update Operations

          A field mask in update operations specifies which fields of the targeted
          resource are going to be updated. The API is required to only change the
          values of the fields as specified in the mask and leave the others
          untouched. If a resource is passed in to describe the updated values,
          the API ignores the values of all fields not covered by the mask.

          If a repeated field is specified for an update operation, new values
          will be appended to the existing repeated field in the target resource.
          Note that a repeated field is only allowed in the last position of a
          ``paths`` string.

          If a sub-message is specified in the last position of the field mask for
          an update operation, then new value will be merged into the existing
          sub-message in the target resource.

          For example, given the target message:

          ::

              f {
                b {
                  d: 1
                  x: 2
                }
                c: [1]
              }

          And an update message:

          ::

              f {
                b {
                  d: 10
                }
                c: [2]
              }

          then if the field mask is:

          paths: ["f.b", "f.c"]

          then the result will be:

          ::

              f {
                b {
                  d: 10
                  x: 2
                }
                c: [1, 2]
              }

          An implementation may provide options to override this default behavior
          for repeated and message fields.

          In order to reset a field's value to the default, the field must be in
          the mask and set to the default value in the provided resource. Hence,
          in order to reset all fields of a resource, provide a default instance
          of the resource and set all fields in the mask, or do not provide a mask
          as described below.

          If a field mask is not present on update, the operation applies to all
          fields (as if a field mask of all fields has been specified). Note that
          in the presence of schema evolution, this may mean that fields the
          client does not know and has therefore not filled into the request will
          be reset to their default. If this is unwanted behavior, a specific
          service may require a client to always specify a field mask, producing
          an error if not.

          As with get operations, the location of the resource which describes the
          updated values in the request message depends on the operation kind. In
          any case, the effect of the field mask is required to be honored by the
          API.

          ## Considerations for HTTP REST

          The HTTP kind of an update operation which uses a field mask must be set
          to PATCH instead of PUT in order to satisfy HTTP semantics (PUT must
          only be used for full updates).

          # JSON Encoding of Field Masks

          In JSON, a field mask is encoded as a single string where paths are
          separated by a comma. Fields name in each path are converted to/from
          lower-camel naming conventions.

          As an example, consider the following message declarations:

          ::

              message Profile {
                User user = 1;
                Photo photo = 2;
              }
              message User {
                string display_name = 1;
                string address = 2;
              }

          In proto a field mask for ``Profile`` may look as such:

          ::

              mask {
                paths: "user.display_name"
                paths: "photo"
              }

          In JSON, the same mask is represented as below:

          ::

              {
                mask: "user.displayName,photo"
              }

          # Field Masks and Oneof Fields

          Field masks treat fields in oneofs just as regular fields. Consider the
          following message:

          ::

              message SampleMessage {
                oneof test_oneof {
                  string name = 4;
                  SubMessage sub_message = 9;
                }
              }

          The field mask can be:

          ::

              mask {
                paths: "name"
              }

          Or:

          ::

              mask {
                paths: "sub_message"
              }

          Note that oneof type names ("test_oneof" in this case) cannot be used in
          paths.

          ## Field Mask Verification

          The implementation of any API method which has a FieldMask type field in
          the request should verify the included field paths, and return an
          ``INVALID_ARGUMENT`` error if any path is duplicated or unmappable.
          REDUCE_COUNT_FALSE (int): The approach to be used to align individual time series. Not all
          alignment functions may be applied to all time series, depending on the
          metric type and value type of the original time series. Alignment may
          change the metric type or the value type of the time series.

          Time series data must be aligned in order to perform cross-time series
          reduction. If ``crossSeriesReducer`` is specified, then
          ``perSeriesAligner`` must be specified and not equal ``ALIGN_NONE`` and
          ``alignmentPeriod`` must be specified; otherwise, an error is returned.
          REDUCE_FRACTION_TRUE (int): Plot type is unspecified. The view will default to ``LINE``.
          REDUCE_PERCENTILE_99 (int): The approach to be used to combine time series. Not all reducer
          functions may be applied to all time series, depending on the metric
          type and the value type of the original time series. Reduction may
          change the metric type of value type of the time series.

          Time series data must be aligned in order to perform cross-time series
          reduction. If ``crossSeriesReducer`` is specified, then
          ``perSeriesAligner`` must be specified and not equal ``ALIGN_NONE`` and
          ``alignmentPeriod`` must be specified; otherwise, an error is returned.
          REDUCE_PERCENTILE_95 (int): Denotes a field as output only. This indicates that the field is
          provided in responses, but including the field in a request does nothing
          (the server *must* ignore it and *must not* throw an error as a result
          of the field's presence).
          REDUCE_PERCENTILE_50 (int): Signed fractions of a second at nanosecond resolution of the span of
          time. Durations less than one second are represented with a 0
          ``seconds`` field and a positive or negative ``nanos`` field. For
          durations of one second or more, a non-zero value for the ``nanos``
          field must be of the same sign as the ``seconds`` field. Must be from
          -999,999,999 to +999,999,999 inclusive.
          REDUCE_PERCENTILE_05 (int): Set true to use the old proto1 MessageSet wire format for
          extensions. This is provided for backwards-compatibility with the
          MessageSet wire format. You should not use this for any other reason:
          It's less efficient, has fewer features, and is more complicated.

          The message must be defined exactly as follows: message Foo { option
          message_set_wire_format = true; extensions 4 to max; } Note that the
          message cannot have any defined fields; MessageSets only have
          extensions.

          All extensions of your type must be singular messages; e.g. they cannot
          be int32s, enums, or repeated messages.

          Because this is an option, the above two restrictions are not enforced
          by the protocol compiler.
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
          MODE_UNSPECIFIED (int): The data is plotted as a heatmap. The series being plotted must have
          a ``DISTRIBUTION`` value type. The value of each bucket in the
          distribution is displayed as a color. This type is not currently
          available in the Stackdriver Monitoring application.
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
              PLOT_TYPE_UNSPECIFIED (int): Align time series via aggregation. The resulting data point in the
              alignment period is the count of all data points in the period. This
              alignment is valid for gauge and delta metrics with numeric or Boolean
              values. The value type of the output is ``INT64``.
              LINE (int): The data is plotted as a set of lines (one line per series).
              STACKED_AREA (int): The data is plotted as a set of filled areas (one area per series),
              with the areas stacked vertically (the base of each area is the top of
              its predecessor, and the base of the first area is the X axis). Since
              the areas do not overlap, each is filled with a different opaque color.
              STACKED_BAR (int): The data is plotted as a set of rectangular boxes (one box per series),
              with the boxes stacked vertically (the base of each box is the top of
              its predecessor, and the base of the first box is the X axis). Since
              the boxes do not overlap, each is filled with a different opaque color.
              HEATMAP (int): If this field is not empty then it must contain the
              ``nextPageToken`` value returned by a previous call to this method.
              Using this field causes the method to return additional results from the
              previous method call.
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
              SCALE_UNSPECIFIED (int): Align time series via aggregation. The resulting data point in the
              alignment period is the standard deviation of all data points in the
              period. This alignment is valid for gauge and delta metrics with numeric
              values. The value type of the output is ``DOUBLE``.
              LINEAR (int): Linear scale.
              LOG10 (int): Logarithmic scale (base 10).
            """

            SCALE_UNSPECIFIED = 0
            LINEAR = 1
            LOG10 = 2
