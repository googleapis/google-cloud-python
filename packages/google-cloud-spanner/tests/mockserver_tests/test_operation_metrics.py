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

import os
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta
from unittest import mock

from google.api_core import exceptions
from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

import google.cloud.spanner_v1._async.client as async_client_mod
import google.cloud.spanner_v1.client as client_mod
from google.cloud.spanner_v1 import (
    Client,
    FixedSizePool,
    KeySet,
    TypeCode,
)
from google.cloud.spanner_v1._async.pool import FixedSizePool as AsyncFixedSizePool
from google.cloud.spanner_v1.metrics.metrics_interceptor import (
    AsyncMetricsInterceptor,
    MetricsInterceptor,
)
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)
from google.cloud.spanner_v1.testing.mock_spanner import (
    PartialResultSetConfig,
    SpannerServicer,
)
from tests.mockserver_tests.mock_server_test_base import (
    AsyncMockServerTestBase,
    MockServerTestBase,
    _make_partial_result_sets,
    add_error,
    add_execute_streaming_sql_error,
    add_execute_streaming_sql_results,
    add_multi_column_result,
    add_select1_result,
    add_single_result,
    deadline_exceeded_status,
    unavailable_status,
)


class _OperationMetricsAssertionsMixin:
    @staticmethod
    def extract_metrics(reader, method: str | None = None) -> dict:
        """Extract metric data points from an InMemoryMetricReader, optionally filtered by RPC method."""
        metric_data = reader.get_metrics_data()
        if not metric_data:
            return {}
        all_metrics = (
            metric
            for resource_metric in metric_data.resource_metrics
            for scope_metric in resource_metric.scope_metrics
            for metric in scope_metric.metrics
        )
        metrics = {}
        for metric in all_metrics:
            points = [
                point
                for point in metric.data.data_points
                if not method or point.attributes.get("method") == method
            ]
            if points:
                metrics[metric.name] = points
        return metrics

    @staticmethod
    @contextmanager
    def patched_metrics_environment(meter_provider):
        """Patch OpenTelemetry MeterProvider and emulator host detection for sync and async clients."""
        with (
            mock.patch.dict(
                os.environ,
                {"SPANNER_DISABLE_BUILTIN_METRICS": "false"},
            ),
            mock.patch(
                "google.cloud.spanner_v1.metrics.metrics_tracer_factory.get_meter_provider",
                return_value=meter_provider,
            ),
            mock.patch(
                "google.cloud.spanner_v1.client.MeterProvider",
                return_value=meter_provider,
            ),
            mock.patch(
                "google.cloud.spanner_v1._async.client.MeterProvider",
                return_value=meter_provider,
            ),
            mock.patch(
                "google.cloud.spanner_v1.client._get_spanner_emulator_host",
                return_value=None,
            ),
            mock.patch(
                "google.cloud.spanner_v1._async.client._get_spanner_emulator_host",
                return_value=None,
            ),
        ):
            yield

    @contextmanager
    def _delayed_streaming_metrics(self, chunk_delay_milliseconds: int):
        """Yield an InMemoryMetricReader with deterministic per-chunk clock advances."""
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False
        async_client_mod._metrics_monitor_initialized = False

        mock_spanner = self.spanner_service.mock_spanner
        original_get_results = mock_spanner.get_execute_streaming_sql_results
        current_time = datetime(2026, 1, 1, 0, 0, 0)
        time_lock = threading.Lock()

        class _FakeDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                with time_lock:
                    return current_time

        def delayed_get_results(query_sql, started_transaction):
            nonlocal current_time
            for message in original_get_results(query_sql, started_transaction):
                with time_lock:
                    current_time += timedelta(milliseconds=chunk_delay_milliseconds)
                yield message

        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])
        with (
            self.patched_metrics_environment(meter_provider),
            mock.patch(
                "google.cloud.spanner_v1.metrics.metrics_tracer.datetime",
                _FakeDatetime,
            ),
            mock.patch.object(
                mock_spanner,
                "get_execute_streaming_sql_results",
                side_effect=delayed_get_results,
            ),
        ):
            yield reader

    def _assert_metrics_not_recorded(self, reader, method, check_count=True):
        metrics = self.extract_metrics(reader, method=method)
        self.assertNotIn("operation_latencies", metrics)
        if check_count:
            self.assertNotIn("operation_count", metrics)

    def _assert_operation_metrics_recorded(
        self,
        reader,
        method,
        expected_count=1,
        min_latency=None,
        check_operation_count=True,
        expected_attempt_count=None,
    ):
        metrics = self.extract_metrics(reader, method=method)
        self.assertIn(
            "operation_latencies",
            metrics,
            f"Metrics: {list(metrics.keys())}",
        )
        latency_points = metrics["operation_latencies"]
        self.assertEqual(len(latency_points), 1)
        latency_point = latency_points[0]
        self.assertEqual(latency_point.count, expected_count)
        if min_latency is not None:
            self.assertGreaterEqual(latency_point.sum, min_latency)

        if check_operation_count:
            self.assertIn("operation_count", metrics)
            operation_count_points = metrics["operation_count"]
            self.assertEqual(len(operation_count_points), 1)
            self.assertEqual(operation_count_points[0].value, expected_count)

        if expected_attempt_count is not None:
            self.assertIn("attempt_count", metrics)
            self.assertEqual(metrics["attempt_count"][0].value, expected_attempt_count)

        return latency_point.sum

    def _assert_latency_unchanged(self, reader, method, expected_sum, expected_count=1):
        metrics_after = self.extract_metrics(reader, method=method)
        point_after = metrics_after["operation_latencies"][0]
        self.assertEqual(point_after.count, expected_count)
        self.assertEqual(point_after.sum, expected_sum)


