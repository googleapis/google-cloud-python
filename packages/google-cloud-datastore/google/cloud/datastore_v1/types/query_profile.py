# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

import proto  # type: ignore

from google.protobuf import struct_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.datastore.v1",
    manifest={
        "QueryMode",
        "QueryPlan",
        "ResultSetStats",
    },
)


class QueryMode(proto.Enum):
    r"""The mode in which the query request must be processed.

    Values:
        NORMAL (0):
            The default mode. Only the query results are
            returned.
        PLAN (1):
            This mode returns only the query plan,
            without any results or execution statistics
            information.
        PROFILE (2):
            This mode returns both the query plan and the
            execution statistics along with the results.
    """
    NORMAL = 0
    PLAN = 1
    PROFILE = 2


class QueryPlan(proto.Message):
    r"""Plan for the query.

    Attributes:
        plan_info (google.protobuf.struct_pb2.Struct):
            Planning phase information for the query. It will include:

            { "indexes_used": [ {"query_scope": "Collection",
            "properties": "(foo ASC, **name** ASC)"}, {"query_scope":
            "Collection", "properties": "(bar ASC, **name** ASC)"} ] }
    """

    plan_info: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=1,
        message=struct_pb2.Struct,
    )


class ResultSetStats(proto.Message):
    r"""Planning and execution statistics for the query.

    Attributes:
        query_plan (google.cloud.datastore_v1.types.QueryPlan):
            Plan for the query.
        query_stats (google.protobuf.struct_pb2.Struct):
            Aggregated statistics from the execution of the query.

            This will only be present when the request specifies
            ``PROFILE`` mode. For example, a query will return the
            statistics including:

            { "results_returned": "20", "documents_scanned": "20",
            "indexes_entries_scanned": "10050", "total_execution_time":
            "100.7 msecs" }
    """

    query_plan: "QueryPlan" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="QueryPlan",
    )
    query_stats: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
