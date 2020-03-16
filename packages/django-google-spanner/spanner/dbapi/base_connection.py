# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from .exceptions import Error
from .utils import get_table_column_schema as get_table_column_schema_impl


class BaseConnection:
    def __init__(self, db_handle, *args, **kwargs):
        self._dbhandle = db_handle
        self._closed = False
        self._ddl_statements = []

    def _raise_if_already_closed(self):
        """
        Raise an exception if attempting to use an already closed connection.
        """
        if self._closed:
            raise Error('attempting to use an already closed connection')

    def __handle_update_ddl(self, ddl_statements):
        """
        Run the list of Data Definition Language (DDL) statements on the underlying
        database. Each DDL statement MUST NOT contain a semicolon.
        Args:
            ddl_statements: a list of DDL statements, each without a semicolon.
        Returns:
            google.api_core.operation.Operation.result()
        """
        self._raise_if_already_closed()
        # Synchronously wait on the operation's completion.
        return self._dbhandle.update_ddl(ddl_statements).result()

    def read_snapshot(self):
        self._raise_if_already_closed()
        return self._dbhandle.snapshot()

    def in_transaction(self, fn, *args, **kwargs):
        self._raise_if_already_closed()
        return self._dbhandle.run_in_transaction(fn, *args, **kwargs)

    def append_ddl_statement(self, ddl_statement):
        self._raise_if_already_closed()
        self._ddl_statements.append(ddl_statement)

    def run_prior_DDL_statements(self):
        self._raise_if_already_closed()

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

    def run_sql_in_snapshot(self, sql):
        # Some SQL e.g. for INFORMATION_SCHEMA cannot be run in read-write transactions
        # hence this method exists to circumvent that limit.
        self.run_prior_DDL_statements()

        with self._dbhandle.snapshot() as snapshot:
            res = snapshot.execute_sql(sql)
            return list(res)

    def get_table_column_schema(self, table_name):
        return get_table_column_schema_impl(self._dbhandle, table_name)
