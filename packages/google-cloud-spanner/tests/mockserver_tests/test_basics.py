# Copyright 2024 Google LLC All rights reserved.
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

from google.api_core import exceptions

from google.cloud.spanner_admin_database_v1.types import spanner_database_admin
from google.cloud.spanner_dbapi import Connection
from google.cloud.spanner_dbapi.parsed_statement import AutocommitDmlMode
from google.cloud.spanner_v1 import (
    BeginTransactionRequest,
    ExecuteBatchDmlRequest,
    ExecuteSqlRequest,
    KeySet,
    ReadRequest,
    TransactionOptions,
    TransactionSelector,
    TypeCode,
)
from google.cloud.spanner_v1._async.transaction import Transaction as AsyncTransaction
from google.cloud.spanner_v1.database_sessions_manager import TransactionType
from google.cloud.spanner_v1.testing.mock_spanner import (
    PartialResultSetConfig,
    SpannerServicer,
)
from google.cloud.spanner_v1.transaction import Transaction
from tests._helpers import is_multiplexed_enabled
from tests.mockserver_tests.mock_server_test_base import (
    AsyncMockServerTestBase,
    MockServerTestBase,
    _make_partial_result_sets,
    aborted_status,
    add_error,
    add_execute_streaming_sql_error,
    add_execute_streaming_sql_results,
    add_multi_column_result,
    add_select1_result,
    add_single_result,
    add_streaming_read_error,
    add_update_count,
    deadline_exceeded_status,
    internal_server_error_status,
    invalid_argument_status,
    unavailable_status,
)


def _requests_of_type(spanner_service: SpannerServicer, request_type: type) -> list:
    return [
        request
        for request in spanner_service.requests
        if isinstance(request, request_type)
    ]


_RETRYABLE_INTERNAL_ERROR_MESSAGES = (
    "Received RST_STREAM with error code 2",
    "stream terminated by RST_STREAM",
    "Received unexpected EOS on DATA frame from server",
    "HTTP/2 error code: INTERNAL_ERROR",
    "Connection closed with unknown cause",
    "Authentication backend internal server error. Please retry",
    "Authentication backend internal server error. Please retry.",
)


