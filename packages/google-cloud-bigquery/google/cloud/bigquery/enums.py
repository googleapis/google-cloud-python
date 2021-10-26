# Copyright 2019 Google LLC
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

import re

import enum
import itertools

from google.cloud.bigquery_v2 import types as gapic_types
from google.cloud.bigquery.query import ScalarQueryParameterType


class AutoRowIDs(enum.Enum):
    """How to handle automatic insert IDs when inserting rows as a stream."""

    DISABLED = enum.auto()
    GENERATE_UUID = enum.auto()


class Compression(object):
    """The compression type to use for exported files. The default value is
    :attr:`NONE`.

    :attr:`DEFLATE` and :attr:`SNAPPY` are
    only supported for Avro.
    """

    GZIP = "GZIP"
    """Specifies GZIP format."""

    DEFLATE = "DEFLATE"
    """Specifies DEFLATE format."""

    SNAPPY = "SNAPPY"
    """Specifies SNAPPY format."""

    NONE = "NONE"
    """Specifies no compression."""


class DecimalTargetType:
    """The data types that could be used as a target type when converting decimal values.

    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#DecimalTargetType

    .. versionadded:: 2.21.0
    """

    NUMERIC = "NUMERIC"
    """Decimal values could be converted to NUMERIC type."""

    BIGNUMERIC = "BIGNUMERIC"
    """Decimal values could be converted to BIGNUMERIC type."""

    STRING = "STRING"
    """Decimal values could be converted to STRING type."""


class CreateDisposition(object):
    """Specifies whether the job is allowed to create new tables. The default
    value is :attr:`CREATE_IF_NEEDED`.

    Creation, truncation and append actions occur as one atomic update
    upon job completion.
    """

    CREATE_IF_NEEDED = "CREATE_IF_NEEDED"
    """If the table does not exist, BigQuery creates the table."""

    CREATE_NEVER = "CREATE_NEVER"
    """The table must already exist. If it does not, a 'notFound' error is
    returned in the job result."""


class DestinationFormat(object):
    """The exported file format. The default value is :attr:`CSV`.

    Tables with nested or repeated fields cannot be exported as CSV.
    """

    CSV = "CSV"
    """Specifies CSV format."""

    NEWLINE_DELIMITED_JSON = "NEWLINE_DELIMITED_JSON"
    """Specifies newline delimited JSON format."""

    AVRO = "AVRO"
    """Specifies Avro format."""

    PARQUET = "PARQUET"
    """Specifies Parquet format."""


class Encoding(object):
    """The character encoding of the data. The default is :attr:`UTF_8`.

    BigQuery decodes the data after the raw, binary data has been
    split using the values of the quote and fieldDelimiter properties.
    """

    UTF_8 = "UTF-8"
    """Specifies UTF-8 encoding."""

    ISO_8859_1 = "ISO-8859-1"
    """Specifies ISO-8859-1 encoding."""


class QueryPriority(object):
    """Specifies a priority for the query. The default value is
    :attr:`INTERACTIVE`.
    """

    INTERACTIVE = "INTERACTIVE"
    """Specifies interactive priority."""

    BATCH = "BATCH"
    """Specifies batch priority."""


class SchemaUpdateOption(object):
    """Specifies an update to the destination table schema as a side effect of
    a load job.
    """

    ALLOW_FIELD_ADDITION = "ALLOW_FIELD_ADDITION"
    """Allow adding a nullable field to the schema."""

    ALLOW_FIELD_RELAXATION = "ALLOW_FIELD_RELAXATION"
    """Allow relaxing a required field in the original schema to nullable."""


class SourceFormat(object):
    """The format of the data files. The default value is :attr:`CSV`.

    Note that the set of allowed values for loading data is different
    than the set used for external data sources (see
    :class:`~google.cloud.bigquery.external_config.ExternalSourceFormat`).
    """

    CSV = "CSV"
    """Specifies CSV format."""

    DATASTORE_BACKUP = "DATASTORE_BACKUP"
    """Specifies datastore backup format"""

    NEWLINE_DELIMITED_JSON = "NEWLINE_DELIMITED_JSON"
    """Specifies newline delimited JSON format."""

    AVRO = "AVRO"
    """Specifies Avro format."""

    PARQUET = "PARQUET"
    """Specifies Parquet format."""

    ORC = "ORC"
    """Specifies Orc format."""


class KeyResultStatementKind:
    """Determines which statement in the script represents the "key result".

    The "key result" is used to populate the schema and query results of the script job.

    https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#keyresultstatementkind
    """

    KEY_RESULT_STATEMENT_KIND_UNSPECIFIED = "KEY_RESULT_STATEMENT_KIND_UNSPECIFIED"
    LAST = "LAST"
    FIRST_SELECT = "FIRST_SELECT"


