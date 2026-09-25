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

Clean-slate implementation driven row-by-row by telemetry_requirements_matrix.csv.
Runs all 22 feature tests against the GAPIC Showcase daemon with 1-to-1 attribute assertions.
"""

from __future__ import annotations

import csv
import json
import os
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
from google.auth import credentials as ga_credentials
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
# CSV Matrix Loader & Global Archival
# ---------------------------------------------------------------------------

CSV_PATH = Path(__file__).parent / "telemetry_requirements_matrix.csv"


def load_feature_matrix() -> dict[str, dict[str, str]]:
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        return {r["Feature ID"]: r for r in csv.DictReader(f)}


FEATURE_MATRIX = load_feature_matrix()
RAW_SPANS_CATALOG: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Test Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def span_exporter():
    """Provides an isolated InMemorySpanExporter and TracerProvider for test assertions."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    old_env = os.environ.get("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED")
    os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "true"

    yield exporter, provider

    if old_env is not None:
        os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = old_env
    else:
        os.environ.pop("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", None)
    exporter.clear()


# ---------------------------------------------------------------------------
# RPC Invocation Runners
# ---------------------------------------------------------------------------


def run_echo_call(
    scenario: str,
    transport: str,
    client_options: ClientOptions,
    use_mtls: bool,
):
    """Executes unary RPC calls against EchoClient."""
    client = conftest.construct_client(
        EchoClient,
        transport_name=transport,
        use_mtls=use_mtls,
        client_options=client_options,
        credentials=ga_credentials.AnonymousCredentials(),
    )
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
                timeout=0.2,
                retry=None,
            )


def run_sequence_retry_call(
    scenario: str,
    transport: str,
    client_options: ClientOptions,
    use_mtls: bool,
    exporter: InMemorySpanExporter,
):
    """Executes retry sequences against SequenceServiceClient."""
    client = conftest.construct_client(
        SequenceServiceClient,
        transport_name=transport,
        use_mtls=use_mtls,
        client_options=client_options,
        credentials=ga_credentials.AnonymousCredentials(),
    )
    is_exhaust = scenario == "Retries Exhausted"
    if is_exhaust:
        responses = [
            Sequence.Response(
                status=status_pb2.Status(
                    code=code_pb2.UNAVAILABLE,
                    message="Persistent outage",
                )
            )
            for _ in range(20)
        ]
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

    seq = client.create_sequence(
        CreateSequenceRequest(sequence=Sequence(responses=responses))
    )
    # Clear setup RPC spans so exporter captures only the attempt_sequence spans
    exporter.clear()

    if is_exhaust:
        retry_policy = retries.Retry(
            predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
            initial=0.01,
            maximum=0.01,
            multiplier=1.0,
            deadline=0.05,
        )
        with pytest.raises((exceptions.RetryError, exceptions.ServiceUnavailable)):
            client.attempt_sequence(
                AttemptSequenceRequest(name=seq.name),
                retry=retry_policy,
            )
    else:
        retry_policy = retries.Retry(
            predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
            initial=0.01,
            maximum=0.05,
            multiplier=1.0,
            deadline=5.0,
        )
        client.attempt_sequence(
            AttemptSequenceRequest(name=seq.name),
            retry=retry_policy,
        )


def execute_scenario(
    scenario: str,
    transport_str: str,
    provider: TracerProvider,
    exporter: InMemorySpanExporter,
    use_mtls: bool,
):
    """Dispatches execution based on the scenario column in the requirements matrix."""
    transport = "grpc" if "grpc" in transport_str.lower() else "rest"
    client_options = ClientOptions(tracer_provider=provider)

    if scenario == "Tracing Off":
        os.environ["GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"] = "false"
        client_options = ClientOptions()
        run_echo_call(scenario, transport, client_options, use_mtls)
    elif scenario in ("Happy Path", "Server Failure", "Client Timeout"):
        run_echo_call(scenario, transport, client_options, use_mtls)
    else:
        run_sequence_retry_call(scenario, transport, client_options, use_mtls, exporter)


# ---------------------------------------------------------------------------
# Universal Matrix-Driven Cell Parser & Assertion Engine
# ---------------------------------------------------------------------------


