# Copyright 2024 Google LLC
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
import decimal
import re

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
import shapely.geometry  # type: ignore

import bigframes.core.compile.sqlglot.sql.base as sql


@pytest.mark.parametrize(
    ("value", "expected_pattern"),
    (
        pytest.param(None, "NULL", id="null"),
        pytest.param(True, "TRUE", id="true"),
        pytest.param(False, "FALSE", id="false"),
        pytest.param(123, "123", id="int"),
        pytest.param(123.75, "123.75", id="float"),
        pytest.param("abc", "'abc'", id="string"),
        pytest.param(
            b"\x01\x02\x03ABC", "CAST(b'\\x01\\x02\\x03ABC' AS BYTES)", id="bytes"
        ),
        pytest.param(
            decimal.Decimal("123.75"), "CAST(123.75 AS NUMERIC)", id="decimal"
        ),
        pytest.param(
            datetime.date(2025, 1, 1), "CAST('2025-01-01' AS DATE)", id="date"
        ),
        pytest.param(
            datetime.datetime(2025, 1, 2, 3, 45, 6, 789123),
            "CAST('2025-01-02T03:45:06.789123' AS DATETIME)",
            id="datetime",
        ),
        pytest.param(
            datetime.time(12, 34, 56, 789123),
            "CAST('12:34:56.789123' AS TIME)",
            id="time",
        ),
        pytest.param(
            datetime.datetime(
                2025, 1, 2, 3, 45, 6, 789123, tzinfo=datetime.timezone.utc
            ),
            "CAST('2025-01-02T03:45:06.789123+00:00' AS TIMESTAMP)",
            id="timestamp",
        ),
        pytest.param(np.int64(123), "123", id="np_int64"),
        pytest.param(np.float64(123.75), "123.75", id="np_float64"),
        pytest.param(float("inf"), "CAST('Infinity' AS FLOAT64)", id="inf"),
        pytest.param(float("-inf"), "CAST('-Infinity' AS FLOAT64)", id="neg_inf"),
        pytest.param(float("nan"), "NULL", id="nan"),
        pytest.param(pd.NA, "NULL", id="pd_na"),
        pytest.param(datetime.timedelta(seconds=1), "1000000", id="timedelta"),
        pytest.param("POINT (0 1)", "'POINT (0 1)'", id="string_geo"),
    ),
)
def test_literal(value, expected_pattern):
    got = sql.to_sql(sql.literal(value))
    assert got == expected_pattern


def test_literal_for_geo():
    value = shapely.geometry.Point(0, 1)
    expected_pattern = r"ST_GEOGFROMTEXT\('POINT \(0[.]?0* 1[.]?0*\)'\)"
    got = sql.to_sql(sql.literal(value))
    assert re.match(expected_pattern, got) is not None


@pytest.mark.parametrize(
    ("value", "dtype", "expected"),
    (
        pytest.param(
            decimal.Decimal("1.23"),
            sql.dtypes.BIGNUMERIC_DTYPE,
            "CAST(1.23 AS BIGNUMERIC)",
            id="bignumeric",
        ),
        pytest.param(
            [],
            pd.ArrowDtype(pa.list_(pa.int64())),
            "ARRAY<INT64>[]",
            id="empty_array",
        ),
        pytest.param(
            {"a": 1, "b": "hello"},
            pd.ArrowDtype(pa.struct([("a", pa.int64()), ("b", pa.string())])),
            "STRUCT(1 AS `a`, 'hello' AS `b`)",
            id="struct",
        ),
        pytest.param(
            float("nan"),
            sql.dtypes.FLOAT_DTYPE,
            "CAST('NaN' AS FLOAT64)",
            id="explicit_nan",
        ),
        pytest.param(
            pa.scalar(123, type=pa.int64()),
            None,
            "123",
            id="pa_scalar_int",
        ),
        pytest.param(
            pa.scalar(None, type=pa.int64()),
            None,
            "CAST(NULL AS INT64)",
            id="pa_scalar_null",
        ),
        pytest.param(
            {"a": 10},
            sql.dtypes.JSON_DTYPE,
            "PARSE_JSON('{\\'a\\': 10}')",
            id="json",
        ),
    ),
)
def test_literal_explicit_dtype(value, dtype, expected):
    got = sql.to_sql(sql.literal(value, dtype=dtype))
    assert got == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        pytest.param([True, False], "[TRUE, FALSE]", id="bool"),
        pytest.param([123, 456], "[123, 456]", id="int"),
        pytest.param(
            [123.75, 456.78, float("nan"), float("inf"), float("-inf")],
            "[\n  123.75,\n  456.78,\n  CAST('NaN' AS FLOAT64),\n  CAST('Infinity' AS FLOAT64),\n  CAST('-Infinity' AS FLOAT64)\n]",
            id="float",
        ),
        pytest.param(
            [b"\x01\x02\x03ABC", b"\x01\x02\x03ABC"],
            "[CAST(b'\\x01\\x02\\x03ABC' AS BYTES), CAST(b'\\x01\\x02\\x03ABC' AS BYTES)]",
            id="bytes",
        ),
        pytest.param(
            [datetime.date(2025, 1, 1), datetime.date(2025, 1, 1)],
            "[CAST('2025-01-01' AS DATE), CAST('2025-01-01' AS DATE)]",
            id="date",
        ),
    ),
)
def test_literal_for_list(value: list, expected: str):
    got = sql.to_sql(sql.literal(value))
    assert got == expected
