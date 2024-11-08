# Copyright 2024 Google LLC
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

from google.cloud.bigtable_v2.types.bigtable import ExecuteQueryResponse
from google.cloud.bigtable_v2.types.data import ProtoRows, Value as PBValue
import grpc.aio


try:
    # async mock for python3.7-10
    from asyncio import coroutine

    def async_mock(return_value=None):
        coro = mock.Mock(name="CoroutineResult")
        corofunc = mock.Mock(name="CoroutineFunction", side_effect=coroutine(coro))
        corofunc.coro = coro
        corofunc.coro.return_value = return_value
        return corofunc

except ImportError:
    # async mock for python3.11 or later
    from unittest.mock import AsyncMock

    def async_mock(return_value=None):
        return AsyncMock(return_value=return_value)


# ExecuteQueryResponse(
#                 metadata={
#                     "proto_schema": {
#                         "columns": [
#                             {"name": "test1", "type_": TYPE_INT},
#                             {"name": "test2", "type_": TYPE_INT},
#                         ]
#                     }
#                 }
#             ),
#             ExecuteQueryResponse(
#                 results={"proto_rows_batch": {"batch_data": messages[0]}}
#             ),


def response_with_metadata():
    schema = {"a": "string_type", "b": "int64_type"}
    return ExecuteQueryResponse(
        {
            "metadata": {
                "proto_schema": {
                    "columns": [
                        {"name": name, "type_": {_type: {}}}
                        for name, _type in schema.items()
                    ]
                }
            }
        }
    )


def response_with_result(*args, resume_token=None):
    if resume_token is None:
        resume_token_dict = {}
    else:
        resume_token_dict = {"resume_token": resume_token}

    values = []
    for column_value in args:
        if column_value is None:
            pb_value = PBValue({})
        else:
            pb_value = PBValue(
                {
                    "int_value"
                    if isinstance(column_value, int)
                    else "string_value": column_value
                }
            )
        values.append(pb_value)
    rows = ProtoRows(values=values)

    return ExecuteQueryResponse(
        {
            "results": {
                "proto_rows_batch": {
                    "batch_data": ProtoRows.serialize(rows),
                },
                **resume_token_dict,
            }
        }
    )


class ExecuteQueryStreamMock:
    def __init__(self, parent):
        self.parent = parent
        self.iter = iter(self.parent.values)

    def __call__(self, *args, **kwargs):
        request = args[0]

        self.parent.execute_query_calls.append(request)
        if request.resume_token:
            self.parent.resume_tokens.append(request.resume_token)

        def stream():
            for value in self.iter:
                if isinstance(value, Exception):
                    raise value
                else:
                    yield value

        return stream()


class ChannelMock:
    def __init__(self):
        self.execute_query_calls = []
        self.values = []
        self.resume_tokens = []

    def set_values(self, values):
        self.values = values

    def unary_unary(self, *args, **kwargs):
        return mock.MagicMock()

    def unary_stream(self, *args, **kwargs):
        if args[0] == "/google.bigtable.v2.Bigtable/ExecuteQuery":
            return ExecuteQueryStreamMock(self)
        return mock.MagicMock()


class ChannelMockAsync(grpc.aio.Channel, mock.MagicMock):
    def __init__(self, *args, **kwargs):
        mock.MagicMock.__init__(self, *args, **kwargs)
        self.execute_query_calls = []
        self.values = []
        self.resume_tokens = []
        self._iter = []

    def get_async_get(self, *args, **kwargs):
        return self.async_gen

    def set_values(self, values):
        self.values = values
        self._iter = iter(self.values)

    def unary_unary(self, *args, **kwargs):
        return async_mock()

    def unary_stream(self, *args, **kwargs):
        if args[0] == "/google.bigtable.v2.Bigtable/ExecuteQuery":

            async def async_gen(*args, **kwargs):
                for value in self._iter:
                    yield value

            iter = async_gen()

            class UnaryStreamCallMock(grpc.aio.UnaryStreamCall):
                def __aiter__(self):
                    async def _impl(*args, **kwargs):
                        try:
                            while True:
                                yield await self.read()
                        except StopAsyncIteration:
                            pass

                    return _impl()

                async def read(self):
                    value = await iter.__anext__()
                    if isinstance(value, Exception):
                        raise value
                    return value

                def add_done_callback(*args, **kwargs):
                    pass

                def cancel(*args, **kwargs):
                    pass

                def cancelled(*args, **kwargs):
                    pass

                def code(*args, **kwargs):
                    pass

                def details(*args, **kwargs):
                    pass

                def done(*args, **kwargs):
                    pass

                def initial_metadata(*args, **kwargs):
                    pass

                def time_remaining(*args, **kwargs):
                    pass

                def trailing_metadata(*args, **kwargs):
                    pass

                async def wait_for_connection(*args, **kwargs):
                    return async_mock()

            class UnaryStreamMultiCallableMock(grpc.aio.UnaryStreamMultiCallable):
                def __init__(self, parent):
                    self.parent = parent

                def __call__(
                    self,
                    request,
                    *,
                    timeout=None,
                    metadata=None,
                    credentials=None,
                    wait_for_ready=None,
                    compression=None
                ):
                    self.parent.execute_query_calls.append(request)
                    if request.resume_token:
                        self.parent.resume_tokens.append(request.resume_token)
                    return UnaryStreamCallMock()

                def add_done_callback(*args, **kwargs):
                    pass

                def cancel(*args, **kwargs):
                    pass

                def cancelled(*args, **kwargs):
                    pass

                def code(*args, **kwargs):
                    pass

                def details(*args, **kwargs):
                    pass

                def done(*args, **kwargs):
                    pass

                def initial_metadata(*args, **kwargs):
                    pass

                def time_remaining(*args, **kwargs):
                    pass

                def trailing_metadata(*args, **kwargs):
                    pass

                def wait_for_connection(*args, **kwargs):
                    pass

            # unary_stream should return https://grpc.github.io/grpc/python/grpc_asyncio.html#grpc.aio.UnaryStreamMultiCallable
            # PTAL https://grpc.github.io/grpc/python/grpc_asyncio.html#grpc.aio.Channel.unary_stream
            return UnaryStreamMultiCallableMock(self)
        return async_mock()

    def stream_unary(self, *args, **kwargs) -> grpc.aio.StreamUnaryMultiCallable:
        raise NotImplementedError()

    def stream_stream(self, *args, **kwargs) -> grpc.aio.StreamStreamMultiCallable:
        raise NotImplementedError()

    async def close(self, grace=None):
        return

    async def channel_ready(self):
        return

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def get_state(self, try_to_connect: bool = False) -> grpc.ChannelConnectivity:
        raise NotImplementedError()

    async def wait_for_state_change(self, last_observed_state):
        raise NotImplementedError()
