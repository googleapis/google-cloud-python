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
import pyarrow as pa
import pytest

import bigframes.dtypes as dtypes
import bigframes.pandas as bpd
from bigframes.testing.utils import assert_series_equal


def test_find(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
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
    bf_series: bpd.Series = scalars_df[col_name]

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
    bf_series: bpd.Series = scalars_df[col_name]

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
        ("H", "h", True, 0, False),
        (", ", "__", True, 0, False),
        (re.compile(r"hEllo", flags=re.I), "blah", None, 0, True),
    ],
)
def test_str_replace(scalars_dfs, pat, repl, case, flags, regex):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]

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
    bf_series: bpd.Series = scalars_df[col_name]
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
    bf_series: bpd.Series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name].astype("object")

    bf_result = bf_series.str.endswith(pat).to_pandas()
    pd_result = pd_series.str.endswith(pat)

    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


def test_len(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.len().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.len()

    # One of dtype mismatches to be documented. Here, the `bf_result.dtype` is `Int64` but
    # the `pd_result.dtype` is `float64`: https://github.com/pandas-dev/pandas/issues/51948
    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


def test_len_with_array_column(nested_df, nested_pandas_df):
    """
    Series.str.len() is expected to work on columns containing lists as well as strings.

    See: https://stackoverflow.com/a/41340543/101923
    """
    col_name = "event_sequence"
    bf_series: bpd.Series = nested_df[col_name]
    bf_result = bf_series.str.len().to_pandas()
    pd_result = nested_pandas_df[col_name].str.len()

    # One of dtype mismatches to be documented. Here, the `bf_result.dtype` is `Int64` but
    # the `pd_result.dtype` is `float64`: https://github.com/pandas-dev/pandas/issues/51948
    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
        check_index_type=False,
    )


