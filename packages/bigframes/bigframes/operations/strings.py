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
from typing import Literal, Optional, Union

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.core.strings.accessor as vendorstr

from bigframes.core import log_adapter
import bigframes.dataframe as df
import bigframes.operations as ops
from bigframes.operations._op_converters import convert_index, convert_slice
import bigframes.operations.base
import bigframes.series as series

# Maps from python to re2
REGEXP_FLAGS = {
    re.IGNORECASE: "i",
    re.MULTILINE: "m",
    re.DOTALL: "s",
}


@log_adapter.class_logger
class StringMethods(bigframes.operations.base.SeriesMethods, vendorstr.StringMethods):
    __doc__ = vendorstr.StringMethods.__doc__

    def __getitem__(self, key: Union[int, slice]) -> series.Series:
        if isinstance(key, int):
            return self._apply_unary_op(convert_index(key))
        elif isinstance(key, slice):
            return self._apply_unary_op(convert_slice(key))
        else:
            raise ValueError(f"key must be an int or slice, got {type(key).__name__}")

    def find(
        self,
        sub: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> series.Series:
        return self._apply_unary_op(ops.StrFindOp(substr=sub, start=start, end=end))

    def len(self) -> series.Series:
        return self._apply_unary_op(ops.len_op)

    def lower(self) -> series.Series:
        return self._apply_unary_op(ops.lower_op)

    def reverse(self) -> series.Series:
        """Reverse strings in the Series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(["apple", "banana", "", bpd.NA])
            >>> s.str.reverse()
            0     elppa
            1    ananab
            2
            3      <NA>
            dtype: string

        Returns:
            bigframes.series.Series: A Series of booleans indicating whether the given
                pattern matches the start of each string element.
        """
        # reverse method is in ibis, not pandas.
        return self._apply_unary_op(ops.reverse_op)

    def slice(
        self,
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> series.Series:
        return self._apply_unary_op(ops.StrSliceOp(start=start, end=stop))

    def strip(self, to_strip: Optional[str] = None) -> series.Series:
        return self._apply_unary_op(
            ops.StrStripOp(to_strip=" \n\t" if to_strip is None else to_strip)
        )

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

    def rstrip(self, to_strip: Optional[str] = None) -> series.Series:
        return self._apply_unary_op(
            ops.StrRstripOp(to_strip=" \n\t" if to_strip is None else to_strip)
        )

    def lstrip(self, to_strip: Optional[str] = None) -> series.Series:
        return self._apply_unary_op(
            ops.StrLstripOp(to_strip=" \n\t" if to_strip is None else to_strip)
        )

    def repeat(self, repeats: int) -> series.Series:
        return self._apply_unary_op(ops.StrRepeatOp(repeats=repeats))

    def capitalize(self) -> series.Series:
        return self._apply_unary_op(ops.capitalize_op)

    def match(self, pat, case=True, flags=0) -> series.Series:
        # \A anchors start of entire string rather than start of any line in multiline mode
        adj_pat = rf"\A{pat}"
        return self.contains(pat=adj_pat, case=case, flags=flags)

    def fullmatch(self, pat, case=True, flags=0) -> series.Series:
        # \A anchors start of entire string rather than start of any line in multiline mode
        # \z likewise anchors to the end of the entire multiline string
        adj_pat = rf"\A{pat}\z"
        return self.contains(pat=adj_pat, case=case, flags=flags)

    def get(self, i: int) -> series.Series:
        return self._apply_unary_op(ops.StrGetOp(i=i))

    def pad(self, width, side="left", fillchar=" ") -> series.Series:
        return self._apply_unary_op(
            ops.StrPadOp(length=width, fillchar=fillchar, side=side)
        )

    def ljust(self, width, fillchar=" ") -> series.Series:
        return self._apply_unary_op(
            ops.StrPadOp(length=width, fillchar=fillchar, side="right")
        )

    def rjust(self, width, fillchar=" ") -> series.Series:
        return self._apply_unary_op(
            ops.StrPadOp(length=width, fillchar=fillchar, side="left")
        )

    def contains(
        self, pat, case: bool = True, flags: int = 0, *, regex: bool = True
    ) -> series.Series:
        if not case:
            return self.contains(pat=pat, flags=flags | re.IGNORECASE, regex=True)
        if regex:
            re2flags = _parse_flags(flags)
            if re2flags:
                pat = re2flags + pat
            return self._apply_unary_op(ops.StrContainsRegexOp(pat=pat))
        else:
            return self._apply_unary_op(ops.StrContainsOp(pat=pat))

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
                self._value_column,
                ops.StrExtractOp(pat=pat, n=i + 1),
                result_label=label,
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
        if isinstance(pat, re.Pattern):
            assert isinstance(pat.pattern, str)
            pat_str = pat.pattern
            flags = pat.flags | flags
        else:
            pat_str = pat

        if case is False:
            return self.replace(pat_str, repl, flags=flags | re.IGNORECASE, regex=True)
        if regex:
            re2flags = _parse_flags(flags)
            if re2flags:
                pat_str = re2flags + pat_str
            return self._apply_unary_op(ops.RegexReplaceStrOp(pat=pat_str, repl=repl))
        else:
            if isinstance(pat, re.Pattern):
                raise ValueError(
                    "Must set 'regex'=True if using compiled regex pattern."
                )
            return self._apply_unary_op(ops.ReplaceStrOp(pat=pat_str, repl=repl))

    def startswith(
        self,
        pat: Union[str, tuple[str, ...]],
    ) -> series.Series:
        if not isinstance(pat, tuple):
            pat = (pat,)
        return self._apply_unary_op(ops.StartsWithOp(pat=pat))

    def endswith(
        self,
        pat: Union[str, tuple[str, ...]],
    ) -> series.Series:
        if not isinstance(pat, tuple):
            pat = (pat,)
        return self._apply_unary_op(ops.EndsWithOp(pat=pat))

    def split(
        self,
        pat: str = " ",
        regex: Union[bool, None] = None,
    ) -> series.Series:
        if regex is True or (regex is None and len(pat) > 1):
            raise NotImplementedError(
                "Regular expressions aren't currently supported. Please set "
                + f"`regex=False` and try again. {constants.FEEDBACK_LINK}"
            )
        return self._apply_unary_op(ops.StringSplitOp(pat=pat))

    def zfill(self, width: int) -> series.Series:
        return self._apply_unary_op(ops.ZfillOp(width=width))

    def center(self, width: int, fillchar: str = " ") -> series.Series:
        return self._apply_unary_op(
            ops.StrPadOp(length=width, fillchar=fillchar, side="both")
        )

    def cat(
        self,
        others: Union[str, series.Series],
        *,
        join: Literal["outer", "left"] = "left",
    ) -> series.Series:
        return self._apply_binary_op(others, ops.strconcat_op, alignment=join)

    def to_blob(self, connection: Optional[str] = None) -> series.Series:
        """Create a BigFrames Blob series from a series of URIs.

        .. note::
            BigFrames Blob is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
            Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
            and might have limited support. For more information, see the launch stage descriptions
            (https://cloud.google.com/products#product-launch-stages).


        Args:
            connection (str or None, default None):
                Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
                If None, use default connection in session context. BigQuery DataFrame will try to create the connection and attach
                permission if the connection isn't fully set up.

        Returns:
            bigframes.series.Series: Blob Series.

        """
        session = self._block.session
        connection = session._create_bq_connection(connection=connection)
        return self._apply_binary_op(connection, ops.obj_make_ref_op)


def _parse_flags(flags: int) -> Optional[str]:
    re2flags = []
    for reflag, re2flag in REGEXP_FLAGS.items():
        if flags & reflag:
            re2flags.append(re2flag)
            flags = flags ^ reflag

    # re2 handles unicode fine by default
    # most compiled re in python will have unicode set
    if re.U and flags:
        flags = flags ^ re.U

    # Remaining flags couldn't be mapped to re2 engine
    if flags:
        raise NotImplementedError(
            f"Could not handle RegexFlag: {flags}. {constants.FEEDBACK_LINK}"
        )

    if re2flags:
        return "(?" + "".join(re2flags) + ")"
    else:
        return None
