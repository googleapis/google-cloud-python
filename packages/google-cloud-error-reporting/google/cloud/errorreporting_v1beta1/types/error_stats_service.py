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

from google.cloud.errorreporting_v1beta1.types import common
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.devtools.clouderrorreporting.v1beta1",
    manifest={
        "TimedCountAlignment",
        "ErrorGroupOrder",
        "ListGroupStatsRequest",
        "ListGroupStatsResponse",
        "ErrorGroupStats",
        "TimedCount",
        "ListEventsRequest",
        "ListEventsResponse",
        "QueryTimeRange",
        "ServiceContextFilter",
        "DeleteEventsRequest",
        "DeleteEventsResponse",
    },
)


class TimedCountAlignment(proto.Enum):
    r"""Specifies how the time periods of error group counts are
    aligned.
    """
    ERROR_COUNT_ALIGNMENT_UNSPECIFIED = 0
    ALIGNMENT_EQUAL_ROUNDED = 1
    ALIGNMENT_EQUAL_AT_END = 2


class ErrorGroupOrder(proto.Enum):
    r"""A sorting order of error groups."""
    GROUP_ORDER_UNSPECIFIED = 0
    COUNT_DESC = 1
    LAST_SEEN_DESC = 2
    CREATED_DESC = 3
    AFFECTED_USERS_DESC = 4


class ListGroupStatsRequest(proto.Message):
    r"""Specifies a set of ``ErrorGroupStats`` to return.
    Attributes:
        project_name (str):
            Required. The resource name of the Google Cloud Platform
            project. Written as ``projects/{projectID}`` or
            ``projects/{projectNumber}``, where ``{projectID}`` and
            ``{projectNumber}`` can be found in the `Google Cloud
            Console <https://support.google.com/cloud/answer/6158840>`__.

            Examples: ``projects/my-project-123``, ``projects/5551234``.
        group_id (Sequence[str]):
            Optional. List all
            <code>ErrorGroupStats</code> with these IDs.
        service_filter (google.cloud.errorreporting_v1beta1.types.ServiceContextFilter):
            Optional. List only
            <code>ErrorGroupStats</code> which belong to a
            service context that matches the filter. Data
            for all service contexts is returned if this
            field is not specified.
        time_range (google.cloud.errorreporting_v1beta1.types.QueryTimeRange):
            Optional. List data for the given time range. If not set, a
            default time range is used. The field time_range_begin in
            the response will specify the beginning of this time range.
            Only ErrorGroupStats with a non-zero count in the given time
            range are returned, unless the request contains an explicit
            group_id list. If a group_id list is given, also
            ErrorGroupStats with zero occurrences are returned.
        timed_count_duration (google.protobuf.duration_pb2.Duration):
            Optional. The preferred duration for a single returned
            ``TimedCount``. If not set, no timed counts are returned.
        alignment (google.cloud.errorreporting_v1beta1.types.TimedCountAlignment):
            Optional. The alignment of the timed counts to be returned.
            Default is ``ALIGNMENT_EQUAL_AT_END``.
        alignment_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Time where the timed counts shall
            be aligned if rounded alignment is chosen.
            Default is 00:00 UTC.
        order (google.cloud.errorreporting_v1beta1.types.ErrorGroupOrder):
            Optional. The sort order in which the results are returned.
            Default is ``COUNT_DESC``.
        page_size (int):
            Optional. The maximum number of results to
            return per response. Default is 20.
        page_token (str):
            Optional. A ``next_page_token`` provided by a previous
            response. To view additional results, pass this token along
            with the identical query parameters as the first request.
    """

    project_name = proto.Field(proto.STRING, number=1,)
    group_id = proto.RepeatedField(proto.STRING, number=2,)
    service_filter = proto.Field(
        proto.MESSAGE, number=3, message="ServiceContextFilter",
    )
    time_range = proto.Field(proto.MESSAGE, number=5, message="QueryTimeRange",)
    timed_count_duration = proto.Field(
        proto.MESSAGE, number=6, message=duration_pb2.Duration,
    )
    alignment = proto.Field(proto.ENUM, number=7, enum="TimedCountAlignment",)
    alignment_time = proto.Field(
        proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,
    )
    order = proto.Field(proto.ENUM, number=9, enum="ErrorGroupOrder",)
    page_size = proto.Field(proto.INT32, number=11,)
    page_token = proto.Field(proto.STRING, number=12,)


