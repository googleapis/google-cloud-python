# Copyright 2025 Google LLC All rights reserved.
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
from datetime import timedelta
from mock import Mock, patch
from os import environ
from time import time, sleep
from typing import Callable
from unittest import TestCase

from google.api_core.exceptions import BadRequest, FailedPrecondition
from google.cloud.spanner_v1.database_sessions_manager import DatabaseSessionsManager
from google.cloud.spanner_v1.database_sessions_manager import TransactionType
from tests._builders import build_database


# Shorten polling and refresh intervals for testing.
@patch.multiple(
    DatabaseSessionsManager,
    _MAINTENANCE_THREAD_POLLING_INTERVAL=timedelta(seconds=1),
    _MAINTENANCE_THREAD_REFRESH_INTERVAL=timedelta(seconds=2),
)
class TestDatabaseSessionManager(TestCase):
    @classmethod
    def setUpClass(cls):
        # Save the original environment variables.
        cls._original_env = dict(environ)

    @classmethod
    def tearDownClass(cls):
        # Restore environment variables.
        environ.clear()
        environ.update(cls._original_env)

    def setUp(self):
        # Build session manager.
        database = build_database()
        self._manager = database._sessions_manager

        # Mock the session pool.
        pool = self._manager._pool
        pool.get = Mock(wraps=pool.get)
        pool.put = Mock(wraps=pool.put)

    def tearDown(self):
        # If the maintenance thread is still alive, set the event and wait
        # for the thread to terminate. We need to do this to ensure that the
        # thread does not interfere with other tests.
        manager = self._manager
        thread = manager._multiplexed_session_thread

        if thread and thread.is_alive():
            manager._multiplexed_session_terminate_event.set()
            self._assert_true_with_timeout(lambda: not thread.is_alive())

    def test_read_only_pooled(self):
        manager = self._manager
        pool = manager._pool

        self._disable_multiplexed_sessions()

        # Get session from pool.
        session = manager.get_session(TransactionType.READ_ONLY)
        self.assertFalse(session.is_multiplexed)
        pool.get.assert_called_once()

        # Return session to pool.
        manager.put_session(session)
        pool.put.assert_called_once_with(session)

    def test_read_only_multiplexed(self):
        manager = self._manager
        pool = manager._pool

        self._enable_multiplexed_sessions()

        # Session is created.
        session_1 = manager.get_session(TransactionType.READ_ONLY)
        self.assertTrue(session_1.is_multiplexed)
        manager.put_session(session_1)

        # Session is re-used.
        session_2 = manager.get_session(TransactionType.READ_ONLY)
        self.assertEqual(session_1, session_2)
        manager.put_session(session_2)

        # Verify that pool was not used.
        pool.get.assert_not_called()
        pool.put.assert_not_called()

        # Verify logger calls.
        info = manager._database.logger.info
        info.assert_called_once_with("Created multiplexed session.")

    def test_partitioned_pooled(self):
        manager = self._manager
        pool = manager._pool

        self._disable_multiplexed_sessions()

        # Get session from pool.
        session = manager.get_session(TransactionType.PARTITIONED)
        self.assertFalse(session.is_multiplexed)
        pool.get.assert_called_once()

        # Return session to pool.
        manager.put_session(session)
        pool.put.assert_called_once_with(session)

    def test_partitioned_multiplexed(self):
        manager = self._manager
        pool = manager._pool

        self._enable_multiplexed_sessions()

        # Session is created.
        session_1 = manager.get_session(TransactionType.PARTITIONED)
        self.assertTrue(session_1.is_multiplexed)
        manager.put_session(session_1)

        # Session is re-used.
        session_2 = manager.get_session(TransactionType.PARTITIONED)
        self.assertEqual(session_1, session_2)
        manager.put_session(session_2)

        # Verify that pool was not used.
        pool.get.assert_not_called()
        pool.put.assert_not_called()

        # Verify logger calls.
        info = manager._database.logger.info
        info.assert_called_once_with("Created multiplexed session.")

    def test_read_write_pooled(self):
        manager = self._manager
        pool = manager._pool

        self._disable_multiplexed_sessions()

        # Get session from pool.
        session = manager.get_session(TransactionType.READ_WRITE)
        self.assertFalse(session.is_multiplexed)
        pool.get.assert_called_once()

        # Return session to pool.
        manager.put_session(session)
        pool.put.assert_called_once_with(session)

    def test_read_write_multiplexed(self):
        manager = self._manager
        pool = manager._pool

        self._enable_multiplexed_sessions()

        # Session is created.
        session_1 = manager.get_session(TransactionType.READ_WRITE)
        self.assertTrue(session_1.is_multiplexed)
        manager.put_session(session_1)

        # Session is re-used.
        session_2 = manager.get_session(TransactionType.READ_WRITE)
        self.assertEqual(session_1, session_2)
        manager.put_session(session_2)

        # Verify that pool was not used.
        pool.get.assert_not_called()
        pool.put.assert_not_called()

        # Verify logger calls.
        info = manager._database.logger.info
        info.assert_called_once_with("Created multiplexed session.")

    def test_multiplexed_maintenance(self):
        manager = self._manager
        self._enable_multiplexed_sessions()

        # Maintenance thread is started.
        session_1 = manager.get_session(TransactionType.READ_ONLY)
        self.assertTrue(session_1.is_multiplexed)
        self.assertTrue(manager._multiplexed_session_thread.is_alive())

        # Wait for maintenance thread to execute.
        self._assert_true_with_timeout(
            lambda: manager._database.spanner_api.create_session.call_count > 1
        )

        # Verify that maintenance thread created new multiplexed session.
        session_2 = manager.get_session(TransactionType.READ_ONLY)
        self.assertTrue(session_2.is_multiplexed)
        self.assertNotEqual(session_1, session_2)

        # Verify logger calls.
        info = manager._database.logger.info
        info.assert_called_with("Created multiplexed session.")

    def test_exception_bad_request(self):
        manager = self._manager
        api = manager._database.spanner_api
        api.create_session.side_effect = BadRequest("")

        with self.assertRaises(BadRequest):
            manager.get_session(TransactionType.READ_ONLY)

    def test_exception_failed_precondition(self):
        manager = self._manager
        api = manager._database.spanner_api
        api.create_session.side_effect = FailedPrecondition("")

        with self.assertRaises(FailedPrecondition):
            manager.get_session(TransactionType.READ_ONLY)

    def test__use_multiplexed_read_only(self):
        transaction_type = TransactionType.READ_ONLY

        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED] = "false"
        self.assertFalse(DatabaseSessionsManager._use_multiplexed(transaction_type))

        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED] = "true"
        self.assertTrue(DatabaseSessionsManager._use_multiplexed(transaction_type))

    def test__use_multiplexed_partitioned(self):
        transaction_type = TransactionType.PARTITIONED

        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_PARTITIONED] = "false"
        self.assertFalse(DatabaseSessionsManager._use_multiplexed(transaction_type))

        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_PARTITIONED] = "true"
        self.assertTrue(DatabaseSessionsManager._use_multiplexed(transaction_type))

        # Test default behavior (should be enabled)
        del environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_PARTITIONED]
        self.assertTrue(DatabaseSessionsManager._use_multiplexed(transaction_type))

    def test__use_multiplexed_read_write(self):
        transaction_type = TransactionType.READ_WRITE

        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_READ_WRITE] = "false"
        self.assertFalse(DatabaseSessionsManager._use_multiplexed(transaction_type))

        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_READ_WRITE] = "true"
        self.assertTrue(DatabaseSessionsManager._use_multiplexed(transaction_type))

        # Test default behavior (should be enabled)
        del environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_READ_WRITE]
        self.assertTrue(DatabaseSessionsManager._use_multiplexed(transaction_type))

    def test__use_multiplexed_unsupported_transaction_type(self):
        unsupported_type = "UNSUPPORTED_TRANSACTION_TYPE"

        with self.assertRaises(ValueError):
            DatabaseSessionsManager._use_multiplexed(unsupported_type)

    def test__getenv(self):
        true_values = ["1", " 1", " 1", "true", "True", "TRUE", " true "]
        for value in true_values:
            environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED] = value
            self.assertTrue(
                DatabaseSessionsManager._use_multiplexed(TransactionType.READ_ONLY)
            )

        false_values = ["false", "False", "FALSE", " false "]
        for value in false_values:
            environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED] = value
            self.assertFalse(
                DatabaseSessionsManager._use_multiplexed(TransactionType.READ_ONLY)
            )

        # Test that empty string and "0" are now treated as true (default enabled)
        default_true_values = ["", "0", "anything", "random"]
        for value in default_true_values:
            environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED] = value
            self.assertTrue(
                DatabaseSessionsManager._use_multiplexed(TransactionType.READ_ONLY)
            )

        del environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED]
        self.assertTrue(
            DatabaseSessionsManager._use_multiplexed(TransactionType.READ_ONLY)
        )

    def _assert_true_with_timeout(self, condition: Callable) -> None:
        """Asserts that the given condition is met within a timeout period.

        :type condition: Callable
        :param condition: A callable that returns a boolean indicating whether the condition is met.
        """

        sleep_seconds = 0.1
        timeout_seconds = 10

        start_time = time()
        while not condition() and time() - start_time < timeout_seconds:
            sleep(sleep_seconds)

        self.assertTrue(condition())

    @staticmethod
    def _disable_multiplexed_sessions() -> None:
        """Sets environment variables to disable multiplexed sessions for all transactions types."""

        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED] = "false"
        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_PARTITIONED] = "false"
        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_READ_WRITE] = "false"

    @staticmethod
    def _enable_multiplexed_sessions() -> None:
        """Sets environment variables to enable multiplexed sessions for all transaction types."""

        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED] = "true"
        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_PARTITIONED] = "true"
        environ[DatabaseSessionsManager._ENV_VAR_MULTIPLEXED_READ_WRITE] = "true"
