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

import functools
import itertools
import typing
from typing import Literal, Optional, Sequence

import bigframes_vendored.ibis
import bigframes_vendored.ibis.backends.bigquery.backend as ibis_bigquery
import bigframes_vendored.ibis.common.deferred as ibis_deferred  # type: ignore
from bigframes_vendored.ibis.expr import builders as ibis_expr_builders
import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
from bigframes_vendored.ibis.expr.operations import window as ibis_expr_window
import bigframes_vendored.ibis.expr.operations as ibis_ops
import bigframes_vendored.ibis.expr.types as ibis_types
from google.cloud import bigquery
import pyarrow as pa

from bigframes.core import utils
import bigframes.core.compile.aggregate_compiler as agg_compiler
import bigframes.core.compile.googlesql
import bigframes.core.compile.ibis_types
import bigframes.core.compile.scalar_op_compiler as op_compilers
import bigframes.core.compile.scalar_op_compiler as scalar_op_compiler
import bigframes.core.expression as ex
from bigframes.core.ordering import OrderingExpression
import bigframes.core.sql
from bigframes.core.window_spec import RangeWindowBounds, RowsWindowBounds, WindowSpec
import bigframes.dtypes
import bigframes.operations.aggregations as agg_ops

op_compiler = op_compilers.scalar_op_compiler


