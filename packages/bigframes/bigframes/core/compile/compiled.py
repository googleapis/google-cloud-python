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

import abc
import functools
import itertools
import typing
from typing import Collection, Literal, Optional, Sequence

import bigframes_vendored.ibis.backends.bigquery.backend as ibis_bigquery
import google.cloud.bigquery
import ibis
import ibis.backends.bigquery.datatypes
import ibis.common.deferred  # type: ignore
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.operations as ibis_ops
import ibis.expr.schema as ibis_schema
import ibis.expr.types as ibis_types
import pandas

import bigframes.core.compile.aggregate_compiler as agg_compiler
import bigframes.core.compile.googlesql
import bigframes.core.compile.ibis_types
import bigframes.core.compile.scalar_op_compiler as op_compilers
import bigframes.core.expression as ex
import bigframes.core.guid
import bigframes.core.identifiers as ids
from bigframes.core.ordering import (
    ascending_over,
    encode_order_string,
    join_orderings,
    OrderingExpression,
    RowOrdering,
    TotalOrdering,
)
import bigframes.core.sql
from bigframes.core.window_spec import RangeWindowBounds, RowsWindowBounds, WindowSpec
import bigframes.dtypes
import bigframes.operations.aggregations as agg_ops

ORDER_ID_COLUMN = "bigframes_ordering_id"
PREDICATE_COLUMN = "bigframes_predicate"


T = typing.TypeVar("T", bound="BaseIbisIR")

op_compiler = op_compilers.scalar_op_compiler


class BaseIbisIR(abc.ABC):
    """Implementation detail, contains common logic between ordered and unordered IR"""

    def __init__(
        self,
        table: ibis_types.Table,
        columns: Sequence[ibis_types.Value],
        predicates: Optional[Collection[ibis_types.BooleanValue]] = None,
    ):
        self._table = table
        self._predicates = tuple(predicates) if predicates is not None else ()
        # Allow creating a DataFrame directly from an Ibis table expression.
        # TODO(swast): Validate that each column references the same table (or
        # no table for literal values).
        self._columns = tuple(
            column.resolve(table)
            # TODO(https://github.com/ibis-project/ibis/issues/7613): use
            # public API to refer to Deferred type.
            if isinstance(column, ibis.common.deferred.Deferred) else column
            for column in columns
        )
        # To allow for more efficient lookup by column name, create a
        # dictionary mapping names to column values.
        self._column_names = {column.get_name(): column for column in self._columns}

    @property
    def columns(self) -> typing.Tuple[ibis_types.Value, ...]:
        return self._columns

    @property
    def column_ids(self) -> typing.Sequence[str]:
        return tuple(self._column_names.keys())

    @property
    def _reduced_predicate(self) -> typing.Optional[ibis_types.BooleanValue]:
        """Returns the frame's predicates as an equivalent boolean value, useful where a single predicate value is preferred."""
        return (
            _reduce_predicate_list(self._predicates).name(PREDICATE_COLUMN)
            if self._predicates
            else None
        )

    @property
    def _ibis_bindings(self) -> dict[str, ibis_types.Value]:
        return {col: self._get_ibis_column(col) for col in self.column_ids}

    @property
    @abc.abstractmethod
    def is_ordered_ir(self: T) -> bool:
        """Whether it is a OrderedIR or UnorderedIR."""
        ...

    @abc.abstractmethod
    def filter(self: T, predicate: ex.Expression) -> T:
        """Filter the table on a given expression, the predicate must be a boolean expression."""
        ...

    @abc.abstractmethod
    def _reproject_to_table(self: T) -> T:
        """
        Internal operators that projects the internal representation into a
        new ibis table expression where each value column is a direct
        reference to a column in that table expression. Needed after
        some operations such as window operations that cannot be used
        recursively in projections.
        """
        ...

    def projection(
        self: T,
        expression_id_pairs: typing.Tuple[typing.Tuple[ex.Expression, str], ...],
    ) -> T:
        """Apply an expression to the ArrayValue and assign the output to a column."""
        bindings = {col: self._get_ibis_column(col) for col in self.column_ids}
        new_values = [
            op_compiler.compile_expression(expression, bindings).name(id)
            for expression, id in expression_id_pairs
        ]
        result = self._select(tuple([*self._columns, *new_values]))  # type: ignore
        return result

    def selection(
        self: T,
        input_output_pairs: typing.Tuple[typing.Tuple[ex.DerefOp, str], ...],
    ) -> T:
        """Apply an expression to the ArrayValue and assign the output to a column."""
        bindings = {col: self._get_ibis_column(col) for col in self.column_ids}
        values = [
            op_compiler.compile_expression(input, bindings).name(id)
            for input, id in input_output_pairs
        ]
        result = self._select(tuple(values))  # type: ignore
        return result

    @abc.abstractmethod
    def _select(self: T, values: typing.Tuple[ibis_types.Value]) -> T:
        ...

    @abc.abstractmethod
    def _set_or_replace_by_id(self: T, id: str, new_value: ibis_types.Value) -> T:
        ...

    def _get_ibis_column(self, key: str) -> ibis_types.Value:
        """Gets the Ibis expression for a given column."""
        if key not in self.column_ids:
            raise ValueError(
                "Column name {} not in set of values: {}".format(key, self.column_ids)
            )
        return typing.cast(ibis_types.Value, self._column_names[key])

    def get_column_type(self, key: str) -> bigframes.dtypes.Dtype:
        ibis_type = typing.cast(
            bigframes.core.compile.ibis_types.IbisDtype,
            self._get_ibis_column(key).type(),
        )
        return typing.cast(
            bigframes.dtypes.Dtype,
            bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(ibis_type),
        )

    def _aggregate_base(
        self,
        table: ibis_types.Table,
        order_by: typing.Sequence[ibis_types.Value] = [],
        aggregations: typing.Sequence[typing.Tuple[ex.Aggregation, str]] = [],
        by_column_ids: typing.Sequence[ex.DerefOp] = (),
        dropna: bool = True,
    ) -> OrderedIR:
        assert not self.is_ordered_ir or len(order_by) > 0

        bindings = {col: table[col] for col in self.column_ids}
        stats = {
            col_out: agg_compiler.compile_aggregate(
                aggregate, bindings, order_by=order_by
            )
            for aggregate, col_out in aggregations
        }
        if by_column_ids:
            result = table.group_by((ref.id.sql for ref in by_column_ids)).aggregate(
                **stats
            )
            # Must have deterministic ordering, so order by the unique "by" column
            ordering = TotalOrdering(
                tuple([OrderingExpression(column_id) for column_id in by_column_ids]),
                total_ordering_columns=frozenset(
                    [ex.DerefOp(ref.id.local_normalized) for ref in by_column_ids]
                ),
            )
            columns = tuple(result[key] for key in result.columns)
            expr = OrderedIR(result, columns=columns, ordering=ordering)
            if dropna:
                for ref in by_column_ids:
                    expr = expr._filter(expr._compile_expression(ref).notnull())
            return expr
        else:
            aggregates = {**stats, ORDER_ID_COLUMN: ibis_types.literal(0)}
            result = table.aggregate(**aggregates)
            # Ordering is irrelevant for single-row output, but set ordering id regardless
            # as other ops(join etc.) expect it.
            # TODO: Maybe can make completely empty
            ordering = TotalOrdering(
                ordering_value_columns=tuple([]),
                total_ordering_columns=frozenset([]),
            )
            return OrderedIR(
                result,
                columns=[result[col_id] for col_id in [*stats.keys()]],
                hidden_ordering_columns=[result[ORDER_ID_COLUMN]],
                ordering=ordering,
            )


