# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.bigquery_storage_v1beta2.types import (
    arrow,
    avro,
    protobuf,
    stream,
    table,
)

__protobuf__ = proto.module(
    package="google.cloud.bigquery.storage.v1beta2",
    manifest={
        "CreateReadSessionRequest",
        "ReadRowsRequest",
        "ThrottleState",
        "StreamStats",
        "ReadRowsResponse",
        "SplitReadStreamRequest",
        "SplitReadStreamResponse",
        "CreateWriteStreamRequest",
        "AppendRowsRequest",
        "AppendRowsResponse",
        "GetWriteStreamRequest",
        "BatchCommitWriteStreamsRequest",
        "BatchCommitWriteStreamsResponse",
        "FinalizeWriteStreamRequest",
        "FinalizeWriteStreamResponse",
        "FlushRowsRequest",
        "FlushRowsResponse",
        "StorageError",
    },
)


class CreateReadSessionRequest(proto.Message):
    r"""Request message for ``CreateReadSession``.

    Attributes:
        parent (str):
            Required. The request project that owns the session, in the
            form of ``projects/{project_id}``.
        read_session (google.cloud.bigquery_storage_v1beta2.types.ReadSession):
            Required. Session to be created.
        max_stream_count (int):
            Max initial number of streams. If unset or
            zero, the server will provide a value of streams
            so as to produce reasonable throughput. Must be
            non-negative. The number of streams may be lower
            than the requested number, depending on the
            amount parallelism that is reasonable for the
            table. Error will be returned if the max count
            is greater than the current system max limit of
            1,000.

            Streams must be read starting from offset 0.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    read_session: stream.ReadSession = proto.Field(
        proto.MESSAGE,
        number=2,
        message=stream.ReadSession,
    )
    max_stream_count: int = proto.Field(
        proto.INT32,
        number=3,
    )


class ReadRowsRequest(proto.Message):
    r"""Request message for ``ReadRows``.

    Attributes:
        read_stream (str):
            Required. Stream to read rows from.
        offset (int):
            The offset requested must be less than the
            last row read from Read. Requesting a larger
            offset is undefined. If not specified, start
            reading from offset zero.
    """

    read_stream: str = proto.Field(
        proto.STRING,
        number=1,
    )
    offset: int = proto.Field(
        proto.INT64,
        number=2,
    )


class ThrottleState(proto.Message):
    r"""Information on if the current connection is being throttled.

    Attributes:
        throttle_percent (int):
            How much this connection is being throttled.
            Zero means no throttling, 100 means fully
            throttled.
    """

    throttle_percent: int = proto.Field(
        proto.INT32,
        number=1,
    )


class StreamStats(proto.Message):
    r"""Estimated stream statistics for a given Stream.

    Attributes:
        progress (google.cloud.bigquery_storage_v1beta2.types.StreamStats.Progress):
            Represents the progress of the current
            stream.
    """

    class Progress(proto.Message):
        r"""

        Attributes:
            at_response_start (float):
                The fraction of rows assigned to the stream that have been
                processed by the server so far, not including the rows in
                the current response message.

                This value, along with ``at_response_end``, can be used to
                interpolate the progress made as the rows in the message are
                being processed using the following formula:
                ``at_response_start + (at_response_end - at_response_start) * rows_processed_from_response / rows_in_response``.

                Note that if a filter is provided, the ``at_response_end``
                value of the previous response may not necessarily be equal
                to the ``at_response_start`` value of the current response.
            at_response_end (float):
                Similar to ``at_response_start``, except that this value
                includes the rows in the current response.
        """

        at_response_start: float = proto.Field(
            proto.DOUBLE,
            number=1,
        )
        at_response_end: float = proto.Field(
            proto.DOUBLE,
            number=2,
        )

    progress: Progress = proto.Field(
        proto.MESSAGE,
        number=2,
        message=Progress,
    )


class ReadRowsResponse(proto.Message):
    r"""Response from calling ``ReadRows`` may include row data, progress
    and throttling information.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        avro_rows (google.cloud.bigquery_storage_v1beta2.types.AvroRows):
            Serialized row data in AVRO format.

            This field is a member of `oneof`_ ``rows``.
        arrow_record_batch (google.cloud.bigquery_storage_v1beta2.types.ArrowRecordBatch):
            Serialized row data in Arrow RecordBatch
            format.

            This field is a member of `oneof`_ ``rows``.
        row_count (int):
            Number of serialized rows in the rows block.
        stats (google.cloud.bigquery_storage_v1beta2.types.StreamStats):
            Statistics for the stream.
        throttle_state (google.cloud.bigquery_storage_v1beta2.types.ThrottleState):
            Throttling state. If unset, the latest
            response still describes the current throttling
            status.
        avro_schema (google.cloud.bigquery_storage_v1beta2.types.AvroSchema):
            Output only. Avro schema.

            This field is a member of `oneof`_ ``schema``.
        arrow_schema (google.cloud.bigquery_storage_v1beta2.types.ArrowSchema):
            Output only. Arrow schema.

            This field is a member of `oneof`_ ``schema``.
    """

    avro_rows: avro.AvroRows = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="rows",
        message=avro.AvroRows,
    )
    arrow_record_batch: arrow.ArrowRecordBatch = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="rows",
        message=arrow.ArrowRecordBatch,
    )
    row_count: int = proto.Field(
        proto.INT64,
        number=6,
    )
    stats: "StreamStats" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="StreamStats",
    )
    throttle_state: "ThrottleState" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="ThrottleState",
    )
    avro_schema: avro.AvroSchema = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="schema",
        message=avro.AvroSchema,
    )
    arrow_schema: arrow.ArrowSchema = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="schema",
        message=arrow.ArrowSchema,
    )


class SplitReadStreamRequest(proto.Message):
    r"""Request message for ``SplitReadStream``.

    Attributes:
        name (str):
            Required. Name of the stream to split.
        fraction (float):
            A value in the range (0.0, 1.0) that
            specifies the fractional point at which the
            original stream should be split. The actual
            split point is evaluated on pre-filtered rows,
            so if a filter is provided, then there is no
            guarantee that the division of the rows between
            the new child streams will be proportional to
            this fractional value. Additionally, because the
            server-side unit for assigning data is
            collections of rows, this fraction will always
            map to a data storage boundary on the server
            side.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    fraction: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )


