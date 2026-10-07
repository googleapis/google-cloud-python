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
from unittest import mock

import grpc
from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

import google.cloud.spanner_v1._async.client as async_client_mod
import google.cloud.spanner_v1.client as client_mod
from google.cloud.spanner_v1 import Client, _helpers
from google.cloud.spanner_v1._async.client import Client as AsyncClient
from google.cloud.spanner_v1._async.pool import FixedSizePool as AsyncFixedSizePool
from google.cloud.spanner_v1.metrics.metrics_interceptor import MetricsInterceptor
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)
from google.cloud.spanner_v1.pool import FixedSizePool
from google.cloud.spanner_v1.services.spanner.async_client import SpannerAsyncClient
from google.cloud.spanner_v1.services.spanner.transports.grpc_asyncio import (
    SpannerGrpcAsyncIOTransport,
)
from tests.mockserver_tests.mock_server_test_base import (
    AsyncMockServerTestBase,
    MockServerTestBase,
    add_header,
    add_select1_result,
)


class TestFrontendMetricsIntegration(MockServerTestBase):
    def setUp(self):
        super().setUp()
        self._orig_disable_builtin_metrics = os.environ.get(
            "SPANNER_DISABLE_BUILTIN_METRICS"
        )
        self._orig_disable_afe_server_timing = os.environ.get(
            "SPANNER_DISABLE_AFE_SERVER_TIMING"
        )
        self._orig_enable_afe_server_timing = _helpers.ENABLE_AFE_SERVER_TIMING

        os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = "false"
        os.environ["SPANNER_DISABLE_AFE_SERVER_TIMING"] = "false"
        _helpers.ENABLE_AFE_SERVER_TIMING = True
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False
        async_client_mod._metrics_monitor_initialized = False

    def tearDown(self):
        super().tearDown()
        if self._orig_disable_builtin_metrics is None:
            os.environ.pop("SPANNER_DISABLE_BUILTIN_METRICS", None)
        else:
            os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = (
                self._orig_disable_builtin_metrics
            )

        if self._orig_disable_afe_server_timing is None:
            os.environ.pop("SPANNER_DISABLE_AFE_SERVER_TIMING", None)
        else:
            os.environ["SPANNER_DISABLE_AFE_SERVER_TIMING"] = (
                self._orig_disable_afe_server_timing
            )

        _helpers.ENABLE_AFE_SERVER_TIMING = self._orig_enable_afe_server_timing
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False
        async_client_mod._metrics_monitor_initialized = False

    def test_gfe_metrics_exported(self):
        add_select1_result()
        add_header(
            "ExecuteStreamingSql",
            "server-timing",
            "gfet4t7; dur=55, afe; dur=23",
        )
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with (
            mock.patch(
                "google.cloud.spanner_v1.metrics.metrics_tracer_factory.get_meter_provider",
                return_value=meter_provider,
            ),
            mock.patch(
                "google.cloud.spanner_v1.client.MeterProvider",
                return_value=meter_provider,
            ),
            mock.patch(
                "google.cloud.spanner_v1.client._get_spanner_emulator_host",
                return_value=None,
            ),
        ):
            client = Client(
                project="p",
                credentials=AnonymousCredentials(),
                client_options=ClientOptions(
                    api_endpoint="localhost:" + str(MockServerTestBase.port),
                ),
            )
            instance = client.instance("test-instance")
            database = instance.database(
                "test-database",
                pool=FixedSizePool(size=10),
                enable_interceptors_in_tests=True,
            )
            database._interceptors.append(MetricsInterceptor())
            database._spanner_api = None  # Force recreation with the new interceptor

            with database.snapshot() as snapshot:
                results = snapshot.execute_sql("select 1")
                # Consume the streaming results to complete the stream
                list(results)

        metric_data = reader.get_metrics_data()
        self.assertIsNotNone(metric_data)
        metrics = {
            metric.name: metric
            for rm in metric_data.resource_metrics
            for sm in rm.scope_metrics
            for metric in sm.metrics
        }

        self.assertIn("gfe_latencies", metrics, f"Metrics: {list(metrics.keys())}")
        gfe_metric = metrics["gfe_latencies"]
        point = next(iter(gfe_metric.data.data_points))
        self.assertEqual(point.sum, 55)

        self.assertIn("afe_latencies", metrics, f"Metrics: {list(metrics.keys())}")
        afe_metric = metrics["afe_latencies"]
        point = next(iter(afe_metric.data.data_points))
        self.assertEqual(point.sum, 23)

    def test_gfe_missing_header_count_exported(self):
        add_select1_result()
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        try:
            with (
                mock.patch(
                    "google.cloud.spanner_v1.metrics.metrics_tracer_factory.get_meter_provider",
                    return_value=meter_provider,
                ),
                mock.patch(
                    "google.cloud.spanner_v1.client.MeterProvider",
                    return_value=meter_provider,
                ),
                mock.patch(
                    "google.cloud.spanner_v1.client._get_spanner_emulator_host",
                    return_value=None,
                ),
            ):
                client = Client(
                    project="p",
                    credentials=AnonymousCredentials(),
                    client_options=ClientOptions(
                        api_endpoint="localhost:" + str(MockServerTestBase.port),
                    ),
                )
                instance = client.instance("test-instance")
                database = instance.database(
                    "test-database",
                    pool=FixedSizePool(size=10),
                    enable_interceptors_in_tests=True,
                )
                database._interceptors.append(MetricsInterceptor())
                database._spanner_api = (
                    None  # Force recreation with the new interceptor
                )

                with database.snapshot() as snapshot:
                    results = snapshot.execute_sql("select 1")
                    list(results)

            metric_data = reader.get_metrics_data()
            self.assertIsNotNone(metric_data)
            metrics = {
                metric.name: metric
                for rm in metric_data.resource_metrics
                for sm in rm.scope_metrics
                for metric in sm.metrics
            }

            self.assertIn(
                "gfe_connectivity_error_count",
                metrics,
                f"Metrics: {list(metrics.keys())}",
            )
            missing_metric = metrics["gfe_connectivity_error_count"]
            point = next(iter(missing_metric.data.data_points))
            self.assertGreaterEqual(point.value, 1)

            self.assertIn(
                "afe_connectivity_error_count",
                metrics,
                f"Metrics: {list(metrics.keys())}",
            )
            afe_missing_metric = metrics["afe_connectivity_error_count"]
            afe_point = next(iter(afe_missing_metric.data.data_points))
            self.assertGreaterEqual(afe_point.value, 1)
        finally:
            pass


