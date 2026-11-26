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

import asyncio
import random
import threading

from google.cloud.spanner_v1 import (
    BatchCreateSessionsRequest,
    BeginTransactionRequest,
    CreateSessionRequest,
    ExecuteSqlRequest,
)
from google.cloud.spanner_v1.database_sessions_manager import TransactionType
from google.cloud.spanner_v1.request_id_header import REQ_RAND_PROCESS_ID
from google.cloud.spanner_v1.testing.mock_spanner import SpannerServicer
from tests.mockserver_tests.mock_server_test_base import (
    AsyncMockServerTestBase,
    MockServerTestBase,
    aborted_status,
    add_error,
    add_select1_result,
    unavailable_status,
)


class _RequestIDAssertionsMixin:
    """Shared synchronous assertions for x-goog-spanner-request-id headers."""

    def _get_request_id_segments(self, database):
        interceptor = database._x_goog_request_id_interceptor
        return interceptor.stream_request_ids, interceptor.unary_request_ids

    @staticmethod
    def _count_leading_session_requests(requests) -> int:
        session_requests_before = 0
        for request in requests:
            if isinstance(request, (BatchCreateSessionsRequest, CreateSessionRequest)):
                session_requests_before += 1
            else:
                break
        return session_requests_before

    def _assert_single_execute_sql_request_ids(self, database, requests):
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest],
            TransactionType.READ_ONLY,
            allow_multiple_batch_create=True,
        )
        nth_client = database._nth_client_id
        channel_id = database._channel_id
        got_stream_segments, got_unary_segments = self._get_request_id_segments(
            database
        )
        filtered_unary_segments = [
            segment
            for segment in got_unary_segments
            if not segment[0].endswith("/CreateSession")
        ]
        want_unary_segments = [
            (
                "/google.spanner.v1.Spanner/BatchCreateSessions",
                (1, REQ_RAND_PROCESS_ID, nth_client, channel_id, 1, 1),
            )
        ]
        session_requests_before = self._count_leading_session_requests(requests)
        want_stream_segments = [
            (
                "/google.spanner.v1.Spanner/ExecuteStreamingSql",
                (
                    1,
                    REQ_RAND_PROCESS_ID,
                    nth_client,
                    channel_id,
                    1 + session_requests_before,
                    1,
                ),
            )
        ]
        self.assertEqual(want_unary_segments, filtered_unary_segments)
        self.assertEqual(want_stream_segments, got_stream_segments)

    def _assert_concurrent_execute_sql_request_ids(
        self, database, requests, concurrency
    ):
        # 1 warmup query + `concurrency` concurrent queries
        expected_queries = concurrency + 1
        expected_min = 1 + expected_queries
        expected_max = expected_min + 1
        self.assertTrue(
            expected_min <= len(requests) <= expected_max,
            f"Expected {expected_min} or {expected_max} requests, got {len(requests)}: {requests}",
        )
        client_id = database._nth_client_id
        channel_id = database._channel_id
        got_stream_segments, got_unary_segments = self._get_request_id_segments(
            database
        )
        want_unary_segment = (
            "/google.spanner.v1.Spanner/BatchCreateSessions",
            (1, REQ_RAND_PROCESS_ID, client_id, channel_id, 1, 1),
        )
        self.assertTrue(
            any(segment == want_unary_segment for segment in got_unary_segments)
        )

        session_requests_before = self._count_leading_session_requests(requests)
        want_stream_segments = [
            (
                "/google.spanner.v1.Spanner/ExecuteStreamingSql",
                (
                    1,
                    REQ_RAND_PROCESS_ID,
                    client_id,
                    channel_id,
                    session_requests_before + index,
                    1,
                ),
            )
            for index in range(1, expected_queries + 1)
        ]
        self.assertEqual(sorted(want_stream_segments), sorted(got_stream_segments))

    def _assert_partitioned_dml_request_ids(self, database, requests):
        self.assert_requests_sequence(
            requests,
            [BeginTransactionRequest, ExecuteSqlRequest],
            TransactionType.PARTITIONED,
            allow_multiple_batch_create=True,
        )
        got_stream_segments, got_unary_segments = self._get_request_id_segments(
            database
        )
        nth_client = database._nth_client_id
        channel_id = database._channel_id
        filtered_unary_segments = [
            segment
            for segment in got_unary_segments
            if not segment[0].endswith("/CreateSession")
        ]
        session_requests_before = self._count_leading_session_requests(requests)
        begin_transaction_seq = 1 + session_requests_before
        execute_sql_seq = 2 + session_requests_before
        want_unary_segments = [
            (
                "/google.spanner.v1.Spanner/BatchCreateSessions",
                (1, REQ_RAND_PROCESS_ID, nth_client, channel_id, 1, 1),
            ),
            (
                "/google.spanner.v1.Spanner/BeginTransaction",
                (
                    1,
                    REQ_RAND_PROCESS_ID,
                    nth_client,
                    channel_id,
                    begin_transaction_seq,
                    1,
                ),
            ),
        ]
        want_stream_segments = [
            (
                "/google.spanner.v1.Spanner/ExecuteStreamingSql",
                (1, REQ_RAND_PROCESS_ID, nth_client, channel_id, execute_sql_seq, 1),
            )
        ]
        self.assertTrue(
            all(segment in filtered_unary_segments for segment in want_unary_segments)
        )
        self.assertEqual(want_stream_segments, got_stream_segments)

    def _assert_unary_retry_request_ids(self, database, requests):
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest],
            TransactionType.READ_ONLY,
            allow_multiple_batch_create=True,
        )
        nth_client = database._nth_client_id
        channel_id = database._channel_id
        got_stream_segments, got_unary_segments = self._get_request_id_segments(
            database
        )
        expected_batch_create_segment = (
            "/google.spanner.v1.Spanner/BatchCreateSessions",
            (1, REQ_RAND_PROCESS_ID, nth_client, channel_id, 1, 1),
        )
        batch_create_segments = [
            segment
            for segment in got_unary_segments
            if segment[0].endswith("/BatchCreateSessions")
        ]
        self.assertEqual([expected_batch_create_segment] * 2, batch_create_segments)
        has_create_session = any(
            segment[0].endswith("/CreateSession") for segment in got_unary_segments
        )
        execute_sql_seq = 3 if has_create_session else 2
        want_stream_segments = [
            (
                "/google.spanner.v1.Spanner/ExecuteStreamingSql",
                (1, REQ_RAND_PROCESS_ID, nth_client, channel_id, execute_sql_seq, 1),
            )
        ]
        self.assertEqual(want_stream_segments, got_stream_segments)


