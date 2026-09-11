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

from unittest import mock

import pytest

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


def test_metrics_capture_reuse(mock_tracer_factory):
    mock_tracer = mock.Mock()
    mock_tracer_factory.return_value = mock_tracer

    capture = MetricsCapture()
    with capture:
        assert SpannerMetricsTracerFactory.get_current_tracer() is mock_tracer

    assert SpannerMetricsTracerFactory.get_current_tracer() is None
    assert capture._token is None

    # Reusing the same context manager instance must not raise an error
    with capture:
        assert SpannerMetricsTracerFactory.get_current_tracer() is mock_tracer

    assert SpannerMetricsTracerFactory.get_current_tracer() is None
    assert capture._token is None


def test_metrics_capture_disabled():
    SpannerMetricsTracerFactory(enabled=False)
    try:
        with MetricsCapture() as capture:
            assert capture is not None
            assert SpannerMetricsTracerFactory.get_current_tracer() is None
    finally:
        SpannerMetricsTracerFactory(enabled=True)


def test_metrics_capture_with_resource_info(mock_tracer_factory):
    mock_tracer = mock.Mock()
    mock_tracer_factory.return_value = mock_tracer

    resource_info = {
        "project": "test_p",
        "instance": "test_i",
        "database": "test_d",
    }
    with MetricsCapture(resource_info=resource_info):
        pass

    mock_tracer.set_project.assert_called_once_with("test_p")
    mock_tracer.set_instance.assert_called_once_with("test_i")
    mock_tracer.set_database.assert_called_once_with("test_d")


def test_metrics_capture_exit_without_token():
    capture = MetricsCapture()
    assert capture.__exit__(None, None, None) is False


def test_metrics_capture_with_partial_resource_info(mock_tracer_factory):
    mock_tracer = mock.Mock()
    mock_tracer_factory.return_value = mock_tracer
    with MetricsCapture(resource_info={"database": "only_db"}):
        pass
    mock_tracer.set_database.assert_called_once_with("only_db")
    mock_tracer.set_project.assert_not_called()
    mock_tracer.set_instance.assert_not_called()


def test_metrics_capture_factory_returns_none(mock_tracer_factory):
    mock_tracer_factory.return_value = None
    with MetricsCapture(resource_info={"project": "p"}):
        pass


def test_metrics_capture_with_project_and_instance_only(mock_tracer_factory):
    mock_tracer = mock.Mock()
    mock_tracer_factory.return_value = mock_tracer
    with MetricsCapture(resource_info={"project": "p", "instance": "i"}):
        pass
    mock_tracer.set_project.assert_called_once_with("p")
    mock_tracer.set_instance.assert_called_once_with("i")
    mock_tracer.set_database.assert_not_called()


def test_metrics_capture_exit_error_resets_token(mock_tracer_factory):
    mock_tracer = mock.Mock()
    mock_tracer.record_operation_completion.side_effect = RuntimeError(
        "Completion failure"
    )
    mock_tracer_factory.return_value = mock_tracer

    with pytest.raises(RuntimeError, match="Completion failure"):
        with MetricsCapture():
            assert SpannerMetricsTracerFactory.get_current_tracer() is mock_tracer

    # Verified: Token is cleanly reset even on exception
    assert SpannerMetricsTracerFactory.get_current_tracer() is None
