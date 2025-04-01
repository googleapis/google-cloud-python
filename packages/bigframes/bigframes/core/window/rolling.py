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

import typing

import bigframes_vendored.pandas.core.window.rolling as vendored_pandas_rolling

from bigframes.core import log_adapter, window_spec
import bigframes.core.blocks as blocks
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
        agg_col_ids = [
            col_id
            for col_id in self._value_column_ids
            if col_id != self._skip_agg_column_id
        ]
        agg_block = self._aggregate_block(op, agg_col_ids)

        if self._skip_agg_column_id is not None:
            # Concat the skipped column to the result.
            agg_block, _ = agg_block.join(
                self._block.select_column(self._skip_agg_column_id), how="outer"
            )

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

    def _aggregate_block(
        self, op: agg_ops.UnaryAggregateOp, agg_col_ids: typing.List[str]
    ) -> blocks.Block:
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
        return block.select_columns(result_ids).with_column_labels(labels)