class TestFrontendMetricsAsyncIntegration(AsyncMockServerTestBase):
    def setUp(self):
        super().setUp()
        self._orig_disable_builtin_metrics = os.environ.get(
            "SPANNER_DISABLE_BUILTIN_METRICS"
        )
        self._orig_disable_afe_server_timing = os.environ.get(
            "SPANNER_DISABLE_AFE_SERVER_TIMING"
        )
        self._orig_enable_afe_server_timing = _helpers.ENABLE_AFE_SERVER_TIMING

        os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = "false"
        os.environ["SPANNER_DISABLE_AFE_SERVER_TIMING"] = "false"
        _helpers.ENABLE_AFE_SERVER_TIMING = True
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False
        async_client_mod._metrics_monitor_initialized = False

    def tearDown(self):
        super().tearDown()
        if self._orig_disable_builtin_metrics is None:
            os.environ.pop("SPANNER_DISABLE_BUILTIN_METRICS", None)
        else:
            os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = (
                self._orig_disable_builtin_metrics
            )

        if self._orig_disable_afe_server_timing is None:
            os.environ.pop("SPANNER_DISABLE_AFE_SERVER_TIMING", None)
        else:
            os.environ["SPANNER_DISABLE_AFE_SERVER_TIMING"] = (
                self._orig_disable_afe_server_timing
            )

        _helpers.ENABLE_AFE_SERVER_TIMING = self._orig_enable_afe_server_timing
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False
        async_client_mod._metrics_monitor_initialized = False

    async def asyncSetUp(self):
        await super().asyncSetUp()
        if AsyncMockServerTestBase.spanner_service:
            AsyncMockServerTestBase.spanner_service.clear_results()

    async def asyncTearDown(self):
        await super().asyncTearDown()
        if AsyncMockServerTestBase.spanner_service:
            AsyncMockServerTestBase.spanner_service.clear_results()

    async def test_async_gfe_metrics_exported(self):
        add_select1_result()
        add_header(
            "ExecuteStreamingSql",
            "server-timing",
            "gfet4t7; dur=55, afe; dur=23",
        )
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with (
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
            client = AsyncClient(
                project="p",
                credentials=AnonymousCredentials(),
                client_options=ClientOptions(
                    api_endpoint="localhost:" + str(AsyncMockServerTestBase.port),
                ),
            )
            instance = client.instance("test-instance")
            database = await instance.database(
                "test-database",
                pool=AsyncFixedSizePool(size=10),
            )
            async with grpc.aio.insecure_channel(
                "localhost:" + str(AsyncMockServerTestBase.port),
            ) as channel:
                transport = SpannerGrpcAsyncIOTransport(
                    channel=channel,
                    metrics_interceptor=MetricsInterceptor(),
                )
                database._spanner_api = SpannerAsyncClient(
                    client_info=client._client_info,
                    transport=transport,
                )

                async with database.snapshot() as snapshot:
                    results = await snapshot.execute_sql("select 1")
                    # Consume the async streaming results to complete the stream
                    async for _ in results:
                        pass

        metric_data = reader.get_metrics_data()
        self.assertIsNotNone(metric_data)
        metrics = {
            metric.name: metric
            for resource_metric in metric_data.resource_metrics
            for scope_metric in resource_metric.scope_metrics
            for metric in scope_metric.metrics
        }

        self.assertIn("gfe_latencies", metrics, f"Metrics: {list(metrics.keys())}")
        gfe_metric = metrics["gfe_latencies"]
        gfe_point = next(iter(gfe_metric.data.data_points))
        self.assertEqual(gfe_point.sum, 55)

        self.assertIn("afe_latencies", metrics, f"Metrics: {list(metrics.keys())}")
        afe_metric = metrics["afe_latencies"]
        afe_point = next(iter(afe_metric.data.data_points))
        self.assertEqual(afe_point.sum, 23)

        self.assertIn("attempt_latencies", metrics, f"Metrics: {list(metrics.keys())}")
        attempt_latencies_metric = metrics["attempt_latencies"]
        streaming_points = [
            point
            for point in attempt_latencies_metric.data.data_points
            if point.attributes.get("method") == "Spanner.ExecuteStreamingSql"
        ]
        self.assertTrue(len(streaming_points) > 0)
        self.assertEqual(streaming_points[0].attributes.get("status"), "OK")

    async def test_async_gfe_missing_header_count_exported(self):
        add_select1_result()
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        with (
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
            client = AsyncClient(
                project="p",
                credentials=AnonymousCredentials(),
                client_options=ClientOptions(
                    api_endpoint="localhost:" + str(AsyncMockServerTestBase.port),
                ),
            )
            instance = client.instance("test-instance")
            database = await instance.database(
                "test-database",
                pool=AsyncFixedSizePool(size=10),
            )
            async with grpc.aio.insecure_channel(
                "localhost:" + str(AsyncMockServerTestBase.port),
            ) as channel:
                transport = SpannerGrpcAsyncIOTransport(
                    channel=channel,
                    metrics_interceptor=MetricsInterceptor(),
                )
                database._spanner_api = SpannerAsyncClient(
                    client_info=client._client_info,
                    transport=transport,
                )

                async with database.snapshot() as snapshot:
                    results = await snapshot.execute_sql("select 1")
                    async for _ in results:
                        pass

        metric_data = reader.get_metrics_data()
        self.assertIsNotNone(metric_data)
        metrics = {
            metric.name: metric
            for resource_metric in metric_data.resource_metrics
            for scope_metric in resource_metric.scope_metrics
            for metric in scope_metric.metrics
        }

        self.assertIn(
            "gfe_connectivity_error_count",
            metrics,
            f"Metrics: {list(metrics.keys())}",
        )
        missing_metric = metrics["gfe_connectivity_error_count"]
        streaming_points = [
            point
            for point in missing_metric.data.data_points
            if point.attributes.get("method") == "Spanner.ExecuteStreamingSql"
        ]
        self.assertTrue(len(streaming_points) > 0)
        self.assertGreaterEqual(streaming_points[0].value, 1)

        self.assertIn(
            "afe_connectivity_error_count",
            metrics,
            f"Metrics: {list(metrics.keys())}",
        )
        afe_missing_metric = metrics["afe_connectivity_error_count"]
        streaming_points = [
            point
            for point in afe_missing_metric.data.data_points
            if point.attributes.get("method") == "Spanner.ExecuteStreamingSql"
        ]
        self.assertTrue(len(streaming_points) > 0)
        self.assertGreaterEqual(streaming_points[0].value, 1)
