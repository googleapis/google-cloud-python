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

"""Synchronous Resumable Upload session and helpers using requests."""

import contextlib
import dataclasses
import datetime
import io
import logging
import time
from typing import (
    Any,
    BinaryIO,
    Callable,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import requests

from google.api_core import exceptions
from google.api_core.retry import Retry, StreamingRetry
from google.api_core.resumable_transfer import common, upload_state

_LOGGER = logging.getLogger(__name__)
_DEFAULT_START_TIMEOUT = 60.0  # seconds for initial start request
_monotonic_clock = time.monotonic


class _IterableStream(io.RawIOBase):
    """Memory-efficient stream wrapper around an Iterable[bytes]."""

    def __init__(self, iterable: Iterable[bytes]) -> None:
        self._iterator = iter(iterable)
        self._buffer = bytearray()

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return False

    def readinto(self, b: bytearray) -> int:
        req_len = len(b)
        while len(self._buffer) < req_len:
            try:
                chunk = next(self._iterator)
                if chunk:
                    self._buffer.extend(chunk)
            except StopIteration:
                break
        n = min(req_len, len(self._buffer))
        b[:n] = self._buffer[:n]
        del self._buffer[:n]
        return n

    def read(self, size: int = -1) -> bytes:
        if size == -1:
            chunks = list(self._iterator)
            data = bytes(self._buffer) + b"".join(chunks)
            self._buffer.clear()
            return data
        while len(self._buffer) < size:
            try:
                chunk = next(self._iterator)
                if chunk:
                    self._buffer.extend(chunk)
            except StopIteration:
                break
        n = min(size, len(self._buffer))
        res = bytes(self._buffer[:n])
        del self._buffer[:n]
        return res


ResumableUploadConfig = common.ResumableUploadConfig


class ResumableUploadSession(common.BaseResumableUploadSession):
    """Manages the full lifecycle of a synchronous resumable upload session."""

    def __init__(
        self,
        upload_url: Optional[str] = None,
        config: Optional[ResumableUploadConfig] = None,
        resumable_url: Optional[str] = None,
        transport: Optional[requests.Session] = None,
        chunk_size: Optional[int] = None,
        stall_minimum_rate: Optional[int] = None,
        stall_timeout: Optional[float] = None,
    ) -> None:
        """Initializes a ResumableUploadSession.

        Args:
            upload_url: The initial URL for the start request.
            config: Optional upload configuration parameters.
            resumable_url: Pre-existing upload session URL if resuming.
            transport: Optional requests session.
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

    def _get_transport(self, transport: Optional[requests.Session]) -> requests.Session:
        """Resolves the requests.Session transport.

        Args:
            transport: Explicit requests session if provided.

        Returns:
            The resolved requests session.

        Raises:
            ValueError: If no requests session is available.
        """
        sess = transport or self._transport
        if sess is None:
            raise ValueError("A requests.Session transport must be provided.")
        return sess

    def _get_retry(
        self,
        retry: Optional[Any] = None,
        is_start: bool = False,
    ) -> Retry:
        """Resolves retry policy for unary control requests.

        Args:
            retry: Explicit retry policy if provided.
            is_start: Whether this retry policy is for the start request.

        Returns:
            Configured or default Retry instance.
        """
        if is_start and self._config.start_retry:
            return self._config.start_retry
        actual_retry = retry if retry is not None else self._config.retry
        if isinstance(actual_retry, Retry):
            return actual_retry
        return Retry(predicate=self._get_retry_predicate())

    def _get_streaming_retry(
        self,
        retry: Optional[Any] = None,
        on_error: Optional[Callable[[Exception], Any]] = None,
    ) -> StreamingRetry:
        """Resolves retry policy for streaming chunk uploads.

        Args:
            retry: Explicit retry policy override if provided.
            on_error: Optional callback executed when an exception triggers a retry attempt.

        Returns:
            Configured or default StreamingRetry instance.
        """
        actual_retry = retry if retry is not None else self._config.retry
        if isinstance(actual_retry, StreamingRetry):
            return actual_retry

        callbacks = [
            cb
            for cb in (getattr(actual_retry, "_on_error", None), on_error)
            if cb is not None
        ]

        def combined_on_error(exc: Exception) -> Any:
            for cb in callbacks:
                cb(exc)

        return StreamingRetry(
            predicate=self._get_streaming_predicate(),
            initial=getattr(actual_retry, "_initial", 1.0),
            maximum=getattr(actual_retry, "_maximum", 60.0),
            multiplier=getattr(actual_retry, "_multiplier", 2.0),
            timeout=getattr(actual_retry, "_timeout", None),
            on_error=combined_on_error if callbacks else None,
        )

    def initiate(
        self,
        transport: Optional[requests.Session] = None,
        request_body: Union[str, bytes] = "",
        size: Optional[int] = None,
        headers: Optional[Union[Mapping[str, str], Sequence[Tuple[str, str]]]] = None,
        content_type: Optional[str] = None,
        retry: Optional[Retry] = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
    ) -> str:
        """Initiates the upload session by sending the start command.

        Args:
            transport: The requests session.
            request_body: JSON payload for initial start request.
            size: Total size of payload in bytes, if known.
            headers: Additional HTTP headers dispatched with start request.
            content_type: MIME type of the stream payload.
            retry: Optional custom retry policy for start request.
            timeout: Optional timeout in seconds for start request.
            deadline: Optional overall upload deadline.
            on_progress: Optional callback for progress updates.

        Returns:
            The upload session URL.
        """
        sess = self._get_transport(transport)
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

        def do_initiate() -> str:
            to = self._get_start_timeout(timeout=timeout, deadline=deadline)
            response = sess.request(
                method, url, data=payload, headers=start_headers, timeout=to
            )
            if not response.ok:
                raise exceptions.from_http_response(response)
            session_url = self._state.process_start_response(
                response.status_code, response.headers
            )
            return session_url

        actual_retry = self._get_retry(retry=retry, is_start=True)
        session_url = actual_retry(do_initiate)()
        self._notify_progress(common.ProgressState.STARTED, on_progress=on_progress)
        return session_url

    def _transmit_chunk(
        self,
        transport: requests.Session,
        stream: BinaryIO,
        size: Optional[int],
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
    ) -> requests.Response:
        """Transmits a single data chunk via HTTP with stall control.

        Args:
            transport: The requests session.
            stream: The input data stream.
            size: Total size of the stream in bytes, if known.
            timeout: Optional timeout ceiling in seconds.
            deadline: Optional overall deadline.
            on_progress: Optional callback for progress updates.

        Returns:
            The HTTP response for the transmitted chunk.

        Raises:
            exceptions.TransferStalledError: If chunk transmission times out.
            exceptions.DeadlineExceeded: If deadline is exceeded.
            exceptions.GoogleAPICallError: If server responds with HTTP error.
        """
        chunk_size = self._state.chunk_size

        if self._buffered_chunk is None:
            raw_bytes = stream.read(chunk_size)
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
        try:
            t_start = _monotonic_clock()
            resp = transport.request(
                method,
                url,
                data=payload,
                headers=headers,
                timeout=per_attempt_timeout,
            )
            t_elapsed = _monotonic_clock() - t_start
        except requests.exceptions.Timeout as exc:
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

        if not resp.ok:
            exc = exceptions.from_http_response(resp)
            self._enrich_exception(exc)
            raise exc

        self._update_stall_control(data_len, t_start, t_elapsed, deadline=deadline)
        self._state.process_chunk_response(
            resp.status_code, resp.headers, data_len
        )
        self._buffered_chunk = None
        self._notify_progress(
            common.ProgressState.FINALIZED
            if self._state.finished
            else common.ProgressState.UPLOADING,
            on_progress=on_progress,
        )
        return resp

    def _recover(
        self,
        transport: requests.Session,
        stream: BinaryIO,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
    ) -> int:
        """Queries server for committed byte offset and adjusts buffer / stream.

        Args:
            transport: The requests session.
            stream: The input data stream.
            timeout: Optional timeout in seconds.
            deadline: Optional overall upload deadline.
            on_progress: Optional callback for progress updates.

        Returns:
            The confirmed server byte offset.

        Raises:
            exceptions.UnseekableStreamError: If server offset precedes buffer and stream cannot be rewound.
            exceptions.GoogleAPICallError: If query request fails on the server.
        """
        method, url, headers, payload = self._state.build_query_request()
        to = self._get_start_timeout(timeout=timeout, deadline=deadline)
        resp = transport.request(
            method, url, data=payload, headers=headers, timeout=to
        )
        if not resp.ok:
            raise exceptions.from_http_response(resp)

        received = self._state.process_query_response(resp.status_code, resp.headers)
        if self._state.finished:
            self._response = self._format_response(resp)
            return received
        self._notify_progress(common.ProgressState.OFFSET_RECEIVED, on_progress=on_progress)
        return self._reposition_stream_offset(stream, received)

    def cancel(
        self,
        transport: Optional[requests.Session] = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
    ) -> None:
        """Cancels the resumable upload session.

        Args:
            transport: Optional requests session to use for dispatching cancellation.
            timeout: Optional timeout in seconds.
            deadline: Optional overall upload deadline.

        Raises:
            ValueError: If no requests session is available.
            GoogleAPICallError: If the cancellation request fails on the server.
        """
        sess = self._get_transport(transport)
        method, url, headers, payload = self._state.build_cancel_request()
        to = self._get_start_timeout(timeout=timeout, deadline=deadline)
        resp = sess.request(method, url, data=payload, headers=headers, timeout=to)
        if not resp.ok:
            raise exceptions.from_http_response(resp)
        self._state.process_cancel_response(resp.status_code, resp.headers)

    def _chunk_stream_generator(
        self,
        transport: requests.Session,
        stream_obj: BinaryIO,
        computed_size: Optional[int],
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
        response_type: Optional[Any] = None,
    ) -> Generator[requests.Response, None, None]:
        """Generates chunk transmission responses with recovery support for StreamingRetry.

        Args:
            transport: The requests session.
            stream_obj: Binary stream yielding upload chunks.
            computed_size: Total payload size in bytes if known.
            timeout: Optional per-chunk timeout in seconds.
            deadline: Optional overall upload deadline.
            on_progress: Optional callback receiving progress updates.
            response_type: Optional response deserialization type.

        Yields:
            HTTP responses from chunk upload requests.
        """
        if self._needs_recovery:
            if self._recovered_from_error:
                self._notify_progress(common.ProgressState.RECOVERING, on_progress=on_progress)
            self._recover(
                transport,
                stream_obj,
                timeout=timeout,
                deadline=deadline,
                on_progress=on_progress,
            )
            self._needs_recovery = False
            self._recovered_from_error = False

        while not self._state.finished and not self._state.invalid:
            resp = self._transmit_chunk(
                transport,
                stream_obj,
                computed_size,
                timeout=timeout,
                deadline=deadline,
                on_progress=on_progress,
            )
            if self._state.finished:
                self._response = self._format_response(resp, response_type=response_type)
            yield resp

    def upload(
        self,
        stream: Union[BinaryIO, bytes, Iterable[bytes]],
        request_body: Union[str, bytes] = "",
        size: Optional[int] = None,
        headers: Optional[Union[Mapping[str, str], Sequence[Tuple[str, str]]]] = None,
        content_type: Optional[str] = None,
        start_retry: Optional[Retry] = None,
        start_timeout: Optional[float] = None,
        retry: Optional[Union[Retry, StreamingRetry]] = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
        response_type: Optional[Any] = None,
        transport: Optional[requests.Session] = None,
    ) -> Any:
        """Executes the resumable upload from start to completion.

        Args:
            stream: Data payload to upload (file-like stream, bytes, or iterable of bytes).
            request_body: Initial metadata payload sent with the start request.
            size: Total stream size in bytes, if known.
            headers: Additional HTTP headers dispatched with start request.
            content_type: MIME type of the stream payload.
            start_retry: Custom retry policy for start request.
            start_timeout: Per-request timeout in seconds for start request.
            retry: Retry policy for chunk uploads and unary queries.
            timeout: Per-request timeout in seconds for chunk uploads.
            deadline: Overall global deadline for the upload process.
            on_progress: Callback function receiving UploadProgress notifications.
            response_type: Optional response deserialization type or callable.
            transport: Optional requests session.

        Returns:
            The final server response payload or deserialized response message.

        Raises:
            ValueError: If transport is missing or upload completes without a response.
            GoogleAPICallError: If an unrecoverable API error occurs.
        """
        sess = self._get_transport(transport)
        try:
            stream_obj, computed_size = self._prepare_stream(stream, size)
            self.initiate(
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

            retry_policy = self._get_streaming_retry(
                retry=retry, on_error=self._on_stream_error
            )
            retryable_stream = retry_policy(self._chunk_stream_generator)(
                sess,
                stream_obj,
                computed_size,
                timeout=timeout,
                deadline=deadline,
                on_progress=on_progress,
                response_type=response_type,
            )
            for _ in retryable_stream:
                pass

            return self._finish_response()
        except Exception as exc:
            self._enrich_exception(exc)
            raise

    def resume(
        self,
        upload_url: Optional[str] = None,
        stream: Optional[Union[BinaryIO, bytes, Iterable[bytes]]] = None,
        size: Optional[int] = None,
        chunk_size: Optional[int] = None,
        retry: Optional[Union[Retry, StreamingRetry]] = None,
        timeout: Optional[float] = None,
        deadline: Optional[datetime.datetime] = None,
        on_progress: Optional[Callable[[common.UploadProgress], None]] = None,
        response_type: Optional[Any] = None,
        transport: Optional[requests.Session] = None,
    ) -> Any:
        """Resumes an existing upload from a saved upload URL.

        Args:
            upload_url: The pre-existing upload session URL.
            stream: The data payload to resume uploading from.
            size: Total size of the payload in bytes, if known.
            chunk_size: Optional chunk size override in bytes.
            retry: Retry policy for chunk uploads and recovery queries.
            timeout: Per-request timeout in seconds.
            deadline: Overall global deadline for the upload process.
            on_progress: Callback function receiving UploadProgress notifications.
            response_type: Optional response deserialization type or callable.
            transport: Optional requests session.

        Returns:
            The final server response payload or deserialized response message.

        Raises:
            ValueError: If required arguments are missing or response not received.
            GoogleAPICallError: If an unrecoverable API error occurs.
        """
        sess = self._get_transport(transport)
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
        try:
            stream_obj, computed_size = self._prepare_stream(stream, size)

            retry_policy = self._get_streaming_retry(
                retry=retry, on_error=self._on_stream_error
            )
            retryable_stream = retry_policy(self._chunk_stream_generator)(
                sess,
                stream_obj,
                computed_size,
                timeout=timeout,
                deadline=deadline,
                on_progress=on_progress,
                response_type=response_type,
            )
            for _ in retryable_stream:
                pass

            return self._finish_response()
        except Exception as exc:
            self._enrich_exception(exc)
            raise

    def _prepare_stream(
        self, stream: Union[BinaryIO, bytes, Iterable[bytes]], size: Optional[int]
    ) -> Tuple[BinaryIO, Optional[int]]:
        """Normalizes stream input into a BinaryIO object and determines stream length.

        Args:
            stream: Input stream, bytes, or iterable of bytes.
            size: Explicit total size in bytes, if known.

        Returns:
            Tuple of (prepared BinaryIO stream, computed total size).
        """
        computed_size = size
        if isinstance(stream, (str, dict)):
            raise TypeError(f"Unsupported stream type: {type(stream)}")
        if isinstance(stream, bytes):
            stream_obj: BinaryIO = io.BytesIO(stream)
            if computed_size is None:
                computed_size = len(stream)
        elif isinstance(stream, (list, tuple)):
            stream_obj = io.BytesIO(b"".join(stream))
            if computed_size is None:
                computed_size = stream_obj.getbuffer().nbytes
        elif not hasattr(stream, "read") and isinstance(stream, Iterable):
            stream_obj = cast(BinaryIO, _IterableStream(stream))
        elif hasattr(stream, "read"):
            stream_obj = cast(BinaryIO, stream)
            if computed_size is None:
                if hasattr(stream_obj, "getbuffer"):
                    computed_size = stream_obj.getbuffer().nbytes
                elif (
                    hasattr(stream_obj, "seekable")
                    and stream_obj.seekable()
                    and hasattr(stream_obj, "tell")
                ):
                    cur = stream_obj.tell()
                    stream_obj.seek(0, io.SEEK_END)
                    computed_size = stream_obj.tell() - cur
                    stream_obj.seek(cur)
        else:
            raise TypeError(f"Unsupported stream type: {type(stream)}")

        if hasattr(stream_obj, "tell"):
            try:
                self._start_stream_offset = stream_obj.tell()
            except (OSError, AttributeError):
                self._start_stream_offset = 0

        return stream_obj, computed_size


_format_response_payload = common.format_response_payload
