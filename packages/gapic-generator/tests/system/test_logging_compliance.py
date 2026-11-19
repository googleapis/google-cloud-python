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

"""Operational Error Logging Compliance Suite (`F4` & `F5`).

Executes declarative, Tidy Data specification rows from
`logging_requirements_matrix.csv` against a live GAPIC Showcase server across
synchronous and asynchronous gRPC and HTTP/REST transports.
"""

from __future__ import annotations

import fnmatch
import json
import logging
import os
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from typing import Any

import pytest

try:
    from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from opentelemetry.trace import SpanKind

    HAS_OPENTELEMETRY = True
except ImportError:
    HAS_OPENTELEMETRY = False

if not HAS_OPENTELEMETRY:
    pytest.skip("OpenTelemetry is not installed", allow_module_level=True)

try:
    from google.api_core import client_logging
    from google.api_core.client_logging import StructuredLogFormatter

    HAS_ERROR_LOGGING = hasattr(client_logging, "is_error_logging_enabled")
except ImportError:
    HAS_ERROR_LOGGING = False

if not HAS_ERROR_LOGGING:
    pytest.skip(
        "Installed google-api-core lacks Operational Error Logging",
        allow_module_level=True,
    )

from google.api_core.client_options import ClientOptions

try:
    from . import conftest
    from .showcase_harness import (
        HAS_ASYNC_CLIENTS,
        InMemoryLogCapture,
        execute_showcase_scenario,
        execute_showcase_scenario_async,
        load_csv_matrix,
    )
except (ImportError, ValueError):
    import conftest
    from showcase_harness import (
        HAS_ASYNC_CLIENTS,
        InMemoryLogCapture,
        execute_showcase_scenario,
        execute_showcase_scenario_async,
        load_csv_matrix,
    )

LOGGING_MATRIX_CSV = Path(__file__).parent / "logging_requirements_matrix.csv"
LOGGING_MATRIX_ROWS = load_csv_matrix(LOGGING_MATRIX_CSV)


BASE_GOOGLE_LOGGER_NAME = "google"
OBSERVABILITY_LOGGER_NAME = "google.api_core._observability"
ENV_LOGGING_SCOPE = "GOOGLE_SDK_PYTHON_LOGGING_SCOPE"
ENV_LOGGING_ENABLED = "GOOGLE_SDK_EXPERIMENTAL_PYTHON_LOGGING_ENABLED"
ENV_TRACING_ENABLED = "GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"
ENV_RAW_LOGS_OUTPUT_PATH = "SHOWCASE_RAW_LOGS_OUTPUT_PATH"
ENV_RAW_LOGGING_SPANS_OUTPUT_PATH = "SHOWCASE_RAW_LOGGING_SPANS_OUTPUT_PATH"

EXACT_OR_GLOB_ATTRIBUTES = (
    "rpc.system.name",
    "rpc.response.status_code",
    "rpc.method",
    "url.full",
    "error.type",
    "gcp.errors.domain",
    "gcp.errors.metadata.zone",
    "status.message",
    "exception.message",
)

ASYNC_OVERRIDE_COLUMNS = frozenset(
    {
        "Message Prefix",
        "error.type",
        "status.message",
        "exception.type",
        "exception.message",
    }
)

CLOUD_LOGGING_TRACE_KEYS = (
    "logging.googleapis.com/trace",
    "logging.googleapis.com/spanId",
    "logging.googleapis.com/trace_sampled",
)

TelemetryHarness = tuple[InMemoryLogCapture, InMemorySpanExporter, TracerProvider]
RawLogsCatalog = dict[str, list[dict[str, Any]]]
RawSpansCatalog = dict[str, list[dict[str, Any]]]


def _expected_value(row: Mapping[str, str], column: str, *, is_async: bool) -> str:
    """Resolves the expected CSV value for `column`, using the Async override when applicable."""
    if is_async and column in ASYNC_OVERRIDE_COLUMNS:
        return row[f"Async {column}"]
    return row[column]


def _param_id(row: Mapping[str, str], *, prefix: str = "") -> str:
    """Formats a readable pytest parameter ID from a matrix row."""
    slug = row["Feature Name"].replace(" ", "_")
    return f"{prefix}{row['Feature ID']}_{slug}"


