# Copyright 2024 Google LLC
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
from __future__ import annotations

import textwrap
from typing import Any, cast, Dict, Iterable, Optional, Tuple, Union
import warnings

import bigframes_vendored.constants as constants
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

import bigframes.dtypes

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


BIDIRECTIONAL_MAPPINGS: Iterable[Tuple[IbisDtype, bigframes.dtypes.Dtype]] = (
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
    (
        ibis_dtypes.GeoSpatial(geotype="geography", srid=4326, nullable=True),
        gpd.array.GeometryDtype(),
    ),
)

BIGFRAMES_TO_IBIS: Dict[bigframes.dtypes.Dtype, ibis_dtypes.DataType] = {
    pandas: ibis for ibis, pandas in BIDIRECTIONAL_MAPPINGS
}
IBIS_TO_BIGFRAMES: Dict[ibis_dtypes.DataType, bigframes.dtypes.Dtype] = {
    ibis: pandas for ibis, pandas in BIDIRECTIONAL_MAPPINGS
}
# Allow REQUIRED fields to map correctly.
IBIS_TO_BIGFRAMES.update(
    {ibis.copy(nullable=False): pandas for ibis, pandas in BIDIRECTIONAL_MAPPINGS}
)
IBIS_TO_BIGFRAMES.update(
    {
        # TODO: Interval
    }
)


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
            ibis_dtypes.int64,
            ibis_dtypes.Decimal(precision=76, scale=38),
        ),
        ibis_dtypes.Decimal(precision=76, scale=38): (
            ibis_dtypes.float64,
            ibis_dtypes.int64,
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
        return cast(ibis_types.StringValue, value.cast(to_type)).capitalize()

    if value.type() == ibis_dtypes.bool and to_type == ibis_dtypes.float64:
        return value.cast(ibis_dtypes.int64).cast(ibis_dtypes.float64)

    if value.type() == ibis_dtypes.float64 and to_type == ibis_dtypes.bool:
        return value != ibis_types.literal(0)

    raise TypeError(
        f"Unsupported cast {value.type()} to {to_type}. {constants.FEEDBACK_LINK}"
    )


def ibis_value_to_canonical_type(value: ibis_types.Value) -> ibis_types.Value:
    """Converts an Ibis expression to canonical type.

    This is useful in cases where multiple types correspond to the same BigFrames dtype.
    """
    ibis_type = value.type()
    name = value.get_name()
    if ibis_type.is_json():
        value = vendored_ibis_ops.ToJsonString(value).to_expr()
        value = value.case().when("null", ibis.null()).else_(value).end()
        return value.name(name)
    # Allow REQUIRED fields to be joined with NULLABLE fields.
    nullable_type = ibis_type.copy(nullable=True)
    return value.cast(nullable_type).name(name)


def bigframes_dtype_to_ibis_dtype(
    bigframes_dtype: Union[
        bigframes.dtypes.DtypeString, bigframes.dtypes.Dtype, np.dtype[Any]
    ]
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
    if str(bigframes_dtype) in bigframes.dtypes.BIGFRAMES_STRING_TO_BIGFRAMES:
        bigframes_dtype = bigframes.dtypes.BIGFRAMES_STRING_TO_BIGFRAMES[
            cast(bigframes.dtypes.DtypeString, str(bigframes_dtype))
        ]

    if bigframes_dtype in BIGFRAMES_TO_IBIS.keys():
        return BIGFRAMES_TO_IBIS[bigframes_dtype]

    elif isinstance(bigframes_dtype, pd.ArrowDtype) and bigframes_dtype.pyarrow_dtype:
        return _arrow_dtype_to_ibis_dtype(bigframes_dtype.pyarrow_dtype)

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


def ibis_dtype_to_bigframes_dtype(
    ibis_dtype: ibis_dtypes.DataType,
) -> bigframes.dtypes.Dtype:
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
        return pd.ArrowDtype(_ibis_dtype_to_arrow_dtype(ibis_dtype))

    if isinstance(ibis_dtype, ibis_dtypes.Struct):
        return pd.ArrowDtype(_ibis_dtype_to_arrow_dtype(ibis_dtype))

    # BigQuery only supports integers of size 64 bits.
    if isinstance(ibis_dtype, ibis_dtypes.Integer):
        return pd.Int64Dtype()

    # Temporary: Will eventually support an explicit json type instead of casting to string.
    if isinstance(ibis_dtype, ibis_dtypes.JSON):
        warnings.warn(
            "Interpreting JSON as string. This behavior may change in future versions.",
            bigframes.exceptions.PreviewWarning,
        )
        return bigframes.dtypes.STRING_DTYPE

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


def _ibis_dtype_to_arrow_dtype(ibis_dtype: ibis_dtypes.DataType) -> pa.DataType:
    """Private utility to convert ibis dtype to equivalent arrow type."""
    if isinstance(ibis_dtype, ibis_dtypes.Array):
        return pa.list_(
            _ibis_dtype_to_arrow_dtype(ibis_dtype.value_type.copy(nullable=True))
        )

    if isinstance(ibis_dtype, ibis_dtypes.Struct):
        return pa.struct(
            [
                pa.field(
                    name,
                    _ibis_dtype_to_arrow_dtype(dtype),
                    nullable=not pa.types.is_list(_ibis_dtype_to_arrow_dtype(dtype)),
                )
                for name, dtype in ibis_dtype.fields.items()
            ]
        )

    if ibis_dtype in IBIS_TO_BIGFRAMES:
        dtype = IBIS_TO_BIGFRAMES[ibis_dtype]
        # Note: arrow mappings are incomplete, no geography type
        return bigframes.dtypes.bigframes_dtype_to_arrow_dtype(dtype)
    else:
        raise ValueError(
            f"Unexpected Ibis data type {ibis_dtype}. {constants.FEEDBACK_LINK}"
        )


_ARROW_TO_IBIS = {
    mapping.arrow_dtype: bigframes_dtype_to_ibis_dtype(mapping.dtype)
    for mapping in bigframes.dtypes.SIMPLE_TYPES
    if mapping.arrow_dtype is not None
}


def _arrow_dtype_to_ibis_dtype(arrow_dtype: pa.DataType) -> ibis_dtypes.DataType:
    if arrow_dtype == pa.null():
        # Used for empty local dataframes where pyarrow has null type
        return ibis_dtypes.float64
    if pa.types.is_struct(arrow_dtype):
        struct_dtype = cast(pa.StructType, arrow_dtype)
        return ibis_dtypes.Struct.from_tuples(
            [
                (field.name, _arrow_dtype_to_ibis_dtype(field.type))
                for field in struct_dtype
            ]
        )
    if pa.types.is_list(arrow_dtype):
        list_dtype = cast(pa.ListType, arrow_dtype)
        value_dtype = list_dtype.value_type
        value_ibis_type = _arrow_dtype_to_ibis_dtype(value_dtype)
        return ibis_dtypes.Array(value_type=value_ibis_type)
    elif arrow_dtype in _ARROW_TO_IBIS:
        return _ARROW_TO_IBIS[arrow_dtype]
    else:
        raise ValueError(f"Unexpected arrow type: {arrow_dtype}")


def literal_to_ibis_scalar(
    literal, force_dtype: Optional[bigframes.dtypes.Dtype] = None, validate: bool = True
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


class UnsupportedTypeError(ValueError):
    def __init__(self, type_, supported_types):
        self.type = type_
        self.supported_types = supported_types


def ibis_type_from_python_type(t: type) -> ibis_dtypes.DataType:
    if t not in bigframes.dtypes.RF_SUPPORTED_IO_PYTHON_TYPES:
        raise UnsupportedTypeError(t, bigframes.dtypes.RF_SUPPORTED_IO_PYTHON_TYPES)
    return python_type_to_bigquery_type(t)


def ibis_type_from_type_kind(tk: bigquery.StandardSqlTypeNames) -> ibis_dtypes.DataType:
    """Convert bq type to ibis. Only to be used for remote functions, does not handle all types."""
    if tk not in bigframes.dtypes.RF_SUPPORTED_IO_BIGQUERY_TYPEKINDS:
        raise UnsupportedTypeError(
            tk, bigframes.dtypes.RF_SUPPORTED_IO_BIGQUERY_TYPEKINDS
        )
    return third_party_ibis_bqtypes.BigQueryType.to_ibis(tk)
