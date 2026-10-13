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

import os
from unittest import mock

import pytest
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

from google.cloud.spanner_v1.metrics import constants
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)


def test_builtin_metrics_with_default_otel(not_emulator, shared_database):
    """
    Verifies that built-in metrics are collected by default when a
    transaction is executed.
    """
    reader = InMemoryMetricReader()
    meter_provider = MeterProvider(metric_readers=[reader])

    old_factory = SpannerMetricsTracerFactory._metrics_tracer_factory
    SpannerMetricsTracerFactory._metrics_tracer_factory = None
    try:
        # Patch the meter provider setup to use our in-memory reader.
        with (
            mock.patch(
                "google.cloud.spanner_v1.metrics.metrics_tracer_factory.get_meter_provider",
                return_value=meter_provider,
            ),
            mock.patch(
                "google.cloud.spanner_v1.client.MeterProvider",
                return_value=meter_provider,
            ),
            mock.patch.dict(os.environ, {"SPANNER_DISABLE_BUILTIN_METRICS": "false"}),
        ):
            with shared_database.snapshot() as snapshot:
                list(snapshot.execute_sql("SELECT 1"))
    finally:
        SpannerMetricsTracerFactory._metrics_tracer_factory = old_factory

    metric_data = reader.get_metrics_data()

    assert len(metric_data.resource_metrics) >= 1
    assert len(metric_data.resource_metrics[0].scope_metrics) >= 1

    collected_metrics = {
        metric.name
        for metric in metric_data.resource_metrics[0].scope_metrics[0].metrics
    }
    expected_metrics = {
        constants.METRIC_NAME_OPERATION_LATENCIES,
        constants.METRIC_NAME_ATTEMPT_LATENCIES,
        constants.METRIC_NAME_OPERATION_COUNT,
        constants.METRIC_NAME_ATTEMPT_COUNT,
        constants.METRIC_NAME_GFE_LATENCY,
        constants.METRIC_NAME_AFE_LATENCY,
    }
    assert expected_metrics.issubset(collected_metrics)

    for metric in metric_data.resource_metrics[0].scope_metrics[0].metrics:
        if metric.name == constants.METRIC_NAME_OPERATION_COUNT:
            point = next(iter(metric.data.data_points))
            assert point.value == 1
            assert point.attributes["method"] == "ExecuteSql"
            return

    pytest.fail(f"Metric '{constants.METRIC_NAME_OPERATION_COUNT}' not found.")
