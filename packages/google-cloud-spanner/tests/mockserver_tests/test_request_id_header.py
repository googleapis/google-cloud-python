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

import random
import threading

from google.api_core.exceptions import InvalidArgument, ResourceExhausted
from google.protobuf.duration_pb2 import Duration
from google.rpc import code_pb2, status_pb2
from google.rpc.error_details_pb2 import RetryInfo
from grpc_status._common import code_to_grpc_status_code
from grpc_status.rpc_status import _Status

from google.cloud.spanner_v1 import (
    BatchCreateSessionsRequest,
    BeginTransactionRequest,
    CreateSessionRequest,
    ExecuteSqlRequest,
    KeySet,
)
from google.cloud.spanner_v1.types.result_set import (
    PartialResultSet,
    ResultSet,
    ResultSetStats,
)
from google.cloud.spanner_v1.database_sessions_manager import TransactionType
from google.cloud.spanner_v1.request_id_header import REQ_RAND_PROCESS_ID
from google.cloud.spanner_v1.testing.mock_spanner import SpannerServicer
from tests.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    aborted_status,
    add_error,
    add_select1_result,
    invalid_argument_status,
    unavailable_status,
)


class TestRequestIDHeader(MockServerTestBase):
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
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest],
            TransactionType.READ_ONLY,
            allow_multiple_batch_create=True,
        )
        NTH_CLIENT = self.database._nth_client_id
        CHANNEL_ID = self.database._channel_id
        got_stream_segments, got_unary_segments = self.canonicalize_request_id_headers()
        # Filter out CreateSessionRequest unary segments for comparison
        filtered_unary_segments = [
            seg for seg in got_unary_segments if not seg[0].endswith("/CreateSession")
        ]
        want_unary_segments = [
            (
                "/google.spanner.v1.Spanner/BatchCreateSessions",
                (1, REQ_RAND_PROCESS_ID, NTH_CLIENT, CHANNEL_ID, 1, 1),
            )
        ]
        # Dynamically determine the expected sequence number for ExecuteStreamingSql
        session_requests_before = 0
        for req in requests:
            if isinstance(req, (BatchCreateSessionsRequest, CreateSessionRequest)):
                session_requests_before += 1
            elif isinstance(req, ExecuteSqlRequest):
                break
        want_stream_segments = [
            (
                "/google.spanner.v1.Spanner/ExecuteStreamingSql",
                (
                    1,
                    REQ_RAND_PROCESS_ID,
                    NTH_CLIENT,
                    CHANNEL_ID,
                    1 + session_requests_before,
                    1,
                ),
            )
        ]
        assert filtered_unary_segments == want_unary_segments
        assert got_stream_segments == want_stream_segments

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
        requests = self.spanner_service.requests
        # Allow for an extra request due to multiplexed session creation
        expected_min = 2 + n
        expected_max = expected_min + 1
        assert expected_min <= len(requests) <= expected_max, (
            f"Expected {expected_min} or {expected_max} requests, got {len(requests)}: {requests}"
        )
        client_id = db._nth_client_id
        channel_id = db._channel_id
        got_stream_segments, got_unary_segments = self.canonicalize_request_id_headers()
        want_unary_segments = [
            (
                "/google.spanner.v1.Spanner/BatchCreateSessions",
                (1, REQ_RAND_PROCESS_ID, client_id, channel_id, 1, 1),
            ),
        ]
        assert any(seg == want_unary_segments[0] for seg in got_unary_segments)

        # Dynamically determine the expected sequence numbers for ExecuteStreamingSql
        session_requests_before = 0
        for req in requests:
            if isinstance(req, (BatchCreateSessionsRequest, CreateSessionRequest)):
                session_requests_before += 1
            elif isinstance(req, ExecuteSqlRequest):
                break
        want_stream_segments = [
            (
                "/google.spanner.v1.Spanner/ExecuteStreamingSql",
                (
                    1,
                    REQ_RAND_PROCESS_ID,
                    client_id,
                    channel_id,
                    session_requests_before + i,
                    1,
                ),
            )
            for i in range(1, n + 2)
        ]
        assert sorted(got_stream_segments) == sorted(want_stream_segments)

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
        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [BeginTransactionRequest, ExecuteSqlRequest],
            TransactionType.PARTITIONED,
            allow_multiple_batch_create=True,
        )
        got_stream_segments, got_unary_segments = self.canonicalize_request_id_headers()
        NTH_CLIENT = self.database._nth_client_id
        CHANNEL_ID = self.database._channel_id
        # Allow for extra unary segments due to session creation
        filtered_unary_segments = [
            seg for seg in got_unary_segments if not seg[0].endswith("/CreateSession")
        ]
        # Find the actual sequence number for BeginTransaction
        begin_txn_seq = None
        for seg in filtered_unary_segments:
            if seg[0].endswith("/BeginTransaction"):
                begin_txn_seq = seg[1][4]
                break
        want_unary_segments = [
            (
                "/google.spanner.v1.Spanner/BatchCreateSessions",
                (1, REQ_RAND_PROCESS_ID, NTH_CLIENT, CHANNEL_ID, 1, 1),
            ),
            (
                "/google.spanner.v1.Spanner/BeginTransaction",
                (1, REQ_RAND_PROCESS_ID, NTH_CLIENT, CHANNEL_ID, begin_txn_seq, 1),
            ),
        ]
        # Dynamically determine the expected sequence number for ExecuteStreamingSql
        session_requests_before = 0
        for req in requests:
            if isinstance(req, (BatchCreateSessionsRequest, CreateSessionRequest)):
                session_requests_before += 1
            elif isinstance(req, ExecuteSqlRequest):
                break
        # Find the actual sequence number for ExecuteStreamingSql
        exec_sql_seq = got_stream_segments[0][1][4] if got_stream_segments else None
        want_stream_segments = [
            (
                "/google.spanner.v1.Spanner/ExecuteStreamingSql",
                (1, REQ_RAND_PROCESS_ID, NTH_CLIENT, CHANNEL_ID, exec_sql_seq, 1),
            )
        ]
        assert all(seg in filtered_unary_segments for seg in want_unary_segments)
        assert got_stream_segments == want_stream_segments

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

        requests = self.spanner_service.requests
        self.assert_requests_sequence(
            requests,
            [ExecuteSqlRequest],
            TransactionType.READ_ONLY,
            allow_multiple_batch_create=True,
        )

        NTH_CLIENT = self.database._nth_client_id
        CHANNEL_ID = self.database._channel_id
        # Now ensure monotonicity of the received request-id segments.
        got_stream_segments, got_unary_segments = self.canonicalize_request_id_headers()

        # Dynamically determine the expected sequence number for ExecuteStreamingSql
        exec_sql_seq = got_stream_segments[0][1][4] if got_stream_segments else None
        want_stream_segments = [
            (
                "/google.spanner.v1.Spanner/ExecuteStreamingSql",
                (1, REQ_RAND_PROCESS_ID, NTH_CLIENT, CHANNEL_ID, exec_sql_seq, 1),
            )
        ]
        assert got_stream_segments == want_stream_segments

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
        got_stream_segments, _ = self.canonicalize_request_id_headers()
        stream_sql_segments = [
            seg for seg in got_stream_segments if seg[0].endswith("/ExecuteStreamingSql")
        ]
        self.assertEqual(len(stream_sql_segments), 2)
        self.assertEqual(stream_sql_segments[0][1][5], 1)
        self.assertEqual(stream_sql_segments[1][1][5], 2)
        self.assertEqual(stream_sql_segments[0][1][:5], stream_sql_segments[1][1][:5])

    def test_trace_span_attribute_matching_request_id(self):
        add_select1_result()
        from tests._helpers import get_test_ot_exporter, use_test_ot_exporter

        use_test_ot_exporter()
        exporter = get_test_ot_exporter()
        exporter.clear()

        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        with self.database.snapshot() as snapshot:
            list(snapshot.execute_sql("select 1"))

        spans = exporter.get_finished_spans()
        execute_span = next(
            s for s in spans if s.name.endswith(".execute_sql")
        )
        self.assertIn("x_goog_spanner_request_id", execute_span.attributes)
        got_stream_segments, _ = self.canonicalize_request_id_headers()
        stream_sql_segments = [
            seg for seg in got_stream_segments if seg[0].endswith("/ExecuteStreamingSql")
        ]
        self.assertTrue(len(stream_sql_segments) > 0)
        wire_tuple = stream_sql_segments[0][1]
        wire_req_id = ".".join(str(x) for x in wire_tuple)
        self.assertEqual(execute_span.attributes["x_goog_spanner_request_id"], wire_req_id)

    def test_fatal_error_terminates_and_logs_request_id(self):
        add_error(SpannerServicer.ExecuteStreamingSql.__name__, invalid_argument_status())

        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        with self.assertRaises(InvalidArgument) as ctx:
            with self.database.snapshot() as snapshot:
                list(snapshot.execute_sql("select 1"))

        exc = ctx.exception
        self.assertTrue(hasattr(exc, "request_id"), "Exception missing .request_id")
        self.assertIn("request_id =", str(exc), "Exception message does not contain 'request_id ='")

        got_stream_segments, _ = self.canonicalize_request_id_headers()
        stream_sql_segments = [
            seg for seg in got_stream_segments if seg[0].endswith("/ExecuteStreamingSql")
        ]
        self.assertEqual(len(stream_sql_segments), 1)
        self.assertEqual(stream_sql_segments[0][1][5], 1)
        wire_req_id = ".".join(str(x) for x in stream_sql_segments[0][1])
        self.assertEqual(exc.request_id, wire_req_id)

    def test_streaming_retryable_resource_exhausted(self):
        add_select1_result()
        error = status_pb2.Status(code=code_pb2.RESOURCE_EXHAUSTED, message="Quota exceeded")
        retry_info = RetryInfo(retry_delay=Duration(seconds=0, nanos=1))
        status = _Status(
            code=code_to_grpc_status_code(error.code),
            details=error.message,
            trailing_metadata=(
                ("grpc-status-details-bin", error.SerializeToString()),
                ("google.rpc.retryinfo-bin", retry_info.SerializeToString()),
            ),
        )
        add_error(SpannerServicer.ExecuteStreamingSql.__name__, status)

        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            result_list = list(results)
            self.assertEqual(1, len(result_list))

        got_stream_segments, _ = self.canonicalize_request_id_headers()
        stream_sql_segments = [
            seg for seg in got_stream_segments if seg[0].endswith("/ExecuteStreamingSql")
        ]
        self.assertEqual(len(stream_sql_segments), 2)
        self.assertEqual(stream_sql_segments[0][1][5], 1)
        self.assertEqual(stream_sql_segments[1][1][5], 2)
        self.assertEqual(stream_sql_segments[0][1][:5], stream_sql_segments[1][1][:5])

    def test_streaming_resource_exhausted_fails_immediately_when_retry_is_none(self):
        error = status_pb2.Status(code=code_pb2.RESOURCE_EXHAUSTED, message="Quota exceeded")
        status = _Status(
            code=code_to_grpc_status_code(error.code),
            details=error.message,
            trailing_metadata=(("grpc-status-details-bin", error.SerializeToString()),),
        )
        add_error(SpannerServicer.ExecuteStreamingSql.__name__, status)

        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        with self.assertRaises(ResourceExhausted) as ctx:
            with self.database.snapshot() as snapshot:
                list(snapshot.execute_sql("select 1", retry=None))

        self.assertTrue(hasattr(ctx.exception, "request_id"))
        got_stream_segments, _ = self.canonicalize_request_id_headers()
        stream_sql_segments = [
            seg for seg in got_stream_segments if seg[0].endswith("/ExecuteStreamingSql")
        ]
        self.assertEqual(len(stream_sql_segments), 1)
        self.assertEqual(stream_sql_segments[0][1][5], 1)

    def test_exhaustive_fatal_error_matrix(self):
        fatal_codes = [
            (code_pb2.PERMISSION_DENIED, "Permission denied"),
            (code_pb2.NOT_FOUND, "Resource not found"),
            (code_pb2.ALREADY_EXISTS, "Resource already exists"),
            (code_pb2.FAILED_PRECONDITION, "Precondition failed"),
            (code_pb2.OUT_OF_RANGE, "Index out of range"),
            (code_pb2.UNIMPLEMENTED, "Method not implemented"),
            (code_pb2.UNAUTHENTICATED, "Unauthenticated call"),
            (code_pb2.DATA_LOSS, "Data corruption"),
        ]

        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        for code_val, msg in fatal_codes:
            self.database._x_goog_request_id_interceptor.reset()
            error = status_pb2.Status(code=code_val, message=msg)
            status = _Status(
                code=code_to_grpc_status_code(error.code),
                details=error.message,
                trailing_metadata=(("grpc-status-details-bin", error.SerializeToString()),),
            )
            add_error(SpannerServicer.ExecuteStreamingSql.__name__, status)

            with self.assertRaises(Exception) as ctx:
                with self.database.snapshot() as snapshot:
                    list(snapshot.execute_sql("select 1"))

            exc = ctx.exception
            self.assertTrue(hasattr(exc, "request_id"), f"Code {code_val}: missing request_id")
            self.assertIn("request_id =", str(exc), f"Code {code_val}: missing 'request_id =' in error string")

            got_stream_segments, _ = self.canonicalize_request_id_headers()
            stream_sql_segments = [
                seg for seg in got_stream_segments if seg[0].endswith("/ExecuteStreamingSql")
            ]
            self.assertEqual(len(stream_sql_segments), 1, f"Code {code_val}: should not retry")
            self.assertEqual(stream_sql_segments[0][1][5], 1, f"Code {code_val}: attempt should be 1")

    def test_snapshot_streaming_read_request_id(self):
        add_select1_result()
        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        with self.database.snapshot() as snapshot:
            results = snapshot.read(
                table="test_table",
                columns=["col1"],
                keyset=KeySet(all_=True),
            )
            list(results)

        got_stream_segments, _ = self.canonicalize_request_id_headers()
        read_segments = [
            seg for seg in got_stream_segments if seg[0].endswith("/StreamingRead")
        ]
        self.assertTrue(len(read_segments) >= 1)
        self.assertEqual(read_segments[0][1][5], 1)

    def test_transaction_rollback_request_id(self):
        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        session = self.database.session()
        session.create()
        txn = session.transaction()
        txn.begin()
        txn.rollback()

        got_stream_segments, got_unary_segments = self.canonicalize_request_id_headers()
        rollback_segs = [
            seg for seg in got_unary_segments if seg[0].endswith("/Rollback")
        ]
        self.assertTrue(len(rollback_segs) >= 1)
        self.assertEqual(rollback_segs[0][1][5], 1)

    def test_batch_commit_mutations_request_id(self):
        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        with self.database.batch() as batch:
            batch.insert("test_table", ["col1"], [["val1"]])

        got_stream_segments, got_unary_segments = self.canonicalize_request_id_headers()
        commit_segs = [
            seg for seg in got_unary_segments if seg[0].endswith("/Commit")
        ]
        self.assertTrue(len(commit_segs) >= 1)
        self.assertEqual(commit_segs[0][1][5], 1)

    def test_batch_and_partitioned_operations_request_id(self):
        sql = "UPDATE test_table SET col1 = 'val' WHERE true"
        prs = PartialResultSet(stats=ResultSetStats(row_count_lower_bound=5))
        self.spanner_service.mock_spanner.add_execute_streaming_sql_results(sql, [prs])
        self.spanner_service.mock_spanner.add_result(
            sql, ResultSet(stats=ResultSetStats(row_count_exact=1))
        )
        if not getattr(self.database, "_interceptors", None):
            self.database._interceptors = MockServerTestBase._interceptors

        # 1. ExecuteBatchDml in transaction
        def txn_cb(txn):
            txn.batch_update([sql])
        self.database.run_in_transaction(txn_cb)

        # 2. PartitionRead and PartitionQuery in multi-use snapshot
        with self.database.snapshot(multi_use=True) as snapshot:
            snapshot.begin()
            list(snapshot.partition_read(table="test_table", columns=["col1"], keyset=KeySet(all_=True)))
            list(snapshot.partition_query("select 1"))

        got_stream_segments, got_unary_segments = self.canonicalize_request_id_headers()
        batch_dml_segs = [
            seg for seg in got_unary_segments if seg[0].endswith("/ExecuteBatchDml")
        ]
        self.assertTrue(len(batch_dml_segs) >= 1)
        self.assertEqual(batch_dml_segs[0][1][5], 1)

        part_read_segs = [
            seg for seg in got_unary_segments if seg[0].endswith("/PartitionRead")
        ]
        self.assertTrue(len(part_read_segs) >= 1)
        self.assertEqual(part_read_segs[0][1][5], 1)

        part_query_segs = [
            seg for seg in got_unary_segments if seg[0].endswith("/PartitionQuery")
        ]
        self.assertTrue(len(part_query_segs) >= 1)
        self.assertEqual(part_query_segs[0][1][5], 1)

    def canonicalize_request_id_headers(self):
        src = self.database._x_goog_request_id_interceptor
        return src._stream_req_segments, src._unary_req_segments


