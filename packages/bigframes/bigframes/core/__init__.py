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
import functools
import io
import typing
from typing import Iterable, Sequence

import ibis.expr.types as ibis_types
import pandas
import pyarrow as pa
import pyarrow.feather as pa_feather

import bigframes.core.compile as compiling
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
    def from_ibis(
        cls,
        session: Session,
        table: ibis_types.Table,
        columns: Sequence[ibis_types.Value],
        hidden_ordering_columns: Sequence[ibis_types.Value],
        ordering: orderings.ExpressionOrdering,
    ):
        node = nodes.ReadGbqNode(
            table=table,
            table_session=session,
            columns=tuple(
                bigframes.dtypes.ibis_value_to_canonical_type(column)
                for column in columns
            ),
            hidden_ordering_columns=tuple(hidden_ordering_columns),
            ordering=ordering,
        )
        return cls(node)

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
        # TODO: switch to use self.node.schema
        return self._compiled_schema

    @functools.cached_property
    def _compiled_schema(self) -> schemata.ArraySchema:
        compiled = self._compile_unordered()
        items = tuple(
            schemata.SchemaItem(id, compiled.get_column_type(id))
            for id in compiled.column_ids
        )
        return schemata.ArraySchema(items)

    def validate_schema(self):
        tree_derived = self.node.schema
        ibis_derived = self._compiled_schema
        if tree_derived.names != ibis_derived.names:
            raise ValueError(
                f"Unexpected names internal {tree_derived.names} vs compiled {ibis_derived.names}"
            )
        if tree_derived.dtypes != ibis_derived.dtypes:
            raise ValueError(
                f"Unexpected types internal {tree_derived.dtypes} vs compiled {ibis_derived.dtypes}"
            )

    def _try_evaluate_local(self):
        """Use only for unit testing paths - not fully featured. Will throw exception if fails."""
        import ibis

        return ibis.pandas.connect({}).execute(
            self._compile_ordered()._to_ibis_expr(ordering_mode="unordered")
        )

    def get_column_type(self, key: str) -> bigframes.dtypes.Dtype:
        return self.schema.get_type(key)

    def _compile_ordered(self) -> compiling.OrderedIR:
        return compiling.compile_ordered_ir(self.node)

    def _compile_unordered(self) -> compiling.UnorderedIR:
        return compiling.compile_unordered_ir(self.node)

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
        return ArrayValue(nodes.PromoteOffsetsNode(child=self.node, col_id=col_id))

    def concat(self, other: typing.Sequence[ArrayValue]) -> ArrayValue:
        """Append together multiple ArrayValue objects."""
        return ArrayValue(
            nodes.ConcatNode(children=tuple([self.node, *[val.node for val in other]]))
        )

    def project_to_id(self, expression: ex.Expression, output_id: str):
        if output_id in self.column_ids:  # Mutate case
            exprs = [
                ((expression if (col_id == output_id) else ex.free_var(col_id)), col_id)
                for col_id in self.column_ids
            ]
        else:  # append case
            self_projection = (
                (ex.free_var(col_id), col_id) for col_id in self.column_ids
            )
            exprs = [*self_projection, (expression, output_id)]
        return ArrayValue(
            nodes.ProjectionNode(
                child=self.node,
                assignments=tuple(exprs),
            )
        )

    def assign(self, source_id: str, destination_id: str) -> ArrayValue:
        if destination_id in self.column_ids:  # Mutate case
            exprs = [
                (
                    (
                        ex.free_var(source_id)
                        if (col_id == destination_id)
                        else ex.free_var(col_id)
                    ),
                    col_id,
                )
                for col_id in self.column_ids
            ]
        else:  # append case
            self_projection = (
                (ex.free_var(col_id), col_id) for col_id in self.column_ids
            )
            exprs = [*self_projection, (ex.free_var(source_id), destination_id)]
        return ArrayValue(
            nodes.ProjectionNode(
                child=self.node,
                assignments=tuple(exprs),
            )
        )

    def assign_constant(
        self,
        destination_id: str,
        value: typing.Any,
        dtype: typing.Optional[bigframes.dtypes.Dtype],
    ) -> ArrayValue:
        if pandas.isna(value):
            # Need to assign a data type when value is NaN.
            dtype = dtype or bigframes.dtypes.DEFAULT_DTYPE

        if destination_id in self.column_ids:  # Mutate case
            exprs = [
                (
                    (
                        ex.const(value, dtype)
                        if (col_id == destination_id)
                        else ex.free_var(col_id)
                    ),
                    col_id,
                )
                for col_id in self.column_ids
            ]
        else:  # append case
            self_projection = (
                (ex.free_var(col_id), col_id) for col_id in self.column_ids
            )
            exprs = [*self_projection, (ex.const(value, dtype), destination_id)]
        return ArrayValue(
            nodes.ProjectionNode(
                child=self.node,
                assignments=tuple(exprs),
            )
        )

    def select_columns(self, column_ids: typing.Sequence[str]) -> ArrayValue:
        selections = ((ex.free_var(col_id), col_id) for col_id in column_ids)
        return ArrayValue(
            nodes.ProjectionNode(
                child=self.node,
                assignments=tuple(selections),
            )
        )

    def drop_columns(self, columns: Iterable[str]) -> ArrayValue:
        new_projection = (
            (ex.free_var(col_id), col_id)
            for col_id in self.column_ids
            if col_id not in columns
        )
        return ArrayValue(
            nodes.ProjectionNode(
                child=self.node,
                assignments=tuple(new_projection),
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
        dtype: typing.Union[
            bigframes.dtypes.Dtype, typing.Tuple[bigframes.dtypes.Dtype, ...]
        ] = pandas.Float64Dtype(),
        how: typing.Literal["left", "right"] = "left",
    ) -> ArrayValue:
        """
        Unpivot ArrayValue columns.

        Args:
            row_labels: Identifies the source of the row. Must be equal to length to source column list in unpivot_columns argument.
            unpivot_columns: Mapping of column id to list of input column ids. Lists of input columns may use None.
            passthrough_columns: Columns that will not be unpivoted. Column id will be preserved.
            index_col_id (str): The column id to be used for the row labels.
            dtype (dtype or list of dtype): Dtype to use for the unpivot columns. If list, must be equal in number to unpivot_columns.

        Returns:
            ArrayValue: The unpivoted ArrayValue
        """
        return ArrayValue(
            nodes.UnpivotNode(
                child=self.node,
                row_labels=tuple(row_labels),
                unpivot_columns=tuple(unpivot_columns),
                passthrough_columns=tuple(passthrough_columns),
                index_col_ids=tuple(index_col_ids),
                dtype=dtype,
                how=how,
            )
        )

    def join(
        self,
        other: ArrayValue,
        join_def: join_def.JoinDefinition,
        allow_row_identity_join: bool = False,
    ):
        join_node = nodes.JoinNode(
            left_child=self.node,
            right_child=other.node,
            join=join_def,
            allow_row_identity_join=allow_row_identity_join,
        )
        if allow_row_identity_join:
            return ArrayValue(bigframes.core.rewrite.maybe_rewrite_join(join_node))
        return ArrayValue(join_node)

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
