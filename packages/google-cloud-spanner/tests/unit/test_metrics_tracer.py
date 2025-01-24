# -*- coding: utf-8 -*-
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

from google.cloud.spanner_v1.metrics.metrics_tracer import MetricsTracer, MetricOpTracer
import mock
from opentelemetry.metrics import Counter, Histogram
from datetime import datetime

pytest.importorskip("opentelemetry")


@pytest.fixture
def metrics_tracer():
    mock_attempt_counter = mock.create_autospec(Counter, instance=True)
    mock_attempt_latency = mock.create_autospec(Histogram, instance=True)
    mock_operation_counter = mock.create_autospec(Counter, instance=True)
    mock_operation_latency = mock.create_autospec(Histogram, instance=True)
    return MetricsTracer(
        enabled=True,
        instrument_attempt_latency=mock_attempt_latency,
        instrument_attempt_counter=mock_attempt_counter,
        instrument_operation_latency=mock_operation_latency,
        instrument_operation_counter=mock_operation_counter,
        client_attributes={"project_id": "test_project"},
    )


def test_record_attempt_start(metrics_tracer):
    metrics_tracer.record_attempt_start()
    assert metrics_tracer.current_op.current_attempt is not None
    assert metrics_tracer.current_op.current_attempt.start_time is not None
    assert metrics_tracer.current_op.attempt_count == 1


def test_record_operation_start(metrics_tracer):
    metrics_tracer.record_operation_start()
    assert metrics_tracer.current_op.start_time is not None


def test_record_attempt_completion(metrics_tracer):
    metrics_tracer.record_attempt_start()
    metrics_tracer.record_attempt_completion()
    assert metrics_tracer.current_op.current_attempt.status == "OK"


def test_record_operation_completion(metrics_tracer):
    metrics_tracer.record_operation_start()
    metrics_tracer.record_attempt_start()
    metrics_tracer.record_attempt_completion()
    metrics_tracer.record_operation_completion()
    assert metrics_tracer.instrument_attempt_counter.add.call_count == 1
    assert metrics_tracer.instrument_attempt_latency.record.call_count == 1
    assert metrics_tracer.instrument_operation_latency.record.call_count == 1
    assert metrics_tracer.instrument_operation_counter.add.call_count == 1


def test_atempt_otel_attributes(metrics_tracer):
    from google.cloud.spanner_v1.metrics.constants import (
        METRIC_LABEL_KEY_DIRECT_PATH_USED,
    )

    metrics_tracer.current_op._current_attempt = None
    attributes = metrics_tracer._create_attempt_otel_attributes()
    assert METRIC_LABEL_KEY_DIRECT_PATH_USED not in attributes


def test_disabled(metrics_tracer):
    mock_operation = mock.create_autospec(MetricOpTracer, instance=True)
    metrics_tracer.enabled = False
    metrics_tracer._current_op = mock_operation

    # Attempt start should be skipped
    metrics_tracer.record_attempt_start()
    assert mock_operation.new_attempt.call_count == 0

    # Attempt completion should also be skipped
    metrics_tracer.record_attempt_completion()
    assert metrics_tracer.instrument_attempt_latency.record.call_count == 0

    # Operation start should be skipped
    metrics_tracer.record_operation_start()
    assert mock_operation.start.call_count == 0

    # Operation completion should also skip all metric logic
    metrics_tracer.record_operation_completion()
    assert metrics_tracer.instrument_attempt_counter.add.call_count == 0
    assert metrics_tracer.instrument_operation_latency.record.call_count == 0
    assert metrics_tracer.instrument_operation_counter.add.call_count == 0
    assert not metrics_tracer._create_operation_otel_attributes()
    assert not metrics_tracer._create_attempt_otel_attributes()


def test_get_ms_time_diff():
    # Create two datetime objects
    start_time = datetime(2025, 1, 1, 12, 0, 0)
    end_time = datetime(2025, 1, 1, 12, 0, 1)  # 1 second later

    # Calculate expected milliseconds difference
    expected_diff = 1000.0  # 1 second in milliseconds

    # Call the static method
    actual_diff = MetricsTracer._get_ms_time_diff(start_time, end_time)

    # Assert the expected and actual values are equal
    assert actual_diff == expected_diff


