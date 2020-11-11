import unittest
import mock

try:
    from opentelemetry import trace as trace_api
    from opentelemetry.trace.status import StatusCanonicalCode

    from opentelemetry.sdk.trace import TracerProvider, export
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    HAS_OPENTELEMETRY_INSTALLED = True
except ImportError:
    HAS_OPENTELEMETRY_INSTALLED = False

    StatusCanonicalCode = mock.Mock()


class OpenTelemetryBase(unittest.TestCase):
    def setUp(self):
        if HAS_OPENTELEMETRY_INSTALLED:
            self.original_tracer_provider = trace_api.get_tracer_provider()
            self.tracer_provider = TracerProvider()
            self.memory_exporter = InMemorySpanExporter()
            span_processor = export.SimpleExportSpanProcessor(self.memory_exporter)
            self.tracer_provider.add_span_processor(span_processor)
            trace_api.set_tracer_provider(self.tracer_provider)

    def tearDown(self):
        if HAS_OPENTELEMETRY_INSTALLED:
            trace_api.set_tracer_provider(self.original_tracer_provider)

    def assertNoSpans(self):
        if HAS_OPENTELEMETRY_INSTALLED:
            span_list = self.memory_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 0)

    def assertSpanAttributes(
        self, name, status=StatusCanonicalCode.OK, attributes=None, span=None
    ):
        if HAS_OPENTELEMETRY_INSTALLED:
            if not span:
                span_list = self.memory_exporter.get_finished_spans()
                self.assertEqual(len(span_list), 1)
                span = span_list[0]

            self.assertEqual(span.name, name)
            self.assertEqual(span.status.canonical_code, status)
            self.assertEqual(dict(span.attributes), attributes)
