# -*- coding: utf-8 -*-
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
#

from concurrent import futures
from unittest import mock

import grpc
import pytest
from google.api_core import _observability
from google.api_core._feature_gating_helpers import FeatureGatingError
from google.auth.credentials import AnonymousCredentials

from google.cloud.secretmanager_v1 import (
    SecretManagerServiceAsyncClient,
    SecretManagerServiceClient,
)
from google.cloud.secretmanager_v1.services.secret_manager_service.transports.grpc import (
    SecretManagerServiceGrpcTransport,
)
from google.cloud.secretmanager_v1.services.secret_manager_service.transports.grpc_asyncio import (
    SecretManagerServiceGrpcAsyncIOTransport,
)

try:
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


class GenericHandler(grpc.GenericRpcHandler):
    """A generic gRPC handler that catches all methods and returns empty bytes."""

    def service(self, handler_call_details):
        return grpc.unary_unary_rpc_method_handler(
            lambda request, context: b"",  # Return empty bytes
            request_deserializer=lambda x: x,
            response_serializer=lambda x: x,
        )


@pytest.fixture(scope="module")
def fake_grpc_server():
    """Starts a local generic gRPC server on an open port."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    server.add_generic_rpc_handlers((GenericHandler(),))
    port = server.add_insecure_port("localhost:0")
    server.start()
    yield f"localhost:{port}"
    server.stop(None)


@pytest.fixture
def insecure_channel_patch(monkeypatch):
    """Mocks grpc.secure_channel and grpc.aio.secure_channel to return insecure channels for local testing."""
    monkeypatch.setattr(
        grpc,
        "secure_channel",
        lambda target, *args, **kwargs: grpc.insecure_channel(target),
    )
    if hasattr(grpc, "aio"):
        monkeypatch.setattr(
            grpc.aio,
            "secure_channel",
            lambda target, *args, **kwargs: grpc.aio.insecure_channel(target),
        )


@pytest.fixture
def otel_in_memory():
    """Sets up in-memory OTel exporting. Skips test if SDK is missing."""
    if not OTEL_AVAILABLE:
        pytest.skip("OpenTelemetry SDK not available")

    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    return provider, exporter


@pytest.mark.parametrize(
    "method_name, kwargs",
    [
        ("list_secrets", {"parent": "projects/test-project"}),
        ("get_secret", {"name": "projects/test-project/secrets/test-secret"}),
    ],
)
def test_otel_tracing_enabled(
    fake_grpc_server,
    insecure_channel_patch,
    otel_in_memory,
    monkeypatch,
    method_name,
    kwargs,
):
    """Verify that calling API methods on SecretManagerServiceClient generates spans
    when OpenTelemetry tracing is enabled.
    """
    provider, exporter = otel_in_memory

    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")

    client = SecretManagerServiceClient(
        transport="grpc",
        client_options={
            "api_endpoint": fake_grpc_server,
            "tracer_provider": provider,
        },
        credentials=AnonymousCredentials(),
    )

    method = getattr(client, method_name)
    try:
        method(**kwargs)
    except Exception as e:
        # GenericHandler returns empty bytes b"", which proto3 deserializes to default message.
        print(f"Call raised: {e}")

    spans = exporter.get_finished_spans()
    assert len(spans) > 0, "No spans recorded!"

    span_names = [s.name for s in spans]
    assert any("SecretManagerService" in name for name in span_names)

    # Validate standard OpenTelemetry gRPC span attributes
    span = spans[0]
    assert span.attributes.get("rpc.system") == "grpc"


def test_otel_tracing_disabled(
    fake_grpc_server,
    insecure_channel_patch,
    otel_in_memory,
    monkeypatch,
):
    """Verify that no spans are generated when tracing is disabled."""
    provider, exporter = otel_in_memory

    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")

    from opentelemetry import trace

    with mock.patch.object(trace, "get_tracer_provider", return_value=provider):
        client = SecretManagerServiceClient(
            transport="grpc",
            client_options={
                "api_endpoint": fake_grpc_server,
            },
            credentials=AnonymousCredentials(),
        )

        try:
            client.list_secrets(parent="projects/test-project")
        except Exception:
            pass

    spans = exporter.get_finished_spans()
    assert len(spans) == 0, (
        f"Spans were recorded but tracing should be disabled! Spans: {[s.name for s in spans]}"
    )


def test_otel_tracing_feature_gating_error(
    fake_grpc_server,
    otel_in_memory,
    monkeypatch,
):
    """Verify that passing tracer_provider without the experimental environment variable
    raises FeatureGatingError (Fail Fast).
    """
    provider, _ = otel_in_memory
    monkeypatch.delenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", raising=False)

    with pytest.raises(
        FeatureGatingError,
        match="requires GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED",
    ):
        SecretManagerServiceClient(
            transport="grpc",
            client_options={
                "api_endpoint": fake_grpc_server,
                "tracer_provider": provider,
            },
            credentials=AnonymousCredentials(),
        )


def test_otel_tracing_custom_channel_with_wrappers(
    fake_grpc_server,
    otel_in_memory,
    monkeypatch,
):
    """Verify that when a custom channel is passed explicitly to the transport with wrappers,
    OpenTelemetry tracing wraps the custom channel and records spans.
    """
    provider, exporter = otel_in_memory
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")

    otel_wrapper = _observability.get_otel_channel_wrapper(
        {"tracer_provider": provider}
    )
    assert otel_wrapper is not None

    custom_channel = grpc.insecure_channel(fake_grpc_server)
    transport = SecretManagerServiceGrpcTransport(
        channel=custom_channel,
        wrappers=[otel_wrapper],
    )
    client = SecretManagerServiceClient(
        transport=transport,
    )

    try:
        client.list_secrets(parent="projects/test-project")
    except Exception:
        pass

    spans = exporter.get_finished_spans()
    assert len(spans) > 0, "No spans recorded on custom channel with OTel wrapper!"


def test_custom_interceptors_and_wrappers_execution(
    fake_grpc_server,
    insecure_channel_patch,
):
    """Verify that SecretManagerServiceGrpcTransport executes both gRPC ClientInterceptor instances
    and Callable[[Channel], Channel] wrappers on real RPC calls to a local server.
    """
    execution_order = []

    class TrackingInterceptor(grpc.UnaryUnaryClientInterceptor):
        def intercept_unary_unary(self, continuation, client_call_details, request):
            execution_order.append("interceptor")
            return continuation(client_call_details, request)

    def tracking_wrapper(ch: grpc.Channel) -> grpc.Channel:
        execution_order.append("wrapper")
        return ch

    interceptor = TrackingInterceptor()
    transport = SecretManagerServiceGrpcTransport(
        host=fake_grpc_server,
        wrappers=[interceptor, tracking_wrapper],
        credentials=AnonymousCredentials(),
    )
    client = SecretManagerServiceClient(
        transport=transport,
    )

    try:
        client.list_secrets(parent="projects/test-project")
    except Exception:
        pass

    assert "wrapper" in execution_order
    assert "interceptor" in execution_order


@pytest.mark.asyncio
async def test_otel_tracing_async_client(
    fake_grpc_server,
    insecure_channel_patch,
    otel_in_memory,
    monkeypatch,
):
    """Verify that OpenTelemetry async client interceptors record spans on async calls."""
    provider, exporter = otel_in_memory
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")

    async_interceptors = _observability.get_otel_async_interceptor(
        {"tracer_provider": provider}
    )
    assert async_interceptors is not None

    async_channel = grpc.aio.insecure_channel(
        fake_grpc_server,
        interceptors=async_interceptors,
    )
    transport = SecretManagerServiceGrpcAsyncIOTransport(channel=async_channel)
    client = SecretManagerServiceAsyncClient(
        transport=transport,
    )

    try:
        await client.list_secrets(parent="projects/test-project")
    except Exception:
        pass

    spans = exporter.get_finished_spans()
    assert len(spans) > 0, "No spans recorded on async client call!"