# Ibis Implementations
class UnorderedIR(BaseIbisIR):
    def __init__(
        self,
        table: ibis_types.Table,
        columns: Sequence[ibis_types.Value],
        predicates: Optional[Collection[ibis_types.BooleanValue]] = None,
    ):
        super().__init__(table, columns, predicates)

    @property
    def is_ordered_ir(self) -> bool:
        return False

    def builder(self):
        """Creates a mutable builder for expressions."""
        # Since ArrayValue is intended to be immutable (immutability offers
        # potential opportunities for caching, though we might need to introduce
        # more node types for that to be useful), we create a builder class.
        return UnorderedIR.Builder(
            self._table,
            columns=self._columns,
            predicates=self._predicates,
        )

    def peek_sql(self, n: int):
        # Peek currently implemented as top level LIMIT op.
        # Execution engine handles limit pushdown.
        # In future, may push down limit/filters in compilation.
        sql = ibis_bigquery.Backend().compile(self._to_ibis_expr().limit(n))
        return typing.cast(str, sql)

    def to_sql(
        self,
        offset_column: typing.Optional[str] = None,
        col_id_overrides: typing.Mapping[str, str] = {},
        ordered: bool = False,
    ) -> str:
        if offset_column or ordered:
            raise ValueError("Cannot produce sorted sql in partial ordering mode")
        sql = ibis_bigquery.Backend().compile(
            self._to_ibis_expr(
                col_id_overrides=col_id_overrides,
            )
        )
        return typing.cast(str, sql)

    def row_count(self) -> OrderedIR:
        original_table = self._to_ibis_expr()
        ibis_table = original_table.agg(
            [
                original_table.count().name("count"),
            ]
        )
        return OrderedIR(
            ibis_table,
            (ibis_table["count"],),
            ordering=TotalOrdering(
                ordering_value_columns=(ascending_over("count"),),
                total_ordering_columns=frozenset([ex.deref("count")]),
            ),
        )

    def _to_ibis_expr(
        self,
        *,
        expose_hidden_cols: bool = False,
        fraction: Optional[float] = None,
        col_id_overrides: typing.Mapping[str, str] = {},
    ):
        """
        Creates an Ibis table expression representing the DataFrame.

        ArrayValue objects are sorted, so the following options are available
        to reflect this in the ibis expression.

        * "string_encoded": An ordered string column is provided in output table.
        * "unordered": No ordering information will be provided in output. Only
          value columns are projected.

        For offset or ordered column, order_col_name can be used to assign the
        output label for the ordering column. If none is specified, the default
        column name will be 'bigframes_ordering_id'

        Args:
            expose_hidden_cols:
                If True, include the hidden ordering columns in the results.
                Only compatible with `order_by` and `unordered`
                ``ordering_mode``.
            col_id_overrides:
                overrides the column ids for the result
        Returns:
            An ibis expression representing the data help by the ArrayValue object.
        """
        columns = list(self._columns)
        columns_to_drop: list[
            str
        ] = []  # Ordering/Filtering columns that will be dropped at end

        if self._reduced_predicate is not None:
            columns.append(self._reduced_predicate)
            # Usually drop predicate as it is will be all TRUE after filtering
            if not expose_hidden_cols:
                columns_to_drop.append(self._reduced_predicate.get_name())

        # Special case for empty tables, since we can't create an empty
        # projection.
        if not columns:
            return ibis.memtable([])

        table = self._table.select(columns)
        base_table = table
        if self._reduced_predicate is not None:
            table = table.filter(base_table[PREDICATE_COLUMN])
        table = table.drop(*columns_to_drop)
        if col_id_overrides:
            table = table.rename(
                {value: key for key, value in col_id_overrides.items()}
            )
        if fraction is not None:
            table = table.filter(ibis.random() < ibis.literal(fraction))
        return table

    def filter(self, predicate: ex.Expression) -> UnorderedIR:
        for ref in predicate.column_references:
            ibis_value = self._get_ibis_column(ref.sql)
            if is_window(ibis_value):
                # ibis doesn't support qualify syntax, so create CTE if filtering over window expression
                # https://github.com/ibis-project/ibis/issues/9775
                return self._reproject_to_table().filter(predicate)

        bindings = {col: self._get_ibis_column(col) for col in self.column_ids}
        condition = op_compiler.compile_expression(predicate, bindings)
        return self._filter(condition)

    def _filter(self, predicate_value: ibis_types.BooleanValue) -> UnorderedIR:
        """Filter the table on a given expression, the predicate must be a boolean series aligned with the table expression."""
        expr = self.builder()
        expr.predicates = [*self._predicates, predicate_value]
        return expr.build()

    def aggregate(
        self,
        aggregations: typing.Sequence[typing.Tuple[ex.Aggregation, str]],
        by_column_ids: typing.Sequence[ex.DerefOp] = (),
        dropna: bool = True,
    ) -> OrderedIR:
        """
        Apply aggregations to the expression.
        Arguments:
            aggregations: input_column_id, operation, output_column_id tuples
            by_column_ids: column ids of the aggregation key, this is preserved through
              the transform
            dropna: whether null keys should be dropped
        Returns:
            OrderedIR: the grouping key is a unique-valued column and has ordering
              information.
        """
        table = self._to_ibis_expr()
        return self._aggregate_base(
            table, aggregations=aggregations, by_column_ids=by_column_ids, dropna=dropna
        )

    def _uniform_sampling(self, fraction: float) -> UnorderedIR:
        """Sampling the table on given fraction.

        .. warning::
            The row numbers of result is non-deterministic, avoid to use.
        """
        table = self._to_ibis_expr(fraction=fraction)
        columns = [table[column_name] for column_name in self._column_names]
        return UnorderedIR(
            table,
            columns=columns,
        )

    def explode(self, columns: typing.Sequence[ex.DerefOp]) -> UnorderedIR:
        table = self._to_ibis_expr()
        column_ids = tuple(ref.id.sql for ref in columns)

        # The offset array ensures null represents empty arrays after unnesting.
        offset_array_id = bigframes.core.guid.generate_guid("offset_array_")
        offset_array = ibis.range(
            0,
            ibis.greatest(
                1,  # We always want at least 1 element to fill in NULLs for empty arrays.
                ibis.least(*[table[column_id].length() for column_id in column_ids]),
            ),
        ).name(offset_array_id)
        table_w_offset_array = table.select(
            offset_array,
            *self._column_names,
        )

        unnest_offset_id = bigframes.core.guid.generate_guid("unnest_offset_")
        unnest_offset = (
            table_w_offset_array[offset_array_id].unnest().name(unnest_offset_id)
        )
        table_w_offset = table_w_offset_array.select(
            unnest_offset,
            *self._column_names,
        )

        unnested_columns = [
            table_w_offset[column_id][table_w_offset[unnest_offset_id]].name(column_id)
            if column_id in column_ids
            else table_w_offset[column_id]
            for column_id in self._column_names
        ]
        table_w_unnest = table_w_offset.select(*unnested_columns)

        columns = [table_w_unnest[column_name] for column_name in self._column_names]
        return UnorderedIR(
            table_w_unnest,
            columns=columns,
        )

    def as_ordered_ir(self) -> OrderedIR:
        """Convert to OrderedIr, but without any definite ordering."""
        return OrderedIR(self._table, self._columns, predicates=self._predicates)

    ## Helpers
    def _set_or_replace_by_id(
        self, id: str, new_value: ibis_types.Value
    ) -> UnorderedIR:
        builder = self.builder()
        if id in self.column_ids:
            builder.columns = [
                val if (col_id != id) else new_value.name(id)
                for col_id, val in zip(self.column_ids, self._columns)
            ]
        else:
            builder.columns = [*self.columns, new_value.name(id)]
        return builder.build()

    def _select(self, values: typing.Tuple[ibis_types.Value]) -> UnorderedIR:
        builder = self.builder()
        builder.columns = values
        return builder.build()

    def _reproject_to_table(self) -> UnorderedIR:
        """
        Internal operators that projects the internal representation into a
        new ibis table expression where each value column is a direct
        reference to a column in that table expression. Needed after
        some operations such as window operations that cannot be used
        recursively in projections.
        """
        table = self._to_ibis_expr()
        columns = [table[column_name] for column_name in self._column_names]
        return UnorderedIR(
            table,
            columns=columns,
        )

    class Builder:
        def __init__(
            self,
            table: ibis_types.Table,
            columns: Collection[ibis_types.Value] = (),
            predicates: Optional[Collection[ibis_types.BooleanValue]] = None,
        ):
            self.table = table
            self.columns = list(columns)
            self.predicates = list(predicates) if predicates is not None else None

        def build(self) -> UnorderedIR:
            return UnorderedIR(
                table=self.table,
                columns=self.columns,
                predicates=self.predicates,
            )


