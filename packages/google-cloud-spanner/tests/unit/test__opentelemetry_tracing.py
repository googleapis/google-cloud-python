import importlib
import mock
import unittest
import sys

try:
    from opentelemetry import trace as trace_api
    from opentelemetry.trace.status import StatusCode
except ImportError:
    pass

from google.api_core.exceptions import GoogleAPICallError
from google.cloud.spanner_v1 import _opentelemetry_tracing

from tests._helpers import (
    OpenTelemetryBase,
    LIB_VERSION,
    HAS_OPENTELEMETRY_INSTALLED,
    enrich_with_otel_scope,
)


def _make_rpc_error(error_cls, trailing_metadata=None):
    import grpc

    grpc_error = mock.create_autospec(grpc.Call, instance=True)
    grpc_error.trailing_metadata.return_value = trailing_metadata
    return error_cls("error", errors=(grpc_error,))


def _make_session():
    from google.cloud.spanner_v1.session import Session

    return mock.Mock(autospec=Session, instance=True)


# Skip all of these tests if we don't have OpenTelemetry
if HAS_OPENTELEMETRY_INSTALLED:

    class TestNoTracing(unittest.TestCase):
        def setUp(self):
            self._temp_opentelemetry = sys.modules["opentelemetry"]

            sys.modules["opentelemetry"] = None
            importlib.reload(_opentelemetry_tracing)

        def tearDown(self):
            sys.modules["opentelemetry"] = self._temp_opentelemetry
            importlib.reload(_opentelemetry_tracing)

        def test_no_trace_call(self):
            with _opentelemetry_tracing.trace_call("Test", _make_session()) as no_span:
                self.assertIsNone(no_span)

    class TestTracing(OpenTelemetryBase):
        def test_trace_call(self):
            extra_attributes = {
                "attribute1": "value1",
                # Since our database is mocked, we have to override the db.instance parameter so it is a string
                "db.instance": "database_name",
            }

            expected_attributes = enrich_with_otel_scope(
                {
                    "db.type": "spanner",
                    "db.url": "spanner.googleapis.com",
                    "net.host.name": "spanner.googleapis.com",
                    "gcp.client.service": "spanner",
                    "gcp.client.version": LIB_VERSION,
                    "gcp.client.repo": "googleapis/python-spanner",
                }
            )
            expected_attributes.update(extra_attributes)

            with _opentelemetry_tracing.trace_call(
                "CloudSpanner.Test", _make_session(), extra_attributes
            ) as span:
                span.set_attribute("after_setup_attribute", 1)

            expected_attributes["after_setup_attribute"] = 1

            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            span = span_list[0]
            self.assertEqual(span.kind, trace_api.SpanKind.CLIENT)
            self.assertEqual(span.attributes, expected_attributes)
            self.assertEqual(span.name, "CloudSpanner.Test")
            self.assertEqual(span.status.status_code, StatusCode.OK)

        def test_trace_error(self):
            extra_attributes = {"db.instance": "database_name"}

            expected_attributes = enrich_with_otel_scope(
                {
                    "db.type": "spanner",
                    "db.url": "spanner.googleapis.com",
                    "net.host.name": "spanner.googleapis.com",
                    "gcp.client.service": "spanner",
                    "gcp.client.version": LIB_VERSION,
                    "gcp.client.repo": "googleapis/python-spanner",
                }
            )
            expected_attributes.update(extra_attributes)

            with self.assertRaises(GoogleAPICallError):
                with _opentelemetry_tracing.trace_call(
                    "CloudSpanner.Test", _make_session(), extra_attributes
                ) as span:
                    from google.api_core.exceptions import InvalidArgument

                    raise _make_rpc_error(InvalidArgument)

            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            span = span_list[0]
            self.assertEqual(span.kind, trace_api.SpanKind.CLIENT)
            self.assertEqual(dict(span.attributes), expected_attributes)
            self.assertEqual(span.name, "CloudSpanner.Test")
            self.assertEqual(span.status.status_code, StatusCode.ERROR)

        def test_trace_grpc_error(self):
            extra_attributes = {"db.instance": "database_name"}

            expected_attributes = enrich_with_otel_scope(
                {
                    "db.type": "spanner",
                    "db.url": "spanner.googleapis.com:443",
                    "net.host.name": "spanner.googleapis.com:443",
                }
            )
            expected_attributes.update(extra_attributes)

            with self.assertRaises(GoogleAPICallError):
                with _opentelemetry_tracing.trace_call(
                    "CloudSpanner.Test", _make_session(), extra_attributes
                ) as span:
                    from google.api_core.exceptions import DataLoss

                    raise DataLoss("error")

            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            span = span_list[0]
            self.assertEqual(span.status.status_code, StatusCode.ERROR)

        def test_trace_codeless_error(self):
            extra_attributes = {"db.instance": "database_name"}

            expected_attributes = enrich_with_otel_scope(
                {
                    "db.type": "spanner",
                    "db.url": "spanner.googleapis.com:443",
                    "net.host.name": "spanner.googleapis.com:443",
                }
            )
            expected_attributes.update(extra_attributes)

            with self.assertRaises(GoogleAPICallError):
                with _opentelemetry_tracing.trace_call(
                    "CloudSpanner.Test", _make_session(), extra_attributes
                ) as span:
                    raise GoogleAPICallError("error")

            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            span = span_list[0]
            self.assertEqual(span.status.status_code, StatusCode.ERROR)

        def test_trace_call_terminal_span_status_ALWAYS_ON_sampler(self):
            # Verify that we don't unconditionally set the terminal span status to
            # SpanStatus.OK per https://github.com/googleapis/python-spanner/issues/1246
            from opentelemetry.sdk.trace.export import SimpleSpanProcessor
            from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
                InMemorySpanExporter,
            )
            from opentelemetry.trace.status import Status, StatusCode
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.sampling import ALWAYS_ON

            tracer_provider = TracerProvider(sampler=ALWAYS_ON)
            trace_exporter = InMemorySpanExporter()
            tracer_provider.add_span_processor(SimpleSpanProcessor(trace_exporter))
            observability_options = dict(tracer_provider=tracer_provider)

            session = _make_session()
            with _opentelemetry_tracing.trace_call(
                "VerifyTerminalSpanStatus",
                session,
                observability_options=observability_options,
            ) as span:
                span.set_status(Status(StatusCode.ERROR, "Our error exhibit"))

            span_list = trace_exporter.get_finished_spans()
            got_statuses = []

            for span in span_list:
                got_statuses.append(
                    (span.name, span.status.status_code, span.status.description)
                )

            want_statuses = [
                ("VerifyTerminalSpanStatus", StatusCode.ERROR, "Our error exhibit"),
            ]
            assert got_statuses == want_statuses

        def test_trace_call_terminal_span_status_ALWAYS_OFF_sampler(self):
            # Verify that we get the correct status even when using the ALWAYS_OFF
            # sampler which produces the NonRecordingSpan per
            # https://github.com/googleapis/python-spanner/issues/1286
            from opentelemetry.sdk.trace.export import SimpleSpanProcessor
            from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
                InMemorySpanExporter,
            )
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.sampling import ALWAYS_OFF

            tracer_provider = TracerProvider(sampler=ALWAYS_OFF)
            trace_exporter = InMemorySpanExporter()
            tracer_provider.add_span_processor(SimpleSpanProcessor(trace_exporter))
            observability_options = dict(tracer_provider=tracer_provider)

            session = _make_session()
            used_span = None
            with _opentelemetry_tracing.trace_call(
                "VerifyWithNonRecordingSpan",
                session,
                observability_options=observability_options,
            ) as span:
                used_span = span

            assert type(used_span).__name__ == "NonRecordingSpan"
            span_list = list(trace_exporter.get_finished_spans())
            assert span_list == []
