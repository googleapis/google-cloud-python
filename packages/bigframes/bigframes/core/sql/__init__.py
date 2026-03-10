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

"""
Utility functions for SQL construction.
"""

import json
from typing import (
    Any,
    cast,
    Collection,
    Iterable,
    Mapping,
    Optional,
    TYPE_CHECKING,
    Union,
)

import bigframes_vendored.sqlglot.expressions as sge

from bigframes.core.compile.sqlglot import sql

if TYPE_CHECKING:
    import google.cloud.bigquery as bigquery

    import bigframes.core.ordering


# shapely.wkt.dumps was moved to shapely.io.to_wkt in 2.0.
try:
    from shapely.io import to_wkt  # type: ignore
except ImportError:
    from shapely.wkt import dumps  # type: ignore

    to_wkt = dumps


def multi_literal(*values: Any):
    literal_strings = [sql.to_sql(sql.literal(i)) for i in values]
    return "(" + ", ".join(literal_strings) + ")"


def cast_as_string(column_name: str) -> str:
    """Return a string representing string casting of a column."""

    return sge.Cast(this=sge.to_identifier(column_name, quoted=True), to="STRING").sql(
        dialect="bigquery"
    )


def to_json_string(column_name: str) -> str:
    """Return a string representing JSON version of a column."""

    return f"TO_JSON_STRING({sql.to_sql(sql.identifier(column_name))})"


def csv(values: Iterable[str]) -> str:
    """Return a string of comma separated values."""
    return ", ".join(values)


def infix_op(opname: str, left_arg: str, right_arg: str):
    # Maybe should add parentheses??
    return f"{left_arg} {opname} {right_arg}"


def is_distinct_sql(columns: Iterable[str], table_ref: bigquery.TableReference) -> str:
    table_expr = sge.Table(
        this=sge.Identifier(this=table_ref.table_id, quoted=True),
        db=sge.Identifier(this=table_ref.dataset_id, quoted=True),
        catalog=sge.Identifier(this=table_ref.project, quoted=True),
    )
    to_select = [sge.to_identifier(col, quoted=True) for col in columns]

    full_table_sql = (
        sge.Select().select(*to_select).from_(table_expr).sql(dialect="bigquery")
    )
    distinct_table_sql = (
        sge.Select()
        .select(*to_select)
        .distinct()
        .from_(table_expr)
        .sql(dialect="bigquery")
    )

    is_unique_sql = f"""WITH full_table AS (
        {full_table_sql}
    ),
    distinct_table AS (
        {distinct_table_sql}
    )

    SELECT (SELECT COUNT(*) FROM full_table) AS `total_count`,
    (SELECT COUNT(*) FROM distinct_table) AS `distinct_count`
    """
    return is_unique_sql


def ordering_clause(
    ordering: Iterable[bigframes.core.ordering.OrderingExpression],
) -> str:
    import bigframes.core.expression

    parts = []
    for col_ref in ordering:
        asc_desc = "ASC" if col_ref.direction.is_ascending else "DESC"
        null_clause = "NULLS LAST" if col_ref.na_last else "NULLS FIRST"
        ordering_expr = col_ref.scalar_expression
        # We don't know how to compile scalar expressions in isolation
        if ordering_expr.is_const:
            # Probably shouldn't have constants in ordering definition, but best to ignore if somehow they end up here.
            continue
        assert isinstance(ordering_expr, bigframes.core.expression.DerefOp)
        part = f"`{ordering_expr.id.sql}` {asc_desc} {null_clause}"
        parts.append(part)
    return f"ORDER BY {' ,'.join(parts)}"


def create_vector_index_ddl(
    *,
    replace: bool,
    index_name: str,
    table_name: str,
    column_name: str,
    stored_column_names: Collection[str],
    options: Mapping[str, Union[str | int | bool | float]] = {},
) -> str:
    """Encode the VECTOR INDEX statement for BigQuery Vector Search."""

    if replace:
        create = "CREATE OR REPLACE VECTOR INDEX "
    else:
        create = "CREATE VECTOR INDEX IF NOT EXISTS "

    if len(stored_column_names) > 0:
        escaped_stored = [
            f"{sql.to_sql(sql.identifier(name))}" for name in stored_column_names
        ]
        storing = f"STORING({', '.join(escaped_stored)}) "
    else:
        storing = ""

    rendered_options = ", ".join(
        [
            f"{option_name} = {sql.to_sql(sql.literal(option_value))}"
            for option_name, option_value in options.items()
        ]
    )

    return f"""
    {create} {sql.to_sql(sql.identifier(index_name))}
    ON {sql.to_sql(sql.identifier(table_name))}({sql.to_sql(sql.identifier(column_name))})
    {storing}
    OPTIONS({rendered_options});
    """


def create_vector_search_sql(
    sql_string: str,
    *,
    base_table: str,
    column_to_search: str,
    query_column_to_search: Optional[str] = None,
    top_k: Optional[int] = None,
    distance_type: Optional[str] = None,
    options: Optional[Mapping[str, Union[str | int | bool | float]]] = None,
) -> str:
    """Encode the VECTOR SEARCH statement for BigQuery Vector Search."""

    vector_search_args = [
        f"TABLE {sql.to_sql(sql.identifier(cast(str, base_table)))}",
        f"{sql.to_sql(sql.literal(column_to_search))}",
        f"({sql_string})",
    ]

    if query_column_to_search is not None:
        vector_search_args.append(
            f"query_column_to_search => {sql.to_sql(sql.literal(query_column_to_search))}"
        )

    if top_k is not None:
        vector_search_args.append(f"top_k=> {sql.to_sql(sql.literal(top_k))}")

    if distance_type is not None:
        vector_search_args.append(
            f"distance_type => {sql.to_sql(sql.literal(distance_type))}"
        )

    if options is not None:
        vector_search_args.append(
            f"options => {sql.to_sql(sql.literal(json.dumps(options, indent=None)))}"
        )

    args_str = ",\n".join(vector_search_args)
    return f"""
    SELECT
        query.*,
        base.*,
        distance,
    FROM VECTOR_SEARCH({args_str})
    """
