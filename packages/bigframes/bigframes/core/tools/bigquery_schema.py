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

"""Helpers for working with BigQuery SchemaFields."""

from typing import Tuple

import google.cloud.bigquery

_LEGACY_TO_GOOGLESQL_TYPES = {
    "BOOLEAN": "BOOL",
    "INTEGER": "INT64",
    "FLOAT": "FLOAT64",
}


def _type_to_sql(field: google.cloud.bigquery.SchemaField):
    """Turn the type information of the field into SQL.

    Ignores the mode, since this has already been handled by _field_to_sql.
    """
    if field.field_type.casefold() in ("record", "struct"):
        return _to_struct(field.fields)

    # Map from legacy SQL names (the ones used in the BigQuery schema API) to
    # the GoogleSQL types. Importantly, FLOAT is from legacy SQL, but not valid
    # in GoogleSQL. See internal issue b/428190014.
    type_ = _LEGACY_TO_GOOGLESQL_TYPES.get(field.field_type.upper(), field.field_type)
    return type_


def _field_to_sql(field: google.cloud.bigquery.SchemaField):
    if field.mode == "REPEATED":
        # Unlike other types, ARRAY are represented as mode="REPEATED". To get
        # the array type, we use SchemaField object but ignore the mode.
        return f"`{field.name}` ARRAY<{_type_to_sql(field)}>"

    return f"`{field.name}` {_type_to_sql(field)}"


def _to_struct(bqschema: Tuple[google.cloud.bigquery.SchemaField, ...]):
    fields = [_field_to_sql(field) for field in bqschema]
    return f"STRUCT<{', '.join(fields)}>"


def to_sql_dry_run(bqschema: Tuple[google.cloud.bigquery.SchemaField, ...]):
    """Create an empty table expression with the correct schema."""
    return f"UNNEST(ARRAY<{_to_struct(bqschema)}>[])"
