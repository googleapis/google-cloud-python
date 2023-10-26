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
from typing import Iterable, Literal, Optional, Union

import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.utils as utils
import bigframes.dataframe
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.series


@typing.overload
def concat(
    objs: Iterable[bigframes.series.Series],
    *,
    axis: typing.Literal["index", 0] = ...,
    join=...,
    ignore_index=...,
) -> bigframes.series.Series:
    ...


@typing.overload
def concat(
    objs: Iterable[bigframes.dataframe.DataFrame],
    *,
    axis: typing.Literal["index", 0] = ...,
    join=...,
    ignore_index=...,
) -> bigframes.dataframe.DataFrame:
    ...


@typing.overload
def concat(
    objs: Iterable[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]],
    *,
    axis: typing.Literal["columns", 1],
    join=...,
    ignore_index=...,
) -> bigframes.dataframe.DataFrame:
    ...


@typing.overload
def concat(
    objs: Iterable[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]],
    *,
    axis=...,
    join=...,
    ignore_index=...,
) -> Union[bigframes.dataframe.DataFrame, bigframes.series.Series]:
    ...


def concat(
    objs: Iterable[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]],
    *,
    axis: typing.Union[str, int] = 0,
    join: Literal["inner", "outer"] = "outer",
    ignore_index: bool = False,
) -> Union[bigframes.dataframe.DataFrame, bigframes.series.Series]:
    axis_n = utils.get_axis_number(axis)
    if axis_n == 0:
        contains_dataframes = any(
            isinstance(x, bigframes.dataframe.DataFrame) for x in objs
        )
        if not contains_dataframes:
            # Special case, all series, so align everything into single column even if labels don't match
            series = typing.cast(typing.Iterable[bigframes.series.Series], objs)
            names = {s.name for s in series}
            # For series case, labels are stripped if they don't all match
            if len(names) > 1:
                blocks = [s._block.with_column_labels([None]) for s in series]
            else:
                blocks = [s._block for s in series]
            block = blocks[0].concat(blocks[1:], how=join, ignore_index=ignore_index)
            return bigframes.series.Series(block)
        blocks = [obj._block for obj in objs]
        block = blocks[0].concat(blocks[1:], how=join, ignore_index=ignore_index)
        return bigframes.dataframe.DataFrame(block)
    else:
        # Note: does not validate inputs
        block_list = [obj._block for obj in objs]
        block = block_list[0]
        for rblock in block_list[1:]:
            combined_index, _ = block.index.join(rblock.index, how=join)
            block = combined_index._block
        return bigframes.dataframe.DataFrame(block)


def cut(
    x: bigframes.series.Series,
    bins: int,
    *,
    labels: Optional[bool] = None,
) -> bigframes.series.Series:
    if bins <= 0:
        raise ValueError("`bins` should be a positive integer.")

    if labels is not False:
        raise NotImplementedError(
            f"Only labels=False is supported in BigQuery DataFrames so far. {constants.FEEDBACK_LINK}"
        )
    return x._apply_window_op(agg_ops.CutOp(bins), window_spec=core.WindowSpec())


def qcut(
    x: bigframes.series.Series,
    q: typing.Union[int, typing.Sequence[float]],
    *,
    labels: Optional[bool] = None,
    duplicates: typing.Literal["drop", "error"] = "error",
) -> bigframes.series.Series:
    if isinstance(q, int) and q <= 0:
        raise ValueError("`q` should be a positive integer.")

    if labels is not False:
        raise NotImplementedError(
            f"Only labels=False is supported in BigQuery DataFrames so far. {constants.FEEDBACK_LINK}"
        )
    if duplicates != "drop":
        raise NotImplementedError(
            f"Only duplicates='drop' is supported in BigQuery DataFrames so far. {constants.FEEDBACK_LINK}"
        )
    block = x._block
    label = block.col_id_to_label[x._value_column]
    block, nullity_id = block.apply_unary_op(x._value_column, ops.notnull_op)
    block, result = block.apply_window_op(
        x._value_column,
        agg_ops.QcutOp(q),
        window_spec=core.WindowSpec(grouping_keys=(nullity_id,)),
    )
    block, result = block.apply_binary_op(
        result, nullity_id, ops.partial_arg3(ops.where_op, None), result_label=label
    )
    return bigframes.series.Series(block.select_column(result))
