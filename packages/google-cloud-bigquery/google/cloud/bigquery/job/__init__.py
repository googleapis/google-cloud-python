# Copyright 2015 Google LLC
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

"""Define API Jobs."""

from google.cloud.bigquery.enums import (
    Compression,
    CreateDisposition,
    DestinationFormat,
    Encoding,
    QueryPriority,
    SchemaUpdateOption,
    SourceFormat,
    WriteDisposition,
)
from google.cloud.bigquery.job.base import (
    _DONE_STATE,
    ReservationUsage,
    ScriptStackFrame,
    ScriptStatistics,
    TransactionInfo,
    UnknownJob,
    _AsyncJob,
    _error_result_to_exception,
    _JobConfig,
    _JobReference,
)
from google.cloud.bigquery.job.copy_ import CopyJob, CopyJobConfig, OperationType
from google.cloud.bigquery.job.extract import ExtractJob, ExtractJobConfig
from google.cloud.bigquery.job.load import LoadJob, LoadJobConfig
from google.cloud.bigquery.job.query import (
    DmlStats,
    IncrementalResultStats,
    QueryJob,
    QueryJobConfig,
    QueryPlanEntry,
    QueryPlanEntryStep,
    ScriptOptions,
    TimelineEntry,
    _contains_order_by,
)

# Include classes previously in job.py for backwards compatibility.
__all__ = [
    "_AsyncJob",
    "_error_result_to_exception",
    "_DONE_STATE",
    "_JobConfig",
    "_JobReference",
    "ReservationUsage",
    "ScriptStatistics",
    "ScriptStackFrame",
    "UnknownJob",
    "CopyJob",
    "CopyJobConfig",
    "OperationType",
    "ExtractJob",
    "ExtractJobConfig",
    "LoadJob",
    "LoadJobConfig",
    "_contains_order_by",
    "DmlStats",
    "QueryJob",
    "QueryJobConfig",
    "QueryPlanEntry",
    "QueryPlanEntryStep",
    "ScriptOptions",
    "TimelineEntry",
    "Compression",
    "CreateDisposition",
    "DestinationFormat",
    "Encoding",
    "QueryPriority",
    "SchemaUpdateOption",
    "SourceFormat",
    "TransactionInfo",
    "WriteDisposition",
    "IncrementalResultStats",
]
