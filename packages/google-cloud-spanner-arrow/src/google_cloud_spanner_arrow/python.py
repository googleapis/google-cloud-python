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

"""Pure-Python fallback implementation of Spanner Arrow converter."""

import base64
import decimal
import math
from typing import Any, List, Optional, Sequence

try:
    import pyarrow as pa
    import pyarrow.compute as pc
    _HAS_PYARROW = True
except ImportError:  # pragma: NO COVER
    _HAS_PYARROW = False
    pa = None
    pc = None

# Spanner TypeCode constants (matching google.cloud.spanner_v1.types.TypeCode)
SPANNER_TYPE_UNSPECIFIED = 0
SPANNER_TYPE_BOOL = 1
SPANNER_TYPE_INT64 = 2
SPANNER_TYPE_FLOAT64 = 3
SPANNER_TYPE_TIMESTAMP = 4
SPANNER_TYPE_DATE = 5
SPANNER_TYPE_STRING = 6
SPANNER_TYPE_BYTES = 7
SPANNER_TYPE_ARRAY = 8
SPANNER_TYPE_STRUCT = 9
SPANNER_TYPE_NUMERIC = 10
SPANNER_TYPE_JSON = 11
SPANNER_TYPE_PROTO = 13
SPANNER_TYPE_ENUM = 14
SPANNER_TYPE_FLOAT32 = 15
SPANNER_TYPE_INTERVAL = 16
SPANNER_TYPE_UUID = 17


def _check_pyarrow():
    if not _HAS_PYARROW:
        raise ImportError(
            "pyarrow is required to use Arrow features. "
            "Install it with `pip install pyarrow`."
        )


def _get_type_code(type_obj: Any) -> int:
    if isinstance(type_obj, int):
        return type_obj
    if hasattr(type_obj, "code"):
        return type_obj.code if isinstance(type_obj.code, int) else int(type_obj.code)
    return SPANNER_TYPE_STRING


def spanner_type_to_arrow_type(spanner_type: Any) -> "pa.DataType":
    """Map a Spanner Type to a PyArrow DataType."""
    _check_pyarrow()
    code = _get_type_code(spanner_type)

    if code == SPANNER_TYPE_BOOL:
        return pa.bool_()
    elif code in (SPANNER_TYPE_INT64, SPANNER_TYPE_ENUM):
        return pa.int64()
    elif code == SPANNER_TYPE_FLOAT32:
        return pa.float32()
    elif code == SPANNER_TYPE_FLOAT64:
        return pa.float64()
    elif code in (SPANNER_TYPE_STRING, SPANNER_TYPE_JSON, SPANNER_TYPE_INTERVAL, SPANNER_TYPE_UUID):
        return pa.string()
    elif code in (SPANNER_TYPE_BYTES, SPANNER_TYPE_PROTO):
        return pa.binary()
    elif code == SPANNER_TYPE_TIMESTAMP:
        return pa.timestamp("us", tz="UTC")
    elif code == SPANNER_TYPE_DATE:
        return pa.date32()
    elif code == SPANNER_TYPE_NUMERIC:
        return pa.decimal128(38, 9)
    elif code == SPANNER_TYPE_ARRAY:
        elem_type = getattr(spanner_type, "array_element_type", SPANNER_TYPE_STRING)
        return pa.list_(spanner_type_to_arrow_type(elem_type))
    elif code == SPANNER_TYPE_STRUCT:
        struct_type = getattr(spanner_type, "struct_type", None)
        fields = getattr(struct_type, "fields", ())
        arrow_fields = [
            pa.field(f.name, spanner_type_to_arrow_type(f.type_)) for f in fields
        ]
        return pa.struct(arrow_fields)
    return pa.string()


def fields_to_arrow_schema(fields: Sequence[Any]) -> "pa.Schema":
    """Convert sequence of Spanner Field descriptors to a PyArrow Schema."""
    _check_pyarrow()
    arrow_fields = []
    for f in fields:
        if isinstance(f, tuple):
            name, type_code = f[0], f[1]
            if len(f) >= 3 and _get_type_code(type_code) == SPANNER_TYPE_STRUCT:
                sub_fields = [
                    pa.field(sf[0], spanner_type_to_arrow_type(sf[1])) for sf in f[2]
                ]
                arrow_fields.append(pa.field(name, pa.struct(sub_fields)))
            elif len(f) >= 3 and _get_type_code(type_code) == SPANNER_TYPE_ARRAY:
                sub_elem = f[2]
                sub_type = sub_elem[1] if isinstance(sub_elem, tuple) else sub_elem
                arrow_fields.append(
                    pa.field(name, pa.list_(spanner_type_to_arrow_type(sub_type)))
                )
            else:
                arrow_fields.append(pa.field(name, spanner_type_to_arrow_type(type_code)))
        else:
            name = getattr(f, "name", "col")
            type_obj = getattr(f, "type_", SPANNER_TYPE_STRING)
            arrow_fields.append(pa.field(name, spanner_type_to_arrow_type(type_obj)))
    return pa.schema(arrow_fields)


