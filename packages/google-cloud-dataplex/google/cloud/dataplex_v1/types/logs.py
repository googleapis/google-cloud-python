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
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.dataplex.v1",
    manifest={
        "DiscoveryEvent",
        "JobEvent",
        "SessionEvent",
    },
)


class DiscoveryEvent(proto.Message):
    r"""The payload associated with Discovery data processing.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        message (str):
            The log message.
        lake_id (str):
            The id of the associated lake.
        zone_id (str):
            The id of the associated zone.
        asset_id (str):
            The id of the associated asset.
        data_location (str):
            The data location associated with the event.
        type_ (google.cloud.dataplex_v1.types.DiscoveryEvent.EventType):
            The type of the event being logged.
        config (google.cloud.dataplex_v1.types.DiscoveryEvent.ConfigDetails):
            Details about discovery configuration in
            effect.

            This field is a member of `oneof`_ ``details``.
        entity (google.cloud.dataplex_v1.types.DiscoveryEvent.EntityDetails):
            Details about the entity associated with the
            event.

            This field is a member of `oneof`_ ``details``.
        partition (google.cloud.dataplex_v1.types.DiscoveryEvent.PartitionDetails):
            Details about the partition associated with
            the event.

            This field is a member of `oneof`_ ``details``.
        action (google.cloud.dataplex_v1.types.DiscoveryEvent.ActionDetails):
            Details about the action associated with the
            event.

            This field is a member of `oneof`_ ``details``.
    """

    class EventType(proto.Enum):
        r"""The type of the event."""
        EVENT_TYPE_UNSPECIFIED = 0
        CONFIG = 1
        ENTITY_CREATED = 2
        ENTITY_UPDATED = 3
        ENTITY_DELETED = 4
        PARTITION_CREATED = 5
        PARTITION_UPDATED = 6
        PARTITION_DELETED = 7

    class EntityType(proto.Enum):
        r"""The type of the entity."""
        ENTITY_TYPE_UNSPECIFIED = 0
        TABLE = 1
        FILESET = 2

    class ConfigDetails(proto.Message):
        r"""Details about configuration events.

        Attributes:
            parameters (Mapping[str, str]):
                A list of discovery configuration parameters
                in effect. The keys are the field paths within
                DiscoverySpec. Eg. includePatterns,
                excludePatterns,
                csvOptions.disableTypeInference, etc.
        """

        parameters = proto.MapField(
            proto.STRING,
            proto.STRING,
            number=1,
        )

    class EntityDetails(proto.Message):
        r"""Details about the entity.

        Attributes:
            entity (str):
                The name of the entity resource.
                The name is the fully-qualified resource name.
            type_ (google.cloud.dataplex_v1.types.DiscoveryEvent.EntityType):
                The type of the entity resource.
        """

        entity = proto.Field(
            proto.STRING,
            number=1,
        )
        type_ = proto.Field(
            proto.ENUM,
            number=2,
            enum="DiscoveryEvent.EntityType",
        )

    class PartitionDetails(proto.Message):
        r"""Details about the partition.

        Attributes:
            partition (str):
                The name to the partition resource.
                The name is the fully-qualified resource name.
            entity (str):
                The name to the containing entity resource.
                The name is the fully-qualified resource name.
            type_ (google.cloud.dataplex_v1.types.DiscoveryEvent.EntityType):
                The type of the containing entity resource.
        """

        partition = proto.Field(
            proto.STRING,
            number=1,
        )
        entity = proto.Field(
            proto.STRING,
            number=2,
        )
        type_ = proto.Field(
            proto.ENUM,
            number=3,
            enum="DiscoveryEvent.EntityType",
        )

    class ActionDetails(proto.Message):
        r"""Details about the action.

        Attributes:
            type_ (str):
                The type of action.
                Eg. IncompatibleDataSchema, InvalidDataFormat
        """

        type_ = proto.Field(
            proto.STRING,
            number=1,
        )

    message = proto.Field(
        proto.STRING,
        number=1,
    )
    lake_id = proto.Field(
        proto.STRING,
        number=2,
    )
    zone_id = proto.Field(
        proto.STRING,
        number=3,
    )
    asset_id = proto.Field(
        proto.STRING,
        number=4,
    )
    data_location = proto.Field(
        proto.STRING,
        number=5,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=10,
        enum=EventType,
    )
    config = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="details",
        message=ConfigDetails,
    )
    entity = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="details",
        message=EntityDetails,
    )
    partition = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof="details",
        message=PartitionDetails,
    )
    action = proto.Field(
        proto.MESSAGE,
        number=23,
        oneof="details",
        message=ActionDetails,
    )


