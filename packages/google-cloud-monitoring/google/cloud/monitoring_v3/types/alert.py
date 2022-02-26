# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.cloud.monitoring_v3.types import common
from google.cloud.monitoring_v3.types import mutation_record as gm_mutation_record
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(package="google.monitoring.v3", manifest={"AlertPolicy",},)


class AlertPolicy(proto.Message):
    r"""A description of the conditions under which some aspect of your
    system is considered to be "unhealthy" and the ways to notify people
    or services about this state. For an overview of alert policies, see
    `Introduction to
    Alerting <https://cloud.google.com/monitoring/alerts/>`__.

    Attributes:
        name (str):
            Required if the policy exists. The resource name for this
            policy. The format is:

            ::

                projects/[PROJECT_ID_OR_NUMBER]/alertPolicies/[ALERT_POLICY_ID]

            ``[ALERT_POLICY_ID]`` is assigned by Stackdriver Monitoring
            when the policy is created. When calling the
            [alertPolicies.create][google.monitoring.v3.AlertPolicyService.CreateAlertPolicy]
            method, do not include the ``name`` field in the alerting
            policy passed as part of the request.
        display_name (str):
            A short name or phrase used to identify the
            policy in dashboards, notifications, and
            incidents. To avoid confusion, don't use the
            same display name for multiple policies in the
            same project. The name is limited to 512 Unicode
            characters.
        documentation (google.cloud.monitoring_v3.types.AlertPolicy.Documentation):
            Documentation that is included with
            notifications and incidents related to this
            policy. Best practice is for the documentation
            to include information to help responders
            understand, mitigate, escalate, and correct the
            underlying problems detected by the alerting
            policy. Notification channels that have limited
            capacity might not show this documentation.
        user_labels (Sequence[google.cloud.monitoring_v3.types.AlertPolicy.UserLabelsEntry]):
            User-supplied key/value data to be used for organizing and
            identifying the ``AlertPolicy`` objects.

            The field can contain up to 64 entries. Each key and value
            is limited to 63 Unicode characters or 128 bytes, whichever
            is smaller. Labels and values can contain only lowercase
            letters, numerals, underscores, and dashes. Keys must begin
            with a letter.
        conditions (Sequence[google.cloud.monitoring_v3.types.AlertPolicy.Condition]):
            A list of conditions for the policy. The conditions are
            combined by AND or OR according to the ``combiner`` field.
            If the combined conditions evaluate to true, then an
            incident is created. A policy can have from one to six
            conditions. If ``condition_time_series_query_language`` is
            present, it must be the only ``condition``.
        combiner (google.cloud.monitoring_v3.types.AlertPolicy.ConditionCombinerType):
            How to combine the results of multiple conditions to
            determine if an incident should be opened. If
            ``condition_time_series_query_language`` is present, this
            must be ``COMBINE_UNSPECIFIED``.
        enabled (google.protobuf.wrappers_pb2.BoolValue):
            Whether or not the policy is enabled. On
            write, the default interpretation if unset is
            that the policy is enabled. On read, clients
            should not make any assumption about the state
            if it has not been populated. The field should
            always be populated on List and Get operations,
            unless a field projection has been specified
            that strips it out.
        validity (google.rpc.status_pb2.Status):
            Read-only description of how the alert policy
            is invalid. OK if the alert policy is valid. If
            not OK, the alert policy will not generate
            incidents.
        notification_channels (Sequence[str]):
            Identifies the notification channels to which notifications
            should be sent when incidents are opened or closed or when
            new violations occur on an already opened incident. Each
            element of this array corresponds to the ``name`` field in
            each of the
            [``NotificationChannel``][google.monitoring.v3.NotificationChannel]
            objects that are returned from the
            [``ListNotificationChannels``]
            [google.monitoring.v3.NotificationChannelService.ListNotificationChannels]
            method. The format of the entries in this field is:

            ::

                projects/[PROJECT_ID_OR_NUMBER]/notificationChannels/[CHANNEL_ID]
        creation_record (google.cloud.monitoring_v3.types.MutationRecord):
            A read-only record of the creation of the
            alerting policy. If provided in a call to create
            or update, this field will be ignored.
        mutation_record (google.cloud.monitoring_v3.types.MutationRecord):
            A read-only record of the most recent change
            to the alerting policy. If provided in a call to
            create or update, this field will be ignored.
        alert_strategy (google.cloud.monitoring_v3.types.AlertPolicy.AlertStrategy):
            Control over how this alert policy's
            notification channels are notified.
    """

    class ConditionCombinerType(proto.Enum):
        r"""Operators for combining conditions."""
        COMBINE_UNSPECIFIED = 0
        AND = 1
        OR = 2
        AND_WITH_MATCHING_RESOURCE = 3

    class Documentation(proto.Message):
        r"""A content string and a MIME type that describes the content
        string's format.

        Attributes:
            content (str):
                The text of the documentation, interpreted according to
                ``mime_type``. The content may not exceed 8,192 Unicode
                characters and may not exceed more than 10,240 bytes when
                encoded in UTF-8 format, whichever is smaller.
            mime_type (str):
                The format of the ``content`` field. Presently, only the
                value ``"text/markdown"`` is supported. See
                `Markdown <https://en.wikipedia.org/wiki/Markdown>`__ for
                more information.
        """

        content = proto.Field(proto.STRING, number=1,)
        mime_type = proto.Field(proto.STRING, number=2,)

    class Condition(proto.Message):
        r"""A condition is a true/false test that determines when an
        alerting policy should open an incident. If a condition
        evaluates to true, it signifies that something is wrong.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            name (str):
                Required if the condition exists. The unique resource name
                for this condition. Its format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/alertPolicies/[POLICY_ID]/conditions/[CONDITION_ID]

                ``[CONDITION_ID]`` is assigned by Stackdriver Monitoring
                when the condition is created as part of a new or updated
                alerting policy.

                When calling the
                [alertPolicies.create][google.monitoring.v3.AlertPolicyService.CreateAlertPolicy]
                method, do not include the ``name`` field in the conditions
                of the requested alerting policy. Stackdriver Monitoring
                creates the condition identifiers and includes them in the
                new policy.

                When calling the
                [alertPolicies.update][google.monitoring.v3.AlertPolicyService.UpdateAlertPolicy]
                method to update a policy, including a condition ``name``
                causes the existing condition to be updated. Conditions
                without names are added to the updated policy. Existing
                conditions are deleted if they are not updated.

                Best practice is to preserve ``[CONDITION_ID]`` if you make
                only small changes, such as those to condition thresholds,
                durations, or trigger values. Otherwise, treat the change as
                a new condition and let the existing condition be deleted.
            display_name (str):
                A short name or phrase used to identify the
                condition in dashboards, notifications, and
                incidents. To avoid confusion, don't use the
                same display name for multiple conditions in the
                same policy.
            condition_threshold (google.cloud.monitoring_v3.types.AlertPolicy.Condition.MetricThreshold):
                A condition that compares a time series
                against a threshold.

                This field is a member of `oneof`_ ``condition``.
            condition_absent (google.cloud.monitoring_v3.types.AlertPolicy.Condition.MetricAbsence):
                A condition that checks that a time series
                continues to receive new data points.

                This field is a member of `oneof`_ ``condition``.
            condition_matched_log (google.cloud.monitoring_v3.types.AlertPolicy.Condition.LogMatch):
                A condition that checks for log messages
                matching given constraints. If set, no other
                conditions can be present.

                This field is a member of `oneof`_ ``condition``.
            condition_monitoring_query_language (google.cloud.monitoring_v3.types.AlertPolicy.Condition.MonitoringQueryLanguageCondition):
                A condition that uses the Monitoring Query
                Language to define alerts.

                This field is a member of `oneof`_ ``condition``.
        """

        class Trigger(proto.Message):
            r"""Specifies how many time series must fail a predicate to trigger a
            condition. If not specified, then a ``{count: 1}`` trigger is used.

            This message has `oneof`_ fields (mutually exclusive fields).
            For each oneof, at most one member field can be set at the same time.
            Setting any member of the oneof automatically clears all other
            members.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                count (int):
                    The absolute number of time series that must
                    fail the predicate for the condition to be
                    triggered.

                    This field is a member of `oneof`_ ``type``.
                percent (float):
                    The percentage of time series that must fail
                    the predicate for the condition to be triggered.

                    This field is a member of `oneof`_ ``type``.
            """

            count = proto.Field(proto.INT32, number=1, oneof="type",)
            percent = proto.Field(proto.DOUBLE, number=2, oneof="type",)

        class MetricThreshold(proto.Message):
            r"""A condition type that compares a collection of time series
            against a threshold.

            Attributes:
                filter (str):
                    Required. A
                    `filter <https://cloud.google.com/monitoring/api/v3/filters>`__
                    that identifies which time series should be compared with
                    the threshold.

                    The filter is similar to the one that is specified in the
                    ```ListTimeSeries``
                    request <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list>`__
                    (that call is useful to verify the time series that will be
                    retrieved / processed). The filter must specify the metric
                    type and the resource type. Optionally, it can specify
                    resource labels and metric labels. This field must not
                    exceed 2048 Unicode characters in length.
                aggregations (Sequence[google.cloud.monitoring_v3.types.Aggregation]):
                    Specifies the alignment of data points in individual time
                    series as well as how to combine the retrieved time series
                    together (such as when aggregating multiple streams on each
                    resource to a single stream for each resource or when
                    aggregating streams across all members of a group of
                    resources). Multiple aggregations are applied in the order
                    specified.

                    This field is similar to the one in the ```ListTimeSeries``
                    request <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list>`__.
                    It is advisable to use the ``ListTimeSeries`` method when
                    debugging this field.
                denominator_filter (str):
                    A
                    `filter <https://cloud.google.com/monitoring/api/v3/filters>`__
                    that identifies a time series that should be used as the
                    denominator of a ratio that will be compared with the
                    threshold. If a ``denominator_filter`` is specified, the
                    time series specified by the ``filter`` field will be used
                    as the numerator.

                    The filter must specify the metric type and optionally may
                    contain restrictions on resource type, resource labels, and
                    metric labels. This field may not exceed 2048 Unicode
                    characters in length.
                denominator_aggregations (Sequence[google.cloud.monitoring_v3.types.Aggregation]):
                    Specifies the alignment of data points in individual time
                    series selected by ``denominatorFilter`` as well as how to
                    combine the retrieved time series together (such as when
                    aggregating multiple streams on each resource to a single
                    stream for each resource or when aggregating streams across
                    all members of a group of resources).

                    When computing ratios, the ``aggregations`` and
                    ``denominator_aggregations`` fields must use the same
                    alignment period and produce time series that have the same
                    periodicity and labels.
                comparison (google.cloud.monitoring_v3.types.ComparisonType):
                    The comparison to apply between the time series (indicated
                    by ``filter`` and ``aggregation``) and the threshold
                    (indicated by ``threshold_value``). The comparison is
                    applied on each time series, with the time series on the
                    left-hand side and the threshold on the right-hand side.

                    Only ``COMPARISON_LT`` and ``COMPARISON_GT`` are supported
                    currently.
                threshold_value (float):
                    A value against which to compare the time
                    series.
                duration (google.protobuf.duration_pb2.Duration):
                    The amount of time that a time series must violate the
                    threshold to be considered failing. Currently, only values
                    that are a multiple of a minute--e.g., 0, 60, 120, or 300
                    seconds--are supported. If an invalid value is given, an
                    error will be returned. When choosing a duration, it is
                    useful to keep in mind the frequency of the underlying time
                    series data (which may also be affected by any alignments
                    specified in the ``aggregations`` field); a good duration is
                    long enough so that a single outlier does not generate
                    spurious alerts, but short enough that unhealthy states are
                    detected and alerted on quickly.
                trigger (google.cloud.monitoring_v3.types.AlertPolicy.Condition.Trigger):
                    The number/percent of time series for which the comparison
                    must hold in order for the condition to trigger. If
                    unspecified, then the condition will trigger if the
                    comparison is true for any of the time series that have been
                    identified by ``filter`` and ``aggregations``, or by the
                    ratio, if ``denominator_filter`` and
                    ``denominator_aggregations`` are specified.
            """

            filter = proto.Field(proto.STRING, number=2,)
            aggregations = proto.RepeatedField(
                proto.MESSAGE, number=8, message=common.Aggregation,
            )
            denominator_filter = proto.Field(proto.STRING, number=9,)
            denominator_aggregations = proto.RepeatedField(
                proto.MESSAGE, number=10, message=common.Aggregation,
            )
            comparison = proto.Field(proto.ENUM, number=4, enum=common.ComparisonType,)
            threshold_value = proto.Field(proto.DOUBLE, number=5,)
            duration = proto.Field(
                proto.MESSAGE, number=6, message=duration_pb2.Duration,
            )
            trigger = proto.Field(
                proto.MESSAGE, number=7, message="AlertPolicy.Condition.Trigger",
            )

        class MetricAbsence(proto.Message):
            r"""A condition type that checks that monitored resources are reporting
            data. The configuration defines a metric and a set of monitored
            resources. The predicate is considered in violation when a time
            series for the specified metric of a monitored resource does not
            include any data in the specified ``duration``.

            Attributes:
                filter (str):
                    Required. A
                    `filter <https://cloud.google.com/monitoring/api/v3/filters>`__
                    that identifies which time series should be compared with
                    the threshold.

                    The filter is similar to the one that is specified in the
                    ```ListTimeSeries``
                    request <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list>`__
                    (that call is useful to verify the time series that will be
                    retrieved / processed). The filter must specify the metric
                    type and the resource type. Optionally, it can specify
                    resource labels and metric labels. This field must not
                    exceed 2048 Unicode characters in length.
                aggregations (Sequence[google.cloud.monitoring_v3.types.Aggregation]):
                    Specifies the alignment of data points in individual time
                    series as well as how to combine the retrieved time series
                    together (such as when aggregating multiple streams on each
                    resource to a single stream for each resource or when
                    aggregating streams across all members of a group of
                    resources). Multiple aggregations are applied in the order
                    specified.

                    This field is similar to the one in the ```ListTimeSeries``
                    request <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list>`__.
                    It is advisable to use the ``ListTimeSeries`` method when
                    debugging this field.
                duration (google.protobuf.duration_pb2.Duration):
                    The amount of time that a time series must fail to report
                    new data to be considered failing. The minimum value of this
                    field is 120 seconds. Larger values that are a multiple of a
                    minute--for example, 240 or 300 seconds--are supported. If
                    an invalid value is given, an error will be returned. The
                    ``Duration.nanos`` field is ignored.
                trigger (google.cloud.monitoring_v3.types.AlertPolicy.Condition.Trigger):
                    The number/percent of time series for which the comparison
                    must hold in order for the condition to trigger. If
                    unspecified, then the condition will trigger if the
                    comparison is true for any of the time series that have been
                    identified by ``filter`` and ``aggregations``.
            """

            filter = proto.Field(proto.STRING, number=1,)
            aggregations = proto.RepeatedField(
                proto.MESSAGE, number=5, message=common.Aggregation,
            )
            duration = proto.Field(
                proto.MESSAGE, number=2, message=duration_pb2.Duration,
            )
            trigger = proto.Field(
                proto.MESSAGE, number=3, message="AlertPolicy.Condition.Trigger",
            )

        class LogMatch(proto.Message):
            r"""A condition type that checks whether a log message in the `scoping
            project <https://cloud.google.com/monitoring/api/v3#project_name>`__
            satisfies the given filter. Logs from other projects in the metrics
            scope are not evaluated.

            Attributes:
                filter (str):
                    Required. A logs-based filter. See `Advanced Logs
                    Queries <https://cloud.google.com/logging/docs/view/advanced-queries>`__
                    for how this filter should be constructed.
                label_extractors (Sequence[google.cloud.monitoring_v3.types.AlertPolicy.Condition.LogMatch.LabelExtractorsEntry]):
                    Optional. A map from a label key to an extractor expression,
                    which is used to extract the value for this label key. Each
                    entry in this map is a specification for how data should be
                    extracted from log entries that match ``filter``. Each
                    combination of extracted values is treated as a separate
                    rule for the purposes of triggering notifications. Label
                    keys and corresponding values can be used in notifications
                    generated by this condition.

                    Please see `the documentation on logs-based metric
                    ``valueExtractor``\ s <https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics#LogMetric.FIELDS.value_extractor>`__
                    for syntax and examples.
            """

            filter = proto.Field(proto.STRING, number=1,)
            label_extractors = proto.MapField(proto.STRING, proto.STRING, number=2,)

        class MonitoringQueryLanguageCondition(proto.Message):
            r"""A condition type that allows alert policies to be defined using
            `Monitoring Query
            Language <https://cloud.google.com/monitoring/mql>`__.

            Attributes:
                query (str):
                    `Monitoring Query
                    Language <https://cloud.google.com/monitoring/mql>`__ query
                    that outputs a boolean stream.
                duration (google.protobuf.duration_pb2.Duration):
                    The amount of time that a time series must violate the
                    threshold to be considered failing. Currently, only values
                    that are a multiple of a minute--e.g., 0, 60, 120, or 300
                    seconds--are supported. If an invalid value is given, an
                    error will be returned. When choosing a duration, it is
                    useful to keep in mind the frequency of the underlying time
                    series data (which may also be affected by any alignments
                    specified in the ``aggregations`` field); a good duration is
                    long enough so that a single outlier does not generate
                    spurious alerts, but short enough that unhealthy states are
                    detected and alerted on quickly.
                trigger (google.cloud.monitoring_v3.types.AlertPolicy.Condition.Trigger):
                    The number/percent of time series for which the comparison
                    must hold in order for the condition to trigger. If
                    unspecified, then the condition will trigger if the
                    comparison is true for any of the time series that have been
                    identified by ``filter`` and ``aggregations``, or by the
                    ratio, if ``denominator_filter`` and
                    ``denominator_aggregations`` are specified.
            """

            query = proto.Field(proto.STRING, number=1,)
            duration = proto.Field(
                proto.MESSAGE, number=2, message=duration_pb2.Duration,
            )
            trigger = proto.Field(
                proto.MESSAGE, number=3, message="AlertPolicy.Condition.Trigger",
            )

        name = proto.Field(proto.STRING, number=12,)
        display_name = proto.Field(proto.STRING, number=6,)
        condition_threshold = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="condition",
            message="AlertPolicy.Condition.MetricThreshold",
        )
        condition_absent = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="condition",
            message="AlertPolicy.Condition.MetricAbsence",
        )
        condition_matched_log = proto.Field(
            proto.MESSAGE,
            number=20,
            oneof="condition",
            message="AlertPolicy.Condition.LogMatch",
        )
        condition_monitoring_query_language = proto.Field(
            proto.MESSAGE,
            number=19,
            oneof="condition",
            message="AlertPolicy.Condition.MonitoringQueryLanguageCondition",
        )

    class AlertStrategy(proto.Message):
        r"""Control over how the notification channels in
        ``notification_channels`` are notified when this alert fires.

        Attributes:
            notification_rate_limit (google.cloud.monitoring_v3.types.AlertPolicy.AlertStrategy.NotificationRateLimit):
                Required for alert policies with a ``LogMatch`` condition.

                This limit is not implemented for alert policies that are
                not log-based.
            auto_close (google.protobuf.duration_pb2.Duration):
                If an alert policy that was active has no
                data for this long, any open incidents will
                close
        """

        class NotificationRateLimit(proto.Message):
            r"""Control over the rate of notifications sent to this alert
            policy's notification channels.

            Attributes:
                period (google.protobuf.duration_pb2.Duration):
                    Not more than one notification per ``period``.
            """

            period = proto.Field(
                proto.MESSAGE, number=1, message=duration_pb2.Duration,
            )

        notification_rate_limit = proto.Field(
            proto.MESSAGE,
            number=1,
            message="AlertPolicy.AlertStrategy.NotificationRateLimit",
        )
        auto_close = proto.Field(
            proto.MESSAGE, number=3, message=duration_pb2.Duration,
        )

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    documentation = proto.Field(proto.MESSAGE, number=13, message=Documentation,)
    user_labels = proto.MapField(proto.STRING, proto.STRING, number=16,)
    conditions = proto.RepeatedField(proto.MESSAGE, number=12, message=Condition,)
    combiner = proto.Field(proto.ENUM, number=6, enum=ConditionCombinerType,)
    enabled = proto.Field(proto.MESSAGE, number=17, message=wrappers_pb2.BoolValue,)
    validity = proto.Field(proto.MESSAGE, number=18, message=status_pb2.Status,)
    notification_channels = proto.RepeatedField(proto.STRING, number=14,)
    creation_record = proto.Field(
        proto.MESSAGE, number=10, message=gm_mutation_record.MutationRecord,
    )
    mutation_record = proto.Field(
        proto.MESSAGE, number=11, message=gm_mutation_record.MutationRecord,
    )
    alert_strategy = proto.Field(proto.MESSAGE, number=21, message=AlertStrategy,)


__all__ = tuple(sorted(__protobuf__.manifest))
