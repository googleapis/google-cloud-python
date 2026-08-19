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

import google.cloud.spanner_v1.client as client_mod
from google.cloud.spanner_v1 import Client
from google.cloud.spanner_v1.metrics.metrics_interceptor import MetricsInterceptor
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)
from google.cloud.spanner_v1.pool import FixedSizePool
from tests.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    add_select1_result,
)


class TestFrontendMetricsIntegration(MockServerTestBase):
    def setUp(self):
        super().setUp()
        os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = "false"
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False

    def tearDown(self):
        super().tearDown()
        os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = "true"
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False

    def test_gfe_metrics_exported(self):
        add_select1_result()
        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(metric_readers=[reader])

        orig_call = grpc._channel._UnaryStreamMultiCallable.__call__
        orig_initial_metadata = grpc._channel._MultiThreadedRendezvous.initial_metadata
        orig_trailing_metadata = (
            grpc._channel._MultiThreadedRendezvous.trailing_metadata
        )

        def custom_initial_metadata(self):
            mocked = getattr(self, "_is_execute_streaming_sql_mock", False)
            if mocked:
                return (("server-timing", "gfet4t7; dur=55, afe; dur=23"),)
            return orig_initial_metadata(self)

        def custom_trailing_metadata(self):
            mocked = getattr(self, "_is_execute_streaming_sql_mock", False)
            if mocked:
                return (("server-timing", "gfet4t7; dur=55, afe; dur=23"),)
            return orig_trailing_metadata(self)

        def custom_call(self_callable, request, *args, **kwargs):
            method = getattr(self_callable, "_method", b"")
            method_str = method.decode("utf-8") if isinstance(method, bytes) else method
            response = orig_call(self_callable, request, *args, **kwargs)
            if "ExecuteStreamingSql" in method_str:
                response._is_execute_streaming_sql_mock = True
            return response

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
                mock.patch(
                    "grpc._channel._UnaryStreamMultiCallable.__call__",
                    custom_call,
                ),
                mock.patch(
                    "grpc._channel._MultiThreadedRendezvous.initial_metadata",
                    custom_initial_metadata,
                ),
                mock.patch(
                    "grpc._channel._MultiThreadedRendezvous.trailing_metadata",
                    custom_trailing_metadata,
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

        finally:
            pass

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
