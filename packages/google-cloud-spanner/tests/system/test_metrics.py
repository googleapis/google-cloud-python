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
import mock
import pytest

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

from google.cloud.spanner_v1 import Client

# System tests are skipped if the environment variables are not set.
PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
INSTANCE_ID = os.environ.get("SPANNER_TEST_INSTANCE")
DATABASE_ID = "test_metrics_db_system"


pytestmark = pytest.mark.skipif(
    not all([PROJECT, INSTANCE_ID]), reason="System test environment variables not set."
)


@pytest.fixture(scope="module")
def metrics_database():
    """Create a database for the test."""
    client = Client(project=PROJECT)
    instance = client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)
    if database.exists():  # Clean up from previous failed run
        database.drop()
    op = database.create()
    op.result(timeout=300)  # Wait for creation to complete
    yield database
    if database.exists():
        database.drop()


def test_builtin_metrics_with_default_otel(metrics_database):
    """
    Verifies that built-in metrics are collected by default when a
    transaction is executed.
    """
    reader = InMemoryMetricReader()
    meter_provider = MeterProvider(metric_readers=[reader])

    # Patch the client's metric setup to use our in-memory reader.
    with mock.patch(
        "google.cloud.spanner_v1.client.MeterProvider",
        return_value=meter_provider,
    ):
        with mock.patch.dict(os.environ, {"SPANNER_DISABLE_BUILTIN_METRICS": "false"}):
            with metrics_database.snapshot() as snapshot:
                list(snapshot.execute_sql("SELECT 1"))

    metric_data = reader.get_metrics_data()

    assert len(metric_data.resource_metrics) >= 1
    assert len(metric_data.resource_metrics[0].scope_metrics) >= 1

    collected_metrics = {
        metric.name
        for metric in metric_data.resource_metrics[0].scope_metrics[0].metrics
    }
    expected_metrics = {
        "spanner/operation_latencies",
        "spanner/attempt_latencies",
        "spanner/operation_count",
        "spanner/attempt_count",
        "spanner/gfe_latencies",
    }
    assert expected_metrics.issubset(collected_metrics)

    for metric in metric_data.resource_metrics[0].scope_metrics[0].metrics:
        if metric.name == "spanner/operation_count":
            point = next(iter(metric.data.data_points))
            assert point.value == 1
            assert point.attributes["method"] == "ExecuteSql"
            return

    pytest.fail("Metric 'spanner/operation_count' not found.")
