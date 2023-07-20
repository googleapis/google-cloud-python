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

import pandas as pd
import pytest

import bigframes.series

from ...utils import assert_series_equal_ignoring_order


def test_find(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.find("W").compute()
    pd_result = scalars_pandas_df[col_name].str.find("W")

    # One of type mismatches to be documented. Here, the `bf_result.dtype` is `Int64` but
    # the `pd_result.dtype` is `float64`: https://github.com/pandas-dev/pandas/issues/51948
    assert_series_equal_ignoring_order(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


def test_len(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.len().compute()
    pd_result = scalars_pandas_df[col_name].str.len()

    # One of dtype mismatches to be documented. Here, the `bf_result.dtype` is `Int64` but
    # the `pd_result.dtype` is `float64`: https://github.com/pandas-dev/pandas/issues/51948
    assert_series_equal_ignoring_order(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


def test_lower(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.lower().compute()
    pd_result = scalars_pandas_df[col_name].str.lower()

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )


def test_reverse(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.reverse().compute()
    pd_result = scalars_pandas_df[col_name].copy()
    for i in pd_result.index:
        cell = pd_result.loc[i]
        if pd.isna(cell):
            pd_result.loc[i] = None
        else:
            pd_result.loc[i] = cell[::-1]

    assert_series_equal_ignoring_order(
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
    bf_result = bf_series.str.slice(start, stop).compute()
    pd_series = scalars_pandas_df[col_name]
    pd_result = pd_series.str.slice(start, stop)

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )


def test_strip(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.strip().compute()
    pd_result = scalars_pandas_df[col_name].str.strip()

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )


def test_upper(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.upper().compute()
    pd_result = scalars_pandas_df[col_name].str.upper()

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )


def test_isnumeric(session):
    pandas_df = pd.DataFrame(
        {
            "numeric_string_col": [
                "٠١٢٣٤٥٦٧٨٩",
                "",
                "0",
                "字",
                "五",
                "0123456789",
                pd.NA,
                "abc 123 mixed letters and numbers",
                "no numbers here",
                "123a",
                "23!",
                " 45",
                "a45",
            ]
        }
    )

    df = session.read_pandas(pandas_df)

    pd_result = pandas_df.numeric_string_col.str.isnumeric()
    bf_result = df.numeric_string_col.str.isnumeric().compute()

    assert_series_equal_ignoring_order(
        bf_result,
        pd_result.astype(pd.BooleanDtype())
        # the dtype here is a case of intentional diversion from pandas
        # see go/bigframes-dtypes
    )


def test_rstrip(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.rstrip().compute()
    pd_result = scalars_pandas_df[col_name].str.rstrip()

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )


def test_lstrip(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.lstrip().compute()
    pd_result = scalars_pandas_df[col_name].str.lstrip()

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(["repeats"], [(5,), (0,), (1,)])
def test_repeat(scalars_dfs, repeats):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.repeat(repeats).compute()
    pd_result = scalars_pandas_df[col_name].str.repeat(repeats)

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )


def test_capitalize(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.str.capitalize().compute()
    pd_result = scalars_pandas_df[col_name].str.capitalize()

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )


def test_cat_with_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_filter: bigframes.series.Series = scalars_df["bool_col"]
    bf_left: bigframes.series.Series = scalars_df[col_name][bf_filter]
    bf_right: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_left.str.cat(others=bf_right).compute()
    pd_filter = scalars_pandas_df["bool_col"]
    pd_left = scalars_pandas_df[col_name][pd_filter]
    pd_right = scalars_pandas_df[col_name]
    pd_result = pd_left.str.cat(others=pd_right)

    assert_series_equal_ignoring_order(
        pd_result,
        bf_result,
    )
