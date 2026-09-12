# Copyright 2026 Google LLC All rights reserved.
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

"""Helper utilities for converting Cloud Spanner types and schemas to PyArrow."""

import base64
from typing import Any, List, Optional, Sequence

from google.cloud.spanner_v1.types.type import TypeCode

try:
    import pyarrow as pa
    import pyarrow.compute as pc

    _HAS_PYARROW = True
except ImportError:  # pragma: NO COVER
    _HAS_PYARROW = False
    pa = None
    pc = None

_NO_PYARROW_ERROR = (
    "pyarrow is required to use Arrow features. "
    "Install it with `pip install google-cloud-spanner[pyarrow]` or `pip install pyarrow`."
)


def _check_pyarrow():
    """Verify pyarrow is installed."""
    if not _HAS_PYARROW:
        raise ImportError(_NO_PYARROW_ERROR)


def spanner_type_to_arrow_type(spanner_type) -> "pa.DataType":
    """Map a Spanner Type to a PyArrow DataType.

    :type spanner_type: :class:`~google.cloud.spanner_v1.types.Type`
    :param spanner_type: Spanner column type.

    :rtype: :class:`pyarrow.DataType`
    :returns: PyArrow DataType corresponding to the Spanner type.
    """
    _check_pyarrow()
    code = spanner_type.code

    if code == TypeCode.BOOL:
        return pa.bool_()
    elif code == TypeCode.INT64:
        return pa.int64()
    elif code == TypeCode.FLOAT32:
        return pa.float32()
    elif code == TypeCode.FLOAT64:
        return pa.float64()
    elif code == TypeCode.STRING:
        return pa.string()
    elif code == TypeCode.BYTES:
        return pa.binary()
    elif code == TypeCode.TIMESTAMP:
        return pa.timestamp("us", tz="UTC")
    elif code == TypeCode.DATE:
        return pa.date32()
    elif code == TypeCode.NUMERIC:
        return pa.decimal128(38, 9)
    elif code == TypeCode.JSON:
        return pa.string()
    elif code == TypeCode.PROTO:
        return pa.binary()
    elif code == TypeCode.ENUM:
        return pa.int64()
    elif code == TypeCode.INTERVAL:
        return pa.string()
    elif code == TypeCode.UUID:
        return pa.string()
    elif code == TypeCode.ARRAY:
        element_type = spanner_type_to_arrow_type(spanner_type.array_element_type)
        return pa.list_(element_type)
    elif code == TypeCode.STRUCT:
        fields = [
            pa.field(f.name, spanner_type_to_arrow_type(f.type_))
            for f in spanner_type.struct_type.fields
        ]
        return pa.struct(fields)
    return pa.string()


def spanner_schema_to_arrow_schema(fields: Sequence[Any]) -> "pa.Schema":
    """Convert Spanner row_type.fields to a PyArrow Schema.

    :type fields: Sequence of :class:`~google.cloud.spanner_v1.types.StructType.Field`
    :param fields: List of Spanner fields describing column names and types.

    :rtype: :class:`pyarrow.Schema`
    :returns: PyArrow Schema corresponding to the Spanner fields.
    """
    _check_pyarrow()
    arrow_fields = [
        pa.field(f.name, spanner_type_to_arrow_type(f.type_)) for f in fields
    ]
    return pa.schema(arrow_fields)