class ListGroupStatsResponse(proto.Message):
    r"""Contains a set of requested error group stats.
    Attributes:
        error_group_stats (Sequence[google.cloud.errorreporting_v1beta1.types.ErrorGroupStats]):
            The error group stats which match the given
            request.
        next_page_token (str):
            If non-empty, more results are available.
            Pass this token, along with the same query
            parameters as the first request, to view the
            next page of results.
        time_range_begin (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp specifies the start time to
            which the request was restricted. The start time
            is set based on the requested time range. It may
            be adjusted to a later time if a project has
            exceeded the storage quota and older data has
            been deleted.
    """

    @property
    def raw_page(self):
        return self

    error_group_stats = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ErrorGroupStats",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    time_range_begin = proto.Field(
        proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,
    )


class ErrorGroupStats(proto.Message):
    r"""Data extracted for a specific group based on certain filter
    criteria, such as a given time period and/or service filter.

    Attributes:
        group (google.cloud.errorreporting_v1beta1.types.ErrorGroup):
            Group data that is independent of the filter
            criteria.
        count (int):
            Approximate total number of events in the
            given group that match the filter criteria.
        affected_users_count (int):
            Approximate number of affected users in the given group that
            match the filter criteria. Users are distinguished by data
            in the ``ErrorContext`` of the individual error events, such
            as their login name or their remote IP address in case of
            HTTP requests. The number of affected users can be zero even
            if the number of errors is non-zero if no data was provided
            from which the affected user could be deduced. Users are
            counted based on data in the request context that was
            provided in the error report. If more users are implicitly
            affected, such as due to a crash of the whole service, this
            is not reflected here.
        timed_counts (Sequence[google.cloud.errorreporting_v1beta1.types.TimedCount]):
            Approximate number of occurrences over time.
            Timed counts returned by ListGroups are
            guaranteed to be:
            - Inside the requested time interval
            - Non-overlapping, and
            - Ordered by ascending time.
        first_seen_time (google.protobuf.timestamp_pb2.Timestamp):
            Approximate first occurrence that was ever seen for this
            group and which matches the given filter criteria, ignoring
            the time_range that was specified in the request.
        last_seen_time (google.protobuf.timestamp_pb2.Timestamp):
            Approximate last occurrence that was ever seen for this
            group and which matches the given filter criteria, ignoring
            the time_range that was specified in the request.
        affected_services (Sequence[google.cloud.errorreporting_v1beta1.types.ServiceContext]):
            Service contexts with a non-zero error count for the given
            filter criteria. This list can be truncated if multiple
            services are affected. Refer to ``num_affected_services``
            for the total count.
        num_affected_services (int):
            The total number of services with a non-zero
            error count for the given filter criteria.
        representative (google.cloud.errorreporting_v1beta1.types.ErrorEvent):
            An arbitrary event that is chosen as
            representative for the whole group. The
            representative event is intended to be used as a
            quick preview for the whole group. Events in the
            group are usually sufficiently similar to each
            other such that showing an arbitrary
            representative provides insight into the
            characteristics of the group as a whole.
    """

    group = proto.Field(proto.MESSAGE, number=1, message=common.ErrorGroup,)
    count = proto.Field(proto.INT64, number=2,)
    affected_users_count = proto.Field(proto.INT64, number=3,)
    timed_counts = proto.RepeatedField(proto.MESSAGE, number=4, message="TimedCount",)
    first_seen_time = proto.Field(
        proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,
    )
    last_seen_time = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )
    affected_services = proto.RepeatedField(
        proto.MESSAGE, number=7, message=common.ServiceContext,
    )
    num_affected_services = proto.Field(proto.INT32, number=8,)
    representative = proto.Field(proto.MESSAGE, number=9, message=common.ErrorEvent,)


class TimedCount(proto.Message):
    r"""The number of errors in a given time period.
    All numbers are approximate since the error events are sampled
    before counting them.

    Attributes:
        count (int):
            Approximate number of occurrences in the
            given time period.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Start of the time period to which ``count`` refers
            (included).
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            End of the time period to which ``count`` refers (excluded).
    """

    count = proto.Field(proto.INT64, number=1,)
    start_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)


