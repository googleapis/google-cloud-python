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
from bigframes.core import array_value, identifiers, nodes, ordering, window_spec
from bigframes.operations import aggregations as agg_ops
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def _apply_nullary_agg_ops(
    obj: bpd.DataFrame,
    ops_list: typing.Sequence[agg_exprs.NullaryAggregation],
    new_names: typing.Sequence[str],
) -> str:
    aggs = [(op, identifiers.ColumnId(name)) for op, name in zip(ops_list, new_names)]

    agg_node = nodes.AggregateNode(obj._block.expr.node, aggregations=tuple(aggs))
    result = array_value.ArrayValue(agg_node)

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def _apply_nullary_window_op(
    obj: bpd.DataFrame,
    op: agg_exprs.NullaryAggregation,
    window_spec: window_spec.WindowSpec,
    new_name: str,
) -> str:
    win_node = nodes.WindowOpNode(
        obj._block.expr.node,
        expression=op,
        window_spec=window_spec,
        output_name=identifiers.ColumnId(new_name),
    )
    result = array_value.ArrayValue(win_node).select_columns([new_name])

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_size(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df
    agg_expr = agg_ops.SizeOp().as_expr()
    sql = _apply_nullary_agg_ops(bf_df, [agg_expr], ["size"])

    snapshot.assert_match(sql, "out.sql")


def test_row_number(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df
    agg_expr = agg_exprs.NullaryAggregation(agg_ops.RowNumberOp())
    window = window_spec.WindowSpec()
    sql = _apply_nullary_window_op(bf_df, agg_expr, window, "row_number")

    snapshot.assert_match(sql, "out.sql")


def test_row_number_with_window(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name, "int64_too"]]
    agg_expr = agg_exprs.NullaryAggregation(agg_ops.RowNumberOp())

    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    # window = window_spec.unbound(ordering=(ordering.ascending_over(col_name),ordering.ascending_over("int64_too")))
    sql = _apply_nullary_window_op(bf_df, agg_expr, window, "row_number")

    snapshot.assert_match(sql, "out.sql")
