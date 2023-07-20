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

import typing
from typing import Callable, Literal, Tuple

import ibis
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.types as ibis_types

import bigframes.core as core
import bigframes.core.guid
import bigframes.core.joins.row_identity
import bigframes.core.ordering


def join_by_column(
    left: core.ArrayValue,
    left_column_ids: typing.Sequence[str],
    right: core.ArrayValue,
    right_column_ids: typing.Sequence[str],
    *,
    how: Literal[
        "inner",
        "left",
        "outer",
        "right",
    ],
    sort: bool = False,
    get_both_join_key_cols: bool = False,
) -> Tuple[
    core.ArrayValue,
    typing.Sequence[str],
    Tuple[Callable[[str], str], Callable[[str], str]],
]:
    """Join two expressions by column equality.

    Arguments:
        left: Expression for left table to join.
        left_column_ids: Column IDs (not label) to join by.
        right: Expression for right table to join.
        right_column_ids: Column IDs (not label) to join by.
        how: The type of join to perform.
        get_both_join_key_cols: if set to True, returned column ids will contain
            both left and right join key columns.

    Returns:
        The joined expression and the objects needed to interpret it.

        * ArrayValue: Joined table with all columns from left and right.
        * Sequence[str]: Column IDs of the coalesced join columns. Sometimes either the
          left/right table will have missing rows. This column pulls the
          non-NULL value from either left/right.
          If get_both_join_key_cols is True, will return uncombined left and
          right key columns.
        * Tuple[Callable, Callable]: For a given column ID from left or right,
          respectively, return the new column id from the combined expression.
    """

    if (
        how in bigframes.core.joins.row_identity.SUPPORTED_ROW_IDENTITY_HOW
        and left.table.equals(right.table)
        # Compare ibis expressions for left/right columns because its possible that
        # they both have the same names but were modified in different ways.
        and all(
            left.get_any_column(lcol).equals(right.get_any_column(rcol))
            for lcol, rcol in zip(left_column_ids, right_column_ids)
        )
    ):
        combined_expr, (
            get_column_left,
            get_column_right,
        ) = bigframes.core.joins.row_identity.join_by_row_identity(left, right, how=how)
        original_ordering = combined_expr._ordering
    else:
        # Generate offsets if non-default ordering is applied
        # Assumption, both sides are totally ordered, otherwise offsets will be nondeterministic
        left_table = left.to_ibis_expr(
            ordering_mode="ordered_col", order_col_name=core.ORDER_ID_COLUMN
        )
        right_table = right.to_ibis_expr(
            ordering_mode="ordered_col", order_col_name=core.ORDER_ID_COLUMN
        )
        join_conditions = [
            value_to_join_key(left_table[left_index])
            == value_to_join_key(right_table[right_index])
            for left_index, right_index in zip(left_column_ids, right_column_ids)
        ]

        combined_table = ibis.join(
            left_table,
            right_table,
            predicates=join_conditions,
            how=how,
            lname="{name}_x",
            rname="{name}_y",
        )

        def get_column_left(key: str) -> str:
            if (
                how == "inner"
                and key in left_column_ids
                and key in combined_table.columns
            ):
                # Ibis doesn't rename the column if the values are guaranteed
                # to be equal on left and right (because they're part of an
                # inner join condition). See:
                # https://github.com/ibis-project/ibis/pull/4651
                pass
            elif key in right_table.columns:
                key = f"{key}_x"

            return key

        def get_column_right(key: str) -> str:
            if (
                how == "inner"
                and key in right_column_ids
                and key in combined_table.columns
            ):
                # Ibis doesn't rename the column if the values are guaranteed
                # to be equal on left and right (because they're part of an
                # inner join condition). See:
                # https://github.com/ibis-project/ibis/pull/4651
                pass
            elif key in left_table.columns:
                key = f"{key}_y"

            return key

        left_ordering_encoding_size = (
            left._ordering.ordering_encoding_size
            or bigframes.core.ordering.DEFAULT_ORDERING_ID_LENGTH
        )
        right_ordering_encoding_size = (
            right._ordering.ordering_encoding_size
            or bigframes.core.ordering.DEFAULT_ORDERING_ID_LENGTH
        )

        # Preserve original ordering accross joins.
        left_order_id = get_column_left(core.ORDER_ID_COLUMN)
        right_order_id = get_column_right(core.ORDER_ID_COLUMN)
        new_order_id_col = _merge_order_ids(
            combined_table[left_order_id],
            left_ordering_encoding_size,
            combined_table[right_order_id],
            right_ordering_encoding_size,
            how,
        )
        new_order_id = new_order_id_col.get_name()
        if new_order_id is None:
            raise ValueError("new_order_id unexpectedly has no name")
        hidden_columns = (new_order_id_col,)
        original_ordering = core.ExpressionOrdering(
            ordering_id_column=core.OrderingColumnReference(new_order_id)
            if (new_order_id_col is not None)
            else None,
            ordering_encoding_size=left_ordering_encoding_size
            + right_ordering_encoding_size,
        )
        combined_expr = core.ArrayValue(
            left._session,
            combined_table,
            hidden_ordering_columns=hidden_columns,
        )

    join_key_cols: list[ibis_types.Value] = []
    for lcol, rcol in zip(left_column_ids, right_column_ids):
        if get_both_join_key_cols:
            join_key_cols.append(
                combined_expr.get_column(get_column_left(lcol)).name(
                    bigframes.core.guid.generate_guid(prefix="index_")
                )
            )
            join_key_cols.append(
                combined_expr.get_column(get_column_right(rcol)).name(
                    bigframes.core.guid.generate_guid(prefix="index_")
                )
            )
        else:
            if how == "left" or how == "inner":
                join_key_cols.append(
                    combined_expr.get_column(get_column_left(lcol)).name(
                        bigframes.core.guid.generate_guid(prefix="index_")
                    )
                )
            elif how == "right":
                join_key_cols.append(
                    combined_expr.get_column(get_column_right(rcol)).name(
                        bigframes.core.guid.generate_guid(prefix="index_")
                    )
                )
            elif how == "outer":
                # The left index and the right index might contain null values, for
                # example due to an outer join with different numbers of rows. Coalesce
                # these to take the index value from either column.
                # Use a random name in case the left index and the right index have the
                # same name. In such a case, _x and _y suffixes will already be used.
                join_key_cols.append(
                    ibis.coalesce(
                        combined_expr.get_column(get_column_left(lcol)),
                        combined_expr.get_column(get_column_right(rcol)),
                    ).name(bigframes.core.guid.generate_guid(prefix="index_"))
                )
            else:
                raise ValueError(f"Unexpected join type: {how}")

    # We could filter out the original join columns, but predicates/ordering
    # might still reference them in implicit joins.
    columns = (
        join_key_cols
        + [
            combined_expr.get_column(get_column_left(key))
            for key in left.column_names.keys()
        ]
        + [
            combined_expr.get_column(get_column_right(key))
            for key in right.column_names.keys()
        ]
    )

    if sort:
        ordering = original_ordering.with_ordering_columns(
            [
                core.OrderingColumnReference(join_key_col.get_name())
                for join_key_col in join_key_cols
            ]
        )
    else:
        ordering = original_ordering

    combined_expr_builder = combined_expr.builder()
    combined_expr_builder.columns = columns
    combined_expr_builder.ordering = ordering
    combined_expr = combined_expr_builder.build()
    return (
        combined_expr,
        [key.get_name() for key in join_key_cols],
        (get_column_left, get_column_right),
    )


def value_to_join_key(value: ibis_types.Value):
    """Converts nullable values to non-null string SQL will not match null keys together - but pandas does."""
    if not value.type().is_string():
        value = value.cast(ibis_dtypes.str)
    return value.fillna(ibis_types.literal("$NULL_SENTINEL$"))


def _merge_order_ids(
    left_id: ibis_types.Value,
    left_encoding_size: int,
    right_id: ibis_types.Value,
    right_encoding_size: int,
    how: str,
) -> ibis_types.StringValue:
    if how == "right":
        return _merge_order_ids(
            right_id, right_encoding_size, left_id, left_encoding_size, "left"
        )
    return (
        (
            bigframes.core.ordering.stringify_order_id(left_id, left_encoding_size)
            + bigframes.core.ordering.stringify_order_id(right_id, right_encoding_size)
        )
    ).name(bigframes.core.guid.generate_guid(prefix="bigframes_ordering_id_"))