# Ibis Implementations
class UnorderedIR:
    def __init__(
        self,
        table: ibis_types.Table,
        columns: Sequence[ibis_types.Value],
    ):
        self._table = table
        # Allow creating a DataFrame directly from an Ibis table expression.
        # TODO(swast): Validate that each column references the same table (or
        # no table for literal values).
        self._columns = tuple(
            column.resolve(table)  # type:ignore
            # TODO(https://github.com/ibis-project/ibis/issues/7613): use
            # public API to refer to Deferred type.
            if isinstance(column, ibis_deferred.Deferred) else column
            for column in columns
        )
        # To allow for more efficient lookup by column name, create a
        # dictionary mapping names to column values.
        self._column_names = {column.get_name(): column for column in self._columns}

    def to_sql(
        self,
        order_by: Sequence[OrderingExpression],
        limit: Optional[int],
        selections: tuple[tuple[ex.DerefOp, str], ...],
    ) -> str:
        ibis_table = self._to_ibis_expr()
        # This set of output transforms maybe should be its own output node??

        selection_strings = tuple((ref.id.sql, name) for ref, name in selections)

        names_preserved = tuple(name for _, name in selections) == tuple(
            self.column_ids
        )
        is_noop_selection = (
            all((i[0] == i[1] for i in selection_strings)) and names_preserved
        )

        if order_by or limit or not is_noop_selection:
            sql = ibis_bigquery.Backend().compile(ibis_table)
            sql = (
                bigframes.core.compile.googlesql.Select()
                .from_(sql)
                .select(selection_strings)
                .sql()
            )

            # Single row frames may not have any ordering columns
            if len(order_by) > 0:
                order_by_clause = bigframes.core.sql.ordering_clause(order_by)
                sql += f"\n{order_by_clause}"
            if limit is not None:
                if not isinstance(limit, int):
                    raise TypeError(f"Limit param: {limit} must be an int.")
                sql += f"\nLIMIT {limit}"
        else:
            sql = ibis_bigquery.Backend().compile(self._to_ibis_expr())
        return typing.cast(str, sql)

    @property
    def columns(self) -> tuple[ibis_types.Value, ...]:
        return self._columns

    @property
    def column_ids(self) -> typing.Sequence[str]:
        return tuple(self._column_names.keys())

    @property
    def _ibis_bindings(self) -> dict[str, ibis_types.Value]:
        return {col: self._get_ibis_column(col) for col in self.column_ids}

    def projection(
        self,
        expression_id_pairs: tuple[tuple[ex.Expression, str], ...],
    ) -> UnorderedIR:
        """Apply an expression to the ArrayValue and assign the output to a column."""
        cannot_inline = any(expr.expensive for expr, _ in expression_id_pairs)

        bindings = {col: self._get_ibis_column(col) for col in self.column_ids}
        new_values = [
            op_compiler.compile_expression(expression, bindings).name(id)
            for expression, id in expression_id_pairs
        ]
        result = UnorderedIR(self._table, (*self._columns, *new_values))
        if cannot_inline:
            return result._reproject_to_table()
        else:
            # Cheap ops can defer "SELECT" and inline into later ops
            return result

    def selection(
        self,
        input_output_pairs: tuple[tuple[ex.DerefOp, str], ...],
    ) -> UnorderedIR:
        """Apply an expression to the ArrayValue and assign the output to a column."""
        bindings = {col: self._get_ibis_column(col) for col in self.column_ids}
        values = [
            op_compiler.compile_expression(input, bindings).name(id)
            for input, id in input_output_pairs
        ]
        return UnorderedIR(self._table, tuple(values))

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

    def row_count(self, name: str) -> UnorderedIR:
        original_table = self._to_ibis_expr()
        ibis_table = original_table.agg(
            [
                original_table.count().name(name),
            ]
        )
        return UnorderedIR(
            ibis_table,
            (ibis_table[name],),
        )

    def _to_ibis_expr(
        self,
        *,
        fraction: Optional[float] = None,
    ):
        """
        Creates an Ibis table expression representing the DataFrame.

        Args:
            expose_hidden_cols:
                If True, include the hidden ordering columns in the results.

        Returns:
            An ibis expression representing the data help by the ArrayValue object.
        """
        # Special case for empty tables, since we can't create an empty
        # projection.
        if not self._columns:
            return self._table.select([bigframes_vendored.ibis.literal(1)])

        table = self._table.select(self._columns)
        if fraction is not None:
            table = table.filter(
                bigframes_vendored.ibis.random() < ibis_types.literal(fraction)
            )
        return table

    def filter(self, predicate: ex.Expression) -> UnorderedIR:
        table = self._to_ibis_expr()
        condition = op_compiler.compile_expression(predicate, table)
        table = table.filter(condition)
        return UnorderedIR(
            table, tuple(table[column_name] for column_name in self._column_names)
        )

    def aggregate(
        self,
        aggregations: typing.Sequence[tuple[ex.Aggregation, str]],
        by_column_ids: typing.Sequence[ex.DerefOp] = (),
        order_by: typing.Sequence[OrderingExpression] = (),
    ) -> UnorderedIR:
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
        bindings = {col: table[col] for col in self.column_ids}
        stats = {
            col_out: agg_compiler.compile_aggregate(
                aggregate,
                bindings,
                order_by=_convert_row_ordering_to_table_values(table, order_by),
            )
            for aggregate, col_out in aggregations
        }
        if by_column_ids:
            result = table.group_by((ref.id.sql for ref in by_column_ids)).aggregate(
                **stats
            )
            return UnorderedIR(
                result, columns=tuple(result[key] for key in result.columns)
            )
        else:
            result = table.aggregate(**stats)
            return UnorderedIR(
                result,
                columns=[result[col_id] for col_id in [*stats.keys()]],
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

    ## Helpers
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

    @classmethod
    def from_polars(
        cls, pa_table: pa.Table, schema: Sequence[bigquery.SchemaField]
    ) -> UnorderedIR:
        """Builds an in-memory only (SQL only) expr from a pyarrow table."""
        import bigframes_vendored.ibis.backends.bigquery.datatypes as third_party_ibis_bqtypes

        # derive the ibis schema from the original pandas schema
        keys_memtable = bigframes_vendored.ibis.memtable(
            pa_table,
            schema=third_party_ibis_bqtypes.BigQuerySchema.to_ibis(list(schema)),
        )
        return cls(
            keys_memtable,
            columns=tuple(keys_memtable[key] for key in keys_memtable.columns),
        )

    def join(
        self: UnorderedIR,
        right: UnorderedIR,
        conditions: tuple[tuple[str, str], ...],
        type: Literal["inner", "outer", "left", "right", "cross"],
        *,
        join_nulls: bool = True,
    ) -> UnorderedIR:
        """Join two expressions by column equality.

        Arguments:
            left: Expression for left table to join.
            left_column_ids: Column IDs (not label) to join by.
            right: Expression for right table to join.
            right_column_ids: Column IDs (not label) to join by.
            how: The type of join to perform.
            join_nulls (bool):
                If True, will joins NULL keys to each other.
        Returns:
            The joined expression. The resulting columns will be, in order,
            first the coalesced join keys, then, all the left columns, and
            finally, all the right columns.
        """
        # Shouldn't need to select the column ids explicitly, but it seems that ibis has some
        # bug resolving column ids otherwise, potentially because of the "JoinChain" op
        left_table = self._to_ibis_expr().select(self.column_ids)
        right_table = right._to_ibis_expr().select(right.column_ids)

        join_conditions = [
            _join_condition(
                left_table[left_index], right_table[right_index], nullsafe=join_nulls
            )
            for left_index, right_index in conditions
        ]

        combined_table = bigframes_vendored.ibis.join(
            left_table,
            right_table,
            predicates=join_conditions,
            how=type,  # type: ignore
        )
        columns = [combined_table[col.get_name()] for col in self.columns] + [
            combined_table[col.get_name()] for col in right.columns
        ]
        return UnorderedIR(
            combined_table,
            columns=columns,
        )

    def isin_join(
        self: UnorderedIR,
        right: UnorderedIR,
        indicator_col: str,
        conditions: tuple[str, str],
        *,
        join_nulls: bool = True,
    ) -> UnorderedIR:
        """Join two expressions by column equality.

        Arguments:
            left: Expression for left table to join.
            right: Expression for right table to join.
            conditions: Id pairs to compare
        Returns:
            The joined expression.
        """
        left_table = self._to_ibis_expr()
        right_table = right._to_ibis_expr()
        if join_nulls:  # nullsafe isin join must actually use "exists" subquery
            new_column = (
                (
                    _join_condition(
                        left_table[conditions[0]],
                        right_table[conditions[1]],
                        nullsafe=True,
                    )
                )
                .any()
                .name(indicator_col)
            )

        else:  # Can do simpler "in" subquery
            new_column = (
                (left_table[conditions[0]])
                .isin((right_table[conditions[1]]))
                .name(indicator_col)
            )

        columns = tuple(
            itertools.chain(
                (left_table[col.get_name()] for col in self.columns), (new_column,)
            )
        )

        return UnorderedIR(
            left_table,
            columns=columns,
        )

    def project_window_op(
        self,
        expression: ex.Aggregation,
        window_spec: WindowSpec,
        output_name: str,
        *,
        never_skip_nulls=False,
    ) -> UnorderedIR:
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
            map(
                ex.DerefOp,
                itertools.chain(
                    expression.column_references, window_spec.all_referenced_columns
                ),
            ),
        )
        can_directly_window = not any(
            map(lambda x: is_literal(x) or is_window(x), used_exprs)
        )
        if not can_directly_window:
            return self._reproject_to_table().project_window_op(
                expression,
                window_spec,
                output_name,
                never_skip_nulls=never_skip_nulls,
            )

        if expression.op.order_independent and window_spec.is_unbounded:
            # notably percentile_cont does not support ordering clause
            window_spec = window_spec.without_order()
        window = self._ibis_window_from_spec(window_spec)
        bindings = {col: self._get_ibis_column(col) for col in self.column_ids}

        window_op = agg_compiler.compile_analytic(
            expression,
            window,
            bindings=bindings,
        )

        inputs = tuple(
            typing.cast(ibis_types.Column, self._compile_expression(ex.DerefOp(column)))
            for column in expression.column_references
        )
        clauses = []
        if expression.op.skips_nulls and not never_skip_nulls:
            for column in inputs:
                clauses.append((column.isnull(), ibis_types.null()))
        if window_spec.min_periods and len(inputs) > 0:
            if expression.op.skips_nulls:
                # Most operations do not count NULL values towards min_periods
                per_col_does_count = (column.notnull() for column in inputs)
                # All inputs must be non-null for observation to count
                is_observation = functools.reduce(
                    lambda x, y: x & y, per_col_does_count
                ).cast(int)
                observation_count = agg_compiler.compile_analytic(
                    ex.UnaryAggregation(agg_ops.sum_op, ex.deref("_observation_count")),
                    window,
                    bindings={"_observation_count": is_observation},
                )
            else:
                # Operations like count treat even NULLs as valid observations for the sake of min_periods
                # notnull is just used to convert null values to non-null (FALSE) values to be counted
                is_observation = inputs[0].notnull()
                observation_count = agg_compiler.compile_analytic(
                    ex.UnaryAggregation(
                        agg_ops.count_op, ex.deref("_observation_count")
                    ),
                    window,
                    bindings={"_observation_count": is_observation},
                )
            clauses.append(
                (
                    observation_count < ibis_types.literal(window_spec.min_periods),
                    ibis_types.null(),
                )
            )
        if clauses:
            case_statement = bigframes_vendored.ibis.case()
            for clause in clauses:
                case_statement = case_statement.when(clause[0], clause[1])
            case_statement = case_statement.else_(window_op).end()  # type: ignore
            window_op = case_statement  # type: ignore

        return UnorderedIR(self._table, (*self.columns, window_op.name(output_name)))

    def _compile_expression(self, expr: ex.Expression):
        return op_compiler.compile_expression(expr, self._ibis_bindings)

    def _ibis_window_from_spec(self, window_spec: WindowSpec):
        group_by: typing.List[ibis_types.Value] = (
            [
                typing.cast(
                    ibis_types.Column, _as_groupable(self._compile_expression(column))
                )
                for column in window_spec.grouping_keys
            ]
            if window_spec.grouping_keys
            else []
        )

        # Construct ordering. There are basically 3 main cases
        # 1. Order-independent op (aggregation, cut, rank) with unbound window - no ordering clause needed
        # 2. Order-independent op (aggregation, cut, rank) with range window - use ordering clause, ties allowed
        # 3. Order-depedenpent op (navigation functions, array_agg) or rows bounds - use total row order to break ties.
        if window_spec.is_row_bounded:
            if not window_spec.ordering:
                # If window spec has following or preceding bounds, we need to apply an unambiguous ordering.
                raise ValueError("No ordering provided for ordered analytic function")
            order_by = _convert_row_ordering_to_table_values(
                self._column_names,
                window_spec.ordering,
            )

        elif window_spec.is_range_bounded:
            order_by = [
                _convert_range_ordering_to_table_value(
                    self._column_names,
                    window_spec.ordering[0],
                )
            ]
        # The rest if branches are for unbounded windows
        elif window_spec.ordering:
            # Unbound grouping window. Suitable for aggregations but not for analytic function application.
            order_by = _convert_row_ordering_to_table_values(
                self._column_names,
                window_spec.ordering,
            )
        else:
            order_by = None

        window = bigframes_vendored.ibis.window(order_by=order_by, group_by=group_by)
        if window_spec.bounds is not None:
            return _add_boundary(window_spec.bounds, window)
        return window


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


