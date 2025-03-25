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

import functools
import typing
from typing import Optional, Sequence

import bigframes_vendored.constants as constants
import pandas as pd

import bigframes.constants
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.expression as ex
import bigframes.core.ordering as ordering
import bigframes.core.window_spec as windows
import bigframes.dtypes
import bigframes.dtypes as dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops


def equals(block1: blocks.Block, block2: blocks.Block) -> bool:
    if not block1.column_labels.equals(block2.column_labels):
        return False
    if block1.dtypes != block2.dtypes:
        return False
    # TODO: More advanced expression tree traversals to short circuit actually querying data

    block1 = block1.reset_index(drop=False)
    block2 = block2.reset_index(drop=False)

    joined_block, (lmap, rmap) = block1.join(block2, how="outer")

    exprs = []
    for lcol, rcol in zip(block1.value_columns, block2.value_columns):
        exprs.append(
            ops.fillna_op.as_expr(
                ops.eq_null_match_op.as_expr(lmap[lcol], rmap[rcol]), ex.const(False)
            )
        )

    joined_block = joined_block.project_exprs(
        exprs, labels=list(range(len(exprs))), drop=True
    )
    stacked_block = joined_block.stack()
    result = stacked_block.get_stat(stacked_block.value_columns[0], agg_ops.all_op)
    return typing.cast(bool, result)


