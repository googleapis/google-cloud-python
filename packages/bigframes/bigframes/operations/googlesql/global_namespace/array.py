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
# This file was generated from: scripts/data/sql-functions/global_namespace/array.yaml
# by the script: scripts/generate_bigframes_bigquery.py

from __future__ import annotations

import decimal
from typing import Any, Literal, Union

import bigframes.core.col
import bigframes.core.googlesql
import bigframes.core.sentinels as sentinels
import bigframes.series as series
from bigframes import dtypes
from bigframes.operations import googlesql


def _ARRAY_CONCAT_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (2 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            if any1_val is not None:
                try:
                    any1_val = dtypes.coerce_to_common(any1_val, inner)
                except TypeError:
                    match_ok = False
            else:
                any1_val = inner
    if match_ok and args[1] is not None:
        if not dtypes.is_array_like(args[1]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[1])
            if any1_val is not None:
                try:
                    any1_val = dtypes.coerce_to_common(any1_val, inner)
                except TypeError:
                    match_ok = False
            else:
                any1_val = inner
    if match_ok:
        if any1_val is not None:
            return dtypes.list_type(any1_val)
        else:
            return None

    raise TypeError(
        f"Could not find matching signature for array_concat with argument types: {[str(t) for t in args]}"
    )


_ARRAY_CONCAT_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_CONCAT",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=_ARRAY_CONCAT_SIG,
)


def _ARRAY_FIRST_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (1 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            if any1_val is not None:
                try:
                    any1_val = dtypes.coerce_to_common(any1_val, inner)
                except TypeError:
                    match_ok = False
            else:
                any1_val = inner
    if match_ok:
        return any1_val

    raise TypeError(
        f"Could not find matching signature for array_first with argument types: {[str(t) for t in args]}"
    )


_ARRAY_FIRST_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_FIRST",
    args=(googlesql.ArgSpec(),),
    signature=_ARRAY_FIRST_SIG,
)


def _ARRAY_FIRST_N_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (2 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            if any1_val is not None:
                try:
                    any1_val = dtypes.coerce_to_common(any1_val, inner)
                except TypeError:
                    match_ok = False
            else:
                any1_val = inner
    if match_ok and args[1] is not None:
        try:
            if dtypes.coerce_to_common(args[1], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        if any1_val is not None:
            return dtypes.list_type(any1_val)
        else:
            return None

    raise TypeError(
        f"Could not find matching signature for array_first_n with argument types: {[str(t) for t in args]}"
    )


_ARRAY_FIRST_N_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_FIRST_N",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=_ARRAY_FIRST_N_SIG,
)
_ARRAY_INCLUDES_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_INCLUDES",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.BOOL_DTYPE,
)
_ARRAY_INCLUDES_ALL_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_INCLUDES_ALL",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.BOOL_DTYPE,
)
_ARRAY_INCLUDES_ANY_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_INCLUDES_ANY",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.BOOL_DTYPE,
)
_ARRAY_IS_DISTINCT_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_IS_DISTINCT",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.BOOL_DTYPE,
)


def _ARRAY_LAST_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (1 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            if any1_val is not None:
                try:
                    any1_val = dtypes.coerce_to_common(any1_val, inner)
                except TypeError:
                    match_ok = False
            else:
                any1_val = inner
    if match_ok:
        return any1_val

    raise TypeError(
        f"Could not find matching signature for array_last with argument types: {[str(t) for t in args]}"
    )


_ARRAY_LAST_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_LAST",
    args=(googlesql.ArgSpec(),),
    signature=_ARRAY_LAST_SIG,
)
_ARRAY_LENGTH_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_LENGTH",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.INT_DTYPE,
)


def _ARRAY_REVERSE_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (1 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            if any1_val is not None:
                try:
                    any1_val = dtypes.coerce_to_common(any1_val, inner)
                except TypeError:
                    match_ok = False
            else:
                any1_val = inner
    if match_ok:
        if any1_val is not None:
            return dtypes.list_type(any1_val)
        else:
            return None

    raise TypeError(
        f"Could not find matching signature for array_reverse with argument types: {[str(t) for t in args]}"
    )


_ARRAY_REVERSE_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_REVERSE",
    args=(googlesql.ArgSpec(),),
    signature=_ARRAY_REVERSE_SIG,
)


