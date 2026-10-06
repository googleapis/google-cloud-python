# Copyright 2025 Google LLC
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

from google.cloud.spanner_v1.metrics.metrics_interceptor import (
    AsyncMetricsInterceptor,
    MetricsInterceptor,
    _AsyncStreamingResponseWrapper,
    _AsyncUnaryResponseWrapper,
    _StreamingResponseWrapper,
)
from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)


@pytest.fixture
def interceptor():
    SpannerMetricsTracerFactory(enabled=True)
    return MetricsInterceptor()


@pytest.fixture
def mock_tracer_ctx():
    tracer = MockMetricTracer()
    token = SpannerMetricsTracerFactory._current_metrics_tracer_ctx.set(tracer)
    yield tracer
    SpannerMetricsTracerFactory._current_metrics_tracer_ctx.reset(token)


class MockMetricTracer:
    def __init__(self):
        self.project = None
        self.instance = None
        self.database = None
        self.record_attempt_start = MagicMock()
        self.record_attempt_completion = MagicMock()
        self.set_method = MagicMock()
        self.record_front_end_metrics = MagicMock()
        self.set_project = MagicMock()
        self.set_instance = MagicMock()
        self.set_database = MagicMock()
        self.client_attributes = {}


def test_parse_resource_path_valid(interceptor):
    path = "projects/my_project/instances/my_instance/databases/my_database"
    expected = {
        "project": "my_project",
        "instance": "my_instance",
        "database": "my_database",
    }
    assert interceptor._parse_resource_path(path) == expected


def test_parse_resource_path_invalid(interceptor):
    path = "invalid/path"
    expected = {}
    assert interceptor._parse_resource_path(path) == expected


def test_extract_resource_from_path(interceptor):
    metadata = [
        (
            "google-cloud-resource-prefix",
            "projects/my_project/instances/my_instance/databases/my_database",
        )
    ]
    expected = {
        "project": "my_project",
        "instance": "my_instance",
        "database": "my_database",
    }
    assert interceptor._extract_resource_from_path(metadata) == expected


def test_set_metrics_tracer_attributes(interceptor, mock_tracer_ctx):
    # mock_tracer_ctx fixture sets the ContextVar
    resources = {
        "project": "my_project",
        "instance": "my_instance",
        "database": "my_database",
    }

    interceptor._set_metrics_tracer_attributes(resources)
    mock_tracer_ctx.set_project.assert_called_with("my_project")
    mock_tracer_ctx.set_instance.assert_called_with("my_instance")
    mock_tracer_ctx.set_database.assert_called_with("my_database")


def test_intercept_with_tracer(interceptor, mock_tracer_ctx):
    # mock_tracer_ctx fixture sets the ContextVar
    invoked_response = Mock()
    invoked_response.initial_metadata.return_value = []

    mock_invoked_method = MagicMock(return_value=invoked_response)
    call_details = MagicMock(
        method="spanner.someMethod",
        metadata=[
            (
                "google-cloud-resource-prefix",
                "projects/my_project/instances/my_instance/databases/my_database",
            )
        ],
    )

    response = interceptor.intercept(mock_invoked_method, "request", call_details)
    assert response == invoked_response
    mock_tracer_ctx.record_attempt_start.assert_called()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()
    mock_tracer_ctx.record_front_end_metrics.assert_called_once()
    mock_invoked_method.assert_called_once_with("request", call_details)


@pytest.fixture
def async_interceptor():
    SpannerMetricsTracerFactory(enabled=True)
    return AsyncMetricsInterceptor()


@pytest.mark.asyncio
async def test_async_intercept_unary_unary(async_interceptor, mock_tracer_ctx):
    class MockUnaryCall:
        def initial_metadata(self):
            return [("server-timing", "gfet4t7; dur=55")]

        def __await__(self):
            async def _coroutine():
                return "unary_result"

            return _coroutine().__await__()

    async def mock_continuation(call_details, request):
        return MockUnaryCall()

    call_details = MagicMock(
        method="/google.spanner.v1.Spanner/ExecuteSql",
        metadata=[
            (
                "google-cloud-resource-prefix",
                "projects/my_project/instances/my_instance/databases/my_database",
            )
        ],
    )

    wrapped_call = await async_interceptor.intercept_unary_unary(
        mock_continuation, call_details, "request_payload"
    )
    assert isinstance(wrapped_call, _AsyncUnaryResponseWrapper)
    result = await wrapped_call
    assert result == "unary_result"
    mock_tracer_ctx.record_attempt_start.assert_called_once()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()
    mock_tracer_ctx.record_front_end_metrics.assert_called_once()


