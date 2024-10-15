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

import ibis
import ibis.backends
import ibis.backends.bigquery
import ibis.expr.types
import pandas as pd

import bigframes.core.compile.compiled as compiled
import bigframes.core.compile.concat as concat_impl
import bigframes.core.compile.default_ordering as default_ordering
import bigframes.core.compile.ibis_types
import bigframes.core.compile.scalar_op_compiler
import bigframes.core.compile.scalar_op_compiler as compile_scalar
import bigframes.core.compile.schema_translator
import bigframes.core.compile.single_column
import bigframes.core.guid as guids
import bigframes.core.identifiers as ids
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
    enable_pruning: bool = False

    def _preprocess(self, node: nodes.BigFrameNode):
        if self.enable_pruning:
            used_fields = frozenset(field.id for field in node.fields)
            node = node.prune(used_fields)
        node = functools.cache(rewrites.replace_slice_ops)(node)
        return node

    def compile_ordered_ir(self, node: nodes.BigFrameNode) -> compiled.OrderedIR:
        ir = typing.cast(
            compiled.OrderedIR, self.compile_node(self._preprocess(node), True)
        )
        if self.strict:
            assert ir.has_total_order
        return ir

    def compile_unordered_ir(self, node: nodes.BigFrameNode) -> compiled.UnorderedIR:
        return typing.cast(
            compiled.UnorderedIR, self.compile_node(self._preprocess(node), False)
        )

    def compile_peak_sql(
        self, node: nodes.BigFrameNode, n_rows: int
    ) -> typing.Optional[str]:
        return self.compile_unordered_ir(self._preprocess(node)).peek_sql(n_rows)

    # TODO: Remove cache when schema no longer requires compilation to derive schema (and therefor only compiles for execution)
    @functools.lru_cache(maxsize=5000)
    def compile_node(
        self, node: nodes.BigFrameNode, ordered: bool = True
    ) -> compiled.UnorderedIR | compiled.OrderedIR:
        """Compile node into CompileArrayValue. Caches result."""
        return self._compile_node(node, ordered)

    @functools.singledispatchmethod
    def _compile_node(
        self, node: nodes.BigFrameNode, ordered: bool = True
    ) -> compiled.UnorderedIR:
        """Defines transformation but isn't cached, always use compile_node instead"""
        raise ValueError(f"Can't compile unrecognized node: {node}")

    @_compile_node.register
    def compile_join(self, node: nodes.JoinNode, ordered: bool = True):
        condition_pairs = tuple(
            (left.id.sql, right.id.sql) for left, right in node.conditions
        )
        if ordered:
            # In general, joins are an ordering destroying operation.
            # With ordering_mode = "partial", make this explicit. In
            # this case, we don't need to provide a deterministic ordering.
            if self.strict:
                left_ordered = self.compile_ordered_ir(node.left_child)
                right_ordered = self.compile_ordered_ir(node.right_child)
                return bigframes.core.compile.single_column.join_by_column_ordered(
                    left=left_ordered,
                    right=right_ordered,
                    type=node.type,
                    conditions=condition_pairs,
                )
            else:
                left_unordered = self.compile_unordered_ir(node.left_child)
                right_unordered = self.compile_unordered_ir(node.right_child)
                return bigframes.core.compile.single_column.join_by_column_unordered(
                    left=left_unordered,
                    right=right_unordered,
                    type=node.type,
                    conditions=condition_pairs,
                ).as_ordered_ir()
        else:
            left_unordered = self.compile_unordered_ir(node.left_child)
            right_unordered = self.compile_unordered_ir(node.right_child)
            return bigframes.core.compile.single_column.join_by_column_unordered(
                left=left_unordered,
                right=right_unordered,
                type=node.type,
                conditions=condition_pairs,
            )

    @_compile_node.register
    def compile_fromrange(self, node: nodes.FromRangeNode, ordered: bool = True):
        # Both start and end are single elements and do not inherently have an order
        start = self.compile_unordered_ir(node.start)
        end = self.compile_unordered_ir(node.end)
        start_table = start._to_ibis_expr()
        end_table = end._to_ibis_expr()

        start_column = start_table.schema().names[0]
        end_column = end_table.schema().names[0]

        # Perform a cross join to avoid errors
        joined_table = start_table.cross_join(end_table)

        labels_array_table = ibis.range(
            joined_table[start_column], joined_table[end_column] + node.step, node.step
        ).name("labels")
        labels = (
            typing.cast(ibis.expr.types.ArrayValue, labels_array_table)
            .unnest()
            .as_table()
        )
        if ordered:
            return compiled.OrderedIR(
                labels,
                columns=[labels[labels.columns[0]]],
                ordering=bf_ordering.TotalOrdering().from_offset_col(labels.columns[0]),
            )
        else:
            return compiled.UnorderedIR(
                labels,
                columns=[labels[labels.columns[0]]],
            )

    @_compile_node.register
    def compile_readlocal(self, node: nodes.ReadLocalNode, ordered: bool = True):
        array_as_pd = pd.read_feather(
            io.BytesIO(node.feather_bytes),
            columns=[item.source_id for item in node.scan_list.items],
        )
        ordered_ir = compiled.OrderedIR.from_pandas(array_as_pd, node.scan_list)
        if ordered:
            return ordered_ir
        else:
            return ordered_ir.to_unordered()

    @_compile_node.register
    def compile_readtable(self, node: nodes.ReadTableNode, ordered: bool = True):
        if ordered:
            return self.compile_read_table_ordered(node.source, node.scan_list)
        else:
            return self.compile_read_table_unordered(node.source, node.scan_list)

    def read_table_as_unordered_ibis(
        self, source: nodes.BigqueryDataSource
    ) -> ibis.expr.types.Table:
        full_table_name = f"{source.table.project_id}.{source.table.dataset_id}.{source.table.table_id}"
        used_columns = tuple(col.name for col in source.table.physical_schema)
        # Physical schema might include unused columns, unsupported datatypes like JSON
        physical_schema = ibis.backends.bigquery.BigQuerySchema.to_ibis(
            list(i for i in source.table.physical_schema if i.name in used_columns)
        )
        if source.at_time is not None or source.sql_predicate is not None:
            import bigframes.session._io.bigquery

            sql = bigframes.session._io.bigquery.to_query(
                full_table_name,
                columns=used_columns,
                sql_predicate=source.sql_predicate,
                time_travel_timestamp=source.at_time,
            )
            return ibis.backends.bigquery.Backend().sql(
                schema=physical_schema, query=sql
            )
        else:
            return ibis.table(physical_schema, full_table_name)

    def compile_read_table_unordered(
        self, source: nodes.BigqueryDataSource, scan: nodes.ScanList
    ):
        ibis_table = self.read_table_as_unordered_ibis(source)
        return compiled.UnorderedIR(
            ibis_table,
            tuple(
                bigframes.core.compile.ibis_types.ibis_value_to_canonical_type(
                    ibis_table[scan_item.source_id].name(scan_item.id.sql)
                )
                for scan_item in scan.items
            ),
        )

    def compile_read_table_ordered(
        self, source: nodes.BigqueryDataSource, scan_list: nodes.ScanList
    ):
        ibis_table = self.read_table_as_unordered_ibis(source)
        if source.ordering is not None:
            visible_column_mapping = {
                ids.ColumnId(scan_item.source_id): scan_item.id
                for scan_item in scan_list.items
            }
            full_mapping = {
                ids.ColumnId(col.name): ids.ColumnId(guids.generate_guid())
                for col in source.ordering.referenced_columns
            }
            full_mapping.update(visible_column_mapping)

            ordering = source.ordering.remap_column_refs(full_mapping)
            hidden_columns = tuple(
                ibis_table[source_id.sql].name(out_id.sql)
                for source_id, out_id in full_mapping.items()
                if source_id not in visible_column_mapping
            )
        elif self.strict:  # In strict mode, we fallback to ordering by row hash
            order_values = [
                col.name(guids.generate_guid())
                for col in default_ordering.gen_default_ordering(
                    ibis_table, use_double_hash=True
                )
            ]
            ordering = bf_ordering.TotalOrdering.from_primary_key(
                [value.get_name() for value in order_values]
            )
            hidden_columns = tuple(order_values)
        else:
            # In unstrict mode, don't generate total ordering from hashing as this is
            # expensive (prevent removing any columns from table scan)
            ordering, hidden_columns = bf_ordering.RowOrdering(), ()

        return compiled.OrderedIR(
            ibis_table,
            columns=tuple(
                bigframes.core.compile.ibis_types.ibis_value_to_canonical_type(
                    ibis_table[scan_item.source_id].name(scan_item.id.sql)
                )
                for scan_item in scan_list.items
            ),
            ordering=ordering,
            hidden_ordering_columns=hidden_columns,
        )

    @_compile_node.register
    def compile_promote_offsets(
        self, node: nodes.PromoteOffsetsNode, ordered: bool = True
    ):
        result = self.compile_ordered_ir(node.child).promote_offsets(node.col_id.sql)
        return result if ordered else result.to_unordered()

    @_compile_node.register
    def compile_filter(self, node: nodes.FilterNode, ordered: bool = True):
        return self.compile_node(node.child, ordered).filter(node.predicate)

    @_compile_node.register
    def compile_orderby(self, node: nodes.OrderByNode, ordered: bool = True):
        if ordered:
            return self.compile_ordered_ir(node.child).order_by(node.by)
        else:
            return self.compile_unordered_ir(node.child)

    @_compile_node.register
    def compile_reversed(self, node: nodes.ReversedNode, ordered: bool = True):
        if ordered:
            return self.compile_ordered_ir(node.child).reversed()
        else:
            return self.compile_unordered_ir(node.child)

    @_compile_node.register
    def compile_selection(self, node: nodes.SelectionNode, ordered: bool = True):
        result = self.compile_node(node.child, ordered)
        selection = tuple((ref, id.sql) for ref, id in node.input_output_pairs)
        return result.selection(selection)

    @_compile_node.register
    def compile_projection(self, node: nodes.ProjectionNode, ordered: bool = True):
        result = self.compile_node(node.child, ordered)
        projections = ((expr, id.sql) for expr, id in node.assignments)
        return result.projection(tuple(projections))

    @_compile_node.register
    def compile_concat(self, node: nodes.ConcatNode, ordered: bool = True):
        if ordered:
            compiled_ordered = [self.compile_ordered_ir(node) for node in node.children]
            return concat_impl.concat_ordered(compiled_ordered)
        else:
            compiled_unordered = [
                self.compile_unordered_ir(node) for node in node.children
            ]
            return concat_impl.concat_unordered(compiled_unordered)

    @_compile_node.register
    def compile_rowcount(self, node: nodes.RowCountNode, ordered: bool = True):
        result = self.compile_unordered_ir(node.child).row_count()
        return result if ordered else result.to_unordered()

    @_compile_node.register
    def compile_aggregate(self, node: nodes.AggregateNode, ordered: bool = True):
        has_ordered_aggregation_ops = any(
            aggregate.op.can_order_by for aggregate, _ in node.aggregations
        )
        aggs = tuple((agg, id.sql) for agg, id in node.aggregations)
        if ordered and has_ordered_aggregation_ops:
            return self.compile_ordered_ir(node.child).aggregate(
                aggs, node.by_column_ids, node.dropna
            )
        else:
            result = self.compile_unordered_ir(node.child).aggregate(
                aggs, node.by_column_ids, node.dropna
            )
            return result if ordered else result.to_unordered()

    @_compile_node.register
    def compile_window(self, node: nodes.WindowOpNode, ordered: bool = True):
        result = self.compile_ordered_ir(node.child).project_window_op(
            node.column_name,
            node.op,
            node.window_spec,
            node.output_name.sql,
            never_skip_nulls=node.never_skip_nulls,
        )
        return result if ordered else result.to_unordered()

    @_compile_node.register
    def compile_explode(self, node: nodes.ExplodeNode, ordered: bool = True):
        return self.compile_node(node.child, ordered).explode(node.column_ids)

    @_compile_node.register
    def compile_random_sample(self, node: nodes.RandomSampleNode, ordered: bool = True):
        return self.compile_node(node.child, ordered)._uniform_sampling(node.fraction)
