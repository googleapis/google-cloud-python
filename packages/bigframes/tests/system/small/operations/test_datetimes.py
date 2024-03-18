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
from tests.system.utils import assert_series_equal, skip_legacy_pandas

DATETIME_COL_NAMES = [("datetime_col",), ("timestamp_col",)]
DATE_COLUMNS = [
    ("datetime_col",),
    ("timestamp_col",),
    ("date_col",),
]


@pytest.mark.parametrize(
    ("col_name",),
    DATE_COLUMNS,
)
@skip_legacy_pandas
def test_dt_day(scalars_dfs, col_name):
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
@skip_legacy_pandas
def test_dt_date(scalars_dfs, col_name):
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
    DATE_COLUMNS,
)
@skip_legacy_pandas
def test_dt_dayofweek(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.dayofweek.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.dayofweek

    assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
@skip_legacy_pandas
def test_dt_hour(scalars_dfs, col_name):
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
@skip_legacy_pandas
def test_dt_minute(scalars_dfs, col_name):
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
    DATE_COLUMNS,
)
@skip_legacy_pandas
def test_dt_month(scalars_dfs, col_name):
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
    DATE_COLUMNS,
)
@skip_legacy_pandas
def test_dt_quarter(scalars_dfs, col_name):
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
@skip_legacy_pandas
def test_dt_second(scalars_dfs, col_name):
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
@skip_legacy_pandas
def test_dt_time(scalars_dfs, col_name):
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
    DATE_COLUMNS,
)
@skip_legacy_pandas
def test_dt_year(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.year.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.year

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
@skip_legacy_pandas
def test_dt_tz(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.tz
    pd_result = scalars_pandas_df[col_name].dt.tz

    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
@skip_legacy_pandas
def test_dt_unit(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.unit
    pd_result = scalars_pandas_df[col_name].dt.unit

    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("column", "date_format"),
    [
        ("timestamp_col", "%B %d, %Y, %r"),
        ("timestamp_col", "%m-%d-%Y %H:%M"),
        ("datetime_col", "%m-%d-%Y %H:%M"),
        ("datetime_col", "%H:%M"),
    ],
)
@skip_legacy_pandas
def test_dt_strftime(scalars_df_index, scalars_pandas_df_index, column, date_format):
    bf_result = scalars_df_index[column].dt.strftime(date_format).to_pandas()
    pd_result = scalars_pandas_df_index[column].dt.strftime(date_format)
    pd.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    assert bf_result.dtype == "string[pyarrow]"


def test_dt_strftime_date():
    bf_series = bigframes.series.Series(
        ["2014-08-15", "2215-08-15", "2016-02-29"]
    ).astype("date32[day][pyarrow]")

    expected_result = pd.Series(["08/15/2014", "08/15/2215", "02/29/2016"])
    bf_result = bf_series.dt.strftime("%m/%d/%Y").to_pandas()

    pd.testing.assert_series_equal(
        bf_result, expected_result, check_index_type=False, check_dtype=False
    )
    assert bf_result.dtype == "string[pyarrow]"


def test_dt_strftime_time():
    bf_series = bigframes.series.Series(
        [143542314, 345234512341, 75543252344, 626546437654754, 8543523452345234]
    ).astype("time64[us][pyarrow]")

    expected_result = pd.Series(
        ["00:02:23", "23:53:54", "20:59:03", "16:40:37", "08:57:32"]
    )
    bf_result = bf_series.dt.strftime("%X").to_pandas()

    pd.testing.assert_series_equal(
        bf_result, expected_result, check_index_type=False, check_dtype=False
    )
    assert bf_result.dtype == "string[pyarrow]"
