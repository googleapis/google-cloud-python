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

from typing import Literal

import pytest

from bigframes import operations as ops
from bigframes.core import array_value, expression, ordering
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
@pytest.mark.parametrize("join_type", ["left", "inner", "right", "outer"])
def test_engines_join_on_key(
    scalars_array_value: array_value.ArrayValue,
    engine,
    join_type: Literal["inner", "outer", "left", "right"],
):
    result, _ = scalars_array_value.relational_join(
        scalars_array_value, conditions=(("int64_col", "int64_col"),), type=join_type
    )

    assert_equivalence_execution(result.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
@pytest.mark.parametrize("join_type", ["left", "inner", "right", "outer"])
def test_engines_join_on_coerced_key(
    scalars_array_value: array_value.ArrayValue,
    engine,
    join_type: Literal["inner", "outer", "left", "right"],
):
    result, _ = scalars_array_value.relational_join(
        scalars_array_value, conditions=(("int64_col", "float64_col"),), type=join_type
    )

    assert_equivalence_execution(result.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
@pytest.mark.parametrize("join_type", ["left", "inner", "right", "outer"])
def test_engines_join_multi_key(
    scalars_array_value: array_value.ArrayValue,
    engine,
    join_type: Literal["inner", "outer", "left", "right"],
):
    l_input = scalars_array_value.order_by([ordering.ascending_over("float64_col")])
    l_input, l_join_cols = scalars_array_value.compute_values(
        [
            ops.mod_op.as_expr("int64_col", expression.const(2)),
            ops.invert_op.as_expr("bool_col"),
        ]
    )
    r_input, r_join_cols = scalars_array_value.compute_values(
        [ops.mod_op.as_expr("int64_col", expression.const(3)), expression.const(True)]
    )

    conditions = tuple((l_col, r_col) for l_col, r_col in zip(l_join_cols, r_join_cols))

    result, _ = l_input.relational_join(r_input, conditions=conditions, type=join_type)

    assert_equivalence_execution(result.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
def test_engines_cross_join(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    result, _ = scalars_array_value.relational_join(scalars_array_value, type="cross")

    assert_equivalence_execution(result.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
@pytest.mark.parametrize(
    ("left_key", "right_key"),
    [
        ("int64_col", "float64_col"),
        ("float64_col", "int64_col"),
        ("int64_too", "int64_col"),
    ],
)
def test_engines_isin(
    scalars_array_value: array_value.ArrayValue, engine, left_key, right_key
):
    other = scalars_array_value.select_columns([right_key])
    result, _ = scalars_array_value.isin(
        other,
        lcol=left_key,
    )

    assert_equivalence_execution(result.node, REFERENCE_ENGINE, engine)
