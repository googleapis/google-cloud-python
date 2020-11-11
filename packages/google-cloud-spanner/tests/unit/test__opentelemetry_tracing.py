import importlib
import mock
import unittest
import sys

try:
    from opentelemetry import trace as trace_api
    from opentelemetry.trace.status import StatusCanonicalCode
except ImportError:
    pass

from google.api_core.exceptions import GoogleAPICallError
from google.cloud.spanner_v1 import _opentelemetry_tracing

from tests._helpers import OpenTelemetryBase, HAS_OPENTELEMETRY_INSTALLED


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

            expected_attributes = {
                "db.type": "spanner",
                "db.url": "spanner.googleapis.com",
                "net.host.name": "spanner.googleapis.com",
            }
            expected_attributes.update(extra_attributes)

            with _opentelemetry_tracing.trace_call(
                "CloudSpanner.Test", _make_session(), extra_attributes
            ) as span:
                span.set_attribute("after_setup_attribute", 1)

            expected_attributes["after_setup_attribute"] = 1

            span_list = self.memory_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            span = span_list[0]
            self.assertEqual(span.kind, trace_api.SpanKind.CLIENT)
            self.assertEqual(span.attributes, expected_attributes)
            self.assertEqual(span.name, "CloudSpanner.Test")
            self.assertEqual(span.status.canonical_code, StatusCanonicalCode.OK)

        def test_trace_error(self):
            extra_attributes = {"db.instance": "database_name"}

            expected_attributes = {
                "db.type": "spanner",
                "db.url": "spanner.googleapis.com",
                "net.host.name": "spanner.googleapis.com",
            }
            expected_attributes.update(extra_attributes)

            with self.assertRaises(GoogleAPICallError):
                with _opentelemetry_tracing.trace_call(
                    "CloudSpanner.Test", _make_session(), extra_attributes
                ) as span:
                    from google.api_core.exceptions import InvalidArgument

                    raise _make_rpc_error(InvalidArgument)

            span_list = self.memory_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            span = span_list[0]
            self.assertEqual(span.kind, trace_api.SpanKind.CLIENT)
            self.assertEqual(dict(span.attributes), expected_attributes)
            self.assertEqual(span.name, "CloudSpanner.Test")
            self.assertEqual(
                span.status.canonical_code, StatusCanonicalCode.INVALID_ARGUMENT
            )

        def test_trace_grpc_error(self):
            extra_attributes = {"db.instance": "database_name"}

            expected_attributes = {
                "db.type": "spanner",
                "db.url": "spanner.googleapis.com:443",
                "net.host.name": "spanner.googleapis.com:443",
            }
            expected_attributes.update(extra_attributes)

            with self.assertRaises(GoogleAPICallError):
                with _opentelemetry_tracing.trace_call(
                    "CloudSpanner.Test", _make_session(), extra_attributes
                ) as span:
                    from google.api_core.exceptions import DataLoss

                    raise DataLoss("error")

            span_list = self.memory_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            span = span_list[0]
            self.assertEqual(span.status.canonical_code, StatusCanonicalCode.DATA_LOSS)

        def test_trace_codeless_error(self):
            extra_attributes = {"db.instance": "database_name"}

            expected_attributes = {
                "db.type": "spanner",
                "db.url": "spanner.googleapis.com:443",
                "net.host.name": "spanner.googleapis.com:443",
            }
            expected_attributes.update(extra_attributes)

            with self.assertRaises(GoogleAPICallError):
                with _opentelemetry_tracing.trace_call(
                    "CloudSpanner.Test", _make_session(), extra_attributes
                ) as span:
                    raise GoogleAPICallError("error")

            span_list = self.memory_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            span = span_list[0]
            self.assertEqual(span.status.canonical_code, StatusCanonicalCode.UNKNOWN)
