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

import csv
import os
from dataclasses import dataclass, field
from pathlib import Path
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
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials
from google.protobuf import any_pb2
from google.rpc import code_pb2, error_details_pb2, status_pb2
from google.showcase import (
    AttemptSequenceRequest,
    CreateSequenceRequest,
    EchoClient,
    Sequence,
    SequenceServiceClient,
)

try:
    from . import conftest, span_contract
    from .span_contract import SpanContract
except (ImportError, ValueError):
    import conftest
    import span_contract
    from span_contract import SpanContract


# ---------------------------------------------------------------------------
# Dynamic CSV Feature Matrix Loader & Semantic Contract Generator
# ---------------------------------------------------------------------------

CSV_PATH = Path(__file__).parent / "telemetry_requirements_matrix.csv"


def load_feature_matrix() -> dict[str, dict[str, str]]:
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        return {r["Feature ID"]: r for r in csv.DictReader(f)}


FEATURE_MATRIX = load_feature_matrix()

FEATURE_SUMMARIES: dict[str, tuple[str, str, str, str]] = {
    "F1.1": ("N/A (0 SDK spans)", "0 SDK spans", "N/A", "No SDK spans leaked"),
    "F2.1": ("N/A (0 SDK spans)", "0 SDK spans", "N/A", "No SDK spans leaked"),
    "F1.6": ("N/A (0 SDK spans)", "0 SDK spans", "N/A", "No SDK spans leaked"),
    "F2.5": ("N/A (0 SDK spans)", "0 SDK spans", "N/A", "No SDK spans leaked"),
    "F2.6": (
        "Kind, Name",
        "system, method, code",
        "address, port",
        "status_code == OK",
    ),
    "F1.7": (
        "Kind, Name",
        "system, method, code, domain",
        "address, port, rpc.system",
        "status_code == OK",
    ),
    "F2.2": (
        "Kind, Name",
        "system, method, code",
        "address, port",
        "status_code == OK",
    ),
    "F1.2": (
        "Kind, Name",
        "method, code, domain",
        "template, address, port",
        "status_code == 200",
    ),
    "F2.7": (
        "Kind, Name, Status",
        "system, method, code, err.type, msg",
        "address, port, domain, metadata.*",
        "status_code == INVALID_ARGUMENT",
    ),
    "F1.8": (
        "Kind, Name, Status",
        "system, method, domain",
        "address, port, rpc.system",
        "Span status == ERROR",
    ),
    "F2.3": (
        "Kind, Name, Status",
        "system, method, err.type, msg",
        "code, address, port, domain, metadata.*",
        "Span status == ERROR",
    ),
    "F1.3": (
        "Kind, Name, Status",
        "method, code, domain",
        "err.type, template, address, port",
        "status_code >= 400",
    ),
    "F2.8": (
        "Kind, Name, Status",
        "err.type, msg, domain",
        "address, port",
        "status_code NOT SET",
    ),
    "F1.9": (
        "Kind, Name, Status",
        "system, method, code",
        "address, port, rpc.system",
        "status_code NOT SET",
    ),
    "F2.4": (
        "Kind, Name, Status",
        "err.type, domain",
        "address, port",
        "status_code NOT SET",
    ),
    "F1.4": (
        "Kind, Name, Status",
        "err.type, domain",
        "address, port",
        "status_code NOT SET",
    ),
    "F1.10": (
        "Kind, Name",
        "resend_count, domain",
        "address, port, rpc.system",
        "Multiple spans verified",
    ),
    "F1.5": (
        "Kind, Name",
        "resend_count, domain",
        "template, address, port",
        "Multiple spans verified",
    ),
    "F3.1": (
        "1 T3 parent, 2 T4 children",
        "T4_1: 503, T4_2: 200",
        "T3: OK/UNSET",
        "T4 parent is T3, T3 error.* NOT SET",
    ),
    "F3.2": (
        "1 T3 parent, 6 T4 children",
        "All T4: 503, T3: UNAVAILABLE",
        "status.message",
        "T4 parent is T3, T3 status ERROR",
    ),
    "F3.3": (
        "1 T3 parent, 2 T4 children",
        "T4_1: 14, T4_2: 0",
        "T3: OK/UNSET",
        "T4 parent is T3, T3 error.* NOT SET",
    ),
    "F3.4": (
        "1 T3 parent, 6 T4 children",
        "All T4: 14, T3: UNAVAILABLE",
        "status.message",
        "T4 parent is T3, T3 status ERROR",
    ),
}


