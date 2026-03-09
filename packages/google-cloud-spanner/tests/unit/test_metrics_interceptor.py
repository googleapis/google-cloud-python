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
from google.cloud.spanner_v1.metrics.metrics_interceptor import MetricsInterceptor
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)
from unittest.mock import MagicMock


@pytest.fixture
def interceptor():
    SpannerMetricsTracerFactory(enabled=True)
    return MetricsInterceptor()


@pytest.fixture
def mock_tracer_ctx():
    tracer = MockMetricTracer()
    token = SpannerMetricsTracerFactory._current_metrics_tracer_ctx.set(tracer)
    yield tracer
    SpannerMetricsTracerFactory._current_metrics_tracer_ctx.reset(token)


class MockMetricTracer:
    def __init__(self):
        self.project = None
        self.instance = None
        self.database = None
        self.gfe_enabled = False
        self.record_attempt_start = MagicMock()
        self.record_attempt_completion = MagicMock()
        self.set_method = MagicMock()
        self.record_gfe_metrics = MagicMock()
        self.set_project = MagicMock()
        self.set_instance = MagicMock()
        self.set_database = MagicMock()
        self.client_attributes = {}


def test_parse_resource_path_valid(interceptor):
    path = "projects/my_project/instances/my_instance/databases/my_database"
    expected = {
        "project": "my_project",
        "instance": "my_instance",
        "database": "my_database",
    }
    assert interceptor._parse_resource_path(path) == expected


def test_parse_resource_path_invalid(interceptor):
    path = "invalid/path"
    expected = {}
    assert interceptor._parse_resource_path(path) == expected


def test_extract_resource_from_path(interceptor):
    metadata = [
        (
            "google-cloud-resource-prefix",
            "projects/my_project/instances/my_instance/databases/my_database",
        )
    ]
    expected = {
        "project": "my_project",
        "instance": "my_instance",
        "database": "my_database",
    }
    assert interceptor._extract_resource_from_path(metadata) == expected


def test_set_metrics_tracer_attributes(interceptor, mock_tracer_ctx):
    # mock_tracer_ctx fixture sets the ContextVar
    resources = {
        "project": "my_project",
        "instance": "my_instance",
        "database": "my_database",
    }

    interceptor._set_metrics_tracer_attributes(resources)
    mock_tracer_ctx.set_project.assert_called_with("my_project")
    mock_tracer_ctx.set_instance.assert_called_with("my_instance")
    mock_tracer_ctx.set_database.assert_called_with("my_database")


def test_intercept_with_tracer(interceptor, mock_tracer_ctx):
    # mock_tracer_ctx fixture sets the ContextVar
    mock_tracer_ctx.gfe_enabled = False

    invoked_response = MagicMock()
    invoked_response.initial_metadata.return_value = {}

    mock_invoked_method = MagicMock(return_value=invoked_response)
    call_details = MagicMock(
        method="spanner.someMethod",
        metadata=[
            (
                "google-cloud-resource-prefix",
                "projects/my_project/instances/my_instance/databases/my_database",
            )
        ],
    )

    response = interceptor.intercept(mock_invoked_method, "request", call_details)
    assert response == invoked_response
    mock_tracer_ctx.record_attempt_start.assert_called()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()
    mock_invoked_method.assert_called_once_with("request", call_details)
