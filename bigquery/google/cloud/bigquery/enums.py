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
import six

from google.cloud.bigquery_v2.gapic import enums as gapic_enums


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
        "GEOGRAPHY",
        "NUMERIC",
    )
)

_SQL_NONSCALAR_TYPES = frozenset(("TYPE_KIND_UNSPECIFIED", "ARRAY", "STRUCT"))


def _make_sql_scalars_enum():
    """Create an enum based on a gapic enum containing only SQL scalar types."""

    new_enum = enum.Enum(
        "StandardSqlDataTypes",
        (
            (member.name, member.value)
            for member in gapic_enums.StandardSqlDataType.TypeKind
            if member.name in _SQL_SCALAR_TYPES
        ),
    )

    # make sure the docstring for the new enum is also correct
    orig_doc = gapic_enums.StandardSqlDataType.TypeKind.__doc__
    skip_pattern = re.compile(
        "|".join(_SQL_NONSCALAR_TYPES)
        + "|because a JSON object"  # the second description line of STRUCT member
    )

    new_doc = "\n".join(
        six.moves.filterfalse(skip_pattern.search, orig_doc.splitlines())
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
    NUMERIC = "NUMERIC"
    BOOLEAN = "BOOLEAN"
    BOOL = "BOOLEAN"
    GEOGRAPHY = "GEOGRAPHY"  # NOTE: not available in legacy types
    RECORD = "RECORD"
    STRUCT = "RECORD"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
