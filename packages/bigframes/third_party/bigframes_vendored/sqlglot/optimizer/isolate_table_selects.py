# Contains code from https://github.com/tobymao/sqlglot/blob/v28.5.0/sqlglot/optimizer/isolate_table_selects.py

from __future__ import annotations

import typing as t

from bigframes_vendored.sqlglot import alias, exp
from bigframes_vendored.sqlglot.errors import OptimizeError
from bigframes_vendored.sqlglot.optimizer.scope import traverse_scope
from bigframes_vendored.sqlglot.schema import ensure_schema

if t.TYPE_CHECKING:
    from bigframes_vendored.sqlglot._typing import E
    from bigframes_vendored.sqlglot.dialects.dialect import DialectType
    from bigframes_vendored.sqlglot.schema import Schema


def isolate_table_selects(
    expression: E,
    schema: t.Optional[t.Dict | Schema] = None,
    dialect: DialectType = None,
) -> E:
    schema = ensure_schema(schema, dialect=dialect)

    for scope in traverse_scope(expression):
        if len(scope.selected_sources) == 1:
            continue

        for _, source in scope.selected_sources.values():
            assert source.parent

            if (
                not isinstance(source, exp.Table)
                or not schema.column_names(source)
                or isinstance(source.parent, exp.Subquery)
                or isinstance(source.parent.parent, exp.Table)
            ):
                continue

            if not source.alias:
                raise OptimizeError(
                    "Tables require an alias. Run qualify_tables optimization."
                )

            source.replace(
                exp.select("*")
                .from_(
                    alias(source, source.alias_or_name, table=True),
                    copy=False,
                )
                .subquery(source.alias, copy=False)
            )

    return expression
