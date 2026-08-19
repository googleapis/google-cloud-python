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
#
# DO NOT MODIFY THIS FILE DIRECTLY.
# This file was generated from: scripts/data/sql-functions/global_namespace/conversion.yaml
# by the script: scripts/generate_bigframes_bigquery.py

from __future__ import annotations

import datetime
from typing import Literal, Union

import bigframes.core.col
import bigframes.core.googlesql
import bigframes.core.sentinels as sentinels
import bigframes.series as series
from bigframes import dtypes
from bigframes.operations import googlesql

_BOOL_OP = googlesql.GoogleSqlScalarOp(
    "BOOL",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.BOOL_DTYPE,
)
_DOUBLE_OP = googlesql.GoogleSqlScalarOp(
    "DOUBLE",
    args=(
        googlesql.ArgSpec(),
        googlesql.ArgSpec(arg_name="wide_number_mode", optional=True),
    ),
    signature=lambda *args: dtypes.FLOAT_DTYPE,
)
_FLOAT64_OP = googlesql.GoogleSqlScalarOp(
    "FLOAT64",
    args=(
        googlesql.ArgSpec(),
        googlesql.ArgSpec(arg_name="wide_number_mode", optional=True),
    ),
    signature=lambda *args: dtypes.FLOAT_DTYPE,
)
_INT64_OP = googlesql.GoogleSqlScalarOp(
    "INT64",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.INT_DTYPE,
)
_PARSE_BIGNUMERIC_OP = googlesql.GoogleSqlScalarOp(
    "PARSE_BIGNUMERIC",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.BIGNUMERIC_DTYPE,
)
_PARSE_NUMERIC_OP = googlesql.GoogleSqlScalarOp(
    "PARSE_NUMERIC",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.NUMERIC_DTYPE,
)
_STRING_OP = googlesql.GoogleSqlScalarOp(
    "STRING",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=lambda *args: dtypes.STRING_DTYPE,
)


def bool_(
    json_string_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts a JSON boolean to a SQL BOOL value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _BOOL_OP,
        json_string_expression,
    )


def double(
    json_string_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
    wide_number_mode: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts a JSON number to a SQL FLOAT64 value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DOUBLE_OP,
        json_string_expression,
        wide_number_mode,
    )


def float64(
    json_string_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
    wide_number_mode: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts a JSON number to a SQL FLOAT64 value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _FLOAT64_OP,
        json_string_expression,
        wide_number_mode,
    )


def int64(
    json_string_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts a JSON number to a SQL INT64 value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _INT64_OP,
        json_string_expression,
    )


def parse_bignumeric(
    string_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts a STRING to a BIGNUMERIC value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _PARSE_BIGNUMERIC_OP,
        string_expression,
    )


def parse_numeric(
    string_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts a STRING to a NUMERIC value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _PARSE_NUMERIC_OP,
        string_expression,
    )


def string(
    expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
            datetime.time,
            str,
        ],
    ],
    timezone: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts a value to a STRING value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _STRING_OP,
        expression,
        timezone,
    )
