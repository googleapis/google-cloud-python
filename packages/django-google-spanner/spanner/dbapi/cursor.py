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

import google.api_core.exceptions as grpc_exceptions

from .exceptions import IntegrityError, OperationalError, ProgrammingError
from .parse_utils import (
    STMT_DDL, STMT_INSERT, STMT_NON_UPDATING, classify_stmt,
    ensure_where_clause, infer_param_types, parse_insert,
    rows_for_insert_or_update, sql_pyformat_args_to_spanner,
)

_UNSET_COUNT = -1
OP_INSERT = 'insert'
OP_UPDATE = 'update'
OP_DELETE = 'delete'
OP_DQL = 'dql'
OP_DDL = 'ddl'
OP_CONN_CLOSE = 'conn_close'


class Cursor(object):
    def __init__(self, db_handle=None):
        self.__itr = None
        self.__res = None
        self.__row_count = _UNSET_COUNT
        self.__db_handle = db_handle
        self.__last_op = None

        # arraysize is a readable and writable property mandated
        # by PEP-0249 https://www.python.org/dev/peps/pep-0249/#arraysize
        # It determines the results of .fetchmany
        self.arraysize = 1

    @property
    def description(self):
        if not (self.__res and self.__res.metadata):
            return None

        row_type = self.__res.metadata.row_type
        columns = []
        for field in row_type.fields:
            columns.append(Column(name=field.name, type_code=field.type.code))
        return tuple(columns)

    @property
    def rowcount(self):
        return self.__row_count

    def close(self):
        if self.__db_handle is None:
            return

        self.__commit_preceding_batch(self.__last_op)
        self.__db_handle = None

    def execute(self, sql, args=None):
        """
        Abstracts and implements execute SQL statements on Cloud Spanner.

        Args:
            sql: A SQL statement
            *args: variadic argument list
            **kwargs: key worded arguments

        Returns:
            None
        """
        if not self.__db_handle:
            raise ProgrammingError('Cursor is not connected to the database')

        # param_types doesn't seem required except as an empty dict to avoid
        # ValueError("Specify 'param_types' when passing 'params'.").
        # See https://github.com/orijtech/spanner-orm/issues/35
        param_types = {} if args else None
        self.__res = None

        # Classify whether this is a read-only SQL statement.
        try:
            classification = classify_stmt(sql)
            if classification == STMT_DDL:
                self.__handle_update_ddl(sql)
            elif classification == STMT_NON_UPDATING:
                self.__handle_DQL(sql, args or None, param_types=param_types)
            elif classification == STMT_INSERT:
                self.__handle_insert(sql, args or None)
            else:
                self.__handle_update(sql, args or None, param_types=param_types)
        except (grpc_exceptions.AlreadyExists, grpc_exceptions.FailedPrecondition) as e:
            raise IntegrityError(e.details if hasattr(e, 'details') else e)
        except grpc_exceptions.InvalidArgument as e:
            raise ProgrammingError(e.details if hasattr(e, 'details') else e)
        except grpc_exceptions.InternalServerError as e:
            raise OperationalError(e.details if hasattr(e, 'details') else e)

    def __handle_update(self, sql, params, param_types):
        self.__commit_preceding_batch(OP_UPDATE)
        self.__db_handle.in_transaction(
            self.__do_execute_update,
            sql, params, param_types,
        )

    def __do_execute_update(self, transaction, sql, params, param_types=None):
        sql = ensure_where_clause(sql)
        sql, params = sql_pyformat_args_to_spanner(sql, params)

        # Given that we now format datetime as a Spanner TimeStamp,
        # i.e. in ISO 8601 format, we need to give Cloud Spanner a
        # hint that the parameter is of Spanner.TimeStamp.
        # See https://cloud.google.com/spanner/docs/data-types#canonical-format_1
        param_types = infer_param_types(params, param_types)

        res = transaction.execute_update(sql, params=params, param_types=param_types)
        self.__itr = None
        if type(res) == int:
            self.__row_count = res

        return res

    def __handle_insert(self, sql, params):
        self.__commit_preceding_batch(OP_DDL)

        # There are 3 variants of an INSERT statement:
        # a) INSERT INTO <table> (columns...) VALUES (<inlined values>): no params
        # b) INSERT INTO <table> (columns...) SELECT_STMT:               no params
        # c) INSERT INTO <table> (columns...) VALUES (%s,...):           with params
        parts = parse_insert(sql)
        columns = parts.get('columns')
        rows = None
        if params:
            # Case c)
            rows = rows_for_insert_or_update(columns, params, parts.get('values_pyformat'))

        self.__db_handle.in_transaction(
            self.__do_execute_insert,
            parts.get('table'),
            columns,
            rows,
        )

    def __do_execute_insert(self, transaction, table, columns, values):
        return transaction.insert(table, columns, values)

    def __execute_insert_no_params(self, transaction, sql):
        return transaction.execute_update(sql)

    def __commit_preceding_batch(self, op=None):
        last_op = self.__last_op
        self.__last_op = op
        if op is OP_DQL:
            # Unconditionally flush all operations
            # before any DQL runs to ensure that
            # any stale batched data that hasn't yet been uploaded
            # to Cloud Spanner doesn't linger. See issue #213.
            return self.__db_handle.commit(OP_DQL)
        else:
            return self.__db_handle.commit(last_op)

    def __handle_DQL(self, sql, params, param_types=None):
        self.__commit_preceding_batch(OP_DQL)

        with self.__db_handle.read_snapshot() as snapshot:
            # Reference
            #  https://googleapis.dev/python/spanner/latest/session-api.html#google.cloud.spanner_v1.session.Session.execute_sql
            sql, params = sql_pyformat_args_to_spanner(sql, params)
            param_types = infer_param_types(params, param_types)
            res = snapshot.execute_sql(sql, params=params, param_types=param_types)
            if type(res) == int:
                self.__row_count = res
                self.__itr = None
            else:
                # Immediately using:
                #   iter(response)
                # here, because this Spanner API doesn't provide
                # easy mechanisms to detect when only a single item
                # is returned or many, yet mixing results that
                # are for .fetchone() with those that would result in
                # many items returns a RuntimeError if .fetchone() is
                # invoked and vice versa.
                self.__res = res
                # Read the first element so that StreamedResult can
                # return the metadata after a DQL statement. See issue #155.
                self.__itr = PeekIterator(self.__res)
                # Unfortunately, Spanner doesn't seem to send back
                # information about the number of rows available.
                self.__row_count = _UNSET_COUNT

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.close()

    def executemany(self, operation, seq_of_params):
        if not self.__db_handle:
            raise ProgrammingError('Cursor is not connected to the database')

        raise ProgrammingError('Unimplemented')

    def __next__(self):
        if self.__itr is None:
            raise ProgrammingError('no results to return')
        return next(self.__itr)

    def __iter__(self):
        self.__commit_preceding_batch(OP_DQL)

        if self.__itr is None:
            raise ProgrammingError('no results to return')
        return self.__itr

    def fetchone(self):
        try:
            return next(self)
        except StopIteration:
            return None

    def fetchall(self):
        return list(self.__iter__())

    def fetchmany(self, size=None):
        """
        Fetch the next set of rows of a query result, returning a sequence of sequences.
        An empty sequence is returned when no more rows are available.

        Args:
            size: optional integer to determine the maximum number of results to fetch.


        Raises:
            Error if the previous call to .execute*() did not produce any result set
            or if no call was issued yet.
        """
        if size is None:
            size = self.arraysize

        items = []
        for i in range(size):
            try:
                items.append(tuple(self.__next__()))
            except StopIteration:
                break

        return items

    @property
    def lastrowid(self):
        return None

    def setinputsizes(sizes):
        raise ProgrammingError('Unimplemented')

    def setoutputsize(size, column=None):
        raise ProgrammingError('Unimplemented')

    def __handle_update_ddl(self, ddl_statement):
        self.__commit_preceding_batch(OP_DDL)

        if not self.__db_handle:
            raise ProgrammingError('Trying to run an DDL update but no database handle')

        return self.__db_handle.handle_update_ddl(ddl_statement, self.__last_op)