class ListEventsRequest(proto.Message):
    r"""Specifies a set of error events to return.
    Attributes:
        project_name (str):
            Required. The resource name of the Google Cloud Platform
            project. Written as ``projects/{projectID}``, where
            ``{projectID}`` is the `Google Cloud Platform project
            ID <https://support.google.com/cloud/answer/6158840>`__.

            Example: ``projects/my-project-123``.
        group_id (str):
            Required. The group for which events shall be
            returned.
        service_filter (google.cloud.errorreporting_v1beta1.types.ServiceContextFilter):
            Optional. List only ErrorGroups which belong
            to a service context that matches the filter.
            Data for all service contexts is returned if
            this field is not specified.
        time_range (google.cloud.errorreporting_v1beta1.types.QueryTimeRange):
            Optional. List only data for the given time range. If not
            set a default time range is used. The field time_range_begin
            in the response will specify the beginning of this time
            range.
        page_size (int):
            Optional. The maximum number of results to
            return per response.
        page_token (str):
            Optional. A ``next_page_token`` provided by a previous
            response.
    """

    project_name = proto.Field(proto.STRING, number=1,)
    group_id = proto.Field(proto.STRING, number=2,)
    service_filter = proto.Field(
        proto.MESSAGE, number=3, message="ServiceContextFilter",
    )
    time_range = proto.Field(proto.MESSAGE, number=4, message="QueryTimeRange",)
    page_size = proto.Field(proto.INT32, number=6,)
    page_token = proto.Field(proto.STRING, number=7,)


class ListEventsResponse(proto.Message):
    r"""Contains a set of requested error events.
    Attributes:
        error_events (Sequence[google.cloud.errorreporting_v1beta1.types.ErrorEvent]):
            The error events which match the given
            request.
        next_page_token (str):
            If non-empty, more results are available.
            Pass this token, along with the same query
            parameters as the first request, to view the
            next page of results.
        time_range_begin (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp specifies the start time to
            which the request was restricted.
    """

    @property
    def raw_page(self):
        return self

    error_events = proto.RepeatedField(
        proto.MESSAGE, number=1, message=common.ErrorEvent,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    time_range_begin = proto.Field(
        proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,
    )


class QueryTimeRange(proto.Message):
    r"""Requests might be rejected or the resulting timed count
    durations might be adjusted for lower durations.

    Attributes:
        period (google.cloud.errorreporting_v1beta1.types.QueryTimeRange.Period):
            Restricts the query to the specified time
            range.
    """

    class Period(proto.Enum):
        r"""The supported time ranges."""
        PERIOD_UNSPECIFIED = 0
        PERIOD_1_HOUR = 1
        PERIOD_6_HOURS = 2
        PERIOD_1_DAY = 3
        PERIOD_1_WEEK = 4
        PERIOD_30_DAYS = 5

    period = proto.Field(proto.ENUM, number=1, enum=Period,)


class ServiceContextFilter(proto.Message):
    r"""Specifies criteria for filtering a subset of service contexts. The
    fields in the filter correspond to the fields in ``ServiceContext``.
    Only exact, case-sensitive matches are supported. If a field is
    unset or empty, it matches arbitrary values.

    Attributes:
        service (str):
            Optional. The exact value to match against
            ```ServiceContext.service`` </error-reporting/reference/rest/v1beta1/ServiceContext#FIELDS.service>`__.
        version (str):
            Optional. The exact value to match against
            ```ServiceContext.version`` </error-reporting/reference/rest/v1beta1/ServiceContext#FIELDS.version>`__.
        resource_type (str):
            Optional. The exact value to match against
            ```ServiceContext.resource_type`` </error-reporting/reference/rest/v1beta1/ServiceContext#FIELDS.resource_type>`__.
    """

    service = proto.Field(proto.STRING, number=2,)
    version = proto.Field(proto.STRING, number=3,)
    resource_type = proto.Field(proto.STRING, number=4,)


class DeleteEventsRequest(proto.Message):
    r"""Deletes all events in the project.
    Attributes:
        project_name (str):
            Required. The resource name of the Google Cloud Platform
            project. Written as ``projects/{projectID}``, where
            ``{projectID}`` is the `Google Cloud Platform project
            ID <https://support.google.com/cloud/answer/6158840>`__.

            Example: ``projects/my-project-123``.
    """

    project_name = proto.Field(proto.STRING, number=1,)


class DeleteEventsResponse(proto.Message):
    r"""Response message for deleting error events.    """


__all__ = tuple(sorted(__protobuf__.manifest))
