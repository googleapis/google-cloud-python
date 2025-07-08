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

from bigframes.core import array_value, expression, identifiers, nodes
import bigframes.operations.aggregations as agg_ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


def apply_agg_to_all_valid(
    array: array_value.ArrayValue, op: agg_ops.UnaryAggregateOp, excluded_cols=[]
) -> array_value.ArrayValue:
    """
    Apply the aggregation to every column in the array that has a compatible datatype.
    """
    exprs_by_name = []
    for arg in array.column_ids:
        if arg in excluded_cols:
            continue
        try:
            _ = op.output_type(array.get_column_type(arg))
            expr = expression.UnaryAggregation(op, expression.deref(arg))
            name = f"{arg}-{op.name}"
            exprs_by_name.append((expr, name))
        except TypeError:
            continue
    assert len(exprs_by_name) > 0
    new_arr = array.aggregate(exprs_by_name)
    return new_arr


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_aggregate_size(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    node = nodes.AggregateNode(
        scalars_array_value.node,
        aggregations=(
            (
                expression.NullaryAggregation(agg_ops.SizeOp()),
                identifiers.ColumnId("size_op"),
            ),
            (
                expression.UnaryAggregation(
                    agg_ops.SizeUnaryOp(), expression.deref("string_col")
                ),
                identifiers.ColumnId("unary_size_op"),
            ),
        ),
    )
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
@pytest.mark.parametrize(
    "op",
    [agg_ops.min_op, agg_ops.max_op, agg_ops.mean_op, agg_ops.sum_op, agg_ops.count_op],
)
def test_engines_unary_aggregates(
    scalars_array_value: array_value.ArrayValue,
    engine,
    op,
):
    node = apply_agg_to_all_valid(scalars_array_value, op).node
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
@pytest.mark.parametrize(
    "grouping_cols",
    [
        ["bool_col"],
        ["string_col", "int64_col"],
        ["date_col"],
        ["datetime_col"],
        ["timestamp_col"],
        ["bytes_col"],
    ],
)
def test_engines_grouped_aggregate(
    scalars_array_value: array_value.ArrayValue, engine, grouping_cols
):
    node = nodes.AggregateNode(
        scalars_array_value.node,
        aggregations=(
            (
                expression.NullaryAggregation(agg_ops.SizeOp()),
                identifiers.ColumnId("size_op"),
            ),
            (
                expression.UnaryAggregation(
                    agg_ops.SizeUnaryOp(), expression.deref("string_col")
                ),
                identifiers.ColumnId("unary_size_op"),
            ),
        ),
        by_column_ids=tuple(expression.deref(id) for id in grouping_cols),
    )
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)