class JobEvent(proto.Message):
    r"""The payload associated with Job logs that contains events
    describing jobs that have run within a Lake.

    Attributes:
        message (str):
            The log message.
        job_id (str):
            The unique id identifying the job.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the job started running.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the job ended running.
        state (google.cloud.dataplex_v1.types.JobEvent.State):
            The job state on completion.
        retries (int):
            The number of retries.
        type_ (google.cloud.dataplex_v1.types.JobEvent.Type):
            The type of the job.
        service (google.cloud.dataplex_v1.types.JobEvent.Service):
            The service used to execute the job.
        service_job (str):
            The reference to the job within the service.
    """

    class Type(proto.Enum):
        r"""The type of the job."""
        TYPE_UNSPECIFIED = 0
        SPARK = 1
        NOTEBOOK = 2

    class State(proto.Enum):
        r"""The completion status of the job."""
        STATE_UNSPECIFIED = 0
        SUCCEEDED = 1
        FAILED = 2
        CANCELLED = 3
        ABORTED = 4

    class Service(proto.Enum):
        r"""The service used to execute the job."""
        SERVICE_UNSPECIFIED = 0
        DATAPROC = 1

    message = proto.Field(
        proto.STRING,
        number=1,
    )
    job_id = proto.Field(
        proto.STRING,
        number=2,
    )
    start_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    retries = proto.Field(
        proto.INT32,
        number=6,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=7,
        enum=Type,
    )
    service = proto.Field(
        proto.ENUM,
        number=8,
        enum=Service,
    )
    service_job = proto.Field(
        proto.STRING,
        number=9,
    )


class SessionEvent(proto.Message):
    r"""These messages contain information about sessions within an
    environment. The monitored resource is 'Environment'.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        message (str):
            The log message.
        user_id (str):
            The information about the user that created
            the session.
        session_id (str):
            Unique identifier for the session.
        type_ (google.cloud.dataplex_v1.types.SessionEvent.EventType):
            The type of the event.
        query (google.cloud.dataplex_v1.types.SessionEvent.QueryDetail):
            The execution details of the query.

            This field is a member of `oneof`_ ``detail``.
    """

    class EventType(proto.Enum):
        r"""The type of the event."""
        EVENT_TYPE_UNSPECIFIED = 0
        START = 1
        STOP = 2
        QUERY = 3

    class QueryDetail(proto.Message):
        r"""Execution details of the query.

        Attributes:
            query_id (str):
                The unique Query id identifying the query.
            query_text (str):
                The query text executed.
            engine (google.cloud.dataplex_v1.types.SessionEvent.QueryDetail.Engine):
                Query Execution engine.
            duration (google.protobuf.duration_pb2.Duration):
                Time taken for execution of the query.
            result_size_bytes (int):
                The size of results the query produced.
            data_processed_bytes (int):
                The data processed by the query.
        """

        class Engine(proto.Enum):
            r"""Query Execution engine."""
            ENGINE_UNSPECIFIED = 0
            SPARK_SQL = 1
            BIGQUERY = 2

        query_id = proto.Field(
            proto.STRING,
            number=1,
        )
        query_text = proto.Field(
            proto.STRING,
            number=2,
        )
        engine = proto.Field(
            proto.ENUM,
            number=3,
            enum="SessionEvent.QueryDetail.Engine",
        )
        duration = proto.Field(
            proto.MESSAGE,
            number=4,
            message=duration_pb2.Duration,
        )
        result_size_bytes = proto.Field(
            proto.INT64,
            number=5,
        )
        data_processed_bytes = proto.Field(
            proto.INT64,
            number=6,
        )

    message = proto.Field(
        proto.STRING,
        number=1,
    )
    user_id = proto.Field(
        proto.STRING,
        number=2,
    )
    session_id = proto.Field(
        proto.STRING,
        number=3,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=4,
        enum=EventType,
    )
    query = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="detail",
        message=QueryDetail,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
