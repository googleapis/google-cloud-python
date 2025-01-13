# Copyright 2024 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from . import _helpers
from google.cloud.spanner_v1 import Client
from google.api_core.exceptions import Aborted
from google.auth.credentials import AnonymousCredentials
from google.rpc import code_pb2

HAS_OTEL_INSTALLED = False

try:
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.sampling import ALWAYS_ON
    from opentelemetry import trace

    HAS_OTEL_INSTALLED = True
except ImportError:
    pass


@pytest.mark.skipif(
    not HAS_OTEL_INSTALLED, reason="OpenTelemetry is necessary to test traces."
)
@pytest.mark.skipif(
    not _helpers.USE_EMULATOR, reason="Emulator is necessary to test traces."
)
def test_observability_options_propagation():
    PROJECT = _helpers.EMULATOR_PROJECT
    CONFIGURATION_NAME = "config-name"
    INSTANCE_ID = _helpers.INSTANCE_ID
    DISPLAY_NAME = "display-name"
    DATABASE_ID = _helpers.unique_id("temp_db")
    NODE_COUNT = 5
    LABELS = {"test": "true"}

    def test_propagation(enable_extended_tracing):
        global_tracer_provider = TracerProvider(sampler=ALWAYS_ON)
        trace.set_tracer_provider(global_tracer_provider)
        global_trace_exporter = InMemorySpanExporter()
        global_tracer_provider.add_span_processor(
            SimpleSpanProcessor(global_trace_exporter)
        )

        inject_tracer_provider = TracerProvider(sampler=ALWAYS_ON)
        inject_trace_exporter = InMemorySpanExporter()
        inject_tracer_provider.add_span_processor(
            SimpleSpanProcessor(inject_trace_exporter)
        )
        observability_options = dict(
            tracer_provider=inject_tracer_provider,
            enable_extended_tracing=enable_extended_tracing,
        )
        client = Client(
            project=PROJECT,
            observability_options=observability_options,
            credentials=_make_credentials(),
        )

        instance = client.instance(
            INSTANCE_ID,
            CONFIGURATION_NAME,
            display_name=DISPLAY_NAME,
            node_count=NODE_COUNT,
            labels=LABELS,
        )

        try:
            instance.create()
        except Exception:
            pass

        db = instance.database(DATABASE_ID)
        try:
            db.create()
        except Exception:
            pass

        assert db.observability_options == observability_options
        with db.snapshot() as snapshot:
            res = snapshot.execute_sql("SELECT 1")
            for val in res:
                _ = val

        from_global_spans = global_trace_exporter.get_finished_spans()
        target_spans = inject_trace_exporter.get_finished_spans()
        from_inject_spans = sorted(target_spans, key=lambda v1: v1.start_time)
        assert (
            len(from_global_spans) == 0
        )  # "Expecting no spans from the global trace exporter"
        assert (
            len(from_inject_spans) >= 2
        )  # "Expecting at least 2 spans from the injected trace exporter"
        gotNames = [span.name for span in from_inject_spans]
        wantNames = [
            "CloudSpanner.CreateSession",
            "CloudSpanner.Snapshot.execute_sql",
        ]
        assert gotNames == wantNames

        # Check for conformance of enable_extended_tracing
        lastSpan = from_inject_spans[len(from_inject_spans) - 1]
        wantAnnotatedSQL = "SELECT 1"
        if not enable_extended_tracing:
            wantAnnotatedSQL = None
        assert (
            lastSpan.attributes.get("db.statement", None) == wantAnnotatedSQL
        )  # "Mismatch in annotated sql"

        try:
            db.delete()
            instance.delete()
        except Exception:
            pass

    # Test the respective options for enable_extended_tracing
    test_propagation(True)
    test_propagation(False)


def create_db_trace_exporter():
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.sampling import ALWAYS_ON

    PROJECT = _helpers.EMULATOR_PROJECT
    CONFIGURATION_NAME = "config-name"
    INSTANCE_ID = _helpers.INSTANCE_ID
    DISPLAY_NAME = "display-name"
    DATABASE_ID = _helpers.unique_id("temp_db")
    NODE_COUNT = 5
    LABELS = {"test": "true"}

    tracer_provider = TracerProvider(sampler=ALWAYS_ON)
    trace_exporter = InMemorySpanExporter()
    tracer_provider.add_span_processor(SimpleSpanProcessor(trace_exporter))
    observability_options = dict(
        tracer_provider=tracer_provider,
        enable_extended_tracing=True,
    )

    client = Client(
        project=PROJECT,
        observability_options=observability_options,
        credentials=AnonymousCredentials(),
    )

    instance = client.instance(
        INSTANCE_ID,
        CONFIGURATION_NAME,
        display_name=DISPLAY_NAME,
        node_count=NODE_COUNT,
        labels=LABELS,
    )

    try:
        instance.create()
    except Exception:
        pass

    db = instance.database(DATABASE_ID)
    try:
        db.create()
    except Exception:
        pass

    return db, trace_exporter


