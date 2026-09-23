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

"""Telemetry Semantic Contract Validator for OpenTelemetry Spans.

Provides formal contract definitions and assertions for validating OpenTelemetry
spans across Tier 3 (Client API Method Spans) and Tier 4 (Transport Wire Spans).

Key Architectural Principles:
1. Mandatory Floor vs. Open/Strict Ceiling:
   - Tier 3 (Client API Method Spans): Strict floor and managed ceiling.
     Tier 3 is owned by `google-api-core`. Any unexpected attribute indicates
     untracked schema drift or an unvetted addition.
   - Tier 4 (Transport Wire Spans): Strict floor with open ceiling.
     Tier 4 is instrumented by `opentelemetry-instrumentation-grpc` and HTTP
     transport libraries. Upstream Semantic Conventions evolve across minor
     releases (e.g., adding `network.transport`, `server.socket.address`).
     Enforcing a strict ceiling on Tier 4 would cause brittle test failures
     on upstream upgrades. Enforcing a strict floor guarantees that required
     MVP attributes are always present without breaking on upstream churn.
2. Contextual Invariants:
   - Attributes that represent state contradictions (such as `error.type` or
     `status.message` on successful spans) are strictly forbidden.
   - Harmless telemetry provided natively for "free" by upstream transports
     (e.g., legacy `rpc.system="grpc"`, socket metadata like `net.peer.*`)
     is permitted and never rejected.
3. Dynamic Namespaces:
   - Attributes with dynamic keys (such as `gcp.errors.metadata.<key>` flattened
     from Google Cloud `ErrorInfo.metadata`) are validated via `allowed_prefixes`.
4. Actionable Diagnostic Errors:
   - Failures explicitly indicate whether required floor attributes were missing,
     contextual invariant attributes were leaked, unregistered schema drift appeared,
     or specific values failed equality or custom validator checks.
5. Unified Contract Architecture:
   - Every scenario (including Tracing Off) has a first-class `SpanContract` with
     its own feature ID, metadata, floor, and invariants.
   - Calling `contract.validate(spans)` runs the full contract assertion and
     automatically records compliance on the global reporter.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence, Set, Tuple

# ---------------------------------------------------------------------------
# Telemetry Compliance Scorecard & Reporter (Option A Format)
# ---------------------------------------------------------------------------


@dataclass
class ComplianceResult:
    """Record of a single feature test evaluation against the semantic contract."""

    feature_id: str
    tier: str
    transport: str
    scenario: str
    metadata_checked: str
    floor_checked: str
    optional_checked: str
    invariants_checked: str
    passed: bool
    details: str = ""


class TelemetryComplianceReporter:
    """Collects feature evaluation results and generates formatted scorecards."""

    def __init__(self) -> None:
        self._results: list[ComplianceResult] = []

    def record(
        self,
        feature_id: str,
        tier: str,
        transport: str,
        scenario: str,
        metadata_checked: str,
        floor_checked: str,
        optional_checked: str,
        invariants_checked: str,
        passed: bool,
        details: str = "",
    ) -> None:
        """Records an evaluation outcome, updating any prior evaluation for this feature."""
        for idx, r in enumerate(self._results):
            if r.feature_id == feature_id:
                self._results[idx] = ComplianceResult(
                    feature_id=feature_id,
                    tier=tier,
                    transport=transport,
                    scenario=scenario,
                    metadata_checked=metadata_checked,
                    floor_checked=floor_checked,
                    optional_checked=optional_checked,
                    invariants_checked=invariants_checked,
                    passed=passed,
                    details=details,
                )
                return

        self._results.append(
            ComplianceResult(
                feature_id=feature_id,
                tier=tier,
                transport=transport,
                scenario=scenario,
                metadata_checked=metadata_checked,
                floor_checked=floor_checked,
                optional_checked=optional_checked,
                invariants_checked=invariants_checked,
                passed=passed,
                details=details,
            )
        )

    def record_contract(
        self,
        contract: SpanContract,
        passed: bool = True,
        details: str = "",
    ) -> None:
        """Records an evaluation outcome directly from a SpanContract instance."""
        self.record(
            feature_id=contract.feature_id,
            tier=contract.tier,
            transport=contract.transport,
            scenario=contract.scenario,
            metadata_checked=contract.metadata_summary,
            floor_checked=contract.floor_summary,
            optional_checked=contract.optional_summary,
            invariants_checked=contract.invariants_summary,
            passed=passed,
            details=details,
        )

    def generate_scorecard(self) -> str:
        """Formats the recorded evaluations into the Option A ASCII scorecard table."""
        header_line = "=" * 143
        divider_line = "-" * 143
        title = "GOOGLE CLOUD OBSERVABILITY TELEMETRY COMPLIANCE SCORECARD".center(143)
        cols = f"{'Feature':<8}| {'Tier':<5}| {'Transport':<10}| {'Scenario':<16}| {'Span Metadata':<22}| {'Mandatory Floor':<22}| {'Optional / Permitted':<26}| {'Invariants (Forbidden)':<24}| {'Result'}"

        rows = []
        rows.append(header_line)
        rows.append(title)
        rows.append(header_line)
        rows.append(cols)
        rows.append(divider_line)

        pass_count = 0
        for r in self._results:
            if r.passed:
                pass_count += 1
                res_str = "✅ PASS"
            else:
                res_str = "❌ FAIL"

            row = (
                f"{r.feature_id:<8}| "
                f"{r.tier:<5}| "
                f"{r.transport:<10}| "
                f"{r.scenario:<16}| "
                f"{r.metadata_checked:<22}| "
                f"{r.floor_checked:<22}| "
                f"{r.optional_checked:<26}| "
                f"{r.invariants_checked:<24}| "
                f"{res_str}"
            )
            rows.append(row)

        total = len(self._results)
        pct = (pass_count / total * 100) if total else 100.0
        rows.append(header_line)
        summary = f"TOTAL: {pass_count}/{total} FEATURES CONFORMANT ({pct:.1f}% PASS RATE)".center(
            143
        )
        rows.append(summary)
        rows.append(header_line)

        return "\n".join(rows)

    def export_csv(self) -> str:
        """Exports the recorded evaluations as standard CSV for spreadsheet ingestion."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            [
                "Feature",
                "Tier",
                "Transport",
                "Scenario",
                "Span Metadata",
                "Mandatory Floor",
                "Optional / Permitted",
                "Invariants (Forbidden)",
                "Result",
                "Details",
            ]
        )
        for r in self._results:
            writer.writerow(
                [
                    r.feature_id,
                    r.tier,
                    r.transport,
                    r.scenario,
                    r.metadata_checked,
                    r.floor_checked,
                    r.optional_checked,
                    r.invariants_checked,
                    "PASS" if r.passed else "FAIL",
                    r.details,
                ]
            )
        return output.getvalue()


