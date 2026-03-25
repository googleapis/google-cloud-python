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

import typing

import pandas as pd

from bigframes import dataframe, dtypes, series
from bigframes.core import agg_expressions, blocks
from bigframes.operations import aggregations

_DEFAULT_DTYPES = (
    dtypes.NUMERIC_BIGFRAMES_TYPES_RESTRICTIVE + dtypes.TEMPORAL_NUMERIC_BIGFRAMES_TYPES
)


def describe(
    input: dataframe.DataFrame | series.Series,
    include: None | typing.Literal["all"],
) -> dataframe.DataFrame | series.Series:
    if isinstance(input, series.Series):
        # Convert the series to a dataframe, describe it, and cast the result back to a series.
        return series.Series(describe(input.to_frame(), include)._block)
    elif not isinstance(input, dataframe.DataFrame):
        raise TypeError(f"Unsupported type: {type(input)}")

    block = input._block

    describe_block = _describe(block, columns=block.value_columns, include=include)
    # we override default stack behavior, because we want very specific ordering
    stack_cols = pd.Index(
        [
            "count",
            "nunique",
            "top",
            "freq",
            "mean",
            "std",
            "min",
            "25%",
            "50%",
            "75%",
            "max",
        ]
    ).intersection(describe_block.column_labels.get_level_values(-1))
    describe_block = describe_block.stack(override_labels=stack_cols)

    return dataframe.DataFrame(describe_block).droplevel(level=0)


def _describe(
    block: blocks.Block,
    columns: typing.Sequence[str],
    include: None | typing.Literal["all"] = None,
    *,
    as_index: bool = True,
    by_col_ids: typing.Sequence[str] = [],
    dropna: bool = False,
) -> blocks.Block:
    stats: list[agg_expressions.Aggregation] = []
    column_labels: list[typing.Hashable] = []

    # include=None behaves like include='all' if no numeric columns present
    if include is None:
        if not any(
            block.expr.get_column_type(col) in _DEFAULT_DTYPES for col in columns
        ):
            include = "all"

    for col_id in columns:
        label = block.col_id_to_label[col_id]
        dtype = block.expr.get_column_type(col_id)
        if include != "all" and dtype not in _DEFAULT_DTYPES:
            continue
        agg_ops = _get_aggs_for_dtype(dtype)
        stats.extend(op.as_expr(col_id) for op in agg_ops)
        label_tuple = (label,) if block.column_labels.nlevels == 1 else label
        column_labels.extend((*label_tuple, op.name) for op in agg_ops)  # type: ignore

    agg_block = block.aggregate(
        by_column_ids=by_col_ids,
        aggregations=stats,
        dropna=dropna,
        column_labels=pd.Index(column_labels, name=(*block.column_labels.names, None)),
    )
    return agg_block if as_index else agg_block.reset_index(drop=False)


def _get_aggs_for_dtype(dtype) -> list[aggregations.UnaryAggregateOp]:
    if dtype in dtypes.NUMERIC_BIGFRAMES_TYPES_RESTRICTIVE:
        return [
            aggregations.count_op,
            aggregations.mean_op,
            aggregations.std_op,
            aggregations.min_op,
            aggregations.ApproxQuartilesOp(1),
            aggregations.ApproxQuartilesOp(2),
            aggregations.ApproxQuartilesOp(3),
            aggregations.max_op,
        ]
    elif dtype in dtypes.TEMPORAL_NUMERIC_BIGFRAMES_TYPES:
        return [aggregations.count_op]
    elif dtype in [
        dtypes.STRING_DTYPE,
        dtypes.BOOL_DTYPE,
        dtypes.BYTES_DTYPE,
        dtypes.TIME_DTYPE,
    ]:
        return [aggregations.count_op, aggregations.nunique_op]
    else:
        return []
