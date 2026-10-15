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


def test_apply_otel_async_channel_interceptors_none_or_empty():
    """Proves that passing None or empty interceptors returns the channel unchanged."""
    channel = mock.Mock()
    assert (
        _observability.apply_otel_async_channel_interceptors(channel, None) is channel
    )
    assert _observability.apply_otel_async_channel_interceptors(channel, []) is channel


def test_apply_otel_async_channel_interceptors_prepends_in_order():
    """Proves that OpenTelemetry interceptors are prepended to the front of channel interceptor lists in order."""
    existing_interceptor = mock.Mock()
    interceptor1 = mock.Mock(spec=["intercept_unary_unary"])
    interceptor2 = mock.Mock(spec=["intercept_unary_unary"])

    channel = mock.Mock()
    channel._unary_unary_interceptors = [existing_interceptor]

    result = _observability.apply_otel_async_channel_interceptors(
        channel, [interceptor1, interceptor2]
    )
    assert result is channel
    assert channel._unary_unary_interceptors == [
        interceptor1,
        interceptor2,
        existing_interceptor,
    ]


def test_apply_otel_async_channel_interceptors_prevents_duplicates():
    """Proves that already-registered interceptors are not prepended again."""
    interceptor = mock.Mock(spec=["intercept_unary_unary"])

    channel = mock.Mock()
    channel._unary_unary_interceptors = [interceptor]

    result = _observability.apply_otel_async_channel_interceptors(
        channel, [interceptor]
    )
    assert result is channel
    assert channel._unary_unary_interceptors == [interceptor]


def test_apply_otel_async_channel_interceptors_non_list_ignored():
    """Proves that non-list interceptor containers on a channel are safely ignored."""
    channel = mock.Mock()
    channel._unary_unary_interceptors = "not-a-list"
    interceptor = mock.Mock(spec=["intercept_unary_unary"])

    result = _observability.apply_otel_async_channel_interceptors(
        channel, [interceptor]
    )
    assert result is channel
    assert channel._unary_unary_interceptors == "not-a-list"


def test_apply_otel_async_channel_interceptors_with_client_options_disabled(
    monkeypatch,
):
    """Proves that apply_otel_async_channel_interceptors returns channel unchanged when tracing is disabled."""
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")
    channel = mock.Mock()
    channel._unary_unary_interceptors = []
    options = _observability.ClientOptions()

    result = _observability.apply_otel_async_channel_interceptors(channel, options)
    assert result is channel
    assert channel._unary_unary_interceptors == []


def test_apply_otel_async_channel_interceptors_with_client_options_enabled(monkeypatch):
    """Proves that apply_otel_async_channel_interceptors resolves interceptors and prepends them."""
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    channel = mock.Mock()
    existing = mock.Mock()
    channel._unary_unary_interceptors = [existing]
    options = _observability.ClientOptions()
    mock_interceptor = mock.Mock(spec=["intercept_unary_unary"])

    with mock.patch.object(
        _observability, "get_otel_async_interceptor", return_value=[mock_interceptor]
    ) as mock_get:
        result = _observability.apply_otel_async_channel_interceptors(channel, options)
        assert result is channel
        mock_get.assert_called_once_with(options)
        assert channel._unary_unary_interceptors == [mock_interceptor, existing]


def test_apply_otel_async_channel_interceptors_sequence_tuple():
    """Proves that passing a sequence tuple of interceptors prepends correctly."""
    channel = mock.Mock()
    existing = mock.Mock()
    channel._unary_unary_interceptors = [existing]
    interceptor = mock.Mock(spec=["intercept_unary_unary"])

    result = _observability.apply_otel_async_channel_interceptors(
        channel, (interceptor,)
    )
    assert result is channel
    assert channel._unary_unary_interceptors == [interceptor, existing]


def test_apply_otel_async_channel_interceptors_invalid_client_options():
    """Proves that passing an invalid client_options type returns the channel unchanged."""
    channel = mock.Mock()
    channel._unary_unary_interceptors = []

    result = _observability.apply_otel_async_channel_interceptors(channel, 12345)
    assert result is channel
    assert channel._unary_unary_interceptors == []


def test_apply_otel_async_channel_interceptors_generic_untyped_fallback():
    """Proves that generic interceptors without standard methods fall back to unary list."""
    channel = mock.Mock()
    existing = mock.Mock()
    channel._unary_unary_interceptors = [existing]
    generic_interceptor = mock.Mock(spec=[])

    result = _observability.apply_otel_async_channel_interceptors(
        channel, [generic_interceptor]
    )
    assert result is channel
    assert channel._unary_unary_interceptors == [generic_interceptor, existing]