def _convert_row_ordering_to_table_values(
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
            bigframes_vendored.ibis.asc(expr)  # type: ignore
            if ordering_col.direction.is_ascending
            else bigframes_vendored.ibis.desc(expr)  # type: ignore
        )
        # Bigquery SQL considers NULLS to be "smallest" values, but we need to override in these cases.
        if (not ordering_col.na_last) and (not ordering_col.direction.is_ascending):
            # Force nulls to be first
            is_null_val = typing.cast(ibis_types.Column, expr.isnull())
            ordering_values.append(bigframes_vendored.ibis.desc(is_null_val))
        elif (ordering_col.na_last) and (ordering_col.direction.is_ascending):
            # Force nulls to be last
            is_null_val = typing.cast(ibis_types.Column, expr.isnull())
            ordering_values.append(bigframes_vendored.ibis.asc(is_null_val))
        ordering_values.append(ordering_value)
    return ordering_values


def _convert_range_ordering_to_table_value(
    value_lookup: typing.Mapping[str, ibis_types.Value],
    ordering_column: OrderingExpression,
) -> ibis_types.Value:
    """Converts the ordering for range windows to Ibis references.

    Note that this method is different from `_convert_row_ordering_to_table_values` in
    that it does not arrange null values. There are two reasons:
    1. Manipulating null positions requires more than one ordering key, which is forbidden
       by SQL window syntax for range rolling.
    2. Pandas does not allow range rolling on timeseries with nulls.

    Therefore, we opt for the simplest approach here: generate the simplest SQL and follow
    the BigQuery engine behavior.
    """
    expr = op_compiler.compile_expression(
        ordering_column.scalar_expression, value_lookup
    )

    if ordering_column.direction.is_ascending:
        return bigframes_vendored.ibis.asc(expr)  # type: ignore
    return bigframes_vendored.ibis.desc(expr)  # type: ignore