def test_lower(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.lower().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.lower()

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_reverse(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
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
    bf_series: bpd.Series = scalars_df[col_name]
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
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.strip().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.strip()

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("to_strip"),
    [
        pytest.param(None, id="none"),
        pytest.param(" ", id="space"),
        pytest.param(" \n", id="space_newline"),
        pytest.param("123.!? \n\t", id="multiple_chars"),
    ],
)
def test_strip_w_to_strip(to_strip):
    s = bpd.Series(["1. Ant.  ", "2. Bee!\n", "3. Cat?\t", bpd.NA])
    pd_s = s.to_pandas()

    bf_result = s.str.strip(to_strip=to_strip).to_pandas()
    pd_result = pd_s.str.strip(to_strip=to_strip)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_upper(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
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


@pytest.mark.skipif(
    "dev" in pa.__version__,
    # b/333484335 pyarrow is inconsistent on the behavior
    reason="pyarrow dev version is inconsistent on isdigit behavior.",
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
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.rstrip().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.rstrip()

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("to_strip"),
    [
        pytest.param(None, id="none"),
        pytest.param(" ", id="space"),
        pytest.param(" \n", id="space_newline"),
        pytest.param("123.!? \n\t", id="multiple_chars"),
    ],
)
def test_rstrip_w_to_strip(to_strip):
    s = bpd.Series(["1. Ant.  ", "2. Bee!\n", "3. Cat?\t", bpd.NA])
    pd_s = s.to_pandas()

    bf_result = s.str.rstrip(to_strip=to_strip).to_pandas()
    pd_result = pd_s.str.rstrip(to_strip=to_strip)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_lstrip(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.lstrip().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.lstrip()

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("to_strip"),
    [
        pytest.param(None, id="none"),
        pytest.param(" ", id="space"),
        pytest.param(" \n", id="space_newline"),
        pytest.param("123.!? \n\t", id="multiple_chars"),
    ],
)
def test_lstrip_w_to_strip(to_strip):
    s = bpd.Series(["1. Ant.  ", "2. Bee!\n", "3. Cat?\t", bpd.NA])
    pd_s = s.to_pandas()

    bf_result = s.str.lstrip(to_strip=to_strip).to_pandas()
    pd_result = pd_s.str.lstrip(to_strip=to_strip)

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(["repeats"], [(5,), (0,), (1,)])
def test_repeat(scalars_dfs, repeats):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.repeat(repeats).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.repeat(repeats)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_capitalize(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.capitalize().to_pandas()
    pd_result = scalars_pandas_df[col_name].str.capitalize()

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_cat_with_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_filter: bpd.Series = scalars_df["bool_col"]
    bf_left: bpd.Series = scalars_df[col_name][bf_filter]
    bf_right: bpd.Series = scalars_df[col_name]
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
    bf_series: bpd.Series = scalars_df[col_name]
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
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.fullmatch(pattern).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.fullmatch(pattern)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_get(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.get(8).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.get(8)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_pad(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
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
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.ljust(7, fillchar="%").to_pandas()
    pd_result = scalars_pandas_df[col_name].str.ljust(7, fillchar="%")

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_str_rjust(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bpd.Series = scalars_df[col_name]
    bf_result = bf_series.str.rjust(9, fillchar="%").to_pandas()
    pd_result = scalars_pandas_df[col_name].str.rjust(9, fillchar="%")

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("pat", "regex"),
    [
        pytest.param(" ", None, id="one_char"),
        pytest.param("ll", False, id="two_chars"),
        pytest.param(
            " ",
            True,
            id="one_char_reg",
            marks=pytest.mark.xfail(raises=NotImplementedError),
        ),
        pytest.param(
            "ll",
            None,
            id="two_chars_reg",
            marks=pytest.mark.xfail(raises=NotImplementedError),
        ),
    ],
)
def test_str_split_raise_errors(scalars_dfs, pat, regex):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = scalars_df[col_name].str.split(pat=pat, regex=regex).to_pandas()
    pd_result = scalars_pandas_df[col_name].str.split(pat=pat, regex=regex)

    # TODO(b/336880368): Allow for NULL values for ARRAY columns in BigQuery.
    pd_result = pd_result.apply(lambda x: [] if pd.isnull(x) is True else x)

    assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("index"),
    [
        pytest.param(
            "first", id="invalid_type", marks=pytest.mark.xfail(raises=ValueError)
        ),
        pytest.param(
            -1, id="neg_index", marks=pytest.mark.xfail(raises=NotImplementedError)
        ),
        pytest.param(
            slice(0, 2, 2),
            id="only_allow_one_step",
            marks=pytest.mark.xfail(raises=NotImplementedError),
        ),
        pytest.param(
            slice(-1, None, None),
            id="neg_slicing",
            marks=pytest.mark.xfail(raises=NotImplementedError),
        ),
    ],
)
def test_getitem_raise_errors(scalars_dfs, index):
    scalars_df, _ = scalars_dfs
    col_name = "string_col"
    scalars_df[col_name].str[index]


@pytest.mark.parametrize(
    ("index"),
    [
        pytest.param(2, id="int"),
        pytest.param(slice(None, None, None), id="default_start_slice"),
        pytest.param(slice(0, None, 1), id="default_stop_slice"),
        pytest.param(slice(0, 2, None), id="default_step_slice"),
    ],
)
def test_getitem_w_string(scalars_dfs, index):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = scalars_df[col_name].str[index].to_pandas()
    pd_result = scalars_pandas_df[col_name].str[index]

    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("index"),
    [
        pytest.param(0, id="int"),
        pytest.param(slice(None, None, None), id="default_start_slice"),
        pytest.param(slice(0, None, 1), id="default_stop_slice"),
        pytest.param(slice(0, 2, None), id="default_step_slice"),
        pytest.param(slice(0, 0, None), id="single_one_slice"),
    ],
)
@pytest.mark.parametrize(
    "column_name",
    [
        pytest.param("int_list_col"),
        pytest.param("bool_list_col"),
        pytest.param("float_list_col"),
        pytest.param("string_list_col"),
        # date, date_time and numeric are excluded because their default types are different
        # in Pandas and BigFrames
    ],
)
def test_getitem_w_array(index, column_name, repeated_df, repeated_pandas_df):
    bf_result = repeated_df[column_name].str[index].to_pandas()
    pd_result = repeated_pandas_df[column_name].str[index]

    assert_series_equal(pd_result, bf_result, check_dtype=False, check_index_type=False)


def test_getitem_w_struct_array():
    pa_struct = pa.struct(
        [
            ("name", pa.string()),
            ("age", pa.int64()),
        ]
    )
    data: list[list[dict]] = [
        [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ],
        [
            {"name": "Charlie", "age": 35},
            {"name": "David", "age": 40},
            {"name": "Eva", "age": 28},
        ],
        [],
        [{"name": "Frank", "age": 50}],
    ]
    s = bpd.Series(data, dtype=bpd.ArrowDtype(pa.list_(pa_struct)))

    result = s.str[1]
    assert dtypes.is_struct_like(result.dtype)

    expected_data = [item[1] if len(item) > 1 else None for item in data]
    expected = bpd.Series(expected_data, dtype=bpd.ArrowDtype((pa_struct)))

    assert_series_equal(result.to_pandas(), expected.to_pandas())
