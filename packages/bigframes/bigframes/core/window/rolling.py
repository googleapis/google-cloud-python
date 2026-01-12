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
from typing import Literal, Mapping, Sequence, TYPE_CHECKING, Union

import bigframes_vendored.pandas.core.window.rolling as vendored_pandas_rolling
import numpy
import pandas

from bigframes import dtypes
from bigframes.core import agg_expressions
from bigframes.core import expression as ex
from bigframes.core import ordering, utils, window_spec
import bigframes.core.blocks as blocks
from bigframes.core.logging import log_adapter
from bigframes.core.window import ordering as window_ordering
import bigframes.operations.aggregations as agg_ops

if TYPE_CHECKING:
    import bigframes.dataframe as df
    import bigframes.series as series


@log_adapter.class_logger
class Window(vendored_pandas_rolling.Window):
    __doc__ = vendored_pandas_rolling.Window.__doc__

    def __init__(
        self,
        block: blocks.Block,
        window_spec: window_spec.WindowSpec,
        value_column_ids: Sequence[str],
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
        return self._apply_aggregate_op(agg_ops.count_op)

    def sum(self):
        return self._apply_aggregate_op(agg_ops.sum_op)

    def mean(self):
        return self._apply_aggregate_op(agg_ops.mean_op)

    def var(self):
        return self._apply_aggregate_op(agg_ops.var_op)

    def std(self):
        return self._apply_aggregate_op(agg_ops.std_op)

    def max(self):
        return self._apply_aggregate_op(agg_ops.max_op)

    def min(self):
        return self._apply_aggregate_op(agg_ops.min_op)

    def agg(self, func) -> Union[df.DataFrame, series.Series]:
        if utils.is_dict_like(func):
            return self._agg_dict(func)
        elif utils.is_list_like(func):
            return self._agg_list(func)
        else:
            return self._agg_func(func)

    aggregate = agg

    def _agg_func(self, func) -> df.DataFrame:
        ids, labels = self._aggregated_columns()
        aggregations = [agg(col_id, agg_ops.lookup_agg_func(func)[0]) for col_id in ids]
        return self._apply_aggs(aggregations, labels)

    def _agg_dict(self, func: Mapping) -> df.DataFrame:
        aggregations: list[agg_expressions.Aggregation] = []
        column_labels = []
        function_labels = []

        want_aggfunc_level = any(utils.is_list_like(aggs) for aggs in func.values())

        for label, funcs_for_id in func.items():
            col_id = self._block.label_to_col_id[label][-1]  # get last matching column
            func_list = (
                funcs_for_id if utils.is_list_like(funcs_for_id) else [funcs_for_id]
            )
            for f in func_list:
                f_op, f_label = agg_ops.lookup_agg_func(f)
                aggregations.append(agg(col_id, f_op))
                column_labels.append(label)
                function_labels.append(f_label)
        if want_aggfunc_level:
            result_labels: pandas.Index = utils.combine_indices(
                pandas.Index(column_labels),
                pandas.Index(function_labels),
            )
        else:
            result_labels = pandas.Index(column_labels)

        return self._apply_aggs(aggregations, result_labels)

    def _agg_list(self, func: Sequence) -> df.DataFrame:
        ids, labels = self._aggregated_columns()
        aggregations = [
            agg(col_id, agg_ops.lookup_agg_func(f)[0]) for col_id in ids for f in func
        ]

        if self._is_series:
            # if series, no need to rebuild
            result_cols_idx = pandas.Index(
                [agg_ops.lookup_agg_func(f)[1] for f in func]
            )
        else:
            if self._block.column_labels.nlevels > 1:
                # Restructure MultiIndex for proper format: (idx1, idx2, func)
                # rather than ((idx1, idx2), func).
                column_labels = [
                    tuple(label) + (agg_ops.lookup_agg_func(f)[1],)
                    for label in labels.to_frame(index=False).to_numpy()
                    for f in func
                ]
            else:  # Single-level index
                column_labels = [
                    (label, agg_ops.lookup_agg_func(f)[1])
                    for label in labels
                    for f in func
                ]
            result_cols_idx = pandas.MultiIndex.from_tuples(
                column_labels, names=[*self._block.column_labels.names, None]
            )
        return self._apply_aggs(aggregations, result_cols_idx)

    def _apply_aggs(
        self, exprs: Sequence[agg_expressions.Aggregation], labels: pandas.Index
    ):
        block, ids = self._block.apply_analytic(
            agg_exprs=exprs,
            window=self._window_spec,
            result_labels=labels,
            skip_null_groups=self._drop_null_groups,
        )

        if self._window_spec.grouping_keys:
            original_index_ids = block.index_columns
            block = block.reset_index(drop=False)
            # grouping keys will always be direct column references, but we should probably
            # refactor this class to enforce this statically
            index_ids = (
                *[col.id.name for col in self._window_spec.grouping_keys],  # type: ignore
                *original_index_ids,
            )
            block = block.set_index(col_ids=index_ids)

        if self._skip_agg_column_id is not None:
            block = block.select_columns([self._skip_agg_column_id, *ids])
        else:
            block = block.select_columns(ids).with_column_labels(labels)

        if self._is_series and (len(block.value_columns) == 1):
            import bigframes.series as series

            return series.Series(block)
        else:
            import bigframes.dataframe as df

            return df.DataFrame(block)

    def _apply_aggregate_op(
        self,
        op: agg_ops.UnaryAggregateOp,
    ):
        ids, labels = self._aggregated_columns()
        aggregations = [agg(col_id, op) for col_id in ids]
        return self._apply_aggs(aggregations, labels)

    def _aggregated_columns(self) -> tuple[Sequence[str], pandas.Index]:
        agg_col_ids = [
            col_id
            for col_id in self._value_column_ids
            if col_id != self._skip_agg_column_id
        ]
        labels: pandas.Index = pandas.Index(
            [self._block.col_id_to_label[col] for col in agg_col_ids]
        )
        return agg_col_ids, labels


def create_range_window(
    block: blocks.Block,
    window: pandas.Timedelta | numpy.timedelta64 | datetime.timedelta | str,
    *,
    value_column_ids: Sequence[str] = tuple(),
    min_periods: int | None,
    on: str | None = None,
    closed: Literal["right", "left", "both", "neither"],
    is_series: bool,
    grouping_keys: Sequence[str] = tuple(),
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


def agg(input: str, op: agg_ops.AggregateOp) -> agg_expressions.Aggregation:
    if isinstance(op, agg_ops.UnaryAggregateOp):
        return agg_expressions.UnaryAggregation(op, ex.deref(input))
    else:
        assert isinstance(op, agg_ops.NullaryAggregateOp)
        return agg_expressions.NullaryAggregation(op)
