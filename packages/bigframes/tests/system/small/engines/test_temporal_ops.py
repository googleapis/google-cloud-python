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

import pytest

from bigframes.core import array_value
import bigframes.operations as ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

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
