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

"""An index based on a single column."""

from __future__ import annotations

import typing
from typing import Hashable, Optional, Sequence, Union

import bigframes_vendored.pandas.core.indexes.base as vendored_pandas_index
import google.cloud.bigquery as bigquery
import numpy as np
import pandas

import bigframes.constants as constants
import bigframes.core.block_transforms as block_ops
import bigframes.core.blocks as blocks
import bigframes.core.expression as ex
import bigframes.core.ordering as order
import bigframes.core.utils as utils
import bigframes.dtypes
import bigframes.formatting_helpers as formatter
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops

if typing.TYPE_CHECKING:
    import bigframes.dataframe
    import bigframes.series


class Index(vendored_pandas_index.Index):
    __doc__ = vendored_pandas_index.Index.__doc__

    def __init__(
        self,
        data=None,
        dtype=None,
        *,
        name=None,
        session=None,
    ):
        import bigframes.dataframe as df
        import bigframes.series as series

        if isinstance(data, blocks.Block):
            block = data.select_columns([])
        elif isinstance(data, df.DataFrame):
            raise ValueError("Cannot construct index from dataframe.")
        elif isinstance(data, series.Series) or isinstance(data, Index):
            if isinstance(data, series.Series):
                block = data._block
                block = block.set_index(
                    col_ids=[data._value_column],
                )
            elif isinstance(data, Index):
                block = data._block
            index = Index(data=block)
            name = data.name if name is None else name
            if name is not None:
                index.name = name
            if dtype is not None:
                index = index.astype(dtype)
            block = index._block
        else:
            pd_index = pandas.Index(data=data, dtype=dtype, name=name)
            pd_df = pandas.DataFrame(index=pd_index)
            block = df.DataFrame(pd_df, session=session)._block
        self._query_job = None
        self._block: blocks.Block = block

    @classmethod
    def from_frame(
        cls, frame: Union[bigframes.series.Series, bigframes.dataframe.DataFrame]
    ) -> Index:
        return FrameIndex(frame)

    @property
    def name(self) -> blocks.Label:
        names = self.names
        if len(names) == 1:
            return self.names[0]
        else:
            # pandas returns None for MultiIndex.name.
            return None

    @name.setter
    def name(self, value: blocks.Label):
        self.names = [value]

    @property
    def names(self) -> typing.Sequence[blocks.Label]:
        """Returns the names of the Index."""
        return self._block._index_labels

    @names.setter
    def names(self, values: typing.Sequence[blocks.Label]):
        new_block = self._block.with_index_labels(values)
        self._block = new_block

    @property
    def nlevels(self) -> int:
        return len(self._block.index_columns)

    @property
    def values(self) -> np.ndarray:
        return self.to_numpy()

    @property
    def ndim(self) -> int:
        return 1

    @property
    def shape(self) -> typing.Tuple[int]:
        return (self._block.shape[0],)

    @property
    def dtype(self):
        return self._block.index.dtypes[0] if self.nlevels == 1 else np.dtype("O")

    @property
    def dtypes(self) -> pandas.Series:
        return pandas.Series(
            data=self._block.index.dtypes, index=self._block.index.names  # type:ignore
        )

    @property
    def size(self) -> int:
        """Returns the size of the Index."""
        return self.shape[0]

    @property
    def empty(self) -> bool:
        """Returns True if the Index is empty, otherwise returns False."""
        return self.shape[0] == 0

    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return a boolean if the values are equal or increasing.

        Returns:
            bool
        """
        return typing.cast(
            bool,
            self._block.is_monotonic_increasing(self._block.index_columns),
        )

    @property
    def is_monotonic_decreasing(self) -> bool:
        """
        Return a boolean if the values are equal or decreasing.

        Returns:
            bool
        """
        return typing.cast(
            bool,
            self._block.is_monotonic_decreasing(self._block.index_columns),
        )

    @property
    def is_unique(self) -> bool:
        # TODO: Cache this at block level
        # Avoid circular imports
        return not self.has_duplicates

    @property
    def has_duplicates(self) -> bool:
        # TODO: Cache this at block level
        # Avoid circular imports
        import bigframes.core.block_transforms as block_ops
        import bigframes.dataframe as df

        duplicates_block, indicator = block_ops.indicate_duplicates(
            self._block, self._block.index_columns
        )
        duplicates_block = duplicates_block.select_columns(
            [indicator]
        ).with_column_labels(["is_duplicate"])
        duplicates_df = df.DataFrame(duplicates_block)
        return duplicates_df["is_duplicate"].any()

    @property
    def T(self) -> Index:
        return self.transpose()

    @property
    def query_job(self) -> Optional[bigquery.QueryJob]:
        """BigQuery job metadata for the most recent query.

        Returns:
            The most recent `QueryJob
            <https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob>`_.
        """
        if self._query_job is None:
            self._query_job = self._block._compute_dry_run()
        return self._query_job

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
        self._query_job = query_job
        return repr(pandas_df.index)

    def copy(self, name: Optional[Hashable] = None):
        copy_index = Index(self._block)
        if name is not None:
            copy_index.name = name
        return copy_index

    def to_series(
        self, index: Optional[Index] = None, name: Optional[Hashable] = None
    ) -> bigframes.series.Series:
        if self.nlevels != 1:
            NotImplementedError(
                f"Converting multi-index to series is not yet supported. {constants.FEEDBACK_LINK}"
            )

        import bigframes.series

        name = self.name if name is None else name
        if index is None:
            return bigframes.series.Series(data=self, index=self, name=name)
        else:
            return bigframes.series.Series(data=self, index=Index(index), name=name)

    def get_level_values(self, level) -> Index:
        level_n = level if isinstance(level, int) else self.names.index(level)
        block = self._block.drop_levels(
            [self._block.index_columns[i] for i in range(self.nlevels) if i != level_n]
        )
        return Index(block)

    def _memory_usage(self) -> int:
        (n_rows,) = self.shape
        return sum(
            self.dtypes.map(
                lambda dtype: bigframes.dtypes.DTYPE_BYTE_SIZES.get(dtype, 8) * n_rows
            )
        )

    def transpose(self) -> Index:
        return self

    def sort_values(self, *, ascending: bool = True, na_position: str = "last"):
        if na_position not in ["first", "last"]:
            raise ValueError("Param na_position must be one of 'first' or 'last'")
        na_last = na_position == "last"
        index_columns = self._block.index_columns
        ordering = [
            order.ascending_over(column, na_last)
            if ascending
            else order.descending_over(column, na_last)
            for column in index_columns
        ]
        return Index(self._block.order_by(ordering))

    def astype(
        self,
        dtype: Union[bigframes.dtypes.DtypeString, bigframes.dtypes.Dtype],
    ) -> Index:
        if self.nlevels > 1:
            raise TypeError("Multiindex does not support 'astype'")
        return self._apply_unary_expr(ops.AsTypeOp(to_type=dtype).as_expr("arg"))

    def all(self) -> bool:
        if self.nlevels > 1:
            raise TypeError("Multiindex does not support 'all'")
        return typing.cast(bool, self._apply_aggregation(agg_ops.all_op))

    def any(self) -> bool:
        if self.nlevels > 1:
            raise TypeError("Multiindex does not support 'any'")
        return typing.cast(bool, self._apply_aggregation(agg_ops.any_op))

    def nunique(self) -> int:
        return typing.cast(int, self._apply_aggregation(agg_ops.nunique_op))

    def max(self) -> typing.Any:
        return self._apply_aggregation(agg_ops.max_op)

    def min(self) -> typing.Any:
        return self._apply_aggregation(agg_ops.min_op)

    def argmax(self) -> int:
        block, row_nums = self._block.promote_offsets()
        block = block.order_by(
            [
                *[order.descending_over(col) for col in self._block.index_columns],
                order.ascending_over(row_nums),
            ]
        )
        import bigframes.series as series

        return typing.cast(int, series.Series(block.select_column(row_nums)).iloc[0])

    def argmin(self) -> int:
        block, row_nums = self._block.promote_offsets()
        block = block.order_by(
            [
                *[order.ascending_over(col) for col in self._block.index_columns],
                order.ascending_over(row_nums),
            ]
        )
        import bigframes.series as series

        return typing.cast(int, series.Series(block.select_column(row_nums)).iloc[0])

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
            self._block.index_columns,
            normalize=normalize,
            ascending=ascending,
            dropna=dropna,
        )
        import bigframes.series as series

        return series.Series(block)

    def fillna(self, value=None) -> Index:
        if self.nlevels > 1:
            raise TypeError("Multiindex does not support 'fillna'")
        return self._apply_unary_expr(ops.fillna_op.as_expr("arg", ex.const(value)))

    def rename(self, name: Union[str, Sequence[str]]) -> Index:
        names = [name] if isinstance(name, str) else list(name)
        if len(names) != self.nlevels:
            raise ValueError("'name' must be same length as levels")
        return Index(self._block.with_index_labels(names))

    def drop(
        self,
        labels: typing.Any,
    ) -> Index:
        # ignore axis, columns params
        block = self._block
        level_id = self._block.index_columns[0]
        if utils.is_list_like(labels):
            block, inverse_condition_id = block.apply_unary_op(
                level_id, ops.IsInOp(values=tuple(labels), match_nulls=True)
            )
            block, condition_id = block.apply_unary_op(
                inverse_condition_id, ops.invert_op
            )
        else:
            block, condition_id = block.project_expr(
                ops.ne_op.as_expr(level_id, ex.const(labels))
            )
        block = block.filter_by_id(condition_id, keep_null=True)
        block = block.drop_columns([condition_id])
        return Index(block)

    def dropna(self, how: str = "any") -> Index:
        if how not in ("any", "all"):
            raise ValueError("'how' must be one of 'any', 'all'")
        result = block_ops.dropna(self._block, self._block.index_columns, how=how)  # type: ignore
        return Index(result)

    def drop_duplicates(self, *, keep: str = "first") -> Index:
        block = block_ops.drop_duplicates(self._block, self._block.index_columns, keep)
        return Index(block)

    def isin(self, values) -> Index:
        if not utils.is_list_like(values):
            raise TypeError(
                "only list-like objects are allowed to be passed to "
                f"isin(), you passed a [{type(values).__name__}]"
            )

        return self._apply_unary_expr(
            ops.IsInOp(values=tuple(values), match_nulls=True).as_expr("arg")
        ).fillna(value=False)

    def _apply_unary_expr(
        self,
        op: ex.Expression,
    ) -> Index:
        """Applies a unary operator to the index."""
        if len(op.unbound_variables) != 1:
            raise ValueError("Expression must have exactly 1 unbound variable.")
        unbound_variable = op.unbound_variables[0]

        block = self._block
        result_ids = []
        for col in self._block.index_columns:
            block, result_id = block.project_expr(op.rename({unbound_variable: col}))
            result_ids.append(result_id)

        block = block.set_index(result_ids, index_labels=self._block.index.names)
        return Index(block)

    def _apply_aggregation(self, op: agg_ops.UnaryAggregateOp) -> typing.Any:
        if self.nlevels > 1:
            raise NotImplementedError(f"Multiindex does not yet support {op.name}")
        column_id = self._block.index_columns[0]
        return self._block.get_stat(column_id, op)

    def __getitem__(self, key: int) -> typing.Any:
        if isinstance(key, int):
            if key != -1:
                result_pd_df, _ = self._block.slice(key, key + 1, 1).to_pandas()
            else:  # special case, want [-1:] instead of [-1:0]
                result_pd_df, _ = self._block.slice(key).to_pandas()
            if result_pd_df.index.empty:
                raise IndexError("single positional indexer is out-of-bounds")
            return result_pd_df.index[0]
        else:
            raise NotImplementedError(f"Index key not supported {key}")

    def to_pandas(self) -> pandas.Index:
        """Gets the Index as a pandas Index.

        Returns:
            pandas.Index:
                A pandas Index with all of the labels from this Index.
        """
        return self._block.index.to_pandas()

    def to_numpy(self, dtype=None, **kwargs) -> np.ndarray:
        return self.to_pandas().to_numpy(dtype, **kwargs)

    __array__ = to_numpy

    def __len__(self):
        return self.shape[0]


# Index that mutates the originating dataframe/series
class FrameIndex(Index):
    def __init__(
        self,
        series_or_dataframe: typing.Union[
            bigframes.series.Series, bigframes.dataframe.DataFrame
        ],
    ):
        super().__init__(series_or_dataframe._block)
        self._whole_frame = series_or_dataframe

    @property
    def names(self) -> typing.Sequence[blocks.Label]:
        """Returns the names of the Index."""
        return self._block._index_labels

    @names.setter
    def names(self, values: typing.Sequence[blocks.Label]):
        new_block = self._whole_frame._get_block().with_index_labels(values)
        self._whole_frame._set_block(new_block)
        self._block = new_block
