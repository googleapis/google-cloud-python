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

import os
from concurrent import futures
from unittest import mock

import grpc
from google.api_core.client_options import ClientOptions
from google.auth.credentials import Credentials, Scoped
from google.cloud.monitoring_v3 import CreateTimeSeriesRequest
from google.protobuf import empty_pb2
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

import google.cloud.spanner_v1.client as client_mod
from google.cloud.spanner_v1 import Client
from google.cloud.spanner_v1.metrics.constants import (
    BUILT_IN_METRICS_METER_NAME,
    METRIC_NAME_OPERATION_COUNT,
    NATIVE_METRICS_PREFIX,
)
from google.cloud.spanner_v1.metrics.metrics_exporter import (
    CloudMonitoringMetricsExporter,
)
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)
from tests.mockserver_tests.mock_server_test_base import MockServerTestBase


class _FakeUniverseCredentials(Credentials, Scoped):
    """Minimal Scoped credentials with configurable universe_domain and project_id."""

    def __init__(
        self,
        universe_domain="googleapis.com",
        project_id="resolved-project",
        scopes=("https://www.googleapis.com/auth/spanner.admin",),
        requires_scopes=False,
    ):
        super().__init__()
        self._universe_domain = universe_domain
        self.project_id = project_id
        self._scopes = scopes
        self._requires_scopes = requires_scopes

    @property
    def universe_domain(self):
        return self._universe_domain

    @property
    def requires_scopes(self):
        return self._requires_scopes

    @property
    def scopes(self):
        return self._scopes

    def with_scopes(self, scopes, default_scopes=None):
        return _FakeUniverseCredentials(
            universe_domain=self._universe_domain,
            project_id=self.project_id,
            scopes=tuple(scopes),
            requires_scopes=False,
        )

    def refresh(self, request):
        self.token = "fake-token"


class _MockMonitoringServer:
    """Local in-process gRPC server implementing CreateServiceTimeSeries."""

    def __init__(self):
        self.requests = []
        self.metadata = []
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        handler = grpc.method_handlers_generic_handler(
            "google.monitoring.v3.MetricService",
            {
                "CreateServiceTimeSeries": grpc.unary_unary_rpc_method_handler(
                    self._create_service_time_series,
                    request_deserializer=CreateTimeSeriesRequest.deserialize,
                    response_serializer=empty_pb2.Empty.SerializeToString,
                ),
            },
        )
        self._server.add_generic_rpc_handlers((handler,))
        self.port = self._server.add_insecure_port("127.0.0.1:0")

    def _create_service_time_series(self, request, context):
        self.requests.append(request)
        self.metadata.append(dict(context.invocation_metadata()))
        return empty_pb2.Empty()

    def start(self):
        self._server.start()
        return self

    def stop(self):
        self._server.stop(grace=0)

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()


def _collect_sample_metrics(project_id):
    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader])
    meter = provider.get_meter(BUILT_IN_METRICS_METER_NAME)
    counter = meter.create_counter(
        name=METRIC_NAME_OPERATION_COUNT,
        description="Test operation count",
        unit="1",
    )
    counter.add(
        1,
        attributes={
            "project_id": project_id,
            "instance_id": "test-instance",
            "instance_config": "regional-us-central1",
            "location": "us-central1",
            "client_hash": "000001",
            "client_uid": "test-uid",
            "client_name": "spanner-python/test",
            "database": "test-db",
            "method": "Spanner.ExecuteStreamingSql",
            "status": "OK",
        },
    )
    return reader.get_metrics_data()


