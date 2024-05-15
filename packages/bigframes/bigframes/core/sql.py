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
import textwrap
from typing import Iterable, TYPE_CHECKING

# Literals and identifiers matching this pattern can be unquoted
unquoted = r"^[A-Za-z_][A-Za-z_0-9]*$"


if TYPE_CHECKING:
    import google.cloud.bigquery as bigquery

    import bigframes.core.ordering


### Writing SQL Values (literals, column references, table references, etc.)
def simple_literal(value: str | int | bool | float):
    """Return quoted input string."""
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#literals
    if isinstance(value, str):
        # Single quoting seems to work nicer with ibis than double quoting
        return f"'{escape_special_characters(value)}'"
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
    else:
        raise ValueError(f"Cannot produce literal for {value}")


def multi_literal(*values: str):
    literal_strings = [simple_literal(i) for i in values]
    return "(" + ", ".join(literal_strings) + ")"


def identifier(id: str) -> str:
    """Return a string representing column reference in a SQL."""
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#identifiers
    # Just always escape, otherwise need to check against every reserved sql keyword
    return f"`{escape_special_characters(id)}`"


def escape_special_characters(value: str):
    """Escapes all special charactesrs"""
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#string_and_bytes_literals
    trans_table = str.maketrans(
        {
            "\a": r"\a",
            "\b": r"\b",
            "\f": r"\f",
            "\n": r"\n",
            "\r": r"\r",
            "\t": r"\t",
            "\v": r"\v",
            "\\": r"\\",
            "?": r"\?",
            '"': r"\"",
            "'": r"\'",
            "`": r"\`",
        }
    )
    return value.translate(trans_table)


def cast_as_string(column_name: str) -> str:
    """Return a string representing string casting of a column."""

    return f"CAST({identifier(column_name)} AS STRING)"


def csv(values: Iterable[str]) -> str:
    """Return a string of comma separated values."""
    return ", ".join(values)


def table_reference(table_ref: bigquery.TableReference) -> str:
    return f"`{escape_special_characters(table_ref.project)}`.`{escape_special_characters(table_ref.dataset_id)}`.`{escape_special_characters(table_ref.table_id)}`"


def infix_op(opname: str, left_arg: str, right_arg: str):
    # Maybe should add parentheses??
    return f"{left_arg} {opname} {right_arg}"


### Writing SELECT expressions
def select_from(columns: Iterable[str], subquery: str, distinct: bool = False):
    selection = ", ".join(map(identifier, columns))
    distinct_clause = "DISTINCT " if distinct else ""

    return textwrap.dedent(
        f"SELECT {distinct_clause}{selection}\nFROM (\n" f"{subquery}\n" ")\n"
    )


def select_table(table_ref: bigquery.TableReference):
    return textwrap.dedent(f"SELECT * FROM {table_reference(table_ref)}")


def is_distinct_sql(columns: Iterable[str], table_sql: str) -> str:
    is_unique_sql = f"""WITH full_table AS (
        {select_from(columns, table_sql)}
    ),
    distinct_table AS (
        {select_from(columns, table_sql, distinct=True)}
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
        assert isinstance(
            ordering_expr, bigframes.core.expression.UnboundVariableExpression
        )
        part = f"`{ordering_expr.id}` {asc_desc} {null_clause}"
        parts.append(part)
    return f"ORDER BY {' ,'.join(parts)}"


def snapshot_clause(time_travel_timestamp: datetime.datetime):
    return f"FOR SYSTEM_TIME AS OF TIMESTAMP({repr(time_travel_timestamp.isoformat())})"