class TestBasics(MockServerTestBase):
    def test_select1(self):
        add_select1_result()
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            result_list = []
            for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest],
            TransactionType.READ_ONLY,
        )

    def test_create_table(self):
        database_admin_api = self.client.database_admin_api
        request = spanner_database_admin.UpdateDatabaseDdlRequest(
            dict(
                database=database_admin_api.database_path(
                    "test-project", "test-instance", "test-database"
                ),
                statements=[
                    "CREATE TABLE Test (Id INT64, Value STRING(MAX)) PRIMARY KEY (Id)",
                ],
            )
        )
        operation = database_admin_api.update_database_ddl(request)
        operation.result(1)

    # TODO: Move this to a separate class once the mock server test setup has
    #       been re-factored to use a base class for the boiler plate code.
    def test_dbapi_partitioned_dml(self):
        sql = "UPDATE singers SET foo='bar' WHERE active = true"
        add_update_count(sql, 100, AutocommitDmlMode.PARTITIONED_NON_ATOMIC)
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        connection.set_autocommit_dml_mode(AutocommitDmlMode.PARTITIONED_NON_ATOMIC)
        with connection.cursor() as cursor:
            # Note: SQLAlchemy uses [] as the list of parameters for statements
            # with no parameters.
            cursor.execute(sql, [])
            self.assertEqual(100, cursor.rowcount)
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [BeginTransactionRequest, ExecuteSqlRequest],
            TransactionType.PARTITIONED,
            allow_multiple_batch_create=True,
        )
        # Find the first BeginTransactionRequest after session creation
        idx = 0
        from google.cloud.spanner_v1 import (
            BatchCreateSessionsRequest,
            CreateSessionRequest,
        )

        while idx < len(requests) and isinstance(
            requests[idx], BatchCreateSessionsRequest
        ):
            idx += 1
        if (
            is_multiplexed_enabled(TransactionType.PARTITIONED)
            and idx < len(requests)
            and isinstance(requests[idx], CreateSessionRequest)
        ):
            idx += 1
        begin_request: BeginTransactionRequest = requests[idx]
        self.assertEqual(
            TransactionOptions(dict(partitioned_dml={})), begin_request.options
        )

    def test_dbapi_partitioned_dml_with_parameters(self):
        sql = "UPDATE singers SET foo = %s WHERE active = %s"
        expected_sql = "UPDATE singers SET foo = @a0 WHERE active = @a1"
        add_update_count(expected_sql, 42, AutocommitDmlMode.PARTITIONED_NON_ATOMIC)
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        connection.set_autocommit_dml_mode(AutocommitDmlMode.PARTITIONED_NON_ATOMIC)
        with connection.cursor() as cursor:
            cursor.execute(sql, ["bar", True])
            self.assertEqual(42, cursor.rowcount)
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [BeginTransactionRequest, ExecuteSqlRequest],
            TransactionType.PARTITIONED,
            allow_multiple_batch_create=True,
        )
        execute_requests = [
            request for request in requests if isinstance(request, ExecuteSqlRequest)
        ]
        self.assertEqual(len(execute_requests), 1)
        self.assertEqual(execute_requests[0].sql, expected_sql)
        self.assertEqual(execute_requests[0].params["a0"], "bar")
        self.assertEqual(execute_requests[0].params["a1"], True)
        self.assertEqual(execute_requests[0].param_types["a0"].code, TypeCode.STRING)
        self.assertEqual(execute_requests[0].param_types["a1"].code, TypeCode.BOOL)

    def test_dbapi_partitioned_dml_does_not_add_dummy_where(self):
        sql = "UPDATE singers SET foo = %s"
        expected_sql = "UPDATE singers SET foo = @a0"
        add_update_count(expected_sql, 15, AutocommitDmlMode.PARTITIONED_NON_ATOMIC)
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        connection.set_autocommit_dml_mode(AutocommitDmlMode.PARTITIONED_NON_ATOMIC)
        with connection.cursor() as cursor:
            cursor.execute(sql, ["baz"])
            self.assertEqual(15, cursor.rowcount)
        requests = self.spanner_service.requests
        execute_requests = [
            request for request in requests if isinstance(request, ExecuteSqlRequest)
        ]
        self.assertEqual(len(execute_requests), 1)
        self.assertEqual(execute_requests[0].sql, expected_sql)
        self.assertNotIn("WHERE", execute_requests[0].sql)

    def test_dbapi_transactional_dml_adds_dummy_where(self):
        sql = "UPDATE singers SET foo = %s"
        expected_sql = "UPDATE singers SET foo = @a0 WHERE 1=1"
        add_update_count(expected_sql, 1)
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(sql, ["baz"])
            self.assertEqual(1, cursor.rowcount)
        requests = self.spanner_service.requests
        execute_requests = [
            request for request in requests if isinstance(request, ExecuteSqlRequest)
        ]
        self.assertEqual(len(execute_requests), 1)
        self.assertEqual(execute_requests[0].sql, expected_sql)

    def test_dbapi_executemany_unqualified_update_adds_dummy_where(self):
        sql = "UPDATE singers SET foo = %s"
        expected_sql = "UPDATE singers SET foo = @a0 WHERE 1=1"
        add_update_count(expected_sql, 1)
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.executemany(sql, [("bar",), ("baz",)])
            self.assertEqual(2, cursor.rowcount)
        requests = self.spanner_service.requests
        batch_requests = [
            request
            for request in requests
            if isinstance(request, ExecuteBatchDmlRequest)
        ]
        self.assertEqual(len(batch_requests), 1)
        self.assertEqual(len(batch_requests[0].statements), 2)
        self.assertEqual(batch_requests[0].statements[0].sql, expected_sql)
        self.assertEqual(batch_requests[0].statements[1].sql, expected_sql)

    def test_dbapi_batch_dml_unqualified_update_adds_dummy_where(self):
        sql = "UPDATE singers SET foo = 'bar'"
        expected_sql = "UPDATE singers SET foo = 'bar' WHERE 1=1"
        add_update_count(expected_sql, 1)
        connection = Connection(self.instance, self.database)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("start batch dml")
            cursor.execute(sql)
            cursor.execute(sql)
            cursor.execute("run batch")
            self.assertEqual(2, cursor.rowcount)
        requests = self.spanner_service.requests
        batch_requests = [
            request
            for request in requests
            if isinstance(request, ExecuteBatchDmlRequest)
        ]
        self.assertEqual(len(batch_requests), 1)
        self.assertEqual(len(batch_requests[0].statements), 2)
        self.assertEqual(batch_requests[0].statements[0].sql, expected_sql)
        self.assertEqual(batch_requests[0].statements[1].sql, expected_sql)

    def test_batch_create_sessions_unavailable(self):
        add_select1_result()
        add_error(SpannerServicer.BatchCreateSessions.__name__, unavailable_status())
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            result_list = []
            for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest],
            TransactionType.READ_ONLY,
            allow_multiple_batch_create=True,
        )

    def test_execute_streaming_sql_unavailable(self):
        add_select1_result()
        # Add an UNAVAILABLE error that is returned the first time the
        # ExecuteStreamingSql RPC is called.
        add_error(SpannerServicer.ExecuteStreamingSql.__name__, unavailable_status())
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            result_list = []
            for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest, ExecuteSqlRequest],
            TransactionType.READ_ONLY,
        )

    def test_last_statement_update(self):
        sql = "update my_table set my_col=1 where id=2"
        add_update_count(sql, 1)
        self.database.run_in_transaction(
            lambda transaction: transaction.execute_update(sql, last_statement=True)
        )
        requests = list(
            filter(
                lambda msg: isinstance(msg, ExecuteSqlRequest),
                self.spanner_service.requests,
            )
        )
        self.assertEqual(1, len(requests), msg=requests)
        self.assertTrue(requests[0].last_statement, requests[0])

    def test_last_statement_batch_update(self):
        sql = "update my_table set my_col=1 where id=2"
        add_update_count(sql, 1)
        self.database.run_in_transaction(
            lambda transaction: transaction.batch_update(
                [sql, sql], last_statement=True
            )
        )
        requests = list(
            filter(
                lambda msg: isinstance(msg, ExecuteBatchDmlRequest),
                self.spanner_service.requests,
            )
        )
        self.assertEqual(1, len(requests), msg=requests)
        self.assertTrue(requests[0].last_statements, requests[0])

    def test_last_statement_query(self):
        sql = "insert into my_table (value) values ('One') then return id"
        add_single_result(sql, "c", TypeCode.INT64, [("1",)])
        self.database.run_in_transaction(
            lambda transaction: _execute_query(transaction, sql)
        )
        requests = list(
            filter(
                lambda msg: isinstance(msg, ExecuteSqlRequest),
                self.spanner_service.requests,
            )
        )
        self.assertEqual(1, len(requests), msg=requests)
        self.assertTrue(requests[0].last_statement, requests[0])

    def test_execute_streaming_sql_last_field(self):
        partial_result_sets = _make_partial_result_sets(
            [("ID", TypeCode.INT64), ("NAME", TypeCode.STRING)],
            [
                {"values": ["1", "ABC", "2", "DEF"]},
                {"values": ["3", "GHI"], "last": True},
            ],
        )

        sql = "select * from my_table"
        add_execute_streaming_sql_results(sql, partial_result_sets)
        count = 1
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(sql)
            result_list = []
            for row in results:
                result_list.append(row)
                self.assertEqual(count, row[0])
                count += 1
            self.assertEqual(3, len(result_list))
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest],
            TransactionType.READ_ONLY,
        )

    def test_execute_streaming_sql_mid_stream_error_at_zero(self):
        # Verify partial_index=0 aborts the stream before any rows are yielded.
        sql = "select id from my_table"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(sql, 0, deadline_exceeded_status())
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(sql)
            row_iterator = iter(results)
            with self.assertRaisesRegex(
                exceptions.DeadlineExceeded, "Deadline exceeded."
            ):
                next(row_iterator)

    def test_execute_streaming_sql_mid_stream_error_after_partial_rows(self):
        # Verify partial_index=1 yields the first chunk's row before failing mid-stream.
        sql = "select id from my_table"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",), ("3",)])
        add_execute_streaming_sql_error(sql, 1, deadline_exceeded_status())
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(sql)
            row_iterator = iter(results)
            self.assertEqual([1], next(row_iterator))
            with self.assertRaisesRegex(
                exceptions.DeadlineExceeded, "Deadline exceeded."
            ):
                next(row_iterator)

    def test_execute_streaming_sql_mid_stream_error_after_all_chunks(self):
        # Verify partial_index >= len(chunks) yields every row then fails at stream end.
        sql = "select id from my_table"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(sql, 2, internal_server_error_status())
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(sql)
            row_iterator = iter(results)
            self.assertEqual([1], next(row_iterator))
            self.assertEqual([2], next(row_iterator))
            with self.assertRaisesRegex(
                exceptions.InternalServerError, "Internal server error."
            ):
                next(row_iterator)

    def test_execute_streaming_sql_mid_stream_unavailable_resumes(self):
        # Verify mid-stream UNAVAILABLE resumes via chunk 0's resume_token without losing rows.
        sql = "select id from my_table"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",), ("3",)])
        add_execute_streaming_sql_error(sql, 1, unavailable_status())
        with self.database.snapshot() as snapshot:
            rows = list(snapshot.execute_sql(sql))
            self.assertEqual([[1], [2], [3]], rows)
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(2, len(execute_requests))
        self.assertEqual(b"", execute_requests[0].resume_token)
        self.assertEqual(b"1", execute_requests[1].resume_token)

    def test_execute_streaming_sql_error_queue_and_validation(self):
        # Verify negative partial_index validation, FIFO per-call error dequeuing,
        # normal fallback once drained, and cleanup via clear_results().
        sql = "select id from my_table"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
        with self.assertRaisesRegex(ValueError, "partial_index must be non-negative"):
            add_execute_streaming_sql_error(sql, -1, aborted_status())

        add_execute_streaming_sql_error(sql, 1, deadline_exceeded_status())
        add_execute_streaming_sql_error(sql, 0, invalid_argument_status())

        with self.database.snapshot() as snapshot:
            first_iter = iter(snapshot.execute_sql(sql))
            self.assertEqual([1], next(first_iter))
            with self.assertRaisesRegex(
                exceptions.DeadlineExceeded, "Deadline exceeded."
            ):
                next(first_iter)

        with self.database.snapshot() as snapshot:
            second_iter = iter(snapshot.execute_sql(sql))
            with self.assertRaisesRegex(
                exceptions.InvalidArgument, "Invalid argument."
            ):
                next(second_iter)

        with self.database.snapshot() as snapshot:
            self.assertEqual([[1], [2]], list(snapshot.execute_sql(sql)))

        add_execute_streaming_sql_error(sql, 0, aborted_status())
        self.spanner_service.clear_results()
        add_single_result(sql, "id", TypeCode.INT64, [("1",)])
        with self.database.snapshot() as snapshot:
            self.assertEqual([[1]], list(snapshot.execute_sql(sql)))

    def test_execute_streaming_sql_mid_stream_error_with_explicit_partials(self):
        # Verify mid-stream error injection works with custom PartialResultSet streams.
        sql = "select id from my_table"
        partials = _make_partial_result_sets(
            [("id", TypeCode.INT64)],
            [
                {"values": ["1"], "resume_token": b"tok1"},
                {"values": ["2"], "resume_token": b"tok2", "last": True},
            ],
        )
        add_execute_streaming_sql_results(sql, partials)
        add_execute_streaming_sql_error(sql, 1, invalid_argument_status())
        with self.database.snapshot() as snapshot:
            row_iterator = iter(snapshot.execute_sql(sql))
            self.assertEqual([1], next(row_iterator))
            with self.assertRaisesRegex(
                exceptions.InvalidArgument, "Invalid argument."
            ):
                next(row_iterator)

    def test_streaming_read_mid_stream_error_and_resumption(self):
        # Verify StreamingRead supports both mid-stream failures and resume_token recovery.
        add_multi_column_result(
            "SELECT id, name FROM my_table",
            [("id", TypeCode.INT64), ("name", TypeCode.STRING)],
            [("1", "Alice"), ("2", "Bob"), ("3", "Charlie")],
        )
        add_streaming_read_error(
            "my_table", ["id", "name"], 1, deadline_exceeded_status()
        )
        with self.database.snapshot() as snapshot:
            row_iterator = iter(
                snapshot.read(
                    table="my_table",
                    columns=["id", "name"],
                    keyset=KeySet(all_=True),
                )
            )
            self.assertEqual([1, "Alice"], next(row_iterator))
            with self.assertRaisesRegex(
                exceptions.DeadlineExceeded, "Deadline exceeded."
            ):
                next(row_iterator)

        self.spanner_service.clear_requests()
        add_streaming_read_error("my_table", ["id", "name"], 1, unavailable_status())
        with self.database.snapshot() as snapshot:
            rows = list(
                snapshot.read(
                    table="my_table",
                    columns=["id", "name"],
                    keyset=KeySet(all_=True),
                )
            )
            self.assertEqual([[1, "Alice"], [2, "Bob"], [3, "Charlie"]], rows)

        read_requests = _requests_of_type(self.spanner_service, ReadRequest)
        self.assertEqual(2, len(read_requests))
        self.assertEqual(b"", read_requests[0].resume_token)
        self.assertEqual(b"1", read_requests[1].resume_token)

    def test_partial_result_set_mid_row_splitting_and_resume_tokens(self):
        # Verify max_values_per_chunk omits resume_token on mid-row chunks and only
        # emits tokens on row boundaries, restarting from b"" before a token arrives.
        sql = "select id, name, role from members"
        config = PartialResultSetConfig(max_values_per_chunk=2)
        add_multi_column_result(
            sql,
            [
                ("id", TypeCode.INT64),
                ("name", TypeCode.STRING),
                ("role", TypeCode.STRING),
            ],
            [
                ("1", "Alice", "admin"),
                ("2", "Bob", "user"),
                ("3", "Charlie", "guest"),
            ],
            chunk_config=config,
        )

        partials = self.spanner_service.mock_spanner.get_result_as_partial_result_sets(
            sql
        )
        # 9 values with max 2 values/chunk:
        # [1, Alice] (mid-row -> no token), [admin, 2] (mid-row -> no token),
        # [Bob, user] (row boundary -> b"1"), [3, Charlie] (mid-row -> no token),
        # [guest] (row boundary -> b"2")
        self.assertEqual(5, len(partials))
        self.assertEqual(
            [b"", b"", b"1", b"", b"2"],
            [partial.resume_token for partial in partials],
        )
        self.assertTrue(all(not partial.chunked_value for partial in partials))

        # Unavailable after mid-row chunk 0 (no resume_token received yet) restarts from scratch.
        add_execute_streaming_sql_error(sql, 1, unavailable_status())
        with self.database.snapshot() as snapshot:
            rows = list(snapshot.execute_sql(sql))
            self.assertEqual(
                [[1, "Alice", "admin"], [2, "Bob", "user"], [3, "Charlie", "guest"]],
                rows,
            )
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(2, len(execute_requests))
        self.assertEqual(b"", execute_requests[1].resume_token)

        # Unavailable after chunk 2 (row 2 boundary, resume_token=b"1") resumes from chunk 3.
        self.spanner_service.clear_requests()
        add_execute_streaming_sql_error(sql, 3, unavailable_status())
        with self.database.snapshot() as snapshot:
            rows = list(snapshot.execute_sql(sql))
            self.assertEqual(
                [[1, "Alice", "admin"], [2, "Bob", "user"], [3, "Charlie", "guest"]],
                rows,
            )
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(2, len(execute_requests))
        self.assertEqual(b"1", execute_requests[1].resume_token)

    def test_partial_result_set_chunked_values_and_resume_tokens(self):
        # Verify max_string_chunk_length sets chunked_value=True without resume_token on
        # intermediate string splits and resumes from b"" until a row end emits a token.
        sql = "select id, payload from docs"
        config = PartialResultSetConfig(max_string_chunk_length=4)
        add_multi_column_result(
            sql,
            [("id", TypeCode.STRING), ("payload", TypeCode.STRING)],
            [("id1", "hello world"), ("id2", "abcdef")],
            chunk_config=config,
        )

        partials = self.spanner_service.mock_spanner.get_result_as_partial_result_sets(
            sql
        )
        # Row 1: ["id1", "hell"] (chunked -> no token), ["o wo"] (chunked -> no token),
        #        ["rld"] (row end -> b"1")
        # Row 2: ["id2", "abcd"] (chunked -> no token), ["ef"] (row end -> b"2")
        self.assertEqual(5, len(partials))
        self.assertEqual(
            [True, True, False, True, False],
            [partial.chunked_value for partial in partials],
        )
        self.assertEqual(
            [b"", b"", b"1", b"", b"2"],
            [partial.resume_token for partial in partials],
        )

        # Unavailable during chunked value (before resume_token) restarts cleanly.
        add_execute_streaming_sql_error(sql, 1, unavailable_status())
        with self.database.snapshot() as snapshot:
            rows = list(snapshot.execute_sql(sql))
            self.assertEqual([["id1", "hello world"], ["id2", "abcdef"]], rows)
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(b"", execute_requests[1].resume_token)

        # Unavailable after row 1 completed (resume_token=b"1") resumes at row 2.
        self.spanner_service.clear_requests()
        add_execute_streaming_sql_error(sql, 3, unavailable_status())
        with self.database.snapshot() as snapshot:
            rows = list(snapshot.execute_sql(sql))
            self.assertEqual([["id1", "hello world"], ["id2", "abcdef"]], rows)
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(b"1", execute_requests[1].resume_token)

    def test_partial_result_set_without_resume_tokens_and_explicit_chunked_value(self):
        # Verify emit_resume_tokens=False suppresses tokens (forcing client buffering
        # until failure) and manual _make_partial_result_sets chunked_value reassembly.
        sql = "select id, text from notes"
        add_multi_column_result(
            sql,
            [("id", TypeCode.INT64), ("text", TypeCode.STRING)],
            [("1", "one"), ("2", "two")],
            chunk_config=PartialResultSetConfig(emit_resume_tokens=False),
        )
        partials = self.spanner_service.mock_spanner.get_result_as_partial_result_sets(
            sql
        )
        self.assertEqual([b"", b""], [partial.resume_token for partial in partials])

        # Without resume_token on chunk 0, _restart_on_unavailable buffers until chunk 1 errors.
        add_execute_streaming_sql_error(sql, 1, deadline_exceeded_status())
        with self.database.snapshot() as snapshot:
            row_iterator = iter(snapshot.execute_sql(sql))
            with self.assertRaisesRegex(
                exceptions.DeadlineExceeded, "Deadline exceeded."
            ):
                next(row_iterator)

        # With emit_resume_tokens=False, UNAVAILABLE drops the buffered chunk and
        # restarts from b"" without duplicating rows.
        self.spanner_service.clear_requests()
        add_execute_streaming_sql_error(sql, 1, unavailable_status())
        with self.database.snapshot() as snapshot:
            self.assertEqual([[1, "one"], [2, "two"]], list(snapshot.execute_sql(sql)))
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(
            [b"", b""], [request.resume_token for request in execute_requests]
        )

        # Verify _make_partial_result_sets supports chunked_value=True with a
        # non-empty resume_token and resumes cleanly mid-string on UNAVAILABLE.
        explicit_partials = _make_partial_result_sets(
            [("id", TypeCode.INT64), ("text", TypeCode.STRING)],
            [
                {
                    "values": ["1", "hel"],
                    "chunked_value": True,
                    "resume_token": b"mid_tok",
                },
                {"values": ["lo"], "last": True},
            ],
        )
        add_execute_streaming_sql_results(sql, explicit_partials)
        self.spanner_service.clear_requests()
        add_execute_streaming_sql_error(sql, 1, unavailable_status())
        with self.database.snapshot() as snapshot:
            self.assertEqual([[1, "hello"]], list(snapshot.execute_sql(sql)))
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(
            [b"", b"mid_tok"], [request.resume_token for request in execute_requests]
        )

    def test_partial_result_set_config_validation(self):
        # Verify PartialResultSetConfig rejects non-positive chunking thresholds.
        with self.assertRaisesRegex(
            ValueError, "max_values_per_chunk must be positive"
        ):
            PartialResultSetConfig(max_values_per_chunk=0)
        with self.assertRaisesRegex(
            ValueError, "max_string_chunk_length must be positive"
        ):
            PartialResultSetConfig(max_string_chunk_length=0)

    def test_partial_result_set_set_last_flag_and_non_mutation(self):
        # Verify set_last_flag marks only the final chunk and inline-begin transaction
        # metadata does not mutate caller-registered explicit PartialResultSet objects.
        sql = "select id from last_flag_table"
        add_single_result(
            sql,
            "id",
            TypeCode.INT64,
            [("1",), ("2",)],
            chunk_config=PartialResultSetConfig(set_last_flag=True),
        )
        partials = self.spanner_service.mock_spanner.get_result_as_partial_result_sets(
            sql
        )
        self.assertEqual([False, True], [partial.last for partial in partials])

        # Registered explicit partials should not be mutated by inline begin transactions.
        explicit_sql = "select id from explicit_table"
        explicit_partials = _make_partial_result_sets(
            [("id", TypeCode.INT64)],
            [{"values": ["1"], "last": True}],
        )
        add_execute_streaming_sql_results(explicit_sql, explicit_partials)
        self.database.run_in_transaction(
            lambda transaction: list(transaction.execute_sql(explicit_sql))
        )
        self.assertEqual(b"", explicit_partials[0].metadata.transaction.id)

    def test_partial_result_set_combined_chunking_options(self):
        # Verify combining max_values_per_chunk, max_string_chunk_length, and set_last_flag.
        sql = "select id, payload, tag from items"
        add_multi_column_result(
            sql,
            [
                ("id", TypeCode.INT64),
                ("payload", TypeCode.STRING),
                ("tag", TypeCode.STRING),
            ],
            [("1", "abcdefgh", "t1"), ("2", "xy", "t2")],
            chunk_config=PartialResultSetConfig(
                max_values_per_chunk=2,
                max_string_chunk_length=4,
                set_last_flag=True,
            ),
        )
        partials = self.spanner_service.mock_spanner.get_result_as_partial_result_sets(
            sql
        )
        # Row 1: [1, "abcd"] (chunked -> no token), ["efgh", "t1"] (row end -> b"1"),
        # Row 2: [2, "xy"] (mid-row -> no token), ["t2"] (last -> b"2", last=True)
        self.assertEqual(
            [True, False, False, False],
            [partial.chunked_value for partial in partials],
        )
        self.assertEqual(
            [b"", b"1", b"", b"2"], [partial.resume_token for partial in partials]
        )
        self.assertEqual(
            [False, False, False, True], [partial.last for partial in partials]
        )
        with self.database.snapshot() as snapshot:
            self.assertEqual(
                [[1, "abcdefgh", "t1"], [2, "xy", "t2"]],
                list(snapshot.execute_sql(sql)),
            )

    def test_partial_result_set_single_column_batching_and_resets(self):
        # Verify multiple 1-column rows batch into a single chunk ending at a row
        # boundary, and re-registering via add_result resets chunking & explicit partials.
        batch_sql = "select id from batched"
        add_single_result(
            batch_sql,
            "id",
            TypeCode.INT64,
            [("1",), ("2",), ("3",)],
            chunk_config=PartialResultSetConfig(max_values_per_chunk=2),
        )
        batch_partials = (
            self.spanner_service.mock_spanner.get_result_as_partial_result_sets(
                batch_sql
            )
        )
        self.assertEqual(2, len(batch_partials))
        self.assertEqual(
            [b"1", b"2"], [partial.resume_token for partial in batch_partials]
        )
        with self.database.snapshot() as snapshot:
            self.assertEqual([[1], [2], [3]], list(snapshot.execute_sql(batch_sql)))

        # Re-registering without chunk_config resets previous chunking behavior, and
        # overrides any earlier add_execute_streaming_sql_results registration.
        add_execute_streaming_sql_results(batch_sql, [])
        add_single_result(batch_sql, "id", TypeCode.INT64, [("1",), ("2",), ("3",)])
        reset_partials = (
            self.spanner_service.mock_spanner.get_result_as_partial_result_sets(
                batch_sql
            )
        )
        self.assertEqual(3, len(reset_partials))
        with self.database.snapshot() as snapshot:
            self.assertEqual([[1], [2], [3]], list(snapshot.execute_sql(batch_sql)))

    def test_partial_result_set_empty_result_set_with_set_last_flag(self):
        # Verify 0-row ResultSet honors set_last_flag=True without emitting a resume_token.
        empty_sql = "select id from empty_table"
        add_single_result(
            empty_sql,
            "id",
            TypeCode.INT64,
            [],
            chunk_config=PartialResultSetConfig(set_last_flag=True),
        )
        empty_partials = (
            self.spanner_service.mock_spanner.get_result_as_partial_result_sets(
                empty_sql
            )
        )
        self.assertEqual(1, len(empty_partials))
        self.assertTrue(empty_partials[0].last)
        self.assertEqual(b"", empty_partials[0].resume_token)
        with self.database.snapshot() as snapshot:
            self.assertEqual([], list(snapshot.execute_sql(empty_sql)))

    def test_partial_result_set_last_flag_without_tokens_and_trailing_error(self):
        # Verify set_last_flag=True with emit_resume_tokens=False completes cleanly,
        # and trailing errors past last=True are drained without failing the caller.
        no_token_last_sql = "select id from no_token_last"
        add_single_result(
            no_token_last_sql,
            "id",
            TypeCode.INT64,
            [("10",), ("20",)],
            chunk_config=PartialResultSetConfig(
                emit_resume_tokens=False, set_last_flag=True
            ),
        )
        with self.database.snapshot() as snapshot:
            self.assertEqual(
                [[10], [20]], list(snapshot.execute_sql(no_token_last_sql))
            )
        add_execute_streaming_sql_error(
            no_token_last_sql, 5, internal_server_error_status()
        )
        with self.database.snapshot() as snapshot:
            self.assertEqual(
                [[10], [20]], list(snapshot.execute_sql(no_token_last_sql))
            )

    def test_streaming_read_empty_columns_wildcard_lookup(self):
        # Verify ReadRequest with empty columns maps to SELECT * FROM <table>.
        add_single_result(
            "SELECT * FROM wildcard_table", "id", TypeCode.INT64, [("9",)]
        )
        add_streaming_read_error(
            "wildcard_table", [], 1, internal_server_error_status()
        )
        with self.database.snapshot() as snapshot:
            row_iterator = iter(
                snapshot.read(
                    table="wildcard_table",
                    columns=[],
                    keyset=KeySet(all_=True),
                )
            )
            self.assertEqual([9], next(row_iterator))
            with self.assertRaisesRegex(
                exceptions.InternalServerError, "Internal server error."
            ):
                next(row_iterator)

    def test_streaming_read_chunking_and_boundary_errors(self):
        # Verify StreamingRead handles combined mid-row/string chunking plus
        # boundary errors at partial_index=0 and partial_index >= len(chunks).
        add_multi_column_result(
            "SELECT id, payload FROM chunked_read",
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("1", "hello world"), ("2", "ok")],
            chunk_config=PartialResultSetConfig(
                max_values_per_chunk=2,
                max_string_chunk_length=4,
            ),
        )
        add_streaming_read_error(
            "chunked_read", ["id", "payload"], 1, unavailable_status()
        )
        with self.database.snapshot() as snapshot:
            self.assertEqual(
                [[1, "hello world"], [2, "ok"]],
                list(
                    snapshot.read(
                        table="chunked_read",
                        columns=["id", "payload"],
                        keyset=KeySet(all_=True),
                    )
                ),
            )

        # partial_index=0 and partial_index >= chunk count on StreamingRead.
        add_streaming_read_error(
            "chunked_read", ["id", "payload"], 0, invalid_argument_status()
        )
        with self.database.snapshot() as snapshot:
            row_iterator = iter(
                snapshot.read(
                    table="chunked_read",
                    columns=["id", "payload"],
                    keyset=KeySet(all_=True),
                )
            )
            with self.assertRaisesRegex(
                exceptions.InvalidArgument, "Invalid argument."
            ):
                next(row_iterator)

        add_streaming_read_error(
            "chunked_read", ["id", "payload"], 10, internal_server_error_status()
        )
        with self.database.snapshot() as snapshot:
            row_iterator = iter(
                snapshot.read(
                    table="chunked_read",
                    columns=["id", "payload"],
                    keyset=KeySet(all_=True),
                )
            )
            self.assertEqual([1, "hello world"], next(row_iterator))
            self.assertEqual([2, "ok"], next(row_iterator))
            with self.assertRaisesRegex(
                exceptions.InternalServerError, "Internal server error."
            ):
                next(row_iterator)

    def test_execute_streaming_sql_multiple_resumptions_and_rst_stream(self):
        # Verify sequential mid-stream UNAVAILABLE and RST_STREAM errors trigger
        # multi-hop resumption using per-RPC partial_index offsets (b"" -> b"1" -> b"2").
        sql = "select id from multi_resume"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",), ("3",), ("4",)])
        # First RPC yields chunk 0 (token b"1"), fails at per-RPC index 1;
        # second RPC resumes at b"1", yields chunk 1 (token b"2"), fails at per-RPC index 1;
        # third RPC resumes at b"2", yields chunks 2 and 3.
        add_execute_streaming_sql_error(sql, 1, unavailable_status())
        add_execute_streaming_sql_error(
            sql,
            1,
            internal_server_error_status("Received RST_STREAM with error code 2"),
        )
        with self.database.snapshot() as snapshot:
            self.assertEqual([[1], [2], [3], [4]], list(snapshot.execute_sql(sql)))
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(
            [b"", b"1", b"2"],
            [request.resume_token for request in execute_requests],
        )

    def test_execute_streaming_sql_retries_all_retryable_internal_errors(self):
        for index, error_message in enumerate(_RETRYABLE_INTERNAL_ERROR_MESSAGES):
            with self.subTest(error_message=error_message):
                self.spanner_service.requests.clear()
                sql = f"select id from retry_internal_{index}"
                add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
                add_execute_streaming_sql_error(
                    sql, 1, internal_server_error_status(error_message)
                )
                with self.database.snapshot() as snapshot:
                    self.assertEqual([[1], [2]], list(snapshot.execute_sql(sql)))
                execute_requests = _requests_of_type(
                    self.spanner_service, ExecuteSqlRequest
                )
                self.assertEqual(
                    [b"", b"1"],
                    [request.resume_token for request in execute_requests],
                )

    def test_execute_streaming_sql_initial_and_non_retryable_internal_errors(self):
        # Initial-stream failure (partial_index=0) retries with empty resume_token.
        retryable_sql = "select id from initial_retry_internal"
        add_single_result(retryable_sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(
            retryable_sql,
            0,
            internal_server_error_status(
                "Authentication backend internal server error. Please retry."
            ),
        )
        self.spanner_service.requests.clear()
        with self.database.snapshot() as snapshot:
            self.assertEqual([[1], [2]], list(snapshot.execute_sql(retryable_sql)))
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(
            [b"", b""],
            [request.resume_token for request in execute_requests],
        )

        # Non-retryable INTERNAL error fails immediately without retrying.
        non_retryable_sql = "select id from non_retry_internal"
        add_single_result(non_retryable_sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(
            non_retryable_sql,
            0,
            internal_server_error_status("Internal server error."),
        )
        self.spanner_service.requests.clear()
        with self.database.snapshot() as snapshot:
            with self.assertRaisesRegex(
                exceptions.InternalServerError, "Internal server error."
            ):
                list(snapshot.execute_sql(non_retryable_sql))
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(1, len(execute_requests))

    def test_inline_begin_transaction_mid_stream_unavailable_switches_to_id(self):
        # Verify resuming an inline-begin read-write stream switches from
        # transaction.begin to transaction.id when sending resume_token.
        sql = "select id from rw_resume"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(sql, 1, unavailable_status())

        def _query(transaction: Transaction):
            return list(transaction.execute_sql(sql))

        rows = self.database.run_in_transaction(_query)
        self.assertEqual([[1], [2]], rows)
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(2, len(execute_requests))
        self.assertNotEqual(TransactionOptions(), execute_requests[0].transaction.begin)
        self.assertEqual(b"", execute_requests[0].resume_token)
        self.assertEqual(TransactionOptions(), execute_requests[1].transaction.begin)
        self.assertTrue(execute_requests[1].transaction.id)
        self.assertEqual(b"1", execute_requests[1].resume_token)

    def test_execute_streaming_sql_server_validation_and_empty_partials(self):
        # Verify mock server rejects unknown resume_token and begin+resume_token with
        # INVALID_ARGUMENT, and returns empty results when [] partials are registered.
        sql = "select id from validation_table"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])

        session = self.database.session()
        session.create()
        api = self.database.spanner_api

        # Unknown resume_token must raise InvalidArgument instead of returning empty OK.
        request_metadata = [("x-goog-spanner-request-id", "1.1.1.1.1.1")]
        with self.assertRaisesRegex(exceptions.InvalidArgument, "Invalid resume_token"):
            list(
                api.execute_streaming_sql(
                    request=ExecuteSqlRequest(
                        session=session.name,
                        sql=sql,
                        resume_token=b"non-existent-token",
                    ),
                    metadata=request_metadata,
                )
            )

        # Combining transaction.begin with non-empty resume_token must raise InvalidArgument.
        with self.assertRaisesRegex(
            exceptions.InvalidArgument,
            "Cannot combine begin transaction with resume_token",
        ):
            list(
                api.execute_streaming_sql(
                    request=ExecuteSqlRequest(
                        session=session.name,
                        sql=sql,
                        transaction=TransactionSelector(
                            begin=TransactionOptions(read_only={})
                        ),
                        resume_token=b"1",
                    ),
                    metadata=request_metadata,
                )
            )

        # Explicitly registered empty PartialResultSet list does not fall back to results.
        empty_explicit_sql = "select id from explicit_empty"
        add_execute_streaming_sql_results(empty_explicit_sql, [])
        with self.database.snapshot() as snapshot:
            self.assertEqual([], list(snapshot.execute_sql(empty_explicit_sql)))

    def test_streamed_result_set_helpers_with_chunked_streams(self):
        # Verify StreamedResultSet helpers (one, one_or_none, to_dict_list, lazy_decode)
        # reassemble mid-row and chunked_value=True streams cleanly.
        sql_one = "select id, payload from helper_one"
        add_multi_column_result(
            sql_one,
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("7", "hello world")],
            chunk_config=PartialResultSetConfig(
                max_values_per_chunk=1, max_string_chunk_length=4
            ),
        )
        with self.database.snapshot(multi_use=True) as snapshot:
            self.assertEqual([7, "hello world"], snapshot.execute_sql(sql_one).one())
            self.assertEqual(
                [7, "hello world"], snapshot.execute_sql(sql_one).one_or_none()
            )
            self.assertEqual(
                [{"id": 7, "payload": "hello world"}],
                snapshot.execute_sql(sql_one).to_dict_list(),
            )
            lazy_results = snapshot.execute_sql(sql_one, lazy_decode=True)
            lazy_rows = list(lazy_results)
            self.assertEqual([7, "hello world"], lazy_results.decode_row(lazy_rows[0]))

    def test_dbapi_fetchall_mid_stream_deadline_exceeded_issue_19079(self):
        sql = "select id from issue_19079_deadline"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
        for read_only in (True, False):
            add_execute_streaming_sql_error(sql, 1, deadline_exceeded_status())
            connection = Connection(self.instance, self.database, read_only=read_only)
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    with self.assertRaisesRegex(
                        exceptions.DeadlineExceeded, "Deadline exceeded."
                    ):
                        cursor.fetchall()
            finally:
                connection.close()

    # TODO(https://github.com/googleapis/google-cloud-python/issues/19079):
    # Remove @unittest.expectedFailure once Cursor._fetch properly retries
    # mid-stream Aborted in read-write transactions and returns all rows.
    @unittest.expectedFailure
    def test_dbapi_fetchall_mid_stream_aborted_issue_19079(self):
        sql = "select id from issue_19079_aborted"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(sql, 1, aborted_status())
        connection = Connection(self.instance, self.database, read_only=False)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                self.assertEqual([[1], [2]], cursor.fetchall())
        finally:
            connection.close()

    def test_streamed_result_set_invalid_termination_raises_internal_error(self):
        for sql, fields, chunks, expected_message in _invalid_termination_scenarios():
            add_execute_streaming_sql_results(
                sql, _make_partial_result_sets(fields, chunks)
            )
            with self.database.snapshot(multi_use=True) as snapshot:
                with self.assertRaisesRegex(
                    exceptions.InternalServerError, expected_message
                ):
                    list(snapshot.execute_sql(sql))
                with self.assertRaisesRegex(
                    exceptions.InternalServerError, expected_message
                ):
                    snapshot.execute_sql(sql).one_or_none()
                with self.assertRaisesRegex(
                    exceptions.InternalServerError, expected_message
                ):
                    snapshot.execute_sql(sql).one()
                with self.assertRaisesRegex(
                    exceptions.InternalServerError, expected_message
                ):
                    snapshot.execute_sql(sql).to_dict_list()


