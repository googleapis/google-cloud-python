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

from typing import Literal, Optional

from bigframes.dataframe import DataFrame
from bigframes.series import Series


def merge(
    left: DataFrame,
    right: DataFrame,
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
) -> DataFrame:
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


def _validate_operand(obj: DataFrame | Series) -> DataFrame:
    if isinstance(obj, DataFrame):
        return obj
    elif isinstance(obj, Series):
        if obj.name is None:
            raise ValueError("Cannot merge a Series without a name")
        return obj.to_frame()
    else:
        raise TypeError(
            f"Can only merge Series or DataFrame objects, a {type(obj)} was passed"
        )
