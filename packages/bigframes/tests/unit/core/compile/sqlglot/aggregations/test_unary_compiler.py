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

from bigframes.core import agg_expressions, array_value, expression, identifiers, nodes
from bigframes.operations import aggregations as agg_ops
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def _apply_unary_op(obj: bpd.DataFrame, op: agg_ops.UnaryWindowOp, arg: str) -> str:
    agg_node = nodes.AggregateNode(
        obj._block.expr.node,
        aggregations=(
            (
                agg_expressions.UnaryAggregation(op, expression.deref(arg)),
                identifiers.ColumnId(arg + "_agg"),
            ),
        ),
    )
    result = array_value.ArrayValue(agg_node)

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_size(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, agg_ops.SizeUnaryOp(), "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_sum(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_unary_op(bf_df, agg_ops.SumOp(), "int64_col")

    snapshot.assert_match(sql, "out.sql")
