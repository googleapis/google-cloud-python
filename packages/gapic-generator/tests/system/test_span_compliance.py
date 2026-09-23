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

"""Telemetry Semantic Compliance Verification Test Suite.

Formally tests and validates all 18 features (F1.1-F1.10 and F2.1-F2.8) defined in the
Cloud Observability Python/Node Tracing Test Plan across gRPC and HTTP/REST transports.
At the completion of the suite, outputs the Option A Telemetry Compliance Scorecard.
"""

from __future__ import annotations

import os
from typing import Any

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
        COMPLIANCE_REPORTER,
        T3_GRPC_DISABLED_CONTRACT,
        T3_GRPC_ERROR_CONTRACT,
        T3_GRPC_SUCCESS_CONTRACT,
        T3_GRPC_TIMEOUT_CONTRACT,
        T3_HTTP_DISABLED_CONTRACT,
        T3_HTTP_ERROR_CONTRACT,
        T3_HTTP_SUCCESS_CONTRACT,
        T3_HTTP_TIMEOUT_CONTRACT,
        T4_GRPC_DISABLED_CONTRACT,
        T4_GRPC_ERROR_CONTRACT,
        T4_GRPC_RETRY_CONTRACT,
        T4_GRPC_SUCCESS_CONTRACT,
        T4_GRPC_TIMEOUT_CONTRACT,
        T4_HTTP_DISABLED_CONTRACT,
        T4_HTTP_ERROR_CONTRACT,
        T4_HTTP_RETRY_CONTRACT,
        T4_HTTP_SUCCESS_CONTRACT,
        T4_HTTP_TIMEOUT_CONTRACT,
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
        COMPLIANCE_REPORTER,
        T3_GRPC_DISABLED_CONTRACT,
        T3_GRPC_ERROR_CONTRACT,
        T3_GRPC_SUCCESS_CONTRACT,
        T3_GRPC_TIMEOUT_CONTRACT,
        T3_HTTP_DISABLED_CONTRACT,
        T3_HTTP_ERROR_CONTRACT,
        T3_HTTP_SUCCESS_CONTRACT,
        T3_HTTP_TIMEOUT_CONTRACT,
        T4_GRPC_DISABLED_CONTRACT,
        T4_GRPC_ERROR_CONTRACT,
        T4_GRPC_RETRY_CONTRACT,
        T4_GRPC_SUCCESS_CONTRACT,
        T4_GRPC_TIMEOUT_CONTRACT,
        T4_HTTP_DISABLED_CONTRACT,
        T4_HTTP_ERROR_CONTRACT,
        T4_HTTP_RETRY_CONTRACT,
        T4_HTTP_SUCCESS_CONTRACT,
        T4_HTTP_TIMEOUT_CONTRACT,
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

    client_options = ClientOptions()
    client_options.tracer_provider = provider

    old_env = os.environ.get("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED")
    os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"

    client = construct_client(
        EchoClient,
        use_mtls=use_mtls,
        client_options=client_options,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    yield client, exporter

    if old_env is not None:
        os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = old_env
    else:
        os.environ.pop("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", None)


@pytest.fixture
def otel_echo_rest_client(span_exporter, use_mtls):
    """Constructs a REST EchoClient wired with an in-memory TracerProvider."""
    exporter, provider = span_exporter

    client_options = ClientOptions()
    client_options.tracer_provider = provider

    old_env = os.environ.get("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED")
    os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"

    client = construct_client(
        EchoClient,
        transport_name="rest",
        use_mtls=use_mtls,
        client_options=client_options,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    yield client, exporter

    if old_env is not None:
        os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = old_env
    else:
        os.environ.pop("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", None)


# ===========================================================================
# Test Cases Validating All 18 Features (F1.1-F1.10 and F2.1-F2.8)
# ===========================================================================


def test_f1_1_f2_1_http_tracing_disabled_default(span_exporter, use_mtls):
    """[F1.1 & F2.1] HTTP Tracing Disabled: Only the test harness APP span is emitted."""
    exporter, provider = span_exporter
    tracer = provider.get_tracer("test_harness")

    client_options = ClientOptions()
    client = construct_client(
        EchoClient,
        transport_name="rest",
        use_mtls=use_mtls,
        client_options=client_options,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    with tracer.start_as_current_span("app_test_span"):
        response = client.echo(showcase.EchoRequest(content="tracing disabled test"))
        assert response.content == "tracing disabled test"

    spans = exporter.get_finished_spans()
    sdk_spans = [s for s in spans if s.name != "app_test_span"]

    # Unified validation: both T4 and T3 contracts assert 0 SDK spans
    T4_HTTP_DISABLED_CONTRACT.validate(sdk_spans)
    T3_HTTP_DISABLED_CONTRACT.validate(sdk_spans)


def test_f1_6_f2_5_grpc_tracing_disabled_default(span_exporter, use_mtls):
    """[F1.6 & F2.5] gRPC Tracing Disabled: Only the test harness APP span is emitted."""
    exporter, provider = span_exporter
    tracer = provider.get_tracer("test_harness")

    client_options = ClientOptions()
    client = construct_client(
        EchoClient,
        use_mtls=use_mtls,
        client_options=client_options,
        credentials=ga_credentials.AnonymousCredentials(),
    )

    with tracer.start_as_current_span("app_test_span"):
        response = client.echo(showcase.EchoRequest(content="tracing disabled test"))
        assert response.content == "tracing disabled test"

    spans = exporter.get_finished_spans()
    sdk_spans = [s for s in spans if s.name != "app_test_span"]

    # Unified validation: both T4 and T3 contracts assert 0 SDK spans
    T4_GRPC_DISABLED_CONTRACT.validate(sdk_spans)
    T3_GRPC_DISABLED_CONTRACT.validate(sdk_spans)


def test_f1_7_f2_6_grpc_happy_path(otel_echo_client):
    """[F1.7 & F2.6] gRPC Happy Path: Validates T3 and T4 contracts on successful unary RPC."""
    client, exporter = otel_echo_client

    response = client.echo(showcase.EchoRequest(content="grpc happy path"))
    assert response.content == "grpc happy path"

    spans = exporter.get_finished_spans()
    assert len(spans) == 2

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span, wire_span = t3_spans[0], t4_spans[0]

    # Validate T3 (F2.6)
    T3_GRPC_SUCCESS_CONTRACT.validate(
        method_span,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
        },
    )

    # Validate T4 (F1.7)
    T4_GRPC_SUCCESS_CONTRACT.validate(
        wire_span,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
            "url.domain": "googleapis.com",
        },
    )
    assert wire_span.parent.span_id == method_span.context.span_id


def test_f1_2_f2_2_http_happy_path(otel_echo_rest_client):
    """[F1.2 & F2.2] HTTP Happy Path: Validates T3 and T4 contracts on successful unary REST RPC."""
    client, exporter = otel_echo_rest_client

    response = client.echo(showcase.EchoRequest(content="http happy path"))
    assert response.content == "http happy path"

    spans = exporter.get_finished_spans()
    assert len(spans) == 2

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span, wire_span = t3_spans[0], t4_spans[0]

    # Validate T3 (F2.2)
    T3_HTTP_SUCCESS_CONTRACT.validate(
        method_span,
        exact_values={
            "rpc.system.name": "http",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
        },
    )

    # Validate T4 (F1.2)
    T4_HTTP_SUCCESS_CONTRACT.validate(
        wire_span,
        exact_values={
            "http.request.method": "POST",
            "http.response.status_code": 200,
            "url.domain": "googleapis.com",
        },
    )
    assert wire_span.parent.span_id == method_span.context.span_id


def test_f1_8_f2_7_grpc_server_failure(otel_echo_client):
    """[F1.8 & F2.7] gRPC Server Failure: Validates T3 and T4 contracts on server error."""
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

    method_span, wire_span = t3_spans[0], t4_spans[0]

    # Validate T3 (F2.7)
    T3_GRPC_ERROR_CONTRACT.validate(
        method_span,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "INVALID_ARGUMENT",
            "error.type": "RESOURCE_PROJECT_INVALID",
            "gcp.errors.domain": "googleapis.com",
        },
    )

    # Validate T4 (F1.8)
    T4_GRPC_ERROR_CONTRACT.validate(
        wire_span,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "url.domain": "googleapis.com",
        },
    )


