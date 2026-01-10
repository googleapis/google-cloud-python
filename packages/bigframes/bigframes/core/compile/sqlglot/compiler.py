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

from bigframes.core import (
    agg_expressions,
    expression,
    guid,
    identifiers,
    nodes,
    pyarrow_utils,
    rewrite,
)
from bigframes.core.compile import configs
import bigframes.core.compile.sqlglot.aggregate_compiler as aggregate_compiler
from bigframes.core.compile.sqlglot.aggregations import windows
from bigframes.core.compile.sqlglot.expressions import typed_expr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler
import bigframes.core.compile.sqlglot.sqlglot_ir as ir
import bigframes.core.ordering as bf_ordering
from bigframes.core.rewrite import schema_binding


def compile_sql(request: configs.CompileRequest) -> configs.CompileResult:
    """Compiles a BigFrameNode according to the request into SQL using SQLGlot."""

    # Generator for unique identifiers.
    uid_gen = guid.SequentialUIDGenerator()
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
        result_node = _remap_variables(result_node, uid_gen)
        result_node = typing.cast(
            nodes.ResultNode, rewrite.defer_selection(result_node)
        )
        sql = _compile_result_node(result_node, uid_gen)
        return configs.CompileResult(
            sql, result_node.schema.to_bigquery(), result_node.order_by
        )

    ordering: typing.Optional[bf_ordering.RowOrdering] = result_node.order_by
    result_node = dataclasses.replace(result_node, order_by=None)
    result_node = typing.cast(nodes.ResultNode, rewrite.column_pruning(result_node))

    result_node = _remap_variables(result_node, uid_gen)
    result_node = typing.cast(nodes.ResultNode, rewrite.defer_selection(result_node))
    sql = _compile_result_node(result_node, uid_gen)
    # Return the ordering iff no extra columns are needed to define the row order
    if ordering is not None:
        output_order = (
            ordering if ordering.referenced_columns.issubset(result_node.ids) else None
        )
    assert (not request.materialize_all_order_keys) or (output_order is not None)
    return configs.CompileResult(sql, result_node.schema.to_bigquery(), output_order)


def _remap_variables(
    node: nodes.ResultNode, uid_gen: guid.SequentialUIDGenerator
) -> nodes.ResultNode:
    """Remaps `ColumnId`s in the BFET of a `ResultNode` to produce deterministic UIDs."""

    result_node, _ = rewrite.remap_variables(
        node, map(identifiers.ColumnId, uid_gen.get_uid_stream("bfcol_"))
    )
    return typing.cast(nodes.ResultNode, result_node)


