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

import typing

import pytest

from bigframes.core import agg_expressions as agg_exprs
from bigframes.core import array_value, identifiers, nodes
from bigframes.operations import aggregations as agg_ops
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def _apply_unary_agg_ops(
    obj: bpd.DataFrame,
    ops_list: typing.Sequence[agg_exprs.UnaryAggregation],
    new_names: typing.Sequence[str],
) -> str:
    aggs = [(op, identifiers.ColumnId(name)) for op, name in zip(ops_list, new_names)]

    agg_node = nodes.AggregateNode(obj._block.expr.node, aggregations=tuple(aggs))
    result = array_value.ArrayValue(agg_node)

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_count(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.CountOp().as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_max(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.MaxOp().as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_min(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.MinOp().as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_sum(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]
    agg_ops_map = {
        "int64_col": agg_ops.SumOp().as_expr("int64_col"),
        "bool_col": agg_ops.SumOp().as_expr("bool_col"),
    }
    sql = _apply_unary_agg_ops(
        bf_df, list(agg_ops_map.values()), list(agg_ops_map.keys())
    )

    snapshot.assert_match(sql, "out.sql")
