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
import pytest

from google.cloud.spanner_admin_database_v1 import DatabaseDialect
from google.cloud.spanner_dbapi.batch_dml_executor import BatchMode
from google.cloud.spanner_dbapi.exceptions import (
    InterfaceError,
    OperationalError,
    ProgrammingError,
)
from google.cloud.spanner_dbapi import Connection
from google.cloud.spanner_dbapi.connection import CLIENT_TRANSACTION_NOT_STARTED_WARNING
from google.cloud.spanner_dbapi.parsed_statement import (
    ParsedStatement,
    StatementType,
    Statement,
    ClientSideStatementType,
    AutocommitDmlMode,
)

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
    def setUp(self):
        self._under_test = self._make_connection()

    def _get_client_info(self):
        from google.api_core.gapic_v1.client_info import ClientInfo

        return ClientInfo(user_agent=USER_AGENT)

    def _make_connection(
        self, database_dialect=DatabaseDialect.DATABASE_DIALECT_UNSPECIFIED, **kwargs
    ):
        from google.cloud.spanner_v1.instance import Instance
        from google.cloud.spanner_v1.client import Client

        # We don't need a real Client object to test the constructor
        client = Client()
        instance = Instance(INSTANCE, client=client)
        database = instance.database(DATABASE, database_dialect=database_dialect)
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
        connection._spanner_transaction_started = True

        connection.autocommit = True

        mock_commit.assert_called_once()
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

    def test_property_current_schema_google_sql_dialect(self):
        from google.cloud.spanner_v1.database import Database

        connection = self._make_connection(
            database_dialect=DatabaseDialect.GOOGLE_STANDARD_SQL
        )
        self.assertIsInstance(connection.database, Database)
        self.assertEqual(connection.current_schema, "")

    def test_property_current_schema_postgres_sql_dialect(self):
        from google.cloud.spanner_v1.database import Database

        connection = self._make_connection(database_dialect=DatabaseDialect.POSTGRESQL)
        self.assertIsInstance(connection.database, Database)
        self.assertEqual(connection.current_schema, "public")

    def test_read_only_connection(self):
        connection = self._make_connection(read_only=True)
        self.assertTrue(connection.read_only)

        connection._spanner_transaction_started = True
        with self.assertRaisesRegex(
            ValueError,
            "Connection read/write mode can't be changed while a transaction is in progress. "
            "Commit or rollback the current transaction and try again.",
        ):
            connection.read_only = False

        connection._spanner_transaction_started = False
        connection.read_only = False
        self.assertFalse(connection.read_only)

    @staticmethod
    def _make_pool():
        from google.cloud.spanner_v1.pool import AbstractSessionPool

        return mock.create_autospec(AbstractSessionPool)

    @mock.patch("google.cloud.spanner_v1.database.Database")
    def test__session_checkout(self, mock_database):
        pool = self._make_pool()
        mock_database._pool = pool
        connection = Connection(INSTANCE, mock_database)

        connection._session_checkout()
        pool.get.assert_called_once_with()
        self.assertEqual(connection._session, pool.get.return_value)

        connection._session = "db_session"
        connection._session_checkout()
        self.assertEqual(connection._session, "db_session")

    def test_session_checkout_database_error(self):
        connection = Connection(INSTANCE)

        with pytest.raises(ValueError):
            connection._session_checkout()

    @mock.patch("google.cloud.spanner_v1.database.Database")
    def test__release_session(self, mock_database):
        pool = self._make_pool()
        mock_database._pool = pool
        connection = Connection(INSTANCE, mock_database)
        connection._session = "session"

        connection._release_session()
        pool.put.assert_called_once_with("session")
        self.assertIsNone(connection._session)

    def test_release_session_database_error(self):
        connection = Connection(INSTANCE)
        connection._session = "session"
        with pytest.raises(ValueError):
            connection._release_session()

    def test_transaction_checkout(self):
        connection = Connection(INSTANCE, DATABASE)
        mock_checkout = mock.MagicMock(autospec=True)
        connection._session_checkout = mock_checkout

        connection.transaction_checkout()

        mock_checkout.assert_called_once_with()

        mock_transaction = mock.MagicMock()
        connection._transaction = mock_transaction
        connection._spanner_transaction_started = True

        self.assertEqual(connection.transaction_checkout(), mock_transaction)

        connection._autocommit = True
        self.assertIsNone(connection.transaction_checkout())

    def test_snapshot_checkout(self):
        connection = Connection(INSTANCE, DATABASE, read_only=True)
        connection.autocommit = False

        session_checkout = mock.MagicMock(autospec=True)
        connection._session_checkout = session_checkout
        release_session = mock.MagicMock()
        connection._release_session = release_session

        snapshot = connection.snapshot_checkout()
        session_checkout.assert_called_once()

        self.assertEqual(snapshot, connection.snapshot_checkout())

        connection.commit()
        self.assertIsNotNone(connection._snapshot)
        release_session.assert_called_once()

        connection.snapshot_checkout()
        self.assertIsNotNone(connection._snapshot)

        connection.rollback()
        self.assertIsNotNone(connection._snapshot)
        self.assertEqual(release_session.call_count, 2)

        connection.autocommit = True
        self.assertIsNone(connection.snapshot_checkout())

    def test_close(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi import InterfaceError

        connection = connect("test-instance", "test-database")

        self.assertFalse(connection.is_closed)

        connection.close()

        self.assertTrue(connection.is_closed)

        with self.assertRaises(InterfaceError):
            connection.cursor()

        mock_transaction = mock.MagicMock()
        connection._transaction = mock_transaction
        connection._spanner_transaction_started = True

        mock_rollback = mock.MagicMock()
        mock_transaction.rollback = mock_rollback

        connection.close()

        mock_rollback.assert_called_once_with()

        connection._transaction = mock.MagicMock()
        connection._own_pool = False
        connection.close()

        self.assertTrue(connection.is_closed)

    @mock.patch.object(warnings, "warn")
    def test_commit_with_spanner_transaction_not_started(self, mock_warn):
        self._under_test._spanner_transaction_started = False

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            self._under_test.commit()

        mock_release.assert_called()

    def test_commit(self):
        self._under_test._transaction = mock_transaction = mock.MagicMock()
        self._under_test._spanner_transaction_started = True
        mock_transaction.commit = mock_commit = mock.MagicMock()
        transaction_helper = self._under_test._transaction_helper
        transaction_helper._statement_result_details_list = [{}, {}]

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            self._under_test.commit()

        mock_commit.assert_called_once_with()
        mock_release.assert_called_once_with()
        self.assertEqual(len(transaction_helper._statement_result_details_list), 0)

    @mock.patch.object(warnings, "warn")
    def test_commit_in_autocommit_mode(self, mock_warn):
        self._under_test._autocommit = True

        self._under_test.commit()

        mock_warn.assert_called_once_with(
            CLIENT_TRANSACTION_NOT_STARTED_WARNING, UserWarning, stacklevel=2
        )

    def test_commit_database_error(self):
        from google.cloud.spanner_dbapi import Connection

        connection = Connection(INSTANCE)

        with pytest.raises(ValueError):
            connection.commit()

    @mock.patch.object(warnings, "warn")
    def test_rollback_spanner_transaction_not_started(self, mock_warn):
        self._under_test._spanner_transaction_started = False

        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            self._under_test.rollback()

        mock_release.assert_called()

    @mock.patch.object(warnings, "warn")
    def test_rollback(self, mock_warn):
        mock_transaction = mock.MagicMock()
        self._under_test._spanner_transaction_started = True
        self._under_test._transaction = mock_transaction
        mock_rollback = mock.MagicMock()
        mock_transaction.rollback = mock_rollback
        transaction_helper = self._under_test._transaction_helper
        transaction_helper._statement_result_details_list = [{}, {}]
        with mock.patch(
            "google.cloud.spanner_dbapi.connection.Connection._release_session"
        ) as mock_release:
            self._under_test.rollback()

        self.assertEqual(len(transaction_helper._statement_result_details_list), 0)
        mock_rollback.assert_called_once_with()
        mock_release.assert_called_once_with()

    @mock.patch.object(warnings, "warn")
    def test_rollback_in_autocommit_mode(self, mock_warn):
        self._under_test._autocommit = True

        self._under_test.rollback()

        mock_warn.assert_called_once_with(
            CLIENT_TRANSACTION_NOT_STARTED_WARNING, UserWarning, stacklevel=2
        )

    def test_start_batch_dml_batch_mode_active(self):
        self._under_test._batch_mode = BatchMode.DML
        cursor = self._under_test.cursor()

        with self.assertRaises(ProgrammingError):
            self._under_test.start_batch_dml(cursor)

    def test_start_batch_dml_connection_read_only(self):
        self._under_test.read_only = True
        cursor = self._under_test.cursor()

        with self.assertRaises(ProgrammingError):
            self._under_test.start_batch_dml(cursor)

    def test_start_batch_dml(self):
        cursor = self._under_test.cursor()

        self._under_test.start_batch_dml(cursor)

        self.assertEqual(self._under_test._batch_mode, BatchMode.DML)

    def test_execute_batch_dml_batch_mode_inactive(self):
        self._under_test._batch_mode = BatchMode.NONE

        with self.assertRaises(ProgrammingError):
            self._under_test.execute_batch_dml_statement(
                ParsedStatement(StatementType.UPDATE, Statement("sql"))
            )

    @mock.patch(
        "google.cloud.spanner_dbapi.batch_dml_executor.BatchDmlExecutor", autospec=True
    )
    def test_execute_batch_dml(self, mock_batch_dml_executor):
        self._under_test._batch_mode = BatchMode.DML
        self._under_test._batch_dml_executor = mock_batch_dml_executor

        parsed_statement = ParsedStatement(StatementType.UPDATE, Statement("sql"))
        self._under_test.execute_batch_dml_statement(parsed_statement)

        mock_batch_dml_executor.execute_statement.assert_called_once_with(
            parsed_statement
        )

    @mock.patch(
        "google.cloud.spanner_dbapi.batch_dml_executor.BatchDmlExecutor", autospec=True
    )
    def test_run_batch_batch_mode_inactive(self, mock_batch_dml_executor):
        self._under_test._batch_mode = BatchMode.NONE
        self._under_test._batch_dml_executor = mock_batch_dml_executor

        with self.assertRaises(ProgrammingError):
            self._under_test.run_batch()

    @mock.patch(
        "google.cloud.spanner_dbapi.batch_dml_executor.BatchDmlExecutor", autospec=True
    )
    def test_run_batch(self, mock_batch_dml_executor):
        self._under_test._batch_mode = BatchMode.DML
        self._under_test._batch_dml_executor = mock_batch_dml_executor

        self._under_test.run_batch()

        mock_batch_dml_executor.run_batch_dml.assert_called_once_with()
        self.assertEqual(self._under_test._batch_mode, BatchMode.NONE)
        self.assertEqual(self._under_test._batch_dml_executor, None)

    @mock.patch(
        "google.cloud.spanner_dbapi.batch_dml_executor.BatchDmlExecutor", autospec=True
    )
    def test_abort_batch_batch_mode_inactive(self, mock_batch_dml_executor):
        self._under_test._batch_mode = BatchMode.NONE
        self._under_test._batch_dml_executor = mock_batch_dml_executor

        with self.assertRaises(ProgrammingError):
            self._under_test.abort_batch()

    @mock.patch(
        "google.cloud.spanner_dbapi.batch_dml_executor.BatchDmlExecutor", autospec=True
    )
    def test_abort_dml_batch(self, mock_batch_dml_executor):
        self._under_test._batch_mode = BatchMode.DML
        self._under_test._batch_dml_executor = mock_batch_dml_executor

        self._under_test.abort_batch()

        self.assertEqual(self._under_test._batch_mode, BatchMode.NONE)
        self.assertEqual(self._under_test._batch_dml_executor, None)

    def test_set_autocommit_dml_mode_with_autocommit_false(self):
        self._under_test.autocommit = False
        parsed_statement = ParsedStatement(
            StatementType.CLIENT_SIDE,
            Statement("sql"),
            ClientSideStatementType.SET_AUTOCOMMIT_DML_MODE,
            ["PARTITIONED_NON_ATOMIC"],
        )

        with self.assertRaises(ProgrammingError):
            self._under_test._set_autocommit_dml_mode(parsed_statement)

    def test_set_autocommit_dml_mode_with_readonly(self):
        self._under_test.autocommit = True
        self._under_test.read_only = True
        parsed_statement = ParsedStatement(
            StatementType.CLIENT_SIDE,
            Statement("sql"),
            ClientSideStatementType.SET_AUTOCOMMIT_DML_MODE,
            ["PARTITIONED_NON_ATOMIC"],
        )

        with self.assertRaises(ProgrammingError):
            self._under_test._set_autocommit_dml_mode(parsed_statement)

    def test_set_autocommit_dml_mode_with_batch_mode(self):
        self._under_test.autocommit = True
        parsed_statement = ParsedStatement(
            StatementType.CLIENT_SIDE,
            Statement("sql"),
            ClientSideStatementType.SET_AUTOCOMMIT_DML_MODE,
            ["PARTITIONED_NON_ATOMIC"],
        )

        self._under_test._set_autocommit_dml_mode(parsed_statement)

        assert (
            self._under_test.autocommit_dml_mode
            == AutocommitDmlMode.PARTITIONED_NON_ATOMIC
        )

    def test_set_autocommit_dml_mode(self):
        self._under_test.autocommit = True
        parsed_statement = ParsedStatement(
            StatementType.CLIENT_SIDE,
            Statement("sql"),
            ClientSideStatementType.SET_AUTOCOMMIT_DML_MODE,
            ["PARTITIONED_NON_ATOMIC"],
        )

        self._under_test._set_autocommit_dml_mode(parsed_statement)
        assert (
            self._under_test.autocommit_dml_mode
            == AutocommitDmlMode.PARTITIONED_NON_ATOMIC
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

    def test_run_prior_DDL_statements_database_error(self):
        from google.cloud.spanner_dbapi import Connection

        connection = Connection(INSTANCE)
        with pytest.raises(ValueError):
            connection.run_prior_DDL_statements()

    def test_as_context_manager(self):
        connection = self._make_connection()
        with connection as conn:
            self.assertEqual(conn, connection)

        self.assertTrue(connection.is_closed)

    def test_begin_cursor_closed(self):
        self._under_test.close()

        with self.assertRaises(InterfaceError):
            self._under_test.begin()

        self.assertEqual(self._under_test._transaction_begin_marked, False)

    def test_begin_transaction_begin_marked(self):
        self._under_test._transaction_begin_marked = True

        with self.assertRaises(OperationalError):
            self._under_test.begin()

    def test_begin_transaction_started(self):
        self._under_test._spanner_transaction_started = True

        with self.assertRaises(OperationalError):
            self._under_test.begin()

        self.assertEqual(self._under_test._transaction_begin_marked, False)

    def test_begin(self):
        self._under_test.begin()

        self.assertEqual(self._under_test._transaction_begin_marked, True)

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

    def test_validate_database_error(self):
        from google.cloud.spanner_dbapi import Connection

        connection = Connection(INSTANCE)

        with pytest.raises(ValueError):
            connection.validate()

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
        connection._spanner_transaction_started = True
        connection._transaction = mock.Mock()

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

    @mock.patch("google.cloud.spanner_dbapi.cursor.PeekIterator")
    def test_staleness_single_use_autocommit(self, MockedPeekIterator):
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
        _result_set = mock.Mock()
        snapshot_obj.execute_sql.return_value = _result_set
        _result_set.stats = None

        snapshot_ctx = mock.Mock()
        snapshot_ctx.__enter__ = mock.Mock(return_value=snapshot_obj)
        snapshot_ctx.__exit__ = exit_ctx_func
        snapshot_method = mock.Mock(return_value=snapshot_ctx)

        connection.database.snapshot = snapshot_method

        cursor = connection.cursor()
        cursor.execute("SELECT 1")

        connection.database.snapshot.assert_called_with(read_timestamp=timestamp)

    @mock.patch("google.cloud.spanner_dbapi.cursor.PeekIterator")
    def test_staleness_single_use_readonly_autocommit(self, MockedPeekIterator):
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
        _result_set = mock.Mock()
        _result_set.stats = None

        snapshot_obj.execute_sql.return_value = _result_set

        snapshot_ctx = mock.Mock()
        snapshot_ctx.__enter__ = mock.Mock(return_value=snapshot_obj)
        snapshot_ctx.__exit__ = exit_ctx_func
        snapshot_method = mock.Mock(return_value=snapshot_ctx)

        connection.database.snapshot = snapshot_method

        cursor = connection.cursor()
        cursor.execute("SELECT 1")

        connection.database.snapshot.assert_called_with(read_timestamp=timestamp)

    def test_request_priority(self):
        from google.cloud.spanner_dbapi.parsed_statement import Statement
        from google.cloud.spanner_v1 import RequestOptions

        sql = "SELECT 1"
        params = []
        param_types = {}
        priority = 2

        connection = self._make_connection()
        connection._spanner_transaction_started = True
        connection._transaction = mock.Mock()
        connection._transaction.execute_sql = mock.Mock()

        connection.request_priority = priority

        req_opts = RequestOptions(priority=priority)

        connection.run_statement(Statement(sql, params, param_types))

        connection._transaction.execute_sql.assert_called_with(
            sql, params, param_types=param_types, request_options=req_opts
        )
        assert connection.request_priority is None

        # check that priority is applied for only one request
        connection.run_statement(Statement(sql, params, param_types))

        connection._transaction.execute_sql.assert_called_with(
            sql, params, param_types=param_types, request_options=None
        )

    def test_custom_client_connection(self):
        from google.cloud.spanner_dbapi import connect

        client = _Client()
        connection = connect("test-instance", "test-database", client=client)
        self.assertTrue(connection.instance._client == client)

    def test_invalid_custom_client_connection(self):
        from google.cloud.spanner_dbapi import connect

        client = _Client()
        with pytest.raises(ValueError):
            connect(
                "test-instance",
                "test-database",
                project="invalid_project",
                client=client,
            )

    def test_connection_wo_database(self):
        from google.cloud.spanner_dbapi import connect

        connection = connect("test-instance")
        self.assertTrue(connection.database is None)


def exit_ctx_func(self, exc_type, exc_value, traceback):
    """Context __exit__ method mock."""
    pass


class _Client(object):
    def __init__(self, project="project_id"):
        self.project = project
        self.project_name = "projects/" + self.project

    def instance(self, instance_id="instance_id"):
        return _Instance(name=instance_id, client=self)


class _Instance(object):
    def __init__(self, name="instance_id", client=None):
        self.name = name
        self._client = client

    def database(
        self,
        database_id="database_id",
        pool=None,
        database_dialect=DatabaseDialect.GOOGLE_STANDARD_SQL,
    ):
        return _Database(database_id, pool, database_dialect)


class _Database(object):
    def __init__(
        self,
        database_id="database_id",
        pool=None,
        database_dialect=DatabaseDialect.GOOGLE_STANDARD_SQL,
    ):
        self.name = database_id
        self.pool = pool
        self.database_dialect = database_dialect