@pytest.mark.asyncio
async def test_async_intercept_stream_unary(async_interceptor, mock_tracer_ctx):
    class MockStreamUnaryCall:
        def initial_metadata(self):
            return []

        def __await__(self):
            async def _coroutine():
                return "stream_unary_result"

            return _coroutine().__await__()

    async def mock_continuation(call_details, request_iterator):
        return MockStreamUnaryCall()

    call_details = MagicMock(
        method="/google.spanner.v1.Spanner/Commit",
        metadata=[],
    )

    wrapped_call = await async_interceptor.intercept_stream_unary(
        mock_continuation, call_details, ["req1"]
    )
    assert isinstance(wrapped_call, _AsyncUnaryResponseWrapper)
    result = await wrapped_call
    assert result == "stream_unary_result"
    mock_tracer_ctx.record_attempt_start.assert_called_once()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


@pytest.mark.asyncio
async def test_async_intercept_unary_stream(async_interceptor, mock_tracer_ctx):
    # Simulates grpc.aio.UnaryStreamCall: defines __aiter__ returning an async generator,
    # but does NOT define __anext__ on the call object itself.
    class MockUnaryStreamCall:
        def initial_metadata(self):
            return [("server-timing", "afe; dur=25")]

        def __aiter__(self):
            async def _generator():
                yield "chunk_1"
                yield "chunk_2"

            return _generator()

    call = MockUnaryStreamCall()
    assert hasattr(call, "__aiter__")
    assert not hasattr(call, "__anext__")

    async def mock_continuation(call_details, request):
        return call

    call_details = MagicMock(
        method="/google.spanner.v1.Spanner/ExecuteStreamingSql",
        metadata=[],
    )

    wrapped_stream = await async_interceptor.intercept_unary_stream(
        mock_continuation, call_details, "request_payload"
    )
    assert isinstance(wrapped_stream, _AsyncStreamingResponseWrapper)

    # Before iteration finishes, attempt completion is not yet recorded
    mock_tracer_ctx.record_attempt_start.assert_called_once()
    mock_tracer_ctx.record_attempt_completion.assert_not_called()

    items = []
    async for item in wrapped_stream:
        items.append(item)

    assert items == ["chunk_1", "chunk_2"]
    mock_tracer_ctx.record_attempt_completion.assert_called_once()
    mock_tracer_ctx.record_front_end_metrics.assert_called_once()


@pytest.mark.asyncio
async def test_async_intercept_stream_stream(async_interceptor, mock_tracer_ctx):
    class MockStreamStreamCall:
        def initial_metadata(self):
            return []

        def __aiter__(self):
            async def _generator():
                yield "stream_stream_chunk"

            return _generator()

    async def mock_continuation(call_details, request_iterator):
        return MockStreamStreamCall()

    call_details = MagicMock(
        method="/google.spanner.v1.Spanner/StreamingRead",
        metadata=[],
    )

    wrapped_stream = await async_interceptor.intercept_stream_stream(
        mock_continuation, call_details, ["req1"]
    )
    assert isinstance(wrapped_stream, _AsyncStreamingResponseWrapper)

    items = []
    async for item in wrapped_stream:
        items.append(item)

    assert items == ["stream_stream_chunk"]
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


@pytest.mark.asyncio
async def test_async_intercept_disabled(mock_tracer_ctx):
    SpannerMetricsTracerFactory._metrics_tracer_factory = None
    SpannerMetricsTracerFactory(enabled=False)
    try:
        interceptor = AsyncMetricsInterceptor()

        async def mock_continuation(call_details, request):
            return "raw_unwrapped_response"

        call_details = MagicMock(
            method="/google.spanner.v1.Spanner/ExecuteSql",
            metadata=[],
        )

        result = await interceptor.intercept_unary_unary(
            mock_continuation, call_details, "request_payload"
        )
        assert result == "raw_unwrapped_response"
        mock_tracer_ctx.record_attempt_start.assert_not_called()
    finally:
        SpannerMetricsTracerFactory._metrics_tracer_factory = None


@pytest.mark.asyncio
async def test_async_streaming_response_wrapper_exception(mock_tracer_ctx):
    class FaultyStreamCall:
        def initial_metadata(self):
            return []

        def __aiter__(self):
            async def _generator():
                yield "first_chunk"
                raise RuntimeError("stream_failed")

            return _generator()

    wrapper = _AsyncStreamingResponseWrapper(FaultyStreamCall(), mock_tracer_ctx)

    with pytest.raises(RuntimeError, match="stream_failed"):
        async for _ in wrapper:
            pass

    mock_tracer_ctx.record_attempt_completion.assert_called_once()


