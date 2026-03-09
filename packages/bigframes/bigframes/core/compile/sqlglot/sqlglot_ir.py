# Copyright 2025 Google LLC
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
import datetime
import functools
import typing

import bigframes_vendored.sqlglot as sg
import bigframes_vendored.sqlglot.expressions as sge
import pyarrow as pa

from bigframes import dtypes
from bigframes.core import guid, local_data, schema
from bigframes.core.compile.sqlglot import sql
from bigframes.core.compile.sqlglot.expressions import typed_expr
import bigframes.core.compile.sqlglot.sqlglot_types as sgt

# shapely.wkt.dumps was moved to shapely.io.to_wkt in 2.0.
try:
    from shapely.io import to_wkt  # type: ignore
except ImportError:
    from shapely.wkt import dumps  # type: ignore

    to_wkt = dumps


@dataclasses.dataclass(frozen=True)
class SQLGlotIR:
    """Helper class to build SQLGlot Query and generate SQL string."""

    expr: typing.Union[sge.Select, sge.Table] = sg.select()
    """The SQLGlot expression representing the query."""

    uid_gen: guid.SequentialUIDGenerator = guid.SequentialUIDGenerator()
    """Generator for unique identifiers."""

    @property
    def sql(self) -> str:
        """Generate SQL string from the given expression."""
        return sql.to_sql(self.expr)

    @classmethod
    def from_pyarrow(
        cls,
        pa_table: pa.Table,
        schema: schema.ArraySchema,
        uid_gen: guid.SequentialUIDGenerator,
    ) -> SQLGlotIR:
        """Builds SQLGlot expression from a pyarrow table.

        This is used to represent in-memory data as a SQL query.
        """
        dtype_expr = sge.DataType(
            this=sge.DataType.Type.STRUCT,
            expressions=[
                sge.ColumnDef(
                    this=sge.to_identifier(field.column, quoted=True),
                    kind=sgt.from_bigframes_dtype(field.dtype),
                )
                for field in schema.items
            ],
            nested=True,
        )
        data_expr = [
            sge.Struct(
                expressions=tuple(
                    sql.literal(
                        value=value,
                        dtype=field.dtype,
                    )
                    for value, field in zip(tuple(row_dict.values()), schema.items)
                )
            )
            for row_dict in local_data._iter_table(pa_table, schema)
        ]
        expr = sge.Unnest(
            expressions=[
                sge.DataType(
                    this=sge.DataType.Type.ARRAY,
                    expressions=[dtype_expr],
                    nested=True,
                    values=data_expr,
                ),
            ],
        )
        return cls(expr=sg.select(sge.Star()).from_(expr), uid_gen=uid_gen)

    @classmethod
    def from_table(
        cls,
        project_id: str,
        dataset_id: str,
        table_id: str,
        uid_gen: guid.SequentialUIDGenerator,
        sql_predicate: typing.Optional[str] = None,
        system_time: typing.Optional[datetime.datetime] = None,
    ) -> SQLGlotIR:
        """Builds a SQLGlotIR expression from a BigQuery table.

        Args:
            project_id (str): The project ID of the BigQuery table.
            dataset_id (str): The dataset ID of the BigQuery table.
            table_id (str): The table ID of the BigQuery table.
            col_names (typing.Sequence[str]): The names of the columns to select.
            alias_names (typing.Sequence[str]): The aliases for the selected columns.
            uid_gen (guid.SequentialUIDGenerator): A generator for unique identifiers.
            sql_predicate (typing.Optional[str]): An optional SQL predicate for filtering.
            system_time (typing.Optional[str]): An optional system time for time-travel queries.
        """
        version = (
            sge.Version(
                this=sge.Identifier(this="SYSTEM_TIME", quoted=False),
                expression=sge.Literal.string(system_time.isoformat()),
                kind="AS OF",
            )
            if system_time
            else None
        )
        table_alias = next(uid_gen.get_uid_stream("bft_"))
        table_expr = sge.Table(
            this=sql.identifier(table_id),
            db=sql.identifier(dataset_id),
            catalog=sql.identifier(project_id),
            version=version,
            alias=sql.identifier(table_alias),
        )
        if sql_predicate:
            select_expr = sge.Select().select(sge.Star()).from_(table_expr)
            select_expr = select_expr.where(
                sg.parse_one(sql_predicate, dialect=sql.base.DIALECT), append=False
            )
            return cls(expr=select_expr, uid_gen=uid_gen)

        return cls(expr=table_expr, uid_gen=uid_gen)

    def select(
        self,
        selections: tuple[tuple[str, sge.Expression], ...] = (),
        predicates: tuple[sge.Expression, ...] = (),
        sorting: tuple[sge.Ordered, ...] = (),
        limit: typing.Optional[int] = None,
    ) -> SQLGlotIR:
        # TODO: Explicitly insert CTEs into plan
        if isinstance(self.expr, sge.Select):
            new_expr, _ = self._select_to_cte()
        else:
            new_expr = sge.Select().from_(self.expr)

        if len(sorting) > 0:
            new_expr = new_expr.order_by(*sorting)

        if len(selections) > 0:
            to_select = [
                sge.Alias(
                    this=expr,
                    alias=sql.identifier(id),
                )
                if expr.alias_or_name != id
                else expr
                for id, expr in selections
            ]
            new_expr = new_expr.select(*to_select, append=False)
        else:
            new_expr = new_expr.select(sge.Star(), append=False)

        if len(predicates) > 0:
            condition = _and(predicates)
            new_expr = new_expr.where(condition, append=False)
        if limit is not None:
            new_expr = new_expr.limit(limit)

        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    @classmethod
    def from_unparsed_query(
        cls,
        query_string: str,
    ) -> SQLGlotIR:
        """Builds a SQLGlot expression from a query string. Wrapping the query
        in a CTE can avoid the query parsing issue for unsupported syntax in
        SQLGlot."""
        uid_gen: guid.SequentialUIDGenerator = guid.SequentialUIDGenerator()
        cte_name = sql.identifier(next(uid_gen.get_uid_stream("bfcte_")))
        cte = sge.CTE(
            this=query_string,
            alias=cte_name,
        )
        select_expr = sge.Select().select(sge.Star()).from_(sge.Table(this=cte_name))
        select_expr = _set_query_ctes(select_expr, [cte])
        return cls(expr=select_expr, uid_gen=uid_gen)

    @classmethod
    def from_union(
        cls,
        selects: typing.Sequence[sge.Select],
        output_aliases: typing.Sequence[typing.Tuple[str, str]],
        uid_gen: guid.SequentialUIDGenerator,
    ) -> SQLGlotIR:
        """Builds a SQLGlot expression by unioning of multiple select expressions."""
        assert (
            len(list(selects)) >= 2
        ), f"At least two select expressions must be provided, but got {selects}."

        existing_ctes: list[sge.CTE] = []
        union_selects: list[sge.Select] = []
        for select in selects:
            assert isinstance(
                select, sge.Select
            ), f"All provided expressions must be of type sge.Select, but got {type(select)}"

            select_expr = select.copy()
            select_expr, select_ctes = _pop_query_ctes(select_expr)
            existing_ctes = _merge_ctes(existing_ctes, select_ctes)
            union_selects.append(select_expr)

        union_expr: sge.Query = union_selects[0].subquery()
        for select in union_selects[1:]:
            union_expr = sge.Union(
                this=union_expr,
                expression=select.subquery(),
                distinct=False,
                copy=False,
            )

        selections = [
            sge.Alias(
                this=sql.identifier(old_name),
                alias=sql.identifier(new_name),
            )
            for old_name, new_name in output_aliases
        ]
        final_select_expr = (
            sge.Select().select(*selections).from_(union_expr.subquery())
        )
        final_select_expr = _set_query_ctes(final_select_expr, existing_ctes)
        return cls(expr=final_select_expr, uid_gen=uid_gen)

    def join(
        self,
        right: SQLGlotIR,
        join_type: typing.Literal["inner", "outer", "left", "right", "cross"],
        conditions: tuple[tuple[typed_expr.TypedExpr, typed_expr.TypedExpr], ...],
        *,
        joins_nulls: bool = True,
    ) -> SQLGlotIR:
        """Joins the current query with another SQLGlotIR instance."""
        left_select, left_cte_name = self._select_to_cte()
        right_select, right_cte_name = right._select_to_cte()

        left_select, left_ctes = _pop_query_ctes(left_select)
        right_select, right_ctes = _pop_query_ctes(right_select)
        merged_ctes = _merge_ctes(left_ctes, right_ctes)

        join_on = _and(
            tuple(
                _join_condition(left, right, joins_nulls) for left, right in conditions
            )
        )

        join_type_str = join_type if join_type != "outer" else "full outer"
        new_expr = (
            sge.Select()
            .select(sge.Star())
            .from_(sge.Table(this=left_cte_name))
            .join(sge.Table(this=right_cte_name), on=join_on, join_type=join_type_str)
        )
        new_expr = _set_query_ctes(new_expr, merged_ctes)

        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def isin_join(
        self,
        right: SQLGlotIR,
        indicator_col: str,
        conditions: tuple[typed_expr.TypedExpr, typed_expr.TypedExpr],
        joins_nulls: bool = True,
    ) -> SQLGlotIR:
        """Joins the current query with another SQLGlotIR instance."""
        left_select, left_cte_name = self._select_to_cte()
        # Prefer subquery over CTE for the IN clause's right side to improve SQL readability.
        right_select = right._as_select()

        left_select, left_ctes = _pop_query_ctes(left_select)
        right_select, right_ctes = _pop_query_ctes(right_select)
        merged_ctes = _merge_ctes(left_ctes, right_ctes)

        left_condition = typed_expr.TypedExpr(
            sge.Column(this=conditions[0].expr, table=left_cte_name),
            conditions[0].dtype,
        )

        new_column: sge.Expression
        if joins_nulls:
            right_table_name = sql.identifier(next(self.uid_gen.get_uid_stream("bft_")))
            right_condition = typed_expr.TypedExpr(
                sge.Column(this=conditions[1].expr, table=right_table_name),
                conditions[1].dtype,
            )
            new_column = sge.Exists(
                this=sge.Select()
                .select(sge.convert(1))
                .from_(sge.Alias(this=right_select.subquery(), alias=right_table_name))
                .where(
                    _join_condition(left_condition, right_condition, joins_nulls=True)
                )
            )
        else:
            new_column = sge.In(
                this=left_condition.expr,
                expressions=[right_select.subquery()],
            )

        new_column = sge.Alias(
            this=new_column,
            alias=sql.identifier(indicator_col),
        )

        new_expr = (
            sge.Select()
            .select(sge.Column(this=sge.Star(), table=left_cte_name), new_column)
            .from_(sge.Table(this=left_cte_name))
        )
        new_expr = _set_query_ctes(new_expr, merged_ctes)

        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def explode(
        self,
        column_names: tuple[str, ...],
        offsets_col: typing.Optional[str],
    ) -> SQLGlotIR:
        """Unnests one or more array columns."""
        num_columns = len(list(column_names))
        assert num_columns > 0, "At least one column must be provided for explode."
        if num_columns == 1:
            return self._explode_single_column(column_names[0], offsets_col)
        else:
            return self._explode_multiple_columns(column_names, offsets_col)

    def sample(self, fraction: float) -> SQLGlotIR:
        """Uniform samples a fraction of the rows."""
        condition = sge.LT(
            this=sge.func("RAND"),
            expression=sql.literal(fraction, dtypes.FLOAT_DTYPE),
        )

        new_expr = self._select_to_cte()[0].where(condition, append=False)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def aggregate(
        self,
        aggregations: tuple[tuple[str, sge.Expression], ...],
        by_cols: tuple[sge.Expression, ...],
        dropna_cols: tuple[sge.Expression, ...],
    ) -> SQLGlotIR:
        """Applies the aggregation expressions.

        Args:
            aggregations: output_column_id, aggregation_expr tuples
            by_cols: column expressions for aggregation
            dropna_cols: columns whether null keys should be dropped
        """
        aggregations_expr = [
            sge.Alias(
                this=expr,
                alias=sql.identifier(id),
            )
            for id, expr in aggregations
        ]

        new_expr, _ = self._select_to_cte()
        new_expr = new_expr.group_by(*by_cols).select(
            *[*by_cols, *aggregations_expr], append=False
        )

        condition = _and(
            tuple(
                sg.not_(sge.Is(this=drop_col, expression=sge.Null()))
                for drop_col in dropna_cols
            )
        )
        if condition is not None:
            new_expr = new_expr.where(condition, append=False)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def resample(
        self,
        right: SQLGlotIR,
        array_col_name: str,
        start_expr: sge.Expression,
        stop_expr: sge.Expression,
        step_expr: sge.Expression,
    ) -> SQLGlotIR:
        # Get identifier for left and right by pushing them to CTEs
        left_select, left_id = self._select_to_cte()
        right_select, right_id = right._select_to_cte()

        # Extract all CTEs from the returned select expressions
        _, left_ctes = _pop_query_ctes(left_select)
        _, right_ctes = _pop_query_ctes(right_select)
        merged_ctes = _merge_ctes(left_ctes, right_ctes)

        generate_array = sge.func("GENERATE_ARRAY", start_expr, stop_expr, step_expr)

        unnested_column_alias = sql.identifier(
            next(self.uid_gen.get_uid_stream("bfcol_"))
        )
        unnest_expr = sge.Unnest(
            expressions=[generate_array],
            alias=sge.TableAlias(columns=[unnested_column_alias]),
        )

        final_col_id = sql.identifier(array_col_name)

        # Build final expression by joining everything directly in a single SELECT
        new_expr = (
            sge.Select()
            .select(unnested_column_alias.as_(final_col_id))
            .from_(sge.Table(this=left_id))
            .join(sge.Table(this=right_id), join_type="cross")
            .join(unnest_expr, join_type="cross")
        )
        new_expr = _set_query_ctes(new_expr, merged_ctes)

        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def _explode_single_column(
        self, column_name: str, offsets_col: typing.Optional[str]
    ) -> SQLGlotIR:
        """Helper method to handle the case of exploding a single column."""
        offset = sql.identifier(offsets_col) if offsets_col else None
        column = sql.identifier(column_name)
        unnested_column_alias = sql.identifier(
            next(self.uid_gen.get_uid_stream("bfcol_"))
        )
        unnest_expr = sge.Unnest(
            expressions=[column],
            alias=sge.TableAlias(columns=[unnested_column_alias]),
            offset=offset,
        )
        selection = sge.Star(replace=[unnested_column_alias.as_(column)])

        new_expr, _ = self._select_to_cte()
        # Use LEFT JOIN to preserve rows when unnesting empty arrays.
        new_expr = new_expr.select(selection, append=False).join(
            unnest_expr, join_type="LEFT"
        )
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def _explode_multiple_columns(
        self,
        column_names: tuple[str, ...],
        offsets_col: typing.Optional[str],
    ) -> SQLGlotIR:
        """Helper method to handle the case of exploding multiple columns."""
        offset = sql.identifier(offsets_col) if offsets_col else None
        columns = [sql.identifier(column_name) for column_name in column_names]

        # If there are multiple columns, we need to unnest by zipping the arrays:
        # https://cloud.google.com/bigquery/docs/arrays#zipping_arrays
        column_lengths = [sge.func("ARRAY_LENGTH", column) - 1 for column in columns]
        generate_array = sge.func(
            "GENERATE_ARRAY",
            sge.convert(0),
            sge.func("LEAST", *column_lengths),
        )
        unnested_offset_alias = sql.identifier(
            next(self.uid_gen.get_uid_stream("bfcol_"))
        )
        unnest_expr = sge.Unnest(
            expressions=[generate_array],
            alias=sge.TableAlias(columns=[unnested_offset_alias]),
            offset=offset,
        )
        selection = sge.Star(
            replace=[
                sge.Bracket(
                    this=column,
                    expressions=[unnested_offset_alias],
                    safe=True,
                    offset=False,
                ).as_(column)
                for column in columns
            ]
        )
        new_expr, _ = self._select_to_cte()
        # Use LEFT JOIN to preserve rows when unnesting empty arrays.
        new_expr = new_expr.select(selection, append=False).join(
            unnest_expr, join_type="LEFT"
        )
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def _as_select(self) -> sge.Select:
        if isinstance(self.expr, sge.Select):
            return self.expr
        else:  # table
            return sge.Select().from_(self.expr)

    def _as_subquery(self) -> sge.Subquery:
        return self._as_select().subquery()

    def _select_to_cte(self) -> tuple[sge.Select, sge.Identifier]:
        """Transforms a given sge.Select query by pushing its main SELECT statement
        into a new CTE and then generates a 'SELECT * FROM new_cte_name'
        for the new query."""
        cte_name = sql.identifier(next(self.uid_gen.get_uid_stream("bfcte_")))
        select_expr = self._as_select().copy()
        select_expr, existing_ctes = _pop_query_ctes(select_expr)
        new_cte = sge.CTE(
            this=select_expr,
            alias=cte_name,
        )
        new_select_expr = (
            sge.Select().select(sge.Star()).from_(sge.Table(this=cte_name))
        )
        new_select_expr = _set_query_ctes(new_select_expr, [*existing_ctes, new_cte])
        return new_select_expr, cte_name


