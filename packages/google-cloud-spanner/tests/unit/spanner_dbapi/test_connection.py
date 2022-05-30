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

"""Cloud Spanner DB-API Connection class unit tests."""

import datetime
import mock
import unittest
import warnings

PROJECT = "test-project"
INSTANCE = "test-instance"
DATABASE = "test-database"
USER_AGENT = "user-agent"


def _make_credentials():
    from google.auth import credentials

    class _CredentialsWithScopes(credentials.Credentials, credentials.Scoped):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


class TestConnection(unittest.TestCase):
    def _get_client_info(self):
        from google.api_core.gapic_v1.client_info import ClientInfo

        return ClientInfo(user_agent=USER_AGENT)

    def _make_connection(self, **kwargs):
        from google.cloud.spanner_dbapi import Connection
        from google.cloud.spanner_v1.instance import Instance

        # We don't need a real Client object to test the constructor
        instance = Instance(INSTANCE, client=None)
        database = instance.database(DATABASE)
        return Connection(instance, database, **kwargs)

    @mock.patch("google.cloud.spanner_dbapi.connection.Connection.commit")
    def test_autocommit_setter_transaction_not_started(self, mock_commit):
        connection = self._make_connection()

        connection.autocommit = True

        mock_commit.assert_not_called()
        self.assertTrue(connection._autocommit)

        connection.autocommit = False
        mock_commit.assert_not_called()
        self.assertFalse(connection._autocommit)

    @mock.patch("google.cloud.spanner_dbapi.connection.Connection.commit")
    def test_autocommit_setter_transaction_started(self, mock_commit):
        connection = self._make_connection()
        connection._transaction = mock.Mock(committed=False, rolled_back=False)

        connection.autocommit = True

        mock_commit.assert_called_once()
        self.assertTrue(connection._autocommit)

    @mock.patch("google.cloud.spanner_dbapi.connection.Connection.commit")
    def test_autocommit_setter_transaction_started_commited_rolled_back(
        self, mock_commit
    ):
        connection = self._make_connection()

        connection._transaction = mock.Mock(committed=True, rolled_back=False)

        connection.autocommit = True
        mock_commit.assert_not_called()
        self.assertTrue(connection._autocommit)

        connection.autocommit = False

        connection._transaction = mock.Mock(committed=False, rolled_back=True)

        connection.autocommit = True
        mock_commit.assert_not_called()
        self.assertTrue(connection._autocommit)

    def test_property_database(self):
        from google.cloud.spanner_v1.database import Database

        connection = self._make_connection()
        self.assertIsInstance(connection.database, Database)
        self.assertEqual(connection.database, connection._database)

    def test_property_instance(self):
        from google.cloud.spanner_v1.instance import Instance

        connection = self._make_connection()
        self.assertIsInstance(connection.instance, Instance)
        self.assertEqual(connection.instance, connection._instance)

    def test_read_only_connection(self):
        connection = self._make_connection(read_only=True)
        self.assertTrue(connection.read_only)

        connection._transaction = mock.Mock(committed=False, rolled_back=False)
        with self.assertRaisesRegex(
            ValueError,
            "Connection read/write mode can't be changed while a transaction is in progress. "
            "Commit or rollback the current transaction and try again.",
        ):
            connection.read_only = False

        connection._transaction = None
        connection.read_only = False
        self.assertFalse(connection.read_only)

    def test_read_only_not_retried(self):
        """
        Testing the unlikely case of a read-only transaction
        failed with Aborted exception. In this case the
        transaction should not be automatically retried.
        """
        from google.api_core.exceptions import Aborted

        connection = self._make_connection(read_only=True)
        connection.retry_transaction = mock.Mock()

        cursor = connection.cursor()
        cursor._itr = mock.Mock(
            __next__=mock.Mock(
                side_effect=Aborted("Aborted"),
            )
        )

        cursor.fetchone()
        cursor.fetchall()
        cursor.fetchmany(5)

        connection.retry_transaction.assert_not_called()

    @staticmethod
    def _make_pool():
        from google.cloud.spanner_v1.pool import AbstractSessionPool

        return mock.create_autospec(AbstractSessionPool)

    @mock.patch("google.cloud.spanner_v1.database.Database")
    def test__session_checkout(self, mock_database):
        from google.cloud.spanner_dbapi import Connection

        pool = self._make_pool()
        mock_database._pool = pool
        connection = Connection(INSTANCE, mock_database)

        connection._session_checkout()
        pool.get.assert_called_once_with()
        self.assertEqual(connection._session, pool.get.return_value)

        connection._session = "db_session"
        connection._session_checkout()
        self.assertEqual(connection._session, "db_session")

    @mock.patch("google.cloud.spanner_v1.database.Database")
    def test__release_session(self, mock_database):
        from google.cloud.spanner_dbapi import Connection

        pool = self._make_pool()
        mock_database._pool = pool
        connection = Connection(INSTANCE, mock_database)
        connection._session = "session"

        connection._release_session()
        pool.put.assert_called_once_with("session")
        self.assertIsNone(connection._session)

    def test_transaction_checkout(self):
        from google.cloud.spanner_dbapi import Connection

        connection = Connection(INSTANCE, DATABASE)
        mock_checkout = mock.MagicMock(autospec=True)
        connection._session_checkout = mock_checkout

        connection.transaction_checkout()

        mock_checkout.assert_called_once_with()

        mock_transaction = mock.MagicMock()
        mock_transaction.committed = mock_transaction.rolled_back = False
        connection._transaction = mock_transaction

        self.assertEqual(connection.transaction_checkout(), mock_transaction)

        connection._autocommit = True
        self.assertIsNone(connection.transaction_checkout())

    def test_snapshot_checkout(self):
        from google.cloud.spanner_dbapi import Connection

        connection = Connection(INSTANCE, DATABASE, read_only=True)
        connection.autocommit = False

        session_checkout = mock.MagicMock(autospec=True)
        connection._session_checkout = session_checkout

        snapshot = connection.snapshot_checkout()
        session_checkout.assert_called_once()

        self.assertEqual(snapshot, connection.snapshot_checkout())

        connection.commit()
        self.assertIsNone(connection._snapshot)

        connection.snapshot_checkout()
        self.assertIsNotNone(connection._snapshot)

        connection.rollback()
        self.assertIsNone(connection._snapshot)

        connection.autocommit = True
        self.assertIsNone(connection.snapshot_checkout())

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_close(self, mock_client):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi import InterfaceError

        connection = connect("test-instance", "test-database")

        self.assertFalse(connection.is_closed)

        connection.close()

        self.assertTrue(connection.is_closed)

        with self.assertRaises(InterfaceError):
            connection.cursor()

        mock_transaction = mock.MagicMock()
        mock_transaction.committed = mock_transaction.rolled_back = False
        connection._transaction = mock_transaction

        mock_rollback = mock.MagicMock()
        mock_transaction.rollback = mock_rollback

        connection.close()

        mock_rollback.assert_called_once_with()

        connection._transaction = mock.MagicMock()
        connection._own_pool = False
        connection.close()

        self.assertTrue(connection.is_closed)

    @mock.patch.object(warnings, "warn")
    def test_commit(self, mock_warn):
        from google.cloud.spanner_dbapi import Connection
        from google.cloud.spanner_dbapi.connection import AUTOCOMMIT_MODE_WARNING

        connection = Connection(INSTANCE, DATABASE)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            connection.commit()

        mock_release.assert_not_called()

        connection._transaction = mock_transaction = mock.MagicMock(
            rolled_back=False, committed=False
        )
        mock_transaction.commit = mock_commit = mock.MagicMock()

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            connection.commit()

        mock_commit.assert_called_once_with()
        mock_release.assert_called_once_with()

        connection._autocommit = True
        connection.commit()
        mock_warn.assert_called_once_with(
            AUTOCOMMIT_MODE_WARNING, UserWarning, stacklevel=2
        )

    @mock.patch.object(warnings, "warn")
    def test_rollback(self, mock_warn):
        from google.cloud.spanner_dbapi import Connection
        from google.cloud.spanner_dbapi.connection import AUTOCOMMIT_MODE_WARNING

        connection = Connection(INSTANCE, DATABASE)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            connection.rollback()

        mock_release.assert_not_called()

        mock_transaction = mock.MagicMock()
        connection._transaction = mock_transaction
        mock_rollback = mock.MagicMock()
        mock_transaction.rollback = mock_rollback

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            connection.rollback()

        mock_rollback.assert_called_once_with()
        mock_release.assert_called_once_with()

        connection._autocommit = True
        connection.rollback()
        mock_warn.assert_called_once_with(
            AUTOCOMMIT_MODE_WARNING, UserWarning, stacklevel=2
        )

    @mock.patch("google.cloud.spanner_v1.database.Database", autospec=True)
    def test_run_prior_DDL_statements(self, mock_database):
        from google.cloud.spanner_dbapi import Connection, InterfaceError

        connection = Connection(INSTANCE, mock_database)

        connection.run_prior_DDL_statements()
        mock_database.update_ddl.assert_not_called()

        ddl = ["ddl"]
        connection._ddl_statements = ddl

        connection.run_prior_DDL_statements()
        mock_database.update_ddl.assert_called_once_with(ddl)

        connection.is_closed = True

        with self.assertRaises(InterfaceError):
            connection.run_prior_DDL_statements()

    def test_as_context_manager(self):
        connection = self._make_connection()
        with connection as conn:
            self.assertEqual(conn, connection)

        self.assertTrue(connection.is_closed)

    def test_run_statement_wo_retried(self):
        """Check that Connection remembers executed statements."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        sql = """SELECT 23 FROM table WHERE id = @a1"""
        params = {"a1": "value"}
        param_types = {"a1": str}

        connection = self._make_connection()
        connection.transaction_checkout = mock.Mock()
        statement = Statement(sql, params, param_types, ResultsChecksum(), False)
        connection.run_statement(statement)

        self.assertEqual(connection._statements[0].sql, sql)
        self.assertEqual(connection._statements[0].params, params)
        self.assertEqual(connection._statements[0].param_types, param_types)
        self.assertIsInstance(connection._statements[0].checksum, ResultsChecksum)

    def test_run_statement_w_retried(self):
        """Check that Connection doesn't remember re-executed statements."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        sql = """SELECT 23 FROM table WHERE id = @a1"""
        params = {"a1": "value"}
        param_types = {"a1": str}

        connection = self._make_connection()
        connection.transaction_checkout = mock.Mock()
        statement = Statement(sql, params, param_types, ResultsChecksum(), False)
        connection.run_statement(statement, retried=True)

        self.assertEqual(len(connection._statements), 0)

    def test_run_statement_w_heterogenous_insert_statements(self):
        """Check that Connection executed heterogenous insert statements."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement
        from google.rpc.status_pb2 import Status
        from google.rpc.code_pb2 import OK

        sql = "INSERT INTO T (f1, f2) VALUES (1, 2)"
        params = None
        param_types = None

        connection = self._make_connection()
        transaction = mock.MagicMock()
        connection.transaction_checkout = mock.Mock(return_value=transaction)
        transaction.batch_update = mock.Mock(return_value=(Status(code=OK), 1))
        statement = Statement(sql, params, param_types, ResultsChecksum(), True)

        connection.run_statement(statement, retried=True)

        self.assertEqual(len(connection._statements), 0)

    def test_run_statement_w_homogeneous_insert_statements(self):
        """Check that Connection executed homogeneous insert statements."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement
        from google.rpc.status_pb2 import Status
        from google.rpc.code_pb2 import OK

        sql = "INSERT INTO T (f1, f2) VALUES (%s, %s), (%s, %s)"
        params = ["a", "b", "c", "d"]
        param_types = {"f1": str, "f2": str}

        connection = self._make_connection()
        transaction = mock.MagicMock()
        connection.transaction_checkout = mock.Mock(return_value=transaction)
        transaction.batch_update = mock.Mock(return_value=(Status(code=OK), 1))
        statement = Statement(sql, params, param_types, ResultsChecksum(), True)

        connection.run_statement(statement, retried=True)

        self.assertEqual(len(connection._statements), 0)

    @mock.patch("google.cloud.spanner_v1.transaction.Transaction")
    def test_commit_clears_statements(self, mock_transaction):
        """
        Check that all the saved statements are
        cleared, when the transaction is commited.
        """
        connection = self._make_connection()
        connection._transaction = mock.Mock(rolled_back=False, committed=False)
        connection._statements = [{}, {}]

        self.assertEqual(len(connection._statements), 2)

        connection.commit()

        self.assertEqual(len(connection._statements), 0)

    @mock.patch("google.cloud.spanner_v1.transaction.Transaction")
    def test_rollback_clears_statements(self, mock_transaction):
        """
        Check that all the saved statements are
        cleared, when the transaction is roll backed.
        """
        connection = self._make_connection()
        connection._transaction = mock.Mock()
        connection._statements = [{}, {}]

        self.assertEqual(len(connection._statements), 2)

        connection.rollback()

        self.assertEqual(len(connection._statements), 0)

    def test_retry_transaction_w_checksum_match(self):
        """Check retrying an aborted transaction."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]
        connection = self._make_connection()
        checksum = ResultsChecksum()
        checksum.consume_result(row)

        retried_checkum = ResultsChecksum()
        run_mock = connection.run_statement = mock.Mock()
        run_mock.return_value = ([row], retried_checkum)

        statement = Statement("SELECT 1", [], {}, checksum, False)
        connection._statements.append(statement)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection._compare_checksums"
        ) as compare_mock:
            connection.retry_transaction()

        compare_mock.assert_called_with(checksum, retried_checkum)
        run_mock.assert_called_with(statement, retried=True)

    def test_retry_transaction_w_checksum_mismatch(self):
        """
        Check retrying an aborted transaction
        with results checksums mismatch.
        """
        from google.cloud.spanner_dbapi.exceptions import RetryAborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]
        retried_row = ["field3", "field4"]
        connection = self._make_connection()

        checksum = ResultsChecksum()
        checksum.consume_result(row)
        retried_checkum = ResultsChecksum()
        run_mock = connection.run_statement = mock.Mock()
        run_mock.return_value = ([retried_row], retried_checkum)

        statement = Statement("SELECT 1", [], {}, checksum, False)
        connection._statements.append(statement)

        with self.assertRaises(RetryAborted):
            connection.retry_transaction()

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_commit_retry_aborted_statements(self, mock_client):
        """Check that retried transaction executing the same statements."""
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()
        cursor._checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, cursor._checksum, False)
        connection._statements.append(statement)
        mock_transaction = mock.Mock(rolled_back=False, committed=False)
        connection._transaction = mock_transaction
        mock_transaction.commit.side_effect = [Aborted("Aborted"), None]
        run_mock = connection.run_statement = mock.Mock()
        run_mock.return_value = ([row], ResultsChecksum())

        connection.commit()

        run_mock.assert_called_with(statement, retried=True)

    def test_retry_transaction_drop_transaction(self):
        """
        Check that before retrying an aborted transaction
        connection drops the original aborted transaction.
        """
        connection = self._make_connection()
        transaction_mock = mock.Mock()
        connection._transaction = transaction_mock

        # as we didn't set any statements, the method
        # will only drop the transaction object
        connection.retry_transaction()
        self.assertIsNone(connection._transaction)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_retry_aborted_retry(self, mock_client):
        """
        Check that in case of a retried transaction failed,
        the connection will retry it once again.
        """
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()
        cursor._checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, cursor._checksum, False)
        connection._statements.append(statement)
        metadata_mock = mock.Mock()
        metadata_mock.trailing_metadata.return_value = {}
        run_mock = connection.run_statement = mock.Mock()
        run_mock.side_effect = [
            Aborted("Aborted", errors=[metadata_mock]),
            ([row], ResultsChecksum()),
        ]

        connection.retry_transaction()

        run_mock.assert_has_calls(
            (
                mock.call(statement, retried=True),
                mock.call(statement, retried=True),
            )
        )

    def test_retry_transaction_raise_max_internal_retries(self):
        """Check retrying raise an error of max internal retries."""
        from google.cloud.spanner_dbapi import connection as conn
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        conn.MAX_INTERNAL_RETRIES = 0
        row = ["field1", "field2"]
        connection = self._make_connection()

        checksum = ResultsChecksum()
        checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, checksum, False)
        connection._statements.append(statement)

        with self.assertRaises(Exception):
            connection.retry_transaction()

        conn.MAX_INTERNAL_RETRIES = 50

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_retry_aborted_retry_without_delay(self, mock_client):
        """
        Check that in case of a retried transaction failed,
        the connection will retry it once again.
        """
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()
        cursor._checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, cursor._checksum, False)
        connection._statements.append(statement)
        metadata_mock = mock.Mock()
        metadata_mock.trailing_metadata.return_value = {}
        run_mock = connection.run_statement = mock.Mock()
        run_mock.side_effect = [
            Aborted("Aborted", errors=[metadata_mock]),
            ([row], ResultsChecksum()),
        ]
        connection._get_retry_delay = mock.Mock(return_value=False)

        connection.retry_transaction()

        run_mock.assert_has_calls(
            (
                mock.call(statement, retried=True),
                mock.call(statement, retried=True),
            )
        )

    def test_retry_transaction_w_multiple_statement(self):
        """Check retrying an aborted transaction."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]
        connection = self._make_connection()

        checksum = ResultsChecksum()
        checksum.consume_result(row)
        retried_checkum = ResultsChecksum()

        statement = Statement("SELECT 1", [], {}, checksum, False)
        statement1 = Statement("SELECT 2", [], {}, checksum, False)
        connection._statements.append(statement)
        connection._statements.append(statement1)
        run_mock = connection.run_statement = mock.Mock()
        run_mock.return_value = ([row], retried_checkum)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection._compare_checksums"
        ) as compare_mock:
            connection.retry_transaction()

        compare_mock.assert_called_with(checksum, retried_checkum)

        run_mock.assert_called_with(statement1, retried=True)

    def test_retry_transaction_w_empty_response(self):
        """Check retrying an aborted transaction."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        row = []
        connection = self._make_connection()

        checksum = ResultsChecksum()
        checksum.count = 1
        retried_checkum = ResultsChecksum()

        statement = Statement("SELECT 1", [], {}, checksum, False)
        connection._statements.append(statement)
        run_mock = connection.run_statement = mock.Mock()
        run_mock.return_value = ([row], retried_checkum)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection._compare_checksums"
        ) as compare_mock:
            connection.retry_transaction()

        compare_mock.assert_called_with(checksum, retried_checkum)

        run_mock.assert_called_with(statement, retried=True)

    def test_validate_ok(self):
        connection = self._make_connection()

        # mock snapshot context manager
        snapshot_obj = mock.Mock()
        snapshot_obj.execute_sql = mock.Mock(return_value=[[1]])

        snapshot_ctx = mock.Mock()
        snapshot_ctx.__enter__ = mock.Mock(return_value=snapshot_obj)
        snapshot_ctx.__exit__ = exit_ctx_func
        snapshot_method = mock.Mock(return_value=snapshot_ctx)

        connection.database.snapshot = snapshot_method

        connection.validate()
        snapshot_obj.execute_sql.assert_called_once_with("SELECT 1")

    def test_validate_fail(self):
        from google.cloud.spanner_dbapi.exceptions import OperationalError

        connection = self._make_connection()

        # mock snapshot context manager
        snapshot_obj = mock.Mock()
        snapshot_obj.execute_sql = mock.Mock(return_value=[[3]])

        snapshot_ctx = mock.Mock()
        snapshot_ctx.__enter__ = mock.Mock(return_value=snapshot_obj)
        snapshot_ctx.__exit__ = exit_ctx_func
        snapshot_method = mock.Mock(return_value=snapshot_ctx)

        connection.database.snapshot = snapshot_method

        with self.assertRaises(OperationalError):
            connection.validate()

        snapshot_obj.execute_sql.assert_called_once_with("SELECT 1")

    def test_validate_error(self):
        from google.cloud.exceptions import NotFound

        connection = self._make_connection()

        # mock snapshot context manager
        snapshot_obj = mock.Mock()
        snapshot_obj.execute_sql = mock.Mock(side_effect=NotFound("Not found"))

        snapshot_ctx = mock.Mock()
        snapshot_ctx.__enter__ = mock.Mock(return_value=snapshot_obj)
        snapshot_ctx.__exit__ = exit_ctx_func
        snapshot_method = mock.Mock(return_value=snapshot_ctx)

        connection.database.snapshot = snapshot_method

        with self.assertRaises(NotFound):
            connection.validate()

        snapshot_obj.execute_sql.assert_called_once_with("SELECT 1")

    def test_validate_closed(self):
        from google.cloud.spanner_dbapi.exceptions import InterfaceError

        connection = self._make_connection()
        connection.close()

        with self.assertRaises(InterfaceError):
            connection.validate()

    def test_staleness_invalid_value(self):
        """Check that `staleness` property accepts only correct values."""
        connection = self._make_connection()

        # incorrect staleness type
        with self.assertRaises(ValueError):
            connection.staleness = {"something": 4}

        # no expected staleness types
        with self.assertRaises(ValueError):
            connection.staleness = {}

    def test_staleness_inside_transaction(self):
        """
        Check that it's impossible to change the `staleness`
        option if a transaction is in progress.
        """
        connection = self._make_connection()
        connection._transaction = mock.Mock(committed=False, rolled_back=False)

        with self.assertRaises(ValueError):
            connection.staleness = {"read_timestamp": datetime.datetime(2021, 9, 21)}

    def test_staleness_multi_use(self):
        """
        Check that `staleness` option is correctly
        sent to the `Snapshot()` constructor.

        READ_ONLY, NOT AUTOCOMMIT
        """
        timestamp = datetime.datetime(2021, 9, 20)

        connection = self._make_connection()
        connection._session = "session"
        connection.read_only = True
        connection.staleness = {"read_timestamp": timestamp}

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Snapshot"
        ) as snapshot_mock:
            connection.snapshot_checkout()

        snapshot_mock.assert_called_with(
            "session", multi_use=True, read_timestamp=timestamp
        )

    def test_staleness_single_use_autocommit(self):
        """
        Check that `staleness` option is correctly
        sent to the snapshot context manager.

        NOT READ_ONLY, AUTOCOMMIT
        """
        timestamp = datetime.datetime(2021, 9, 20)

        connection = self._make_connection()
        connection._session_checkout = mock.MagicMock(autospec=True)

        connection.autocommit = True
        connection.staleness = {"read_timestamp": timestamp}

        # mock snapshot context manager
        snapshot_obj = mock.Mock()
        snapshot_obj.execute_sql = mock.Mock(return_value=[1])

        snapshot_ctx = mock.Mock()
        snapshot_ctx.__enter__ = mock.Mock(return_value=snapshot_obj)
        snapshot_ctx.__exit__ = exit_ctx_func
        snapshot_method = mock.Mock(return_value=snapshot_ctx)

        connection.database.snapshot = snapshot_method

        cursor = connection.cursor()
        cursor.execute("SELECT 1")

        connection.database.snapshot.assert_called_with(read_timestamp=timestamp)

    def test_staleness_single_use_readonly_autocommit(self):
        """
        Check that `staleness` option is correctly sent to the
        snapshot context manager while in `autocommit` mode.

        READ_ONLY, AUTOCOMMIT
        """
        timestamp = datetime.datetime(2021, 9, 20)

        connection = self._make_connection()
        connection.autocommit = True
        connection.read_only = True
        connection._session_checkout = mock.MagicMock(autospec=True)

        connection.staleness = {"read_timestamp": timestamp}

        # mock snapshot context manager
        snapshot_obj = mock.Mock()
        snapshot_obj.execute_sql = mock.Mock(return_value=[1])

        snapshot_ctx = mock.Mock()
        snapshot_ctx.__enter__ = mock.Mock(return_value=snapshot_obj)
        snapshot_ctx.__exit__ = exit_ctx_func
        snapshot_method = mock.Mock(return_value=snapshot_ctx)

        connection.database.snapshot = snapshot_method

        cursor = connection.cursor()
        cursor.execute("SELECT 1")

        connection.database.snapshot.assert_called_with(read_timestamp=timestamp)


def exit_ctx_func(self, exc_type, exc_value, traceback):
    """Context __exit__ method mock."""
    pass
