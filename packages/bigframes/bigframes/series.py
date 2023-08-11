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

"""Series is a 1 dimensional data structure."""

from __future__ import annotations

import numbers
import textwrap
import typing
from typing import Any, Mapping, Optional, Tuple, Union

import google.cloud.bigquery as bigquery
import ibis.expr.types as ibis_types
import numpy
import pandas
import pandas.core.dtypes.common
import typing_extensions

import bigframes.constants as constants
import bigframes.core
from bigframes.core import WindowSpec
import bigframes.core.block_transforms as block_ops
import bigframes.core.blocks as blocks
import bigframes.core.groupby as groupby
import bigframes.core.indexers
import bigframes.core.indexes as indexes
from bigframes.core.ordering import (
    OrderingColumnReference,
    OrderingDirection,
    STABLE_SORTS,
)
import bigframes.core.scalar as scalars
import bigframes.core.window
import bigframes.dataframe
import bigframes.dtypes
import bigframes.formatting_helpers as formatter
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.operations.base
import bigframes.operations.datetimes as dt
import bigframes.operations.strings as strings
import third_party.bigframes_vendored.pandas.core.series as vendored_pandas_series

LevelType = typing.Union[str, int]
LevelsType = typing.Union[LevelType, typing.Sequence[LevelType]]


