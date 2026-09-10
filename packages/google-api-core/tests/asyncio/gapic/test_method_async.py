# Copyright 2017 Google LLC
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

import datetime

try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER  # noqa: F401
except ImportError:  # pragma: NO COVER
    import mock  # type: ignore
import pytest

try:
    from grpc import Compression, aio
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)

from google.api_core import (
    client_options as client_options_lib,
)
from google.api_core import (
    exceptions,
    gapic_v1,
    grpc_helpers_async,
    retry_async,
    timeout,
)
from google.api_core.gapic_v1 import client_info
from tests.helpers import assert_uninstrumented_gapic_callable


def _utcnow_monotonic():
    current_time = datetime.datetime.min
    delta = datetime.timedelta(seconds=0.5)
    while True:
        yield current_time
        current_time += delta


@pytest.mark.asyncio
async def test_wrap_method_basic():
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped_method = gapic_v1.method_async.wrap_method(method)

    result = await wrapped_method(1, 2, meep="moop")

    assert result == 42
    method.assert_called_once_with(1, 2, meep="moop", metadata=mock.ANY)

    # Check that the default client info was specified in the metadata.
    metadata = method.call_args[1]["metadata"]
    assert len(metadata) == 1
    client_info = gapic_v1.client_info.DEFAULT_CLIENT_INFO
    user_agent_metadata = client_info.to_grpc_metadata()
    assert user_agent_metadata in metadata


@pytest.mark.asyncio
async def test_wrap_method_with_no_client_info():
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall()
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped_method = gapic_v1.method_async.wrap_method(method, client_info=None)

    await wrapped_method(1, 2, meep="moop")

    method.assert_called_once_with(1, 2, meep="moop")


@pytest.mark.asyncio
async def test_wrap_method_with_custom_client_info():
    client_info = gapic_v1.client_info.ClientInfo(
        python_version=1,
        grpc_version=2,
        api_core_version=3,
        gapic_version=4,
        client_library_version=5,
        protobuf_runtime_version=6,
    )
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall()
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped_method = gapic_v1.method_async.wrap_method(method, client_info=client_info)

    await wrapped_method(1, 2, meep="moop")

    method.assert_called_once_with(1, 2, meep="moop", metadata=mock.ANY)

    # Check that the custom client info was specified in the metadata.
    metadata = method.call_args[1]["metadata"]
    assert client_info.to_grpc_metadata() in metadata


@pytest.mark.asyncio
async def test_wrap_method_with_no_compression():
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall()
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped_method = gapic_v1.method_async.wrap_method(method)

    await wrapped_method(1, 2, meep="moop", compression=None)

    method.assert_called_once_with(1, 2, meep="moop", metadata=mock.ANY)


@pytest.mark.asyncio
async def test_wrap_method_with_custom_compression():
    compression = Compression.Gzip
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall()
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped_method = gapic_v1.method_async.wrap_method(
        method, default_compression=compression
    )

    await wrapped_method(1, 2, meep="moop", compression=Compression.Deflate)

    method.assert_called_once_with(
        1, 2, meep="moop", metadata=mock.ANY, compression=Compression.Deflate
    )


@pytest.mark.asyncio
async def test_invoke_wrapped_method_with_metadata():
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall()
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped_method = gapic_v1.method_async.wrap_method(method)

    await wrapped_method(mock.sentinel.request, metadata=[("a", "b")])

    method.assert_called_once_with(mock.sentinel.request, metadata=mock.ANY)
    metadata = method.call_args[1]["metadata"]
    # Metadata should have two items: the client info metadata and our custom
    # metadata.
    assert len(metadata) == 2
    assert ("a", "b") in metadata


@pytest.mark.asyncio
async def test_invoke_wrapped_method_with_metadata_as_none():
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall()
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped_method = gapic_v1.method_async.wrap_method(method)

    await wrapped_method(mock.sentinel.request, metadata=None)

    method.assert_called_once_with(mock.sentinel.request, metadata=mock.ANY)
    metadata = method.call_args[1]["metadata"]
    # Metadata should have just one items: the client info metadata.
    assert len(metadata) == 1


@mock.patch("asyncio.sleep")
@pytest.mark.asyncio
async def test_wrap_method_with_default_retry_timeout_and_compression(unused_sleep):
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(
        spec=aio.UnaryUnaryMultiCallable,
        side_effect=[exceptions.InternalServerError(None), fake_call],
    )

    default_retry = retry_async.AsyncRetry()
    default_timeout = timeout.ConstantTimeout(60)
    default_compression = Compression.Gzip
    wrapped_method = gapic_v1.method_async.wrap_method(
        method, default_retry, default_timeout, default_compression
    )

    result = await wrapped_method()

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(
        timeout=60, compression=default_compression, metadata=mock.ANY
    )


@mock.patch("asyncio.sleep")
@pytest.mark.asyncio
async def test_wrap_method_with_default_retry_and_timeout_using_sentinel(unused_sleep):
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(
        spec=aio.UnaryUnaryMultiCallable,
        side_effect=[exceptions.InternalServerError(None), fake_call],
    )

    default_retry = retry_async.AsyncRetry()
    default_timeout = timeout.ConstantTimeout(60)
    default_compression = Compression.Gzip
    wrapped_method = gapic_v1.method_async.wrap_method(
        method, default_retry, default_timeout, default_compression
    )

    result = await wrapped_method(
        retry=gapic_v1.method_async.DEFAULT,
        timeout=gapic_v1.method_async.DEFAULT,
        compression=gapic_v1.method_async.DEFAULT,
    )

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(
        timeout=60, compression=Compression.Gzip, metadata=mock.ANY
    )


