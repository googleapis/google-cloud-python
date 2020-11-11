# Copyright 2020 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Database cursor for Google Cloud Spanner DB-API."""

from google.api_core.exceptions import AlreadyExists
from google.api_core.exceptions import FailedPrecondition
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import InvalidArgument

from collections import namedtuple

from google.cloud import spanner_v1 as spanner

from google.cloud.spanner_dbapi.exceptions import IntegrityError
from google.cloud.spanner_dbapi.exceptions import InterfaceError
from google.cloud.spanner_dbapi.exceptions import OperationalError
from google.cloud.spanner_dbapi.exceptions import ProgrammingError

from google.cloud.spanner_dbapi import _helpers
from google.cloud.spanner_dbapi._helpers import ColumnInfo
from google.cloud.spanner_dbapi._helpers import code_to_display_size

from google.cloud.spanner_dbapi import parse_utils
from google.cloud.spanner_dbapi.parse_utils import get_param_types
from google.cloud.spanner_dbapi.utils import PeekIterator

_UNSET_COUNT = -1

ColumnDetails = namedtuple("column_details", ["null_ok", "spanner_type"])


class Cursor(object):
    """Database cursor to manage the context of a fetch operation.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: A DB-API connection to Google Cloud Spanner.
    """

    def __init__(self, connection):
        self._itr = None
        self._result_set = None
        self._row_count = _UNSET_COUNT
        self.connection = connection
        self._is_closed = False

        # the number of rows to fetch at a time with fetchmany()
        self.arraysize = 1

    @property
    def is_closed(self):
        """The cursor close indicator.

        :rtype: bool
        :returns: True if the cursor or the parent connection is closed,
                  otherwise False.
        """
        return self._is_closed or self.connection.is_closed

    @property
    def description(self):
        """Read-only attribute containing a sequence of the following items:

        -   ``name``
        -   ``type_code``
        -   ``display_size``
        -   ``internal_size``
        -   ``precision``
        -   ``scale``
        -   ``null_ok``
        """
        if not (self._result_set and self._result_set.metadata):
            return None

        row_type = self._result_set.metadata.row_type
        columns = []

        for field in row_type.fields:
            column_info = ColumnInfo(
                name=field.name,
                type_code=field.type.code,
                # Size of the SQL type of the column.
                display_size=code_to_display_size.get(field.type.code),
                # Client perceived size of the column.
                internal_size=field.ByteSize(),
            )
            columns.append(column_info)

        return tuple(columns)

    @property
    def rowcount(self):
        """The number of rows produced by the last `.execute()`."""
        return self._row_count

    def _raise_if_closed(self):
        """Raise an exception if this cursor is closed.

        Helper to check this cursor's state before running a
        SQL/DDL/DML query. If the parent connection is
        already closed it also raises an error.

        :raises: :class:`InterfaceError` if this cursor is closed.
        """
        if self.is_closed:
            raise InterfaceError("Cursor and/or connection is already closed.")

    def callproc(self, procname, args=None):
        """A no-op, raising an error if the cursor or connection is closed."""
        self._raise_if_closed()

    def close(self):
        """Closes this Cursor, making it unusable from this point forward."""
        self._is_closed = True

    def _do_execute_update(self, transaction, sql, params, param_types=None):
        sql = parse_utils.ensure_where_clause(sql)
        sql, params = parse_utils.sql_pyformat_args_to_spanner(sql, params)

        result = transaction.execute_update(
            sql, params=params, param_types=get_param_types(params)
        )
        self._itr = None
        if type(result) == int:
            self._row_count = result

        return result

    def execute(self, sql, args=None):
        """Prepares and executes a Spanner database operation.

        :type sql: str
        :param sql: A SQL query statement.

        :type args: list
        :param args: Additional parameters to supplement the SQL query.
        """
        if not self.connection:
            raise ProgrammingError("Cursor is not connected to the database")

        self._raise_if_closed()

        self._result_set = None

        # Classify whether this is a read-only SQL statement.
        try:
            classification = parse_utils.classify_stmt(sql)
            if classification == parse_utils.STMT_DDL:
                self.connection._ddl_statements.append(sql)
                return

            # For every other operation, we've got to ensure that
            # any prior DDL statements were run.
            # self._run_prior_DDL_statements()
            self.connection.run_prior_DDL_statements()

            if not self.connection.autocommit:
                transaction = self.connection.transaction_checkout()

                sql, params = parse_utils.sql_pyformat_args_to_spanner(sql, args)

                self._result_set = transaction.execute_sql(
                    sql, params, param_types=get_param_types(params)
                )
                self._itr = PeekIterator(self._result_set)
                return

            if classification == parse_utils.STMT_NON_UPDATING:
                self._handle_DQL(sql, args or None)
            elif classification == parse_utils.STMT_INSERT:
                _helpers.handle_insert(self.connection, sql, args or None)
            else:
                self.connection.database.run_in_transaction(
                    self._do_execute_update, sql, args or None
                )
        except (AlreadyExists, FailedPrecondition) as e:
            raise IntegrityError(e.details if hasattr(e, "details") else e)
        except InvalidArgument as e:
            raise ProgrammingError(e.details if hasattr(e, "details") else e)
        except InternalServerError as e:
            raise OperationalError(e.details if hasattr(e, "details") else e)

    def executemany(self, operation, seq_of_params):
        """Execute the given SQL with every parameters set
        from the given sequence of parameters.

        :type operation: str
        :param operation: SQL code to execute.

        :type seq_of_params: list
        :param seq_of_params: Sequence of additional parameters to run
                              the query with.
        """
        self._raise_if_closed()

        for params in seq_of_params:
            self.execute(operation, params)

    def fetchone(self):
        """Fetch the next row of a query result set, returning a single
        sequence, or None when no more data is available."""
        self._raise_if_closed()

        try:
            return next(self)
        except StopIteration:
            return None

    def fetchmany(self, size=None):
        """Fetch the next set of rows of a query result, returning a sequence
        of sequences. An empty sequence is returned when no more rows are available.

        :type size: int
        :param size: (Optional) The maximum number of results to fetch.

        :raises InterfaceError:
            if the previous call to .execute*() did not produce any result set
            or if no call was issued yet.
        """
        self._raise_if_closed()

        if size is None:
            size = self.arraysize

        items = []
        for i in range(size):
            try:
                items.append(tuple(self.__next__()))
            except StopIteration:
                break

        return items

    def fetchall(self):
        """Fetch all (remaining) rows of a query result, returning them as
        a sequence of sequences.
        """
        self._raise_if_closed()

        return list(self.__iter__())

    def nextset(self):
        """A no-op, raising an error if the cursor or connection is closed."""
        self._raise_if_closed()

    def setinputsizes(self, sizes):
        """A no-op, raising an error if the cursor or connection is closed."""
        self._raise_if_closed()

    def setoutputsize(self, size, column=None):
        """A no-op, raising an error if the cursor or connection is closed."""
        self._raise_if_closed()

    def _handle_DQL(self, sql, params):
        with self.connection.database.snapshot() as snapshot:
            # Reference
            #  https://googleapis.dev/python/spanner/latest/session-api.html#google.cloud.spanner_v1.session.Session.execute_sql
            sql, params = parse_utils.sql_pyformat_args_to_spanner(sql, params)
            res = snapshot.execute_sql(
                sql, params=params, param_types=get_param_types(params)
            )
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
                self._result_set = res
                # Read the first element so that the StreamedResultSet can
                # return the metadata after a DQL statement. See issue #155.
                self._itr = PeekIterator(self._result_set)
                # Unfortunately, Spanner doesn't seem to send back
                # information about the number of rows available.
                self._row_count = _UNSET_COUNT

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.close()

    def __next__(self):
        if self._itr is None:
            raise ProgrammingError("no results to return")
        return next(self._itr)

    def __iter__(self):
        if self._itr is None:
            raise ProgrammingError("no results to return")
        return self._itr

    def list_tables(self):
        return self.run_sql_in_snapshot(_helpers.SQL_LIST_TABLES)

    def run_sql_in_snapshot(self, sql, params=None, param_types=None):
        # Some SQL e.g. for INFORMATION_SCHEMA cannot be run in read-write transactions
        # hence this method exists to circumvent that limit.
        self.connection.run_prior_DDL_statements()

        with self.connection.database.snapshot() as snapshot:
            res = snapshot.execute_sql(sql, params=params, param_types=param_types)
            return list(res)

    def get_table_column_schema(self, table_name):
        rows = self.run_sql_in_snapshot(
            sql=_helpers.SQL_GET_TABLE_COLUMN_SCHEMA,
            params={"table_name": table_name},
            param_types={"table_name": spanner.param_types.STRING},
        )

        column_details = {}
        for column_name, is_nullable, spanner_type in rows:
            column_details[column_name] = ColumnDetails(
                null_ok=is_nullable == "YES", spanner_type=spanner_type
            )
        return column_details