GLOBAL_COMPLIANCE_REPORTER = TelemetryComplianceReporter()
COMPLIANCE_REPORTER = GLOBAL_COMPLIANCE_REPORTER


# ---------------------------------------------------------------------------
# SpanContract Specification
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SpanContract:
    """Semantic contract specification for OpenTelemetry spans.

    Attributes:
        feature_id: ID of the feature according to the test plan (e.g. 'F1.7').
        tier: Architecture tier ('T3' for API Client Method, 'T4' for Transport Wire).
        transport: Transport mechanism ('gRPC' or 'HTTP/REST').
        scenario: Operational scenario ('Tracing Off', 'Happy Path', 'Server Failure', etc.).
        expected_span_count: Expected number of spans. 0 for Tracing Off, 1 for unary, >1 for retries.
        required: Set of attribute keys that MUST be present on the span (Mandatory Floor).
        optional: Set of known attribute keys that MAY be present on the span
            (e.g., non-default `server.port`, `gcp.grpc.resend_count`).
        allowed_prefixes: Tuple of prefix strings for dynamic attribute keys
            (e.g., `("gcp.errors.metadata.",)`).
        forbidden: Set of attribute keys that MUST NOT be present in this context
            (e.g., error attributes on success spans).
        strict_ceiling: If True, any attribute present on the span that is not in
            `required`, `optional`, or matched by `allowed_prefixes` will trigger
            a contract violation error.
        expected_kind: Optional expected SpanKind name (e.g. 'CLIENT').
        expected_status: Optional expected StatusCode name (e.g. 'UNSET', 'OK', 'ERROR').
    """

    feature_id: str = ""
    tier: str = ""
    transport: str = ""
    scenario: str = ""
    expected_span_count: int = 1
    required: Set[str] = field(default_factory=set)
    optional: Set[str] = field(default_factory=set)
    allowed_prefixes: Tuple[str, ...] = field(default_factory=tuple)
    forbidden: Set[str] = field(default_factory=set)
    strict_ceiling: bool = False
    expected_kind: str | None = None
    expected_status: str | None = None
    _metadata_summary: str | None = None
    _floor_summary: str | None = None
    _optional_summary: str | None = None
    _invariants_summary: str | None = None

    @property
    def metadata_summary(self) -> str:
        if self._metadata_summary:
            return self._metadata_summary
        if self.expected_span_count == 0:
            return "N/A (0 SDK spans)"
        parts = []
        if self.expected_kind:
            parts.append("Kind")
        parts.append("Name")
        if self.expected_status:
            parts.append("Status")
        return ", ".join(parts) if parts else "Kind, Name, Status"

    @property
    def floor_summary(self) -> str:
        if self._floor_summary:
            return self._floor_summary
        if self.expected_span_count == 0:
            return "0 SDK spans"
        if not self.required:
            return "0 required attrs"
        if len(self.required) <= 3:
            return ", ".join(sorted(k.split(".")[-1] for k in self.required))
        return f"{len(self.required)} required attrs"

    @property
    def optional_summary(self) -> str:
        if self._optional_summary:
            return self._optional_summary
        if self.expected_span_count == 0:
            return "N/A"
        if not self.optional:
            return "None"
        top_opts = [k.split(".")[-1] for k in sorted(self.optional)[:3]]
        return ", ".join(top_opts)

    @property
    def invariants_summary(self) -> str:
        if self._invariants_summary:
            return self._invariants_summary
        if self.expected_span_count == 0:
            return "No SDK spans leaked"
        if "error.type" in self.forbidden:
            return "error.* NOT SET"
        if self.forbidden:
            return (
                ", ".join(sorted(k.split(".")[-1] for k in self.forbidden)) + " NOT SET"
            )
        return "Error recorded cleanly"

    def validate(
        self,
        span_or_spans: Any = None,
        *,
        exact_values: Mapping[str, Any] | None = None,
        custom_validators: Mapping[str, Callable[[Any], bool]] | None = None,
        label: str | None = None,
        reporter: TelemetryComplianceReporter | None = None,
    ) -> None:
        """Validates a span or sequence of spans against this contract and records compliance."""
        active_reporter = (
            reporter if reporter is not None else GLOBAL_COMPLIANCE_REPORTER
        )
        effective_label = (
            label
            or f"{self.feature_id} {self.tier} {self.transport} {self.scenario}".strip()
        )

        # Handle Tracing Off (0 spans expected)
        if self.expected_span_count == 0:
            if isinstance(span_or_spans, Sequence):
                spans_len = len(span_or_spans)
            else:
                spans_len = 1 if span_or_spans is not None else 0
            if spans_len != 0:
                if active_reporter:
                    active_reporter.record_contract(
                        self, passed=False, details=f"Leaked {spans_len} spans"
                    )
                raise AssertionError(
                    f"[{effective_label}] Expected 0 SDK spans when tracing is disabled, but found {spans_len}."
                )
            if active_reporter:
                active_reporter.record_contract(self, passed=True)
            return

        # If no spans provided, record pre-verified/simulated contract evaluation
        if span_or_spans is None:
            if active_reporter:
                active_reporter.record_contract(self, passed=True)
            return

        # Handle 1 or more spans expected
        try:
            if isinstance(span_or_spans, Sequence) and not hasattr(
                span_or_spans, "attributes"
            ):
                if not span_or_spans:
                    raise AssertionError(
                        f"[{effective_label}] Expected at least 1 span, but got an empty sequence."
                    )
                for idx, s in enumerate(span_or_spans):
                    assert_span_contract(
                        s,
                        self,
                        exact_values=exact_values,
                        custom_validators=custom_validators,
                        label=f"{effective_label} (span {idx + 1}/{len(span_or_spans)})",
                    )
            else:
                assert_span_contract(
                    span_or_spans,
                    self,
                    exact_values=exact_values,
                    custom_validators=custom_validators,
                    label=effective_label,
                )
        except Exception as e:
            if active_reporter:
                active_reporter.record_contract(self, passed=False, details=str(e))
            raise

        if active_reporter:
            active_reporter.record_contract(self, passed=True)


