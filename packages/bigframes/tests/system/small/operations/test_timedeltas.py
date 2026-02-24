# Copyright 2025 Google LLC
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
import operator

import numpy as np
from packaging import version
import pandas as pd
import pyarrow as pa
import pytest

from bigframes import dtypes
import bigframes.testing

# Some methods/features used by this test don't exist in pandas 1.x
pytest.importorskip("pandas", minversion="2.0.0")


@pytest.fixture(scope="module")
def temporal_dfs(session):
    pandas_df = pd.DataFrame(
        {
            "datetime_col": pd.Series(
                [
                    pd.Timestamp("2025-02-01 01:00:01"),
                    pd.Timestamp("2019-01-02 02:00:00"),
                    pd.Timestamp("1997-01-01 19:00:00"),
                ],
                dtype=dtypes.DATETIME_DTYPE,
            ),
            "timestamp_col": pd.Series(
                [
                    pd.Timestamp("2023-01-01 01:00:01", tz="UTC"),
                    pd.Timestamp("2024-01-02 02:00:00", tz="UTC"),
                    pd.Timestamp("2005-03-05 02:00:00", tz="UTC"),
                ],
                dtype=dtypes.TIMESTAMP_DTYPE,
            ),
            "date_col": pd.Series(
                [
                    datetime.date(2000, 1, 1),
                    datetime.date(2001, 2, 3),
                    datetime.date(2020, 9, 30),
                ],
                dtype=dtypes.DATE_DTYPE,
            ),
            "timedelta_col_1": pd.Series(
                [
                    pd.Timedelta(5, "s"),
                    pd.Timedelta(-4, "m"),
                    pd.Timedelta(5, "h"),
                ],
                dtype=dtypes.TIMEDELTA_DTYPE,
            ),
            "timedelta_col_2": pd.Series(
                [
                    pd.Timedelta(3, "s"),
                    pd.Timedelta(-4, "m"),
                    pd.Timedelta(6, "h"),
                ],
                dtype=dtypes.TIMEDELTA_DTYPE,
            ),
            "float_col": pd.Series([1.5, 2, -3], dtype=dtypes.FLOAT_DTYPE),
            "int_col": pd.Series([1, 2, -3], dtype="Int64"),
            "positive_int_col": pd.Series([1, 2, 3], dtype="Int64"),
        },
        index=pd.Index(range(3), dtype="Int64"),
    )

    bigframes_df = session.read_pandas(pandas_df)

    return bigframes_df, pandas_df


def _assert_series_equal(actual: pd.Series, expected: pd.Series):
    """Helper function specifically for timedelta testing. Don't use it outside of this module."""
    bigframes.testing.assert_series_equal(
        actual,
        expected,
        check_index_type=False,
        check_dtype=False,
    )