def _and(conditions: tuple[sge.Expression, ...]) -> typing.Optional[sge.Expression]:
    """Chains multiple expressions together using a logical AND."""
    if not conditions:
        return None

    return functools.reduce(
        lambda left, right: sge.And(this=left, expression=right), conditions
    )


def _join_condition(
    left: typed_expr.TypedExpr,
    right: typed_expr.TypedExpr,
    joins_nulls: bool,
) -> typing.Union[sge.EQ, sge.And]:
    """Generates a join condition to match pandas's null-handling logic.

    Pandas treats null values as distinct from each other, leading to a
    cross-join-like behavior for null keys. In contrast, BigQuery SQL treats
    null values as equal, leading to a inner-join-like behavior.

    This function generates the appropriate SQL condition to replicate the
    desired pandas behavior in BigQuery.

    Args:
        left: The left-side join key.
        right: The right-side join key.
        joins_nulls: If True, generates complex logic to handle nulls/NaNs.
            Otherwise, uses a simple equality check where appropriate.
    """
    is_floating_types = (
        left.dtype == dtypes.FLOAT_DTYPE and right.dtype == dtypes.FLOAT_DTYPE
    )
    if not is_floating_types and not joins_nulls:
        return sge.EQ(this=left.expr, expression=right.expr)

    is_numeric_types = dtypes.is_numeric(
        left.dtype, include_bool=False
    ) and dtypes.is_numeric(right.dtype, include_bool=False)
    if is_numeric_types:
        return _join_condition_for_numeric(left, right)
    else:
        return _join_condition_for_others(left, right)


