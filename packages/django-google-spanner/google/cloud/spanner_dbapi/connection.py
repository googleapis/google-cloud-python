# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""Cloud Spanner DB connection object."""

from collections import namedtuple
import warnings

from google.cloud import spanner_v1

from .cursor import Cursor
from .exceptions import InterfaceError

AUTOCOMMIT_MODE_WARNING = "This method is non-operational in autocommit mode"

ColumnDetails = namedtuple("column_details", ["null_ok", "spanner_type"])


class Connection:
    """Representation of a connection to a Cloud Spanner database.

    You most likely don't need to instantiate `Connection` objects
    directly, use the `connect` module function instead.

    :type instance: :class:`~google.cloud.spanner_v1.instance.Instance`
    :param instance: Cloud Spanner instance to connect to.

    :type database: :class:`~google.cloud.spanner_v1.database.Database`
    :param database: Cloud Spanner database to connect to.
    """

    def __init__(self, instance, database):
        self._instance = instance
        self._database = database

        self._ddl_statements = []
        self._transaction = None
        self._session = None

        self.is_closed = False
        self._autocommit = False

    @property
    def autocommit(self):
        """Autocommit mode flag for this connection.

        :rtype: bool
        :returns: Autocommit mode flag value.
        """
        return self._autocommit

    @autocommit.setter
    def autocommit(self, value):
        """Change this connection autocommit mode.

        :type value: bool
        :param value: New autocommit mode state.
        """
        if value and not self._autocommit:
            self.commit()

        self._autocommit = value

    @property
    def database(self):
        """Database to which this connection relates.

        :rtype: :class:`~google.cloud.spanner_v1.database.Database`
        :returns: The related database object.
        """
        return self._database

    @property
    def instance(self):
        """Instance to which this connection relates.

        :rtype: :class:`~google.cloud.spanner_v1.instance.Instance`
        :returns: The related instance object.
        """
        return self._instance

    def _session_checkout(self):
        """Get a Cloud Spanner session from the pool.

        If there is already a session associated with
        this connection, it'll be used instead.

        :rtype: :class:`google.cloud.spanner_v1.session.Session`
        :returns: Cloud Spanner session object ready to use.
        """
        if not self._session:
            self._session = self.database._pool.get()

        return self._session

    def _release_session(self):
        """Release the currently used Spanner session.

        The session will be returned into the sessions pool.
        """
        self.database._pool.put(self._session)
        self._session = None

    def transaction_checkout(self):
        """Get a Cloud Spanner transaction.

        Begin a new transaction, if there is no transaction in
        this connection yet. Return the begun one otherwise.

        The method is non operational in autocommit mode.

        :rtype: :class:`google.cloud.spanner_v1.transaction.Transaction`
        :returns: A Cloud Spanner transaction object, ready to use.
        """
        if not self.autocommit:
            if (
                not self._transaction
                or self._transaction.committed
                or self._transaction.rolled_back
            ):
                self._transaction = self._session_checkout().transaction()
                self._transaction.begin()

            return self._transaction

    def cursor(self):
        self._raise_if_closed()

        return Cursor(self)

    def _raise_if_closed(self):
        """Raise an exception if this connection is closed.

        Helper to check the connection state before
        running a SQL/DDL/DML query.

        :raises: :class:`InterfaceError` if this connection is closed.
        """
        if self.is_closed:
            raise InterfaceError("connection is already closed")

    def __handle_update_ddl(self, ddl_statements):
        """
        Run the list of Data Definition Language (DDL) statements on the underlying
        database. Each DDL statement MUST NOT contain a semicolon.
        Args:
            ddl_statements: a list of DDL statements, each without a semicolon.
        Returns:
            google.api_core.operation.Operation.result()
        """
        self._raise_if_closed()
        # Synchronously wait on the operation's completion.
        return self.database.update_ddl(ddl_statements).result()

    def read_snapshot(self):
        self._raise_if_closed()
        return self.database.snapshot()

    def in_transaction(self, fn, *args, **kwargs):
        self._raise_if_closed()
        return self.database.run_in_transaction(fn, *args, **kwargs)

    def append_ddl_statement(self, ddl_statement):
        self._raise_if_closed()
        self._ddl_statements.append(ddl_statement)

    def run_prior_DDL_statements(self):
        self._raise_if_closed()

        if not self._ddl_statements:
            return

        ddl_statements = self._ddl_statements
        self._ddl_statements = []

        return self.__handle_update_ddl(ddl_statements)

    def list_tables(self):
        return self.run_sql_in_snapshot(
            """
            SELECT
              t.table_name
            FROM
              information_schema.tables AS t
            WHERE
              t.table_catalog = '' and t.table_schema = ''
            """
        )

    def run_sql_in_snapshot(self, sql, params=None, param_types=None):
        # Some SQL e.g. for INFORMATION_SCHEMA cannot be run in read-write transactions
        # hence this method exists to circumvent that limit.
        self.run_prior_DDL_statements()

        with self.database.snapshot() as snapshot:
            res = snapshot.execute_sql(
                sql, params=params, param_types=param_types
            )
            return list(res)

    def get_table_column_schema(self, table_name):
        rows = self.run_sql_in_snapshot(
            """SELECT
                COLUMN_NAME, IS_NULLABLE, SPANNER_TYPE
            FROM
                INFORMATION_SCHEMA.COLUMNS
            WHERE
                TABLE_SCHEMA = ''
            AND
                TABLE_NAME = @table_name""",
            params={"table_name": table_name},
            param_types={"table_name": spanner_v1.param_types.STRING},
        )

        column_details = {}
        for column_name, is_nullable, spanner_type in rows:
            column_details[column_name] = ColumnDetails(
                null_ok=is_nullable == "YES", spanner_type=spanner_type
            )
        return column_details

    def close(self):
        """Close this connection.

        The connection will be unusable from this point forward. If the
        connection has an active transaction, it will be rolled back.
        """
        if (
            self._transaction
            and not self._transaction.committed
            and not self._transaction.rolled_back
        ):
            self._transaction.rollback()

        self.is_closed = True

    def commit(self):
        """Commit all the pending transactions."""
        if self.autocommit:
            warnings.warn(AUTOCOMMIT_MODE_WARNING, UserWarning, stacklevel=2)
        elif self._transaction:
            self._transaction.commit()
            self._release_session()

    def rollback(self):
        """Rollback all the pending transactions."""
        if self.autocommit:
            warnings.warn(AUTOCOMMIT_MODE_WARNING, UserWarning, stacklevel=2)
        elif self._transaction:
            self._transaction.rollback()
            self._release_session()

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.commit()
        self.close()
