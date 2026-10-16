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

from google.api_core import _observability


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method_name",
    [
        "intercept_unary_unary",
        "intercept_unary_stream",
        "intercept_stream_unary",
        "intercept_stream_stream",
    ],
    ids=["unary_unary", "unary_stream", "stream_unary", "stream_stream"],
)
async def test_async_suppressing_interceptor_invocations(method_name):
    """Verifies that _AsyncSuppressingClientInterceptor wraps downstream async calls in suppress_instrumentation.

    When global OpenTelemetry gRPC auto-instrumentation is enabled, it emits
    generic, un-enriched attempt spans. We wrap downstream async calls in
    suppress_instrumentation so only our enriched Google Cloud SDK T4 span is emitted.
    """
    suppressor = _observability._AsyncSuppressingClientInterceptor()

    with mock.patch(
        "google.api_core._observability._suppress_instrumentation"
    ) as mock_suppress:
        mock_continuation = mock.AsyncMock(return_value="expected_response")
        interceptor_method = getattr(suppressor, method_name)
        result = await interceptor_method(
            mock_continuation, "call_details", "request_or_iterator"
        )

        assert result == "expected_response"
        mock_continuation.assert_called_once_with("call_details", "request_or_iterator")
        mock_suppress.assert_called_once()


@pytest.mark.parametrize(
    "options_or_interceptors",
    [
        None,
        [],
        12345,
        {},
        _observability.ClientOptions(),
    ],
    ids=[
        "none_options",
        "empty_list",
        "invalid_type",
        "client_options_dict",
        "client_options_tracing_disabled",
    ],
)
def test_apply_otel_async_channel_interceptors_inactive_or_empty(
    mock_async_channel, monkeypatch, options_or_interceptors
):
    """Proves that passing inactive or empty options/interceptors returns channel unchanged."""
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")

    result = _observability.apply_otel_async_channel_interceptors(
        mock_async_channel, options_or_interceptors
    )
    assert result is mock_async_channel
    assert mock_async_channel._unary_unary_interceptors == []
    assert mock_async_channel._unary_stream_interceptors == []


@pytest.mark.parametrize(
    "seq_type",
    [list, tuple],
    ids=["list", "tuple"],
)
def test_apply_otel_async_channel_interceptors_sequence_prepending(
    mock_async_channel, seq_type
):
    """Proves that interceptor sequences (list or tuple) are prepended in order."""
    existing_interceptor = mock.Mock()
    mock_async_channel._unary_unary_interceptors = [existing_interceptor]

    interceptor1 = mock.Mock(spec=["intercept_unary_unary"])
    interceptor2 = mock.Mock(spec=["intercept_unary_unary"])

    result = _observability.apply_otel_async_channel_interceptors(
        mock_async_channel, seq_type([interceptor1, interceptor2])
    )
    assert result is mock_async_channel
    assert mock_async_channel._unary_unary_interceptors == [
        interceptor1,
        interceptor2,
        existing_interceptor,
    ]


def test_apply_otel_async_channel_interceptors_client_options_prepending(
    mock_async_channel, monkeypatch
):
    """Proves that interceptors resolved from ClientOptions are prepended in order."""
    existing_interceptor = mock.Mock()
    mock_async_channel._unary_unary_interceptors = [existing_interceptor]

    interceptor1 = mock.Mock(spec=["intercept_unary_unary"])
    interceptor2 = mock.Mock(spec=["intercept_unary_unary"])

    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    monkeypatch.setattr(
        _observability,
        "get_otel_async_interceptor",
        lambda opts: [interceptor1, interceptor2],
    )

    result = _observability.apply_otel_async_channel_interceptors(
        mock_async_channel, _observability.ClientOptions()
    )
    assert result is mock_async_channel
    assert mock_async_channel._unary_unary_interceptors == [
        interceptor1,
        interceptor2,
        existing_interceptor,
    ]


@pytest.mark.parametrize(
    "case,setup_channel,interceptor_spec,expected_result",
    [
        (
            "prevent_duplicates",
            lambda ch, i: setattr(ch, "_unary_unary_interceptors", [i]),
            ["intercept_unary_unary"],
            lambda ch, i: ch._unary_unary_interceptors == [i],
        ),
        (
            "non_list_ignored",
            lambda ch, i: setattr(ch, "_unary_unary_interceptors", "not-a-list"),
            ["intercept_unary_unary"],
            lambda ch, i: ch._unary_unary_interceptors == "not-a-list",
        ),
        (
            "generic_untyped_fallback",
            lambda ch, i: setattr(ch, "_unary_unary_interceptors", ["existing"]),
            [],
            lambda ch, i: ch._unary_unary_interceptors == [i, "existing"],
        ),
    ],
    ids=["prevent_duplicates", "non_list_ignored", "generic_untyped_fallback"],
)
def test_apply_otel_async_channel_interceptors_edge_cases(
    mock_async_channel, case, setup_channel, interceptor_spec, expected_result
):
    """Proves edge case handling: deduplication, non-list attributes, and untyped fallback."""
    interceptor = mock.Mock(spec=interceptor_spec)
    setup_channel(mock_async_channel, interceptor)

    result = _observability.apply_otel_async_channel_interceptors(
        mock_async_channel, [interceptor]
    )
    assert result is mock_async_channel
    assert expected_result(mock_async_channel, interceptor)
