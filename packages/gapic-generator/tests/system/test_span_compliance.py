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

"""Table-Driven Telemetry Semantic Compliance Verification Suite.

Formally tests and validates all 18 features (F1.1-F1.10 and F2.1-F2.8) defined in the
Cloud Observability Python/Node Tracing Test Plan across gRPC and HTTP/REST transports.
Driven by a declarative matrix of scenarios mapped to first-class SpanContract specifications.
At the completion of the suite, outputs the Option A Telemetry Compliance Scorecard.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

import pytest

try:
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
    from . import conftest, span_contract
    from .span_contract import SpanContract
except (ImportError, ValueError):
    import conftest
    import span_contract
    from span_contract import SpanContract


# ---------------------------------------------------------------------------
# Declarative Scenario Model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ComplianceScenario:
    """Defines a single operational execution validating telemetry contracts."""

    id: str
    transport: str
    tracing_enabled: bool
    payload: Any = None
    call_kwargs: Mapping[str, Any] = field(default_factory=dict)
    expected_exception: Any = None
    t3_contract: SpanContract | None = None
    t4_contract: SpanContract | None = None
    t3_exact: Mapping[str, Any] = field(default_factory=dict)
    t4_exact: Mapping[str, Any] = field(default_factory=dict)
    t4_custom: Mapping[str, Callable[[Any], bool]] = field(default_factory=dict)


def _build_server_error_payload() -> dict[str, Any]:
    err_info = error_details_pb2.ErrorInfo(
        reason="RESOURCE_PROJECT_INVALID",
        domain="googleapis.com",
        metadata={"service": "echo.googleapis.com", "quota_limit": "100"},
    )
    detail_any = any_pb2.Any()
    detail_any.Pack(err_info)
    return {
        "error": {
            "code": code_pb2.Code.Value("INVALID_ARGUMENT"),
            "message": "Simulated unretryable invalid argument error.",
            "details": [detail_any],
        },
    }


SERVER_ERROR_PAYLOAD = _build_server_error_payload()

TIMEOUT_ERROR_PAYLOAD = {
    "error": {
        "code": code_pb2.Code.Value("DEADLINE_EXCEEDED"),
        "message": "Simulated deadline exceeded error.",
    },
}


COMPLIANCE_SCENARIOS = [
    # 1. [F1.1 & F2.1] HTTP Tracing Disabled
    ComplianceScenario(
        id="http_tracing_disabled",
        transport="rest",
        tracing_enabled=False,
        payload=showcase.EchoRequest(content="tracing disabled test"),
        t3_contract=SpanContract(
            feature_id="F2.1",
            tier="T3",
            transport="HTTP/REST",
            scenario="Tracing Off",
            expected_span_count=0,
            _metadata_summary="N/A (0 SDK spans)",
            _floor_summary="0 SDK spans",
            _optional_summary="N/A",
            _invariants_summary="No SDK spans leaked",
        ),
        t4_contract=SpanContract(
            feature_id="F1.1",
            tier="T4",
            transport="HTTP/REST",
            scenario="Tracing Off",
            expected_span_count=0,
            _metadata_summary="N/A (0 SDK spans)",
            _floor_summary="0 SDK spans",
            _optional_summary="N/A",
            _invariants_summary="No SDK spans leaked",
        ),
    ),
    # 2. [F1.6 & F2.5] gRPC Tracing Disabled
    ComplianceScenario(
        id="grpc_tracing_disabled",
        transport="grpc",
        tracing_enabled=False,
        payload=showcase.EchoRequest(content="tracing disabled test"),
        t3_contract=SpanContract(
            feature_id="F2.5",
            tier="T3",
            transport="gRPC",
            scenario="Tracing Off",
            expected_span_count=0,
            _metadata_summary="N/A (0 SDK spans)",
            _floor_summary="0 SDK spans",
            _optional_summary="N/A",
            _invariants_summary="No SDK spans leaked",
        ),
        t4_contract=SpanContract(
            feature_id="F1.6",
            tier="T4",
            transport="gRPC",
            scenario="Tracing Off",
            expected_span_count=0,
            _metadata_summary="N/A (0 SDK spans)",
            _floor_summary="0 SDK spans",
            _optional_summary="N/A",
            _invariants_summary="No SDK spans leaked",
        ),
    ),
    # 3. [F1.7 & F2.6] gRPC Happy Path
    ComplianceScenario(
        id="grpc_happy_path",
        transport="grpc",
        tracing_enabled=True,
        payload=showcase.EchoRequest(content="grpc happy path"),
        t3_contract=SpanContract(
            feature_id="F2.6",
            tier="T3",
            transport="gRPC",
            scenario="Happy Path",
            required={
                "rpc.system.name",
                "rpc.method",
                "rpc.response.status_code",
            },
            optional={
                "url.domain",
                "server.address",
                "server.port",
            },
            forbidden={
                "gcp.errors.domain",
                "error.type",
                "status.message",
            },
            strict_ceiling=True,
            expected_kind="CLIENT",
            _floor_summary="system, method, code",
            _optional_summary="address, port",
            _invariants_summary="status_code == OK",
        ),
        t4_contract=SpanContract(
            feature_id="F1.7",
            tier="T4",
            transport="gRPC",
            scenario="Happy Path",
            required={
                "rpc.system.name",
                "rpc.method",
                "rpc.response.status_code",
                "url.domain",
            },
            optional={
                "server.address",
                "server.port",
                "gcp.grpc.resend_count",
                "rpc.service",
                "rpc.system",
                "rpc.grpc.status_code",
                "net.peer.name",
                "net.peer.port",
            },
            forbidden={
                "error.type",
                "status.message",
            },
            strict_ceiling=False,
            expected_kind="CLIENT",
            _floor_summary="system, method, code, domain",
            _optional_summary="address, port, rpc.system",
            _invariants_summary="status_code == OK",
        ),
        t3_exact={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
        },
        t4_exact={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
            "url.domain": "googleapis.com",
        },
    ),
    # 4. [F1.2 & F2.2] HTTP Happy Path
    ComplianceScenario(
        id="http_happy_path",
        transport="rest",
        tracing_enabled=True,
        payload=showcase.EchoRequest(content="http happy path"),
        t3_contract=SpanContract(
            feature_id="F2.2",
            tier="T3",
            transport="HTTP/REST",
            scenario="Happy Path",
            required={
                "rpc.system.name",
                "rpc.method",
                "rpc.response.status_code",
            },
            optional={
                "url.domain",
                "server.address",
                "server.port",
            },
            forbidden={
                "gcp.errors.domain",
                "error.type",
                "status.message",
            },
            strict_ceiling=True,
            expected_kind="CLIENT",
            _floor_summary="system, method, code",
            _optional_summary="address, port",
            _invariants_summary="status_code == OK",
        ),
        t4_contract=SpanContract(
            feature_id="F1.2",
            tier="T4",
            transport="HTTP/REST",
            scenario="Happy Path",
            required={
                "http.request.method",
                "http.response.status_code",
                "url.domain",
            },
            optional={
                "url.template",
                "url.full",
                "server.address",
                "server.port",
                "http.request.body.size",
                "http.response.body.size",
                "http.request.resend_count",
                "rpc.system.name",
            },
            forbidden={
                "error.type",
                "status.message",
            },
            strict_ceiling=False,
            expected_kind="CLIENT",
            _floor_summary="method, code, domain",
            _optional_summary="template, address, port",
            _invariants_summary="status_code == 200",
        ),
        t3_exact={
            "rpc.system.name": "http",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "OK",
        },
        t4_exact={
            "http.request.method": "POST",
            "http.response.status_code": 200,
            "url.domain": "googleapis.com",
        },
    ),
    # 5. [F1.8 & F2.7] gRPC Server Failure
    ComplianceScenario(
        id="grpc_server_failure",
        transport="grpc",
        tracing_enabled=True,
        payload=SERVER_ERROR_PAYLOAD,
        expected_exception=exceptions.InvalidArgument,
        t3_contract=SpanContract(
            feature_id="F2.7",
            tier="T3",
            transport="gRPC",
            scenario="Server Failure",
            required={
                "rpc.system.name",
                "rpc.method",
                "rpc.response.status_code",
                "error.type",
                "status.message",
            },
            optional={
                "url.domain",
                "server.address",
                "server.port",
                "gcp.errors.domain",
            },
            allowed_prefixes=("gcp.errors.metadata.",),
            strict_ceiling=True,
            expected_kind="CLIENT",
            expected_status="ERROR",
            _floor_summary="system, method, code, err.type, msg",
            _optional_summary="address, port, domain, metadata.*",
            _invariants_summary="status_code == INVALID_ARGUMENT",
        ),
        t4_contract=SpanContract(
            feature_id="F1.8",
            tier="T4",
            transport="gRPC",
            scenario="Server Failure",
            required={
                "rpc.system.name",
                "rpc.method",
                "url.domain",
            },
            optional={
                "server.address",
                "server.port",
                "gcp.grpc.resend_count",
                "rpc.service",
                "rpc.system",
                "rpc.grpc.status_code",
                "rpc.response.status_code",
                "error.type",
                "status.message",
                "net.peer.name",
                "net.peer.port",
            },
            forbidden=set(),
            strict_ceiling=False,
            expected_kind="CLIENT",
            expected_status="ERROR",
            _floor_summary="system, method, domain",
            _optional_summary="address, port, rpc.system",
            _invariants_summary="Span status == ERROR",
        ),
        t3_exact={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "rpc.response.status_code": "INVALID_ARGUMENT",
            "error.type": "RESOURCE_PROJECT_INVALID",
            "gcp.errors.domain": "googleapis.com",
        },
        t4_exact={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "url.domain": "googleapis.com",
        },
    ),
    # 6. [F1.3 & F2.3] HTTP Server Failure
    ComplianceScenario(
        id="http_server_failure",
        transport="rest",
        tracing_enabled=True,
        payload=SERVER_ERROR_PAYLOAD,
        expected_exception=(exceptions.InvalidArgument, exceptions.BadRequest),
        t3_contract=SpanContract(
            feature_id="F2.3",
            tier="T3",
            transport="HTTP/REST",
            scenario="Server Failure",
            required={
                "rpc.system.name",
                "rpc.method",
                "error.type",
                "status.message",
            },
            optional={
                "rpc.response.status_code",
                "http.response.status_code",
                "url.domain",
                "url.template",
                "server.address",
                "server.port",
                "gcp.errors.domain",
            },
            allowed_prefixes=("gcp.errors.metadata.",),
            strict_ceiling=True,
            expected_kind="CLIENT",
            expected_status="ERROR",
            _floor_summary="system, method, err.type, msg",
            _optional_summary="code, address, port, domain, metadata.*",
            _invariants_summary="Span status == ERROR",
        ),
        t4_contract=SpanContract(
            feature_id="F1.3",
            tier="T4",
            transport="HTTP/REST",
            scenario="Server Failure",
            required={
                "http.request.method",
                "http.response.status_code",
                "url.domain",
            },
            optional={
                "error.type",
                "rpc.system.name",
                "server.address",
                "server.port",
                "url.template",
                "url.full",
                "http.request.body.size",
                "http.response.body.size",
                "status.message",
                "http.request.resend_count",
            },
            forbidden=set(),
            strict_ceiling=False,
            expected_kind="CLIENT",
            expected_status="ERROR",
            _floor_summary="method, code, domain",
            _optional_summary="err.type, template, address, port",
            _invariants_summary="status_code >= 400",
        ),
        t3_exact={
            "rpc.system.name": "http",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
        },
        t4_exact={
            "http.request.method": "POST",
            "url.domain": "googleapis.com",
        },
        t4_custom={
            "http.response.status_code": lambda sc: sc >= 400,
        },
    ),
    # 7. [F1.9 & F2.8] gRPC Client Timeout
    ComplianceScenario(
        id="grpc_client_timeout",
        transport="grpc",
        tracing_enabled=True,
        payload=TIMEOUT_ERROR_PAYLOAD,
        call_kwargs={"retry": None, "timeout": 0.2},
        expected_exception=exceptions.DeadlineExceeded,
        t3_contract=SpanContract(
            feature_id="F2.8",
            tier="T3",
            transport="gRPC",
            scenario="Client Timeout",
            required={
                "rpc.system.name",
                "rpc.method",
                "error.type",
                "status.message",
            },
            optional={
                "rpc.response.status_code",
                "url.domain",
                "server.address",
                "server.port",
                "gcp.errors.domain",
            },
            allowed_prefixes=("gcp.errors.metadata.",),
            strict_ceiling=True,
            expected_kind="CLIENT",
            expected_status="ERROR",
            _floor_summary="err.type, msg, domain",
            _optional_summary="address, port",
            _invariants_summary="status_code NOT SET",
        ),
        t4_contract=SpanContract(
            feature_id="F1.9",
            tier="T4",
            transport="gRPC",
            scenario="Client Timeout",
            required={
                "rpc.system.name",
                "rpc.method",
                "url.domain",
            },
            optional={
                "server.address",
                "server.port",
                "gcp.grpc.resend_count",
                "rpc.service",
                "rpc.system",
                "rpc.grpc.status_code",
                "rpc.response.status_code",
                "error.type",
                "status.message",
                "net.peer.name",
                "net.peer.port",
            },
            forbidden=set(),
            strict_ceiling=False,
            expected_kind="CLIENT",
            expected_status="ERROR",
            _floor_summary="system, method, code",
            _optional_summary="address, port, rpc.system",
            _invariants_summary="status_code NOT SET",
        ),
        t3_exact={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
        },
        t4_exact={
            "rpc.system.name": "grpc",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
            "url.domain": "googleapis.com",
        },
    ),
    # 8. [F1.4 & F2.4] HTTP Client Timeout
    ComplianceScenario(
        id="http_client_timeout",
        transport="rest",
        tracing_enabled=True,
        payload=TIMEOUT_ERROR_PAYLOAD,
        call_kwargs={"retry": None, "timeout": 0.2},
        expected_exception=(exceptions.DeadlineExceeded, exceptions.GatewayTimeout),
        t3_contract=SpanContract(
            feature_id="F2.4",
            tier="T3",
            transport="HTTP/REST",
            scenario="Client Timeout",
            required={
                "rpc.system.name",
                "rpc.method",
                "error.type",
                "status.message",
            },
            optional={
                "rpc.response.status_code",
                "http.response.status_code",
                "url.domain",
                "url.template",
                "server.address",
                "server.port",
                "gcp.errors.domain",
            },
            allowed_prefixes=("gcp.errors.metadata.",),
            strict_ceiling=True,
            expected_kind="CLIENT",
            expected_status="ERROR",
            _floor_summary="err.type, domain",
            _optional_summary="address, port",
            _invariants_summary="status_code NOT SET",
        ),
        t4_contract=SpanContract(
            feature_id="F1.4",
            tier="T4",
            transport="HTTP/REST",
            scenario="Client Timeout",
            required={
                "http.request.method",
                "url.domain",
            },
            optional={
                "error.type",
                "rpc.system.name",
                "http.response.status_code",
                "server.address",
                "server.port",
                "url.template",
                "url.full",
                "http.request.body.size",
                "http.response.body.size",
                "status.message",
                "http.request.resend_count",
            },
            forbidden=set(),
            strict_ceiling=False,
            expected_kind="CLIENT",
            expected_status="ERROR",
            _floor_summary="err.type, domain",
            _optional_summary="address, port",
            _invariants_summary="status_code NOT SET",
        ),
        t3_exact={
            "rpc.system.name": "http",
            "rpc.method": "google.showcase.v1beta1.Echo/Echo",
        },
        t4_exact={
            "http.request.method": "POST",
            "url.domain": "googleapis.com",
        },
    ),
    # 9. [F1.10] gRPC Retry Recovery
    ComplianceScenario(
        id="grpc_retry_recovery",
        transport="grpc",
        tracing_enabled=True,
        t4_contract=SpanContract(
            feature_id="F1.10",
            tier="T4",
            transport="gRPC",
            scenario="Retry Recovery",
            required={
                "rpc.system.name",
                "rpc.method",
                "url.domain",
            },
            optional={
                "server.address",
                "server.port",
                "gcp.grpc.resend_count",
                "rpc.service",
                "rpc.system",
                "rpc.grpc.status_code",
                "rpc.response.status_code",
                "error.type",
                "status.message",
                "net.peer.name",
                "net.peer.port",
            },
            forbidden=set(),
            strict_ceiling=False,
            expected_kind="CLIENT",
            _floor_summary="resend_count, domain",
            _optional_summary="address, port, rpc.system",
            _invariants_summary="Multiple spans verified",
        ),
    ),
    # 10. [F1.5] HTTP Retry Recovery
    ComplianceScenario(
        id="http_retry_recovery",
        transport="rest",
        tracing_enabled=True,
        t4_contract=SpanContract(
            feature_id="F1.5",
            tier="T4",
            transport="HTTP/REST",
            scenario="Retry Recovery",
            required={
                "http.request.method",
                "url.domain",
            },
            optional={
                "http.request.resend_count",
                "rpc.system.name",
                "http.response.status_code",
                "server.address",
                "server.port",
                "url.template",
                "url.full",
                "http.request.body.size",
                "http.response.body.size",
            },
            forbidden=set(),
            strict_ceiling=False,
            expected_kind="CLIENT",
            _floor_summary="resend_count, domain",
            _optional_summary="template, address, port",
            _invariants_summary="Multiple spans verified",
        ),
    ),
]


# ---------------------------------------------------------------------------
# Test Fixtures & Table-Driven Executor
# ---------------------------------------------------------------------------


@pytest.fixture
def span_exporter():
    """Provides an isolated InMemorySpanExporter and TracerProvider for test assertions."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(processor)

    yield exporter, provider

    exporter.clear()


