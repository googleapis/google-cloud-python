# Copyright 2025 Google LLC
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
from __future__ import annotations

import typing

import sqlglot.expressions as sge

from bigframes.core import utils, window_spec
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler
import bigframes.core.ordering as ordering_spec


def apply_window_if_present(
    value: sge.Expression,
    window: typing.Optional[window_spec.WindowSpec] = None,
) -> sge.Expression:
    if window is None:
        return value

    if window.is_row_bounded and not window.ordering:
        raise ValueError("No ordering provided for ordered analytic function")
    elif (
        not window.is_row_bounded
        and not window.is_range_bounded
        and not window.ordering
    ):
        # Unbound grouping window.
        order_by = None
    elif window.is_range_bounded:
        # Note that, when the window is range-bounded, we only need one ordering key.
        # There are two reasons:
        # 1. Manipulating null positions requires more than one ordering key, which
        #  is forbidden by SQL window syntax for range rolling.
        # 2. Pandas does not allow range rolling on timeseries with nulls.
        order_by = get_window_order_by((window.ordering[0],), override_null_order=False)
    else:
        order_by = get_window_order_by(window.ordering, override_null_order=True)

    order = sge.Order(expressions=order_by) if order_by else None

    group_by = (
        [
            scalar_compiler.scalar_op_compiler.compile_expression(key)
            for key in window.grouping_keys
        ]
        if window.grouping_keys
        else None
    )

    # This is the key change. Don't create a spec for the default window frame
    # if there's no ordering. This avoids generating an `ORDER BY NULL` clause.
    if not window.bounds and not order:
        return sge.Window(this=value, partition_by=group_by)

    if not window.bounds:
        return sge.Window(this=value, partition_by=group_by, order=order)

    kind = (
        "ROWS" if isinstance(window.bounds, window_spec.RowsWindowBounds) else "RANGE"
    )

    start: typing.Union[int, float, None] = None
    end: typing.Union[int, float, None] = None
    if isinstance(window.bounds, window_spec.RangeWindowBounds):
        if window.bounds.start is not None:
            start = utils.timedelta_to_micros(window.bounds.start)
        if window.bounds.end is not None:
            end = utils.timedelta_to_micros(window.bounds.end)
    elif window.bounds:
        start = window.bounds.start
        end = window.bounds.end

    start_value, start_side = _get_window_bounds(start, is_preceding=True)
    end_value, end_side = _get_window_bounds(end, is_preceding=False)

    spec = sge.WindowSpec(
        kind=kind,
        start=start_value,
        start_side=start_side,
        end=end_value,
        end_side=end_side,
        over="OVER",
    )

    return sge.Window(this=value, partition_by=group_by, order=order, spec=spec)


def get_window_order_by(
    ordering: typing.Tuple[ordering_spec.OrderingExpression, ...],
    override_null_order: bool = False,
) -> typing.Optional[tuple[sge.Ordered, ...]]:
    """Returns the SQL order by clause for a window specification."""
    if not ordering:
        return None

    order_by = []
    for ordering_spec_item in ordering:
        expr = scalar_compiler.scalar_op_compiler.compile_expression(
            ordering_spec_item.scalar_expression
        )
        desc = not ordering_spec_item.direction.is_ascending
        nulls_first = not ordering_spec_item.na_last

        if override_null_order:
            # Bigquery SQL considers NULLS to be "smallest" values, but we need
            # to override in these cases.
            is_null_expr = sge.Is(this=expr, expression=sge.Null())
            if nulls_first and desc:
                order_by.append(
                    sge.Ordered(
                        this=is_null_expr,
                        desc=desc,
                        nulls_first=nulls_first,
                    )
                )
            elif not nulls_first and not desc:
                order_by.append(
                    sge.Ordered(
                        this=is_null_expr,
                        desc=desc,
                        nulls_first=nulls_first,
                    )
                )

        order_by.append(
            sge.Ordered(
                this=expr,
                desc=desc,
                nulls_first=nulls_first,
            )
        )
    return tuple(order_by)


def _get_window_bounds(
    value, is_preceding: bool
) -> tuple[typing.Union[str, sge.Expression], typing.Optional[str]]:
    """Compiles a single boundary value into its SQL components."""
    if value is None:
        side = "PRECEDING" if is_preceding else "FOLLOWING"
        return "UNBOUNDED", side

    if value == 0:
        return "CURRENT ROW", None

    side = "PRECEDING" if value < 0 else "FOLLOWING"
    return sge.convert(abs(value)), side
