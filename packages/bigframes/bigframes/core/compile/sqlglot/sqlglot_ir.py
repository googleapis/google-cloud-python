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
import typing

from google.cloud import bigquery
import numpy as np
import pyarrow as pa
import sqlglot as sg
import sqlglot.dialects.bigquery
import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes.core import guid, utils
from bigframes.core.compile.sqlglot.expressions import typed_expr
import bigframes.core.compile.sqlglot.sqlglot_types as sgt
import bigframes.core.local_data as local_data
import bigframes.core.schema as bf_schema

# shapely.wkt.dumps was moved to shapely.io.to_wkt in 2.0.
try:
    from shapely.io import to_wkt  # type: ignore
except ImportError:
    from shapely.wkt import dumps  # type: ignore

    to_wkt = dumps


@dataclasses.dataclass(frozen=True)
class SQLGlotIR:
    """Helper class to build SQLGlot Query and generate SQL string."""

    expr: sge.Select = sg.select()
    """The SQLGlot expression representing the query."""

    dialect = sqlglot.dialects.bigquery.BigQuery
    """The SQL dialect used for generation."""

    quoted: bool = True
    """Whether to quote identifiers in the generated SQL."""

    pretty: bool = True
    """Whether to pretty-print the generated SQL."""

    uid_gen: guid.SequentialUIDGenerator = guid.SequentialUIDGenerator()
    """Generator for unique identifiers."""

    @property
    def sql(self) -> str:
        """Generate SQL string from the given expression."""
        return self.expr.sql(dialect=self.dialect, pretty=self.pretty)

    @classmethod
    def from_pyarrow(
        cls,
        pa_table: pa.Table,
        schema: bf_schema.ArraySchema,
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
                    kind=sgt.SQLGlotType.from_bigframes_dtype(field.dtype),
                )
                for field in schema.items
            ],
            nested=True,
        )
        data_expr = [
            sge.Struct(
                expressions=tuple(
                    _literal(
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
        col_names: typing.Sequence[str],
        alias_names: typing.Sequence[str],
        uid_gen: guid.SequentialUIDGenerator,
    ) -> SQLGlotIR:
        """Builds a SQLGlotIR expression from a BigQuery table.

        Args:
            project_id (str): The project ID of the BigQuery table.
            dataset_id (str): The dataset ID of the BigQuery table.
            table_id (str): The table ID of the BigQuery table.
            col_names (typing.Sequence[str]): The names of the columns to select.
            alias_names (typing.Sequence[str]): The aliases for the selected columns.
            uid_gen (guid.SequentialUIDGenerator): A generator for unique identifiers.
        """
        selections = [
            sge.Alias(
                this=sge.to_identifier(col_name, quoted=cls.quoted),
                alias=sge.to_identifier(alias_name, quoted=cls.quoted),
            )
            for col_name, alias_name in zip(col_names, alias_names)
        ]
        table_expr = sge.Table(
            this=sg.to_identifier(table_id, quoted=cls.quoted),
            db=sg.to_identifier(dataset_id, quoted=cls.quoted),
            catalog=sg.to_identifier(project_id, quoted=cls.quoted),
        )
        select_expr = sge.Select().select(*selections).from_(table_expr)
        return cls(expr=select_expr, uid_gen=uid_gen)

    @classmethod
    def from_query_string(
        cls,
        query_string: str,
    ) -> SQLGlotIR:
        """Builds a SQLGlot expression from a query string"""
        uid_gen: guid.SequentialUIDGenerator = guid.SequentialUIDGenerator()
        cte_name = sge.to_identifier(
            next(uid_gen.get_uid_stream("bfcte_")), quoted=cls.quoted
        )
        cte = sge.CTE(
            this=query_string,
            alias=cte_name,
        )
        select_expr = sge.Select().select(sge.Star()).from_(sge.Table(this=cte_name))
        select_expr.set("with", sge.With(expressions=[cte]))
        return cls(expr=select_expr, uid_gen=uid_gen)

    @classmethod
    def from_union(
        cls,
        selects: typing.Sequence[sge.Select],
        output_ids: typing.Sequence[str],
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
            existing_ctes = [*existing_ctes, *select_expr.args.pop("with", [])]

            new_cte_name = sge.to_identifier(
                next(uid_gen.get_uid_stream("bfcte_")), quoted=cls.quoted
            )
            new_cte = sge.CTE(
                this=select_expr,
                alias=new_cte_name,
            )
            existing_ctes = [*existing_ctes, new_cte]

            selections = [
                sge.Alias(
                    this=sge.to_identifier(expr.alias_or_name, quoted=cls.quoted),
                    alias=sge.to_identifier(output_id, quoted=cls.quoted),
                )
                for expr, output_id in zip(select_expr.expressions, output_ids)
            ]
            union_selects.append(
                sge.Select().select(*selections).from_(sge.Table(this=new_cte_name))
            )

        union_expr = sg.union(
            *union_selects,
            distinct=False,
            copy=False,
        )
        final_select_expr = sge.Select().select(sge.Star()).from_(union_expr.subquery())
        final_select_expr.set("with", sge.With(expressions=existing_ctes))
        return cls(expr=final_select_expr, uid_gen=uid_gen)

    def select(
        self,
        selected_cols: tuple[tuple[str, sge.Expression], ...],
    ) -> SQLGlotIR:
        """Replaces new selected columns of the current SELECT clause."""
        selections = [
            sge.Alias(
                this=expr,
                alias=sge.to_identifier(id, quoted=self.quoted),
            )
            for id, expr in selected_cols
        ]

        new_expr = _select_to_cte(
            self.expr,
            sge.to_identifier(
                next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
            ),
        )
        new_expr = new_expr.select(*selections, append=False)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def project(
        self,
        projected_cols: tuple[tuple[str, sge.Expression], ...],
    ) -> SQLGlotIR:
        """Adds new columns to the SELECT clause."""
        projected_cols_expr = [
            sge.Alias(
                this=expr,
                alias=sge.to_identifier(id, quoted=self.quoted),
            )
            for id, expr in projected_cols
        ]
        new_expr = _select_to_cte(
            self.expr,
            sge.to_identifier(
                next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
            ),
        )
        new_expr = new_expr.select(*projected_cols_expr, append=True)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def order_by(
        self,
        ordering: tuple[sge.Ordered, ...],
    ) -> SQLGlotIR:
        """Adds an ORDER BY clause to the query."""
        if len(ordering) == 0:
            return SQLGlotIR(expr=self.expr.copy(), uid_gen=self.uid_gen)
        new_expr = self.expr.order_by(*ordering)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def limit(
        self,
        limit: int | None,
    ) -> SQLGlotIR:
        """Adds a LIMIT clause to the query."""
        if limit is not None:
            new_expr = self.expr.limit(limit)
        else:
            new_expr = self.expr.copy()
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def filter(
        self,
        condition: sge.Expression,
    ) -> SQLGlotIR:
        """Filters the query by adding a WHERE clause."""
        new_expr = _select_to_cte(
            self.expr,
            sge.to_identifier(
                next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
            ),
        )
        return SQLGlotIR(
            expr=new_expr.where(condition, append=False), uid_gen=self.uid_gen
        )

    def join(
        self,
        right: SQLGlotIR,
        join_type: typing.Literal["inner", "outer", "left", "right", "cross"],
        conditions: tuple[tuple[typed_expr.TypedExpr, typed_expr.TypedExpr], ...],
        *,
        joins_nulls: bool = True,
    ) -> SQLGlotIR:
        """Joins the current query with another SQLGlotIR instance."""
        left_cte_name = sge.to_identifier(
            next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
        )
        right_cte_name = sge.to_identifier(
            next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
        )

        left_select = _select_to_cte(self.expr, left_cte_name)
        right_select = _select_to_cte(right.expr, right_cte_name)

        left_ctes = left_select.args.pop("with", [])
        right_ctes = right_select.args.pop("with", [])
        merged_ctes = [*left_ctes, *right_ctes]

        join_conditions = [
            _join_condition(left, right, joins_nulls) for left, right in conditions
        ]
        join_on = sge.And(expressions=join_conditions) if join_conditions else None

        join_type_str = join_type if join_type != "outer" else "full outer"
        new_expr = (
            sge.Select()
            .select(sge.Star())
            .from_(sge.Table(this=left_cte_name))
            .join(sge.Table(this=right_cte_name), on=join_on, join_type=join_type_str)
        )
        new_expr.set("with", sge.With(expressions=merged_ctes))

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
        uuid_col = sge.to_identifier(
            next(self.uid_gen.get_uid_stream("bfcol_")), quoted=self.quoted
        )
        uuid_expr = sge.Alias(this=sge.func("RAND"), alias=uuid_col)
        condition = sge.LT(
            this=uuid_col,
            expression=_literal(fraction, dtypes.FLOAT_DTYPE),
        )

        new_cte_name = sge.to_identifier(
            next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
        )
        new_expr = _select_to_cte(
            self.expr.select(uuid_expr, append=True), new_cte_name
        ).where(condition, append=False)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def insert(
        self,
        destination: bigquery.TableReference,
    ) -> str:
        """Generates an INSERT INTO SQL statement from the current SELECT clause."""
        return sge.insert(self.expr.subquery(), _table(destination)).sql(
            dialect=self.dialect, pretty=self.pretty
        )

    def replace(
        self,
        destination: bigquery.TableReference,
    ) -> str:
        """Generates a MERGE statement to replace the destination table's contents.
        by the current SELECT clause.
        """
        # Workaround for SQLGlot breaking change:
        # https://github.com/tobymao/sqlglot/pull/4495
        whens_expr = [
            sge.When(matched=False, source=True, then=sge.Delete()),
            sge.When(matched=False, then=sge.Insert(this=sge.Var(this="ROW"))),
        ]
        whens_str = "\n".join(
            when_expr.sql(dialect=self.dialect, pretty=self.pretty)
            for when_expr in whens_expr
        )

        merge_str = sge.Merge(
            this=_table(destination),
            using=self.expr.subquery(),
            on=_literal(False, dtypes.BOOL_DTYPE),
        ).sql(dialect=self.dialect, pretty=self.pretty)
        return f"{merge_str}\n{whens_str}"

    def _explode_single_column(
        self, column_name: str, offsets_col: typing.Optional[str]
    ) -> SQLGlotIR:
        """Helper method to handle the case of exploding a single column."""
        offset = (
            sge.to_identifier(offsets_col, quoted=self.quoted) if offsets_col else None
        )
        column = sge.to_identifier(column_name, quoted=self.quoted)
        unnested_column_alias = sge.to_identifier(
            next(self.uid_gen.get_uid_stream("bfcol_")), quoted=self.quoted
        )
        unnest_expr = sge.Unnest(
            expressions=[column],
            alias=sge.TableAlias(columns=[unnested_column_alias]),
            offset=offset,
        )
        selection = sge.Star(replace=[unnested_column_alias.as_(column)])

        # TODO: "CROSS" if not keep_empty else "LEFT"
        # TODO: overlaps_with_parent to replace existing column.
        new_expr = _select_to_cte(
            self.expr,
            sge.to_identifier(
                next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
            ),
        )
        new_expr = new_expr.select(selection, append=False).join(
            unnest_expr, join_type="CROSS"
        )
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def _explode_multiple_columns(
        self,
        column_names: tuple[str, ...],
        offsets_col: typing.Optional[str],
    ) -> SQLGlotIR:
        """Helper method to handle the case of exploding multiple columns."""
        offset = (
            sge.to_identifier(offsets_col, quoted=self.quoted) if offsets_col else None
        )
        columns = [
            sge.to_identifier(column_name, quoted=self.quoted)
            for column_name in column_names
        ]

        # If there are multiple columns, we need to unnest by zipping the arrays:
        # https://cloud.google.com/bigquery/docs/arrays#zipping_arrays
        column_lengths = [
            sge.func("ARRAY_LENGTH", sge.to_identifier(column, quoted=self.quoted)) - 1
            for column in columns
        ]
        generate_array = sge.func(
            "GENERATE_ARRAY",
            sge.convert(0),
            sge.func("LEAST", *column_lengths),
        )
        unnested_offset_alias = sge.to_identifier(
            next(self.uid_gen.get_uid_stream("bfcol_")), quoted=self.quoted
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
        new_expr = _select_to_cte(
            self.expr,
            sge.to_identifier(
                next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
            ),
        )
        new_expr = new_expr.select(selection, append=False).join(
            unnest_expr, join_type="CROSS"
        )
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)


def _select_to_cte(expr: sge.Select, cte_name: sge.Identifier) -> sge.Select:
    """Transforms a given sge.Select query by pushing its main SELECT statement
    into a new CTE and then generates a 'SELECT * FROM new_cte_name'
    for the new query."""
    select_expr = expr.copy()
    existing_ctes = select_expr.args.pop("with", [])
    new_cte = sge.CTE(
        this=select_expr,
        alias=cte_name,
    )
    new_with_clause = sge.With(expressions=[*existing_ctes, new_cte])
    new_select_expr = sge.Select().select(sge.Star()).from_(sge.Table(this=cte_name))
    new_select_expr.set("with", new_with_clause)
    return new_select_expr


def _literal(value: typing.Any, dtype: dtypes.Dtype) -> sge.Expression:
    sqlglot_type = sgt.SQLGlotType.from_bigframes_dtype(dtype)
    if value is None:
        return _cast(sge.Null(), sqlglot_type)
    elif dtype == dtypes.BYTES_DTYPE:
        return _cast(str(value), sqlglot_type)
    elif dtypes.is_time_like(dtype):
        if isinstance(value, np.generic):
            value = value.item()
        return _cast(sge.convert(value.isoformat()), sqlglot_type)
    elif dtype in (dtypes.NUMERIC_DTYPE, dtypes.BIGNUMERIC_DTYPE):
        return _cast(sge.convert(value), sqlglot_type)
    elif dtypes.is_geo_like(dtype):
        wkt = value if isinstance(value, str) else to_wkt(value)
        return sge.func("ST_GEOGFROMTEXT", sge.convert(wkt))
    elif dtype == dtypes.JSON_DTYPE:
        return sge.ParseJSON(this=sge.convert(str(value)))
    elif dtype == dtypes.TIMEDELTA_DTYPE:
        return sge.convert(utils.timedelta_to_micros(value))
    elif dtypes.is_struct_like(dtype):
        items = [
            _literal(value=value[field_name], dtype=field_dtype).as_(
                field_name, quoted=True
            )
            for field_name, field_dtype in dtypes.get_struct_fields(dtype).items()
        ]
        return sge.Struct.from_arg_list(items)
    elif dtypes.is_array_like(dtype):
        value_type = dtypes.get_array_inner_type(dtype)
        values = sge.Array(
            expressions=[_literal(value=v, dtype=value_type) for v in value]
        )
        return values if len(value) > 0 else _cast(values, sqlglot_type)
    else:
        if isinstance(value, np.generic):
            value = value.item()
        return sge.convert(value)


def _cast(arg: typing.Any, to: str) -> sge.Cast:
    return sge.Cast(this=arg, to=to)


def _table(table: bigquery.TableReference) -> sge.Table:
    return sge.Table(
        this=sg.to_identifier(table.table_id, quoted=True),
        db=sg.to_identifier(table.dataset_id, quoted=True),
        catalog=sg.to_identifier(table.project, quoted=True),
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
    left_str = _cast(left.expr, "STRING")
    right_str = _cast(right.expr, "STRING")
    left_0 = sge.func("COALESCE", left_str, _literal("0", dtypes.STRING_DTYPE))
    left_1 = sge.func("COALESCE", left_str, _literal("1", dtypes.STRING_DTYPE))
    right_0 = sge.func("COALESCE", right_str, _literal("0", dtypes.STRING_DTYPE))
    right_1 = sge.func("COALESCE", right_str, _literal("1", dtypes.STRING_DTYPE))
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
    left_0 = sge.func("COALESCE", left.expr, _literal(0, left.dtype))
    left_1 = sge.func("COALESCE", left.expr, _literal(1, left.dtype))
    right_0 = sge.func("COALESCE", right.expr, _literal(0, right.dtype))
    right_1 = sge.func("COALESCE", right.expr, _literal(1, right.dtype))
    if not is_floating_types:
        return sge.And(
            this=sge.EQ(this=left_0, expression=right_0),
            expression=sge.EQ(this=left_1, expression=right_1),
        )

    left_2 = sge.If(
        this=sge.IsNan(this=left.expr), true=_literal(2, left.dtype), false=left_0
    )
    left_3 = sge.If(
        this=sge.IsNan(this=left.expr), true=_literal(3, left.dtype), false=left_1
    )
    right_2 = sge.If(
        this=sge.IsNan(this=right.expr), true=_literal(2, right.dtype), false=right_0
    )
    right_3 = sge.If(
        this=sge.IsNan(this=right.expr), true=_literal(3, right.dtype), false=right_1
    )
    return sge.And(
        this=sge.EQ(this=left_2, expression=right_2),
        expression=sge.EQ(this=left_3, expression=right_3),
    )
