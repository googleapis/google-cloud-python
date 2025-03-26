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


@pytest.fixture(scope="module")
def rolling_dfs(scalars_dfs):
    bf_df, pd_df = scalars_dfs

    target_cols = ["int64_too", "float64_col", "bool_col"]

    bf_df = bf_df[target_cols].set_index("bool_col")
    pd_df = pd_df[target_cols].set_index("bool_col")

    return bf_df, pd_df


@pytest.fixture(scope="module")
def rolling_series(scalars_dfs):
    bf_df, pd_df = scalars_dfs
    target_col = "int64_too"

    return bf_df[target_col], pd_df[target_col]


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
def test_dataframe_rolling_closed_param(rolling_dfs, closed):
    bf_df, pd_df = rolling_dfs

    actual_result = bf_df.rolling(window=3, closed=closed).sum().to_pandas()

    expected_result = pd_df.rolling(window=3, closed=closed).sum()
    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
def test_dataframe_groupby_rolling_closed_param(rolling_dfs, closed):
    bf_df, pd_df = rolling_dfs

    actual_result = (
        bf_df.groupby(level=0).rolling(window=3, closed=closed).sum().to_pandas()
    )

    expected_result = pd_df.groupby(level=0).rolling(window=3, closed=closed).sum()
    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)


def test_dataframe_rolling_default_closed_param(rolling_dfs):
    bf_df, pd_df = rolling_dfs

    actual_result = bf_df.rolling(window=3).sum().to_pandas()

    expected_result = pd_df.rolling(window=3).sum()
    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)


def test_dataframe_groupby_rolling_default_closed_param(rolling_dfs):
    bf_df, pd_df = rolling_dfs

    actual_result = bf_df.groupby(level=0).rolling(window=3).sum().to_pandas()

    expected_result = pd_df.groupby(level=0).rolling(window=3).sum()
    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
def test_series_rolling_closed_param(rolling_series, closed):
    bf_series, df_series = rolling_series

    actual_result = bf_series.rolling(window=3, closed=closed).sum().to_pandas()

    expected_result = df_series.rolling(window=3, closed=closed).sum()
    pd.testing.assert_series_equal(actual_result, expected_result, check_dtype=False)


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
def test_series_groupby_rolling_closed_param(rolling_series, closed):
    bf_series, df_series = rolling_series

    actual_result = (
        bf_series.groupby(bf_series % 2)
        .rolling(window=3, closed=closed)
        .sum()
        .to_pandas()
    )

    expected_result = (
        df_series.groupby(df_series % 2).rolling(window=3, closed=closed).sum()
    )
    pd.testing.assert_series_equal(actual_result, expected_result, check_dtype=False)


def test_series_rolling_default_closed_param(rolling_series):
    bf_series, df_series = rolling_series

    actual_result = bf_series.rolling(window=3).sum().to_pandas()

    expected_result = df_series.rolling(window=3).sum()
    pd.testing.assert_series_equal(actual_result, expected_result, check_dtype=False)


def test_series_groupby_rolling_default_closed_param(rolling_series):
    bf_series, df_series = rolling_series

    actual_result = bf_series.groupby(bf_series % 2).rolling(window=3).sum().to_pandas()

    expected_result = df_series.groupby(df_series % 2).rolling(window=3).sum()
    pd.testing.assert_series_equal(actual_result, expected_result, check_dtype=False)


@pytest.mark.parametrize(
    ("windowing"),
    [
        pytest.param(lambda x: x.expanding(), id="expanding"),
        pytest.param(lambda x: x.rolling(3, min_periods=3), id="rolling"),
        pytest.param(
            lambda x: x.groupby(x % 2).rolling(3, min_periods=3), id="rollinggroupby"
        ),
        pytest.param(
            lambda x: x.groupby(x % 3).expanding(min_periods=2), id="expandinggroupby"
        ),
    ],
)
@pytest.mark.parametrize(
    ("agg_op"),
    [
        pytest.param(lambda x: x.sum(), id="sum"),
        pytest.param(lambda x: x.min(), id="min"),
        pytest.param(lambda x: x.max(), id="max"),
        pytest.param(lambda x: x.mean(), id="mean"),
        pytest.param(lambda x: x.count(), id="count"),
        pytest.param(lambda x: x.std(), id="std"),
        pytest.param(lambda x: x.var(), id="var"),
    ],
)
def test_series_window_agg_ops(rolling_series, windowing, agg_op):
    bf_series, pd_series = rolling_series

    actual_result = agg_op(windowing(bf_series)).to_pandas()

    expected_result = agg_op(windowing(pd_series))
    pd.testing.assert_series_equal(expected_result, actual_result, check_dtype=False)


@pytest.mark.parametrize(
    ("windowing"),
    [
        pytest.param(lambda x: x.expanding(), id="expanding"),
        pytest.param(lambda x: x.rolling(3, min_periods=3), id="rolling"),
        pytest.param(
            lambda x: x.groupby(level=0).rolling(3, min_periods=3), id="rollinggroupby"
        ),
        pytest.param(
            lambda x: x.groupby("int64_too").expanding(min_periods=2),
            id="expandinggroupby",
        ),
    ],
)
@pytest.mark.parametrize(
    ("agg_op"),
    [
        pytest.param(lambda x: x.sum(), id="sum"),
        pytest.param(lambda x: x.min(), id="min"),
        pytest.param(lambda x: x.max(), id="max"),
        pytest.param(lambda x: x.mean(), id="mean"),
        pytest.param(lambda x: x.count(), id="count"),
        pytest.param(lambda x: x.std(), id="std"),
        pytest.param(lambda x: x.var(), id="var"),
    ],
)
def test_dataframe_window_agg_ops(rolling_dfs, windowing, agg_op):
    bf_df, pd_df = rolling_dfs

    bf_result = agg_op(windowing(bf_df)).to_pandas()

    pd_result = agg_op(windowing(pd_df))
    pd.testing.assert_frame_equal(pd_result, bf_result, check_dtype=False)
