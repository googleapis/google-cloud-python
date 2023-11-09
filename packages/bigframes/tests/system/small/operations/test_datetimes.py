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
from tests.system.utils import assert_series_equal

DATETIME_COL_NAMES = [("datetime_col",), ("timestamp_col",)]


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_day(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.day.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.day

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_date(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.date.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.date

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_dayofweek(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.dayofweek.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.dayofweek

    assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_hour(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.hour.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.hour

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_minute(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.minute.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.minute

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_month(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.month.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.month

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_quarter(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.quarter.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.quarter

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_second(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.second.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.second

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_time(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.time.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.time

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_year(scalars_dfs, col_name):
    if pd.__version__.startswith("1."):
        pytest.skip("Pyarrow datetime objects not support in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.year.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.year

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )
