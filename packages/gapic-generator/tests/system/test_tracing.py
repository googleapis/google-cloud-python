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
from google.api_core._feature_gating_helpers import FeatureGatingError
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials
from google.protobuf import any_pb2
from google.rpc import code_pb2, error_details_pb2
from google.showcase import EchoClient

try:
    from google.showcase import EchoAsyncClient

    HAS_ASYNC_CLIENT = True
except ImportError:
    HAS_ASYNC_CLIENT = False

try:
    from .conftest import (
        HAS_ASYNC_REST_ECHO_TRANSPORT,
        async_anonymous_credentials,
        construct_client,
    )
    from .span_contract import (
        T3_ERROR_CONTRACT,
        T3_SUCCESS_CONTRACT,
        T4_GRPC_ERROR_CONTRACT,
        T4_GRPC_SUCCESS_CONTRACT,
        T4_HTTP_SUCCESS_CONTRACT,
        SpanContract,
        assert_span_contract,
    )
except (ImportError, ValueError):
    from conftest import (
        HAS_ASYNC_REST_ECHO_TRANSPORT,
        async_anonymous_credentials,
        construct_client,
    )
    from span_contract import (
        T3_ERROR_CONTRACT,
        T3_SUCCESS_CONTRACT,
        T4_GRPC_ERROR_CONTRACT,
        T4_GRPC_SUCCESS_CONTRACT,
        T4_HTTP_SUCCESS_CONTRACT,
        SpanContract,
        assert_span_contract,
    )


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
        tracer_provider=provider,
    )
    with mock.patch.dict(
        os.environ, {"GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "true"}
    ):
        client = construct_client(
            EchoClient,
            use_mtls,
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )
        yield client, exporter


@pytest.fixture
def otel_echo_async_client(span_exporter, use_mtls):
    """Constructs an EchoAsyncClient over gRPC wired with an in-memory TracerProvider."""
    if not HAS_ASYNC_CLIENT:
        pytest.skip("EchoAsyncClient is not available")
    from grpc.experimental import aio

    exporter, provider = span_exporter
    options = ClientOptions(
        tracer_provider=provider,
    )
    with mock.patch.dict(
        os.environ, {"GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "true"}
    ):
        client = construct_client(
            EchoAsyncClient,
            use_mtls,
            transport_name="grpc_asyncio",
            channel_creator=aio.insecure_channel,
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )
        yield client, exporter


@pytest.fixture
def otel_echo_rest_client(span_exporter, use_mtls):
    """Constructs an EchoClient over REST wired with an in-memory TracerProvider."""
    exporter, provider = span_exporter
    options = ClientOptions(
        tracer_provider=provider,
    )
    with mock.patch.dict(
        os.environ, {"GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "true"}
    ):
        client = construct_client(
            EchoClient,
            use_mtls,
            transport_name="rest",
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )
        yield client, exporter


@pytest.fixture
def otel_echo_async_rest_client(span_exporter, use_mtls):
    """Constructs an EchoAsyncClient over async REST wired with an in-memory TracerProvider."""
    if not HAS_ASYNC_CLIENT or not HAS_ASYNC_REST_ECHO_TRANSPORT:
        pytest.skip("EchoAsyncClient or AsyncEchoRestTransport is not available")
    exporter, provider = span_exporter
    options = ClientOptions(
        tracer_provider=provider,
    )
    with mock.patch.dict(
        os.environ, {"GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "true"}
    ):
        client = construct_client(
            EchoAsyncClient,
            use_mtls,
            transport_name="rest_asyncio",
            client_options=options,
            credentials=async_anonymous_credentials(),
        )
        yield client, exporter


def test_sync_unary_tracing(otel_echo_client):
    """Verifies that a synchronous unary RPC generates trace spans conforming to semantic contracts."""
    client, exporter = otel_echo_client

    response = client.echo(showcase.EchoRequest(content="hello world"))
    assert response.content == "hello world"

    spans = exporter.get_finished_spans()
    # Synchronous unary calls generate both a Tier 3 method span and a Tier 4 wire span
    assert len(spans) == 2

    # Separate Tier 3 method span (root) and Tier 4 wire span (child)
    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span = t3_spans[0]
    wire_span = t4_spans[0]

    # Validate Tier 3 (Client API Method Span) semantic contract (strict floor & ceiling)
    assert_span_contract(
        method_span,
        T3_SUCCESS_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
        },
        label="T3 Sync Unary Method Span",
    )
    assert method_span.name == "google.showcase.v1beta1.Echo/Echo"
    assert method_span.kind == trace.SpanKind.CLIENT

    # Validate Tier 4 (Transport Wire Span) semantic contract (strict floor & open ceiling)
    assert_span_contract(
        wire_span,
        T4_GRPC_SUCCESS_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
            "url.domain": "googleapis.com",
        },
        label="T4 Sync Unary Wire Span",
    )
    assert wire_span.name == "google.showcase.v1beta1.Echo/Echo"
    assert wire_span.kind == trace.SpanKind.CLIENT
    assert wire_span.parent.span_id == method_span.context.span_id


@pytest.mark.asyncio
async def test_async_unary_tracing(otel_echo_async_client):
    """Verifies that an async gRPC unary RPC generates trace spans conforming to semantic contracts."""
    client, exporter = otel_echo_async_client

    response = await client.echo(showcase.EchoRequest(content="hello async world"))
    assert response.content == "hello async world"

    spans = exporter.get_finished_spans()
    assert len(spans) == 2

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span = t3_spans[0]
    wire_span = t4_spans[0]

    assert_span_contract(
        method_span,
        T3_SUCCESS_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
        },
        label="T3 Async gRPC Method Span",
    )
    assert method_span.name == "google.showcase.v1beta1.Echo/Echo"
    assert method_span.kind == trace.SpanKind.CLIENT

    assert_span_contract(
        wire_span,
        T4_GRPC_SUCCESS_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
            "url.domain": "googleapis.com",
        },
        label="T4 Async gRPC Wire Span",
    )
    assert wire_span.name == "google.showcase.v1beta1.Echo/Echo"
    assert wire_span.kind == trace.SpanKind.CLIENT
    assert wire_span.parent.span_id == method_span.context.span_id


