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
from typing import cast, Optional

import bigframes_vendored.ibis.backends.bigquery as ibis_bigquery
import bigframes_vendored.ibis.expr.api as ibis_api
import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.types as ibis_types

from bigframes import dtypes, operations
from bigframes.core import expression, pyarrow_utils
import bigframes.core.compile.compiled as compiled
import bigframes.core.compile.concat as concat_impl
import bigframes.core.compile.configs as configs
import bigframes.core.compile.explode
import bigframes.core.compile.scalar_op_compiler as compile_scalar
import bigframes.core.nodes as nodes
import bigframes.core.ordering as bf_ordering
import bigframes.core.rewrite as rewrites

if typing.TYPE_CHECKING:
    import bigframes.core


def compile_sql(request: configs.CompileRequest) -> configs.CompileResult:
    output_names = tuple((expression.DerefOp(id), id.sql) for id in request.node.ids)
    result_node = nodes.ResultNode(
        request.node,
        output_cols=output_names,
        limit=request.peek_count,
    )
    if request.sort_rows:
        # Can only pullup slice if we are doing ORDER BY in outermost SELECT
        # Need to do this before replacing unsupported ops, as that will rewrite slice ops
        result_node = rewrites.pull_up_limits(result_node)
    result_node = _replace_unsupported_ops(result_node)
    # prune before pulling up order to avoid unnnecessary row_number() ops
    result_node = cast(nodes.ResultNode, rewrites.column_pruning(result_node))
    result_node = rewrites.defer_order(
        result_node, output_hidden_row_keys=request.materialize_all_order_keys
    )
    if request.sort_rows:
        result_node = cast(nodes.ResultNode, rewrites.column_pruning(result_node))
        sql = compile_result_node(result_node)
        return configs.CompileResult(
            sql, result_node.schema.to_bigquery(), result_node.order_by
        )

    ordering: Optional[bf_ordering.RowOrdering] = result_node.order_by
    result_node = dataclasses.replace(result_node, order_by=None)
    result_node = cast(nodes.ResultNode, rewrites.column_pruning(result_node))
    result_node = cast(nodes.ResultNode, rewrites.defer_selection(result_node))
    sql = compile_result_node(result_node)
    # Return the ordering iff no extra columns are needed to define the row order
    if ordering is not None:
        output_order = (
            ordering if ordering.referenced_columns.issubset(result_node.ids) else None
        )
    assert (not request.materialize_all_order_keys) or (output_order is not None)
    return configs.CompileResult(sql, result_node.schema.to_bigquery(), output_order)


def _replace_unsupported_ops(node: nodes.BigFrameNode):
    # TODO: Run all replacement rules as single bottom-up pass
    node = nodes.bottom_up(node, rewrites.rewrite_slice)
    node = nodes.bottom_up(node, rewrites.rewrite_timedelta_expressions)
    node = nodes.bottom_up(node, rewrites.rewrite_range_rolling)
    return node


def compile_result_node(root: nodes.ResultNode) -> str:
    return compile_node(root.child).to_sql(
        order_by=root.order_by.all_ordering_columns if root.order_by else (),
        limit=root.limit,
        selections=root.output_cols,
    )


# TODO: Remove cache when schema no longer requires compilation to derive schema (and therefor only compiles for execution)
@functools.lru_cache(maxsize=5000)
def compile_node(node: nodes.BigFrameNode) -> compiled.UnorderedIR:
    """Compile node into CompileArrayValue. Caches result."""
    return node.reduce_up(lambda node, children: _compile_node(node, *children))


@functools.singledispatch
def _compile_node(
    node: nodes.BigFrameNode, *compiled_children: compiled.UnorderedIR
) -> compiled.UnorderedIR:
    """Defines transformation but isn't cached, always use compile_node instead"""
    raise ValueError(f"Can't compile unrecognized node: {node}")


@_compile_node.register
def compile_join(
    node: nodes.JoinNode, left: compiled.UnorderedIR, right: compiled.UnorderedIR
):
    condition_pairs = tuple(
        (left.id.sql, right.id.sql) for left, right in node.conditions
    )
    return left.join(
        right=right,
        type=node.type,
        conditions=condition_pairs,
        join_nulls=node.joins_nulls,
    )


@_compile_node.register
def compile_isin(
    node: nodes.InNode, left: compiled.UnorderedIR, right: compiled.UnorderedIR
):
    return left.isin_join(
        right=right,
        indicator_col=node.indicator_col.sql,
        conditions=(node.left_col.id.sql, node.right_col.id.sql),
        join_nulls=node.joins_nulls,
    )


