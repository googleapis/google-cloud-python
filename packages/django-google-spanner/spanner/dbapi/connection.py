# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from .cursor import Cursor
from .exceptions import Error


class Connection(object):
    def __init__(self, db_handle):
        self.__dbhandle = db_handle
        self.__closed = False
        self.__ddl_statements = []

    def __raise_if_already_closed(self):
        """
        Raises an exception if attempting to use an already closed connection.
        """
        if self.__closed:
            raise Error('attempting to use an already closed connection')

    def close(self):
        self.commit()
        self.__raise_if_already_closed()
        self.__dbhandle = None
        self.__closed = True

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        return self.close()

    def commit(self):
        self.run_prior_DDL_statements()

    def rollback(self):
        # We don't manage transactions.
        pass

    def cursor(self):
        return Cursor(self)

    def __handle_update_ddl(self, ddl_statements):
        """
        Runs the list of Data Definition Language (DDL) statements on the underlying
        database. Note that each DDL statement MUST NOT contain a semicolon.

        Args:
            ddl_statements: a list of DDL statements, each without a semicolon.

        Returns:
            google.api_core.operation.Operation.result()
        """
        # Synchronously wait on the operation's completion.
        return self.__dbhandle.update_ddl(ddl_statements).result()

    def read_snapshot(self):
        return self.__dbhandle.snapshot()

    def in_transaction(self, fn, *args, **kwargs):
        return self.__dbhandle.run_in_transaction(fn, *args, **kwargs)

    def append_ddl_statement(self, ddl_statement):
        self.__ddl_statements.append(ddl_statement)

    def run_prior_DDL_statements(self):
        if not self.__ddl_statements:
            return

        ddl_statements = self.__ddl_statements
        self.__ddl_statements = []
        return self.__handle_update_ddl(ddl_statements)