class SplitReadStreamResponse(proto.Message):
    r"""

    Attributes:
        primary_stream (google.cloud.bigquery_storage_v1beta2.types.ReadStream):
            Primary stream, which contains the beginning portion of
            \|original_stream|. An empty value indicates that the
            original stream can no longer be split.
        remainder_stream (google.cloud.bigquery_storage_v1beta2.types.ReadStream):
            Remainder stream, which contains the tail of
            \|original_stream|. An empty value indicates that the
            original stream can no longer be split.
    """

    primary_stream: stream.ReadStream = proto.Field(
        proto.MESSAGE,
        number=1,
        message=stream.ReadStream,
    )
    remainder_stream: stream.ReadStream = proto.Field(
        proto.MESSAGE,
        number=2,
        message=stream.ReadStream,
    )


class CreateWriteStreamRequest(proto.Message):
    r"""Request message for ``CreateWriteStream``.

    Attributes:
        parent (str):
            Required. Reference to the table to which the stream
            belongs, in the format of
            ``projects/{project}/datasets/{dataset}/tables/{table}``.
        write_stream (google.cloud.bigquery_storage_v1beta2.types.WriteStream):
            Required. Stream to be created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    write_stream: stream.WriteStream = proto.Field(
        proto.MESSAGE,
        number=2,
        message=stream.WriteStream,
    )


class AppendRowsRequest(proto.Message):
    r"""Request message for ``AppendRows``.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        write_stream (str):
            Required. The stream that is the target of the append
            operation. This value must be specified for the initial
            request. If subsequent requests specify the stream name, it
            must equal to the value provided in the first request. To
            write to the \_default stream, populate this field with a
            string in the format
            ``projects/{project}/datasets/{dataset}/tables/{table}/_default``.
        offset (google.protobuf.wrappers_pb2.Int64Value):
            If present, the write is only performed if the next append
            offset is same as the provided value. If not present, the
            write is performed at the current end of stream. Specifying
            a value for this field is not allowed when calling
            AppendRows for the '_default' stream.
        proto_rows (google.cloud.bigquery_storage_v1beta2.types.AppendRowsRequest.ProtoData):
            Rows in proto format.

            This field is a member of `oneof`_ ``rows``.
        trace_id (str):
            Id set by client to annotate its identity.
            Only initial request setting is respected.
    """

    class ProtoData(proto.Message):
        r"""Proto schema and data.

        Attributes:
            writer_schema (google.cloud.bigquery_storage_v1beta2.types.ProtoSchema):
                Proto schema used to serialize the data.
            rows (google.cloud.bigquery_storage_v1beta2.types.ProtoRows):
                Serialized row data in protobuf message
                format.
        """

        writer_schema: protobuf.ProtoSchema = proto.Field(
            proto.MESSAGE,
            number=1,
            message=protobuf.ProtoSchema,
        )
        rows: protobuf.ProtoRows = proto.Field(
            proto.MESSAGE,
            number=2,
            message=protobuf.ProtoRows,
        )

    write_stream: str = proto.Field(
        proto.STRING,
        number=1,
    )
    offset: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )
    proto_rows: ProtoData = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="rows",
        message=ProtoData,
    )
    trace_id: str = proto.Field(
        proto.STRING,
        number=6,
    )


class AppendRowsResponse(proto.Message):
    r"""Response message for ``AppendRows``.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        append_result (google.cloud.bigquery_storage_v1beta2.types.AppendRowsResponse.AppendResult):
            Result if the append is successful.

            This field is a member of `oneof`_ ``response``.
        error (google.rpc.status_pb2.Status):
            Error returned when problems were encountered. If present,
            it indicates rows were not accepted into the system. Users
            can retry or continue with other append requests within the
            same connection.

            Additional information about error signalling:

            ALREADY_EXISTS: Happens when an append specified an offset,
            and the backend already has received data at this offset.
            Typically encountered in retry scenarios, and can be
            ignored.

            OUT_OF_RANGE: Returned when the specified offset in the
            stream is beyond the current end of the stream.

            INVALID_ARGUMENT: Indicates a malformed request or data.

            ABORTED: Request processing is aborted because of prior
            failures. The request can be retried if previous failure is
            addressed.

            INTERNAL: Indicates server side error(s) that can be
            retried.

            This field is a member of `oneof`_ ``response``.
        updated_schema (google.cloud.bigquery_storage_v1beta2.types.TableSchema):
            If backend detects a schema update, pass it
            to user so that user can use it to input new
            type of message. It will be empty when no schema
            updates have occurred.
    """

    class AppendResult(proto.Message):
        r"""AppendResult is returned for successful append requests.

        Attributes:
            offset (google.protobuf.wrappers_pb2.Int64Value):
                The row offset at which the last append
                occurred. The offset will not be set if
                appending using default streams.
        """

        offset: wrappers_pb2.Int64Value = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.Int64Value,
        )

    append_result: AppendResult = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="response",
        message=AppendResult,
    )
    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="response",
        message=status_pb2.Status,
    )
    updated_schema: table.TableSchema = proto.Field(
        proto.MESSAGE,
        number=3,
        message=table.TableSchema,
    )


class GetWriteStreamRequest(proto.Message):
    r"""Request message for ``GetWriteStreamRequest``.

    Attributes:
        name (str):
            Required. Name of the stream to get, in the form of
            ``projects/{project}/datasets/{dataset}/tables/{table}/streams/{stream}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class BatchCommitWriteStreamsRequest(proto.Message):
    r"""Request message for ``BatchCommitWriteStreams``.

    Attributes:
        parent (str):
            Required. Parent table that all the streams should belong
            to, in the form of
            ``projects/{project}/datasets/{dataset}/tables/{table}``.
        write_streams (MutableSequence[str]):
            Required. The group of streams that will be
            committed atomically.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    write_streams: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class BatchCommitWriteStreamsResponse(proto.Message):
    r"""Response message for ``BatchCommitWriteStreams``.

    Attributes:
        commit_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which streams were committed in microseconds
            granularity. This field will only exist when there are no
            stream errors. **Note** if this field is not set, it means
            the commit was not successful.
        stream_errors (MutableSequence[google.cloud.bigquery_storage_v1beta2.types.StorageError]):
            Stream level error if commit failed. Only
            streams with error will be in the list.
            If empty, there is no error and all streams are
            committed successfully. If non empty, certain
            streams have errors and ZERO stream is committed
            due to atomicity guarantee.
    """

    commit_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    stream_errors: MutableSequence["StorageError"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="StorageError",
    )


class FinalizeWriteStreamRequest(proto.Message):
    r"""Request message for invoking ``FinalizeWriteStream``.

    Attributes:
        name (str):
            Required. Name of the stream to finalize, in the form of
            ``projects/{project}/datasets/{dataset}/tables/{table}/streams/{stream}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FinalizeWriteStreamResponse(proto.Message):
    r"""Response message for ``FinalizeWriteStream``.

    Attributes:
        row_count (int):
            Number of rows in the finalized stream.
    """

    row_count: int = proto.Field(
        proto.INT64,
        number=1,
    )


