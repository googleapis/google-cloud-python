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
from google.cloud.bigquery_storage_v1beta2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.big_query_read import BigQueryReadAsyncClient, BigQueryReadClient
from .services.big_query_write import BigQueryWriteAsyncClient, BigQueryWriteClient
from .types.arrow import ArrowRecordBatch, ArrowSchema, ArrowSerializationOptions
from .types.avro import AvroRows, AvroSchema
from .types.protobuf import ProtoRows, ProtoSchema
from .types.storage import (
    AppendRowsRequest,
    AppendRowsResponse,
    BatchCommitWriteStreamsRequest,
    BatchCommitWriteStreamsResponse,
    CreateReadSessionRequest,
    CreateWriteStreamRequest,
    FinalizeWriteStreamRequest,
    FinalizeWriteStreamResponse,
    FlushRowsRequest,
    FlushRowsResponse,
    GetWriteStreamRequest,
    ReadRowsRequest,
    ReadRowsResponse,
    SplitReadStreamRequest,
    SplitReadStreamResponse,
    StorageError,
    StreamStats,
    ThrottleState,
)
from .types.stream import DataFormat, ReadSession, ReadStream, WriteStream
from .types.table import TableFieldSchema, TableSchema

__all__ = (
    "BigQueryReadAsyncClient",
    "BigQueryWriteAsyncClient",
    "AppendRowsRequest",
    "AppendRowsResponse",
    "ArrowRecordBatch",
    "ArrowSchema",
    "ArrowSerializationOptions",
    "AvroRows",
    "AvroSchema",
    "BatchCommitWriteStreamsRequest",
    "BatchCommitWriteStreamsResponse",
    "BigQueryReadClient",
    "BigQueryWriteClient",
    "CreateReadSessionRequest",
    "CreateWriteStreamRequest",
    "DataFormat",
    "FinalizeWriteStreamRequest",
    "FinalizeWriteStreamResponse",
    "FlushRowsRequest",
    "FlushRowsResponse",
    "GetWriteStreamRequest",
    "ProtoRows",
    "ProtoSchema",
    "ReadRowsRequest",
    "ReadRowsResponse",
    "ReadSession",
    "ReadStream",
    "SplitReadStreamRequest",
    "SplitReadStreamResponse",
    "StorageError",
    "StreamStats",
    "TableFieldSchema",
    "TableSchema",
    "ThrottleState",
    "WriteStream",
)
