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

import pandas as pd
import sqlglot as sg
import sqlglot.dialects.bigquery
import sqlglot.expressions as sge

from bigframes import dtypes
import bigframes.core.compile.sqlglot.sqlglot_types as sgt


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

    @property
    def sql(self) -> str:
        """Generate SQL string from the given expression."""
        return self.expr.sql(dialect=self.dialect, pretty=self.pretty)

    @classmethod
    def from_pandas(
        cls,
        pd_df: pd.DataFrame,
        schema_names: typing.Sequence[str],
        schema_dtypes: typing.Sequence[dtypes.Dtype],
    ) -> SQLGlotIR:
        """Builds SQLGlot expression from pyarrow table."""
        dtype_expr = sge.DataType(
            this=sge.DataType.Type.STRUCT,
            expressions=[
                sge.ColumnDef(
                    this=sge.to_identifier(name, quoted=True),
                    kind=sgt.SQLGlotType.from_bigframes_dtype(dtype),
                )
                for name, dtype in zip(schema_names, schema_dtypes)
            ],
            nested=True,
        )
        data_expr = [
            sge.Tuple(
                expressions=tuple(
                    _literal(
                        value=value,
                        dtype=sgt.SQLGlotType.from_bigframes_dtype(dtype),
                    )
                    for value, dtype in zip(row, schema_dtypes)
                )
            )
            for _, row in pd_df.iterrows()
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
        return cls(expr=sg.select(sge.Star()).from_(expr))

    def select(
        self,
        select_cols: typing.Dict[str, sge.Expression],
    ) -> SQLGlotIR:
        selected_cols = [
            sge.Alias(
                this=expr,
                alias=sge.to_identifier(id, quoted=self.quoted),
            )
            for id, expr in select_cols.items()
        ]
        expr = self.expr.select(*selected_cols, append=False)
        return SQLGlotIR(expr=expr)


def _literal(value: typing.Any, dtype: str) -> sge.Expression:
    if value is None:
        return _cast(sge.Null(), dtype)

    # TODO: handle other types like visit_DefaultLiteral
    return sge.convert(value)


def _cast(arg, to) -> sge.Cast:
    return sge.Cast(this=arg, to=to)
