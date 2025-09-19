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

import functools
from typing import Sequence

import pandas as pd

from bigframes.core import blocks
from bigframes.core import expression as ex
import bigframes.enums
import bigframes.operations as ops


def block_groupby_iter(
    block: blocks.Block,
    *,
    by_col_ids: Sequence[str],
    by_key_is_singular: bool,
    dropna: bool,
):
    original_index_columns = block._index_columns
    original_index_labels = block._index_labels
    by_col_ids = by_col_ids
    block = block.reset_index(
        level=None,
        # Keep the original index columns so they can be recovered.
        drop=False,
        allow_duplicates=True,
        replacement=bigframes.enums.DefaultIndexKind.NULL,
    ).set_index(
        by_col_ids,
        # Keep by_col_ids in-place so the ordering doesn't change.
        drop=False,
        append=False,
    )
    block.cached(
        force=True,
        # All DataFrames will be filtered by by_col_ids, so
        # force block.cached() to cluster by the new index by explicitly
        # setting `session_aware=False`. This will ensure that the filters
        # are more efficient.
        session_aware=False,
    )
    keys_block, _ = block.aggregate(by_col_ids, dropna=dropna)
    for chunk in keys_block.to_pandas_batches():
        # Convert to MultiIndex to make sure we get tuples,
        # even for singular keys.
        by_keys_index = chunk.index
        if not isinstance(by_keys_index, pd.MultiIndex):
            by_keys_index = pd.MultiIndex.from_frame(by_keys_index.to_frame())

        for by_keys in by_keys_index:
            filtered_block = (
                # To ensure the cache is used, filter first, then reset the
                # index before yielding the DataFrame.
                block.filter(
                    functools.reduce(
                        ops.and_op.as_expr,
                        (
                            ops.eq_op.as_expr(by_col, ex.const(by_key))
                            for by_col, by_key in zip(by_col_ids, by_keys)
                        ),
                    ),
                ).set_index(
                    original_index_columns,
                    # We retained by_col_ids in the set_index call above,
                    # so it's safe to drop the duplicates now.
                    drop=True,
                    append=False,
                    index_labels=original_index_labels,
                )
            )

            if by_key_is_singular:
                yield by_keys[0], filtered_block
            else:
                yield by_keys, filtered_block
