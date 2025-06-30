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

import itertools

import pytest

from bigframes.core import array_value
import bigframes.operations as ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()

# numeric domain


def apply_op_pairwise(
    array: array_value.ArrayValue, op: ops.BinaryOp, excluded_cols=[]
) -> array_value.ArrayValue:
    exprs = []
    for l_arg, r_arg in itertools.permutations(array.column_ids, 2):
        if (l_arg in excluded_cols) or (r_arg in excluded_cols):
            continue
        try:
            _ = op.output_type(
                array.get_column_type(l_arg), array.get_column_type(r_arg)
            )
            exprs.append(op.as_expr(l_arg, r_arg))
        except TypeError:
            continue
    assert len(exprs) > 0
    new_arr, _ = array.compute_values(exprs)
    return new_arr


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
@pytest.mark.parametrize(
    "op",
    [
        ops.eq_op,
        ops.eq_null_match_op,
        ops.ne_op,
        ops.gt_op,
        ops.lt_op,
        ops.le_op,
        ops.ge_op,
    ],
)
def test_engines_project_comparison_op(
    scalars_array_value: array_value.ArrayValue, engine, op
):
    # exclude string cols as does not contain dates
    # bool col actually doesn't work properly for bq engine
    arr = apply_op_pairwise(scalars_array_value, op, excluded_cols=["string_col"])
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)