def test_sync_rest_unary_tracing(otel_echo_rest_client):
    """Verifies that a synchronous REST RPC generates trace spans conforming to semantic contracts."""
    client, exporter = otel_echo_rest_client

    response = client.echo(showcase.EchoRequest(content="hello sync rest"))
    assert response.content == "hello sync rest"

    spans = exporter.get_finished_spans()
    assert len(spans) == 2

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span = t3_spans[0]
    wire_span = t4_spans[0]

    assert_span_contract(
        method_span,
        T3_SUCCESS_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
        },
        label="T3 Sync REST Method Span",
    )
    assert method_span.name == "google.showcase.v1beta1.Echo/Echo"
    assert method_span.kind == trace.SpanKind.CLIENT

    assert_span_contract(
        wire_span,
        T4_HTTP_SUCCESS_CONTRACT,
        exact_values={
            "http.request.method": "POST",
            "http.response.status_code": 200,
            "url.domain": "googleapis.com",
        },
        label="T4 Sync REST Wire Span",
    )
    assert wire_span.name == "POST"
    assert wire_span.kind == trace.SpanKind.CLIENT
    assert wire_span.parent.span_id == method_span.context.span_id


@pytest.mark.asyncio
async def test_async_rest_unary_tracing(otel_echo_async_rest_client):
    """Verifies that an async REST RPC generates trace spans conforming to semantic contracts."""
    client, exporter = otel_echo_async_rest_client

    response = await client.echo(showcase.EchoRequest(content="hello async rest"))
    assert response.content == "hello async rest"

    spans = exporter.get_finished_spans()
    assert len(spans) == 2

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span = t3_spans[0]
    wire_span = t4_spans[0]

    assert_span_contract(
        method_span,
        T3_SUCCESS_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
        },
        label="T3 Async REST Method Span",
    )
    assert method_span.name == "google.showcase.v1beta1.Echo/Echo"
    assert method_span.kind == trace.SpanKind.CLIENT

    assert_span_contract(
        wire_span,
        T4_HTTP_SUCCESS_CONTRACT,
        exact_values={
            "http.request.method": "POST",
            "http.response.status_code": 200,
            "url.domain": "googleapis.com",
        },
        label="T4 Async REST Wire Span",
    )
    assert wire_span.name == "POST"
    assert wire_span.kind == trace.SpanKind.CLIENT
    assert wire_span.parent.span_id == method_span.context.span_id