def _compile_result_node(
    root: nodes.ResultNode, uid_gen: guid.SequentialUIDGenerator
) -> str:
    # Have to bind schema as the final step before compilation.
    root = typing.cast(nodes.ResultNode, schema_binding.bind_schema_to_tree(root))
    selected_cols: tuple[tuple[str, sge.Expression], ...] = tuple(
        (name, scalar_compiler.scalar_op_compiler.compile_expression(ref))
        for ref, name in root.output_cols
    )
    sqlglot_ir = compile_node(root.child, uid_gen).select(selected_cols)

    if root.order_by is not None:
        ordering_cols = tuple(
            sge.Ordered(
                this=scalar_compiler.scalar_op_compiler.compile_expression(
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
def compile_readlocal(node: nodes.ReadLocalNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    pa_table = node.local_data_source.data
    pa_table = pa_table.select([item.source_id for item in node.scan_list.items])
    pa_table = pa_table.rename_columns([item.id.sql for item in node.scan_list.items])

    offsets = node.offsets_col.sql if node.offsets_col else None
    if offsets:
        pa_table = pyarrow_utils.append_offsets(pa_table, offsets)

    return ir.SQLGlotIR.from_pyarrow(pa_table, node.schema, uid_gen=child.uid_gen)


@_compile_node.register
def compile_readtable(node: nodes.ReadTableNode, child: ir.SQLGlotIR):
    table = node.source.table
    return ir.SQLGlotIR.from_table(
        table.project_id,
        table.dataset_id,
        table.table_id,
        col_names=[col.source_id for col in node.scan_list.items],
        alias_names=[col.id.sql for col in node.scan_list.items],
        uid_gen=child.uid_gen,
        sql_predicate=node.source.sql_predicate,
        system_time=node.source.at_time,
    )


@_compile_node.register
def compile_selection(node: nodes.SelectionNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    selected_cols: tuple[tuple[str, sge.Expression], ...] = tuple(
        (id.sql, scalar_compiler.scalar_op_compiler.compile_expression(expr))
        for expr, id in node.input_output_pairs
    )
    return child.select(selected_cols)


@_compile_node.register
def compile_projection(node: nodes.ProjectionNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    projected_cols: tuple[tuple[str, sge.Expression], ...] = tuple(
        (id.sql, scalar_compiler.scalar_op_compiler.compile_expression(expr))
        for expr, id in node.assignments
    )
    return child.project(projected_cols)


@_compile_node.register
def compile_filter(node: nodes.FilterNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    condition = scalar_compiler.scalar_op_compiler.compile_expression(node.predicate)
    return child.filter(tuple([condition]))


@_compile_node.register
def compile_join(
    node: nodes.JoinNode, left: ir.SQLGlotIR, right: ir.SQLGlotIR
) -> ir.SQLGlotIR:
    conditions = tuple(
        (
            typed_expr.TypedExpr(
                scalar_compiler.scalar_op_compiler.compile_expression(left),
                left.output_type,
            ),
            typed_expr.TypedExpr(
                scalar_compiler.scalar_op_compiler.compile_expression(right),
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
            scalar_compiler.scalar_op_compiler.compile_expression(node.left_col),
            node.left_col.output_type,
        ),
        typed_expr.TypedExpr(
            scalar_compiler.scalar_op_compiler.compile_expression(
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

    output_ids = [id.sql for id in node.output_ids]
    return ir.SQLGlotIR.from_union(
        [child.expr for child in children],
        output_ids=output_ids,
        uid_gen=uid_gen,
    )


@_compile_node.register
def compile_explode(node: nodes.ExplodeNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    offsets_col = node.offsets_col.sql if (node.offsets_col is not None) else None
    columns = tuple(ref.id.sql for ref in node.column_ids)
    return child.explode(columns, offsets_col)


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
        scalar_compiler.scalar_op_compiler.compile_expression(by_col)
        for by_col in node.by_column_ids
    )

    dropna_cols = []
    if node.dropna:
        for key, by_col in zip(node.by_column_ids, by_cols):
            if node.child.field_by_id[key.id].nullable:
                dropna_cols.append(by_col)

    return child.aggregate(aggregations, by_cols, tuple(dropna_cols))


@_compile_node.register
def compile_window(node: nodes.WindowOpNode, child: ir.SQLGlotIR) -> ir.SQLGlotIR:
    window_spec = node.window_spec
    result = child
    for cdef in node.agg_exprs:
        assert isinstance(cdef.expression, agg_expressions.Aggregation)
        if cdef.expression.op.order_independent and window_spec.is_unbounded:
            # notably percentile_cont does not support ordering clause
            window_spec = window_spec.without_order()

        window_op = aggregate_compiler.compile_analytic(cdef.expression, window_spec)

        inputs: tuple[sge.Expression, ...] = tuple(
            scalar_compiler.scalar_op_compiler.compile_expression(
                expression.DerefOp(column)
            )
            for column in cdef.expression.column_references
        )

        clauses: list[tuple[sge.Expression, sge.Expression]] = []
        if window_spec.min_periods and len(inputs) > 0:
            if not cdef.expression.op.nulls_count_for_min_values:
                # Most operations do not count NULL values towards min_periods
                not_null_columns = [
                    sge.Not(this=sge.Is(this=column, expression=sge.Null()))
                    for column in inputs
                ]
                # All inputs must be non-null for observation to count
                if not not_null_columns:
                    is_observation_expr: sge.Expression = sge.convert(True)
                else:
                    is_observation_expr = not_null_columns[0]
                    for expr in not_null_columns[1:]:
                        is_observation_expr = sge.And(
                            this=is_observation_expr, expression=expr
                        )
                is_observation = ir._cast(is_observation_expr, "INT64")
                observation_count = windows.apply_window_if_present(
                    sge.func("SUM", is_observation), window_spec
                )
                observation_count = sge.func(
                    "COALESCE", observation_count, sge.convert(0)
                )
            else:
                # Operations like count treat even NULLs as valid observations
                # for the sake of min_periods notnull is just used to convert
                # null values to non-null (FALSE) values to be counted.
                is_observation = ir._cast(
                    sge.Not(this=sge.Is(this=inputs[0], expression=sge.Null())),
                    "INT64",
                )
                observation_count = windows.apply_window_if_present(
                    sge.func("COUNT", is_observation), window_spec
                )

            clauses.append(
                (
                    observation_count < sge.convert(window_spec.min_periods),
                    sge.Null(),
                )
            )
        if clauses:
            when_expressions = [sge.When(this=cond, true=res) for cond, res in clauses]
            window_op = sge.Case(ifs=when_expressions, default=window_op)

        # TODO: check if we can directly window the expression.
        result = result.window(
            window_op=window_op,
            output_column_id=cdef.id.sql,
        )
    return result


def _replace_unsupported_ops(node: nodes.BigFrameNode):
    node = nodes.bottom_up(node, rewrite.rewrite_slice)
    node = nodes.bottom_up(node, rewrite.rewrite_range_rolling)
    return node
