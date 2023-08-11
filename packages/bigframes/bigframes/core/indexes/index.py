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
from typing import Callable, Tuple

import numpy as np
import pandas

import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.joins as joins
import bigframes.dtypes as bf_dtypes
import third_party.bigframes_vendored.pandas.core.indexes.base as vendored_pandas_index


class Index(vendored_pandas_index.Index):
    __doc__ = vendored_pandas_index.Index.__doc__

    def __init__(self, data: blocks.BlockHolder):
        self._data = data

    @property
    def name(self) -> typing.Optional[str]:
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
        return self._data._set_block(self._data._get_block().with_index_labels(values))

    @property
    def shape(self) -> typing.Tuple[int]:
        return (self._data._get_block().shape[0],)

    @property
    def size(self) -> int:
        """Returns the size of the Index."""
        return self.shape[0]

    @property
    def empty(self) -> bool:
        """Returns True if the Index is empty, otherwise returns False."""
        return self.shape[0] == 0

    def __getitem__(self, key: int) -> typing.Any:
        if isinstance(key, int):
            result_pd_df, _ = self._data._get_block().slice(key, key + 1, 1).to_pandas()
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
        return IndexValue(self._data._get_block()).to_pandas()

    def to_numpy(self, dtype=None, **kwargs) -> np.ndarray:
        return self.to_pandas().to_numpy(dtype, **kwargs)

    __array__ = to_numpy

    def __len__(self):
        return self.shape[0]


class IndexValue:
    """An immutable index."""

    def __init__(self, block: blocks.Block):
        self._block = block

    @property
    def _expr(self) -> core.ArrayValue:
        return self._block.expr

    @property
    def name(self) -> typing.Optional[str]:
        return self._block._index_labels[0]

    @property
    def names(self) -> typing.Sequence[typing.Optional[str]]:
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
        index_column = self._block.index_columns[0]
        expr = self._expr.projection([self._expr.get_any_column(index_column)])
        results, _ = expr.start_query()
        df = expr._session._rows_to_dataframe(results)
        df.set_index(index_column)
        index = df.index
        index.name = self._block._index_labels[0]
        return index

    def join(
        self,
        other: IndexValue,
        *,
        how="left",
        sort=False,
        block_identity_join: bool = False,
    ) -> Tuple[IndexValue, Tuple[Callable[[str], str], Callable[[str], str]],]:
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
) -> Tuple[IndexValue, Tuple[Callable[[str], str], Callable[[str], str]],]:
    (
        combined_expr,
        joined_index_col_names,
        (get_column_left, get_column_right),
    ) = joins.join_by_column(
        left._block.expr,
        left._block.index_columns,
        right._block.expr,
        right._block.index_columns,
        how=how,
        sort=sort,
        allow_row_identity_join=(not block_identity_join),
    )
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    left_indices = [get_column_left(col_id) for col_id in left._block.index_columns]
    right_indices = [get_column_right(col_id) for col_id in right._block.index_columns]
    combined_expr = combined_expr.drop_columns(left_indices).drop_columns(right_indices)
    block = blocks.Block(
        combined_expr,
        index_columns=[*joined_index_col_names],
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
) -> Tuple[IndexValue, Tuple[Callable[[str], str], Callable[[str], str]],]:
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
    (
        combined_expr,
        joined_index_col_names,
        (get_column_left, get_column_right),
    ) = joins.join_by_column(
        left._block.expr,
        left_join_ids,
        right._block.expr,
        right_join_ids,
        how=how,
        sort=sort,
        # If we're only joining on a subset of the index columns, we need to
        # perform a true join.
        allow_row_identity_join=names_fully_match and not block_identity_join,
    )
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    combined_expr = combined_expr.drop_columns(
        [get_column_left(col) for col in left_join_ids]
    ).drop_columns([get_column_right(col) for col in right_join_ids])

    if left.nlevels == 1:
        index_labels = right.names
    elif right.nlevels == 1:
        index_labels = left.names
    else:
        index_labels = [*common_names, *left_only_names, *right_only_names]

    def resolve_label_id(label: blocks.Label) -> str:
        if label in common_names:
            return joined_index_col_names[common_names.index(label)]
        if label in left_only_names:
            return get_column_left(left.resolve_level_name(label))
        if label in right_only_names:
            return get_column_right(right.resolve_level_name(label))
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
