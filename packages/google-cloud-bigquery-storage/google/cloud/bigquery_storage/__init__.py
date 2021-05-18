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

from google.cloud.bigquery_storage_v1 import BigQueryReadClient

from google.cloud.bigquery_storage_v1 import gapic_types as types
from google.cloud.bigquery_storage_v1 import __version__
from google.cloud.bigquery_storage_v1.types.arrow import ArrowRecordBatch
from google.cloud.bigquery_storage_v1.types.arrow import ArrowSchema
from google.cloud.bigquery_storage_v1.types.arrow import ArrowSerializationOptions
from google.cloud.bigquery_storage_v1.types.avro import AvroRows
from google.cloud.bigquery_storage_v1.types.avro import AvroSchema
from google.cloud.bigquery_storage_v1.types.storage import CreateReadSessionRequest
from google.cloud.bigquery_storage_v1.types.storage import ReadRowsRequest
from google.cloud.bigquery_storage_v1.types.storage import ReadRowsResponse
from google.cloud.bigquery_storage_v1.types.storage import SplitReadStreamRequest
from google.cloud.bigquery_storage_v1.types.storage import SplitReadStreamResponse
from google.cloud.bigquery_storage_v1.types.storage import StreamStats
from google.cloud.bigquery_storage_v1.types.storage import ThrottleState
from google.cloud.bigquery_storage_v1.types.stream import ReadSession
from google.cloud.bigquery_storage_v1.types.stream import ReadStream
from google.cloud.bigquery_storage_v1.types.stream import DataFormat

__all__ = (
    "BigQueryReadClient",
    "__version__",
    "types",
    "ArrowRecordBatch",
    "ArrowSchema",
    "ArrowSerializationOptions",
    "AvroRows",
    "AvroSchema",
    "CreateReadSessionRequest",
    "ReadRowsRequest",
    "ReadRowsResponse",
    "SplitReadStreamRequest",
    "SplitReadStreamResponse",
    "StreamStats",
    "ThrottleState",
    "ReadSession",
    "ReadStream",
    "DataFormat",
)
