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

"""Asynchronous Resumable Upload session and helpers using aiohttp."""

import asyncio
import datetime
import inspect
import io
import logging
import time
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    BinaryIO,
    Callable,
    Generator,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from google.api_core import exceptions
from google.api_core.retry import AsyncRetry, AsyncStreamingRetry, Retry
from google.api_core.resumable_transfer import common, upload_state

ResumableUploadConfig = common.ResumableUploadConfig
_format_response_payload = common.format_response_payload

try:
    import aiohttp
except ImportError:  # pragma: NO COVER
    aiohttp = None  # type: ignore

_LOGGER = logging.getLogger(__name__)
_DEFAULT_START_TIMEOUT = 60.0  # seconds for initial start request
_monotonic_clock = time.monotonic


class AsyncResumableUploadSession(common.BaseResumableUploadSession):
    """Manages the full lifecycle of an asynchronous resumable upload session."""

    def __init__(
        self,
        upload_url: Optional[str] = None,
        config: Optional[ResumableUploadConfig] = None,
        resumable_url: Optional[str] = None,
        transport: Optional[Any] = None,
        chunk_size: Optional[int] = None,
        stall_minimum_rate: Optional[int] = None,
        stall_timeout: Optional[float] = None,
    ) -> None:
        """Initializes an AsyncResumableUploadSession.

        Args:
            upload_url: The initial URL for the start request.
            config: Optional upload configuration parameters.
            resumable_url: Pre-existing upload session URL if resuming.
            transport: Optional aiohttp.ClientSession.
            chunk_size: Optional chunk size override in bytes.
            stall_minimum_rate: Optional stall minimum rate override (bytes/s).
            stall_timeout: Optional stall timeout duration override in seconds.
        """
        super().__init__(
            upload_url=upload_url,
            config=config,
            resumable_url=resumable_url,
            transport=transport,
            chunk_size=chunk_size,
            stall_minimum_rate=stall_minimum_rate,
            stall_timeout=stall_timeout,
        )

    def _ensure_aiohttp(self) -> None:
        """Validates that aiohttp dependency is installed.

        Raises:
            ImportError: If aiohttp is not installed.
        """
        if aiohttp is None:
            raise ImportError(
                "aiohttp is required for AsyncResumableUploadSession. "
                "Install with `pip install google-api-core[async_rest]`."
            )

    def _get_async_retry(
        self,
        retry: Optional[Any] = None,
        is_start: bool = False,
    ) -> AsyncRetry:
        """Resolves async retry policy for unary control requests.

        Args:
            retry: Explicit retry policy if provided.
            is_start: Whether this retry policy is for the start request.

        Returns:
            Configured or default AsyncRetry instance.
        """
        if is_start and self._config.start_retry:
            if isinstance(self._config.start_retry, AsyncRetry):
                return self._config.start_retry
            return AsyncRetry(
                predicate=getattr(
                    self._config.start_retry, "_predicate", self._get_retry_predicate()
                ),
                initial=getattr(self._config.start_retry, "_initial", 1.0),
                maximum=getattr(self._config.start_retry, "_maximum", 60.0),
                multiplier=getattr(self._config.start_retry, "_multiplier", 2.0),
                timeout=getattr(self._config.start_retry, "_timeout", None),
            )
        actual_retry = retry if retry is not None else self._config.retry
        if isinstance(actual_retry, AsyncRetry):
            return actual_retry
        if actual_retry is not None:
            return AsyncRetry(
                predicate=getattr(
                    actual_retry, "_predicate", self._get_retry_predicate()
                ),
                initial=getattr(actual_retry, "_initial", 1.0),
                maximum=getattr(actual_retry, "_maximum", 60.0),
                multiplier=getattr(actual_retry, "_multiplier", 2.0),
                timeout=getattr(actual_retry, "_timeout", None),
            )
        return AsyncRetry(predicate=self._get_retry_predicate())

    def _get_async_streaming_retry(
        self,
        retry: Optional[Any] = None,
        on_error: Optional[Callable[[Exception], Any]] = None,
    ) -> AsyncStreamingRetry:
        """Resolves async retry policy for streaming chunk uploads.

        Args:
            retry: Explicit retry policy override if provided.
            on_error: Optional callback executed when an exception triggers a retry attempt.

        Returns:
            Configured or default AsyncStreamingRetry instance.
        """
        actual_retry = retry if retry is not None else self._config.retry
        if isinstance(actual_retry, AsyncStreamingRetry):
            return actual_retry

        predicate = self._get_streaming_predicate()
        initial = getattr(actual_retry, "_initial", 1.0)
        maximum = getattr(actual_retry, "_maximum", 60.0)
        multiplier = getattr(actual_retry, "_multiplier", 2.0)
        timeout = getattr(actual_retry, "_timeout", None)

        user_on_error = getattr(actual_retry, "_on_error", None)

        callbacks = [cb for cb in (user_on_error, on_error) if cb is not None]

        def combined_on_error(exc: Exception) -> Any:
            for cb in callbacks:
                cb(exc)

        return AsyncStreamingRetry(
            predicate=predicate,
            initial=initial,
            maximum=maximum,
            multiplier=multiplier,
            timeout=timeout,
            on_error=combined_on_error if callbacks else None,
        )

    async def _async_retry(
        self,
        func: Callable[[], Awaitable[Any]],
        max_attempts: int = 3,
        initial_delay: float = 0.1,
        max_delay: float = 1.0,
        multiplier: float = 2.0,
    ) -> Any:
        """Executes an async callable with exponential backoff retry logic.

        Maintained for backwards-compatibility with custom async call sites.

        Args:
            func: Async callable to execute with retries.
            max_attempts: Maximum retry attempts before giving up.
            initial_delay: Initial delay in seconds.
            max_delay: Maximum delay ceiling in seconds.
            multiplier: Backoff growth multiplier.

        Returns:
            Result of the executed callable.
        """
        delay = initial_delay
        for attempt in range(max_attempts):
            try:
                return await func()
            except exceptions.MissingStatusHeaderError:
                if attempt == max_attempts - 1:
                    raise
            except exceptions.GoogleAPICallError as exc:
                if exc.code not in common.RETRYABLE_STATUS_CODES:
                    raise
                if attempt == max_attempts - 1:
                    raise
            except Exception:
                if attempt == max_attempts - 1:
                    raise

            await asyncio.sleep(delay)
            delay = min(delay * multiplier, max_delay)

    async def initiate(
        self,
        transport: Any,
        request_body: Union[str, bytes] = "",
        size: Optional[int] = None,
        headers: Optional[Union[Mapping[str, str], Sequence[Tuple[str, str]]]] = None,
        content_type: Optional[str] = None,
        retry: Optional[Union[AsyncRetry, Retry]] = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
    ) -> str:
        """Initiates the upload session by sending the start command asynchronously.

        Args:
            transport: The aiohttp client session.
            request_body: Initial metadata payload sent with start command.
            size: Total stream size in bytes, if known.
            headers: Additional HTTP headers dispatched with start request.
            content_type: MIME type of the stream payload.
            retry: Optional custom retry policy for start request.
            timeout: Optional timeout in seconds for start request.
            deadline: Optional overall upload deadline.
            on_progress: Optional callback for progress updates.

        Returns:
            The upload session URL.

        Raises:
            GoogleAPICallError: If the server rejects the start request.
            MissingStatusHeaderError: If the server response lacks status header.
        """
        self._ensure_aiohttp()
        req_headers = headers if headers is not None else self._config.start_headers
        req_content_type = (
            content_type if content_type is not None else self._config.content_type
        )
        method, url, start_headers, payload = self._state.build_start_request(
            body=request_body,
            headers=req_headers,
            content_type=req_content_type,
            size=size,
        )

        async def do_initiate() -> str:
            timeout_sec = self._get_start_timeout(timeout=timeout, deadline=deadline)
            client_timeout = aiohttp.ClientTimeout(total=timeout_sec)
            async with transport.request(
                method, url, data=payload, headers=start_headers, timeout=client_timeout
            ) as resp:
                resp_headers = dict(resp.headers)
                body = await resp.read()
                if resp.status not in (200, 201):
                    raise exceptions.from_http_status(
                        resp.status, body.decode("utf-8", errors="replace")
                    )
                session_url = self._state.process_start_response(
                    resp.status, resp_headers
                )
                return session_url

        session_url = await self._get_async_retry(retry=retry, is_start=True)(do_initiate)()
        self._notify_progress(common.ProgressState.STARTED, on_progress=on_progress)
        return session_url

    async def _transmit_chunk(
        self,
        transport: Any,
        reader_fn: Callable[[int], Awaitable[bytes]],
        size: Optional[int],
        stream_obj: Any = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
    ) -> Tuple[int, Mapping[str, str], bytes]:
        """Transmits a single data chunk asynchronously via aiohttp with stall control.

        Args:
            transport: The aiohttp client session.
            reader_fn: Async callable returning chunk bytes.
            size: Total stream size in bytes, if known.
            stream_obj: Underlying stream object for recovery seeking.
            timeout: Optional timeout ceiling in seconds.
            deadline: Optional overall deadline.
            on_progress: Optional callback for progress updates.

        Returns:
            Tuple of (status code, headers mapping, response body bytes).

        Raises:
            TransferStalledError: If chunk transfer throughput stalls.
            DeadlineExceeded: If upload deadline is reached.
            GoogleAPICallError: If chunk upload encounters an unrecoverable error.
        """
        chunk_size = self._state.chunk_size

        if self._buffered_chunk is None:
            raw_bytes = await reader_fn(chunk_size)
            if not raw_bytes:
                raw_bytes = b""
            if len(raw_bytes) < chunk_size:
                self._stream_eof = True
            self._buffered_chunk = memoryview(raw_bytes)
            self._buffered_chunk_offset = self._state.bytes_uploaded

        data = self._buffered_chunk
        data_len = len(data)

        if size is not None:
            is_last = self._state.bytes_uploaded + data_len >= size
        else:
            is_last = self._stream_eof and (
                data_len == 0 or len(self._buffered_chunk) == data_len
            )

        method, url, headers, payload = self._state.build_chunk_request(
            data=data,
            is_last_chunk=is_last,
            content_type=self._config.content_type,
        )

        per_attempt_timeout = self._compute_chunk_timeout(
            data_len, timeout=timeout, deadline=deadline
        )
        client_timeout = aiohttp.ClientTimeout(total=per_attempt_timeout)
        try:
            t_start = _monotonic_clock()
            async with transport.request(
                method,
                url,
                data=payload,
                headers=headers,
                timeout=client_timeout,
            ) as resp:
                resp_headers = dict(resp.headers)
                resp_body = await resp.read()
                t_elapsed = _monotonic_clock() - t_start
                if resp.status not in (200, 201):
                    raise exceptions.from_http_status(
                        resp.status, resp_body.decode("utf-8", errors="replace")
                    )
        except (
            asyncio.TimeoutError,
            getattr(aiohttp, "ServerTimeoutError", ()),
        ) as exc:
            self._enrich_exception(exc)
            remaining = self._get_deadline_remaining(deadline)
            if remaining is not None and remaining <= 0:
                dl = deadline or self._config.deadline
                raise exceptions.DeadlineExceeded(
                    f"Resumable upload deadline {dl} exceeded."
                ) from exc
            raise exceptions.TransferStalledError(
                f"Upload stalled: chunk transfer timed out ({exc}).",
                upload_url=self.upload_url,
                chunk_size=self.chunk_size,
            ) from exc
        except Exception as exc:
            self._enrich_exception(exc)
            raise

        self._update_stall_control(data_len, t_start, t_elapsed, deadline=deadline)

        self._state.process_chunk_response(resp.status, resp_headers, data_len)
        self._buffered_chunk = None
        self._notify_progress(
            common.ProgressState.FINALIZED
            if self._state.finished
            else common.ProgressState.UPLOADING,
            on_progress=on_progress,
        )
        return resp.status, resp_headers, resp_body

    async def _recover(
        self,
        transport: Any,
        stream_obj: Any = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
        response_type: Optional[Any] = None,
    ) -> int:
        """Queries server for committed byte offset and adjusts buffer.

        Args:
            transport: The aiohttp client session.
            stream_obj: Underlying stream object to rewind if seekable.
            timeout: Optional timeout in seconds.
            deadline: Optional overall upload deadline.
            on_progress: Optional callback for progress updates.
            response_type: Optional response deserialization type.

        Returns:
            The confirmed server byte offset.

        Raises:
            exceptions.UnseekableStreamError: If server offset precedes buffer and stream cannot be rewound.
            exceptions.GoogleAPICallError: If query request fails on the server.
        """
        method, url, headers, payload = self._state.build_query_request()
        timeout_sec = self._get_start_timeout(timeout=timeout, deadline=deadline)
        client_timeout = aiohttp.ClientTimeout(total=timeout_sec)
        async with transport.request(
            method, url, data=payload, headers=headers, timeout=client_timeout
        ) as resp:
            resp_headers = dict(resp.headers)
            body = await resp.read()
            if resp.status not in (200, 201):
                raise exceptions.from_http_status(
                    resp.status, body.decode("utf-8", errors="replace")
                )

        received = self._state.process_query_response(resp.status, resp_headers)
        if self._state.finished:
            self._response = self._format_response(body, response_type=response_type)
            return received
        self._notify_progress(common.ProgressState.OFFSET_RECEIVED, on_progress=on_progress)
        return self._reposition_stream_offset(stream_obj, received)

    async def cancel(
        self,
        transport: Optional[Any] = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
    ) -> None:
        """Cancels the resumable upload session asynchronously.

        Args:
            transport: Optional aiohttp client session.
            timeout: Optional timeout in seconds.
            deadline: Optional overall upload deadline.

        Raises:
            ValueError: If transport is missing.
            exceptions.GoogleAPICallError: If cancellation request fails on the server.
        """
        self._ensure_aiohttp()
        sess = transport or self._transport
        if sess is None:
            raise ValueError("An aiohttp.ClientSession transport must be provided.")
        method, url, headers, payload = self._state.build_cancel_request()
        timeout_sec = self._get_start_timeout(timeout=timeout, deadline=deadline)
        client_timeout = aiohttp.ClientTimeout(total=timeout_sec)
        async with sess.request(
            method, url, data=payload, headers=headers, timeout=client_timeout
        ) as resp:
            resp_headers = dict(resp.headers)
            body = await resp.read()
            if resp.status not in (200, 201):
                raise exceptions.from_http_status(
                    resp.status, body.decode("utf-8", errors="replace")
                )
            self._state.process_cancel_response(resp.status, resp_headers)

    async def _async_chunk_stream_generator(
        self,
        transport: Any,
        reader_fn: Callable[[int], Awaitable[bytes]],
        size: Optional[int],
        stream_obj: Any = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
        response_type: Optional[Any] = None,
    ) -> AsyncIterator[Tuple[int, Mapping[str, str], bytes]]:
        """Generates chunk transmission responses asynchronously with recovery support for AsyncStreamingRetry.

        Args:
            transport: The aiohttp client session.
            reader_fn: Async callable returning chunk bytes.
            size: Total stream size in bytes, if known.
            stream_obj: Underlying stream object for recovery seeking.
            timeout: Optional per-chunk timeout in seconds.
            deadline: Optional overall upload deadline.
            on_progress: Optional callback receiving progress updates.
            response_type: Optional response deserialization type.

        Yields:
            Tuple of (status code, headers mapping, response body bytes).
        """
        if self._needs_recovery:
            if self._recovered_from_error:
                self._notify_progress(common.ProgressState.RECOVERING, on_progress=on_progress)
            await self._recover(
                transport,
                stream_obj,
                timeout=timeout,
                deadline=deadline,
                on_progress=on_progress,
                response_type=response_type,
            )
            self._needs_recovery = False
            self._recovered_from_error = False

        while not self._state.finished and not self._state.invalid:
            resp_tuple = await self._transmit_chunk(
                transport,
                reader_fn,
                size,
                stream_obj=stream_obj,
                timeout=timeout,
                deadline=deadline,
                on_progress=on_progress,
            )
            if self._state.finished:
                _, _, body_bytes = resp_tuple
                self._response = self._format_response(body_bytes, response_type=response_type)
            yield resp_tuple

    async def upload(
        self,
        stream: Union[AsyncIterable[bytes], BinaryIO, bytes, Iterable[bytes]],
        request_body: Union[str, bytes] = "",
        size: Optional[int] = None,
        headers: Optional[Union[Mapping[str, str], Sequence[Tuple[str, str]]]] = None,
        content_type: Optional[str] = None,
        start_retry: Optional[Union[AsyncRetry, Retry]] = None,
        start_timeout: Optional[float] = None,
        retry: Optional[Union[AsyncRetry, AsyncStreamingRetry, Retry]] = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
        response_type: Optional[Any] = None,
        transport: Optional[Any] = None,
    ) -> Any:
        """Executes the upload asynchronously from start to completion.

        Args:
            stream: Data payload to upload (async iterable, binary stream, bytes, or iterable).
            request_body: Initial metadata payload sent with the start request.
            size: Total stream size in bytes, if known.
            headers: Additional HTTP headers dispatched with start request.
            content_type: MIME type of the stream payload.
            start_retry: Custom retry policy for start request.
            start_timeout: Per-request timeout in seconds for start request.
            retry: Retry policy for chunk uploads and recovery queries.
            timeout: Per-request timeout in seconds for chunk uploads.
            deadline: Overall global deadline for the upload process.
            on_progress: Callback function receiving UploadProgress notifications.
            response_type: Optional response deserialization type or callable.
            transport: Optional aiohttp client session.

        Returns:
            The final server response payload or deserialized response message.

        Raises:
            ValueError: If transport is missing or upload completes without a response.
            GoogleAPICallError: If an unrecoverable API error occurs.
        """
        self._ensure_aiohttp()
        sess = transport or self._transport
        if sess is None:
            raise ValueError("An aiohttp.ClientSession transport must be provided.")

        reader_fn, computed_size, stream_obj = self._prepare_async_reader(stream, size)
        try:
            await self.initiate(
                transport=sess,
                request_body=request_body,
                size=computed_size,
                headers=headers,
                content_type=content_type,
                retry=start_retry or retry,
                timeout=start_timeout or timeout,
                deadline=deadline,
                on_progress=on_progress,
            )

            retry_policy = self._get_async_streaming_retry(
                retry=retry, on_error=self._on_stream_error
            )
            retryable_stream_fn = retry_policy(self._async_chunk_stream_generator)
            stream_iter = await retryable_stream_fn(
                sess,
                reader_fn,
                computed_size,
                stream_obj=stream_obj,
                timeout=timeout,
                deadline=deadline,
                on_progress=on_progress,
                response_type=response_type,
            )
            async for _ in stream_iter:
                pass

            return self._finish_response()
        except Exception as exc:
            self._enrich_exception(exc)
            raise

    async def resume(
        self,
        upload_url: Optional[str] = None,
        stream: Optional[
            Union[AsyncIterable[bytes], BinaryIO, bytes, Iterable[bytes]]
        ] = None,
        size: Optional[int] = None,
        chunk_size: Optional[int] = None,
        retry: Optional[Union[AsyncRetry, AsyncStreamingRetry, Retry]] = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
        response_type: Optional[Any] = None,
        transport: Optional[Any] = None,
    ) -> Any:
        """Resumes an existing upload asynchronously from a saved upload URL.

        Args:
            upload_url: Established upload session URL.
            stream: Data payload to resume uploading.
            size: Total stream size in bytes, if known.
            chunk_size: Optional chunk size override in bytes.
            retry: Retry policy for chunk uploads and recovery queries.
            timeout: Per-request timeout in seconds.
            deadline: Overall global deadline for the upload process.
            on_progress: Callback function receiving UploadProgress notifications.
            response_type: Optional response deserialization type or callable.
            transport: Optional aiohttp client session.

        Returns:
            The final server response payload or deserialized response message.

        Raises:
            ValueError: If required arguments are missing or response not received.
            GoogleAPICallError: If an unrecoverable API error occurs.
        """
        self._ensure_aiohttp()
        sess = transport or self._transport
        if sess is None:
            raise ValueError("An aiohttp.ClientSession transport must be provided.")

        actual_url = upload_url or self.upload_url
        if not actual_url:
            raise ValueError("An upload URL must be provided to resume.")
        if stream is None:
            raise ValueError("A data stream or payload must be provided to resume.")

        if chunk_size is not None:
            self._state._chunk_size = chunk_size
        self._state._resumable_url = actual_url
        self._needs_recovery = True
        self._recovered_from_error = False

        reader_fn, computed_size, stream_obj = self._prepare_async_reader(stream, size)
        try:
            retry_policy = self._get_async_streaming_retry(
                retry=retry, on_error=self._on_stream_error
            )
            retryable_stream_fn = retry_policy(self._async_chunk_stream_generator)
            stream_iter = await retryable_stream_fn(
                sess,
                reader_fn,
                computed_size,
                stream_obj=stream_obj,
                timeout=timeout,
                deadline=deadline,
                on_progress=on_progress,
                response_type=response_type,
            )
            async for _ in stream_iter:
                pass

            return self._finish_response()
        except Exception as exc:
            self._enrich_exception(exc)
            raise

    def _prepare_async_reader(
        self,
        stream: Union[AsyncIterable[bytes], BinaryIO, bytes, Iterable[bytes]],
        size: Optional[int],
    ) -> Tuple[Callable[[int], Awaitable[bytes]], Optional[int], Any]:
        """Creates an asynchronous byte reader and determines stream length.

        Args:
            stream: Input payload (async iterable, binary stream, bytes, or iterable).
            size: Explicit total size in bytes, if known.

        Returns:
            Tuple of (async reader function, computed total size, underlying stream object).

        Raises:
            TypeError: If the stream type is not supported.
        """
        computed_size = size

        if isinstance(stream, (str, dict)):
            raise TypeError(f"Unsupported stream type: {type(stream)}")

        if isinstance(stream, bytes):
            bytes_io = io.BytesIO(stream)
            if computed_size is None:
                computed_size = len(stream)

            async def reader(n: int) -> bytes:
                return bytes_io.read(n)

            return reader, computed_size, bytes_io

        if hasattr(stream, "read") and inspect.iscoroutinefunction(stream.read):
            # Native async reader (e.g. asyncio.StreamReader)
            async def reader(n: int) -> bytes:
                return await stream.read(n)  # type: ignore

            return reader, computed_size, stream

        if hasattr(stream, "read"):
            # Synchronous binary stream: offload blocking reads to worker thread
            sync_stream: Any = stream
            if computed_size is None and hasattr(sync_stream, "getbuffer"):
                computed_size = sync_stream.getbuffer().nbytes

            if hasattr(sync_stream, "tell"):
                try:
                    self._start_stream_offset = sync_stream.tell()
                except (OSError, AttributeError):
                    self._start_stream_offset = 0

            async def reader(n: int) -> bytes:
                return await asyncio.to_thread(sync_stream.read, n)

            return reader, computed_size, sync_stream

        if hasattr(stream, "__aiter__"):
            # Native AsyncIterable[bytes]
            iterator = stream.__aiter__()
            buffer = bytearray()

            async def reader(n: int) -> bytes:
                while len(buffer) < n:
                    try:
                        chunk = await iterator.__anext__()
                        buffer.extend(chunk)
                    except StopAsyncIteration:
                        break
                result = bytes(buffer[:n])
                del buffer[:n]
                return result

            return reader, computed_size, None

        if isinstance(stream, Iterable):
            # Synchronous Iterable[bytes]: offload to worker thread
            iterator = iter(stream)
            buffer = bytearray()

            def _next_chunk():
                try:
                    return next(iterator)
                except StopIteration:
                    return None

            async def reader(n: int) -> bytes:
                while len(buffer) < n:
                    chunk = await asyncio.to_thread(_next_chunk)
                    if chunk is None:
                        break
                    buffer.extend(chunk)
                result = bytes(buffer[:n])
                del buffer[:n]
                return result

            return reader, computed_size, None

        raise TypeError(f"Unsupported stream type: {type(stream)}")
