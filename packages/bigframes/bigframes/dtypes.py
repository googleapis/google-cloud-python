# Copyright 2023 Google LLC
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

"""Mappings for Pandas dtypes supported by BigQuery DataFrames package"""

import datetime
import decimal
import typing
from typing import Any, Dict, Literal, Union

import bigframes_vendored.ibis.backends.bigquery.datatypes as third_party_ibis_bqtypes
import geopandas as gpd  # type: ignore
import ibis
import numpy as np
import pandas as pd
import pyarrow as pa

import bigframes.constants as constants

# Type hints for Pandas dtypes supported by BigQuery DataFrame
Dtype = Union[
    pd.BooleanDtype,
    pd.Float64Dtype,
    pd.Int64Dtype,
    pd.StringDtype,
    pd.ArrowDtype,
    gpd.array.GeometryDtype,
]
# Represents both column types (dtypes) and local-only types
# None represents the type of a None scalar.
ExpressionType = typing.Optional[Dtype]


INT_DTYPE = pd.Int64Dtype()
FLOAT_DTYPE = pd.Float64Dtype()
BOOL_DTYPE = pd.BooleanDtype()
STRING_DTYPE = pd.StringDtype(storage="pyarrow")
BYTES_DTYPE = pd.ArrowDtype(pa.binary())
DATE_DTYPE = pd.ArrowDtype(pa.date32())
TIME_DTYPE = pd.ArrowDtype(pa.time64("us"))
DATETIME_DTYPE = pd.ArrowDtype(pa.timestamp("us"))
TIMESTAMP_DTYPE = pd.ArrowDtype(pa.timestamp("us", tz="UTC"))
GEO_DTYPE = gpd.array.GeometryDtype()

# Used when storing Null expressions
DEFAULT_DTYPE = FLOAT_DTYPE

# Type hints for dtype strings supported by BigQuery DataFrame
DtypeString = Literal[
    "boolean",
    "Float64",
    "Int64",
    "int64[pyarrow]",
    "string",
    "string[pyarrow]",
    "timestamp[us, tz=UTC][pyarrow]",
    "timestamp[us][pyarrow]",
    "date32[day][pyarrow]",
    "time64[us][pyarrow]",
    "decimal128(38, 9)[pyarrow]",
    "decimal256(76, 38)[pyarrow]",
    "binary[pyarrow]",
]

BOOL_BIGFRAMES_TYPES = [pd.BooleanDtype()]

# Corresponds to the pandas concept of numeric type (such as when 'numeric_only' is specified in an operation)
# Pandas is inconsistent, so two definitions are provided, each used in different contexts
NUMERIC_BIGFRAMES_TYPES_RESTRICTIVE = [
    pd.Float64Dtype(),
    pd.Int64Dtype(),
]
NUMERIC_BIGFRAMES_TYPES_PERMISSIVE = NUMERIC_BIGFRAMES_TYPES_RESTRICTIVE + [
    pd.BooleanDtype(),
    pd.ArrowDtype(pa.decimal128(38, 9)),
    pd.ArrowDtype(pa.decimal256(76, 38)),
]


## dtype predicates - use these to maintain consistency
def is_datetime_like(type: ExpressionType) -> bool:
    return type in (DATETIME_DTYPE, TIMESTAMP_DTYPE)


def is_date_like(type: ExpressionType) -> bool:
    return type in (DATETIME_DTYPE, TIMESTAMP_DTYPE, DATE_DTYPE)


def is_time_like(type: ExpressionType) -> bool:
    return type in (DATETIME_DTYPE, TIMESTAMP_DTYPE, TIME_DTYPE)


def is_binary_like(type: ExpressionType) -> bool:
    return type in (BOOL_DTYPE, BYTES_DTYPE, INT_DTYPE)


def is_string_like(type: ExpressionType) -> bool:
    return type in (STRING_DTYPE, BYTES_DTYPE)