class Series(bigframes.operations.base.SeriesMethods, vendored_pandas_series.Series):
    def __init__(self, *args, **kwargs):
        self._query_job: Optional[bigquery.QueryJob] = None
        super().__init__(*args, **kwargs)

    @property
    def dt(self) -> dt.DatetimeMethods:
        return dt.DatetimeMethods(self._block)

    @property
    def dtype(self):
        return self._dtype

    @property
    def dtypes(self):
        return self._dtype

    @property
    def index(self) -> indexes.Index:
        return indexes.Index(self)

    @property
    def loc(self) -> bigframes.core.indexers.LocSeriesIndexer:
        return bigframes.core.indexers.LocSeriesIndexer(self)

    @property
    def iloc(self) -> bigframes.core.indexers.IlocSeriesIndexer:
        return bigframes.core.indexers.IlocSeriesIndexer(self)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def shape(self) -> typing.Tuple[int]:
        return (self._block.shape[0],)

    @property
    def size(self) -> int:
        return self.shape[0]

    @property
    def empty(self) -> bool:
        return self.shape[0] == 0

    @property
    def values(self) -> numpy.ndarray:
        return self.to_numpy()

    @property
    def query_job(self) -> Optional[bigquery.QueryJob]:
        """BigQuery job metadata for the most recent query.

        Returns:
            The most recent `QueryJob
            <https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob>`_.
        """
        if self._query_job is None:
            self._set_internal_query_job(self._compute_dry_run())
        return self._query_job

    def _set_internal_query_job(self, query_job: bigquery.QueryJob):
        self._query_job = query_job

    def __len__(self):
        return self.shape[0]

    def copy(self) -> Series:
        return Series(self._block)

    def rename(
        self, index: Union[blocks.Label, Mapping[Any, Any]] = None, **kwargs
    ) -> Series:
        if len(kwargs) != 0:
            raise NotImplementedError(
                f"rename does not currently support any keyword arguments. {constants.FEEDBACK_LINK}"
            )

        # rename the Series name
        if index is None or isinstance(
            index, str
        ):  # Python 3.9 doesn't allow isinstance of Optional
            index = typing.cast(Optional[str], index)
            block = self._block.with_column_labels([index])
            return Series(block)

        # rename the index
        if isinstance(index, Mapping):
            index = typing.cast(Mapping[Any, Any], index)
            block = self._block
            for k, v in index.items():
                new_idx_ids = []
                for idx_id, idx_dtype in zip(block.index_columns, block.index_dtypes):
                    # Will throw if key type isn't compatible with index type, which leads to invalid SQL.
                    block.create_constant(k, dtype=idx_dtype)

                    # Will throw if value type isn't compatible with index type.
                    block, const_id = block.create_constant(v, dtype=idx_dtype)
                    block, cond_id = block.apply_unary_op(
                        idx_id, ops.BinopPartialRight(ops.ne_op, k)
                    )
                    block, new_idx_id = block.apply_ternary_op(
                        idx_id, cond_id, const_id, ops.where_op
                    )

                    new_idx_ids.append(new_idx_id)
                    block = block.drop_columns([const_id, cond_id])

                block = block.set_index(new_idx_ids, index_labels=block.index_labels)

            return Series(block)

        raise ValueError(f"Unsupported type of parameter index: {type(index)}")

    def rename_axis(
        self,
        mapper: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        **kwargs,
    ) -> Series:
        if len(kwargs) != 0:
            raise NotImplementedError(
                f"rename_axis does not currently support any keyword arguments. {constants.FEEDBACK_LINK}"
            )
        # limited implementation: the new index name is simply the 'mapper' parameter
        if _is_list_like(mapper):
            labels = mapper
        else:
            labels = [mapper]
        return Series(self._block.with_index_labels(labels))

    def reset_index(
        self,
        *,
        name: typing.Optional[str] = None,
        drop: bool = False,
    ) -> bigframes.dataframe.DataFrame | Series:
        block = self._block.reset_index(drop)
        if drop:
            return Series(block)
        else:
            if name:
                block = block.assign_label(self._value_column, name)
            return bigframes.dataframe.DataFrame(block)

    def __repr__(self) -> str:
        # TODO(swast): Add a timeout here? If the query is taking a long time,
        # maybe we just print the job metadata that we have so far?
        # TODO(swast): Avoid downloading the whole series by using job
        # metadata, like we do with DataFrame.
        opts = bigframes.options.display
        max_results = opts.max_rows
        if opts.repr_mode == "deferred":
            return formatter.repr_query_job(self.query_job)

        pandas_df, _, query_job = self._block.retrieve_repr_request_results(max_results)
        self._set_internal_query_job(query_job)

        return repr(pandas_df.iloc[:, 0])

    def _to_ibis_expr(self):
        """Creates an Ibis table expression representing the Series."""
        expr = self._block.expr.projection([self._value])
        ibis_expr = expr.to_ibis_expr()[self._value_column]
        if self._name:
            return ibis_expr.name(self._name)
        return ibis_expr

    def astype(
        self,
        dtype: Union[bigframes.dtypes.DtypeString, bigframes.dtypes.Dtype],
    ) -> Series:
        return self._apply_unary_op(bigframes.operations.AsTypeOp(dtype))

    def to_pandas(
        self,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
    ) -> pandas.Series:
        """Writes Series to pandas Series.

        Args:
            max_download_size (int, default None):
                Download size threshold in MB. If max_download_size is exceeded when downloading data
                (e.g., to_pandas()), the data will be downsampled if
                bigframes.options.sampling.enable_downsampling is True, otherwise, an error will be
                raised. If set to a value other than None, this will supersede the global config.
            sampling_method (str, default None):
                Downsampling algorithms to be chosen from, the choices are: "head": This algorithm
                returns a portion of the data from the beginning. It is fast and requires minimal
                computations to perform the downsampling; "uniform": This algorithm returns uniform
                random samples of the data. If set to a value other than None, this will supersede
                the global config.
            random_state (int, default None):
                The seed for the uniform downsampling algorithm. If provided, the uniform method may
                take longer to execute and require more computation. If set to a value other than
                None, this will supersede the global config.

        Returns:
            pandas.Series: A pandas Series with all rows of this Series if the data_sampling_threshold_mb
                is not exceeded; otherwise, a pandas Series with downsampled rows of the DataFrame.
        """
        df, query_job = self._block.to_pandas(
            (self._value_column,),
            max_download_size=max_download_size,
            sampling_method=sampling_method,
            random_state=random_state,
        )
        self._set_internal_query_job(query_job)
        series = df[self._value_column]
        series.name = self._name
        return series

    def _compute_dry_run(self) -> bigquery.QueryJob:
        return self._block._compute_dry_run((self._value_column,))

    def drop(
        self,
        labels: typing.Any = None,
        *,
        axis: typing.Union[int, str] = 0,
        index: typing.Any = None,
        columns: Union[blocks.Label, typing.Iterable[blocks.Label]] = None,
        level: typing.Optional[LevelType] = None,
    ) -> Series:
        if labels and index:
            raise ValueError("Must specify exacly one of 'labels' or 'index'")
        index = labels or index

        # ignore axis, columns params
        block = self._block
        level_id = self._resolve_levels(level or 0)[0]
        if _is_list_like(labels):
            block, inverse_condition_id = block.apply_unary_op(
                level_id, ops.IsInOp(index, match_nulls=True)
            )
            block, condition_id = block.apply_unary_op(
                inverse_condition_id, ops.invert_op
            )
        else:
            block, condition_id = block.apply_unary_op(
                level_id, ops.partial_right(ops.ne_op, labels)
            )
        block = block.filter(condition_id, keep_null=True)
        block = block.drop_columns([condition_id])
        return Series(block.select_column(self._value_column))

    def droplevel(self, level: LevelsType):
        resolved_level_ids = self._resolve_levels(level)
        return Series(self._block.drop_levels(resolved_level_ids))

    def reorder_levels(self, order: LevelsType):
        resolved_level_ids = self._resolve_levels(order)
        return Series(self._block.reorder_levels(resolved_level_ids))

    def _resolve_levels(self, level: LevelsType) -> typing.Sequence[str]:
        if _is_list_like(level):
            levels = list(level)
        else:
            levels = [level]
        resolved_level_ids = []
        for level_ref in levels:
            if isinstance(level_ref, int):
                resolved_level_ids.append(self._block.index_columns[level_ref])
            elif isinstance(level_ref, str):
                matching_ids = self._block.index_name_to_col_id.get(level_ref, [])
                if len(matching_ids) != 1:
                    raise ValueError("level name cannot be found or is ambiguous")
                resolved_level_ids.append(matching_ids[0])
            else:
                raise ValueError(f"Unexpected level: {level_ref}")
        return resolved_level_ids

    def between(self, left, right, inclusive="both"):
        if inclusive not in ["both", "neither", "left", "right"]:
            raise ValueError(
                "Must set 'inclusive' to one of 'both', 'neither', 'left', or 'right'"
            )
        left_op = ops.ge_op if (inclusive in ["left", "both"]) else ops.gt_op
        right_op = ops.le_op if (inclusive in ["right", "both"]) else ops.lt_op
        return self._apply_binary_op(left, left_op).__and__(
            self._apply_binary_op(right, right_op)
        )

    def cumsum(self) -> Series:
        return self._apply_window_op(
            agg_ops.sum_op, bigframes.core.WindowSpec(following=0)
        )

    def cummax(self) -> Series:
        return self._apply_window_op(
            agg_ops.max_op, bigframes.core.WindowSpec(following=0)
        )

    def cummin(self) -> Series:
        return self._apply_window_op(
            agg_ops.min_op, bigframes.core.WindowSpec(following=0)
        )

    def cumprod(self) -> Series:
        return self._apply_window_op(
            agg_ops.product_op, bigframes.core.WindowSpec(following=0)
        )

    def shift(self, periods: int = 1) -> Series:
        window = bigframes.core.WindowSpec(
            preceding=periods if periods > 0 else None,
            following=-periods if periods < 0 else None,
        )
        return self._apply_window_op(agg_ops.ShiftOp(periods), window)

    def diff(self, periods: int = 1) -> Series:
        return self - self.shift(periods=periods)

    def rank(
        self,
        axis=0,
        method: str = "average",
        numeric_only=False,
        na_option: str = "keep",
        ascending: bool = True,
    ) -> Series:
        return Series(block_ops.rank(self._block, method, na_option, ascending))

    def fillna(self, value=None) -> "Series" | None:
        return self._apply_binary_op(value, ops.fillna_op)

    def head(self, n: int = 5) -> Series:
        return typing.cast(Series, self.iloc[0:n])

    def tail(self, n: int = 5) -> Series:
        return typing.cast(Series, self.iloc[-n:])

    def nlargest(self, n: int = 5, keep: str = "first") -> Series:
        if keep not in ("first", "last", "all"):
            raise ValueError("'keep must be one of 'first', 'last', or 'all'")
        block = self._block
        if keep == "last":
            block = block.reversed()
        ordering = (
            OrderingColumnReference(
                self._value_column, direction=OrderingDirection.DESC
            ),
        )
        block = block.order_by(ordering, stable=True)
        if keep in ("first", "last"):
            return Series(block.slice(0, n))
        else:  # keep == "all":
            block, counter = block.apply_window_op(
                self._value_column,
                agg_ops.rank_op,
                window_spec=WindowSpec(ordering=ordering),
            )
            block, condition = block.apply_unary_op(
                counter, ops.partial_right(ops.le_op, n)
            )
            block = block.filter(condition)
            block = block.select_column(self._value_column)
            return Series(block)

    def nsmallest(self, n: int = 5, keep: str = "first") -> Series:
        if keep not in ("first", "last", "all"):
            raise ValueError("'keep must be one of 'first', 'last', or 'all'")
        block = self._block
        if keep == "last":
            block = block.reversed()
        ordering = (OrderingColumnReference(self._value_column),)
        block = block.order_by(ordering, stable=True)
        if keep in ("first", "last"):
            return Series(block.slice(0, n))
        else:  # keep == "all":
            block, counter = block.apply_window_op(
                self._value_column,
                agg_ops.rank_op,
                window_spec=WindowSpec(ordering=ordering),
            )
            block, condition = block.apply_unary_op(
                counter, ops.partial_right(ops.le_op, n)
            )
            block = block.filter(condition)
            block = block.select_column(self._value_column)
            return Series(block)

    def isna(self) -> "Series":
        return self._apply_unary_op(ops.isnull_op)

    isnull = isna

    def notna(self) -> "Series":
        return self._apply_unary_op(ops.notnull_op)

    notnull = notna

    def __and__(self, other: bool | int | Series) -> Series:
        return self._apply_binary_op(other, ops.and_op)

    __rand__ = __and__

    def __or__(self, other: bool | int | Series) -> Series:
        return self._apply_binary_op(other, ops.or_op)

    __ror__ = __or__

    def __add__(self, other: float | int | Series) -> Series:
        return self.add(other)

    def __radd__(self, other: float | int | Series) -> Series:
        return self.radd(other)

    def add(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.add_op)

    def radd(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.reverse(ops.add_op))

    def __sub__(self, other: float | int | Series) -> Series:
        return self.sub(other)

    def __rsub__(self, other: float | int | Series) -> Series:
        return self.rsub(other)

    def sub(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.sub_op)

    def rsub(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.reverse(ops.sub_op))

    subtract = sub

    def __mul__(self, other: float | int | Series) -> Series:
        return self.mul(other)

    def __rmul__(self, other: float | int | Series) -> Series:
        return self.rmul(other)

    def mul(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.mul_op)

    def rmul(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.reverse(ops.mul_op))

    multiply = mul

    def __truediv__(self, other: float | int | Series) -> Series:
        return self.truediv(other)

    def __rtruediv__(self, other: float | int | Series) -> Series:
        return self.rtruediv(other)

    def truediv(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.div_op)

    def rtruediv(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.reverse(ops.div_op))

    div = truediv

    divide = truediv

    rdiv = rtruediv

    def __floordiv__(self, other: float | int | Series) -> Series:
        return self.floordiv(other)

    def __rfloordiv__(self, other: float | int | Series) -> Series:
        return self.rfloordiv(other)

    def floordiv(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.floordiv_op)

    def rfloordiv(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.reverse(ops.floordiv_op))

    def __lt__(self, other: float | int | Series) -> Series:  # type: ignore
        return self.lt(other)

    def __le__(self, other: float | int | Series) -> Series:  # type: ignore
        return self.le(other)

    def lt(self, other) -> Series:
        return self._apply_binary_op(other, ops.lt_op)

    def le(self, other) -> Series:
        return self._apply_binary_op(other, ops.le_op)

    def __gt__(self, other: float | int | Series) -> Series:  # type: ignore
        return self.gt(other)

    def __ge__(self, other: float | int | Series) -> Series:  # type: ignore
        return self.ge(other)

    def gt(self, other) -> Series:
        return self._apply_binary_op(other, ops.gt_op)

    def ge(self, other) -> Series:
        return self._apply_binary_op(other, ops.ge_op)

    def __mod__(self, other) -> Series:  # type: ignore
        return self.mod(other)

    def __rmod__(self, other) -> Series:  # type: ignore
        return self.rmod(other)

    def mod(self, other) -> Series:  # type: ignore
        return self._apply_binary_op(other, ops.mod_op)

    def rmod(self, other) -> Series:  # type: ignore
        return self._apply_binary_op(other, ops.reverse(ops.mod_op))

    def divmod(self, other) -> Tuple[Series, Series]:  # type: ignore
        # TODO(huanc): when self and other both has dtype int and other contains zeros,
        # the output should be dtype float, both floordiv and mod returns dtype int in this case.
        return (self.floordiv(other), self.mod(other))

    def rdivmod(self, other) -> Tuple[Series, Series]:  # type: ignore
        # TODO(huanc): when self and other both has dtype int and self contains zeros,
        # the output should be dtype float, both floordiv and mod returns dtype int in this case.
        return (self.rfloordiv(other), self.rmod(other))

    def __matmul__(self, other):
        return (self * other).sum()

    dot = __matmul__

    def abs(self) -> Series:
        return self._apply_unary_op(ops.abs_op)

    def round(self, decimals=0) -> "Series":
        def round_op(x: ibis_types.Value, y: ibis_types.Value):
            return typing.cast(ibis_types.NumericValue, x).round(
                digits=typing.cast(ibis_types.IntegerValue, y)
            )

        return self._apply_binary_op(decimals, round_op)

    def all(self) -> bool:
        return typing.cast(bool, self._apply_aggregation(agg_ops.all_op))

    def any(self) -> bool:
        return typing.cast(bool, self._apply_aggregation(agg_ops.any_op))

    def count(self) -> int:
        return typing.cast(int, self._apply_aggregation(agg_ops.count_op))

    def nunique(self) -> int:
        return typing.cast(int, self._apply_aggregation(agg_ops.nunique_op))

    def max(self) -> scalars.Scalar:
        return self._apply_aggregation(agg_ops.max_op)

    def min(self) -> scalars.Scalar:
        return self._apply_aggregation(agg_ops.min_op)

    def std(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.std_op))

    def var(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.var_op))

    def _central_moment(self, n: int) -> float:
        """Useful helper for calculating central moment statistics"""
        # Nth central moment is mean((x-mean(x))^n)
        # See: https://en.wikipedia.org/wiki/Moment_(mathematics)
        mean = self.mean()
        mean_deltas = self - mean
        delta_power = mean_deltas
        # TODO(tbergeron): Replace with pow once implemented
        for i in range(1, n):
            delta_power = delta_power * mean_deltas
        return delta_power.mean()

    def agg(self, func: str | typing.Sequence[str]) -> scalars.Scalar | Series:
        if _is_list_like(func):
            if self.dtype not in bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES:
                raise NotImplementedError(
                    f"Multiple aggregations only supported on numeric series. {constants.FEEDBACK_LINK}"
                )
            aggregations = [agg_ops.AGGREGATIONS_LOOKUP[f] for f in func]
            return Series(
                self._block.summarize(
                    [self._value_column],
                    aggregations,
                )
            )
        else:

            return self._apply_aggregation(
                agg_ops.AGGREGATIONS_LOOKUP[typing.cast(str, func)]
            )

    def skew(self):
        count = self.count()
        if count < 3:
            return pandas.NA

        moment3 = self._central_moment(3)
        moment2 = self.var() * (count - 1) / count  # Convert sample var to pop var

        # See G1 estimator:
        # https://en.wikipedia.org/wiki/Skewness#Sample_skewness
        numerator = moment3
        denominator = moment2 ** (3 / 2)
        adjustment = (count * (count - 1)) ** 0.5 / (count - 2)

        return (numerator / denominator) * adjustment

    def kurt(self):
        count = self.count()
        if count < 4:
            return pandas.NA

        moment4 = self._central_moment(4)
        moment2 = self.var() * (count - 1) / count  # Convert sample var to pop var

        # Kurtosis is often defined as the second standardize moment: moment(4)/moment(2)**2
        # Pandas however uses Fisher’s estimator, implemented below
        numerator = (count + 1) * (count - 1) * moment4
        denominator = (count - 2) * (count - 3) * moment2**2
        adjustment = 3 * (count - 1) ** 2 / ((count - 2) * (count - 3))

        return (numerator / denominator) - adjustment

    kurtosis = kurt

    def mode(self) -> Series:
        block = self._block
        # Approach: Count each value, return each value for which count(x) == max(counts))
        block, agg_ids = block.aggregate(
            by_column_ids=[self._value_column],
            aggregations=((self._value_column, agg_ops.count_op),),
            as_index=False,
        )
        value_count_col_id = agg_ids[0]
        block, max_value_count_col_id = block.apply_window_op(
            value_count_col_id,
            agg_ops.max_op,
            window_spec=WindowSpec(),
        )
        block, is_mode_col_id = block.apply_binary_op(
            value_count_col_id,
            max_value_count_col_id,
            ops.eq_op,
        )
        block = block.filter(is_mode_col_id)
        mode_values_series = Series(
            block.select_column(self._value_column).assign_label(
                self._value_column, self.name
            )
        )
        return typing.cast(
            Series, mode_values_series.sort_values().reset_index(drop=True)
        )

    def mean(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.mean_op))

    def median(self, *, exact: bool = False) -> float:
        if exact:
            raise NotImplementedError(
                f"Only approximate median is supported. {constants.FEEDBACK_LINK}"
            )
        return typing.cast(float, self._apply_aggregation(agg_ops.median_op))

    def sum(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.sum_op))

    def prod(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.product_op))

    product = prod

    def __eq__(self, other: object) -> Series:  # type: ignore
        return self.eq(other)

    def __ne__(self, other: object) -> Series:  # type: ignore
        return self.ne(other)

    def __invert__(self) -> Series:
        return self._apply_unary_op(ops.invert_op)

    def eq(self, other: object) -> Series:
        # TODO: enforce stricter alignment
        return self._apply_binary_op(other, ops.eq_op)

    def ne(self, other: object) -> Series:
        # TODO: enforce stricter alignment
        return self._apply_binary_op(other, ops.ne_op)

    def where(self, cond, other=None):
        value_id, cond_id, other_id, block = self._align3(cond, other)
        block, result_id = block.apply_ternary_op(
            value_id, cond_id, other_id, ops.where_op
        )
        return Series(block.select_column(result_id).with_column_labels([self.name]))

    def clip(self, lower, upper):
        if lower is None and upper is None:
            return self
        if lower is None:
            return self._apply_binary_op(upper, ops.clip_upper, alignment="left")
        if upper is None:
            return self._apply_binary_op(lower, ops.clip_lower, alignment="left")
        value_id, lower_id, upper_id, block = self._align3(lower, upper)
        block, result_id = block.apply_ternary_op(
            value_id, lower_id, upper_id, ops.clip_op
        )
        return Series(block.select_column(result_id).with_column_labels([self.name]))

    def argmax(self) -> scalars.Scalar:
        block, row_nums = self._block.promote_offsets()
        block = block.order_by(
            [
                OrderingColumnReference(
                    self._value_column, direction=OrderingDirection.DESC
                ),
                OrderingColumnReference(row_nums),
            ]
        )
        return typing.cast(
            scalars.Scalar, Series(block.select_column(row_nums)).iloc[0]
        )

    def argmin(self) -> scalars.Scalar:
        block, row_nums = self._block.promote_offsets()
        block = block.order_by(
            [
                OrderingColumnReference(self._value_column),
                OrderingColumnReference(row_nums),
            ]
        )
        return typing.cast(
            scalars.Scalar, Series(block.select_column(row_nums)).iloc[0]
        )

    def __getitem__(self, indexer):
        # TODO: enforce stricter alignment, should fail if indexer is missing any keys.
        use_iloc = (
            isinstance(indexer, slice)
            and all(
                isinstance(x, numbers.Integral) or (x is None)
                for x in [indexer.start, indexer.stop, indexer.step]
            )
        ) or (
            isinstance(indexer, numbers.Integral)
            and not isinstance(self._block.index.dtypes[0], pandas.Int64Dtype)
        )
        if use_iloc:
            return self.iloc[indexer]
        if isinstance(indexer, Series):
            (left, right, block) = self._align(indexer, "left")
            block = block.filter(right)
            block = block.select_column(left)
            return Series(block)
        return self.loc[indexer]

    def __getattr__(self, key: str):
        if hasattr(pandas.Series, key):
            raise NotImplementedError(
                textwrap.dedent(
                    f"""
                    BigQuery DataFrames has not yet implemented an equivalent to
                    'pandas.Series.{key}'. {constants.FEEDBACK_LINK}
                    """
                )
            )
        else:
            raise AttributeError(key)

    def _align3(self, other1: Series | scalars.Scalar, other2: Series | scalars.Scalar, how="left") -> tuple[str, str, str, blocks.Block]:  # type: ignore
        """Aligns the series value with 2 other scalars or series objects. Returns new values and joined tabled expression."""
        values, index = self._align_n([other1, other2], how)
        return (values[0], values[1], values[2], index)

    def _apply_aggregation(self, op: agg_ops.AggregateOp) -> Any:
        return self._block.get_stat(self._value_column, op)

    def _apply_window_op(
        self,
        op: agg_ops.WindowOp,
        window_spec: bigframes.core.WindowSpec,
    ):
        block = self._block
        block, result_id = block.apply_window_op(
            self._value_column, op, window_spec=window_spec, result_label=self.name
        )
        return Series(block.select_column(result_id))

    def value_counts(
        self,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        *,
        dropna: bool = True,
    ):
        block = block_ops.value_counts(
            self._block,
            [self._value_column],
            normalize=normalize,
            ascending=ascending,
            dropna=dropna,
        )
        return Series(block)

    def sort_values(
        self, *, axis=0, ascending=True, kind: str = "quicksort", na_position="last"
    ) -> Series:
        if na_position not in ["first", "last"]:
            raise ValueError("Param na_position must be one of 'first' or 'last'")
        direction = OrderingDirection.ASC if ascending else OrderingDirection.DESC
        block = self._block.order_by(
            [
                OrderingColumnReference(
                    self._value_column,
                    direction=direction,
                    na_last=(na_position == "last"),
                )
            ],
            stable=kind in STABLE_SORTS,
        )
        return Series(block)

    def sort_index(self, *, axis=0, ascending=True, na_position="last") -> Series:
        # TODO(tbergeron): Support level parameter once multi-index introduced.
        if na_position not in ["first", "last"]:
            raise ValueError("Param na_position must be one of 'first' or 'last'")
        block = self._block
        direction = OrderingDirection.ASC if ascending else OrderingDirection.DESC
        na_last = na_position == "last"
        ordering = [
            OrderingColumnReference(column, direction=direction, na_last=na_last)
            for column in block.index_columns
        ]
        block = block.order_by(ordering)
        return Series(block)

    def rolling(self, window: int, min_periods=None) -> bigframes.core.window.Window:
        # To get n size window, need current row and n-1 preceding rows.
        window_spec = WindowSpec(
            preceding=window - 1, following=0, min_periods=min_periods or window
        )
        return bigframes.core.window.Window(
            self._block, window_spec, self._value_column
        )

    def expanding(self, min_periods: int = 1) -> bigframes.core.window.Window:
        window_spec = WindowSpec(following=0, min_periods=min_periods)
        return bigframes.core.window.Window(
            self._block, window_spec, self._value_column
        )

    def groupby(
        self,
        by: typing.Union[
            blocks.Label, Series, typing.Sequence[typing.Union[blocks.Label, Series]]
        ] = None,
        axis=0,
        level: typing.Optional[
            int | str | typing.Sequence[int] | typing.Sequence[str]
        ] = None,
        as_index: bool = True,
        *,
        dropna: bool = True,
    ) -> bigframes.core.groupby.SeriesGroupBy:
        if (by is not None) and (level is not None):
            raise ValueError("Do not specify both 'by' and 'level'")
        if not as_index:
            raise ValueError("as_index=False only valid with DataFrame")
        if axis:
            raise ValueError("No axis named {} for object type Series".format(level))
        if not as_index:
            raise ValueError("'as_index'=False only applies to DataFrame")
        if by is not None:
            return self._groupby_values(by, dropna)
        if level is not None:
            return self._groupby_level(level, dropna)
        else:
            raise TypeError("You have to supply one of 'by' and 'level'")

    def _groupby_level(
        self,
        level: int | str | typing.Sequence[int] | typing.Sequence[str],
        dropna: bool = True,
    ) -> bigframes.core.groupby.SeriesGroupBy:
        return groupby.SeriesGroupBy(
            self._block,
            self._value_column,
            by_col_ids=self._resolve_levels(level),
            value_name=self.name,
            dropna=dropna,
        )

    def _groupby_values(
        self,
        by: typing.Union[
            blocks.Label, Series, typing.Sequence[typing.Union[blocks.Label, Series]]
        ],
        dropna: bool = True,
    ) -> bigframes.core.groupby.SeriesGroupBy:
        if not isinstance(by, Series) and _is_list_like(by):
            by = list(by)
        else:
            by = [typing.cast(typing.Union[blocks.Label, Series], by)]

        block = self._block
        grouping_cols: typing.Sequence[str] = []
        value_col = self._value_column
        for key in by:
            if isinstance(key, Series):
                combined_index, (
                    get_column_left,
                    get_column_right,
                ) = block.index.join(
                    key._block.index, how="inner" if dropna else "left"
                )

                value_col = get_column_left(self._value_column)
                grouping_cols = [
                    *[get_column_left(value) for value in grouping_cols],
                    get_column_right(key._value_column),
                ]
                block = combined_index._block
            else:
                # Interpret as index level
                matches = block.index_name_to_col_id.get(key, [])
                if len(matches) != 1:
                    raise ValueError(
                        f"GroupBy key {key} does not match a unique index level. BigQuery DataFrames only interprets lists of strings as index level names, not directly as per-row group assignments."
                    )
                grouping_cols = [*grouping_cols, matches[0]]

        return groupby.SeriesGroupBy(
            block,
            value_col,
            by_col_ids=grouping_cols,
            value_name=self.name,
            dropna=dropna,
        )

    def apply(self, func) -> Series:
        # TODO(shobs, b/274645634): Support convert_dtype, args, **kwargs
        # is actually a ternary op
        return self._apply_unary_op(ops.RemoteFunctionOp(func))

    def add_prefix(self, prefix: str, axis: int | str | None = None) -> Series:
        return Series(self._get_block().add_prefix(prefix))

    def add_suffix(self, suffix: str, axis: int | str | None = None) -> Series:
        return Series(self._get_block().add_suffix(suffix))

    def drop_duplicates(self, *, keep: str = "first") -> Series:
        block = block_ops.drop_duplicates(self._block, (self._value_column,), keep)
        return Series(block)

    def unique(self) -> Series:
        return self.drop_duplicates()

    def duplicated(self, keep: str = "first") -> Series:
        block, indicator = block_ops.indicate_duplicates(
            self._block, (self._value_column,), keep
        )
        return Series(
            block.select_column(
                indicator,
            ).with_column_labels([self.name])
        )

    def mask(self, cond, other=None) -> Series:
        if callable(cond):
            cond = self.apply(cond)

        if not isinstance(cond, Series):
            raise TypeError(
                f"Only bigframes series condition is supported, received {type(cond).__name__}. "
                f"{constants.FEEDBACK_LINK}"
            )
        return self.where(~cond, other)

    def to_frame(self) -> bigframes.dataframe.DataFrame:
        # To be consistent with Pandas, it assigns 0 as the column name if missing. 0 is the first element of RangeIndex.
        block = self._block.with_column_labels([self.name] if self.name else ["0"])
        return bigframes.dataframe.DataFrame(block)

    def to_csv(self, path_or_buf=None, **kwargs) -> typing.Optional[str]:
        # TODO(b/280651142): Implement version that leverages bq export native csv support to bypass local pandas step.
        return self.to_pandas().to_csv(path_or_buf, **kwargs)

    def to_dict(self, into: type[dict] = dict) -> typing.Mapping:
        return typing.cast(dict, self.to_pandas().to_dict(into))

    def to_excel(self, excel_writer, sheet_name="Sheet1", **kwargs) -> None:
        return self.to_pandas().to_excel(excel_writer, sheet_name, **kwargs)

    def to_json(
        self,
        path_or_buf=None,
        orient: typing.Literal[
            "split", "records", "index", "columns", "values", "table"
        ] = "columns",
        **kwargs,
    ) -> typing.Optional[str]:
        # TODO(b/280651142): Implement version that leverages bq export native csv support to bypass local pandas step.
        return self.to_pandas().to_json(path_or_buf, **kwargs)

    def to_latex(
        self, buf=None, columns=None, header=True, index=True, **kwargs
    ) -> typing.Optional[str]:
        return self.to_pandas().to_latex(
            buf, columns=columns, header=header, index=index, **kwargs
        )

    def tolist(self) -> list:
        return self.to_pandas().to_list()

    to_list = tolist

    def to_markdown(
        self,
        buf: typing.IO[str] | None = None,
        mode: str = "wt",
        index: bool = True,
        **kwargs,
    ) -> typing.Optional[str]:
        return self.to_pandas().to_markdown(buf, mode=mode, index=index, **kwargs)  # type: ignore

    def to_numpy(
        self, dtype=None, copy=False, na_value=None, **kwargs
    ) -> numpy.ndarray:
        return self.to_pandas().to_numpy(dtype, copy, na_value, **kwargs)

    __array__ = to_numpy

    def to_pickle(self, path, **kwargs) -> None:
        return self.to_pandas().to_pickle(path, **kwargs)

    def to_string(
        self,
        buf=None,
        na_rep="NaN",
        float_format=None,
        header=True,
        index=True,
        length=False,
        dtype=False,
        name=False,
        max_rows=None,
        min_rows=None,
    ) -> typing.Optional[str]:
        return self.to_pandas().to_string(
            buf,
            na_rep,
            float_format,
            header,
            index,
            length,
            dtype,
            name,
            max_rows,
            min_rows,
        )

    def to_xarray(self):
        return self.to_pandas().to_xarray()

    # Keep this at the bottom of the Series class to avoid
    # confusing type checker by overriding str
    @property
    def str(self) -> strings.StringMethods:
        return strings.StringMethods(self._block)

    def _slice(
        self,
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None,
        step: typing.Optional[int] = None,
    ) -> bigframes.series.Series:
        return bigframes.series.Series(
            self._block.slice(start=start, stop=stop, step=step).select_column(
                self._value_column
            ),
        )


def _is_list_like(obj: typing.Any) -> typing_extensions.TypeGuard[typing.Sequence]:
    return pandas.api.types.is_list_like(obj)
