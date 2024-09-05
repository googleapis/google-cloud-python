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
import bigframes.core.compile.schema_translator
import bigframes.core.compile.single_column
import bigframes.core.nodes as nodes
import bigframes.core.ordering as bf_ordering

if typing.TYPE_CHECKING:
    import bigframes.core
    import bigframes.session


@dataclasses.dataclass(frozen=True)
class Compiler:
    # In strict mode, ordering will always be deterministic
    # In unstrict mode, ordering from ReadTable or after joins may be ambiguous to improve query performance.
    strict: bool = True

    def compile_ordered_ir(self, node: nodes.BigFrameNode) -> compiled.OrderedIR:
        ir = typing.cast(compiled.OrderedIR, self.compile_node(node, True))
        if self.strict:
            assert ir.has_total_order
        return ir

    def compile_unordered_ir(self, node: nodes.BigFrameNode) -> compiled.UnorderedIR:
        return typing.cast(compiled.UnorderedIR, self.compile_node(node, False))

    def compile_peak_sql(
        self, node: nodes.BigFrameNode, n_rows: int
    ) -> typing.Optional[str]:
        return self.compile_unordered_ir(node).peek_sql(n_rows)

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
        if ordered:
            left_ordered = self.compile_ordered_ir(node.left_child)
            right_ordered = self.compile_ordered_ir(node.right_child)
            return bigframes.core.compile.single_column.join_by_column_ordered(
                left=left_ordered,
                right=right_ordered,
                join=node.join,
            )
        else:
            left_unordered = self.compile_unordered_ir(node.left_child)
            right_unordered = self.compile_unordered_ir(node.right_child)
            return bigframes.core.compile.single_column.join_by_column_unordered(
                left=left_unordered,
                right=right_unordered,
                join=node.join,
            )

    @_compile_node.register
    def compile_readlocal(self, node: nodes.ReadLocalNode, ordered: bool = True):
        array_as_pd = pd.read_feather(io.BytesIO(node.feather_bytes))
        ordered_ir = compiled.OrderedIR.from_pandas(array_as_pd, node.schema)
        if ordered:
            return ordered_ir
        else:
            return ordered_ir.to_unordered()

    @_compile_node.register
    def compile_cached_table(self, node: nodes.CachedTableNode, ordered: bool = True):
        full_table_name = (
            f"{node.table.project_id}.{node.table.dataset_id}.{node.table.table_id}"
        )
        used_columns = (
            *node.schema.names,
            *node.hidden_columns,
        )
        # Physical schema might include unused columns, unsupported datatypes like JSON
        physical_schema = ibis.backends.bigquery.BigQuerySchema.to_ibis(
            list(i for i in node.table.physical_schema if i.name in used_columns)
        )
        ibis_table = ibis.table(physical_schema, full_table_name)
        if ordered:
            if node.ordering is None:
                # If this happens, session malfunctioned while applying cached results.
                raise ValueError(
                    "Cannot use unordered cached value. Result requires ordering information."
                )
            if self.strict and not isinstance(node.ordering, bf_ordering.TotalOrdering):
                raise ValueError(
                    "Cannot use partially ordered cached value. Result requires total ordering information."
                )
            return compiled.OrderedIR(
                ibis_table,
                columns=tuple(
                    bigframes.core.compile.ibis_types.ibis_value_to_canonical_type(
                        ibis_table[col]
                    )
                    for col in node.schema.names
                ),
                ordering=node.ordering,
                hidden_ordering_columns=[ibis_table[c] for c in node.hidden_columns],
            )

        else:
            return compiled.UnorderedIR(
                ibis_table,
                columns=tuple(
                    bigframes.core.compile.ibis_types.ibis_value_to_canonical_type(
                        ibis_table[col]
                    )
                    for col in node.schema.names
                ),
            )

    @_compile_node.register
    def compile_readtable(self, node: nodes.ReadTableNode, ordered: bool = True):
        if ordered:
            return self.compile_read_table_ordered(node)
        else:
            return self.compile_read_table_unordered(node)

    def read_table_as_unordered_ibis(
        self, node: nodes.ReadTableNode
    ) -> ibis.expr.types.Table:
        full_table_name = (
            f"{node.table.project_id}.{node.table.dataset_id}.{node.table.table_id}"
        )
        used_columns = (
            *node.schema.names,
            *[i for i in node.total_order_cols if i not in node.schema.names],
        )
        # Physical schema might include unused columns, unsupported datatypes like JSON
        physical_schema = ibis.backends.bigquery.BigQuerySchema.to_ibis(
            list(i for i in node.table.physical_schema if i.name in used_columns)
        )
        if node.at_time is not None or node.sql_predicate is not None:
            import bigframes.session._io.bigquery

            sql = bigframes.session._io.bigquery.to_query(
                full_table_name,
                columns=used_columns,
                sql_predicate=node.sql_predicate,
                time_travel_timestamp=node.at_time,
            )
            return ibis.backends.bigquery.Backend().sql(
                schema=physical_schema, query=sql
            )
        else:
            return ibis.table(physical_schema, full_table_name)

    def compile_read_table_unordered(self, node: nodes.ReadTableNode):
        ibis_table = self.read_table_as_unordered_ibis(node)
        return compiled.UnorderedIR(
            ibis_table,
            tuple(
                bigframes.core.compile.ibis_types.ibis_value_to_canonical_type(
                    ibis_table[col]
                )
                for col in node.schema.names
            ),
        )

    def compile_read_table_ordered(self, node: nodes.ReadTableNode):
        ibis_table = self.read_table_as_unordered_ibis(node)
        if node.total_order_cols:
            ordering_value_columns = tuple(
                bf_ordering.ascending_over(col) for col in node.total_order_cols
            )
            if node.order_col_is_sequential:
                integer_encoding = bf_ordering.IntegerEncoding(
                    is_encoded=True, is_sequential=True
                )
            else:
                integer_encoding = bf_ordering.IntegerEncoding()
            ordering: bf_ordering.RowOrdering = bf_ordering.TotalOrdering(
                ordering_value_columns,
                integer_encoding=integer_encoding,
                total_ordering_columns=frozenset(node.total_order_cols),
            )
            hidden_columns = ()
        elif self.strict:
            ibis_table, ordering = default_ordering.gen_default_ordering(
                ibis_table, use_double_hash=True
            )
            hidden_columns = tuple(
                ibis_table[col]
                for col in ibis_table.columns
                if col not in node.schema.names
            )
        else:
            # In unstrict mode, don't generate total ordering from hashing as this is
            # expensive (prevent removing any columns from table scan)
            ordering, hidden_columns = bf_ordering.RowOrdering(), ()
        return compiled.OrderedIR(
            ibis_table,
            columns=tuple(
                bigframes.core.compile.ibis_types.ibis_value_to_canonical_type(
                    ibis_table[col]
                )
                for col in node.schema.names
            ),
            ordering=ordering,
            hidden_ordering_columns=hidden_columns,
        )

    @_compile_node.register
    def compile_promote_offsets(
        self, node: nodes.PromoteOffsetsNode, ordered: bool = True
    ):
        result = self.compile_ordered_ir(node.child).promote_offsets(node.col_id)
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
        return result.selection(node.input_output_pairs)

    @_compile_node.register
    def compile_projection(self, node: nodes.ProjectionNode, ordered: bool = True):
        result = self.compile_node(node.child, ordered)
        return result.projection(node.assignments)

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
        if ordered and has_ordered_aggregation_ops:
            return self.compile_ordered_ir(node.child).aggregate(
                node.aggregations, node.by_column_ids, node.dropna
            )
        else:
            result = self.compile_unordered_ir(node.child).aggregate(
                node.aggregations, node.by_column_ids, node.dropna
            )
            return result if ordered else result.to_unordered()

    @_compile_node.register
    def compile_window(self, node: nodes.WindowOpNode, ordered: bool = True):
        result = self.compile_ordered_ir(node.child).project_window_op(
            node.column_name,
            node.op,
            node.window_spec,
            node.output_name,
            never_skip_nulls=node.never_skip_nulls,
        )
        return result if ordered else result.to_unordered()

    @_compile_node.register
    def compile_reproject(self, node: nodes.ReprojectOpNode, ordered: bool = True):
        return self.compile_node(node.child, ordered)._reproject_to_table()

    @_compile_node.register
    def compile_explode(self, node: nodes.ExplodeNode, ordered: bool = True):
        return self.compile_node(node.child, ordered).explode(node.column_ids)

    @_compile_node.register
    def compile_random_sample(self, node: nodes.RandomSampleNode, ordered: bool = True):
        return self.compile_node(node.child, ordered)._uniform_sampling(node.fraction)
