# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""C-extension accelerated implementation of Spanner Arrow converter."""

from typing import Any, Optional, Sequence
import pyarrow as pa

from google_cloud_spanner_arrow import _spanner_arrow
from google_cloud_spanner_arrow.python import (
    fields_to_arrow_schema,
    spanner_type_to_arrow_type,
    _get_type_code,
    SPANNER_TYPE_ARRAY,
    SPANNER_TYPE_STRUCT,
)


def _normalize_single_field(f: Any) -> tuple:
    if isinstance(f, tuple):
        name = f[0]
        type_obj = f[1]
        type_code = _get_type_code(type_obj)
        if len(f) >= 3:
            sub = f[2]
            if type_code == SPANNER_TYPE_ARRAY:
                return (name, type_code, _normalize_single_field(sub))
            elif type_code == SPANNER_TYPE_STRUCT and isinstance(sub, (list, tuple)):
                return (name, type_code, tuple(_normalize_single_field(sf) for sf in sub))
            return (name, type_code, sub)
    else:
        name = getattr(f, "name", "col")
        type_obj = getattr(f, "type_", 6)
        type_code = _get_type_code(type_obj)

    if type_code == SPANNER_TYPE_ARRAY:
        elem_type = getattr(type_obj, "array_element_type", 6)
        child_tuple = _normalize_single_field(("item", elem_type))
        return (name, type_code, child_tuple)
    elif type_code == SPANNER_TYPE_STRUCT:
        struct_type = getattr(type_obj, "struct_type", None)
        sub_fields = getattr(struct_type, "fields", ())
        children = tuple(_normalize_single_field(sub_f) for sub_f in sub_fields)
        return (name, type_code, children)
    return (name, type_code)


def _normalize_fields(fields: Sequence[Any]):
    return [_normalize_single_field(f) for f in fields]


def rows_to_arrow_batch(
    fields: Sequence[Any],
    rows: Sequence[Sequence[Any]],
    schema: Optional[pa.Schema] = None,
) -> pa.RecordBatch:
    """Convert sequence of Spanner rows to pyarrow.RecordBatch using native C acceleration."""
    if not rows:
        if schema is None:
            schema = fields_to_arrow_schema(fields)
        return pa.RecordBatch.from_arrays(
            [pa.array([], type=f.type) for f in schema], schema=schema
        )

    field_tuples = _normalize_fields(fields)
    array_ptr, schema_ptr = _spanner_arrow.rows_to_c_batch(field_tuples, rows)
    return pa.RecordBatch._import_from_c(array_ptr, schema_ptr)


def wire_prs_to_arrow_batch(
    fields: Sequence[Any],
    wire_chunks: Sequence[bytes],
    schema: Optional[pa.Schema] = None,
) -> pa.RecordBatch:
    """Convert sequence of raw PartialResultSet protobuf wire bytes to pyarrow.RecordBatch in C."""
    if not wire_chunks:
        if schema is None:
            schema = fields_to_arrow_schema(fields)
        return pa.RecordBatch.from_arrays(
            [pa.array([], type=f.type) for f in schema], schema=schema
        )

    field_tuples = _normalize_fields(fields)
    array_ptr, schema_ptr = _spanner_arrow.wire_prs_to_c_batch(field_tuples, wire_chunks)
    return pa.RecordBatch._import_from_c(array_ptr, schema_ptr)
