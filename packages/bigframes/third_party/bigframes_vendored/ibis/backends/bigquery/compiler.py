# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/backends/bigquery/compiler.py
"""Module to convert from Ibis expression to SQL string."""

from __future__ import annotations

import re

from ibis.backends.base.sql import compiler as sql_compiler
import ibis.backends.bigquery.compiler
from ibis.backends.bigquery.datatypes import BigQueryType
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops

_NAME_REGEX = re.compile(r'[^!"$()*,./;?@[\\\]^`{}~\n]+')
_EXACT_NAME_REGEX = re.compile(f"^{_NAME_REGEX.pattern}$")


class BigQueryTableSetFormatter(sql_compiler.TableSetFormatter):
    def _quote_identifier(self, name):
        """Restore 6.x version of identifier quoting.

        7.x uses sqlglot which as of December 2023 doesn't know about the
        extended unicode names for BigQuery yet.
        """
        if _EXACT_NAME_REGEX.match(name) is not None:
            return name
        return f"`{name}`"

    def _format_in_memory_table(self, op):
        """Restore 6.x version of InMemoryTable.

        BigQuery DataFrames explicitly uses InMemoryTable only when we know
        the data is small enough to embed in SQL.
        """
        schema = op.schema
        names = schema.names
        types = schema.types

        raw_rows = []
        for row in op.data.to_frame().itertuples(index=False):
            raw_row = ", ".join(
                f"{self._translate(lit)} AS {name}"
                for lit, name in zip(
                    map(ops.Literal, row, types), map(self._quote_identifier, names)
                )
            )
            raw_rows.append(f"STRUCT({raw_row})")
        array_type = BigQueryType.from_ibis(dt.Array(op.schema.as_struct()))

        return f"UNNEST({array_type}[{', '.join(raw_rows)}])"


# Override implementation.
ibis.backends.bigquery.compiler.BigQueryTableSetFormatter._quote_identifier = (
    BigQueryTableSetFormatter._quote_identifier
)
ibis.backends.bigquery.compiler.BigQueryTableSetFormatter._format_in_memory_table = (
    BigQueryTableSetFormatter._format_in_memory_table
)
