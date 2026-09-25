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

"""Telemetry Semantic Compliance Verification Suite.

This module implements a spec-driven, matrix-governed verification engine for OpenTelemetry
tracing across Google Cloud Client Libraries (GAPIC), evaluated live against the GAPIC Showcase daemon.

Architectural Overview:
-----------------------
Rather than hardcoding dozens of repetitive test functions with fragile assertions, this suite
operates as a data-driven test engine governed by a Single Source of Truth (SSOT):
`telemetry_requirements_matrix.csv`.

The engine operates across five distinct phases:

1. Specification Matrix (`telemetry_requirements_matrix.csv`):
   Defines the contract for all 22 required observability features across transports (gRPC, REST),
   span tiers (T3 Logical Client vs. T4 Wire Attempt), error scenarios, and retry sequences.

2. Scenario Execution & Span Capture (`execute_scenario`):
   Instantiates isolated Showcase clients configured with in-memory OpenTelemetry tracer
   providers and dispatches live requests (unary echo calls, stateful multi-step retry sequences)
   against the Showcase test daemon.

3. Hierarchy Classification:
   Partitions captured finished spans by parentage:
   - Root Spans (parent is None): Represents the outer logical RPC call (T3 Tier).
   - Child Spans (parent is not None): Represents physical wire attempts (T4 Tier).
   Enforces the hierarchical invariant that all T4 spans must link directly to the T3 span ID.

4. Cell Grammar Parser & Sub-Validators (`resolve_expected_value`, `assert_span_matches_row`):
   Parses matrix cell expressions (supporting static values, positional sequences across attempts
   such as '503 | 200', and tier-partitioned expressions such as 'T3: OK | T4: NOT SET').
   Validates span names, kinds, status codes, string attributes (with wildcard support),
   integer attributes, substring status messages, and protocol-specific resend counts.

5. Diagnostic Archival (`RAW_SPANS_CATALOG` & `test_z_dump_raw_spans`):
   Serializes every captured span in full JSON format to `raw_spans_output.json`, enabling
   offline auditability and regression post-mortems without re-running the live server.
"""

from __future__ import annotations

import contextlib
import csv
import json
from pathlib import Path
from typing import Any

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
from google.rpc import code_pb2, status_pb2
from google.showcase import (
    AttemptSequenceRequest,
    CreateSequenceRequest,
    EchoClient,
    Sequence,
    SequenceServiceClient,
)

try:
    from . import conftest
except (ImportError, ValueError):
    import conftest


# ---------------------------------------------------------------------------
# Test Harness Performance & Tuning Knobs
# ---------------------------------------------------------------------------
# These constants govern execution timing and timeout budgets during test runs.
# They are intentionally separated from the telemetry specification itself:
# while production defaults use exponential backoffs and multi-second retry windows,
# test scenarios require ultra-fast, deterministic execution to keep the CI suite snappy
# without flaking under high concurrency.
SHORT_CLIENT_TIMEOUT_SECONDS = 0.2
FAST_RETRY_BACKOFF_SECONDS = 0.01
# Setting multiplier to 1.0 enforces constant/linear polling intervals, bypassing
# exponential backoff delay calculation during retry loops:
CONSTANT_BACKOFF_MULTIPLIER = 1.0
FAST_EXHAUSTION_DEADLINE_SECONDS = 0.05
GENEROUS_RECOVERY_DEADLINE_SECONDS = 5.0
# Queue depth buffer configured on Showcase server for retry exhaustion tests:
SHOWCASE_EXHAUSTION_QUEUE_BUFFER = 20


# ---------------------------------------------------------------------------
# CSV Matrix Loader & Diagnostic Archival
# ---------------------------------------------------------------------------

CSV_PATH = Path(__file__).parent / "telemetry_requirements_matrix.csv"


def load_feature_matrix() -> dict[str, dict[str, str]]:
    """Loads and indexes the Single Source of Truth CSV requirements matrix.

    Returns:
        A dictionary mapping Feature ID (e.g. 'grpc_happy_path') to its dictionary
        of column names and raw string specifications.
    """
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        return {r["Feature ID"]: r for r in csv.DictReader(f)}