def _string_cast_join_cond(
    lvalue: ibis_types.Column, rvalue: ibis_types.Column
) -> ibis_types.BooleanColumn:
    result = (
        lvalue.cast(ibis_dtypes.str).fill_null(ibis_types.literal("0"))
        == rvalue.cast(ibis_dtypes.str).fill_null(ibis_types.literal("0"))
    ) & (
        lvalue.cast(ibis_dtypes.str).fill_null(ibis_types.literal("1"))
        == rvalue.cast(ibis_dtypes.str).fill_null(ibis_types.literal("1"))
    )
    return typing.cast(ibis_types.BooleanColumn, result)


def _numeric_join_cond(
    lvalue: ibis_types.Column, rvalue: ibis_types.Column
) -> ibis_types.BooleanColumn:
    lvalue1 = lvalue.fill_null(ibis_types.literal(0))
    lvalue2 = lvalue.fill_null(ibis_types.literal(1))
    rvalue1 = rvalue.fill_null(ibis_types.literal(0))
    rvalue2 = rvalue.fill_null(ibis_types.literal(1))
    if lvalue.type().is_floating() and rvalue.type().is_floating():
        # NaN aren't equal so need to coalesce as well with diff constants
        lvalue1 = (
            typing.cast(ibis_types.FloatingColumn, lvalue)
            .isnan()
            .ifelse(ibis_types.literal(2), lvalue1)
        )
        lvalue2 = (
            typing.cast(ibis_types.FloatingColumn, lvalue)
            .isnan()
            .ifelse(ibis_types.literal(3), lvalue2)
        )
        rvalue1 = (
            typing.cast(ibis_types.FloatingColumn, rvalue)
            .isnan()
            .ifelse(ibis_types.literal(2), rvalue1)
        )
        rvalue2 = (
            typing.cast(ibis_types.FloatingColumn, rvalue)
            .isnan()
            .ifelse(ibis_types.literal(3), rvalue2)
        )
    result = (lvalue1 == rvalue1) & (lvalue2 == rvalue2)
    return typing.cast(ibis_types.BooleanColumn, result)


