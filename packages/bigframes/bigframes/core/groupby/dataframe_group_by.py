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
from typing import Literal, Sequence, Tuple, Union

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.core.groupby as vendored_pandas_groupby
import numpy
import pandas as pd

from bigframes import session
from bigframes.core import expression as ex
from bigframes.core import log_adapter
import bigframes.core.block_transforms as block_ops
import bigframes.core.blocks as blocks
from bigframes.core.groupby import aggs, series_group_by
import bigframes.core.ordering as order
import bigframes.core.utils as utils
import bigframes.core.validations as validations
from bigframes.core.window import rolling
import bigframes.core.window as windows
import bigframes.core.window_spec as window_specs
import bigframes.dataframe as df
import bigframes.dtypes as dtypes
import bigframes.operations.aggregations as agg_ops
import bigframes.series as series


@log_adapter.class_logger
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

    @property
    def _session(self) -> session.Session:
        return self._block.session

    def __getitem__(
        self,
        key: typing.Union[
            blocks.Label,
            typing.Sequence[blocks.Label],
        ],
    ):
        import bigframes._tools.strings

        if utils.is_list_like(key):
            keys = list(key)
        else:
            keys = [key]

        bad_keys = [key for key in keys if key not in self._block.column_labels]

        # Raise a KeyError message with the possible correct key(s)
        if len(bad_keys) > 0:
            possible_key = []
            for bad_key in bad_keys:
                possible_key.append(
                    min(
                        self._block.column_labels,
                        key=lambda item: bigframes._tools.strings.levenshtein_distance(
                            bad_key, item
                        ),
                    )
                )
            raise KeyError(
                f"Columns not found: {str(bad_keys)[1:-1]}. Did you mean {str(possible_key)[1:-1]}?"
            )

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
            return series_group_by.SeriesGroupBy(
                self._block,
                columns[0],
                self._by_col_ids,
                value_name=self._col_id_labels[columns[0]],
                dropna=self._dropna,
            )

    @validations.requires_ordering()
    def head(self, n: int = 5) -> df.DataFrame:
        block = self._block
        if self._dropna:
            block = block_ops.dropna(self._block, self._by_col_ids, how="any")
        return df.DataFrame(
            block.grouped_head(
                by_column_ids=self._by_col_ids,
                value_columns=self._block.value_columns,
                n=n,
            )
        )

    def size(self) -> typing.Union[df.DataFrame, series.Series]:
        agg_block, _ = self._block.aggregate_size(
            by_column_ids=self._by_col_ids,
            dropna=self._dropna,
        )
        agg_block = agg_block.with_column_labels(pd.Index(["size"]))
        dataframe = df.DataFrame(agg_block)

        if self._as_index:
            series = dataframe["size"]
            return series.rename(None)
        else:
            return self._convert_index(dataframe)

    def sum(self, numeric_only: bool = False, *args) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("sum")
        return self._aggregate_all(agg_ops.sum_op, numeric_only=True)

    def mean(self, numeric_only: bool = False, *args) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("mean")
        return self._aggregate_all(agg_ops.mean_op, numeric_only=True)

    def median(self, numeric_only: bool = False, *, exact: bool = True) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("median")
        if exact:
            return self.quantile(0.5)
        return self._aggregate_all(agg_ops.median_op, numeric_only=True)

    def rank(
        self, method="average", ascending: bool = True, na_option: str = "keep"
    ) -> df.DataFrame:
        return df.DataFrame(
            block_ops.rank(
                self._block,
                method,
                na_option,
                ascending,
                grouping_cols=tuple(self._by_col_ids),
                columns=tuple(self._selected_cols),
            )
        )

    def quantile(
        self, q: Union[float, Sequence[float]] = 0.5, *, numeric_only: bool = False
    ) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("quantile")
        q_cols = tuple(
            col
            for col in self._selected_cols
            if self._column_type(col) in dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE
        )
        multi_q = utils.is_list_like(q)
        result = block_ops.quantile(
            self._block,
            q_cols,
            qs=tuple(q) if multi_q else (q,),  # type: ignore
            grouping_column_ids=self._by_col_ids,
            dropna=self._dropna,
        )
        result_df = df.DataFrame(result)
        if multi_q:
            return result_df.stack()
        else:
            return result_df.droplevel(-1, 1)

    def min(self, numeric_only: bool = False, *args) -> df.DataFrame:
        return self._aggregate_all(agg_ops.min_op, numeric_only=numeric_only)

    def max(self, numeric_only: bool = False, *args) -> df.DataFrame:
        return self._aggregate_all(agg_ops.max_op, numeric_only=numeric_only)

    def std(
        self,
        *,
        numeric_only: bool = False,
    ) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("std")
        return self._aggregate_all(agg_ops.std_op, numeric_only=True)

    def var(
        self,
        *,
        numeric_only: bool = False,
    ) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("var")
        return self._aggregate_all(agg_ops.var_op, numeric_only=True)

    def skew(
        self,
        *,
        numeric_only: bool = False,
    ) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("skew")
        block = block_ops.skew(self._block, self._selected_cols, self._by_col_ids)
        return df.DataFrame(block)

    def kurt(
        self,
        *,
        numeric_only: bool = False,
    ) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("kurt")
        block = block_ops.kurt(self._block, self._selected_cols, self._by_col_ids)
        return df.DataFrame(block)

    kurtosis = kurt

    def all(self) -> df.DataFrame:
        return self._aggregate_all(agg_ops.all_op)

    def any(self) -> df.DataFrame:
        return self._aggregate_all(agg_ops.any_op)

    def count(self) -> df.DataFrame:
        return self._aggregate_all(agg_ops.count_op)

    def nunique(self) -> df.DataFrame:
        return self._aggregate_all(agg_ops.nunique_op)

    @validations.requires_ordering()
    def cumcount(self, ascending: bool = True) -> series.Series:
        window_spec = (
            window_specs.cumulative_rows(grouping_keys=tuple(self._by_col_ids))
            if ascending
            else window_specs.inverse_cumulative_rows(
                grouping_keys=tuple(self._by_col_ids)
            )
        )
        block, result_id = self._block.apply_analytic(
            ex.NullaryAggregation(agg_ops.size_op),
            window=window_spec,
            result_label=None,
        )
        result = series.Series(block.select_column(result_id)) - 1
        if self._dropna and (len(self._by_col_ids) == 1):
            result = result.mask(
                series.Series(block.select_column(self._by_col_ids[0])).isna()
            )
        return result

    @validations.requires_ordering()
    def cumsum(self, *args, numeric_only: bool = False, **kwargs) -> df.DataFrame:
        if not numeric_only:
            self._raise_on_non_numeric("cumsum")
        return self._apply_window_op(agg_ops.sum_op, numeric_only=True)

    @validations.requires_ordering()
    def cummin(self, *args, numeric_only: bool = False, **kwargs) -> df.DataFrame:
        return self._apply_window_op(agg_ops.min_op, numeric_only=numeric_only)

    @validations.requires_ordering()
    def cummax(self, *args, numeric_only: bool = False, **kwargs) -> df.DataFrame:
        return self._apply_window_op(agg_ops.max_op, numeric_only=numeric_only)

    @validations.requires_ordering()
    def cumprod(self, *args, **kwargs) -> df.DataFrame:
        return self._apply_window_op(agg_ops.product_op, numeric_only=True)

    @validations.requires_ordering()
    def shift(self, periods=1) -> series.Series:
        # Window framing clause is not allowed for analytic function lag.
        window = window_specs.unbound(
            grouping_keys=tuple(self._by_col_ids),
        )
        return self._apply_window_op(agg_ops.ShiftOp(periods), window=window)

    @validations.requires_ordering()
    def diff(self, periods=1) -> series.Series:
        # Window framing clause is not allowed for analytic function lag.
        window = window_specs.rows(
            grouping_keys=tuple(self._by_col_ids),
        )
        return self._apply_window_op(agg_ops.DiffOp(periods), window=window)

    @validations.requires_ordering()
    def rolling(
        self,
        window: int | pd.Timedelta | numpy.timedelta64 | datetime.timedelta | str,
        min_periods=None,
        on: str | None = None,
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
            skip_agg_col_id = (
                None if on is None else self._block.resolve_label_exact_or_error(on)
            )
            return windows.Window(
                block,
                window_spec,
                self._selected_cols,
                drop_null_groups=self._dropna,
                skip_agg_column_id=skip_agg_col_id,
            )

        return rolling.create_range_window(
            self._block,
            window,
            min_periods=min_periods,
            value_column_ids=self._selected_cols,
            on=on,
            closed=closed,
            is_series=False,
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
            block, window_spec, self._selected_cols, drop_null_groups=self._dropna
        )

    def agg(self, func=None, **kwargs) -> typing.Union[df.DataFrame, series.Series]:
        if func:
            if isinstance(func, str):
                return self.size() if func == "size" else self._agg_string(func)
            elif utils.is_dict_like(func):
                return self._agg_dict(func)
            elif utils.is_list_like(func):
                return self._agg_list(func)
            else:
                raise NotImplementedError(
                    f"Aggregate with {func} not supported. {constants.FEEDBACK_LINK}"
                )
        else:
            return self._agg_named(**kwargs)

    def _agg_string(self, func: str) -> df.DataFrame:
        ids, labels = self._aggregated_columns()
        aggregations = [
            aggs.agg(col_id, agg_ops.lookup_agg_func(func)) for col_id in ids
        ]
        agg_block, _ = self._block.aggregate(
            by_column_ids=self._by_col_ids,
            aggregations=aggregations,
            dropna=self._dropna,
            column_labels=labels,
        )
        dataframe = df.DataFrame(agg_block)
        return dataframe if self._as_index else self._convert_index(dataframe)

    def _agg_dict(self, func: typing.Mapping) -> df.DataFrame:
        aggregations: typing.List[ex.Aggregation] = []
        column_labels = []

        want_aggfunc_level = any(utils.is_list_like(aggs) for aggs in func.values())

        for label, funcs_for_id in func.items():
            col_id = self._resolve_label(label)
            func_list = (
                funcs_for_id if utils.is_list_like(funcs_for_id) else [funcs_for_id]
            )
            for f in func_list:
                aggregations.append(aggs.agg(col_id, agg_ops.lookup_agg_func(f)))
                column_labels.append(label)
        agg_block, _ = self._block.aggregate(
            by_column_ids=self._by_col_ids,
            aggregations=aggregations,
            dropna=self._dropna,
        )
        if want_aggfunc_level:
            agg_block = agg_block.with_column_labels(
                utils.combine_indices(
                    pd.Index(column_labels),
                    pd.Index(
                        typing.cast(agg_ops.AggregateOp, agg.op).name
                        for agg in aggregations
                    ),
                )
            )
        else:
            agg_block = agg_block.with_column_labels(pd.Index(column_labels))
        dataframe = df.DataFrame(agg_block)
        return dataframe if self._as_index else self._convert_index(dataframe)

    def _agg_list(self, func: typing.Sequence) -> df.DataFrame:
        ids, labels = self._aggregated_columns()
        aggregations = [
            aggs.agg(col_id, agg_ops.lookup_agg_func(f)) for col_id in ids for f in func
        ]

        if self._block.column_labels.nlevels > 1:
            # Restructure MultiIndex for proper format: (idx1, idx2, func)
            # rather than ((idx1, idx2), func).
            column_labels = [
                tuple(label) + (f,)
                for label in labels.to_frame(index=False).to_numpy()
                for f in func
            ]
        else:  # Single-level index
            column_labels = [(label, f) for label in labels for f in func]

        agg_block, _ = self._block.aggregate(
            by_column_ids=self._by_col_ids,
            aggregations=aggregations,
            dropna=self._dropna,
        )
        agg_block = agg_block.with_column_labels(
            pd.MultiIndex.from_tuples(
                column_labels, names=[*self._block.column_labels.names, None]
            )
        )
        dataframe = df.DataFrame(agg_block)
        return dataframe if self._as_index else self._convert_index(dataframe)

    def _agg_named(self, **kwargs) -> df.DataFrame:
        aggregations = []
        column_labels = []
        for k, v in kwargs.items():
            if not isinstance(k, str):
                raise NotImplementedError(
                    f"Only string aggregate names supported. {constants.FEEDBACK_LINK}"
                )
            if not isinstance(v, tuple) or (len(v) != 2):
                raise TypeError("kwargs values must be 2-tuples of column, aggfunc")
            col_id = self._resolve_label(v[0])
            aggregations.append(aggs.agg(col_id, agg_ops.lookup_agg_func(v[1])))
            column_labels.append(k)
        agg_block, _ = self._block.aggregate(
            by_column_ids=self._by_col_ids,
            aggregations=aggregations,
            dropna=self._dropna,
        )
        agg_block = agg_block.with_column_labels(column_labels)
        dataframe = df.DataFrame(agg_block)
        return dataframe if self._as_index else self._convert_index(dataframe)

    def _convert_index(self, dataframe: df.DataFrame):
        """Convert index levels to columns except where names conflict."""
        levels_to_drop = [
            level for level in dataframe.index.names if level in dataframe.columns
        ]

        if len(levels_to_drop) == dataframe.index.nlevels:
            return dataframe.reset_index(drop=True)
        return dataframe.droplevel(levels_to_drop).reset_index(drop=False)

    aggregate = agg

    def _raise_on_non_numeric(self, op: str):
        if not all(
            self._column_type(col) in dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE
            for col in self._selected_cols
        ):
            raise NotImplementedError(
                f"'{op}' does not support non-numeric columns. "
                "Set 'numeric_only'=True to ignore non-numeric columns. "
                f"{constants.FEEDBACK_LINK}"
            )
        return self

    def _aggregated_columns(
        self, numeric_only: bool = False
    ) -> Tuple[typing.Sequence[str], pd.Index]:
        valid_agg_cols: list[str] = []
        offsets: list[int] = []
        for i, col_id in enumerate(self._block.value_columns):
            is_numeric = (
                self._column_type(col_id) in dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE
            )
            if (col_id in self._selected_cols) and (is_numeric or not numeric_only):
                offsets.append(i)
                valid_agg_cols.append(col_id)
        return valid_agg_cols, self._block.column_labels.take(offsets)

    def _column_type(self, col_id: str) -> dtypes.Dtype:
        col_offset = self._block.value_columns.index(col_id)
        dtype = self._block.dtypes[col_offset]
        return dtype

    def _aggregate_all(
        self, aggregate_op: agg_ops.UnaryAggregateOp, numeric_only: bool = False
    ) -> df.DataFrame:
        aggregated_col_ids, labels = self._aggregated_columns(numeric_only=numeric_only)
        aggregations = [aggs.agg(col_id, aggregate_op) for col_id in aggregated_col_ids]
        result_block, _ = self._block.aggregate(
            by_column_ids=self._by_col_ids,
            aggregations=aggregations,
            column_labels=labels,
            dropna=self._dropna,
        )
        dataframe = df.DataFrame(result_block)
        return dataframe if self._as_index else self._convert_index(dataframe)

    def _apply_window_op(
        self,
        op: agg_ops.UnaryWindowOp,
        window: typing.Optional[window_specs.WindowSpec] = None,
        numeric_only: bool = False,
    ):
        """Apply window op to groupby. Defaults to grouped cumulative window."""
        window_spec = window or window_specs.cumulative_rows(
            grouping_keys=tuple(self._by_col_ids)
        )
        columns, _ = self._aggregated_columns(numeric_only=numeric_only)
        block, result_ids = self._block.multi_apply_window_op(
            columns,
            op,
            window_spec=window_spec,
        )
        result = df.DataFrame(block.select_columns(result_ids))
        return result

    def _resolve_label(self, label: blocks.Label) -> str:
        """Resolve label to column id."""
        col_ids = self._block.label_to_col_id.get(label, ())
        if len(col_ids) > 1:
            raise ValueError(f"Label {label} is ambiguous")
        if len(col_ids) == 0:
            raise ValueError(f"Label {label} does not match any columns")
        return col_ids[0]