FEATURE_MATRIX = load_feature_matrix()
RAW_SPANS_CATALOG: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Test Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def span_exporter(monkeypatch):
    """Provides an isolated OpenTelemetry in-memory span exporter and provider.

    Lifecycle:
        1. Instantiates an InMemorySpanExporter coupled to a SimpleSpanProcessor.
        2. Sets the SDK tracing feature flag ('GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED=true')
           via pytest's monkeypatch fixture to guarantee process-level isolation without
           polluting global environment state.
        3. Yields the (exporter, provider) pair to the test body.
        4. Clears all buffered spans on teardown to prevent state leakage between tests.

    Args:
        monkeypatch: Pytest fixture for thread-safe environment variable management.

    Yields:
        tuple[InMemorySpanExporter, TracerProvider]: The span collector and provider.
    """
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")

    yield exporter, provider
    exporter.clear()


# ---------------------------------------------------------------------------
# RPC Invocation Runners & Client Construction
# ---------------------------------------------------------------------------


def construct_observability_client(
    client_class,
    transport: str,
    client_options: ClientOptions | None = None,
    use_mtls: bool = False,
):
    """Factory helper to instantiate GAPIC Showcase clients with test harness defaults.

    This function encapsulates client instantiation by supplying `use_mtls=False`
    by default (the standard for local Showcase daemon testing) while forwarding
    transport configuration and OpenTelemetry client_options.

    Design Note:
        Rather than modifying the shared system test fixture helper (`conftest.construct_client`),
        wrapping it locally insulates this compliance suite with zero blast radius on existing
        Showcase tests.

    Args:
        client_class: The GAPIC client class to instantiate (e.g. EchoClient).
        transport: Target transport name ('grpc' or 'rest').
        client_options: Optional ClientOptions containing the TracerProvider.
        use_mtls: Whether to enable mTLS (defaults to False).

    Returns:
        An instantiated, ready-to-call Showcase client instance.
    """
    return conftest.construct_client(
        client_class,
        use_mtls=use_mtls,
        transport_name=transport,
        client_options=client_options,
    )


def run_echo_call(client: EchoClient, scenario: str):
    """Executes unary RPC requests against an injected EchoClient.

    This runner exercises the three standard unary RPC lifecycle scenarios:
    - 'Happy Path' / 'Tracing Off': Dispatches a successful unary EchoRequest.
    - 'Server Failure': Injects a non-retryable INVALID_ARGUMENT gRPC status on the
      Showcase server, expecting an immediate InvalidArgument or BadRequest exception.
    - 'Client Timeout': Enforces a tight client-side timeout (`SHORT_CLIENT_TIMEOUT_SECONDS`)
      with retries disabled, expecting a DeadlineExceeded or GatewayTimeout exception.

    Args:
        client: The instantiated EchoClient (injected by `execute_scenario`).
        scenario: The scenario name string from the CSV matrix row.
    """
    if scenario in ("Happy Path", "Tracing Off"):
        client.echo(showcase.EchoRequest(content="hello"))
    elif scenario == "Server Failure":
        with pytest.raises((exceptions.InvalidArgument, exceptions.BadRequest)):
            client.echo(
                showcase.EchoRequest(
                    error=status_pb2.Status(
                        code=code_pb2.INVALID_ARGUMENT,
                        message="Simulated unretryable invalid argument error.",
                    )
                )
            )
    elif scenario == "Client Timeout":
        with pytest.raises((exceptions.DeadlineExceeded, exceptions.GatewayTimeout)):
            client.echo(
                showcase.EchoRequest(
                    error=status_pb2.Status(
                        code=code_pb2.DEADLINE_EXCEEDED,
                        message="Client deadline exceeded",
                    )
                ),
                timeout=SHORT_CLIENT_TIMEOUT_SECONDS,
                retry=None,
            )


