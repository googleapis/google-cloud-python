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
import math
import typing
from typing import Collection, Dict, Iterable, Literal, Optional, Sequence, Tuple

from google.cloud import bigquery
import ibis
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.types as ibis_types
import pandas

import bigframes.constants as constants
import bigframes.core.guid
from bigframes.core.ordering import (
    encode_order_string,
    ExpressionOrdering,
    IntegerEncoding,
    OrderingColumnReference,
    reencode_order_string,
    StringEncoding,
)
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops

if typing.TYPE_CHECKING:
    from bigframes.session import Session

ORDER_ID_COLUMN = "bigframes_ordering_id"
PREDICATE_COLUMN = "bigframes_predicate"


@dataclass(frozen=True)
class WindowSpec:
    """
    Specifies a window over which aggregate and analytic function may be applied.
    grouping_keys: set of column ids to group on
    preceding: Number of preceding rows in the window
    following: Number of preceding rows in the window
    ordering: List of columns ids and ordering direction to override base ordering
    """

    grouping_keys: typing.Sequence[str] = tuple()
    ordering: typing.Sequence[OrderingColumnReference] = tuple()
    preceding: typing.Optional[int] = None
    following: typing.Optional[int] = None
    min_periods: int = 0


# TODO(swast): We might want to move this to it's own sub-module.
class ArrayValue:
    """Immutable BigQuery DataFrames expression tree.

    Note: Usage of this class is considered to be private and subject to change
    at any time.

    This class is a wrapper around Ibis expressions. Its purpose is to defer
    Ibis projection operations to keep generated SQL small and correct when
    mixing and matching columns from different versions of a DataFrame.

    Args:
        session:
            A BigQuery DataFrames session to allow more flexibility in running
            queries.
        table: An Ibis table expression.
        columns: Ibis value expressions that can be projected as columns.
        hidden_ordering_columns: Ibis value expressions to store ordering.
        ordering: An ordering property of the data frame.
        predicates: A list of filters on the data frame.
    """

    def __init__(
        self,
        session: Session,
        table: ibis_types.Table,
        columns: Sequence[ibis_types.Value],
        hidden_ordering_columns: Optional[Sequence[ibis_types.Value]] = None,
        ordering: ExpressionOrdering = ExpressionOrdering(),
        predicates: Optional[Collection[ibis_types.BooleanValue]] = None,
    ):
        self._session = session
        self._table = table
        self._predicates = tuple(predicates) if predicates is not None else ()
        # TODO: Validate ordering
        if not ordering.total_ordering_columns:
            raise ValueError("Must have total ordering defined by one or more columns")
        self._ordering = ordering
        # Allow creating a DataFrame directly from an Ibis table expression.
        # TODO(swast): Validate that each column references the same table (or
        # no table for literal values).
        self._columns = tuple(columns)

        # Meta columns store ordering, or other data that doesn't correspond to dataframe columns
        self._hidden_ordering_columns = (
            tuple(hidden_ordering_columns)
            if hidden_ordering_columns is not None
            else ()
        )

        # To allow for more efficient lookup by column name, create a
        # dictionary mapping names to column values.
        self._column_names = {column.get_name(): column for column in self._columns}
        self._hidden_ordering_column_names = {
            column.get_name(): column for column in self._hidden_ordering_columns
        }
        ### Validation
        value_col_ids = self._column_names.keys()
        hidden_col_ids = self._hidden_ordering_column_names.keys()

        all_columns = value_col_ids | hidden_col_ids
        ordering_valid = all(
            col.column_id in all_columns for col in ordering.all_ordering_columns
        )
        if value_col_ids & hidden_col_ids:
            raise ValueError(
                f"Keys in both hidden and exposed list: {value_col_ids & hidden_col_ids}"
            )
        if not ordering_valid:
            raise ValueError(f"Illegal ordering keys: {ordering.all_ordering_columns}")

    @classmethod
    def mem_expr_from_pandas(
        cls,
        pd_df: pandas.DataFrame,
        session: Optional[Session],
    ) -> ArrayValue:
        """
        Builds an in-memory only (SQL only) expr from a pandas dataframe.

        Caution: If session is None, only a subset of expr functionality will be available (null Session is usually not supported).
        """
        # must set non-null column labels. these are not the user-facing labels
        pd_df = pd_df.set_axis(
            [column or bigframes.core.guid.generate_guid() for column in pd_df.columns],
            axis="columns",
        )
        pd_df = pd_df.assign(**{ORDER_ID_COLUMN: range(len(pd_df))})
        # ibis memtable cannot handle NA, must convert to None
        pd_df = pd_df.astype("object")  # type: ignore
        pd_df = pd_df.where(pandas.notnull(pd_df), None)
        keys_memtable = ibis.memtable(pd_df)
        return cls(
            session,  # type: ignore # Session cannot normally be none, see "caution" above
            keys_memtable,
            ordering=ExpressionOrdering(
                ordering_value_columns=[OrderingColumnReference(ORDER_ID_COLUMN)],
                total_ordering_columns=frozenset([ORDER_ID_COLUMN]),
            ),
            hidden_ordering_columns=(keys_memtable[ORDER_ID_COLUMN],),
        )

    @property
    def table(self) -> ibis_types.Table:
        return self._table

    @property
    def reduced_predicate(self) -> typing.Optional[ibis_types.BooleanValue]:
        """Returns the frame's predicates as an equivalent boolean value, useful where a single predicate value is preferred."""
        return (
            _reduce_predicate_list(self._predicates).name(PREDICATE_COLUMN)
            if self._predicates
            else None
        )

    @property
    def columns(self) -> typing.Tuple[ibis_types.Value, ...]:
        return self._columns

    @property
    def column_names(self) -> Dict[str, ibis_types.Value]:
        return self._column_names

    @property
    def hidden_ordering_columns(self) -> typing.Tuple[ibis_types.Value, ...]:
        return self._hidden_ordering_columns

    @property
    def _ibis_order(self) -> Sequence[ibis_types.Value]:
        """Returns a sequence of ibis values which can be directly used to order a table expression. Has direction modifiers applied."""
        return _convert_ordering_to_table_values(
            {**self._column_names, **self._hidden_ordering_column_names},
            self._ordering.all_ordering_columns,
        )

    def builder(self) -> ArrayValueBuilder:
        """Creates a mutable builder for expressions."""
        # Since ArrayValue is intended to be immutable (immutability offers
        # potential opportunities for caching, though we might need to introduce
        # more node types for that to be useful), we create a builder class.
        return ArrayValueBuilder(
            self._session,
            self._table,
            columns=self._columns,
            hidden_ordering_columns=self._hidden_ordering_columns,
            ordering=self._ordering,
            predicates=self._predicates,
        )

    def drop_columns(self, columns: Iterable[str]) -> ArrayValue:
        # Must generate offsets if we are dropping a column that ordering depends on
        expr = self
        for ordering_column in set(columns).intersection(
            [col.column_id for col in self._ordering.ordering_value_columns]
        ):
            expr = self._hide_column(ordering_column)

        expr_builder = expr.builder()
        remain_cols = [
            column for column in expr.columns if column.get_name() not in columns
        ]
        expr_builder.columns = remain_cols
        return expr_builder.build()

    def get_column_type(self, key: str) -> bigframes.dtypes.Dtype:
        ibis_type = typing.cast(
            bigframes.dtypes.IbisDtype, self.get_any_column(key).type()
        )
        return typing.cast(
            bigframes.dtypes.Dtype,
            bigframes.dtypes.ibis_dtype_to_bigframes_dtype(ibis_type),
        )

    def get_column(self, key: str) -> ibis_types.Value:
        """Gets the Ibis expression for a given column."""
        if key not in self._column_names.keys():
            raise ValueError(
                "Column name {} not in set of values: {}".format(
                    key, self._column_names.keys()
                )
            )
        return typing.cast(ibis_types.Value, self._column_names[key])

    def get_any_column(self, key: str) -> ibis_types.Value:
        """Gets the Ibis expression for a given column. Will also get hidden columns."""
        all_columns = {**self._column_names, **self._hidden_ordering_column_names}
        if key not in all_columns.keys():
            raise ValueError(
                "Column name {} not in set of values: {}".format(
                    key, all_columns.keys()
                )
            )
        return typing.cast(ibis_types.Value, all_columns[key])

    def _get_hidden_ordering_column(self, key: str) -> ibis_types.Column:
        """Gets the Ibis expression for a given hidden column."""
        if key not in self._hidden_ordering_column_names.keys():
            raise ValueError(
                "Column name {} not in set of values: {}".format(
                    key, self._hidden_ordering_column_names.keys()
                )
            )
        return typing.cast(ibis_types.Column, self._hidden_ordering_column_names[key])

    def apply_limit(self, max_results: int) -> ArrayValue:
        table = self.to_ibis_expr(
            ordering_mode="order_by",
            expose_hidden_cols=True,
        ).limit(max_results)
        columns = [table[column_name] for column_name in self._column_names]
        hidden_ordering_columns = [
            table[column_name] for column_name in self._hidden_ordering_column_names
        ]
        return ArrayValue(
            self._session,
            table,
            columns=columns,
            hidden_ordering_columns=hidden_ordering_columns,
            ordering=self._ordering,
        )

    def filter(self, predicate: ibis_types.BooleanValue) -> ArrayValue:
        """Filter the table on a given expression, the predicate must be a boolean series aligned with the table expression."""
        expr = self.builder()
        expr.ordering = expr.ordering.with_non_sequential()
        expr.predicates = [*self._predicates, predicate]
        return expr.build()

    def order_by(
        self, by: Sequence[OrderingColumnReference], stable: bool = False
    ) -> ArrayValue:
        expr_builder = self.builder()
        expr_builder.ordering = self._ordering.with_ordering_columns(by, stable=stable)
        return expr_builder.build()

    def reversed(self) -> ArrayValue:
        expr_builder = self.builder()
        expr_builder.ordering = self._ordering.with_reverse()
        return expr_builder.build()

    def _uniform_sampling(self, fraction: float) -> ArrayValue:
        table = self.to_ibis_expr(
            ordering_mode="order_by", expose_hidden_cols=True, fraction=fraction
        )
        columns = [table[column_name] for column_name in self._column_names]
        hidden_ordering_columns = [
            table[column_name] for column_name in self._hidden_ordering_column_names
        ]
        return ArrayValue(
            self._session,
            table,
            columns=columns,
            hidden_ordering_columns=hidden_ordering_columns,
            ordering=self._ordering,
        )

    @property
    def offsets(self):
        if not self._ordering.is_sequential:
            raise ValueError(
                "Expression does not have offsets. Generate them first using project_offsets."
            )
        if not self._ordering.total_order_col:
            raise ValueError(
                "Ordering is invalid. Marked as sequential but no total order columns."
            )
        return self.get_any_column(self._ordering.total_order_col.column_id)

    def project_offsets(self) -> ArrayValue:
        """Create a new expression that contains offsets. Should only be executed when offsets are needed for an operations. Has no effect on expression semantics."""
        if self._ordering.is_sequential:
            return self
        # TODO(tbergeron): Enforce total ordering
        table = self.to_ibis_expr(
            ordering_mode="offset_col", order_col_name=ORDER_ID_COLUMN
        )
        columns = [table[column_name] for column_name in self._column_names]
        ordering = ExpressionOrdering(
            ordering_value_columns=[OrderingColumnReference(ORDER_ID_COLUMN)],
            total_ordering_columns=frozenset([ORDER_ID_COLUMN]),
            integer_encoding=IntegerEncoding(True, is_sequential=True),
        )
        return ArrayValue(
            self._session,
            table,
            columns=columns,
            hidden_ordering_columns=[table[ORDER_ID_COLUMN]],
            ordering=ordering,
        )

    def _hide_column(self, column_id) -> ArrayValue:
        """Pushes columns to hidden columns list. Used to hide ordering columns that have been dropped or destructively mutated."""
        expr_builder = self.builder()
        # Need to rename column as caller might be creating a new row with the same name but different values.
        # Can avoid this if don't allow callers to determine ids and instead generate unique ones in this class.
        new_name = bigframes.core.guid.generate_guid(prefix="bigframes_hidden_")
        expr_builder.hidden_ordering_columns = [
            *self._hidden_ordering_columns,
            self.get_column(column_id).name(new_name),
        ]
        expr_builder.ordering = self._ordering.with_column_remap({column_id: new_name})
        return expr_builder.build()

    def promote_offsets(self) -> typing.Tuple[ArrayValue, str]:
        """
        Convenience function to promote copy of column offsets to a value column. Can be used to reset index.
        """
        # Special case: offsets already exist
        ordering = self._ordering

        if (not ordering.is_sequential) or (not ordering.total_order_col):
            return self.project_offsets().promote_offsets()
        col_id = bigframes.core.guid.generate_guid()
        expr_builder = self.builder()
        expr_builder.columns = [
            self.get_any_column(ordering.total_order_col.column_id).name(col_id),
            *self.columns,
        ]
        return expr_builder.build(), col_id

    def select_columns(self, column_ids: typing.Sequence[str]):
        return self.projection([self.get_column(col_id) for col_id in column_ids])

    def projection(self, columns: Iterable[ibis_types.Value]) -> ArrayValue:
        """Creates a new expression based on this expression with new columns."""
        # TODO(swast): We might want to do validation here that columns derive
        # from the same table expression instead of (in addition to?) at
        # construction time.

        expr = self
        for ordering_column in set(self.column_names.keys()).intersection(
            [col_ref.column_id for col_ref in self._ordering.ordering_value_columns]
        ):
            # Need to hide ordering columns that are being dropped. Alternatively, could project offsets
            expr = expr._hide_column(ordering_column)
        builder = expr.builder()
        builder.columns = list(columns)
        new_expr = builder.build()
        return new_expr

    def shape(self) -> typing.Tuple[int, int]:
        """Returns dimensions as (length, width) tuple."""
        width = len(self.columns)
        count_expr = self.to_ibis_expr(ordering_mode="unordered").count()
        sql = self._session.ibis_client.compile(count_expr)
        row_iterator, _ = self._session._start_query(
            sql=sql,
            max_results=1,
        )
        length = next(row_iterator)[0]
        return (length, width)

    def concat(self, other: typing.Sequence[ArrayValue]) -> ArrayValue:
        """Append together multiple ArrayValue objects."""
        if len(other) == 0:
            return self
        tables = []
        prefix_base = 10
        prefix_size = math.ceil(math.log(len(other) + 1, prefix_base))
        # Must normalize all ids to the same encoding size
        max_encoding_size = max(
            self._ordering.string_encoding.length,
            *[expression._ordering.string_encoding.length for expression in other],
        )
        for i, expr in enumerate([self, *other]):
            ordering_prefix = str(i).zfill(prefix_size)
            table = expr.to_ibis_expr(
                ordering_mode="string_encoded", order_col_name=ORDER_ID_COLUMN
            )
            # Rename the value columns based on horizontal offset before applying union.
            table = table.select(
                [
                    table[col].name(f"column_{i}")
                    if col != ORDER_ID_COLUMN
                    else (
                        ordering_prefix
                        + reencode_order_string(
                            table[ORDER_ID_COLUMN], max_encoding_size
                        )
                    ).name(ORDER_ID_COLUMN)
                    for i, col in enumerate(table.columns)
                ]
            )
            tables.append(table)
        combined_table = ibis.union(*tables)
        ordering = ExpressionOrdering(
            ordering_value_columns=[OrderingColumnReference(ORDER_ID_COLUMN)],
            total_ordering_columns=frozenset([ORDER_ID_COLUMN]),
            string_encoding=StringEncoding(True, prefix_size + max_encoding_size),
        )
        return ArrayValue(
            self._session,
            combined_table,
            columns=[
                combined_table[col]
                for col in combined_table.columns
                if col != ORDER_ID_COLUMN
            ],
            hidden_ordering_columns=[combined_table[ORDER_ID_COLUMN]],
            ordering=ordering,
        )

    def project_unary_op(
        self, column_name: str, op: ops.UnaryOp, output_name=None
    ) -> ArrayValue:
        """Creates a new expression based on this expression with unary operation applied to one column."""
        value = op._as_ibis(self.get_column(column_name)).name(
            output_name or column_name
        )
        return self._set_or_replace_by_id(output_name or column_name, value)

    def project_binary_op(
        self,
        left_column_id: str,
        right_column_id: str,
        op: ops.BinaryOp,
        output_column_id: str,
    ) -> ArrayValue:
        """Creates a new expression based on this expression with binary operation applied to two columns."""
        value = op(
            self.get_column(left_column_id), self.get_column(right_column_id)
        ).name(output_column_id)
        return self._set_or_replace_by_id(output_column_id, value)

    def project_ternary_op(
        self,
        col_id_1: str,
        col_id_2: str,
        col_id_3: str,
        op: ops.TernaryOp,
        output_column_id: str,
    ) -> ArrayValue:
        """Creates a new expression based on this expression with ternary operation applied to three columns."""
        value = op(
            self.get_column(col_id_1),
            self.get_column(col_id_2),
            self.get_column(col_id_3),
        ).name(output_column_id)
        return self._set_or_replace_by_id(output_column_id, value)

    def aggregate(
        self,
        aggregations: typing.Sequence[typing.Tuple[str, agg_ops.AggregateOp, str]],
        by_column_ids: typing.Sequence[str] = (),
        dropna: bool = True,
    ) -> ArrayValue:
        """
        Apply aggregations to the expression.
        Arguments:
            by_column_id: column id of the aggregation key, this is preserved through the transform
            aggregations: input_column_id, operation, output_column_id tuples
            dropna: whether null keys should be dropped
        """
        table = self.to_ibis_expr(ordering_mode="unordered")
        stats = {
            col_out: agg_op._as_ibis(table[col_in])
            for col_in, agg_op, col_out in aggregations
        }
        if by_column_ids:
            result = table.group_by(by_column_ids).aggregate(**stats)
            # Must have deterministic ordering, so order by the unique "by" column
            ordering = ExpressionOrdering(
                [
                    OrderingColumnReference(column_id=column_id)
                    for column_id in by_column_ids
                ],
                total_ordering_columns=frozenset(by_column_ids),
            )
            columns = tuple(result[key] for key in result.columns)
            expr = ArrayValue(self._session, result, columns=columns, ordering=ordering)
            if dropna:
                for column_id in by_column_ids:
                    expr = expr.filter(
                        ops.notnull_op._as_ibis(expr.get_column(column_id))
                    )
            # Can maybe remove this as Ordering id is redundant as by_column is unique after aggregation
            return expr.project_offsets()
        else:
            aggregates = {**stats, ORDER_ID_COLUMN: ibis_types.literal(0)}
            result = table.aggregate(**aggregates)
            # Ordering is irrelevant for single-row output, but set ordering id regardless as other ops(join etc.) expect it.
            ordering = ExpressionOrdering(
                ordering_value_columns=[OrderingColumnReference(ORDER_ID_COLUMN)],
                total_ordering_columns=frozenset([ORDER_ID_COLUMN]),
                integer_encoding=IntegerEncoding(is_encoded=True, is_sequential=True),
            )
            return ArrayValue(
                self._session,
                result,
                columns=[result[col_id] for col_id in [*stats.keys()]],
                hidden_ordering_columns=[result[ORDER_ID_COLUMN]],
                ordering=ordering,
            )

    def project_window_op(
        self,
        column_name: str,
        op: agg_ops.WindowOp,
        window_spec: WindowSpec,
        output_name=None,
        *,
        skip_null_groups=False,
        skip_reproject_unsafe: bool = False,
    ) -> ArrayValue:
        """
        Creates a new expression based on this expression with unary operation applied to one column.
        column_name: the id of the input column present in the expression
        op: the windowable operator to apply to the input column
        window_spec: a specification of the window over which to apply the operator
        output_name: the id to assign to the output of the operator, by default will replace input col if distinct output id not provided
        skip_null_groups: will filter out any rows where any of the grouping keys is null
        skip_reproject_unsafe: skips the reprojection step, can be used when performing many non-dependent window operations, user responsible for not nesting window expressions, or using outputs as join, filter or aggregation keys before a reprojection
        """
        column = typing.cast(ibis_types.Column, self.get_column(column_name))
        window = self._ibis_window_from_spec(window_spec, allow_ties=op.handles_ties)

        window_op = op._as_ibis(column, window)

        clauses = []
        if op.skips_nulls:
            clauses.append((column.isnull(), ibis.NA))
        if skip_null_groups:
            for key in window_spec.grouping_keys:
                clauses.append((self.get_column(key).isnull(), ibis.NA))
        if window_spec.min_periods:
            clauses.append(
                (
                    agg_ops.count_op._as_ibis(column, window)
                    < ibis_types.literal(window_spec.min_periods),
                    ibis.NA,
                )
            )

        if clauses:
            case_statement = ibis.case()
            for clause in clauses:
                case_statement = case_statement.when(clause[0], clause[1])
            case_statement = case_statement.else_(window_op).end()
            window_op = case_statement

        result = self._set_or_replace_by_id(output_name or column_name, window_op)
        # TODO(tbergeron): Automatically track analytic expression usage and defer reprojection until required for valid query generation.
        return result._reproject_to_table() if not skip_reproject_unsafe else result

    def to_ibis_expr(
        self,
        ordering_mode: Literal[
            "order_by", "string_encoded", "offset_col", "unordered"
        ] = "order_by",
        order_col_name: Optional[str] = ORDER_ID_COLUMN,
        expose_hidden_cols: bool = False,
        fraction: Optional[float] = None,
        col_id_overrides: typing.Mapping[str, str] = {},
    ):
        """
        Creates an Ibis table expression representing the DataFrame.

        ArrayValue objects are sorted, so the following options are available
        to reflect this in the ibis expression.

        * "order_by" (Default): The output table will not have an ordering
          column, however there will be an order_by clause applied to the ouput.
        * "offset_col": Zero-based offsets are generated as a column, this will
          not sort the rows however.
        * "string_encoded": An ordered string column is provided in output table.
        * "unordered": No ordering information will be provided in output. Only
          value columns are projected.

        For offset or ordered column, order_col_name can be used to assign the
        output label for the ordering column. If none is specified, the default
        column name will be 'bigframes_ordering_id'

        Args:
            ordering_mode:
                How to construct the Ibis expression from the ArrayValue. See
                above for details.
            order_col_name:
                If the ordering mode outputs a single ordering or offsets
                column, use this as the column name.
            expose_hidden_cols:
                If True, include the hidden ordering columns in the results.
                Only compatible with `order_by` and `unordered`
                ``ordering_mode``.
            col_id_overrides:
                overrides the column ids for the result
        Returns:
            An ibis expression representing the data help by the ArrayValue object.
        """
        assert ordering_mode in (
            "order_by",
            "string_encoded",
            "offset_col",
            "unordered",
        )
        if expose_hidden_cols and ordering_mode in ("ordered_col", "offset_col"):
            raise ValueError(
                f"Cannot expose hidden ordering columns with ordering_mode {ordering_mode}"
            )

        columns = list(self._columns)
        columns_to_drop: list[
            str
        ] = []  # Ordering/Filtering columns that will be dropped at end

        if self.reduced_predicate is not None:
            columns.append(self.reduced_predicate)
            # Usually drop predicate as it is will be all TRUE after filtering
            if not expose_hidden_cols:
                columns_to_drop.append(self.reduced_predicate.get_name())

        order_columns = self._create_order_columns(
            ordering_mode, order_col_name, expose_hidden_cols
        )
        columns.extend(order_columns)
        if (ordering_mode == "order_by") and not expose_hidden_cols:
            columns_to_drop.extend(col.get_name() for col in order_columns)

        # Special case for empty tables, since we can't create an empty
        # projection.
        if not columns:
            return ibis.memtable([])

        # Make sure all dtypes are the "canonical" ones for BigFrames. This is
        # important for operations like UNION where the schema must match.
        table = self._table.select(
            bigframes.dtypes.ibis_value_to_canonical_type(column) for column in columns
        )
        base_table = table
        if self.reduced_predicate is not None:
            table = table.filter(base_table[PREDICATE_COLUMN])
        if ordering_mode == "order_by":
            table = table.order_by(
                _convert_ordering_to_table_values(
                    {col: base_table[col] for col in table.columns},
                    self._ordering.all_ordering_columns,
                )  # type: ignore
            )
        table = table.drop(*columns_to_drop)
        if col_id_overrides:
            table = table.relabel(col_id_overrides)
        if fraction is not None:
            table = table.filter(ibis.random() < ibis.literal(fraction))
        return table

    def _create_order_columns(
        self,
        ordering_mode: str,
        order_col_name: Optional[str],
        expose_hidden_cols: bool,
    ) -> typing.Sequence[ibis_types.Value]:
        # Generate offsets if current ordering id semantics are not sufficiently strict
        if ordering_mode == "offset_col":
            return (self._create_offset_column().name(order_col_name),)
        elif ordering_mode == "string_encoded":
            return (self._create_string_ordering_column().name(order_col_name),)
        elif ordering_mode == "order_by" or expose_hidden_cols:
            return self.hidden_ordering_columns
        return ()

    def _create_offset_column(self) -> ibis_types.IntegerColumn:
        if self._ordering.total_order_col and self._ordering.is_sequential:
            offsets = self.get_any_column(self._ordering.total_order_col.column_id)
            return typing.cast(ibis_types.IntegerColumn, offsets)
        else:
            window = ibis.window(order_by=self._ibis_order)
            if self._predicates:
                window = window.group_by(self.reduced_predicate)
            offsets = ibis.row_number().over(window)
            return typing.cast(ibis_types.IntegerColumn, offsets)

    def _create_string_ordering_column(self) -> ibis_types.StringColumn:
        if self._ordering.total_order_col and self._ordering.is_string_encoded:
            string_order_ids = self.get_any_column(
                self._ordering.total_order_col.column_id
            )
            return typing.cast(ibis_types.StringColumn, string_order_ids)
        if (
            self._ordering.total_order_col
            and self._ordering.integer_encoding.is_encoded
        ):
            # Special case: non-negative integer ordering id can be converted directly to string without regenerating row numbers
            int_values = self.get_any_column(self._ordering.total_order_col.column_id)
            return encode_order_string(
                typing.cast(ibis_types.IntegerColumn, int_values),
            )
        else:
            # Have to build string from scratch
            window = ibis.window(order_by=self._ibis_order)
            if self._predicates:
                window = window.group_by(self.reduced_predicate)
            row_nums = typing.cast(
                ibis_types.IntegerColumn, ibis.row_number().over(window)
            )
            return encode_order_string(row_nums)

    def start_query(
        self,
        job_config: Optional[bigquery.job.QueryJobConfig] = None,
        max_results: Optional[int] = None,
        expose_extra_columns: bool = False,
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
        table = self.to_ibis_expr(expose_hidden_cols=expose_extra_columns)
        sql = self._session.ibis_client.compile(table)  # type:ignore
        return self._session._start_query(
            sql=sql,
            job_config=job_config,
            max_results=max_results,
        )

    def _get_table_size(self, destination_table):
        return self._session._get_table_size(destination_table)

    def _reproject_to_table(self) -> ArrayValue:
        """
        Internal operators that projects the internal representation into a
        new ibis table expression where each value column is a direct
        reference to a column in that table expression. Needed after
        some operations such as window operations that cannot be used
        recursively in projections.
        """
        table = self.to_ibis_expr(
            ordering_mode="unordered",
            expose_hidden_cols=True,
        )
        columns = [table[column_name] for column_name in self._column_names]
        ordering_col_ids = [
            ref.column_id for ref in self._ordering.all_ordering_columns
        ]
        hidden_ordering_columns = [
            table[column_name]
            for column_name in self._hidden_ordering_column_names
            if column_name in ordering_col_ids
        ]
        return ArrayValue(
            self._session,
            table,
            columns=columns,
            hidden_ordering_columns=hidden_ordering_columns,
            ordering=self._ordering,
        )

    def _ibis_window_from_spec(self, window_spec: WindowSpec, allow_ties: bool = False):
        group_by: typing.List[ibis_types.Value] = (
            [
                typing.cast(ibis_types.Column, _as_identity(self.get_column(column)))
                for column in window_spec.grouping_keys
            ]
            if window_spec.grouping_keys
            else []
        )
        if self.reduced_predicate is not None:
            group_by.append(self.reduced_predicate)
        if window_spec.ordering:
            order_by = _convert_ordering_to_table_values(
                {**self._column_names, **self._hidden_ordering_column_names},
                window_spec.ordering,
            )
            if not allow_ties:
                # Most operator need an unambiguous ordering, so the table's total ordering is appended
                order_by = tuple([*order_by, *self._ibis_order])
        elif (window_spec.following is not None) or (window_spec.preceding is not None):
            # If window spec has following or preceding bounds, we need to apply an unambiguous ordering.
            order_by = tuple(self._ibis_order)
        else:
            # Unbound grouping window. Suitable for aggregations but not for analytic function application.
            order_by = None
        return ibis.window(
            preceding=window_spec.preceding,
            following=window_spec.following,
            order_by=order_by,
            group_by=group_by,
        )

    def unpivot_single_row(
        self,
        row_labels: typing.Sequence[typing.Optional[str]],
        unpivot_columns: typing.Sequence[typing.Tuple[str, typing.Sequence[str]]],
        *,
        index_col_id: str = "index",
        dtype=pandas.Float64Dtype(),
    ) -> ArrayValue:
        """Unpivot a single row."""
        # TODO: Generalize to multiple row input
        table = self.to_ibis_expr(ordering_mode="unordered")
        sub_expressions = []

        # TODO: validate all columns are equal length, as well as row labels
        row_n = len(row_labels)
        if not all(
            len(source_columns) == row_n for _, source_columns in unpivot_columns
        ):
            raise ValueError("Columns and row labels must all be same length.")

        # Select each column
        for i in range(row_n):
            values = []
            for result_col, source_cols in unpivot_columns:
                values.append(
                    ops.AsTypeOp(dtype)._as_ibis(table[source_cols[i]]).name(result_col)
                )

            sub_expr = table.select(
                ibis_types.literal(row_labels[i]).name(index_col_id),
                *values,
                ibis_types.literal(i).name(ORDER_ID_COLUMN),
            )
            sub_expressions.append(sub_expr)
        rotated_table = ibis.union(*sub_expressions)

        value_columns = [
            rotated_table[value_col_id] for value_col_id, _ in unpivot_columns
        ]
        return ArrayValue(
            session=self._session,
            table=rotated_table,
            columns=[rotated_table[index_col_id], *value_columns],
            hidden_ordering_columns=[rotated_table[ORDER_ID_COLUMN]],
            ordering=ExpressionOrdering(
                ordering_value_columns=[OrderingColumnReference(ORDER_ID_COLUMN)],
                total_ordering_columns=frozenset([ORDER_ID_COLUMN]),
            ),
        )

    def assign(self, source_id: str, destination_id: str) -> ArrayValue:
        return self._set_or_replace_by_id(destination_id, self.get_column(source_id))

    def assign_constant(
        self,
        destination_id: str,
        value: typing.Any,
        dtype: typing.Optional[bigframes.dtypes.Dtype],
    ) -> ArrayValue:
        # TODO(b/281587571): Solve scalar constant aggregation problem w/Ibis.
        ibis_value = bigframes.dtypes.literal_to_ibis_scalar(value, dtype)
        if ibis_value is None:
            raise NotImplementedError(
                f"Type not supported as scalar value {type(value)}. {constants.FEEDBACK_LINK}"
            )
        expr = self._set_or_replace_by_id(destination_id, ibis_value)
        return expr._reproject_to_table()

    def _set_or_replace_by_id(self, id: str, new_value: ibis_types.Value) -> ArrayValue:
        """Safely assign by id while maintaining ordering integrity."""
        # TODO: Split into explicit set and replace methods
        ordering_col_ids = [
            col_ref.column_id for col_ref in self._ordering.ordering_value_columns
        ]
        if id in ordering_col_ids:
            return self._hide_column(id)._set_or_replace_by_id(id, new_value)

        builder = self.builder()
        if id in self.column_names:
            builder.columns = [
                val if (col_id != id) else new_value.name(id)
                for col_id, val in self.column_names.items()
            ]
        else:
            builder.columns = [*self.columns, new_value.name(id)]
        return builder.build()

    def slice(
        self,
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None,
        step: typing.Optional[int] = None,
    ) -> ArrayValue:
        if step == 0:
            raise ValueError("slice step cannot be zero")

        if not step:
            step = 1

        # Special cases for head() and tail(), where we don't need to project
        # offsets. LIMIT clause is much more efficient in BigQuery than a
        # filter on row_number().
        if (
            (start is None or start == 0)
            and step == 1
            and stop is not None
            and stop > 0
        ):
            return self.apply_limit(stop)

        if start is not None and start < 0 and step == 1 and stop is None:
            return self.reversed().apply_limit(abs(start)).reversed()

        expr_with_offsets = self.project_offsets()

        # start with True and reduce with start, stop, and step conditions
        cond_list = [expr_with_offsets.offsets == expr_with_offsets.offsets]

        last_offset = expr_with_offsets.offsets.max()

        # Convert negative indexes to positive indexes
        if start and start < 0:
            start = last_offset + start + 1
        if stop and stop < 0:
            stop = last_offset + stop + 1

        if start is not None:
            if step >= 1:
                cond_list.append(expr_with_offsets.offsets >= start)
            else:
                cond_list.append(expr_with_offsets.offsets <= start)
        if stop is not None:
            if step >= 1:
                cond_list.append(expr_with_offsets.offsets < stop)
            else:
                cond_list.append(expr_with_offsets.offsets > stop)
        if step > 1:
            start = start if (start is not None) else 0
            cond_list.append((expr_with_offsets.offsets - start) % step == 0)
        if step < 0:
            start = start if (start is not None) else last_offset
            cond_list.append((start - expr_with_offsets.offsets) % (-step) == 0)

        sliced_expr = expr_with_offsets.filter(
            functools.reduce(lambda x, y: x & y, cond_list)
        )
        return sliced_expr if step > 0 else sliced_expr.reversed()


class ArrayValueBuilder:
    """Mutable expression class.
    Use ArrayValue.builder() to create from a ArrayValue object.
    """

    def __init__(
        self,
        session: Session,
        table: ibis_types.Table,
        ordering: ExpressionOrdering,
        columns: Collection[ibis_types.Value] = (),
        hidden_ordering_columns: Collection[ibis_types.Value] = (),
        predicates: Optional[Collection[ibis_types.BooleanValue]] = None,
    ):
        self.session = session
        self.table = table
        self.columns = list(columns)
        self.hidden_ordering_columns = list(hidden_ordering_columns)
        self.ordering = ordering
        self.predicates = list(predicates) if predicates is not None else None

    def build(self) -> ArrayValue:
        return ArrayValue(
            session=self.session,
            table=self.table,
            columns=self.columns,
            hidden_ordering_columns=self.hidden_ordering_columns,
            ordering=self.ordering,
            predicates=self.predicates,
        )


def _reduce_predicate_list(
    predicate_list: typing.Collection[ibis_types.BooleanValue],
) -> ibis_types.BooleanValue:
    """Converts a list of predicates BooleanValues into a single BooleanValue."""
    if len(predicate_list) == 0:
        raise ValueError("Cannot reduce empty list of predicates")
    if len(predicate_list) == 1:
        (item,) = predicate_list
        return item
    return functools.reduce(lambda acc, pred: acc.__and__(pred), predicate_list)


def _convert_ordering_to_table_values(
    value_lookup: typing.Mapping[str, ibis_types.Value],
    ordering_columns: typing.Sequence[OrderingColumnReference],
) -> typing.Sequence[ibis_types.Value]:
    column_refs = ordering_columns
    ordering_values = []
    for ordering_col in column_refs:
        column = typing.cast(ibis_types.Column, value_lookup[ordering_col.column_id])
        ordering_value = (
            ibis.asc(column)
            if ordering_col.direction.is_ascending
            else ibis.desc(column)
        )
        # Bigquery SQL considers NULLS to be "smallest" values, but we need to override in these cases.
        if (not ordering_col.na_last) and (not ordering_col.direction.is_ascending):
            # Force nulls to be first
            is_null_val = typing.cast(ibis_types.Column, column.isnull())
            ordering_values.append(ibis.desc(is_null_val))
        elif (ordering_col.na_last) and (ordering_col.direction.is_ascending):
            # Force nulls to be last
            is_null_val = typing.cast(ibis_types.Column, column.isnull())
            ordering_values.append(ibis.asc(is_null_val))
        ordering_values.append(ordering_value)
    return ordering_values


def _as_identity(value: ibis_types.Value):
    # Some types need to be converted to string to enable groupby
    if value.type().is_float64() or value.type().is_geospatial():
        return value.cast(ibis_dtypes.str)
    return value
