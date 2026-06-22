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

from unittest.mock import MagicMock, Mock

import pytest

# Check if grpc is available
try:
    import grpc

    has_grpc = True
except ImportError:
    has_grpc = False

# Skip all tests in this module if grpc is not installed
pytestmark = pytest.mark.skipif(not has_grpc, reason="grpc package is required")

if has_grpc:

    class MockClientCallDetails(grpc.ClientCallDetails):
        pass

else:
    # Tell mypy that we are intentionally redefining this class for the non-gRPC fallback path.
    class MockClientCallDetails:  # type: ignore[no-redef]
        pass


@pytest.fixture
def mock_span(mocker):
    """Mocks trace.get_current_span to return a recording span."""
    mock_span_obj = MagicMock()
    mock_span_obj.is_recording.return_value = True
    mocker.patch("opentelemetry.trace.get_current_span", return_value=mock_span_obj)
    return mock_span_obj


@pytest.fixture
def mock_span_non_recording(mocker):
    """Mocks trace.get_current_span to return a non-recording span."""
    mock_span_obj = MagicMock()
    mock_span_obj.is_recording.return_value = False
    mocker.patch("opentelemetry.trace.get_current_span", return_value=mock_span_obj)
    return mock_span_obj


def test_enricher_non_recording_span(mock_span_non_recording):
    """Verifies that non-recording spans do not have attributes set and extractor is skipped."""
    from google.api_core.observability.tracing import OtelSpanEnricher

    extractor = Mock()
    enricher = OtelSpanEnricher(
        static_attributes={"static.key": "static.val"}, attribute_extractor=extractor
    )

    continuation = Mock(return_value="response")
    details = MockClientCallDetails()
    request = "request"

    res = enricher.intercept_unary_unary(continuation, details, request)

    assert res == "response"
    continuation.assert_called_once_with(details, request)
    mock_span_non_recording.set_attribute.assert_not_called()
    extractor.assert_not_called()


@pytest.mark.parametrize(
    "static_attrs,request_val,extractor_return,expected_attrs",
    [
        # Case 1: Only static attributes
        ({"static.key": "static.val"}, "req", None, {"static.key": "static.val"}),
        # Case 2: Only dynamic attributes
        (None, "req", {"dynamic.key": "dynamic.val"}, {"dynamic.key": "dynamic.val"}),
        # Case 3: Both static and dynamic
        (
            {"static.key": "static.val"},
            "req",
            {"dynamic.key": "dynamic.val"},
            {"static.key": "static.val", "dynamic.key": "dynamic.val"},
        ),
        # Case 4: Dynamic extractor returns None values (should be skipped)
        (
            {"static.key": "static.val"},
            "req",
            {"dynamic.key": None, "other.key": "other.val"},
            {"static.key": "static.val", "other.key": "other.val"},
        ),
    ],
)
def test_enricher_recording_span(
    mock_span, static_attrs, request_val, extractor_return, expected_attrs
):
    """Verifies static and dynamic attribute resolution on recording spans."""
    from google.api_core.observability.tracing import OtelSpanEnricher

    if extractor_return is not None:
        extractor = Mock(return_value=extractor_return)
    else:
        extractor = None

    enricher = OtelSpanEnricher(
        static_attributes=static_attrs, attribute_extractor=extractor
    )

    continuation = Mock(return_value="response")
    details = MockClientCallDetails()
    request = request_val

    res = enricher.intercept_unary_unary(continuation, details, request)

    assert res == "response"
    continuation.assert_called_once_with(details, request)

    # Check that expected attributes were set
    for key, val in expected_attrs.items():
        mock_span.set_attribute.assert_any_call(key, val)

    # Total set_attribute calls should match expected_attrs size
    assert mock_span.set_attribute.call_count == len(expected_attrs)

    if extractor:
        extractor.assert_called_once_with(request, details)


def test_enricher_extractor_exception(mock_span):
    """Verifies that exceptions in attribute extraction are caught and do not fail the call."""
    from google.api_core.observability.tracing import OtelSpanEnricher

    def bad_extractor(req, details):
        raise ValueError("Extraction failure")

    enricher = OtelSpanEnricher(
        static_attributes={"static.key": "static.val"},
        attribute_extractor=bad_extractor,
    )

    continuation = Mock(return_value="response")
    details = MockClientCallDetails()
    request = "req"

    res = enricher.intercept_unary_unary(continuation, details, request)

    assert res == "response"
    continuation.assert_called_once_with(details, request)

    # Static attributes should still be set before extractor failure
    mock_span.set_attribute.assert_called_once_with("static.key", "static.val")