def indicate_duplicates(
    block: blocks.Block, columns: typing.Sequence[str], keep: str = "first"
) -> typing.Tuple[blocks.Block, str]:
    """Create a boolean column where True indicates a duplicate value"""
    if keep not in ["first", "last", False]:
        raise ValueError("keep must be one of 'first', 'last', or False'")

    if keep == "first":
        # Count how many copies occur up to current copy of value
        # Discard this value if there are copies BEFORE
        window_spec = windows.cumulative_rows(
            grouping_keys=tuple(columns),
        )
    elif keep == "last":
        # Count how many copies occur up to current copy of values
        # Discard this value if there are copies AFTER
        window_spec = windows.inverse_cumulative_rows(
            grouping_keys=tuple(columns),
        )
    else:  # keep == False
        # Count how many copies of the value occur in entire series.
        # Discard this value if there are copies ANYWHERE
        window_spec = windows.unbound(grouping_keys=tuple(columns))
    block, dummy = block.create_constant(1)
    # use row number as will work even with partial ordering
    block, val_count_col_id = block.apply_window_op(
        dummy,
        agg_ops.sum_op,
        window_spec=window_spec,
    )
    block, duplicate_indicator = block.project_expr(
        ops.gt_op.as_expr(val_count_col_id, ex.const(1))
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


def quantile(
    block: blocks.Block,
    columns: Sequence[str],
    qs: Sequence[float],
    grouping_column_ids: Sequence[str] = (),
    dropna: bool = False,
) -> blocks.Block:
    # TODO: handle windowing and more interpolation methods
    window = windows.unbound(
        grouping_keys=tuple(grouping_column_ids),
    )
    quantile_cols = []
    labels = []
    if len(columns) * len(qs) > bigframes.constants.MAX_COLUMNS:
        raise NotImplementedError("Too many aggregates requested.")
    for col in columns:
        for q in qs:
            label = block.col_id_to_label[col]
            new_label = (*label, q) if isinstance(label, tuple) else (label, q)
            labels.append(new_label)
            block, quantile_col = block.apply_window_op(
                col,
                agg_ops.QuantileOp(q),
                window_spec=window,
            )
            quantile_cols.append(quantile_col)
    block, _ = block.aggregate(
        grouping_column_ids,
        tuple(
            ex.UnaryAggregation(agg_ops.AnyValueOp(), ex.deref(col))
            for col in quantile_cols
        ),
        column_labels=pd.Index(labels),
        dropna=dropna,
    )
    return block


def interpolate(block: blocks.Block, method: str = "linear") -> blocks.Block:
    supported_methods = [
        "linear",
        "values",
        "index",
        "nearest",
        "zero",
        "slinear",
    ]
    if method not in supported_methods:
        raise NotImplementedError(
            f"Method {method} not supported, following interpolate methods supported: {', '.join(supported_methods)}. {constants.FEEDBACK_LINK}"
        )
    output_column_ids = []

    original_columns = block.value_columns
    original_labels = block.column_labels

    if method == "linear":  # Assumes evenly spaced, ignore index
        block, xvalues = block.promote_offsets()
    else:
        index_columns = block.index_columns
        if len(index_columns) != 1:
            raise ValueError("only method 'linear' supports multi-index")
        xvalues = block.index_columns[0]
        if block.index.dtypes[0] not in dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE:
            raise ValueError("Can only interpolate on numeric index.")

    for column in original_columns:
        # null in same places column is null
        should_interpolate = block._column_type(column) in [
            pd.Float64Dtype(),
            pd.Int64Dtype(),
        ]
        if should_interpolate:
            interpolate_method_map = {
                "linear": "linear",
                "values": "linear",
                "index": "linear",
                "slinear": "linear",
                "zero": "ffill",
                "nearest": "nearest",
            }
            extrapolating_methods = ["linear", "values", "index"]
            interpolate_method = interpolate_method_map[method]
            do_extrapolate = method in extrapolating_methods
            block, interpolated = _interpolate_column(
                block,
                column,
                xvalues,
                interpolate_method=interpolate_method,
                do_extrapolate=do_extrapolate,
            )
            output_column_ids.append(interpolated)
        else:
            output_column_ids.append(column)

    block = block.select_columns(output_column_ids)
    return block.with_column_labels(original_labels)


def _interpolate_column(
    block: blocks.Block,
    column: str,
    x_values: str,
    interpolate_method: str,
    do_extrapolate: bool = True,
) -> typing.Tuple[blocks.Block, str]:
    if interpolate_method not in ["linear", "nearest", "ffill"]:
        raise ValueError("interpolate method not supported")
    window_ordering = (ordering.OrderingExpression(ex.deref(x_values)),)
    backwards_window = windows.rows(end=0, ordering=window_ordering)
    forwards_window = windows.rows(start=0, ordering=window_ordering)

    # Note, this method may
    block, notnull = block.apply_unary_op(column, ops.notnull_op)
    block, masked_offsets = block.project_expr(
        ops.where_op.as_expr(x_values, notnull, ex.const(None))
    )

    block, previous_value = block.apply_window_op(
        column, agg_ops.LastNonNullOp(), backwards_window
    )
    block, next_value = block.apply_window_op(
        column, agg_ops.FirstNonNullOp(), forwards_window
    )
    block, previous_value_offset = block.apply_window_op(
        masked_offsets,
        agg_ops.LastNonNullOp(),
        backwards_window,
        skip_reproject_unsafe=True,
    )
    block, next_value_offset = block.apply_window_op(
        masked_offsets,
        agg_ops.FirstNonNullOp(),
        forwards_window,
        skip_reproject_unsafe=True,
    )

    if interpolate_method == "linear":
        block, prediction_id = _interpolate_points_linear(
            block,
            previous_value_offset,
            previous_value,
            next_value_offset,
            next_value,
            x_values,
        )
    elif interpolate_method == "nearest":
        block, prediction_id = _interpolate_points_nearest(
            block,
            previous_value_offset,
            previous_value,
            next_value_offset,
            next_value,
            x_values,
        )
    else:  # interpolate_method == 'ffill':
        block, prediction_id = _interpolate_points_ffill(
            block,
            previous_value_offset,
            previous_value,
            next_value_offset,
            next_value,
            x_values,
        )
    if do_extrapolate:
        block, prediction_id = block.apply_binary_op(
            prediction_id, previous_value, ops.fillna_op
        )

    return block.apply_binary_op(column, prediction_id, ops.fillna_op)


def _interpolate_points_linear(
    block: blocks.Block,
    x0_id: str,
    y0_id: str,
    x1_id: str,
    y1_id: str,
    xpredict_id: str,
) -> typing.Tuple[blocks.Block, str]:
    """Applies linear interpolation equation to predict y values for xpredict."""
    block, x1x0diff = block.apply_binary_op(x1_id, x0_id, ops.sub_op)
    block, y1y0diff = block.apply_binary_op(y1_id, y0_id, ops.sub_op)
    block, xpredictx0diff = block.apply_binary_op(xpredict_id, x0_id, ops.sub_op)

    block, y1_weight = block.apply_binary_op(y1y0diff, x1x0diff, ops.div_op)
    block, y1_part = block.apply_binary_op(xpredictx0diff, y1_weight, ops.mul_op)

    block, prediction_id = block.apply_binary_op(y0_id, y1_part, ops.add_op)
    block = block.drop_columns([x1x0diff, y1y0diff, xpredictx0diff, y1_weight, y1_part])
    return block, prediction_id


def _interpolate_points_nearest(
    block: blocks.Block,
    x0_id: str,
    y0_id: str,
    x1_id: str,
    y1_id: str,
    xpredict_id: str,
) -> typing.Tuple[blocks.Block, str]:
    """Interpolate by taking the y value of the nearest x value"""
    left_diff = ops.sub_op.as_expr(xpredict_id, x0_id)
    right_diff = ops.sub_op.as_expr(x1_id, xpredict_id)
    # If diffs equal, choose left
    choose_left = ops.fillna_op.as_expr(
        ops.le_op.as_expr(left_diff, right_diff), ex.const(False)
    )

    nearest = ops.where_op.as_expr(y0_id, choose_left, y1_id)

    is_interpolation = ops.and_op.as_expr(
        ops.notnull_op.as_expr(y0_id), ops.notnull_op.as_expr(y1_id)
    )

    return block.project_expr(
        ops.where_op.as_expr(nearest, is_interpolation, ex.const(None))
    )


def _interpolate_points_ffill(
    block: blocks.Block,
    x0_id: str,
    y0_id: str,
    x1_id: str,
    y1_id: str,
    xpredict_id: str,
) -> typing.Tuple[blocks.Block, str]:
    """Interpolates by using the preceding values"""
    # check for existance of y1, otherwise we are extrapolating instead of interpolating
    return block.project_expr(
        ops.where_op.as_expr(y0_id, ops.notnull_op.as_expr(y1_id), ex.const(None))
    )


def drop_duplicates(
    block: blocks.Block, columns: typing.Sequence[str], keep: str = "first"
) -> blocks.Block:
    block, dupe_indicator_id = indicate_duplicates(block, columns, keep)
    block, keep_indicator_id = block.apply_unary_op(dupe_indicator_id, ops.invert_op)
    return block.filter_by_id(keep_indicator_id).drop_columns(
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
        aggregations=[ex.UnaryAggregation(agg_ops.count_op, ex.deref(dummy))],
        dropna=dropna,
    )
    count_id = agg_ids[0]
    if normalize:
        unbound_window = windows.unbound()
        block, total_count_id = block.apply_window_op(
            count_id, agg_ops.sum_op, unbound_window
        )
        block, count_id = block.apply_binary_op(count_id, total_count_id, ops.div_op)

    if sort:
        block = block.order_by(
            [
                ordering.OrderingExpression(
                    ex.deref(count_id),
                    direction=ordering.OrderingDirection.ASC
                    if ascending
                    else ordering.OrderingDirection.DESC,
                )
            ]
        )
    return block.select_column(count_id).with_column_labels(
        ["proportion" if normalize else "count"]
    )


def pct_change(block: blocks.Block, periods: int = 1) -> blocks.Block:
    column_labels = block.column_labels

    # Window framing clause is not allowed for analytic function lag.
    window_spec = windows.unbound()

    original_columns = block.value_columns
    block, shift_columns = block.multi_apply_window_op(
        original_columns, agg_ops.ShiftOp(periods), window_spec=window_spec
    )
    exprs = []
    for original_col, shifted_col in zip(original_columns, shift_columns):
        change_expr = ops.sub_op.as_expr(original_col, shifted_col)
        pct_change_expr = ops.div_op.as_expr(change_expr, shifted_col)
        exprs.append(pct_change_expr)
    return block.project_exprs(exprs, labels=column_labels, drop=True)


def rank(
    block: blocks.Block,
    method: str = "average",
    na_option: str = "keep",
    ascending: bool = True,
    grouping_cols: tuple[str, ...] = (),
    columns: tuple[str, ...] = (),
):
    if method not in ["average", "min", "max", "first", "dense"]:
        raise ValueError(
            "method must be one of 'average', 'min', 'max', 'first', or 'dense'"
        )
    if na_option not in ["keep", "top", "bottom"]:
        raise ValueError("na_option must be one of 'keep', 'top', or 'bottom'")

    columns = columns or tuple(col for col in block.value_columns)
    labels = [block.col_id_to_label[id] for id in columns]
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
        window_ordering = (
            ordering.OrderingExpression(
                ex.deref(col),
                ordering.OrderingDirection.ASC
                if ascending
                else ordering.OrderingDirection.DESC,
                na_last=(na_option in ["bottom", "keep"]),
            ),
        )
        # Count_op ignores nulls, so if na_option is "top" or "bottom", we instead count the nullity columns, where nulls have been mapped to bools
        block, rownum_id = block.apply_window_op(
            col if na_option == "keep" else nullity_col_id,
            agg_ops.dense_rank_op if method == "dense" else agg_ops.count_op,
            window_spec=windows.unbound(
                grouping_keys=grouping_cols, ordering=window_ordering
            )
            if method == "dense"
            else windows.rows(
                end=0, ordering=window_ordering, grouping_keys=grouping_cols
            ),
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
                window_spec=windows.unbound(grouping_keys=(columns[i], *grouping_cols)),
                skip_reproject_unsafe=(i < (len(columns) - 1)),
            )
            post_agg_rownum_col_ids.append(result_id)
        rownum_col_ids = post_agg_rownum_col_ids

    # Pandas masks all values where any grouping column is null
    # Note: we use pd.NA instead of float('nan')
    if grouping_cols:
        predicate = functools.reduce(
            ops.and_op.as_expr,
            [ops.notnull_op.as_expr(column_id) for column_id in grouping_cols],
        )
        block = block.project_exprs(
            [
                ops.where_op.as_expr(
                    ex.deref(col),
                    predicate,
                    ex.const(None),
                )
                for col in rownum_col_ids
            ],
            labels=labels,
        )
        rownum_col_ids = list(block.value_columns[-len(rownum_col_ids) :])

    # Step 3: post processing: mask null values and cast to float
    if method in ["min", "max", "first", "dense"]:
        # Pandas rank always produces Float64, so must cast for aggregation types that produce ints
        return (
            block.select_columns(rownum_col_ids)
            .multi_apply_unary_op(ops.AsTypeOp(pd.Float64Dtype()))
            .with_column_labels(labels)
        )
    if na_option == "keep":
        # For na_option "keep", null inputs must produce null outputs
        exprs = []
        for i in range(len(columns)):
            exprs.append(
                ops.where_op.as_expr(
                    ex.const(pd.NA, dtype=pd.Float64Dtype()),
                    nullity_col_ids[i],
                    rownum_col_ids[i],
                )
            )
        return block.project_exprs(exprs, labels=labels, drop=True)

    return block.select_columns(rownum_col_ids).with_column_labels(labels)


def dropna(
    block: blocks.Block,
    column_ids: typing.Sequence[str],
    how: typing.Literal["all", "any"] = "any",
    subset: Optional[typing.Sequence[str]] = None,
):
    """
    Drop na entries from block
    """
    if subset is None:
        subset = column_ids

    predicates = [
        ops.notnull_op.as_expr(column_id)
        for column_id in column_ids
        if column_id in subset
    ]
    if len(predicates) == 0:
        return block
    if how == "any":
        predicate = functools.reduce(ops.and_op.as_expr, predicates)
    else:  # "all"
        predicate = functools.reduce(ops.or_op.as_expr, predicates)
    return block.filter(predicate)


def nsmallest(
    block: blocks.Block,
    n: int,
    column_ids: typing.Sequence[str],
    keep: str,
) -> blocks.Block:
    if keep not in ("first", "last", "all"):
        raise ValueError("'keep must be one of 'first', 'last', or 'all'")
    if keep == "last":
        block = block.reversed()
    order_refs = [
        ordering.OrderingExpression(
            ex.deref(col_id), direction=ordering.OrderingDirection.ASC
        )
        for col_id in column_ids
    ]
    block = block.order_by(order_refs)
    if keep in ("first", "last"):
        return block.slice(0, n)
    else:  # keep == "all":
        block, counter = block.apply_window_op(
            column_ids[0],
            agg_ops.rank_op,
            window_spec=windows.unbound(ordering=tuple(order_refs)),
        )
        block, condition = block.project_expr(ops.le_op.as_expr(counter, ex.const(n)))
        block = block.filter_by_id(condition)
        return block.drop_columns([counter, condition])


def nlargest(
    block: blocks.Block,
    n: int,
    column_ids: typing.Sequence[str],
    keep: str,
) -> blocks.Block:
    if keep not in ("first", "last", "all"):
        raise ValueError("'keep must be one of 'first', 'last', or 'all'")
    if keep == "last":
        block = block.reversed()
    order_refs = [
        ordering.OrderingExpression(
            ex.deref(col_id), direction=ordering.OrderingDirection.DESC
        )
        for col_id in column_ids
    ]
    block = block.order_by(order_refs)
    if keep in ("first", "last"):
        return block.slice(0, n)
    else:  # keep == "all":
        block, counter = block.apply_window_op(
            column_ids[0],
            agg_ops.rank_op,
            window_spec=windows.unbound(ordering=tuple(order_refs)),
        )
        block, condition = block.project_expr(ops.le_op.as_expr(counter, ex.const(n)))
        block = block.filter_by_id(condition)
        return block.drop_columns([counter, condition])


def skew(
    block: blocks.Block,
    skew_column_ids: typing.Sequence[str],
    grouping_column_ids: typing.Sequence[str] = (),
) -> blocks.Block:

    original_columns = skew_column_ids
    column_labels = block.select_columns(original_columns).column_labels

    block, delta3_ids = _mean_delta_to_power(
        block, 3, original_columns, grouping_column_ids
    )
    # counts, moment3 for each column
    aggregations = []
    for i, col in enumerate(original_columns):
        count_agg = ex.UnaryAggregation(
            agg_ops.count_op,
            ex.deref(col),
        )
        moment3_agg = ex.UnaryAggregation(
            agg_ops.mean_op,
            ex.deref(delta3_ids[i]),
        )
        variance_agg = ex.UnaryAggregation(
            agg_ops.PopVarOp(),
            ex.deref(col),
        )
        aggregations.extend([count_agg, moment3_agg, variance_agg])

    block, agg_ids = block.aggregate(
        by_column_ids=grouping_column_ids, aggregations=aggregations
    )

    skew_ids = []
    for i, col in enumerate(original_columns):
        # Corresponds to order of aggregations in preceding loop
        count_id, moment3_id, var_id = agg_ids[i * 3 : (i * 3) + 3]
        block, skew_id = _skew_from_moments_and_count(
            block, count_id, moment3_id, var_id
        )
        skew_ids.append(skew_id)

    block = block.select_columns(skew_ids).with_column_labels(column_labels)
    if not grouping_column_ids:
        # When ungrouped, transpose result row into a series
        # perform transpose last, so as to not invalidate cache
        block, index_col = block.create_constant(None, None)
        block = block.set_index([index_col])
        return block.transpose(original_row_index=pd.Index([None]))
    return block


def kurt(
    block: blocks.Block,
    skew_column_ids: typing.Sequence[str],
    grouping_column_ids: typing.Sequence[str] = (),
) -> blocks.Block:
    original_columns = skew_column_ids
    column_labels = block.select_columns(original_columns).column_labels

    block, delta4_ids = _mean_delta_to_power(
        block, 4, original_columns, grouping_column_ids
    )
    # counts, moment4 for each column
    aggregations = []
    for i, col in enumerate(original_columns):
        count_agg = ex.UnaryAggregation(agg_ops.count_op, ex.deref(col))
        moment4_agg = ex.UnaryAggregation(agg_ops.mean_op, ex.deref(delta4_ids[i]))
        variance_agg = ex.UnaryAggregation(agg_ops.PopVarOp(), ex.deref(col))
        aggregations.extend([count_agg, moment4_agg, variance_agg])

    block, agg_ids = block.aggregate(
        by_column_ids=grouping_column_ids, aggregations=aggregations
    )

    kurt_ids = []
    for i, col in enumerate(original_columns):
        # Corresponds to order of aggregations in preceding loop
        count_id, moment4_id, var_id = agg_ids[i * 3 : (i * 3) + 3]
        block, kurt_id = _kurt_from_moments_and_count(
            block, count_id, moment4_id, var_id
        )
        kurt_ids.append(kurt_id)

    block = block.select_columns(kurt_ids).with_column_labels(column_labels)
    if not grouping_column_ids:
        # When ungrouped, transpose result row into a series
        # perform transpose last, so as to not invalidate cache
        block, index_col = block.create_constant(None, None)
        block = block.set_index([index_col])
        return block.transpose(original_row_index=pd.Index([None]))
    return block


def _mean_delta_to_power(
    block: blocks.Block,
    n_power: int,
    column_ids: typing.Sequence[str],
    grouping_column_ids: typing.Sequence[str],
) -> typing.Tuple[blocks.Block, typing.Sequence[str]]:
    """Calculate (x-mean(x))^n. Useful for calculating moment statistics such as skew and kurtosis."""
    window = windows.unbound(grouping_keys=tuple(grouping_column_ids))
    block, mean_ids = block.multi_apply_window_op(column_ids, agg_ops.mean_op, window)
    delta_ids = []
    for val_id, mean_val_id in zip(column_ids, mean_ids):
        delta = ops.sub_op.as_expr(val_id, mean_val_id)
        delta_power = ops.pow_op.as_expr(delta, ex.const(n_power))
        block, delta_power_id = block.project_expr(delta_power)
        delta_ids.append(delta_power_id)
    return block, delta_ids


def _skew_from_moments_and_count(
    block: blocks.Block, count_id: str, moment3_id: str, moment2_id: str
) -> typing.Tuple[blocks.Block, str]:
    # Calculate skew using count, third moment and population variance
    # See G1 estimator:
    # https://en.wikipedia.org/wiki/Skewness#Sample_skewness
    moments_estimator = ops.div_op.as_expr(
        moment3_id, ops.pow_op.as_expr(moment2_id, ex.const(3 / 2))
    )

    countminus1 = ops.sub_op.as_expr(count_id, ex.const(1))
    countminus2 = ops.sub_op.as_expr(count_id, ex.const(2))
    adjustment = ops.div_op.as_expr(
        ops.unsafe_pow_op.as_expr(
            ops.mul_op.as_expr(count_id, countminus1), ex.const(1 / 2)
        ),
        countminus2,
    )

    skew = ops.mul_op.as_expr(moments_estimator, adjustment)

    # Need to produce NA if have less than 3 data points
    cleaned_skew = ops.where_op.as_expr(
        skew, ops.ge_op.as_expr(count_id, ex.const(3)), ex.const(None)
    )
    return block.project_expr(cleaned_skew)


def _kurt_from_moments_and_count(
    block: blocks.Block, count_id: str, moment4_id: str, moment2_id: str
) -> typing.Tuple[blocks.Block, str]:
    # Kurtosis is often defined as the second standardize moment: moment(4)/moment(2)**2
    # Pandas however uses Fisher’s estimator, implemented below
    # numerator = (count + 1) * (count - 1) * moment4
    # denominator = (count - 2) * (count - 3) * moment2**2
    # adjustment = 3 * (count - 1) ** 2 / ((count - 2) * (count - 3))
    # kurtosis = (numerator / denominator) - adjustment

    numerator = ops.mul_op.as_expr(
        moment4_id,
        ops.mul_op.as_expr(
            ops.sub_op.as_expr(count_id, ex.const(1)),
            ops.add_op.as_expr(count_id, ex.const(1)),
        ),
    )

    # Denominator
    countminus2 = ops.sub_op.as_expr(count_id, ex.const(2))
    countminus3 = ops.sub_op.as_expr(count_id, ex.const(3))

    # Denominator
    denominator = ops.mul_op.as_expr(
        ops.unsafe_pow_op.as_expr(moment2_id, ex.const(2)),
        ops.mul_op.as_expr(countminus2, countminus3),
    )

    # Adjustment
    adj_num = ops.mul_op.as_expr(
        ops.unsafe_pow_op.as_expr(
            ops.sub_op.as_expr(count_id, ex.const(1)), ex.const(2)
        ),
        ex.const(3),
    )
    adj_denom = ops.mul_op.as_expr(countminus2, countminus3)
    adjustment = ops.div_op.as_expr(adj_num, adj_denom)

    # Combine
    kurt = ops.sub_op.as_expr(ops.div_op.as_expr(numerator, denominator), adjustment)

    # Need to produce NA if have less than 4 data points
    cleaned_kurt = ops.where_op.as_expr(
        kurt, ops.ge_op.as_expr(count_id, ex.const(4)), ex.const(None)
    )
    return block.project_expr(cleaned_kurt)


def align(
    left_block: blocks.Block,
    right_block: blocks.Block,
    join: str = "outer",
    axis: typing.Union[str, int, None] = None,
) -> typing.Tuple[blocks.Block, blocks.Block]:
    axis_n = core.utils.get_axis_number(axis) if axis is not None else None
    # Must align columns first as other way will likely create extra joins
    if (axis_n is None) or axis_n == 1:
        left_block, right_block = align_columns(left_block, right_block, join=join)
    if (axis_n is None) or axis_n == 0:
        left_block, right_block = align_rows(left_block, right_block, join=join)
    return left_block, right_block


def align_rows(
    left_block: blocks.Block,
    right_block: blocks.Block,
    join: str = "outer",
):
    joined_block, (get_column_left, get_column_right) = left_block.join(
        right_block, how=join
    )
    left_columns = [get_column_left[col] for col in left_block.value_columns]
    right_columns = [get_column_right[col] for col in right_block.value_columns]

    left_block = joined_block.select_columns(left_columns)
    right_block = joined_block.select_columns(right_columns)
    return left_block, right_block


def align_columns(
    left_block: blocks.Block,
    right_block: blocks.Block,
    join: str = "outer",
):
    columns, lcol_indexer, rcol_indexer = left_block.column_labels.join(
        right_block.column_labels, how=join, return_indexers=True
    )
    column_indices = zip(
        lcol_indexer if (lcol_indexer is not None) else range(len(columns)),
        rcol_indexer if (rcol_indexer is not None) else range(len(columns)),
    )
    left_column_ids = []
    right_column_ids = []

    original_left_block = left_block
    original_right_block = right_block

    for left_index, right_index in column_indices:
        if left_index >= 0:
            left_col_id = original_left_block.value_columns[left_index]
        else:
            dtype = right_block.dtypes[right_index]
            left_block, left_col_id = left_block.create_constant(
                None, dtype=dtype, label=original_right_block.column_labels[right_index]
            )
        left_column_ids.append(left_col_id)

        if right_index >= 0:
            right_col_id = original_right_block.value_columns[right_index]
        else:
            dtype = original_left_block.dtypes[left_index]
            right_block, right_col_id = right_block.create_constant(
                None, dtype=dtype, label=left_block.column_labels[left_index]
            )
        right_column_ids.append(right_col_id)
    left_final = left_block.select_columns(left_column_ids)
    right_final = right_block.select_columns(right_column_ids)
    return left_final, right_final


def idxmin(block: blocks.Block) -> blocks.Block:
    return _idx_extrema(block, "min")


def idxmax(block: blocks.Block) -> blocks.Block:
    return _idx_extrema(block, "max")


def _idx_extrema(
    block: blocks.Block, min_or_max: typing.Literal["min", "max"]
) -> blocks.Block:
    block._throw_if_null_index("idx")
    if len(block.index_columns) > 1:
        # TODO: Need support for tuple dtype
        raise NotImplementedError(
            f"idxmin not support for multi-index. {constants.FEEDBACK_LINK}"
        )

    original_block = block
    result_cols = []
    for value_col in original_block.value_columns:
        direction = (
            ordering.OrderingDirection.ASC
            if min_or_max == "min"
            else ordering.OrderingDirection.DESC
        )
        # Have to find the min for each
        order_refs = [
            ordering.OrderingExpression(ex.deref(value_col), direction),
            *[
                ordering.OrderingExpression(ex.deref(idx_col))
                for idx_col in original_block.index_columns
            ],
        ]
        window_spec = windows.unbound(ordering=tuple(order_refs))
        idx_col = original_block.index_columns[0]
        block, result_col = block.apply_window_op(
            idx_col, agg_ops.first_op, window_spec
        )
        result_cols.append(result_col)

    block = block.select_columns(result_cols).with_column_labels(
        original_block.column_labels
    )
    # Stack the entire column axis to produce single-column result
    # Assumption: uniform dtype for stackability
    return block.aggregate_all_and_stack(
        agg_ops.AnyValueOp(),
    ).with_column_labels([original_block.index.name])
