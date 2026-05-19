# Copyright 2026 Google LLC
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

import abc
from typing import TYPE_CHECKING, Optional

from bigframes.core import bigframe_node
from bigframes.session import executor, semi_executor
import bigframes.core.rewrite.slices as slices_rewrite
from bigframes.core import nodes

if TYPE_CHECKING:
    import pyarrow as pa


class SubstraitConsumer(abc.ABC):
    """
    Interface for consuming Substrait plans and executing them.
    This acts as a plugin interface for different Substrait execution engines.
    """

    @abc.abstractmethod
    def consume(self, plan: bytes, tables: dict[str, pa.Table]) -> pa.Table:
        """
        Executes a Substrait plan and returns a PyArrow Table.

        Args:
            plan: The Substrait plan as bytes (usually a serialized Protobuf).
            tables: A dictionary of table names to PyArrow Tables for local data.

        Returns:
            A PyArrow Table containing the results.
        """
        pass


class DataFusionSubstraitConsumer(SubstraitConsumer):
    """
    Executes Substrait plans using Apache DataFusion.
    """

    def consume(self, plan_proto: bytes, tables: dict[str, pa.Table]) -> pa.Table:
        # Import datafusion lazily to avoid hard dependency
        try:
            import datafusion
        except ImportError:
            raise ImportError(
                "The datafusion package is required to use DataFusionSubstraitConsumer. "
                "Install it with `pip install datafusion`."
            )

        # Create a DataFusion context
        ctx = datafusion.SessionContext()

        for name, table in tables.items():
             df = ctx.from_arrow_table(table)
             ctx.register_table(name, df)
        
        # NOTE: The actual API for running Substrait in DataFusion python bindings may vary.
        # Assuming something like ctx.from_substrait(plan) or ctx.execute_substrait(plan).
        # We will need to verify this with the actual datafusion python package if available.
        # For now, we raise NotImplementedError if we cannot find the method, or try a likely one.
        
        import datafusion.substrait

        import substrait.plan_pb2 as plan_pb2
        from google.protobuf import json_format
        plan_obj = plan_pb2.Plan.FromString(plan_proto)
        print("DEBUG PLAN JSON:")
        print(json_format.MessageToJson(plan_obj))
        datafusion_substrait_plan = datafusion.substrait.Serde.deserialize_bytes(plan_proto)
        logical_plan = datafusion.substrait.Consumer.from_substrait_plan(ctx, datafusion_substrait_plan)
        df = ctx.create_dataframe_from_logical_plan(logical_plan)
        return df.to_arrow_table()


