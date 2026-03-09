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
from unittest import mock
from google.cloud.spanner_v1.metrics.metrics_capture import MetricsCapture
from google.cloud.spanner_v1.metrics.metrics_tracer_factory import MetricsTracerFactory
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)


@pytest.fixture
def mock_tracer_factory():
    SpannerMetricsTracerFactory(enabled=True)
    with mock.patch.object(
        MetricsTracerFactory, "create_metrics_tracer"
    ) as mock_create:
        yield mock_create


def test_metrics_capture_enter(mock_tracer_factory):
    mock_tracer = mock.Mock()
    mock_tracer_factory.return_value = mock_tracer

    with MetricsCapture() as capture:
        assert capture is not None
        mock_tracer_factory.assert_called_once()
        mock_tracer.record_operation_start.assert_called_once()


def test_metrics_capture_exit(mock_tracer_factory):
    mock_tracer = mock.Mock()
    mock_tracer_factory.return_value = mock_tracer

    with MetricsCapture():
        pass

    mock_tracer.record_operation_completion.assert_called_once()