def _extract_cell_value(cell: Any, spanner_type: Any = None) -> Any:
    """Extract raw value from protobuf Value or Python object for fast Arrow ingestion."""
    if cell is None:
        return None

    type_code = spanner_type.code if hasattr(spanner_type, "code") else spanner_type

    # Check if cell is a google.protobuf.Value
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
            if type_code == TypeCode.BYTES:
                return base64.b64decode(val_str)
            elif type_code in (TypeCode.FLOAT32, TypeCode.FLOAT64):
                return float(val_str)
            return val_str
        elif kind == "list_value":
            if type_code == TypeCode.STRUCT and hasattr(spanner_type, "struct_type"):
                struct_fields = spanner_type.struct_type.fields
                return {
                    f.name: _extract_nested_element(elem, f.type_)
                    for f, elem in zip(struct_fields, cell.list_value.values)
                }
            element_type = (
                spanner_type.array_element_type
                if hasattr(spanner_type, "array_element_type")
                else None
            )
            return [
                _extract_nested_element(elem, element_type)
                for elem in cell.list_value.values
            ]
        elif kind == "struct_value":
            struct_fields_dict = {
                f.name: f.type_
                for f in getattr(
                    getattr(spanner_type, "struct_type", None), "fields", ()
                )
            }
            return {
                k: _extract_nested_element(v, struct_fields_dict.get(k))
                for k, v in cell.struct_value.fields.items()
            }
        return None

    # Cell is already a Python object
    if type_code == TypeCode.BYTES and isinstance(cell, str):
        return base64.b64decode(cell)
    if type_code in (
        TypeCode.STRING,
        TypeCode.INTERVAL,
        TypeCode.JSON,
        TypeCode.UUID,
    ) and not isinstance(cell, str):
        return str(cell)
    return cell


def _extract_nested_element(elem: Any, spanner_type: Any = None) -> Any:
    """Extract nested array/struct elements into python scalars for PyArrow nested builders."""
    if elem is None:
        return None
    type_code = spanner_type.code if hasattr(spanner_type, "code") else spanner_type
    val = _extract_cell_value(elem, spanner_type)
    if isinstance(val, str):
        if type_code == TypeCode.INT64:
            return int(val)
        elif type_code == TypeCode.NUMERIC:
            import decimal

            return decimal.Decimal(val)
    return val


def extract_columns_from_rows(
    rows: Sequence[Sequence[Any]], field_types: Sequence[Any]
) -> List[List[Any]]:
    """Extract columnar data from a batch of rows using fast list comprehensions."""
    num_columns = len(field_types)
    return [
        [_extract_cell_value(row[idx], field_types[idx]) for row in rows]
        for idx in range(num_columns)
    ]


def convert_column_to_arrow_array(
    column_values: List[Any],
    arrow_field: "pa.Field",
    type_code: Optional[int] = None,
) -> "pa.Array":
    """Convert a single column's raw values into a PyArrow Array using fast C++ parsing.

    :type column_values: List[Any]
    :param column_values: Extracted raw values for the column.

    :type arrow_field: :class:`pyarrow.Field`
    :param arrow_field: PyArrow target field.

    :type type_code: Optional[int]
    :param type_code: Spanner TypeCode for the column.

    :rtype: :class:`pyarrow.Array`
    :returns: PyArrow Array for the column.
    """
    _check_pyarrow()
    arrow_type = arrow_field.type

    # If column is empty, return empty array with appropriate type
    if not column_values:
        return pa.array([], type=arrow_type)

    # If column contains string-encoded primitives from protobuf, use fast C++ casting
    first_non_null = next((v for v in column_values if v is not None), None)
    if isinstance(first_non_null, str):
        if type_code == TypeCode.INT64:
            return pc.cast(pa.array(column_values, type=pa.string()), pa.int64())
        elif type_code == TypeCode.DATE:
            return pc.cast(pa.array(column_values, type=pa.string()), pa.date32())
        elif type_code == TypeCode.TIMESTAMP:
            return pc.cast(
                pa.array(column_values, type=pa.string()),
                pa.timestamp("us", tz="UTC"),
            )
        elif type_code == TypeCode.NUMERIC:
            return pc.cast(pa.array(column_values, type=pa.string()), arrow_type)

    # Standard array construction for BOOL, FLOAT, STRING, BYTES, JSON, ARRAY, STRUCT, and native objects
    return pa.array(column_values, type=arrow_type)
