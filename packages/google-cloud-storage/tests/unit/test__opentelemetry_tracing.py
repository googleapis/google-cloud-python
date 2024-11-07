# Copyright 2024 Google LLC
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

import importlib
import os
import pytest
import sys

import mock
from google.api_core.exceptions import GoogleAPICallError
from google.cloud.storage import __version__
from google.cloud.storage import _opentelemetry_tracing


@pytest.fixture
def setup():
    """Setup OTel packages and tracer provider."""
    try:
        from opentelemetry import trace as trace_api
        from opentelemetry.sdk.trace import TracerProvider, export
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
            InMemorySpanExporter,
        )
    except ImportError:  # pragma: NO COVER
        pytest.skip("This test suite requires OpenTelemetry pacakges.")

    tracer_provider = TracerProvider()
    memory_exporter = InMemorySpanExporter()
    span_processor = export.SimpleSpanProcessor(memory_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace_api.set_tracer_provider(tracer_provider)
    importlib.reload(_opentelemetry_tracing)
    yield memory_exporter


@pytest.fixture()
def mock_os_environ(monkeypatch):
    """Mock os.environ."""
    monkeypatch.setattr(os, "environ", {})
    return os.environ


@pytest.fixture()
def setup_optin(mock_os_environ):
    """Mock envar to opt-in tracing for storage client."""
    mock_os_environ["ENABLE_GCS_PYTHON_CLIENT_OTEL_TRACES"] = True
    importlib.reload(_opentelemetry_tracing)


def test_opentelemetry_not_installed(setup, monkeypatch):
    monkeypatch.setitem(sys.modules, "opentelemetry", None)
    importlib.reload(_opentelemetry_tracing)
    # Test no-ops when OpenTelemetry is not installed.
    with _opentelemetry_tracing.create_trace_span("No-ops w/o opentelemetry") as span:
        assert span is None
    assert not _opentelemetry_tracing.HAS_OPENTELEMETRY


def test_opentelemetry_no_trace_optin(setup):
    assert _opentelemetry_tracing.HAS_OPENTELEMETRY
    assert not _opentelemetry_tracing.enable_otel_traces
    # Test no-ops when user has not opt-in.
    # This prevents customers accidentally being billed for tracing.
    with _opentelemetry_tracing.create_trace_span("No-ops w/o opt-in") as span:
        assert span is None


def test_enable_trace_yield_span(setup, setup_optin):
    assert _opentelemetry_tracing.HAS_OPENTELEMETRY
    assert _opentelemetry_tracing.enable_otel_traces
    with _opentelemetry_tracing.create_trace_span("No-ops for opentelemetry") as span:
        assert span is not None


def test_enable_trace_call(setup, setup_optin):
    from opentelemetry import trace as trace_api

    extra_attributes = {
        "attribute1": "value1",
    }
    expected_attributes = _opentelemetry_tracing._default_attributes.copy()
    expected_attributes.update(_opentelemetry_tracing._cloud_trace_adoption_attrs)
    expected_attributes.update(extra_attributes)

    with _opentelemetry_tracing.create_trace_span(
        "OtelTracing.Test", attributes=extra_attributes
    ) as span:
        span.set_attribute("after_setup_attribute", 1)

        expected_attributes["after_setup_attribute"] = 1

        assert span.kind == trace_api.SpanKind.CLIENT
        assert span.attributes == expected_attributes
        assert span.name == "OtelTracing.Test"


def test_enable_trace_error(setup, setup_optin):
    from opentelemetry import trace as trace_api

    extra_attributes = {
        "attribute1": "value1",
    }
    expected_attributes = _opentelemetry_tracing._default_attributes.copy()
    expected_attributes.update(_opentelemetry_tracing._cloud_trace_adoption_attrs)
    expected_attributes.update(extra_attributes)

    with pytest.raises(GoogleAPICallError):
        with _opentelemetry_tracing.create_trace_span(
            "OtelTracing.Test", attributes=extra_attributes
        ) as span:
            from google.cloud.exceptions import NotFound

            assert span.kind == trace_api.SpanKind.CLIENT
            assert span.attributes == expected_attributes
            assert span.name == "OtelTracing.Test"
            raise NotFound("Test catching NotFound error in trace span.")


def test_get_final_attributes(setup, setup_optin):
    from google.api_core import retry as api_retry

    test_span_name = "OtelTracing.Test"
    test_span_attributes = {
        "foo": "bar",
    }
    api_request = {
        "method": "GET",
        "path": "/foo/bar/baz",
        "timeout": (100, 100),
    }
    retry_obj = api_retry.Retry()

    expected_attributes = {
        "foo": "bar",
        "rpc.service": "CloudStorage",
        "rpc.system": "http",
        "user_agent.original": f"gcloud-python/{__version__}",
        "http.request.method": "GET",
        "url.full": "https://testOtel.org/foo/bar/baz",
        "connect_timeout,read_timeout": (100, 100),
        "retry": f"multiplier{retry_obj._multiplier}/deadline{retry_obj._deadline}/max{retry_obj._maximum}/initial{retry_obj._initial}/predicate{retry_obj._predicate}",
    }
    expected_attributes.update(_opentelemetry_tracing._cloud_trace_adoption_attrs)

    with mock.patch("google.cloud.storage.client.Client") as test_client:
        test_client.project = "test_project"
        test_client._connection.API_BASE_URL = "https://testOtel.org"
        with _opentelemetry_tracing.create_trace_span(
            test_span_name,
            attributes=test_span_attributes,
            client=test_client,
            api_request=api_request,
            retry=retry_obj,
        ) as span:
            assert span is not None
            assert span.name == test_span_name
            assert span.attributes == expected_attributes


def test_set_conditional_retry_attr(setup, setup_optin):
    from google.api_core import retry as api_retry
    from google.cloud.storage.retry import ConditionalRetryPolicy

    test_span_name = "OtelTracing.Test"
    retry_policy = api_retry.Retry()
    conditional_predicate = mock.Mock()
    required_kwargs = ("kwarg",)
    retry_obj = ConditionalRetryPolicy(
        retry_policy, conditional_predicate, required_kwargs
    )

    retry_attrs = {
        "retry": f"multiplier{retry_policy._multiplier}/deadline{retry_policy._deadline}/max{retry_policy._maximum}/initial{retry_policy._initial}/predicate{conditional_predicate}",
    }
    expected_attributes = _opentelemetry_tracing._default_attributes.copy()
    expected_attributes.update(_opentelemetry_tracing._cloud_trace_adoption_attrs)
    expected_attributes.update(retry_attrs)

    with _opentelemetry_tracing.create_trace_span(
        test_span_name,
        retry=retry_obj,
    ) as span:
        assert span is not None
        assert span.name == test_span_name
        assert span.attributes == expected_attributes


def test_set_api_request_attr():
    from google.cloud.storage import Client

    test_client = Client()
    args_method = {"method": "GET"}
    expected_attributes = {"http.request.method": "GET"}
    attr = _opentelemetry_tracing._set_api_request_attr(args_method, test_client)
    assert attr == expected_attributes

    args_path = {"path": "/foo/bar/baz"}
    expected_attributes = {"url.full": "https://storage.googleapis.com/foo/bar/baz"}
    attr = _opentelemetry_tracing._set_api_request_attr(args_path, test_client)
    assert attr == expected_attributes

    args_timeout = {"timeout": (100, 100)}
    expected_attributes = {
        "connect_timeout,read_timeout": (100, 100),
    }
    attr = _opentelemetry_tracing._set_api_request_attr(args_timeout, test_client)
    assert attr == expected_attributes
