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
from bigframes.core import guid
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
        """Builds SQLGlot expression from pyarrow table."""
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
        """Builds SQLGlot expression from a query string"""
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
        """Builds SQLGlot expression by union of multiple select expressions."""
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
                    this=expr.alias_or_name,
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
        squash_selections: bool = True,
    ) -> SQLGlotIR:
        selections = [
            sge.Alias(
                this=expr,
                alias=sge.to_identifier(id, quoted=self.quoted),
            )
            for id, expr in selected_cols
        ]

        # If squashing is enabled, we try to simplify the selections
        # by checking if the new selections are simply aliases of the
        # original columns.
        if squash_selections:
            new_selections = _squash_selections(self.expr.expressions, selections)
            if new_selections != []:
                new_expr = self.expr.select(*new_selections, append=False)
                return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

        new_expr = self._encapsulate_as_cte().select(*selections, append=False)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def order_by(
        self,
        ordering: tuple[sge.Ordered, ...],
    ) -> SQLGlotIR:
        """Adds ORDER BY clause to the query."""
        if len(ordering) == 0:
            return SQLGlotIR(expr=self.expr.copy(), uid_gen=self.uid_gen)
        new_expr = self.expr.order_by(*ordering)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def limit(
        self,
        limit: int | None,
    ) -> SQLGlotIR:
        """Adds LIMIT clause to the query."""
        if limit is not None:
            new_expr = self.expr.limit(limit)
        else:
            new_expr = self.expr.copy()
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def project(
        self,
        projected_cols: tuple[tuple[str, sge.Expression], ...],
    ) -> SQLGlotIR:
        projected_cols_expr = [
            sge.Alias(
                this=expr,
                alias=sge.to_identifier(id, quoted=self.quoted),
            )
            for id, expr in projected_cols
        ]
        new_expr = self._encapsulate_as_cte().select(*projected_cols_expr, append=True)
        return SQLGlotIR(expr=new_expr, uid_gen=self.uid_gen)

    def insert(
        self,
        destination: bigquery.TableReference,
    ) -> str:
        return sge.insert(self.expr.subquery(), _table(destination)).sql(
            dialect=self.dialect, pretty=self.pretty
        )

    def replace(
        self,
        destination: bigquery.TableReference,
    ) -> str:
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

    def _encapsulate_as_cte(
        self,
    ) -> sge.Select:
        """Transforms a given sge.Select query by pushing its main SELECT statement
        into a new CTE and then generates a 'SELECT * FROM new_cte_name'
        for the new query."""
        select_expr = self.expr.copy()

        existing_ctes = select_expr.args.pop("with", [])
        new_cte_name = sge.to_identifier(
            next(self.uid_gen.get_uid_stream("bfcte_")), quoted=self.quoted
        )
        new_cte = sge.CTE(
            this=select_expr,
            alias=new_cte_name,
        )
        new_with_clause = sge.With(expressions=[*existing_ctes, new_cte])
        new_select_expr = (
            sge.Select().select(sge.Star()).from_(sge.Table(this=new_cte_name))
        )
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


def _squash_selections(
    old_expr: list[sge.Expression], new_expr: list[sge.Alias]
) -> list[sge.Alias]:
    """
    TODO: Reanble this function to optimize the SQL.
    Simplifies the select column expressions if existing (old_expr) and
    new (new_expr) selected columns are both simple aliases of column definitions.

    Example:
    old_expr: [A AS X, B AS Y]
    new_expr: [X AS P, Y AS Q]
    Result:   [A AS P, B AS Q]
    """
    old_alias_map: typing.Dict[str, str] = {}
    for selected in old_expr:
        column_alias_pair = _get_column_alias_pair(selected)
        if column_alias_pair is None:
            return []
        else:
            old_alias_map[column_alias_pair[1]] = column_alias_pair[0]

    new_selected_cols: typing.List[sge.Alias] = []
    for selected in new_expr:
        column_alias_pair = _get_column_alias_pair(selected)
        if column_alias_pair is None or column_alias_pair[0] not in old_alias_map:
            return []
        else:
            new_alias_expr = sge.Alias(
                this=sge.ColumnDef(
                    this=sge.to_identifier(
                        old_alias_map[column_alias_pair[0]], quoted=True
                    )
                ),
                alias=sg.to_identifier(column_alias_pair[1], quoted=True),
            )
            new_selected_cols.append(new_alias_expr)
    return new_selected_cols


def _get_column_alias_pair(
    expr: sge.Expression,
) -> typing.Optional[typing.Tuple[str, str]]:
    """Checks if an expression is a simple alias of a column definition
    (e.g., "column_name AS alias_name").
    If it is, returns a tuple containing the alias name and original column name.
    Returns `None` otherwise.
    """
    if not isinstance(expr, sge.Alias):
        return None
    if not isinstance(expr.this, sge.ColumnDef):
        return None

    column_def_expr: sge.ColumnDef = expr.this
    if not isinstance(column_def_expr.this, sge.Identifier):
        return None

    original_identifier: sge.Identifier = column_def_expr.this
    return (original_identifier.this, expr.alias)
