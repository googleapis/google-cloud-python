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

import re
from typing import cast, Literal, Optional, Union

import bigframes.constants as constants
from bigframes.core import log_adapter
import bigframes.dataframe as df
import bigframes.operations as ops
import bigframes.operations.base
import bigframes.series as series
import third_party.bigframes_vendored.pandas.core.strings.accessor as vendorstr

# Maps from python to re2
REGEXP_FLAGS = {
    re.IGNORECASE: "i",
    re.MULTILINE: "m",
    re.DOTALL: "s",
}


@log_adapter.class_logger
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

    def isalpha(
        self,
    ) -> series.Series:
        return self._apply_unary_op(ops.isalpha_op)

    def isdigit(
        self,
    ) -> series.Series:
        return self._apply_unary_op(ops.isdigit_op)

    def isdecimal(
        self,
    ) -> series.Series:
        return self._apply_unary_op(ops.isdecimal_op)

    def isalnum(
        self,
    ) -> series.Series:
        return self._apply_unary_op(ops.isalnum_op)

    def isspace(
        self,
    ) -> series.Series:
        return self._apply_unary_op(ops.isspace_op)

    def islower(
        self,
    ) -> series.Series:
        return self._apply_unary_op(ops.islower_op)

    def isupper(
        self,
    ) -> series.Series:
        return self._apply_unary_op(ops.isupper_op)

    def rstrip(self) -> series.Series:
        return self._apply_unary_op(ops.rstrip_op)

    def lstrip(self) -> series.Series:
        return self._apply_unary_op(ops.lstrip_op)

    def repeat(self, repeats: int) -> series.Series:
        return self._apply_unary_op(ops.RepeatOp(repeats))

    def capitalize(self) -> series.Series:
        return self._apply_unary_op(ops.capitalize_op)

    def match(self, pat, case=True, flags=0) -> series.Series:
        # \A anchors start of entire string rather than start of any line in multiline mode
        adj_pat = rf"\A{pat}"
        return self.contains(adj_pat, case=case, flags=flags)

    def fullmatch(self, pat, case=True, flags=0) -> series.Series:
        # \A anchors start of entire string rather than start of any line in multiline mode
        # \z likewise anchors to the end of the entire multiline string
        adj_pat = rf"\A{pat}\z"
        return self.contains(adj_pat, case=case, flags=flags)

    def get(self, i: int) -> series.Series:
        return self._apply_unary_op(ops.StrGetOp(i))

    def pad(self, width, side="left", fillchar=" ") -> series.Series:
        return self._apply_unary_op(ops.StrPadOp(width, fillchar, side))

    def ljust(self, width, fillchar=" ") -> series.Series:
        return self._apply_unary_op(ops.StrPadOp(width, fillchar, "right"))

    def rjust(self, width, fillchar=" ") -> series.Series:
        return self._apply_unary_op(ops.StrPadOp(width, fillchar, "left"))

    def contains(
        self, pat, case: bool = True, flags: int = 0, *, regex: bool = True
    ) -> series.Series:
        if not case:
            return self.contains(pat, flags=flags | re.IGNORECASE, regex=True)
        if regex:
            re2flags = _parse_flags(flags)
            if re2flags:
                pat = re2flags + pat
            return self._apply_unary_op(ops.ContainsRegexOp(pat))
        else:
            return self._apply_unary_op(ops.ContainsStringOp(pat))

    def extract(self, pat: str, flags: int = 0) -> df.DataFrame:
        re2flags = _parse_flags(flags)
        if re2flags:
            pat = re2flags + pat
        compiled = re.compile(pat)
        if compiled.groups == 0:
            raise ValueError("No capture groups in 'pat'")

        results: list[str] = []
        block = self._block
        for i in range(compiled.groups):
            labels = [
                label
                for label, groupn in compiled.groupindex.items()
                if i + 1 == groupn
            ]
            label = labels[0] if labels else str(i)
            block, id = block.apply_unary_op(
                self._value_column, ops.ExtractOp(pat, i + 1), result_label=label
            )
            results.append(id)
        block = block.select_columns(results)
        return df.DataFrame(block)

    def replace(
        self,
        pat: Union[str, re.Pattern],
        repl: str,
        *,
        case: Optional[bool] = None,
        flags: int = 0,
        regex: bool = False,
    ) -> series.Series:
        is_compiled = isinstance(pat, re.Pattern)
        patstr = cast(str, pat.pattern if is_compiled else pat)  # type: ignore
        if case is False:
            return self.replace(pat, repl, flags=flags | re.IGNORECASE, regex=True)
        if regex:
            re2flags = _parse_flags(flags)
            if re2flags:
                patstr = re2flags + patstr
            return self._apply_unary_op(ops.ReplaceRegexOp(patstr, repl))
        else:
            if is_compiled:
                raise ValueError(
                    "Must set 'regex'=True if using compiled regex pattern."
                )
            return self._apply_unary_op(ops.ReplaceStringOp(patstr, repl))

    def startswith(
        self,
        pat: Union[str, tuple[str, ...]],
    ) -> series.Series:
        if not isinstance(pat, tuple):
            pat = (pat,)
        return self._apply_unary_op(ops.StartsWithOp(pat))

    def endswith(
        self,
        pat: Union[str, tuple[str, ...]],
    ) -> series.Series:
        if not isinstance(pat, tuple):
            pat = (pat,)
        return self._apply_unary_op(ops.EndsWithOp(pat))

    def zfill(self, width: int) -> series.Series:
        return self._apply_unary_op(ops.ZfillOp(width))

    def center(self, width: int, fillchar: str = " ") -> series.Series:
        return self._apply_unary_op(ops.StrPadOp(width, fillchar, "both"))

    def cat(
        self,
        others: Union[str, series.Series],
        *,
        join: Literal["outer", "left"] = "left",
    ) -> series.Series:
        return self._apply_binary_op(others, ops.concat_op, alignment=join)


def _parse_flags(flags: int) -> Optional[str]:
    re2flags = []
    for reflag, re2flag in REGEXP_FLAGS.items():
        if flags & flags:
            re2flags.append(re2flag)
            flags = flags ^ reflag

    # Remaining flags couldn't be mapped to re2 engine
    if flags:
        raise NotImplementedError(
            f"Could not handle RegexFlag: {flags}. {constants.FEEDBACK_LINK}"
        )

    if re2flags:
        return "(?" + "".join(re2flags) + ")"
    else:
        return None
