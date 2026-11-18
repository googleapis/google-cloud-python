# Copyright 2026 Google LLC All rights reserved.
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

"""End-to-end mockserver tests for DB-API transaction retry error handling."""

from unittest import mock

from google.api_core.exceptions import Aborted
from google.rpc import code_pb2, status_pb2
from grpc_status._common import code_to_grpc_status_code
from grpc_status.rpc_status import _Status

from google.cloud.spanner_dbapi import Connection
from google.cloud.spanner_dbapi.checksum import RETRY_ABORTED_ERROR
from google.cloud.spanner_dbapi.exceptions import ProgrammingError, RetryAborted
from google.cloud.spanner_v1.testing.mock_spanner import SpannerServicer
from tests.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    aborted_status,
    add_error,
    add_update_count,
)

_BATCH_INSERT_SQL = "insert into singers (id, name) values (1, 'Some Singer')"
_UPDATE_SQL = "update singers set name = 'Updated' where id = 1"


def _rpc_status(code: code_pb2.Code, message: str) -> _Status:
    error = status_pb2.Status(code=code, message=message)
    return _Status(
        code=code_to_grpc_status_code(error.code),
        details=error.message,
        trailing_metadata=(("grpc-status-details-bin", error.SerializeToString()),),
    )


class TestDbapiRetryHelper(MockServerTestBase):
    def setUp(self):
        super().setUp()
        add_update_count(_BATCH_INSERT_SQL, 1)
        add_update_count(_UPDATE_SQL, 1)

    def tearDown(self):
        self.spanner_service.mock_spanner._errors_list = {}
        super().tearDown()

    def test_previously_succeeding_statement_fails_on_retry_raises_retry_aborted(self):
        """Verifies that if a statement succeeds on the initial attempt, commit
        is aborted, and replaying that statement during retry fails with a
        non-Aborted error, commit raises RetryAborted.
        """
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        try:
            with connection.cursor() as cursor:
                cursor.executemany(_BATCH_INSERT_SQL, [()])
                cursor.execute(_UPDATE_SQL)
                self.assertEqual(cursor.rowcount, 1)

            add_error(SpannerServicer.Commit.__name__, aborted_status())
            add_error(
                SpannerServicer.ExecuteStreamingSql.__name__,
                _rpc_status(code_pb2.INTERNAL, "unexpected replay failure"),
            )

            with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
                connection.commit()
        finally:
            connection.close()

    def test_matching_grpc_error_with_different_request_ids_commits_on_retry(self):
        """Verifies retry when the application catches a failed statement and
        continues the transaction. When commit later aborts and the transaction
        is replayed, the client attaches a new request_id to each RPC, so retry
        must compare the underlying gRPC status code and message while ignoring
        request_id.
        """
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        try:
            with connection.cursor() as cursor:
                cursor.executemany(_BATCH_INSERT_SQL, [()])

                add_error(
                    SpannerServicer.ExecuteStreamingSql.__name__,
                    _rpc_status(code_pb2.INVALID_ARGUMENT, "Division by zero"),
                )
                with self.assertRaises(ProgrammingError) as first_failure:
                    cursor.execute(_UPDATE_SQL)
                first_request_id = getattr(
                    first_failure.exception.__cause__, "request_id", None
                )
                self.assertIsNotNone(first_request_id)

            add_error(SpannerServicer.Commit.__name__, aborted_status())
            add_error(
                SpannerServicer.ExecuteStreamingSql.__name__,
                _rpc_status(code_pb2.INVALID_ARGUMENT, "Division by zero"),
            )
            connection.commit()

            execute_sql_requests = [
                request
                for request in self.spanner_service.requests
                if type(request).__name__ == "ExecuteSqlRequest"
            ]
            commit_requests = [
                request
                for request in self.spanner_service.requests
                if type(request).__name__ == "CommitRequest"
            ]
            self.assertEqual(len(execute_sql_requests), 2)
            self.assertEqual(len(commit_requests), 2)
        finally:
            connection.close()

    def test_different_grpc_message_on_retry_raises_retry_aborted(self):
        """Verifies retry when the application catches a failed statement, commit
        later aborts, and replaying that statement fails with the same gRPC
        status code but a different error message. Because the error message
        changed, commit must raise RetryAborted.
        """
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        try:
            with connection.cursor() as cursor:
                cursor.executemany(_BATCH_INSERT_SQL, [()])

                add_error(
                    SpannerServicer.ExecuteStreamingSql.__name__,
                    _rpc_status(code_pb2.INVALID_ARGUMENT, "Division by zero"),
                )
                with self.assertRaises(ProgrammingError):
                    cursor.execute(_UPDATE_SQL)

            add_error(SpannerServicer.Commit.__name__, aborted_status())
            add_error(
                SpannerServicer.ExecuteStreamingSql.__name__,
                _rpc_status(code_pb2.INVALID_ARGUMENT, "Out of range"),
            )
            with self.assertRaisesRegex(RetryAborted, RETRY_ABORTED_ERROR):
                connection.commit()
        finally:
            connection.close()

    def test_max_internal_retries_exceeded_raises_aborted(self):
        """Verifies that when Aborted errors occur repeatedly within a single
        transaction and exceed MAX_INTERNAL_RETRIES, the client stops retrying
        and raises Aborted to the caller.
        """
        connection = Connection(self.instance, self.database)
        connection.autocommit = False
        try:
            with connection.cursor() as cursor:
                cursor.executemany(_BATCH_INSERT_SQL, [()])
                cursor.execute(_UPDATE_SQL)

            add_error(SpannerServicer.Commit.__name__, aborted_status())
            add_error(SpannerServicer.ExecuteStreamingSql.__name__, aborted_status())
            add_error(SpannerServicer.ExecuteStreamingSql.__name__, aborted_status())

            with mock.patch(
                "google.cloud.spanner_dbapi.transaction_helper.MAX_INTERNAL_RETRIES", 2
            ):
                with self.assertRaises(Aborted):
                    connection.commit()
        finally:
            connection.close()