class OrderedIR(BaseIbisIR):
    """Immutable BigQuery DataFrames expression tree.

    Note: Usage of this class is considered to be private and subject to change
    at any time.

    This class is a wrapper around Ibis expressions. Its purpose is to defer
    Ibis projection operations to keep generated SQL small and correct when
    mixing and matching columns from different versions of a DataFrame.

    Args:
        table: An Ibis table expression.
        columns: Ibis value expressions that can be projected as columns.
        hidden_ordering_columns: Ibis value expressions to store ordering.
        ordering: An ordering property of the data frame.
        predicates: A list of filters on the data frame.
    """

    def __init__(
        self,
        table: ibis_types.Table,
        columns: Sequence[ibis_types.Value],
        hidden_ordering_columns: Optional[Sequence[ibis_types.Value]] = None,
        ordering: RowOrdering = RowOrdering(),
        predicates: Optional[Collection[ibis_types.BooleanValue]] = None,
    ):
        super().__init__(table, columns, predicates)
        self._ordering = ordering
        # Meta columns store ordering, or other data that doesn't correspond to dataframe columns
        self._hidden_ordering_columns = (
            tuple(hidden_ordering_columns)
            if hidden_ordering_columns is not None
            else ()
        )

        # To allow for more efficient lookup by column name, create a
        # dictionary mapping names to column values.
        self._column_names = {
            (
                column.resolve(table)
                # TODO(https://github.com/ibis-project/ibis/issues/7613): use
                # public API to refer to Deferred type.
                if isinstance(column, ibis.common.deferred.Deferred)
                else column
            ).get_name(): column
            for column in self._columns
        }
        self._hidden_ordering_column_names = {
            typing.cast(str, column.get_name()): column
            for column in self._hidden_ordering_columns
        }
        ### Validation
        value_col_ids = self._column_names.keys()
        hidden_col_ids = self._hidden_ordering_column_names.keys()

        all_columns = value_col_ids | hidden_col_ids
        ordering_valid = all(
            set(ref.sql for ref in col.scalar_expression.column_references).issubset(
                all_columns
            )
            for col in ordering.all_ordering_columns
        )
        if value_col_ids & hidden_col_ids:
            raise ValueError(
                f"Keys in both hidden and exposed list: {value_col_ids & hidden_col_ids}"
            )
        if not ordering_valid:
            raise ValueError(f"Illegal ordering keys: {ordering.all_ordering_columns}")

    @property
    def is_ordered_ir(self) -> bool:
        return True

    @property
    def has_total_order(self) -> bool:
        return isinstance(self._ordering, TotalOrdering)

    @classmethod
    def from_pandas(
        cls, pd_df: pandas.DataFrame, scan_cols: bigframes.core.nodes.ScanList
    ) -> OrderedIR:
        """
        Builds an in-memory only (SQL only) expr from a pandas dataframe.

        Assumed that the dataframe has unique string column names and bigframes-suppported
        dtypes.
        """

        # ibis memtable cannot handle NA, must convert to None
        # this destroys the schema however
        ibis_values = pd_df.astype("object").where(pandas.notnull(pd_df), None)  # type: ignore
        ibis_values = ibis_values.assign(**{ORDER_ID_COLUMN: range(len(pd_df))})
        # derive the ibis schema from the original pandas schema
        ibis_schema = [
            (
                local_label,
                bigframes.core.compile.ibis_types.bigframes_dtype_to_ibis_dtype(dtype),
            )
            for id, dtype, local_label in scan_cols.items
        ]
        ibis_schema.append((ORDER_ID_COLUMN, ibis_dtypes.int64))

        keys_memtable = ibis.memtable(ibis_values, schema=ibis.schema(ibis_schema))

        return cls(
            keys_memtable,
            columns=[
                keys_memtable[local_label].name(col_id.sql)
                for col_id, _, local_label in scan_cols.items
            ],
            ordering=TotalOrdering.from_offset_col(ORDER_ID_COLUMN),
            hidden_ordering_columns=(keys_memtable[ORDER_ID_COLUMN],),
        )

    @property
    def _ibis_bindings(self) -> dict[str, ibis_types.Value]:
        all_keys = itertools.chain(self.column_ids, self._hidden_column_ids)
        return {col: self._get_any_column(col) for col in all_keys}

    @property
    def _hidden_column_ids(self) -> typing.Sequence[str]:
        return tuple(self._hidden_ordering_column_names.keys())

    @property
    def _ibis_order(self) -> Sequence[ibis_types.Value]:
        """Returns a sequence of ibis values which can be directly used to order a
        table expression. Has direction modifiers applied."""
        return _convert_ordering_to_table_values(
            {**self._column_names, **self._hidden_ordering_column_names},
            self._ordering.all_ordering_columns,
        )

    def to_unordered(self) -> UnorderedIR:
        return UnorderedIR(self._table, self._columns, self._predicates)

    def builder(self) -> OrderedIR.Builder:
        """Creates a mutable builder for expressions."""
        # Since ArrayValue is intended to be immutable (immutability offers
        # potential opportunities for caching, though we might need to introduce
        # more node types for that to be useful), we create a builder class.
        return OrderedIR.Builder(
            self._table,
            columns=self._columns,
            hidden_ordering_columns=self._hidden_ordering_columns,
            ordering=self._ordering,
            predicates=self._predicates,
        )

    def order_by(self, by: Sequence[OrderingExpression]) -> OrderedIR:
        expr_builder = self.builder()
        expr_builder.ordering = self._ordering.with_ordering_columns(by)
        return expr_builder.build()

    def reversed(self) -> OrderedIR:
        expr_builder = self.builder()
        expr_builder.ordering = self._ordering.with_reverse()
        return expr_builder.build()

    def aggregate(
        self,
        aggregations: typing.Sequence[typing.Tuple[ex.Aggregation, str]],
        by_column_ids: typing.Sequence[ex.DerefOp] = (),
        dropna: bool = True,
    ) -> OrderedIR:
        """
        Apply aggregations to the expression.
        Arguments:
            aggregations: input_column_id, operation, output_column_id tuples
            by_column_ids: column ids of the aggregation key, this is preserved through
              the transform
            dropna: whether null keys should be dropped
        Returns:
            OrderedIR
        """
        table = self._to_ibis_expr(ordering_mode="unordered", expose_hidden_cols=True)

        all_columns = {
            column_name: table[column_name]
            for column_name in {
                **self._column_names,
                **self._hidden_ordering_column_names,
            }
        }
        order_by = _convert_ordering_to_table_values(
            all_columns,
            self._ordering.all_ordering_columns,
        )

        return self._aggregate_base(
            table,
            order_by=order_by,
            aggregations=aggregations,
            by_column_ids=by_column_ids,
            dropna=dropna,
        )

    def _uniform_sampling(self, fraction: float) -> OrderedIR:
        """Sampling the table on given fraction.

        .. warning::
            The row numbers of result is non-deterministic, avoid to use.
        """
        table = self._to_ibis_expr(
            ordering_mode="unordered", expose_hidden_cols=True, fraction=fraction
        )
        columns = [table[column_name] for column_name in self._column_names]
        hidden_ordering_columns = [
            table[column_name] for column_name in self._hidden_ordering_column_names
        ]
        return OrderedIR(
            table,
            columns=columns,
            hidden_ordering_columns=hidden_ordering_columns,
            ordering=self._ordering,
        )

    def explode(self, columns: typing.Sequence[ex.DerefOp]) -> OrderedIR:
        table = self._to_ibis_expr(ordering_mode="unordered", expose_hidden_cols=True)
        column_ids = tuple(ref.id.sql for ref in columns)

        offset_array_id = bigframes.core.guid.generate_guid("offset_array_")
        offset_array = ibis.range(
            0,
            ibis.greatest(
                1,  # We always want at least 1 element to fill in NULLs for empty arrays.
                ibis.least(*[table[column_id].length() for column_id in column_ids]),
            ),
        ).name(offset_array_id)
        table_w_offset_array = table.select(
            offset_array,
            *self._column_names,
            *self._hidden_ordering_column_names,
        )

        unnest_offset_id = bigframes.core.guid.generate_guid("unnest_offset_")
        unnest_offset = (
            table_w_offset_array[offset_array_id].unnest().name(unnest_offset_id)
        )
        table_w_offset = table_w_offset_array.select(
            unnest_offset,
            *self._column_names,
            *self._hidden_ordering_column_names,
        )

        unnested_columns = [
            table_w_offset[column_id][table_w_offset[unnest_offset_id]].name(column_id)
            if column_id in column_ids
            else table_w_offset[column_id]
            for column_id in self._column_names
        ]

        table_w_unnest = table_w_offset.select(
            table_w_offset[unnest_offset_id],
            *unnested_columns,
            *self._hidden_ordering_column_names,
        )

        columns = [table_w_unnest[column_name] for column_name in self._column_names]
        hidden_ordering_columns = [
            *[
                table_w_unnest[column_name]
                for column_name in self._hidden_ordering_column_names
            ],
            table_w_unnest[unnest_offset_id],
        ]
        l_mappings = {id: id for id in self._ordering.referenced_columns}
        r_mappings = {ids.ColumnId(unnest_offset_id): ids.ColumnId(unnest_offset_id)}
        ordering = join_orderings(
            self._ordering,
            TotalOrdering.from_offset_col(unnest_offset_id),
            l_mappings,
            r_mappings,
        )

        return OrderedIR(
            table_w_unnest,
            columns=columns,
            hidden_ordering_columns=hidden_ordering_columns,
            ordering=ordering,
        )

    def promote_offsets(self, col_id: str) -> OrderedIR:
        """
        Convenience function to promote copy of column offsets to a value column. Can be used to reset index.
        """
        # Special case: offsets already exist
        ordering = self._ordering
        # Case 1, already have offsets, just create column from them
        if ordering.is_sequential and (ordering.total_order_col is not None):
            expr_builder = self.builder()
            expr_builder.columns = [
                *self.columns,
                self._compile_expression(
                    ordering.total_order_col.scalar_expression
                ).name(col_id),
            ]
            return expr_builder.build()
        # Cannot nest analytic expressions, so reproject to cte first if needed.
        # Also ibis cannot window literals, so need to reproject those (even though this is legal in googlesql)
        # Seee: https://github.com/ibis-project/ibis/issues/9773
        can_directly_window = not any(
            map(
                lambda x: is_literal(x) or is_window(x),
                itertools.chain(self._ibis_order, self._predicates),
            )
        )
        if not can_directly_window:
            return self._reproject_to_table().promote_offsets(col_id)

        window = ibis.window(order_by=self._ibis_order)
        if self._predicates:
            window = window.group_by(self._reduced_predicate)
        offsets = ibis.row_number().over(window)
        expr_builder = self.builder()
        expr_builder.columns = [
            *self.columns,
            offsets.name(col_id),
        ]
        # Reproject, so that offsets are just a scalar value that can be used elsewhere
        expr_builder.ordering = TotalOrdering.from_offset_col(col_id)
        return expr_builder.build()._reproject_to_table()

    ## Methods that only work with ordering
    def project_window_op(
        self,
        column_name: ex.DerefOp,
        op: agg_ops.UnaryWindowOp,
        window_spec: WindowSpec,
        output_name: str,
        *,
        never_skip_nulls=False,
    ) -> OrderedIR:
        """
        Creates a new expression based on this expression with unary operation applied to one column.
        column_name: the id of the input column present in the expression
        op: the windowable operator to apply to the input column
        window_spec: a specification of the window over which to apply the operator
        output_name: the id to assign to the output of the operator
        never_skip_nulls: will disable null skipping for operators that would otherwise do so
        """
        # Cannot nest analytic expressions, so reproject to cte first if needed.
        # Also ibis cannot window literals, so need to reproject those (even though this is legal in googlesql)
        # See: https://github.com/ibis-project/ibis/issues/9773
        used_exprs = map(
            self._compile_expression,
            itertools.chain(
                (column_name,), map(ex.DerefOp, window_spec.all_referenced_columns)
            ),
        )
        can_directly_window = not any(
            map(lambda x: is_literal(x) or is_window(x), used_exprs)
        )
        if not can_directly_window:
            return self._reproject_to_table().project_window_op(
                column_name,
                op,
                window_spec,
                output_name,
                never_skip_nulls=never_skip_nulls,
            )

        column = typing.cast(ibis_types.Column, self._compile_expression(column_name))
        window = self._ibis_window_from_spec(
            window_spec, require_total_order=op.uses_total_row_ordering
        )
        bindings = {col: self._get_ibis_column(col) for col in self.column_ids}

        window_op = agg_compiler.compile_analytic(
            ex.UnaryAggregation(op, column_name),
            window,
            bindings=bindings,
        )

        clauses = []
        if op.skips_nulls and not never_skip_nulls:
            clauses.append((column.isnull(), ibis.null()))
        if window_spec.min_periods:
            if op.skips_nulls:
                # Most operations do not count NULL values towards min_periods
                observation_count = agg_compiler.compile_analytic(
                    ex.UnaryAggregation(agg_ops.count_op, column_name),
                    window,
                    bindings=bindings,
                )
            else:
                # Operations like count treat even NULLs as valid observations for the sake of min_periods
                # notnull is just used to convert null values to non-null (FALSE) values to be counted
                denulled_value = typing.cast(ibis_types.BooleanColumn, column.notnull())
                observation_count = agg_compiler.compile_analytic(
                    ex.UnaryAggregation(agg_ops.count_op, ex.deref("_denulled")),
                    window,
                    bindings={**bindings, "_denulled": denulled_value},
                )
            clauses.append(
                (
                    observation_count < ibis_types.literal(window_spec.min_periods),
                    ibis.null(),
                )
            )
        if clauses:
            case_statement = ibis.case()
            for clause in clauses:
                case_statement = case_statement.when(clause[0], clause[1])
            case_statement = case_statement.else_(window_op).end()  # type: ignore
            window_op = case_statement

        result = self._set_or_replace_by_id(output_name, window_op)
        return result

    def _reproject_to_table(self) -> OrderedIR:
        table = self._to_ibis_expr(
            ordering_mode="unordered",
            expose_hidden_cols=True,
        )
        columns = [table[column_name] for column_name in self._column_names]
        ordering_col_ids = list(
            id.sql
            for id in itertools.chain.from_iterable(
                ref.scalar_expression.column_references
                for ref in self._ordering.all_ordering_columns
            )
        )
        hidden_ordering_columns = [
            table[column_name]
            for column_name in self._hidden_ordering_column_names
            if column_name in ordering_col_ids
        ]
        return OrderedIR(
            table,
            columns=columns,
            hidden_ordering_columns=hidden_ordering_columns,
            ordering=self._ordering,
        )

    def to_sql(
        self,
        col_id_overrides: typing.Mapping[str, str] = {},
        ordered: bool = False,
        limit: Optional[int] = None,
    ) -> str:
        if ordered or limit:
            # Need to bake ordering expressions into the selected column in order for our ordering clause builder to work.
            baked_ir = self._bake_ordering()
            sql = ibis_bigquery.Backend().compile(
                baked_ir._to_ibis_expr(
                    ordering_mode="unordered",
                    col_id_overrides=col_id_overrides,
                    expose_hidden_cols=True,
                )
            )
            output_columns = [
                col_id_overrides.get(col, col) for col in baked_ir.column_ids
            ]
            sql = (
                bigframes.core.compile.googlesql.Select()
                .from_(sql)
                .select(output_columns)
                .sql()
            )

            # Single row frames may not have any ordering columns
            if len(baked_ir._ordering.all_ordering_columns) > 0:
                order_by_clause = bigframes.core.sql.ordering_clause(
                    baked_ir._ordering.all_ordering_columns
                )
                sql += f"\n{order_by_clause}"
            if limit is not None:
                if not isinstance(limit, int):
                    raise TypeError(f"Limit param: {limit} must be an int.")
                sql += f"\nLIMIT {limit}"
        else:
            sql = ibis_bigquery.Backend().compile(
                self._to_ibis_expr(
                    ordering_mode="unordered",
                    col_id_overrides=col_id_overrides,
                    expose_hidden_cols=False,
                )
            )
        return typing.cast(str, sql)

    def raw_sql_and_schema(
        self,
    ) -> typing.Tuple[str, typing.Sequence[google.cloud.bigquery.SchemaField]]:
        """Return sql with all hidden columns. Used to cache with ordering information.

        Also returns schema, as the extra ordering columns are determined compile-time.
        """
        all_columns = (*self.column_ids, *self._hidden_ordering_column_names.keys())
        as_ibis = self._to_ibis_expr(
            ordering_mode="unordered",
            expose_hidden_cols=True,
        ).select(all_columns)

        # Ibis will produce non-nullable schema types, but bigframes should always be nullable
        fixed_ibis_schema = ibis_schema.Schema.from_tuples(
            (name, dtype.copy(nullable=True))
            for (name, dtype) in as_ibis.schema().items()
        )
        bq_schema = ibis.backends.bigquery.datatypes.BigQuerySchema.from_ibis(
            fixed_ibis_schema
        )
        return ibis_bigquery.Backend().compile(as_ibis), bq_schema

    def _to_ibis_expr(
        self,
        *,
        expose_hidden_cols: bool = False,
        fraction: Optional[float] = None,
        col_id_overrides: typing.Mapping[str, str] = {},
        ordering_mode: Literal["string_encoded", "unordered"],
        order_col_name: Optional[str] = ORDER_ID_COLUMN,
    ):
        """
        Creates an Ibis table expression representing the DataFrame.

        ArrayValue objects are sorted, so the following options are available
        to reflect this in the ibis expression.


        * "string_encoded": An ordered string column is provided in output table.
        * "unordered": No ordering information will be provided in output. Only
          value columns are projected.

        For offset or ordered column, order_col_name can be used to assign the
        output label for the ordering column. If none is specified, the default
        column name will be 'bigframes_ordering_id'

        Args:
            expose_hidden_cols:
                If True, include the hidden ordering columns in the results.
                Only compatible with `order_by` and `unordered`
                ``ordering_mode``.
            ordering_mode:
                How to construct the Ibis expression from the ArrayValue. See
                above for details.
            order_col_name:
                If the ordering mode outputs a single ordering or offsets
                column, use this as the column name.
            col_id_overrides:
                overrides the column ids for the result
        Returns:
            An ibis expression representing the data help by the ArrayValue object.
        """
        assert ordering_mode in (
            "string_encoded",
            "unordered",
        )
        if expose_hidden_cols and ordering_mode in ("ordered_col"):
            raise ValueError(
                f"Cannot expose hidden ordering columns with ordering_mode {ordering_mode}"
            )

        columns = list(self._columns)
        columns_to_drop: list[
            str
        ] = []  # Ordering/Filtering columns that will be dropped at end

        if self._reduced_predicate is not None:
            columns.append(self._reduced_predicate)
            # Usually drop predicate as it is will be all TRUE after filtering
            if not expose_hidden_cols:
                columns_to_drop.append(self._reduced_predicate.get_name())

        order_columns = self._create_order_columns(
            ordering_mode, order_col_name, expose_hidden_cols
        )
        columns.extend(order_columns)

        # Special case for empty tables, since we can't create an empty
        # projection.
        if not columns:
            return ibis.memtable([])

        # Make sure we don't have any unbound (deferred) columns.
        table = self._table.select(columns)

        table = table.select(table[column] for column in table.columns)
        base_table = table
        if self._reduced_predicate is not None:
            table = table.filter(base_table[PREDICATE_COLUMN])
        table = table.drop(*columns_to_drop)
        if col_id_overrides:
            table = table.rename(
                {value: key for key, value in col_id_overrides.items()}
            )
        if fraction is not None:
            table = table.filter(ibis.random() < ibis.literal(fraction))
        return table

    def filter(self, predicate: ex.Expression) -> OrderedIR:
        for ref in predicate.column_references:
            ibis_value = self._get_ibis_column(ref.sql)
            if is_window(ibis_value):
                # ibis doesn't support qualify syntax, so create CTE if filtering over window expression
                # https://github.com/ibis-project/ibis/issues/9775
                return self._reproject_to_table().filter(predicate)

        bindings = {col: self._get_ibis_column(col) for col in self.column_ids}
        condition = op_compiler.compile_expression(predicate, bindings)
        return self._filter(condition)

    def _filter(self, predicate_value: ibis_types.BooleanValue) -> OrderedIR:
        """Filter the table on a given expression, the predicate must be a boolean series aligned with the table expression."""
        expr = self.builder()
        expr.ordering = expr.ordering.with_non_sequential()
        expr.predicates = [*self._predicates, predicate_value]
        return expr.build()

    def _set_or_replace_by_id(self, id: str, new_value: ibis_types.Value) -> OrderedIR:
        """Safely assign by id while maintaining ordering integrity."""
        # TODO: Split into explicit set and replace methods
        ordering_col_ids = set(
            id.sql
            for id in itertools.chain.from_iterable(
                col_ref.scalar_expression.column_references
                for col_ref in self._ordering.ordering_value_columns
            )
        )
        if id in ordering_col_ids:
            return self._hide_column(id)._set_or_replace_by_id(id, new_value)

        builder = self.builder()
        if id in self.column_ids:
            builder.columns = [
                val if (col_id != id) else new_value.name(id)
                for col_id, val in zip(self.column_ids, self._columns)
            ]
        else:
            builder.columns = [*self.columns, new_value.name(id)]
        return builder.build()

    def _select(self, values: typing.Tuple[ibis_types.Value]) -> OrderedIR:
        """Safely assign by id while maintaining ordering integrity."""
        # TODO: Split into explicit set and replace methods
        ordering_col_ids = set(
            id.sql
            for id in itertools.chain.from_iterable(
                [
                    col_ref.scalar_expression.column_references
                    for col_ref in self._ordering.ordering_value_columns
                ]
            )
        )
        ir = self
        mappings = {typing.cast(str, value.get_name()): value for value in values}
        for ordering_id in ordering_col_ids:
            # Drop case
            if (ordering_id not in mappings) and (ordering_id in ir.column_ids):
                # id is being dropped, hide it first
                ir = ir._hide_column(ordering_id)
            # Mutate case
            elif (ordering_id in mappings) and not mappings[ordering_id].equals(
                ir._get_any_column(ordering_id)
            ):
                ir = ir._hide_column(ordering_id)

        builder = ir.builder()
        builder.columns = list(values)
        return builder.build()

    ## Ordering specific helpers
    def _get_any_column(self, key: str) -> ibis_types.Value:
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

    def _hide_column(self, column_id: str) -> OrderedIR:
        """Pushes columns to hidden columns list. Used to hide ordering columns that have been dropped or destructively mutated."""
        expr_builder = self.builder()
        # Need to rename column as caller might be creating a new row with the same name but different values.
        # Can avoid this if don't allow callers to determine ids and instead generate unique ones in this class.
        new_name = ids.ColumnId(
            bigframes.core.guid.generate_guid(prefix="bigframes_hidden_")
        )
        expr_builder.hidden_ordering_columns = [
            *self._hidden_ordering_columns,
            self._get_ibis_column(column_id).name(new_name.sql),
        ]
        matching_ref = next(
            ref for ref in self._ordering.referenced_columns if ref.sql == column_id
        )
        # allow_partial_bindings since only remapping hidden column, not all columns
        expr_builder.ordering = self._ordering.remap_column_refs(
            {matching_ref: new_name}, allow_partial_bindings=True
        )
        return expr_builder.build()

    def _bake_ordering(self) -> OrderedIR:
        """Bakes ordering expression into the selection, maybe creating hidden columns."""
        ordering_expressions = self._ordering.all_ordering_columns
        new_exprs: list[OrderingExpression] = []
        new_baked_cols: list[ibis_types.Value] = []
        for expr in ordering_expressions:
            if isinstance(expr.scalar_expression, ex.OpExpression):
                baked_column = self._compile_expression(expr.scalar_expression).name(
                    bigframes.core.guid.generate_guid()
                )
                new_baked_cols.append(baked_column)
                new_expr = OrderingExpression(
                    ex.deref(baked_column.get_name()), expr.direction, expr.na_last
                )
                new_exprs.append(new_expr)
            elif isinstance(expr.scalar_expression, ex.DerefOp):
                order_col = expr.scalar_expression.id
                new_exprs.append(expr)
                if order_col.sql not in self.column_ids:
                    new_baked_cols.append(
                        self._ibis_bindings[expr.scalar_expression.id.sql]
                    )

        if isinstance(self._ordering, TotalOrdering):
            new_ordering: RowOrdering = TotalOrdering(
                tuple(new_exprs),
                self._ordering.integer_encoding,
                self._ordering.string_encoding,
                self._ordering.total_ordering_columns,
            )
        else:
            new_ordering = RowOrdering(
                tuple(new_exprs),
                self._ordering.integer_encoding,
                self._ordering.string_encoding,
            )
        return OrderedIR(
            self._table,
            columns=self.columns,
            hidden_ordering_columns=tuple(new_baked_cols),
            ordering=new_ordering,
            predicates=self._predicates,
        )

    def _create_order_columns(
        self,
        ordering_mode: str,
        order_col_name: Optional[str],
        expose_hidden_cols: bool,
    ) -> typing.Sequence[ibis_types.Value]:
        # Generate offsets if current ordering id semantics are not sufficiently strict
        if ordering_mode == "string_encoded":
            return (self._create_string_ordering_column().name(order_col_name),)
        elif expose_hidden_cols:
            return self._hidden_ordering_columns
        return ()

    def _create_offset_column(self) -> ibis_types.IntegerColumn:
        if self._ordering.total_order_col and self._ordering.is_sequential:
            offsets = self._compile_expression(
                self._ordering.total_order_col.scalar_expression
            )
            return typing.cast(ibis_types.IntegerColumn, offsets)
        else:
            window = ibis.window(order_by=self._ibis_order)
            if self._predicates:
                window = window.group_by(self._reduced_predicate)
            offsets = ibis.row_number().over(window)
            return typing.cast(ibis_types.IntegerColumn, offsets)

    def _create_string_ordering_column(self) -> ibis_types.StringColumn:
        if self._ordering.total_order_col and self._ordering.is_string_encoded:
            string_order_ids = op_compiler.compile_expression(
                self._ordering.total_order_col.scalar_expression, self._ibis_bindings
            )
            return typing.cast(ibis_types.StringColumn, string_order_ids)
        if (
            self._ordering.total_order_col
            and self._ordering.integer_encoding.is_encoded
        ):
            # Special case: non-negative integer ordering id can be converted directly to string without regenerating row numbers
            int_values = self._compile_expression(
                self._ordering.total_order_col.scalar_expression
            )
            return encode_order_string(
                typing.cast(ibis_types.IntegerColumn, int_values),
            )
        else:
            # Have to build string from scratch
            window = ibis.window(order_by=self._ibis_order)
            if self._predicates:
                window = window.group_by(self._reduced_predicate)
            row_nums = typing.cast(
                ibis_types.IntegerColumn, ibis.row_number().over(window)
            )
            return encode_order_string(row_nums)

    def _compile_expression(self, expr: ex.Expression):
        return op_compiler.compile_expression(expr, self._ibis_bindings)

    def _ibis_window_from_spec(
        self, window_spec: WindowSpec, require_total_order: bool
    ):
        group_by: typing.List[ibis_types.Value] = (
            [
                typing.cast(
                    ibis_types.Column, _as_identity(self._compile_expression(column))
                )
                for column in window_spec.grouping_keys
            ]
            if window_spec.grouping_keys
            else []
        )
        if self._reduced_predicate is not None:
            group_by.append(self._reduced_predicate)

        # Construct ordering. There are basically 3 main cases
        # 1. Order-independent op (aggregation, cut, rank) with unbound window - no ordering clause needed
        # 2. Order-independent op (aggregation, cut, rank) with range window - use ordering clause, ties allowed
        # 3. Order-depedenpent op (navigation functions, array_agg) or rows bounds - use total row order to break ties.
        if window_spec.ordering:
            order_by = _convert_ordering_to_table_values(
                {**self._column_names, **self._hidden_ordering_column_names},
                window_spec.ordering,
            )
            if require_total_order or isinstance(window_spec.bounds, RowsWindowBounds):
                # Some operators need an unambiguous ordering, so the table's total ordering is appended
                order_by = tuple([*order_by, *self._ibis_order])
        elif isinstance(window_spec.bounds, RowsWindowBounds):
            # If window spec has following or preceding bounds, we need to apply an unambiguous ordering.
            order_by = tuple(self._ibis_order)
        else:
            # Unbound grouping window. Suitable for aggregations but not for analytic function application.
            order_by = None

        bounds = window_spec.bounds
        window = ibis.window(order_by=order_by, group_by=group_by)
        if bounds is not None:
            if isinstance(bounds, RangeWindowBounds):
                window = window.preceding_following(
                    bounds.preceding, bounds.following, how="range"
                )
            if isinstance(bounds, RowsWindowBounds):
                if bounds.preceding is not None or bounds.following is not None:
                    window = window.preceding_following(
                        bounds.preceding, bounds.following, how="rows"
                    )
            else:
                raise ValueError(f"unrecognized window bounds {bounds}")
        return window

    class Builder:
        def __init__(
            self,
            table: ibis_types.Table,
            ordering: RowOrdering,
            columns: Collection[ibis_types.Value] = (),
            hidden_ordering_columns: Collection[ibis_types.Value] = (),
            predicates: Optional[Collection[ibis_types.BooleanValue]] = None,
        ):
            self.table = table
            self.columns = list(columns)
            self.hidden_ordering_columns = list(hidden_ordering_columns)
            self.ordering = ordering
            self.predicates = list(predicates) if predicates is not None else None

        def build(self) -> OrderedIR:
            return OrderedIR(
                table=self.table,
                columns=self.columns,
                hidden_ordering_columns=self.hidden_ordering_columns,
                ordering=self.ordering,
                predicates=self.predicates,
            )