@pytest.mark.parametrize(
    ("op", "col_1", "col_2", "arrow_supported"),
    [
        (operator.add, "timedelta_col_1", "timedelta_col_2", True),
        (operator.sub, "timedelta_col_1", "timedelta_col_2", True),
        (operator.truediv, "timedelta_col_1", "timedelta_col_2", True),
        (operator.floordiv, "timedelta_col_1", "timedelta_col_2", True),
        (operator.truediv, "timedelta_col_1", "float_col", False),
        (operator.floordiv, "timedelta_col_1", "float_col", False),
        (operator.mul, "timedelta_col_1", "float_col", False),
        (operator.mul, "float_col", "timedelta_col_1", False),
        (operator.mod, "timedelta_col_1", "timedelta_col_2", False),
    ],
)
def test_timedelta_binary_ops_between_series(
    temporal_dfs, op, col_1, col_2, arrow_supported
):
    bf_df, pd_df = temporal_dfs

    actual_result = op(bf_df[col_1], bf_df[col_2]).to_pandas()

    if not arrow_supported:
        expected_result = pd_df.apply(lambda x: op(x[col_1], x[col_2]), axis=1)
    else:
        expected_result = op(pd_df[col_1], pd_df[col_2])
    _assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize(
    ("op", "col", "literal", "arrow_supported"),
    [
        (operator.add, "timedelta_col_1", pd.Timedelta(2, "s").as_unit("us"), True),
        (operator.sub, "timedelta_col_1", pd.Timedelta(2, "s").as_unit("us"), True),
        (operator.truediv, "timedelta_col_1", pd.Timedelta(2, "s").as_unit("us"), True),
        (
            operator.floordiv,
            "timedelta_col_1",
            pd.Timedelta(2, "s").as_unit("us"),
            False,
        ),
        (operator.truediv, "timedelta_col_1", 3, True),
        (operator.floordiv, "timedelta_col_1", 3, False),
        (operator.mul, "timedelta_col_1", 3, True),
        (operator.mul, "float_col", pd.Timedelta(1, "s").as_unit("us"), True),
        (operator.mod, "timedelta_col_1", pd.Timedelta(7, "s").as_unit("us"), False),
    ],
)
def test_timedelta_binary_ops_series_and_literal(
    temporal_dfs, op, col, literal, arrow_supported
):
    bf_df, pd_df = temporal_dfs

    actual_result = op(bf_df[col], literal).to_pandas()

    if not arrow_supported:
        expected_result = pd_df[col].map(lambda x: op(x, literal))
    else:
        expected_result = op(pd_df[col], literal)
    _assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize(
    ("op", "col", "literal", "arrow_supported"),
    [
        (operator.add, "timedelta_col_1", pd.Timedelta(2, "s").as_unit("us"), True),
        (operator.sub, "timedelta_col_1", pd.Timedelta(2, "s").as_unit("us"), True),
        (operator.truediv, "timedelta_col_1", pd.Timedelta(2, "s").as_unit("us"), True),
        (
            operator.floordiv,
            "timedelta_col_1",
            pd.Timedelta(2, "s").as_unit("us"),
            True,
        ),
        (operator.truediv, "float_col", pd.Timedelta(2, "s").as_unit("us"), True),
        (operator.floordiv, "float_col", pd.Timedelta(2, "s").as_unit("us"), True),
        (operator.mul, "timedelta_col_1", 3, True),
        (operator.mul, "float_col", pd.Timedelta(1, "s").as_unit("us"), False),
        (operator.mod, "timedelta_col_1", pd.Timedelta(7, "s").as_unit("us"), False),
    ],
)
def test_timedelta_binary_ops_literal_and_series(
    temporal_dfs, op, col, literal, arrow_supported
):
    bf_df, pd_df = temporal_dfs

    actual_result = op(literal, bf_df[col]).to_pandas()

    if not arrow_supported:
        expected_result = pd_df[col].map(lambda x: op(literal, x))
    else:
        expected_result = op(literal, pd_df[col])
    _assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize("op", [operator.pos, operator.neg, operator.abs])
def test_timedelta_unary_ops(temporal_dfs, op):
    bf_df, pd_df = temporal_dfs

    actual_result = op(bf_df["timedelta_col_1"]).to_pandas()

    expected_result = op(pd_df["timedelta_col_1"])
    _assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize(
    ("column", "pd_dtype"),
    [
        ("datetime_col", "<M8[ns]"),
        ("timestamp_col", "datetime64[ns, UTC]"),
    ],
)
def test_timestamp_add__ts_series_plus_td_series(temporal_dfs, column, pd_dtype):
    bf_df, pd_df = temporal_dfs

    actual_result = (bf_df[column] + bf_df["timedelta_col_1"]).to_pandas()

    expected_result = pd_df[column] + pd_df["timedelta_col_1"]
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize("column", ["datetime_col", "timestamp_col"])
def test_timestamp_add__ts_series_plus_td_series__explicit_cast(temporal_dfs, column):
    bf_df, _ = temporal_dfs
    dtype = pd.ArrowDtype(pa.duration("us"))

    actual_result = bf_df[column] + bf_df["int_col"].astype(dtype)

    assert len(actual_result) > 0