def _join_condition(
    lvalue: ibis_types.Column, rvalue: ibis_types.Column, nullsafe: bool
) -> ibis_types.BooleanColumn:
    if (lvalue.type().is_floating()) and (lvalue.type().is_floating()):
        # Need to always make safe join condition to handle nan, even if no nulls
        return _numeric_join_cond(lvalue, rvalue)
    if nullsafe:
        # TODO: Define more coalesce constants for non-numeric types to avoid cast
        if (lvalue.type().is_numeric()) and (lvalue.type().is_numeric()):
            return _numeric_join_cond(lvalue, rvalue)
        else:
            return _string_cast_join_cond(lvalue, rvalue)
    return typing.cast(ibis_types.BooleanColumn, lvalue == rvalue)


def _as_groupable(value: ibis_types.Value):
    # Some types need to be converted to another type to enable groupby
    if value.type().is_float64():
        return value.cast(ibis_dtypes.str)
    elif value.type().is_geospatial():
        return typing.cast(ibis_types.GeoSpatialColumn, value).as_binary()
    elif value.type().is_json():
        return scalar_op_compiler.to_json_string(value)
    else:
        return value


def _to_ibis_boundary(
    boundary: Optional[int],
) -> Optional[ibis_expr_window.WindowBoundary]:
    if boundary is None:
        return None
    return ibis_expr_window.WindowBoundary(
        abs(boundary), preceding=boundary <= 0  # type:ignore
    )


def _add_boundary(
    bounds: typing.Union[RowsWindowBounds, RangeWindowBounds],
    ibis_window: ibis_expr_builders.LegacyWindowBuilder,
) -> ibis_expr_builders.LegacyWindowBuilder:
    if isinstance(bounds, RangeWindowBounds):
        return ibis_window.range(
            start=_to_ibis_boundary(
                None
                if bounds.start is None
                else utils.timedelta_to_micros(bounds.start)
            ),
            end=_to_ibis_boundary(
                None if bounds.end is None else utils.timedelta_to_micros(bounds.end)
            ),
        )
    if isinstance(bounds, RowsWindowBounds):
        if bounds.start is not None or bounds.end is not None:
            return ibis_window.rows(
                start=_to_ibis_boundary(bounds.start),
                end=_to_ibis_boundary(bounds.end),
            )
        return ibis_window
    else:
        raise ValueError(f"unrecognized window bounds {bounds}")