@pytest.fixture(scope="session")
def raw_logs_catalog(
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[RawLogsCatalog]:
    """Collects structured JSON logs per feature and writes them hermetically at teardown."""
    catalog: RawLogsCatalog = {}
    yield catalog
    if catalog:
        configured_path = os.environ.get(ENV_RAW_LOGS_OUTPUT_PATH)
        output_path = (
            Path(configured_path)
            if configured_path
            else tmp_path_factory.mktemp("showcase_logs") / "raw_logs_output.json"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(catalog, indent=2, sort_keys=True),
            encoding="utf-8",
        )


@pytest.fixture(scope="session")
def raw_spans_catalog(
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[RawSpansCatalog]:
    """Collects companion OpenTelemetry spans for active-trace logging cases at teardown."""
    catalog: RawSpansCatalog = {}
    yield catalog
    if catalog:
        configured_spans_path = os.environ.get(ENV_RAW_LOGGING_SPANS_OUTPUT_PATH)
        configured_logs_path = os.environ.get(ENV_RAW_LOGS_OUTPUT_PATH)
        if configured_spans_path:
            output_path = Path(configured_spans_path)
        elif configured_logs_path:
            output_path = (
                Path(configured_logs_path).parent / "raw_logging_spans_output.json"
            )
        else:
            output_path = (
                tmp_path_factory.mktemp("showcase_logs")
                / "raw_logging_spans_output.json"
            )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(catalog, indent=2, sort_keys=True),
            encoding="utf-8",
        )


@pytest.fixture
def telemetry_harness(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[TelemetryHarness]:
    """Provides isolated OpenTelemetry span capture and `"google"` logger capture."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    base_logger = logging.getLogger(BASE_GOOGLE_LOGGER_NAME)
    obs_logger = logging.getLogger(OBSERVABILITY_LOGGER_NAME)
    orig_base_level = base_logger.level
    orig_base_propagate = base_logger.propagate
    orig_base_handlers = list(base_logger.handlers)
    orig_obs_level = obs_logger.level
    orig_obs_propagate = obs_logger.propagate
    orig_obs_handlers = list(obs_logger.handlers)

    capture = InMemoryLogCapture(level=logging.NOTSET)
    # Keep "google" at WARNING so legacy GAPIC payload debug logging (`google.showcase_v1beta1.*`)
    # stays disabled unless explicitly configured, while child `google.api_core._observability`
    # controls L4 DEBUG vs L3 WARNING visibility cleanly.
    base_logger.handlers = [capture]
    base_logger.setLevel(logging.WARNING)
    base_logger.propagate = False
    obs_logger.setLevel(logging.NOTSET)
    obs_logger.handlers = []
    obs_logger.propagate = True

    monkeypatch.delenv(ENV_LOGGING_SCOPE, raising=False)
    monkeypatch.delenv(ENV_LOGGING_ENABLED, raising=False)
    monkeypatch.delenv(ENV_TRACING_ENABLED, raising=False)

    try:
        yield capture, exporter, provider
    finally:
        exporter.clear()
        capture.clear()
        obs_logger.setLevel(orig_obs_level)
        obs_logger.handlers = orig_obs_handlers
        obs_logger.propagate = orig_obs_propagate
        base_logger.handlers = orig_base_handlers
        base_logger.setLevel(orig_base_level)
        base_logger.propagate = orig_base_propagate


def _configure_environment_for_row(
    row: Mapping[str, str],
    monkeypatch: pytest.MonkeyPatch,
    provider: TracerProvider,
) -> ClientOptions:
    """Applies environment flags, logger level, and `ClientOptions` from a matrix row."""
    logging_enabled = row["Logging Enabled"] == "True"
    tracing_enabled = row["Tracing Enabled"] == "True"
    monkeypatch.setenv(
        ENV_LOGGING_ENABLED,
        "true" if logging_enabled else "false",
    )
    monkeypatch.setenv(
        ENV_TRACING_ENABLED,
        "true" if tracing_enabled else "false",
    )

    obs_logger = logging.getLogger(OBSERVABILITY_LOGGER_NAME)
    configured_level = getattr(logging, row["Configured Logger Level"])
    obs_logger.setLevel(configured_level)

    if tracing_enabled:
        return ClientOptions(tracer_provider=provider)
    return ClientOptions()


def _execute_row_sync(
    row: Mapping[str, str],
    capture: InMemoryLogCapture,
    exporter: InMemorySpanExporter,
    provider: TracerProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Executes a matrix row synchronously against Showcase."""
    client_options = _configure_environment_for_row(row, monkeypatch, provider)
    transport_name = "grpc" if row["Transport"] == "gRPC" else "rest"
    execute_showcase_scenario(
        row["Scenario"],
        transport_name,
        client_options,
        span_exporter=exporter,
        log_capture=capture,
        include_error_info=True,
    )


async def _execute_row_async(
    row: Mapping[str, str],
    capture: InMemoryLogCapture,
    exporter: InMemorySpanExporter,
    provider: TracerProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Executes a matrix row asynchronously (`grpc_asyncio` or `rest_asyncio`) against Showcase."""
    client_options = _configure_environment_for_row(row, monkeypatch, provider)
    transport_name = "grpc_asyncio" if row["Transport"] == "gRPC" else "rest_asyncio"
    await execute_showcase_scenario_async(
        row["Scenario"],
        transport_name,
        client_options,
        span_exporter=exporter,
        log_capture=capture,
        include_error_info=True,
    )


def _partition_tier_records(
    records: Sequence[logging.LogRecord], tier: str
) -> Sequence[logging.LogRecord]:
    """Selects captured records belonging to the target logging tier (`L4` or `L3`)."""
    expected_level = logging.DEBUG if tier == "L4" else logging.WARNING
    return [r for r in records if r.levelno == expected_level]


def _archive_records(
    catalog: RawLogsCatalog,
    feature_id: str,
    records: Sequence[logging.LogRecord],
) -> None:
    """Serializes captured records via `StructuredLogFormatter` into `catalog`."""
    formatter = StructuredLogFormatter()
    entries: list[dict[str, Any]] = []
    for record in records:
        payload = json.loads(formatter.format(record))
        payload["created_unix_nano"] = int(record.created * 1_000_000_000)
        entries.append(payload)
    catalog[feature_id] = entries


def _archive_spans(
    catalog: RawSpansCatalog,
    feature_id: str,
    spans: Sequence[ReadableSpan],
) -> None:
    """Serializes captured OpenTelemetry spans for active-trace audit verification."""
    catalog[feature_id] = [
        {
            "name": span.name,
            "kind": span.kind.name,
            "trace_id": f"{span.context.trace_id:032x}",
            "span_id": f"{span.context.span_id:016x}",
            "parent_span_id": (
                f"{span.parent.span_id:016x}" if span.parent is not None else None
            ),
            "start_time_unix_nano": span.start_time,
            "end_time_unix_nano": span.end_time,
        }
        for span in spans
    ]


def _assert_string_or_glob(actual: Any, expected: str, *, field_label: str) -> None:
    """Asserts exact string equality, or `fnmatchcase` glob matching if `*` is in `expected`."""
    assert isinstance(actual, str), (
        f"{field_label}: expected str {expected!r}, got {actual!r}"
    )
    if "*" in expected:
        assert fnmatch.fnmatchcase(actual, expected), (
            f"{field_label}: {actual!r} did not match pattern {expected!r}"
        )
    else:
        assert actual == expected, (
            f"{field_label}: expected {expected!r}, got {actual!r}"
        )


def _assert_http_request_fields(
    record_dict: Mapping[str, Any],
    json_payload: Mapping[str, Any],
    row: Mapping[str, str],
) -> None:
    """Validates `httpRequest.*` columns on both raw `LogRecord` and JSON output."""
    expected_method = row["httpRequest.requestMethod"]
    if expected_method == "NOT SET":
        assert "httpRequest" not in record_dict
        assert "httpRequest" not in json_payload
        return

    for container_name, container in (
        ("LogRecord", record_dict),
        ("StructuredLogFormatter", json_payload),
    ):
        http_req = container.get("httpRequest")
        assert isinstance(http_req, dict), (
            f"{container_name} missing httpRequest dict: {http_req!r}"
        )
        assert http_req.get("requestMethod") == expected_method
        _assert_string_or_glob(
            http_req.get("requestUrl"),
            row["httpRequest.requestUrl"],
            field_label=f"{container_name}.httpRequest.requestUrl",
        )
        expected_status = row["httpRequest.status"]
        if expected_status == "NOT SET":
            assert "status" not in http_req, (
                f"{container_name}.httpRequest should omit 'status', got {http_req!r}"
            )
        else:
            assert http_req.get("status") == int(expected_status)


def _assert_trace_correlation(
    record_dict: Mapping[str, Any],
    json_payload: Mapping[str, Any],
    row: Mapping[str, str],
    spans: Sequence[ReadableSpan],
) -> None:
    """Validates `trace_id`, `span_id`, and `logging.googleapis.com/*` correlation fields."""
    expected_trace = row["trace_id"]
    expected_span = row["span_id"]
    expected_cloud = row["Cloud Logging Trace Fields"]

    if expected_trace == "NOT SET":
        for key in ("trace_id", "span_id", *CLOUD_LOGGING_TRACE_KEYS):
            assert key not in record_dict, f"Unexpected {key} on LogRecord"
            assert key not in json_payload, f"Unexpected {key} in JSON output"
        return

    t3_spans = [s for s in spans if s.kind == SpanKind.INTERNAL]
    t4_spans = [s for s in spans if s.kind == SpanKind.CLIENT]
    assert len(t3_spans) == 1, f"Expected 1 T3 INTERNAL span, got {len(t3_spans)}"
    assert len(t4_spans) >= 1, f"Expected >= 1 T4 CLIENT span, got {len(t4_spans)}"

    attempt_idx = int(row["Attempt"])
    t4_attempt_span = t4_spans[attempt_idx]
    assert t4_attempt_span.parent is not None
    assert t4_attempt_span.parent.span_id == t3_spans[0].context.span_id
    assert t4_attempt_span.context.span_id != t3_spans[0].context.span_id

    if expected_span == "T3.span_id":
        target_span = t3_spans[0]
    elif expected_span == "T4.span_id":
        target_span = t4_attempt_span
    else:
        raise ValueError(f"Unsupported span_id sentinel: {expected_span!r}")

    expected_trace_hex = f"{t3_spans[0].context.trace_id:032x}"
    expected_span_hex = f"{target_span.context.span_id:016x}"

    for container_name, container in (
        ("LogRecord", record_dict),
        ("StructuredLogFormatter", json_payload),
    ):
        assert container.get("trace_id") == expected_trace_hex, (
            f"{container_name}.trace_id mismatch"
        )
        assert container.get("span_id") == expected_span_hex, (
            f"{container_name}.span_id mismatch"
        )
        if expected_cloud == "MATCH_SPAN_CONTEXT":
            assert container.get("logging.googleapis.com/trace") == expected_trace_hex
            assert container.get("logging.googleapis.com/spanId") == expected_span_hex
            assert container.get("logging.googleapis.com/trace_sampled") is True
        else:
            raise ValueError(
                f"Unsupported Cloud Logging Trace Fields sentinel: {expected_cloud!r}"
            )


def assert_log_record_matches_row(
    record: logging.LogRecord,
    row: Mapping[str, str],
    spans: Sequence[ReadableSpan],
    *,
    is_async: bool = False,
) -> None:
    """Validates a single captured `LogRecord` and its `StructuredLogFormatter` JSON against `row`."""
    formatter = StructuredLogFormatter()
    json_payload = json.loads(formatter.format(record))
    record_dict = vars(record)

    # 1. Envelope fields
    assert record.levelname == row["Log Level"]
    assert json_payload["severity"] == row["Log Level"]
    assert record.name == row["Logger Name"]
    assert json_payload["name"] == row["Logger Name"]

    message = record.getMessage()
    expected_prefix = _expected_value(row, "Message Prefix", is_async=is_async)
    if "*" in expected_prefix:
        assert fnmatch.fnmatchcase(message, f"{expected_prefix}*"), (
            f"Message {message!r} did not match prefix pattern {expected_prefix!r}"
        )
    else:
        assert message.startswith(expected_prefix), (
            f"Message {message!r} did not start with {expected_prefix!r}"
        )
    assert json_payload["message"] == message

    expected_exc_info = row["exc_info Present"] == "True"
    assert bool(record.exc_info) is expected_exc_info

    # Ensure StructuredLogFormatter unpacked json_fields without emitting a duplicate nested key
    assert "json_fields" not in json_payload

    # 2. Exact / glob string attributes across both LogRecord and JSON output
    assert "rpcName" not in record_dict, "Legacy rpcName must not be emitted"
    assert "rpcName" not in json_payload, "Legacy rpcName must not be emitted in JSON"
    for attr_name in EXACT_OR_GLOB_ATTRIBUTES:
        expected_val = _expected_value(row, attr_name, is_async=is_async)
        if expected_val == "NOT SET":
            assert attr_name not in record_dict, (
                f"Expected {attr_name} NOT SET on LogRecord, got {record_dict.get(attr_name)!r}"
            )
            assert attr_name not in json_payload, (
                f"Expected {attr_name} NOT SET in JSON, got {json_payload.get(attr_name)!r}"
            )
        else:
            _assert_string_or_glob(
                record_dict.get(attr_name),
                expected_val,
                field_label=f"LogRecord[{attr_name!r}]",
            )
            _assert_string_or_glob(
                json_payload.get(attr_name),
                expected_val,
                field_label=f"JSON[{attr_name!r}]",
            )

    # 3. HTTP request sub-dictionary
    _assert_http_request_fields(record_dict, json_payload, row)

    # 4. Exception type & stacktrace
    expected_exc_type = _expected_value(row, "exception.type", is_async=is_async)
    if expected_exc_type == "NOT SET":
        assert "exception.type" not in record_dict
        assert "exception.type" not in json_payload
    else:
        assert record_dict.get("exception.type") == expected_exc_type
        assert json_payload.get("exception.type") == expected_exc_type

    expected_stack = row["exception.stacktrace"]
    if expected_stack == "NOT SET":
        assert "exception.stacktrace" not in record_dict
        assert "exception.stacktrace" not in json_payload
    elif expected_stack == "<TRACEBACK>":
        for container_name, container in (
            ("LogRecord", record_dict),
            ("JSON", json_payload),
        ):
            stack = container.get("exception.stacktrace")
            assert (
                isinstance(stack, str)
                and "Traceback (most recent call last):" in stack
                and '\n  File "' in stack
            ), (
                f"{container_name}['exception.stacktrace']: expected multi-frame Python "
                f"traceback, got {stack!r}"
            )
    else:
        raise ValueError(
            f"Unsupported exception.stacktrace sentinel: {expected_stack!r}"
        )

    # 6. Trace & Span correlation
    _assert_trace_correlation(record_dict, json_payload, row, spans)


# ---------------------------------------------------------------------------
# Boundary & Matrix Compliance Tests (`F4.1` - `F5.14`)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "transport_name,expected_l4_error_type,expected_l3_error_type",
    [
        pytest.param("rest", "400", "400", id="rest_without_error_info"),
        pytest.param(
            "grpc", "INVALID_ARGUMENT", "INVALID_ARGUMENT", id="grpc_without_error_info"
        ),
    ],
)
def test_server_failure_without_error_info_falls_back_to_status(
    transport_name: str,
    expected_l4_error_type: str,
    expected_l3_error_type: str,
    telemetry_harness: TelemetryHarness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifies `error.type` falls back to status code and omits `gcp.errors.*` when `ErrorInfo` is absent."""
    capture, _, _ = telemetry_harness
    monkeypatch.setenv(ENV_LOGGING_ENABLED, "true")
    logging.getLogger(OBSERVABILITY_LOGGER_NAME).setLevel(logging.DEBUG)

    execute_showcase_scenario(
        "Server Failure",
        transport_name,
        ClientOptions(),
        include_error_info=False,
    )

    with conftest.skip_on_core_mismatch():
        l4_records = _partition_tier_records(capture.records, "L4")
        l3_records = _partition_tier_records(capture.records, "L3")
        assert len(l4_records) == 1
        assert len(l3_records) == 1
        assert vars(l4_records[0])["error.type"] == expected_l4_error_type
        assert vars(l3_records[0])["error.type"] == expected_l3_error_type
        for record in (l4_records[0], l3_records[0]):
            assert "gcp.errors.domain" not in vars(record)
            assert "gcp.errors.metadata.zone" not in vars(record)


@pytest.mark.parametrize(
    "row",
    [
        pytest.param(r, id=_param_id(r))
        for r in LOGGING_MATRIX_ROWS
        if int(r["Tier Log Count"]) == 0
    ],
)
def test_sync_no_logs_emitted(
    row: Mapping[str, str],
    telemetry_harness: TelemetryHarness,
    raw_logs_catalog: RawLogsCatalog,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifies zero logs are emitted synchronously when disabled, on success, or on L3 retry recovery."""
    capture, exporter, provider = telemetry_harness

    _execute_row_sync(row, capture, exporter, provider, monkeypatch)

    with conftest.skip_on_core_mismatch():
        _archive_records(raw_logs_catalog, row["Feature ID"], capture.records)
        assert capture.records == []


@pytest.mark.parametrize(
    "row",
    [
        pytest.param(r, id=_param_id(r))
        for r in LOGGING_MATRIX_ROWS
        if int(r["Tier Log Count"]) > 0
    ],
)
def test_sync_error_log_emitted(
    row: Mapping[str, str],
    telemetry_harness: TelemetryHarness,
    raw_logs_catalog: RawLogsCatalog,
    raw_spans_catalog: RawSpansCatalog,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifies sync L4 `DEBUG` and L3 `WARNING` error logs match matrix specs across HTTP/REST and gRPC."""
    capture, exporter, provider = telemetry_harness

    _execute_row_sync(row, capture, exporter, provider, monkeypatch)

    with conftest.skip_on_core_mismatch():
        spans = exporter.get_finished_spans()
        _archive_records(raw_logs_catalog, row["Feature ID"], capture.records)
        if row["trace_id"] != "NOT SET":
            _archive_spans(raw_spans_catalog, row["Feature ID"], spans)
        assert len(capture.records) == int(row["Total Log Count"])
        tier_records = _partition_tier_records(capture.records, row["Tier"])
        assert len(tier_records) == int(row["Tier Log Count"])
        target_record = tier_records[int(row["Attempt"])]
        assert_log_record_matches_row(target_record, row, spans)


@pytest.mark.skipif(not HAS_ASYNC_CLIENTS, reason="Async clients disabled")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "row",
    [
        pytest.param(r, id=_param_id(r, prefix="async_"))
        for r in LOGGING_MATRIX_ROWS
        if int(r["Tier Log Count"]) == 0
    ],
)
async def test_async_no_logs_emitted(
    row: Mapping[str, str],
    telemetry_harness: TelemetryHarness,
    raw_logs_catalog: RawLogsCatalog,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifies zero logs are emitted asynchronously when disabled, on success, or on L3 retry recovery."""
    capture, exporter, provider = telemetry_harness

    await _execute_row_async(row, capture, exporter, provider, monkeypatch)

    with conftest.skip_on_core_mismatch():
        _archive_records(
            raw_logs_catalog, f"async_{row['Feature ID']}", capture.records
        )
        assert capture.records == []


@pytest.mark.skipif(not HAS_ASYNC_CLIENTS, reason="Async clients disabled")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "row",
    [
        pytest.param(r, id=_param_id(r, prefix="async_"))
        for r in LOGGING_MATRIX_ROWS
        if int(r["Tier Log Count"]) > 0
    ],
)
async def test_async_error_log_emitted(
    row: Mapping[str, str],
    telemetry_harness: TelemetryHarness,
    raw_logs_catalog: RawLogsCatalog,
    raw_spans_catalog: RawSpansCatalog,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verifies async gRPC (`grpc_asyncio`) and async REST (`rest_asyncio`) error logs match matrix specs."""
    capture, exporter, provider = telemetry_harness

    await _execute_row_async(row, capture, exporter, provider, monkeypatch)

    with conftest.skip_on_core_mismatch():
        spans = exporter.get_finished_spans()
        feature_key = f"async_{row['Feature ID']}"
        _archive_records(raw_logs_catalog, feature_key, capture.records)
        if row["trace_id"] != "NOT SET":
            _archive_spans(raw_spans_catalog, feature_key, spans)
        assert len(capture.records) == int(row["Total Log Count"])
        tier_records = _partition_tier_records(capture.records, row["Tier"])
        assert len(tier_records) == int(row["Tier Log Count"])
        target_record = tier_records[int(row["Attempt"])]
        assert_log_record_matches_row(
            target_record,
            row,
            spans,
            is_async=True,
        )
