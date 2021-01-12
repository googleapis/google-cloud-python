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


from google.cloud.bigquery_storage_v1.types import arrow
from google.cloud.bigquery_storage_v1.types import avro
from google.cloud.bigquery_storage_v1.types import stream


__protobuf__ = proto.module(
    package="google.cloud.bigquery.storage.v1",
    manifest={
        "CreateReadSessionRequest",
        "ReadRowsRequest",
        "ThrottleState",
        "StreamStats",
        "ReadRowsResponse",
        "SplitReadStreamRequest",
        "SplitReadStreamResponse",
    },
)


class CreateReadSessionRequest(proto.Message):
    r"""Request message for ``CreateReadSession``.

    Attributes:
        parent (str):
            Required. The request project that owns the session, in the
            form of ``projects/{project_id}``.
        read_session (google.cloud.bigquery_storage_v1.types.ReadSession):
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

    parent = proto.Field(proto.STRING, number=1)

    read_session = proto.Field(proto.MESSAGE, number=2, message=stream.ReadSession,)

    max_stream_count = proto.Field(proto.INT32, number=3)


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

    read_stream = proto.Field(proto.STRING, number=1)

    offset = proto.Field(proto.INT64, number=2)


class ThrottleState(proto.Message):
    r"""Information on if the current connection is being throttled.

    Attributes:
        throttle_percent (int):
            How much this connection is being throttled.
            Zero means no throttling, 100 means fully
            throttled.
    """

    throttle_percent = proto.Field(proto.INT32, number=1)


class StreamStats(proto.Message):
    r"""Estimated stream statistics for a given Stream.

    Attributes:
        progress (google.cloud.bigquery_storage_v1.types.StreamStats.Progress):
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

        at_response_start = proto.Field(proto.DOUBLE, number=1)

        at_response_end = proto.Field(proto.DOUBLE, number=2)

    progress = proto.Field(proto.MESSAGE, number=2, message=Progress,)


class ReadRowsResponse(proto.Message):
    r"""Response from calling ``ReadRows`` may include row data, progress
    and throttling information.

    Attributes:
        avro_rows (google.cloud.bigquery_storage_v1.types.AvroRows):
            Serialized row data in AVRO format.
        arrow_record_batch (google.cloud.bigquery_storage_v1.types.ArrowRecordBatch):
            Serialized row data in Arrow RecordBatch
            format.
        row_count (int):
            Number of serialized rows in the rows block.
        stats (google.cloud.bigquery_storage_v1.types.StreamStats):
            Statistics for the stream.
        throttle_state (google.cloud.bigquery_storage_v1.types.ThrottleState):
            Throttling state. If unset, the latest
            response still describes the current throttling
            status.
    """

    avro_rows = proto.Field(
        proto.MESSAGE, number=3, oneof="rows", message=avro.AvroRows,
    )

    arrow_record_batch = proto.Field(
        proto.MESSAGE, number=4, oneof="rows", message=arrow.ArrowRecordBatch,
    )

    row_count = proto.Field(proto.INT64, number=6)

    stats = proto.Field(proto.MESSAGE, number=2, message="StreamStats",)

    throttle_state = proto.Field(proto.MESSAGE, number=5, message="ThrottleState",)


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

    name = proto.Field(proto.STRING, number=1)

    fraction = proto.Field(proto.DOUBLE, number=2)


class SplitReadStreamResponse(proto.Message):
    r"""Response message for ``SplitReadStream``.

    Attributes:
        primary_stream (google.cloud.bigquery_storage_v1.types.ReadStream):
            Primary stream, which contains the beginning portion of
            \|original_stream|. An empty value indicates that the
            original stream can no longer be split.
        remainder_stream (google.cloud.bigquery_storage_v1.types.ReadStream):
            Remainder stream, which contains the tail of
            \|original_stream|. An empty value indicates that the
            original stream can no longer be split.
    """

    primary_stream = proto.Field(proto.MESSAGE, number=1, message=stream.ReadStream,)

    remainder_stream = proto.Field(proto.MESSAGE, number=2, message=stream.ReadStream,)


__all__ = tuple(sorted(__protobuf__.manifest))
