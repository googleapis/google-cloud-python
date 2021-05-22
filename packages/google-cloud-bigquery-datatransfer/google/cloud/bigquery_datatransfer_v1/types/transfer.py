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

from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.datatransfer.v1",
    manifest={
        "TransferType",
        "TransferState",
        "EmailPreferences",
        "ScheduleOptions",
        "TransferConfig",
        "TransferRun",
        "TransferMessage",
    },
)


class TransferType(proto.Enum):
    r"""DEPRECATED. Represents data transfer type."""
    _pb_options = {"deprecated": True}
    TRANSFER_TYPE_UNSPECIFIED = 0
    BATCH = 1
    STREAMING = 2


class TransferState(proto.Enum):
    r"""Represents data transfer run state."""
    TRANSFER_STATE_UNSPECIFIED = 0
    PENDING = 2
    RUNNING = 3
    SUCCEEDED = 4
    FAILED = 5
    CANCELLED = 6


class EmailPreferences(proto.Message):
    r"""Represents preferences for sending email notifications for
    transfer run events.

    Attributes:
        enable_failure_email (bool):
            If true, email notifications will be sent on
            transfer run failures.
    """

    enable_failure_email = proto.Field(proto.BOOL, number=1,)


class ScheduleOptions(proto.Message):
    r"""Options customizing the data transfer schedule.
    Attributes:
        disable_auto_scheduling (bool):
            If true, automatic scheduling of data
            transfer runs for this configuration will be
            disabled. The runs can be started on ad-hoc
            basis using StartManualTransferRuns API. When
            automatic scheduling is disabled, the
            TransferConfig.schedule field will be ignored.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Specifies time to start scheduling transfer
            runs. The first run will be scheduled at or
            after the start time according to a recurrence
            pattern defined in the schedule string. The
            start time can be changed at any moment. The
            time when a data transfer can be trigerred
            manually is not limited by this option.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Defines time to stop scheduling transfer
            runs. A transfer run cannot be scheduled at or
            after the end time. The end time can be changed
            at any moment. The time when a data transfer can
            be trigerred manually is not limited by this
            option.
    """

    disable_auto_scheduling = proto.Field(proto.BOOL, number=3,)
    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)


