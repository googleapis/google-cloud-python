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

from typing import Literal, Optional, Union

import bigframes.operations as ops
import bigframes.operations.base
import bigframes.series as series
import third_party.bigframes_vendored.pandas.core.strings.accessor as vendorstr


class StringMethods(bigframes.operations.base.SeriesMethods, vendorstr.StringMethods):
    __doc__ = vendorstr.StringMethods.__doc__

    def find(
        self,
        sub: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> series.Series:
        return self._apply_unary_op(ops.FindOp(sub, start, end))

    def len(self) -> series.Series:
        return self._apply_unary_op(ops.len_op)

    def lower(self) -> series.Series:
        return self._apply_unary_op(ops.lower_op)

    def reverse(self) -> series.Series:
        """Reverse strings in the Series."""
        # reverse method is in ibis, not pandas.
        return self._apply_unary_op(ops.reverse_op)

    def slice(
        self,
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> series.Series:
        return self._apply_unary_op(ops.SliceOp(start, stop))

    def strip(self) -> series.Series:
        return self._apply_unary_op(ops.strip_op)

    def upper(self) -> series.Series:
        return self._apply_unary_op(ops.upper_op)

    def isnumeric(self) -> series.Series:
        return self._apply_unary_op(ops.isnumeric_op)

    def rstrip(self) -> series.Series:
        return self._apply_unary_op(ops.rstrip_op)

    def lstrip(self) -> series.Series:
        return self._apply_unary_op(ops.lstrip_op)

    def repeat(self, repeats: int) -> series.Series:
        return self._apply_unary_op(ops.RepeatOp(repeats))

    def capitalize(self) -> series.Series:
        return self._apply_unary_op(ops.capitalize_op)

    def cat(
        self,
        others: Union[str, series.Series],
        *,
        join: Literal["outer", "left"] = "left",
    ) -> series.Series:
        return self._apply_binary_op(others, ops.concat_op, alignment=join)
