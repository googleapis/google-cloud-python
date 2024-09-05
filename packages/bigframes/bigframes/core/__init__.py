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
import io
import itertools
import typing
from typing import Iterable, Optional, Sequence
import warnings

import google.cloud.bigquery
import pandas
import pyarrow as pa
import pyarrow.feather as pa_feather

import bigframes.core.compile
import bigframes.core.expression as ex
import bigframes.core.guid
import bigframes.core.join_def as join_def
import bigframes.core.local_data as local_data
import bigframes.core.nodes as nodes
from bigframes.core.ordering import OrderingExpression
import bigframes.core.ordering as orderings
import bigframes.core.rewrite
import bigframes.core.schema as schemata
import bigframes.core.utils
from bigframes.core.window_spec import WindowSpec
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.session._io.bigquery

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
        adapted_table = local_data.adapt_pa_table(arrow_table)
        schema = local_data.arrow_schema_to_bigframes(adapted_table.schema)

        iobytes = io.BytesIO()
        pa_feather.write_feather(adapted_table, iobytes)
        node = nodes.ReadLocalNode(
            iobytes.getvalue(),
            data_schema=schema,
            session=session,
            n_rows=arrow_table.num_rows,
        )
        return cls(node)

    @classmethod
    def from_table(
        cls,
        table: google.cloud.bigquery.Table,
        schema: schemata.ArraySchema,
        session: Session,
        *,
        predicate: Optional[str] = None,
        at_time: Optional[datetime.datetime] = None,
        primary_key: Sequence[str] = (),
        offsets_col: Optional[str] = None,
    ):
        if offsets_col and primary_key:
            raise ValueError("must set at most one of 'offests', 'primary_key'")
        if any(i.field_type == "JSON" for i in table.schema if i.name in schema.names):
            warnings.warn(
                "Interpreting JSON column(s) as StringDtype. This behavior may change in future versions.",
                bigframes.exceptions.PreviewWarning,
            )
        node = nodes.ReadTableNode(
            table=nodes.GbqTable.from_table(table),
            total_order_cols=(offsets_col,) if offsets_col else tuple(primary_key),
            order_col_is_sequential=(offsets_col is not None),
            columns=schema,
            at_time=at_time,
            table_session=session,
            sql_predicate=predicate,
        )
        return cls(node)

    @property
    def column_ids(self) -> typing.Sequence[str]:
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

    @functools.cached_property
    def _compiled_schema(self) -> schemata.ArraySchema:
        return bigframes.core.compile.test_only_ibis_inferred_schema(self.node)

    def as_cached(
        self: ArrayValue,
        cache_table: google.cloud.bigquery.Table,
        ordering: Optional[orderings.RowOrdering],
    ) -> ArrayValue:
        """
        Replace the node with an equivalent one that references a tabel where the value has been materialized to.
        """
        node = nodes.CachedTableNode(
            original_node=self.node,
            table=nodes.GbqTable.from_table(cache_table),
            ordering=ordering,
        )
        return ArrayValue(node)

    def _try_evaluate_local(self):
        """Use only for unit testing paths - not fully featured. Will throw exception if fails."""
        return bigframes.core.compile.test_only_try_evaluate(self.node)

    def get_column_type(self, key: str) -> bigframes.dtypes.Dtype:
        return self.schema.get_type(key)

    def row_count(self) -> ArrayValue:
        """Get number of rows in ArrayValue as a single-entry ArrayValue."""
        return ArrayValue(nodes.RowCountNode(child=self.node))

    # Operations
    def filter_by_id(self, predicate_id: str, keep_null: bool = False) -> ArrayValue:
        """Filter the table on a given expression, the predicate must be a boolean series aligned with the table expression."""
        predicate: ex.Expression = ex.free_var(predicate_id)
        if keep_null:
            predicate = ops.fillna_op.as_expr(predicate, ex.const(True))
        return self.filter(predicate)

    def filter(self, predicate: ex.Expression):
        return ArrayValue(nodes.FilterNode(child=self.node, predicate=predicate))

    def order_by(self, by: Sequence[OrderingExpression]) -> ArrayValue:
        return ArrayValue(nodes.OrderByNode(child=self.node, by=tuple(by)))

    def reversed(self) -> ArrayValue:
        return ArrayValue(nodes.ReversedNode(child=self.node))

    def promote_offsets(self, col_id: str) -> ArrayValue:
        """
        Convenience function to promote copy of column offsets to a value column. Can be used to reset index.
        """
        if self.node.order_ambiguous and not (self.session._strictly_ordered):
            if not self.session._allows_ambiguity:
                raise ValueError(
                    "Generating offsets not supported in partial ordering mode"
                )
            else:
                warnings.warn(
                    "Window ordering may be ambiguous, this can cause unstable results.",
                    bigframes.exceptions.AmbiguousWindowWarning,
                )

        return ArrayValue(nodes.PromoteOffsetsNode(child=self.node, col_id=col_id))

    def concat(self, other: typing.Sequence[ArrayValue]) -> ArrayValue:
        """Append together multiple ArrayValue objects."""
        return ArrayValue(
            nodes.ConcatNode(children=tuple([self.node, *[val.node for val in other]]))
        )

    def project_to_id(self, expression: ex.Expression, output_id: str):
        return ArrayValue(
            nodes.ProjectionNode(
                child=self.node,
                assignments=(
                    (
                        expression,
                        output_id,
                    ),
                ),
            )
        )

    def assign(self, source_id: str, destination_id: str) -> ArrayValue:
        if destination_id in self.column_ids:  # Mutate case
            exprs = [
                (
                    (source_id if (col_id == destination_id) else col_id),
                    col_id,
                )
                for col_id in self.column_ids
            ]
        else:  # append case
            self_projection = ((col_id, col_id) for col_id in self.column_ids)
            exprs = [*self_projection, (source_id, destination_id)]
        return ArrayValue(
            nodes.SelectionNode(
                child=self.node,
                input_output_pairs=tuple(exprs),
            )
        )

    def create_constant(
        self,
        destination_id: str,
        value: typing.Any,
        dtype: typing.Optional[bigframes.dtypes.Dtype],
    ) -> ArrayValue:
        if pandas.isna(value):
            # Need to assign a data type when value is NaN.
            dtype = dtype or bigframes.dtypes.DEFAULT_DTYPE

        return ArrayValue(
            nodes.ProjectionNode(
                child=self.node,
                assignments=((ex.const(value, dtype), destination_id),),
            )
        )

    def select_columns(self, column_ids: typing.Sequence[str]) -> ArrayValue:
        # This basically just drops and reorders columns - logically a no-op except as a final step
        selections = ((col_id, col_id) for col_id in column_ids)
        return ArrayValue(
            nodes.SelectionNode(
                child=self.node,
                input_output_pairs=tuple(selections),
            )
        )

    def drop_columns(self, columns: Iterable[str]) -> ArrayValue:
        new_projection = (
            (col_id, col_id) for col_id in self.column_ids if col_id not in columns
        )
        return ArrayValue(
            nodes.SelectionNode(
                child=self.node,
                input_output_pairs=tuple(new_projection),
            )
        )

    def aggregate(
        self,
        aggregations: typing.Sequence[typing.Tuple[ex.Aggregation, str]],
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
        return ArrayValue(
            nodes.AggregateNode(
                child=self.node,
                aggregations=tuple(aggregations),
                by_column_ids=tuple(by_column_ids),
                dropna=dropna,
            )
        )

    def project_window_op(
        self,
        column_name: str,
        op: agg_ops.UnaryWindowOp,
        window_spec: WindowSpec,
        output_name=None,
        *,
        never_skip_nulls=False,
        skip_reproject_unsafe: bool = False,
    ) -> ArrayValue:
        """
        Creates a new expression based on this expression with unary operation applied to one column.
        column_name: the id of the input column present in the expression
        op: the windowable operator to apply to the input column
        window_spec: a specification of the window over which to apply the operator
        output_name: the id to assign to the output of the operator, by default will replace input col if distinct output id not provided
        never_skip_nulls: will disable null skipping for operators that would otherwise do so
        skip_reproject_unsafe: skips the reprojection step, can be used when performing many non-dependent window operations, user responsible for not nesting window expressions, or using outputs as join, filter or aggregation keys before a reprojection
        """
        # TODO: Support non-deterministic windowing
        if window_spec.row_bounded or not op.order_independent:
            if self.node.order_ambiguous and not self.session._strictly_ordered:
                if not self.session._allows_ambiguity:
                    raise ValueError(
                        "Generating offsets not supported in partial ordering mode"
                    )
                else:
                    warnings.warn(
                        "Window ordering may be ambiguous, this can cause unstable results.",
                        bigframes.exceptions.AmbiguousWindowWarning,
                    )

        return ArrayValue(
            nodes.WindowOpNode(
                child=self.node,
                column_name=column_name,
                op=op,
                window_spec=window_spec,
                output_name=output_name,
                never_skip_nulls=never_skip_nulls,
                skip_reproject_unsafe=skip_reproject_unsafe,
            )
        )

    def _reproject_to_table(self) -> ArrayValue:
        """
        Internal operators that projects the internal representation into a
        new ibis table expression where each value column is a direct
        reference to a column in that table expression. Needed after
        some operations such as window operations that cannot be used
        recursively in projections.
        """
        return ArrayValue(
            nodes.ReprojectOpNode(
                child=self.node,
            )
        )

    def unpivot(
        self,
        row_labels: typing.Sequence[typing.Hashable],
        unpivot_columns: typing.Sequence[
            typing.Tuple[str, typing.Tuple[typing.Optional[str], ...]]
        ],
        *,
        passthrough_columns: typing.Sequence[str] = (),
        index_col_ids: typing.Sequence[str] = ["index"],
        join_side: typing.Literal["left", "right"] = "left",
    ) -> ArrayValue:
        """
        Unpivot ArrayValue columns.

        Args:
            row_labels: Identifies the source of the row. Must be equal to length to source column list in unpivot_columns argument.
            unpivot_columns: Mapping of column id to list of input column ids. Lists of input columns may use None.
            passthrough_columns: Columns that will not be unpivoted. Column id will be preserved.
            index_col_id (str): The column id to be used for the row labels.

        Returns:
            ArrayValue: The unpivoted ArrayValue
        """
        # There will be N labels, used to disambiguate which of N source columns produced each output row
        explode_offsets_id = bigframes.core.guid.generate_guid("unpivot_offsets_")
        labels_array = self._create_unpivot_labels_array(
            row_labels, index_col_ids, explode_offsets_id
        )

        # Unpivot creates N output rows for each input row, labels disambiguate these N rows
        joined_array = self._cross_join_w_labels(labels_array, join_side)

        # Build the output rows as a case statment that selects between the N input columns
        unpivot_exprs = []
        # Supports producing multiple stacked ouput columns for stacking only part of hierarchical index
        for col_id, input_ids in unpivot_columns:
            # row explode offset used to choose the input column
            # we use offset instead of label as labels are not necessarily unique
            cases = itertools.chain(
                *(
                    (
                        ops.eq_op.as_expr(explode_offsets_id, ex.const(i)),
                        ex.free_var(id_or_null)
                        if (id_or_null is not None)
                        else ex.const(None),
                    )
                    for i, id_or_null in enumerate(input_ids)
                )
            )
            col_expr = ops.case_when_op.as_expr(*cases)
            unpivot_exprs.append((col_expr, col_id))

        unpivot_col_ids = [id for id, _ in unpivot_columns]
        return ArrayValue(
            nodes.ProjectionNode(
                child=joined_array.node,
                assignments=(*unpivot_exprs,),
            )
        ).select_columns([*index_col_ids, *unpivot_col_ids, *passthrough_columns])

    def _cross_join_w_labels(
        self, labels_array: ArrayValue, join_side: typing.Literal["left", "right"]
    ) -> ArrayValue:
        """
        Convert each row in self to N rows, one for each label in labels array.
        """
        table_join_side = (
            join_def.JoinSide.LEFT if join_side == "left" else join_def.JoinSide.RIGHT
        )
        labels_join_side = table_join_side.inverse()
        labels_mappings = tuple(
            join_def.JoinColumnMapping(labels_join_side, id, id)
            for id in labels_array.schema.names
        )
        table_mappings = tuple(
            join_def.JoinColumnMapping(table_join_side, id, id)
            for id in self.schema.names
        )
        join = join_def.JoinDefinition(
            conditions=(), mappings=(*labels_mappings, *table_mappings), type="cross"
        )
        if join_side == "left":
            joined_array = self.relational_join(labels_array, join_def=join)
        else:
            joined_array = labels_array.relational_join(self, join_def=join)
        return joined_array

    def _create_unpivot_labels_array(
        self,
        former_column_labels: typing.Sequence[typing.Hashable],
        col_ids: typing.Sequence[str],
        offsets_id: str,
    ) -> ArrayValue:
        """Create an ArrayValue from a list of label tuples."""
        rows = []
        for row_offset in range(len(former_column_labels)):
            row_label = former_column_labels[row_offset]
            row_label = (row_label,) if not isinstance(row_label, tuple) else row_label
            row = {
                col_ids[i]: (row_label[i] if pandas.notnull(row_label[i]) else None)
                for i in range(len(col_ids))
            }
            row[offsets_id] = row_offset
            rows.append(row)

        return ArrayValue.from_pyarrow(pa.Table.from_pylist(rows), session=self.session)

    def relational_join(
        self,
        other: ArrayValue,
        join_def: join_def.JoinDefinition,
    ) -> ArrayValue:
        join_node = nodes.JoinNode(
            left_child=self.node,
            right_child=other.node,
            join=join_def,
        )
        return ArrayValue(join_node)

    def try_align_as_projection(
        self,
        other: ArrayValue,
        join_type: join_def.JoinType,
        join_keys: typing.Tuple[join_def.CoalescedColumnMapping, ...],
        mappings: typing.Tuple[join_def.JoinColumnMapping, ...],
    ) -> typing.Optional[ArrayValue]:
        result = bigframes.core.rewrite.join_as_projection(
            self.node, other.node, join_keys, mappings, join_type
        )
        if result is not None:
            return ArrayValue(result)
        return None

    def explode(self, column_ids: typing.Sequence[str]) -> ArrayValue:
        assert len(column_ids) > 0
        for column_id in column_ids:
            assert bigframes.dtypes.is_array_like(self.get_column_type(column_id))

        return ArrayValue(
            nodes.ExplodeNode(child=self.node, column_ids=tuple(column_ids))
        )

    def _uniform_sampling(self, fraction: float) -> ArrayValue:
        """Sampling the table on given fraction.

        .. warning::
            The row numbers of result is non-deterministic, avoid to use.
        """
        return ArrayValue(nodes.RandomSampleNode(self.node, fraction))
