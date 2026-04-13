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

import bigframes.core.compile.sqlglot.sqlglot_types as sgt
from bigframes import dtypes
from bigframes.core import guid, local_data, schema
from bigframes.core.compile.sqlglot import sql
from bigframes.core.compile.sqlglot.expressions import typed_expr

# shapely.wkt.dumps was moved to shapely.io.to_wkt in 2.0.
try:
    from shapely.io import to_wkt  # type: ignore
except ImportError:
    from shapely.wkt import dumps  # type: ignore

    to_wkt = dumps


class SelectFragment:
    def __init__(self, select_expr: sge.Select):
        self.select_expr = select_expr

    def as_select_all(self) -> sge.Select:
        return self.select_expr

    def select(self, *items: sge.Expression) -> sge.Select:
        return sge.Select().select(*items).from_(self.select_expr.subquery())

    def as_from_item(self) -> sge.Expression:
        return self.select_expr.subquery()


class TableFragment:
    def __init__(self, table: sge.Table | sge.Unnest):
        self.table = table

    def as_select_all(self) -> sge.Select:
        return sge.Select().select(sge.Star()).from_(self.table)

    def select(self, *items: sge.Expression) -> sge.Select:
        return sge.Select().select(*items).from_(self.table)

    def as_from_item(self) -> sge.Expression:
        return self.table


class DeferredSelectFragment:
    def __init__(self, select_supplier: typing.Callable[[sge.Select], sge.Select]):
        self.select_supplier = select_supplier

    def as_select_all(self) -> sge.Select:
        return self.select_supplier(sge.Select().select(sge.Star()))

    def select(self, *items: sge.Expression) -> sge.Select:
        return self.select_supplier(sge.Select().select(*items))

    def as_from_item(self) -> sge.Expression:
        return self.select_supplier(sge.Select().select(sge.Star())).subquery()


ExprT = SelectFragment | TableFragment | DeferredSelectFragment


