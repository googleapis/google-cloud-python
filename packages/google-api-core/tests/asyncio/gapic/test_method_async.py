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

import asyncio
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


@pytest.fixture(autouse=True)
def set_event_loop():
    try:
        asyncio.get_running_loop()
        yield
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            yield
        finally:
            loop.close()
            asyncio.set_event_loop(None)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kwargs,capabilities_enabled",
    [
        (
            {
                "method_name": "google.cloud.secretmanager.v1.SecretManagerService/ListSecrets"
            },
            False,
        ),
        ({}, True),
        (
            {
                "method_name": "/google.cloud.secretmanager.v1.SecretManagerService/StreamingRead",
                "is_streaming": True,
            },
            True,
        ),
        (
            {
                "method_name": "google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
                "kind": "unsupported_transport",
            },
            True,
        ),
    ],
    ids=[
        "disabled_by_flag",
        "omitted_method_name",
        "streaming_skipped",
        "unsupported_kind_skipped",
    ],
)
async def test_wrap_method_async_otel_tracing_skips_span(
    monkeypatch, kwargs, capabilities_enabled
):
    """Proves that under various gating conditions, no async Tier 3 span is created."""
    mock_target = mock.AsyncMock(return_value="success")
    mock_trace = mock.Mock()

    with (
        mock.patch(
            "google.api_core._observability.is_otel_capabilities_enabled",
            return_value=capabilities_enabled,
        ),
        mock.patch.dict(
            "sys.modules",
            {
                "opentelemetry": mock.Mock(trace=mock_trace),
                "opentelemetry.trace": mock_trace,
            },
        ),
    ):
        wrapped = gapic_v1.method_async.wrap_method(mock_target, **kwargs)
        result = await wrapped()

    assert result == "success"
    mock_trace.get_tracer.assert_not_called()


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_enabled_success(mock_otel):
    """Proves that when OpenTelemetry tracing is enabled and method_name is passed, a T3 client span is started and awaited."""
    mock_target = mock.AsyncMock(return_value="async_success")

    wrapped = gapic_v1.method_async.wrap_method(
        mock_target,
        default_timeout=60,
        method_name="/google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
        kind="grpc_asyncio",
    )
    result = await wrapped()

    assert result == "async_success"
    mock_otel.tracer.start_as_current_span.assert_called_once_with(
        "google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
        kind="CLIENT",
        attributes={
            "rpc.system.name": "grpc",
            "rpc.method": "google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
        },
    )
    mock_otel.span.set_attribute.assert_called_with("rpc.response.status_code", "OK")


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["rest", "rest_asyncio"])
async def test_wrap_method_async_otel_tracing_enabled_rest_transports(mock_otel, kind):
    """Proves that when kind is 'rest' or 'rest_asyncio', a T3 client span is started."""
    mock_target = mock.AsyncMock(return_value="rest_success")

    wrapped = gapic_v1.method_async.wrap_method(
        mock_target,
        default_timeout=60,
        method_name="/google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
        kind=kind,
    )
    result = await wrapped()

    assert result == "rest_success"
    mock_otel.tracer.start_as_current_span.assert_called_once_with(
        "google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
        kind="CLIENT",
        attributes={
            "rpc.system.name": "grpc",
            "rpc.method": "google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
        },
    )
    mock_otel.span.set_attribute.assert_called_with("rpc.response.status_code", "OK")


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_coroutine_duration(mock_otel):
    """Proves that the span remains active across asynchronous awaits and closes only after completion."""
    span_open_during_call = False

    async def delayed_target(*args, **kwargs):
        nonlocal span_open_during_call
        span_open_during_call = (
            mock_otel.tracer.start_as_current_span.return_value.__enter__.called
            and not mock_otel.tracer.start_as_current_span.return_value.__exit__.called
        )
        await asyncio.sleep(0.01)
        return "delayed_result"

    wrapped = gapic_v1.method_async.wrap_method(
        delayed_target,
        method_name="/google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
    )
    result = await wrapped()

    assert result == "delayed_result"
    assert span_open_during_call is True
    assert mock_otel.tracer.start_as_current_span.return_value.__exit__.called is True


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_custom_client_options(mock_otel):
    """Proves that providing client_options with a custom tracer_provider uses that provider."""
    mock_target = mock.AsyncMock(return_value="success")

    mock_provider = mock.Mock()
    mock_provider.get_tracer.return_value = mock_otel.tracer

    client_options = client_options_lib.ClientOptions(tracer_provider=mock_provider)

    wrapped = gapic_v1.method_async.wrap_method(
        mock_target,
        client_options=client_options,
        method_name="/google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
    )
    result = await wrapped()

    assert result == "success"
    mock_provider.get_tracer.assert_called_once_with("google.api_core")


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_dict_client_options(mock_otel):
    """Proves that providing a dict with tracer_provider uses that provider."""
    mock_target = mock.AsyncMock(return_value="success")

    mock_provider = mock.Mock()
    mock_provider.get_tracer.return_value = mock_otel.tracer

    wrapped = gapic_v1.method_async.wrap_method(
        mock_target,
        client_options={"tracer_provider": mock_provider},
        method_name="/google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
    )
    result = await wrapped()

    assert result == "success"
    mock_provider.get_tracer.assert_called_once_with("google.api_core")


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_enabled_error(mock_otel):
    """Proves that on async error, status code and error attributes are recorded and exception is raised."""
    error = exceptions.NotFound("Secret not found")
    mock_target = mock.AsyncMock(side_effect=error)

    wrapped = gapic_v1.method_async.wrap_method(
        mock_target,
        method_name="/google.cloud.secretmanager.v1.SecretManagerService/GetSecret",
    )

    with pytest.raises(exceptions.NotFound):
        await wrapped()

    mock_otel.span.set_attribute.assert_any_call(
        "rpc.response.status_code", "NOT_FOUND"
    )


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_records_gcp_error_attributes(mock_otel):
    """Proves that GCP error attributes (domain, reason, metadata) are recorded on the span."""
    error_info = mock.Mock(
        domain="googleapis.com",
        reason="RESOURCE_NOT_FOUND",
        metadata={"service": "secretmanager"},
    )
    error = exceptions.GoogleAPICallError("Resource not found")
    error._error_info = error_info
    mock_target = mock.AsyncMock(side_effect=error)

    wrapped = gapic_v1.method_async.wrap_method(
        mock_target,
        method_name="/google.cloud.secretmanager.v1.SecretManagerService/GetSecret",
    )

    with pytest.raises(exceptions.GoogleAPICallError):
        await wrapped()

    mock_otel.span.set_attribute.assert_any_call("gcp.errors.domain", "googleapis.com")
    mock_otel.span.set_attribute.assert_any_call("error.type", "RESOURCE_NOT_FOUND")
    mock_otel.span.set_attribute.assert_any_call(
        "gcp.errors.metadata.service", "secretmanager"
    )


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_import_error(monkeypatch):
    """Proves that if opentelemetry fails to import, method execution proceeds gracefully without tracing."""
    mock_target = mock.AsyncMock(return_value="graceful_success")

    with (
        mock.patch(
            "google.api_core._observability.is_otel_capabilities_enabled",
            return_value=True,
        ),
        mock.patch.dict("sys.modules", {"opentelemetry": None}),
    ):
        wrapped = gapic_v1.method_async.wrap_method(
            mock_target,
            method_name="/google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
        )
        result = await wrapped()

    assert result == "graceful_success"


@pytest.mark.asyncio
async def test_wrap_method_async_otel_tracing_start_span_error_bypasses_tracing(
    mock_otel,
):
    """Proves that if tracer.start_as_current_span throws an exception, the call executes cleanly."""
    mock_otel.tracer.start_as_current_span.side_effect = RuntimeError("Tracing broken")
    mock_target = mock.AsyncMock(return_value="resilient_success")

    wrapped = gapic_v1.method_async.wrap_method(
        mock_target,
        method_name="/google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
    )
    result = await wrapped()

    assert result == "resilient_success"
