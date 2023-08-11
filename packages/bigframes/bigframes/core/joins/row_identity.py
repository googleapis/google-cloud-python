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

import functools
import typing
from typing import Callable, Tuple

import ibis
import ibis.expr.types as ibis_types

import bigframes.constants as constants
import bigframes.core as core

SUPPORTED_ROW_IDENTITY_HOW = {"outer", "left", "inner"}


def join_by_row_identity(
    left: core.ArrayValue, right: core.ArrayValue, *, how: str
) -> Tuple[core.ArrayValue, Tuple[Callable[[str], str], Callable[[str], str]],]:
    """Compute join when we are joining by row identity not a specific column."""
    if how not in SUPPORTED_ROW_IDENTITY_HOW:
        raise NotImplementedError(
            f"Only how='outer','left','inner' currently supported. {constants.FEEDBACK_LINK}"
        )

    if not left.table.equals(right.table):
        raise ValueError(
            "Cannot combine objects without an explicit join/merge key. "
            f"Left based on: {left.table.compile()}, but "
            f"right based on: {right.table.compile()}"
        )

    left_predicates = left._predicates
    right_predicates = right._predicates
    # TODO(tbergeron): Skip generating these for inner part of join
    (
        left_relative_predicates,
        right_relative_predicates,
    ) = _get_relative_predicates(left_predicates, right_predicates)

    combined_predicates = []
    if left_predicates or right_predicates:
        joined_predicates = _join_predicates(
            left_predicates, right_predicates, join_type=how
        )
        combined_predicates = list(joined_predicates)  # builder expects mutable list

    left_mask = left_relative_predicates if how in ["right", "outer"] else None
    right_mask = right_relative_predicates if how in ["left", "outer"] else None
    joined_columns = [
        _mask_value(left.get_column(key), left_mask).name(map_left_id(key))
        for key in left.column_names.keys()
    ] + [
        _mask_value(right.get_column(key), right_mask).name(map_right_id(key))
        for key in right.column_names.keys()
    ]

    # If left isn't being masked, can just use left ordering
    if not left_mask:
        col_mapping = {
            order_ref.column_id: map_left_id(order_ref.column_id)
            for order_ref in left._ordering.ordering_value_columns
        }
        new_ordering = left._ordering.with_column_remap(col_mapping)
    else:
        ordering_columns = [
            col_ref.with_name(map_left_id(col_ref.column_id))
            for col_ref in left._ordering.ordering_value_columns
        ] + [
            col_ref.with_name(map_right_id(col_ref.column_id))
            for col_ref in right._ordering.ordering_value_columns
        ]
        left_total_order_cols = frozenset(
            map_left_id(col) for col in left._ordering.total_ordering_columns
        )
        # Assume that left ordering is sufficient since 1:1 join over same base table
        join_total_order_cols = left_total_order_cols
        new_ordering = core.ExpressionOrdering(
            ordering_columns, total_ordering_columns=join_total_order_cols
        )

    hidden_ordering_columns = [
        left._get_hidden_ordering_column(key.column_id).name(map_left_id(key.column_id))
        for key in left._ordering.ordering_value_columns
        if key.column_id in left._hidden_ordering_column_names.keys()
    ] + [
        right._get_hidden_ordering_column(key.column_id).name(
            map_right_id(key.column_id)
        )
        for key in right._ordering.ordering_value_columns
        if key.column_id in right._hidden_ordering_column_names.keys()
    ]

    joined_expr = core.ArrayValue(
        left._session,
        left.table,
        columns=joined_columns,
        hidden_ordering_columns=hidden_ordering_columns,
        ordering=new_ordering,
        predicates=combined_predicates,
    )
    return joined_expr, (
        lambda key: map_left_id(key),
        lambda key: map_right_id(key),
    )


def map_left_id(left_side_id):
    return f"{left_side_id}_x"


def map_right_id(right_side_id):
    return f"{right_side_id}_y"


def _mask_value(
    value: ibis_types.Value,
    predicates: typing.Optional[typing.Sequence[ibis_types.BooleanValue]] = None,
):
    if predicates:
        return (
            ibis.case()
            .when(_reduce_predicate_list(predicates), value)
            .else_(ibis.null())
            .end()
        )
    return value


def _join_predicates(
    left_predicates: typing.Collection[ibis_types.BooleanValue],
    right_predicates: typing.Collection[ibis_types.BooleanValue],
    join_type: str = "outer",
) -> typing.Tuple[ibis_types.BooleanValue, ...]:
    """Combines predicates lists for each side of a join."""
    if join_type == "outer":
        if not left_predicates:
            return ()
        if not right_predicates:
            return ()
        # TODO(tbergeron): Investigate factoring out common predicates
        joined_predicates = _reduce_predicate_list(left_predicates).__or__(
            _reduce_predicate_list(right_predicates)
        )
        return (joined_predicates,)
    if join_type == "left":
        return tuple(left_predicates)
    if join_type == "inner":
        _, right_relative_predicates = _get_relative_predicates(
            left_predicates, right_predicates
        )
        return (*left_predicates, *right_relative_predicates)
    else:
        raise ValueError(
            f"Unsupported join_type: {join_type}. {constants.FEEDBACK_LINK}"
        )


def _get_relative_predicates(
    left_predicates: typing.Collection[ibis_types.BooleanValue],
    right_predicates: typing.Collection[ibis_types.BooleanValue],
) -> tuple[
    typing.Tuple[ibis_types.BooleanValue, ...],
    typing.Tuple[ibis_types.BooleanValue, ...],
]:
    """Get predicates that apply to only one side of the join. Not strictly necessary but simplifies resulting query."""
    left_relative_predicates = tuple(left_predicates) or ()
    right_relative_predicates = tuple(right_predicates) or ()
    if left_predicates and right_predicates:
        # Factor out common predicates needed for left/right column masking
        left_relative_predicates = tuple(set(left_predicates) - set(right_predicates))
        right_relative_predicates = tuple(set(right_predicates) - set(left_predicates))
    return (left_relative_predicates, right_relative_predicates)


def _reduce_predicate_list(
    predicate_list: typing.Collection[ibis_types.BooleanValue],
) -> ibis_types.BooleanValue:
    """Converts a list of predicates BooleanValues into a single BooleanValue."""
    if len(predicate_list) == 0:
        raise ValueError("Cannot reduce empty list of predicates")
    if len(predicate_list) == 1:
        (item,) = predicate_list
        return item
    return functools.reduce(lambda acc, pred: acc.__and__(pred), predicate_list)