def _join_condition_for_others(
    left: typed_expr.TypedExpr,
    right: typed_expr.TypedExpr,
) -> sge.And:
    """Generates a join condition for non-numeric types to match pandas's
    null-handling logic.
    """
    left_str = sql.cast(left.expr, "STRING")
    right_str = sql.cast(right.expr, "STRING")
    left_0 = sge.func("COALESCE", left_str, sql.literal("0", dtypes.STRING_DTYPE))
    left_1 = sge.func("COALESCE", left_str, sql.literal("1", dtypes.STRING_DTYPE))
    right_0 = sge.func("COALESCE", right_str, sql.literal("0", dtypes.STRING_DTYPE))
    right_1 = sge.func("COALESCE", right_str, sql.literal("1", dtypes.STRING_DTYPE))
    return sge.And(
        this=sge.EQ(this=left_0, expression=right_0),
        expression=sge.EQ(this=left_1, expression=right_1),
    )


def _join_condition_for_numeric(
    left: typed_expr.TypedExpr,
    right: typed_expr.TypedExpr,
) -> sge.And:
    """Generates a join condition for non-numeric types to match pandas's
    null-handling logic. Specifically for FLOAT types, Pandas treats NaN aren't
    equal so need to coalesce as well with different constants.
    """
    is_floating_types = (
        left.dtype == dtypes.FLOAT_DTYPE and right.dtype == dtypes.FLOAT_DTYPE
    )
    left_0 = sge.func("COALESCE", left.expr, sql.literal(0, left.dtype))
    left_1 = sge.func("COALESCE", left.expr, sql.literal(1, left.dtype))
    right_0 = sge.func("COALESCE", right.expr, sql.literal(0, right.dtype))
    right_1 = sge.func("COALESCE", right.expr, sql.literal(1, right.dtype))
    if not is_floating_types:
        return sge.And(
            this=sge.EQ(this=left_0, expression=right_0),
            expression=sge.EQ(this=left_1, expression=right_1),
        )

    left_2 = sge.If(
        this=sge.IsNan(this=left.expr), true=sql.literal(2, left.dtype), false=left_0
    )
    left_3 = sge.If(
        this=sge.IsNan(this=left.expr), true=sql.literal(3, left.dtype), false=left_1
    )
    right_2 = sge.If(
        this=sge.IsNan(this=right.expr), true=sql.literal(2, right.dtype), false=right_0
    )
    right_3 = sge.If(
        this=sge.IsNan(this=right.expr), true=sql.literal(3, right.dtype), false=right_1
    )
    return sge.And(
        this=sge.EQ(this=left_2, expression=right_2),
        expression=sge.EQ(this=left_3, expression=right_3),
    )