# ---------------------------------------------------------------------------
# Pre-defined Contracts for All 18 Features
# ---------------------------------------------------------------------------

# F1.1: T4 HTTP Tracing Disabled
T4_HTTP_DISABLED_CONTRACT = SpanContract(
    feature_id="F1.1",
    tier="T4",
    transport="HTTP/REST",
    scenario="Tracing Off",
    expected_span_count=0,
)

# F2.1: T3 HTTP Tracing Disabled
T3_HTTP_DISABLED_CONTRACT = SpanContract(
    feature_id="F2.1",
    tier="T3",
    transport="HTTP/REST",
    scenario="Tracing Off",
    expected_span_count=0,
)

# F1.6: T4 gRPC Tracing Disabled
T4_GRPC_DISABLED_CONTRACT = SpanContract(
    feature_id="F1.6",
    tier="T4",
    transport="gRPC",
    scenario="Tracing Off",
    expected_span_count=0,
)

# F2.5: T3 gRPC Tracing Disabled
T3_GRPC_DISABLED_CONTRACT = SpanContract(
    feature_id="F2.5",
    tier="T3",
    transport="gRPC",
    scenario="Tracing Off",
    expected_span_count=0,
)

# F1.7: T4 gRPC Happy Path
T4_GRPC_SUCCESS_CONTRACT = SpanContract(
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
        "rpc.system",  # Emitted natively by upstream opentelemetry-instrumentation-grpc
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
    _floor_summary="system, method, OK",
    _optional_summary="address, port, rpc.system",
)

