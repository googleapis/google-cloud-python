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

import bigframes.constants as constants
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
    coalesce_join_keys: bool = True,
    allow_row_identity_join: bool = True,
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
        coalesce_join_keys: if set to False, returned column ids will contain
            both left and right join key columns.
        allow_row_identity_join (bool):
            If True, allow matching by row identity. Set to False to always
            perform a true JOIN in generated SQL.

    Returns:
        The joined expression and the objects needed to interpret it.

        * ArrayValue: Joined table with all columns from left and right.
        * Sequence[str]: Column IDs of the coalesced join columns. Sometimes either the
          left/right table will have missing rows. This column pulls the
          non-NULL value from either left/right.
          If coalesce_join_keys is False, will return uncombined left and
          right key columns.
        * Tuple[Callable, Callable]: For a given column ID from left or right,
          respectively, return the new column id from the combined expression.
    """
    if (
        allow_row_identity_join
        and how in bigframes.core.joins.row_identity.SUPPORTED_ROW_IDENTITY_HOW
        and left.table.equals(right.table)
        # Make sure we're joining on exactly the same column(s), at least with
        # regards to value its possible that they both have the same names but
        # were modified in different ways. Ignore differences in the names.
        and all(
            left.get_any_column(lcol)
            .name("index")
            .equals(right.get_any_column(rcol).name("index"))
            for lcol, rcol in zip(left_column_ids, right_column_ids)
        )
    ):
        combined_expr, (
            get_column_left,
            get_column_right,
        ) = bigframes.core.joins.row_identity.join_by_row_identity(left, right, how=how)
        left_join_keys = [
            combined_expr.get_column(get_column_left(col)) for col in left_column_ids
        ]
        right_join_keys = [
            combined_expr.get_column(get_column_right(col)) for col in right_column_ids
        ]
        join_key_cols = get_join_cols(
            left_join_keys, right_join_keys, how, coalesce_join_keys
        )
        join_key_ids = [col.get_name() for col in join_key_cols]
        combined_expr = combined_expr.projection(
            [*join_key_cols, *combined_expr.columns]
        )
        if sort:
            combined_expr = combined_expr.order_by(
                [
                    core.OrderingColumnReference(join_col_id)
                    for join_col_id in join_key_ids
                ]
            )
        return (
            combined_expr,
            join_key_ids,
            (
                get_column_left,
                get_column_right,
            ),
        )
    else:
        # Generate offsets if non-default ordering is applied
        # Assumption, both sides are totally ordered, otherwise offsets will be nondeterministic
        left_table = left.to_ibis_expr(
            ordering_mode="string_encoded", order_col_name=core.ORDER_ID_COLUMN
        )
        right_table = right.to_ibis_expr(
            ordering_mode="string_encoded", order_col_name=core.ORDER_ID_COLUMN
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
            left._ordering.string_encoding.length
            if left._ordering.is_string_encoded
            else bigframes.core.ordering.DEFAULT_ORDERING_ID_LENGTH
        )
        right_ordering_encoding_size = (
            right._ordering.string_encoding.length
            if right._ordering.is_string_encoded
            else bigframes.core.ordering.DEFAULT_ORDERING_ID_LENGTH
        )

        # Preserve original ordering accross joins.
        left_order_id = get_column_left(core.ORDER_ID_COLUMN)
        right_order_id = get_column_right(core.ORDER_ID_COLUMN)
        new_order_id_col = _merge_order_ids(
            typing.cast(ibis_types.StringColumn, combined_table[left_order_id]),
            left_ordering_encoding_size,
            typing.cast(ibis_types.StringColumn, combined_table[right_order_id]),
            right_ordering_encoding_size,
            how,
        )
        new_order_id = new_order_id_col.get_name()
        if new_order_id is None:
            raise ValueError("new_order_id unexpectedly has no name")

        hidden_columns = (new_order_id_col,)
        ordering = core.ExpressionOrdering(
            # Order id is non-nullable but na_last=False generates simpler sql with current impl
            ordering_value_columns=[
                core.OrderingColumnReference(new_order_id, na_last=False)
            ],
            total_ordering_columns=frozenset([new_order_id]),
            string_encoding=core.StringEncoding(
                True, left_ordering_encoding_size + right_ordering_encoding_size
            ),
        )

        left_join_keys = [
            combined_table[get_column_left(col)] for col in left_column_ids
        ]
        right_join_keys = [
            combined_table[get_column_right(col)] for col in right_column_ids
        ]
        join_key_cols = get_join_cols(
            left_join_keys, right_join_keys, how, coalesce_join_keys
        )
        # We could filter out the original join columns, but predicates/ordering
        # might still reference them in implicit joins.
        columns = (
            join_key_cols
            + [combined_table[get_column_left(col.get_name())] for col in left.columns]
            + [
                combined_table[get_column_right(col.get_name())]
                for col in right.columns
            ]
        )
        combined_expr = core.ArrayValue(
            left._session,
            combined_table,
            columns=columns,
            hidden_ordering_columns=hidden_columns,
            ordering=ordering,
        )
        if sort:
            combined_expr = combined_expr.order_by(
                [
                    core.OrderingColumnReference(join_key_col.get_name())
                    for join_key_col in join_key_cols
                ]
            )
        return (
            combined_expr,
            [key.get_name() for key in join_key_cols],
            (get_column_left, get_column_right),
        )


def get_join_cols(
    left_join_cols: typing.Iterable[ibis_types.Value],
    right_join_cols: typing.Iterable[ibis_types.Value],
    how: str,
    coalesce_join_keys: bool = True,
) -> typing.List[ibis_types.Value]:
    join_key_cols: list[ibis_types.Value] = []
    for left_col, right_col in zip(left_join_cols, right_join_cols):
        if not coalesce_join_keys:
            join_key_cols.append(
                left_col.name(bigframes.core.guid.generate_guid(prefix="index_"))
            )
            join_key_cols.append(
                right_col.name(bigframes.core.guid.generate_guid(prefix="index_"))
            )
        else:
            if how == "left" or how == "inner":
                join_key_cols.append(
                    left_col.name(bigframes.core.guid.generate_guid(prefix="index_"))
                )
            elif how == "right":
                join_key_cols.append(
                    right_col.name(bigframes.core.guid.generate_guid(prefix="index_"))
                )
            elif how == "outer":
                # The left index and the right index might contain null values, for
                # example due to an outer join with different numbers of rows. Coalesce
                # these to take the index value from either column.
                # Use a random name in case the left index and the right index have the
                # same name. In such a case, _x and _y suffixes will already be used.
                # Don't need to coalesce if they are exactly the same column.
                if left_col.name("index").equals(right_col.name("index")):
                    join_key_cols.append(
                        left_col.name(
                            bigframes.core.guid.generate_guid(prefix="index_")
                        )
                    )
                else:
                    join_key_cols.append(
                        ibis.coalesce(
                            left_col,
                            right_col,
                        ).name(bigframes.core.guid.generate_guid(prefix="index_"))
                    )
            else:
                raise ValueError(
                    f"Unexpected join type: {how}. {constants.FEEDBACK_LINK}"
                )
    return join_key_cols


def value_to_join_key(value: ibis_types.Value):
    """Converts nullable values to non-null string SQL will not match null keys together - but pandas does."""
    if not value.type().is_string():
        value = value.cast(ibis_dtypes.str)
    return value.fillna(ibis_types.literal("$NULL_SENTINEL$"))


def _merge_order_ids(
    left_id: ibis_types.StringColumn,
    left_encoding_size: int,
    right_id: ibis_types.StringColumn,
    right_encoding_size: int,
    how: str,
) -> ibis_types.StringColumn:
    if how == "right":
        return _merge_order_ids(
            right_id, right_encoding_size, left_id, left_encoding_size, "left"
        )

    if how == "left":
        right_id = typing.cast(
            ibis_types.StringColumn,
            right_id.fillna(ibis_types.literal(":" * right_encoding_size)),
        )
    elif how != "inner":  # outer join
        left_id = typing.cast(
            ibis_types.StringColumn,
            left_id.fillna(ibis_types.literal(":" * left_encoding_size)),
        )
        right_id = typing.cast(
            ibis_types.StringColumn,
            right_id.fillna(ibis_types.literal(":" * right_encoding_size)),
        )
    return (left_id + right_id).name(
        bigframes.core.guid.generate_guid(prefix="bigframes_ordering_id_")
    )
