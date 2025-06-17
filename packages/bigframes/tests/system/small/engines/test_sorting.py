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

from bigframes.core import array_value, nodes, ordering
import bigframes.operations as bf_ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_reverse(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    node = apply_reverse(scalars_array_value.node)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_double_reverse(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    node = apply_reverse(scalars_array_value.node)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
@pytest.mark.parametrize(
    "sort_col",
    [
        "bool_col",
        "int64_col",
        "bytes_col",
        "date_col",
        "datetime_col",
        "int64_col",
        "int64_too",
        "numeric_col",
        "float64_col",
        "string_col",
        "time_col",
        "timestamp_col",
    ],
)
def test_engines_sort_over_column(
    scalars_array_value: array_value.ArrayValue, engine, sort_col
):
    node = apply_reverse(scalars_array_value.node)
    ORDER_EXPRESSIONS = (ordering.descending_over(sort_col, nulls_last=False),)
    node = nodes.OrderByNode(node, ORDER_EXPRESSIONS)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_sort_multi_column_refs(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    node = scalars_array_value.node
    ORDER_EXPRESSIONS = (
        ordering.ascending_over("bool_col", nulls_last=False),
        ordering.descending_over("int64_col"),
    )
    node = nodes.OrderByNode(node, ORDER_EXPRESSIONS)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars"], indirect=True)
def test_polars_engines_skips_unrecognized_order_expr(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    node = scalars_array_value.node
    ORDER_EXPRESSIONS = (
        ordering.OrderingExpression(
            scalar_expression=bf_ops.sin_op.as_expr("float_col")
        ),
    )
    node = nodes.OrderByNode(node, ORDER_EXPRESSIONS)
    assert engine.execute(node, ordered=True) is None


def apply_reverse(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    return nodes.ReversedNode(node)