def test_get_ms_time_diff_negative():
    # Create two datetime objects where end is before start
    start_time = datetime(2025, 1, 1, 12, 0, 1)
    end_time = datetime(2025, 1, 1, 12, 0, 0)  # 1 second earlier

    # Calculate expected milliseconds difference
    expected_diff = -1000.0  # -1 second in milliseconds

    # Call the static method
    actual_diff = MetricsTracer._get_ms_time_diff(start_time, end_time)

    # Assert the expected and actual values are equal
    assert actual_diff == expected_diff


def test_set_project(metrics_tracer):
    metrics_tracer.set_project("test_project")
    assert metrics_tracer.client_attributes["project_id"] == "test_project"

    # Ensure it does not overwrite
    metrics_tracer.set_project("new_project")
    assert metrics_tracer.client_attributes["project_id"] == "test_project"


def test_set_instance(metrics_tracer):
    metrics_tracer.set_instance("test_instance")
    assert metrics_tracer.client_attributes["instance_id"] == "test_instance"

    # Ensure it does not overwrite
    metrics_tracer.set_instance("new_instance")
    assert metrics_tracer.client_attributes["instance_id"] == "test_instance"


def test_set_instance_config(metrics_tracer):
    metrics_tracer.set_instance_config("test_config")
    assert metrics_tracer.client_attributes["instance_config"] == "test_config"

    # Ensure it does not overwrite
    metrics_tracer.set_instance_config("new_config")
    assert metrics_tracer.client_attributes["instance_config"] == "test_config"


def test_set_location(metrics_tracer):
    metrics_tracer.set_location("test_location")
    assert metrics_tracer.client_attributes["location"] == "test_location"

    # Ensure it does not overwrite
    metrics_tracer.set_location("new_location")
    assert metrics_tracer.client_attributes["location"] == "test_location"


def test_set_client_hash(metrics_tracer):
    metrics_tracer.set_client_hash("test_hash")
    assert metrics_tracer.client_attributes["client_hash"] == "test_hash"

    # Ensure it does not overwrite
    metrics_tracer.set_client_hash("new_hash")
    assert metrics_tracer.client_attributes["client_hash"] == "test_hash"


def test_set_client_uid(metrics_tracer):
    metrics_tracer.set_client_uid("test_uid")
    assert metrics_tracer.client_attributes["client_uid"] == "test_uid"

    # Ensure it does not overwrite
    metrics_tracer.set_client_uid("new_uid")
    assert metrics_tracer.client_attributes["client_uid"] == "test_uid"


def test_set_client_name(metrics_tracer):
    metrics_tracer.set_client_name("test_name")
    assert metrics_tracer.client_attributes["client_name"] == "test_name"

    # Ensure it does not overwrite
    metrics_tracer.set_client_name("new_name")
    assert metrics_tracer.client_attributes["client_name"] == "test_name"


def test_set_database(metrics_tracer):
    metrics_tracer.set_database("test_db")
    assert metrics_tracer.client_attributes["database"] == "test_db"

    # Ensure it does not overwrite
    metrics_tracer.set_database("new_db")
    assert metrics_tracer.client_attributes["database"] == "test_db"


def test_enable_direct_path(metrics_tracer):
    metrics_tracer.enable_direct_path(True)
    assert metrics_tracer.client_attributes["directpath_enabled"] == "True"

    # Ensure it does not overwrite
    metrics_tracer.enable_direct_path(False)
    assert metrics_tracer.client_attributes["directpath_enabled"] == "True"


def test_set_method(metrics_tracer):
    metrics_tracer.set_method("test_method")
    assert metrics_tracer.client_attributes["method"] == "test_method"

    # Ensure it does not overwrite
    metrics_tracer.set_method("new_method")
    assert metrics_tracer.client_attributes["method"] == "test_method"