@pytest.mark.skipif(
    not _helpers.USE_EMULATOR,
    reason="Emulator needed to run this test",
)
@pytest.mark.skipif(
    not HAS_OTEL_INSTALLED,
    reason="Tracing requires OpenTelemetry",
)
def test_transaction_abort_then_retry_spans():
    from opentelemetry.trace.status import StatusCode

    db, trace_exporter = create_db_trace_exporter()

    counters = dict(aborted=0)

    def select_in_txn(txn):
        results = txn.execute_sql("SELECT 1")
        for row in results:
            _ = row

        if counters["aborted"] == 0:
            counters["aborted"] = 1
            raise Aborted(
                "Thrown from ClientInterceptor for testing",
                errors=[_helpers.FauxCall(code_pb2.ABORTED)],
            )

    db.run_in_transaction(select_in_txn)

    got_statuses, got_events = finished_spans_statuses(trace_exporter)

    # Check for the series of events
    want_events = [
        ("Acquiring session", {"kind": "BurstyPool"}),
        ("Waiting for a session to become available", {"kind": "BurstyPool"}),
        ("No sessions available in pool. Creating session", {"kind": "BurstyPool"}),
        ("Creating Session", {}),
        (
            "Transaction was aborted in user operation, retrying",
            {"delay_seconds": "EPHEMERAL", "cause": "EPHEMERAL", "attempt": 1},
        ),
        ("Starting Commit", {}),
        ("Commit Done", {}),
    ]
    assert got_events == want_events

    # Check for the statues.
    codes = StatusCode
    want_statuses = [
        ("CloudSpanner.Database.run_in_transaction", codes.OK, None),
        ("CloudSpanner.CreateSession", codes.OK, None),
        ("CloudSpanner.Session.run_in_transaction", codes.OK, None),
        ("CloudSpanner.Transaction.execute_sql", codes.OK, None),
        ("CloudSpanner.Transaction.execute_sql", codes.OK, None),
        ("CloudSpanner.Transaction.commit", codes.OK, None),
    ]
    assert got_statuses == want_statuses


def finished_spans_statuses(trace_exporter):
    span_list = trace_exporter.get_finished_spans()
    # Sort the spans by their start time in the hierarchy.
    span_list = sorted(span_list, key=lambda span: span.start_time)

    got_events = []
    got_statuses = []

    # Some event attributes are noisy/highly ephemeral
    # and can't be directly compared against.
    imprecise_event_attributes = ["exception.stacktrace", "delay_seconds", "cause"]
    for span in span_list:
        got_statuses.append(
            (span.name, span.status.status_code, span.status.description)
        )

        for event in span.events:
            evt_attributes = event.attributes.copy()
            for attr_name in imprecise_event_attributes:
                if attr_name in evt_attributes:
                    evt_attributes[attr_name] = "EPHEMERAL"

            got_events.append((event.name, evt_attributes))

    return got_statuses, got_events


