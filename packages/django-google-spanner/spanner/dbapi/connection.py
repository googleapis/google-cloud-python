# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from .cursor import (
    OP_CONN_CLOSE, OP_DDL, OP_DELETE, OP_INSERT, OP_UPDATE, Cursor,
)
from .exceptions import Error


class Connection(object):
    def __init__(self, db_handle):
        self.__dbhandle = db_handle
        self.__closed = False
        self.__ops = []
        self.__ddl_statements = []

    def __raise_if_already_closed(self):
        """
        Raises an exception if attempting to use an already closed connection.
        """
        if self.__closed:
            raise Error('attempting to use an already closed connection')

    def close(self):
        self.commit(OP_CONN_CLOSE)
        self.__raise_if_already_closed()
        self.__dbhandle = None
        self.__closed = True

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        return self.close()

    def commit(self, last_op=None):
        self.__check_or_flush_update_ddl(last_op)

        if not self.__ops:
            return

        ops, self.__ops = self.__ops, []
        with self.__dbhandle.batch() as batch:
            for (op, table, columns, values) in ops:
                if op == OP_DELETE:
                    batch.delete(table)
                elif op == OP_INSERT:
                    batch.insert(table, columns, values)
                elif op == OP_UPDATE:
                    batch.update(table, columns, values)

    def rollback(self):
        # We don't manage transactions.
        pass

    def append_to_batch_stack(self, op, table, columns, values):
        self.__ops.append((op, table, columns, values))

    def cursor(self):
        return Cursor(self)

    def __update_ddl(self, ddl_statements):
        """
        Runs the list of Data Definition Language (DDL) statements on the specified
        database. Note that each DDL statement MUST NOT contain a semicolon.

        Args:
            ddl_statements: a list of DDL statements, each without a semicolon.

        Returns:
            google.api_core.operation.Operation
        """
        # Synchronously wait on the operation's completion.
        return self.__dbhandle.update_ddl(ddl_statements).result()

    def read_snapshot(self):
        return self.__dbhandle.snapshot()

    def in_transaction(self, fn, *args, **kwargs):
        return self.__dbhandle.run_in_transaction(fn, *args, **kwargs)

    def handle_update_ddl(self, ddl_statement, prev_op=None):
        if prev_op is None or prev_op != OP_DDL:
            return self.__update_ddl([ddl_statement])
        self.__ddl_statements.append(ddl_statement)

    def __check_or_flush_update_ddl(self, last_op):
        """
        Run the batched DDL statements if last_op is a non-DDL statement.
        """
        if last_op == OP_DDL or last_op is None:
            # Nothing to do here and we can keep on collecting
            # DDL statements to later send in a batch.
            return

        if self.__ddl_statements:
            ddl_statements = self.__ddl_statements
            self.__ddl_statements = []
            return self.__update_ddl(ddl_statements)
