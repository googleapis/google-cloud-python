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

import pyarrow as pa
import sqlglot as sg
import sqlglot.dialects.bigquery
import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes.core import guid
import bigframes.core.compile.sqlglot.sqlglot_types as sgt
import bigframes.core.local_data as local_data
import bigframes.core.schema as schemata

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
        schema: schemata.ArraySchema,
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

    def select(
        self,
        selected_cols: tuple[tuple[str, sge.Expression], ...],
    ) -> SQLGlotIR:
        cols_expr = [
            sge.Alias(
                this=expr,
                alias=sge.to_identifier(id, quoted=self.quoted),
            )
            for id, expr in selected_cols
        ]
        new_expr = self._encapsulate_as_cte().select(*cols_expr, append=False)
        return SQLGlotIR(expr=new_expr)

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
        # TODO: some columns are not able to be projected into the same select.
        select_expr = self.expr.select(*projected_cols_expr, append=True)
        return SQLGlotIR(expr=select_expr)

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
        new_with_clause = sge.With(expressions=existing_ctes + [new_cte])
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
        return _cast(sge.convert(value.isoformat()), sqlglot_type)
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
        return sge.convert(value)


def _cast(arg: typing.Any, to: str) -> sge.Cast:
    return sge.Cast(this=arg, to=to)
