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

"""Cursor() class unit tests."""

import mock
import sys
import unittest


class TestCursor(unittest.TestCase):

    INSTANCE = "test-instance"
    DATABASE = "test-database"

    def _get_target_class(self):
        from google.cloud.spanner_dbapi import Cursor

        return Cursor

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def _make_connection(self, *args, **kwargs):
        from google.cloud.spanner_dbapi import Connection

        return Connection(*args, **kwargs)

    def _transaction_mock(self, mock_response=[]):
        from google.rpc.code_pb2 import OK

        transaction = mock.Mock(committed=False, rolled_back=False)
        transaction.batch_update = mock.Mock(
            return_value=[mock.Mock(code=OK), mock_response]
        )
        return transaction

    def test_property_connection(self):
        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)
        self.assertEqual(cursor.connection, connection)

    def test_property_description(self):
        from google.cloud.spanner_dbapi._helpers import ColumnInfo

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)

        self.assertIsNone(cursor.description)
        cursor._result_set = res_set = mock.MagicMock()
        res_set.metadata.row_type.fields = [mock.MagicMock()]
        self.assertIsNotNone(cursor.description)
        self.assertIsInstance(cursor.description[0], ColumnInfo)

    def test_property_rowcount(self):
        from google.cloud.spanner_dbapi.cursor import _UNSET_COUNT

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)

        self.assertEqual(cursor.rowcount, _UNSET_COUNT)

    def test_callproc(self):
        from google.cloud.spanner_dbapi.exceptions import InterfaceError

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)
        cursor._is_closed = True
        with self.assertRaises(InterfaceError):
            cursor.callproc(procname=None)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_close(self, mock_client):
        from google.cloud.spanner_dbapi import connect, InterfaceError

        connection = connect(self.INSTANCE, self.DATABASE)

        cursor = connection.cursor()
        self.assertFalse(cursor.is_closed)

        cursor.close()

        self.assertTrue(cursor.is_closed)

        with self.assertRaises(InterfaceError):
            cursor.execute("SELECT * FROM database")

    def test_do_execute_update(self):
        from google.cloud.spanner_dbapi.cursor import _UNSET_COUNT

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)
        transaction = mock.MagicMock()

        def run_helper(ret_value):
            transaction.execute_update.return_value = ret_value
            res = cursor._do_execute_update(
                transaction=transaction,
                sql="SELECT * WHERE true",
                params={},
            )
            return res

        expected = "good"
        self.assertEqual(run_helper(expected), expected)
        self.assertEqual(cursor._row_count, _UNSET_COUNT)

        expected = 1234
        self.assertEqual(run_helper(expected), expected)
        self.assertEqual(cursor._row_count, expected)

    def test_do_batch_update(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_v1.param_types import INT64
        from google.cloud.spanner_v1.types.spanner import Session

        sql = "DELETE FROM table WHERE col1 = %s"

        connection = connect("test-instance", "test-database")

        connection.autocommit = True
        transaction = self._transaction_mock(mock_response=[1, 1, 1])
        cursor = connection.cursor()

        with mock.patch(
            "google.cloud.spanner_v1.services.spanner.client.SpannerClient.create_session",
            return_value=Session(),
        ):
            with mock.patch(
                "google.cloud.spanner_v1.session.Session.transaction",
                return_value=transaction,
            ):
                cursor.executemany(sql, [(1,), (2,), (3,)])

        transaction.batch_update.assert_called_once_with(
            [
                ("DELETE FROM table WHERE col1 = @a0", {"a0": 1}, {"a0": INT64}),
                ("DELETE FROM table WHERE col1 = @a0", {"a0": 2}, {"a0": INT64}),
                ("DELETE FROM table WHERE col1 = @a0", {"a0": 3}, {"a0": INT64}),
            ]
        )
        self.assertEqual(cursor._row_count, 3)

    def test_execute_programming_error(self):
        from google.cloud.spanner_dbapi.exceptions import ProgrammingError

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)
        cursor.connection = None
        with self.assertRaises(ProgrammingError):
            cursor.execute(sql="")

    def test_execute_attribute_error(self):
        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)

        with self.assertRaises(AttributeError):
            cursor.execute(sql="SELECT 1")

    def test_execute_autocommit_off(self):
        from google.cloud.spanner_dbapi.utils import PeekIterator

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor.connection._autocommit = False
        cursor.connection.transaction_checkout = mock.MagicMock(autospec=True)

        cursor.execute("sql")
        self.assertIsInstance(cursor._result_set, mock.MagicMock)
        self.assertIsInstance(cursor._itr, PeekIterator)

    def test_execute_insert_statement_autocommit_off(self):
        from google.cloud.spanner_dbapi import parse_utils
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.utils import PeekIterator

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor.connection._autocommit = False
        cursor.connection.transaction_checkout = mock.MagicMock(autospec=True)

        cursor._checksum = ResultsChecksum()
        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            return_value=parse_utils.STMT_INSERT,
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                return_value=(mock.MagicMock(), ResultsChecksum()),
            ):
                cursor.execute(
                    sql="INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)"
                )
                self.assertIsInstance(cursor._result_set, mock.MagicMock)
                self.assertIsInstance(cursor._itr, PeekIterator)

    def test_execute_statement(self):
        from google.cloud.spanner_dbapi import parse_utils

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            side_effect=[parse_utils.STMT_DDL, parse_utils.STMT_INSERT],
        ) as mock_classify_stmt:
            sql = "sql"
            with self.assertRaises(ValueError):
                cursor.execute(sql=sql)
            mock_classify_stmt.assert_called_with(sql)
            self.assertEqual(mock_classify_stmt.call_count, 2)
            self.assertEqual(cursor.connection._ddl_statements, [])

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            return_value=parse_utils.STMT_DDL,
        ) as mock_classify_stmt:
            sql = "sql"
            cursor.execute(sql=sql)
            mock_classify_stmt.assert_called_with(sql)
            self.assertEqual(mock_classify_stmt.call_count, 2)
            self.assertEqual(cursor.connection._ddl_statements, [sql])

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            return_value=parse_utils.STMT_NON_UPDATING,
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.cursor.Cursor._handle_DQL",
                return_value=parse_utils.STMT_NON_UPDATING,
            ) as mock_handle_ddl:
                connection.autocommit = True
                sql = "sql"
                cursor.execute(sql=sql)
                mock_handle_ddl.assert_called_once_with(sql, None)

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            return_value=parse_utils.STMT_INSERT,
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi._helpers.handle_insert",
                return_value=parse_utils.STMT_INSERT,
            ) as mock_handle_insert:
                sql = "sql"
                cursor.execute(sql=sql)
                mock_handle_insert.assert_called_once_with(connection, sql, None)

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            return_value="other_statement",
        ):
            cursor.connection._database = mock_db = mock.MagicMock()
            mock_db.run_in_transaction = mock_run_in = mock.MagicMock()
            sql = "sql"
            cursor.execute(sql=sql)
            mock_run_in.assert_called_once_with(cursor._do_execute_update, sql, None)

    def test_execute_integrity_error(self):
        from google.api_core import exceptions
        from google.cloud.spanner_dbapi.exceptions import IntegrityError

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            side_effect=exceptions.AlreadyExists("message"),
        ):
            with self.assertRaises(IntegrityError):
                cursor.execute(sql="sql")

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            side_effect=exceptions.FailedPrecondition("message"),
        ):
            with self.assertRaises(IntegrityError):
                cursor.execute(sql="sql")

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            side_effect=exceptions.OutOfRange("message"),
        ):
            with self.assertRaises(IntegrityError):
                cursor.execute("sql")

    def test_execute_invalid_argument(self):
        from google.api_core import exceptions
        from google.cloud.spanner_dbapi.exceptions import ProgrammingError

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            side_effect=exceptions.InvalidArgument("message"),
        ):
            with self.assertRaises(ProgrammingError):
                cursor.execute(sql="sql")

    def test_execute_internal_server_error(self):
        from google.api_core import exceptions
        from google.cloud.spanner_dbapi.exceptions import OperationalError

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            side_effect=exceptions.InternalServerError("message"),
        ):
            with self.assertRaises(OperationalError):
                cursor.execute(sql="sql")

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_executemany_on_closed_cursor(self, mock_client):
        from google.cloud.spanner_dbapi import InterfaceError
        from google.cloud.spanner_dbapi import connect

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor.close()

        with self.assertRaises(InterfaceError):
            cursor.executemany("""SELECT * FROM table1 WHERE "col1" = @a1""", ())

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_executemany_DLL(self, mock_client):
        from google.cloud.spanner_dbapi import connect, ProgrammingError

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()

        with self.assertRaises(ProgrammingError):
            cursor.executemany("""DROP DATABASE database_name""", ())

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_executemany(self, mock_client):
        from google.cloud.spanner_dbapi import connect

        operation = """SELECT * FROM table1 WHERE "col1" = @a1"""
        params_seq = ((1,), (2,))

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._result_set = [1, 2, 3]
        cursor._itr = iter([1, 2, 3])

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.execute"
        ) as execute_mock:
            cursor.executemany(operation, params_seq)

        execute_mock.assert_has_calls(
            (mock.call(operation, (1,)), mock.call(operation, (2,)))
        )

    def test_executemany_delete_batch_autocommit(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_v1.param_types import INT64
        from google.cloud.spanner_v1.types.spanner import Session

        sql = "DELETE FROM table WHERE col1 = %s"

        connection = connect("test-instance", "test-database")

        connection.autocommit = True
        transaction = self._transaction_mock()
        cursor = connection.cursor()

        with mock.patch(
            "google.cloud.spanner_v1.services.spanner.client.SpannerClient.create_session",
            return_value=Session(),
        ):
            with mock.patch(
                "google.cloud.spanner_v1.session.Session.transaction",
                return_value=transaction,
            ):
                cursor.executemany(sql, [(1,), (2,), (3,)])

        transaction.batch_update.assert_called_once_with(
            [
                ("DELETE FROM table WHERE col1 = @a0", {"a0": 1}, {"a0": INT64}),
                ("DELETE FROM table WHERE col1 = @a0", {"a0": 2}, {"a0": INT64}),
                ("DELETE FROM table WHERE col1 = @a0", {"a0": 3}, {"a0": INT64}),
            ]
        )

    def test_executemany_update_batch_autocommit(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_v1.param_types import INT64, STRING
        from google.cloud.spanner_v1.types.spanner import Session

        sql = "UPDATE table SET col1 = %s WHERE col2 = %s"

        connection = connect("test-instance", "test-database")

        connection.autocommit = True
        transaction = self._transaction_mock()
        cursor = connection.cursor()

        with mock.patch(
            "google.cloud.spanner_v1.services.spanner.client.SpannerClient.create_session",
            return_value=Session(),
        ):
            with mock.patch(
                "google.cloud.spanner_v1.session.Session.transaction",
                return_value=transaction,
            ):
                cursor.executemany(sql, [(1, "a"), (2, "b"), (3, "c")])

        transaction.batch_update.assert_called_once_with(
            [
                (
                    "UPDATE table SET col1 = @a0 WHERE col2 = @a1",
                    {"a0": 1, "a1": "a"},
                    {"a0": INT64, "a1": STRING},
                ),
                (
                    "UPDATE table SET col1 = @a0 WHERE col2 = @a1",
                    {"a0": 2, "a1": "b"},
                    {"a0": INT64, "a1": STRING},
                ),
                (
                    "UPDATE table SET col1 = @a0 WHERE col2 = @a1",
                    {"a0": 3, "a1": "c"},
                    {"a0": INT64, "a1": STRING},
                ),
            ]
        )

    def test_executemany_insert_batch_non_autocommit(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_v1.param_types import INT64
        from google.cloud.spanner_v1.types.spanner import Session

        sql = """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (%s, %s, %s, %s)"""

        connection = connect("test-instance", "test-database")

        transaction = self._transaction_mock()

        cursor = connection.cursor()
        with mock.patch(
            "google.cloud.spanner_v1.services.spanner.client.SpannerClient.create_session",
            return_value=Session(),
        ):
            with mock.patch(
                "google.cloud.spanner_v1.session.Session.transaction",
                return_value=transaction,
            ):
                cursor.executemany(sql, [(1, 2, 3, 4), (5, 6, 7, 8)])

        transaction.batch_update.assert_called_once_with(
            [
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 1, "a1": 2, "a2": 3, "a3": 4},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 5, "a1": 6, "a2": 7, "a3": 8},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
            ]
        )

    def test_executemany_insert_batch_autocommit(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_v1.param_types import INT64
        from google.cloud.spanner_v1.types.spanner import Session

        sql = """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (%s, %s, %s, %s)"""

        connection = connect("test-instance", "test-database")

        connection.autocommit = True

        transaction = self._transaction_mock()
        transaction.commit = mock.Mock()

        cursor = connection.cursor()
        with mock.patch(
            "google.cloud.spanner_v1.services.spanner.client.SpannerClient.create_session",
            return_value=Session(),
        ):
            with mock.patch(
                "google.cloud.spanner_v1.session.Session.transaction",
                return_value=transaction,
            ):
                cursor.executemany(sql, [(1, 2, 3, 4), (5, 6, 7, 8)])

        transaction.batch_update.assert_called_once_with(
            [
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 1, "a1": 2, "a2": 3, "a3": 4},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 5, "a1": 6, "a2": 7, "a3": 8},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
            ]
        )
        transaction.commit.assert_called_once()

    def test_executemany_insert_batch_failed(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi.exceptions import OperationalError
        from google.cloud.spanner_v1.types.spanner import Session
        from google.rpc.code_pb2 import UNKNOWN

        sql = """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (%s, %s, %s, %s)"""
        err_details = "Details here"

        connection = connect("test-instance", "test-database")

        connection.autocommit = True
        cursor = connection.cursor()

        transaction = mock.Mock(committed=False, rolled_back=False)
        transaction.batch_update = mock.Mock(
            return_value=(mock.Mock(code=UNKNOWN, message=err_details), [])
        )

        with mock.patch(
            "google.cloud.spanner_v1.services.spanner.client.SpannerClient.create_session",
            return_value=Session(),
        ):
            with mock.patch(
                "google.cloud.spanner_v1.session.Session.transaction",
                return_value=transaction,
            ):
                with self.assertRaisesRegex(OperationalError, err_details):
                    cursor.executemany(sql, [(1, 2, 3, 4), (5, 6, 7, 8)])

    def test_executemany_insert_batch_aborted(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_v1.param_types import INT64
        from google.rpc.code_pb2 import ABORTED

        sql = """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (%s, %s, %s, %s)"""
        err_details = "Aborted details here"

        connection = connect("test-instance", "test-database")

        transaction1 = mock.Mock(committed=False, rolled_back=False)
        transaction1.batch_update = mock.Mock(
            side_effect=[(mock.Mock(code=ABORTED, message=err_details), [])]
        )

        transaction2 = self._transaction_mock()

        connection.transaction_checkout = mock.Mock(
            side_effect=[transaction1, transaction2]
        )
        connection.retry_transaction = mock.Mock()

        cursor = connection.cursor()
        cursor.executemany(sql, [(1, 2, 3, 4), (5, 6, 7, 8)])

        transaction1.batch_update.assert_called_with(
            [
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 1, "a1": 2, "a2": 3, "a3": 4},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 5, "a1": 6, "a2": 7, "a3": 8},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
            ]
        )
        transaction2.batch_update.assert_called_with(
            [
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 1, "a1": 2, "a2": 3, "a3": 4},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 5, "a1": 6, "a2": 7, "a3": 8},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
            ]
        )
        connection.retry_transaction.assert_called_once()

        self.assertEqual(
            connection._statements[0][0],
            [
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 1, "a1": 2, "a2": 3, "a3": 4},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
                (
                    """INSERT INTO table (col1, "col2", `col3`, `"col4"`) VALUES (@a0, @a1, @a2, @a3)""",
                    {"a0": 5, "a1": 6, "a2": 7, "a3": 8},
                    {"a0": INT64, "a1": INT64, "a2": INT64, "a3": INT64},
                ),
            ],
        )
        self.assertIsInstance(connection._statements[0][1], ResultsChecksum)

    @unittest.skipIf(
        sys.version_info[0] < 3, "Python 2 has an outdated iterator definition"
    )
    def test_fetchone(self):
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor._checksum = ResultsChecksum()
        lst = [1, 2, 3]
        cursor._itr = iter(lst)
        for i in range(len(lst)):
            self.assertEqual(cursor.fetchone(), lst[i])
        self.assertIsNone(cursor.fetchone())

    @unittest.skipIf(
        sys.version_info[0] < 3, "Python 2 has an outdated iterator definition"
    )
    def test_fetchone_w_autocommit(self):
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        connection.autocommit = True
        cursor = self._make_one(connection)
        cursor._checksum = ResultsChecksum()
        lst = [1, 2, 3]
        cursor._itr = iter(lst)
        for i in range(len(lst)):
            self.assertEqual(cursor.fetchone(), lst[i])
        self.assertIsNone(cursor.fetchone())

    def test_fetchmany(self):
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor._checksum = ResultsChecksum()
        lst = [(1,), (2,), (3,)]
        cursor._itr = iter(lst)

        self.assertEqual(cursor.fetchmany(), [lst[0]])

        result = cursor.fetchmany(len(lst))
        self.assertEqual(result, lst[1:])

    def test_fetchmany_w_autocommit(self):
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        connection.autocommit = True
        cursor = self._make_one(connection)
        cursor._checksum = ResultsChecksum()
        lst = [(1,), (2,), (3,)]
        cursor._itr = iter(lst)

        self.assertEqual(cursor.fetchmany(), [lst[0]])

        result = cursor.fetchmany(len(lst))
        self.assertEqual(result, lst[1:])

    def test_fetchall(self):
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor._checksum = ResultsChecksum()
        lst = [(1,), (2,), (3,)]
        cursor._itr = iter(lst)
        self.assertEqual(cursor.fetchall(), lst)

    def test_fetchall_w_autocommit(self):
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        connection.autocommit = True
        cursor = self._make_one(connection)
        cursor._checksum = ResultsChecksum()
        lst = [(1,), (2,), (3,)]
        cursor._itr = iter(lst)
        self.assertEqual(cursor.fetchall(), lst)

    def test_nextset(self):
        from google.cloud.spanner_dbapi import exceptions

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor.close()
        with self.assertRaises(exceptions.InterfaceError):
            cursor.nextset()

    def test_setinputsizes(self):
        from google.cloud.spanner_dbapi import exceptions

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor.close()
        with self.assertRaises(exceptions.InterfaceError):
            cursor.setinputsizes(sizes=None)

    def test_setoutputsize(self):
        from google.cloud.spanner_dbapi import exceptions

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor.close()
        with self.assertRaises(exceptions.InterfaceError):
            cursor.setoutputsize(size=None)

    def test_handle_dql(self):
        from google.cloud.spanner_dbapi import utils
        from google.cloud.spanner_dbapi.cursor import _UNSET_COUNT

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        ) = mock.MagicMock()
        cursor = self._make_one(connection)

        mock_snapshot.execute_sql.return_value = ["0"]
        cursor._handle_DQL("sql", params=None)
        self.assertEqual(cursor._result_set, ["0"])
        self.assertIsInstance(cursor._itr, utils.PeekIterator)
        self.assertEqual(cursor._row_count, _UNSET_COUNT)

    def test_context(self):
        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)
        with cursor as c:
            self.assertEqual(c, cursor)

        self.assertTrue(c.is_closed)

    def test_next(self):
        from google.cloud.spanner_dbapi import exceptions

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)
        with self.assertRaises(exceptions.ProgrammingError):
            cursor.__next__()

        lst = [(1,), (2,), (3,)]
        cursor._itr = iter(lst)
        i = 0
        for c in cursor._itr:
            self.assertEqual(c, lst[i])
            i += 1

    def test_iter(self):
        from google.cloud.spanner_dbapi import exceptions

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)
        with self.assertRaises(exceptions.ProgrammingError):
            _ = iter(cursor)

        iterator = iter([(1,), (2,), (3,)])
        cursor._itr = iterator
        self.assertEqual(iter(cursor), iterator)

    def test_list_tables(self):
        from google.cloud.spanner_dbapi import _helpers

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)

        table_list = ["table1", "table2", "table3"]
        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.run_sql_in_snapshot",
            return_value=table_list,
        ) as mock_run_sql:
            cursor.list_tables()
            mock_run_sql.assert_called_once_with(_helpers.SQL_LIST_TABLES)

    def test_run_sql_in_snapshot(self):
        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        ) = mock.MagicMock()
        cursor = self._make_one(connection)

        results = 1, 2, 3
        mock_snapshot.execute_sql.return_value = results
        self.assertEqual(cursor.run_sql_in_snapshot("sql"), list(results))

    def test_get_table_column_schema(self):
        from google.cloud.spanner_dbapi.cursor import ColumnDetails
        from google.cloud.spanner_dbapi import _helpers
        from google.cloud.spanner_v1 import param_types

        connection = self._make_connection(self.INSTANCE, self.DATABASE)
        cursor = self._make_one(connection)

        column_name = "column1"
        is_nullable = "YES"
        spanner_type = "spanner_type"
        rows = [(column_name, is_nullable, spanner_type)]
        expected = {column_name: ColumnDetails(null_ok=True, spanner_type=spanner_type)}
        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.run_sql_in_snapshot",
            return_value=rows,
        ) as mock_run_sql:
            table_name = "table1"
            result = cursor.get_table_column_schema(table_name=table_name)
            mock_run_sql.assert_called_once_with(
                sql=_helpers.SQL_GET_TABLE_COLUMN_SCHEMA,
                params={"table_name": table_name},
                param_types={"table_name": param_types.STRING},
            )
            self.assertEqual(result, expected)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_peek_iterator_aborted(self, mock_client):
        """
        Checking that an Aborted exception is retried in case it happened
        while streaming the first element with a PeekIterator.
        """
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.connection import connect

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        with mock.patch(
            "google.cloud.spanner_dbapi.utils.PeekIterator.__init__",
            side_effect=(Aborted("Aborted"), None),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.retry_transaction"
            ) as retry_mock:
                with mock.patch(
                    "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                    return_value=((1, 2, 3), None),
                ):
                    cursor.execute("SELECT * FROM table_name")

                retry_mock.assert_called_with()

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchone_retry_aborted(self, mock_client):
        """Check that aborted fetch re-executing transaction."""
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__next__",
            side_effect=(Aborted("Aborted"), None),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.retry_transaction"
            ) as retry_mock:

                cursor.fetchone()

                retry_mock.assert_called_with()

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchone_retry_aborted_statements(self, mock_client):
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

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__next__",
            side_effect=(Aborted("Aborted"), None),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                return_value=([row], ResultsChecksum()),
            ) as run_mock:

                cursor.fetchone()

                run_mock.assert_called_with(statement, retried=True)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchone_retry_aborted_statements_checksums_mismatch(self, mock_client):
        """Check transaction retrying with underlying data being changed."""
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.exceptions import RetryAborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]
        row2 = ["updated_field1", "field2"]

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()
        cursor._checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, cursor._checksum, False)
        connection._statements.append(statement)

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__next__",
            side_effect=(Aborted("Aborted"), None),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                return_value=([row2], ResultsChecksum()),
            ) as run_mock:

                with self.assertRaises(RetryAborted):
                    cursor.fetchone()

                run_mock.assert_called_with(statement, retried=True)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchall_retry_aborted(self, mock_client):
        """Check that aborted fetch re-executing transaction."""
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__iter__",
            side_effect=(Aborted("Aborted"), iter([])),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.retry_transaction"
            ) as retry_mock:

                cursor.fetchall()

                retry_mock.assert_called_with()

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchall_retry_aborted_statements(self, mock_client):
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

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__iter__",
            side_effect=(Aborted("Aborted"), iter(row)),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                return_value=([row], ResultsChecksum()),
            ) as run_mock:
                cursor.fetchall()

                run_mock.assert_called_with(statement, retried=True)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchall_retry_aborted_statements_checksums_mismatch(self, mock_client):
        """Check transaction retrying with underlying data being changed."""
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.exceptions import RetryAborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]
        row2 = ["updated_field1", "field2"]

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()
        cursor._checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, cursor._checksum, False)
        connection._statements.append(statement)

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__iter__",
            side_effect=(Aborted("Aborted"), iter(row)),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                return_value=([row2], ResultsChecksum()),
            ) as run_mock:

                with self.assertRaises(RetryAborted):
                    cursor.fetchall()

                run_mock.assert_called_with(statement, retried=True)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchmany_retry_aborted(self, mock_client):
        """Check that aborted fetch re-executing transaction."""
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__next__",
            side_effect=(Aborted("Aborted"), None),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.retry_transaction"
            ) as retry_mock:

                cursor.fetchmany()

                retry_mock.assert_called_with()

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchmany_retry_aborted_statements(self, mock_client):
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

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__next__",
            side_effect=(Aborted("Aborted"), None),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                return_value=([row], ResultsChecksum()),
            ) as run_mock:

                cursor.fetchmany(len(row))

                run_mock.assert_called_with(statement, retried=True)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_fetchmany_retry_aborted_statements_checksums_mismatch(self, mock_client):
        """Check transaction retrying with underlying data being changed."""
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_dbapi.exceptions import RetryAborted
        from google.cloud.spanner_dbapi.checksum import ResultsChecksum
        from google.cloud.spanner_dbapi.connection import connect
        from google.cloud.spanner_dbapi.cursor import Statement

        row = ["field1", "field2"]
        row2 = ["updated_field1", "field2"]

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor._checksum = ResultsChecksum()
        cursor._checksum.consume_result(row)

        statement = Statement("SELECT 1", [], {}, cursor._checksum, False)
        connection._statements.append(statement)

        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.__next__",
            side_effect=(Aborted("Aborted"), None),
        ):
            with mock.patch(
                "google.cloud.spanner_dbapi.connection.Connection.run_statement",
                return_value=([row2], ResultsChecksum()),
            ) as run_mock:

                with self.assertRaises(RetryAborted):
                    cursor.fetchmany(len(row))

                run_mock.assert_called_with(statement, retried=True)

    @mock.patch("google.cloud.spanner_v1.Client")
    def test_ddls_with_semicolon(self, mock_client):
        """
        Check that one script with several DDL statements separated
        with semicolons is splitted into several DDLs.
        """
        from google.cloud.spanner_dbapi.connection import connect

        EXP_DDLS = [
            "CREATE TABLE table_name (row_id INT64) PRIMARY KEY ()",
            "DROP INDEX index_name",
            (
                "CREATE TABLE papers ("
                "\n    id INT64,"
                "\n    authors ARRAY<STRING(100)>,"
                '\n    author_list STRING(MAX) AS (ARRAY_TO_STRING(authors, ";")) stored'
                ") PRIMARY KEY (id)"
            ),
            "DROP TABLE table_name",
        ]

        connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE table_name (row_id INT64) PRIMARY KEY ();"
            "DROP INDEX index_name;\n"
            "CREATE TABLE papers ("
            "\n    id INT64,"
            "\n    authors ARRAY<STRING(100)>,"
            '\n    author_list STRING(MAX) AS (ARRAY_TO_STRING(authors, ";")) stored'
            ") PRIMARY KEY (id);"
            "DROP TABLE table_name;",
        )

        self.assertEqual(connection._ddl_statements, EXP_DDLS)
