# Copyright 2024 Google LLC
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
from typing import Iterable, Literal, Union

import bigframes_vendored.pandas.core.reshape.concat as vendored_pandas_concat

import bigframes.core.utils as utils
import bigframes.dataframe
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
            block, _ = block.join(rblock, how=join)
        return bigframes.dataframe.DataFrame(block)


concat.__doc__ = vendored_pandas_concat.concat.__doc__
