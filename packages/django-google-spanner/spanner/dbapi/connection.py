# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .cursor import OP_DELETE, OP_INSERT, OP_UPDATE, Cursor
from .exceptions import Error


class Connection(object):
    def __init__(self, db_handle):
        self.__dbhandle = db_handle
        self.__closed = False
        self.__ops = []

    def __raise_if_already_closed(self):
        """
        Raises an exception if attempting to use an already closed connection.
        """
        if self.__closed:
            raise Error('attempting to use an already closed connection')

    def close(self):
        self.commit()
        self.__raise_if_already_closed()
        self._clear_all_sessions()
        self.__dbhandle = None
        self.__closed = True

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        return self.close()

    def commit(self):
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
        session = self._new_session()
        return Cursor(session, self)

    def _new_session(self):
        return self.__dbhandle._pool.get()

    def _done_with_session(self, session):
        if session:
            self.__dbhandle._pool.put(session)

    def _clear_all_sessions(self):
        return self.__dbhandle._pool.clear()

    def update_ddl(self, ddl_statements):
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