def run_sequence_retry_call(
    client: SequenceServiceClient,
    scenario: str,
    exporter: InMemorySpanExporter,
):
    """Executes stateful retry sequence requests against an injected SequenceServiceClient.

    The Showcase SequenceService allows configuring a server-side queue of pre-programmed
    responses that return sequentially across consecutive attempt RPCs.

    Execution Flow:
    1. Pre-programs the server-side sequence queue via `create_sequence`:
       - 'Retries Exhausted': Configures an array of UNAVAILABLE ('Persistent outage') responses
         and a tight deadline (`FAST_EXHAUSTION_DEADLINE_SECONDS`).
       - 'Retry with Recovery': Configures one UNAVAILABLE ('Temporary glitch') response
         followed by an OK response, and a generous deadline (`GENEROUS_RECOVERY_DEADLINE_SECONDS`).
    2. Flushes the in-memory span exporter (`exporter.clear()`).
       CRITICAL: The `create_sequence` setup call emits its own OpenTelemetry spans!
       Purging the exporter ensures that downstream assertions strictly evaluate spans emitted
       by the target `attempt_sequence` call.
    3. Invokes `attempt_sequence` with a custom fast Retry policy.
       Uses `contextlib.nullcontext()` as a "do-nothing" placeholder so we can run the test
       call using a single `with expectation:` block. If we expect the call to fail, `expectation`
       is `pytest.raises(...)` to catch the error. If we expect it to succeed, `expectation` is
       `nullcontext()`, which just lets the code run normally. This saves us from having to
       write out the client call twice!

    Args:
        client: The instantiated SequenceServiceClient (injected by `execute_scenario`).
        scenario: The scenario name string from the CSV matrix row.
        exporter: The active span exporter used to purge pre-flight setup spans.
    """
    is_exhaust = scenario == "Retries Exhausted"

    if is_exhaust:
        responses = [
            Sequence.Response(
                status=status_pb2.Status(
                    code=code_pb2.UNAVAILABLE,
                    message="Persistent outage",
                )
            )
        ] * SHOWCASE_EXHAUSTION_QUEUE_BUFFER
        deadline = FAST_EXHAUSTION_DEADLINE_SECONDS
        expectation = pytest.raises(
            (exceptions.RetryError, exceptions.ServiceUnavailable)
        )
    else:
        responses = [
            Sequence.Response(
                status=status_pb2.Status(
                    code=code_pb2.UNAVAILABLE,
                    message="Temporary glitch",
                )
            ),
            Sequence.Response(status=status_pb2.Status(code=code_pb2.OK)),
        ]
        deadline = GENEROUS_RECOVERY_DEADLINE_SECONDS
        expectation = contextlib.nullcontext()

    # Step 1: Pre-program response sequence on the Showcase daemon
    seq = client.create_sequence(
        CreateSequenceRequest(sequence=Sequence(responses=responses))
    )

    # Step 2: Flush setup RPC spans so assertions evaluate only attempt_sequence
    exporter.clear()

    # Step 3: Configure fast retry policy and execute sequence attempts
    retry_policy = retries.Retry(
        predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
        initial=FAST_RETRY_BACKOFF_SECONDS,
        maximum=FAST_RETRY_BACKOFF_SECONDS,
        multiplier=CONSTANT_BACKOFF_MULTIPLIER,
        deadline=deadline,
    )

    with expectation:
        client.attempt_sequence(
            AttemptSequenceRequest(name=seq.name),
            retry=retry_policy,
        )


def execute_scenario(
    scenario: str,
    transport_str: str,
    provider: TracerProvider,
    exporter: InMemorySpanExporter,
    monkeypatch: pytest.MonkeyPatch,
):
    """High-level scenario dispatcher and Dependency Injection (DI) coordinator.

    Responsibilities:
    1. Normalizes transport strings ('grpc' vs 'rest').
    2. Injects the TracerProvider into `ClientOptions` (or unsets it for 'Tracing Off').
    3. Handles scenario-specific environment configuration via `monkeypatch`.
    4. Instantiates the appropriate client class (`EchoClient` vs `SequenceServiceClient`).
    5. Dispatches execution to the corresponding runner (`run_echo_call` or `run_sequence_retry_call`).

    Args:
        scenario: The scenario column value from the CSV matrix row.
        transport_str: The transport column value ('gRPC' or 'REST').
        provider: The active OpenTelemetry TracerProvider.
        exporter: The active InMemorySpanExporter.
        monkeypatch: Pytest monkeypatch fixture for environment variable scoping.
    """
    transport = "grpc" if "grpc" in transport_str.lower() else "rest"
    client_options = ClientOptions(tracer_provider=provider)

    if scenario == "Tracing Off":
        monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")
        client_options = ClientOptions()

    if scenario in ("Happy Path", "Server Failure", "Client Timeout", "Tracing Off"):
        client = construct_observability_client(EchoClient, transport, client_options)
        run_echo_call(client, scenario)
    else:
        client = construct_observability_client(
            SequenceServiceClient, transport, client_options
        )
        run_sequence_retry_call(client, scenario, exporter)


