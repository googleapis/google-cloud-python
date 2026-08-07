# Copyright 2026 Google LLC
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

from unittest import mock

import pytest
from google.auth import credentials as ga_credentials
from google.cloud import secretmanager_v1
from google.cloud.secretmanager_v1.services.secret_manager_service.client import (
    HAVE_FEATURE_GATING,
    HAVE_OTEL,
)
from google.cloud.secretmanager_v1.types import service

# We use the clean pattern from BigQuery tests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


@pytest.fixture
def setup_otel():
    """Fixture to set up in-memory OTel exporting."""
    tracer_provider = TracerProvider()
    memory_exporter = InMemorySpanExporter()
    span_processor = SimpleSpanProcessor(memory_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Override internal global var to inject our provider
    orig_trace_provider = trace._TRACER_PROVIDER
    trace._TRACER_PROVIDER = tracer_provider

    yield memory_exporter

    trace._TRACER_PROVIDER = orig_trace_provider


@pytest.mark.skipif(
    not HAVE_FEATURE_GATING or not HAVE_OTEL,
    reason="Requires feature gating and OpenTelemetry",
)
def test_access_secret_version_custom_span(setup_otel, monkeypatch):
    """Verify that calling access_secret_version produces a custom T3 span with attributes."""

    # Enable tracing via env var (assuming this is how we gate it for clients too)
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    client = secretmanager_v1.SecretManagerServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    request = service.AccessSecretVersionRequest(
        name="projects/test-project/secrets/test-secret/versions/1"
    )

    # Mock the actual transport call to avoid network calls and focus on wrapping
    with mock.patch.object(
        type(client.transport.access_secret_version), "__call__"
    ) as call:
        call.return_value = service.AccessSecretVersionResponse(
            name="projects/test-project/secrets/test-secret/versions/1",
        )

        client.access_secret_version(request)

    # Verify spans
    exported_spans = setup_otel.get_finished_spans()

    # We expect at least one span (the T3 span)
    assert len(exported_spans) >= 1

    # Find the T3 span (it should be the custom one from the client)
    # Naming convention might be "SecretManagerServiceClient.access_secret_version"
    t3_span = None
    for span in exported_spans:
        if "access_secret_version" in span.name:
            t3_span = span
            break

    assert t3_span is not None, "T3 span not found"

    # Verify custom attributes
    attributes = t3_span.attributes
    assert (
        attributes.get("gcp.secretmanager.secret.name")
        == "projects/test-project/secrets/test-secret/versions/1"
    )


@pytest.mark.skipif(
    not HAVE_FEATURE_GATING or not HAVE_OTEL,
    reason="Requires feature gating and OpenTelemetry",
)
def test_access_secret_version_custom_span_disabled(setup_otel, monkeypatch):
    """Verify that calling access_secret_version does NOT produce custom span if disabled."""

    # Disable tracing
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "false")

    client = secretmanager_v1.SecretManagerServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    request = service.AccessSecretVersionRequest(
        name="projects/test-project/secrets/test-secret/versions/1"
    )

    with mock.patch.object(
        type(client.transport.access_secret_version), "__call__"
    ) as call:
        call.return_value = service.AccessSecretVersionResponse(
            name="projects/test-project/secrets/test-secret/versions/1",
        )

        client.access_secret_version(request)

    exported_spans = setup_otel.get_finished_spans()

    # We expect NO spans
    assert len(exported_spans) == 0
    # We might also expect standard attributes like service.name etc, but let's focus on custom ones.
