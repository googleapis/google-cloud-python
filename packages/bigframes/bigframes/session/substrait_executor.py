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
import asyncio
from typing import TYPE_CHECKING, Optional, cast

import bigframes.core.compile.substrait.compiler as substrait_compiler
import bigframes.core.rewrite as rewrite
from bigframes.core import bigframe_node, nodes
from bigframes.session import executor, semi_executor

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

        ctx = datafusion.SessionContext()

        for name, table in tables.items():
            df = ctx.from_arrow_table(table)
            ctx.register_table(name, df)

        import datafusion.substrait

        datafusion_substrait_plan = datafusion.substrait.Serde.deserialize_bytes(
            plan_proto
        )
        logical_plan = datafusion.substrait.Consumer.from_substrait_plan(
            ctx, datafusion_substrait_plan
        )
        df = ctx.create_dataframe_from_logical_plan(logical_plan)
        return df.to_arrow_table()


class AceroSubstraitConsumer(SubstraitConsumer):
    """
    Executes Substrait plans using Apache Arrow Acero.
    """

    def consume(self, plan_proto: bytes, tables: dict[str, pa.Table]) -> pa.Table:
        import pyarrow.substrait as pa_substrait

        def provide_table(name: list[str], schema: pa.Schema) -> pa.Table:
            return tables[name[0]]

        batch_reader = pa_substrait.run_query(plan_proto, table_provider=provide_table)
        return batch_reader.read_all()


class SubstraitExecutor(semi_executor.SemiExecutor):
    """
    Executes plans by compiling them to Substrait and running them via a consumer.
    """

    def __init__(
        self,
        consumer: SubstraitConsumer,
        compiler: substrait_compiler.SubstraitCompiler,
    ):
        self._consumer = consumer
        self._compiler = compiler

    @classmethod
    def default_for_engine(cls, engine_name: str) -> SubstraitExecutor:
        if engine_name == "acero":
            return cls(
                AceroSubstraitConsumer(),
                substrait_compiler.SubstraitCompiler(
                    duration_type="int", use_precision_types=False
                ),
            )
        elif engine_name == "datafusion":
            return cls(
                DataFusionSubstraitConsumer(),
                substrait_compiler.SubstraitCompiler(duration_type="int"),
            )
        else:
            raise ValueError(f"Unknown engine: {engine_name}")

    async def execute(
        self,
        plan: bigframe_node.BigFrameNode,
        ordered: bool,
        peek: Optional[int] = None,
    ) -> Optional[executor.ExecuteResult]:
        plan = plan.bottom_up(rewrite.rewrite_slice)
        # Only needed for acero technically, datafusion can handle timedeltas
        plan = plan.bottom_up(rewrite.rewrite_timedelta_expressions)

        from bigframes.core import expression

        output_cols = tuple((expression.DerefOp(id), id.name) for id in plan.ids)
        result_node = nodes.ResultNode(
            plan,
            output_cols=output_cols,
        )
        result_node = cast(nodes.ResultNode, rewrite.column_pruning(result_node))
        result_node = rewrite.defer_order(result_node, output_hidden_row_keys=False)

        rewritten_plan = result_node.child

        if (
            ordered
            and result_node.order_by
            and result_node.order_by.all_ordering_columns
        ):
            rewritten_plan = nodes.OrderByNode(
                rewritten_plan,
                by=tuple(result_node.order_by.all_ordering_columns),
            )

        original_ids = tuple(id for id in plan.ids)
        if rewritten_plan.ids != original_ids:
            rewritten_plan = nodes.SelectionNode(
                rewritten_plan,
                input_output_pairs=tuple(
                    nodes.AliasedRef.identity(id) for id in original_ids
                ),
            )

        if not self._can_execute(rewritten_plan):
            return None

        substrait_plan_proto = self._compiler.compile(rewritten_plan)
        if substrait_plan_proto is None:
            return None

        tables = {}
        for node in rewritten_plan.unique_nodes():
            if isinstance(node, nodes.ReadLocalNode):
                table_name = f"table_{id(node)}"
                table = node.local_data_source.to_pyarrow_table(duration_type="int")
                table = table.select([item.source_id for item in node.scan_list.items])
                table = table.rename_columns(
                    [item.id.sql for item in node.scan_list.items]
                )
                if node.offsets_col is not None:
                    from bigframes.core import pyarrow_utils

                    table = pyarrow_utils.append_offsets(table, node.offsets_col.sql)
                tables[table_name] = table

        pa_table = await asyncio.to_thread(
            self._consumer.consume, substrait_plan_proto, tables
        )

        if peek is not None:
            pa_table = pa_table.slice(0, peek)

        return executor.LocalExecuteResult(
            data=pa_table,
            bf_schema=rewritten_plan.schema,
        )

    def _can_execute(self, plan: bigframe_node.BigFrameNode) -> bool:
        return self._compiler.can_compile(plan)