class Column:
    def __init__(self, name, type_code, display_size=None, internal_size=None,
                 precision=None, scale=None, null_ok=False):
        self.name = name
        self.type_code = type_code
        self.display_size = display_size
        self.internal_size = internal_size
        self.precision = precision
        self.scale = scale
        self.null_ok = null_ok

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        if index == 0:
            return self.name
        elif index == 1:
            return self.type_code
        elif index == 2:
            return self.display_size
        elif index == 3:
            return self.internal_size
        elif index == 4:
            return self.precision
        elif index == 5:
            return self.scale
        elif index == 6:
            return self.null_ok

    def __str__(self):
        rstr = ', '.join([field for field in [
            "name='%s'" % self.name,
            "type_code=%d" % self.type_code,
            None if not self.display_size else "display_size='%s'" % self.display_size,
            None if not self.internal_size else "internal_size='%s'" % self.internal_size,
            None if not self.precision else "precision='%s'" % self.precision,
            None if not self.scale else "scale='%s'" % self.scale,
            None if not self.null_ok else "null_ok='%s'" % self.null_ok,
        ] if field])

        return 'Column(%s)' % rstr


class PeekIterator(object):
    """
    PeekIterator peeks at the first element out of an iterator
    for the sake of operations like auto-population of fields on reading
    the first element.
    """
    def __init__(self, source):
        itr_src = iter(source)

        self.__iters = []
        self.__index = 0

        try:
            head = next(itr_src)
            # Restitch and prepare to read from multiple iterators.
            self.__iters = [iter(itr) for itr in [[head], itr_src]]
        except StopIteration:
            pass

    def __next__(self):
        if self.__index >= len(self.__iters):
            raise StopIteration

        iterator = self.__iters[self.__index]
        try:
            head = next(iterator)
        except StopIteration:
            # That iterator has been exhausted, try with the next one.
            self.__index += 1
            return self.__next__()
        else:
            return head

    def __iter__(self):
        return self
