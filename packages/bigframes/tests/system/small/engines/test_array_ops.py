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

from bigframes.core import array_value, expression
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_to_array_op(scalars_array_value: array_value.ArrayValue, engine):
    # Bigquery won't allow you to materialize arrays with null, so use non-nullable
    int64_non_null = ops.coalesce_op.as_expr("int64_col", expression.const(0))
    bool_col_non_null = ops.coalesce_op.as_expr("bool_col", expression.const(False))
    float_col_non_null = ops.coalesce_op.as_expr("float64_col", expression.const(0.0))
    string_col_non_null = ops.coalesce_op.as_expr("string_col", expression.const(""))

    arr, _ = scalars_array_value.compute_values(
        [
            ops.ToArrayOp().as_expr(int64_non_null),
            ops.ToArrayOp().as_expr(
                int64_non_null, bool_col_non_null, float_col_non_null
            ),
            ops.ToArrayOp().as_expr(string_col_non_null, string_col_non_null),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_array_reduce_op(arrays_array_value: array_value.ArrayValue, engine):
    arr, _ = arrays_array_value.compute_values(
        [
            ops.ArrayReduceOp(agg_ops.SumOp()).as_expr("float_list_col"),
            ops.ArrayReduceOp(agg_ops.StdOp()).as_expr("float_list_col"),
            ops.ArrayReduceOp(agg_ops.MaxOp()).as_expr("date_list_col"),
            ops.ArrayReduceOp(agg_ops.CountOp()).as_expr("string_list_col"),
            ops.ArrayReduceOp(agg_ops.AnyOp()).as_expr("bool_list_col"),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)
