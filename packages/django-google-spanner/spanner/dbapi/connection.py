# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from .cursor import Cursor
from .exceptions import Error
from .periodic_auto_refresh import PeriodicAutoRefreshingTransaction


class Connection(object):
    def __init__(self, db_handle, session, discard_session):
        self.__sess = session
        self.__discard_session = discard_session
        self.__txn = None
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
        self.rollback()
        self.__clear()
        self.__closed = True

    def __enter__(self):
        return self

    def __clear(self):
        self.__dbhandle = None
        self.__discard_session()
        self.__sess = None

    def __exit__(self, etype, value, traceback):
        self.__raise_if_already_closed()

        self.run_prior_DDL_statements()

        if not etype:  # Not an exception thus we should commit.
            self.commit()
        else:  # An exception occured within the context so rollback.
            self.rollback()

        self.__clear()

    def __can_commit_or_rollback(self):
        # For now it is alright to access Transaction._rolled_back
        # even though it is unexported. We've filed a follow-up issue:
        #   https://github.com/googleapis/python-spanner/issues/13
        return self.__txn and not (self.__txn.committed or self.__txn._rolled_back)

    def commit(self):
        if self.__can_commit_or_rollback():
            res = self.__txn.commit()
            self.__txn = None
            return res
        elif hasattr(self.__txn, 'stop'):
            self.__txn.stop()

    def rollback(self):
        if self.__can_commit_or_rollback():
            res = self.__txn.rollback()
            self.__txn = None
            return res
        elif hasattr(self.__txn, 'stop'):
            self.__txn.stop()

    def cursor(self):
        self.__raise_if_already_closed()

        return Cursor(self)

    def discard_aborted_txn(self):
        # Discard the prior, now bad transaction.
        if hasattr(self.__txn, 'stop'):
            self.__txn.stop()
        self.__txn = None

    def get_txn(self):
        self.run_prior_DDL_statements()

        if not self.__txn:
            if True:  # An easy toggle for if we need to switch to plain Transactions.
                self.__txn = self.__sess.transaction()
            else:
                self.__txn = PeriodicAutoRefreshingTransaction(self.__sess.transaction())

            self.__txn.begin()

        # For now it is alright to access Transaction._rolled_back
        # even though it is unexported. We've filed a follow-up issue:
        #   https://github.com/googleapis/python-spanner/issues/13
        if self.__txn.committed or self.__txn._rolled_back:
            self.discard_aborted_txn()
            # Retry getting that transaction afresh.
            self.__txn = self.get_txn()

        return self.__txn

    def append_ddl_statement(self, ddl_statement):
        self.__ddl_statements.append(ddl_statement)

    def run_prior_DDL_statements(self):
        """
        Runs the list of saved Data Definition Language (DDL) statements on the underlying
        database. Note that each DDL statement MUST NOT contain a semicolon.

        Args:
            ddl_statements: a list of DDL statements, each without a semicolon.

        Returns:
            google.api_core.operation.Operation.result()
        """
        self.__raise_if_already_closed()

        if not self.__ddl_statements:
            return

        # DDL and Transactions in Cloud Spanner don't mix thus before any DDL is executed,
        # any prior transaction MUST have been committed. This behavior is also present
        # on MySQL. Please see:
        # * https://gist.github.com/odeke-em/8e02576d8523e07eb27b43a772aecc92
        # * https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html
        # * https://wiki.postgresql.org/wiki/Transactional_DDL_in_PostgreSQL:_A_Competitive_Analysis
        self.commit()

        ddl_statements = self.__ddl_statements
        self.__ddl_statements = []
        return self.__dbhandle.update_ddl(ddl_statements).result()

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

    def list_tables(self):
        # We CANNOT list tables with
        #   SELECT
        #     t.table_name
        #   FROM
        #     information_schema.tables AS t
        #   WHERE
        #     t.table_catalog = '' and t.table_schema = ''
        # with a transaction otherwise we get back:
        #   400 Unsupported concurrency mode in query using INFORMATION_SCHEMA.
        # hence this specialized method.
        self.run_prior_DDL_statements()

        with self.__dbhandle.snapshot() as snapshot:
            res = snapshot.execute_sql("""
             SELECT
              t.table_name
            FROM
              information_schema.tables AS t
            WHERE
              t.table_catalog = '' and t.table_schema = ''
            """)
            return list(res)