def _set_query_ctes(
    expr: sge.Select,
    ctes: list[sge.CTE],
) -> sge.Select:
    """Sets the CTEs of a given sge.Select expression."""
    new_expr = expr.copy()
    with_expr = sge.With(expressions=ctes) if len(ctes) > 0 else None

    if "with" in new_expr.arg_types.keys():
        new_expr.set("with", with_expr)
    elif "with_" in new_expr.arg_types.keys():
        new_expr.set("with_", with_expr)
    else:
        raise ValueError("The expression does not support CTEs.")
    return new_expr


def _merge_ctes(ctes1: list[sge.CTE], ctes2: list[sge.CTE]) -> list[sge.CTE]:
    """Merges two lists of CTEs, de-duplicating by alias name."""
    seen = {cte.alias: cte for cte in ctes1}
    for cte in ctes2:
        if cte.alias not in seen:
            seen[cte.alias] = cte
    return list(seen.values())


def _pop_query_ctes(
    expr: sge.Select,
) -> tuple[sge.Select, list[sge.CTE]]:
    """Pops the CTEs of a given sge.Select expression."""
    if "with" in expr.arg_types.keys():
        expr_ctes = expr.args.pop("with", [])
        return expr, expr_ctes
    elif "with_" in expr.arg_types.keys():
        expr_ctes = expr.args.pop("with_", [])
        return expr, expr_ctes
    else:
        raise ValueError("The expression does not support CTEs.")
