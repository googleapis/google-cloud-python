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

import asyncio

import pandas as pd
import pytest

import bigframes.operations as ops
from bigframes import dtypes
from bigframes.core import array_value
from bigframes.core import expression as ex
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import SPEC, assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
def test_engines_dt_floor(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.FloorDtOp("us").as_expr("timestamp_col"),
            ops.FloorDtOp("ms").as_expr("timestamp_col"),
            ops.FloorDtOp("s").as_expr("timestamp_col"),
            ops.FloorDtOp("min").as_expr("timestamp_col"),
            ops.FloorDtOp("h").as_expr("timestamp_col"),
            ops.FloorDtOp("D").as_expr("timestamp_col"),
            ops.FloorDtOp("W").as_expr("timestamp_col"),
            ops.FloorDtOp("M").as_expr("timestamp_col"),
            ops.FloorDtOp("Q").as_expr("timestamp_col"),
            ops.FloorDtOp("Y").as_expr("timestamp_col"),
            ops.FloorDtOp("Q").as_expr("datetime_col"),
            ops.FloorDtOp("us").as_expr("datetime_col"),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
def test_engines_date_accessors(scalars_array_value: array_value.ArrayValue, engine):
    datelike_cols = ["datetime_col", "timestamp_col", "date_col"]
    accessors = [
        ops.day_op,
        ops.dayofweek_op,
        ops.month_op,
        ops.quarter_op,
        ops.year_op,
        ops.iso_day_op,
        ops.iso_week_op,
        ops.iso_year_op,
    ]

    exprs = [acc.as_expr(col) for acc in accessors for col in datelike_cols]

    arr, _ = scalars_array_value.compute_values(exprs)
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["bq", "bq-sqlglot"], indirect=True)
def test_engines_temporal_arithmetic(
    scalars_array_value: array_value.ArrayValue, engine
):
    exprs = [
        ops.timestamp_add_op.as_expr(
            "timestamp_col", ex.const(pd.Timedelta(seconds=1), dtypes.TIMEDELTA_DTYPE)
        ),
        ops.timestamp_sub_op.as_expr(
            "timestamp_col", ex.const(pd.Timedelta(seconds=1), dtypes.TIMEDELTA_DTYPE)
        ),
        ops.date_add_op.as_expr(
            "date_col", ex.const(pd.Timedelta(days=1), dtypes.TIMEDELTA_DTYPE)
        ),
        ops.date_sub_op.as_expr(
            "date_col", ex.const(pd.Timedelta(days=1), dtypes.TIMEDELTA_DTYPE)
        ),
        ops.timestamp_diff_op.as_expr("timestamp_col", "timestamp_col"),
        ops.date_diff_op.as_expr("date_col", "date_col"),
    ]

    arr, _ = scalars_array_value.compute_values(exprs)
    res = asyncio.run(engine.execute(arr.node, SPEC))
    assert res is not None
    assert len(res.batches().to_pandas()) > 0


@pytest.mark.parametrize("engine", ["bq", "bq-sqlglot"], indirect=True)
def test_engines_to_datetime(scalars_array_value: array_value.ArrayValue, engine):
    exprs = [
        ops.ToDatetimeOp().as_expr("timestamp_col"),
    ]
    arr, _ = scalars_array_value.compute_values(exprs)
    res = asyncio.run(engine.execute(arr.node, SPEC))
    assert res is not None
    df = res.batches().to_pandas()
    # The input timestamp was: TIMESTAMP('2021-07-21T17:43:43.945289+00:00')
    # The output should be naive DATETIME('2021-07-21T17:43:43.945289')
    val = df.iloc[0, -1]
    assert pd.Timestamp(val) == pd.Timestamp("2021-07-21T17:43:43.945289")