class TestMetricsExporterEndpointIntegration(MockServerTestBase):
    def setUp(self):
        super().setUp()
        self._orig_disable = os.environ.get("SPANNER_DISABLE_BUILTIN_METRICS")
        os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = "false"
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False

    def tearDown(self):
        super().tearDown()
        if self._orig_disable is None:
            os.environ.pop("SPANNER_DISABLE_BUILTIN_METRICS", None)
        else:
            os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = self._orig_disable
        metrics.set_meter_provider(metrics.NoOpMeterProvider())
        SpannerMetricsTracerFactory._metrics_tracer_factory = None
        client_mod._metrics_monitor_initialized = False

    def test_exporter_sends_rpc_to_configured_endpoint_with_matching_universe(self):
        """End-to-end gRPC export hits the configured Monitoring server and sends user-agent."""
        creds = _FakeUniverseCredentials(
            universe_domain="custom-universe.test",
            project_id="test-project",
        )
        with _MockMonitoringServer() as server:
            endpoint = f"127.0.0.1:{server.port}"
            with (
                mock.patch.dict(
                    os.environ,
                    {
                        "GOOGLE_API_USE_CLIENT_CERTIFICATE": "false",
                        "GOOGLE_API_USE_MTLS_ENDPOINT": "never",
                    },
                ),
                mock.patch(
                    "google.cloud.spanner_v1.metrics.metrics_exporter."
                    "MetricServiceGrpcTransport.create_channel",
                    side_effect=lambda host, **kw: grpc.insecure_channel(
                        host, options=kw.get("options")
                    ),
                ),
            ):
                exporter = CloudMonitoringMetricsExporter(
                    project_id="test-project",
                    credentials=creds,
                    client_options=ClientOptions(
                        api_endpoint=endpoint,
                        universe_domain="custom-universe.test",
                    ),
                )
                try:
                    metrics_data = _collect_sample_metrics("test-project")
                    self.assertTrue(exporter.export(metrics_data))
                finally:
                    exporter.shutdown()

            self.assertEqual(len(server.requests), 1)
            self.assertEqual(server.requests[0].name, "projects/test-project")
            self.assertEqual(len(server.requests[0].time_series), 1)
            self.assertEqual(
                server.requests[0].time_series[0].metric.type,
                f"{NATIVE_METRICS_PREFIX}/{METRIC_NAME_OPERATION_COUNT}",
            )
            self.assertIn(
                "python-spanner; google-cloud-service-metric-exporter",
                server.metadata[0].get("user-agent", ""),
            )

    def test_client_env_universe_domain_propagates_to_monitoring_channel(self):
        """Client respects GOOGLE_CLOUD_UNIVERSE_DOMAIN end-to-end for Monitoring."""
        creds = _FakeUniverseCredentials(
            universe_domain="env-universe.test",
            project_id="env-project",
        )
        captured = {}

        def _capture_channel(host, **kwargs):
            captured["host"] = host
            captured["credentials"] = kwargs.get("credentials")
            return mock.MagicMock()

        env_override = {
            "SPANNER_DISABLE_BUILTIN_METRICS": "false",
            "GOOGLE_CLOUD_UNIVERSE_DOMAIN": "env-universe.test",
            "GOOGLE_API_USE_CLIENT_CERTIFICATE": "false",
            "GOOGLE_API_USE_MTLS_ENDPOINT": "never",
        }
        with (
            mock.patch.dict(os.environ, env_override),
            mock.patch(
                "google.cloud.spanner_v1.client._get_spanner_emulator_host",
                return_value=None,
            ),
            mock.patch(
                "google.cloud.spanner_v1.client.PeriodicExportingMetricReader"
            ) as mock_reader,
            mock.patch(
                "google.cloud.spanner_v1.metrics.metrics_exporter."
                "MetricServiceGrpcTransport.create_channel",
                side_effect=_capture_channel,
            ),
        ):
            os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
            os.environ.pop("GCLOUD_PROJECT", None)
            Client(project=None, credentials=creds)

        self.assertEqual(captured["host"], "monitoring.env-universe.test:443")
        self.assertEqual(
            captured["credentials"].scopes,
            ("https://www.googleapis.com/auth/monitoring.write",),
        )
        exporter = mock_reader.call_args[0][0]
        self.assertEqual(exporter.project_id, "env-project")
        self.assertEqual(exporter.project_name, "projects/env-project")

    def test_client_custom_api_endpoint_never_opens_monitoring_channel(self):
        """Client with a custom api_endpoint does not initialize CloudMonitoringMetricsExporter."""
        creds = _FakeUniverseCredentials(project_id="test-project")
        with (
            mock.patch(
                "google.cloud.spanner_v1.client._get_spanner_emulator_host",
                return_value=None,
            ),
            mock.patch(
                "google.cloud.spanner_v1.metrics.metrics_exporter."
                "MetricServiceGrpcTransport.create_channel"
            ) as mock_create_channel,
        ):
            Client(
                project="test-project",
                credentials=creds,
                client_options=ClientOptions(
                    api_endpoint=f"localhost:{MockServerTestBase.port}",
                ),
            )

        mock_create_channel.assert_not_called()
        self.assertIsInstance(metrics.get_meter_provider(), metrics.NoOpMeterProvider)

    def test_client_universe_domain_propagates_to_monitoring_channel_and_project(self):
        """Client with project=None and custom universe_domain routes Monitoring to that universe."""
        creds = _FakeUniverseCredentials(
            universe_domain="custom-universe.test",
            project_id="creds-project",
        )
        captured = {}

        def _capture_channel(host, **kwargs):
            captured["host"] = host
            captured["credentials"] = kwargs.get("credentials")
            return mock.MagicMock()

        env_override = {
            "SPANNER_DISABLE_BUILTIN_METRICS": "false",
            "GOOGLE_API_USE_CLIENT_CERTIFICATE": "false",
            "GOOGLE_API_USE_MTLS_ENDPOINT": "never",
        }
        with (
            mock.patch.dict(os.environ, env_override),
            mock.patch(
                "google.cloud.spanner_v1.client._get_spanner_emulator_host",
                return_value=None,
            ),
            mock.patch(
                "google.cloud.spanner_v1.client.PeriodicExportingMetricReader"
            ) as mock_reader,
            mock.patch(
                "google.cloud.spanner_v1.metrics.metrics_exporter."
                "MetricServiceGrpcTransport.create_channel",
                side_effect=_capture_channel,
            ),
        ):
            os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
            os.environ.pop("GCLOUD_PROJECT", None)
            Client(
                project=None,
                credentials=creds,
                client_options=ClientOptions(universe_domain="custom-universe.test"),
            )

        self.assertEqual(captured["host"], "monitoring.custom-universe.test:443")
        self.assertEqual(
            captured["credentials"].scopes,
            ("https://www.googleapis.com/auth/monitoring.write",),
        )
        exporter = mock_reader.call_args[0][0]
        self.assertEqual(exporter.project_id, "creds-project")
        self.assertEqual(exporter.project_name, "projects/creds-project")

    def test_client_custom_api_endpoint_with_spanner_monitoring_host(self):
        """SPANNER_MONITORING_HOST opts in to metrics export with a custom api_endpoint."""
        creds = _FakeUniverseCredentials(project_id="test-project")
        captured = {}

        def _capture_channel(host, **kwargs):
            captured["host"] = host
            return mock.MagicMock()

        env_override = {
            "SPANNER_DISABLE_BUILTIN_METRICS": "false",
            "SPANNER_MONITORING_HOST": "monitoring-psc.internal:443",
            "GOOGLE_API_USE_CLIENT_CERTIFICATE": "false",
            "GOOGLE_API_USE_MTLS_ENDPOINT": "never",
        }
        with (
            mock.patch.dict(os.environ, env_override),
            mock.patch(
                "google.cloud.spanner_v1.client._get_spanner_emulator_host",
                return_value=None,
            ),
            mock.patch("google.cloud.spanner_v1.client.PeriodicExportingMetricReader"),
            mock.patch(
                "google.cloud.spanner_v1.metrics.metrics_exporter."
                "MetricServiceGrpcTransport.create_channel",
                side_effect=_capture_channel,
            ),
        ):
            Client(
                project="test-project",
                credentials=creds,
                client_options=ClientOptions(
                    api_endpoint="spanner.us-central1.rep.googleapis.com",
                ),
            )

        self.assertEqual(captured["host"], "monitoring-psc.internal:443")
