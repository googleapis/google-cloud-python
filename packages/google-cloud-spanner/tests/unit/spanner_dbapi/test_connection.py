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
import sys
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

    @unittest.skipIf(sys.version_info[0] < 3, "Python 2 patching is outdated")
    def test_property_autocommit_setter(self):
        from google.cloud.spanner_dbapi import Connection

        connection = Connection(self.INSTANCE, self.DATABASE)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.commit"
        ) as mock_commit:
            connection.autocommit = True
            mock_commit.assert_called_once_with()
            self.assertEqual(connection._autocommit, True)

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection.commit"
        ) as mock_commit:
            connection.autocommit = False
            mock_commit.assert_not_called()
            self.assertEqual(connection._autocommit, False)

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

        connection._transaction = mock_transaction = mock.MagicMock()
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
        from google.cloud.spanner_dbapi import Connection

        connection = Connection(self.INSTANCE, self.DATABASE)
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
