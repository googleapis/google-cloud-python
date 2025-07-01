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

from bigframes.core import array_value, expression, nodes
import bigframes.operations as ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_filter_bool_col(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    node = nodes.FilterNode(
        scalars_array_value.node, predicate=expression.deref("bool_col")
    )
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_filter_expr_cond(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    predicate = ops.gt_op.as_expr(
        expression.deref("float64_col"), expression.deref("int64_col")
    )
    node = nodes.FilterNode(scalars_array_value.node, predicate=predicate)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_filter_true(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    predicate = expression.const(True)
    node = nodes.FilterNode(scalars_array_value.node, predicate=predicate)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_filter_false(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    predicate = expression.const(False)
    node = nodes.FilterNode(scalars_array_value.node, predicate=predicate)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)
