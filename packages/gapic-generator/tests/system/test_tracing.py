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
from google.showcase import EchoClient

from .conftest import construct_client


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
    """Verifies that default client options emit zero spans (zero overhead guarantee)."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    client = construct_client(
        EchoClient,
        use_mtls,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    response = client.echo(showcase.EchoRequest(content="no tracing"))
    assert response.content == "no tracing"

    # Zero spans must be emitted when tracing is disabled
    assert len(exporter.get_finished_spans()) == 0


def test_custom_tracer_provider(use_mtls):
    """Verifies that spans are emitted exclusively to the injected custom TracerProvider."""
    custom_exporter = InMemorySpanExporter()
    custom_provider = TracerProvider()
    custom_provider.add_span_processor(SimpleSpanProcessor(custom_exporter))

    other_exporter = InMemorySpanExporter()
    other_provider = TracerProvider()
    other_provider.add_span_processor(SimpleSpanProcessor(other_exporter))

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
    assert len(other_exporter.get_finished_spans()) == 0


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