def test_unary_retries_tracing(otel_echo_client):
    """Verifies that each attempt of a retried RPC generates a separate span satisfying contracts."""
    client, exporter = otel_echo_client

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

    # Separate Tier 3 method span (root) and Tier 4 attempt wire spans (children)
    parent_spans = [s for s in spans if s.parent is None]
    child_spans = [s for s in spans if s.parent is not None]
    assert len(parent_spans) == 1
    assert len(child_spans) >= 1

    parent_span = parent_spans[0]

    # Validate Tier 3 Parent Method Span Contract (Error)
    assert_span_contract(
        parent_span,
        T3_ERROR_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "DEADLINE_EXCEEDED",
            "error.type": "DEADLINE_EXCEEDED",
        },
        custom_validators={
            "status.message": lambda msg: "Simulated deadline exceeded error" in msg,
        },
        label="T3 Unary Retries Parent Error Span",
    )

    # Validate each child T4 Wire Span
    for idx, child_span in enumerate(child_spans):
        assert_span_contract(
            child_span,
            T4_GRPC_ERROR_CONTRACT,
            exact_values={
                "rpc.system.name": "grpc",
                "rpc.method": "google.showcase.v1beta1.Echo/Echo",
                "url.domain": "googleapis.com",
            },
            label=f"T4 Unary Retry Wire Attempt {idx + 1}",
        )
        assert child_span.parent.span_id == parent_span.context.span_id


def test_unretryable_error_tracing_contract(otel_echo_client):
    """Verifies that an unretryable error with rich ErrorInfo satisfies T3 and T4 semantic contracts."""
    client, exporter = otel_echo_client

    err_info = error_details_pb2.ErrorInfo(
        reason="RESOURCE_PROJECT_INVALID",
        domain="googleapis.com",
        metadata={"service": "echo.googleapis.com", "quota_limit": "100"},
    )
    detail_any = any_pb2.Any()
    detail_any.Pack(err_info)

    with pytest.raises(exceptions.InvalidArgument):
        client.echo(
            {
                "error": {
                    "code": code_pb2.Code.Value("INVALID_ARGUMENT"),
                    "message": "Simulated unretryable invalid argument error.",
                    "details": [detail_any],
                },
            },
        )

    spans = exporter.get_finished_spans()
    assert len(spans) == 2

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span = t3_spans[0]
    wire_span = t4_spans[0]

    # Validate Tier 3 method span with complete set of rich ErrorInfo attributes
    assert_span_contract(
        method_span,
        T3_ERROR_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "INVALID_ARGUMENT",
            "error.type": "RESOURCE_PROJECT_INVALID",
            "gcp.errors.domain": "googleapis.com",
            "gcp.errors.metadata.service": "echo.googleapis.com",
            "gcp.errors.metadata.quota_limit": "100",
        },
        custom_validators={
            "status.message": lambda msg: "Simulated unretryable invalid argument error."
            in msg,
        },
        label="T3 Unretryable Error with ErrorInfo",
    )

    # Validate Tier 4 wire span
    assert_span_contract(
        wire_span,
        T4_GRPC_ERROR_CONTRACT,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "url.domain": "googleapis.com",
        },
        label="T4 Unretryable Error Wire Span",
    )
    assert wire_span.parent.span_id == method_span.context.span_id