def is_literal(column: ibis_types.Value) -> bool:
    # Unfortunately, Literals in ibis are not "Columns"s and therefore can't be aggregated.
    return not isinstance(column, ibis_types.Column)


def is_window(column: ibis_types.Value) -> bool:
    matches = (
        (column)
        .op()
        .find_topmost(
            lambda x: isinstance(x, (ibis_ops.WindowFunction, ibis_ops.Relation))
        )
    )
    return any(isinstance(op, ibis_ops.WindowFunction) for op in matches)


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
    ordering_columns: typing.Sequence[OrderingExpression],
) -> typing.Sequence[ibis_types.Value]:
    column_refs = ordering_columns
    ordering_values = []
    for ordering_col in column_refs:
        expr = op_compiler.compile_expression(
            ordering_col.scalar_expression, value_lookup
        )
        ordering_value = (
            ibis.asc(expr) if ordering_col.direction.is_ascending else ibis.desc(expr)
        )
        # Bigquery SQL considers NULLS to be "smallest" values, but we need to override in these cases.
        if (not ordering_col.na_last) and (not ordering_col.direction.is_ascending):
            # Force nulls to be first
            is_null_val = typing.cast(ibis_types.Column, expr.isnull())
            ordering_values.append(ibis.desc(is_null_val))
        elif (ordering_col.na_last) and (ordering_col.direction.is_ascending):
            # Force nulls to be last
            is_null_val = typing.cast(ibis_types.Column, expr.isnull())
            ordering_values.append(ibis.asc(is_null_val))
        ordering_values.append(ordering_value)
    return ordering_values


def _as_identity(value: ibis_types.Value):
    # Some types need to be converted to string to enable groupby
    if value.type().is_float64() or value.type().is_geospatial():
        return value.cast(ibis_dtypes.str)
    return value