@mock.patch("asyncio.sleep")
@pytest.mark.asyncio
async def test_wrap_method_with_overriding_retry_timeout_and_compression(unused_sleep):
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(
        spec=aio.UnaryUnaryMultiCallable,
        side_effect=[exceptions.NotFound(None), fake_call],
    )

    default_retry = retry_async.AsyncRetry()
    default_timeout = timeout.ConstantTimeout(60)
    default_compression = Compression.Gzip
    wrapped_method = gapic_v1.method_async.wrap_method(
        method, default_retry, default_timeout, default_compression
    )

    result = await wrapped_method(
        retry=retry_async.AsyncRetry(
            retry_async.if_exception_type(exceptions.NotFound)
        ),
        timeout=timeout.ConstantTimeout(22),
        compression=Compression.Deflate,
    )

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(
        timeout=22, compression=Compression.Deflate, metadata=mock.ANY
    )


@pytest.mark.asyncio
async def test_wrap_method_with_overriding_timeout_as_a_number():
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)
    default_retry = retry_async.AsyncRetry()
    default_timeout = timeout.ConstantTimeout(60)
    wrapped_method = gapic_v1.method_async.wrap_method(
        method, default_retry, default_timeout
    )

    result = await wrapped_method(timeout=22)

    assert result == 42

    actual_timeout = method.call_args[1]["timeout"]
    metadata = method.call_args[1]["metadata"]
    assert metadata == mock.ANY
    assert actual_timeout == pytest.approx(22, abs=0.05)


@pytest.mark.asyncio
async def test_wrap_method_without_wrap_errors():
    fake_call = mock.AsyncMock()

    wrapped_method = gapic_v1.method_async.wrap_method(fake_call, kind="rest")
    with mock.patch("google.api_core.grpc_helpers_async.wrap_errors") as method:
        await wrapped_method()

        method.assert_not_called()


_ASYNC_SERVICE_DEFAULT_SPAN_ATTRIBUTES = {
    "rpc.system.name": "grpc",
    "rpc.method": "google.test.AsyncService/AsyncMethod",
}


@pytest.mark.asyncio
async def test_wrap_method_async_with_otel_tracing(mock_otel):
    """Proves that method_async.wrap_method creates a T3 span upon invocation."""
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped_method = gapic_v1.method_async.wrap_method(
        method,
        method_name="google.test.AsyncService/AsyncMethod",
    )
    result = await wrapped_method(1, 2, meep="moop")

    assert result == 42
    mock_otel.tracer.start_as_current_span.assert_called_once_with(
        "google.test.AsyncService/AsyncMethod",
        kind="CLIENT",
        attributes=_ASYNC_SERVICE_DEFAULT_SPAN_ATTRIBUTES,
    )
    mock_otel.span.set_attribute.assert_called_with("rpc.response.status_code", "OK")


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_streaming_skips_span(mock_otel):
    """Proves that method_async.wrap_method with is_streaming=True skips span creation."""
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    wrapped = gapic_v1.method_async.wrap_method(
        method,
        method_name="google.test.AsyncService/AsyncMethod",
        is_streaming=True,
    )
    result = await wrapped(1, 2)

    assert_uninstrumented_gapic_callable(
        wrapped,
        result,
        method,
        mock_trace=mock_otel.trace,
        expected_result=42,
    )


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_custom_client_options(mock_otel):
    """Proves that method_async.wrap_method forwards custom client_options tracer_provider."""
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    mock_provider = mock.Mock()
    mock_provider.get_tracer.return_value = mock_otel.tracer
    client_options = client_options_lib.ClientOptions(tracer_provider=mock_provider)

    wrapped = gapic_v1.method_async.wrap_method(
        method,
        client_options=client_options,
        method_name="google.test.AsyncService/AsyncMethod",
    )
    result = await wrapped(1, 2)

    assert result == 42
    mock_provider.get_tracer.assert_called_once_with("google.api_core")
    mock_otel.tracer.start_as_current_span.assert_called_once_with(
        "google.test.AsyncService/AsyncMethod",
        kind="CLIENT",
        attributes=_ASYNC_SERVICE_DEFAULT_SPAN_ATTRIBUTES,
    )
    mock_otel.span.set_attribute.assert_called_with("rpc.response.status_code", "OK")


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_with_client_info(mock_otel):
    """Proves that method_async.wrap_method omits deferred gcp.client.* attributes even with client_info."""
    fake_call = grpc_helpers_async.FakeUnaryUnaryCall(42)
    method = mock.Mock(spec=aio.UnaryUnaryMultiCallable, return_value=fake_call)

    info = client_info.ClientInfo(client_library_version="3.0.0")

    wrapped = gapic_v1.method_async.wrap_method(
        method,
        client_info=info,
        method_name="google.test.AsyncService/AsyncMethod",
    )
    result = await wrapped(1, 2)

    assert result == 42
    mock_otel.tracer.start_as_current_span.assert_called_once_with(
        "google.test.AsyncService/AsyncMethod",
        kind="CLIENT",
        attributes=_ASYNC_SERVICE_DEFAULT_SPAN_ATTRIBUTES,
    )
    mock_otel.span.set_attribute.assert_called_with("rpc.response.status_code", "OK")
