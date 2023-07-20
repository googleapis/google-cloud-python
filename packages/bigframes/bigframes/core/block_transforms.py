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

import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.ordering as ordering
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops


def indicate_duplicates(
    block: blocks.Block, columns: typing.Sequence[str], keep: str = "first"
) -> typing.Tuple[blocks.Block, str]:
    """Create a boolean column where True indicates a duplicate value"""
    if keep not in ["first", "last", False]:
        raise ValueError("keep must be one of 'first', 'last', or False'")

    if keep == "first":
        # Count how many copies occur up to current copy of value
        # Discard this value if there are copies BEFORE
        window_spec = core.WindowSpec(
            grouping_keys=tuple(columns),
            following=0,
        )
    elif keep == "last":
        # Count how many copies occur up to current copy of values
        # Discard this value if there are copies AFTER
        window_spec = core.WindowSpec(
            grouping_keys=tuple(columns),
            preceding=0,
        )
    else:  # keep == False
        # Count how many copies of the value occur in entire series.
        # Discard this value if there are copies ANYWHERE
        window_spec = core.WindowSpec(grouping_keys=tuple(columns))
    block, dummy = block.create_constant(1)
    block, val_count_col_id = block.apply_window_op(
        dummy,
        agg_ops.count_op,
        window_spec=window_spec,
    )
    block, duplicate_indicator = block.apply_unary_op(
        val_count_col_id,
        ops.partial_right(ops.gt_op, 1),
    )
    return (
        block.drop_columns(
            (
                dummy,
                val_count_col_id,
            )
        ),
        duplicate_indicator,
    )


def drop_duplicates(
    block: blocks.Block, columns: typing.Sequence[str], keep: str = "first"
) -> blocks.Block:
    block, dupe_indicator_id = indicate_duplicates(block, columns, keep)
    block, keep_indicator_id = block.apply_unary_op(dupe_indicator_id, ops.invert_op)
    return block.filter(keep_indicator_id).drop_columns(
        (dupe_indicator_id, keep_indicator_id)
    )


def value_counts(
    block: blocks.Block,
    columns: typing.Sequence[str],
    normalize: bool = False,
    sort: bool = True,
    ascending: bool = False,
    dropna: bool = True,
):
    block, dummy = block.create_constant(1)
    block, agg_ids = block.aggregate(
        by_column_ids=columns,
        aggregations=[(dummy, agg_ops.count_op)],
        dropna=dropna,
        as_index=True,
    )
    count_id = agg_ids[0]
    if normalize:
        unbound_window = core.WindowSpec()
        block, total_count_id = block.apply_window_op(
            count_id, agg_ops.sum_op, unbound_window
        )
        block, count_id = block.apply_binary_op(count_id, total_count_id, ops.div_op)

    if sort:
        block = block.order_by(
            [
                ordering.OrderingColumnReference(
                    count_id,
                    direction=ordering.OrderingDirection.ASC
                    if ascending
                    else ordering.OrderingDirection.DESC,
                )
            ]
        )
    return block.select_column(count_id).with_column_labels(["count"])


def rank(
    block: blocks.Block,
    method: str = "average",
    na_option: str = "keep",
    ascending: bool = True,
):
    if method not in ["average", "min", "max", "first", "dense"]:
        raise ValueError(
            "method must be one of 'average', 'min', 'max', 'first', or 'dense'"
        )
    if na_option not in ["keep", "top", "bottom"]:
        raise ValueError("na_option must be one of 'keep', 'top', or 'bottom'")

    columns = block.value_columns
    labels = block.column_labels
    # Step 1: Calculate row numbers for each row
    # Identify null values to be treated according to na_option param
    rownum_col_ids = []
    nullity_col_ids = []
    for col in columns:
        block, nullity_col_id = block.apply_unary_op(
            col,
            ops.isnull_op,
        )
        nullity_col_ids.append(nullity_col_id)
        window = core.WindowSpec(
            # BigQuery has syntax to reorder nulls with "NULLS FIRST/LAST", but that is unavailable through ibis presently, so must order on a separate nullity expression first.
            ordering=(
                ordering.OrderingColumnReference(
                    col,
                    ordering.OrderingDirection.ASC
                    if ascending
                    else ordering.OrderingDirection.DESC,
                    na_last=(na_option in ["bottom", "keep"]),
                ),
            ),
        )
        # Count_op ignores nulls, so if na_option is "top" or "bottom", we instead count the nullity columns, where nulls have been mapped to bools
        block, rownum_id = block.apply_window_op(
            col if na_option == "keep" else nullity_col_id,
            agg_ops.dense_rank_op if method == "dense" else agg_ops.count_op,
            window_spec=window,
            skip_reproject_unsafe=(col != columns[-1]),
        )
        rownum_col_ids.append(rownum_id)

    # Step 2: Apply aggregate to groups of like input values.
    # This step is skipped for method=='first' or 'dense'
    if method in ["average", "min", "max"]:
        agg_op = {
            "average": agg_ops.mean_op,
            "min": agg_ops.min_op,
            "max": agg_ops.max_op,
        }[method]
        post_agg_rownum_col_ids = []
        for i in range(len(columns)):
            block, result_id = block.apply_window_op(
                rownum_col_ids[i],
                agg_op,
                window_spec=core.WindowSpec(grouping_keys=[columns[i]]),
                skip_reproject_unsafe=(i < (len(columns) - 1)),
            )
            post_agg_rownum_col_ids.append(result_id)
        rownum_col_ids = post_agg_rownum_col_ids

    # Step 3: post processing: mask null values and cast to float
    if method in ["min", "max", "first", "dense"]:
        # Pandas rank always produces Float64, so must cast for aggregation types that produce ints
        block = block.multi_apply_unary_op(
            rownum_col_ids, ops.AsTypeOp(pd.Float64Dtype())
        )
    if na_option == "keep":
        # For na_option "keep", null inputs must produce null outputs
        for i in range(len(columns)):
            block, null_const = block.create_constant(pd.NA, dtype=pd.Float64Dtype())
            block, rownum_col_ids[i] = block.apply_ternary_op(
                null_const, nullity_col_ids[i], rownum_col_ids[i], ops.where_op
            )

    return block.select_columns(rownum_col_ids).with_column_labels(labels)
