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
from google.cloud.spanner import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.spanner_v1.services.spanner.async_client import SpannerAsyncClient
from google.cloud.spanner_v1.services.spanner.client import SpannerClient
from google.cloud.spanner_v1.types.change_stream import ChangeStreamRecord
from google.cloud.spanner_v1.types.commit_response import CommitResponse
from google.cloud.spanner_v1.types.keys import KeyRange, KeySet
from google.cloud.spanner_v1.types.location import (
    CacheUpdate,
    Group,
    KeyRecipe,
    Range,
    RecipeList,
    RoutingHint,
    Tablet,
)
from google.cloud.spanner_v1.types.mutation import Mutation
from google.cloud.spanner_v1.types.query_plan import (
    PlanNode,
    QueryAdvisorResult,
    QueryPlan,
)
from google.cloud.spanner_v1.types.result_set import (
    PartialResultSet,
    ResultSet,
    ResultSetMetadata,
    ResultSetStats,
)
from google.cloud.spanner_v1.types.spanner import (
    BatchCreateSessionsRequest,
    BatchCreateSessionsResponse,
    BatchWriteRequest,
    BatchWriteResponse,
    BeginTransactionRequest,
    CommitRequest,
    CreateSessionRequest,
    DeleteSessionRequest,
    DirectedReadOptions,
    ExecuteBatchDmlRequest,
    ExecuteBatchDmlResponse,
    ExecuteSqlRequest,
    GetSessionRequest,
    ListSessionsRequest,
    ListSessionsResponse,
    Partition,
    PartitionOptions,
    PartitionQueryRequest,
    PartitionReadRequest,
    PartitionResponse,
    ReadRequest,
    RequestOptions,
    RollbackRequest,
    Session,
)
from google.cloud.spanner_v1.types.transaction import (
    MultiplexedSessionPrecommitToken,
    Transaction,
    TransactionOptions,
    TransactionSelector,
)
from google.cloud.spanner_v1.types.type import (
    StructType,
    Type,
    TypeAnnotationCode,
    TypeCode,
)

__all__ = (
    "SpannerClient",
    "SpannerAsyncClient",
    "ChangeStreamRecord",
    "CommitResponse",
    "KeyRange",
    "KeySet",
    "CacheUpdate",
    "Group",
    "KeyRecipe",
    "Range",
    "RecipeList",
    "RoutingHint",
    "Tablet",
    "Mutation",
    "PlanNode",
    "QueryAdvisorResult",
    "QueryPlan",
    "PartialResultSet",
    "ResultSet",
    "ResultSetMetadata",
    "ResultSetStats",
    "BatchCreateSessionsRequest",
    "BatchCreateSessionsResponse",
    "BatchWriteRequest",
    "BatchWriteResponse",
    "BeginTransactionRequest",
    "CommitRequest",
    "CreateSessionRequest",
    "DeleteSessionRequest",
    "DirectedReadOptions",
    "ExecuteBatchDmlRequest",
    "ExecuteBatchDmlResponse",
    "ExecuteSqlRequest",
    "GetSessionRequest",
    "ListSessionsRequest",
    "ListSessionsResponse",
    "Partition",
    "PartitionOptions",
    "PartitionQueryRequest",
    "PartitionReadRequest",
    "PartitionResponse",
    "ReadRequest",
    "RequestOptions",
    "RollbackRequest",
    "Session",
    "MultiplexedSessionPrecommitToken",
    "Transaction",
    "TransactionOptions",
    "TransactionSelector",
    "StructType",
    "Type",
    "TypeAnnotationCode",
    "TypeCode",
)