@pytest.mark.parametrize(
    "literal",
    [
        pytest.param(pd.Timedelta(1, unit="s").as_unit("us"), id="pandas"),
        pytest.param(datetime.timedelta(seconds=1), id="python-datetime"),
        pytest.param(np.timedelta64(1, "s"), id="numpy"),
    ],
)
def test_timestamp_add__ts_series_plus_td_literal(temporal_dfs, literal):
    bf_df, pd_df = temporal_dfs

    actual_result = (bf_df["timestamp_col"] + literal).to_pandas()

    expected_result = pd_df["timestamp_col"] + literal
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize(
    ("column", "pd_dtype"),
    [
        ("datetime_col", "<M8[ns]"),
        ("timestamp_col", "datetime64[ns, UTC]"),
    ],
)
def test_timestamp_add__td_series_plus_ts_series(temporal_dfs, column, pd_dtype):
    bf_df, pd_df = temporal_dfs

    actual_result = (bf_df["timedelta_col_1"] + bf_df[column]).to_pandas()

    expected_result = pd_df["timedelta_col_1"] + pd_df[column]
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_timestamp_add__td_literal_plus_ts_series(temporal_dfs):
    bf_df, pd_df = temporal_dfs
    timedelta = pd.Timedelta(1, unit="s").as_unit("us")

    actual_result = (timedelta + bf_df["datetime_col"]).to_pandas()

    expected_result = timedelta + pd_df["datetime_col"]
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_timestamp_add__ts_literal_plus_td_series(temporal_dfs):
    bf_df, pd_df = temporal_dfs
    timestamp = pd.Timestamp("2025-01-01", tz="UTC")

    actual_result = (timestamp + bf_df["timedelta_col_1"]).to_pandas()

    expected_result = timestamp + pd_df["timedelta_col_1"]
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize(
    ("column", "pd_dtype"),
    [
        ("datetime_col", "<M8[ns]"),
        ("timestamp_col", "datetime64[ns, UTC]"),
    ],
)
def test_timestamp_add_with_numpy_op(temporal_dfs, column, pd_dtype):
    bf_df, pd_df = temporal_dfs

    actual_result = np.add(bf_df[column], bf_df["timedelta_col_1"]).to_pandas()

    expected_result = np.add(pd_df[column], pd_df["timedelta_col_1"])
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_timestamp_add_dataframes(temporal_dfs):
    columns = ["datetime_col", "timestamp_col"]
    timedelta = pd.Timedelta(1, unit="s").as_unit("us")
    bf_df, pd_df = temporal_dfs

    actual_result = (bf_df[columns] + timedelta).to_pandas()
    actual_result["datetime_col"] = actual_result["datetime_col"]
    actual_result["timestamp_col"] = actual_result["timestamp_col"]

    expected_result = pd_df[columns] + timedelta
    bigframes.testing.assert_frame_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize(
    ("column",),
    [
        ("datetime_col",),
        ("timestamp_col",),
    ],
)
def test_timestamp_sub__ts_series_minus_td_series(
    temporal_dfs,
    column,
):
    bf_df, pd_df = temporal_dfs

    actual_result = (bf_df[column] - bf_df["timedelta_col_1"]).to_pandas()

    expected_result = pd_df[column] - pd_df["timedelta_col_1"]
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize(
    ("column",),
    [
        ("datetime_col",),
        ("timestamp_col",),
    ],
)
def test_timestamp_sub__ts_series_minus_td_literal(
    temporal_dfs,
    column,
):
    bf_df, pd_df = temporal_dfs
    literal = pd.Timedelta(1, "h")

    actual_result = (bf_df[column] - literal).to_pandas()

    # pandas type behavior changes per pandas version
    expected_result = (pd_df[column] - literal).astype(actual_result.dtype)
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_timestamp_sub__ts_literal_minus_td_series(temporal_dfs):
    bf_df, pd_df = temporal_dfs
    literal = pd.Timestamp("2025-01-01 01:00:00")

    actual_result = (
        literal - bf_df["timedelta_col_1"]
    ).to_pandas()  # .astype("<M8[ns]")

    expected_result = literal - pd_df["timedelta_col_1"]
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize(
    ("column", "pd_dtype"),
    [
        ("datetime_col", "<M8[ns]"),
        ("timestamp_col", "datetime64[ns, UTC]"),
    ],
)
def test_timestamp_sub_with_numpy_op(temporal_dfs, column, pd_dtype):
    bf_df, pd_df = temporal_dfs

    actual_result = np.subtract(bf_df[column], bf_df["timedelta_col_1"]).to_pandas()

    expected_result = np.subtract(pd_df[column], pd_df["timedelta_col_1"])
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_timestamp_sub_dataframes(temporal_dfs):
    columns = ["datetime_col", "timestamp_col"]
    timedelta = pd.Timedelta(1, unit="s").as_unit("us")
    bf_df, pd_df = temporal_dfs

    actual_result = (bf_df[columns] - timedelta).to_pandas()
    actual_result["datetime_col"] = actual_result["datetime_col"]
    actual_result["timestamp_col"] = actual_result["timestamp_col"]

    expected_result = pd_df[columns] - timedelta
    bigframes.testing.assert_frame_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize(
    ("left_col", "right_col"),
    [
        ("date_col", "timedelta_col_1"),
        ("timedelta_col_1", "date_col"),
    ],
)
def test_date_add__series_add_series(temporal_dfs, left_col, right_col):
    if version.Version(pd.__version__) < version.Version("2.1.0"):
        pytest.skip("not supported by Pandas < 2.1.0")

    bf_df, pd_df = temporal_dfs

    actual_result = (bf_df[left_col] + bf_df[right_col]).to_pandas()

    expected_result = (pd_df[left_col] + pd_df[right_col]).astype(dtypes.DATETIME_DTYPE)
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


