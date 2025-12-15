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

from dataclasses import dataclass
import datetime
import functools
import typing
from typing import Iterable, List, Mapping, Optional, Sequence, Tuple

import google.cloud.bigquery
import pandas
import pyarrow as pa

from bigframes.core import (
    agg_expressions,
    bq_data,
    expression_factoring,
    join_def,
    local_data,
)
import bigframes.core.expression as ex
import bigframes.core.guid
import bigframes.core.identifiers as ids
import bigframes.core.nodes as nodes
from bigframes.core.ordering import OrderingExpression
import bigframes.core.ordering as orderings
import bigframes.core.schema as schemata
import bigframes.core.tree_properties
from bigframes.core.window_spec import WindowSpec
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops

if typing.TYPE_CHECKING:
    from bigframes.session import Session

ORDER_ID_COLUMN = "bigframes_ordering_id"
PREDICATE_COLUMN = "bigframes_predicate"


@dataclass(frozen=True)
class ArrayValue:
    """
    ArrayValue is an immutable type representing a 2D array with per-column types.
    """

    node: nodes.BigFrameNode

    @classmethod
    def from_pyarrow(cls, arrow_table: pa.Table, session: Session):
        data_source = local_data.ManagedArrowTable.from_pyarrow(arrow_table)
        return cls.from_managed(source=data_source, session=session)

    @classmethod
    def from_managed(cls, source: local_data.ManagedArrowTable, session: Session):
        scan_list = nodes.ScanList(
            tuple(
                nodes.ScanItem(ids.ColumnId(item.column), item.column)
                for item in source.schema.items
            )
        )
        node = nodes.ReadLocalNode(
            source,
            session=session,
            scan_list=scan_list,
        )
        return cls(node)

    @classmethod
    def from_range(cls, start, end, step):
        return cls(
            nodes.FromRangeNode(
                start=start.node,
                end=end.node,
                step=step,
            )
        )

    @classmethod
    def from_table(
        cls,
        table: google.cloud.bigquery.Table,
        session: Session,
        *,
        columns: Optional[Sequence[str]] = None,
        predicate: Optional[str] = None,
        at_time: Optional[datetime.datetime] = None,
        primary_key: Sequence[str] = (),
        offsets_col: Optional[str] = None,
        n_rows: Optional[int] = None,
    ):
        if offsets_col and primary_key:
            raise ValueError("must set at most one of 'offests', 'primary_key'")
        # define data source only for needed columns, this makes row-hashing cheaper
        table_def = bq_data.GbqTable.from_table(table, columns=columns or ())

        # create ordering from info
        ordering = None
        if offsets_col:
            ordering = orderings.TotalOrdering.from_offset_col(offsets_col)
        elif primary_key:
            ordering = orderings.TotalOrdering.from_primary_key(
                [ids.ColumnId(key_part) for key_part in primary_key]
            )

        bf_schema = schemata.ArraySchema.from_bq_table(table, columns=columns)
        # Scan all columns by default, we define this list as it can be pruned while preserving source_def
        scan_list = nodes.ScanList(
            tuple(
                nodes.ScanItem(ids.ColumnId(item.column), item.column)
                for item in bf_schema.items
            )
        )
        source_def = bq_data.BigqueryDataSource(
            table=table_def,
            schema=bf_schema,
            at_time=at_time,
            sql_predicate=predicate,
            ordering=ordering,
            n_rows=n_rows,
        )
        return cls.from_bq_data_source(source_def, scan_list, session)

    @classmethod
    def from_bq_data_source(
        cls,
        source: bq_data.BigqueryDataSource,
        scan_list: nodes.ScanList,
        session: Session,
    ):
        node = nodes.ReadTableNode(
            source=source,
            scan_list=scan_list,
            table_session=session,
        )
        return cls(node)

    @property
    def column_ids(self) -> typing.Sequence[str]:
        """Returns column ids as strings."""
        return self.schema.names

    @property
    def session(self) -> Session:
        required_session = self.node.session
        from bigframes import get_global_session

        return (
            required_session if (required_session is not None) else get_global_session()
        )

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        return self.node.schema

    @property
    def explicitly_ordered(self) -> bool:
        # see BigFrameNode.explicitly_ordered
        return self.node.explicitly_ordered

    @property
    def order_ambiguous(self) -> bool:
        # see BigFrameNode.order_ambiguous
        return self.node.order_ambiguous

    @property
    def supports_fast_peek(self) -> bool:
        return bigframes.core.tree_properties.can_fast_peek(self.node)

    def get_column_type(self, key: str) -> bigframes.dtypes.Dtype:
        return self.schema.get_type(key)

    def row_count(self) -> ArrayValue:
        """Get number of rows in ArrayValue as a single-entry ArrayValue."""
        return ArrayValue(
            nodes.AggregateNode(
                child=self.node,
                aggregations=(
                    (
                        agg_expressions.NullaryAggregation(agg_ops.size_op),
                        ids.ColumnId(bigframes.core.guid.generate_guid()),
                    ),
                ),
            )
        )

    # Operations
    def filter_by_id(self, predicate_id: str, keep_null: bool = False) -> ArrayValue:
        """Filter the table on a given expression, the predicate must be a boolean series aligned with the table expression."""
        predicate: ex.Expression = ex.deref(predicate_id)
        if keep_null:
            predicate = ops.fillna_op.as_expr(predicate, ex.const(True))
        return self.filter(predicate)

    def filter(self, predicate: ex.Expression):
        return ArrayValue(nodes.FilterNode(child=self.node, predicate=predicate))

    def order_by(
        self, by: Sequence[OrderingExpression], is_total_order: bool = False
    ) -> ArrayValue:
        return ArrayValue(
            nodes.OrderByNode(
                child=self.node, by=tuple(by), is_total_order=is_total_order
            )
        )

    def reversed(self) -> ArrayValue:
        return ArrayValue(nodes.ReversedNode(child=self.node))

    def slice(
        self, start: Optional[int], stop: Optional[int], step: Optional[int]
    ) -> ArrayValue:
        return ArrayValue(
            nodes.SliceNode(
                self.node,
                start=start,
                stop=stop,
                step=step if (step is not None) else 1,
            )
        )

    def promote_offsets(self) -> Tuple[ArrayValue, str]:
        """
        Convenience function to promote copy of column offsets to a value column. Can be used to reset index.
        """
        col_id = self._gen_namespaced_uid()
        return (
            ArrayValue(
                nodes.PromoteOffsetsNode(child=self.node, col_id=ids.ColumnId(col_id))
            ),
            col_id,
        )

    def concat(self, other: typing.Sequence[ArrayValue]) -> ArrayValue:
        """Append together multiple ArrayValue objects."""
        return ArrayValue(
            nodes.ConcatNode(
                children=tuple([self.node, *[val.node for val in other]]),
                output_ids=tuple(
                    ids.ColumnId(bigframes.core.guid.generate_guid())
                    for id in self.column_ids
                ),
            )
        )

    def compute_values(self, assignments: Sequence[ex.Expression]):
        col_ids = self._gen_namespaced_uids(len(assignments))
        ex_id_pairs = tuple(
            (ex, ids.ColumnId(id)) for ex, id in zip(assignments, col_ids)
        )
        return (
            ArrayValue(nodes.ProjectionNode(child=self.node, assignments=ex_id_pairs)),
            col_ids,
        )

    def compute_general_expression(self, assignments: Sequence[ex.Expression]):
        """
        Applies arbitrary column expressions to the current execution block.

        This method transforms the logical plan by applying a sequence of expressions that
        preserve the length of the input columns. It supports both scalar operations
        and window functions. Each expression is assigned a unique internal column identifier.

        Args:
            assignments (Sequence[ex.Expression]): A sequence of expression objects
                representing the transformations to apply to the columns.

        Returns:
            Tuple[ArrayValue, Tuple[str, ...]]: A tuple containing:
                - An `ArrayValue` wrapping the new root node of the updated logical plan.
                - A tuple of strings representing the unique column IDs generated for
                  each expression in the assignments.
        """
        named_exprs = [
            nodes.ColumnDef(expr, ids.ColumnId.unique()) for expr in assignments
        ]
        # TODO: Push this to rewrite later to go from block expression to planning form
        new_root = expression_factoring.apply_col_exprs_to_plan(self.node, named_exprs)

        target_ids = tuple(named_expr.id for named_expr in named_exprs)
        return (ArrayValue(new_root), target_ids)

    def compute_general_reduction(
        self,
        assignments: Sequence[ex.Expression],
        by_column_ids: typing.Sequence[str] = (),
        *,
        dropna: bool = False,
    ):
        """
        Applies arbitrary aggregation expressions to the block, optionally grouped by keys.

        This method handles reduction operations (e.g., sum, mean, count) that collapse
        multiple input rows into a single scalar value per group. If grouping keys are
        provided, the operation is performed per group; otherwise, it is a global reduction.

        Note: Intermediate aggregations (those that are inputs to further aggregations)
        must be windowizable. Notably excluded are approx quantile, top count ops.

        Args:
            assignments (Sequence[ex.Expression]): A sequence of aggregation expressions
                to be calculated.
            by_column_ids (typing.Sequence[str], optional): A sequence of column IDs
                to use as grouping keys. Defaults to an empty tuple (global reduction).
            dropna (bool, optional): If True, rows containing null values in the
                `by_column_ids` columns will be filtered out before the reduction
                is applied. Defaults to False.

        Returns:
            ArrayValue:
               The new root node representing the aggregation/group-by result.
        """
        plan = self.node

        # shortcircuit to keep things simple if all aggs are simple
        # TODO: Fully unify paths once rewriters are strong enough to simplify complexity from full path
        def _is_direct_agg(agg_expr):
            return isinstance(agg_expr, agg_expressions.Aggregation) and all(
                isinstance(child, (ex.DerefOp, ex.ScalarConstantExpression))
                for child in agg_expr.children
            )

        if all(_is_direct_agg(agg) for agg in assignments):
            agg_defs = tuple((agg, ids.ColumnId.unique()) for agg in assignments)
            return ArrayValue(
                nodes.AggregateNode(
                    child=self.node,
                    aggregations=agg_defs,  # type: ignore
                    by_column_ids=tuple(map(ex.deref, by_column_ids)),
                    dropna=dropna,
                )
            )

        if dropna:
            for col_id in by_column_ids:
                plan = nodes.FilterNode(plan, ops.notnull_op.as_expr(col_id))

        named_exprs = [
            nodes.ColumnDef(expr, ids.ColumnId.unique()) for expr in assignments
        ]
        # TODO: Push this to rewrite later to go from block expression to planning form
        new_root = expression_factoring.apply_agg_exprs_to_plan(
            plan, named_exprs, grouping_keys=[ex.deref(by) for by in by_column_ids]
        )
        return ArrayValue(new_root)

    def project_to_id(self, expression: ex.Expression):
        array_val, ids = self.compute_values(
            [expression],
        )
        return array_val, ids[0]

    def assign(self, source_id: str, destination_id: str) -> ArrayValue:
        if destination_id in self.column_ids:  # Mutate case
            exprs = [
                (
                    bigframes.core.nodes.AliasedRef(
                        ex.deref(source_id if (col_id == destination_id) else col_id),
                        ids.ColumnId(col_id),
                    )
                )
                for col_id in self.column_ids
            ]
        else:  # append case
            self_projection = (
                bigframes.core.nodes.AliasedRef.identity(ids.ColumnId(col_id))
                for col_id in self.column_ids
            )
            exprs = [
                *self_projection,
                (
                    bigframes.core.nodes.AliasedRef(
                        ex.deref(source_id), ids.ColumnId(destination_id)
                    )
                ),
            ]
        return ArrayValue(
            nodes.SelectionNode(
                child=self.node,
                input_output_pairs=tuple(exprs),
            )
        )

    def create_constant(
        self,
        value: typing.Any,
        dtype: typing.Optional[bigframes.dtypes.Dtype],
    ) -> Tuple[ArrayValue, str]:
        if pandas.isna(value):
            # Need to assign a data type when value is NaN.
            dtype = dtype or bigframes.dtypes.DEFAULT_DTYPE

        return self.project_to_id(ex.const(value, dtype))

    def select_columns(
        self, column_ids: typing.Sequence[str], allow_renames: bool = False
    ) -> ArrayValue:
        # This basically just drops and reorders columns - logically a no-op except as a final step
        selections = []
        seen = set()

        for id in column_ids:
            if id not in seen:
                ref = nodes.AliasedRef.identity(ids.ColumnId(id))
            elif allow_renames:
                ref = nodes.AliasedRef(
                    ex.deref(id), ids.ColumnId(bigframes.core.guid.generate_guid())
                )
            else:
                raise ValueError(
                    "Must set allow_renames=True to select columns repeatedly"
                )
            selections.append(ref)
            seen.add(id)

        return ArrayValue(
            nodes.SelectionNode(
                child=self.node,
                input_output_pairs=tuple(selections),
            )
        )

    def rename_columns(self, col_id_overrides: Mapping[str, str]) -> ArrayValue:
        if not col_id_overrides:
            return self
        output_ids = [col_id_overrides.get(id, id) for id in self.node.schema.names]
        return ArrayValue(
            nodes.SelectionNode(
                self.node,
                tuple(
                    nodes.AliasedRef(ex.DerefOp(old_id), ids.ColumnId(out_id))
                    for old_id, out_id in zip(self.node.ids, output_ids)
                ),
            )
        )

    def drop_columns(self, columns: Iterable[str]) -> ArrayValue:
        return self.select_columns(
            [col_id for col_id in self.column_ids if col_id not in columns]
        )

    def aggregate(
        self,
        aggregations: typing.Sequence[typing.Tuple[agg_expressions.Aggregation, str]],
        by_column_ids: typing.Sequence[str] = (),
        dropna: bool = True,
    ) -> ArrayValue:
        """
        Apply aggregations to the expression.
        Arguments:
            aggregations: input_column_id, operation, output_column_id tuples
            by_column_id: column id of the aggregation key, this is preserved through the transform
            dropna: whether null keys should be dropped
        """
        agg_defs = tuple((agg, ids.ColumnId(name)) for agg, name in aggregations)
        return ArrayValue(
            nodes.AggregateNode(
                child=self.node,
                aggregations=agg_defs,
                by_column_ids=tuple(map(ex.deref, by_column_ids)),
                dropna=dropna,
            )
        )

    def project_window_expr(
        self,
        expressions: Sequence[agg_expressions.Aggregation],
        window: WindowSpec,
    ):
        id_strings = [self._gen_namespaced_uid() for _ in expressions]
        agg_exprs = tuple(
            nodes.ColumnDef(expression, ids.ColumnId(id_str))
            for expression, id_str in zip(expressions, id_strings)
        )

        return (
            ArrayValue(
                nodes.WindowOpNode(
                    child=self.node,
                    agg_exprs=agg_exprs,
                    window_spec=window,
                )
            ),
            id_strings,
        )

    def isin(
        self,
        other: ArrayValue,
        lcol: str,
    ) -> typing.Tuple[ArrayValue, str]:
        assert len(other.column_ids) == 1
        node = nodes.InNode(
            self.node,
            other.node,
            ex.deref(lcol),
            indicator_col=ids.ColumnId.unique(),
        )
        return ArrayValue(node), node.indicator_col.name

    def relational_join(
        self,
        other: ArrayValue,
        conditions: typing.Tuple[typing.Tuple[str, str], ...] = (),
        type: typing.Literal["inner", "outer", "left", "right", "cross"] = "inner",
        propogate_order: Optional[bool] = None,
    ) -> typing.Tuple[ArrayValue, typing.Tuple[dict[str, str], dict[str, str]]]:
        for lcol, rcol in conditions:
            ltype = self.get_column_type(lcol)
            rtype = other.get_column_type(rcol)
            if not bigframes.dtypes.can_compare(ltype, rtype):
                raise TypeError(
                    f"Cannot join with non-comparable join key types: {ltype}, {rtype}"
                )

        l_mapping = {  # Identity mapping, only rename right side
            lcol.name: lcol.name for lcol in self.node.ids
        }
        other_node, r_mapping = self.prepare_join_names(other)
        join_node = nodes.JoinNode(
            left_child=self.node,
            right_child=other_node,
            conditions=tuple(
                (ex.deref(l_mapping[l_col]), ex.deref(r_mapping[r_col]))
                for l_col, r_col in conditions
            ),
            type=type,
            propogate_order=propogate_order or self.session._strictly_ordered,
        )
        return ArrayValue(join_node), (l_mapping, r_mapping)

    def try_row_join(
        self,
        other: ArrayValue,
        conditions: typing.Tuple[typing.Tuple[str, str], ...] = (),
    ) -> Optional[
        typing.Tuple[ArrayValue, typing.Tuple[dict[str, str], dict[str, str]]]
    ]:
        l_mapping = {  # Identity mapping, only rename right side
            lcol.name: lcol.name for lcol in self.node.ids
        }
        other_node, r_mapping = self.prepare_join_names(other)
        import bigframes.core.rewrite

        result_node = bigframes.core.rewrite.try_row_join(
            self.node, other_node, conditions
        )
        if result_node is None:
            return None

        return (
            ArrayValue(result_node),
            (l_mapping, r_mapping),
        )

    def prepare_join_names(
        self, other: ArrayValue
    ) -> Tuple[bigframes.core.nodes.BigFrameNode, dict[str, str]]:
        if set(other.node.ids) & set(self.node.ids):
            r_mapping = {  # Rename conflicting names
                rcol.name: rcol.name
                if (rcol.name not in self.column_ids)
                else bigframes.core.guid.generate_guid()
                for rcol in other.node.ids
            }
            return (
                nodes.SelectionNode(
                    other.node,
                    tuple(
                        bigframes.core.nodes.AliasedRef(
                            ex.deref(old_id), ids.ColumnId(new_id)
                        )
                        for old_id, new_id in r_mapping.items()
                    ),
                ),
                r_mapping,
            )
        else:
            return other.node, {id: id for id in other.column_ids}

    def try_legacy_row_join(
        self,
        other: ArrayValue,
        join_type: join_def.JoinType,
        join_keys: typing.Tuple[join_def.CoalescedColumnMapping, ...],
        mappings: typing.Tuple[join_def.JoinColumnMapping, ...],
    ) -> typing.Optional[ArrayValue]:
        import bigframes.core.rewrite

        result = bigframes.core.rewrite.legacy_join_as_projection(
            self.node, other.node, join_keys, mappings, join_type
        )
        if result is not None:
            return ArrayValue(result)
        return None

    def explode(self, column_ids: typing.Sequence[str]) -> ArrayValue:
        assert len(column_ids) > 0
        for column_id in column_ids:
            assert bigframes.dtypes.is_array_like(self.get_column_type(column_id))

        offsets = tuple(ex.deref(id) for id in column_ids)
        return ArrayValue(nodes.ExplodeNode(child=self.node, column_ids=offsets))

    def _uniform_sampling(self, fraction: float) -> ArrayValue:
        """Sampling the table on given fraction.

        .. warning::
            The row numbers of result is non-deterministic, avoid to use.
        """
        return ArrayValue(nodes.RandomSampleNode(self.node, fraction))

    # Deterministically generate namespaced ids for new variables
    # These new ids are only unique within the current namespace.
    # Many operations, such as joins, create new namespaces. See: BigFrameNode.defines_namespace
    # When migrating to integer ids, these will generate the next available integer, in order to densely pack ids
    # this will help represent variables sets as compact bitsets
    def _gen_namespaced_uid(self) -> str:
        return self._gen_namespaced_uids(1)[0]

    def _gen_namespaced_uids(self, n: int) -> List[str]:
        return [ids.ColumnId.unique().name for _ in range(n)]
