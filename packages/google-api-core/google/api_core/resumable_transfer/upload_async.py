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
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

try:
    import aiohttp
except ImportError:  # pragma: NO COVER
    aiohttp = None  # type: ignore

from google.api_core import exceptions
from google.api_core.resumable_transfer import common, upload_state
from google.api_core.resumable_transfer.upload import (
    ResumableUploadConfig,
    _format_response_payload,
)

_LOGGER = logging.getLogger(__name__)
_DEFAULT_START_TIMEOUT = 60.0  # seconds for initial start request
_DONE_SENTINEL = object()
_monotonic_clock = time.monotonic

ResponseProto = TypeVar("ResponseProto")


class _AsyncRecoveryRetransmit(Exception):
    """Internal exception indicating state synchronization succeeded and chunk should retransmit."""

    pass


class AsyncUploadOperation(Generic[ResponseProto], Awaitable[ResponseProto]):
    """Handle representing an active asynchronous upload operation.

    Implements Awaitable[ResponseProto] so awaiting the operation directly
    returns the deserialized response upon transfer completion.
    """

    def __init__(
        self,
        task: asyncio.Task,
        session: "AsyncResumableUploadSession",
        progress_queue: asyncio.Queue,
    ) -> None:
        """Initializes the active upload operation handle.

        Args:
            task: Background asyncio task driving the upload.
            session: Underlying asynchronous resumable upload session.
            progress_queue: Queue used to deliver upload progress updates.
        """
        self._task = task
        self._session = session
        self._progress_queue = progress_queue

    def __await__(self) -> Generator[Any, None, ResponseProto]:
        """Awaits completion of the upload task and returns the server response."""
        return self._task.__await__()

    async def progress(self) -> AsyncIterator[common.UploadProgress]:
        """Returns an asynchronous stream yielding progress snapshots without blocking uploads.

        Yields:
            UploadProgress snapshots for each progress transition.

        Raises:
            Exception: Re-raises any exception encountered during the background transfer.
        """
        while True:
            item = await self._progress_queue.get()
            if item is _DONE_SENTINEL:
                break
            if isinstance(item, Exception):
                raise item
            yield item

    @property
    def response(self) -> Optional[ResponseProto]:
        """The deserialized protobuf response message, or None if in progress."""
        return self._session.response

    @property
    def upload_url(self) -> Optional[str]:
        """The session upload URL."""
        return self._session.upload_url

    @property
    def chunk_size(self) -> int:
        """The negotiated chunk size."""
        return self._session.chunk_size

    @property
    def bytes_uploaded(self) -> int:
        """Total confirmed bytes committed so far."""
        return self._session.bytes_uploaded


