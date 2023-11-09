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

import re

import pandas as pd
import pytest

import bigframes.series

from ...utils import assert_series_equal


def test_find(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.find("W").to_pandas()
    pd_result = scalars_pandas_df[col_name].str.find("W")

    # One of type mismatches to be documented. Here, the `bf_result.dtype` is `Int64` but
    # the `pd_result.dtype` is `float64`: https://github.com/pandas-dev/pandas/issues/51948
    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


@pytest.mark.parametrize(
    ("pat", "case", "flags", "regex"),
    [
        ("hEllo", True, 0, False),
        ("hEllo", False, 0, False),
        ("hEllo", False, re.I, True),
        (".*", True, 0, True),
        (".*", True, 0, False),
    ],
)
def test_str_contains(scalars_dfs, pat, case, flags, regex):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]

    bf_result = bf_series.str.contains(
        pat, case=case, flags=flags, regex=regex
    ).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.contains(
        pat, case=case, flags=flags, regex=regex
    )

    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("pat"),
    [(r"(ell)(lo)"), (r"(?P<somename>h..)"), (r"(?P<somename>e.*o)([g-l]+)")],
)
def test_str_extract(scalars_dfs, pat):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]

    bf_result = bf_series.str.extract(pat).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.extract(pat)

    # Pandas produces int col labels, while bq df only supports str labels at present
    pd_result = pd_result.set_axis(pd_result.columns.astype(str), axis=1)
    pd.testing.assert_frame_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("pat", "repl", "case", "flags", "regex"),
    [
        ("hEllo", "blah", True, 0, False),
        ("hEllo", "blah", False, 0, False),
        ("hEllo", "blah", False, re.I, True),
        (".*", "blah", True, 0, True),
        ("h.l", "blah", False, 0, True),
        (re.compile("(?i).e.."), "blah", None, 0, True),
    ],
)
def test_str_replace(scalars_dfs, pat, repl, case, flags, regex):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]

    bf_result = bf_series.str.replace(
        pat, repl=repl, case=case, flags=flags, regex=regex
    ).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.replace(
        pat, repl=repl, case=case, flags=flags, regex=regex
    )

    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("pat",),
    [
        ("こん",),
        ("Tag!",),
        (
            (
                "Tag!",
                "Hel",
            ),
        ),
    ],
)
def test_str_startswith(scalars_dfs, pat):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name].astype("object")

    bf_result = bf_series.str.startswith(pat).to_pandas()
    pd_result = pd_series.str.startswith(pat)

    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("pat",),
    [
        ("こん",),
        ("Tag!",),
        (
            (
                "Tag!",
                "Hel",
            ),
        ),
    ],
)
def test_str_endswith(scalars_dfs, pat):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name].astype("object")

    bf_result = bf_series.str.endswith(pat).to_pandas()
    pd_result = pd_series.str.endswith(pat)

    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


def test_len(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.len().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.len()

    # One of dtype mismatches to be documented. Here, the `bf_result.dtype` is `Int64` but
    # the `pd_result.dtype` is `float64`: https://github.com/pandas-dev/pandas/issues/51948
    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


def test_lower(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.lower().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.lower()

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_reverse(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.reverse().to_pandas()
    pd_result = scalars_pandas_df[col_name].copy()
    for i in pd_result.index:
        cell = pd_result.loc[i]
        if pd.isna(cell):
            pd_result.loc[i] = None
        else:
            pd_result.loc[i] = cell[::-1]

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ["start", "stop"], [(0, 1), (3, 5), (100, 101), (None, 1), (0, 12), (0, None)]
)
def test_slice(scalars_dfs, start, stop):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.slice(start, stop).to_pandas()
    pd_series = scalars_pandas_df[col_name]
    pd_result = pd_series.str.slice(start, stop)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_strip(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.strip().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.strip()

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_upper(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.upper().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.upper()

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_isnumeric(weird_strings, weird_strings_pd):
    pd_result = weird_strings_pd.str.isnumeric()
    bf_result = weird_strings.str.isnumeric().to_pandas()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_isalpha(weird_strings, weird_strings_pd):
    pd_result = weird_strings_pd.str.isalpha()
    bf_result = weird_strings.str.isalpha().to_pandas()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_isdigit(weird_strings, weird_strings_pd):
    pd_result = weird_strings_pd.str.isdigit()
    bf_result = weird_strings.str.isdigit().to_pandas()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_isdecimal(weird_strings, weird_strings_pd):
    pd_result = weird_strings_pd.str.isdecimal()
    bf_result = weird_strings.str.isdecimal().to_pandas()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_isalnum(weird_strings, weird_strings_pd):
    pd_result = weird_strings_pd.str.isalnum()
    bf_result = weird_strings.str.isalnum().to_pandas()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_isspace(weird_strings, weird_strings_pd):
    pd_result = weird_strings_pd.str.isspace()
    bf_result = weird_strings.str.isspace().to_pandas()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_islower(weird_strings, weird_strings_pd):
    pd_result = weird_strings_pd.str.islower()
    bf_result = weird_strings.str.islower().to_pandas()

    assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_isupper(weird_strings, weird_strings_pd):
    pd_result = weird_strings_pd.str.isupper()
    bf_result = weird_strings.str.isupper().to_pandas()

    assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_rstrip(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.rstrip().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.rstrip()

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_lstrip(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.lstrip().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.lstrip()

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(["repeats"], [(5,), (0,), (1,)])
def test_repeat(scalars_dfs, repeats):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.repeat(repeats).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.repeat(repeats)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_capitalize(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.capitalize().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.capitalize()

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_cat_with_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_filter: bigframes.series.Series = scalars_df["bool_col"]
    bf_left: bigframes.series.Series = scalars_df[col_name][bf_filter]
    bf_right: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_left.str.cat(others=bf_right).to_pandas()
    pd_filter = scalars_pandas_df["bool_col"]
    pd_left = scalars_pandas_df[col_name][pd_filter]
    pd_right = scalars_pandas_df[col_name]
    pd_result = pd_left.str.cat(others=pd_right)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_match(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    pattern = "[A-Z].*"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.match(pattern).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.match(pattern)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_fullmatch(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    pattern = "[A-Z].*!"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.fullmatch(pattern).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.fullmatch(pattern)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_get(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.get(8).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.get(8)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_pad(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.pad(8, side="both", fillchar="%").to_pandas()
    pd_result = scalars_pandas_df[col_name].str.pad(8, side="both", fillchar="%")

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_zfill(weird_strings, weird_strings_pd):
    bf_result = weird_strings.str.zfill(5).to_pandas()
    pd_result = weird_strings_pd.str.zfill(5)

    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_ljust(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.ljust(7, fillchar="%").to_pandas()
    pd_result = scalars_pandas_df[col_name].str.ljust(7, fillchar="%")

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_rjust(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.rjust(9, fillchar="%").to_pandas()
    pd_result = scalars_pandas_df[col_name].str.rjust(9, fillchar="%")

    assert_series_equal(
        pd_result,
        bf_result,
    )