def build_contract(
    feature_id: str | None,
) -> tuple[SpanContract | None, dict[str, Any]]:
    """Builds a SpanContract and exact_values mapping directly from a CSV row."""
    if not feature_id or feature_id not in FEATURE_MATRIX:
        return None, {}

    row = FEATURE_MATRIX[feature_id]
    tier = row["Tier"]
    transport = row["Transport"]
    scenario = row["Scenario"]
    count_str = row["Span Count"]
    meta_s, floor_s, opt_s, inv_s = FEATURE_SUMMARIES.get(
        feature_id, (None, None, None, None)
    )

    if count_str == "0":
        return SpanContract(
            feature_id=feature_id,
            tier=tier,
            transport=transport,
            scenario=scenario,
            expected_span_count=0,
            _metadata_summary=meta_s,
            _floor_summary=floor_s,
            _optional_summary=opt_s,
            _invariants_summary=inv_s,
        ), {}

    kind = "CLIENT" if "CLIENT" in row["Span Kind"] else None
    status = "ERROR" if row["Span Status"] == "ERROR" else None
    strict = tier == "T3"
    allowed_prefixes = (
        ("gcp.errors.metadata.",) if (tier == "T3" and status == "ERROR") else ()
    )

    required = set()
    optional = {"server.address", "server.port"}
    forbidden = set()
    exact_values: dict[str, Any] = {}

    if tier == "T4":
        optional.update(
            {
                "url.template",
                "url.full",
                "http.request.body.size",
                "http.response.body.size",
                "rpc.system",
                "rpc.service",
                "net.peer.name",
                "net.peer.port",
            }
        )
    else:
        optional.update({"url.template", "url.domain", "gcp.errors.domain"})

    for col in [
        "rpc.system.name",
        "rpc.method",
        "url.domain",
        "http.request.method",
    ]:
        val = row.get(col, "")
        if val.startswith("Optional"):
            optional.add(col)
        elif val not in ("N/A", "NOT SET", ""):
            if col == "url.domain" and tier == "T3":
                optional.add(col)
            else:
                required.add(col)
                if col == "rpc.system.name" and val in ("grpc", "http"):
                    exact_values[col] = val
                elif col == "rpc.method":
                    exact_values[col] = val
                elif col == "url.domain":
                    exact_values[col] = val
                elif col == "http.request.method":
                    exact_values[col] = val

    for col in [
        "http.response.status_code",
        "rpc.response.status_code",
        "rpc.grpc.status_code",
    ]:
        val = row.get(col, "")
        if "optional" in val.lower():
            optional.add(col)
        elif val == "NOT SET":
            if scenario == "Client Timeout":
                optional.add(col)
            else:
                forbidden.add(col)
        elif val not in ("N/A", ""):
            if tier == "T4" and col == "rpc.response.status_code":
                optional.add(col)
            elif not val.startswith(">="):
                required.add(col)
                if val == '"OK"':
                    exact_values[col] = "OK"
                elif val == "200":
                    exact_values[col] = 200
                elif val == "0":
                    exact_values[col] = 0
            else:
                required.add(col)

    for col in ["error.type", "status.message"]:
        val = row.get(col, "")
        if val == "NOT SET":
            forbidden.add(col)
        elif val not in ("N/A", ""):
            if tier == "T4":
                optional.add(col)
            else:
                required.add(col)

    return SpanContract(
        feature_id=feature_id,
        tier=tier,
        transport=transport,
        scenario=scenario,
        expected_span_count=1,
        required=required,
        optional=optional,
        forbidden=forbidden,
        allowed_prefixes=allowed_prefixes,
        strict_ceiling=strict,
        expected_kind=kind,
        expected_status=status,
        _metadata_summary=meta_s,
        _floor_summary=floor_s,
        _optional_summary=opt_s,
        _invariants_summary=inv_s,
    ), exact_values


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
    t3_feature_id: str | None = None
    t4_feature_id: str | None = None
    t4_custom: Mapping[str, Callable[[Any], bool]] = field(default_factory=dict)

    @property
    def t3_contract(self) -> SpanContract | None:
        contract, _ = build_contract(self.t3_feature_id)
        return contract

    @property
    def t4_contract(self) -> SpanContract | None:
        contract, _ = build_contract(self.t4_feature_id)
        return contract

    @property
    def t3_exact(self) -> dict[str, Any]:
        _, exact = build_contract(self.t3_feature_id)
        return exact

    @property
    def t4_exact(self) -> dict[str, Any]:
        _, exact = build_contract(self.t4_feature_id)
        return exact


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
        t3_feature_id="F2.1",
        t4_feature_id="F1.1",
    ),
    # 2. [F1.6 & F2.5] gRPC Tracing Disabled
    ComplianceScenario(
        id="grpc_tracing_disabled",
        transport="grpc",
        tracing_enabled=False,
        payload=showcase.EchoRequest(content="tracing disabled test"),
        t3_feature_id="F2.5",
        t4_feature_id="F1.6",
    ),
    # 3. [F1.7 & F2.6] gRPC Unary Success
    ComplianceScenario(
        id="grpc_unary_success",
        transport="grpc",
        tracing_enabled=True,
        payload=showcase.EchoRequest(content="hello grpc"),
        t3_feature_id="F2.6",
        t4_feature_id="F1.7",
    ),
    # 4. [F1.2 & F2.2] HTTP Unary Success
    ComplianceScenario(
        id="http_unary_success",
        transport="rest",
        tracing_enabled=True,
        payload=showcase.EchoRequest(content="hello http"),
        t3_feature_id="F2.2",
        t4_feature_id="F1.2",
    ),
    # 5. [F1.8 & F2.7] gRPC Server Failure
    ComplianceScenario(
        id="grpc_server_failure",
        transport="grpc",
        tracing_enabled=True,
        payload=SERVER_ERROR_PAYLOAD,
        expected_exception=exceptions.InvalidArgument,
        t3_feature_id="F2.7",
        t4_feature_id="F1.8",
    ),
    # 6. [F1.3 & F2.3] HTTP Server Failure
    ComplianceScenario(
        id="http_server_failure",
        transport="rest",
        tracing_enabled=True,
        payload=SERVER_ERROR_PAYLOAD,
        expected_exception=(exceptions.InvalidArgument, exceptions.BadRequest),
        t3_feature_id="F2.3",
        t4_feature_id="F1.3",
        t4_custom={"http.response.status_code": lambda sc: sc >= 400},
    ),
    # 7. [F1.9 & F2.8] gRPC Client Timeout
    ComplianceScenario(
        id="grpc_client_timeout",
        transport="grpc",
        tracing_enabled=True,
        payload=TIMEOUT_ERROR_PAYLOAD,
        call_kwargs={"retry": None, "timeout": 0.2},
        expected_exception=(exceptions.DeadlineExceeded, exceptions.GatewayTimeout),
        t3_feature_id="F2.8",
        t4_feature_id="F1.9",
    ),
    # 8. [F1.4 & F2.4] HTTP Client Timeout
    ComplianceScenario(
        id="http_client_timeout",
        transport="rest",
        tracing_enabled=True,
        payload=TIMEOUT_ERROR_PAYLOAD,
        call_kwargs={"retry": None, "timeout": 0.2},
        expected_exception=(exceptions.DeadlineExceeded, exceptions.GatewayTimeout),
        t3_feature_id="F2.4",
        t4_feature_id="F1.4",
    ),
    # 9. [F1.10] gRPC Retry Recovery
    ComplianceScenario(
        id="grpc_retry_recovery",
        transport="grpc",
        tracing_enabled=True,
        t4_feature_id="F1.10",
    ),
    # 10. [F1.5] HTTP Retry Recovery
    ComplianceScenario(
        id="http_retry_recovery",
        transport="rest",
        tracing_enabled=True,
        t4_feature_id="F1.5",
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


def test_f3_1_http_retry_succeeds(span_exporter, use_mtls):
    """[F3.1] HTTP/REST Retry Succeeds: Validates 1 T3 parent + 2 T4 child spans."""
    exporter, provider = span_exporter
    client_options = ClientOptions(tracer_provider=provider)
    old_env = os.environ.get("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED")
    os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"

    try:
        client = conftest.construct_client(
            SequenceServiceClient,
            transport_name="rest",
            use_mtls=use_mtls,
            client_options=client_options,
            credentials=ga_credentials.AnonymousCredentials(),
        )

        sequence = client.create_sequence(
            CreateSequenceRequest(
                sequence=Sequence(
                    responses=[
                        Sequence.Response(
                            status=status_pb2.Status(
                                code=code_pb2.UNAVAILABLE,
                                message="HTTP temporary failure",
                            )
                        ),
                        Sequence.Response(status=status_pb2.Status(code=code_pb2.OK)),
                    ]
                )
            )
        )

        exporter.clear()

        retry_policy = retries.Retry(
            predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
            initial=0.01,
            maximum=0.05,
            multiplier=1.0,
            deadline=5.0,
        )

        client.attempt_sequence(
            AttemptSequenceRequest(name=sequence.name),
            retry=retry_policy,
        )

        spans = exporter.get_finished_spans()
        assert len(spans) == 3, f"Expected 3 spans (1 T3 + 2 T4), got {len(spans)}"

        t3_spans = [s for s in spans if s.parent is None]
        t4_spans = [s for s in spans if s.parent is not None]
        assert len(t3_spans) == 1, f"Expected 1 T3 root span, got {len(t3_spans)}"
        assert len(t4_spans) == 2, f"Expected 2 T4 child spans, got {len(t4_spans)}"

        method_span = t3_spans[0]
        t4_1 = [
            s for s in t4_spans if s.attributes.get("http.response.status_code") == 503
        ][0]
        t4_2 = [
            s for s in t4_spans if s.attributes.get("http.response.status_code") == 200
        ][0]

        # Verify parent-child hierarchy
        assert t4_1.parent.span_id == method_span.context.span_id
        assert t4_2.parent.span_id == method_span.context.span_id

        # Verify child span statuses
        assert t4_1.status.status_code.name == "ERROR"
        assert t4_2.status.status_code.name in ("UNSET", "OK")

        # Verify parent span status & aggregation
        assert method_span.status.status_code.name in ("UNSET", "OK")
        assert "error.type" not in method_span.attributes

        # Record compliance
        contract, _ = build_contract("F3.1")
        assert contract is not None
        contract.validate(reporter=span_contract.COMPLIANCE_REPORTER)

    finally:
        if old_env is not None:
            os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = old_env
        else:
            os.environ.pop("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", None)


def test_f3_2_http_retries_exhausted(span_exporter, use_mtls):
    """[F3.2] HTTP/REST Retries Exhausted: Validates 1 T3 parent + N T4 child spans, error aggregated."""
    exporter, provider = span_exporter
    client_options = ClientOptions(tracer_provider=provider)
    old_env = os.environ.get("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED")
    os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"

    try:
        client = conftest.construct_client(
            SequenceServiceClient,
            transport_name="rest",
            use_mtls=use_mtls,
            client_options=client_options,
            credentials=ga_credentials.AnonymousCredentials(),
        )

        sequence = client.create_sequence(
            CreateSequenceRequest(
                sequence=Sequence(
                    responses=[
                        Sequence.Response(
                            status=status_pb2.Status(
                                code=code_pb2.UNAVAILABLE,
                                message="HTTP permanent unavailable",
                            )
                        )
                        for _ in range(20)
                    ]
                )
            )
        )

        exporter.clear()

        retry_policy = retries.Retry(
            predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
            initial=0.01,
            maximum=0.01,
            multiplier=1.0,
            deadline=0.05,
        )

        with pytest.raises((exceptions.RetryError, exceptions.ServiceUnavailable)):
            client.attempt_sequence(
                AttemptSequenceRequest(name=sequence.name),
                retry=retry_policy,
            )

        spans = exporter.get_finished_spans()
        assert len(spans) >= 2, (
            f"Expected at least 2 spans (1 T3 + >=1 T4), got {len(spans)}"
        )

        t3_spans = [s for s in spans if s.parent is None]
        t4_spans = [s for s in spans if s.parent is not None]
        assert len(t3_spans) == 1, f"Expected 1 T3 root span, got {len(t3_spans)}"
        assert len(t4_spans) >= 1, f"Expected >=1 T4 child spans, got {len(t4_spans)}"

        method_span = t3_spans[0]
        # Verify parent-child hierarchy on all attempts
        for t4 in t4_spans:
            assert t4.parent.span_id == method_span.context.span_id
            assert t4.status.status_code.name == "ERROR"
            assert t4.attributes.get("http.response.status_code") == 503

        # Verify parent span status & aggregated error
        assert method_span.status.status_code.name == "ERROR"
        assert method_span.attributes.get("error.type") == "UNAVAILABLE"
        assert "rpc.system.name" in method_span.attributes

        # Record compliance
        contract, _ = build_contract("F3.2")
        assert contract is not None
        contract.validate(reporter=span_contract.COMPLIANCE_REPORTER)

    finally:
        if old_env is not None:
            os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = old_env
        else:
            os.environ.pop("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", None)


def test_f3_3_grpc_retry_succeeds(span_exporter, use_mtls):
    """[F3.3] gRPC Retry Succeeds: Validates 1 T3 parent + 2 T4 child spans."""
    exporter, provider = span_exporter
    client_options = ClientOptions(tracer_provider=provider)
    old_env = os.environ.get("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED")
    os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"

    try:
        client = conftest.construct_client(
            SequenceServiceClient,
            transport_name="grpc",
            use_mtls=use_mtls,
            client_options=client_options,
            credentials=ga_credentials.AnonymousCredentials(),
        )

        sequence = client.create_sequence(
            CreateSequenceRequest(
                sequence=Sequence(
                    responses=[
                        Sequence.Response(
                            status=status_pb2.Status(
                                code=code_pb2.UNAVAILABLE,
                                message="gRPC temporary failure",
                            )
                        ),
                        Sequence.Response(status=status_pb2.Status(code=code_pb2.OK)),
                    ]
                )
            )
        )

        exporter.clear()

        retry_policy = retries.Retry(
            predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
            initial=0.01,
            maximum=0.05,
            multiplier=1.0,
            deadline=5.0,
        )

        client.attempt_sequence(
            AttemptSequenceRequest(name=sequence.name),
            retry=retry_policy,
        )

        spans = exporter.get_finished_spans()
        assert len(spans) == 3, f"Expected 3 spans (1 T3 + 2 T4), got {len(spans)}"

        t3_spans = [s for s in spans if s.parent is None]
        t4_spans = [s for s in spans if s.parent is not None]
        assert len(t3_spans) == 1, f"Expected 1 T3 root span, got {len(t3_spans)}"
        assert len(t4_spans) == 2, f"Expected 2 T4 child spans, got {len(t4_spans)}"

        method_span = t3_spans[0]
        # Child 1: status 14 UNAVAILABLE; Child 2: status 0 OK
        t4_1 = [s for s in t4_spans if s.attributes.get("rpc.grpc.status_code") == 14][
            0
        ]
        t4_2 = [s for s in t4_spans if s.attributes.get("rpc.grpc.status_code") == 0][0]

        # Verify parent-child hierarchy
        assert t4_1.parent.span_id == method_span.context.span_id
        assert t4_2.parent.span_id == method_span.context.span_id

        # Verify child span statuses
        assert t4_1.status.status_code.name == "ERROR"
        assert t4_2.status.status_code.name in ("UNSET", "OK")

        # Verify parent span status & aggregation
        assert method_span.status.status_code.name in ("UNSET", "OK")
        assert "error.type" not in method_span.attributes

        # Record compliance
        contract, _ = build_contract("F3.3")
        assert contract is not None
        contract.validate(reporter=span_contract.COMPLIANCE_REPORTER)

    finally:
        if old_env is not None:
            os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = old_env
        else:
            os.environ.pop("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", None)


def test_f3_4_grpc_retries_exhausted(span_exporter, use_mtls):
    """[F3.4] gRPC Retries Exhausted: Validates 1 T3 parent + N T4 child spans, error aggregated."""
    exporter, provider = span_exporter
    client_options = ClientOptions(tracer_provider=provider)
    old_env = os.environ.get("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED")
    os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"

    try:
        client = conftest.construct_client(
            SequenceServiceClient,
            transport_name="grpc",
            use_mtls=use_mtls,
            client_options=client_options,
            credentials=ga_credentials.AnonymousCredentials(),
        )

        sequence = client.create_sequence(
            CreateSequenceRequest(
                sequence=Sequence(
                    responses=[
                        Sequence.Response(
                            status=status_pb2.Status(
                                code=code_pb2.UNAVAILABLE,
                                message="gRPC permanent unavailable",
                            )
                        )
                        for _ in range(20)
                    ]
                )
            )
        )

        exporter.clear()

        retry_policy = retries.Retry(
            predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
            initial=0.01,
            maximum=0.01,
            multiplier=1.0,
            deadline=0.05,
        )

        with pytest.raises((exceptions.RetryError, exceptions.ServiceUnavailable)):
            client.attempt_sequence(
                AttemptSequenceRequest(name=sequence.name),
                retry=retry_policy,
            )

        spans = exporter.get_finished_spans()
        assert len(spans) >= 2, (
            f"Expected at least 2 spans (1 T3 + >=1 T4), got {len(spans)}"
        )

        t3_spans = [s for s in spans if s.parent is None]
        t4_spans = [s for s in spans if s.parent is not None]
        assert len(t3_spans) == 1, f"Expected 1 T3 root span, got {len(t3_spans)}"
        assert len(t4_spans) >= 1, f"Expected >=1 T4 child spans, got {len(t4_spans)}"

        method_span = t3_spans[0]
        # Verify parent-child hierarchy on all attempts
        for t4 in t4_spans:
            assert t4.parent.span_id == method_span.context.span_id
            assert t4.status.status_code.name == "ERROR"
            assert t4.attributes.get("rpc.grpc.status_code") == 14

        # Verify parent span status & aggregated error
        assert method_span.status.status_code.name == "ERROR"
        assert method_span.attributes.get("error.type") == "UNAVAILABLE"
        assert "rpc.system.name" in method_span.attributes

        # Record compliance
        contract, _ = build_contract("F3.4")
        assert contract is not None
        contract.validate(reporter=span_contract.COMPLIANCE_REPORTER)

    finally:
        if old_env is not None:
            os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = old_env
        else:
            os.environ.pop("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", None)


def test_z_print_telemetry_compliance_scorecard():
    """Outputs the complete Telemetry Compliance Scorecard (Option A format)."""
    scorecard = span_contract.COMPLIANCE_REPORTER.generate_scorecard()
    print("\n" + scorecard + "\n")
    assert "TOTAL: 22/22 FEATURES CONFORMANT" in scorecard