@pytest.mark.asyncio
async def test_async_streaming_response_wrapper_delegation(mock_tracer_ctx):
    mock_response = MagicMock()
    mock_response.cancel.return_value = True
    mock_response.cancelled.return_value = False
    mock_response.code.return_value = 0
    mock_response.details.return_value = "details"
    mock_response.done.return_value = True
    mock_response.initial_metadata.return_value = []
    mock_response.time_remaining.return_value = 10.0
    mock_response.trailing_metadata.return_value = []
    mock_response.wait_for_connection.return_value = None
    mock_response.read.return_value = "chunk"
    mock_response.write.return_value = None
    mock_response.done_writing.return_value = None

    wrapper = _AsyncStreamingResponseWrapper(mock_response, mock_tracer_ctx)

    assert wrapper.cancel() is True
    mock_response.cancel.assert_called_once()
    assert wrapper.cancelled() is False
    assert wrapper.code() == 0
    assert wrapper.details() == "details"
    assert wrapper.done() is True
    assert wrapper.initial_metadata() == []
    assert wrapper.time_remaining() == 10.0
    assert wrapper.trailing_metadata() == []
    assert wrapper.wait_for_connection() is None
    assert wrapper.read() == "chunk"
    assert wrapper.write("msg") is None
    mock_response.write.assert_called_once_with("msg")
    assert wrapper.done_writing() is None
    mock_response.done_writing.assert_called_once()
    mock_response.custom_attribute = "custom"
    assert wrapper.custom_attribute == "custom"

    callback = MagicMock()
    wrapper.add_done_callback(callback)
    mock_response.add_done_callback.assert_called_once_with(callback)


@pytest.mark.asyncio
async def test_async_unary_response_wrapper_exception(mock_tracer_ctx):
    class FaultyUnaryCall:
        def initial_metadata(self):
            return []

        def __await__(self):
            async def _coroutine():
                raise RuntimeError("unary_failed")

            return _coroutine().__await__()

    wrapper = _AsyncUnaryResponseWrapper(FaultyUnaryCall(), mock_tracer_ctx)

    with pytest.raises(RuntimeError, match="unary_failed"):
        await wrapper

    mock_tracer_ctx.record_attempt_completion.assert_called_once()


@pytest.mark.asyncio
async def test_async_unary_response_wrapper_delegation(mock_tracer_ctx):
    mock_response = MagicMock()
    mock_response.cancel.return_value = True
    mock_response.cancelled.return_value = False
    mock_response.code.return_value = 0
    mock_response.details.return_value = "details"
    mock_response.done.return_value = True
    mock_response.initial_metadata.return_value = []
    mock_response.time_remaining.return_value = 10.0
    mock_response.trailing_metadata.return_value = []
    mock_response.wait_for_connection.return_value = None
    mock_response.write.return_value = None
    mock_response.done_writing.return_value = None
    mock_response.custom_attribute = "custom"

    wrapper = _AsyncUnaryResponseWrapper(mock_response, mock_tracer_ctx)

    assert wrapper.cancel() is True
    mock_response.cancel.assert_called_once()
    assert wrapper.cancelled() is False
    assert wrapper.code() == 0
    assert wrapper.details() == "details"
    assert wrapper.done() is True
    assert wrapper.initial_metadata() == []
    assert wrapper.time_remaining() == 10.0
    assert wrapper.trailing_metadata() == []
    assert wrapper.wait_for_connection() is None
    assert wrapper.write("msg") is None
    mock_response.write.assert_called_once_with("msg")
    assert wrapper.done_writing() is None
    mock_response.done_writing.assert_called_once()
    assert wrapper.custom_attribute == "custom"

    callback = MagicMock()
    wrapper.add_done_callback(callback)
    mock_response.add_done_callback.assert_called_once_with(callback)


def test_async_unary_response_wrapper_del_unrecorded(mock_tracer_ctx):
    mock_response = MagicMock()
    wrapper = _AsyncUnaryResponseWrapper(mock_response, mock_tracer_ctx)
    wrapper.__del__()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()

    # Second call should not record again
    wrapper.__del__()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


@pytest.mark.asyncio
async def test_async_streaming_response_wrapper_anext_direct(mock_tracer_ctx):
    class MockCall:
        def initial_metadata(self):
            return []

        def __aiter__(self):
            async def _generator():
                yield "val1"
                yield "val2"

            return _generator()

    wrapper = _AsyncStreamingResponseWrapper(MockCall(), mock_tracer_ctx)
    # Direct __anext__ without calling __aiter__ first (matching StreamedResultSet._consume_next)
    assert await wrapper.__anext__() == "val1"
    assert await wrapper.__anext__() == "val2"
    with pytest.raises(StopAsyncIteration):
        await wrapper.__anext__()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


