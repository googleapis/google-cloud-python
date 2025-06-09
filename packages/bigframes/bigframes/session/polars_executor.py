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

from typing import Optional, TYPE_CHECKING

import pyarrow as pa

from bigframes.core import array_value, bigframe_node, local_data, nodes
from bigframes.session import executor, semi_executor

if TYPE_CHECKING:
    import polars as pl


_COMPATIBLE_NODES = (
    nodes.ReadLocalNode,
    nodes.OrderByNode,
    nodes.ReversedNode,
    nodes.SelectionNode,
    nodes.FilterNode,  # partial support
    nodes.ProjectionNode,  # partial support
)


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
                array_value.ArrayValue(plan)
            )
        except Exception:
            return None
        if peek is not None:
            lazy_frame = lazy_frame.limit(peek)
        pa_table = lazy_frame.collect().to_arrow()
        return executor.ExecuteResult(
            arrow_batches=iter(map(self._adapt_batch, pa_table.to_batches())),
            schema=plan.schema,
            total_bytes=pa_table.nbytes,
            total_rows=pa_table.num_rows,
        )

    def _can_execute(self, plan: bigframe_node.BigFrameNode):
        return all(isinstance(node, _COMPATIBLE_NODES) for node in plan.unique_nodes())

    def _adapt_array(self, array: pa.Array) -> pa.Array:
        target_type = local_data.logical_type_replacements(array.type)
        if target_type != array.type:
            return array.cast(target_type)
        return array

    def _adapt_batch(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        new_arrays = [self._adapt_array(arr) for arr in batch.columns]
        return pa.RecordBatch.from_arrays(new_arrays, names=batch.column_names)
