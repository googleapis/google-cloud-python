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


def _DATE_ADD_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (3 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if dtypes.coerce_to_common(args[0], dtypes.DATE_DTYPE) != dtypes.DATE_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if dtypes.coerce_to_common(args[1], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[2])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[2]
    if match_ok:
        return dtypes.DATE_DTYPE

    # Try matching impl 1
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if dtypes.coerce_to_common(args[1], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[2])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[2]
    if match_ok:
        return dtypes.TIMESTAMP_DTYPE

    raise TypeError(
        f"Could not find matching signature for date_add with argument types: {[str(t) for t in args]}"
    )


_DATE_ADD_OP = googlesql.GoogleSqlScalarOp(
    "DATE_ADD",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=_DATE_ADD_SIG,
)


def _DATE_BUCKET_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (3 - len(args))
    # Try matching impl 0
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if dtypes.coerce_to_common(args[0], dtypes.DATE_DTYPE) != dtypes.DATE_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[1], dtypes.TIMEDELTA_DTYPE)
                != dtypes.TIMEDELTA_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        try:
            if dtypes.coerce_to_common(args[2], dtypes.DATE_DTYPE) != dtypes.DATE_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.DATE_DTYPE

    # Try matching impl 1
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[1], dtypes.TIMEDELTA_DTYPE)
                != dtypes.TIMEDELTA_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[2], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.TIMESTAMP_DTYPE

    raise TypeError(
        f"Could not find matching signature for date_bucket with argument types: {[str(t) for t in args]}"
    )


_DATE_BUCKET_OP = googlesql.GoogleSqlScalarOp(
    "DATE_BUCKET",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=_DATE_BUCKET_SIG,
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


def _DATE_SUB_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (3 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if dtypes.coerce_to_common(args[0], dtypes.DATE_DTYPE) != dtypes.DATE_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if dtypes.coerce_to_common(args[1], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[2])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[2]
    if match_ok:
        return dtypes.DATE_DTYPE

    # Try matching impl 1
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if dtypes.coerce_to_common(args[1], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[2])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[2]
    if match_ok:
        return dtypes.TIMESTAMP_DTYPE

    raise TypeError(
        f"Could not find matching signature for date_sub with argument types: {[str(t) for t in args]}"
    )


_DATE_SUB_OP = googlesql.GoogleSqlScalarOp(
    "DATE_SUB",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=_DATE_SUB_SIG,
)


def _DATE_TRUNC_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (3 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if dtypes.coerce_to_common(args[0], dtypes.DATE_DTYPE) != dtypes.DATE_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[1])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[1]
    if match_ok:
        return dtypes.DATE_DTYPE

    # Try matching impl 1
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[1])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[1]
    if match_ok:
        return dtypes.TIMESTAMP_DTYPE

    # Try matching impl 2
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[1])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[1]
    if match_ok and args[2] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[2], dtypes.STRING_DTYPE)
                != dtypes.STRING_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.TIMESTAMP_DTYPE

    raise TypeError(
        f"Could not find matching signature for date_trunc with argument types: {[str(t) for t in args]}"
    )


_DATE_TRUNC_OP = googlesql.GoogleSqlScalarOp(
    "DATE_TRUNC",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=_DATE_TRUNC_SIG,
)


def _EXTRACT_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (3 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if dtypes.coerce_to_common(args[0], dtypes.DATE_DTYPE) != dtypes.DATE_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[1])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[1]
    if match_ok:
        return dtypes.INT_DTYPE

    # Try matching impl 1
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[1])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[1]
    if match_ok and args[2] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[2], dtypes.STRING_DTYPE)
                != dtypes.STRING_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.INT_DTYPE

    # Try matching impl 2
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[1])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[1]
    if match_ok:
        return dtypes.INT_DTYPE

    # Try matching impl 3
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if dtypes.coerce_to_common(args[0], dtypes.TIME_DTYPE) != dtypes.TIME_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[1])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[1]
    if match_ok:
        return dtypes.INT_DTYPE

    # Try matching impl 4
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMEDELTA_DTYPE)
                != dtypes.TIMEDELTA_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        if any1_val is not None:
            try:
                any1_val = dtypes.coerce_to_common(any1_val, args[1])
            except TypeError:
                match_ok = False
        else:
            any1_val = args[1]
    if match_ok:
        return dtypes.INT_DTYPE

    # Try matching impl 5
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[1], dtypes.STRING_DTYPE)
                != dtypes.STRING_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.TIME_DTYPE

    # Try matching impl 6
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.TIMESTAMP_DTYPE)
                != dtypes.TIMESTAMP_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.TIME_DTYPE

    raise TypeError(
        f"Could not find matching signature for extract with argument types: {[str(t) for t in args]}"
    )


_EXTRACT_OP = googlesql.GoogleSqlScalarOp(
    "EXTRACT",
    args=(
        googlesql.ArgSpec(),
        googlesql.ArgSpec(optional=True),
        googlesql.ArgSpec(optional=True),
    ),
    signature=_EXTRACT_SIG,
)
_FORMAT_DATE_OP = googlesql.GoogleSqlScalarOp(
    "FORMAT_DATE",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
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
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
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


def date_bucket(
    date_in_bucket: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
    ],
    bucket_width: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], datetime.timedelta],
    ],
    bucket_origin: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Gets the lower bound of the date bucket that contains a date."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DATE_BUCKET_OP,
        date_in_bucket,
        bucket_width,
        bucket_origin,
    )


def date_diff(
    end_date: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
    ],
    start_date: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
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
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
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
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
    ],
    granularity: Union[
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
    """Truncates a DATE, DATETIME, or TIMESTAMP value at a particular granularity."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _DATE_TRUNC_OP,
        date_value,
        granularity,
        time_zone,
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
            datetime.timedelta,
        ],
    ],
    part: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
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
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
    ],
    time_zone: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Formats a DATE value according to a specified format string."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _FORMAT_DATE_OP,
        format_string,
        date_expr,
        time_zone,
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
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT],
            datetime.date,
            datetime.datetime,
        ],
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
