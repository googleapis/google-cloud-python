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

from bigframes_vendored import constants
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
    left_index: bool = False,
    right_index: bool = False,
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

    left_join_ids, right_join_ids = _validate_left_right_on(
        left,
        right,
        on,
        left_on=left_on,
        right_on=right_on,
        left_index=left_index,
        right_index=right_index,
    )

    block = left._block.merge(
        right._block,
        how,
        left_join_ids,
        right_join_ids,
        sort=sort,
        suffixes=suffixes,
        left_index=left_index,
        right_index=right_index,
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
    left_index: bool = False,
    right_index: bool = False,
) -> tuple[list[str], list[str]]:
    # Turn left_on and right_on to lists
    if left_on is not None and not isinstance(left_on, (tuple, list)):
        left_on = [left_on]
    if right_on is not None and not isinstance(right_on, (tuple, list)):
        right_on = [right_on]

    if left_index and left.index.nlevels > 1:
        raise ValueError(
            f"Joining with multi-level index is not supported. {constants.FEEDBACK_LINK}"
        )
    if right_index and right.index.nlevels > 1:
        raise ValueError(
            f"Joining with multi-level index is not supported. {constants.FEEDBACK_LINK}"
        )

    # The following checks are copied from Pandas.
    if on is None and left_on is None and right_on is None:
        if left_index and right_index:
            return list(left._block.index_columns), list(right._block.index_columns)
        elif left_index:
            raise ValueError("Must pass right_on or right_index=True")
        elif right_index:
            raise ValueError("Must pass left_on or left_index=True")
        else:
            # use the common columns
            common_cols = left.columns.intersection(right.columns)
            if len(common_cols) == 0:
                raise ValueError(
                    "No common columns to perform merge on. "
                    f"Merge options: left_on={left_on}, "
                    f"right_on={right_on}, "
                    f"left_index={left_index}, "
                    f"right_index={right_index}"
                )
            if (
                not left.columns.join(common_cols, how="inner").is_unique
                or not right.columns.join(common_cols, how="inner").is_unique
            ):
                raise ValueError(f"Data columns not unique: {repr(common_cols)}")
            return _to_col_ids(left, common_cols.to_list()), _to_col_ids(
                right, common_cols.to_list()
            )

    elif on is not None:
        if left_on is not None or right_on is not None:
            raise ValueError(
                'Can only pass argument "on" OR "left_on" '
                'and "right_on", not a combination of both.'
            )
        if left_index or right_index:
            raise ValueError(
                'Can only pass argument "on" OR "left_index" '
                'and "right_index", not a combination of both.'
            )
        return _to_col_ids(left, on), _to_col_ids(right, on)

    elif left_on is not None:
        if left_index:
            raise ValueError(
                'Can only pass argument "left_on" OR "left_index" not both.'
            )
        if not right_index and right_on is None:
            raise ValueError('Must pass "right_on" OR "right_index".')
        if right_index:
            if len(left_on) != right.index.nlevels:
                raise ValueError(
                    "len(left_on) must equal the number "
                    'of levels in the index of "right"'
                )
            return _to_col_ids(left, left_on), list(right._block.index_columns)

    elif right_on is not None:
        if right_index:
            raise ValueError(
                'Can only pass argument "right_on" OR "right_index" not both.'
            )
        if not left_index and left_on is None:
            raise ValueError('Must pass "left_on" OR "left_index".')
        if left_index:
            if len(right_on) != left.index.nlevels:
                raise ValueError(
                    "len(right_on) must equal the number "
                    'of levels in the index of "left"'
                )
            return list(left._block.index_columns), _to_col_ids(right, right_on)

    # The user correctly specified left_on and right_on
    if len(right_on) != len(left_on):  # type: ignore
        raise ValueError("len(right_on) must equal len(left_on)")

    return _to_col_ids(left, left_on), _to_col_ids(right, right_on)


def _to_col_ids(
    df: dataframe.DataFrame, join_cols: blocks.Label | Sequence[blocks.Label]
) -> list[str]:
    if utils.is_list_like(join_cols):
        return [df._block.resolve_label_exact_or_error(col) for col in join_cols]

    return [df._block.resolve_label_exact_or_error(join_cols)]