class TestBasicsAsync(AsyncMockServerTestBase):
    async def test_async_select1(self):
        add_select1_result()
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql("select 1")
            result_list = []
            async for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest],
            TransactionType.READ_ONLY,
        )

    async def test_async_execute_streaming_sql_restarts_without_resume_token(self):
        # Verify chunk 0 without a resume_token (chunked_value=True) restarts from b"".
        sql = "select id, payload from async_restart_docs"
        add_multi_column_result(
            sql,
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("1", "hello world"), ("2", "abcdef")],
            chunk_config=PartialResultSetConfig(
                max_values_per_chunk=2, max_string_chunk_length=4
            ),
        )
        add_execute_streaming_sql_error(sql, 1, unavailable_status())
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(sql)
            rows = [row async for row in results]
            self.assertEqual([[1, "hello world"], [2, "abcdef"]], rows)
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(
            [b"", b""], [request.resume_token for request in execute_requests]
        )

    async def test_async_execute_streaming_sql_resumes_with_resume_token(self):
        # Verify chunk 2 row boundary emits resume_token=b"1" and resumes at index 3.
        sql = "select id, payload from async_row_boundary_docs"
        add_multi_column_result(
            sql,
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("1", "hello world"), ("2", "abcdef")],
            chunk_config=PartialResultSetConfig(max_string_chunk_length=4),
        )
        add_execute_streaming_sql_error(sql, 3, unavailable_status())
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(sql)
            rows = [row async for row in results]
            self.assertEqual([[1, "hello world"], [2, "abcdef"]], rows)
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(
            [b"", b"1"], [request.resume_token for request in execute_requests]
        )

    async def test_async_streaming_read_resumes_with_resume_token(self):
        # Verify async StreamingRead resumes from non-empty resume_token=b"1".
        add_multi_column_result(
            "SELECT id, payload FROM async_read_docs",
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("1", "hello world"), ("2", "abcdef")],
        )
        add_streaming_read_error(
            "async_read_docs", ["id", "payload"], 1, unavailable_status()
        )
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            read_results = await snapshot.read(
                table="async_read_docs",
                columns=["id", "payload"],
                keyset=KeySet(all_=True),
            )
            read_rows = [row async for row in read_results]
            self.assertEqual([[1, "hello world"], [2, "abcdef"]], read_rows)
        read_requests = _requests_of_type(self.spanner_service, ReadRequest)
        self.assertEqual(
            [b"", b"1"], [request.resume_token for request in read_requests]
        )

    async def test_async_execute_streaming_sql_mid_stream_deadline_exceeded(self):
        # Verify async iteration yields row 1 before raising mid-stream DeadlineExceeded.
        sql = "select id, payload from async_deadline_docs"
        add_multi_column_result(
            sql,
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("1", "hello world"), ("2", "abcdef")],
            chunk_config=PartialResultSetConfig(max_string_chunk_length=4),
        )
        add_execute_streaming_sql_error(sql, 3, deadline_exceeded_status())
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(sql)
            row_iterator = aiter(results)
            self.assertEqual([1, "hello world"], await anext(row_iterator))
            with self.assertRaisesRegex(
                exceptions.DeadlineExceeded, "Deadline exceeded."
            ):
                await anext(row_iterator)

    async def test_async_execute_streaming_sql_last_flag_trailing_error_drained(self):
        # Verify async _drain_stream absorbs trailing errors sent after last=True.
        sql = "select id from async_last_flag"
        add_single_result(
            sql,
            "id",
            TypeCode.INT64,
            [("10",), ("20",)],
            chunk_config=PartialResultSetConfig(set_last_flag=True),
        )
        add_execute_streaming_sql_error(sql, 5, internal_server_error_status())
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(sql)
            rows = [row async for row in results]
            self.assertEqual([[10], [20]], rows)

    async def test_async_execute_streaming_sql_multiple_resumptions_and_rst_stream(
        self,
    ):
        sql = "select id from async_multi_resume"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",), ("3",), ("4",)])
        add_execute_streaming_sql_error(sql, 1, unavailable_status())
        add_execute_streaming_sql_error(
            sql,
            1,
            internal_server_error_status("Received RST_STREAM with error code 2"),
        )
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(sql)
            self.assertEqual([[1], [2], [3], [4]], [row async for row in results])
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(
            [b"", b"1", b"2"],
            [request.resume_token for request in execute_requests],
        )

    async def test_async_inline_begin_transaction_mid_stream_unavailable_switches_to_id(
        self,
    ):
        sql = "select id from async_rw_resume"
        add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(sql, 1, unavailable_status())

        async def _query(transaction: AsyncTransaction):
            results = await transaction.execute_sql(sql)
            return [row async for row in results]

        database = await self.get_database()
        rows = await database.run_in_transaction(_query)
        self.assertEqual([[1], [2]], rows)
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(2, len(execute_requests))
        self.assertNotEqual(TransactionOptions(), execute_requests[0].transaction.begin)
        self.assertEqual(b"", execute_requests[0].resume_token)
        self.assertEqual(TransactionOptions(), execute_requests[1].transaction.begin)
        self.assertTrue(execute_requests[1].transaction.id)
        self.assertEqual(b"1", execute_requests[1].resume_token)

    async def test_async_streaming_read_chunking_and_boundary_errors(self):
        add_multi_column_result(
            "SELECT id, payload FROM async_chunked_read",
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("1", "hello world"), ("2", "ok")],
            chunk_config=PartialResultSetConfig(
                max_values_per_chunk=2,
                max_string_chunk_length=4,
            ),
        )
        add_streaming_read_error(
            "async_chunked_read", ["id", "payload"], 1, unavailable_status()
        )
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            read_results = await snapshot.read(
                table="async_chunked_read",
                columns=["id", "payload"],
                keyset=KeySet(all_=True),
            )
            self.assertEqual(
                [[1, "hello world"], [2, "ok"]],
                [row async for row in read_results],
            )

        add_streaming_read_error(
            "async_chunked_read", ["id", "payload"], 0, invalid_argument_status()
        )
        async with database.snapshot() as snapshot:
            read_results = await snapshot.read(
                table="async_chunked_read",
                columns=["id", "payload"],
                keyset=KeySet(all_=True),
            )
            row_iterator = aiter(read_results)
            with self.assertRaisesRegex(
                exceptions.InvalidArgument, "Invalid argument."
            ):
                await anext(row_iterator)

        add_streaming_read_error(
            "async_chunked_read", ["id", "payload"], 10, internal_server_error_status()
        )
        async with database.snapshot() as snapshot:
            read_results = await snapshot.read(
                table="async_chunked_read",
                columns=["id", "payload"],
                keyset=KeySet(all_=True),
            )
            row_iterator = aiter(read_results)
            self.assertEqual([1, "hello world"], await anext(row_iterator))
            self.assertEqual([2, "ok"], await anext(row_iterator))
            with self.assertRaisesRegex(
                exceptions.InternalServerError, "Internal server error."
            ):
                await anext(row_iterator)

    async def test_async_streamed_result_set_helpers_with_chunked_streams(self):
        sql_one = "select id, payload from async_helper_one"
        add_multi_column_result(
            sql_one,
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("7", "hello world")],
            chunk_config=PartialResultSetConfig(
                max_values_per_chunk=1, max_string_chunk_length=4
            ),
        )
        database = await self.get_database()
        async with database.snapshot(multi_use=True) as snapshot:
            self.assertEqual(
                [7, "hello world"], await (await snapshot.execute_sql(sql_one)).one()
            )
            self.assertEqual(
                [7, "hello world"],
                await (await snapshot.execute_sql(sql_one)).one_or_none(),
            )
            self.assertEqual(
                [{"id": 7, "payload": "hello world"}],
                await (await snapshot.execute_sql(sql_one)).to_dict_list(),
            )
            lazy_results = await snapshot.execute_sql(sql_one, lazy_decode=True)
            lazy_rows = [row async for row in lazy_results]
            self.assertEqual([7, "hello world"], lazy_results.decode_row(lazy_rows[0]))

    async def test_async_execute_streaming_sql_retries_all_retryable_internal_errors(
        self,
    ):
        database = await self.get_database()
        for index, error_message in enumerate(_RETRYABLE_INTERNAL_ERROR_MESSAGES):
            with self.subTest(error_message=error_message):
                self.spanner_service.requests.clear()
                sql = f"select id from async_retry_internal_{index}"
                add_single_result(sql, "id", TypeCode.INT64, [("1",), ("2",)])
                add_execute_streaming_sql_error(
                    sql, 1, internal_server_error_status(error_message)
                )
                async with database.snapshot() as snapshot:
                    results = await snapshot.execute_sql(sql)
                    rows = [row async for row in results]
                    self.assertEqual([[1], [2]], rows)
                execute_requests = _requests_of_type(
                    self.spanner_service, ExecuteSqlRequest
                )
                self.assertEqual(
                    [b"", b"1"],
                    [request.resume_token for request in execute_requests],
                )

    async def test_async_execute_streaming_sql_initial_and_non_retryable_internal_errors(
        self,
    ):
        database = await self.get_database()
        retryable_sql = "select id from async_initial_retry_internal"
        add_single_result(retryable_sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(
            retryable_sql,
            0,
            internal_server_error_status(
                "Authentication backend internal server error. Please retry."
            ),
        )
        self.spanner_service.requests.clear()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(retryable_sql)
            rows = [row async for row in results]
            self.assertEqual([[1], [2]], rows)
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(
            [b"", b""],
            [request.resume_token for request in execute_requests],
        )

        non_retryable_sql = "select id from async_non_retry_internal"
        add_single_result(non_retryable_sql, "id", TypeCode.INT64, [("1",), ("2",)])
        add_execute_streaming_sql_error(
            non_retryable_sql,
            0,
            internal_server_error_status("Internal server error."),
        )
        self.spanner_service.requests.clear()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(non_retryable_sql)
            with self.assertRaisesRegex(
                exceptions.InternalServerError, "Internal server error."
            ):
                async for _ in results:
                    pass
        execute_requests = _requests_of_type(self.spanner_service, ExecuteSqlRequest)
        self.assertEqual(1, len(execute_requests))

    async def test_async_streamed_result_set_invalid_termination_raises_internal_error(
        self,
    ):
        database = await self.get_database()
        for sql, fields, chunks, expected_message in _invalid_termination_scenarios(
            "async_"
        ):
            add_execute_streaming_sql_results(
                sql, _make_partial_result_sets(fields, chunks)
            )
            async with database.snapshot(multi_use=True) as snapshot:
                results = await snapshot.execute_sql(sql)
                with self.assertRaisesRegex(
                    exceptions.InternalServerError, expected_message
                ):
                    _ = [row async for row in results]
                one_or_none_results = await snapshot.execute_sql(sql)
                with self.assertRaisesRegex(
                    exceptions.InternalServerError, expected_message
                ):
                    await one_or_none_results.one_or_none()
                one_results = await snapshot.execute_sql(sql)
                with self.assertRaisesRegex(
                    exceptions.InternalServerError, expected_message
                ):
                    await one_results.one()
                dict_results = await snapshot.execute_sql(sql)
                with self.assertRaisesRegex(
                    exceptions.InternalServerError, expected_message
                ):
                    await dict_results.to_dict_list()


def _invalid_termination_scenarios(prefix: str = ""):
    fields = [("id", TypeCode.INT64), ("payload", TypeCode.STRING)]
    return [
        (
            f"select id, payload from {prefix}invalid_chunk_eof",
            fields,
            [{"values": ["1", "partial "], "chunked_value": True, "last": False}],
            "Stream ended while waiting for continuation of chunked value.",
        ),
        (
            f"select id, payload from {prefix}invalid_chunk_last",
            fields,
            [{"values": ["1", "partial "], "chunked_value": True, "last": True}],
            "Stream ended while waiting for continuation of chunked value.",
        ),
        (
            f"select id, payload from {prefix}invalid_chunk_empty_last",
            fields,
            [
                {"values": ["1", "partial "], "chunked_value": True, "last": False},
                {"values": [], "chunked_value": False, "last": True},
            ],
            "Stream ended while waiting for continuation of chunked value.",
        ),
        (
            f"select id, payload from {prefix}invalid_empty_values_chunked",
            fields,
            [{"values": [], "chunked_value": True, "last": False}],
            "Received chunked_value=True with empty values.",
        ),
        (
            f"select id, payload from {prefix}invalid_row_eof",
            fields,
            [{"values": ["1", "ok", "2"], "chunked_value": False, "last": False}],
            "Stream ended with an incomplete row.",
        ),
        (
            f"select id, payload from {prefix}invalid_row_last",
            fields,
            [{"values": ["1", "ok", "2"], "chunked_value": False, "last": True}],
            "Stream ended with an incomplete row.",
        ),
        (
            f"select id, payload from {prefix}invalid_missing_row_type",
            [],
            [{"values": ["1"], "chunked_value": False, "last": True}],
            "Missing row_type in PartialResultSet metadata.",
        ),
    ]


def _execute_query(transaction: Transaction, sql: str):
    rows = transaction.execute_sql(sql, last_statement=True)
    for _ in rows:
        pass
