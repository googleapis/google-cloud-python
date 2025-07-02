# Copyright 2023 Google LLC
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

import dataclasses
import functools
import typing

from google.cloud import bigquery
import sqlglot.expressions as sge

from bigframes.core import expression, guid, identifiers, nodes, pyarrow_utils, rewrite
from bigframes.core.compile import configs
from bigframes.core.compile.sqlglot.expressions import typed_expr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
import bigframes.core.ordering as bf_ordering
from bigframes.core.rewrite import schema_binding


class SQLGlotCompiler:
    """Compiles BigFrame nodes into SQL using SQLGlot."""

    uid_gen: guid.SequentialUIDGenerator
    """Generator for unique identifiers."""

    def __init__(self):
        self.uid_gen = guid.SequentialUIDGenerator()

    def compile(
        self,
        node: nodes.BigFrameNode,
        *,
        ordered: bool = True,
        limit: typing.Optional[int] = None,
    ) -> str:
        """Compiles node into sql where rows are sorted with ORDER BY."""
        request = configs.CompileRequest(node, sort_rows=ordered, peek_count=limit)
        return self._compile_sql(request).sql

    def compile_raw(
        self,
        node: nodes.BigFrameNode,
    ) -> typing.Tuple[
        str, typing.Sequence[bigquery.SchemaField], bf_ordering.RowOrdering
    ]:
        """Compiles node into sql that exposes all columns, including hidden
        ordering-only columns."""
        request = configs.CompileRequest(
            node, sort_rows=False, materialize_all_order_keys=True
        )
        result = self._compile_sql(request)
        assert result.row_order is not None
        return result.sql, result.sql_schema, result.row_order

    def _compile_sql(self, request: configs.CompileRequest) -> configs.CompileResult:
        output_names = tuple(
            (expression.DerefOp(id), id.sql) for id in request.node.ids
        )
        result_node = nodes.ResultNode(
            request.node,
            output_cols=output_names,
            limit=request.peek_count,
        )
        if request.sort_rows:
            # Can only pullup slice if we are doing ORDER BY in outermost SELECT
            # Need to do this before replacing unsupported ops, as that will rewrite slice ops
            result_node = rewrite.pull_up_limits(result_node)
        result_node = _replace_unsupported_ops(result_node)
        # prune before pulling up order to avoid unnnecessary row_number() ops
        result_node = typing.cast(nodes.ResultNode, rewrite.column_pruning(result_node))
        result_node = rewrite.defer_order(
            result_node, output_hidden_row_keys=request.materialize_all_order_keys
        )
        if request.sort_rows:
            result_node = typing.cast(
                nodes.ResultNode, rewrite.column_pruning(result_node)
            )
            result_node = self._remap_variables(result_node)
            result_node = typing.cast(
                nodes.ResultNode, rewrite.defer_selection(result_node)
            )
            sql = self._compile_result_node(result_node)
            return configs.CompileResult(
                sql, result_node.schema.to_bigquery(), result_node.order_by
            )

        ordering: typing.Optional[bf_ordering.RowOrdering] = result_node.order_by
        result_node = dataclasses.replace(result_node, order_by=None)
        result_node = typing.cast(nodes.ResultNode, rewrite.column_pruning(result_node))

        result_node = self._remap_variables(result_node)
        result_node = typing.cast(
            nodes.ResultNode, rewrite.defer_selection(result_node)
        )
        sql = self._compile_result_node(result_node)
        # Return the ordering iff no extra columns are needed to define the row order
        if ordering is not None:
            output_order = (
                ordering
                if ordering.referenced_columns.issubset(result_node.ids)
                else None
            )
        assert (not request.materialize_all_order_keys) or (output_order is not None)
        return configs.CompileResult(
            sql, result_node.schema.to_bigquery(), output_order
        )

    def _remap_variables(self, node: nodes.ResultNode) -> nodes.ResultNode:
        """Remaps `ColumnId`s in the BFET of a `ResultNode` to produce deterministic UIDs."""

        result_node, _ = rewrite.remap_variables(
            node, map(identifiers.ColumnId, self.uid_gen.get_uid_stream("bfcol_"))
        )
        return typing.cast(nodes.ResultNode, result_node)

    def _compile_result_node(self, root: nodes.ResultNode) -> str:
        # Have to bind schema as the final step before compilation.
        root = typing.cast(nodes.ResultNode, schema_binding.bind_schema_to_tree(root))
        selected_cols: tuple[tuple[str, sge.Expression], ...] = tuple(
            (name, scalar_compiler.compile_scalar_expression(ref))
            for ref, name in root.output_cols
        )
        sqlglot_ir = self.compile_node(root.child).select(selected_cols)

        if root.order_by is not None:
            ordering_cols = tuple(
                sge.Ordered(
                    this=scalar_compiler.compile_scalar_expression(
                        ordering.scalar_expression
                    ),
                    desc=ordering.direction.is_ascending is False,
                    nulls_first=ordering.na_last is False,
                )
                for ordering in root.order_by.all_ordering_columns
            )
            sqlglot_ir = sqlglot_ir.order_by(ordering_cols)

        if root.limit is not None:
            sqlglot_ir = sqlglot_ir.limit(root.limit)

        return sqlglot_ir.sql

    @functools.lru_cache(maxsize=5000)
    def compile_node(self, node: nodes.BigFrameNode) -> ir.SQLGlotIR:
        """Compiles node into CompileArrayValue. Caches result."""
        return node.reduce_up(
            lambda node, children: self._compile_node(node, *children)
        )

    @functools.singledispatchmethod
    def _compile_node(
        self, node: nodes.BigFrameNode, *compiled_children: ir.SQLGlotIR
    ) -> ir.SQLGlotIR:
        """Defines transformation but isn't cached, always use compile_node instead"""
        raise ValueError(f"Can't compile unrecognized node: {node}")

    @_compile_node.register
    def compile_readlocal(self, node: nodes.ReadLocalNode, *args) -> ir.SQLGlotIR:
        pa_table = node.local_data_source.data
        pa_table = pa_table.select([item.source_id for item in node.scan_list.items])
        pa_table = pa_table.rename_columns(
            [item.id.sql for item in node.scan_list.items]
        )

        offsets = node.offsets_col.sql if node.offsets_col else None
        if offsets:
            pa_table = pyarrow_utils.append_offsets(pa_table, offsets)

        return ir.SQLGlotIR.from_pyarrow(pa_table, node.schema, uid_gen=self.uid_gen)

    @_compile_node.register
    def compile_readtable(self, node: nodes.ReadTableNode, *args):
        table = node.source.table
        return ir.SQLGlotIR.from_table(
            table.project_id,
            table.dataset_id,
            table.table_id,
            col_names=[col.source_id for col in node.scan_list.items],
            alias_names=[col.id.sql for col in node.scan_list.items],
            uid_gen=self.uid_gen,
        )

    @_compile_node.register
    def compile_selection(
        self, node: nodes.SelectionNode, child: ir.SQLGlotIR
    ) -> ir.SQLGlotIR:
        selected_cols: tuple[tuple[str, sge.Expression], ...] = tuple(
            (id.sql, scalar_compiler.compile_scalar_expression(expr))
            for expr, id in node.input_output_pairs
        )
        return child.select(selected_cols)

    @_compile_node.register
    def compile_projection(
        self, node: nodes.ProjectionNode, child: ir.SQLGlotIR
    ) -> ir.SQLGlotIR:
        projected_cols: tuple[tuple[str, sge.Expression], ...] = tuple(
            (id.sql, scalar_compiler.compile_scalar_expression(expr))
            for expr, id in node.assignments
        )
        return child.project(projected_cols)

    @_compile_node.register
    def compile_filter(
        self, node: nodes.FilterNode, child: ir.SQLGlotIR
    ) -> ir.SQLGlotIR:
        condition = scalar_compiler.compile_scalar_expression(node.predicate)
        return child.filter(condition)

    @_compile_node.register
    def compile_join(
        self, node: nodes.JoinNode, left: ir.SQLGlotIR, right: ir.SQLGlotIR
    ) -> ir.SQLGlotIR:
        conditions = tuple(
            (
                typed_expr.TypedExpr(
                    scalar_compiler.compile_scalar_expression(left), left.output_type
                ),
                typed_expr.TypedExpr(
                    scalar_compiler.compile_scalar_expression(right), right.output_type
                ),
            )
            for left, right in node.conditions
        )

        return left.join(
            right,
            join_type=node.type,
            conditions=conditions,
            joins_nulls=node.joins_nulls,
        )

    @_compile_node.register
    def compile_concat(
        self, node: nodes.ConcatNode, *children: ir.SQLGlotIR
    ) -> ir.SQLGlotIR:
        output_ids = [id.sql for id in node.output_ids]
        return ir.SQLGlotIR.from_union(
            [child.expr for child in children],
            output_ids=output_ids,
            uid_gen=self.uid_gen,
        )

    @_compile_node.register
    def compile_explode(
        self, node: nodes.ExplodeNode, child: ir.SQLGlotIR
    ) -> ir.SQLGlotIR:
        offsets_col = node.offsets_col.sql if (node.offsets_col is not None) else None
        columns = tuple(ref.id.sql for ref in node.column_ids)
        return child.explode(columns, offsets_col)

    @_compile_node.register
    def compile_random_sample(
        self, node: nodes.RandomSampleNode, child: ir.SQLGlotIR
    ) -> ir.SQLGlotIR:
        return child.sample(node.fraction)


def _replace_unsupported_ops(node: nodes.BigFrameNode):
    node = nodes.bottom_up(node, rewrite.rewrite_slice)
    node = nodes.bottom_up(node, rewrite.rewrite_range_rolling)
    return node
