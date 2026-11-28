# Copyright 2023 Google LLC All rights reserved.
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
import unittest
from unittest import mock

import grpc
from google.api_core.exceptions import (
    Aborted,
    InternalServerError,
    Unknown,
    from_grpc_error,
)

from google.cloud.spanner_dbapi.checksum import (
    RETRY_ABORTED_ERROR,
    ChecksumIterator,
    ResultsChecksum,
)
from google.cloud.spanner_dbapi.exceptions import (
    OperationalError,
    ProgrammingError,
    RetryAborted,
)
from google.cloud.spanner_dbapi.parsed_statement import ParsedStatement, StatementType
from google.cloud.spanner_dbapi.transaction_helper import (
    ChecksumStatement,
    CursorStatementType,
    ExecuteStatement,
    FetchStatement,
    ResultType,
    TransactionRetryHelper,
)
from google.cloud.spanner_dbapi.utils import PeekIterator
from google.cloud.spanner_v1 import (
    PartialResultSet,
    ResultSetMetadata,
    StructType,
    Type,
    TypeCode,
)
from google.cloud.spanner_v1._helpers import _make_value_pb
from google.cloud.spanner_v1.exceptions import wrap_with_request_id
from google.cloud.spanner_v1.streamed import StreamedResultSet


def _get_checksum(row):
    checksum = ResultsChecksum()
    checksum.consume_result(row)
    return checksum


SQL = "SELECT 1"
ARGS = []


