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

import datetime

import numpy as np
import pandas as pd
import pytest

from bigframes import dtypes


@pytest.fixture(scope="module")
def rows_rolling_dfs(scalars_dfs):
    bf_df, pd_df = scalars_dfs

    target_cols = ["int64_too", "float64_col", "int64_col"]

    return bf_df[target_cols], pd_df[target_cols]


@pytest.fixture(scope="module")
def range_rolling_dfs(session):
    values = np.arange(20)
    pd_df = pd.DataFrame(
        {
            "ts_col": pd.Timestamp("20250101", tz="UTC") + pd.to_timedelta(values, "s"),
            "int_col": values % 4,
            "float_col": values / 2,
        }
    )

    bf_df = session.read_pandas(pd_df)

    return bf_df, pd_df


@pytest.fixture(scope="module")
def rows_rolling_series(scalars_dfs):
    bf_df, pd_df = scalars_dfs
    target_col = "int64_too"

    return bf_df[target_col], pd_df[target_col]


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
def test_dataframe_rolling_closed_param(rows_rolling_dfs, closed):
    bf_df, pd_df = rows_rolling_dfs

    actual_result = bf_df.rolling(window=3, closed=closed).sum().to_pandas()

    expected_result = pd_df.rolling(window=3, closed=closed).sum()
    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
def test_dataframe_groupby_rolling_closed_param(rows_rolling_dfs, closed):
    bf_df, pd_df = rows_rolling_dfs
    # Need to specify column subset for comparison due to b/406841327
    check_columns = ["float64_col", "int64_col"]

    actual_result = (
        bf_df.groupby(bf_df["int64_too"] % 2)
        .rolling(window=3, closed=closed)
        .sum()
        .to_pandas()
    )

    expected_result = (
        pd_df.groupby(pd_df["int64_too"] % 2).rolling(window=3, closed=closed).sum()
    )
    pd.testing.assert_frame_equal(
        actual_result[check_columns], expected_result, check_dtype=False
    )


def test_dataframe_rolling_on(rows_rolling_dfs):
    bf_df, pd_df = rows_rolling_dfs

    actual_result = bf_df.rolling(window=3, on="int64_too").sum().to_pandas()

    expected_result = pd_df.rolling(window=3, on="int64_too").sum()
    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)


def test_dataframe_rolling_on_invalid_column_raise_error(rows_rolling_dfs):
    bf_df, _ = rows_rolling_dfs

    with pytest.raises(ValueError):
        bf_df.rolling(window=3, on="whatever").sum()


def test_dataframe_groupby_rolling_on(rows_rolling_dfs):
    bf_df, pd_df = rows_rolling_dfs
    # Need to specify column subset for comparison due to b/406841327
    check_columns = ["float64_col", "int64_col"]

    actual_result = (
        bf_df.groupby(bf_df["int64_too"] % 2)
        .rolling(window=3, on="float64_col")
        .sum()
        .to_pandas()
    )

    expected_result = (
        pd_df.groupby(pd_df["int64_too"] % 2).rolling(window=3, on="float64_col").sum()
    )
    pd.testing.assert_frame_equal(
        actual_result[check_columns], expected_result, check_dtype=False
    )


def test_dataframe_groupby_rolling_on_invalid_column_raise_error(rows_rolling_dfs):
    bf_df, _ = rows_rolling_dfs

    with pytest.raises(ValueError):
        bf_df.groupby(level=0).rolling(window=3, on="whatever").sum()


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
def test_series_rolling_closed_param(rows_rolling_series, closed):
    bf_series, df_series = rows_rolling_series

    actual_result = bf_series.rolling(window=3, closed=closed).sum().to_pandas()

    expected_result = df_series.rolling(window=3, closed=closed).sum()
    pd.testing.assert_series_equal(actual_result, expected_result, check_dtype=False)


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
def test_series_groupby_rolling_closed_param(rows_rolling_series, closed):
    bf_series, df_series = rows_rolling_series

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
def test_series_window_agg_ops(rows_rolling_series, windowing, agg_op):
    bf_series, pd_series = rows_rolling_series

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
def test_dataframe_window_agg_ops(scalars_dfs, windowing, agg_op):
    bf_df, pd_df = scalars_dfs
    target_columns = ["int64_too", "float64_col", "bool_col"]
    index_column = "bool_col"
    bf_df = bf_df[target_columns].set_index(index_column)
    pd_df = pd_df[target_columns].set_index(index_column)

    bf_result = agg_op(windowing(bf_df)).to_pandas()

    pd_result = agg_op(windowing(pd_df))
    pd.testing.assert_frame_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