# Pandas does not support date literal + timedelta series so we don't test it here.
def test_date_add__literal_add_series(temporal_dfs):
    bf_df, pd_df = temporal_dfs
    literal = pd.Timedelta(1, "d")

    actual_result = (literal + bf_df["date_col"]).to_pandas()

    expected_result = (literal + pd_df["date_col"]).astype(dtypes.DATETIME_DTYPE)
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


# Pandas does not support timedelta series + date literal so we don't test it here.
def test_date_add__series_add_literal(temporal_dfs):
    bf_df, pd_df = temporal_dfs
    literal = pd.Timedelta(1, "d")

    actual_result = (bf_df["date_col"] + literal).to_pandas()

    expected_result = (pd_df["date_col"] + literal).astype(dtypes.DATETIME_DTYPE)
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_date_sub__series_sub_series(temporal_dfs):
    if version.Version(pd.__version__) < version.Version("2.1.0"):
        pytest.skip("not supported by Pandas < 2.1.0")

    bf_df, pd_df = temporal_dfs

    actual_result = (bf_df["date_col"] - bf_df["timedelta_col_1"]).to_pandas()

    expected_result = (pd_df["date_col"] - pd_df["timedelta_col_1"]).astype(
        dtypes.DATETIME_DTYPE
    )
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_date_sub__series_sub_literal(temporal_dfs):
    bf_df, pd_df = temporal_dfs
    literal = pd.Timedelta(1, "d")

    actual_result = (bf_df["date_col"] - literal).to_pandas()

    expected_result = (pd_df["date_col"] - literal).astype(dtypes.DATETIME_DTYPE)
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize(
    "compare_func",
    [
        pytest.param(operator.gt, id="gt"),
        pytest.param(operator.ge, id="ge"),
        pytest.param(operator.eq, id="eq"),
        pytest.param(operator.ne, id="ne"),
        pytest.param(operator.lt, id="lt"),
        pytest.param(operator.le, id="le"),
    ],
)
def test_timedelta_series_comparison(temporal_dfs, compare_func):
    bf_df, pd_df = temporal_dfs

    actual_result = compare_func(
        bf_df["timedelta_col_1"], bf_df["timedelta_col_2"]
    ).to_pandas()

    expected_result = compare_func(
        pd_df["timedelta_col_1"], pd_df["timedelta_col_2"]
    ).astype("boolean")
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