class TestRequestIDHeader(_RequestIDAssertionsMixin, MockServerTestBase):
    def tearDown(self):
        super().tearDown()
        self.database._x_goog_request_id_interceptor.reset()

    def test_snapshot_execute_sql(self):
        add_select1_result()
        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            result_list = []
            for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))
        self._assert_single_execute_sql_request_ids(
            self.database, self.spanner_service.requests
        )

    def test_snapshot_read_concurrent(self):
        add_select1_result()
        db = self.database
        with db.snapshot() as snapshot:
            rows = snapshot.execute_sql("select 1")
            for row in rows:
                _ = row

        def select1():
            with db.snapshot() as snapshot:
                rows = snapshot.execute_sql("select 1")
                res_list = []
                for row in rows:
                    self.assertEqual(1, row[0])
                    res_list.append(row)
                self.assertEqual(1, len(res_list))

        n = 10
        threads = []
        for i in range(n):
            th = threading.Thread(target=select1, name=f"snapshot-select1-{i}")
            threads.append(th)
            th.start()
        random.shuffle(threads)
        for thread in threads:
            thread.join()
        self._assert_concurrent_execute_sql_request_ids(
            db, self.spanner_service.requests, n
        )

    def test_database_run_in_transaction_retries_on_abort(self):
        counters = dict(aborted=0)
        want_failed_attempts = 2

        def select_in_txn(txn):
            results = txn.execute_sql("select 1")
            for row in results:
                _ = row

            if counters["aborted"] < want_failed_attempts:
                counters["aborted"] += 1
                add_error(SpannerServicer.Commit.__name__, aborted_status())

        add_select1_result()
        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        self.database.run_in_transaction(select_in_txn)

    def test_database_execute_partitioned_dml_request_id(self):
        add_select1_result()
        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors
        _ = self.database.execute_partitioned_dml("select 1")
        self._assert_partitioned_dml_request_ids(
            self.database, self.spanner_service.requests
        )

    def test_unary_retryable_error(self):
        add_select1_result()
        add_error(SpannerServicer.BatchCreateSessions.__name__, unavailable_status())

        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            result_list = []
            for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))

        self._assert_unary_retry_request_ids(
            self.database, self.spanner_service.requests
        )

    def test_streaming_retryable_error(self):
        add_select1_result()
        add_error(SpannerServicer.ExecuteStreamingSql.__name__, unavailable_status())

        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors
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
            allow_multiple_batch_create=True,
        )

    def canonicalize_request_id_headers(self):
        return self._get_request_id_segments(self.database)


