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

import bigframes_vendored.sqlglot.expressions as sge

from bigframes import dtypes
from bigframes.core import (
    expression,
    guid,
    identifiers,
    nodes,
    pyarrow_utils,
    rewrite,
    sql_nodes,
)
from bigframes.core.compile import configs
import bigframes.core.compile.sqlglot.aggregate_compiler as aggregate_compiler
from bigframes.core.compile.sqlglot.aggregations import windows
import bigframes.core.compile.sqlglot.expression_compiler as expression_compiler
from bigframes.core.compile.sqlglot.expressions import typed_expr
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
from bigframes.core.logging import data_types as data_type_logger
import bigframes.core.ordering as bf_ordering
from bigframes.core.rewrite import schema_binding


def compile_sql(request: configs.CompileRequest) -> configs.CompileResult:
    """Compiles a BigFrameNode according to the request into SQL using SQLGlot."""

    output_names = tuple((expression.DerefOp(id), id.sql) for id in request.node.ids)
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
        result_node = typing.cast(nodes.ResultNode, rewrite.column_pruning(result_node))
        encoded_type_refs = data_type_logger.encode_type_refs(result_node)
        sql = _compile_result_node(result_node)
        return configs.CompileResult(
            sql,
            result_node.schema.to_bigquery(),
            result_node.order_by,
            encoded_type_refs,
        )

    ordering: typing.Optional[bf_ordering.RowOrdering] = result_node.order_by
    result_node = dataclasses.replace(result_node, order_by=None)
    result_node = typing.cast(nodes.ResultNode, rewrite.column_pruning(result_node))
    encoded_type_refs = data_type_logger.encode_type_refs(result_node)
    sql = _compile_result_node(result_node)
    # Return the ordering iff no extra columns are needed to define the row order
    if ordering is not None:
        output_order = (
            ordering if ordering.referenced_columns.issubset(result_node.ids) else None
        )
    assert (not request.materialize_all_order_keys) or (output_order is not None)
    return configs.CompileResult(
        sql, result_node.schema.to_bigquery(), output_order, encoded_type_refs
    )


def _remap_variables(
    node: nodes.ResultNode, uid_gen: guid.SequentialUIDGenerator
) -> nodes.ResultNode:
    """Remaps `ColumnId`s in the BFET of a `ResultNode` to produce deterministic UIDs."""

    result_node, _ = rewrite.remap_variables(
        node, map(identifiers.ColumnId, uid_gen.get_uid_stream("bfcol_"))
    )
    return typing.cast(nodes.ResultNode, result_node)


def _compile_result_node(root: nodes.ResultNode) -> str:
    # Create UIDs to standardize variable names and ensure consistent compilation
    # of nodes using the same generator.
    uid_gen = guid.SequentialUIDGenerator()
    root = _remap_variables(root, uid_gen)
    root = typing.cast(nodes.ResultNode, rewrite.defer_selection(root))

    # Have to bind schema as the final step before compilation.
    # Probably, should defer even further
    root = typing.cast(nodes.ResultNode, schema_binding.bind_schema_to_tree(root))

    sqlglot_ir = compile_node(rewrite.as_sql_nodes(root), uid_gen)
    return sqlglot_ir.sql


def compile_node(
    node: nodes.BigFrameNode, uid_gen: guid.SequentialUIDGenerator
) -> ir.SQLGlotIR:
    """Compiles the given BigFrameNode from bottem-up into SQLGlotIR."""
    bf_to_sqlglot: dict[nodes.BigFrameNode, ir.SQLGlotIR] = {}
    child_results: tuple[ir.SQLGlotIR, ...] = ()
    for current_node in list(node.iter_nodes_topo()):
        if current_node.child_nodes == ():
            # For leaf node, generates a dumpy child to pass the UID generator.
            child_results = tuple([ir.SQLGlotIR(uid_gen=uid_gen)])
        else:
            # Child nodes should have been compiled in the reverse topological order.
            child_results = tuple(
                bf_to_sqlglot[child] for child in current_node.child_nodes
            )
        result = _compile_node(current_node, *child_results)
        bf_to_sqlglot[current_node] = result

    return bf_to_sqlglot[node]


@functools.singledispatch
def _compile_node(
    node: nodes.BigFrameNode, *compiled_children: ir.SQLGlotIR
) -> ir.SQLGlotIR:
    """Defines transformation but isn't cached, always use compile_node instead"""
    raise ValueError(f"Can't compile unrecognized node: {node}")


@_compile_node.register
def compile_sql_select(node: sql_nodes.SqlSelectNode, child: ir.SQLGlotIR):
    ordering_cols = tuple(
        sge.Ordered(
            this=expression_compiler.expression_compiler.compile_expression(
                ordering.scalar_expression
            ),
            desc=ordering.direction.is_ascending is False,
            nulls_first=ordering.na_last is False,
        )
        for ordering in node.sorting
    )

    projected_cols: tuple[tuple[str, sge.Expression], ...] = tuple()
    if not node.is_star_selection:
        projected_cols = tuple(
            (
                cdef.id.sql,
                expression_compiler.expression_compiler.compile_expression(
                    cdef.expression
                ),
            )
            for cdef in node.selections
        )

    sge_predicates = tuple(
        expression_compiler.expression_compiler.compile_expression(expression)
        for expression in node.predicates
    )

    return child.select(projected_cols, sge_predicates, ordering_cols, node.limit)