class AsyncResumableUploadSession:
    """Manages the full lifecycle of an asynchronous resumable upload session."""

    def __init__(
        self,
        upload_url: Optional[str] = None,
        config: Optional[ResumableUploadConfig] = None,
        resumable_url: Optional[str] = None,
        transport: Optional[Any] = None,
    ) -> None:
        """Initializes an AsyncResumableUploadSession.

        Args:
            upload_url: The initial URL for the start request.
            config: Optional upload configuration parameters.
            resumable_url: Pre-existing upload session URL if resuming.
            transport: Optional aiohttp.ClientSession.
        """
        self._config = config or ResumableUploadConfig()
        self._transport = transport
        self._response: Optional[Any] = None
        self._state = upload_state.ProtocolState(
            upload_url=upload_url,
            chunk_size=self._config.chunk_size,
            resumable_url=resumable_url,
        )

        # In-memory zero-copy buffer
        self._buffered_chunk: Optional[memoryview] = None
        self._buffered_chunk_offset: int = 0
        self._start_stream_offset: int = 0

        # Stall control tracking via monotonic clock
        self._aggregate_lag: float = 0.0
        self._stall_timeout_started: Optional[float] = None

    @property
    def upload_url(self) -> Optional[str]:
        """Optional[str]: The unique upload URL for this session."""
        return self._state.resumable_url

    @property
    def chunk_size(self) -> int:
        """int: The negotiated chunk size."""
        return self._state.chunk_size

    @property
    def response(self) -> Optional[Any]:
        """Optional[Any]: The cached response message if finished."""
        return self._response

    @property
    def bytes_uploaded(self) -> int:
        """int: Confirmed number of bytes committed so far."""
        return self._state.bytes_uploaded

    @property
    def finished(self) -> bool:
        """bool: Whether the upload has completed successfully."""
        return self._state.finished

    def _ensure_aiohttp(self) -> None:
        """Validates that aiohttp is installed and accessible.

        Raises:
            ImportError: If aiohttp is not installed.
        """
        if aiohttp is None:
            raise ImportError(
                "The aiohttp library is required to use AsyncResumableUploadSession. "
                "Please install google-api-core[async_rest]."
            )

    def _notify_progress(
        self, state: common.ProgressState, queue: Optional[asyncio.Queue] = None
    ) -> None:
        """Notifies registered progress callback and queue with current upload status.

        Args:
            state: ProgressState transition milestone.
            queue: Optional queue to receive progress event.
        """
        if self.upload_url:
            progress = common.UploadProgress(
                upload_url=self.upload_url,
                chunk_size=self.chunk_size,
                bytes_uploaded=self._state.bytes_uploaded,
                total_bytes=self._state.total_bytes,
                state=state,
            )
            if self._config.on_progress:
                try:
                    self._config.on_progress(progress)
                except Exception:  # pragma: NO COVER
                    pass
            if queue is not None:
                queue.put_nowait(progress)

    def _get_deadline_remaining(self) -> Optional[float]:
        """Calculates remaining seconds until the configured upload deadline.

        Returns:
            Remaining seconds before deadline, or None if no deadline configured.

        Raises:
            exceptions.DeadlineExceeded: If deadline has already elapsed.
        """
        if self._config.deadline:
            now = datetime.datetime.now(datetime.timezone.utc)
            dl = self._config.deadline
            if dl.tzinfo is None:
                dl = dl.replace(tzinfo=datetime.timezone.utc)
            remaining = (dl - now).total_seconds()
            if remaining <= 0:
                raise exceptions.DeadlineExceeded(
                    f"Resumable upload deadline {self._config.deadline} exceeded."
                )
            return remaining
        return None

    def _get_start_timeout(self) -> float:
        """Computes timeout in seconds for start and control requests.

        Returns:
            Applicable timeout in seconds.
        """
        remaining = self._get_deadline_remaining()
        timeout = (
            self._config.start_timeout or self._config.timeout or _DEFAULT_START_TIMEOUT
        )
        if remaining is not None:
            return min(timeout, remaining)
        return timeout

    async def _async_retry(
        self, coro_fn: Callable[[], Awaitable[Any]], max_attempts: int = 4
    ) -> Any:
        """Executes an asynchronous callable with exponential backoff retry logic.

        Args:
            coro_fn: Asynchronous nullary function to invoke and retry.
            max_attempts: Maximum retry attempts before propagating failure.

        Returns:
            The successful return value of coro_fn.
        """
        delay = 1.0
        multiplier = 2.0
        max_delay = 60.0
        for attempt in range(max_attempts):
            try:
                return await coro_fn()
            except (
                exceptions.DeadlineExceeded,
                exceptions.TransferStalledError,
                exceptions.UploadCancelledError,
            ):
                raise
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
        progress_queue: Optional[asyncio.Queue] = None,
    ) -> str:
        """Initiates the upload session by sending the start command asynchronously.

        Args:
            transport: The aiohttp client session.
            request_body: Initial metadata payload sent with start command.
            size: Total stream size in bytes, if known.
            progress_queue: Optional queue to receive progress event.

        Returns:
            The upload session URL.

        Raises:
            GoogleAPICallError: If the server rejects the start request.
            MissingStatusHeaderError: If the server response lacks status header.
        """
        self._ensure_aiohttp()
        method, url, headers, payload = self._state.build_start_request(
            body=request_body,
            headers=self._config.start_headers,
            content_type=self._config.content_type,
            size=size,
        )

        async def do_initiate():
            timeout_sec = self._get_start_timeout()
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
                session_url = self._state.process_start_response(
                    resp.status, resp_headers
                )
                return session_url

        session_url = await self._async_retry(do_initiate)
        self._notify_progress(common.ProgressState.STARTED, progress_queue)
        return session_url

    async def _transmit_chunk(
        self,
        transport: Any,
        reader_fn: Callable[[int], Awaitable[bytes]],
        size: Optional[int],
        progress_queue: Optional[asyncio.Queue] = None,
        stream_obj: Any = None,
    ) -> Tuple[int, Mapping[str, str], bytes]:
        """Transmits the next data chunk asynchronously with stall control.

        Args:
            transport: The aiohttp client session.
            reader_fn: Async callable returning chunk bytes.
            size: Total stream size in bytes, if known.
            progress_queue: Optional queue to receive progress updates.
            stream_obj: Underlying stream object for recovery seeking.

        Returns:
            Tuple of (status code, headers mapping, response body bytes).

        Raises:
            TransferStalledError: If chunk transfer throughput stalls.
            DeadlineExceeded: If upload deadline is reached.
            GoogleAPICallError: If chunk upload encounters an unrecoverable error.
        """
        async def do_transmit():
            chunk_size = self._state.chunk_size

            # Retain active chunk in zero-copy buffer if not present
            if self._buffered_chunk is None:
                raw_bytes = await reader_fn(chunk_size)
                if not raw_bytes:
                    raw_bytes = b""
                self._buffered_chunk = memoryview(raw_bytes)
                self._buffered_chunk_offset = self._state.bytes_uploaded

            data = self._buffered_chunk
            data_len = len(data)

            is_last = data_len < chunk_size
            if size is not None and self._state.bytes_uploaded + data_len >= size:
                is_last = True

            method, url, headers, payload = self._state.build_chunk_request(
                data=data,
                is_last_chunk=is_last,
                content_type=self._config.content_type,
            )

            async def do_http():
                rate = self._config.stall_minimum_rate
                expected_sec = data_len / rate if rate > 0 else 60.0
                next_chunk_timeout = max(
                    1.0,
                    expected_sec - self._aggregate_lag + self._config.stall_timeout,
                )
                per_attempt_timeout = max(
                    5.0, min(next_chunk_timeout, 2.0 * expected_sec)
                )

                if self._config.timeout:
                    per_attempt_timeout = min(self._config.timeout, per_attempt_timeout)

                remaining = self._get_deadline_remaining()
                if remaining is not None:
                    per_attempt_timeout = min(per_attempt_timeout, remaining)

                client_timeout = aiohttp.ClientTimeout(total=per_attempt_timeout)
                async with transport.request(
                    method, url, data=payload, headers=headers, timeout=client_timeout
                ) as resp:
                    resp_headers = dict(resp.headers)
                    resp_body = await resp.read()
                    if resp.status not in (200, 201):
                        raise exceptions.from_http_status(
                            resp.status, resp_body.decode("utf-8", errors="replace")
                        )
                    return resp.status, resp_headers, resp_body

            try:
                t_start = _monotonic_clock()
                status_code, resp_headers, resp_body = await self._async_retry(do_http)
                t_elapsed = _monotonic_clock() - t_start

                # Evaluate stall control lag & timer
                if self._config.stall_minimum_rate and self._config.stall_timeout:
                    rate = self._config.stall_minimum_rate
                    expected_sec = data_len / rate if rate > 0 else 0.0
                    current_lag = t_elapsed - expected_sec
                    self._aggregate_lag = max(0.0, self._aggregate_lag + current_lag)
                    if self._aggregate_lag > 0.0:
                        if self._stall_timeout_started is None:
                            self._stall_timeout_started = t_start
                        if (
                            _monotonic_clock() - self._stall_timeout_started
                            >= self._config.stall_timeout
                        ):
                            remaining = self._get_deadline_remaining()
                            if remaining is not None and remaining <= 0:
                                raise exceptions.DeadlineExceeded(
                                    f"Resumable upload deadline {self._config.deadline} exceeded."
                                )
                            raise exceptions.TransferStalledError(
                                f"Upload stalled: transfer rate remained below {rate} bytes/s for longer than {self._config.stall_timeout}s."
                            )
                    else:
                        self._stall_timeout_started = None

                self._state.process_chunk_response(status_code, resp_headers, data_len)
                self._buffered_chunk = None
                self._notify_progress(
                    common.ProgressState.FINALIZED
                    if self._state.finished
                    else common.ProgressState.UPLOADING,
                    progress_queue,
                )
                return status_code, resp_headers, resp_body
            except Exception as exc:
                if hasattr(exc, "__dict__"):
                    exc.upload_url = self.upload_url
                    exc.chunk_size = self.chunk_size
                if isinstance(exc, (asyncio.TimeoutError, exceptions.DeadlineExceeded)):
                    remaining = self._get_deadline_remaining()
                    if remaining is not None and remaining <= 0:
                        raise exceptions.DeadlineExceeded(
                            f"Resumable upload deadline {self._config.deadline} exceeded."
                        ) from exc
                    stalled_err = exceptions.TransferStalledError(
                        f"Upload stalled: chunk transfer timed out ({exc})."
                    )
                    stalled_err.upload_url = self.upload_url
                    stalled_err.chunk_size = self.chunk_size
                    raise stalled_err from exc

                is_recoverable = (
                    isinstance(exc, exceptions.GoogleAPICallError)
                    and exc.code in common.RECOVERABLE_STATUS_CODES
                ) or isinstance(exc, exceptions.MissingStatusHeaderError)

                if is_recoverable:
                    _LOGGER.info(
                        "Recoverable error %s during async chunk upload. Querying server offset.",
                        exc,
                    )
                    self._notify_progress(
                        common.ProgressState.RECOVERING, progress_queue
                    )
                    await self._recover(transport, stream_obj)
                    raise _AsyncRecoveryRetransmit()
                raise

        while True:
            try:
                return await do_transmit()
            except _AsyncRecoveryRetransmit:
                continue

    async def _recover(self, transport: Any, stream_obj: Any = None) -> int:
        """Queries server for committed byte offset and adjusts buffer.

        Args:
            transport: The aiohttp client session.
            stream_obj: Underlying stream object to rewind if seekable.

        Returns:
            The confirmed server byte offset.

        Raises:
            exceptions.UnseekableStreamError: If server offset precedes buffer and stream cannot be rewound.
            exceptions.GoogleAPICallError: If query request fails on the server.
        """
        method, url, headers, payload = self._state.build_query_request()

        async def do_query():
            timeout_sec = self._get_start_timeout()
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
                return resp.status, resp_headers

        status_code, resp_headers = await self._async_retry(do_query)
        received = self._state.process_query_response(status_code, resp_headers)

        if self._buffered_chunk is not None:
            chunk_start = self._buffered_chunk_offset
            chunk_end = chunk_start + len(self._buffered_chunk)
            if chunk_start <= received <= chunk_end:
                discard_len = received - chunk_start
                self._buffered_chunk = self._buffered_chunk[discard_len:]
                self._buffered_chunk_offset = received
                return received

        self._buffered_chunk = None
        if stream_obj is not None and hasattr(stream_obj, "seek"):
            if hasattr(stream_obj, "seekable") and not stream_obj.seekable():
                err = exceptions.UnseekableStreamError(
                    f"Stream is not seekable. Cannot recover upload to offset {received}."
                )
                err.upload_url = self.upload_url
                err.chunk_size = self.chunk_size
                raise err
            try:
                stream_obj.seek(self._start_stream_offset + received)
                return received
            except (OSError, AttributeError) as exc:
                err = exceptions.UnseekableStreamError(
                    f"Failed to seek stream to offset {received}: {exc}"
                )
                err.upload_url = self.upload_url
                err.chunk_size = self.chunk_size
                raise err from exc

        err = exceptions.UnseekableStreamError(
            f"Server offset {received} precedes active buffer. Stream cannot be rewound."
        )
        err.upload_url = self.upload_url
        err.chunk_size = self.chunk_size
        raise err

    async def cancel(self, transport: Optional[Any] = None) -> None:
        """Cancels the resumable upload session asynchronously.

        Args:
            transport: Optional aiohttp client session.

        Raises:
            ValueError: If transport is missing.
            exceptions.GoogleAPICallError: If cancellation request fails on the server.
        """
        self._ensure_aiohttp()
        sess = transport or self._transport
        if sess is None:
            raise ValueError("An aiohttp.ClientSession transport must be provided.")
        method, url, headers, payload = self._state.build_cancel_request()
        timeout_sec = self._get_start_timeout()
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

    def upload(
        self,
        stream: Union[AsyncIterable[bytes], BinaryIO, bytes, Iterable[bytes]],
        request_body: Union[str, bytes] = "",
        size: Optional[int] = None,
        transport: Optional[Any] = None,
    ) -> AsyncUploadOperation:
        """Initiates and executes upload asynchronously, returning an AsyncUploadOperation.

        Args:
            stream: Data payload to upload (async iterable, binary stream, bytes, or iterable).
            request_body: Initial metadata payload sent with the start request.
            size: Total stream size in bytes, if known.
            transport: Optional aiohttp client session.

        Returns:
            An AsyncUploadOperation handle representing the active transfer.

        Raises:
            ValueError: If transport is missing.
        """
        self._ensure_aiohttp()
        sess = transport or self._transport
        if sess is None:
            raise ValueError("An aiohttp.ClientSession transport must be provided.")

        progress_queue: asyncio.Queue = asyncio.Queue()

        async def _run():
            try:
                reader_fn, computed_size, stream_obj = self._prepare_async_reader(
                    stream, size
                )
                await self.initiate(
                    transport=sess,
                    request_body=request_body,
                    size=computed_size,
                    progress_queue=progress_queue,
                )

                final_resp_tuple = None
                while not self._state.finished and not self._state.invalid:
                    final_resp_tuple = await self._transmit_chunk(
                        sess, reader_fn, computed_size, progress_queue, stream_obj
                    )

                if final_resp_tuple is None:
                    raise ValueError(
                        "Upload completed without receiving a final response."
                    )

                _, _, body_bytes = final_resp_tuple
                self._response = self._format_response(body_bytes)
                progress_queue.put_nowait(_DONE_SENTINEL)
                return self._response
            except Exception as exc:
                if hasattr(exc, "__dict__"):
                    exc.upload_url = self.upload_url
                    exc.chunk_size = self.chunk_size
                progress_queue.put_nowait(exc)
                raise

        task = asyncio.create_task(_run())
        return AsyncUploadOperation(
            task=task, session=self, progress_queue=progress_queue
        )

    def resume(
        self,
        upload_url: str,
        stream: Union[AsyncIterable[bytes], BinaryIO, bytes, Iterable[bytes]],
        size: Optional[int] = None,
        chunk_size: Optional[int] = None,
        transport: Optional[Any] = None,
    ) -> AsyncUploadOperation:
        """Resumes an existing upload asynchronously, returning an AsyncUploadOperation.

        Args:
            upload_url: Established upload session URL.
            stream: Data payload to resume uploading.
            size: Total stream size in bytes, if known.
            chunk_size: Optional chunk size override in bytes.
            transport: Optional aiohttp client session.

        Returns:
            An AsyncUploadOperation handle representing the resumed transfer.

        Raises:
            ValueError: If transport is missing.
        """
        self._ensure_aiohttp()
        sess = transport or self._transport
        if sess is None:
            raise ValueError("An aiohttp.ClientSession transport must be provided.")

        if chunk_size is not None:
            self._state._chunk_size = chunk_size

        self._state._resumable_url = upload_url
        progress_queue: asyncio.Queue = asyncio.Queue()

        async def _run():
            try:
                reader_fn, computed_size, stream_obj = self._prepare_async_reader(
                    stream, size
                )
                await self._recover(sess, stream_obj)
                self._notify_progress(
                    common.ProgressState.OFFSET_RECEIVED, progress_queue
                )

                final_resp_tuple = None
                while not self._state.finished and not self._state.invalid:
                    final_resp_tuple = await self._transmit_chunk(
                        sess, reader_fn, computed_size, progress_queue, stream_obj
                    )

                if final_resp_tuple is None:
                    raise ValueError(
                        "Upload resumed but completed without receiving a final response."
                    )

                _, _, body_bytes = final_resp_tuple
                self._response = self._format_response(body_bytes)
                progress_queue.put_nowait(_DONE_SENTINEL)
                return self._response
            except Exception as exc:
                if hasattr(exc, "__dict__"):
                    exc.upload_url = self.upload_url
                    exc.chunk_size = self.chunk_size
                progress_queue.put_nowait(exc)
                raise

        task = asyncio.create_task(_run())
        return AsyncUploadOperation(
            task=task, session=self, progress_queue=progress_queue
        )

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
        stream_obj = None

        if isinstance(stream, bytes):
            stream_obj = io.BytesIO(stream)
            if computed_size is None:
                computed_size = len(stream)

            async def reader(n: int) -> bytes:
                return stream_obj.read(n)

            return reader, computed_size, stream_obj

        if hasattr(stream, "read") and inspect.iscoroutinefunction(stream.read):
            # Native async reader (e.g. asyncio.StreamReader)
            async def reader(n: int) -> bytes:
                return await stream.read(n)  # type: ignore

            return reader, computed_size, stream

        if hasattr(stream, "read"):
            # Synchronous binary stream: offload blocking reads to worker thread
            stream_obj = stream
            if computed_size is None and hasattr(stream, "getbuffer"):
                computed_size = stream.getbuffer().nbytes

            if hasattr(stream_obj, "tell"):
                try:
                    self._start_stream_offset = stream_obj.tell()
                except (OSError, AttributeError):
                    self._start_stream_offset = 0

            async def reader(n: int) -> bytes:
                return await asyncio.to_thread(stream.read, n)  # type: ignore

            return reader, computed_size, stream_obj

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

    def _format_response(self, response_bytes: bytes) -> Any:
        """Formats response bytes into protobuf message type if provided.

        Args:
            response_bytes: Raw HTTP response body bytes from final chunk.

        Returns:
            Deserialized protobuf message or the raw bytes response.
        """
        return _format_response_payload(response_bytes, self._config.response_type)