def _ARRAY_SLICE_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (3 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            if any1_val is not None:
                try:
                    any1_val = dtypes.coerce_to_common(any1_val, inner)
                except TypeError:
                    match_ok = False
            else:
                any1_val = inner
    if match_ok and args[1] is not None:
        try:
            if dtypes.coerce_to_common(args[1], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        try:
            if dtypes.coerce_to_common(args[2], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        if any1_val is not None:
            return dtypes.list_type(any1_val)
        else:
            return None

    raise TypeError(
        f"Could not find matching signature for array_slice with argument types: {[str(t) for t in args]}"
    )


_ARRAY_SLICE_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_SLICE",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=_ARRAY_SLICE_SIG,
)


def _ARRAY_TO_STRING_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (3 - len(args))
    # Try matching impl 0
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            try:
                if (
                    dtypes.coerce_to_common(inner, dtypes.STRING_DTYPE)
                    != dtypes.STRING_DTYPE
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
        return dtypes.STRING_DTYPE

    # Try matching impl 1
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            try:
                if (
                    dtypes.coerce_to_common(inner, dtypes.BYTES_DTYPE)
                    != dtypes.BYTES_DTYPE
                ):
                    match_ok = False
            except TypeError:
                match_ok = False
    if match_ok and args[1] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[1], dtypes.BYTES_DTYPE)
                != dtypes.BYTES_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[2], dtypes.BYTES_DTYPE)
                != dtypes.BYTES_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.BYTES_DTYPE

    raise TypeError(
        f"Could not find matching signature for array_to_string with argument types: {[str(t) for t in args]}"
    )


_ARRAY_TO_STRING_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_TO_STRING",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=_ARRAY_TO_STRING_SIG,
)


def _FLATTEN_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (2 - len(args))
    # Try matching impl 0
    any1_val = None
    match_ok = True
    if match_ok and args[0] is not None:
        if not dtypes.is_array_like(args[0]):
            match_ok = False
        else:
            inner = dtypes.get_array_inner_type(args[0])
            if any1_val is not None:
                try:
                    any1_val = dtypes.coerce_to_common(any1_val, inner)
                except TypeError:
                    match_ok = False
            else:
                any1_val = inner
    if match_ok and args[1] is not None:
        try:
            if dtypes.coerce_to_common(args[1], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        if any1_val is not None:
            return dtypes.list_type(any1_val)
        else:
            return None

    raise TypeError(
        f"Could not find matching signature for flatten with argument types: {[str(t) for t in args]}"
    )


_FLATTEN_OP = googlesql.GoogleSqlScalarOp(
    "FLATTEN",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(arg_name="depth", optional=True)),
    signature=_FLATTEN_SIG,
)


def _GENERATE_ARRAY_SIG(*args):
    # Pad args with None to match max expected args
    args = args + (None,) * (3 - len(args))
    # Try matching impl 0
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if dtypes.coerce_to_common(args[0], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
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
        try:
            if dtypes.coerce_to_common(args[2], dtypes.INT_DTYPE) != dtypes.INT_DTYPE:
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.list_type(dtypes.INT_DTYPE)

    # Try matching impl 1
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.NUMERIC_DTYPE)
                != dtypes.NUMERIC_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[1], dtypes.NUMERIC_DTYPE)
                != dtypes.NUMERIC_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[2], dtypes.NUMERIC_DTYPE)
                != dtypes.NUMERIC_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.list_type(dtypes.NUMERIC_DTYPE)

    # Try matching impl 2
    match_ok = True
    if match_ok and args[0] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[0], dtypes.FLOAT_DTYPE)
                != dtypes.FLOAT_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[1] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[1], dtypes.FLOAT_DTYPE)
                != dtypes.FLOAT_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok and args[2] is not None:
        try:
            if (
                dtypes.coerce_to_common(args[2], dtypes.FLOAT_DTYPE)
                != dtypes.FLOAT_DTYPE
            ):
                match_ok = False
        except TypeError:
            match_ok = False
    if match_ok:
        return dtypes.list_type(dtypes.FLOAT_DTYPE)

    raise TypeError(
        f"Could not find matching signature for generate_array with argument types: {[str(t) for t in args]}"
    )


_GENERATE_ARRAY_OP = googlesql.GoogleSqlScalarOp(
    "GENERATE_ARRAY",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=_GENERATE_ARRAY_SIG,
)


def array_concat(
    array_expression_1: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    array_expression_2: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Concatenates one or more arrays with the same element type into a single array."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_CONCAT_OP,
        array_expression_1,
        array_expression_2,
    )


def array_first(
    array_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Takes an array and returns the first element in the array."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_FIRST_OP,
        array_expression,
    )


def array_first_n(
    input_array: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    n: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns a prefix of `input_array` consisting of the first `n` elements."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_FIRST_N_OP,
        input_array,
        n,
    )


