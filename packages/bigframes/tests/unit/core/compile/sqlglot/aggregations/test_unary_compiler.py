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

import sys
import typing

import pytest

from bigframes.core import agg_expressions as agg_exprs
from bigframes.core import (
    array_value,
    expression,
    identifiers,
    nodes,
    ordering,
    window_spec,
)
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


def _apply_unary_window_op(
    obj: bpd.DataFrame,
    op: agg_exprs.UnaryAggregation,
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


def test_all(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "bool_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.AllOp().as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_approx_quartiles(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_ops_map = {
        "q1": agg_ops.ApproxQuartilesOp(quartile=1).as_expr(col_name),
        "q2": agg_ops.ApproxQuartilesOp(quartile=2).as_expr(col_name),
        "q3": agg_ops.ApproxQuartilesOp(quartile=3).as_expr(col_name),
    }
    sql = _apply_unary_agg_ops(
        bf_df, list(agg_ops_map.values()), list(agg_ops_map.keys())
    )

    snapshot.assert_match(sql, "out.sql")


def test_approx_top_count(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.ApproxTopCountOp(number=10).as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_any_value(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.AnyValueOp().as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_count(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.CountOp().as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_dense_rank(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_exprs.UnaryAggregation(
        agg_ops.DenseRankOp(), expression.deref(col_name)
    )
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    sql = _apply_unary_window_op(bf_df, agg_expr, window, "agg_int64")

    snapshot.assert_match(sql, "out.sql")


def test_date_series_diff(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "date_col"
    bf_df = scalar_types_df[[col_name]]
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    op = agg_exprs.UnaryAggregation(
        agg_ops.DateSeriesDiffOp(periods=1), expression.deref(col_name)
    )
    sql = _apply_unary_window_op(bf_df, op, window, "diff_date")
    snapshot.assert_match(sql, "out.sql")


def test_diff(scalar_types_df: bpd.DataFrame, snapshot):
    # Test integer
    int_col = "int64_col"
    bf_df_int = scalar_types_df[[int_col]]
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(int_col),))
    int_op = agg_exprs.UnaryAggregation(
        agg_ops.DiffOp(periods=1), expression.deref(int_col)
    )
    int_sql = _apply_unary_window_op(bf_df_int, int_op, window, "diff_int")
    snapshot.assert_match(int_sql, "diff_int.sql")

    # Test boolean
    bool_col = "bool_col"
    bf_df_bool = scalar_types_df[[bool_col]]
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(bool_col),))
    bool_op = agg_exprs.UnaryAggregation(
        agg_ops.DiffOp(periods=1), expression.deref(bool_col)
    )
    bool_sql = _apply_unary_window_op(bf_df_bool, bool_op, window, "diff_bool")
    snapshot.assert_match(bool_sql, "diff_bool.sql")


def test_first(scalar_types_df: bpd.DataFrame, snapshot):
    if sys.version_info < (3, 12):
        pytest.skip(
            "Skipping test due to inconsistent SQL formatting on Python < 3.12.",
        )
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_exprs.UnaryAggregation(agg_ops.FirstOp(), expression.deref(col_name))
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    sql = _apply_unary_window_op(bf_df, agg_expr, window, "agg_int64")

    snapshot.assert_match(sql, "out.sql")


def test_first_non_null(scalar_types_df: bpd.DataFrame, snapshot):
    if sys.version_info < (3, 12):
        pytest.skip(
            "Skipping test due to inconsistent SQL formatting on Python < 3.12.",
        )
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_exprs.UnaryAggregation(
        agg_ops.FirstNonNullOp(), expression.deref(col_name)
    )
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    sql = _apply_unary_window_op(bf_df, agg_expr, window, "agg_int64")

    snapshot.assert_match(sql, "out.sql")


def test_last(scalar_types_df: bpd.DataFrame, snapshot):
    if sys.version_info < (3, 12):
        pytest.skip(
            "Skipping test due to inconsistent SQL formatting on Python < 3.12.",
        )
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_exprs.UnaryAggregation(agg_ops.LastOp(), expression.deref(col_name))
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    sql = _apply_unary_window_op(bf_df, agg_expr, window, "agg_int64")

    snapshot.assert_match(sql, "out.sql")


def test_last_non_null(scalar_types_df: bpd.DataFrame, snapshot):
    if sys.version_info < (3, 12):
        pytest.skip(
            "Skipping test due to inconsistent SQL formatting on Python < 3.12.",
        )
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_exprs.UnaryAggregation(
        agg_ops.LastNonNullOp(), expression.deref(col_name)
    )
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    sql = _apply_unary_window_op(bf_df, agg_expr, window, "agg_int64")

    snapshot.assert_match(sql, "out.sql")


def test_max(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.MaxOp().as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_mean(scalar_types_df: bpd.DataFrame, snapshot):
    col_names = ["int64_col", "bool_col", "duration_col"]
    bf_df = scalar_types_df[col_names]
    bf_df["duration_col"] = bpd.to_timedelta(bf_df["duration_col"], unit="us")

    # The `to_timedelta` creates a new mapping for the column id.
    col_names.insert(0, "rowindex")
    name2id = {
        col_name: col_id
        for col_name, col_id in zip(col_names, bf_df._block.expr.column_ids)
    }

    agg_ops_map = {
        "int64_col": agg_ops.MeanOp().as_expr(name2id["int64_col"]),
        "bool_col": agg_ops.MeanOp().as_expr(name2id["bool_col"]),
        "duration_col": agg_ops.MeanOp().as_expr(name2id["duration_col"]),
        "int64_col_w_floor": agg_ops.MeanOp(should_floor_result=True).as_expr(
            name2id["int64_col"]
        ),
    }
    sql = _apply_unary_agg_ops(
        bf_df, list(agg_ops_map.values()), list(agg_ops_map.keys())
    )

    snapshot.assert_match(sql, "out.sql")


def test_median(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df
    ops_map = {
        "int64_col": agg_ops.MedianOp().as_expr("int64_col"),
        "date_col": agg_ops.MedianOp().as_expr("date_col"),
        "string_col": agg_ops.MedianOp().as_expr("string_col"),
    }
    sql = _apply_unary_agg_ops(bf_df, list(ops_map.values()), list(ops_map.keys()))

    snapshot.assert_match(sql, "out.sql")


def test_min(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.MinOp().as_expr(col_name)
    sql = _apply_unary_agg_ops(bf_df, [agg_expr], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_quantile(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_ops_map = {
        "quantile": agg_ops.QuantileOp(q=0.5).as_expr(col_name),
        "quantile_floor": agg_ops.QuantileOp(q=0.5, should_floor_result=True).as_expr(
            col_name
        ),
    }
    sql = _apply_unary_agg_ops(
        bf_df, list(agg_ops_map.values()), list(agg_ops_map.keys())
    )

    snapshot.assert_match(sql, "out.sql")


def test_rank(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_exprs.UnaryAggregation(agg_ops.RankOp(), expression.deref(col_name))

    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    sql = _apply_unary_window_op(bf_df, agg_expr, window, "agg_int64")

    snapshot.assert_match(sql, "out.sql")


def test_shift(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))

    # Test lag
    lag_op = agg_exprs.UnaryAggregation(
        agg_ops.ShiftOp(periods=1), expression.deref(col_name)
    )
    lag_sql = _apply_unary_window_op(bf_df, lag_op, window, "lag")
    snapshot.assert_match(lag_sql, "lag.sql")

    # Test lead
    lead_op = agg_exprs.UnaryAggregation(
        agg_ops.ShiftOp(periods=-1), expression.deref(col_name)
    )
    lead_sql = _apply_unary_window_op(bf_df, lead_op, window, "lead")
    snapshot.assert_match(lead_sql, "lead.sql")

    # Test no-op
    noop_op = agg_exprs.UnaryAggregation(
        agg_ops.ShiftOp(periods=0), expression.deref(col_name)
    )
    noop_sql = _apply_unary_window_op(bf_df, noop_op, window, "noop")
    snapshot.assert_match(noop_sql, "noop.sql")


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


def test_time_series_diff(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    window = window_spec.WindowSpec(ordering=(ordering.ascending_over(col_name),))
    op = agg_exprs.UnaryAggregation(
        agg_ops.TimeSeriesDiffOp(periods=1), expression.deref(col_name)
    )
    sql = _apply_unary_window_op(bf_df, op, window, "diff_time")
    snapshot.assert_match(sql, "out.sql")
