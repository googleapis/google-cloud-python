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

    def consume(self, plan: bytes, tables: dict[str, pa.Table]) -> pa.Table:
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

        json_str = plan.decode('utf-8')
        plan_obj = datafusion.substrait.Plan.from_json(json_str)
        print("DEBUG RE-SERIALIZED JSON SUBSTRAIT PLAN:")
        print(plan_obj.to_json())
        logical_plan = datafusion.substrait.Consumer.from_substrait_plan(ctx, plan_obj)
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
        rewritten_plan = plan.bottom_up(slices_rewrite.rewrite_slice)
        
        if not self._can_execute(rewritten_plan):
            return None

        substrait_plan = self._compiler.compile(rewritten_plan)

        if substrait_plan is None:
            return None

        tables = {}
        for node in rewritten_plan.unique_nodes():
             if isinstance(node, nodes.ReadLocalNode):
                  table_name = f"table_{node.local_data_source.id.hex}"
                  tables[table_name] = node.local_data_source.data

        pa_table = self._consumer.consume(substrait_plan, tables)

        if peek is not None:
            pa_table = pa_table.slice(0, peek)

        return executor.LocalExecuteResult(
            data=pa_table,
            bf_schema=rewritten_plan.schema,
        )

    def _can_execute(self, plan: bigframe_node.BigFrameNode) -> bool:
        return self._compiler.can_compile(plan)
