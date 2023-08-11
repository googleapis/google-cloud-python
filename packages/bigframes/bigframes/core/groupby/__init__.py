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

import pandas as pd
import typing_extensions

import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.ordering as order
import bigframes.core.window as windows
import bigframes.dataframe as df
import bigframes.dtypes as dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.series as series
import third_party.bigframes_vendored.pandas.core.groupby as vendored_pandas_groupby


class DataFrameGroupBy(vendored_pandas_groupby.DataFrameGroupBy):
    __doc__ = vendored_pandas_groupby.GroupBy.__doc__

    def __init__(
        self,
        block: blocks.Block,
        by_col_ids: typing.Sequence[str],
        *,
        selected_cols: typing.Optional[typing.Sequence[str]] = None,
        dropna: bool = True,
        as_index: bool = True,
    ):
        # TODO(tbergeron): Support more group-by expression types
        self._block = block
        self._col_id_labels = {
            value_column: column_label
            for value_column, column_label in zip(
                block.value_columns, block.column_labels
            )
        }
        self._by_col_ids = by_col_ids

        self._dropna = dropna
        self._as_index = as_index
        if selected_cols:
            for col in selected_cols:
                if col not in self._block.value_columns:
                    raise ValueError(f"Invalid column selection: {col}")
            self._selected_cols = selected_cols
        else:
            self._selected_cols = [
                col_id
                for col_id in self._block.value_columns
                if col_id not in self._by_col_ids
            ]

    def __getitem__(
        self,
        key: typing.Union[
            blocks.Label,
            typing.Sequence[blocks.Label],
        ],
    ):
        if _is_list_like(key):
            keys = list(key)
        else:
            keys = [key]
        columns = [
            col_id for col_id, label in self._col_id_labels.items() if label in keys
        ]

        if len(columns) > 1 or (not self._as_index):
            return DataFrameGroupBy(
                self._block,
                self._by_col_ids,
                selected_cols=columns,
                dropna=self._dropna,
                as_index=self._as_index,
            )
        else:
            return SeriesGroupBy(
                self._block,
                columns[0],
                self._by_col_ids,
                value_name=self._col_id_labels[columns[0]],
                dropna=self._dropna,
            )

    def sum(self, numeric_only: bool = False, *args) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("sum")
        return self._aggregate(agg_ops.sum_op, numeric_only=True)

    def mean(self, numeric_only: bool = False, *args) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("mean")
        return self._aggregate(agg_ops.mean_op, numeric_only=True)

    def median(
        self, numeric_only: bool = False, *, exact: bool = False
    ) -> df.DataFrame:
        if exact:
            raise NotImplementedError(
                f"Only approximate median is supported. {constants.FEEDBACK_LINK}"
            )
        if not numeric_only:
            self._raise_on_non_numeric("median")
        return self._aggregate(agg_ops.median_op, numeric_only=True)

    def min(self, numeric_only: bool = False, *args) -> df.DataFrame:
        return self._aggregate(agg_ops.min_op, numeric_only=numeric_only)

    def max(self, numeric_only: bool = False, *args) -> df.DataFrame:
        return self._aggregate(agg_ops.max_op, numeric_only=numeric_only)

    def std(
        self,
        *,
        numeric_only: bool = False,
    ) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("std")
        return self._aggregate(agg_ops.std_op, numeric_only=True)

    def var(
        self,
        *,
        numeric_only: bool = False,
    ) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("var")
        return self._aggregate(agg_ops.var_op, numeric_only=True)

    def all(self) -> df.DataFrame:
        return self._aggregate(agg_ops.all_op)

    def any(self) -> df.DataFrame:
        return self._aggregate(agg_ops.any_op)

    def count(self) -> df.DataFrame:
        return self._aggregate(agg_ops.count_op)

    def cumsum(self, *args, numeric_only: bool = False, **kwargs) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("cumsum")
        return self._apply_window_op(agg_ops.sum_op, numeric_only=True)

    def cummin(self, *args, numeric_only: bool = False, **kwargs) -> df.DataFrame:
        return self._apply_window_op(agg_ops.min_op, numeric_only=numeric_only)

    def cummax(self, *args, numeric_only: bool = False, **kwargs) -> df.DataFrame:
        return self._apply_window_op(agg_ops.max_op, numeric_only=numeric_only)

    def cumprod(self, *args, **kwargs) -> df.DataFrame:
        return self._apply_window_op(agg_ops.product_op, numeric_only=True)

    def _raise_on_non_numeric(self, op: str):
        if not all(
            dtype in dtypes.NUMERIC_BIGFRAMES_TYPES for dtype in self._block.dtypes
        ):
            raise NotImplementedError(
                f"'{op}' does not support non-numeric columns. "
                "Set 'numeric_only'=True to ignore non-numeric columns. "
                f"{constants.FEEDBACK_LINK}"
            )
        return self

    def _aggregated_columns(self, numeric_only: bool = False) -> typing.Sequence[str]:
        valid_agg_cols: list[str] = []
        for col_id in self._selected_cols:
            is_numeric = self._column_type(col_id) in dtypes.NUMERIC_BIGFRAMES_TYPES
            if is_numeric or not numeric_only:
                valid_agg_cols.append(col_id)
        return valid_agg_cols

    def _column_type(self, col_id: str) -> dtypes.Dtype:
        col_offset = self._block.value_columns.index(col_id)
        dtype = self._block.dtypes[col_offset]
        return dtype

    def _aggregate(
        self, aggregate_op: agg_ops.AggregateOp, numeric_only: bool = False
    ) -> df.DataFrame:
        aggregated_col_ids = self._aggregated_columns(numeric_only=numeric_only)
        aggregations = [(col_id, aggregate_op) for col_id in aggregated_col_ids]
        result_block, _ = self._block.aggregate(
            by_column_ids=self._by_col_ids,
            aggregations=aggregations,
            as_index=self._as_index,
            dropna=self._dropna,
        )
        return df.DataFrame(result_block)

    def _apply_window_op(
        self,
        op: agg_ops.WindowOp,
        window: typing.Optional[core.WindowSpec] = None,
        numeric_only: bool = False,
    ):
        """Apply window op to groupby. Defaults to grouped cumulative window."""
        window_spec = window or core.WindowSpec(
            grouping_keys=self._by_col_ids, following=0
        )
        columns = self._aggregated_columns(numeric_only=numeric_only)
        block = self._block.multi_apply_window_op(
            columns, op, window_spec=window_spec, skip_null_groups=self._dropna
        )
        block = block.select_columns(columns)
        return df.DataFrame(block)


