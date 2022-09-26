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

from google.protobuf import duration_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.bigtable.v2",
    manifest={
        "ReadIteratorStats",
        "RequestLatencyStats",
        "ReadEfficiencyStats",
        "AllReadStats",
        "RequestStats",
    },
)


class ReadIteratorStats(proto.Message):
    r"""ReadIteratorStats captures information about the iteration of
    rows or cells over the course of a read, e.g. how many results
    were scanned in a read operation versus the results returned.

    Attributes:
        rows_seen_count (int):
            The rows seen (scanned) as part of the
            request. This includes the count of rows
            returned, as captured below.
        rows_returned_count (int):
            The rows returned as part of the request.
        cells_seen_count (int):
            The cells seen (scanned) as part of the
            request. This includes the count of cells
            returned, as captured below.
        cells_returned_count (int):
            The cells returned as part of the request.
        deletes_seen_count (int):
            The deletes seen as part of the request.
    """

    rows_seen_count = proto.Field(
        proto.INT64,
        number=1,
    )
    rows_returned_count = proto.Field(
        proto.INT64,
        number=2,
    )
    cells_seen_count = proto.Field(
        proto.INT64,
        number=3,
    )
    cells_returned_count = proto.Field(
        proto.INT64,
        number=4,
    )
    deletes_seen_count = proto.Field(
        proto.INT64,
        number=5,
    )


class RequestLatencyStats(proto.Message):
    r"""RequestLatencyStats provides a measurement of the latency of
    the request as it interacts with different systems over its
    lifetime, e.g. how long the request took to execute within a
    frontend server.

    Attributes:
        frontend_server_latency (google.protobuf.duration_pb2.Duration):
            The latency measured by the frontend server
            handling this request, from when the request was
            received, to when this value is sent back in the
            response. For more context on the component that
            is measuring this latency, see:
            https://cloud.google.com/bigtable/docs/overview
            Note: This value may be slightly shorter than
            the value reported into aggregate latency
            metrics in Monitoring for this request
            (https://cloud.google.com/bigtable/docs/monitoring-instance)
            as this value needs to be sent in the response
            before the latency measurement including that
            transmission is finalized.
    """

    frontend_server_latency = proto.Field(
        proto.MESSAGE,
        number=1,
        message=duration_pb2.Duration,
    )


class ReadEfficiencyStats(proto.Message):
    r"""ReadEfficiencyStats captures information about the efficiency
    of a read.

    Attributes:
        read_iterator_stats (google.cloud.bigtable_v2.types.ReadIteratorStats):
            Iteration stats describe how efficient the
            read is, e.g. comparing rows seen vs. rows
            returned or cells seen vs cells returned can
            provide an indication of read efficiency (the
            higher the ratio of seen to retuned the better).
        request_latency_stats (google.cloud.bigtable_v2.types.RequestLatencyStats):
            Request latency stats describe the time taken
            to complete a request, from the server side.
    """

    read_iterator_stats = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ReadIteratorStats",
    )
    request_latency_stats = proto.Field(
        proto.MESSAGE,
        number=2,
        message="RequestLatencyStats",
    )


class AllReadStats(proto.Message):
    r"""AllReadStats captures all known information about a read.

    Attributes:
        read_iterator_stats (google.cloud.bigtable_v2.types.ReadIteratorStats):
            Iteration stats describe how efficient the
            read is, e.g. comparing rows seen vs. rows
            returned or cells seen vs cells returned can
            provide an indication of read efficiency (the
            higher the ratio of seen to retuned the better).
        request_latency_stats (google.cloud.bigtable_v2.types.RequestLatencyStats):
            Request latency stats describe the time taken
            to complete a request, from the server side.
    """

    read_iterator_stats = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ReadIteratorStats",
    )
    request_latency_stats = proto.Field(
        proto.MESSAGE,
        number=2,
        message="RequestLatencyStats",
    )


class RequestStats(proto.Message):
    r"""RequestStats is the container for additional information pertaining
    to a single request, helpful for evaluating the performance of the
    sent request. Currently, there are the following supported methods:

    -  google.bigtable.v2.ReadRows

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        read_efficiency_stats (google.cloud.bigtable_v2.types.ReadEfficiencyStats):
            Available with the
            ReadRowsRequest.RequestStatsView.REQUEST_STATS_EFFICIENCY
            view, see package google.bigtable.v2.

            This field is a member of `oneof`_ ``stats``.
        all_read_stats (google.cloud.bigtable_v2.types.AllReadStats):
            Available with the
            ReadRowsRequest.RequestStatsView.REQUEST_STATS_FULL view,
            see package google.bigtable.v2.

            This field is a member of `oneof`_ ``stats``.
    """

    read_efficiency_stats = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="stats",
        message="ReadEfficiencyStats",
    )
    all_read_stats = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="stats",
        message="AllReadStats",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
