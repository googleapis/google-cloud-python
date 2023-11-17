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
import io
import typing
from typing import Iterable, Literal, Optional, Sequence, Tuple

from google.cloud import bigquery
import ibis
import ibis.expr.types as ibis_types
import pandas

import bigframes.core.compile.compiled as compiled
import bigframes.core.compile.compiler as compiler
import bigframes.core.guid
import bigframes.core.nodes as nodes
from bigframes.core.ordering import OrderingColumnReference
import bigframes.core.ordering as orderings
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
            columns=tuple(columns),
            hidden_ordering_columns=tuple(hidden_ordering_columns),
            ordering=ordering,
        )
        return cls(node)

    @classmethod
    def from_pandas(cls, pd_df: pandas.DataFrame):
        iobytes = io.BytesIO()
        # Discard row labels and use simple string ids for columns
        column_ids = tuple(str(label) for label in pd_df.columns)
        pd_df.reset_index(drop=True).set_axis(column_ids, axis=1).to_feather(iobytes)
        node = nodes.ReadLocalNode(iobytes.getvalue(), column_ids=column_ids)
        return cls(node)

    @property
    def column_ids(self) -> typing.Sequence[str]:
        return self._compile_ordered().column_ids

    @property
    def session(self) -> Session:
        required_session = self.node.session
        from bigframes import get_global_session

        return self.node.session[0] if required_session else get_global_session()

    def get_column_type(self, key: str) -> bigframes.dtypes.Dtype:
        return self._compile_ordered().get_column_type(key)

    def _compile_ordered(self) -> compiled.OrderedIR:
        return compiler.compile_ordered(self.node)

    def _compile_unordered(self) -> compiled.UnorderedIR:
        return compiler.compile_unordered(self.node)

    def shape(self) -> typing.Tuple[int, int]:
        """Returns dimensions as (length, width) tuple."""
        width = len(self._compile_unordered().columns)
        count_expr = self._compile_unordered()._to_ibis_expr().count()

        # Support in-memory engines for hermetic unit tests.
        if not self.node.session:
            try:
                length = ibis.pandas.connect({}).execute(count_expr)
                return (length, width)
            except Exception:
                # Not all cases can be handled by pandas engine
                pass

        sql = self.session.ibis_client.compile(count_expr)
        row_iterator, _ = self.session._start_query(
            sql=sql,
            max_results=1,
        )
        length = next(row_iterator)[0]
        return (length, width)

    def to_sql(
        self,
        offset_column: typing.Optional[str] = None,
        col_id_overrides: typing.Mapping[str, str] = {},
        sorted: bool = False,
    ) -> str:
        array_value = self
        if offset_column:
            array_value = self.promote_offsets(offset_column)
        if sorted:
            return array_value._compile_ordered().to_sql(
                col_id_overrides=col_id_overrides,
                sorted=sorted,
            )
        else:
            return array_value._compile_unordered().to_sql(
                col_id_overrides=col_id_overrides
            )

    def start_query(
        self,
        job_config: Optional[bigquery.job.QueryJobConfig] = None,
        max_results: Optional[int] = None,
        *,
        sorted: bool = True,
    ) -> Tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
        """Execute a query and return metadata about the results."""
        # TODO(swast): Cache the job ID so we can look it up again if they ask
        # for the results? We'd need a way to invalidate the cache if DataFrame
        # becomes mutable, though. Or move this method to the immutable
        # expression class.
        # TODO(swast): We might want to move this method to Session and/or
        # provide our own minimal metadata class. Tight coupling to the
        # BigQuery client library isn't ideal, especially if we want to support
        # a LocalSession for unit testing.
        # TODO(swast): Add a timeout here? If the query is taking a long time,
        # maybe we just print the job metadata that we have so far?
        sql = self.to_sql(sorted=sorted)  # type:ignore
        return self.session._start_query(
            sql=sql,
            job_config=job_config,
            max_results=max_results,
        )

    def cached(self, cluster_cols: typing.Sequence[str]) -> ArrayValue:
        """Write the ArrayValue to a session table and create a new block object that references it."""
        compiled_value = self._compile_ordered()
        ibis_expr = compiled_value._to_ibis_expr(
            ordering_mode="unordered", expose_hidden_cols=True
        )
        tmp_table = self.session._ibis_to_temp_table(
            ibis_expr, cluster_cols=cluster_cols, api_name="cached"
        )

        table_expression = self.session.ibis_client.table(
            f"{tmp_table.project}.{tmp_table.dataset_id}.{tmp_table.table_id}"
        )
        new_columns = [table_expression[column] for column in compiled_value.column_ids]
        new_hidden_columns = [
            table_expression[column]
            for column in compiled_value._hidden_ordering_column_names
        ]
        return ArrayValue.from_ibis(
            self.session,
            table_expression,
            columns=new_columns,
            hidden_ordering_columns=new_hidden_columns,
            ordering=compiled_value._ordering,
        )

    # Operations

    def drop_columns(self, columns: Iterable[str]) -> ArrayValue:
        return ArrayValue(
            nodes.DropColumnsNode(child=self.node, columns=tuple(columns))
        )

    def filter(self, predicate_id: str, keep_null: bool = False) -> ArrayValue:
        """Filter the table on a given expression, the predicate must be a boolean series aligned with the table expression."""
        return ArrayValue(
            nodes.FilterNode(
                child=self.node, predicate_id=predicate_id, keep_null=keep_null
            )
        )

    def order_by(self, by: Sequence[OrderingColumnReference]) -> ArrayValue:
        return ArrayValue(nodes.OrderByNode(child=self.node, by=tuple(by)))

    def reversed(self) -> ArrayValue:
        return ArrayValue(nodes.ReversedNode(child=self.node))

    def promote_offsets(self, col_id: str) -> ArrayValue:
        """
        Convenience function to promote copy of column offsets to a value column. Can be used to reset index.
        """
        return ArrayValue(nodes.PromoteOffsetsNode(child=self.node, col_id=col_id))

    def select_columns(self, column_ids: typing.Sequence[str]) -> ArrayValue:
        return ArrayValue(
            nodes.SelectNode(child=self.node, column_ids=tuple(column_ids))
        )

    def concat(self, other: typing.Sequence[ArrayValue]) -> ArrayValue:
        """Append together multiple ArrayValue objects."""
        return ArrayValue(
            nodes.ConcatNode(children=tuple([self.node, *[val.node for val in other]]))
        )

    def project_unary_op(
        self, column_name: str, op: ops.UnaryOp, output_name=None
    ) -> ArrayValue:
        """Creates a new expression based on this expression with unary operation applied to one column."""
        return ArrayValue(
            nodes.ProjectUnaryOpNode(
                child=self.node, input_id=column_name, op=op, output_id=output_name
            )
        )

    def project_binary_op(
        self,
        left_column_id: str,
        right_column_id: str,
        op: ops.BinaryOp,
        output_column_id: str,
    ) -> ArrayValue:
        """Creates a new expression based on this expression with binary operation applied to two columns."""
        return ArrayValue(
            nodes.ProjectBinaryOpNode(
                child=self.node,
                left_input_id=left_column_id,
                right_input_id=right_column_id,
                op=op,
                output_id=output_column_id,
            )
        )

    def project_ternary_op(
        self,
        col_id_1: str,
        col_id_2: str,
        col_id_3: str,
        op: ops.TernaryOp,
        output_column_id: str,
    ) -> ArrayValue:
        """Creates a new expression based on this expression with ternary operation applied to three columns."""
        return ArrayValue(
            nodes.ProjectTernaryOpNode(
                child=self.node,
                input_id1=col_id_1,
                input_id2=col_id_2,
                input_id3=col_id_3,
                op=op,
                output_id=output_column_id,
            )
        )

    def aggregate(
        self,
        aggregations: typing.Sequence[typing.Tuple[str, agg_ops.AggregateOp, str]],
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

    def corr_aggregate(
        self, corr_aggregations: typing.Sequence[typing.Tuple[str, str, str]]
    ) -> ArrayValue:
        """
        Get correlations between each lef_column_id and right_column_id, stored in the respective output_column_id.
        This uses BigQuery's CORR under the hood, and thus only Pearson's method is used.
        Arguments:
            corr_aggregations: left_column_id, right_column_id, output_column_id tuples
        """
        return ArrayValue(
            nodes.CorrNode(child=self.node, corr_aggregations=tuple(corr_aggregations))
        )

    def project_window_op(
        self,
        column_name: str,
        op: agg_ops.WindowOp,
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

    def assign(self, source_id: str, destination_id: str) -> ArrayValue:
        return ArrayValue(
            nodes.AssignNode(
                child=self.node, source_id=source_id, destination_id=destination_id
            )
        )

    def assign_constant(
        self,
        destination_id: str,
        value: typing.Any,
        dtype: typing.Optional[bigframes.dtypes.Dtype],
    ) -> ArrayValue:
        return ArrayValue(
            nodes.AssignConstantNode(
                child=self.node, destination_id=destination_id, value=value, dtype=dtype
            )
        )

    def join(
        self,
        self_column_ids: typing.Sequence[str],
        other: ArrayValue,
        other_column_ids: typing.Sequence[str],
        *,
        how: Literal[
            "inner",
            "left",
            "outer",
            "right",
            "cross",
        ],
        allow_row_identity_join: bool = True,
    ):
        return ArrayValue(
            nodes.JoinNode(
                left_child=self.node,
                right_child=other.node,
                left_column_ids=tuple(self_column_ids),
                right_column_ids=tuple(other_column_ids),
                how=how,
                allow_row_identity_join=allow_row_identity_join,
            )
        )

    def _uniform_sampling(self, fraction: float) -> ArrayValue:
        """Sampling the table on given fraction.

        .. warning::
            The row numbers of result is non-deterministic, avoid to use.
        """
        return ArrayValue(nodes.RandomSampleNode(self.node, fraction))