@dataclasses.dataclass(frozen=True)
class SQLGlotIR:
    """Helper class to build SQLGlot Query and generate SQL string."""

    expr: ExprT
    """The SQLGlot expression representing the query."""

    uid_gen: guid.SequentialUIDGenerator = guid.SequentialUIDGenerator()
    """Generator for unique identifiers."""

    @property
    def sql(self) -> str:
        """Generate SQL string from the given expression."""
        return sql.to_sql(self.expr.as_select_all())

    @classmethod
    def empty(
        cls, uid_gen: guid.SequentialUIDGenerator = guid.SequentialUIDGenerator()
    ) -> SQLGlotIR:
        return cls(expr=SelectFragment(sge.select()), uid_gen=uid_gen)

    @classmethod
    def from_expr(
        cls,
        expr: sge.Expression,
        uid_gen: guid.SequentialUIDGenerator = guid.SequentialUIDGenerator(),
    ) -> SQLGlotIR:
        if isinstance(expr, sge.Select):
            return cls(expr=SelectFragment(expr), uid_gen=uid_gen)
        elif isinstance(expr, (sge.Table, sge.Unnest)):
            return cls(expr=TableFragment(expr), uid_gen=uid_gen)
        else:
            raise ValueError(f"Unsupported expression type: {type(expr)}")

    @classmethod
    def from_func(
        cls,
        select_handler: typing.Callable[[sge.Select], sge.Select],
        uid_gen: guid.SequentialUIDGenerator = guid.SequentialUIDGenerator(),
    ):
        return cls(expr=DeferredSelectFragment(select_handler), uid_gen=uid_gen)

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
        return cls.from_expr(expr=expr, uid_gen=uid_gen)

    @classmethod
    def from_table(
        cls,
        project_id: str,
        dataset_id: str,
        table_id: str,
        uid_gen: guid.SequentialUIDGenerator,
        columns: typing.Sequence[str] = (),
        sql_predicate: typing.Optional[str] = None,
        system_time: typing.Optional[datetime.datetime] = None,
    ) -> SQLGlotIR:
        """Builds a SQLGlotIR expression from a BigQuery table.

        Args:
            project_id (str): The project ID of the BigQuery table.
            dataset_id (str): The dataset ID of the BigQuery table.
            table_id (str): The table ID of the BigQuery table.
            uid_gen (guid.SequentialUIDGenerator): A generator for unique identifiers.
            columns (typing.Sequence[str]): The names of the columns to select.
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

        if not columns and not sql_predicate:
            return cls.from_expr(expr=table_expr, uid_gen=uid_gen)

        select_items: list[sge.Expression] = (
            [sge.Column(this=sql.identifier(col), table=sql.identifier(table_alias)) for col in columns]
            if columns
            else [sge.Star()]
        )
        select_expr = sge.Select().select(*select_items).from_(table_expr)

        if sql_predicate:
            select_expr = select_expr.where(
                sg.parse_one(sql_predicate, dialect=sql.base.DIALECT), append=False
            )

        return cls.from_expr(expr=select_expr, uid_gen=uid_gen)

    @classmethod
    def from_cte_ref(
        cls,
        cte_ref: str,
        uid_gen: guid.SequentialUIDGenerator,
    ) -> SQLGlotIR:
        table_expr = sge.Table(
            this=sql.identifier(cte_ref),
        )
        return cls.from_expr(expr=table_expr, uid_gen=uid_gen)

    def select(
        self,
        selections: tuple[tuple[str, sge.Expression], ...] = (),
        predicates: tuple[sge.Expression, ...] = (),
        sorting: tuple[sge.Ordered, ...] = (),
        limit: typing.Optional[int] = None,
    ) -> SQLGlotIR:
        # TODO: Explicitly insert CTEs into plan
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
            new_expr = self.expr.select(*to_select)
        else:
            new_expr = self.expr.as_select_all()

        if len(sorting) > 0:
            new_expr = new_expr.order_by(*sorting)

        if len(predicates) > 0:
            condition = _and(predicates)
            new_expr = new_expr.where(condition, append=False)
        if limit is not None:
            new_expr = new_expr.limit(limit)

        return SQLGlotIR.from_expr(expr=new_expr, uid_gen=self.uid_gen)

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
        return cls.from_expr(expr=select_expr, uid_gen=uid_gen)

    @classmethod
    def from_union(
        cls,
        selects: typing.Sequence[sge.Select],
        output_aliases: typing.Sequence[typing.Tuple[str, str]],
        uid_gen: guid.SequentialUIDGenerator,
    ) -> SQLGlotIR:
        """Builds a SQLGlot expression by unioning of multiple select expressions."""
        assert len(list(selects)) >= 2, (
            f"At least two select expressions must be provided, but got {selects}."
        )
        union_expr: sge.Query = selects[0].subquery()
        for select in selects[1:]:
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
        return cls.from_expr(expr=final_select_expr, uid_gen=uid_gen)

    def join(
        self,
        right: SQLGlotIR,
        join_type: typing.Literal["inner", "outer", "left", "right", "cross"],
        conditions: tuple[tuple[typed_expr.TypedExpr, typed_expr.TypedExpr], ...],
        *,
        joins_nulls: bool = True,
    ) -> SQLGlotIR:
        """Joins the current query with another SQLGlotIR instance."""
        left_from = self.expr.as_from_item()
        right_from = right.expr.as_from_item()

        join_on = _and(
            tuple(
                _join_condition(left, right, joins_nulls) for left, right in conditions
            )
        )

        join_type_str = join_type if join_type != "outer" else "full outer"
        return SQLGlotIR.from_func(
            lambda select: select.from_(left_from).join(
                right_from, on=join_on, join_type=join_type_str
            ),
            uid_gen=self.uid_gen,
        )

    def isin_join(
        self,
        right: SQLGlotIR,
        indicator_col: str,
        conditions: tuple[typed_expr.TypedExpr, typed_expr.TypedExpr],
        joins_nulls: bool = True,
    ) -> SQLGlotIR:
        """Joins the current query with another SQLGlotIR instance."""
        left_from = self.expr.as_from_item()

        new_column: sge.Expression
        if joins_nulls:
            force_float_domain = False
            if (
                conditions[0].dtype == dtypes.FLOAT_DTYPE
                or conditions[1].dtype == dtypes.FLOAT_DTYPE
            ):
                force_float_domain = True
            left_expr1, left_expr2 = _value_to_non_null_identity(
                conditions[0], force_float_domain
            )
            right_expr1, right_expr2 = _value_to_non_null_identity(
                conditions[1], force_float_domain
            )

            # Use EXISTS for better performance.
            # We use COALESCE on both sides in the WHERE clause as requested.
            new_column = sge.Exists(
                this=sge.Select()
                .select(sge.convert(1))
                .from_(right.expr.as_from_item())
                .where(
                    sge.and_(
                        sge.EQ(this=left_expr1, expression=right_expr1),
                        sge.EQ(this=left_expr2, expression=right_expr2),
                    )
                )
            )
        else:
            new_column = sge.In(
                this=conditions[0].expr,
                expressions=[right._as_subquery()],
            )

        new_column = sge.Alias(
            this=new_column,
            alias=sql.identifier(indicator_col),
        )

        new_expr = sge.Select().select(sge.Star(), new_column).from_(left_from)
        return SQLGlotIR.from_expr(expr=new_expr, uid_gen=self.uid_gen)

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

        new_expr = self.expr.as_select_all().where(condition, append=False)
        return SQLGlotIR.from_expr(expr=new_expr, uid_gen=self.uid_gen)

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

        new_expr = self.expr.select(*[*by_cols, *aggregations_expr]).group_by(*by_cols)

        condition = _and(
            tuple(
                sg.not_(sge.Is(this=drop_col, expression=sge.Null()))
                for drop_col in dropna_cols
            )
        )
        if condition is not None:
            new_expr = new_expr.where(condition, append=False)
        return SQLGlotIR.from_expr(expr=new_expr, uid_gen=self.uid_gen)

    def with_ctes(
        self,
        ctes: tuple[tuple[str, SQLGlotIR], ...],
    ) -> SQLGlotIR:
        sge_ctes = [
            sge.CTE(
                this=cte.expr.as_select_all(),
                alias=sql.identifier(cte_name),
            )
            for cte_name, cte in ctes
        ]
        select_expr = _set_query_ctes(self.expr.as_select_all(), sge_ctes)
        return SQLGlotIR.from_expr(expr=select_expr, uid_gen=self.uid_gen)

    def resample(
        self,
        right: SQLGlotIR,
        array_col_name: str,
        start_expr: sge.Expression,
        stop_expr: sge.Expression,
        step_expr: sge.Expression,
    ) -> SQLGlotIR:
        generate_array = sge.func(
            "GENERATE_ARRAY",
            start_expr,
            stop_expr,
            step_expr,
        )

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
            .from_(self.expr.as_from_item())
            .join(right.expr.as_from_item(), join_type="cross")
            .join(unnest_expr, join_type="cross")
        )

        return SQLGlotIR.from_expr(expr=new_expr, uid_gen=self.uid_gen)

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

        # Use LEFT JOIN to preserve rows when unnesting empty arrays.
        new_expr = self.expr.select(selection).join(unnest_expr, join_type="LEFT")
        return SQLGlotIR.from_expr(expr=new_expr, uid_gen=self.uid_gen)

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
        # Use LEFT JOIN to preserve rows when unnesting empty arrays.
        new_expr = self.expr.select(selection).join(unnest_expr, join_type="LEFT")
        return SQLGlotIR.from_expr(expr=new_expr, uid_gen=self.uid_gen)

    def _as_subquery(self) -> sge.Subquery:
        # Sometimes explicitly need a subquery, e.g. for IN expressions.
        return self.expr.as_select_all().subquery()


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
    if not joins_nulls:
        return sge.EQ(this=left.expr, expression=right.expr)

    force_float_domain = False
    if left.dtype == dtypes.FLOAT_DTYPE or right.dtype == dtypes.FLOAT_DTYPE:
        force_float_domain = True
    left_expr1, left_expr2 = _value_to_non_null_identity(left, force_float_domain)
    right_expr1, right_expr2 = _value_to_non_null_identity(right, force_float_domain)
    return sge.And(
        this=sge.EQ(this=left_expr1, expression=right_expr1),
        expression=sge.EQ(this=left_expr2, expression=right_expr2),
    )


def _value_to_non_null_identity(
    value: typed_expr.TypedExpr, force_float_domain: bool = False
) -> tuple[sge.Expression, sge.Expression]:
    # normal_value -> (normal_value, normal_value)
    # null_value -> (0, 1)
    # nan_value -> (2, 3)
    if dtypes.is_numeric(value.dtype, include_bool=False):
        dtype = dtypes.FLOAT_DTYPE if force_float_domain else value.dtype
        expr1 = sge.func(
            "COALESCE", value.expr, sql.literal(0.0 if force_float_domain else 0, dtype)
        )
        expr2 = sge.func(
            "COALESCE", value.expr, sql.literal(1.0 if force_float_domain else 1, dtype)
        )
        if value.dtype == dtypes.FLOAT_DTYPE:
            expr1 = sge.If(
                this=sge.IsNan(this=value.expr),
                true=sql.literal(2.0, value.dtype),
                false=expr1,
            )
            expr2 = sge.If(
                this=sge.IsNan(this=value.expr),
                true=sql.literal(3, value.dtype),
                false=expr2,
            )
    else:  # general case, convert to string and coalesce
        expr1 = sge.func(
            "COALESCE",
            sql.cast(value.expr, "STRING"),
            sql.literal("0", dtypes.STRING_DTYPE),
        )
        expr2 = sge.func(
            "COALESCE",
            sql.cast(value.expr, "STRING"),
            sql.literal("1", dtypes.STRING_DTYPE),
        )
    return expr1, expr2


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