class TestRequestIDHeaderAsync(_RequestIDAssertionsMixin, AsyncMockServerTestBase):
    async def get_database(self):
        if self._database is None:
            self._database = await self.create_database(
                enable_interceptors_in_tests=True
            )
        return self._database

    async def test_async_snapshot_execute_sql(self):
        add_select1_result()
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql("select 1")
            result_list = []
            async for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))
        self._assert_single_execute_sql_request_ids(
            database, self.spanner_service.requests
        )

    async def test_async_snapshot_read_concurrent(self):
        add_select1_result()
        database = await self.get_database()
        async with database.snapshot() as snapshot:
            rows = await snapshot.execute_sql("select 1")
            async for _ in rows:
                pass

        async def select1():
            async with database.snapshot() as snapshot:
                rows = await snapshot.execute_sql("select 1")
                result_list = []
                async for row in rows:
                    self.assertEqual(1, row[0])
                    result_list.append(row)
                self.assertEqual(1, len(result_list))

        concurrency = 10
        await asyncio.wait_for(
            asyncio.gather(*(select1() for _ in range(concurrency))),
            timeout=5.0,
        )
        self._assert_concurrent_execute_sql_request_ids(
            database, self.spanner_service.requests, concurrency
        )

    async def test_async_database_run_in_transaction_retries_on_abort(self):
        counters = {"aborted": 0}
        want_failed_attempts = 2

        async def select_in_transaction(transaction):
            results = await transaction.execute_sql("select 1")
            async for _ in results:
                pass

            if counters["aborted"] < want_failed_attempts:
                counters["aborted"] += 1
                add_error(SpannerServicer.Commit.__name__, aborted_status())

        add_select1_result()
        database = await self.get_database()
        await database.run_in_transaction(select_in_transaction)
        got_stream_segments, got_unary_segments = self._get_request_id_segments(
            database
        )
        stream_segments = [
            segment
            for segment in got_stream_segments
            if segment[0].endswith("/ExecuteStreamingSql")
        ]
        commit_segments = [
            segment for segment in got_unary_segments if segment[0].endswith("/Commit")
        ]
        expected_attempts = want_failed_attempts + 1
        self.assertEqual(expected_attempts, len(stream_segments))
        self.assertEqual(expected_attempts, len(commit_segments))

        expected_prefix = (
            1,
            REQ_RAND_PROCESS_ID,
            database._nth_client_id,
            database._channel_id,
        )
        session_requests_before = self._count_leading_session_requests(
            self.spanner_service.requests
        )
        for attempt_index, (stream_segment, commit_segment) in enumerate(
            zip(stream_segments, commit_segments)
        ):
            execute_seq = session_requests_before + 1 + 2 * attempt_index
            self.assertEqual(
                (*expected_prefix, execute_seq, 1),
                stream_segment[1],
            )
            self.assertEqual(
                (*expected_prefix, execute_seq + 1, 1),
                commit_segment[1],
            )

    async def test_async_database_execute_partitioned_dml_request_id(self):
        add_select1_result()
        database = await self.get_database()
        _ = await database.execute_partitioned_dml("select 1")
        self._assert_partitioned_dml_request_ids(
            database, self.spanner_service.requests
        )

    async def test_async_unary_retryable_error(self):
        add_select1_result()
        add_error(SpannerServicer.BatchCreateSessions.__name__, unavailable_status())

        database = await self.get_database()
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql("select 1")
            result_list = []
            async for row in results:
                result_list.append(row)
                self.assertEqual(1, row[0])
            self.assertEqual(1, len(result_list))

        self._assert_unary_retry_request_ids(database, self.spanner_service.requests)

    async def test_async_streaming_retryable_error(self):
        add_select1_result()
        add_error(SpannerServicer.ExecuteStreamingSql.__name__, unavailable_status())

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
            [ExecuteSqlRequest, ExecuteSqlRequest],
            TransactionType.READ_ONLY,
            allow_multiple_batch_create=True,
        )
