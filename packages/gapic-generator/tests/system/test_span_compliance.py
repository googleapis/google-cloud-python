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
# 1-to-1 Span Assertions
# ---------------------------------------------------------------------------


def assert_span_matches_row(span, row: dict[str, str]):
    """Validates a single span against its row specification in the matrix."""
    if row["Span Name"] != "N/A":
        assert span.name == row["Span Name"]
    if row["Span Kind"] != "N/A":
        assert span.kind.name == row["Span Kind"]
    if row["Span Status"] != "N/A":
        assert span.status.status_code.name == row["Span Status"]

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
        "status.message",
    ]
    for attr in str_attrs:
        expected = row.get(attr, "N/A")
        if expected == "NOT SET":
            assert attr not in span.attributes, (
                f"Attribute {attr} should NOT be set, found: {span.attributes.get(attr)}"
            )
        elif expected != "N/A":
            actual = span.attributes.get(attr)
            assert actual == expected, (
                f"Attribute {attr}: expected '{expected}', got '{actual}'"
            )

    # Integer attributes
    int_attrs = [
        "http.response.status_code",
        "rpc.grpc.status_code",
        "server.port",
    ]
    for attr in int_attrs:
        expected = row.get(attr, "N/A")
        if expected == "NOT SET":
            assert attr not in span.attributes, (
                f"Attribute {attr} should NOT be set, found: {span.attributes.get(attr)}"
            )
        elif expected != "N/A":
            actual = span.attributes.get(attr)
            assert actual == int(expected), (
                f"Attribute {attr}: expected {expected}, got {actual}"
            )

    # Resend count
    resend_expected = row.get("resend_count", "N/A")
    if resend_expected == "NOT SET":
        assert "http.request.resend_count" not in span.attributes
        assert "gcp.grpc.resend_count" not in span.attributes

    # Parentage
    parent_expected = row.get("parent_span_id", "N/A")
    if parent_expected == "None (Root)":
        assert span.parent is None, (
            f"Expected root span with no parent, got {span.parent}"
        )
    elif parent_expected == "T3.span_id":
        assert span.parent is not None, "Expected child span with parent, got None"


def assert_retry_child_spans(spans, row: dict[str, str]):
    """Validates T4 child retry spans for F1.5 and F1.10."""
    t4_spans = [s for s in spans if s.parent is not None]
    assert len(t4_spans) == 2, f"Expected 2 T4 child spans, got {len(t4_spans)}"
    t4_1, t4_2 = t4_spans[0], t4_spans[1]

    # Attempt 1 failed
    assert t4_1.status.status_code.name == "ERROR"
    if "grpc" in row["Transport"].lower():
        assert t4_1.attributes.get("rpc.grpc.status_code") == 14
        assert t4_2.status.status_code.name == "UNSET"
        assert t4_2.attributes.get("rpc.grpc.status_code") == 0
        assert t4_2.attributes.get("rpc.response.status_code") == "OK"
    else:
        assert t4_1.attributes.get("http.response.status_code") == 503
        assert t4_2.status.status_code.name == "OK"
        assert t4_2.attributes.get("http.response.status_code") == 200


def assert_retry_hierarchy_and_aggregation(spans, row: dict[str, str]):
    """Validates parent-child hierarchy and status aggregation for F3.1-F3.4."""
    t3_spans = [s for s in spans if s.parent is None]
    t4_spans = [s for s in spans if s.parent is not None]

    assert len(t3_spans) == 1, f"Expected 1 T3 root span, got {len(t3_spans)}"
    root = t3_spans[0]

    # Every child must reference the root span id
    for child in t4_spans:
        assert child.parent.span_id == root.context.span_id

    scenario = row["Scenario"]
    is_grpc = "grpc" in row["Transport"].lower()

    if scenario == "Retry Recovery":
        assert len(t4_spans) == 2, f"Expected 2 T4 child spans, got {len(t4_spans)}"
        t4_1, t4_2 = t4_spans[0], t4_spans[1]

        # Root aggregates success
        assert root.status.status_code.name == "UNSET"
        assert root.attributes.get("rpc.response.status_code") == "OK"
        assert "error.type" not in root.attributes

        # Child checks
        if is_grpc:
            assert t4_1.status.status_code.name == "ERROR"
            assert t4_1.attributes.get("rpc.grpc.status_code") == 14
            assert t4_2.status.status_code.name == "UNSET"
            assert t4_2.attributes.get("rpc.grpc.status_code") == 0
            assert t4_2.attributes.get("rpc.response.status_code") == "OK"
        else:
            assert t4_1.status.status_code.name == "ERROR"
            assert t4_1.attributes.get("http.response.status_code") == 503
            assert t4_2.status.status_code.name == "OK"
            assert t4_2.attributes.get("http.response.status_code") == 200

    elif scenario == "Retries Exhausted":
        assert len(t4_spans) >= 2, f"Expected >=2 T4 child spans, got {len(t4_spans)}"

        # Root aggregates error
        assert root.status.status_code.name == "ERROR"
        assert root.attributes.get("rpc.response.status_code") == "UNAVAILABLE"
        assert root.attributes.get("error.type") == "UNAVAILABLE"

        # All children failed
        for child in t4_spans:
            assert child.status.status_code.name == "ERROR"
            if is_grpc:
                assert child.attributes.get("rpc.grpc.status_code") == 14
            else:
                assert child.attributes.get("http.response.status_code") == 503


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

    # 3. Partition and Assert
    tier = row["Tier"]

    # Tracing Off scenarios emit 0 spans
    if row["Span Count"] == "0":
        assert len(spans) == 0, f"Expected 0 spans for {feature_id}, found {len(spans)}"
        return

    if tier == "T3":
        t3_spans = [s for s in spans if s.parent is None]
        assert len(t3_spans) == 1, f"Expected 1 T3 root span, got {len(t3_spans)}"
        assert_span_matches_row(t3_spans[0], row)

    elif tier == "T4":
        if row["Span Count"] == "2":
            assert_retry_child_spans(spans, row)
        else:
            t4_spans = [s for s in spans if s.parent is not None]
            assert len(t4_spans) == 1, f"Expected 1 T4 child span, got {len(t4_spans)}"
            assert_span_matches_row(t4_spans[0], row)

    elif tier == "T3 + T4":
        assert_retry_hierarchy_and_aggregation(spans, row)


# ---------------------------------------------------------------------------
# Session Teardown: Raw Spans Archival
# ---------------------------------------------------------------------------


def test_z_dump_raw_spans():
    """Dumps all captured raw spans to raw_spans_output.json for audit and review."""
    output_path = Path(__file__).parent / "raw_spans_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(RAW_SPANS_CATALOG, f, indent=2)
