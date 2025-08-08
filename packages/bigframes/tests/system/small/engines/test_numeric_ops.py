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
import itertools

import pytest

from bigframes.core import array_value, expression
import bigframes.operations as ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


def apply_op_pairwise(
    array: array_value.ArrayValue, op: ops.BinaryOp, excluded_cols=[]
) -> array_value.ArrayValue:
    exprs = []
    labels = []
    for l_arg, r_arg in itertools.product(array.column_ids, array.column_ids):
        if (l_arg in excluded_cols) or (r_arg in excluded_cols):
            continue
        try:
            _ = op.output_type(
                array.get_column_type(l_arg), array.get_column_type(r_arg)
            )
            expr = op.as_expr(l_arg, r_arg)
            exprs.append(expr)
            labels.append(f"{l_arg}_{r_arg}")
        except TypeError:
            continue
    assert len(exprs) > 0
    new_arr, ids = array.compute_values(exprs)
    new_arr = new_arr.rename_columns(
        {new_col: label for new_col, label in zip(ids, labels)}
    )
    return new_arr


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
def test_engines_project_add(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    arr = apply_op_pairwise(scalars_array_value, ops.add_op)
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
def test_engines_project_sub(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    arr = apply_op_pairwise(scalars_array_value, ops.sub_op)
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_project_mul(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    arr = apply_op_pairwise(scalars_array_value, ops.mul_op)
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_project_div(scalars_array_value: array_value.ArrayValue, engine):
    # TODO: Duration div is sensitive to zeroes
    # TODO: Numeric col is sensitive to scale shifts
    arr = apply_op_pairwise(
        scalars_array_value, ops.div_op, excluded_cols=["duration_col", "numeric_col"]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_project_div_durations(
    scalars_array_value: array_value.ArrayValue, engine
):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.div_op.as_expr(
                expression.deref("duration_col"),
                expression.const(datetime.timedelta(seconds=3)),
            ),
            ops.div_op.as_expr(
                expression.deref("duration_col"),
                expression.const(datetime.timedelta(seconds=-3)),
            ),
            ops.div_op.as_expr(expression.deref("duration_col"), expression.const(4)),
            ops.div_op.as_expr(expression.deref("duration_col"), expression.const(-4)),
            ops.div_op.as_expr(
                expression.deref("duration_col"), expression.const(55.55)
            ),
            ops.div_op.as_expr(
                expression.deref("duration_col"), expression.const(-55.55)
            ),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_project_floordiv(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    arr = apply_op_pairwise(
        scalars_array_value,
        ops.floordiv_op,
        excluded_cols=["duration_col", "numeric_col"],
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_project_floordiv_durations(
    scalars_array_value: array_value.ArrayValue, engine
):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.floordiv_op.as_expr(
                expression.deref("duration_col"),
                expression.const(datetime.timedelta(seconds=3)),
            ),
            ops.floordiv_op.as_expr(
                expression.deref("duration_col"),
                expression.const(datetime.timedelta(seconds=-3)),
            ),
            ops.floordiv_op.as_expr(
                expression.deref("duration_col"), expression.const(4)
            ),
            ops.floordiv_op.as_expr(
                expression.deref("duration_col"), expression.const(-4)
            ),
            ops.floordiv_op.as_expr(
                expression.deref("duration_col"), expression.const(55.55)
            ),
            ops.floordiv_op.as_expr(
                expression.deref("duration_col"), expression.const(-55.55)
            ),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_project_mod(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    arr = apply_op_pairwise(scalars_array_value, ops.mod_op)
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)
