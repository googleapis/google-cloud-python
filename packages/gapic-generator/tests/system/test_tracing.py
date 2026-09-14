# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import os
from unittest import mock

import grpc
import pytest

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    HAS_OPENTELEMETRY = True
except ImportError:
    HAS_OPENTELEMETRY = False

if not HAS_OPENTELEMETRY:
    pytest.skip("OpenTelemetry is not installed", allow_module_level=True)

from google import showcase
from google.api_core import exceptions
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials
from google.rpc import code_pb2
from google.showcase import EchoAsyncClient, EchoClient

try:
    from .conftest import construct_client
except ImportError:
    from conftest import construct_client


@pytest.fixture
def span_exporter():
    """Provides an isolated InMemorySpanExporter and TracerProvider for test assertions."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(processor)

    yield exporter, provider

    exporter.clear()


@pytest.fixture
def otel_echo_client(span_exporter, use_mtls):
    """Constructs an EchoClient wired with an in-memory TracerProvider."""
    exporter, provider = span_exporter
    options = ClientOptions(
        tracing_enabled=True,
        tracer_provider=provider,
    )
    client = construct_client(
        EchoClient,
        use_mtls,
        client_options=options,
        credentials=ga_credentials.AnonymousCredentials(),
    )
    return client, exporter


@pytest.fixture
def otel_echo_async_client(span_exporter, use_mtls):
    """Constructs an EchoAsyncClient wired with an in-memory TracerProvider."""
    exporter, provider = span_exporter
    options = ClientOptions(
        tracing_enabled=True,
        tracer_provider=provider,
    )
    client = construct_client(
        EchoAsyncClient,
        use_mtls,
        transport_name="grpc_asyncio",
        client_options=options,
        credentials=ga_credentials.AnonymousCredentials(),
    )
    return client, exporter


def test_sync_unary_tracing(otel_echo_client):
    """Verifies that a synchronous unary RPC generates a trace span with expected attributes."""
    client, exporter = otel_echo_client

    response = client.echo(showcase.EchoRequest(content="hello world"))
    assert response.content == "hello world"

    spans = exporter.get_finished_spans()
    assert len(spans) == 1

    span = spans[0]
    assert span.name == "google.showcase.v1beta1.Echo/Echo"
    assert span.attributes.get("rpc.system.name") == "grpc"
    assert span.attributes.get("rpc.method") == "google.showcase.v1beta1.Echo/Echo"
    assert span.attributes.get("rpc.response.status_code") == "OK"
    assert span.attributes.get("url.domain") == "googleapis.com"
    assert span.kind == trace.SpanKind.CLIENT


def test_unary_retries_tracing(span_exporter, use_mtls):
    """Verifies that each attempt of a retried RPC generates a separate span."""
    exporter, provider = span_exporter
    options = ClientOptions(
        tracing_enabled=True,
        tracer_provider=provider,
    )
    client = construct_client(
        EchoClient,
        use_mtls,
        client_options=options,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Configure a custom retry policy with 2 attempts on DeadlineExceeded
    custom_retry = retries.Retry(
        predicate=retries.if_exception_type(exceptions.DeadlineExceeded),
        initial=0.05,
        maximum=0.1,
        multiplier=1.0,
        deadline=0.3,
    )

    with pytest.raises((exceptions.DeadlineExceeded, exceptions.RetryError)):
        client.echo(
            {
                "error": {
                    "code": code_pb2.Code.Value("DEADLINE_EXCEEDED"),
                    "message": "Simulated deadline exceeded error for retry testing.",
                },
            },
            retry=custom_retry,
        )

    spans = exporter.get_finished_spans()
    # At least two attempts should have been made and recorded
    assert len(spans) >= 2
    for span in spans:
        assert span.name == "google.showcase.v1beta1.Echo/Echo"
        assert span.attributes.get("rpc.system.name") == "grpc"
        assert span.attributes.get("rpc.method") == "google.showcase.v1beta1.Echo/Echo"
        # Non-successful attempt should not have rpc.response.status_code == "OK"
        assert span.attributes.get("rpc.response.status_code") != "OK"


def test_tracing_disabled_default(use_mtls):
    """Verifies that default client options emit zero spans (zero overhead guarantee).

    Ensures that configuring a `TracerProvider` in `ClientOptions` without explicitly
    enabling tracing (via `tracing_enabled=True` or the environment variable
    `GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED`) records zero spans and incurs
    no tracing overhead.

    An active `TracerProvider` with an in-memory exporter is passed to the client.
    The test executes an actual unary RPC and asserts that no finished spans are
    recorded.
    """
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    # Provide the provider, but leave tracing_enabled=False / unset
    options = ClientOptions(
        tracing_enabled=False,
        tracer_provider=provider,
    )
    client = construct_client(
        EchoClient,
        use_mtls,
        client_options=options,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    response = client.echo(showcase.EchoRequest(content="no tracing"))
    assert response.content == "no tracing"

    # Zero spans must be emitted when tracing is disabled
    assert len(exporter.get_finished_spans()) == 0


def test_custom_tracer_provider(use_mtls):
    """Verifies that spans are emitted exclusively to the injected custom TracerProvider.

    Ensures strict isolation of trace data: when a client is configured with a
    custom `TracerProvider`, generated RPC spans must be routed solely to that
    provider's exporters and never leak into the ambient/global `TracerProvider`.

    Configures an ambient global `TracerProvider` with `global_exporter`, while
    configuring the client with `custom_provider` and `custom_exporter`. After
    executing an RPC, the test asserts that `custom_exporter` captured the span
    while `global_exporter` recorded zero spans.
    """
    custom_exporter = InMemorySpanExporter()
    custom_provider = TracerProvider()
    custom_provider.add_span_processor(SimpleSpanProcessor(custom_exporter))

    global_exporter = InMemorySpanExporter()
    global_provider = TracerProvider()
    global_provider.add_span_processor(SimpleSpanProcessor(global_exporter))

    # Temporarily set the ambient global tracer provider
    original_provider = trace.get_tracer_provider()
    trace.set_tracer_provider(global_provider)
    try:
        options = ClientOptions(
            tracing_enabled=True,
            tracer_provider=custom_provider,
        )
        client = construct_client(
            EchoClient,
            use_mtls,
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )

        response = client.echo(showcase.EchoRequest(content="isolated trace"))
        assert response.content == "isolated trace"

        assert len(custom_exporter.get_finished_spans()) == 1
        assert len(global_exporter.get_finished_spans()) == 0
    finally:
        trace.set_tracer_provider(original_provider)


def test_direct_client_initialization_tracing(span_exporter):
    """Verifies end-to-end trace injection via direct EchoClient instantiation.

    Validates the template wiring in `client.py.j2` directly. In system test
    harnesses, `construct_client` often creates the transport instance manually,
    which bypasses `client.py`'s `if not transport_provided:` branch. This test
    instantiates `EchoClient(client_options=...)` directly to prove that the client
    resolves `_observability.get_otel_interceptor` and passes it to `EchoGrpcTransport`.

    Constructs `EchoClient` without a pre-instantiated transport. Patches
    `EchoGrpcTransport.create_channel` solely to target the local insecure Showcase
    endpoint (`localhost:7469`). Executes `client.echo()` and asserts span generation.
    """
    exporter, provider = span_exporter
    options = ClientOptions(
        tracing_enabled=True,
        tracer_provider=provider,
    )

    with mock.patch.object(
        EchoClient.get_transport_class("grpc"),
        "create_channel",
        side_effect=lambda host, **kwargs: grpc.insecure_channel("localhost:7469"),
    ):
        # Client constructs the transport and wires interceptors itself
        client = EchoClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )
        response = client.echo(showcase.EchoRequest(content="direct client wiring"))
        assert response.content == "direct client wiring"

        spans = exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].name == "google.showcase.v1beta1.Echo/Echo"
        assert spans[0].attributes.get("rpc.system.name") == "grpc"


def test_env_var_opt_in(span_exporter, use_mtls):
    """Verifies that setting the environment variable enables tracing without tracing_enabled=True."""
    exporter, provider = span_exporter

    options = ClientOptions(
        tracer_provider=provider,
    )

    env_patch = {
        "GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "true",
    }
    with mock.patch.dict(os.environ, env_patch):
        client = construct_client(
            EchoClient,
            use_mtls,
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )
        response = client.echo(showcase.EchoRequest(content="env opt in"))
        assert response.content == "env opt in"

        spans = exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].name == "google.showcase.v1beta1.Echo/Echo"


@pytest.fixture(autouse=True)
def set_event_loop():
    try:
        asyncio.get_running_loop()
        yield
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            yield
        finally:
            loop.close()
            asyncio.set_event_loop(None)


@pytest.mark.asyncio
async def test_async_unary_tracing(otel_echo_async_client):
    """Verifies that an asynchronous unary RPC generates a trace span with expected attributes."""
    client, exporter = otel_echo_async_client

    response = await client.echo(showcase.EchoRequest(content="hello async world"))
    assert response.content == "hello async world"

    spans = exporter.get_finished_spans()
    assert len(spans) == 1

    span = spans[0]
    assert span.name == "google.showcase.v1beta1.Echo/Echo"
    assert span.attributes.get("rpc.system.name") == "grpc"
    assert span.attributes.get("rpc.method") == "google.showcase.v1beta1.Echo/Echo"
    assert span.attributes.get("rpc.response.status_code") == "OK"
    assert span.attributes.get("url.domain") == "googleapis.com"
    assert span.kind == trace.SpanKind.CLIENT


@pytest.mark.asyncio
async def test_async_unary_retries_tracing(span_exporter, use_mtls):
    """Verifies that each attempt of a retried async RPC generates a separate span."""
    from google.api_core import retry_async as retries_async

    exporter, provider = span_exporter
    options = ClientOptions(
        tracing_enabled=True,
        tracer_provider=provider,
    )
    client = construct_client(
        EchoAsyncClient,
        use_mtls,
        transport_name="grpc_asyncio",
        client_options=options,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    custom_retry = retries_async.AsyncRetry(
        predicate=retries_async.if_exception_type(exceptions.DeadlineExceeded),
        initial=0.05,
        maximum=0.1,
        multiplier=1.0,
        deadline=0.3,
    )

    with pytest.raises((exceptions.DeadlineExceeded, exceptions.RetryError)):
        await client.echo(
            {
                "error": {
                    "code": code_pb2.Code.Value("DEADLINE_EXCEEDED"),
                    "message": "Simulated deadline exceeded error for async retry testing.",
                },
            },
            retry=custom_retry,
        )

    spans = exporter.get_finished_spans()
    assert len(spans) >= 2
    for span in spans:
        assert span.name == "google.showcase.v1beta1.Echo/Echo"
        assert span.attributes.get("rpc.system.name") == "grpc"
        assert span.attributes.get("rpc.method") == "google.showcase.v1beta1.Echo/Echo"
        assert span.attributes.get("rpc.response.status_code") != "OK"


@pytest.mark.asyncio
async def test_async_tracing_disabled_default(use_mtls):
    """Verifies that default async client options emit zero spans."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    options = ClientOptions(
        tracing_enabled=False,
        tracer_provider=provider,
    )
    client = construct_client(
        EchoAsyncClient,
        use_mtls,
        transport_name="grpc_asyncio",
        client_options=options,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    response = await client.echo(showcase.EchoRequest(content="no tracing"))
    assert response.content == "no tracing"
    assert len(exporter.get_finished_spans()) == 0


@pytest.mark.asyncio
async def test_async_custom_tracer_provider(use_mtls):
    """Verifies that async spans are emitted exclusively to the injected custom TracerProvider."""
    custom_exporter = InMemorySpanExporter()
    custom_provider = TracerProvider()
    custom_provider.add_span_processor(SimpleSpanProcessor(custom_exporter))

    global_exporter = InMemorySpanExporter()
    global_provider = TracerProvider()
    global_provider.add_span_processor(SimpleSpanProcessor(global_exporter))

    original_provider = trace.get_tracer_provider()
    trace.set_tracer_provider(global_provider)
    try:
        options = ClientOptions(
            tracing_enabled=True,
            tracer_provider=custom_provider,
        )
        client = construct_client(
            EchoAsyncClient,
            use_mtls,
            transport_name="grpc_asyncio",
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )

        response = await client.echo(
            showcase.EchoRequest(content="isolated async trace")
        )
        assert response.content == "isolated async trace"

        assert len(custom_exporter.get_finished_spans()) == 1
        assert len(global_exporter.get_finished_spans()) == 0
    finally:
        trace.set_tracer_provider(original_provider)


@pytest.mark.asyncio
async def test_async_direct_client_initialization_tracing(span_exporter):
    """Verifies end-to-end trace injection via direct EchoAsyncClient instantiation."""
    exporter, provider = span_exporter
    options = ClientOptions(
        tracing_enabled=True,
        tracer_provider=provider,
    )

    with mock.patch.object(
        EchoAsyncClient.get_transport_class("grpc_asyncio"),
        "create_channel",
        side_effect=lambda host, **kwargs: grpc.aio.insecure_channel("localhost:7469"),
    ):
        client = EchoAsyncClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )
        response = await client.echo(
            showcase.EchoRequest(content="direct async client wiring")
        )
        assert response.content == "direct async client wiring"

        spans = exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].name == "google.showcase.v1beta1.Echo/Echo"
        assert spans[0].attributes.get("rpc.system.name") == "grpc"


@pytest.mark.asyncio
async def test_async_env_var_opt_in(span_exporter, use_mtls):
    """Verifies that setting the environment variable enables async tracing without tracing_enabled=True."""
    exporter, provider = span_exporter

    options = ClientOptions(
        tracer_provider=provider,
    )

    env_patch = {
        "GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "true",
    }
    with mock.patch.dict(os.environ, env_patch):
        client = construct_client(
            EchoAsyncClient,
            use_mtls,
            transport_name="grpc_asyncio",
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )
        response = await client.echo(showcase.EchoRequest(content="env opt in async"))
        assert response.content == "env opt in async"

        spans = exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].name == "google.showcase.v1beta1.Echo/Echo"