class TestTransactionHelper(unittest.TestCase):
    @mock.patch("google.cloud.spanner_dbapi.cursor.Cursor")
    @mock.patch("google.cloud.spanner_dbapi.connection.Connection")
    def setUp(self, mock_connection, mock_cursor):
        self._under_test = TransactionRetryHelper(mock_connection)
        self._mock_cursor = mock_cursor

    def test_retry_transaction_execute(self):
        """
        Test retrying a transaction with an execute statement works.
        """
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.NONE,
            result_details=None,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()

        self._under_test.retry_transaction()

        run_mock.assert_called_with(SQL, ARGS)

    def test_retry_transaction_dml_execute(self):
        """
        Test retrying a transaction with an execute DML statement works.
        """
        update_count = 3
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.ROW_COUNT,
            result_details=update_count,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor = mock.Mock()
        run_mock().rowcount = update_count

        self._under_test.retry_transaction()

        run_mock().execute.assert_called_with(SQL, ARGS)

    def test_retry_transaction_dml_execute_exception(self):
        """
        Test retrying a transaction with an execute DML statement with different
        row update count than original throws RetryAborted exception.
        """
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.ROW_COUNT,
            result_details=2,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor = mock.Mock()
        run_mock().rowcount = 3

        with self.assertRaises(RetryAborted):
            self._under_test.retry_transaction()

        run_mock().execute.assert_called_with(SQL, ARGS)

    def test_retry_transaction_execute_many(self):
        """
        Test retrying a transaction with an executemany on Query statement works.
        """
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE_MANY,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.NONE,
            result_details=None,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().executemany = mock.Mock()

        self._under_test.retry_transaction()

        run_mock.assert_called_with(SQL, ARGS)

    def test_retry_transaction_dml_execute_many(self):
        """
        Test retrying a transaction with an executemany on DML statement works.
        """
        update_count = 3
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE_MANY,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.ROW_COUNT,
            result_details=update_count,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor = mock.Mock()
        run_mock().rowcount = update_count

        self._under_test.retry_transaction()

        run_mock().executemany.assert_called_with(SQL, ARGS)

    def test_retry_transaction_dml_executemany_exception(self):
        """
        Test retrying a transaction with an executemany DML statement with different
        row update count than original throws RetryAborted exception.
        """
        rows_inserted = [3, 4]
        self._mock_cursor._batch_dml_rows_count = rows_inserted
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE_MANY,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.BATCH_DML_ROWS_COUNT,
            result_details=rows_inserted,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor = mock.Mock()
        run_mock()._batch_dml_rows_count = [4, 3]

        with self.assertRaises(RetryAborted):
            self._under_test.retry_transaction()

        run_mock().executemany.assert_called_with(SQL, ARGS)

    def test_retry_transaction_fetchall(self):
        """
        Test retrying a transaction on a fetchall statement works.
        """
        result_row = ("field1", "field2")
        fetch_statement = FetchStatement(
            cursor=self._mock_cursor,
            statement_type=CursorStatementType.FETCH_ALL,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(result_row),
        )
        self._under_test._statement_result_details_list.append(fetch_statement)
        run_mock = self._under_test._connection.cursor().fetchall = mock.Mock()
        run_mock.return_value = [result_row]

        self._under_test.retry_transaction()

        run_mock.assert_called_with()

    def test_retry_transaction_fetchall_exception(self):
        """
        Test retrying a transaction on a fetchall statement throws exception
        when results is different from original in retry.
        """
        result_row = ("field1", "field2")
        fetch_statement = FetchStatement(
            cursor=self._mock_cursor,
            statement_type=CursorStatementType.FETCH_ALL,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(result_row),
        )
        self._under_test._statement_result_details_list.append(fetch_statement)
        run_mock = self._under_test._connection.cursor().fetchall = mock.Mock()
        retried_result_row = "field3"
        run_mock.return_value = [retried_result_row]

        with self.assertRaises(RetryAborted):
            self._under_test.retry_transaction()

        run_mock.assert_called_with()

    def test_retry_transaction_fetchmany(self):
        """
        Test retrying a transaction on a fetchmany statement works.
        """
        result_row = ("field1", "field2")
        fetch_statement = FetchStatement(
            cursor=self._mock_cursor,
            statement_type=CursorStatementType.FETCH_MANY,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(result_row),
            size=1,
        )
        self._under_test._statement_result_details_list.append(fetch_statement)
        run_mock = self._under_test._connection.cursor().fetchmany = mock.Mock()
        run_mock.return_value = [result_row]

        self._under_test.retry_transaction()

        run_mock.assert_called_with(1)

    def test_retry_transaction_fetchmany_exception(self):
        """
        Test retrying a transaction on a fetchmany statement throws exception
        when results is different from original in retry.
        """
        result_row = ("field1", "field2")
        fetch_statement = FetchStatement(
            cursor=self._mock_cursor,
            statement_type=CursorStatementType.FETCH_MANY,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(result_row),
            size=1,
        )
        self._under_test._statement_result_details_list.append(fetch_statement)
        run_mock = self._under_test._connection.cursor().fetchmany = mock.Mock()
        retried_result_row = "field3"
        run_mock.return_value = [retried_result_row]

        with self.assertRaises(RetryAborted):
            self._under_test.retry_transaction()

        run_mock.assert_called_with(1)

    def test_retry_transaction_same_exception(self):
        """
        Test retrying a transaction with statement throwing same exception in
        retry works.
        """
        exception = Exception("Test")
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.EXCEPTION,
            result_details=exception,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.side_effect = exception

        self._under_test.retry_transaction()

        run_mock.assert_called_with(SQL, ARGS)

    def test_retry_transaction_different_exception(self):
        """
        Test retrying a transaction with statement throwing different exception
        in retry results in RetryAborted exception.
        """
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.EXCEPTION,
            result_details=Exception("Test"),
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.side_effect = Exception("Test2")

        with self.assertRaises(RetryAborted):
            self._under_test.retry_transaction()

        run_mock.assert_called_with(SQL, ARGS)

    def test_retry_transaction_aborted_retry(self):
        """
        Check that in case of a retried transaction aborted,
        it will be retried once again.
        """
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.NONE,
            result_details=None,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        metadata_mock = mock.Mock()
        metadata_mock.trailing_metadata.return_value = {}
        run_mock.side_effect = [
            Aborted("Aborted", errors=[metadata_mock]),
            None,
        ]

        self._under_test.retry_transaction(default_retry_delay=0)

        run_mock.assert_has_calls(
            (
                mock.call(SQL, ARGS),
                mock.call(SQL, ARGS),
            )
        )

    def test_add_execute_statement_for_retry(self):
        """
        Test add_execute_statement_for_retry method works
        """
        self._mock_cursor._parsed_statement = ParsedStatement(
            statement_type=StatementType.INSERT, statement=None
        )

        sql = "INSERT INTO Table"
        rows_inserted = 3
        self._mock_cursor.rowcount = rows_inserted
        self._mock_cursor._batch_dml_rows_count = None
        self._under_test.add_execute_statement_for_retry(
            self._mock_cursor, sql, [], None, False
        )

        expected_statement_result_details = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=sql,
            args=[],
            result_type=ResultType.ROW_COUNT,
            result_details=rows_inserted,
        )
        self.assertEqual(
            self._under_test._last_statement_details_per_cursor,
            {self._mock_cursor: expected_statement_result_details},
        )
        self.assertEqual(
            self._under_test._statement_result_details_list,
            [expected_statement_result_details],
        )

    def test_add_execute_statement_for_retry_with_exception(self):
        """
        Test add_execute_statement_for_retry method with exception
        """
        self._mock_cursor._parsed_statement = ParsedStatement(
            statement_type=StatementType.INSERT, statement=None
        )
        self._mock_cursor.rowcount = -1

        sql = "INSERT INTO Table"
        exception = Exception("Test")
        self._under_test.add_execute_statement_for_retry(
            self._mock_cursor, sql, [], exception, False
        )

        expected_statement_result_details = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=sql,
            args=[],
            result_type=ResultType.EXCEPTION,
            result_details=exception,
        )
        self.assertEqual(
            self._under_test._last_statement_details_per_cursor,
            {self._mock_cursor: expected_statement_result_details},
        )
        self.assertEqual(
            self._under_test._statement_result_details_list,
            [expected_statement_result_details],
        )

    def test_add_execute_statement_for_retry_query_statement(self):
        """
        Test add_execute_statement_for_retry method works for non DML statement
        """
        self._mock_cursor._parsed_statement = ParsedStatement(
            statement_type=StatementType.QUERY, statement=None
        )
        self._mock_cursor._row_count = None
        self._mock_cursor._batch_dml_rows_count = None

        sql = "SELECT 1"
        self._under_test.add_execute_statement_for_retry(
            self._mock_cursor, sql, [], None, False
        )

        expected_statement_result_details = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=sql,
            args=[],
            result_type=ResultType.NONE,
            result_details=None,
        )
        self.assertEqual(
            self._under_test._last_statement_details_per_cursor,
            {self._mock_cursor: expected_statement_result_details},
        )
        self.assertEqual(
            self._under_test._statement_result_details_list,
            [expected_statement_result_details],
        )

    def test_add_execute_many_statement_for_retry(self):
        """
        Test add_execute_statement_for_retry method works for executemany
        """
        self._mock_cursor._parsed_statement = ParsedStatement(
            statement_type=StatementType.INSERT, statement=None
        )

        sql = "INSERT INTO Table"
        rows_inserted = [3, 4]
        self._mock_cursor._batch_dml_rows_count = rows_inserted
        self._under_test.add_execute_statement_for_retry(
            self._mock_cursor, sql, [], None, True
        )

        expected_statement_result_details = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE_MANY,
            cursor=self._mock_cursor,
            sql=sql,
            args=[],
            result_type=ResultType.BATCH_DML_ROWS_COUNT,
            result_details=rows_inserted,
        )
        self.assertEqual(
            self._under_test._last_statement_details_per_cursor,
            {self._mock_cursor: expected_statement_result_details},
        )
        self.assertEqual(
            self._under_test._statement_result_details_list,
            [expected_statement_result_details],
        )

    def test_add_fetch_statement_for_retry(self):
        """
        Test add_fetch_statement_for_retry method when last_statement_result_details is a
        Fetch statement
        """
        result_row = ("field1", "field2")
        result_checksum = _get_checksum(result_row)
        original_checksum_digest = result_checksum.checksum.digest()
        last_statement_result_details = FetchStatement(
            statement_type=CursorStatementType.FETCH_MANY,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=result_checksum,
            size=1,
        )
        self._under_test._last_statement_details_per_cursor = {
            self._mock_cursor: last_statement_result_details
        }
        new_rows = [("field3", "field4"), ("field5", "field6")]

        self._under_test.add_fetch_statement_for_retry(
            self._mock_cursor, new_rows, None, False
        )

        updated_last_statement_result_details = (
            self._under_test._last_statement_details_per_cursor.get(self._mock_cursor)
        )
        self.assertEqual(
            updated_last_statement_result_details.size,
            3,
        )
        self.assertNotEqual(
            updated_last_statement_result_details.result_details.checksum.digest(),
            original_checksum_digest,
        )

    def test_add_fetch_statement_for_retry_with_exception(self):
        """
        Test add_fetch_statement_for_retry method with exception
        """
        result_row = ("field1", "field2")
        fetch_statement = FetchStatement(
            statement_type=CursorStatementType.FETCH_MANY,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(result_row),
            size=1,
        )
        self._under_test._last_statement_details_per_cursor = {
            self._mock_cursor: fetch_statement
        }
        exception = Exception("Test")

        self._under_test.add_fetch_statement_for_retry(
            self._mock_cursor, [], exception, False
        )

        self.assertEqual(
            self._under_test._last_statement_details_per_cursor.get(self._mock_cursor),
            FetchStatement(
                statement_type=CursorStatementType.FETCH_MANY,
                cursor=self._mock_cursor,
                result_type=ResultType.EXCEPTION,
                result_details=exception,
                size=1,
            ),
        )

    def test_add_fetch_statement_for_retry_last_statement_not_exists(self):
        """
        Test add_fetch_statement_for_retry method when last_statement_result_details
        doesn't exists
        """
        row = ("field3", "field4")

        self._under_test.add_fetch_statement_for_retry(
            self._mock_cursor, [row], None, False
        )

        expected_statement = FetchStatement(
            statement_type=CursorStatementType.FETCH_MANY,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(row),
            size=1,
        )
        self.assertEqual(
            self._under_test._last_statement_details_per_cursor,
            {self._mock_cursor: expected_statement},
        )
        self.assertEqual(
            self._under_test._statement_result_details_list,
            [expected_statement],
        )

    def test_add_fetch_statement_for_retry_fetch_all_statement(self):
        """
        Test add_fetch_statement_for_retry method for fetchall statement
        """
        row = ("field3", "field4")

        self._under_test.add_fetch_statement_for_retry(
            self._mock_cursor, [row], None, True
        )

        expected_statement = FetchStatement(
            statement_type=CursorStatementType.FETCH_ALL,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(row),
        )
        self.assertEqual(
            self._under_test._last_statement_details_per_cursor,
            {self._mock_cursor: expected_statement},
        )
        self.assertEqual(
            self._under_test._statement_result_details_list,
            [expected_statement],
        )

    def test_add_fetch_statement_for_retry_when_last_statement_is_not_fetch(self):
        """
        Test add_fetch_statement_for_retry method when last statement is not
        a fetch type of statement
        """
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.ROW_COUNT,
            result_details=2,
        )
        self._under_test._last_statement_details_per_cursor = {
            self._mock_cursor: execute_statement
        }
        self._under_test._statement_result_details_list.append(execute_statement)
        row = ("field3", "field4")

        self._under_test.add_fetch_statement_for_retry(
            self._mock_cursor, [row], None, False
        )

        expected_fetch_statement = FetchStatement(
            statement_type=CursorStatementType.FETCH_MANY,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(row),
            size=1,
        )
        self.assertEqual(
            self._under_test._last_statement_details_per_cursor,
            {self._mock_cursor: expected_fetch_statement},
        )
        self.assertEqual(
            self._under_test._statement_result_details_list,
            [execute_statement, expected_fetch_statement],
        )

    def test_add_checksum_iterator_for_retry_when_not_in_transaction(self):
        self._under_test._connection._client_transaction_started = False
        checksum_iterator = ChecksumIterator(iter([(1,)]))

        self._under_test.add_checksum_iterator_for_retry(
            self._mock_cursor, checksum_iterator
        )

        self.assertEqual(self._under_test._statement_result_details_list, [])
        self.assertEqual(self._under_test._last_statement_details_per_cursor, {})

    def test_add_checksum_iterator_for_retry_registers_statement(self):
        self._under_test._connection._client_transaction_started = True
        checksum_iterator = ChecksumIterator(iter([(1,)]))

        self._under_test.add_checksum_iterator_for_retry(
            self._mock_cursor, checksum_iterator
        )

        expected_statement = ChecksumStatement(
            statement_type=CursorStatementType.CHECKSUM_ITERATOR,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=checksum_iterator,
        )
        self.assertEqual(
            self._under_test._last_statement_details_per_cursor,
            {self._mock_cursor: expected_statement},
        )
        self.assertEqual(
            self._under_test._statement_result_details_list,
            [expected_statement],
        )

    def test_retry_transaction_checksum_iterator_success_and_result_set_swap(self):
        checksum_iterator = ChecksumIterator(iter([(1,), (2,), (3,)]))
        self.assertEqual(next(checksum_iterator), (1,))

        original_result_set = mock.Mock()
        retried_result_set = mock.Mock()
        self._mock_cursor._itr = checksum_iterator
        self._mock_cursor._result_set = original_result_set

        retried_cursor = mock.Mock()
        retried_cursor._itr = iter([(1,), (2,), (3,)])
        retried_cursor._result_set = retried_result_set
        self._under_test._connection.cursor.return_value = retried_cursor

        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.NONE,
            result_details=None,
        )
        checksum_statement = ChecksumStatement(
            statement_type=CursorStatementType.CHECKSUM_ITERATOR,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=checksum_iterator,
        )
        self._under_test._statement_result_details_list.extend(
            [execute_statement, checksum_statement]
        )

        self._under_test.retry_transaction()

        retried_cursor.execute.assert_called_once_with(SQL, ARGS)
        self.assertIs(self._mock_cursor._result_set, retried_result_set)
        self.assertEqual(list(checksum_iterator), [(2,), (3,)])

    def test_retry_transaction_stale_checksum_iterator_does_not_clobber_result_set(
        self,
    ):
        checksum_iterator = ChecksumIterator(iter([(1,)]))
        self.assertEqual(list(checksum_iterator), [(1,)])

        current_result_set = mock.Mock()
        self._mock_cursor._itr = mock.Mock()  # Moved on to a newer statement.
        self._mock_cursor._result_set = current_result_set

        retried_cursor = mock.Mock()
        retried_cursor._itr = iter([(1,)])
        retried_cursor._result_set = mock.Mock()
        self._under_test._connection.cursor.return_value = retried_cursor

        checksum_statement = ChecksumStatement(
            statement_type=CursorStatementType.CHECKSUM_ITERATOR,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=checksum_iterator,
        )
        self._under_test._statement_result_details_list.append(checksum_statement)

        self._under_test.retry_transaction()

        self.assertIs(self._mock_cursor._result_set, current_result_set)

    def test_retry_transaction_checksum_iterator_mismatch_raises_retry_aborted(self):
        checksum_iterator = ChecksumIterator(iter([(1,)]))
        self.assertEqual(list(checksum_iterator), [(1,)])

        retried_cursor = mock.Mock()
        retried_cursor._itr = iter([(1,), (2,)])  # Concurrent insert past EOF.
        self._under_test._connection.cursor.return_value = retried_cursor

        checksum_statement = ChecksumStatement(
            statement_type=CursorStatementType.CHECKSUM_ITERATOR,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=checksum_iterator,
        )
        self._under_test._statement_result_details_list.append(checksum_statement)

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            self._under_test.retry_transaction()

    def test_retry_transaction_checksum_iterator_aborted_retries_again(self):
        checksum_iterator = ChecksumIterator(iter([(1,), (2,)]))
        self.assertEqual(next(checksum_iterator), (1,))

        def failing_then_succeeding():
            if retried_cursor.execute.call_count == 1:
                raise Aborted("mid-stream abort")
            yield (1,)
            yield (2,)

        retried_cursor = mock.Mock()
        retried_cursor._itr = None

        def assign_itr(*_args, **_kwargs):
            retried_cursor._itr = failing_then_succeeding()

        retried_cursor.execute.side_effect = assign_itr
        self._under_test._connection.cursor.return_value = retried_cursor

        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.NONE,
            result_details=None,
        )
        checksum_statement = ChecksumStatement(
            statement_type=CursorStatementType.CHECKSUM_ITERATOR,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=checksum_iterator,
        )
        self._under_test._statement_result_details_list.extend(
            [execute_statement, checksum_statement]
        )

        self._under_test.retry_transaction(default_retry_delay=0)

        self.assertEqual(retried_cursor.execute.call_count, 2)
        self.assertEqual(list(checksum_iterator), [(2,)])

    def test_retry_transaction_unexpected_exception_on_non_exception_statement(self):
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.NONE,
            result_details=None,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        unexpected_error = InternalServerError("unexpected failure")
        run_mock.side_effect = unexpected_error

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR) as context:
            self._under_test.retry_transaction()

        self.assertIs(context.exception.__cause__, unexpected_error)

    def test_retry_transaction_unexpected_exception_on_fetch_checksum_statement(self):
        fetch_statement = FetchStatement(
            statement_type=CursorStatementType.FETCH_ALL,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=_get_checksum(("a",)),
        )
        self._under_test._statement_result_details_list.append(fetch_statement)
        run_mock = self._under_test._connection.cursor().fetchall = mock.Mock()
        unexpected_error = InternalServerError("unexpected mid-stream failure")
        run_mock.side_effect = unexpected_error

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR) as context:
            self._under_test.retry_transaction()

        self.assertIs(context.exception.__cause__, unexpected_error)

    def test_retry_transaction_same_grpc_error_different_wrapper_details(self):
        original_cause = InternalServerError("same error")
        original_error = OperationalError(["detail-1"])
        original_error.__cause__ = original_cause

        retried_cause = InternalServerError("same error")
        retried_error = OperationalError(["detail-2"])
        retried_error.__cause__ = retried_cause

        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.EXCEPTION,
            result_details=original_error,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.side_effect = retried_error

        self._under_test.retry_transaction()

        run_mock.assert_called_once_with(SQL, ARGS)

    def test_retry_transaction_same_grpc_code_different_message_raises(self):
        original_cause = InternalServerError("first message")
        original_error = OperationalError([])
        original_error.__cause__ = original_cause

        retried_cause = InternalServerError("second message")
        retried_error = OperationalError([])
        retried_error.__cause__ = retried_cause

        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.EXCEPTION,
            result_details=original_error,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.side_effect = retried_error

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            self._under_test.retry_transaction()

    def test_retry_transaction_unknown_grpc_error_different_args_raises(self):
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.EXCEPTION,
            result_details=Unknown("first"),
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.side_effect = Unknown("second")

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            self._under_test.retry_transaction()

    def test_retry_transaction_aborted_without_errors_list_and_max_retries(self):
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.NONE,
            result_details=None,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.side_effect = Aborted("no errors list")

        with mock.patch(
            "google.cloud.spanner_dbapi.transaction_helper.MAX_INTERNAL_RETRIES", 2
        ):
            with self.assertRaisesRegex(Aborted, "no errors list"):
                self._under_test.retry_transaction(default_retry_delay=0)

        self.assertEqual(run_mock.call_count, 2)

    def test_retry_transaction_exception_statement_succeeds_raises_retry_aborted(self):
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.EXCEPTION,
            result_details=InternalServerError("initial failure"),
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.return_value = None

        with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
            self._under_test.retry_transaction()

        run_mock.assert_called_once_with(SQL, ARGS)

    def test_retry_transaction_sleeps_with_retry_delay_on_aborted(self):
        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.NONE,
            result_details=None,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.side_effect = [Aborted("transient"), None]

        with mock.patch(
            "google.cloud.spanner_dbapi.transaction_helper.time.sleep"
        ) as sleep_mock:
            self._under_test.retry_transaction(default_retry_delay=0.25)

        sleep_mock.assert_called_once_with(0.25)
        self.assertEqual(run_mock.call_count, 2)

    def test_retry_transaction_multi_cursor_streamed_result_set_and_peek_iterator(
        self,
    ):
        metadata = ResultSetMetadata(
            row_type=StructType(
                fields=[StructType.Field(name="id", type_=Type(code=TypeCode.INT64))]
            )
        )

        def make_streamed_peek_iterator(chunks, trailing_error=None):
            def response_stream():
                for values in chunks:
                    partial_result_set = PartialResultSet(metadata=metadata)
                    for value in values:
                        partial_result_set.values.append(_make_value_pb(value))
                    yield partial_result_set
                if trailing_error is not None:
                    raise trailing_error

            result_set = StreamedResultSet(response_stream())
            return result_set, PeekIterator(result_set)

        # Cursor 1: DML statement + query consumed to EOF.
        cursor1 = mock.Mock()
        result_set_1, peek_iterator_1 = make_streamed_peek_iterator([[1], [2]])
        cursor1._result_set = result_set_1
        first_checksum_iterator = ChecksumIterator(peek_iterator_1)
        cursor1._itr = first_checksum_iterator
        self.assertEqual(list(first_checksum_iterator), [(1,), (2,)])

        # Cursor 2: partially consumed query (1 of 3 rows consumed).
        cursor2 = mock.Mock()
        result_set_2, peek_iterator_2 = make_streamed_peek_iterator([[10], [20, 30]])
        cursor2._result_set = result_set_2
        second_checksum_iterator = ChecksumIterator(peek_iterator_2)
        cursor2._itr = second_checksum_iterator
        self.assertEqual(next(second_checksum_iterator), (10,))

        # Cursor 3: query hitting mid-stream error on row 2.
        cursor3 = mock.Mock()
        result_set_3, peek_iterator_3 = make_streamed_peek_iterator(
            [[100]], trailing_error=InternalServerError("mid-stream boom")
        )
        cursor3._result_set = result_set_3
        third_checksum_iterator = ChecksumIterator(peek_iterator_3)
        cursor3._itr = third_checksum_iterator
        self.assertEqual(next(third_checksum_iterator), (100,))
        with self.assertRaisesRegex(InternalServerError, "mid-stream boom"):
            next(third_checksum_iterator)

        # Prepare retried cursors corresponding 1-to-1 with original cursors.
        retried_cursor1 = mock.Mock()
        retried_cursor2 = mock.Mock()
        retried_cursor3 = mock.Mock()
        self._under_test._connection.cursor.side_effect = [
            retried_cursor1,
            retried_cursor2,
            retried_cursor3,
        ]

        retried_result_set_1, first_retried_peek = make_streamed_peek_iterator(
            [[1], [2]]
        )
        retried_result_set_2, second_retried_peek = make_streamed_peek_iterator(
            [[10], [20, 30]]
        )
        retried_result_set_3, third_retried_peek = make_streamed_peek_iterator(
            [[100]], trailing_error=InternalServerError("mid-stream boom")
        )

        def exec_cursor1(sql, _args):
            if sql.startswith("UPDATE"):
                retried_cursor1.rowcount = 4
                retried_cursor1._batch_dml_rows_count = None
            else:
                retried_cursor1._result_set = retried_result_set_1
                retried_cursor1._itr = first_retried_peek

        def exec_cursor2(_sql, _args):
            retried_cursor2._result_set = retried_result_set_2
            retried_cursor2._itr = second_retried_peek

        def exec_cursor3(_sql, _args):
            retried_cursor3._result_set = retried_result_set_3
            retried_cursor3._itr = third_retried_peek

        retried_cursor1.execute.side_effect = exec_cursor1
        retried_cursor2.execute.side_effect = exec_cursor2
        retried_cursor3.execute.side_effect = exec_cursor3

        self._under_test._statement_result_details_list.extend(
            [
                ExecuteStatement(
                    statement_type=CursorStatementType.EXECUTE,
                    cursor=cursor1,
                    sql="UPDATE T SET X = 1",
                    args=None,
                    result_type=ResultType.ROW_COUNT,
                    result_details=4,
                ),
                ExecuteStatement(
                    statement_type=CursorStatementType.EXECUTE,
                    cursor=cursor1,
                    sql="SELECT id FROM T1",
                    args=None,
                    result_type=ResultType.NONE,
                    result_details=None,
                ),
                ChecksumStatement(
                    statement_type=CursorStatementType.CHECKSUM_ITERATOR,
                    cursor=cursor1,
                    result_type=ResultType.CHECKSUM,
                    result_details=first_checksum_iterator,
                ),
                ExecuteStatement(
                    statement_type=CursorStatementType.EXECUTE,
                    cursor=cursor2,
                    sql="SELECT id FROM T2",
                    args=None,
                    result_type=ResultType.NONE,
                    result_details=None,
                ),
                ChecksumStatement(
                    statement_type=CursorStatementType.CHECKSUM_ITERATOR,
                    cursor=cursor2,
                    result_type=ResultType.CHECKSUM,
                    result_details=second_checksum_iterator,
                ),
                ExecuteStatement(
                    statement_type=CursorStatementType.EXECUTE,
                    cursor=cursor3,
                    sql="SELECT id FROM T3",
                    args=None,
                    result_type=ResultType.NONE,
                    result_details=None,
                ),
                ChecksumStatement(
                    statement_type=CursorStatementType.CHECKSUM_ITERATOR,
                    cursor=cursor3,
                    result_type=ResultType.CHECKSUM,
                    result_details=third_checksum_iterator,
                ),
            ]
        )

        self._under_test.retry_transaction()

        self.assertIs(cursor1._result_set, retried_result_set_1)
        self.assertIs(cursor2._result_set, retried_result_set_2)
        self.assertIs(cursor3._result_set, retried_result_set_3)
        # Cursor 2 seamlessly yields remaining rows from the retried StreamedResultSet.
        self.assertEqual(list(second_checksum_iterator), [(20,), (30,)])

    def test_retry_transaction_closed_checksum_iterator_does_not_overwrite_result_set(
        self,
    ):
        checksum_iterator = ChecksumIterator(iter([(1,), (2,)]))
        self.assertEqual(next(checksum_iterator), (1,))
        checksum_iterator.close()

        original_result_set = mock.Mock()
        self._mock_cursor._itr = checksum_iterator
        self._mock_cursor._result_set = original_result_set

        retried_cursor = mock.Mock()
        retried_cursor._itr = iter([(1,), (2,)])
        retried_cursor._result_set = mock.Mock()
        self._under_test._connection.cursor.return_value = retried_cursor

        checksum_statement = ChecksumStatement(
            statement_type=CursorStatementType.CHECKSUM_ITERATOR,
            cursor=self._mock_cursor,
            result_type=ResultType.CHECKSUM,
            result_details=checksum_iterator,
        )
        self._under_test._statement_result_details_list.append(checksum_statement)

        self._under_test.retry_transaction()

        self.assertIs(self._mock_cursor._result_set, original_result_set)

    def test_checksum_iterator_retry_callback_invokes_retry_transaction_and_resumes(
        self,
    ):
        self._under_test._connection._client_transaction_started = True

        def failing_stream():
            yield (1,)
            raise Aborted("mid-stream abort")

        checksum_iterator = ChecksumIterator(
            failing_stream(),
            retry_callback=lambda: self._under_test.retry_transaction(
                default_retry_delay=0
            ),
        )
        self._mock_cursor._itr = checksum_iterator
        self._mock_cursor._result_set = mock.Mock()
        self._mock_cursor._batch_dml_rows_count = None
        self._mock_cursor._row_count = None

        retried_result_set = mock.Mock()
        retried_cursor = mock.Mock()
        retried_cursor.execute.side_effect = lambda _sql, _args: setattr(
            retried_cursor, "_itr", iter([(1,), (2,), (3,)])
        )
        retried_cursor._result_set = retried_result_set
        self._under_test._connection.cursor.return_value = retried_cursor

        self._under_test.add_execute_statement_for_retry(
            self._mock_cursor, SQL, ARGS, None, False
        )
        self._under_test.add_checksum_iterator_for_retry(
            self._mock_cursor, checksum_iterator
        )

        self.assertEqual(list(checksum_iterator), [(1,), (2,), (3,)])
        retried_cursor.execute.assert_called_once_with(SQL, ARGS)
        self.assertIs(self._mock_cursor._result_set, retried_result_set)

    def test_retry_transaction_with_request_id_augmented_grpc_errors(self):
        class StubRpcError(grpc.RpcError):
            def __init__(self, status_code, details_message):
                super().__init__()
                self._status_code = status_code
                self._details_message = details_message

            def code(self):
                return self._status_code

            def details(self):
                return self._details_message

            def trailing_metadata(self):
                return ()

        original_cause = wrap_with_request_id(
            from_grpc_error(
                StubRpcError(grpc.StatusCode.INVALID_ARGUMENT, "Division by zero")
            ),
            "1.1.1.1.1",
        )
        original_error = ProgrammingError(original_cause.details)
        original_error.__cause__ = original_cause

        retried_cause = wrap_with_request_id(
            from_grpc_error(
                StubRpcError(grpc.StatusCode.INVALID_ARGUMENT, "Division by zero")
            ),
            "1.1.1.1.2",
        )
        retried_error = ProgrammingError(retried_cause.details)
        retried_error.__cause__ = retried_cause

        execute_statement = ExecuteStatement(
            statement_type=CursorStatementType.EXECUTE,
            cursor=self._mock_cursor,
            sql=SQL,
            args=ARGS,
            result_type=ResultType.EXCEPTION,
            result_details=original_error,
        )
        self._under_test._statement_result_details_list.append(execute_statement)
        run_mock = self._under_test._connection.cursor().execute = mock.Mock()
        run_mock.side_effect = retried_error

        self._under_test.retry_transaction()

        run_mock.assert_called_once_with(SQL, ARGS)

    def test_checksum_iterator_repeated_abort_on_row_k_respects_max_retries(self):
        self._under_test._connection._client_transaction_started = True

        def stream_aborting_on_row_2():
            yield (1,)
            raise Aborted("row 2 aborted")

        checksum_iterator = ChecksumIterator(
            stream_aborting_on_row_2(),
            retry_callback=lambda: self._under_test.retry_transaction(
                default_retry_delay=0
            ),
        )
        self._mock_cursor._itr = checksum_iterator
        self._mock_cursor._result_set = mock.Mock()
        self._mock_cursor._batch_dml_rows_count = None
        self._mock_cursor._row_count = None

        retried_cursor = mock.Mock()
        retried_cursor.execute.side_effect = lambda _sql, _args: setattr(
            retried_cursor, "_itr", stream_aborting_on_row_2()
        )
        self._under_test._connection.cursor.return_value = retried_cursor

        self._under_test.add_execute_statement_for_retry(
            self._mock_cursor, SQL, ARGS, None, False
        )
        self._under_test.add_checksum_iterator_for_retry(
            self._mock_cursor, checksum_iterator
        )

        self.assertEqual(next(checksum_iterator), (1,))
        with mock.patch(
            "google.cloud.spanner_dbapi.transaction_helper.MAX_INTERNAL_RETRIES", 2
        ):
            with self.assertRaisesRegex(Aborted, "row 2 aborted"):
                next(checksum_iterator)

        self.assertEqual(retried_cursor.execute.call_count, 2)

        # Calling retry_transaction directly after exhaustion also raises without replaying.
        with mock.patch(
            "google.cloud.spanner_dbapi.transaction_helper.MAX_INTERNAL_RETRIES", 2
        ):
            with self.assertRaisesRegex(
                Aborted, "Internal transaction retry maximum exceeded."
            ):
                self._under_test.retry_transaction(default_retry_delay=0)

        self.assertEqual(retried_cursor.execute.call_count, 2)

        # reset() clears _retry_attempts for the next transaction.
        self._under_test.reset()
        self.assertEqual(self._under_test._retry_attempts, 0)

    def test_retry_transaction_closes_attempt_1_swapped_iterator_on_second_attempt(
        self,
    ):
        class CloseableRowIterator:
            def __init__(self, rows):
                self._iterator = iter(rows)
                self.close_count = 0

            def __iter__(self):
                return self

            def __next__(self):
                return next(self._iterator)

            def close(self):
                self.close_count += 1

        self._under_test._connection._client_transaction_started = True
        original_iterator = CloseableRowIterator([(1,), (2,)])
        attempt_1_iterator = CloseableRowIterator([(1,), (2,)])
        attempt_2_iterator = CloseableRowIterator([(1,), (2,)])

        checksum_iterator = ChecksumIterator(original_iterator)
        self._mock_cursor._itr = checksum_iterator
        self._mock_cursor._batch_dml_rows_count = None
        self._mock_cursor._row_count = None
        self.assertEqual(next(checksum_iterator), (1,))

        retried_cursor = mock.Mock()
        self._under_test._connection.cursor.return_value = retried_cursor
        replay_iterators = iter([attempt_1_iterator, attempt_2_iterator])
        dml_attempt = [0]

        def execute_side_effect(sql, _args):
            if sql.startswith("SELECT"):
                retried_cursor._itr = next(replay_iterators)
            else:
                dml_attempt[0] += 1
                if dml_attempt[0] == 1:
                    raise Aborted("abort on second statement")
                retried_cursor.rowcount = 1
                retried_cursor._batch_dml_rows_count = None

        retried_cursor.execute.side_effect = execute_side_effect

        self._under_test.add_execute_statement_for_retry(
            self._mock_cursor, "SELECT id FROM T", None, None, False
        )
        self._under_test.add_checksum_iterator_for_retry(
            self._mock_cursor, checksum_iterator
        )
        self._mock_cursor._row_count = 1
        self._mock_cursor.rowcount = 1
        self._under_test.add_execute_statement_for_retry(
            self._mock_cursor, "UPDATE T SET x = 1", None, None, False
        )

        self._under_test.retry_transaction(default_retry_delay=0)

        self.assertEqual(original_iterator.close_count, 1)
        self.assertEqual(attempt_1_iterator.close_count, 1)
        self.assertEqual(attempt_2_iterator.close_count, 0)
        self.assertIs(checksum_iterator.iterator, attempt_2_iterator)
        self.assertEqual(list(checksum_iterator), [(2,)])