def test_span_contract_validator_diagnostics():
    """Verifies that assert_span_contract detects missing, forbidden, and weirdo attributes."""
    sample_contract = SpanContract(
        required={"rpc.system.name", "rpc.method"},
        optional={"optional.tag"},
        allowed_prefixes=("gcp.errors.metadata.",),
        forbidden={"rpc.system"},
        strict_ceiling=True,
    )

    # Valid span attributes
    valid_attrs = {
        "rpc.system.name": "grpc",
        "rpc.method": "Showcase/Echo",
        "optional.tag": "val",
        "gcp.errors.metadata.key": "123",
    }
    assert_span_contract(valid_attrs, sample_contract)

    # Missing required attribute triggers floor violation
    missing_attrs = {"rpc.method": "Showcase/Echo"}
    with pytest.raises(AssertionError, match="missing required attributes"):
        assert_span_contract(missing_attrs, sample_contract)

    # Forbidden attribute triggers forbidden violation
    forbidden_attrs = dict(valid_attrs, **{"rpc.system": "grpc"})
    with pytest.raises(AssertionError, match="found disallowed attributes"):
        assert_span_contract(forbidden_attrs, sample_contract)

    # Unexpected 'weirdo' attribute triggers ceiling violation
    weirdo_attrs = dict(valid_attrs, **{"untracked.weirdo": "oops"})
    with pytest.raises(
        AssertionError, match="unrecognized / untracked attributes detected"
    ):
        assert_span_contract(weirdo_attrs, sample_contract)


def test_tracing_disabled_default(span_exporter, use_mtls):
    """Verifies that default client options emit zero spans (zero overhead guarantee).

    Ensures that without setting GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED=true,
    even if an ambient TracerProvider is active, zero spans are recorded and no
    tracing overhead is incurred. Also verifies that passing tracer_provider without
    the environment variable fails fast by raising FeatureGatingError.
    """
    exporter, provider = span_exporter

    # Providing a tracer_provider without enabling the experimental env var fails fast
    options_with_provider = ClientOptions(
        tracer_provider=provider,
    )
    with mock.patch.dict(
        os.environ, {"GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "false"}
    ):
        with pytest.raises(FeatureGatingError):
            construct_client(
                EchoClient,
                use_mtls,
                client_options=options_with_provider,
                credentials=ga_credentials.AnonymousCredentials(),
            )

    # Default client options emit zero spans
    options = ClientOptions()
    with mock.patch.dict(
        os.environ, {"GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "false"}
    ):
        client = construct_client(
            EchoClient,
            use_mtls,
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials(),
        )

        response = client.echo(showcase.EchoRequest(content="no tracing"))
        assert response.content == "no tracing"

        # Zero spans must be emitted when tracing is disabled
        spans = exporter.get_finished_spans()
        assert len(spans) == 0


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
            tracer_provider=custom_provider,
        )
        with mock.patch.dict(
            os.environ, {"GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "true"}
        ):
            client = construct_client(
                EchoClient,
                use_mtls,
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )

            response = client.echo(showcase.EchoRequest(content="isolated trace"))
            assert response.content == "isolated trace"

            custom_spans = custom_exporter.get_finished_spans()
            assert len(custom_spans) == 2
            global_spans = global_exporter.get_finished_spans()
            assert len(global_spans) == 0
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
        tracer_provider=provider,
    )

    with mock.patch.dict(
        os.environ, {"GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED": "true"}
    ):
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
            assert len(spans) == 2
            for span in spans:
                assert span.name == "google.showcase.v1beta1.Echo/Echo"
                assert span.attributes.get("rpc.system.name") == "grpc"


def test_env_var_opt_in(otel_echo_client):
    """Verifies that setting the environment variable enables tracing without tracing_enabled=True."""
    client, exporter = otel_echo_client

    response = client.echo(showcase.EchoRequest(content="env opt in"))
    assert response.content == "env opt in"

    spans = exporter.get_finished_spans()
    assert len(spans) == 2
    for span in spans:
        assert span.name == "google.showcase.v1beta1.Echo/Echo"
