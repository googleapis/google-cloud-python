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
from __future__ import annotations

import itertools
from typing import Optional, TYPE_CHECKING

from bigframes.core import (
    agg_expressions,
    array_value,
    bigframe_node,
    expression,
    nodes,
)
import bigframes.operations
from bigframes.operations import aggregations as agg_ops
from bigframes.operations import (
    bool_ops,
    comparison_ops,
    date_ops,
    frequency_ops,
    generic_ops,
    numeric_ops,
    string_ops,
)
import bigframes.operations.json_ops as json_ops
from bigframes.session import executor, semi_executor

if TYPE_CHECKING:
    import polars as pl

# Polars executor can execute more node types, but these are the validated ones
_COMPATIBLE_NODES = (
    nodes.ReadLocalNode,
    nodes.OrderByNode,
    nodes.ReversedNode,
    nodes.SelectionNode,
    nodes.ProjectionNode,
    nodes.SliceNode,
    nodes.AggregateNode,
    nodes.FilterNode,
    nodes.ConcatNode,
    nodes.JoinNode,
    nodes.InNode,
    nodes.PromoteOffsetsNode,
)

_COMPATIBLE_SCALAR_OPS = (
    bool_ops.AndOp,
    bool_ops.OrOp,
    bool_ops.XorOp,
    comparison_ops.EqOp,
    comparison_ops.EqNullsMatchOp,
    comparison_ops.NeOp,
    comparison_ops.LtOp,
    comparison_ops.GtOp,
    comparison_ops.LeOp,
    comparison_ops.GeOp,
    date_ops.YearOp,
    date_ops.QuarterOp,
    date_ops.MonthOp,
    date_ops.DayOfWeekOp,
    date_ops.DayOp,
    date_ops.IsoYearOp,
    date_ops.IsoWeekOp,
    date_ops.IsoDayOp,
    frequency_ops.FloorDtOp,
    numeric_ops.AddOp,
    numeric_ops.SubOp,
    numeric_ops.MulOp,
    numeric_ops.DivOp,
    numeric_ops.FloorDivOp,
    numeric_ops.ModOp,
    generic_ops.AsTypeOp,
    generic_ops.WhereOp,
    generic_ops.CoalesceOp,
    generic_ops.FillNaOp,
    generic_ops.CaseWhenOp,
    generic_ops.InvertOp,
    generic_ops.IsInOp,
    generic_ops.IsNullOp,
    generic_ops.NotNullOp,
    string_ops.StartsWithOp,
    string_ops.EndsWithOp,
    string_ops.StrContainsOp,
    string_ops.StrContainsRegexOp,
    json_ops.JSONDecode,
)
_COMPATIBLE_AGG_OPS = (
    agg_ops.SizeOp,
    agg_ops.SizeUnaryOp,
    agg_ops.MinOp,
    agg_ops.MaxOp,
    agg_ops.SumOp,
    agg_ops.MeanOp,
    agg_ops.CountOp,
    agg_ops.VarOp,
    agg_ops.PopVarOp,
    agg_ops.StdOp,
)


def _get_expr_ops(expr: expression.Expression) -> set[bigframes.operations.ScalarOp]:
    if isinstance(expr, expression.OpExpression):
        return set(itertools.chain.from_iterable(map(_get_expr_ops, expr.children)))
    return set()


def _is_node_polars_executable(node: nodes.BigFrameNode):
    if not isinstance(node, _COMPATIBLE_NODES):
        return False
    for expr in node._node_expressions:
        if isinstance(expr, agg_expressions.Aggregation):
            if not type(expr.op) in _COMPATIBLE_AGG_OPS:
                return False
        if isinstance(expr, expression.Expression):
            if not set(map(type, _get_expr_ops(expr))).issubset(_COMPATIBLE_SCALAR_OPS):
                return False
    return True


class PolarsExecutor(semi_executor.SemiExecutor):
    def __init__(self):
        # This will error out if polars is not installed
        from bigframes.core.compile.polars import PolarsCompiler

        self._compiler = PolarsCompiler()

    def execute(
        self,
        plan: bigframe_node.BigFrameNode,
        ordered: bool,
        peek: Optional[int] = None,
    ) -> Optional[executor.ExecuteResult]:
        if not self._can_execute(plan):
            return None
        # Note: Ignoring ordered flag, as just executing totally ordered is fine.
        try:
            lazy_frame: pl.LazyFrame = self._compiler.compile(
                array_value.ArrayValue(plan).node
            )
        except Exception:
            return None
        if peek is not None:
            lazy_frame = lazy_frame.limit(peek)
        pa_table = lazy_frame.collect().to_arrow()
        return executor.LocalExecuteResult(
            data=pa_table,
            bf_schema=plan.schema,
        )

    def _can_execute(self, plan: bigframe_node.BigFrameNode):
        return all(_is_node_polars_executable(node) for node in plan.unique_nodes())