@_compile_node.register
def compile_readlocal(node: nodes.ReadLocalNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    pa_table = node.local_data_source.data
    pa_table = pa_table.select([item.source_id for item in node.scan_list.items])
    pa_table = pa_table.rename_columns([item.id.sql for item in node.scan_list.items])

    offsets = node.offsets_col.sql if node.offsets_col else None
    if offsets:
        pa_table = pyarrow_utils.append_offsets(pa_table, offsets)

    return ir.SQLGlotIR.from_pyarrow(pa_table, node.schema, uid_gen=child.uid_gen)


@_compile_node.register
def compile_readtable(node: sql_nodes.SqlDataSource, child: ir.SQLGlotIR):
    table = node.source.table
    return ir.SQLGlotIR.from_table(
        table.project_id,
        table.dataset_id,
        table.table_id,
        uid_gen=child.uid_gen,
        sql_predicate=node.source.sql_predicate,
        system_time=node.source.at_time,
    )


@_compile_node.register
def compile_join(
    node: nodes.JoinNode, left: ir.SQLGlotIR, right: ir.SQLGlotIR
) -> ir.SQLGlotIR:
    conditions = tuple(
        (
            typed_expr.TypedExpr(
                expression_compiler.expression_compiler.compile_expression(left),
                left.output_type,
            ),
            typed_expr.TypedExpr(
                expression_compiler.expression_compiler.compile_expression(right),
                right.output_type,
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
def compile_isin_join(
    node: nodes.InNode, left: ir.SQLGlotIR, right: ir.SQLGlotIR
) -> ir.SQLGlotIR:
    right_field = node.right_child.fields[0]
    conditions = (
        typed_expr.TypedExpr(
            expression_compiler.expression_compiler.compile_expression(node.left_col),
            node.left_col.output_type,
        ),
        typed_expr.TypedExpr(
            expression_compiler.expression_compiler.compile_expression(
                expression.DerefOp(right_field.id)
            ),
            right_field.dtype,
        ),
    )

    return left.isin_join(
        right,
        indicator_col=node.indicator_col.sql,
        conditions=conditions,
        joins_nulls=node.joins_nulls,
    )


@_compile_node.register
def compile_concat(node: nodes.ConcatNode, *children: ir.SQLGlotIR) -> ir.SQLGlotIR:
    assert len(children) >= 1
    uid_gen = children[0].uid_gen

    # BigQuery `UNION` query takes the column names from the first `SELECT` clause.
    default_output_ids = [field.id.sql for field in node.child_nodes[0].fields]
    output_aliases = [
        (default_output_id, output_id.sql)
        for default_output_id, output_id in zip(default_output_ids, node.output_ids)
    ]

    return ir.SQLGlotIR.from_union(
        [child._as_select() for child in children],
        output_aliases=output_aliases,
        uid_gen=uid_gen,
    )


@_compile_node.register
def compile_explode(node: nodes.ExplodeNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    offsets_col = node.offsets_col.sql if (node.offsets_col is not None) else None
    columns = tuple(ref.id.sql for ref in node.column_ids)
    return child.explode(columns, offsets_col)


@_compile_node.register
def compile_fromrange(
    node: nodes.FromRangeNode, start: ir.SQLGlotIR, end: ir.SQLGlotIR
) -> ir.SQLGlotIR:
    start_col_id = node.start.fields[0].id
    end_col_id = node.end.fields[0].id

    start_expr = expression_compiler.expression_compiler.compile_expression(
        expression.DerefOp(start_col_id)
    )
    end_expr = expression_compiler.expression_compiler.compile_expression(
        expression.DerefOp(end_col_id)
    )
    step_expr = ir._literal(node.step, dtypes.INT_DTYPE)

    return start.resample(end, node.output_id.sql, start_expr, end_expr, step_expr)


@_compile_node.register
def compile_random_sample(
    node: nodes.RandomSampleNode, child: ir.SQLGlotIR
) -> ir.SQLGlotIR:
    return child.sample(node.fraction)


@_compile_node.register
def compile_aggregate(node: nodes.AggregateNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    # The BigQuery ordered aggregation cannot support for NULL FIRST/LAST,
    # so we need to add extra expressions to enforce the null ordering.
    ordering_cols = windows.get_window_order_by(node.order_by, override_null_order=True)
    aggregations: tuple[tuple[str, sge.Expression], ...] = tuple(
        (
            id.sql,
            aggregate_compiler.compile_aggregate(
                agg, order_by=ordering_cols if ordering_cols else ()
            ),
        )
        for agg, id in node.aggregations
    )
    by_cols: tuple[sge.Expression, ...] = tuple(
        expression_compiler.expression_compiler.compile_expression(by_col)
        for by_col in node.by_column_ids
    )

    dropna_cols = []
    if node.dropna:
        for key, by_col in zip(node.by_column_ids, by_cols):
            if node.child.field_by_id[key.id].nullable:
                dropna_cols.append(by_col)

    return child.aggregate(aggregations, by_cols, tuple(dropna_cols))


def _replace_unsupported_ops(node: nodes.BigFrameNode):
    node = nodes.bottom_up(node, rewrite.rewrite_slice)
    node = nodes.bottom_up(node, rewrite.rewrite_range_rolling)
    return node