def is_array_like(type: ExpressionType) -> bool:
    return isinstance(type, pd.ArrowDtype) and isinstance(
        type.pyarrow_dtype, pa.ListType
    )


def is_array_string_like(type: ExpressionType) -> bool:
    return (
        isinstance(type, pd.ArrowDtype)
        and isinstance(type.pyarrow_dtype, pa.ListType)
        and pa.types.is_string(type.pyarrow_dtype.value_type)
    )


def is_struct_like(type: ExpressionType) -> bool:
    return isinstance(type, pd.ArrowDtype) and isinstance(
        type.pyarrow_dtype, pa.StructType
    )


def is_numeric(type: ExpressionType) -> bool:
    return type in NUMERIC_BIGFRAMES_TYPES_PERMISSIVE


def is_iterable(type: ExpressionType) -> bool:
    return type in (STRING_DTYPE, BYTES_DTYPE) or is_array_like(type)


def is_comparable(type: ExpressionType) -> bool:
    return (type is not None) and is_orderable(type)


def is_orderable(type: ExpressionType) -> bool:
    # On BQ side, ARRAY, STRUCT, GEOGRAPHY, JSON are not orderable
    return not is_array_like(type) and not is_struct_like(type) and (type != GEO_DTYPE)


def is_bool_coercable(type: ExpressionType) -> bool:
    # TODO: Implement more bool coercions
    return (type is None) or is_numeric(type) or is_string_like(type)


_ALL_DTYPES = (
    pd.BooleanDtype(),
    pd.ArrowDtype(pa.date32()),
    pd.Float64Dtype(),
    pd.Int64Dtype(),
    pd.StringDtype(storage="pyarrow"),
    pd.ArrowDtype(pa.time64("us")),
    pd.ArrowDtype(pa.timestamp("us")),
    pd.ArrowDtype(pa.timestamp("us", tz="UTC")),
    pd.ArrowDtype(pa.binary()),
    pd.ArrowDtype(pa.decimal128(38, 9)),
    pd.ArrowDtype(pa.decimal256(76, 38)),
    gpd.array.GeometryDtype(),
)

BIGFRAMES_STRING_TO_BIGFRAMES: Dict[DtypeString, Dtype] = {
    typing.cast(DtypeString, dtype.name): dtype for dtype in _ALL_DTYPES
}

# special case - string[pyarrow] doesn't include the storage in its name, and both
# "string" and "string[pyarrow]" are accepted
BIGFRAMES_STRING_TO_BIGFRAMES["string[pyarrow]"] = pd.StringDtype(storage="pyarrow")

# special case - both "Int64" and "int64[pyarrow]" are accepted
BIGFRAMES_STRING_TO_BIGFRAMES["int64[pyarrow]"] = pd.Int64Dtype()

# For the purposes of dataframe.memory_usage
# https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#data_type_sizes
DTYPE_BYTE_SIZES = {
    pd.BooleanDtype(): 1,
    pd.Int64Dtype(): 8,
    pd.Float32Dtype(): 8,
    pd.StringDtype(): 8,
    pd.ArrowDtype(pa.time64("us")): 8,
    pd.ArrowDtype(pa.timestamp("us")): 8,
    pd.ArrowDtype(pa.timestamp("us", tz="UTC")): 8,
    pd.ArrowDtype(pa.date32()): 8,
}


def dtype_for_etype(etype: ExpressionType) -> Dtype:
    if etype is None:
        return DEFAULT_DTYPE
    else:
        return etype


def arrow_dtype_to_bigframes_dtype(arrow_dtype: pa.DataType) -> Dtype:
    # TODO: Directly convert instead of using ibis dtype as intermediate step
    from bigframes.core.compile.ibis_types import (
        _arrow_dtype_to_ibis_dtype,
        ibis_dtype_to_bigframes_dtype,
    )

    return ibis_dtype_to_bigframes_dtype(_arrow_dtype_to_ibis_dtype(arrow_dtype))