class TransferConfig(proto.Message):
    r"""Represents a data transfer configuration. A transfer configuration
    contains all metadata needed to perform a data transfer. For
    example, ``destination_dataset_id`` specifies where data should be
    stored. When a new transfer configuration is created, the specified
    ``destination_dataset_id`` is created when needed and shared with
    the appropriate data source service account.

    Attributes:
        name (str):
            The resource name of the transfer config. Transfer config
            names have the form of
            ``projects/{project_id}/locations/{region}/transferConfigs/{config_id}``.
            The name is automatically generated based on the config_id
            specified in CreateTransferConfigRequest along with
            project_id and region. If config_id is not provided, usually
            a uuid, even though it is not guaranteed or required, will
            be generated for config_id.
        destination_dataset_id (str):
            The BigQuery target dataset id.
        display_name (str):
            User specified display name for the data
            transfer.
        data_source_id (str):
            Data source id. Cannot be changed once data
            transfer is created.
        params (google.protobuf.struct_pb2.Struct):
            Data transfer specific parameters.
        schedule (str):
            Data transfer schedule. If the data source does not support
            a custom schedule, this should be empty. If it is empty, the
            default value for the data source will be used. The
            specified times are in UTC. Examples of valid format:
            ``1st,3rd monday of month 15:30``,
            ``every wed,fri of jan,jun 13:15``, and
            ``first sunday of quarter 00:00``. See more explanation
            about the format here:
            https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format
            NOTE: the granularity should be at least 8 hours, or less
            frequent.
        schedule_options (google.cloud.bigquery_datatransfer_v1.types.ScheduleOptions):
            Options customizing the data transfer
            schedule.
        data_refresh_window_days (int):
            The number of days to look back to automatically refresh the
            data. For example, if ``data_refresh_window_days = 10``,
            then every day BigQuery reingests data for [today-10,
            today-1], rather than ingesting data for just [today-1].
            Only valid if the data source supports the feature. Set the
            value to 0 to use the default value.
        disabled (bool):
            Is this config disabled. When set to true, no
            runs are scheduled for a given transfer.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Data transfer modification time.
            Ignored by server on input.
        next_run_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Next time when data transfer
            will run.
        state (google.cloud.bigquery_datatransfer_v1.types.TransferState):
            Output only. State of the most recently
            updated transfer run.
        user_id (int):
            Deprecated. Unique ID of the user on whose
            behalf transfer is done.
        dataset_region (str):
            Output only. Region in which BigQuery dataset
            is located.
        notification_pubsub_topic (str):
            Pub/Sub topic where notifications will be
            sent after transfer runs associated with this
            transfer config finish.
        email_preferences (google.cloud.bigquery_datatransfer_v1.types.EmailPreferences):
            Email notifications will be sent according to
            these preferences to the email address of the
            user who owns this transfer config.
    """

    name = proto.Field(proto.STRING, number=1,)
    destination_dataset_id = proto.Field(proto.STRING, number=2, oneof="destination",)
    display_name = proto.Field(proto.STRING, number=3,)
    data_source_id = proto.Field(proto.STRING, number=5,)
    params = proto.Field(proto.MESSAGE, number=9, message=struct_pb2.Struct,)
    schedule = proto.Field(proto.STRING, number=7,)
    schedule_options = proto.Field(proto.MESSAGE, number=24, message="ScheduleOptions",)
    data_refresh_window_days = proto.Field(proto.INT32, number=12,)
    disabled = proto.Field(proto.BOOL, number=13,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    next_run_time = proto.Field(
        proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(proto.ENUM, number=10, enum="TransferState",)
    user_id = proto.Field(proto.INT64, number=11,)
    dataset_region = proto.Field(proto.STRING, number=14,)
    notification_pubsub_topic = proto.Field(proto.STRING, number=15,)
    email_preferences = proto.Field(
        proto.MESSAGE, number=18, message="EmailPreferences",
    )


class TransferRun(proto.Message):
    r"""Represents a data transfer run.
    Attributes:
        name (str):
            The resource name of the transfer run. Transfer run names
            have the form
            ``projects/{project_id}/locations/{location}/transferConfigs/{config_id}/runs/{run_id}``.
            The name is ignored when creating a transfer run.
        schedule_time (google.protobuf.timestamp_pb2.Timestamp):
            Minimum time after which a transfer run can
            be started.
        run_time (google.protobuf.timestamp_pb2.Timestamp):
            For batch transfer runs, specifies the date
            and time of the data should be ingested.
        error_status (google.rpc.status_pb2.Status):
            Status of the transfer run.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when transfer run was
            started. Parameter ignored by server for input
            requests.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when transfer run ended.
            Parameter ignored by server for input requests.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last time the data transfer run
            state was updated.
        params (google.protobuf.struct_pb2.Struct):
            Output only. Data transfer specific
            parameters.
        destination_dataset_id (str):
            Output only. The BigQuery target dataset id.
        data_source_id (str):
            Output only. Data source id.
        state (google.cloud.bigquery_datatransfer_v1.types.TransferState):
            Data transfer run state. Ignored for input
            requests.
        user_id (int):
            Deprecated. Unique ID of the user on whose
            behalf transfer is done.
        schedule (str):
            Output only. Describes the schedule of this transfer run if
            it was created as part of a regular schedule. For batch
            transfer runs that are scheduled manually, this is empty.
            NOTE: the system might choose to delay the schedule
            depending on the current load, so ``schedule_time`` doesn't
            always match this.
        notification_pubsub_topic (str):
            Output only. Pub/Sub topic where a
            notification will be sent after this transfer
            run finishes
        email_preferences (google.cloud.bigquery_datatransfer_v1.types.EmailPreferences):
            Output only. Email notifications will be sent
            according to these preferences to the email
            address of the user who owns the transfer config
            this run was derived from.
    """

    name = proto.Field(proto.STRING, number=1,)
    schedule_time = proto.Field(
        proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,
    )
    run_time = proto.Field(proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,)
    error_status = proto.Field(proto.MESSAGE, number=21, message=status_pb2.Status,)
    start_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    params = proto.Field(proto.MESSAGE, number=9, message=struct_pb2.Struct,)
    destination_dataset_id = proto.Field(proto.STRING, number=2, oneof="destination",)
    data_source_id = proto.Field(proto.STRING, number=7,)
    state = proto.Field(proto.ENUM, number=8, enum="TransferState",)
    user_id = proto.Field(proto.INT64, number=11,)
    schedule = proto.Field(proto.STRING, number=12,)
    notification_pubsub_topic = proto.Field(proto.STRING, number=23,)
    email_preferences = proto.Field(
        proto.MESSAGE, number=25, message="EmailPreferences",
    )


class TransferMessage(proto.Message):
    r"""Represents a user facing message for a particular data
    transfer run.

    Attributes:
        message_time (google.protobuf.timestamp_pb2.Timestamp):
            Time when message was logged.
        severity (google.cloud.bigquery_datatransfer_v1.types.TransferMessage.MessageSeverity):
            Message severity.
        message_text (str):
            Message text.
    """

    class MessageSeverity(proto.Enum):
        r"""Represents data transfer user facing message severity."""
        MESSAGE_SEVERITY_UNSPECIFIED = 0
        INFO = 1
        WARNING = 2
        ERROR = 3

    message_time = proto.Field(
        proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,
    )
    severity = proto.Field(proto.ENUM, number=2, enum=MessageSeverity,)
    message_text = proto.Field(proto.STRING, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