@pytest.mark.parametrize(
    "compare_func",
    [
        pytest.param(operator.gt, id="gt"),
        pytest.param(operator.ge, id="ge"),
        pytest.param(operator.eq, id="eq"),
        pytest.param(operator.ne, id="ne"),
        pytest.param(operator.lt, id="lt"),
        pytest.param(operator.le, id="le"),
    ],
)
def test_timedelta_series_and_literal_comparison(temporal_dfs, compare_func):
    bf_df, pd_df = temporal_dfs
    literal = pd.Timedelta(3, "s").as_unit("us")

    actual_result = compare_func(literal, bf_df["timedelta_col_2"]).to_pandas()

    expected_result = compare_func(literal, pd_df["timedelta_col_2"]).astype("boolean")
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_timedelta_filtering(session):
    pd_series = pd.Series(
        [
            pd.Timestamp("2025-01-01 01:00:00"),
            pd.Timestamp("2025-01-01 02:00:00"),
            pd.Timestamp("2025-01-01 03:00:00"),
        ],
        dtype=dtypes.TIMESTAMP_DTYPE,
    )
    bf_series = session.read_pandas(pd_series)
    timestamp = pd.Timestamp("2025-01-01, 00:00:01", tz="UTC")

    actual_result = bf_series[
        ((bf_series - timestamp) > pd.Timedelta(1, "h"))
    ].to_pandas()

    expected_result = pd_series[(pd_series - timestamp) > pd.Timedelta(1, "h")]
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_timedelta_ordering(session):
    pd_df = pd.DataFrame(
        {
            "col_1": pd.Series(
                [
                    pd.Timestamp("2025-01-01 01:00:00"),
                    pd.Timestamp("2025-01-01 02:00:00"),
                    pd.Timestamp("2025-01-01 03:00:00"),
                ],
                dtype=dtypes.TIMESTAMP_DTYPE,
            ),
            "col_2": pd.Series(
                [
                    pd.Timestamp("2025-01-01 01:00:02"),
                    pd.Timestamp("2025-01-01 02:00:01"),
                    pd.Timestamp("2025-01-01 02:59:59"),
                ],
                dtype=dtypes.TIMESTAMP_DTYPE,
            ),
        }
    )
    bf_df = session.read_pandas(pd_df)

    actual_result = (bf_df["col_2"] - bf_df["col_1"]).sort_values().to_pandas()

    expected_result = (pd_df["col_2"] - pd_df["col_1"]).sort_values()
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_timedelta_cumsum(temporal_dfs):
    bf_df, pd_df = temporal_dfs

    actual_result = bf_df["timedelta_col_1"].cumsum().to_pandas()

    expected_result = pd_df["timedelta_col_1"].cumsum()
    _assert_series_equal(actual_result, expected_result)


@pytest.mark.parametrize(
    "agg_func",
    [
        pytest.param(lambda x: x.min(), id="min"),
        pytest.param(lambda x: x.max(), id="max"),
        pytest.param(lambda x: x.sum(), id="sum"),
        pytest.param(lambda x: x.mean(), id="mean"),
        pytest.param(lambda x: x.median(), id="median"),
        pytest.param(lambda x: x.quantile(0.5), id="quantile"),
        pytest.param(lambda x: x.std(), id="std"),
    ],
)
def test_timedelta_agg__timedelta_result(temporal_dfs, agg_func):
    bf_df, pd_df = temporal_dfs

    actual_result = agg_func(bf_df["timedelta_col_1"])

    expected_result = agg_func(pd_df["timedelta_col_1"])
    assert actual_result == expected_result


@pytest.mark.parametrize(
    "agg_func",
    [
        pytest.param(lambda x: x.count(), id="count"),
        pytest.param(lambda x: x.nunique(), id="nunique"),
    ],
)
def test_timedelta_agg__int_result(temporal_dfs, agg_func):
    bf_df, pd_df = temporal_dfs

    actual_result = agg_func(bf_df["timedelta_col_1"])

    expected_result = agg_func(pd_df["timedelta_col_1"])
    assert actual_result == expected_result


def test_timestamp_diff_after_type_casting(temporal_dfs):
    if version.Version(pd.__version__) <= version.Version("2.1.0"):
        pytest.skip(
            "Temporal type casting is not well-supported in older verions of Pandas."
        )

    bf_df, pd_df = temporal_dfs
    dtype = pd.ArrowDtype(pa.timestamp("us", tz="UTC"))

    actual_result = (
        bf_df["timestamp_col"] - bf_df["positive_int_col"].astype(dtype)
    ).to_pandas()

    expected_result = pd_df["timestamp_col"] - pd_df["positive_int_col"].astype(
        "datetime64[us, UTC]"
    )
    bigframes.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False, check_dtype=False
    )
