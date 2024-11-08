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

from __future__ import annotations

import asyncio
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Optional,
    Sequence,
    Tuple,
    TYPE_CHECKING,
)

from google.api_core import retry as retries

from google.cloud.bigtable.data.execute_query._byte_cursor import _ByteCursor
from google.cloud.bigtable.data._helpers import (
    _attempt_timeout_generator,
    _retry_exception_factory,
)
from google.cloud.bigtable.data.exceptions import InvalidExecuteQueryResponse
from google.cloud.bigtable.data.execute_query.values import QueryResultRow
from google.cloud.bigtable.data.execute_query.metadata import Metadata, ProtoMetadata
from google.cloud.bigtable.data.execute_query._reader import (
    _QueryResultRowReader,
    _Reader,
)
from google.cloud.bigtable_v2.types.bigtable import (
    ExecuteQueryRequest as ExecuteQueryRequestPB,
)

if TYPE_CHECKING:
    from google.cloud.bigtable.data import BigtableDataClientAsync


class ExecuteQueryIteratorAsync:
    """
    ExecuteQueryIteratorAsync handles collecting streaming responses from the
    ExecuteQuery RPC and parsing them to QueryResultRows.

    ExecuteQueryIteratorAsync implements Asynchronous Iterator interface and can
    be used with "async for" syntax. It is also a context manager.

    It is **not thread-safe**. It should not be used by multiple asyncio Tasks.

    Args:
        client: bigtable client
        instance_id: id of the instance on which the query is executed
        request_body: dict representing the body of the ExecuteQueryRequest
        attempt_timeout: the time budget for the entire operation, in seconds.
            Failed requests will be retried within the budget.
            Defaults to 600 seconds.
        operation_timeout: the time budget for an individual network request, in seconds.
            If it takes longer than this time to complete, the request will be cancelled with
            a DeadlineExceeded exception, and a retry will be attempted.
            Defaults to the 20 seconds. If None, defaults to operation_timeout.
        req_metadata: metadata used while sending the gRPC request
        retryable_excs: a list of errors that will be retried if encountered.
    Raises:
        RuntimeError: if the instance is not created within an async event loop context.
    """

    def __init__(
        self,
        client: BigtableDataClientAsync,
        instance_id: str,
        app_profile_id: Optional[str],
        request_body: Dict[str, Any],
        attempt_timeout: float | None,
        operation_timeout: float,
        req_metadata: Sequence[Tuple[str, str]] = (),
        retryable_excs: Sequence[type[Exception]] = (),
    ) -> None:
        self._table_name = None
        self._app_profile_id = app_profile_id
        self._client = client
        self._instance_id = instance_id
        self._byte_cursor = _ByteCursor[ProtoMetadata]()
        self._reader: _Reader[QueryResultRow] = _QueryResultRowReader(self._byte_cursor)
        self._result_generator = self._next_impl()
        self._register_instance_task = None
        self._is_closed = False
        self._request_body = request_body
        self._attempt_timeout_gen = _attempt_timeout_generator(
            attempt_timeout, operation_timeout
        )
        retryable_excs = retryable_excs or []
        self._async_stream = retries.retry_target_stream_async(
            self._make_request_with_resume_token,
            retries.if_exception_type(*retryable_excs),
            retries.exponential_sleep_generator(0.01, 60, multiplier=2),
            operation_timeout,
            exception_factory=_retry_exception_factory,
        )
        self._req_metadata = req_metadata

        try:
            self._register_instance_task = asyncio.create_task(
                self._client._register_instance(instance_id, self)
            )
        except RuntimeError as e:
            raise RuntimeError(
                f"{self.__class__.__name__} must be created within an async event loop context."
            ) from e

    @property
    def is_closed(self) -> bool:
        """Returns True if the iterator is closed, False otherwise."""
        return self._is_closed

    @property
    def app_profile_id(self) -> Optional[str]:
        """Returns the app_profile_id of the iterator."""
        return self._app_profile_id

    @property
    def table_name(self) -> Optional[str]:
        """Returns the table_name of the iterator."""
        return self._table_name

    async def _make_request_with_resume_token(self):
        """
        perfoms the rpc call using the correct resume token.
        """
        resume_token = self._byte_cursor.prepare_for_new_request()
        request = ExecuteQueryRequestPB(
            {
                **self._request_body,
                "resume_token": resume_token,
            }
        )
        return await self._client._gapic_client.execute_query(
            request,
            timeout=next(self._attempt_timeout_gen),
            metadata=self._req_metadata,
            retry=None,
        )

    async def _await_metadata(self) -> None:
        """
        If called before the first response was recieved, the first response
        is awaited as part of this call.
        """
        if self._byte_cursor.metadata is None:
            metadata_msg = await self._async_stream.__anext__()
            self._byte_cursor.consume_metadata(metadata_msg)

    async def _next_impl(self) -> AsyncIterator[QueryResultRow]:
        """
        Generator wrapping the response stream which parses the stream results
        and returns full `QueryResultRow`s.
        """
        await self._await_metadata()

        async for response in self._async_stream:
            try:
                bytes_to_parse = self._byte_cursor.consume(response)
                if bytes_to_parse is None:
                    continue

                results = self._reader.consume(bytes_to_parse)
                if results is None:
                    continue

            except ValueError as e:
                raise InvalidExecuteQueryResponse(
                    "Invalid ExecuteQuery response received"
                ) from e

            for result in results:
                yield result
        await self.close()

    async def __anext__(self) -> QueryResultRow:
        if self._is_closed:
            raise StopAsyncIteration
        return await self._result_generator.__anext__()

    def __aiter__(self):
        return self

    async def metadata(self) -> Optional[Metadata]:
        """
        Returns query metadata from the server or None if the iterator was
        explicitly closed.
        """
        if self._is_closed:
            return None
        # Metadata should be present in the first response in a stream.
        if self._byte_cursor.metadata is None:
            try:
                await self._await_metadata()
            except StopIteration:
                return None
        return self._byte_cursor.metadata

    async def close(self) -> None:
        """
        Cancel all background tasks. Should be called all rows were processed.
        """
        if self._is_closed:
            return
        self._is_closed = True
        if self._register_instance_task is not None:
            self._register_instance_task.cancel()
        await self._client._remove_instance_registration(self._instance_id, self)
