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

"""Tests for OpenTelemetry gRPC interceptor integration in google-api-core."""

import sys
import types
from concurrent import futures
from unittest import mock

import pytest

try:
    import grpc
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)

from google.api_core import grpc_helpers


class GenericEchoHandler(grpc.GenericRpcHandler):
    """
    A generic handler that routes low-level gRPC calls without requiring
    compiled protobuf stubs.
    """

    def service(self, handler_call_details):
        if handler_call_details.method == "/DummyService/Echo":
            # Return a simple Unary-Unary handler that echoes back the request
            return grpc.unary_unary_rpc_method_handler(
                lambda request, context: request,  # Echo logic
                request_deserializer=lambda x: x,  # Pass raw bytes through
                response_serializer=lambda x: x,  # Pass raw bytes through
            )
        elif handler_call_details.method == "/DummyService/Error":
            def error_behavior(request, context):
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Intentional test error")
                return b""
            return grpc.unary_unary_rpc_method_handler(
                error_behavior,
                request_deserializer=lambda x: x,
                response_serializer=lambda x: x,
            )
        return None


@pytest.fixture(scope="module")
def local_grpc_server():
    """Starts a local generic gRPC server on an open port."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    server.add_generic_rpc_handlers((GenericEchoHandler(),))

    # Bind to an ephemeral port (port 0 lets the OS assign one)
    port = server.add_insecure_port("localhost:0")
    server.start()

    yield f"localhost:{port}"

    server.stop(None)


@pytest.fixture
def mock_otel_grpc(monkeypatch):
    """Fixture to mock OpenTelemetry gRPC hierarchy."""
    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock()
    mock_otel_grpc.client_interceptor.return_value = mock_interceptor

    modules = {
        "opentelemetry": mock_otel,
        "opentelemetry.instrumentation": mock_otel.instrumentation,
        "opentelemetry.instrumentation.grpc": mock_otel_grpc,
    }

    for name, mod in modules.items():
        monkeypatch.setitem(sys.modules, name, mod)

    return mock_otel_grpc


@pytest.mark.parametrize(
    "is_otel_installed, tracing_env_var_value, expect_otel_interceptor",
    [
        pytest.param(True, "true", True, id="installed_and_enabled"),
        pytest.param(True, "false", False, id="installed_but_disabled"),
        pytest.param(False, "true", False, id="not_installed_fails_open"),
    ],
)
def test_create_channel_otel_combos(
    monkeypatch,
    mock_otel_grpc,
    is_otel_installed,
    tracing_env_var_value,
    expect_otel_interceptor,
):
    """Verify create_channel behavior with various OTel installation and enablement states."""

    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", tracing_env_var_value)

    if not is_otel_installed:
        monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)

    mock_channel = "raw_channel"
    mock_otel_grpc.intercept_channel.side_effect = lambda ch, inc: f"wrapped_{ch}"

    with (
        mock.patch(
            "grpc.secure_channel", return_value=mock_channel
        ) as mock_secure_channel,
    ):
        with mock.patch(
            "google.api_core.grpc_helpers._create_composite_credentials",
            return_value=mock.Mock(),
        ):
            channel = grpc_helpers.create_channel("localhost:1234")

            # Always expect raw channel creation
            mock_secure_channel.assert_called_once()

            if expect_otel_interceptor:
                mock_otel_grpc.client_interceptor.assert_called_once()
                mock_otel_grpc.intercept_channel.assert_called_once_with(
                    mock_channel, mock_otel_grpc.client_interceptor.return_value
                )
                assert channel == f"wrapped_{mock_channel}"
            else:
                # OTel should NOT have been called
                mock_otel_grpc.intercept_channel.assert_not_called()
                assert channel == mock_channel


@pytest.mark.parametrize(
    "config_factory",
    [
        lambda tp: {"tracer_provider": tp},
        lambda tp: types.SimpleNamespace(tracer_provider=tp),
    ],
    ids=["dict", "object"],
)
def test_create_channel_with_custom_tracer_provider(
    monkeypatch, mock_otel_grpc, config_factory
):
    """Verify that create_channel passes custom tracer_provider to OTel interceptor."""

    mock_tracer_provider = mock.Mock()
    config = config_factory(mock_tracer_provider)

    mock_channel = "raw_channel"
    with (
        mock.patch("grpc.secure_channel", return_value=mock_channel),
    ):
        with mock.patch(
            "google.api_core.grpc_helpers._create_composite_credentials",
            return_value=mock.Mock(),
        ):
            grpc_helpers.create_channel("localhost:1234", configuration=config)

            mock_otel_grpc.client_interceptor.assert_called_once_with(
                tracer_provider=mock_tracer_provider
            )


@pytest.mark.parametrize(
    "config_factory",
    [
        lambda tp: {"tracer_provider": tp},
        lambda tp: types.SimpleNamespace(tracer_provider=tp),
    ],
    ids=["dict", "object"],
)
def test_otel_integration_with_fake_endpoint(local_grpc_server, monkeypatch, config_factory):
    """Verify OpenTelemetry integration with a real local gRPC server."""
    try:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
            InMemorySpanExporter,
        )
    except ImportError as e:
        pytest.skip(f"opentelemetry-sdk not installed or import failed: {e}")

    # A) Setup OpenTelemetry with an In-Memory Exporter
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    config = config_factory(provider)

    # B) Enable tracing via environment variable
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "True")

    # C) Mock secure_channel to return an insecure channel
    # This is needed because local_grpc_server is insecure but create_channel defaults to secure.
    def mock_secure(*args, **kwargs):
        return grpc.insecure_channel(args[0])

    monkeypatch.setattr(grpc, "secure_channel", mock_secure)

    # D) Call the code under test
    channel = grpc_helpers.create_channel(
        local_grpc_server, configuration=config
    )

    # E) Make a low-level generic call
    method_callable = channel.unary_unary(
        "/DummyService/Echo",
        request_serializer=lambda x: x,
        response_deserializer=lambda x: x,
    )

    payload = b"ping-test"
    response = method_callable(payload)

    # F) Assertions
    assert response == payload  # Server responded correctly

    spans = exporter.get_finished_spans()
    assert len(spans) > 0, "No spans were recorded by OpenTelemetry!"

    span_names = [s.name for s in spans]
    assert any("DummyService" in name for name in span_names)


def test_otel_integration_with_fake_endpoint_error(local_grpc_server, monkeypatch):
    """Verify OpenTelemetry integration records errors correctly."""
    try:
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
            InMemorySpanExporter,
        )
    except ImportError as e:
        pytest.skip(f"opentelemetry-sdk not installed or import failed: {e}")

    # A) Setup OpenTelemetry with an In-Memory Exporter
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    # B) Enable tracing via environment variable
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "True")

    # C) Mock secure_channel to return an insecure channel
    def mock_secure(*args, **kwargs):
        return grpc.insecure_channel(args[0])

    monkeypatch.setattr(grpc, "secure_channel", mock_secure)

    # D) Call the code under test
    channel = grpc_helpers.create_channel(
        local_grpc_server, configuration={"tracer_provider": provider}
    )

    # E) Make a low-level generic call that triggers an error
    method_callable = channel.unary_unary(
        "/DummyService/Error",
        request_serializer=lambda x: x,
        response_deserializer=lambda x: x,
    )

    payload = b"ping-test"

    # Expect a gRPC error
    with pytest.raises(grpc.RpcError) as excinfo:
        method_callable(payload)

    # F) Assertions
    spans = exporter.get_finished_spans()
    assert len(spans) > 0, "No spans were recorded by OpenTelemetry!"

    # Verify that the span recorded the error
    # The exact way OTel records errors might vary by version, but status should be ERROR
    # or it should have error attributes.
    error_spans = [s for s in spans if not s.status.is_ok]
    assert len(error_spans) > 0, "No error spans recorded!"

    span = error_spans[0]
    assert "DummyService" in span.name
