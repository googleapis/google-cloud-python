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


def _apply_binary_agg_ops(
    obj: bpd.DataFrame,
    ops_list: typing.Sequence[agg_exprs.BinaryAggregation],
    new_names: typing.Sequence[str],
) -> str:
    aggs = [(op, identifiers.ColumnId(name)) for op, name in zip(ops_list, new_names)]

    agg_node = nodes.AggregateNode(obj._block.expr.node, aggregations=tuple(aggs))
    result = array_value.ArrayValue(agg_node)

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_corr(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "float64_col"]]
    agg_expr = agg_ops.CorrOp().as_expr("int64_col", "float64_col")
    sql = _apply_binary_agg_ops(bf_df, [agg_expr], ["corr_col"])

    snapshot.assert_match(sql, "out.sql")


def test_cov(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "float64_col"]]
    agg_expr = agg_ops.CovOp().as_expr("int64_col", "float64_col")
    sql = _apply_binary_agg_ops(bf_df, [agg_expr], ["cov_col"])

    snapshot.assert_match(sql, "out.sql")