class FlushRowsRequest(proto.Message):
    r"""Request message for ``FlushRows``.

    Attributes:
        write_stream (str):
            Required. The stream that is the target of
            the flush operation.
        offset (google.protobuf.wrappers_pb2.Int64Value):
            Ending offset of the flush operation. Rows
            before this offset(including this offset) will
            be flushed.
    """

    write_stream: str = proto.Field(
        proto.STRING,
        number=1,
    )
    offset: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int64Value,
    )


class FlushRowsResponse(proto.Message):
    r"""Respond message for ``FlushRows``.

    Attributes:
        offset (int):
            The rows before this offset (including this
            offset) are flushed.
    """

    offset: int = proto.Field(
        proto.INT64,
        number=1,
    )


class StorageError(proto.Message):
    r"""Structured custom BigQuery Storage error message. The error
    can be attached as error details in the returned rpc Status. In
    particular, the use of error codes allows more structured error
    handling, and reduces the need to evaluate unstructured error
    text strings.

    Attributes:
        code (google.cloud.bigquery_storage_v1beta2.types.StorageError.StorageErrorCode):
            BigQuery Storage specific error code.
        entity (str):
            Name of the failed entity.
        error_message (str):
            Message that describes the error.
    """

    class StorageErrorCode(proto.Enum):
        r"""Error code for ``StorageError``.

        Values:
            STORAGE_ERROR_CODE_UNSPECIFIED (0):
                Default error.
            TABLE_NOT_FOUND (1):
                Table is not found in the system.
            STREAM_ALREADY_COMMITTED (2):
                Stream is already committed.
            STREAM_NOT_FOUND (3):
                Stream is not found.
            INVALID_STREAM_TYPE (4):
                Invalid Stream type.
                For example, you try to commit a stream that is
                not pending.
            INVALID_STREAM_STATE (5):
                Invalid Stream state.
                For example, you try to commit a stream that is
                not finalized or is garbaged.
            STREAM_FINALIZED (6):
                Stream is finalized.
        """
        STORAGE_ERROR_CODE_UNSPECIFIED = 0
        TABLE_NOT_FOUND = 1
        STREAM_ALREADY_COMMITTED = 2
        STREAM_NOT_FOUND = 3
        INVALID_STREAM_TYPE = 4
        INVALID_STREAM_STATE = 5
        STREAM_FINALIZED = 6

    code: StorageErrorCode = proto.Field(
        proto.ENUM,
        number=1,
        enum=StorageErrorCode,
    )
    entity: str = proto.Field(
        proto.STRING,
        number=2,
    )
    error_message: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
