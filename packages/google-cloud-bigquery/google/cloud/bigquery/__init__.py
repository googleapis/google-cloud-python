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

"""Google BigQuery API wrapper.

The main concepts with this API are:

- :class:`~google.cloud.bigquery.client.Client` manages connections to the
  BigQuery API. Use the client methods to run jobs (such as a
  :class:`~google.cloud.bigquery.job.QueryJob` via
  :meth:`~google.cloud.bigquery.client.Client.query`) and manage resources.

- :class:`~google.cloud.bigquery.dataset.Dataset` represents a
  collection of tables.

- :class:`~google.cloud.bigquery.table.Table` represents a single "relation".
"""

import sys
import warnings

from google.cloud.bigquery import version as bigquery_version

__version__ = bigquery_version.__version__

from google.cloud.bigquery import enums
from google.cloud.bigquery.client import Client
from google.cloud.bigquery.dataset import AccessEntry, Dataset, DatasetReference
from google.cloud.bigquery.encryption_configuration import EncryptionConfiguration
from google.cloud.bigquery.enums import (
    AutoRowIDs,
    DecimalTargetType,
    KeyResultStatementKind,
    SqlTypeNames,
    StandardSqlTypeNames,
)
from google.cloud.bigquery.exceptions import (
    LegacyBigQueryStorageError,
    LegacyPandasError,
    LegacyPyarrowError,
)
from google.cloud.bigquery.external_config import (
    BigtableColumn,
    BigtableColumnFamily,
    BigtableOptions,
    CSVOptions,
    ExternalConfig,
    ExternalSourceFormat,
    GoogleSheetsOptions,
    HivePartitioningOptions,
)
from google.cloud.bigquery.format_options import AvroOptions, ParquetOptions
from google.cloud.bigquery.job import (
    Compression,
    CopyJob,
    CopyJobConfig,
    CreateDisposition,
    DestinationFormat,
    DmlStats,
    Encoding,
    ExtractJob,
    ExtractJobConfig,
    LoadJob,
    LoadJobConfig,
    OperationType,
    QueryJob,
    QueryJobConfig,
    QueryPriority,
    SchemaUpdateOption,
    ScriptOptions,
    SourceFormat,
    TransactionInfo,
    UnknownJob,
    WriteDisposition,
)
from google.cloud.bigquery.job.base import SessionInfo
from google.cloud.bigquery.model import Model, ModelReference
from google.cloud.bigquery.query import (
    ArrayQueryParameter,
    ArrayQueryParameterType,
    ConnectionProperty,
    RangeQueryParameter,
    RangeQueryParameterType,
    ScalarQueryParameter,
    ScalarQueryParameterType,
    SqlParameterScalarTypes,
    StructQueryParameter,
    StructQueryParameterType,
    UDFResource,
)
from google.cloud.bigquery.retry import DEFAULT_RETRY
from google.cloud.bigquery.routine import (
    DeterminismLevel,
    ExternalRuntimeOptions,
    RemoteFunctionOptions,
    Routine,
    RoutineArgument,
    RoutineReference,
    RoutineType,
)
from google.cloud.bigquery.schema import FieldElementType, PolicyTagList, SchemaField
from google.cloud.bigquery.standard_sql import (
    StandardSqlDataType,
    StandardSqlField,
    StandardSqlStructType,
    StandardSqlTableType,
)
from google.cloud.bigquery.table import (
    CloneDefinition,
    PartitionRange,
    RangePartitioning,
    Row,
    SnapshotDefinition,
    Table,
    TableReference,
    TimePartitioning,
    TimePartitioningType,
)

try:
    import bigquery_magics  # type: ignore
except ImportError:
    bigquery_magics = None

if sys.version_info < (3, 10):  # pragma: NO COVER
    warnings.warn(
        "The python-bigquery library no longer supports Python <= 3.9. "
        f"Your Python version is {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}. We "
        "recommend that you update soon to ensure ongoing support. For "
        "more details, see: [Google Cloud Client Libraries Supported Python Versions policy](https://cloud.google.com/python/docs/supported-python-versions)",
        FutureWarning,
    )

__all__ = [
    "__version__",
    "Client",
    # Queries
    "ConnectionProperty",
    "QueryJob",
    "QueryJobConfig",
    "ArrayQueryParameter",
    "ScalarQueryParameter",
    "StructQueryParameter",
    "RangeQueryParameter",
    "ArrayQueryParameterType",
    "ScalarQueryParameterType",
    "SqlParameterScalarTypes",
    "StructQueryParameterType",
    "RangeQueryParameterType",
    # Datasets
    "Dataset",
    "DatasetReference",
    "AccessEntry",
    # Tables
    "Table",
    "TableReference",
    "PartitionRange",
    "RangePartitioning",
    "Row",
    "SnapshotDefinition",
    "CloneDefinition",
    "TimePartitioning",
    "TimePartitioningType",
    # Jobs
    "CopyJob",
    "CopyJobConfig",
    "ExtractJob",
    "ExtractJobConfig",
    "LoadJob",
    "LoadJobConfig",
    "SessionInfo",
    "UnknownJob",
    # Models
    "Model",
    "ModelReference",
    # Routines
    "Routine",
    "RoutineArgument",
    "RoutineReference",
    "RemoteFunctionOptions",
    "ExternalRuntimeOptions",
    # Shared helpers
    "SchemaField",
    "FieldElementType",
    "PolicyTagList",
    "UDFResource",
    "ExternalConfig",
    "AvroOptions",
    "BigtableOptions",
    "BigtableColumnFamily",
    "BigtableColumn",
    "DmlStats",
    "CSVOptions",
    "GoogleSheetsOptions",
    "HivePartitioningOptions",
    "ParquetOptions",
    "ScriptOptions",
    "TransactionInfo",
    "DEFAULT_RETRY",
    # Standard SQL types
    "StandardSqlDataType",
    "StandardSqlField",
    "StandardSqlStructType",
    "StandardSqlTableType",
    # Enum Constants
    "enums",
    "AutoRowIDs",
    "Compression",
    "CreateDisposition",
    "DecimalTargetType",
    "DestinationFormat",
    "DeterminismLevel",
    "ExternalSourceFormat",
    "Encoding",
    "KeyResultStatementKind",
    "OperationType",
    "QueryPriority",
    "RoutineType",
    "SchemaUpdateOption",
    "SourceFormat",
    "SqlTypeNames",
    "StandardSqlTypeNames",
    "WriteDisposition",
    # EncryptionConfiguration
    "EncryptionConfiguration",
    # Custom exceptions
    "LegacyBigQueryStorageError",
    "LegacyPyarrowError",
    "LegacyPandasError",
]


def load_ipython_extension(ipython):
    """Called by IPython when this module is loaded as an IPython extension."""
    warnings.warn(
        "%load_ext google.cloud.bigquery is deprecated. Install bigquery-magics package and use `%load_ext bigquery_magics`, instead.",
        category=FutureWarning,
    )

    if bigquery_magics is not None:
        bigquery_magics.load_ipython_extension(ipython)
    else:
        from google.cloud.bigquery.magics.magics import _cell_magic

        ipython.register_magic_function(
            _cell_magic, magic_kind="cell", magic_name="bigquery"
        )
