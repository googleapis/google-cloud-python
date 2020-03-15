# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import google.api_core.exceptions as grpc_exceptions

from .base_cursor import BaseCursor
from .exceptions import (
    Error, IntegrityError, OperationalError, ProgrammingError,
)
from .parse_utils import (
    STMT_DDL, STMT_INSERT, STMT_NON_UPDATING, classify_stmt,
    ensure_where_clause, get_param_types, parse_insert,
    sql_pyformat_args_to_spanner,
)
from .utils import PeekIterator

_UNSET_COUNT = -1


class Cursor(BaseCursor):
    def _raise_if_already_closed(self):
        """
        Raises an exception if attempting to use an already closed connection.
        """
        if self._closed:
            raise Error('attempting to use an already closed connection')

    def close(self):
        self.__clear()
        self._closed = True

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

    def executemany(self, operation, seq_of_params):
        self._raise_if_already_closed()

        if not self._connection:
            raise ProgrammingError('Cursor is not connected to the database')

        raise ProgrammingError('Unimplemented')