_SQL_SCALAR_TYPES = frozenset(
    (
        "INT64",
        "BOOL",
        "FLOAT64",
        "STRING",
        "BYTES",
        "TIMESTAMP",
        "DATE",
        "TIME",
        "DATETIME",
        "INTERVAL",
        "GEOGRAPHY",
        "NUMERIC",
        "BIGNUMERIC",
        "JSON",
    )
)

_SQL_NONSCALAR_TYPES = frozenset(("TYPE_KIND_UNSPECIFIED", "ARRAY", "STRUCT"))


def _make_sql_scalars_enum():
    """Create an enum based on a gapic enum containing only SQL scalar types."""

    new_enum = enum.Enum(
        "StandardSqlDataTypes",
        (
            (member.name, member.value)
            for member in gapic_types.StandardSqlDataType.TypeKind
            if member.name in _SQL_SCALAR_TYPES
        ),
    )

    # make sure the docstring for the new enum is also correct
    orig_doc = gapic_types.StandardSqlDataType.TypeKind.__doc__
    skip_pattern = re.compile(
        "|".join(_SQL_NONSCALAR_TYPES)
        + "|because a JSON object"  # the second description line of STRUCT member
    )

    new_doc = "\n".join(
        itertools.filterfalse(skip_pattern.search, orig_doc.splitlines())
    )
    new_enum.__doc__ = "An Enum of scalar SQL types.\n" + new_doc

    return new_enum


StandardSqlDataTypes = _make_sql_scalars_enum()


# See also: https://cloud.google.com/bigquery/data-types#legacy_sql_data_types
# and https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
class SqlTypeNames(str, enum.Enum):
    """Enum of allowed SQL type names in schema.SchemaField."""

    STRING = "STRING"
    BYTES = "BYTES"
    INTEGER = "INTEGER"
    INT64 = "INTEGER"
    FLOAT = "FLOAT"
    FLOAT64 = "FLOAT"
    DECIMAL = NUMERIC = "NUMERIC"
    BIGDECIMAL = BIGNUMERIC = "BIGNUMERIC"
    BOOLEAN = "BOOLEAN"
    BOOL = "BOOLEAN"
    GEOGRAPHY = "GEOGRAPHY"  # NOTE: not available in legacy types
    RECORD = "RECORD"
    STRUCT = "RECORD"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    INTERVAL = "INTERVAL"  # NOTE: not available in legacy types


class SqlParameterScalarTypes:
    """Supported scalar SQL query parameter types as type objects."""

    BOOL = ScalarQueryParameterType("BOOL")
    BOOLEAN = ScalarQueryParameterType("BOOL")
    BIGDECIMAL = ScalarQueryParameterType("BIGNUMERIC")
    BIGNUMERIC = ScalarQueryParameterType("BIGNUMERIC")
    BYTES = ScalarQueryParameterType("BYTES")
    DATE = ScalarQueryParameterType("DATE")
    DATETIME = ScalarQueryParameterType("DATETIME")
    DECIMAL = ScalarQueryParameterType("NUMERIC")
    FLOAT = ScalarQueryParameterType("FLOAT64")
    FLOAT64 = ScalarQueryParameterType("FLOAT64")
    GEOGRAPHY = ScalarQueryParameterType("GEOGRAPHY")
    INT64 = ScalarQueryParameterType("INT64")
    INTEGER = ScalarQueryParameterType("INT64")
    NUMERIC = ScalarQueryParameterType("NUMERIC")
    STRING = ScalarQueryParameterType("STRING")
    TIME = ScalarQueryParameterType("TIME")
    TIMESTAMP = ScalarQueryParameterType("TIMESTAMP")


class WriteDisposition(object):
    """Specifies the action that occurs if destination table already exists.

    The default value is :attr:`WRITE_APPEND`.

    Each action is atomic and only occurs if BigQuery is able to complete
    the job successfully. Creation, truncation and append actions occur as one
    atomic update upon job completion.
    """

    WRITE_APPEND = "WRITE_APPEND"
    """If the table already exists, BigQuery appends the data to the table."""

    WRITE_TRUNCATE = "WRITE_TRUNCATE"
    """If the table already exists, BigQuery overwrites the table data."""

    WRITE_EMPTY = "WRITE_EMPTY"
    """If the table already exists and contains data, a 'duplicate' error is
    returned in the job result."""


class DeterminismLevel:
    """Specifies determinism level for JavaScript user-defined functions (UDFs).

    https://cloud.google.com/bigquery/docs/reference/rest/v2/routines#DeterminismLevel
    """

    DETERMINISM_LEVEL_UNSPECIFIED = "DETERMINISM_LEVEL_UNSPECIFIED"
    """The determinism of the UDF is unspecified."""

    DETERMINISTIC = "DETERMINISTIC"
    """The UDF is deterministic, meaning that 2 function calls with the same inputs
    always produce the same result, even across 2 query runs."""

    NOT_DETERMINISTIC = "NOT_DETERMINISTIC"
    """The UDF is not deterministic."""