class TestOperationMetricsIntegration(
    MockServerTestBase, _OperationMetricsAssertionsMixin
):
    def setUp(self):
        super().setUp()
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False

    def tearDown(self):
        super().tearDown()
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False

    def _setup_database(self):
        from google.cloud.spanner_v1.testing.database_test import TestDatabase

        client = Client(
            project="p",
            credentials=AnonymousCredentials(),
            client_options=ClientOptions(
                api_endpoint="localhost:" + str(MockServerTestBase.port),
            ),
        )
        instance = client.instance("test-instance")
        database = TestDatabase(
            "test-database",
            instance,
            pool=FixedSizePool(size=10),
        )
        database._interceptors.append(MetricsInterceptor())

        def _cleanup_database():
            try:
                database.close()
            finally:
                spanner_api = getattr(database, "_spanner_api", None)
                transport = getattr(spanner_api, "transport", None)
                if transport is not None:
                    transport.close()

        self.addCleanup(_cleanup_database)
        database._pool.bind(database)
        # Pre-initialize pool sessions so they don't produce metric noise during queries
        session = database._pool.get()
        database._pool.put(session)
        return database

    def _run_delayed_query_and_get_latency(
        self,
        sql: str,
        chunk_delay_milliseconds: int,
        min_latency: int | None = None,
    ):
        with self._delayed_streaming_metrics(chunk_delay_milliseconds) as reader:
            database = self._setup_database()
            with database.snapshot() as snapshot:
                results = snapshot.execute_sql(sql)
                rows = iter(results)
                first_row = next(rows)
                self.assertEqual(first_row, [1])

                recorded_sum = self._assert_operation_metrics_recorded(
                    reader,
                    method="Spanner.ExecuteStreamingSql",
                    min_latency=min_latency,
                    check_operation_count=False,
                )

                remaining_rows = list(rows)
                self.assertEqual(remaining_rows, [[2], [3]])
                self._assert_latency_unchanged(
                    reader,
                    method="Spanner.ExecuteStreamingSql",
                    expected_sum=recorded_sum,
                )
                return recorded_sum

    def test_operation_latency_not_recorded_before_stream_consumed(self):
        fields = [("col1", TypeCode.INT64)]
        partials = _make_partial_result_sets(
            fields,
            [
                {"values": ["1"], "last": True},
            ],
        )
        add_execute_streaming_sql_results("select 1", partials)
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = self._setup_database()
            with database.snapshot() as snapshot:
                results = snapshot.execute_sql("select 1")

                # Verify that operational metrics for ExecuteStreamingSql have NOT been recorded yet
                self._assert_metrics_not_recorded(
                    reader, method="Spanner.ExecuteStreamingSql"
                )

                # Consume the results while keeping `results` alive in local scope
                rows = list(results)
                self.assertEqual(len(rows), 1)

                # Verify that operational metrics are recorded immediately upon stream completion
                # even while `results` is still alive in scope (regression test for last=True).
                self._assert_operation_metrics_recorded(
                    reader, method="Spanner.ExecuteStreamingSql"
                )

    def test_operation_latency_measures_full_stream_duration(self):
        fields = [("col1", TypeCode.INT64)]
        results_cfg = [
            {"values": ["1"], "last": False},
            {"values": ["2"], "last": False},
            {"values": ["3"], "last": False},
        ]
        partials = _make_partial_result_sets(fields, results_cfg)
        add_execute_streaming_sql_results("select 1", partials)
        self._run_delayed_query_and_get_latency(
            "select 1", chunk_delay_milliseconds=30, min_latency=90
        )

    def test_operation_latency_last_true_and_last_false_consistency(self):
        """Verifies last=True and last=False both record operation_latencies
        before yielding buffered rows and include the full stream duration."""
        fields = [("col1", TypeCode.INT64)]
        partials_no_last = _make_partial_result_sets(
            fields,
            [
                {"values": ["1"], "last": False},
                {"values": ["2"], "last": False},
                {"values": ["3"], "last": False},
            ],
        )
        partials_with_last = _make_partial_result_sets(
            fields,
            [
                {"values": ["1"], "last": False},
                {"values": ["2"], "last": False},
                {"values": ["3"], "last": True},
            ],
        )
        add_execute_streaming_sql_results("select no_last", partials_no_last)
        add_execute_streaming_sql_results("select with_last", partials_with_last)

        latency_no_last = self._run_delayed_query_and_get_latency(
            "select no_last", chunk_delay_milliseconds=25
        )
        latency_with_last = self._run_delayed_query_and_get_latency(
            "select with_last", chunk_delay_milliseconds=25
        )

        self.assertGreaterEqual(latency_no_last, 75)
        self.assertGreaterEqual(latency_with_last, 75)

    def test_operation_latency_with_retries(self):
        add_select1_result()
        add_error(SpannerServicer.ExecuteStreamingSql.__name__, unavailable_status())
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = self._setup_database()
            with database.snapshot() as snapshot:
                results = snapshot.execute_sql("select 1")
                rows = list(results)
                self.assertEqual(len(rows), 1)

            # Should record 1 logical operation but 2 attempts
            self._assert_operation_metrics_recorded(
                reader,
                method="Spanner.ExecuteStreamingSql",
                expected_attempt_count=2,
            )

    def test_session_ping_emits_operation_metrics(self):
        add_select1_result()
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = self._setup_database()
            session = database._pool.get()
            try:
                session.ping()
            finally:
                database._pool.put(session)

            self._assert_operation_metrics_recorded(reader, method="Spanner.ExecuteSql")

    def test_operation_latency_streaming_read(self):
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = self._setup_database()
            with database.snapshot() as snapshot:
                results = snapshot.read(
                    table="citizens",
                    columns=["email", "first_name"],
                    keyset=KeySet(all_=True),
                )
                # Before consumption
                self._assert_metrics_not_recorded(
                    reader,
                    method="Spanner.StreamingRead",
                    check_count=False,
                )

                # Consume
                list(results)

            self._assert_operation_metrics_recorded(
                reader,
                method="Spanner.StreamingRead",
                check_operation_count=False,
            )