def bigframes_dtype_to_arrow_dtype(
    bigframes_dtype: Union[DtypeString, Dtype, np.dtype[Any]]
) -> pa.DataType:
    # TODO: Directly convert instead of using ibis dtype as intermediate step
    from bigframes.core.compile.ibis_types import (
        _ibis_dtype_to_arrow_dtype,
        bigframes_dtype_to_ibis_dtype,
    )

    return _ibis_dtype_to_arrow_dtype(bigframes_dtype_to_ibis_dtype(bigframes_dtype))


def is_dtype(scalar: typing.Any, dtype: Dtype) -> bool:
    """Captures whether a scalar can be losslessly represented by a dtype."""
    if scalar is None:
        return True
    if pd.api.types.is_bool_dtype(dtype):
        return pd.api.types.is_bool(scalar)
    if pd.api.types.is_float_dtype(dtype):
        return pd.api.types.is_float(scalar)
    if pd.api.types.is_integer_dtype(dtype):
        return pd.api.types.is_integer(scalar)
    if isinstance(dtype, pd.StringDtype):
        return isinstance(scalar, str)
    if isinstance(dtype, pd.ArrowDtype):
        pa_type = dtype.pyarrow_dtype
        return is_patype(scalar, pa_type)
    return False


# string is binary
def is_patype(scalar: typing.Any, pa_type: pa.DataType) -> bool:
    """Determine whether a scalar's type matches a given pyarrow type."""
    if pa_type == pa.time64("us"):
        return isinstance(scalar, datetime.time)
    elif pa_type == pa.timestamp("us"):
        if isinstance(scalar, datetime.datetime):
            return not scalar.tzinfo
        if isinstance(scalar, pd.Timestamp):
            return not scalar.tzinfo
    elif pa_type == pa.timestamp("us", tz="UTC"):
        if isinstance(scalar, datetime.datetime):
            return scalar.tzinfo == datetime.timezone.utc
        if isinstance(scalar, pd.Timestamp):
            return scalar.tzinfo == datetime.timezone.utc
    elif pa_type == pa.date32():
        return isinstance(scalar, datetime.date)
    elif pa_type == pa.binary():
        return isinstance(scalar, bytes)
    elif pa_type == pa.decimal128(38, 9):
        # decimal.Decimal is a superset, but ibis performs out-of-bounds and loss-of-precision checks
        return isinstance(scalar, decimal.Decimal)
    elif pa_type == pa.decimal256(76, 38):
        # decimal.Decimal is a superset, but ibis performs out-of-bounds and loss-of-precision checks
        return isinstance(scalar, decimal.Decimal)
    return False


def is_compatible(scalar: typing.Any, dtype: Dtype) -> typing.Optional[Dtype]:
    """Whether scalar can be compare to items of dtype (though maybe requiring coercion). Returns the datatype that must be used for the comparison"""
    if is_dtype(scalar, dtype):
        return dtype
    elif pd.api.types.is_numeric_dtype(dtype):
        # Implicit conversion currently only supported for numeric types
        if pd.api.types.is_bool(scalar):
            return lcd_type(pd.BooleanDtype(), dtype)
        if pd.api.types.is_float(scalar):
            return lcd_type(pd.Float64Dtype(), dtype)
        if pd.api.types.is_integer(scalar):
            return lcd_type(pd.Int64Dtype(), dtype)
        if isinstance(scalar, decimal.Decimal):
            # TODO: Check context to see if can use NUMERIC instead of BIGNUMERIC
            return lcd_type(pd.ArrowDtype(pa.decimal256(76, 38)), dtype)
    return None