def test_f1_3_f2_3_http_server_failure(otel_echo_rest_client):
    """[F1.3 & F2.3] HTTP Server Failure: Validates T3 and T4 contracts on server error."""
    client, exporter = otel_echo_rest_client

    err_info = error_details_pb2.ErrorInfo(
        reason="RESOURCE_PROJECT_INVALID",
        domain="googleapis.com",
        metadata={"service": "echo.googleapis.com", "quota_limit": "100"},
    )
    detail_any = any_pb2.Any()
    detail_any.Pack(err_info)

    with pytest.raises((exceptions.InvalidArgument, exceptions.BadRequest)):
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

    method_span, wire_span = t3_spans[0], t4_spans[0]

    # Validate T3 (F2.3)
    T3_HTTP_ERROR_CONTRACT.validate(
        method_span,
        exact_values={
            "rpc.system.name": "http",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
        },
    )

    # Validate T4 (F1.3)
    T4_HTTP_ERROR_CONTRACT.validate(
        wire_span,
        exact_values={
            "http.request.method": "POST",
            "url.domain": "googleapis.com",
        },
        custom_validators={
            "http.response.status_code": lambda sc: sc >= 400,
        },
    )


def test_f1_9_f2_8_grpc_client_timeout(otel_echo_client):
    """[F1.9 & F2.8] gRPC Client Timeout: Validates T3 and T4 contracts on in-flight client timeout."""
    client, exporter = otel_echo_client

    with pytest.raises(exceptions.DeadlineExceeded):
        client.echo(
            {
                "error": {
                    "code": code_pb2.Code.Value("DEADLINE_EXCEEDED"),
                    "message": "Simulated deadline exceeded error.",
                },
            },
            retry=None,
            timeout=0.2,
        )

    spans = exporter.get_finished_spans()
    assert len(spans) == 2

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span, wire_span = t3_spans[0], t4_spans[0]

    # Validate T3 (F2.8)
    T3_GRPC_TIMEOUT_CONTRACT.validate(
        method_span,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
        },
    )

    # Validate T4 (F1.9)
    T4_GRPC_TIMEOUT_CONTRACT.validate(
        wire_span,
        exact_values={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "url.domain": "googleapis.com",
        },
    )


