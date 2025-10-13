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
from bigframes.core import array_value, identifiers, nodes, ordering
from bigframes.operations import aggregations as agg_ops
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def _apply_ordered_unary_agg_ops(
    obj: bpd.DataFrame,
    ops_list: typing.Sequence[agg_exprs.UnaryAggregation],
    new_names: typing.Sequence[str],
    ordering_args: typing.Sequence[str],
) -> str:
    ordering_exprs = tuple(ordering.ascending_over(arg) for arg in ordering_args)
    aggs = [(op, identifiers.ColumnId(name)) for op, name in zip(ops_list, new_names)]

    agg_node = nodes.AggregateNode(
        obj._block.expr.node,
        aggregations=tuple(aggs),
        by_column_ids=(),
        order_by=ordering_exprs,
    )
    result = array_value.ArrayValue(agg_node)

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_array_agg(scalar_types_df: bpd.DataFrame, snapshot):
    # TODO: Verify "NULL LAST" syntax issue on Python < 3.12
    if sys.version_info < (3, 12):
        pytest.skip(
            "Skipping test due to inconsistent SQL formatting on Python < 3.12.",
        )

    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.ArrayAggOp().as_expr(col_name)
    sql = _apply_ordered_unary_agg_ops(
        bf_df, [agg_expr], [col_name], ordering_args=[col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_string_agg(scalar_types_df: bpd.DataFrame, snapshot):
    # TODO: Verify "NULL LAST" syntax issue on Python < 3.12
    if sys.version_info < (3, 12):
        pytest.skip(
            "Skipping test due to inconsistent SQL formatting on Python < 3.12.",
        )

    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    agg_expr = agg_ops.StringAggOp(sep=",").as_expr(col_name)
    sql = _apply_ordered_unary_agg_ops(
        bf_df, [agg_expr], [col_name], ordering_args=[col_name]
    )

    snapshot.assert_match(sql, "out.sql")
