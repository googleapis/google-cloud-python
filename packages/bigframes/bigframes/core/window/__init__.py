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

from bigframes.core import log_adapter
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.operations.aggregations as agg_ops
import third_party.bigframes_vendored.pandas.core.window.rolling as vendored_pandas_rolling


@log_adapter.class_logger
class Window(vendored_pandas_rolling.Window):
    __doc__ = vendored_pandas_rolling.Window.__doc__

    def __init__(
        self,
        block: blocks.Block,
        window_spec: core.WindowSpec,
        value_column_ids: typing.Sequence[str],
        drop_null_groups: bool = True,
        is_series: bool = False,
    ):
        self._block = block
        self._window_spec = window_spec
        self._value_column_ids = value_column_ids
        self._drop_null_groups = drop_null_groups
        self._is_series = is_series

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
        op: agg_ops.AggregateOp,
    ):
        block = self._block
        labels = [block.col_id_to_label[col] for col in self._value_column_ids]
        block, result_ids = block.multi_apply_window_op(
            self._value_column_ids,
            op,
            self._window_spec,
            skip_null_groups=self._drop_null_groups,
            never_skip_nulls=True,
        )

        if self._window_spec.grouping_keys:
            original_index_ids = block.index_columns
            block = block.reset_index(drop=False)
            index_ids = (
                *[col for col in self._window_spec.grouping_keys],
                *original_index_ids,
            )
            block = block.set_index(col_ids=index_ids)

        if self._is_series:
            from bigframes.series import Series

            return Series(block.select_columns(result_ids).with_column_labels(labels))
        else:
            from bigframes.dataframe import DataFrame

            return DataFrame(
                block.select_columns(result_ids).with_column_labels(labels)
            )