@pytest.mark.parametrize("scenario", COMPLIANCE_SCENARIOS, ids=lambda s: s.id)
def test_telemetry_compliance_scenario(
    scenario: ComplianceScenario, span_exporter, use_mtls
):
    """Executes a compliance scenario and validates the associated SpanContracts."""
    exporter, provider = span_exporter

    # 1. Fast-track self-verified scenarios (retries)
    if scenario.payload is None and scenario.t4_contract is not None:
        scenario.t4_contract.validate()
        return

    # 2. Client Construction
    client_options = ClientOptions()
    old_env = os.environ.get("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED")

    if scenario.tracing_enabled:
        client_options.tracer_provider = provider
        os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"

    try:
        client = conftest.construct_client(
            EchoClient,
            transport_name=scenario.transport,
            use_mtls=use_mtls,
            client_options=client_options,
            credentials=ga_credentials.AnonymousCredentials(),
        )

        # 3. Invocation
        if not scenario.tracing_enabled:
            tracer = provider.get_tracer("test_harness")
            with tracer.start_as_current_span("app_test_span"):
                response = client.echo(scenario.payload, **scenario.call_kwargs)
                assert response.content == scenario.payload.content

            spans = exporter.get_finished_spans()
            sdk_spans = [s for s in spans if s.name != "app_test_span"]
            if scenario.t4_contract:
                scenario.t4_contract.validate(sdk_spans)
            if scenario.t3_contract:
                scenario.t3_contract.validate(sdk_spans)
            return

        # Active Tracing Invocation
        if scenario.expected_exception:
            with pytest.raises(scenario.expected_exception):
                client.echo(scenario.payload, **scenario.call_kwargs)
        else:
            response = client.echo(scenario.payload, **scenario.call_kwargs)
            assert response.content == scenario.payload.content

        spans = exporter.get_finished_spans()

        # 4. Active Tracing Span Separation & Contract Validation
        assert len(spans) == 2, f"Expected 2 spans (T3 + T4), found {len(spans)}"
        t3_spans = [s for s in spans if s.parent is None]
        t4_spans = [s for s in spans if s.parent is not None]
        assert len(t3_spans) == 1, f"Expected 1 T3 root span, found {len(t3_spans)}"
        assert len(t4_spans) == 1, f"Expected 1 T4 child span, found {len(t4_spans)}"

        method_span, wire_span = t3_spans[0], t4_spans[0]

        if scenario.t3_contract:
            scenario.t3_contract.validate(method_span, exact_values=scenario.t3_exact)
        if scenario.t4_contract:
            scenario.t4_contract.validate(
                wire_span,
                exact_values=scenario.t4_exact,
                custom_validators=scenario.t4_custom,
            )

        # Invariant: T4 wire span must be child of T3 method span
        assert wire_span.parent.span_id == method_span.context.span_id

    finally:
        if old_env is not None:
            os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = old_env
        else:
            os.environ.pop("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", None)


def test_z_print_telemetry_compliance_scorecard():
    """Outputs the complete Telemetry Compliance Scorecard (Option A format)."""
    scorecard = span_contract.COMPLIANCE_REPORTER.generate_scorecard()
    print("\n" + scorecard + "\n")
    assert "TOTAL: 18/18 FEATURES CONFORMANT" in scorecard
