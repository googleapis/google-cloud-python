# Copyright 2026 Google LLC
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

"""Tests for OpenTelemetry Tracing Interceptors."""

from unittest.mock import MagicMock, Mock

import pytest

has_deps = True
try:
    import grpc  # noqa: F401
    from opentelemetry import trace  # noqa: F401
except ImportError:
    has_deps = False

pytestmark = pytest.mark.skipif(
    not has_deps, reason="Skipping gRPC/OTel tests because dependencies are missing"
)


class MockClientCallDetails:
    def __init__(
        self,
        method="/google.cloud.secretmanager.v1.SecretManagerService/AccessSecretVersion",
    ):
        self.method = method
        self.timeout = None
        self.metadata = []
        self.credentials = None
        self.wait_for_ready = None


@pytest.fixture
def mock_tracer(mocker):
    """Mocks tracer and start_as_current_span context manager."""
    mock_tracer_obj = MagicMock()
    mock_span_obj = MagicMock()

    # Configure start_as_current_span to act as a context manager returning mock_span_obj
    mock_cm = MagicMock()
    mock_cm.__enter__.return_value = mock_span_obj
    mock_tracer_obj.start_as_current_span.return_value = mock_cm

    mocker.patch("opentelemetry.trace.get_tracer", return_value=mock_tracer_obj)
    return mock_tracer_obj, mock_span_obj


def test_interceptor_creates_span(mock_tracer, monkeypatch):
    """F1.7 (Partial): Verifies that the interceptor creates a CLIENT span with the correct name."""
    from google.api_core.observability.tracing import OtelUnaryClientInterceptor

    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    mock_tracer_obj, mock_span_obj = mock_tracer
    mock_span_obj.is_recording.return_value = True

    interceptor = OtelUnaryClientInterceptor()

    continuation = Mock(return_value="response")
    details = MockClientCallDetails(method="/MyService/MyMethod")
    request = "request_payload"

    res = interceptor.intercept_unary_unary(continuation, details, request)

    assert res == "response"

    # Verify span creation
    mock_tracer_obj.start_as_current_span.assert_called_once_with(
        "/MyService/MyMethod", kind=trace.SpanKind.CLIENT
    )

    # Verify continuation was called
    continuation.assert_called_once_with(details, request)


def test_interceptor_disabled(mock_tracer, monkeypatch):
    """F1.6: Verifies that the interceptor does NOT create a span if disabled."""
    from google.api_core.observability.tracing import OtelUnaryClientInterceptor

    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "false")

    mock_tracer_obj, _ = mock_tracer

    interceptor = OtelUnaryClientInterceptor()

    continuation = Mock(return_value="response")
    details = MockClientCallDetails()
    request = "request_payload"

    res = interceptor.intercept_unary_unary(continuation, details, request)

    assert res == "response"

    # Verify NO span creation
    mock_tracer_obj.start_as_current_span.assert_not_called()

    # Verify continuation was called
    continuation.assert_called_once_with(details, request)


def test_interceptor_adds_static_attributes(mock_tracer, monkeypatch):
    """Verifies that static attributes are added to the span."""
    from google.api_core.observability.tracing import OtelUnaryClientInterceptor

    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    mock_tracer_obj, mock_span_obj = mock_tracer
    mock_span_obj.is_recording.return_value = True

    static_attrs = {"gcp.client.repo": "googleapis/google-cloud-python"}
    interceptor = OtelUnaryClientInterceptor(static_attributes=static_attrs)

    continuation = Mock(return_value="response")
    details = MockClientCallDetails()
    request = "request_payload"

    interceptor.intercept_unary_unary(continuation, details, request)

    # Verify attributes set
    mock_span_obj.set_attribute.assert_any_call(
        "gcp.client.repo", "googleapis/google-cloud-python"
    )
    mock_span_obj.set_attribute.assert_any_call("rpc.system.name", "grpc")


def test_interceptor_non_recording_span(mock_tracer, monkeypatch):
    """Verifies that non-recording spans skip attribute injection."""
    from google.api_core.observability.tracing import OtelUnaryClientInterceptor

    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    mock_tracer_obj, mock_span_obj = mock_tracer
    mock_span_obj.is_recording.return_value = False

    static_attrs = {"static.key": "static.val"}
    interceptor = OtelUnaryClientInterceptor(static_attributes=static_attrs)

    continuation = Mock(return_value="response")
    details = MockClientCallDetails()
    request = "request_payload"

    interceptor.intercept_unary_unary(continuation, details, request)

    # Verify set_attribute was NOT called
    mock_span_obj.set_attribute.assert_not_called()


@pytest.mark.parametrize(
    "metadata,expected_destination_id",
    [
        # Case A: Success with 'name'
        (
            [
                (
                    "x-goog-request-params",
                    "name=projects/my-project/secrets/my-secret/versions/1&other=val",
                )
            ],
            "projects/my-project/secrets/my-secret/versions/1",
        ),
        # Case B: Success with 'parent'
        (
            [
                (
                    "x-goog-request-params",
                    "parent=projects/my-project/locations/us-central1&other=val",
                )
            ],
            "projects/my-project/locations/us-central1",
        ),
        # Case C: Other metadata keys (Loop continues, no destination id)
        ([("some-other-header", "value")], None),
        # Case D: x-goog-request-params exists but no name/parent
        ([("x-goog-request-params", "other=val")], None),
        # Case E: Malformed x-goog-request-params (Exception caught, fails open)
        ([("x-goog-request-params", "name=foo=bar")], None),
    ],
)
def test_interceptor_metadata_parsing(
    mock_tracer, monkeypatch, metadata, expected_destination_id
):
    """F1.7 (Partial): Verifies metadata parsing scenarios, including success, missing keys, and malformed data."""
    from google.api_core.observability.tracing import OtelUnaryClientInterceptor

    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    mock_tracer_obj, mock_span_obj = mock_tracer
    mock_span_obj.is_recording.return_value = True

    interceptor = OtelUnaryClientInterceptor()

    continuation = Mock(return_value="response")
    details = MockClientCallDetails()
    details.metadata = metadata
    request = "request_payload"

    interceptor.intercept_unary_unary(continuation, details, request)

    if expected_destination_id:
        mock_span_obj.set_attribute.assert_any_call(
            "gcp.resource.destination.id", expected_destination_id
        )
    else:
        # Verify gcp.resource.destination.id was NOT called
        called_keys = [
            call[0][0] for call in mock_span_obj.set_attribute.call_args_list
        ]
        assert "gcp.resource.destination.id" not in called_keys