@_compile_node.register
def compile_fromrange(
    node: nodes.FromRangeNode, start: compiled.UnorderedIR, end: compiled.UnorderedIR
):
    # Both start and end are single elements and do not inherently have an order)
    start_table = start._to_ibis_expr()
    end_table = end._to_ibis_expr()

    start_column = start_table.schema().names[0]
    end_column = end_table.schema().names[0]

    # Perform a cross join to avoid errors
    joined_table = start_table.cross_join(end_table)

    labels_array_table = ibis_api.range(
        joined_table[start_column], joined_table[end_column] + node.step, node.step
    ).name(node.output_id.sql)
    labels = (
        typing.cast(ibis_types.ArrayValue, labels_array_table)
        .as_table()
        .unnest([node.output_id.sql])
    )
    return compiled.UnorderedIR(
        labels,
        columns=[labels[labels.columns[0]]],
    )


@_compile_node.register
def compile_readlocal(node: nodes.ReadLocalNode, *args):
    offsets = node.offsets_col.sql if node.offsets_col else None
    pa_table = node.local_data_source.data
    bq_schema = node.schema.to_bigquery()

    pa_table = pa_table.select([item.source_id for item in node.scan_list.items])
    pa_table = pa_table.rename_columns([item.id.sql for item in node.scan_list.items])

    if offsets:
        pa_table = pyarrow_utils.append_offsets(pa_table, offsets)
    return compiled.UnorderedIR.from_polars(pa_table, bq_schema)


@_compile_node.register
def compile_readtable(node: nodes.ReadTableNode, *args):
    ibis_table = _table_to_ibis(
        node.source, scan_cols=[col.source_id for col in node.scan_list.items]
    )

    # TODO(b/395912450): Remove workaround solution once b/374784249 got resolved.
    for scan_item in node.scan_list.items:
        if (
            scan_item.dtype == dtypes.JSON_DTYPE
            and ibis_table[scan_item.source_id].type() == ibis_dtypes.string
        ):
            json_column = compile_scalar.parse_json(
                ibis_table[scan_item.source_id]
            ).name(scan_item.source_id)
            ibis_table = ibis_table.mutate(json_column)

    return compiled.UnorderedIR(
        ibis_table,
        tuple(
            ibis_table[scan_item.source_id].name(scan_item.id.sql)
            for scan_item in node.scan_list.items
        ),
    )


def _table_to_ibis(
    source: nodes.BigqueryDataSource,
    scan_cols: typing.Sequence[str],
) -> ibis_types.Table:
    full_table_name = (
        f"{source.table.project_id}.{source.table.dataset_id}.{source.table.table_id}"
    )
    # Physical schema might include unused columns, unsupported datatypes like JSON
    physical_schema = ibis_bigquery.BigQuerySchema.to_ibis(
        list(source.table.physical_schema)
    )
    if source.at_time is not None or source.sql_predicate is not None:
        import bigframes.session._io.bigquery

        sql = bigframes.session._io.bigquery.to_query(
            full_table_name,
            columns=scan_cols,
            sql_predicate=source.sql_predicate,
            time_travel_timestamp=source.at_time,
        )
        return ibis_bigquery.Backend().sql(schema=physical_schema, query=sql)
    else:
        return ibis_api.table(physical_schema, full_table_name).select(scan_cols)


@_compile_node.register
def compile_filter(node: nodes.FilterNode, child: compiled.UnorderedIR):
    return child.filter(node.predicate)


@_compile_node.register
def compile_selection(node: nodes.SelectionNode, child: compiled.UnorderedIR):
    selection = tuple((ref, id.sql) for ref, id in node.input_output_pairs)
    return child.selection(selection)


@_compile_node.register
def compile_projection(node: nodes.ProjectionNode, child: compiled.UnorderedIR):
    projections = ((expr, id.sql) for expr, id in node.assignments)
    return child.projection(tuple(projections))


@_compile_node.register
def compile_concat(node: nodes.ConcatNode, *children: compiled.UnorderedIR):
    output_ids = [id.sql for id in node.output_ids]
    return concat_impl.concat_unordered(children, output_ids)


@_compile_node.register
def compile_aggregate(node: nodes.AggregateNode, child: compiled.UnorderedIR):
    aggs = tuple((agg, id.sql) for agg, id in node.aggregations)
    result = child.aggregate(aggs, node.by_column_ids, order_by=node.order_by)
    # TODO: Remove dropna field and use filter node instead
    if node.dropna:
        for key in node.by_column_ids:
            if node.child.field_by_id[key.id].nullable:
                result = result.filter(operations.notnull_op.as_expr(key))
    return result


@_compile_node.register
def compile_window(node: nodes.WindowOpNode, child: compiled.UnorderedIR):
    result = child.project_window_op(
        node.expression,
        node.window_spec,
        node.output_name.sql,
        never_skip_nulls=node.never_skip_nulls,
    )
    return result


@_compile_node.register
def compile_explode(node: nodes.ExplodeNode, child: compiled.UnorderedIR):
    offsets_col = node.offsets_col.sql if (node.offsets_col is not None) else None
    return bigframes.core.compile.explode.explode_unordered(
        child, node.column_ids, offsets_col
    )


@_compile_node.register
def compile_random_sample(node: nodes.RandomSampleNode, child: compiled.UnorderedIR):
    return child._uniform_sampling(node.fraction)
