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

import datetime
from typing import Any, Literal, Optional, TypeVar, Union

import bigframes.bigquery._googlesql
import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.core.sentinels as sentinels
import bigframes.operations as ops
import bigframes.series as series
from bigframes import dtypes
from bigframes.operations import googlesql

T = TypeVar("T", series.Series, bigframes.core.col.Expression)

_ARRAY_CONCAT_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_CONCAT",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: None,
)
_ARRAY_FIRST_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_FIRST",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: None,
)
_ARRAY_FIRST_N_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_FIRST_N",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: None,
)
_ARRAY_INCLUDES_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_INCLUDES",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: None,
)
_ARRAY_INCLUDES_ALL_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_INCLUDES_ALL",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: None,
)
_ARRAY_INCLUDES_ANY_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_INCLUDES_ANY",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: None,
)
_ARRAY_IS_DISTINCT_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_IS_DISTINCT",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: None,
)
_ARRAY_LAST_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_LAST",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: None,
)
_ARRAY_LENGTH_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_LENGTH",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: None,
)
_ARRAY_REVERSE_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_REVERSE",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: None,
)
_ARRAY_SLICE_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_SLICE",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: None,
)
_ARRAY_TO_STRING_OP = googlesql.GoogleSqlScalarOp(
    "ARRAY_TO_STRING",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=lambda *args: None,
)
_FLATTEN_OP = googlesql.GoogleSqlScalarOp(
    "FLATTEN",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(arg_name="depth", optional=True)),
    signature=lambda *args: None,
)
_GENERATE_ARRAY_OP = googlesql.GoogleSqlScalarOp(
    "GENERATE_ARRAY",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec(optional=True)),
    signature=lambda *args: None,
)


def array_concat(
    array_expression_1: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    array_expression_2: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Concatenates one or more arrays with the same element type into a single array."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_CONCAT_OP,
        array_expression_1,
        array_expression_2,
    )


def array_first(
    array_expression: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Takes an array and returns the first element in the array."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_FIRST_OP,
        array_expression,
    )


def array_first_n(
    input_array: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    n: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Returns a prefix of `input_array` consisting of the first `n` elements."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_FIRST_N_OP,
        input_array,
        n,
    )


def array_includes(
    array_to_search: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    search_value: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Takes an array and returns `TRUE` if there is an element in the array that is equal to the search_value."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_INCLUDES_OP,
        array_to_search,
        search_value,
    )


def array_includes_all(
    array_to_search: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    search_values: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Takes an array to search and an array of search values. Returns `TRUE` if all search values are in the array to search, otherwise returns `FALSE`."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_INCLUDES_ALL_OP,
        array_to_search,
        search_values,
    )


def array_includes_any(
    array_to_search: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    search_values: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Takes an array to search and an array of search values. Returns `TRUE` if any search values are in the array to search, otherwise returns `FALSE`."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_INCLUDES_ANY_OP,
        array_to_search,
        search_values,
    )


def array_is_distinct(
    array_expression: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Returns `TRUE` if the array contains no repeated elements, using the same equality comparison logic as `SELECT DISTINCT`."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_IS_DISTINCT_OP,
        array_expression,
    )


def array_last(
    array_expression: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Takes an array and returns the last element in the array."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_LAST_OP,
        array_expression,
    )


def array_length(
    series: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
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

    You can also apply this function directly to Series.

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
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_LENGTH_OP,
        series,
    )


def array_reverse(
    value: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Returns the input `ARRAY` with elements in reverse order."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_REVERSE_OP,
        value,
    )


def array_slice(
    array_to_slice: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    start_offset: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    end_offset: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
) -> T:
    """Returns an array containing zero or more consecutive elements from the input array."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_SLICE_OP,
        array_to_slice,
        start_offset,
        end_offset,
    )


def array_to_string(
    series: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    delimiter: Union[
        T,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], bytes, str],
    ],
    null_text: Union[
        T,
        bigframes.core.col.Expression,
        Union[Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], bytes, str],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> T:
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

    Args:
        series (bigframes.series.Series): A Series containing arrays.
        delimiter (str): The string used to separate array elements.
        null_text (str, optional): The string to replace any NULL values in the array with.

    Returns:
        bigframes.series.Series: A Series containing delimited strings.
    """
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ARRAY_TO_STRING_OP,
        series,
        delimiter,
        null_text,
    )


def flatten(
    array_to_flatten: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    depth: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> T:
    """Takes an array of nested data and flattens a specific part of it into a single, flat array with the [array elements field access operator][array-el-field-operator]. Returns `NULL` if the input value is `NULL`."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _FLATTEN_OP,
        array_to_flatten,
        depth,
    )


def generate_array(
    start_expression: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    end_expression: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ],
    step_expression: Union[
        T,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT]],
    ] = sentinels.Sentinel.ARGUMENT_DEFAULT,
) -> T:
    """Returns an array of values. The `start_expression` and `end_expression` parameters determine the inclusive start and end of the array."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _GENERATE_ARRAY_OP,
        start_expression,
        end_expression,
        step_expression,
    )
