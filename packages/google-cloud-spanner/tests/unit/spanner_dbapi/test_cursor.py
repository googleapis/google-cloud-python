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

    def test_close(self):
        from google.cloud.spanner_dbapi import connect, InterfaceError

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=True
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists", return_value=True
            ):
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
                transaction=transaction, sql="sql", params=None
            )
            return res

        expected = "good"
        self.assertEqual(run_helper(expected), expected)
        self.assertEqual(cursor._row_count, _UNSET_COUNT)

        expected = 1234
        self.assertEqual(run_helper(expected), expected)
        self.assertEqual(cursor._row_count, expected)

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
            cursor.execute(sql="")

    def test_execute_autocommit_off(self):
        from google.cloud.spanner_dbapi.utils import PeekIterator

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        cursor.connection._autocommit = False
        cursor.connection.transaction_checkout = mock.MagicMock(autospec=True)

        cursor.execute("sql")
        self.assertIsInstance(cursor._result_set, mock.MagicMock)
        self.assertIsInstance(cursor._itr, PeekIterator)

    def test_execute_statement(self):
        from google.cloud.spanner_dbapi import parse_utils

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)

        with mock.patch(
            "google.cloud.spanner_dbapi.parse_utils.classify_stmt",
            return_value=parse_utils.STMT_DDL,
        ) as mock_classify_stmt:
            sql = "sql"
            cursor.execute(sql=sql)
            mock_classify_stmt.assert_called_once_with(sql)
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

    def test_executemany_on_closed_cursor(self):
        from google.cloud.spanner_dbapi import InterfaceError
        from google.cloud.spanner_dbapi import connect

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=True
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists", return_value=True
            ):
                connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor.close()

        with self.assertRaises(InterfaceError):
            cursor.executemany("""SELECT * FROM table1 WHERE "col1" = @a1""", ())

    def test_executemany(self):
        from google.cloud.spanner_dbapi import connect

        operation = """SELECT * FROM table1 WHERE "col1" = @a1"""
        params_seq = ((1,), (2,))

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=True
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists", return_value=True
            ):
                connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.execute"
        ) as execute_mock:
            cursor.executemany(operation, params_seq)

        execute_mock.assert_has_calls(
            (mock.call(operation, (1,)), mock.call(operation, (2,)))
        )

    @unittest.skipIf(
        sys.version_info[0] < 3, "Python 2 has an outdated iterator definition"
    )
    def test_fetchone(self):
        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        lst = [1, 2, 3]
        cursor._itr = iter(lst)
        for i in range(len(lst)):
            self.assertEqual(cursor.fetchone(), lst[i])
        self.assertIsNone(cursor.fetchone())

    def test_fetchmany(self):
        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
        lst = [(1,), (2,), (3,)]
        cursor._itr = iter(lst)

        self.assertEqual(cursor.fetchmany(), [lst[0]])

        result = cursor.fetchmany(len(lst))
        self.assertEqual(result, lst[1:])

    def test_fetchall(self):
        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        cursor = self._make_one(connection)
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

    # def test_handle_insert(self):
    #     pass
    #
    # def test_do_execute_insert_heterogenous(self):
    #     pass
    #
    # def test_do_execute_insert_homogenous(self):
    #     pass

    def test_handle_dql(self):
        from google.cloud.spanner_dbapi import utils
        from google.cloud.spanner_dbapi.cursor import _UNSET_COUNT

        connection = self._make_connection(self.INSTANCE, mock.MagicMock())
        connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        ) = mock.MagicMock()
        cursor = self._make_one(connection)

        mock_snapshot.execute_sql.return_value = int(0)
        cursor._handle_DQL("sql", params=None)
        self.assertEqual(cursor._row_count, 0)
        self.assertIsNone(cursor._itr)

        mock_snapshot.execute_sql.return_value = "0"
        cursor._handle_DQL("sql", params=None)
        self.assertEqual(cursor._result_set, "0")
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
