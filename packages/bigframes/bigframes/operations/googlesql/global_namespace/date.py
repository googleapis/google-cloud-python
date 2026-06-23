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
# This file was generated from: scripts/data/sql-functions/global_namespace/date.yaml
# by the script: scripts/generate_bigframes_bigquery.py

from __future__ import annotations

import datetime
from typing import Any, Literal, Union

import bigframes.core.col
import bigframes.core.googlesql
import bigframes.core.sentinels as sentinels
import bigframes.series as series
from bigframes import dtypes
from bigframes.operations import googlesql

_CURRENT_DATE_OP = googlesql.GoogleSqlScalarOp(
    "CURRENT_DATE",
    args=(googlesql.ArgSpec(optional=True),),
    signature=lambda *args: dtypes.DATE_DTYPE,
)
_DATE_OP = googlesql.GoogleSqlScalarOp(
    "DATE",
    args=(
        googlesql.ArgSpec(optional=True),
        googlesql.ArgSpec(optional=True),
        googlesql.ArgSpec(optional=True),
        googlesql.ArgSpec(optional=True),
        googlesql.ArgSpec(optional=True),
    ),
    signature=lambda *args: dtypes.DATE_DTYPE,
)
_DATE_ADD_OP = googlesql.GoogleSqlScalarOp(
    "DATE_ADD",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.DATE_DTYPE,
)
_DATE_DIFF_OP = googlesql.GoogleSqlScalarOp(
    "DATE_DIFF",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.INT_DTYPE,
)
_DATE_FROM_UNIX_DATE_OP = googlesql.GoogleSqlScalarOp(
    "DATE_FROM_UNIX_DATE",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.DATE_DTYPE,
)
_DATE_SUB_OP = googlesql.GoogleSqlScalarOp(
    "DATE_SUB",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.DATE_DTYPE,
)
_DATE_TRUNC_OP = googlesql.GoogleSqlScalarOp(
    "DATE_TRUNC",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.DATE_DTYPE,
)
_EXTRACT_OP = googlesql.GoogleSqlScalarOp(
    "EXTRACT",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=lambda *args: dtypes.INT_DTYPE,
)
_FORMAT_DATE_OP = googlesql.GoogleSqlScalarOp(
    "FORMAT_DATE",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.STRING_DTYPE,
)
_GENERATE_DATE_ARRAY_OP = googlesql.GoogleSqlScalarOp(
    "GENERATE_DATE_ARRAY",
    args=(
        googlesql.ArgSpec(),
        googlesql.ArgSpec(),
        googlesql.ArgSpec(optional=True),
        googlesql.ArgSpec(optional=True),
    ),
    signature=lambda *args: dtypes.list_type(dtypes.DATE_DTYPE),
)
_LAST_DAY_OP = googlesql.GoogleSqlScalarOp(
    "LAST_DAY",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=lambda *args: dtypes.DATE_DTYPE,
)
_PARSE_DATE_OP = googlesql.GoogleSqlScalarOp(
    "PARSE_DATE",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.DATE_DTYPE,
)
_UNIX_DATE_OP = googlesql.GoogleSqlScalarOp(
    "UNIX_DATE",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.INT_DTYPE,
)


def current_date(
    time_zone_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns the current date as a DATE object. Parentheses are optional when called with no arguments."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _CURRENT_DATE_OP,
        time_zone_expression,
    )


def date(
    expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
            str,
        ],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
    time_zone_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
    year: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
    month: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
    day: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Constructs or extracts a date."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DATE_OP,
        expression,
        time_zone_expression,
        year,
        month,
        day,
    )


def date_add(
    date_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
    int64_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ],
    date_part: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Adds a specified time interval to a DATE."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DATE_ADD_OP,
        date_expression,
        int64_expression,
        date_part,
    )


def date_diff(
    end_date: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
    start_date: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
    granularity: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Gets the number of unit boundaries between two DATE values (end_date - start_date) at a particular time granularity."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DATE_DIFF_OP,
        end_date,
        start_date,
        granularity,
    )


def date_from_unix_date(
    int64_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Interprets an INT64 expression as the number of days since 1970-01-01."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DATE_FROM_UNIX_DATE_OP,
        int64_expression,
    )


def date_sub(
    date_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
    int64_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ],
    date_part: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Subtracts a specified time interval from a DATE."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DATE_SUB_OP,
        date_expression,
        int64_expression,
        date_part,
    )


def date_trunc(
    date_value: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
    granularity: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Truncates a DATE, DATETIME, or TIMESTAMP value at a particular granularity."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DATE_TRUNC_OP,
        date_value,
        granularity,
    )


def extract(
    date_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
            datetime.time,
        ],
    ],
    part: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    time_zone: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns the value corresponding to the specified date part."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _EXTRACT_OP,
        date_expression,
        part,
        time_zone,
    )


def format_date(
    format_string: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
    date_expr: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Formats a DATE value according to a specified format string."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _FORMAT_DATE_OP,
        format_string,
        date_expr,
    )


def generate_date_array(
    start_date: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
    end_date: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
    int64_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
    date_part: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Generates an array of dates in a range."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _GENERATE_DATE_ARRAY_OP,
        start_date,
        end_date,
        int64_expression,
        date_part,
    )


def last_day(
    date_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
    date_part: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns the last day from a date expression. This is commonly used to return the last day of the month."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _LAST_DAY_OP,
        date_expression,
        date_part,
    )


def parse_date(
    format_string: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
    date_string: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts a STRING value to a DATE value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _PARSE_DATE_OP,
        format_string,
        date_string,
    )


def unix_date(
    date_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.date],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns the number of days since 1970-01-01."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _UNIX_DATE_OP,
        date_expression,
    )