def lcd_type(*dtypes: Dtype) -> Dtype:
    if len(dtypes) < 1:
        raise ValueError("at least one dypes should be provided")
    if len(dtypes) == 1:
        return dtypes[0]
    unique_dtypes = set(dtypes)
    if len(unique_dtypes) == 1:
        return unique_dtypes.pop()
    # Implicit conversion currently only supported for numeric types
    hierarchy: list[Dtype] = [
        pd.BooleanDtype(),
        pd.Int64Dtype(),
        pd.ArrowDtype(pa.decimal128(38, 9)),
        pd.ArrowDtype(pa.decimal256(76, 38)),
        pd.Float64Dtype(),
    ]
    if any([dtype not in hierarchy for dtype in dtypes]):
        return None
    lcd_index = max([hierarchy.index(dtype) for dtype in dtypes])
    return hierarchy[lcd_index]


def coerce_to_common(etype1: ExpressionType, etype2: ExpressionType) -> ExpressionType:
    """Coerce types to a common type or throw a TypeError"""
    if etype1 is not None and etype2 is not None:
        common_supertype = lcd_type(etype1, etype2)
        if common_supertype is not None:
            return common_supertype
    if can_coerce(etype1, etype2):
        return etype2
    if can_coerce(etype2, etype1):
        return etype1
    raise TypeError(f"Cannot coerce {etype1} and {etype2} to a common type.")


def can_coerce(source_type: ExpressionType, target_type: ExpressionType) -> bool:
    if source_type is None:
        return True  # None can be coerced to any supported type
    else:
        return (source_type == STRING_DTYPE) and (
            target_type in (DATETIME_DTYPE, TIMESTAMP_DTYPE, TIME_DTYPE, DATE_DTYPE)
        )


def lcd_type_or_throw(dtype1: Dtype, dtype2: Dtype) -> Dtype:
    result = lcd_type(dtype1, dtype2)
    if result is None:
        raise NotImplementedError(
            f"BigFrames cannot upcast {dtype1} and {dtype2} to common type. {constants.FEEDBACK_LINK}"
        )
    return result


def infer_literal_type(literal) -> typing.Optional[Dtype]:
    if pd.isna(literal):
        return None  # Null value without a definite type
    # Temporary logic, use ibis inferred type
    from bigframes.core.compile.ibis_types import (
        ibis_dtype_to_bigframes_dtype,
        literal_to_ibis_scalar,
    )

    ibis_literal = literal_to_ibis_scalar(literal)
    return ibis_dtype_to_bigframes_dtype(ibis_literal.type())


def infer_literal_arrow_type(literal) -> typing.Optional[pa.DataType]:
    if pd.isna(literal):
        return None  # Null value without a definite type
    # Temporary logic, use ibis inferred type
    # TODO: Directly convert instead of using ibis dtype as intermediate step
    from bigframes.core.compile.ibis_types import (
        _ibis_dtype_to_arrow_dtype,
        literal_to_ibis_scalar,
    )

    ibis_literal = literal_to_ibis_scalar(literal)
    return _ibis_dtype_to_arrow_dtype(ibis_literal.type())


def bf_type_from_type_kind(bf_schema) -> Dict[str, Dtype]:
    """Converts bigquery sql type to the default bigframes dtype."""
    ibis_schema: ibis.Schema = third_party_ibis_bqtypes.BigQuerySchema.to_ibis(
        bf_schema
    )
    # TODO: Directly convert instead of using ibis dtype as intermediate step
    from bigframes.core.compile.ibis_types import ibis_dtype_to_bigframes_dtype

    return {
        name: ibis_dtype_to_bigframes_dtype(type) for name, type in ibis_schema.items()
    }


# Remote functions use only
# TODO: Refactor into remote function module

# Input and output types supported by BigQuery DataFrames remote functions.
# TODO(shobs): Extend the support to all types supported by BQ remote functions
# https://cloud.google.com/bigquery/docs/remote-functions#limitations
RF_SUPPORTED_IO_PYTHON_TYPES = {bool, bytes, float, int, str}

RF_SUPPORTED_IO_BIGQUERY_TYPEKINDS = {
    "BOOLEAN",
    "BOOL",
    "BYTES",
    "FLOAT",
    "FLOAT64",
    "INT64",
    "INTEGER",
    "STRING",
}