@pytest.mark.skipif(
    not _helpers.USE_EMULATOR,
    reason="Emulator needed to run this tests",
)
@pytest.mark.skipif(
    not HAS_OTEL_INSTALLED,
    reason="Tracing requires OpenTelemetry",
)
def test_transaction_update_implicit_begin_nested_inside_commit():
    # Tests to ensure that transaction.commit() without a began transaction
    # has transaction.begin() inlined and nested under the commit span.
    from google.auth.credentials import AnonymousCredentials
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.sampling import ALWAYS_ON

    PROJECT = _helpers.EMULATOR_PROJECT
    CONFIGURATION_NAME = "config-name"
    INSTANCE_ID = _helpers.INSTANCE_ID
    DISPLAY_NAME = "display-name"
    DATABASE_ID = _helpers.unique_id("temp_db")
    NODE_COUNT = 5
    LABELS = {"test": "true"}

    def tx_update(txn):
        txn.insert(
            "Singers",
            columns=["SingerId", "FirstName"],
            values=[["1", "Bryan"], ["2", "Slash"]],
        )

    tracer_provider = TracerProvider(sampler=ALWAYS_ON)
    trace_exporter = InMemorySpanExporter()
    tracer_provider.add_span_processor(SimpleSpanProcessor(trace_exporter))
    observability_options = dict(
        tracer_provider=tracer_provider,
        enable_extended_tracing=True,
    )

    client = Client(
        project=PROJECT,
        observability_options=observability_options,
        credentials=AnonymousCredentials(),
    )

    instance = client.instance(
        INSTANCE_ID,
        CONFIGURATION_NAME,
        display_name=DISPLAY_NAME,
        node_count=NODE_COUNT,
        labels=LABELS,
    )

    try:
        instance.create()
    except Exception:
        pass

    db = instance.database(DATABASE_ID)
    try:
        db._ddl_statements = [
            """CREATE TABLE Singers (
            SingerId     INT64 NOT NULL,
            FirstName    STRING(1024),
            LastName     STRING(1024),
            SingerInfo   BYTES(MAX),
            FullName   STRING(2048) AS (
                ARRAY_TO_STRING([FirstName, LastName], " ")
            ) STORED
            ) PRIMARY KEY (SingerId)""",
            """CREATE TABLE Albums (
                SingerId     INT64 NOT NULL,
                AlbumId      INT64 NOT NULL,
                AlbumTitle   STRING(MAX),
                MarketingBudget INT64,
            ) PRIMARY KEY (SingerId, AlbumId),
            INTERLEAVE IN PARENT Singers ON DELETE CASCADE""",
        ]
        db.create()
    except Exception:
        pass

    try:
        db.run_in_transaction(tx_update)
    except Exception:
        pass

    span_list = trace_exporter.get_finished_spans()
    # Sort the spans by their start time in the hierarchy.
    span_list = sorted(span_list, key=lambda span: span.start_time)
    got_span_names = [span.name for span in span_list]
    want_span_names = [
        "CloudSpanner.Database.run_in_transaction",
        "CloudSpanner.CreateSession",
        "CloudSpanner.Session.run_in_transaction",
        "CloudSpanner.Transaction.commit",
        "CloudSpanner.Transaction.begin",
    ]

    assert got_span_names == want_span_names

    # Our object is to ensure that .begin() is a child of .commit()
    span_tx_begin = span_list[-1]
    span_tx_commit = span_list[-2]
    assert span_tx_begin.parent.span_id == span_tx_commit.context.span_id


@pytest.mark.skipif(
    not _helpers.USE_EMULATOR,
    reason="Emulator needed to run this test",
)
@pytest.mark.skipif(
    not HAS_OTEL_INSTALLED,
    reason="Tracing requires OpenTelemetry",
)
def test_database_partitioned_error():
    from opentelemetry.trace.status import StatusCode

    db, trace_exporter = create_db_trace_exporter()

    try:
        db.execute_partitioned_dml("UPDATE NonExistent SET name = 'foo' WHERE id > 1")
    except Exception:
        pass

    got_statuses, got_events = finished_spans_statuses(trace_exporter)
    # Check for the series of events
    want_events = [
        ("Acquiring session", {"kind": "BurstyPool"}),
        ("Waiting for a session to become available", {"kind": "BurstyPool"}),
        ("No sessions available in pool. Creating session", {"kind": "BurstyPool"}),
        ("Creating Session", {}),
        ("Starting BeginTransaction", {}),
        (
            "exception",
            {
                "exception.type": "google.api_core.exceptions.InvalidArgument",
                "exception.message": "400 Table not found: NonExistent [at 1:8]\nUPDATE NonExistent SET name = 'foo' WHERE id > 1\n       ^",
                "exception.stacktrace": "EPHEMERAL",
                "exception.escaped": "False",
            },
        ),
        (
            "exception",
            {
                "exception.type": "google.api_core.exceptions.InvalidArgument",
                "exception.message": "400 Table not found: NonExistent [at 1:8]\nUPDATE NonExistent SET name = 'foo' WHERE id > 1\n       ^",
                "exception.stacktrace": "EPHEMERAL",
                "exception.escaped": "False",
            },
        ),
    ]
    assert got_events == want_events

    # Check for the statues.
    codes = StatusCode
    want_statuses = [
        (
            "CloudSpanner.Database.execute_partitioned_pdml",
            codes.ERROR,
            "InvalidArgument: 400 Table not found: NonExistent [at 1:8]\nUPDATE NonExistent SET name = 'foo' WHERE id > 1\n       ^",
        ),
        ("CloudSpanner.CreateSession", codes.OK, None),
        (
            "CloudSpanner.ExecuteStreamingSql",
            codes.ERROR,
            "InvalidArgument: 400 Table not found: NonExistent [at 1:8]\nUPDATE NonExistent SET name = 'foo' WHERE id > 1\n       ^",
        ),
    ]
    assert got_statuses == want_statuses


def _make_credentials():
    from google.auth.credentials import AnonymousCredentials

    return AnonymousCredentials()
