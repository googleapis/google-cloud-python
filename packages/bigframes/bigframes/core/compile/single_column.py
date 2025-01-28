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

"""Helpers to join ArrayValue objects."""

from __future__ import annotations

from typing import Literal, Tuple

import bigframes_vendored.ibis.expr.api as ibis_api
import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.types as ibis_types

import bigframes.core.compile.compiled as compiled


def join_by_column_unordered(
    left: compiled.UnorderedIR,
    right: compiled.UnorderedIR,
    conditions: Tuple[Tuple[str, str], ...],
    type: Literal["inner", "outer", "left", "right", "cross"],
) -> compiled.UnorderedIR:
    """Join two expressions by column equality.

    Arguments:
        left: Expression for left table to join.
        left_column_ids: Column IDs (not label) to join by.
        right: Expression for right table to join.
        right_column_ids: Column IDs (not label) to join by.
        how: The type of join to perform.
        allow_row_identity_join (bool):
            If True, allow matching by row identity. Set to False to always
            perform a true JOIN in generated SQL.
    Returns:
        The joined expression. The resulting columns will be, in order,
        first the coalesced join keys, then, all the left columns, and
        finally, all the right columns.
    """
    # Shouldn't need to select the column ids explicitly, but it seems that ibis has some
    # bug resolving column ids otherwise, potentially because of the "JoinChain" op
    left_table = left._to_ibis_expr().select(left.column_ids)
    right_table = right._to_ibis_expr().select(right.column_ids)
    join_conditions = [
        value_to_join_key(left_table[left_index])
        == value_to_join_key(right_table[right_index])
        for left_index, right_index in conditions
    ]

    combined_table = ibis_api.join(
        left_table,
        right_table,
        predicates=join_conditions,
        how=type,  # type: ignore
    )
    columns = [combined_table[col.get_name()] for col in left.columns] + [
        combined_table[col.get_name()] for col in right.columns
    ]
    return compiled.UnorderedIR(
        combined_table,
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