def _extract_cell_value(cell: Any, type_code: int) -> Any:
    if cell is None:
        return None

    if hasattr(cell, "WhichOneof"):
        kind = cell.WhichOneof("kind")
        if kind == "null_value" or kind is None:
            return None
        elif kind == "bool_value":
            return cell.bool_value
        elif kind == "number_value":
            return cell.number_value
        elif kind == "string_value":
            val_str = cell.string_value
            if type_code in (SPANNER_TYPE_BYTES, SPANNER_TYPE_PROTO):
                return base64.b64decode(val_str)
            elif type_code in (SPANNER_TYPE_FLOAT32, SPANNER_TYPE_FLOAT64):
                if val_str == "NaN":
                    return float("nan")
                elif val_str == "Infinity":
                    return float("inf")
                elif val_str == "-Infinity":
                    return float("-inf")
                return float(val_str)
            return val_str
        elif kind == "list_value":
            return [
                _extract_cell_value(elem, SPANNER_TYPE_STRING)
                for elem in cell.list_value.values
            ]
        elif kind == "struct_value":
            return {
                k: _extract_cell_value(v, SPANNER_TYPE_STRING)
                for k, v in cell.struct_value.fields.items()
            }
        return None

    if type_code in (SPANNER_TYPE_BYTES, SPANNER_TYPE_PROTO) and isinstance(cell, str):
        return base64.b64decode(cell)
    return cell


def convert_column_to_arrow_array(
    column_values: List[Any],
    arrow_field: "pa.Field",
    type_code: Optional[int] = None,
) -> "pa.Array":
    """Convert a single column's raw values into a PyArrow Array with fast casting."""
    arrow_type = arrow_field.type
    if not column_values:
        return pa.array([], type=arrow_type)

    first_non_null = next((v for v in column_values if v is not None), None)
    if isinstance(first_non_null, str):
        if type_code in (SPANNER_TYPE_INT64, SPANNER_TYPE_ENUM):
            return pc.cast(pa.array(column_values, type=pa.string()), pa.int64())
        elif type_code == SPANNER_TYPE_FLOAT32:
            return pc.cast(pa.array(column_values, type=pa.string()), pa.float32())
        elif type_code == SPANNER_TYPE_FLOAT64:
            return pc.cast(pa.array(column_values, type=pa.string()), pa.float64())
        elif type_code == SPANNER_TYPE_DATE:
            return pc.cast(pa.array(column_values, type=pa.string()), pa.date32())
        elif type_code == SPANNER_TYPE_TIMESTAMP:
            return pc.cast(
                pa.array(column_values, type=pa.string()),
                pa.timestamp("us", tz="UTC"),
            )
        elif type_code == SPANNER_TYPE_NUMERIC:
            return pc.cast(pa.array(column_values, type=pa.string()), arrow_type)

    return pa.array(column_values, type=arrow_type)


def rows_to_arrow_batch(
    fields: Sequence[Any], rows: Sequence[Sequence[Any]], schema: Optional["pa.Schema"] = None
) -> "pa.RecordBatch":
    """Convert sequence of rows to pyarrow.RecordBatch in pure Python."""
    _check_pyarrow()
    if schema is None:
        schema = fields_to_arrow_schema(fields)

    num_cols = len(fields)
    type_codes = [
        _get_type_code(f[1] if isinstance(f, tuple) else getattr(f, "type_", SPANNER_TYPE_STRING))
        for f in fields
    ]

    if not rows:
        return pa.RecordBatch.from_arrays(
            [pa.array([], type=f.type) for f in schema], schema=schema
        )

    columns_data: List[List[Any]] = [[] for _ in range(num_cols)]
    for row in rows:
        row_len = len(row)
        for c in range(num_cols):
            cell = row[c] if c < row_len else None
            columns_data[c].append(_extract_cell_value(cell, type_codes[c]))

    arrays = [
        convert_column_to_arrow_array(col_vals, pa_field, type_code)
        for col_vals, pa_field, type_code in zip(columns_data, schema, type_codes)
    ]

    return pa.RecordBatch.from_arrays(arrays, schema=schema)