def resolve_expected_value(
    raw_val: str | None, target_tier: str, attempt_idx: int = 0
) -> str:
    """Resolves the expected value from a CSV cell for a given tier and attempt index.

    Supports:
    1. Static values: '200', 'POST', 'NOT SET', 'N/A'
    2. Positional sequences: '503 | 200', 'ERROR | OK'
    3. Tier-partitioned cells: 'T3: OK | T4: NOT SET', 'T3: UNSET | T4: ERROR | OK'
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

    # Step 2: Handle sequence across attempts (e.g. '503 | 200')
    if "|" in tier_content:
        parts = [p.strip() for p in tier_content.split("|")]
        return parts[attempt_idx] if attempt_idx < len(parts) else parts[-1]

    return tier_content.strip()


def assert_span_matches_row(
    span, row: dict[str, str], target_tier: str, attempt_idx: int = 0
):
    """Validates a single span against row specifications for the given tier and attempt index."""
    span_name = resolve_expected_value(row.get("Span Name"), target_tier, attempt_idx)
    if span_name != "N/A":
        assert span.name == span_name, (
            f"Span name mismatch on {target_tier} attempt {attempt_idx}: "
            f"expected '{span_name}', got '{span.name}'"
        )

    span_kind = resolve_expected_value(row.get("Span Kind"), target_tier, attempt_idx)
    if span_kind != "N/A":
        assert span.kind.name == span_kind, (
            f"Span kind mismatch on {target_tier} attempt {attempt_idx}: "
            f"expected '{span_kind}', got '{span.kind.name}'"
        )

    span_status = resolve_expected_value(
        row.get("Span Status"), target_tier, attempt_idx
    )
    if span_status != "N/A":
        assert span.status.status_code.name == span_status, (
            f"Span status mismatch on {target_tier} attempt {attempt_idx}: "
            f"expected '{span_status}', got '{span.status.status_code.name}'"
        )

    # String attributes
    str_attrs = [
        "rpc.system.name",
        "rpc.method",
        "rpc.response.status_code",
        "http.request.method",
        "url.domain",
        "url.template",
        "server.address",
        "error.type",
    ]
    for attr in str_attrs:
        expected = resolve_expected_value(row.get(attr), target_tier, attempt_idx)
        if expected == "NOT SET":
            assert attr not in span.attributes, (
                f"Attribute {attr} should NOT be set on {target_tier} attempt {attempt_idx}, "
                f"found: {span.attributes.get(attr)}"
            )
        elif expected != "N/A":
            actual = span.attributes.get(attr)
            assert actual is not None, (
                f"Attribute {attr} missing on {target_tier} attempt {attempt_idx}, "
                f"expected '{expected}'"
            )
            if expected.endswith("/*"):
                prefix = expected[:-1]
                assert str(actual).startswith(prefix), (
                    f"Attribute {attr} on {target_tier} attempt {attempt_idx}: "
                    f"expected to start with '{prefix}', got '{actual}'"
                )
            else:
                assert actual == expected, (
                    f"Attribute {attr} on {target_tier} attempt {attempt_idx}: "
                    f"expected '{expected}', got '{actual}'"
                )

    # Status message (matches exact or substring to allow URL paths)
    expected_msg = resolve_expected_value(
        row.get("status.message"), target_tier, attempt_idx
    )
    if expected_msg == "NOT SET":
        assert "status.message" not in span.attributes
    elif expected_msg != "N/A":
        actual_msg = span.attributes.get("status.message")
        assert actual_msg is not None, (
            f"Expected status.message containing '{expected_msg}', got None"
        )
        assert expected_msg in actual_msg, (
            f"status.message on {target_tier} attempt {attempt_idx}: "
            f"expected '{expected_msg}' in '{actual_msg}'"
        )

    # Integer attributes
    int_attrs = [
        "http.response.status_code",
        "rpc.grpc.status_code",
        "server.port",
    ]
    for attr in int_attrs:
        expected = resolve_expected_value(row.get(attr), target_tier, attempt_idx)
        if expected == "NOT SET":
            assert attr not in span.attributes, (
                f"Attribute {attr} should NOT be set on {target_tier} attempt {attempt_idx}, "
                f"found: {span.attributes.get(attr)}"
            )
        elif expected != "N/A":
            actual = span.attributes.get(attr)
            assert actual == int(expected), (
                f"Attribute {attr} on {target_tier} attempt {attempt_idx}: "
                f"expected {expected}, got {actual}"
            )

    # Resend count
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
        assert actual_resend == int(expected_resend), (
            f"Resend count on {target_tier} attempt {attempt_idx}: "
            f"expected {expected_resend}, got {actual_resend}"
        )


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
def test_feature(feature_id: str, span_exporter, use_mtls):
    """Executes each feature scenario and validates 1-to-1 against matrix specifications."""
    row = FEATURE_MATRIX[feature_id]
    exporter, provider = span_exporter

    # 1. Execute physical scenario
    execute_scenario(row["Scenario"], row["Transport"], provider, exporter, use_mtls)
    spans = exporter.get_finished_spans()

    # 2. Archive raw spans for downstream inspection
    RAW_SPANS_CATALOG[feature_id] = [json.loads(s.to_json()) for s in spans]

    # Tracing Off scenarios emit 0 spans
    if row["Span Count"] == "0":
        assert len(spans) == 0, f"Expected 0 spans for {feature_id}, found {len(spans)}"
        return

    # 3. Partition Spans into Root (T3) and Children (T4)
    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]

    tier = row["Tier"]

    # 4. Evaluate Root T3 Span (if applicable)
    if tier in ("T3", "T3 + T4"):
        assert len(t3_spans) == 1, f"Expected 1 T3 root span, got {len(t3_spans)}"
        assert_span_matches_row(t3_spans[0], row, target_tier="T3", attempt_idx=0)

    # 5. Evaluate Child T4 Spans (if applicable)
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
            # For N + 1 exhausted retries
            assert len(t4_spans) >= 2, (
                f"Expected >=2 T4 child spans, got {len(t4_spans)}"
            )

        for idx, child in enumerate(t4_spans):
            assert_span_matches_row(child, row, target_tier="T4", attempt_idx=idx)
            # Hierarchy Invariant: child must point to root T3 span
            if t3_spans:
                assert child.parent.span_id == t3_spans[0].context.span_id


# ---------------------------------------------------------------------------
# Session Teardown: Raw Spans Archival
# ---------------------------------------------------------------------------


def test_z_dump_raw_spans():
    """Dumps all captured raw spans to raw_spans_output.json for audit and review."""
    output_path = Path(__file__).parent / "raw_spans_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(RAW_SPANS_CATALOG, f, indent=2)
