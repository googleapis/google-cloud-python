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

import mock
import unittest
import warnings


def _make_credentials():
    from google.auth import credentials

    class _CredentialsWithScopes(credentials.Credentials, credentials.Scoped):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


class TestConnection(unittest.TestCase):

    PROJECT = "test-project"
    INSTANCE = "test-instance"
    DATABASE = "test-database"
    USER_AGENT = "user-agent"
    CREDENTIALS = _make_credentials()

    def _get_client_info(self):
        from google.api_core.gapic_v1.client_info import ClientInfo

        return ClientInfo(user_agent=self.USER_AGENT)

    def _make_connection(self):
        from google.cloud.spanner_dbapi import Connection
        from google.cloud.spanner_v1.instance import Instance

        # We don't need a real Client object to test the constructor
        instance = Instance(self.INSTANCE, client=None)
        database = instance.database(self.DATABASE)
        return Connection(instance, database)

    def test_autocommit_setter_transaction_not_started(self):
        connection = self._make_connection()

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.commit"
        ) as mock_commit:
            connection.autocommit = True
            mock_commit.assert_not_called()
            self.assertTrue(connection._autocommit)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.commit"
        ) as mock_commit:
            connection.autocommit = False
            mock_commit.assert_not_called()
            self.assertFalse(connection._autocommit)

    def test_autocommit_setter_transaction_started(self):
        connection = self._make_connection()

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.commit"
        ) as mock_commit:
            connection._transaction = mock.Mock(committed=False, rolled_back=False)

            connection.autocommit = True
            mock_commit.assert_called_once()
            self.assertTrue(connection._autocommit)

    def test_autocommit_setter_transaction_started_commited_rolled_back(self):
        connection = self._make_connection()

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.commit"
        ) as mock_commit:
            connection._transaction = mock.Mock(committed=True, rolled_back=False)

            connection.autocommit = True
            mock_commit.assert_not_called()
            self.assertTrue(connection._autocommit)

        connection.autocommit = False

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.commit"
        ) as mock_commit:
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

    def test__session_checkout(self):
        from google.cloud.spanner_dbapi import Connection

        with mock.patch("google.cloud.spanner_v1.database.Database") as mock_database:
            mock_database._pool = mock.MagicMock()
            mock_database._pool.get = mock.MagicMock(return_value="db_session_pool")
            connection = Connection(self.INSTANCE, mock_database)

            connection._session_checkout()
            mock_database._pool.get.assert_called_once_with()
            self.assertEqual(connection._session, "db_session_pool")

            connection._session = "db_session"
            connection._session_checkout()
            self.assertEqual(connection._session, "db_session")

    def test__release_session(self):
        from google.cloud.spanner_dbapi import Connection

        with mock.patch("google.cloud.spanner_v1.database.Database") as mock_database:
            mock_database._pool = mock.MagicMock()
            mock_database._pool.put = mock.MagicMock()
            connection = Connection(self.INSTANCE, mock_database)
            connection._session = "session"

            connection._release_session()
            mock_database._pool.put.assert_called_once_with("session")
            self.assertIsNone(connection._session)

    def test_transaction_checkout(self):
        from google.cloud.spanner_dbapi import Connection

        connection = Connection(self.INSTANCE, self.DATABASE)
        connection._session_checkout = mock_checkout = mock.MagicMock(autospec=True)
        connection.transaction_checkout()
        mock_checkout.assert_called_once_with()

        connection._transaction = mock_transaction = mock.MagicMock()
        mock_transaction.committed = mock_transaction.rolled_back = False
        self.assertEqual(connection.transaction_checkout(), mock_transaction)

        connection._autocommit = True
        self.assertIsNone(connection.transaction_checkout())

    def test_close(self):
        from google.cloud.spanner_dbapi import connect, InterfaceError

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=True
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists", return_value=True
            ):
                connection = connect("test-instance", "test-database")

        self.assertFalse(connection.is_closed)
        connection.close()
        self.assertTrue(connection.is_closed)

        with self.assertRaises(InterfaceError):
            connection.cursor()

        connection._transaction = mock_transaction = mock.MagicMock()
        mock_transaction.committed = mock_transaction.rolled_back = False
        mock_transaction.rollback = mock_rollback = mock.MagicMock()
        connection.close()
        mock_rollback.assert_called_once_with()

    @mock.patch.object(warnings, "warn")
    def test_commit(self, mock_warn):
        from google.cloud.spanner_dbapi import Connection
        from google.cloud.spanner_dbapi.connection import AUTOCOMMIT_MODE_WARNING

        connection = Connection(self.INSTANCE, self.DATABASE)

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

        connection = Connection(self.INSTANCE, self.DATABASE)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            connection.rollback()
            mock_release.assert_not_called()

        connection._transaction = mock_transaction = mock.MagicMock()
        mock_transaction.rollback = mock_rollback = mock.MagicMock()

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

    def test_run_prior_DDL_statements(self):
        from google.cloud.spanner_dbapi import Connection, InterfaceError

        with mock.patch(
            "google.cloud.spanner_v1.database.Database", autospec=True
        ) as mock_database:
            connection = Connection(self.INSTANCE, mock_database)

            connection.run_prior_DDL_statements()
            mock_database.update_ddl.assert_not_called()

            ddl = ["ddl"]
            connection._ddl_statements = ddl

            connection.run_prior_DDL_statements()
            mock_database.update_ddl.assert_called_once_with(ddl)

            connection.is_closed = True

            with self.assertRaises(InterfaceError):
                connection.run_prior_DDL_statements()

    def test_context(self):
        connection = self._make_connection()
        with connection as conn:
            self.assertEqual(conn, connection)

        self.assertTrue(connection.is_closed)

    def test_connect(self):
        from google.cloud.spanner_dbapi import Connection, connect

        with mock.patch("google.cloud.spanner_v1.Client"):
            with mock.patch(
                "google.api_core.gapic_v1.client_info.ClientInfo",
                return_value=self._get_client_info(),
            ):
                connection = connect(
                    self.INSTANCE,
                    self.DATABASE,
                    self.PROJECT,
                    self.CREDENTIALS,
                    self.USER_AGENT,
                )
                self.assertIsInstance(connection, Connection)

    def test_connect_instance_not_found(self):
        from google.cloud.spanner_dbapi import connect

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=False
        ):
            with self.assertRaises(ValueError):
                connect("test-instance", "test-database")

    def test_connect_database_not_found(self):
        from google.cloud.spanner_dbapi import connect

        with mock.patch(
            "google.cloud.spanner_v1.database.Database.exists", return_value=False
        ):
            with mock.patch(
                "google.cloud.spanner_v1.instance.Instance.exists", return_value=True
            ):
                with self.assertRaises(ValueError):
                    connect("test-instance", "test-database")

    def test_default_sessions_pool(self):
        from google.cloud.spanner_dbapi import connect

        with mock.patch("google.cloud.spanner_v1.instance.Instance.database"):
            with mock.patch(
                "google.cloud.spanner_v1.instance.Instance.exists", return_value=True
            ):
                connection = connect("test-instance", "test-database")

                self.assertIsNotNone(connection.database._pool)

    def test_sessions_pool(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_v1.pool import FixedSizePool

        database_id = "test-database"
        pool = FixedSizePool()

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.database"
        ) as database_mock:
            with mock.patch(
                "google.cloud.spanner_v1.instance.Instance.exists", return_value=True
            ):
                connect("test-instance", database_id, pool=pool)
                database_mock.assert_called_once_with(database_id, pool=pool)

    def test_run_statement_remember_statements(self):
        """Check that Connection remembers executed statements."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        sql = """SELECT 23 FROM table WHERE id = @a1"""
        params = {"a1": "value"}
        param_types = {"a1": str}

        connection = self._make_connection()

        statement = Statement(sql, params, param_types, ResultsChecksum(), False)
        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.transaction_checkout"
        ):
            connection.run_statement(statement)

        self.assertEqual(connection._statements[0].sql, sql)
        self.assertEqual(connection._statements[0].params, params)
        self.assertEqual(connection._statements[0].param_types, param_types)
        self.assertIsInstance(connection._statements[0].checksum, ResultsChecksum)

    def test_run_statement_dont_remember_retried_statements(self):
        """Check that Connection doesn't remember re-executed statements."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        sql = """SELECT 23 FROM table WHERE id = @a1"""
        params = {"a1": "value"}
        param_types = {"a1": str}

        connection = self._make_connection()

        statement = Statement(sql, params, param_types, ResultsChecksum(), False)
        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.transaction_checkout"
        ):
            connection.run_statement(statement, retried=True)

        self.assertEqual(len(connection._statements), 0)

    def test_clear_statements_on_commit(self):
        """
        Check that all the saved statements are
        cleared, when the transaction is commited.
        """
        connection = self._make_connection()
        connection._transaction = mock.Mock(rolled_back=False, committed=False)
        connection._statements = [{}, {}]

        self.assertEqual(len(connection._statements), 2)

        with mock.patch("google.cloud.spanner_v1.transaction.Transaction.commit"):
            connection.commit()

        self.assertEqual(len(connection._statements), 0)

    def test_clear_statements_on_rollback(self):
        """
        Check that all the saved statements are
        cleared, when the transaction is roll backed.
        """
        connection = self._make_connection()
        connection._transaction = mock.Mock()
        connection._statements = [{}, {}]

        self.assertEqual(len(connection._statements), 2)

        with mock.patch("google.cloud.spanner_v1.transaction.Transaction.commit"):
            connection.rollback()

        self.assertEqual(len(connection._statements), 0)

    def test_retry_transaction(self):
        """Check retrying an aborted transaction."""
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]
        connection = self._make_connection()

        checksum = ResultsChecksum()
        checksum.consume_result(row)
        retried_checkum = ResultsChecksum()

        statement = Statement("SELECT 1", [], {}, checksum, False)
        connection._statements.append(statement)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.run_statement",
            return_value=([row], retried_checkum),
        ) as run_mock:
            with mock.patch(
                "google.cloud.spanner_dbapi.connection._compare_checksums"
            ) as compare_mock:
                connection.retry_transaction()

                compare_mock.assert_called_with(checksum, retried_checkum)

            run_mock.assert_called_with(statement, retried=True)

    def test_retry_transaction_checksum_mismatch(self):
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

        statement = Statement("SELECT 1", [], {}, checksum, False)
        connection._statements.append(statement)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.run_statement",
            return_value=([retried_row], retried_checkum),
        ):
            with self.assertRaises(RetryAborted):
                connection.retry_transaction()

    def test_commit_retry_aborted_statements(self):
        """Check that retried transaction executing the same statements."""
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]
        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=True,
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists", return_value=True,
            ):
                connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()
        cursor._checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, cursor._checksum, False)
        connection._statements.append(statement)
        connection._transaction = mock.Mock(rolled_back=False, committed=False)

        with mock.patch.object(
            connection._transaction, "commit", side_effect=(Aborted("Aborted"), None),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                return_value=([row], ResultsChecksum()),
            ) as run_mock:

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

    def test_retry_aborted_retry(self):
        """
        Check that in case of a retried transaction failed,
        the connection will retry it once again.
        """
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=True,
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists", return_value=True,
            ):
                connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()
        cursor._checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, cursor._checksum, False)
        connection._statements.append(statement)

        metadata_mock = mock.Mock()
        metadata_mock.trailing_metadata.return_value = {}

        with mock.patch.object(
            connection,
            "run_statement",
            side_effect=(
                Aborted("Aborted", errors=[metadata_mock]),
                ([row], ResultsChecksum()),
            ),
        ) as retry_mock:

            connection.retry_transaction()

            retry_mock.assert_has_calls(
                (
                    mock.call(statement, retried=True),
                    mock.call(statement, retried=True),
                )
            )
