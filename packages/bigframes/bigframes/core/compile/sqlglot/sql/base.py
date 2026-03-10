# Copyright 2026 Google LLC
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

import typing

import bigframes_vendored.sqlglot as sg
import bigframes_vendored.sqlglot.expressions as sge
from google.cloud import bigquery
import numpy as np
import pandas as pd
import pyarrow as pa

from bigframes import dtypes
from bigframes.core import utils
from bigframes.core.compile.sqlglot.expressions import constants
import bigframes.core.compile.sqlglot.sqlglot_types as sgt

# shapely.wkt.dumps was moved to shapely.io.to_wkt in 2.0.
try:
    from shapely.io import to_wkt  # type: ignore
except ImportError:
    from shapely.wkt import dumps  # type: ignore

    to_wkt = dumps


QUOTED: bool = True
"""Whether to quote identifiers in the generated SQL."""

PRETTY: bool = True
"""Whether to pretty-print the generated SQL."""

DIALECT = sg.dialects.bigquery.BigQuery
"""The SQL dialect used for generation."""


def to_sql(expr: sge.Expression) -> str:
    """Generate SQL string from the given expression."""
    return expr.sql(dialect=DIALECT, pretty=PRETTY)


def identifier(id: str) -> sge.Identifier:
    """Return a string representing column reference in a SQL."""
    return sge.to_identifier(id, quoted=QUOTED)


def literal(value: typing.Any, dtype: dtypes.Dtype | None = None) -> sge.Expression:
    """Return a string representing column reference in a SQL."""
    if dtype is None:
        dtype = dtypes.infer_literal_type(value)

    sqlglot_type = sgt.from_bigframes_dtype(dtype) if dtype else None
    if sqlglot_type is None:
        if not pd.isna(value):
            raise ValueError(f"Cannot infer SQLGlot type from None dtype: {value}")
        return sge.Null()

    if value is None:
        return cast(sge.Null(), sqlglot_type)
    if dtypes.is_struct_like(dtype):
        items = [
            literal(value=value[field_name], dtype=field_dtype).as_(
                field_name, quoted=True
            )
            for field_name, field_dtype in dtypes.get_struct_fields(dtype).items()
        ]
        return sge.Struct.from_arg_list(items)
    elif dtypes.is_array_like(dtype):
        value_type = dtypes.get_array_inner_type(dtype)
        values = sge.Array(
            expressions=[literal(value=v, dtype=value_type) for v in value]
        )
        return values if len(value) > 0 else cast(values, sqlglot_type)
    elif dtype == dtypes.FLOAT_DTYPE:
        if pd.isna(value):
            if isinstance(value, (float, np.floating)) and np.isnan(value):
                return constants._NAN
            return cast(sge.Null(), sqlglot_type)
        if np.isinf(value):
            return constants._INF if value > 0 else constants._NEG_INF
        return sge.convert(value)
    elif pd.isna(value) or (isinstance(value, pa.Scalar) and not value.is_valid):
        return cast(sge.Null(), sqlglot_type)
    elif dtype == dtypes.JSON_DTYPE:
        return sge.ParseJSON(this=sge.convert(str(value)))
    elif dtype == dtypes.BYTES_DTYPE:
        return cast(str(value), sqlglot_type)
    elif dtypes.is_time_like(dtype):
        if isinstance(value, str):
            return cast(sge.convert(value), sqlglot_type)
        if isinstance(value, np.generic):
            value = value.item()
        return cast(sge.convert(value.isoformat()), sqlglot_type)
    elif dtype in (dtypes.NUMERIC_DTYPE, dtypes.BIGNUMERIC_DTYPE):
        return cast(sge.convert(value), sqlglot_type)
    elif dtypes.is_geo_like(dtype):
        wkt = value if isinstance(value, str) else to_wkt(value)
        return sge.func("ST_GEOGFROMTEXT", sge.convert(wkt))
    elif dtype == dtypes.TIMEDELTA_DTYPE:
        return sge.convert(utils.timedelta_to_micros(value))
    else:
        if isinstance(value, np.generic):
            value = value.item()
        if isinstance(value, pa.Scalar):
            value = value.as_py()
        return sge.convert(value)


def cast(arg: typing.Any, to: str, safe: bool = False) -> sge.Cast | sge.TryCast:
    """Return a SQL expression that casts the given argument to the specified type."""
    if safe:
        return sge.TryCast(this=arg, to=to)
    else:
        return sge.Cast(this=arg, to=to)


def table(table: bigquery.TableReference) -> sge.Table:
    """Return a SQLGlot Table expression representing the given BigQuery table reference."""
    return sge.Table(
        this=sge.to_identifier(table.table_id, quoted=True),
        db=sge.to_identifier(table.dataset_id, quoted=True),
        catalog=sge.to_identifier(table.project, quoted=True),
    )


def escape_chars(value: str):
    """Escapes all special characters"""
    # TODO: Reuse literal's escaping logic instead of re-implementing it here.
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#string_and_bytes_literals
    trans_table = str.maketrans(
        {
            "\a": r"\a",
            "\b": r"\b",
            "\f": r"\f",
            "\n": r"\n",
            "\r": r"\r",
            "\t": r"\t",
            "\v": r"\v",
            "\\": r"\\",
            "?": r"\?",
            '"': r"\"",
            "'": r"\'",
            "`": r"\`",
        }
    )
    return value.translate(trans_table)


def is_null_literal(expr: sge.Expression) -> bool:
    """Checks if the given expression is a NULL literal."""
    if isinstance(expr, sge.Null):
        return True
    if isinstance(expr, sge.Cast) and isinstance(expr.this, sge.Null):
        return True
    return False
