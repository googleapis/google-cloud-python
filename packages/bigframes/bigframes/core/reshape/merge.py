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

import typing
from typing import Literal, Optional

import bigframes_vendored.pandas.core.reshape.merge as vendored_pandas_merge

# Avoid cirular imports.
if typing.TYPE_CHECKING:
    import bigframes.dataframe
    import bigframes.series


def merge(
    left: bigframes.dataframe.DataFrame,
    right: bigframes.dataframe.DataFrame,
    how: Literal[
        "inner",
        "left",
        "outer",
        "right",
        "cross",
    ] = "inner",
    on: Optional[str] = None,
    *,
    left_on: Optional[str] = None,
    right_on: Optional[str] = None,
    sort: bool = False,
    suffixes: tuple[str, str] = ("_x", "_y"),
) -> bigframes.dataframe.DataFrame:
    left = _validate_operand(left)
    right = _validate_operand(right)

    return left.merge(
        right,
        how=how,
        on=on,
        left_on=left_on,
        right_on=right_on,
        sort=sort,
        suffixes=suffixes,
    )


merge.__doc__ = vendored_pandas_merge.merge.__doc__


def _validate_operand(
    obj: bigframes.dataframe.DataFrame | bigframes.series.Series,
) -> bigframes.dataframe.DataFrame:
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
