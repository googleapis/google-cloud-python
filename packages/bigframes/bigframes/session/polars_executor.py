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

import pyarrow as pa

from bigframes.core import array_value, bigframe_node, expression, local_data, nodes
import bigframes.operations
from bigframes.operations import aggregations as agg_ops
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
)

_COMPATIBLE_SCALAR_OPS = (
    bigframes.operations.eq_op,
    bigframes.operations.eq_null_match_op,
    bigframes.operations.ne_op,
    bigframes.operations.gt_op,
    bigframes.operations.lt_op,
    bigframes.operations.ge_op,
    bigframes.operations.le_op,
)
_COMPATIBLE_AGG_OPS = (
    agg_ops.SizeOp,
    agg_ops.SizeUnaryOp,
    agg_ops.MinOp,
    agg_ops.MaxOp,
    agg_ops.SumOp,
    agg_ops.MeanOp,
    agg_ops.CountOp,
)


def _get_expr_ops(expr: expression.Expression) -> set[bigframes.operations.ScalarOp]:
    if isinstance(expr, expression.OpExpression):
        return set(itertools.chain.from_iterable(map(_get_expr_ops, expr.children)))
    return set()


def _is_node_polars_executable(node: nodes.BigFrameNode):
    if not isinstance(node, _COMPATIBLE_NODES):
        return False
    for expr in node._node_expressions:
        if isinstance(expr, expression.Aggregation):
            if not type(expr.op) in _COMPATIBLE_AGG_OPS:
                return False
        if isinstance(expr, expression.Expression):
            if not _get_expr_ops(expr).issubset(_COMPATIBLE_SCALAR_OPS):
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
        return executor.ExecuteResult(
            _arrow_batches=iter(map(self._adapt_batch, pa_table.to_batches())),
            schema=plan.schema,
            total_bytes=pa_table.nbytes,
            total_rows=pa_table.num_rows,
        )

    def _can_execute(self, plan: bigframe_node.BigFrameNode):
        return all(_is_node_polars_executable(node) for node in plan.unique_nodes())

    def _adapt_array(self, array: pa.Array) -> pa.Array:
        target_type = local_data.logical_type_replacements(array.type)
        if target_type != array.type:
            return array.cast(target_type)
        return array

    def _adapt_batch(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        new_arrays = [self._adapt_array(arr) for arr in batch.columns]
        return pa.RecordBatch.from_arrays(new_arrays, names=batch.column_names)