class SubstraitExecutor(semi_executor.SemiExecutor):
    """
    Executes plans by compiling them to Substrait and running them via a consumer.
    """

    def __init__(self, consumer: SubstraitConsumer):
        self._consumer = consumer
        # Lazy import to avoid circular dependencies
        from bigframes.core.compile.substrait.compiler import SubstraitCompiler
        self._compiler = SubstraitCompiler()

    def execute(
        self,
        plan: bigframe_node.BigFrameNode,
        ordered: bool,
        peek: Optional[int] = None,
    ) -> Optional[executor.ExecuteResult]:
        def resolve_promote_offsets(node: bigframe_node.BigFrameNode) -> bigframe_node.BigFrameNode:
             if isinstance(node, nodes.PromoteOffsetsNode):
                  res = self.execute(node.child, ordered=ordered)
                  if res is None:
                       return node
                  table = res.batches().to_arrow_table()
                  import pyarrow as pa
                  table = table.append_column(node.col_id.name, pa.array(range(len(table)), type=pa.int64()))
                  
                  from bigframes.core import local_data, identifiers
                  from bigframes.core.schema import ArraySchema, SchemaItem
                  import bigframes.dtypes
                  
                  schema_items = []
                  for col_name in table.column_names:
                       if col_name == node.col_id.name:
                            schema_items.append(SchemaItem(col_name, bigframes.dtypes.INT_DTYPE))
                       else:
                            schema_items.append(SchemaItem(col_name, node.child.schema.get_type(col_name)))
                  new_schema = ArraySchema(tuple(schema_items))
                  
                  scan_items = []
                  for col_name in table.column_names:
                       col_id = identifiers.ColumnId(col_name)
                       scan_items.append(nodes.ScanItem(col_id, col_name))
                  scan_list = nodes.ScanList(tuple(scan_items))
                  
                  session = None
                  for child_node in node.child.unique_nodes():
                       if isinstance(child_node, nodes.ReadLocalNode):
                            session = child_node.session
                            break
                  
                  managed_table = local_data.ManagedArrowTable.from_pyarrow(table, schema=new_schema)
                  new_node = nodes.ReadLocalNode(
                       local_data_source=managed_table,
                       scan_list=scan_list,
                       session=session,
                       offsets_col=None,
                  )
                  return new_node
             return node

        # 1. Rewrite all SliceNodes to standard Selection/Filter/Projection/PromoteOffsetsNodes
        plan = plan.bottom_up(slices_rewrite.rewrite_slice)

        # 2. Resolve all PromoteOffsetsNodes to concrete local tables
        plan = plan.bottom_up(resolve_promote_offsets)

        # 3. Wrap plan in a ResultNode to apply defer_order
        from bigframes.core import expression, rewrite
        output_cols = tuple((expression.DerefOp(id), id.name) for id in plan.ids)
        result_node = nodes.ResultNode(
            plan,
            output_cols=output_cols,
        )
        import typing
        result_node = typing.cast(nodes.ResultNode, rewrite.column_pruning(result_node))
        result_node = rewrite.defer_order(result_node, output_hidden_row_keys=False)

        rewritten_plan = result_node.child

        # 4. Apply outermost sorting if ordered
        if ordered and result_node.order_by and result_node.order_by.all_ordering_columns:
            rewritten_plan = nodes.OrderByNode(
                rewritten_plan,
                by=tuple(result_node.order_by.all_ordering_columns),
            )

        # 5. Project only the original output columns to preserve correct result schema
        original_ids = tuple(id for id in plan.ids)
        if rewritten_plan.ids != original_ids:
            rewritten_plan = nodes.SelectionNode(
                rewritten_plan,
                input_output_pairs=tuple(nodes.AliasedRef.identity(id) for id in original_ids)
            )

        if not self._can_execute(rewritten_plan):
            return None

        substrait_plan_proto = self._compiler.compile(rewritten_plan)
        if substrait_plan_proto is None:
            return None

        import google.protobuf.json_format as json_format
        from substrait.plan_pb2 import Plan
        plan_proto = Plan()
        plan_proto.ParseFromString(substrait_plan_proto)
        import os
        import uuid
        os.makedirs("/usr/local/google/home/tbergeron/src/google-cloud-python/packages/bigframes/scratch", exist_ok=True)
        filename = f"/usr/local/google/home/tbergeron/src/google-cloud-python/packages/bigframes/scratch/plan_{rewritten_plan.__class__.__name__}_{uuid.uuid4().hex[:8]}.json"
        with open(filename, "w") as f:
             f.write(json_format.MessageToJson(plan_proto))

        tables = {}
        for node in rewritten_plan.unique_nodes():
             if isinstance(node, nodes.ReadLocalNode):
                  table_name = f"table_{id(node)}"
                  table = node.local_data_source.data
                  table = table.select([item.source_id for item in node.scan_list.items])
                  table = table.rename_columns([item.id.sql for item in node.scan_list.items])
                  if node.offsets_col is not None:
                       from bigframes.core import pyarrow_utils
                       table = pyarrow_utils.append_offsets(table, node.offsets_col.sql)
                  tables[table_name] = table

        pa_table = self._consumer.consume(substrait_plan_proto, tables)

        # Sanitize pa_table: replace inf/nan/is_inf with null for INT_DTYPE columns
        import pyarrow.compute as pc
        import bigframes.dtypes as dtypes
        import pyarrow as pa
        sanitized_columns = []
        for col_name in pa_table.column_names:
             col_data = pa_table.column(col_name)
             try:
                  expected_dtype = rewritten_plan.schema.get_type(col_name)
             except ValueError:
                  expected_dtype = None
             
             if expected_dtype == dtypes.INT_DTYPE and pa.types.is_floating(col_data.type):
                  is_nan = pc.is_nan(col_data)
                  is_inf = pc.is_inf(col_data)
                  is_invalid = pc.or_(is_nan, is_inf)
                  null_val = pa.scalar(None, type=col_data.type)
                  col_data = pc.if_else(is_invalid, null_val, col_data)
             sanitized_columns.append(col_data)
        pa_table = pa.Table.from_arrays(sanitized_columns, names=pa_table.column_names)

        # Handle SliceNode post-processing
        for node in rewritten_plan.unique_nodes():
             if isinstance(node, nodes.SliceNode):
                  is_simple = (node.start is None or node.start >= 0) and (node.stop is None or node.stop >= 0) and (node.step is None or node.step == 1)
                  if not is_simple:
                       df = pa_table.to_pandas()
                       df = df.iloc[node.start:node.stop:node.step]
                       pa_table = pa.Table.from_pandas(df, schema=pa_table.schema)
        offset_cols = set()
        for node in rewritten_plan.unique_nodes():
             if isinstance(node, nodes.PromoteOffsetsNode):
                  offset_cols.add(node.col_id.name)
                  
        for col_name in pa_table.column_names:
             if col_name in offset_cols:
                  idx = pa_table.column_names.index(col_name)
                  pa_table = pa_table.set_column(idx, col_name, pa.array(range(len(pa_table)), type=pa.int64()))

        import sys
        sys.stderr.write(f"PA_TABLE ON EXECUTE:\n{pa_table.to_pandas()}\n")
        sys.stderr.flush()

        if peek is not None:
            pa_table = pa_table.slice(0, peek)

        return executor.LocalExecuteResult(
            data=pa_table,
            bf_schema=rewritten_plan.schema,
        )

    def _can_execute(self, plan: bigframe_node.BigFrameNode) -> bool:
        return self._compiler.can_compile(plan)
