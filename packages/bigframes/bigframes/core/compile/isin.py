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

"""Helpers to join ArrayValue objects."""

from __future__ import annotations

import itertools
from typing import Tuple

import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.types as ibis_types

import bigframes.core.compile.compiled as compiled


def isin_unordered(
    left: compiled.UnorderedIR,
    right: compiled.UnorderedIR,
    indicator_col: str,
    conditions: Tuple[str, str],
) -> compiled.UnorderedIR:
    """Join two expressions by column equality.

    Arguments:
        left: Expression for left table to join.
        right: Expression for right table to join.
        conditions: Id pairs to compare
    Returns:
        The joined expression.
    """
    left_table = left._to_ibis_expr()
    right_table = right._to_ibis_expr()
    new_column = (
        value_to_join_key(left_table[conditions[0]])
        .isin(value_to_join_key(right_table[conditions[1]]))
        .name(indicator_col)
    )

    columns = tuple(
        itertools.chain(
            (left_table[col.get_name()] for col in left.columns), (new_column,)
        )
    )

    return compiled.UnorderedIR(
        left_table,
        columns=columns,
    )


def value_to_join_key(value: ibis_types.Value):
    """Converts nullable values to non-null string SQL will not match null keys together - but pandas does."""
    if not value.type().is_string():
        value = value.cast(ibis_dtypes.str)
    return (
        value.fill_null(ibis_types.literal("$NULL_SENTINEL$"))
        if hasattr(value, "fill_null")
        else value.fillna(ibis_types.literal("$NULL_SENTINEL$"))
    )
