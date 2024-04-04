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
import textwrap
import typing
from typing import Any, Dict, Iterable, Literal, Tuple, Union

import bigframes_vendored.ibis.backends.bigquery.datatypes as third_party_ibis_bqtypes
import bigframes_vendored.ibis.expr.operations as vendored_ibis_ops
import geopandas as gpd  # type: ignore
import google.cloud.bigquery as bigquery
import ibis
import ibis.expr.datatypes as ibis_dtypes
from ibis.expr.datatypes.core import dtype as python_type_to_bigquery_type
import ibis.expr.types as ibis_types
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

# Used when storing Null expressions
DEFAULT_DTYPE = FLOAT_DTYPE

# On BQ side, ARRAY, STRUCT, GEOGRAPHY, JSON are not orderable
UNORDERED_DTYPES = [gpd.array.GeometryDtype()]

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

# Type hints for Ibis data types supported by BigQuery DataFrame
IbisDtype = Union[
    ibis_dtypes.Boolean,
    ibis_dtypes.Float64,
    ibis_dtypes.Int64,
    ibis_dtypes.String,
    ibis_dtypes.Date,
    ibis_dtypes.Time,
    ibis_dtypes.Timestamp,
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


def is_numeric(type: ExpressionType) -> bool:
    return type in NUMERIC_BIGFRAMES_TYPES_PERMISSIVE


def is_iterable(type: ExpressionType) -> bool:
    return type in (STRING_DTYPE, BYTES_DTYPE) or is_array_like(type)


def is_comparable(type: ExpressionType) -> bool:
    return (type is not None) and (type not in UNORDERED_DTYPES)


# Type hints for Ibis data types that can be read to Python objects by BigQuery DataFrame
ReadOnlyIbisDtype = Union[
    ibis_dtypes.Binary,
    ibis_dtypes.JSON,
    ibis_dtypes.Decimal,
    ibis_dtypes.GeoSpatial,
    ibis_dtypes.Array,
    ibis_dtypes.Struct,
]

BIDIRECTIONAL_MAPPINGS: Iterable[Tuple[IbisDtype, Dtype]] = (
    (ibis_dtypes.boolean, pd.BooleanDtype()),
    (ibis_dtypes.date, pd.ArrowDtype(pa.date32())),
    (ibis_dtypes.float64, pd.Float64Dtype()),
    (ibis_dtypes.int64, pd.Int64Dtype()),
    (ibis_dtypes.string, pd.StringDtype(storage="pyarrow")),
    (ibis_dtypes.time, pd.ArrowDtype(pa.time64("us"))),
    (ibis_dtypes.Timestamp(timezone=None), pd.ArrowDtype(pa.timestamp("us"))),
    (
        ibis_dtypes.Timestamp(timezone="UTC"),
        pd.ArrowDtype(pa.timestamp("us", tz="UTC")),
    ),
    (ibis_dtypes.binary, pd.ArrowDtype(pa.binary())),
    (
        ibis_dtypes.Decimal(precision=38, scale=9, nullable=True),
        pd.ArrowDtype(pa.decimal128(38, 9)),
    ),
    (
        ibis_dtypes.Decimal(precision=76, scale=38, nullable=True),
        pd.ArrowDtype(pa.decimal256(76, 38)),
    ),
)

BIGFRAMES_TO_IBIS: Dict[Dtype, ibis_dtypes.DataType] = {
    pandas: ibis for ibis, pandas in BIDIRECTIONAL_MAPPINGS
}

IBIS_TO_ARROW: Dict[ibis_dtypes.DataType, pa.DataType] = {
    ibis_dtypes.boolean: pa.bool_(),
    ibis_dtypes.date: pa.date32(),
    ibis_dtypes.float64: pa.float64(),
    ibis_dtypes.int64: pa.int64(),
    ibis_dtypes.string: pa.string(),
    ibis_dtypes.time: pa.time64("us"),
    ibis_dtypes.Timestamp(timezone=None): pa.timestamp("us"),
    ibis_dtypes.Timestamp(timezone="UTC"): pa.timestamp("us", tz="UTC"),
    ibis_dtypes.binary: pa.binary(),
    ibis_dtypes.Decimal(precision=38, scale=9, nullable=True): pa.decimal128(38, 9),
    ibis_dtypes.Decimal(precision=76, scale=38, nullable=True): pa.decimal256(76, 38),
}

ARROW_TO_IBIS = {arrow: ibis for ibis, arrow in IBIS_TO_ARROW.items()}

IBIS_TO_BIGFRAMES: Dict[ibis_dtypes.DataType, Dtype] = {
    ibis: pandas for ibis, pandas in BIDIRECTIONAL_MAPPINGS
}
# Allow REQUIRED fields to map correctly.
IBIS_TO_BIGFRAMES.update(
    {ibis.copy(nullable=False): pandas for ibis, pandas in BIDIRECTIONAL_MAPPINGS}
)
IBIS_TO_BIGFRAMES.update(
    {
        ibis_dtypes.GeoSpatial(
            geotype="geography", srid=4326, nullable=True
        ): gpd.array.GeometryDtype(),
        # TODO: Interval
    }
)

BIGFRAMES_STRING_TO_BIGFRAMES: Dict[DtypeString, Dtype] = {
    typing.cast(DtypeString, dtype.name): dtype for dtype in BIGFRAMES_TO_IBIS.keys()
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


def ibis_dtype_to_bigframes_dtype(
    ibis_dtype: ibis_dtypes.DataType,
) -> Dtype:
    """Converts an Ibis dtype to a BigQuery DataFrames dtype

    Args:
        ibis_dtype: The ibis dtype used to represent this type, which
        should in turn correspond to an underlying BigQuery type

    Returns:
        The supported BigQuery DataFrames dtype, which may be provided by
        pandas, numpy, or db_types

    Raises:
        ValueError: if passed an unexpected type
    """
    # Special cases: Ibis supports variations on these types, but currently
    # our IO returns them as objects. Eventually, we should support them as
    # ArrowDType (and update the IO accordingly)
    if isinstance(ibis_dtype, ibis_dtypes.Array):
        return pd.ArrowDtype(ibis_dtype_to_arrow_dtype(ibis_dtype))

    if isinstance(ibis_dtype, ibis_dtypes.Struct):
        return pd.ArrowDtype(ibis_dtype_to_arrow_dtype(ibis_dtype))

    # BigQuery only supports integers of size 64 bits.
    if isinstance(ibis_dtype, ibis_dtypes.Integer):
        return pd.Int64Dtype()

    if ibis_dtype in IBIS_TO_BIGFRAMES:
        return IBIS_TO_BIGFRAMES[ibis_dtype]
    elif isinstance(ibis_dtype, ibis_dtypes.Decimal):
        # Temporary workaround for ibis decimal issue (b/323387826)
        if ibis_dtype.precision >= 76:
            return pd.ArrowDtype(pa.decimal256(76, 38))
        else:
            return pd.ArrowDtype(pa.decimal128(38, 9))
    elif isinstance(ibis_dtype, ibis_dtypes.Null):
        # Fallback to STRING for NULL values for most flexibility in SQL.
        return IBIS_TO_BIGFRAMES[ibis_dtypes.string]
    else:
        raise ValueError(
            f"Unexpected Ibis data type {ibis_dtype}. {constants.FEEDBACK_LINK}"
        )


def ibis_dtype_to_arrow_dtype(ibis_dtype: ibis_dtypes.DataType) -> pa.DataType:
    if isinstance(ibis_dtype, ibis_dtypes.Array):
        return pa.list_(
            ibis_dtype_to_arrow_dtype(ibis_dtype.value_type.copy(nullable=True))
        )

    if isinstance(ibis_dtype, ibis_dtypes.Struct):
        return pa.struct(
            [
                (name, ibis_dtype_to_arrow_dtype(dtype))
                for name, dtype in ibis_dtype.fields.items()
            ]
        )

    if ibis_dtype in IBIS_TO_ARROW:
        return IBIS_TO_ARROW[ibis_dtype]
    else:
        raise ValueError(
            f"Unexpected Ibis data type {ibis_dtype}. {constants.FEEDBACK_LINK}"
        )


def ibis_value_to_canonical_type(value: ibis_types.Value) -> ibis_types.Value:
    """Converts an Ibis expression to canonical type.

    This is useful in cases where multiple types correspond to the same BigFrames dtype.
    """
    ibis_type = value.type()
    name = value.get_name()
    if ibis_type.is_json():
        value = vendored_ibis_ops.ToJsonString(value).to_expr()
        return value.name(name)
    # Allow REQUIRED fields to be joined with NULLABLE fields.
    nullable_type = ibis_type.copy(nullable=True)
    return value.cast(nullable_type).name(name)


def arrow_dtype_to_ibis_dtype(arrow_dtype: pa.DataType) -> ibis_dtypes.DataType:
    if pa.types.is_struct(arrow_dtype):
        struct_dtype = typing.cast(pa.StructType, arrow_dtype)
        return ibis_dtypes.Struct.from_tuples(
            [
                (field.name, arrow_dtype_to_ibis_dtype(field.type))
                for field in struct_dtype
            ]
        )

    if arrow_dtype in ARROW_TO_IBIS:
        return ARROW_TO_IBIS[arrow_dtype]
    if arrow_dtype == pa.null():
        # Used for empty local dataframes where pyarrow has null type
        return ibis_dtypes.float64
    else:
        raise ValueError(
            f"Unexpected Arrow data type {arrow_dtype}. {constants.FEEDBACK_LINK}"
        )


def arrow_dtype_to_bigframes_dtype(arrow_dtype: pa.DataType) -> Dtype:
    return ibis_dtype_to_bigframes_dtype(arrow_dtype_to_ibis_dtype(arrow_dtype))


def bigframes_dtype_to_ibis_dtype(
    bigframes_dtype: Union[DtypeString, Dtype, np.dtype[Any]]
) -> ibis_dtypes.DataType:
    """Converts a BigQuery DataFrames supported dtype to an Ibis dtype.

    Args:
        bigframes_dtype:
            A dtype supported by BigQuery DataFrame

    Returns:
        IbisDtype: The corresponding Ibis type

    Raises:
        ValueError: If passed a dtype not supported by BigQuery DataFrames.
    """
    if isinstance(bigframes_dtype, pd.ArrowDtype):
        return arrow_dtype_to_ibis_dtype(bigframes_dtype.pyarrow_dtype)

    type_string = str(bigframes_dtype)
    if type_string in BIGFRAMES_STRING_TO_BIGFRAMES:
        bigframes_dtype = BIGFRAMES_STRING_TO_BIGFRAMES[
            typing.cast(DtypeString, type_string)
        ]
    else:
        raise ValueError(
            textwrap.dedent(
                f"""
                Unexpected data type {bigframes_dtype}. The following
                        str dtypes are supppted: 'boolean','Float64','Int64',
                        'int64[pyarrow]','string','string[pyarrow]',
                        'timestamp[us, tz=UTC][pyarrow]','timestamp[us][pyarrow]',
                        'date32[day][pyarrow]','time64[us][pyarrow]'.
                        The following pandas.ExtensionDtype are supported:
                        pandas.BooleanDtype(), pandas.Float64Dtype(),
                        pandas.Int64Dtype(), pandas.StringDtype(storage="pyarrow"),
                        pd.ArrowDtype(pa.date32()), pd.ArrowDtype(pa.time64("us")),
                        pd.ArrowDtype(pa.timestamp("us")),
                        pd.ArrowDtype(pa.timestamp("us", tz="UTC")).
                {constants.FEEDBACK_LINK}
                """
            )
        )

    return BIGFRAMES_TO_IBIS[bigframes_dtype]


def literal_to_ibis_scalar(
    literal, force_dtype: typing.Optional[Dtype] = None, validate: bool = True
):
    """Accept any literal and, if possible, return an Ibis Scalar
    expression with a BigQuery DataFrames compatible data type

    Args:
        literal:
            any value accepted by Ibis
        force_dtype:
            force the value to a specific dtype
        validate:
            If true, will raise ValueError if type cannot be stored in a
            BigQuery DataFrames object. If used as a subexpression, this should
            be disabled.

    Returns:
        An ibis Scalar supported by BigQuery DataFrame

    Raises:
        ValueError: if passed literal cannot be coerced to a
        BigQuery DataFrames compatible scalar
    """
    # Special case: Can create nulls for non-bidirectional types
    if (force_dtype == gpd.array.GeometryDtype()) and pd.isna(literal):
        # Ibis has bug for casting nulltype to geospatial, so we perform intermediate cast first
        geotype = ibis_dtypes.GeoSpatial(geotype="geography", srid=4326, nullable=True)
        return ibis.literal(None, geotype)
    ibis_dtype = BIGFRAMES_TO_IBIS[force_dtype] if force_dtype else None

    if pd.api.types.is_list_like(literal):
        if validate:
            raise ValueError(
                f"List types can't be stored in BigQuery DataFrames. {constants.FEEDBACK_LINK}"
            )
        # "correct" way would be to use ibis.array, but this produces invalid BQ SQL syntax
        return tuple(literal)
    if not pd.api.types.is_list_like(literal) and pd.isna(literal):
        if ibis_dtype:
            return ibis.null().cast(ibis_dtype)
        else:
            return ibis.null()

    scalar_expr = ibis.literal(literal)
    if ibis_dtype:
        scalar_expr = ibis.literal(literal, ibis_dtype)
    elif scalar_expr.type().is_floating():
        scalar_expr = ibis.literal(literal, ibis_dtypes.float64)
    elif scalar_expr.type().is_integer():
        scalar_expr = ibis.literal(literal, ibis_dtypes.int64)
    elif scalar_expr.type().is_decimal():
        precision = scalar_expr.type().precision
        scale = scalar_expr.type().scale
        if (not precision and not scale) or (
            precision and scale and scale <= 9 and precision + (9 - scale) <= 38
        ):
            scalar_expr = ibis.literal(
                literal, ibis_dtypes.decimal(precision=38, scale=9)
            )
        elif precision and scale and scale <= 38 and precision + (38 - scale) <= 76:
            scalar_expr = ibis.literal(
                literal, ibis_dtypes.decimal(precision=76, scale=38)
            )
        else:
            raise TypeError(
                "BigQuery's decimal data type supports a maximum precision of 76 and a maximum scale of 38."
                f"Current precision: {precision}. Current scale: {scale}"
            )

    # TODO(bmil): support other literals that can be coerced to compatible types
    if validate and (scalar_expr.type() not in BIGFRAMES_TO_IBIS.values()):
        raise ValueError(
            f"Literal did not coerce to a supported data type: {scalar_expr.type()}. {constants.FEEDBACK_LINK}"
        )

    return scalar_expr


def cast_ibis_value(
    value: ibis_types.Value, to_type: ibis_dtypes.DataType
) -> ibis_types.Value:
    """Perform compatible type casts of ibis values

    Args:
        value:
            Ibis value, which could be a literal, scalar, or column

        to_type:
            The Ibis type to cast to

    Returns:
        A new Ibis value of type to_type

    Raises:
        TypeError: if the type cast cannot be executed"""
    if value.type() == to_type:
        return value
    # casts that just work
    # TODO(bmil): add to this as more casts are verified
    good_casts = {
        ibis_dtypes.bool: (ibis_dtypes.int64,),
        ibis_dtypes.int64: (
            ibis_dtypes.bool,
            ibis_dtypes.float64,
            ibis_dtypes.string,
            ibis_dtypes.Decimal(precision=38, scale=9),
            ibis_dtypes.Decimal(precision=76, scale=38),
            ibis_dtypes.time,
            ibis_dtypes.timestamp,
            ibis_dtypes.Timestamp(timezone="UTC"),
        ),
        ibis_dtypes.float64: (
            ibis_dtypes.string,
            ibis_dtypes.int64,
            ibis_dtypes.Decimal(precision=38, scale=9),
            ibis_dtypes.Decimal(precision=76, scale=38),
        ),
        ibis_dtypes.string: (
            ibis_dtypes.int64,
            ibis_dtypes.float64,
            ibis_dtypes.Decimal(precision=38, scale=9),
            ibis_dtypes.Decimal(precision=76, scale=38),
            ibis_dtypes.binary,
            ibis_dtypes.date,
            ibis_dtypes.timestamp,
            ibis_dtypes.Timestamp(timezone="UTC"),
        ),
        ibis_dtypes.date: (
            ibis_dtypes.string,
            ibis_dtypes.timestamp,
            ibis_dtypes.Timestamp(timezone="UTC"),
        ),
        ibis_dtypes.Decimal(precision=38, scale=9): (
            ibis_dtypes.float64,
            ibis_dtypes.Decimal(precision=76, scale=38),
        ),
        ibis_dtypes.Decimal(precision=76, scale=38): (
            ibis_dtypes.float64,
            ibis_dtypes.Decimal(precision=38, scale=9),
        ),
        ibis_dtypes.time: (
            ibis_dtypes.int64,
            ibis_dtypes.string,
        ),
        ibis_dtypes.timestamp: (
            ibis_dtypes.date,
            ibis_dtypes.int64,
            ibis_dtypes.string,
            ibis_dtypes.time,
            ibis_dtypes.Timestamp(timezone="UTC"),
        ),
        ibis_dtypes.Timestamp(timezone="UTC"): (
            ibis_dtypes.date,
            ibis_dtypes.int64,
            ibis_dtypes.string,
            ibis_dtypes.time,
            ibis_dtypes.timestamp,
        ),
        ibis_dtypes.binary: (ibis_dtypes.string,),
    }

    value = ibis_value_to_canonical_type(value)
    if value.type() in good_casts:
        if to_type in good_casts[value.type()]:
            return value.cast(to_type)
    else:
        # this should never happen
        raise TypeError(
            f"Unexpected value type {value.type()}. {constants.FEEDBACK_LINK}"
        )

    # casts that need some encouragement

    # BigQuery casts bools to lower case strings. Capitalize the result to match Pandas
    # TODO(bmil): remove this workaround after fixing Ibis
    if value.type() == ibis_dtypes.bool and to_type == ibis_dtypes.string:
        return typing.cast(ibis_types.StringValue, value.cast(to_type)).capitalize()

    if value.type() == ibis_dtypes.bool and to_type == ibis_dtypes.float64:
        return value.cast(ibis_dtypes.int64).cast(ibis_dtypes.float64)

    if value.type() == ibis_dtypes.float64 and to_type == ibis_dtypes.bool:
        return value != ibis_types.literal(0)

    raise TypeError(
        f"Unsupported cast {value.type()} to {to_type}. {constants.FEEDBACK_LINK}"
    )


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


def lcd_type(dtype1: Dtype, dtype2: Dtype) -> Dtype:
    """Get the supertype of the two types."""
    if dtype1 == dtype2:
        return dtype1
    # Implicit conversion currently only supported for numeric types
    hierarchy: list[Dtype] = [
        pd.BooleanDtype(),
        pd.Int64Dtype(),
        pd.ArrowDtype(pa.decimal128(38, 9)),
        pd.ArrowDtype(pa.decimal256(76, 38)),
        pd.Float64Dtype(),
    ]
    if (dtype1 not in hierarchy) or (dtype2 not in hierarchy):
        return None
    lcd_index = max(hierarchy.index(dtype1), hierarchy.index(dtype2))
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
    ibis_literal = literal_to_ibis_scalar(literal)
    return ibis_dtype_to_bigframes_dtype(ibis_literal.type())


def infer_literal_arrow_type(literal) -> typing.Optional[pa.DataType]:
    if pd.isna(literal):
        return None  # Null value without a definite type
    # Temporary logic, use ibis inferred type
    ibis_literal = literal_to_ibis_scalar(literal)
    return ibis_dtype_to_arrow_dtype(ibis_literal.type())


# Input and output types supported by BigQuery DataFrames remote functions.
# TODO(shobs): Extend the support to all types supported by BQ remote functions
# https://cloud.google.com/bigquery/docs/remote-functions#limitations
SUPPORTED_IO_PYTHON_TYPES = {bool, float, int, str}
SUPPORTED_IO_BIGQUERY_TYPEKINDS = {
    "BOOLEAN",
    "BOOL",
    "FLOAT",
    "FLOAT64",
    "INT64",
    "INTEGER",
    "STRING",
}


class UnsupportedTypeError(ValueError):
    def __init__(self, type_, supported_types):
        self.type = type_
        self.supported_types = supported_types


def ibis_type_from_python_type(t: type) -> ibis_dtypes.DataType:
    if t not in SUPPORTED_IO_PYTHON_TYPES:
        raise UnsupportedTypeError(t, SUPPORTED_IO_PYTHON_TYPES)
    return python_type_to_bigquery_type(t)


def ibis_type_from_type_kind(tk: bigquery.StandardSqlTypeNames) -> ibis_dtypes.DataType:
    """Convert bq type to ibis. Only to be used for remote functions, does not handle all types."""
    if tk not in SUPPORTED_IO_BIGQUERY_TYPEKINDS:
        raise UnsupportedTypeError(tk, SUPPORTED_IO_BIGQUERY_TYPEKINDS)
    return third_party_ibis_bqtypes.BigQueryType.to_ibis(tk)


def bf_type_from_type_kind(bf_schema) -> Dict[str, Dtype]:
    """Converts bigquery sql type to the default bigframes dtype."""
    ibis_schema: ibis.Schema = third_party_ibis_bqtypes.BigQuerySchema.to_ibis(
        bf_schema
    )
    return {
        name: ibis_dtype_to_bigframes_dtype(type) for name, type in ibis_schema.items()
    }
