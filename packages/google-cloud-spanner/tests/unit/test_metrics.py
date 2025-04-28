# Copyright 2025 Google LLC
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

import pytest
from unittest.mock import MagicMock
from google.api_core.exceptions import ServiceUnavailable
from google.cloud.spanner_v1.client import Client
from unittest.mock import patch
from grpc._interceptor import _UnaryOutcome
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)
from opentelemetry import metrics

pytest.importorskip("opentelemetry")
# Skip if semconv attributes are not present, as tracing wont' be enabled either
# pytest.importorskip("opentelemetry.semconv.attributes.otel_attributes")


@pytest.fixture(autouse=True)
def patched_client(monkeypatch):
    monkeypatch.setenv("SPANNER_ENABLE_BUILTIN_METRICS", "true")
    metrics.set_meter_provider(metrics.NoOpMeterProvider())

    # Remove the Tracer factory to avoid previously disabled factory polluting from other tests
    if SpannerMetricsTracerFactory._metrics_tracer_factory is not None:
        SpannerMetricsTracerFactory._metrics_tracer_factory = None

    client = Client()
    yield client

    # Resetting
    metrics.set_meter_provider(metrics.NoOpMeterProvider())
    SpannerMetricsTracerFactory._metrics_tracer_factory = None
    SpannerMetricsTracerFactory.current_metrics_tracer = None


def test_metrics_emission_with_failure_attempt(patched_client):
    instance = patched_client.instance("test-instance")
    database = instance.database("example-db")
    factory = SpannerMetricsTracerFactory()

    assert factory.enabled

    transport = database.spanner_api._transport
    metrics_interceptor = transport._metrics_interceptor
    original_intercept = metrics_interceptor.intercept
    first_attempt = True

    def mocked_raise(*args, **kwargs):
        raise ServiceUnavailable("Service Unavailable")

    def mocked_call(*args, **kwargs):
        return _UnaryOutcome(MagicMock(), MagicMock())

    def intercept_wrapper(invoked_method, request_or_iterator, call_details):
        nonlocal first_attempt
        invoked_method = mocked_call
        if first_attempt:
            first_attempt = False
            invoked_method = mocked_raise
        response = original_intercept(
            invoked_method=invoked_method,
            request_or_iterator=request_or_iterator,
            call_details=call_details,
        )
        return response

    metrics_interceptor.intercept = intercept_wrapper
    patch_path = "google.cloud.spanner_v1.metrics.metrics_exporter.CloudMonitoringMetricsExporter.export"
    with patch(patch_path):
        with database.snapshot():
            pass

    # Verify that the attempt count increased from the failed initial attempt
    assert (
        SpannerMetricsTracerFactory.current_metrics_tracer.current_op.attempt_count
    ) == 2
