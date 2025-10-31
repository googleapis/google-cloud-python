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

"""
Functions for Merging Data Structures in BigFrames.
"""

from __future__ import annotations

from typing import Literal, Sequence

import bigframes_vendored.pandas.core.reshape.merge as vendored_pandas_merge

from bigframes import dataframe, series
from bigframes.core import blocks, utils


def merge(
    left: dataframe.DataFrame,
    right: dataframe.DataFrame,
    how: Literal[
        "inner",
        "left",
        "outer",
        "right",
        "cross",
    ] = "inner",
    on: blocks.Label | Sequence[blocks.Label] | None = None,
    *,
    left_on: blocks.Label | Sequence[blocks.Label] | None = None,
    right_on: blocks.Label | Sequence[blocks.Label] | None = None,
    sort: bool = False,
    suffixes: tuple[str, str] = ("_x", "_y"),
) -> dataframe.DataFrame:
    left = _validate_operand(left)
    right = _validate_operand(right)

    if how == "cross":
        if on is not None:
            raise ValueError("'on' is not supported for cross join.")
        result_block = left._block.merge(
            right._block,
            left_join_ids=[],
            right_join_ids=[],
            suffixes=suffixes,
            how=how,
            sort=True,
        )
        return dataframe.DataFrame(result_block)

    left_on, right_on = _validate_left_right_on(
        left, right, on, left_on=left_on, right_on=right_on
    )

    if utils.is_list_like(left_on):
        left_on = list(left_on)  # type: ignore
    else:
        left_on = [left_on]

    if utils.is_list_like(right_on):
        right_on = list(right_on)  # type: ignore
    else:
        right_on = [right_on]

    left_join_ids = []
    for label in left_on:  # type: ignore
        left_col_id = left._resolve_label_exact(label)
        # 0 elements already throws an exception
        if not left_col_id:
            raise ValueError(f"No column {label} found in self.")
        left_join_ids.append(left_col_id)

    right_join_ids = []
    for label in right_on:  # type: ignore
        right_col_id = right._resolve_label_exact(label)
        if not right_col_id:
            raise ValueError(f"No column {label} found in other.")
        right_join_ids.append(right_col_id)

    block = left._block.merge(
        right._block,
        how,
        left_join_ids,
        right_join_ids,
        sort=sort,
        suffixes=suffixes,
    )
    return dataframe.DataFrame(block)


merge.__doc__ = vendored_pandas_merge.merge.__doc__


def _validate_operand(
    obj: dataframe.DataFrame | series.Series,
) -> dataframe.DataFrame:
    import bigframes.dataframe
    import bigframes.series

    if isinstance(obj, bigframes.dataframe.DataFrame):
        return obj
    elif isinstance(obj, bigframes.series.Series):
        if obj.name is None:
            raise ValueError("Cannot merge a bigframes.series.Series without a name")
        return obj.to_frame()
    else:
        raise TypeError(
            f"Can only merge bigframes.series.Series or bigframes.dataframe.DataFrame objects, a {type(obj)} was passed"
        )


def _validate_left_right_on(
    left: dataframe.DataFrame,
    right: dataframe.DataFrame,
    on: blocks.Label | Sequence[blocks.Label] | None = None,
    *,
    left_on: blocks.Label | Sequence[blocks.Label] | None = None,
    right_on: blocks.Label | Sequence[blocks.Label] | None = None,
):
    if on is not None:
        if left_on is not None or right_on is not None:
            raise ValueError(
                "Can not pass both `on` and `left_on` + `right_on` params."
            )
        return on, on

    if left_on is not None and right_on is not None:
        return left_on, right_on

    left_cols = left.columns
    right_cols = right.columns
    common_cols = left_cols.intersection(right_cols)
    if len(common_cols) == 0:
        raise ValueError(
            "No common columns to perform merge on."
            f"Merge options: left_on={left_on}, "
            f"right_on={right_on}, "
        )
    if (
        not left_cols.join(common_cols, how="inner").is_unique
        or not right_cols.join(common_cols, how="inner").is_unique
    ):
        raise ValueError(f"Data columns not unique: {repr(common_cols)}")

    return common_cols, common_cols
