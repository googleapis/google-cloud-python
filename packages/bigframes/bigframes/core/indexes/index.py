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
from typing import Mapping, Sequence, Tuple, Union

import numpy as np
import pandas

import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.block_transforms as block_ops
import bigframes.core.blocks as blocks
import bigframes.core.joins as joining
import bigframes.core.ordering as order
import bigframes.core.utils as utils
import bigframes.dtypes
import bigframes.dtypes as bf_dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import third_party.bigframes_vendored.pandas.core.indexes.base as vendored_pandas_index


class Index(vendored_pandas_index.Index):
    __doc__ = vendored_pandas_index.Index.__doc__

    def __init__(self, data: blocks.BlockHolder):
        self._data = data

    @property
    def name(self) -> blocks.Label:
        return self.names[0]

    @name.setter
    def name(self, value: blocks.Label):
        self.names = [value]

    @property
    def names(self) -> typing.Sequence[blocks.Label]:
        """Returns the names of the Index."""
        return self._data._get_block()._index_labels

    @names.setter
    def names(self, values: typing.Sequence[blocks.Label]):
        return self._data._set_block(self._block.with_index_labels(values))

    @property
    def nlevels(self) -> int:
        return len(self._data._get_block().index_columns)

    @property
    def values(self) -> np.ndarray:
        return self.to_numpy()

    @property
    def ndim(self) -> int:
        return 1

    @property
    def shape(self) -> typing.Tuple[int]:
        return (self._data._get_block().shape[0],)

    @property
    def dtype(self):
        return self._block.index_dtypes[0] if self.nlevels == 1 else np.dtype("O")

    @property
    def dtypes(self) -> pandas.Series:
        return pandas.Series(
            data=self._block.index_dtypes, index=self._block.index_labels  # type:ignore
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
            self._data._get_block().is_monotonic_increasing(
                self._data._get_block().index_columns
            ),
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
            self._data._get_block().is_monotonic_decreasing(
                self._data._get_block().index_columns
            ),
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
    def _block(self) -> blocks.Block:
        return self._data._get_block()

    @property
    def T(self) -> Index:
        return self.transpose()

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
        direction = (
            order.OrderingDirection.ASC if ascending else order.OrderingDirection.DESC
        )
        na_last = na_position == "last"
        index_columns = self._block.index_columns
        ordering = [
            order.OrderingColumnReference(column, direction=direction, na_last=na_last)
            for column in index_columns
        ]
        return Index._from_block(self._block.order_by(ordering))

    def astype(
        self,
        dtype: Union[bigframes.dtypes.DtypeString, bigframes.dtypes.Dtype],
    ) -> Index:
        if self.nlevels > 1:
            raise TypeError("Multiindex does not support 'astype'")
        return self._apply_unary_op(ops.AsTypeOp(dtype))

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
                *[
                    order.OrderingColumnReference(
                        col, direction=order.OrderingDirection.DESC
                    )
                    for col in self._block.index_columns
                ],
                order.OrderingColumnReference(row_nums),
            ]
        )
        import bigframes.series as series

        return typing.cast(int, series.Series(block.select_column(row_nums)).iloc[0])

    def argmin(self) -> int:
        block, row_nums = self._block.promote_offsets()
        block = block.order_by(
            [
                *[
                    order.OrderingColumnReference(col)
                    for col in self._block.index_columns
                ],
                order.OrderingColumnReference(row_nums),
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
        return self._apply_unary_op(ops.partial_right(ops.fillna_op, value))

    def rename(self, name: Union[str, Sequence[str]]) -> Index:
        names = [name] if isinstance(name, str) else list(name)
        if len(names) != self.nlevels:
            raise ValueError("'name' must be same length as levels")
        return Index._from_block(self._block.with_index_labels(names))

    def drop(
        self,
        labels: typing.Any,
    ) -> Index:
        # ignore axis, columns params
        block = self._block
        level_id = self._block.index_columns[0]
        if utils.is_list_like(labels):
            block, inverse_condition_id = block.apply_unary_op(
                level_id, ops.IsInOp(labels, match_nulls=True)
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
        return Index._from_block(block)

    def dropna(self, how: str = "any") -> Index:
        if how not in ("any", "all"):
            raise ValueError("'how' must be one of 'any', 'all'")
        result = block_ops.dropna(self._block, self._block.index_columns, how=how)  # type: ignore
        return Index._from_block(result)

    def drop_duplicates(self, *, keep: str = "first") -> Index:
        block = block_ops.drop_duplicates(self._block, self._block.index_columns, keep)
        return Index._from_block(block)

    def isin(self, values) -> Index:
        if not utils.is_list_like(values):
            raise TypeError(
                "only list-like objects are allowed to be passed to "
                f"isin(), you passed a [{type(values).__name__}]"
            )

        return self._apply_unary_op(ops.IsInOp(values, match_nulls=True)).fillna(
            value=False
        )

    def _apply_unary_op(
        self,
        op: ops.UnaryOp,
    ) -> Index:
        """Applies a unary operator to the index."""
        block = self._block
        result_ids = []
        for col in self._block.index_columns:
            block, result_id = block.apply_unary_op(col, op)
            result_ids.append(result_id)

        block = block.set_index(result_ids, index_labels=self._block.index_labels)
        return Index._from_block(block)

    def _apply_aggregation(self, op: agg_ops.AggregateOp) -> typing.Any:
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
            if result_pd_df.empty:
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
        return IndexValue(self._block).to_pandas()

    def to_numpy(self, dtype=None, **kwargs) -> np.ndarray:
        return self.to_pandas().to_numpy(dtype, **kwargs)

    __array__ = to_numpy

    def __len__(self):
        return self.shape[0]

    @classmethod
    def _from_block(cls, block: blocks.Block) -> Index:
        import bigframes.dataframe as df

        return Index(df.DataFrame(block))


class IndexValue:
    """An immutable index."""

    def __init__(self, block: blocks.Block):
        self._block = block

    @property
    def _expr(self) -> core.ArrayValue:
        return self._block.expr

    @property
    def name(self) -> blocks.Label:
        return self._block._index_labels[0]

    @property
    def names(self) -> typing.Sequence[blocks.Label]:
        return self._block._index_labels

    @property
    def nlevels(self) -> int:
        return len(self._block._index_columns)

    @property
    def dtypes(
        self,
    ) -> typing.Sequence[typing.Union[bf_dtypes.Dtype, np.dtype[typing.Any]]]:
        return self._block.index_dtypes

    def __repr__(self) -> str:
        """Converts an Index to a string."""
        # TODO(swast): Add a timeout here? If the query is taking a long time,
        # maybe we just print the job metadata that we have so far?
        # TODO(swast): Avoid downloading the whole index by using job
        # metadata, like we do with DataFrame.
        preview = self.to_pandas()
        return repr(preview)

    def to_pandas(self) -> pandas.Index:
        """Executes deferred operations and downloads the results."""
        # Project down to only the index column. So the query can be cached to visualize other data.
        index_columns = list(self._block.index_columns)
        dtypes = dict(zip(index_columns, self.dtypes))
        expr = self._expr.select_columns(index_columns)
        results, _ = expr.start_query()
        df = expr.session._rows_to_dataframe(results, dtypes)
        df = df.set_index(index_columns)
        index = df.index
        index.names = list(self._block._index_labels)
        return index

    def join(
        self,
        other: IndexValue,
        *,
        how="left",
        sort=False,
        block_identity_join: bool = False,
    ) -> Tuple[IndexValue, Tuple[Mapping[str, str], Mapping[str, str]],]:
        if not isinstance(other, IndexValue):
            # TODO(swast): We need to improve this error message to be more
            # actionable for the user. For example, it's possible they
            # could call set_index and try again to resolve this error.
            raise ValueError(
                f"Tried to join with an unexpected type: {type(other)}. {constants.FEEDBACK_LINK}"
            )

        # TODO(swast): Support cross-joins (requires reindexing).
        if how not in {"outer", "left", "right", "inner"}:
            raise NotImplementedError(
                f"Only how='outer','left','right','inner' currently supported. {constants.FEEDBACK_LINK}"
            )
        if self.nlevels == other.nlevels == 1:
            return join_mono_indexed(
                self, other, how=how, sort=sort, block_identity_join=block_identity_join
            )
        else:
            # Always sort mult-index join
            return join_multi_indexed(
                self, other, how=how, sort=sort, block_identity_join=block_identity_join
            )

    def resolve_level_name(self: IndexValue, label: blocks.Label) -> str:
        matches = self._block.index_name_to_col_id.get(label, [])
        if len(matches) > 1:
            raise ValueError(f"Ambiguous index level name {label}")
        if len(matches) == 0:
            raise ValueError(f"Cannot resolve index level name {label}")
        return matches[0]

    def is_uniquely_named(self: IndexValue):
        return len(set(self.names)) == len(self.names)


def join_mono_indexed(
    left: IndexValue,
    right: IndexValue,
    *,
    how="left",
    sort=False,
    block_identity_join: bool = False,
) -> Tuple[IndexValue, Tuple[Mapping[str, str], Mapping[str, str]],]:
    left_expr = left._block.expr
    right_expr = right._block.expr
    get_column_left, get_column_right = joining.JOIN_NAME_REMAPPER(
        left_expr.column_ids, right_expr.column_ids
    )
    combined_expr = left._block.expr.join(
        left._block.index_columns,
        right._block.expr,
        right._block.index_columns,
        how=how,
        allow_row_identity_join=(not block_identity_join),
    )
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    left_index = get_column_left[left._block.index_columns[0]]
    right_index = get_column_right[right._block.index_columns[0]]
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    combined_expr, coalesced_join_cols = coalesce_columns(
        combined_expr, [left_index], [right_index], how=how
    )
    if sort:
        combined_expr = combined_expr.order_by(
            [order.OrderingColumnReference(col_id) for col_id in coalesced_join_cols]
        )
    block = blocks.Block(
        combined_expr,
        index_columns=coalesced_join_cols,
        column_labels=[*left._block.column_labels, *right._block.column_labels],
        index_labels=[left.name] if left.name == right.name else [None],
    )
    return (
        typing.cast(IndexValue, block.index),
        (get_column_left, get_column_right),
    )


def join_multi_indexed(
    left: IndexValue,
    right: IndexValue,
    *,
    how="left",
    sort=False,
    block_identity_join: bool = False,
) -> Tuple[IndexValue, Tuple[Mapping[str, str], Mapping[str, str]],]:
    if not (left.is_uniquely_named() and right.is_uniquely_named()):
        raise ValueError("Joins not supported on indices with non-unique level names")

    common_names = [name for name in left.names if name in right.names]
    if len(common_names) == 0:
        raise ValueError("Cannot join without a index level in common.")

    left_only_names = [name for name in left.names if name not in right.names]
    right_only_names = [name for name in right.names if name not in left.names]

    left_join_ids = [left.resolve_level_name(name) for name in common_names]
    right_join_ids = [right.resolve_level_name(name) for name in common_names]

    names_fully_match = len(left_only_names) == 0 and len(right_only_names) == 0

    left_expr = left._block.expr
    right_expr = right._block.expr
    get_column_left, get_column_right = joining.JOIN_NAME_REMAPPER(
        left_expr.column_ids, right_expr.column_ids
    )

    combined_expr = left_expr.join(
        left_join_ids,
        right_expr,
        right_join_ids,
        how=how,
        # If we're only joining on a subset of the index columns, we need to
        # perform a true join.
        allow_row_identity_join=(names_fully_match and not block_identity_join),
    )
    left_ids_post_join = [get_column_left[id] for id in left_join_ids]
    right_ids_post_join = [get_column_right[id] for id in right_join_ids]
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    combined_expr, coalesced_join_cols = coalesce_columns(
        combined_expr, left_ids_post_join, right_ids_post_join, how=how
    )
    if sort:
        combined_expr = combined_expr.order_by(
            [order.OrderingColumnReference(col_id) for col_id in coalesced_join_cols]
        )

    if left.nlevels == 1:
        index_labels = right.names
    elif right.nlevels == 1:
        index_labels = left.names
    else:
        index_labels = [*common_names, *left_only_names, *right_only_names]

    def resolve_label_id(label: blocks.Label) -> str:
        # if name is shared between both blocks, coalesce the values
        if label in common_names:
            return coalesced_join_cols[common_names.index(label)]
        if label in left_only_names:
            return get_column_left[left.resolve_level_name(label)]
        if label in right_only_names:
            return get_column_right[right.resolve_level_name(label)]
        raise ValueError(f"Unexpected label: {label}")

    index_columns = [resolve_label_id(label) for label in index_labels]

    block = blocks.Block(
        combined_expr,
        index_columns=index_columns,
        column_labels=[*left._block.column_labels, *right._block.column_labels],
        index_labels=index_labels,
    )
    return (
        typing.cast(IndexValue, block.index),
        (get_column_left, get_column_right),
    )


def coalesce_columns(
    expr: core.ArrayValue,
    left_ids: typing.Sequence[str],
    right_ids: typing.Sequence[str],
    how: str,
) -> Tuple[core.ArrayValue, Sequence[str]]:
    result_ids = []
    for left_id, right_id in zip(left_ids, right_ids):
        if how == "left" or how == "inner":
            result_ids.append(left_id)
            expr = expr.drop_columns([right_id])
        elif how == "right":
            result_ids.append(right_id)
            expr = expr.drop_columns([left_id])
        elif how == "outer":
            coalesced_id = bigframes.core.guid.generate_guid()
            expr = expr.project_binary_op(
                left_id, right_id, ops.coalesce_op, coalesced_id
            )
            expr = expr.drop_columns([left_id, right_id])
            result_ids.append(coalesced_id)
        else:
            raise ValueError(f"Unexpected join type: {how}. {constants.FEEDBACK_LINK}")
    return expr, result_ids