@pytest.mark.asyncio
async def test_async_streaming_response_wrapper_anext_without_aiter(mock_tracer_ctx):
    class MockCallWithoutAiter:
        def initial_metadata(self):
            return []

        async def __anext__(self):
            raise StopAsyncIteration

    wrapper = _AsyncStreamingResponseWrapper(MockCallWithoutAiter(), mock_tracer_ctx)
    with pytest.raises(StopAsyncIteration):
        await wrapper.__anext__()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


@pytest.mark.asyncio
async def test_async_streaming_response_wrapper_awaitable_metadata(mock_tracer_ctx):
    class MockCallAwaitableMetadata:
        async def initial_metadata(self):
            return [("server-timing", "gfet4t7; dur=42")]

        def __aiter__(self):
            async def _generator():
                yield "item"

            return _generator()

    wrapper = _AsyncStreamingResponseWrapper(
        MockCallAwaitableMetadata(), mock_tracer_ctx
    )
    async for _ in wrapper:
        pass
    mock_tracer_ctx.record_front_end_metrics.assert_called_once_with(
        [("server-timing", "gfet4t7; dur=42")]
    )


def test_async_streaming_response_wrapper_del_unrecorded(mock_tracer_ctx):
    mock_response = MagicMock()
    wrapper = _AsyncStreamingResponseWrapper(mock_response, mock_tracer_ctx)
    wrapper.__del__()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()

    # Second call should not record again
    wrapper.__del__()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


@pytest.mark.asyncio
async def test_async_streaming_response_wrapper_with_streamed_result_set(
    mock_tracer_ctx,
):
    from google.cloud.spanner_v1._async.streamed import StreamedResultSet
    from google.cloud.spanner_v1._helpers import _make_value_pb
    from google.cloud.spanner_v1.types import (
        PartialResultSet,
        ResultSetMetadata,
        StructType,
        Type,
        TypeCode,
    )

    metadata = ResultSetMetadata(
        row_type=StructType(
            fields=[StructType.Field(name="col", type_=Type(code=TypeCode.STRING))]
        )
    )
    partial_1 = PartialResultSet(metadata=metadata)
    partial_1.values.append(_make_value_pb("val1"))
    partial_2 = PartialResultSet()
    partial_2.values.append(_make_value_pb("val2"))

    class MockAsyncStreamCall:
        def initial_metadata(self):
            return [("server-timing", "gfet4t7; dur=50")]

        def __aiter__(self):
            async def _gen():
                yield partial_1
                yield partial_2

            return _gen()

    call = MockAsyncStreamCall()
    wrapper = _AsyncStreamingResponseWrapper(call, mock_tracer_ctx)

    streamed = StreamedResultSet(wrapper)
    rows = []
    async for row in streamed:
        rows.append(row)

    assert rows == [["val1"], ["val2"]]
    mock_tracer_ctx.record_attempt_completion.assert_called_once()
    mock_tracer_ctx.record_front_end_metrics.assert_called_once()


def test_sync_streaming_response_wrapper(mock_tracer_ctx):
    mock_response = iter(["item1", "item2"])
    wrapper = _StreamingResponseWrapper(mock_response, mock_tracer_ctx)

    items = list(wrapper)
    assert items == ["item1", "item2"]
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


def test_sync_streaming_response_wrapper_direct_next(mock_tracer_ctx):
    mock_response = ["item1"]
    wrapper = _StreamingResponseWrapper(mock_response, mock_tracer_ctx)

    assert next(wrapper) == "item1"
    with pytest.raises(StopIteration):
        next(wrapper)
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


def test_sync_streaming_response_wrapper_exception(mock_tracer_ctx):
    def faulty_generator():
        yield "item1"
        raise RuntimeError("stream_failed")

    wrapper = _StreamingResponseWrapper(faulty_generator(), mock_tracer_ctx)
    with pytest.raises(RuntimeError, match="stream_failed"):
        list(wrapper)
    mock_tracer_ctx.record_attempt_completion.assert_called_once()


def test_sync_streaming_response_wrapper_del_unrecorded(mock_tracer_ctx):
    mock_response = MagicMock()
    wrapper = _StreamingResponseWrapper(mock_response, mock_tracer_ctx)
    wrapper.__del__()
    mock_tracer_ctx.record_attempt_completion.assert_called_once()
