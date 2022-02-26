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

from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.dataflow.v1beta3",
    manifest={
        "JobMessageImportance",
        "JobMessage",
        "StructuredMessage",
        "AutoscalingEvent",
        "ListJobMessagesRequest",
        "ListJobMessagesResponse",
    },
)


class JobMessageImportance(proto.Enum):
    r"""Indicates the importance of the message."""
    JOB_MESSAGE_IMPORTANCE_UNKNOWN = 0
    JOB_MESSAGE_DEBUG = 1
    JOB_MESSAGE_DETAILED = 2
    JOB_MESSAGE_BASIC = 5
    JOB_MESSAGE_WARNING = 3
    JOB_MESSAGE_ERROR = 4


class JobMessage(proto.Message):
    r"""A particular message pertaining to a Dataflow job.

    Attributes:
        id (str):
            Deprecated.
        time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp of the message.
        message_text (str):
            The text of the message.
        message_importance (google.cloud.dataflow_v1beta3.types.JobMessageImportance):
            Importance level of the message.
    """

    id = proto.Field(proto.STRING, number=1,)
    time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    message_text = proto.Field(proto.STRING, number=3,)
    message_importance = proto.Field(proto.ENUM, number=4, enum="JobMessageImportance",)


class StructuredMessage(proto.Message):
    r"""A rich message format, including a human readable string, a
    key for identifying the message, and structured data associated
    with the message for programmatic consumption.

    Attributes:
        message_text (str):
            Human-readable version of message.
        message_key (str):
            Identifier for this message type.  Used by
            external systems to internationalize or
            personalize message.
        parameters (Sequence[google.cloud.dataflow_v1beta3.types.StructuredMessage.Parameter]):
            The structured data associated with this
            message.
    """

    class Parameter(proto.Message):
        r"""Structured data associated with this message.

        Attributes:
            key (str):
                Key or name for this parameter.
            value (google.protobuf.struct_pb2.Value):
                Value for this parameter.
        """

        key = proto.Field(proto.STRING, number=1,)
        value = proto.Field(proto.MESSAGE, number=2, message=struct_pb2.Value,)

    message_text = proto.Field(proto.STRING, number=1,)
    message_key = proto.Field(proto.STRING, number=2,)
    parameters = proto.RepeatedField(proto.MESSAGE, number=3, message=Parameter,)


class AutoscalingEvent(proto.Message):
    r"""A structured message reporting an autoscaling decision made
    by the Dataflow service.

    Attributes:
        current_num_workers (int):
            The current number of workers the job has.
        target_num_workers (int):
            The target number of workers the worker pool
            wants to resize to use.
        event_type (google.cloud.dataflow_v1beta3.types.AutoscalingEvent.AutoscalingEventType):
            The type of autoscaling event to report.
        description (google.cloud.dataflow_v1beta3.types.StructuredMessage):
            A message describing why the system decided
            to adjust the current number of workers, why it
            failed, or why the system decided to not make
            any changes to the number of workers.
        time (google.protobuf.timestamp_pb2.Timestamp):
            The time this event was emitted to indicate a new target or
            current num_workers value.
        worker_pool (str):
            A short and friendly name for the worker pool
            this event refers to.
    """

    class AutoscalingEventType(proto.Enum):
        r"""Indicates the type of autoscaling event."""
        TYPE_UNKNOWN = 0
        TARGET_NUM_WORKERS_CHANGED = 1
        CURRENT_NUM_WORKERS_CHANGED = 2
        ACTUATION_FAILURE = 3
        NO_CHANGE = 4

    current_num_workers = proto.Field(proto.INT64, number=1,)
    target_num_workers = proto.Field(proto.INT64, number=2,)
    event_type = proto.Field(proto.ENUM, number=3, enum=AutoscalingEventType,)
    description = proto.Field(proto.MESSAGE, number=4, message="StructuredMessage",)
    time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    worker_pool = proto.Field(proto.STRING, number=7,)


class ListJobMessagesRequest(proto.Message):
    r"""Request to list job messages. Up to max_results messages will be
    returned in the time range specified starting with the oldest
    messages first. If no time range is specified the results with start
    with the oldest message.

    Attributes:
        project_id (str):
            A project id.
        job_id (str):
            The job to get messages about.
        minimum_importance (google.cloud.dataflow_v1beta3.types.JobMessageImportance):
            Filter to only get messages with importance
            >= level
        page_size (int):
            If specified, determines the maximum number
            of messages to return.  If unspecified, the
            service may choose an appropriate default, or
            may return an arbitrarily large number of
            results.
        page_token (str):
            If supplied, this should be the value of next_page_token
            returned by an earlier call. This will cause the next page
            of results to be returned.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            If specified, return only messages with timestamps >=
            start_time. The default is the job creation time (i.e.
            beginning of messages).
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Return only messages with timestamps < end_time. The default
            is now (i.e. return up to the latest messages available).
        location (str):
            The [regional endpoint]
            (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints)
            that contains the job specified by job_id.
    """

    project_id = proto.Field(proto.STRING, number=1,)
    job_id = proto.Field(proto.STRING, number=2,)
    minimum_importance = proto.Field(proto.ENUM, number=3, enum="JobMessageImportance",)
    page_size = proto.Field(proto.INT32, number=4,)
    page_token = proto.Field(proto.STRING, number=5,)
    start_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    location = proto.Field(proto.STRING, number=8,)


class ListJobMessagesResponse(proto.Message):
    r"""Response to a request to list job messages.

    Attributes:
        job_messages (Sequence[google.cloud.dataflow_v1beta3.types.JobMessage]):
            Messages in ascending timestamp order.
        next_page_token (str):
            The token to obtain the next page of results
            if there are more.
        autoscaling_events (Sequence[google.cloud.dataflow_v1beta3.types.AutoscalingEvent]):
            Autoscaling events in ascending timestamp
            order.
    """

    @property
    def raw_page(self):
        return self

    job_messages = proto.RepeatedField(proto.MESSAGE, number=1, message="JobMessage",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    autoscaling_events = proto.RepeatedField(
        proto.MESSAGE, number=3, message="AutoscalingEvent",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