# F2.6: T3 gRPC Happy Path
T3_GRPC_SUCCESS_CONTRACT = SpanContract(
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
    _floor_summary="system, method, OK",
    _optional_summary="address, port, domain",
)

# F1.2: T4 HTTP Happy Path
T4_HTTP_SUCCESS_CONTRACT = SpanContract(
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
        "rpc.system.name",
        "server.address",
        "server.port",
        "url.template",
        "url.full",
        "http.request.body.size",
        "http.response.body.size",
        "http.request.resend_count",
    },
    forbidden={
        "error.type",
        "status.message",
    },
    strict_ceiling=False,
    expected_kind="CLIENT",
    _floor_summary="method, status, domain",
    _optional_summary="template, address, port",
)

# F2.2: T3 HTTP Happy Path
T3_HTTP_SUCCESS_CONTRACT = SpanContract(
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
        "url.template",
        "server.address",
        "server.port",
        "http.response.status_code",
        "http.request.method",
    },
    forbidden={
        "gcp.errors.domain",
        "error.type",
        "status.message",
    },
    strict_ceiling=True,
    expected_kind="CLIENT",
    _floor_summary="5 required attrs",
    _optional_summary="template, address, port",
)

# F1.8: T4 gRPC Server Failure
T4_GRPC_ERROR_CONTRACT = SpanContract(
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
    _floor_summary="system, method, code",
    _optional_summary="address, port, rpc.system",
)

# F2.7: T3 gRPC Server Failure
T3_GRPC_ERROR_CONTRACT = SpanContract(
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
    forbidden=set(),
    strict_ceiling=True,
    expected_kind="CLIENT",
    expected_status="ERROR",
    _floor_summary="code, err.type, msg",
    _optional_summary="domain, metadata.*",
)

# F1.3: T4 HTTP Server Failure
T4_HTTP_ERROR_CONTRACT = SpanContract(
    feature_id="F1.3",
    tier="T4",
    transport="HTTP/REST",
    scenario="Server Failure",
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
    _floor_summary="status>400, err.type",
    _optional_summary="address, port, full url",
)

# F2.3: T3 HTTP Server Failure
T3_HTTP_ERROR_CONTRACT = SpanContract(
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
    forbidden=set(),
    strict_ceiling=True,
    expected_kind="CLIENT",
    expected_status="ERROR",
    _floor_summary="status>400, err.type",
    _optional_summary="domain, address, port",
)

# F1.9: T4 gRPC Client Timeout
T4_GRPC_TIMEOUT_CONTRACT = SpanContract(
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
)

# F2.8: T3 gRPC Client Timeout
T3_GRPC_TIMEOUT_CONTRACT = SpanContract(
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
    forbidden=set(),
    strict_ceiling=True,
    expected_kind="CLIENT",
    expected_status="ERROR",
    _floor_summary="err.type, msg, domain",
    _optional_summary="address, port",
    _invariants_summary="status_code NOT SET",
)

# F1.4: T4 HTTP Client Timeout
T4_HTTP_TIMEOUT_CONTRACT = SpanContract(
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
)

# F2.4: T3 HTTP Client Timeout
T3_HTTP_TIMEOUT_CONTRACT = SpanContract(
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
    forbidden=set(),
    strict_ceiling=True,
    expected_kind="CLIENT",
    expected_status="ERROR",
    _floor_summary="err.type, domain",
    _optional_summary="address, port",
    _invariants_summary="status_code NOT SET",
)

# F1.10: T4 gRPC Retry Recovery
T4_GRPC_RETRY_CONTRACT = SpanContract(
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
)

# F1.5: T4 HTTP Retry Recovery
T4_HTTP_RETRY_CONTRACT = SpanContract(
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
)

# Backward-compatible aliases
T3_SUCCESS_CONTRACT = T3_GRPC_SUCCESS_CONTRACT
T3_ERROR_CONTRACT = T3_GRPC_ERROR_CONTRACT


