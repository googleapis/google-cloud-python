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

from __future__ import annotations

import datetime
import typing

import bigframes_vendored.pandas.core.window.rolling as vendored_pandas_rolling
import numpy
import pandas

from bigframes import dtypes
from bigframes.core import expression as ex
from bigframes.core import log_adapter, ordering, window_spec
import bigframes.core.blocks as blocks
from bigframes.core.window import ordering as window_ordering
import bigframes.operations.aggregations as agg_ops


@log_adapter.class_logger
class Window(vendored_pandas_rolling.Window):
    __doc__ = vendored_pandas_rolling.Window.__doc__

    def __init__(
        self,
        block: blocks.Block,
        window_spec: window_spec.WindowSpec,
        value_column_ids: typing.Sequence[str],
        drop_null_groups: bool = True,
        is_series: bool = False,
        skip_agg_column_id: str | None = None,
    ):
        self._block = block
        self._window_spec = window_spec
        self._value_column_ids = value_column_ids
        self._drop_null_groups = drop_null_groups
        self._is_series = is_series
        # The column ID that won't be aggregated on.
        # This is equivalent to pandas `on` parameter in rolling()
        self._skip_agg_column_id = skip_agg_column_id

    def count(self):
        return self._apply_aggregate(agg_ops.count_op)

    def sum(self):
        return self._apply_aggregate(agg_ops.sum_op)

    def mean(self):
        return self._apply_aggregate(agg_ops.mean_op)

    def var(self):
        return self._apply_aggregate(agg_ops.var_op)

    def std(self):
        return self._apply_aggregate(agg_ops.std_op)

    def max(self):
        return self._apply_aggregate(agg_ops.max_op)

    def min(self):
        return self._apply_aggregate(agg_ops.min_op)

    def _apply_aggregate(
        self,
        op: agg_ops.UnaryAggregateOp,
    ):
        agg_block = self._aggregate_block(op)

        if self._is_series:
            from bigframes.series import Series

            return Series(agg_block)
        else:
            from bigframes.dataframe import DataFrame

            # Preserve column order.
            column_labels = [
                self._block.col_id_to_label[col_id] for col_id in self._value_column_ids
            ]
            return DataFrame(agg_block)._reindex_columns(column_labels)

    def _aggregate_block(self, op: agg_ops.UnaryAggregateOp) -> blocks.Block:
        agg_col_ids = [
            col_id
            for col_id in self._value_column_ids
            if col_id != self._skip_agg_column_id
        ]
        block, result_ids = self._block.multi_apply_window_op(
            agg_col_ids,
            op,
            self._window_spec,
            skip_null_groups=self._drop_null_groups,
            never_skip_nulls=True,
        )

        if self._window_spec.grouping_keys:
            original_index_ids = block.index_columns
            block = block.reset_index(drop=False)
            index_ids = (
                *[col.id.name for col in self._window_spec.grouping_keys],
                *original_index_ids,
            )
            block = block.set_index(col_ids=index_ids)

        labels = [self._block.col_id_to_label[col] for col in agg_col_ids]
        if self._skip_agg_column_id is not None:
            result_ids = [self._skip_agg_column_id, *result_ids]
            labels.insert(0, self._block.col_id_to_label[self._skip_agg_column_id])

        return block.select_columns(result_ids).with_column_labels(labels)


def create_range_window(
    block: blocks.Block,
    window: pandas.Timedelta | numpy.timedelta64 | datetime.timedelta | str,
    *,
    value_column_ids: typing.Sequence[str] = tuple(),
    min_periods: int | None,
    on: str | None = None,
    closed: typing.Literal["right", "left", "both", "neither"],
    is_series: bool,
    grouping_keys: typing.Sequence[str] = tuple(),
    drop_null_groups: bool = True,
) -> Window:

    if on is None:
        # Rolling on index
        index_dtypes = block.index.dtypes
        if len(index_dtypes) > 1:
            raise ValueError("Range rolling on MultiIndex is not supported")
        if index_dtypes[0] != dtypes.TIMESTAMP_DTYPE:
            raise ValueError("Index type should be timestamps with timezones")
        rolling_key_col_id = block.index_columns[0]
    else:
        # Rolling on a specific column
        rolling_key_col_id = block.resolve_label_exact_or_error(on)
        if block.expr.get_column_type(rolling_key_col_id) != dtypes.TIMESTAMP_DTYPE:
            raise ValueError(f"Column {on} type should be timestamps with timezones")

    order_direction = window_ordering.find_order_direction(
        block.expr.node, rolling_key_col_id
    )
    if order_direction is None:
        target_str = "index" if on is None else f"column {on}"
        raise ValueError(
            f"The {target_str} might not be in a monotonic order. Please sort by {target_str} before rolling."
        )
    if isinstance(window, str):
        window = pandas.Timedelta(window)
    spec = window_spec.WindowSpec(
        bounds=window_spec.RangeWindowBounds.from_timedelta_window(window, closed),
        min_periods=1 if min_periods is None else min_periods,
        ordering=(
            ordering.OrderingExpression(ex.deref(rolling_key_col_id), order_direction),
        ),
        grouping_keys=tuple(ex.deref(col) for col in grouping_keys),
    )

    selected_value_col_ids = (
        value_column_ids if value_column_ids else block.value_columns
    )
    # This step must be done after finding the order direction of the window key.
    if grouping_keys:
        block = block.order_by([ordering.ascending_over(col) for col in grouping_keys])

    return Window(
        block,
        spec,
        value_column_ids=selected_value_col_ids,
        is_series=is_series,
        skip_agg_column_id=None if on is None else rolling_key_col_id,
        drop_null_groups=drop_null_groups,
    )