class TestOperationMetricsAsyncIntegration(
    AsyncMockServerTestBase, _OperationMetricsAssertionsMixin
):
    def setUp(self):
        super().setUp()
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False
        async_client_mod._metrics_monitor_initialized = False

    def tearDown(self):
        super().tearDown()
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False
        async_client_mod._metrics_monitor_initialized = False

    async def _setup_database(self):
        client = self.create_client(disable_builtin_metrics=False)
        database = await self.create_database(
            client=client,
            pool=AsyncFixedSizePool(size=10),
            enable_interceptors_in_tests=True,
            interceptors=[AsyncMetricsInterceptor()],
        )
        session = await database._pool.get()
        await database._pool.put(session)
        return database

    async def test_async_operation_latency_not_recorded_before_stream_consumed(self):
        fields = [("col1", TypeCode.INT64)]
        partials = _make_partial_result_sets(
            fields,
            [
                {"values": ["1"], "last": True},
            ],
        )
        add_execute_streaming_sql_results("select 1", partials)
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = await self._setup_database()
            async with database.snapshot() as snapshot:
                results = await snapshot.execute_sql("select 1")

                self._assert_metrics_not_recorded(
                    reader, method="Spanner.ExecuteStreamingSql"
                )

                rows = [row async for row in results]
                self.assertEqual(len(rows), 1)

                self._assert_operation_metrics_recorded(
                    reader, method="Spanner.ExecuteStreamingSql"
                )

    async def _run_delayed_query_and_get_latency(
        self,
        sql: str,
        chunk_delay_milliseconds: int,
        min_latency: int | None = None,
    ):
        with self._delayed_streaming_metrics(chunk_delay_milliseconds) as reader:
            database = await self._setup_database()
            return await self._consume_and_assert_streaming_latency(
                database,
                reader,
                sql,
                min_latency=min_latency,
            )

    async def _consume_and_assert_streaming_latency(
        self,
        database,
        reader,
        sql: str,
        min_latency: int | None = None,
    ):
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(sql)
            rows = aiter(results)
            first_row = await anext(rows)
            self.assertEqual(first_row, [1])

            recorded_sum = self._assert_operation_metrics_recorded(
                reader,
                method="Spanner.ExecuteStreamingSql",
                min_latency=min_latency,
                check_operation_count=False,
            )

            remaining_rows = [row async for row in rows]
            self.assertEqual(remaining_rows, [[2], [3]])
            self._assert_latency_unchanged(
                reader,
                method="Spanner.ExecuteStreamingSql",
                expected_sum=recorded_sum,
            )
            return recorded_sum

    async def test_async_operation_latency_measures_full_stream_duration(self):
        fields = [("col1", TypeCode.INT64)]
        partials = _make_partial_result_sets(
            fields,
            [
                {"values": ["1"], "last": False},
                {"values": ["2"], "last": False},
                {"values": ["3"], "last": False},
            ],
        )
        add_execute_streaming_sql_results("select 1", partials)
        await self._run_delayed_query_and_get_latency(
            "select 1", chunk_delay_milliseconds=30, min_latency=90
        )

    async def test_async_operation_latency_last_true_and_last_false_consistency(self):
        fields = [("col1", TypeCode.INT64)]
        partials_no_last = _make_partial_result_sets(
            fields,
            [
                {"values": ["1"], "last": False},
                {"values": ["2"], "last": False},
                {"values": ["3"], "last": False},
            ],
        )
        partials_with_last = _make_partial_result_sets(
            fields,
            [
                {"values": ["1"], "last": False},
                {"values": ["2"], "last": False},
                {"values": ["3"], "last": True},
            ],
        )
        add_execute_streaming_sql_results("select no_last", partials_no_last)
        add_execute_streaming_sql_results("select with_last", partials_with_last)

        latency_no_last = await self._run_delayed_query_and_get_latency(
            "select no_last", chunk_delay_milliseconds=25
        )
        latency_with_last = await self._run_delayed_query_and_get_latency(
            "select with_last", chunk_delay_milliseconds=25
        )

        self.assertGreaterEqual(latency_no_last, 75)
        self.assertGreaterEqual(latency_with_last, 75)

    async def test_async_operation_latency_with_retries(self):
        add_select1_result()
        add_error(SpannerServicer.ExecuteStreamingSql.__name__, unavailable_status())
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = await self._setup_database()
            async with database.snapshot() as snapshot:
                results = await snapshot.execute_sql("select 1")
                rows = [row async for row in results]
                self.assertEqual(len(rows), 1)

            self._assert_operation_metrics_recorded(
                reader,
                method="Spanner.ExecuteStreamingSql",
                expected_attempt_count=2,
            )

    async def test_async_session_ping_emits_operation_metrics(self):
        add_select1_result()
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = await self._setup_database()
            session = await database._pool.get()
            try:
                await session.ping()
            finally:
                await database._pool.put(session)

            self._assert_operation_metrics_recorded(reader, method="Spanner.ExecuteSql")

    async def test_async_operation_latency_streaming_read(self):
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = await self._setup_database()
            async with database.snapshot() as snapshot:
                results = await snapshot.read(
                    table="citizens",
                    columns=["email", "first_name"],
                    keyset=KeySet(all_=True),
                )
                self._assert_metrics_not_recorded(
                    reader,
                    method="Spanner.StreamingRead",
                    check_count=False,
                )

                _ = [row async for row in results]

            self._assert_operation_metrics_recorded(
                reader,
                method="Spanner.StreamingRead",
                check_operation_count=False,
            )

    async def test_async_operation_latency_recorded_on_early_stream_close(self):
        sql = "select id from early_close_table"
        add_single_result(
            sql,
            "id",
            TypeCode.INT64,
            [("1",), ("2",), ("3",)],
            chunk_config=PartialResultSetConfig(set_last_flag=True),
        )
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = await self._setup_database()
            async with database.snapshot() as snapshot:
                results = await snapshot.execute_sql(sql)
                row_iterator = aiter(results)
                first_row = await anext(row_iterator)
                self.assertEqual([1], first_row)

                self._assert_metrics_not_recorded(
                    reader,
                    method="Spanner.ExecuteStreamingSql",
                    check_count=False,
                )

                # AsyncStreamedResultSet.__aiter__ does not close _response_iterator on aclose().
                await results._response_iterator.aclose()
                await row_iterator.aclose()

                self._assert_operation_metrics_recorded(
                    reader, method="Spanner.ExecuteStreamingSql"
                )

    async def test_async_operation_latency_recorded_on_mid_stream_error(self):
        sql = "select id, payload from error_metrics_docs"
        add_multi_column_result(
            sql,
            [("id", TypeCode.INT64), ("payload", TypeCode.STRING)],
            [("1", "hello world"), ("2", "abcdef")],
            chunk_config=PartialResultSetConfig(max_string_chunk_length=4),
        )
        add_execute_streaming_sql_error(sql, 3, deadline_exceeded_status())
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with self.patched_metrics_environment(meter_provider):
            database = await self._setup_database()
            async with database.snapshot() as snapshot:
                results = await snapshot.execute_sql(sql)
                row_iterator = aiter(results)
                self.assertEqual([1, "hello world"], await anext(row_iterator))
                with self.assertRaisesRegex(
                    exceptions.DeadlineExceeded, "Deadline exceeded."
                ):
                    await anext(row_iterator)

            self._assert_operation_metrics_recorded(
                reader, method="Spanner.ExecuteStreamingSql"
            )