# ---------------------------------------------------------------------------
# Universal Matrix-Driven Cell Parser & Assertion Engine
# ---------------------------------------------------------------------------


def resolve_expected_value(
    raw_val: str | None, target_tier: str, attempt_idx: int = 0
) -> str:
    """Resolves the expected value from a CSV cell using the matrix mini-grammar.

    The CSV requirements matrix uses a compact domain-specific language (DSL) to encode
    expectations across different span tiers (T3 vs T4) and retry attempt sequences
    without exploding the number of columns.

    Supported Syntax Patterns:
    --------------------------
    1. Static Values:
       - '200', 'POST', 'INTERNAL', 'NOT SET', 'N/A'
       - Directly returns the string literal when the expected value is identical everywhere.

    2. Positional Sequences (Across Retry Attempts):
       - '503 | 200'
       - 'ERROR | OK'
       - When a call retries, each try (attempt 0, attempt 1, etc.) can produce a different result.
         For example, the first try might fail with 503, but the second try succeeds with 200.
       - The pipe ('|') separates what we expect on each consecutive try:
         * Attempt 0 checks the 1st item ('503').
         * Attempt 1 checks the 2nd item ('200').
       - If there are more attempts than values listed (like a loop that keeps failing 20 times),
         it holds onto the last item in the list.

    3. Tier-Partitioned Expressions (Per-Layer Rules):
       - 'T3: OK | T4: NOT SET'
       - 'T3: UNSET | T4: ERROR | OK'
       - A single row in our matrix often checks an attribute that behaves differently depending
         on which layer of the software we look at:
         * Tier 3 (T3): The outer, overall operation span.
         * Tier 4 (T4): The inner, individual network attempt spans.
       - We label each tier with 'T3:' or 'T4:', followed by the value (or positional sequence)
         for that tier:
         * 'T3: OK | T4: NOT SET' means: "The outer T3 span should be OK, but every inner T4
           attempt span should NOT have this attribute set."
         * 'T3: UNSET | T4: ERROR | OK' means: "The outer T3 span should be UNSET, while the T4
           spans will see an ERROR on the 1st try and OK on the 2nd try."
       - If a tier is not mentioned in the cell, it returns 'N/A' (meaning that tier doesn't care
         about this attribute in this test).

    Args:
        raw_val: Raw string content from the CSV cell (or None if empty).
        target_tier: The span tier currently being evaluated ('T3' or 'T4').
        attempt_idx: Zero-based attempt index for child T4 spans (defaults to 0 for T3).

    Returns:
        The resolved expected string value (e.g. 'OK', 'NOT SET', 'N/A').
    """
    if raw_val is None:
        return "N/A"
    raw = raw_val.strip()
    if not raw or raw == "N/A":
        return "N/A"

    # Step 1: Check for tier partitioning (T3: ... | T4: ...)
    tier_content = raw
    if "T3:" in raw or "T4:" in raw:
        if target_tier == "T3":
            if "T3:" in raw:
                after_t3 = raw.split("T3:")[1]
                tier_content = after_t3.split("| T4:")[0].strip()
            else:
                return "N/A"
        elif target_tier == "T4":
            if "T4:" in raw:
                tier_content = raw.split("T4:")[1].strip()
            else:
                return "N/A"

    # Step 2: Handle positional sequence across attempts (e.g. '503 | 200')
    if "|" in tier_content:
        parts = [p.strip() for p in tier_content.split("|")]
        return parts[attempt_idx] if attempt_idx < len(parts) else parts[-1]

    return tier_content.strip()


# OpenTelemetry attributes validated as strings
STRING_ATTRIBUTES = [
    "rpc.system.name",
    "rpc.method",
    "rpc.response.status_code",
    "http.request.method",
    "url.domain",
    "url.template",
    "server.address",
    "error.type",
]

# OpenTelemetry attributes validated as exact integer types
INTEGER_ATTRIBUTES = [
    "http.response.status_code",
    "rpc.grpc.status_code",
    "server.port",
]


