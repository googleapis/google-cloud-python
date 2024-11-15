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
    not _helpers.USE_EMULATOR, reason="mulator is necessary to test traces."
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
        from_inject_spans = inject_trace_exporter.get_finished_spans()
        assert (
            len(from_global_spans) == 0
        )  # "Expecting no spans from the global trace exporter"
        assert (
            len(from_inject_spans) >= 2
        )  # "Expecting at least 2 spans from the injected trace exporter"
        gotNames = [span.name for span in from_inject_spans]
        wantNames = ["CloudSpanner.CreateSession", "CloudSpanner.ReadWriteTransaction"]
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


def _make_credentials():
    from google.auth.credentials import AnonymousCredentials

    return AnonymousCredentials()
