# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import google.api_core.exceptions as grpc_exceptions
from google.cloud.spanner_v1 import param_types

from .exceptions import (
    IntegrityError, InterfaceError, OperationalError, ProgrammingError,
)
from .parse_utils import (
    STMT_DDL, STMT_INSERT, STMT_NON_UPDATING, classify_stmt,
    ensure_where_clause, get_param_types, parse_insert,
    sql_pyformat_args_to_spanner,
)
from .utils import PeekIterator

_UNSET_COUNT = -1


# This table maps spanner_types to Spanner's data type sizes as per
#   https://cloud.google.com/spanner/docs/data-types#allowable-types
# It is used to map `display_size` to a known type for Cursor.description
# after a row fetch.
# Since ResultMetadata
#   https://cloud.google.com/spanner/docs/reference/rest/v1/ResultSetMetadata
# does not send back the actual size, we have to lookup the respective size.
# Some fields' sizes are dependent upon the dynamic data hence aren't sent back
# by Cloud Spanner.
code_to_display_size = {
    param_types.BOOL.code: 1,
    param_types.DATE.code: 4,
    param_types.FLOAT64.code: 8,
    param_types.INT64.code: 8,
    param_types.TIMESTAMP.code: 12,
}


class Cursor:
    def __init__(self, connection):
        self._itr = None
        self._res = None
        self._row_count = _UNSET_COUNT
        self._connection = connection
        self._closed = False

        # arraysize is a readable and writable property mandated
        # by PEP-0249 https://www.python.org/dev/peps/pep-0249/#arraysize
        # It determines the results of .fetchmany
        self.arraysize = 1

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
        self._raise_if_already_closed()

        if not self._connection:
            raise ProgrammingError('Cursor is not connected to the database')

        self._res = None

        # Classify whether this is a read-only SQL statement.
        try:
            classification = classify_stmt(sql)
            if classification == STMT_DDL:
                self._connection.append_ddl_statement(sql)
                return

            # For every other operation, we've got to ensure that
            # any prior DDL statements were run.
            self._run_prior_DDL_statements()

            if classification == STMT_NON_UPDATING:
                self.__handle_DQL(sql, args or None)
            elif classification == STMT_INSERT:
                self.__handle_insert(sql, args or None)
            else:
                self.__handle_update(sql, args or None)
        except (grpc_exceptions.AlreadyExists, grpc_exceptions.FailedPrecondition) as e:
            raise IntegrityError(e.details if hasattr(e, 'details') else e)
        except grpc_exceptions.InvalidArgument as e:
            raise ProgrammingError(e.details if hasattr(e, 'details') else e)
        except grpc_exceptions.InternalServerError as e:
            raise OperationalError(e.details if hasattr(e, 'details') else e)

    def __handle_update(self, sql, params):
        self._connection.in_transaction(
            self.__do_execute_update,
            sql, params,
        )

    def __do_execute_update(self, transaction, sql, params, param_types=None):
        sql = ensure_where_clause(sql)
        sql, params = sql_pyformat_args_to_spanner(sql, params)

        res = transaction.execute_update(sql, params=params, param_types=get_param_types(params))
        self._itr = None
        if type(res) == int:
            self._row_count = res

        return res

    def __handle_insert(self, sql, params):
        parts = parse_insert(sql, params)

        # The split between the two styles exists because:
        # in the common case of multiple values being passed
        # with simple pyformat arguments,
        #   SQL: INSERT INTO T (f1, f2) VALUES (%s, %s, %s)
        #   Params:   [(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,)]
        # we can take advantage of a single RPC with:
        #       transaction.insert(table, columns, values)
        # instead of invoking:
        #   with transaction:
        #       for sql, params in sql_params_list:
        #           transaction.execute_sql(sql, params, param_types)
        # which invokes more RPCs and is more costly.

        if parts.get('homogenous'):
            # The common case of multiple values being passed in
            # non-complex pyformat args and need to be uploaded in one RPC.
            return self._connection.in_transaction(
                self.__do_execute_insert_homogenous,
                parts,
            )
        else:
            # All the other cases that are esoteric and need
            #   transaction.execute_sql
            sql_params_list = parts.get('sql_params_list')
            return self._connection.in_transaction(
                self.__do_execute_insert_heterogenous,
                sql_params_list,
            )

    def __do_execute_insert_heterogenous(self, transaction, sql_params_list):
        for sql, params in sql_params_list:
            sql, params = sql_pyformat_args_to_spanner(sql, params)
            param_types = get_param_types(params)
            res = transaction.execute_sql(sql, params=params, param_types=param_types)
            # TODO: File a bug with Cloud Spanner and the Python client maintainers
            # about a lost commit when res isn't read from.
            _ = list(res)

    def __do_execute_insert_homogenous(self, transaction, parts):
        # Perform an insert in one shot.
        table = parts.get('table')
        columns = parts.get('columns')
        values = parts.get('values')
        return transaction.insert(table, columns, values)

    def __handle_DQL(self, sql, params):
        with self._connection.read_snapshot() as snapshot:
            # Reference
            #  https://googleapis.dev/python/spanner/latest/session-api.html#google.cloud.spanner_v1.session.Session.execute_sql
            sql, params = sql_pyformat_args_to_spanner(sql, params)
            res = snapshot.execute_sql(sql, params=params, param_types=get_param_types(params))
            if type(res) == int:
                self._row_count = res
                self._itr = None
            else:
                # Immediately using:
                #   iter(response)
                # here, because this Spanner API doesn't provide
                # easy mechanisms to detect when only a single item
                # is returned or many, yet mixing results that
                # are for .fetchone() with those that would result in
                # many items returns a RuntimeError if .fetchone() is
                # invoked and vice versa.
                self._res = res
                # Read the first element so that StreamedResult can
                # return the metadata after a DQL statement. See issue #155.
                self._itr = PeekIterator(self._res)
                # Unfortunately, Spanner doesn't seem to send back
                # information about the number of rows available.
                self._row_count = _UNSET_COUNT

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.__clear()

    def __clear(self):
        self._connection = None

    @property
    def description(self):
        if not (self._res and self._res.metadata):
            return None

        row_type = self._res.metadata.row_type
        columns = []
        for field in row_type.fields:
            columns.append(
                Column(
                    name=field.name,
                    type_code=field.type.code,
                    # Size of the SQL type of the column.
                    display_size=code_to_display_size.get(field.type.code),
                    # Client perceived size of the column.
                    internal_size=field.ByteSize(),
                )
            )
        return tuple(columns)

    @property
    def rowcount(self):
        return self._row_count

    def _raise_if_already_closed(self):
        """
        Raise an exception if attempting to use an already closed connection.
        """
        if self._closed:
            raise InterfaceError('cursor already closed')

    def close(self):
        self.__clear()
        self._closed = True

    def executemany(self, operation, seq_of_params):
        if not self._connection:
            raise ProgrammingError('Cursor is not connected to the database')

        for params in seq_of_params:
            self.execute(operation, params)

    def __next__(self):
        if self._itr is None:
            raise ProgrammingError('no results to return')
        return next(self._itr)

    def __iter__(self):
        if self._itr is None:
            raise ProgrammingError('no results to return')
        return self._itr

    def fetchone(self):
        self._raise_if_already_closed()

        try:
            return next(self)
        except StopIteration:
            return None

    def fetchall(self):
        self._raise_if_already_closed()

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
        self._raise_if_already_closed()

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

    def _run_prior_DDL_statements(self):
        return self._connection.run_prior_DDL_statements()

    def list_tables(self):
        return self._connection.list_tables()

    def run_sql_in_snapshot(self, sql):
        return self._connection.run_sql_in_snapshot(sql)

    def get_table_column_schema(self, table_name):
        return self._connection.get_table_column_schema(table_name)


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
            None if not self.display_size else "display_size=%d" % self.display_size,
            None if not self.internal_size else "internal_size=%d" % self.internal_size,
            None if not self.precision else "precision='%s'" % self.precision,
            None if not self.scale else "scale='%s'" % self.scale,
            None if not self.null_ok else "null_ok='%s'" % self.null_ok,
        ] if field])

        return 'Column(%s)' % rstr