def _assert_attribute(
    span,
    attr: str,
    raw_expected: str | None,
    target_tier: str,
    attempt_idx: int = 0,
    comparator=None,
):
    """Universal triage helper for single-attribute validation against a matrix cell.

    This helper standardizes attribute verification across all sub-validators:
    - 'N/A': Skips assertion (attribute is irrelevant or not applicable to this scenario).
    - 'NOT SET': Enforces negative assertion, verifying the key is completely absent
      from `span.attributes`.
    - Present values: Asserts presence, then applies either a custom comparator callback
      (e.g. for wildcard prefixes or integer parsing) or default strict equality.

    Args:
        span: The OpenTelemetry ReadableSpan instance being evaluated.
        attr: The attribute name key (e.g. 'rpc.system.name').
        raw_expected: The raw string value from the CSV row cell.
        target_tier: The span tier being evaluated ('T3' or 'T4').
        attempt_idx: Zero-based attempt index for child spans (0 for root).
        comparator: Optional callable `comparator(actual, expected)` for custom validation.
    """
    expected = resolve_expected_value(raw_expected, target_tier, attempt_idx)
    if expected == "N/A":
        return

    if expected == "NOT SET":
        assert attr not in span.attributes, (
            f"Attribute {attr} should NOT be set on {target_tier} attempt {attempt_idx}, "
            f"found: {span.attributes.get(attr)}"
        )
        return

    actual = span.attributes.get(attr)
    assert actual is not None, (
        f"Attribute {attr} missing on {target_tier} attempt {attempt_idx}, "
        f"expected '{expected}'"
    )

    if comparator:
        comparator(actual, expected)
    else:
        assert actual == expected, (
            f"Attribute {attr} on {target_tier} attempt {attempt_idx}: "
            f"expected '{expected}', got '{actual}'"
        )


def _assert_span_metadata(
    span, row: dict[str, str], target_tier: str, attempt_idx: int
):
    """Validates top-level span header fields (Name, Kind, and Status Code).

    Args:
        span: The OpenTelemetry ReadableSpan being validated.
        row: The CSV requirements dictionary for this feature.
        target_tier: 'T3' (root operation) or 'T4' (child attempt).
        attempt_idx: Zero-based attempt index.
    """
    metadata_fields = (
        ("Span Name", span.name, "Span name"),
        ("Span Kind", span.kind.name, "Span kind"),
        ("Span Status", span.status.status_code.name, "Span status"),
    )
    for col, actual, label in metadata_fields:
        expected = resolve_expected_value(row.get(col), target_tier, attempt_idx)
        if expected != "N/A":
            assert actual == expected, (
                f"{label} mismatch on {target_tier} attempt {attempt_idx}: "
                f"expected '{expected}', got '{actual}'"
            )


def _assert_string_attributes(
    span, row: dict[str, str], target_tier: str, attempt_idx: int
):
    """Validates string OpenTelemetry attributes with wildcard prefix support.

    Supports wildcard templates in the matrix (e.g. 'http://localhost:7469/v1beta1/echo:echo/*')
    by checking `startswith` when an expected value ends with '/*'.

    Args:
        span: The OpenTelemetry ReadableSpan being validated.
        row: The CSV requirements dictionary for this feature.
        target_tier: 'T3' or 'T4'.
        attempt_idx: Zero-based attempt index.
    """

    def _match_string(actual: Any, expected: str):
        if expected.endswith("/*"):
            prefix = expected[:-1]
            assert str(actual).startswith(prefix), (
                f"Expected attribute to start with '{prefix}', got '{actual}'"
            )
        else:
            assert actual == expected, f"Expected '{expected}', got '{actual}'"

    for attr in STRING_ATTRIBUTES:
        _assert_attribute(
            span,
            attr,
            row.get(attr),
            target_tier,
            attempt_idx,
            comparator=_match_string,
        )


