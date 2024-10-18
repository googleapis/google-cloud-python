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

import datetime
import math
from typing import cast, Collection, Iterable, Mapping, TYPE_CHECKING, Union

import bigframes.core.compile.googlesql as googlesql

if TYPE_CHECKING:
    import google.cloud.bigquery as bigquery

    import bigframes.core.ordering


### Writing SQL Values (literals, column references, table references, etc.)
def simple_literal(value: str | int | bool | float | datetime.datetime):
    """Return quoted input string."""
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#literals
    if isinstance(value, str):
        # Single quoting seems to work nicer with ibis than double quoting
        return f"'{googlesql._escape_chars(value)}'"
    elif isinstance(value, (bool, int)):
        return str(value)
    elif isinstance(value, float):
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#floating_point_literals
        if math.isnan(value):
            return 'CAST("nan" as FLOAT)'
        if value == math.inf:
            return 'CAST("+inf" as FLOAT)'
        if value == -math.inf:
            return 'CAST("-inf" as FLOAT)'
        return str(value)
    if isinstance(value, datetime.datetime):
        return f"TIMESTAMP('{value.isoformat()}')"
    else:
        raise ValueError(f"Cannot produce literal for {value}")


def multi_literal(*values: str):
    literal_strings = [simple_literal(i) for i in values]
    return "(" + ", ".join(literal_strings) + ")"


def cast_as_string(column_name: str) -> str:
    """Return a string representing string casting of a column."""

    return googlesql.Cast(
        googlesql.ColumnExpression(column_name), googlesql.DataType.STRING
    ).sql()


def to_json_string(column_name: str) -> str:
    """Return a string representing JSON version of a column."""

    return f"TO_JSON_STRING({googlesql.identifier(column_name)})"


def csv(values: Iterable[str]) -> str:
    """Return a string of comma separated values."""
    return ", ".join(values)


def infix_op(opname: str, left_arg: str, right_arg: str):
    # Maybe should add parentheses??
    return f"{left_arg} {opname} {right_arg}"


def is_distinct_sql(columns: Iterable[str], table_ref: bigquery.TableReference) -> str:
    is_unique_sql = f"""WITH full_table AS (
        {googlesql.Select().from_(table_ref).select(columns).sql()}
    ),
    distinct_table AS (
        {googlesql.Select().from_(table_ref).select(columns, distinct=True).sql()}
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
            f"{googlesql.identifier(name)}" for name in stored_column_names
        ]
        storing = f"STORING({', '.join(escaped_stored)}) "
    else:
        storing = ""

    rendered_options = ", ".join(
        [
            f"{option_name} = {simple_literal(option_value)}"
            for option_name, option_value in options.items()
        ]
    )

    return f"""
    {create} {googlesql.identifier(index_name)}
    ON {googlesql.identifier(table_name)}({googlesql.identifier(column_name)})
    {storing}
    OPTIONS({rendered_options});
    """


def create_vector_search_sql(
    sql_string: str,
    options: Mapping[str, Union[str | int | bool | float]] = {},
) -> str:
    """Encode the VECTOR SEARCH statement for BigQuery Vector Search."""

    base_table = options["base_table"]
    column_to_search = options["column_to_search"]
    distance_type = options["distance_type"]
    top_k = options["top_k"]
    query_column_to_search = options.get("query_column_to_search", None)

    if query_column_to_search is not None:
        query_str = f"""
    SELECT
        query.*,
        base.*,
        distance,
    FROM VECTOR_SEARCH(
        TABLE {googlesql.identifier(cast(str, base_table))},
        {simple_literal(column_to_search)},
        ({sql_string}),
        {simple_literal(query_column_to_search)},
        distance_type => {simple_literal(distance_type)},
        top_k => {simple_literal(top_k)}
    )
    """
    else:
        query_str = f"""
    SELECT
        query.*,
        base.*,
        distance,
    FROM VECTOR_SEARCH(
        TABLE {googlesql.identifier(cast(str, base_table))},
        {simple_literal(column_to_search)},
        ({sql_string}),
        distance_type => {simple_literal(distance_type)},
        top_k => {simple_literal(top_k)}
    )
    """
    return query_str
