# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from django.core.exceptions import EmptyResultSet
from django.db.models.sql.compiler import (
    SQLAggregateCompiler as BaseSQLAggregateCompiler,
    SQLCompiler as BaseSQLCompiler, SQLDeleteCompiler as BaseSQLDeleteCompiler,
    SQLInsertCompiler as BaseSQLInsertCompiler,
    SQLUpdateCompiler as BaseSQLUpdateCompiler,
)
from django.db.utils import DatabaseError


class SQLCompiler(BaseSQLCompiler):
    def get_combinator_sql(self, combinator, all):
        """
        Copied from the base class except for:
            combinator_sql += ' ALL' if all else ' DISTINCT'
        Cloud Spanner requires ALL or DISTINCT.
        """
        features = self.connection.features
        compilers = [
            query.get_compiler(self.using, self.connection)
            for query in self.query.combined_queries if not query.is_empty()
        ]
        if not features.supports_slicing_ordering_in_compound:
            for query, compiler in zip(self.query.combined_queries, compilers):
                if query.low_mark or query.high_mark:
                    raise DatabaseError('LIMIT/OFFSET not allowed in subqueries of compound statements.')
                if compiler.get_order_by():
                    raise DatabaseError('ORDER BY not allowed in subqueries of compound statements.')
        parts = ()
        for compiler in compilers:
            try:
                # If the columns list is limited, then all combined queries
                # must have the same columns list. Set the selects defined on
                # the query on all combined queries, if not already set.
                if not compiler.query.values_select and self.query.values_select:
                    compiler.query.set_values((
                        *self.query.extra_select,
                        *self.query.values_select,
                        *self.query.annotation_select,
                    ))
                part_sql, part_args = compiler.as_sql()
                if compiler.query.combinator:
                    # Wrap in a subquery if wrapping in parentheses isn't
                    # supported.
                    if not features.supports_parentheses_in_compound:
                        part_sql = 'SELECT * FROM ({})'.format(part_sql)
                    # Add parentheses when combining with compound query if not
                    # already added for all compound queries.
                    elif not features.supports_slicing_ordering_in_compound:
                        part_sql = '({})'.format(part_sql)
                parts += ((part_sql, part_args),)
            except EmptyResultSet:
                # Omit the empty queryset with UNION and with DIFFERENCE if the
                # first queryset is nonempty.
                if combinator == 'union' or (combinator == 'difference' and parts):
                    continue
                raise
        if not parts:
            raise EmptyResultSet
        combinator_sql = self.connection.ops.set_operators[combinator]
        combinator_sql += ' ALL' if all else ' DISTINCT'
        braces = '({})' if features.supports_slicing_ordering_in_compound else '{}'
        sql_parts, args_parts = zip(*((braces.format(sql), args) for sql, args in parts))
        result = [' {} '.format(combinator_sql).join(sql_parts)]
        params = []
        for part in args_parts:
            params.extend(part)
        return result, params


class SQLInsertCompiler(BaseSQLInsertCompiler, SQLCompiler):
    pass


class SQLDeleteCompiler(BaseSQLDeleteCompiler, SQLCompiler):
    pass


class SQLUpdateCompiler(BaseSQLUpdateCompiler, SQLCompiler):
    pass


class SQLAggregateCompiler(BaseSQLAggregateCompiler, SQLCompiler):
    pass