def _assert_integer_attributes(
    span, row: dict[str, str], target_tier: str, attempt_idx: int
):
    """Validates integer OpenTelemetry attributes (e.g. status codes, ports).

    Enforces strict integer type conversion to prevent false positives where string
    values might accidentally pass comparison.

    Args:
        span: The OpenTelemetry ReadableSpan being validated.
        row: The CSV requirements dictionary for this feature.
        target_tier: 'T3' or 'T4'.
        attempt_idx: Zero-based attempt index.
    """

    def _match_int(actual: Any, expected: str):
        assert actual == int(expected), f"Expected {expected}, got {actual}"

    for attr in INTEGER_ATTRIBUTES:
        _assert_attribute(
            span,
            attr,
            row.get(attr),
            target_tier,
            attempt_idx,
            comparator=_match_int,
        )


def _assert_status_message(
    span, row: dict[str, str], target_tier: str, attempt_idx: int
):
    """Validates status.message via substring containment matching.

    Because gRPC and REST backends format error message payloads slightly differently,
    the matrix specifies key error phrases (e.g. 'Persistent outage') that must appear
    inside the captured `status.message` attribute.

    Args:
        span: The OpenTelemetry ReadableSpan being validated.
        row: The CSV requirements dictionary for this feature.
        target_tier: 'T3' or 'T4'.
        attempt_idx: Zero-based attempt index.
    """

    def _match_message(actual: Any, expected: str):
        assert expected in str(actual), (
            f"Expected '{expected}' in status.message '{actual}'"
        )

    _assert_attribute(
        span,
        "status.message",
        row.get("status.message"),
        target_tier,
        attempt_idx,
        comparator=_match_message,
    )


def _assert_resend_count(span, row: dict[str, str], target_tier: str, attempt_idx: int):
    """Validates retry resend counts across HTTP and gRPC attribute variations.

    Protocol Discrepancies Handled:
    - HTTP / REST spans record resend counts under `http.request.resend_count`.
    - gRPC spans record resend counts under `gcp.grpc.resend_count`.

    Dynamic Index Token ('attempt_index'):
    - Attempt 0 (initial request): Resend count must be NOT SET (initial call is not a retry).
    - Attempt N (N > 0): Resend count must equal integer N.

    Args:
        span: The OpenTelemetry ReadableSpan being validated.
        row: The CSV requirements dictionary for this feature.
        target_tier: 'T3' or 'T4'.
        attempt_idx: Zero-based attempt index.
    """
    expected_resend = resolve_expected_value(
        row.get("resend_count"), target_tier, attempt_idx
    )
    if expected_resend == "attempt_index":
        expected_resend = "NOT SET" if attempt_idx == 0 else str(attempt_idx)

    if expected_resend == "NOT SET":
        assert "http.request.resend_count" not in span.attributes
        assert "gcp.grpc.resend_count" not in span.attributes
    elif expected_resend != "N/A":
        actual_resend = span.attributes.get(
            "http.request.resend_count"
        ) or span.attributes.get("gcp.grpc.resend_count")
        assert actual_resend is not None, (
            f"Resend count missing on {target_tier} attempt {attempt_idx}, "
            f"expected {expected_resend}"
        )
        assert actual_resend == int(expected_resend), (
            f"Resend count on {target_tier} attempt {attempt_idx}: "
            f"expected {expected_resend}, got {actual_resend}"
        )


def assert_span_matches_row(
    span, row: dict[str, str], target_tier: str, attempt_idx: int = 0
):
    """Master validator delegating span verification across specialized sub-validators.

    Coordinates verification of:
    1. Top-level Span Metadata (Name, Kind, Status)
    2. String Attributes (System, Method, URL, Error Type)
    3. Integer Attributes (HTTP / gRPC Status Codes, Port)
    4. Status Error Message (Substring containment)
    5. Retry Resend Count (Protocol-aware retry progression)

    Args:
        span: The OpenTelemetry ReadableSpan instance being checked.
        row: The CSV requirements dictionary for this feature.
        target_tier: 'T3' (logical operation) or 'T4' (wire attempt).
        attempt_idx: Zero-based attempt index (defaults to 0).
    """
    _assert_span_metadata(span, row, target_tier, attempt_idx)
    _assert_string_attributes(span, row, target_tier, attempt_idx)
    _assert_integer_attributes(span, row, target_tier, attempt_idx)
    _assert_status_message(span, row, target_tier, attempt_idx)
    _assert_resend_count(span, row, target_tier, attempt_idx)


