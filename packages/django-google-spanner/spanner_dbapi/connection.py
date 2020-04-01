# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from collections import namedtuple

from google.cloud import spanner_v1 as spanner

from .cursor import Cursor
from .exceptions import InterfaceError

ColumnDetails = namedtuple('column_details', ['null_ok', 'spanner_type'])


class Connection:
    def __init__(self, db_handle):
        self._dbhandle = db_handle
        self._closed = False
        self._ddl_statements = []

    def cursor(self):
        self.__raise_if_already_closed()

        return Cursor(self)

    def __raise_if_already_closed(self):
        """
        Raise an exception if attempting to use an already closed connection.
        """
        if self._closed:
            raise InterfaceError('connection already closed')

    def __handle_update_ddl(self, ddl_statements):
        """
        Run the list of Data Definition Language (DDL) statements on the underlying
        database. Each DDL statement MUST NOT contain a semicolon.
        Args:
            ddl_statements: a list of DDL statements, each without a semicolon.
        Returns:
            google.api_core.operation.Operation.result()
        """
        self.__raise_if_already_closed()
        # Synchronously wait on the operation's completion.
        return self._dbhandle.update_ddl(ddl_statements).result()

    def read_snapshot(self):
        self.__raise_if_already_closed()
        return self._dbhandle.snapshot()

    def in_transaction(self, fn, *args, **kwargs):
        self.__raise_if_already_closed()
        return self._dbhandle.run_in_transaction(fn, *args, **kwargs)

    def append_ddl_statement(self, ddl_statement):
        self.__raise_if_already_closed()
        self._ddl_statements.append(ddl_statement)

    def run_prior_DDL_statements(self):
        self.__raise_if_already_closed()

        if not self._ddl_statements:
            return

        ddl_statements = self._ddl_statements
        self._ddl_statements = []

        return self.__handle_update_ddl(ddl_statements)

    def list_tables(self):
        return self.run_sql_in_snapshot("""
            SELECT
              t.table_name
            FROM
              information_schema.tables AS t
            WHERE
              t.table_catalog = '' and t.table_schema = ''
            """)

    def run_sql_in_snapshot(self, sql, params=None, param_types=None):
        # Some SQL e.g. for INFORMATION_SCHEMA cannot be run in read-write transactions
        # hence this method exists to circumvent that limit.
        self.run_prior_DDL_statements()

        with self._dbhandle.snapshot() as snapshot:
            res = snapshot.execute_sql(sql, params=params, param_types=param_types)
            return list(res)

    def get_table_column_schema(self, table_name):
        rows = self.run_sql_in_snapshot(
            '''SELECT
                COLUMN_NAME, IS_NULLABLE, SPANNER_TYPE
            FROM
                INFORMATION_SCHEMA.COLUMNS
            WHERE
                TABLE_SCHEMA = ''
            AND
                TABLE_NAME = @table_name''',
            params={'table_name': table_name},
            param_types={'table_name': spanner.param_types.STRING},
        )

        column_details = {}
        for column_name, is_nullable, spanner_type in rows:
            column_details[column_name] = ColumnDetails(
                null_ok=is_nullable == 'YES',
                spanner_type=spanner_type,
            )
        return column_details

    def close(self):
        self.rollback()
        self.__dbhandle = None
        self._closed = True

    def commit(self):
        self.__raise_if_already_closed()

        self.run_prior_DDL_statements()

    def rollback(self):
        self.__raise_if_already_closed()

        # TODO: to be added.

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.commit()
        self.close()