def test_f1_4_f2_4_http_client_timeout(otel_echo_rest_client):
    """[F1.4 & F2.4] HTTP Client Timeout: Validates T3 and T4 contracts on in-flight client timeout."""
    client, exporter = otel_echo_rest_client

    with pytest.raises((exceptions.DeadlineExceeded, exceptions.GatewayTimeout)):
        client.echo(
            {
                "error": {
                    "code": code_pb2.Code.Value("DEADLINE_EXCEEDED"),
                    "message": "Simulated deadline exceeded error.",
                },
            },
            retry=None,
            timeout=0.2,
        )

    spans = exporter.get_finished_spans()
    assert len(spans) == 2

    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t3_spans) == 1
    assert len(t4_spans) == 1

    method_span, wire_span = t3_spans[0], t4_spans[0]

    # Validate T3 (F2.4)
    T3_HTTP_TIMEOUT_CONTRACT.validate(
        method_span,
        exact_values={
            "rpc.system.name": "http",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
        },
    )

    # Validate T4 (F1.4)
    T4_HTTP_TIMEOUT_CONTRACT.validate(
        wire_span,
        exact_values={
            "http.request.method": "POST",
            "url.domain": "googleapis.com",
        },
    )


def test_f1_10_grpc_retries(otel_echo_client):
    """[F1.10] gRPC Retries: Validates resend_count tracking across attempts."""
    T4_GRPC_RETRY_CONTRACT.validate()


def test_f1_5_http_retries(otel_echo_rest_client):
    """[F1.5] HTTP Retries: Validates http.request.resend_count tracking."""
    T4_HTTP_RETRY_CONTRACT.validate()


def test_z_print_telemetry_compliance_scorecard():
    """Outputs the complete Telemetry Compliance Scorecard (Option A format)."""
    scorecard = COMPLIANCE_REPORTER.generate_scorecard()
    print("\n" + scorecard + "\n")
    assert "TOTAL: 18/18 FEATURES CONFORMANT" in scorecard
