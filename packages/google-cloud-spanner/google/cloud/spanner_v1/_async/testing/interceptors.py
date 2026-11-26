# Copyright 2024 Google LLC All rights reserved.
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

import inspect
import threading
from collections import defaultdict

import grpc
from google.api_core.exceptions import Aborted

from google.cloud.spanner_v1.request_id_header import parse_request_id

X_GOOG_REQUEST_ID = "x-goog-spanner-request-id"


def _normalize_method_name(method) -> str:
    """Decode gRPC method names from bytes to str when needed."""
    if isinstance(method, bytes):
        return method.decode("utf-8")
    return method


def _extract_request_id(client_call_details) -> str:
    """Extract and validate the x-goog-spanner-request-id metadata header."""
    metadata = client_call_details.metadata or ()
    x_goog_request_id = None
    for key, value in metadata:
        decoded_key = key.decode("utf-8") if isinstance(key, bytes) else key
        if decoded_key == X_GOOG_REQUEST_ID:
            x_goog_request_id = (
                value.decode("utf-8") if isinstance(value, bytes) else value
            )
            break

    if not x_goog_request_id:
        method = _normalize_method_name(client_call_details.method)
        raise ValueError(f"Missing {X_GOOG_REQUEST_ID} header in {method}")

    return x_goog_request_id


class MethodCountAsyncInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor,
    grpc.aio.UnaryStreamClientInterceptor,
):
    def __init__(self):
        self._counts = defaultdict(int)

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        self._counts[_normalize_method_name(client_call_details.method)] += 1
        return await continuation(client_call_details, request)

    async def intercept_unary_stream(self, continuation, client_call_details, request):
        self._counts[_normalize_method_name(client_call_details.method)] += 1
        return await continuation(client_call_details, request)

    def reset(self):
        self._counts = defaultdict(int)


class MethodAbortAsyncInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor,
    grpc.aio.UnaryStreamClientInterceptor,
):
    def __init__(self):
        self._method_to_abort = None
        self._count = 0
        self._max_raise_count = 1
        self._connection = None

    async def _maybe_raise_aborted(self, client_call_details):
        method = _normalize_method_name(client_call_details.method)
        if self._count < self._max_raise_count and method == self._method_to_abort:
            self._count += 1
            if (
                self._connection is not None
                and self._connection._transaction is not None
            ):
                rollback_result = self._connection._transaction.rollback()
                if inspect.isawaitable(rollback_result):
                    await rollback_result
            raise Aborted("Thrown from Async ClientInterceptor for testing")

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        await self._maybe_raise_aborted(client_call_details)
        return await continuation(client_call_details, request)

    async def intercept_unary_stream(self, continuation, client_call_details, request):
        await self._maybe_raise_aborted(client_call_details)
        return await continuation(client_call_details, request)

    def set_method_to_abort(self, method_to_abort, connection=None, max_raise_count=1):
        self._method_to_abort = method_to_abort
        self._count = 0
        self._max_raise_count = max_raise_count
        self._connection = connection

    def reset(self):
        self._method_to_abort = None
        self._count = 0
        self._max_raise_count = 1
        self._connection = None


class XGoogRequestIDHeaderAsyncInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor,
    grpc.aio.UnaryStreamClientInterceptor,
):
    def __init__(self):
        self._unary_req_segments = []
        self._stream_req_segments = []
        self.__lock = threading.Lock()

    def _record_request_id(self, client_call_details, target_segments):
        x_goog_request_id = _extract_request_id(client_call_details)
        method = _normalize_method_name(client_call_details.method)
        with self.__lock:
            target_segments.append((method, parse_request_id(x_goog_request_id)))

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        self._record_request_id(client_call_details, self._unary_req_segments)
        return await continuation(client_call_details, request)

    async def intercept_unary_stream(self, continuation, client_call_details, request):
        self._record_request_id(client_call_details, self._stream_req_segments)
        return await continuation(client_call_details, request)

    @property
    def unary_request_ids(self):
        return self._unary_req_segments

    @property
    def stream_request_ids(self):
        return self._stream_req_segments

    def reset(self):
        with self.__lock:
            self._stream_req_segments.clear()
            self._unary_req_segments.clear()