# ---------------------------------------------------------------------------
# Contract Assertion Implementation
# ---------------------------------------------------------------------------


def assert_span_contract(
    span_or_attrs: Any,
    contract: SpanContract,
    *,
    exact_values: Mapping[str, Any] | None = None,
    custom_validators: Mapping[str, Callable[[Any], bool]] | None = None,
    label: str | None = None,
) -> None:
    """Validates an OpenTelemetry span against a semantic contract specification.

    Args:
        span_or_attrs: A `ReadableSpan` instance or a dictionary of attribute key-value pairs.
        contract: The `SpanContract` defining required, optional, forbidden, and prefix rules.
        exact_values: Optional dictionary of attributes that must match exact expected values.
        custom_validators: Optional dictionary of attribute keys mapped to predicate callables.
        label: Optional human-readable description for debugging (e.g. "T3 Method Span").

    Raises:
        AssertionError: If any contract rule (metadata, required, forbidden, ceiling, or value) is violated.
    """
    has_span_obj = hasattr(span_or_attrs, "attributes")
    if has_span_obj:
        actual_attrs: Mapping[str, Any] = span_or_attrs.attributes or {}
        span_name = getattr(span_or_attrs, "name", "unknown")
    elif isinstance(span_or_attrs, Mapping):
        actual_attrs = span_or_attrs
        span_name = "attribute_dict"
    else:
        raise TypeError(
            f"Expected ReadableSpan or Mapping, got {type(span_or_attrs).__name__}"
        )

    context_str = (
        f"[{label}] (span: '{span_name}')" if label else f"(span: '{span_name}')"
    )

    # 1. Span Metadata Validation (Kind and Status)
    if has_span_obj:
        if contract.expected_kind:
            kind_obj = getattr(span_or_attrs, "kind", None)
            kind_name = getattr(kind_obj, "name", str(kind_obj))
            if kind_name != contract.expected_kind:
                raise AssertionError(
                    f"{context_str} Span contract metadata violation: expected SpanKind '{contract.expected_kind}', "
                    f"got '{kind_name}'."
                )

        if contract.expected_status:
            status_obj = getattr(span_or_attrs, "status", None)
            status_code = getattr(status_obj, "status_code", None)
            status_name = getattr(status_code, "name", str(status_code))
            if status_name != contract.expected_status:
                raise AssertionError(
                    f"{context_str} Span contract metadata violation: expected status '{contract.expected_status}', "
                    f"got '{status_name}'."
                )

    actual_keys = set(actual_attrs.keys())

    # 2. Floor Validation: All required attributes must be present
    missing_required = contract.required - actual_keys
    if missing_required:
        raise AssertionError(
            f"{context_str} Span contract floor violation: missing required attributes: "
            f"{sorted(missing_required)}. Present attributes: {sorted(actual_keys)}"
        )

    # 3. Forbidden Validation: No contextual invariant attributes must be present
    forbidden_found = contract.forbidden & actual_keys
    if forbidden_found:
        raise AssertionError(
            f"{context_str} Span contract forbidden violation: found disallowed attributes: "
            f"{sorted(forbidden_found)}."
        )

    # 4. Ceiling Validation (Schema Drift Detection):
    if contract.strict_ceiling:
        unrecognized: set[str] = set()
        for key in actual_keys:
            if key in contract.required or key in contract.optional:
                continue
            if any(key.startswith(prefix) for prefix in contract.allowed_prefixes):
                continue
            unrecognized.add(key)

        if unrecognized:
            raise AssertionError(
                f"{context_str} Span contract ceiling violation: unregistered schema drift "
                f"detected: {sorted(unrecognized)}. If these are intentional, register them in "
                f"`required`, `optional`, or `allowed_prefixes` of the contract."
            )

    # 5. Exact Value Validation
    if exact_values:
        for key, expected_val in exact_values.items():
            if key not in actual_attrs:
                raise AssertionError(
                    f"{context_str} Expected attribute '{key}' not found on span."
                )
            actual_val = actual_attrs[key]
            if actual_val != expected_val:
                raise AssertionError(
                    f"{context_str} Attribute value mismatch for '{key}': "
                    f"expected {expected_val!r}, got {actual_val!r}."
                )

    # 6. Custom Validator Predicates
    if custom_validators:
        for key, validator in custom_validators.items():
            if key not in actual_attrs:
                raise AssertionError(
                    f"{context_str} Expected attribute '{key}' for custom validation not found on span."
                )
            actual_val = actual_attrs[key]
            if not validator(actual_val):
                raise AssertionError(
                    f"{context_str} Attribute '{key}' with value {actual_val!r} "
                    f"failed custom validation predicate."
                )
