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

from typing import Mapping

import ibis
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.types as ibis_types

import bigframes.core.compile.compiled as compiled
import bigframes.core.join_def as join_defs
import bigframes.core.joins as joining
import bigframes.core.ordering as orderings


def join_by_column_ordered(
    left: compiled.OrderedIR,
    right: compiled.OrderedIR,
    join: join_defs.JoinDefinition,
) -> compiled.OrderedIR:
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

    l_hidden_mapping, r_hidden_mapping = joining.JoinNameRemapper(namespace="hidden")(
        left._hidden_column_ids, right._hidden_column_ids
    )
    l_mapping = {**join.get_left_mapping(), **l_hidden_mapping}
    r_mapping = {**join.get_right_mapping(), **r_hidden_mapping}

    left_table = left._to_ibis_expr(
        ordering_mode="unordered",
        expose_hidden_cols=True,
        col_id_overrides=l_mapping,
    )
    right_table = right._to_ibis_expr(
        ordering_mode="unordered",
        expose_hidden_cols=True,
        col_id_overrides=r_mapping,
    )
    join_conditions = [
        value_to_join_key(left_table[l_mapping[left_index]])
        == value_to_join_key(right_table[r_mapping[right_index]])
        for left_index, right_index in join.conditions
    ]

    combined_table = ibis.join(
        left_table,
        right_table,
        predicates=join_conditions,
        how=join.type,  # type: ignore
    )

    # Preserve ordering accross joins.
    ordering = join_orderings(
        left._ordering,
        right._ordering,
        l_mapping,
        r_mapping,
        left_order_dominates=(join.type != "right"),
    )

    # We could filter out the original join columns, but predicates/ordering
    # might still reference them in implicit joins.
    columns = [combined_table[l_mapping[col.get_name()]] for col in left.columns] + [
        combined_table[r_mapping[col.get_name()]] for col in right.columns
    ]
    hidden_ordering_columns = [
        *[
            combined_table[l_hidden_mapping[col.get_name()]]
            for col in left._hidden_ordering_columns
        ],
        *[
            combined_table[r_hidden_mapping[col.get_name()]]
            for col in right._hidden_ordering_columns
        ],
    ]
    return compiled.OrderedIR(
        combined_table,
        columns=columns,
        hidden_ordering_columns=hidden_ordering_columns,
        ordering=ordering,
    )


def join_by_column_unordered(
    left: compiled.UnorderedIR,
    right: compiled.UnorderedIR,
    join: join_defs.JoinDefinition,
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
    # Value column mapping must use JOIN_NAME_REMAPPER to stay in sync with consumers of join result
    l_mapping = join.get_left_mapping()
    r_mapping = join.get_right_mapping()
    left_table = left._to_ibis_expr(
        col_id_overrides=l_mapping,
    )
    right_table = right._to_ibis_expr(
        col_id_overrides=r_mapping,
    )
    join_conditions = [
        value_to_join_key(left_table[l_mapping[left_index]])
        == value_to_join_key(right_table[r_mapping[right_index]])
        for left_index, right_index in join.conditions
    ]

    combined_table = ibis.join(
        left_table,
        right_table,
        predicates=join_conditions,
        how=join.type,  # type: ignore
    )
    # We could filter out the original join columns, but predicates/ordering
    # might still reference them in implicit joins.
    columns = [combined_table[l_mapping[col.get_name()]] for col in left.columns] + [
        combined_table[r_mapping[col.get_name()]] for col in right.columns
    ]
    return compiled.UnorderedIR(
        combined_table,
        columns=columns,
    )


def value_to_join_key(value: ibis_types.Value):
    """Converts nullable values to non-null string SQL will not match null keys together - but pandas does."""
    if not value.type().is_string():
        value = value.cast(ibis_dtypes.str)
    return value.fillna(ibis_types.literal("$NULL_SENTINEL$"))


def join_orderings(
    left: orderings.ExpressionOrdering,
    right: orderings.ExpressionOrdering,
    left_id_mapping: Mapping[str, str],
    right_id_mapping: Mapping[str, str],
    left_order_dominates: bool = True,
) -> orderings.ExpressionOrdering:
    left_ordering_refs = [
        ref.remap_names(left_id_mapping) for ref in left.all_ordering_columns
    ]
    right_ordering_refs = [
        ref.remap_names(right_id_mapping) for ref in right.all_ordering_columns
    ]
    if left_order_dominates:
        joined_refs = [*left_ordering_refs, *right_ordering_refs]
    else:
        joined_refs = [*right_ordering_refs, *left_ordering_refs]

    left_total_order_cols = frozenset(
        [left_id_mapping[id] for id in left.total_ordering_columns]
    )
    right_total_order_cols = frozenset(
        [right_id_mapping[id] for id in right.total_ordering_columns]
    )
    return orderings.ExpressionOrdering(
        ordering_value_columns=tuple(joined_refs),
        total_ordering_columns=left_total_order_cols | right_total_order_cols,
    )