# ---------------------------------------------------------------------------
# Parametrized Test Runner (22 Features)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "feature_id",
    list(FEATURE_MATRIX.keys()),
    ids=[
        f"{fid}_{FEATURE_MATRIX[fid]['Feature Name'].replace(' ', '_')}"
        for fid in FEATURE_MATRIX
    ],
)
def test_feature(feature_id: str, span_exporter, monkeypatch):
    """Executes a single observability scenario and validates 1-to-1 against matrix specifications.

    Test Lifecycle:
    ---------------
    1. Execute Scenario:
       Invokes `execute_scenario` to dispatch unary or retry requests to the live Showcase server.
    2. Capture Spans:
       Retrieves all finished spans from the in-memory exporter and archives them into
       `RAW_SPANS_CATALOG` for diagnostic output.
    3. Handle 'Tracing Off':
       If the row specifies 'Span Count = 0', asserts that zero spans were produced.
    4. Span Partitioning:
       Partitions captured spans into root spans (`parent is None`, representing T3)
       and child spans (`parent is not None`, representing T4).
    5. Evaluate T3 Root Span:
       Verifies that exactly 1 root span was emitted (if required by Tier) and validates
       its metadata and attributes.
    6. Evaluate T4 Child Spans:
       Verifies child span cardinality, evaluates each attempt sequentially against
       positional expectations, and validates the parent-child span ID linkage invariant.

    Args:
        feature_id: Unique matrix identifier (e.g. 'grpc_happy_path', 'rest_retry_recovery').
        span_exporter: Isolated test fixture yielding (exporter, provider).
        monkeypatch: Pytest environment variable isolation fixture.
    """
    row = FEATURE_MATRIX[feature_id]
    exporter, provider = span_exporter

    # Phase 1: Execute physical scenario against Showcase daemon
    execute_scenario(row["Scenario"], row["Transport"], provider, exporter, monkeypatch)
    spans = exporter.get_finished_spans()

    # Phase 2: Archive raw spans in memory for end-of-session JSON diagnostic dump
    RAW_SPANS_CATALOG[feature_id] = [json.loads(s.to_json()) for s in spans]

    # Phase 3: Verify Tracing Off scenarios emit zero telemetry
    if row["Span Count"] == "0":
        assert len(spans) == 0, f"Expected 0 spans for {feature_id}, found {len(spans)}"
        return

    # Phase 4: Partition captured spans into Root (T3) and Child (T4) attempts
    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]

    tier = row["Tier"]

    # Phase 5: Evaluate Root T3 Span (if applicable)
    if tier in ("T3", "T3 + T4"):
        assert len(t3_spans) == 1, f"Expected 1 T3 root span, got {len(t3_spans)}"
        assert_span_matches_row(t3_spans[0], row, target_tier="T3", attempt_idx=0)

    # Phase 6: Evaluate Child T4 Spans (if applicable)
    if tier in ("T4", "T3 + T4"):
        expected_count = row["Span Count"]
        if expected_count.isdigit():
            expected_t4_count = (
                int(expected_count) if tier == "T4" else int(expected_count) - 1
            )
            assert len(t4_spans) == expected_t4_count, (
                f"Expected {expected_t4_count} T4 child spans, got {len(t4_spans)}"
            )
        else:
            # Dynamic count for retries exhausted (N attempts + 1 root >= 2 children)
            assert len(t4_spans) >= 2, (
                f"Expected >=2 T4 child spans, got {len(t4_spans)}"
            )

        for idx, child in enumerate(t4_spans):
            assert_span_matches_row(child, row, target_tier="T4", attempt_idx=idx)
            # Hierarchy Invariant: child span must point to root T3 span ID as its parent
            if t3_spans:
                assert child.parent.span_id == t3_spans[0].context.span_id


# ---------------------------------------------------------------------------
# Session Teardown: Raw Spans Archival
# ---------------------------------------------------------------------------


def test_z_dump_raw_spans():
    """Serializes all captured raw spans to raw_spans_output.json for audit and review.

    Named with 'test_z_' prefix to guarantee it runs after all 22 feature tests have
    populated `RAW_SPANS_CATALOG`. This generated JSON file serves as an immutable
    diagnostic artifact showing every span's exact attributes, timing, and hierarchy.
    """
    output_path = Path(__file__).parent / "raw_spans_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(RAW_SPANS_CATALOG, f, indent=2)