class SeriesGroupBy(vendored_pandas_groupby.SeriesGroupBy):
    __doc__ = vendored_pandas_groupby.GroupBy.__doc__

    def __init__(
        self,
        block: blocks.Block,
        value_column: str,
        by_col_ids: typing.Sequence[str],
        value_name: typing.Optional[str] = None,
        dropna=True,
    ):
        # TODO(tbergeron): Support more group-by expression types
        self._block = block
        self._value_column = value_column
        self._by_col_ids = by_col_ids
        self._value_name = value_name
        self._dropna = dropna  # Applies to aggregations but not windowing

    @property
    def _value(self):
        return self._block.expr.get_column(self._value_column)

    def all(self) -> series.Series:
        return self._aggregate(agg_ops.all_op)

    def any(self) -> series.Series:
        return self._aggregate(agg_ops.any_op)

    def min(self, *args) -> series.Series:
        return self._aggregate(agg_ops.min_op)

    def max(self, *args) -> series.Series:
        return self._aggregate(agg_ops.max_op)

    def count(self) -> series.Series:
        return self._aggregate(agg_ops.count_op)

    def sum(self, *args) -> series.Series:
        return self._aggregate(agg_ops.sum_op)

    def mean(self, *args) -> series.Series:
        return self._aggregate(agg_ops.mean_op)

    def median(self, *args, **kwargs) -> series.Series:
        return self._aggregate(agg_ops.mean_op)

    def std(self, *args, **kwargs) -> series.Series:
        return self._aggregate(agg_ops.std_op)

    def var(self, *args, **kwargs) -> series.Series:
        return self._aggregate(agg_ops.var_op)

    def prod(self, *args) -> series.Series:
        return self._aggregate(agg_ops.product_op)

    def cumsum(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.sum_op,
        )

    def cumprod(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.product_op,
        )

    def cummax(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.max_op,
        )

    def cummin(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.min_op,
        )

    def cumcount(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.rank_op,
            discard_name=True,
        )._apply_unary_op(ops.partial_right(ops.sub_op, 1))

    def shift(self, periods=1) -> series.Series:
        """Shift index by desired number of periods."""
        window = core.WindowSpec(
            grouping_keys=self._by_col_ids,
            preceding=periods if periods > 0 else None,
            following=-periods if periods < 0 else None,
        )
        return self._apply_window_op(agg_ops.ShiftOp(periods), window=window)

    def diff(self) -> series.Series:
        return self._ungroup() - self.shift(1)

    def rolling(self, window: int, min_periods=None) -> windows.Window:
        # To get n size window, need current row and n-1 preceding rows.
        window_spec = core.WindowSpec(
            grouping_keys=self._by_col_ids,
            preceding=window - 1,
            following=0,
            min_periods=min_periods or window,
        )
        block = self._block.order_by(
            [order.OrderingColumnReference(col) for col in self._by_col_ids],
            stable=True,
        )
        return windows.Window(block, window_spec, self._value_column)

    def expanding(self, min_periods: int = 1) -> windows.Window:
        window_spec = core.WindowSpec(
            grouping_keys=self._by_col_ids,
            following=0,
            min_periods=min_periods,
        )
        block = self._block.order_by(
            [order.OrderingColumnReference(col) for col in self._by_col_ids],
            stable=True,
        )
        return windows.Window(block, window_spec, self._value_column)

    def _ungroup(self) -> series.Series:
        return series.Series(self._block.select_column(self._value_column))

    def _aggregate(self, aggregate_op: agg_ops.AggregateOp) -> series.Series:
        result_block, _ = self._block.aggregate(
            self._by_col_ids,
            ((self._value_column, aggregate_op),),
            dropna=self._dropna,
        )

        return series.Series(result_block.with_column_labels([self._value_name]))

    def _apply_window_op(
        self,
        op: agg_ops.WindowOp,
        discard_name=False,
        window: typing.Optional[core.WindowSpec] = None,
    ):
        """Apply window op to groupby. Defaults to grouped cumulative window."""
        window_spec = window or core.WindowSpec(
            grouping_keys=self._by_col_ids, following=0
        )

        label = self._value_name if not discard_name else None
        block, result_id = self._block.apply_window_op(
            self._value_column,
            op,
            result_label=label,
            window_spec=window_spec,
            skip_null_groups=self._dropna,
        )
        return series.Series(block.select_column(result_id))


def _is_list_like(obj: typing.Any) -> typing_extensions.TypeGuard[typing.Sequence]:
    return pd.api.types.is_list_like(obj)
