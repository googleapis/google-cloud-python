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

import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.operations.aggregations as agg_ops
import third_party.bigframes_vendored.pandas.core.window.rolling as vendored_pandas_rolling

if typing.TYPE_CHECKING:
    from bigframes.series import Series


class Window(vendored_pandas_rolling.Window):
    __doc__ = vendored_pandas_rolling.Window.__doc__

    # TODO(tbergeron): Windows with groupings should create multi-indexed results

    def __init__(
        self,
        block: blocks.Block,
        window_spec: core.WindowSpec,
        value_column_id: str,
    ):
        self._block = block
        self._window_spec = window_spec
        self._value_column_id = value_column_id

    def count(self) -> Series:
        return self._apply_aggregate(agg_ops.count_op)

    def sum(self) -> Series:
        return self._apply_aggregate(agg_ops.sum_op)

    def mean(self) -> Series:
        return self._apply_aggregate(agg_ops.mean_op)

    def var(self) -> Series:
        return self._apply_aggregate(agg_ops.var_op)

    def std(self) -> Series:
        return self._apply_aggregate(agg_ops.std_op)

    def max(self) -> Series:
        return self._apply_aggregate(agg_ops.max_op)

    def min(self) -> Series:
        return self._apply_aggregate(agg_ops.min_op)

    def _apply_aggregate(
        self,
        op: agg_ops.AggregateOp,
    ) -> Series:
        block = self._block
        label = block.col_id_to_label[self._value_column_id]
        block, result_id = block.apply_window_op(
            self._value_column_id, op, self._window_spec, result_label=label
        )

        if self._window_spec.grouping_keys:
            original_index_ids = block.index_columns
            block = block.reset_index(drop=False)
            index_ids = (
                *[col for col in self._window_spec.grouping_keys],
                *original_index_ids,
            )
            block = block.set_index(col_ids=index_ids)

        from bigframes.series import Series

        return Series(block.select_column(result_id))
