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

import numpy
from pandas import testing
import pandas as pd
import pytest

import bigframes.series
from bigframes.testing.utils import assert_series_equal

DATETIME_COL_NAMES = [("datetime_col",), ("timestamp_col",)]
DATE_COLUMNS = [
    ("datetime_col",),
    ("timestamp_col",),
    ("date_col",),
]


@pytest.fixture
def timedelta_series(session):
    pd_s = pd.Series(pd.to_timedelta([1.1010101, 2.2020102, 3.3030103], unit="d"))
    bf_s = session.read_pandas(pd_s)

    return bf_s, pd_s


@pytest.mark.parametrize(
    ("col_name",),
    DATE_COLUMNS,
)
def test_dt_day(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_date(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_dayofweek(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.dayofweek.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.dayofweek

    assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("col_name",),
    DATE_COLUMNS,
)
def test_dt_dayofyear(scalars_dfs, col_name):
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.dayofyear.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.dayofyear

    assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_dt_hour(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_minute(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_month(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_quarter(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_second(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_time(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_year(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.year.to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.year

    assert_series_equal(
        pd_result.astype(pd.Int64Dtype()),
        bf_result,
    )


def test_dt_isocalendar(session):
    # We don't re-use the exisintg scalars_dfs fixture because iso calendar
    # get tricky when a new year starts, but the dataset `scalars_dfs` does not cover
    # this case.
    pd_s = pd.Series(pd.date_range("2009-12-25", "2010-01-07", freq="d"))
    bf_s = session.read_pandas(pd_s)

    actual_result = bf_s.dt.isocalendar().to_pandas()

    expected_result = pd_s.dt.isocalendar()
    testing.assert_frame_equal(
        actual_result, expected_result, check_dtype=False, check_index_type=False
    )


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_dt_tz(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df[col_name]
    bf_result = bf_series.dt.tz
    pd_result = scalars_pandas_df[col_name].dt.tz

    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_dt_unit(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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
def test_dt_strftime(scalars_df_index, scalars_pandas_df_index, column, date_format):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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


@pytest.mark.parametrize(
    ("col_name",),
    DATETIME_COL_NAMES,
)
def test_dt_normalize(scalars_dfs, col_name):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].dt.normalize().to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.normalize()

    assert_series_equal(
        pd_result.astype(scalars_df[col_name].dtype),  # normalize preserves type
        bf_result,
    )


@pytest.mark.parametrize(
    ("col_name", "freq"),
    [
        ("timestamp_col", "D"),
        ("timestamp_col", "min"),
        ("datetime_col", "s"),
        ("datetime_col", "us"),
    ],
)
def test_dt_floor(scalars_dfs, col_name, freq):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].dt.floor(freq).to_pandas()
    pd_result = scalars_pandas_df[col_name].dt.floor(freq)

    assert_series_equal(
        pd_result.astype(scalars_df[col_name].dtype),  # floor preserves type
        bf_result,
    )


def test_dt_compare_coerce_str_datetime(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df["datetime_col"]

    bf_result = (bf_series >= "2024-01-01").to_pandas()
    pd_result = scalars_pandas_df["datetime_col"] >= pd.to_datetime("2024-01-01")

    # pandas produces pyarrow bool dtype
    assert_series_equal(pd_result, bf_result, check_dtype=False)


def test_dt_clip_datetime_literals(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df["date_col"]
    bf_result = bf_series.clip(
        datetime.date(2020, 1, 1), datetime.date(2024, 1, 1)
    ).to_pandas()

    pd_result = scalars_pandas_df["date_col"].clip(
        datetime.date(2020, 1, 1), datetime.date(2024, 1, 1)
    )

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_dt_clip_coerce_str_date(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df["date_col"]
    bf_result = bf_series.clip("2020-01-01", "2024-01-01").to_pandas()

    # Pandas can't coerce with pyarrow types so convert first
    pd_result = scalars_pandas_df["date_col"].clip(
        datetime.date(2020, 1, 1), datetime.date(2024, 1, 1)
    )

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_dt_clip_coerce_str_timestamp(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series: bigframes.series.Series = scalars_df["timestamp_col"]
    bf_result = bf_series.clip(
        "2020-01-01T20:03:50Z", "2024-01-01T20:03:50Z"
    ).to_pandas()

    pd_result = scalars_pandas_df["timestamp_col"].clip(
        pd.to_datetime("2020-01-01T20:03:50Z", utc=True),
        pd.to_datetime("2024-01-01T20:03:50Z", utc=True),
    )

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize("column", ["timestamp_col", "datetime_col"])
def test_timestamp_diff_two_series(scalars_dfs, column):
    bf_df, pd_df = scalars_dfs
    bf_series = bf_df[column]
    pd_series = pd_df[column]

    actual_result = (bf_series - bf_series).to_pandas()

    expected_result = pd_series - pd_series
    assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize("column", ["timestamp_col", "datetime_col"])
def test_timestamp_diff_two_series_with_numpy_ops(scalars_dfs, column):
    bf_df, pd_df = scalars_dfs
    bf_series = bf_df[column]
    pd_series = pd_df[column]

    actual_result = numpy.subtract(bf_series, bf_series).to_pandas()

    expected_result = numpy.subtract(pd_series, pd_series)
    assert_series_equal(actual_result, expected_result)


def test_timestamp_diff_two_dataframes(scalars_dfs):
    columns = ["timestamp_col", "datetime_col"]
    bf_df, pd_df = scalars_dfs
    bf_df = bf_df[columns]
    pd_df = pd_df[columns]

    actual_result = (bf_df - bf_df).to_pandas()

    expected_result = pd_df - pd_df
    testing.assert_frame_equal(actual_result, expected_result)


def test_timestamp_diff_two_series_with_different_types_raise_error(scalars_dfs):
    df, _ = scalars_dfs

    with pytest.raises(TypeError):
        (df["timestamp_col"] - df["datetime_col"]).to_pandas()


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("timestamp_col", pd.Timestamp("2025-01-01 00:00:01", tz="America/New_York")),
        ("datetime_col", datetime.datetime(2025, 1, 1, 0, 0, 1)),
    ],
)
def test_timestamp_diff_series_sub_literal(scalars_dfs, column, value):
    bf_df, pd_df = scalars_dfs
    bf_series = bf_df[column]
    pd_series = pd_df[column]

    actual_result = (bf_series - value).to_pandas()

    expected_result = pd_series - value
    assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("timestamp_col", pd.Timestamp("2025-01-01 00:00:01", tz="America/New_York")),
        ("datetime_col", datetime.datetime(2025, 1, 1, 0, 0, 1)),
    ],
)
def test_timestamp_diff_literal_sub_series(scalars_dfs, column, value):
    bf_df, pd_df = scalars_dfs
    bf_series = bf_df[column]
    pd_series = pd_df[column]

    actual_result = (value - bf_series).to_pandas()

    expected_result = value - pd_series
    assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize("column", ["timestamp_col", "datetime_col"])
def test_timestamp_series_diff_agg(scalars_dfs, column):
    bf_df, pd_df = scalars_dfs
    bf_series = bf_df[column]
    pd_series = pd_df[column]

    actual_result = bf_series.diff().to_pandas()

    expected_result = pd_series.diff()
    assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize(
    "access",
    [
        pytest.param(lambda x: x.dt.days, id="dt.days"),
        pytest.param(lambda x: x.dt.seconds, id="dt.seconds"),
        pytest.param(lambda x: x.dt.microseconds, id="dt.microseconds"),
        pytest.param(lambda x: x.dt.total_seconds(), id="dt.total_seconds()"),
    ],
)
def test_timedelta_dt_accessors(timedelta_series, access):
    bf_s, pd_s = timedelta_series

    actual_result = access(bf_s).to_pandas()

    expected_result = access(pd_s)
    assert_series_equal(
        actual_result, expected_result, check_dtype=False, check_index_type=False
    )


@pytest.mark.parametrize(
    "access",
    [
        pytest.param(lambda x: x.dt.days, id="dt.days"),
        pytest.param(lambda x: x.dt.seconds, id="dt.seconds"),
        pytest.param(lambda x: x.dt.microseconds, id="dt.microseconds"),
        pytest.param(lambda x: x.dt.total_seconds(), id="dt.total_seconds()"),
    ],
)
def test_timedelta_dt_accessors_on_wrong_type_raise_exception(scalars_dfs, access):
    bf_df, _ = scalars_dfs

    with pytest.raises(TypeError):
        access(bf_df["timestamp_col"])