@pytest.mark.parametrize(
    "window",  # skipped numpy timedelta because Pandas does not support it.
    [pd.Timedelta("3s"), datetime.timedelta(seconds=3), "3s"],
)
@pytest.mark.parametrize("ascending", [True, False])
def test_series_range_rolling(range_rolling_dfs, window, closed, ascending):
    bf_df, pd_df = range_rolling_dfs
    bf_series = bf_df.set_index("ts_col")["int_col"]
    pd_series = pd_df.set_index("ts_col")["int_col"]

    actual_result = (
        bf_series.sort_index(ascending=ascending)
        .rolling(window=window, closed=closed)
        .min()
        .to_pandas()
    )

    expected_result = (
        pd_series.sort_index(ascending=ascending)
        .rolling(window=window, closed=closed)
        .min()
    )
    pd.testing.assert_series_equal(
        actual_result, expected_result, check_dtype=False, check_index=False
    )


def test_series_groupby_range_rolling(range_rolling_dfs):
    bf_df, pd_df = range_rolling_dfs
    bf_series = bf_df.set_index("ts_col")["int_col"]
    pd_series = pd_df.set_index("ts_col")["int_col"]

    actual_result = (
        bf_series.sort_index()
        .groupby(bf_series % 2 == 0)
        .rolling(window="3s")
        .min()
        .to_pandas()
    )

    expected_result = (
        pd_series.sort_index().groupby(pd_series % 2 == 0).rolling(window="3s").min()
    )
    pd.testing.assert_series_equal(
        actual_result, expected_result, check_dtype=False, check_index=False
    )


@pytest.mark.parametrize("closed", ["left", "right", "both", "neither"])
@pytest.mark.parametrize(
    "window",  # skipped numpy timedelta because Pandas does not support it.
    [pd.Timedelta("3s"), datetime.timedelta(seconds=3), "3s"],
)
@pytest.mark.parametrize("ascending", [True, False])
def test_dataframe_range_rolling(range_rolling_dfs, window, closed, ascending):
    bf_df, pd_df = range_rolling_dfs
    bf_df = bf_df.set_index("ts_col")
    pd_df = pd_df.set_index("ts_col")

    actual_result = (
        bf_df.sort_index(ascending=ascending)
        .rolling(window=window, closed=closed)
        .min()
        .to_pandas()
    )

    expected_result = (
        pd_df.sort_index(ascending=ascending)
        .rolling(window=window, closed=closed)
        .min()
    )
    # Need to cast Pandas index type. Otherwise it uses DatetimeIndex that
    # does not exist in BigFrame
    expected_result.index = expected_result.index.astype(dtypes.TIMESTAMP_DTYPE)
    pd.testing.assert_frame_equal(
        actual_result,
        expected_result,
        check_dtype=False,
    )


def test_dataframe_range_rolling_on(range_rolling_dfs):
    bf_df, pd_df = range_rolling_dfs
    on = "ts_col"

    actual_result = bf_df.sort_values(on).rolling(window="3s", on=on).min().to_pandas()

    expected_result = pd_df.sort_values(on).rolling(window="3s", on=on).min()
    # Need to specify the column order because Pandas (seemingly)
    # re-arranges columns alphabetically
    cols = ["ts_col", "int_col", "float_col"]
    pd.testing.assert_frame_equal(
        actual_result[cols],
        expected_result[cols],
        check_dtype=False,
        check_index_type=False,
    )


def test_dataframe_groupby_range_rolling(range_rolling_dfs):
    bf_df, pd_df = range_rolling_dfs
    on = "ts_col"

    actual_result = (
        bf_df.sort_values(on)
        .groupby("int_col")
        .rolling(window="3s", on=on)
        .min()
        .to_pandas()
    )

    expected_result = (
        pd_df.sort_values(on).groupby("int_col").rolling(window="3s", on=on).min()
    )
    expected_result.index = expected_result.index.set_names("index", level=1)
    pd.testing.assert_frame_equal(
        actual_result,
        expected_result,
        check_dtype=False,
        check_index_type=False,
    )


def test_range_rolling_order_info_lookup(range_rolling_dfs):
    bf_df, pd_df = range_rolling_dfs

    actual_result = (
        bf_df.set_index("ts_col")
        .sort_index(ascending=False)["int_col"]
        .isin(bf_df["int_col"])
        .rolling(window="3s")
        .count()
        .to_pandas()
    )

    expected_result = (
        pd_df.set_index("ts_col")
        .sort_index(ascending=False)["int_col"]
        .isin(pd_df["int_col"])
        .rolling(window="3s")
        .count()
    )
    pd.testing.assert_series_equal(
        actual_result, expected_result, check_dtype=False, check_index=False
    )


def test_range_rolling_unsupported_index_type_raise_error(range_rolling_dfs):
    bf_df, _ = range_rolling_dfs

    with pytest.raises(ValueError):
        bf_df["int_col"].sort_index().rolling(window="3s")


def test_range_rolling_unsorted_index_raise_error(range_rolling_dfs):
    bf_df, _ = range_rolling_dfs

    with pytest.raises(ValueError):
        bf_df.set_index("ts_col")["int_col"].rolling(window="3s")


def test_range_rolling_unsorted_column_raise_error(range_rolling_dfs):
    bf_df, _ = range_rolling_dfs

    with pytest.raises(ValueError):
        bf_df.rolling(window="3s", on="ts_col")
