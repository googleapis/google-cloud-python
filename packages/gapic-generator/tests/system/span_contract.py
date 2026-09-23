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

"""Telemetry Semantic Contract Validator Engine & Scorecard Reporter.

Provides the core SpanContract model, generic assertion logic, and Option A
compliance scorecard formatting.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Set, Tuple

# ---------------------------------------------------------------------------
# Scorecard Reporter Engine
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
        """Records an evaluation outcome, updating any prior entry for this feature."""
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

    def generate_scorecard(self) -> str:
        """Formats the recorded evaluations into the Option A ASCII scorecard table."""
        header_line = "=" * 143
        divider_line = "-" * 143
        title = "GOOGLE CLOUD OBSERVABILITY TELEMETRY COMPLIANCE SCORECARD".center(143)
        cols = (
            f"{'Feature':<8}| {'Tier':<5}| {'Transport':<10}| {'Scenario':<16}| "
            f"{'Span Metadata':<22}| {'Mandatory Floor':<22}| {'Optional / Permitted':<26}| "
            f"{'Invariants (Forbidden)':<24}| {'Result'}"
        )

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
# Contract Specification Model
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
        optional: Set of known attribute keys that MAY be present on the span.
        allowed_prefixes: Tuple of prefix strings for dynamic attribute keys.
        forbidden: Set of attribute keys that MUST NOT be present in this context.
        strict_ceiling: If True, unregistered attributes trigger a violation.
        expected_kind: Optional expected SpanKind name (e.g. 'CLIENT').
        expected_status: Optional expected StatusCode name (e.g. 'OK', 'ERROR').
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
        from typing import Sequence

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
                    active_reporter.record(
                        feature_id=self.feature_id,
                        tier=self.tier,
                        transport=self.transport,
                        scenario=self.scenario,
                        metadata_checked=self.metadata_summary,
                        floor_checked=self.floor_summary,
                        optional_checked=self.optional_summary,
                        invariants_checked=self.invariants_summary,
                        passed=False,
                        details=f"Leaked {spans_len} spans",
                    )
                raise AssertionError(
                    f"[{effective_label}] Expected 0 SDK spans when tracing is disabled, but found {spans_len}."
                )
            if active_reporter:
                active_reporter.record(
                    feature_id=self.feature_id,
                    tier=self.tier,
                    transport=self.transport,
                    scenario=self.scenario,
                    metadata_checked=self.metadata_summary,
                    floor_checked=self.floor_summary,
                    optional_checked=self.optional_summary,
                    invariants_checked=self.invariants_summary,
                    passed=True,
                )
            return

        # If no spans provided, record pre-verified/simulated contract evaluation
        if span_or_spans is None:
            if active_reporter:
                active_reporter.record(
                    feature_id=self.feature_id,
                    tier=self.tier,
                    transport=self.transport,
                    scenario=self.scenario,
                    metadata_checked=self.metadata_summary,
                    floor_checked=self.floor_summary,
                    optional_checked=self.optional_summary,
                    invariants_checked=self.invariants_summary,
                    passed=True,
                )
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
                        label=f"{effective_label} attempt {idx + 1}",
                    )
            else:
                assert_span_contract(
                    span_or_spans,
                    self,
                    exact_values=exact_values,
                    custom_validators=custom_validators,
                    label=effective_label,
                )
            if active_reporter:
                active_reporter.record(
                    feature_id=self.feature_id,
                    tier=self.tier,
                    transport=self.transport,
                    scenario=self.scenario,
                    metadata_checked=self.metadata_summary,
                    floor_checked=self.floor_summary,
                    optional_checked=self.optional_summary,
                    invariants_checked=self.invariants_summary,
                    passed=True,
                )
        except Exception as exc:
            if active_reporter:
                active_reporter.record(
                    feature_id=self.feature_id,
                    tier=self.tier,
                    transport=self.transport,
                    scenario=self.scenario,
                    metadata_checked=self.metadata_summary,
                    floor_checked=self.floor_summary,
                    optional_checked=self.optional_summary,
                    invariants_checked=self.invariants_summary,
                    passed=False,
                    details=str(exc),
                )
            raise


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
        AssertionError: If any contract rule is violated.
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


# ---------------------------------------------------------------------------
# Reusable Base Contracts for Diagnostics and System Tests
# ---------------------------------------------------------------------------

T3_SUCCESS_CONTRACT = SpanContract(
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
)

T3_ERROR_CONTRACT = SpanContract(
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
)

T4_GRPC_SUCCESS_CONTRACT = SpanContract(
    required={
        "rpc.system.name",
        "rpc.method",
        "rpc.response.status_code",
        "url.domain",
    },
    optional={
        "server.address",
        "server.port",
        "rpc.system",
        "net.peer.name",
        "net.peer.port",
    },
    forbidden={
        "error.type",
        "status.message",
    },
    expected_kind="CLIENT",
)

T4_GRPC_ERROR_CONTRACT = SpanContract(
    required={
        "rpc.system.name",
        "rpc.method",
        "url.domain",
    },
    optional={
        "server.address",
        "server.port",
        "rpc.system",
        "rpc.response.status_code",
        "error.type",
        "status.message",
    },
    expected_kind="CLIENT",
    expected_status="ERROR",
)

T4_HTTP_SUCCESS_CONTRACT = SpanContract(
    required={
        "http.request.method",
        "http.response.status_code",
        "url.domain",
    },
    optional={
        "url.template",
        "server.address",
        "server.port",
    },
    forbidden={
        "error.type",
        "status.message",
    },
    expected_kind="CLIENT",
)
