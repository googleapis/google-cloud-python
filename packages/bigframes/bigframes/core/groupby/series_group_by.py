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

import datetime
import typing
from typing import Iterable, Literal, Sequence, Tuple, Union

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.core.groupby as vendored_pandas_groupby
import numpy
import pandas

from bigframes import session
from bigframes.core import expression as ex
from bigframes.core import log_adapter
import bigframes.core.block_transforms as block_ops
import bigframes.core.blocks as blocks
from bigframes.core.groupby import aggs, group_by
import bigframes.core.ordering as order
import bigframes.core.utils as utils
import bigframes.core.validations as validations
from bigframes.core.window import rolling
import bigframes.core.window as windows
import bigframes.core.window_spec as window_specs
import bigframes.dataframe as df
import bigframes.dtypes
import bigframes.operations.aggregations as agg_ops
import bigframes.series as series


@log_adapter.class_logger
class SeriesGroupBy(vendored_pandas_groupby.SeriesGroupBy):
    __doc__ = vendored_pandas_groupby.GroupBy.__doc__

    def __init__(
        self,
        block: blocks.Block,
        value_column: str,
        by_col_ids: typing.Sequence[str],
        value_name: blocks.Label = None,
        dropna=True,
        *,
        by_key_is_singular: bool = False,
    ):
        # TODO(tbergeron): Support more group-by expression types
        self._block = block
        self._value_column = value_column
        self._by_col_ids = by_col_ids
        self._value_name = value_name
        self._dropna = dropna  # Applies to aggregations but not windowing

        self._by_key_is_singular = by_key_is_singular
        if by_key_is_singular:
            assert len(by_col_ids) == 1, "singular key should be exactly one group key"

    @property
    def _session(self) -> session.Session:
        return self._block.session

    @validations.requires_ordering()
    def head(self, n: int = 5) -> series.Series:
        block = self._block
        if self._dropna:
            block = block_ops.dropna(self._block, self._by_col_ids, how="any")
        return series.Series(
            block.grouped_head(
                by_column_ids=self._by_col_ids, value_columns=[self._value_column], n=n
            )
        )

    def describe(self, include: None | Literal["all"] = None):
        from bigframes.pandas.core.methods import describe

        return df.DataFrame(
            describe._describe(
                self._block,
                columns=[self._value_column],
                include=include,
                as_index=True,
                by_col_ids=self._by_col_ids,
                dropna=self._dropna,
            )
        ).droplevel(level=0, axis=1)

    def __iter__(self) -> Iterable[Tuple[blocks.Label, series.Series]]:
        for group_keys, filtered_block in group_by.block_groupby_iter(
            self._block,
            by_col_ids=self._by_col_ids,
            by_key_is_singular=self._by_key_is_singular,
            dropna=self._dropna,
        ):
            filtered_series = series.Series(
                filtered_block.select_column(self._value_column)
            )
            filtered_series.name = self._value_name
            yield group_keys, filtered_series

    def __len__(self) -> int:
        return len(self.agg([]))

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

    def nunique(self) -> series.Series:
        return self._aggregate(agg_ops.nunique_op)

    def sum(self, *args) -> series.Series:
        return self._aggregate(agg_ops.sum_op)

    def mean(self, *args) -> series.Series:
        return self._aggregate(agg_ops.mean_op)

    def rank(
        self,
        method="average",
        ascending: bool = True,
        na_option: str = "keep",
        pct: bool = False,
    ) -> series.Series:
        return series.Series(
            block_ops.rank(
                self._block,
                method,
                na_option,
                ascending,
                grouping_cols=tuple(self._by_col_ids),
                columns=(self._value_column,),
                pct=pct,
            )
        )

    def median(
        self,
        *args,
        exact: bool = True,
        **kwargs,
    ) -> series.Series:
        if exact:
            return self.quantile(0.5)
        else:
            return self._aggregate(agg_ops.median_op)

    def quantile(
        self, q: Union[float, Sequence[float]] = 0.5, *, numeric_only: bool = False
    ) -> series.Series:
        multi_q = utils.is_list_like(q)
        result = block_ops.quantile(
            self._block,
            (self._value_column,),
            qs=tuple(q) if multi_q else (q,),  # type: ignore
            grouping_column_ids=self._by_col_ids,
            dropna=self._dropna,
        )
        if multi_q:
            return series.Series(result.stack())
        else:
            return series.Series(result.stack()).droplevel(-1)

    def std(self, *args, **kwargs) -> series.Series:
        return self._aggregate(agg_ops.std_op)

    def var(self, *args, **kwargs) -> series.Series:
        return self._aggregate(agg_ops.var_op)

    def size(self) -> series.Series:
        agg_block, _ = self._block.aggregate_size(
            by_column_ids=self._by_col_ids,
            dropna=self._dropna,
        )
        return series.Series(agg_block.with_column_labels([self._value_name]))

    def skew(self, *args, **kwargs) -> series.Series:
        block = block_ops.skew(self._block, [self._value_column], self._by_col_ids)
        return series.Series(block)

    def kurt(self, *args, **kwargs) -> series.Series:
        block = block_ops.kurt(self._block, [self._value_column], self._by_col_ids)
        return series.Series(block)

    kurtosis = kurt

    @validations.requires_ordering()
    def first(self, numeric_only: bool = False, min_count: int = -1) -> series.Series:
        if numeric_only and not bigframes.dtypes.is_numeric(
            self._block.expr.get_column_type(self._value_column)
        ):
            raise TypeError(
                f"Cannot use 'numeric_only' with non-numeric column {self._value_name}."
            )
        window_spec = window_specs.unbound(
            grouping_keys=tuple(self._by_col_ids),
            min_periods=min_count if min_count >= 0 else 0,
        )
        block, firsts_id = self._block.apply_window_op(
            self._value_column,
            agg_ops.FirstNonNullOp(),
            window_spec=window_spec,
        )
        block, _ = block.aggregate(
            self._by_col_ids,
            (aggs.agg(firsts_id, agg_ops.AnyValueOp()),),
            dropna=self._dropna,
        )
        return series.Series(block.with_column_labels([self._value_name]))

    @validations.requires_ordering()
    def last(self, numeric_only: bool = False, min_count: int = -1) -> series.Series:
        if numeric_only and not bigframes.dtypes.is_numeric(
            self._block.expr.get_column_type(self._value_column)
        ):
            raise TypeError(
                f"Cannot use 'numeric_only' with non-numeric column {self._value_name}."
            )
        window_spec = window_specs.unbound(
            grouping_keys=tuple(self._by_col_ids),
            min_periods=min_count if min_count >= 0 else 0,
        )
        block, firsts_id = self._block.apply_window_op(
            self._value_column,
            agg_ops.LastNonNullOp(),
            window_spec=window_spec,
        )
        block, _ = block.aggregate(
            self._by_col_ids,
            (aggs.agg(firsts_id, agg_ops.AnyValueOp()),),
            dropna=self._dropna,
        )
        return series.Series(block.with_column_labels([self._value_name]))

    def prod(self, *args) -> series.Series:
        return self._aggregate(agg_ops.product_op)

    def agg(self, func=None) -> typing.Union[df.DataFrame, series.Series]:
        column_names: list[str] = []
        if utils.is_dict_like(func):
            raise NotImplementedError(
                f"Aggregate with {func} not supported. {constants.FEEDBACK_LINK}"
            )
        if not utils.is_list_like(func):
            func = [func]

        aggregations = [
            aggs.agg(self._value_column, agg_ops.lookup_agg_func(f)[0]) for f in func
        ]
        column_names = [agg_ops.lookup_agg_func(f)[1] for f in func]

        agg_block, _ = self._block.aggregate(
            by_column_ids=self._by_col_ids,
            aggregations=aggregations,
            dropna=self._dropna,
        )

        if column_names:
            agg_block = agg_block.with_column_labels(column_names)

        if len(aggregations) == 1:
            return series.Series(agg_block)
        return df.DataFrame(agg_block)

    aggregate = agg

    def value_counts(
        self,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ) -> Union[df.DataFrame, series.Series]:
        columns = [self._value_column]
        block = self._block
        if self._dropna:  # this drops null grouping columns
            block = block_ops.dropna(block, self._by_col_ids)
        block = block_ops.value_counts(
            block,
            columns,
            normalize=normalize,
            sort=sort,
            ascending=ascending,
            drop_na=dropna,  # this drops null value columns
            grouping_keys=self._by_col_ids,
        )
        # TODO: once as_index=Fales supported, return DataFrame instead by resetting index
        # with .to_frame().reset_index(drop=False)
        return series.Series(block)

    @validations.requires_ordering()
    def cumsum(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.sum_op,
        )

    @validations.requires_ordering()
    def cumprod(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.product_op,
        )

    @validations.requires_ordering()
    def cummax(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.max_op,
        )

    @validations.requires_ordering()
    def cummin(self, *args, **kwargs) -> series.Series:
        return self._apply_window_op(
            agg_ops.min_op,
        )

    @validations.requires_ordering()
    def cumcount(self, *args, **kwargs) -> series.Series:
        # TODO: Add nullary op support to implement more cleanly
        return (
            self._apply_window_op(
                agg_ops.SizeUnaryOp(),
                discard_name=True,
                never_skip_nulls=True,
            )
            - 1
        )

    @validations.requires_ordering()
    def shift(self, periods=1) -> series.Series:
        """Shift index by desired number of periods."""
        # Window framing clause is not allowed for analytic function lag.
        window = window_specs.rows(
            grouping_keys=tuple(self._by_col_ids),
        )
        return self._apply_window_op(agg_ops.ShiftOp(periods), window=window)

    @validations.requires_ordering()
    def diff(self, periods=1) -> series.Series:
        window = window_specs.rows(
            grouping_keys=tuple(self._by_col_ids),
        )
        return self._apply_window_op(agg_ops.DiffOp(periods), window=window)

    @validations.requires_ordering()
    def rolling(
        self,
        window: int | pandas.Timedelta | numpy.timedelta64 | datetime.timedelta | str,
        min_periods=None,
        closed: Literal["right", "left", "both", "neither"] = "right",
    ) -> windows.Window:
        if isinstance(window, int):
            window_spec = window_specs.WindowSpec(
                bounds=window_specs.RowsWindowBounds.from_window_size(window, closed),
                min_periods=min_periods if min_periods is not None else window,
                grouping_keys=tuple(ex.deref(col) for col in self._by_col_ids),
            )
            block = self._block.order_by(
                [order.ascending_over(col) for col in self._by_col_ids],
            )
            return windows.Window(
                block,
                window_spec,
                [self._value_column],
                drop_null_groups=self._dropna,
                is_series=True,
            )

        return rolling.create_range_window(
            self._block,
            window,
            min_periods=min_periods,
            value_column_ids=[self._value_column],
            closed=closed,
            is_series=True,
            grouping_keys=self._by_col_ids,
            drop_null_groups=self._dropna,
        )

    @validations.requires_ordering()
    def expanding(self, min_periods: int = 1) -> windows.Window:
        window_spec = window_specs.cumulative_rows(
            grouping_keys=tuple(self._by_col_ids),
            min_periods=min_periods,
        )
        block = self._block.order_by(
            [order.ascending_over(col) for col in self._by_col_ids],
        )
        return windows.Window(
            block,
            window_spec,
            [self._value_column],
            drop_null_groups=self._dropna,
            is_series=True,
        )

    def _aggregate(self, aggregate_op: agg_ops.UnaryAggregateOp) -> series.Series:
        result_block, _ = self._block.aggregate(
            self._by_col_ids,
            (aggs.agg(self._value_column, aggregate_op),),
            dropna=self._dropna,
        )

        return series.Series(result_block.with_column_labels([self._value_name]))

    def _apply_window_op(
        self,
        op: agg_ops.UnaryWindowOp,
        discard_name=False,
        window: typing.Optional[window_specs.WindowSpec] = None,
        never_skip_nulls: bool = False,
    ) -> series.Series:
        """Apply window op to groupby. Defaults to grouped cumulative window."""
        window_spec = window or window_specs.cumulative_rows(
            grouping_keys=tuple(self._by_col_ids)
        )

        label = self._value_name if not discard_name else None
        block, result_id = self._block.apply_window_op(
            self._value_column,
            op,
            result_label=label,
            window_spec=window_spec,
            never_skip_nulls=never_skip_nulls,
        )
        return series.Series(block.select_column(result_id))
