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
import io
import typing

import bigframes_vendored.ibis.backends.bigquery as ibis_bigquery
import bigframes_vendored.ibis.expr.api as ibis_api
import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.types as ibis_types
import google.cloud.bigquery
import pandas as pd

from bigframes import dtypes, operations
from bigframes.core import utils
import bigframes.core.compile.compiled as compiled
import bigframes.core.compile.concat as concat_impl
import bigframes.core.compile.explode
import bigframes.core.compile.ibis_types
import bigframes.core.compile.scalar_op_compiler as compile_scalar
import bigframes.core.compile.schema_translator
import bigframes.core.nodes as nodes
import bigframes.core.ordering as bf_ordering
import bigframes.core.rewrite as rewrites

if typing.TYPE_CHECKING:
    import bigframes.core
    import bigframes.session


@dataclasses.dataclass(frozen=True)
class Compiler:
    # In strict mode, ordering will always be deterministic
    # In unstrict mode, ordering from ReadTable or after joins may be ambiguous to improve query performance.
    strict: bool = True
    scalar_op_compiler = compile_scalar.ScalarOpCompiler()

    def compile_sql(
        self,
        node: nodes.BigFrameNode,
        ordered: bool,
        limit: typing.Optional[int] = None,
    ) -> str:
        # later steps might add ids, so snapshot before those steps.
        output_ids = node.schema.names
        if ordered:
            # Need to do this before replacing unsupported ops, as that will rewrite slice ops
            node, pulled_up_limit = rewrites.pullup_limit_from_slice(node)
            if (pulled_up_limit is not None) and (
                (limit is None) or limit > pulled_up_limit
            ):
                limit = pulled_up_limit

        node = self._replace_unsupported_ops(node)
        # prune before pulling up order to avoid unnnecessary row_number() ops
        node = rewrites.column_pruning(node)
        node, ordering = rewrites.pull_up_order(node, order_root=ordered)
        # final pruning to cleanup up any leftovers unused values
        node = rewrites.column_pruning(node)
        return self.compile_node(node).to_sql(
            order_by=ordering.all_ordering_columns if ordered else (),
            limit=limit,
            selections=output_ids,
        )

    def compile_raw(
        self,
        node: nodes.BigFrameNode,
    ) -> typing.Tuple[
        str, typing.Sequence[google.cloud.bigquery.SchemaField], bf_ordering.RowOrdering
    ]:
        node = self._replace_unsupported_ops(node)
        node = rewrites.column_pruning(node)
        node, ordering = rewrites.pull_up_order(node, order_root=True)
        node = rewrites.column_pruning(node)
        sql = self.compile_node(node).to_sql()
        return sql, node.schema.to_bigquery(), ordering

    def _replace_unsupported_ops(self, node: nodes.BigFrameNode):
        # TODO: Run all replacement rules as single bottom-up pass
        node = nodes.bottom_up(node, rewrites.rewrite_slice)
        node = nodes.bottom_up(node, rewrites.rewrite_timedelta_expressions)
        return node

    # TODO: Remove cache when schema no longer requires compilation to derive schema (and therefor only compiles for execution)
    @functools.lru_cache(maxsize=5000)
    def compile_node(self, node: nodes.BigFrameNode) -> compiled.UnorderedIR:
        """Compile node into CompileArrayValue. Caches result."""
        return self._compile_node(node)

    @functools.singledispatchmethod
    def _compile_node(self, node: nodes.BigFrameNode) -> compiled.UnorderedIR:
        """Defines transformation but isn't cached, always use compile_node instead"""
        raise ValueError(f"Can't compile unrecognized node: {node}")

    @_compile_node.register
    def compile_join(self, node: nodes.JoinNode):
        condition_pairs = tuple(
            (left.id.sql, right.id.sql) for left, right in node.conditions
        )

        left_unordered = self.compile_node(node.left_child)
        right_unordered = self.compile_node(node.right_child)
        return left_unordered.join(
            right=right_unordered,
            type=node.type,
            conditions=condition_pairs,
            join_nulls=node.joins_nulls,
        )

    @_compile_node.register
    def compile_isin(self, node: nodes.InNode):
        left_unordered = self.compile_node(node.left_child)
        right_unordered = self.compile_node(node.right_child)
        return left_unordered.isin_join(
            right=right_unordered,
            indicator_col=node.indicator_col.sql,
            conditions=(node.left_col.id.sql, node.right_col.id.sql),
            join_nulls=node.joins_nulls,
        )

    @_compile_node.register
    def compile_fromrange(self, node: nodes.FromRangeNode):
        # Both start and end are single elements and do not inherently have an order
        start = self.compile_node(node.start)
        end = self.compile_node(node.end)
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
    def compile_readlocal(self, node: nodes.ReadLocalNode):
        array_as_pd = pd.read_feather(
            io.BytesIO(node.feather_bytes),
            columns=[item.source_id for item in node.scan_list.items],
        )

        # Convert timedeltas to microseconds for compatibility with BigQuery
        _ = utils.replace_timedeltas_with_micros(array_as_pd)

        offsets = node.offsets_col.sql if node.offsets_col else None
        return compiled.UnorderedIR.from_pandas(
            array_as_pd, node.scan_list, offsets=offsets
        )

    @_compile_node.register
    def compile_readtable(self, node: nodes.ReadTableNode):
        return self.compile_read_table_unordered(node.source, node.scan_list)

    def read_table_as_unordered_ibis(
        self,
        source: nodes.BigqueryDataSource,
        scan_cols: typing.Sequence[str],
    ) -> ibis_types.Table:
        full_table_name = f"{source.table.project_id}.{source.table.dataset_id}.{source.table.table_id}"
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

    def compile_read_table_unordered(
        self, source: nodes.BigqueryDataSource, scan: nodes.ScanList
    ):
        ibis_table = self.read_table_as_unordered_ibis(
            source, scan_cols=[col.source_id for col in scan.items]
        )

        # TODO(b/395912450): Remove workaround solution once b/374784249 got resolved.
        for scan_item in scan.items:
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
                for scan_item in scan.items
            ),
        )

    @_compile_node.register
    def compile_filter(self, node: nodes.FilterNode):
        return self.compile_node(node.child).filter(node.predicate)

    @_compile_node.register
    def compile_selection(self, node: nodes.SelectionNode):
        result = self.compile_node(node.child)
        selection = tuple((ref, id.sql) for ref, id in node.input_output_pairs)
        return result.selection(selection)

    @_compile_node.register
    def compile_projection(self, node: nodes.ProjectionNode):
        result = self.compile_node(node.child)
        projections = ((expr, id.sql) for expr, id in node.assignments)
        return result.projection(tuple(projections))

    @_compile_node.register
    def compile_concat(self, node: nodes.ConcatNode):
        output_ids = [id.sql for id in node.output_ids]
        compiled_unordered = [self.compile_node(node) for node in node.children]
        return concat_impl.concat_unordered(compiled_unordered, output_ids)

    @_compile_node.register
    def compile_rowcount(self, node: nodes.RowCountNode):
        result = self.compile_node(node.child).row_count(name=node.col_id.sql)
        return result

    @_compile_node.register
    def compile_aggregate(self, node: nodes.AggregateNode):
        aggs = tuple((agg, id.sql) for agg, id in node.aggregations)
        result = self.compile_node(node.child).aggregate(
            aggs, node.by_column_ids, order_by=node.order_by
        )
        # TODO: Remove dropna field and use filter node instead
        if node.dropna:
            for key in node.by_column_ids:
                if node.child.field_by_id[key.id].nullable:
                    result = result.filter(operations.notnull_op.as_expr(key))
        return result

    @_compile_node.register
    def compile_window(self, node: nodes.WindowOpNode):
        result = self.compile_node(node.child).project_window_op(
            node.expression,
            node.window_spec,
            node.output_name.sql,
            never_skip_nulls=node.never_skip_nulls,
        )
        return result

    @_compile_node.register
    def compile_explode(self, node: nodes.ExplodeNode):
        offsets_col = node.offsets_col.sql if (node.offsets_col is not None) else None
        return bigframes.core.compile.explode.explode_unordered(
            self.compile_node(node.child), node.column_ids, offsets_col
        )

    @_compile_node.register
    def compile_random_sample(self, node: nodes.RandomSampleNode):
        return self.compile_node(node.child)._uniform_sampling(node.fraction)