def array_includes(
    array_to_search: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    search_value: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Takes an array and returns `TRUE` if there is an element in the array that is equal to the search_value."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_INCLUDES_OP,
        array_to_search,
        search_value,
    )


def array_includes_all(
    array_to_search: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    search_values: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Takes an array to search and an array of search values. Returns `TRUE` if all search values are in the array to search, otherwise returns `FALSE`."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_INCLUDES_ALL_OP,
        array_to_search,
        search_values,
    )


def array_includes_any(
    array_to_search: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    search_values: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Takes an array to search and an array of search values. Returns `TRUE` if any search values are in the array to search, otherwise returns `FALSE`."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_INCLUDES_ANY_OP,
        array_to_search,
        search_values,
    )


def array_is_distinct(
    array_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns `TRUE` if the array contains no repeated elements, using the same equality comparison logic as `SELECT DISTINCT`."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_IS_DISTINCT_OP,
        array_expression,
    )


def array_last(
    array_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Takes an array and returns the last element in the array."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_LAST_OP,
        array_expression,
    )


def array_length(
    series: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Compute the length of each array element in the Series.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq

        >>> s = bpd.Series([[1, 2, 8, 3], [], [3, 4]])
        >>> bbq.array_length(s)
        0    4
        1    0
        2    2
        dtype: Int64

    You can call this function using the Series `bigquery` accessor.

        >>> s.bigquery.array_length()
        0    4
        1    0
        2    2
        dtype: Int64

    You can also use this accessor on a pandas Series after importing bigframes.

        >>> import bigframes
        >>> import pandas as pd
        >>> ps = pd.Series([[1, 2, 8, 3], [], [3, 4]])
        >>> ps.bigquery.array_length()
        0    4
        1    0
        2    2
        dtype: Int64

    You can also apply this function directly to Series using `apply`.

        >>> s.apply(bbq.array_length, by_row=False)
        0    4
        1    0
        2    2
        dtype: Int64

    Args:
        series (bigframes.series.Series): A Series with array columns.

    Returns:
        bigframes.series.Series: A Series of integer values indicating
            the length of each element in the Series.
    """
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_LENGTH_OP,
        series,
    )


def array_reverse(
    value: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns the input `ARRAY` with elements in reverse order."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_REVERSE_OP,
        value,
    )


def array_slice(
    array_to_slice: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    start_offset: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ],
    end_offset: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns an array containing zero or more consecutive elements from the input array."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_SLICE_OP,
        array_to_slice,
        start_offset,
        end_offset,
    )


def array_to_string(
    series: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    delimiter: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], bytes, str],
    ],
    null_text: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], bytes, str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Converts array elements within a Series into delimited strings.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq

        >>> s = bpd.Series([["H", "i", "!"], ["Hello", "World"], np.nan, [], ["Hi"]])
        >>> bbq.array_to_string(s, delimiter=", ")
        0         H, i, !
        1    Hello, World
        2
        3
        4              Hi
        dtype: string

    You can call this function using the Series `bigquery` accessor.

        >>> s.bigquery.array_to_string(delimiter=", ")
        0         H, i, !
        1    Hello, World
        2
        3
        4              Hi
        dtype: string

    You can also use this accessor on a pandas Series after importing bigframes.

        >>> import bigframes
        >>> import pandas as pd
        >>> ps = pd.Series([["H", "i", "!"], ["Hello", "World"], None, [], ["Hi"]])
        >>> ps.bigquery.array_to_string(delimiter=", ")
        0         H, i, !
        1    Hello, World
        2
        3
        4              Hi
        dtype: string

    Args:
        series (bigframes.series.Series): A Series containing arrays.
        delimiter (str): The string used to separate array elements.
        null_text (str, optional): The string to replace any NULL values in the array with.

    Returns:
        bigframes.series.Series: A Series containing delimited strings.
    """
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _ARRAY_TO_STRING_OP,
        series,
        delimiter,
        null_text,
    )


def flatten(
    array_to_flatten: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    depth: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], int],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Takes an array of nested data and flattens a specific part of it into a single, flat array with the [array elements field access operator][array-el-field-operator]. Returns `NULL` if the input value is `NULL`."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _FLATTEN_OP,
        array_to_flatten,
        depth,
    )


def generate_array(
    start_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], decimal.Decimal, float, int
        ],
    ],
    end_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], decimal.Decimal, float, int
        ],
    ],
    step_expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[
            Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], decimal.Decimal, float, int
        ],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Returns an array of values. The `start_expression` and `end_expression` parameters determine the inclusive start and end of the array."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _GENERATE_ARRAY_OP,
        start_expression,
        end_expression,
        step_expression,
    )
