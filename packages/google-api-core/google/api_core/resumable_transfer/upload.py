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
)

import google.protobuf.message
import proto
import requests
from google.protobuf import json_format

import google.api_core.retry
from google.api_core import exceptions
from google.api_core.resumable_transfer import common, upload_state

_LOGGER = logging.getLogger(__name__)
_DEFAULT_START_TIMEOUT = 60.0  # seconds for initial start request
_monotonic_clock = time.monotonic


class _RecoveryRetransmit(Exception):
    """Internal exception indicating state synchronization succeeded and chunk should retransmit."""

    pass


@dataclasses.dataclass
class ResumableUploadConfig:
    """Configuration options for a resumable upload.

    Attributes:
        chunk_size: Size in bytes for each uploaded data chunk. Defaults to 10 MiB.
        start_timeout: Local per-request timeout in seconds for start request.
        start_retry: Custom retry policy for the start request.
        stall_minimum_rate: Minimum transfer rate in bytes per second. Defaults to 64 KiB/s.
        stall_timeout: Stall duration threshold in seconds. Defaults to 120s.
        additional_headers: Additional HTTP headers dispatched exclusively with start request.
        deadline: Overall global deadline for the upload process.
        timeout: Fallback per-request timeout.
        retry: Fallback retry policy.
        on_progress: Callback function receiving UploadProgress notifications.
        response_type: Optional message class (proto.Message or google.protobuf.message.Message),
            callable deserializer, or None to return raw response.
        content_type: MIME type of the stream payload.
    """

    chunk_size: int = common.DEFAULT_CHUNK_SIZE
    start_timeout: Optional[float] = None
    start_retry: Optional[google.api_core.retry.Retry] = None
    stall_minimum_rate: int = 64 * 1024
    stall_timeout: float = 120.0
    additional_headers: Optional[
        Union[Mapping[str, str], Sequence[Tuple[str, str]]]
    ] = None
    deadline: Optional[datetime.datetime] = None
    timeout: Optional[float] = None
    retry: Optional[google.api_core.retry.Retry] = None
    on_progress: Optional[Callable[[common.UploadProgress], None]] = None
    response_type: Optional[Any] = None
    content_type: Optional[str] = None

    def __post_init__(self) -> None:
        """Normalizes fallback timeouts and retry policies."""
        if self.start_timeout is not None and self.timeout is None:
            self.timeout = self.start_timeout
        elif self.timeout is not None and self.start_timeout is None:
            self.start_timeout = self.timeout

        if self.start_retry is not None and self.retry is None:
            self.retry = self.start_retry
        elif self.retry is not None and self.start_retry is None:
            self.start_retry = self.retry

    @property
    def start_headers(self) -> Optional[Sequence[Tuple[str, str]]]:
        """Returns normalized additional headers for the start request."""
        if self.additional_headers is None:
            return None
        if isinstance(self.additional_headers, Mapping):
            return list(self.additional_headers.items())
        return list(self.additional_headers)


class ResumableUploadSession:
    """Manages the full lifecycle of a resumable upload session."""

    def __init__(
        self,
        upload_url: Optional[str] = None,
        config: Optional[ResumableUploadConfig] = None,
        resumable_url: Optional[str] = None,
        transport: Optional[requests.Session] = None,
    ) -> None:
        """Initializes a ResumableUploadSession.

        Args:
            upload_url: The initial URL for the start request.
            config: Optional upload configuration parameters.
            resumable_url: Pre-existing upload session URL if resuming.
            transport: Optional requests session.
        """
        self._config = config or ResumableUploadConfig()
        self._transport = transport
        self._response: Optional[Any] = None
        self._state = upload_state.ProtocolState(
            upload_url=upload_url,
            chunk_size=self._config.chunk_size,
            resumable_url=resumable_url,
        )

        # In-memory zero-copy buffer (never discard chunk until confirmed)
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

    def _enrich_exception(self, exc: BaseException) -> None:
        """Attaches session diagnostic metadata to an active exception.

        Args:
            exc: Exception instance to augment with upload_url and chunk_size.
        """
        if hasattr(exc, "__dict__"):
            exc.upload_url = self.upload_url
            exc.chunk_size = self.chunk_size

    def _notify_progress(self, state: common.ProgressState) -> None:
        """Notifies registered progress callback with current upload status.

        Args:
            state: ProgressState transition milestone.
        """
        if self._config.on_progress and self.upload_url:
            self._config.on_progress(
                common.UploadProgress(
                    upload_url=self.upload_url,
                    chunk_size=self.chunk_size,
                    bytes_uploaded=self._state.bytes_uploaded,
                    total_bytes=self._state.total_bytes,
                    state=state,
                )
            )

    @contextlib.contextmanager
    def _capture_progress(
        self,
    ) -> Generator[List[common.UploadProgress], None, None]:
        """Intercepts progress events to buffer snapshots for generator consumers.

        Yields:
            List buffering UploadProgress snapshots during generator execution.
        """
        captured: List[common.UploadProgress] = []
        old_cb = self._config.on_progress

        def capture(p: common.UploadProgress) -> None:
            captured.append(p)
            if old_cb:
                old_cb(p)

        self._config.on_progress = capture
        try:
            yield captured
        finally:
            self._config.on_progress = old_cb

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

    def _get_retry_predicate(self) -> Callable[[Any], bool]:
        """Returns a predicate function for determining if an exception is retryable.

        Returns:
            A callable accepting an exception and returning a boolean.
        """

        def should_retry(exc: Any) -> bool:
            if isinstance(
                exc,
                (
                    exceptions.DeadlineExceeded,
                    exceptions.TransferStalledError,
                    exceptions.UploadCancelledError,
                ),
            ):
                return False
            if isinstance(exc, exceptions.MissingStatusHeaderError):
                return True
            if isinstance(exc, requests.exceptions.RequestException):
                if isinstance(
                    exc,
                    (
                        requests.exceptions.ConnectionError,
                        requests.exceptions.ChunkedEncodingError,
                    ),
                ):
                    return True
                if isinstance(exc, requests.exceptions.Timeout):
                    if self._config.stall_minimum_rate and self._config.stall_timeout:
                        return False
                    return True
            if isinstance(exc, exceptions.GoogleAPICallError):
                return exc.code in common.RETRYABLE_STATUS_CODES
            return False

        return should_retry

    def _get_retry(self, is_start: bool = False) -> google.api_core.retry.Retry:
        """Resolves retry policy for requests.

        Args:
            is_start: Whether this retry policy is for the start request.

        Returns:
            Configured or default Retry instance.
        """
        if is_start and self._config.start_retry:
            return self._config.start_retry
        if self._config.retry:
            return self._config.retry
        return google.api_core.retry.Retry(predicate=self._get_retry_predicate())

    def _compute_chunk_timeout(self, data_len: int) -> float:
        """Computes the dynamic per-attempt chunk timeout based on stall control and deadlines.

        Args:
            data_len: Length of the current chunk in bytes.

        Returns:
            Timeout in seconds for chunk transmission attempt.
        """
        rate = self._config.stall_minimum_rate
        expected_sec = data_len / rate if rate > 0 else 60.0
        next_chunk_timeout = max(
            1.0,
            expected_sec - self._aggregate_lag + self._config.stall_timeout,
        )
        per_attempt_timeout = max(5.0, min(next_chunk_timeout, 2.0 * expected_sec))

        if self._config.timeout:
            per_attempt_timeout = min(self._config.timeout, per_attempt_timeout)

        remaining = self._get_deadline_remaining()
        if remaining is not None:
            per_attempt_timeout = min(per_attempt_timeout, remaining)

        return per_attempt_timeout

    def _update_stall_control(
        self, data_len: int, t_start: float, t_elapsed: float
    ) -> None:
        """Updates aggregate transfer rate lag and enforces stall timeout and deadlines.

        Args:
            data_len: Length of the transmitted chunk in bytes.
            t_start: Monotonic timestamp before chunk transmission began.
            t_elapsed: Elapsed duration in seconds for chunk transmission.

        Raises:
            exceptions.DeadlineExceeded: If upload deadline is exceeded.
            exceptions.TransferStalledError: If transfer throughput stalls past configured timeout.
        """
        if not (self._config.stall_minimum_rate and self._config.stall_timeout):
            return

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
                    f"Upload stalled: transfer rate remained below {rate} bytes/s "
                    f"for longer than {self._config.stall_timeout}s."
                )
        else:
            self._stall_timeout_started = None

    def _reposition_stream_offset(self, stream: BinaryIO, received: int) -> int:
        """Adjusts in-memory chunk buffer or seeks input stream to server offset.

        Args:
            stream: The input data stream.
            received: Confirmed byte offset committed on the server.

        Returns:
            The confirmed server byte offset.

        Raises:
            exceptions.UnseekableStreamError: If server offset precedes buffer and stream cannot be rewound.
        """
        if self._buffered_chunk is not None:
            chunk_start = self._buffered_chunk_offset
            chunk_end = chunk_start + len(self._buffered_chunk)
            if chunk_start <= received <= chunk_end:
                discard_len = received - chunk_start
                self._buffered_chunk = self._buffered_chunk[discard_len:]
                self._buffered_chunk_offset = received
                return received

        self._buffered_chunk = None
        if hasattr(stream, "seekable") and not stream.seekable():
            err = exceptions.UnseekableStreamError(
                f"Stream is not seekable. Cannot recover upload to offset {received}."
            )
            self._enrich_exception(err)
            raise err
        try:
            stream.seek(self._start_stream_offset + received)
        except (OSError, AttributeError) as exc:
            err = exceptions.UnseekableStreamError(
                f"Failed to seek stream to offset {received}: {exc}"
            )
            self._enrich_exception(err)
            raise err from exc

        return received

    def initiate(
        self,
        transport: requests.Session,
        request_body: Union[str, bytes] = "",
        size: Optional[int] = None,
    ) -> str:
        """Initiates the upload session by sending the start command.

        Args:
            transport: The requests session.
            request_body: JSON payload for initial start request.
            size: Total size of payload in bytes, if known.

        Returns:
            The upload session URL.
        """
        method, url, headers, payload = self._state.build_start_request(
            body=request_body,
            headers=self._config.start_headers,
            content_type=self._config.content_type,
            size=size,
        )

        def do_initiate() -> str:
            timeout = self._get_start_timeout()
            response = transport.request(
                method, url, data=payload, headers=headers, timeout=timeout
            )
            if not response.ok:
                raise exceptions.from_http_response(response)
            session_url = self._state.process_start_response(
                response.status_code, response.headers
            )
            return session_url

        session_url = self._get_retry(is_start=True)(do_initiate)()
        self._notify_progress(common.ProgressState.STARTED)
        return session_url

    def _transmit_chunk(
        self, transport: requests.Session, stream: BinaryIO, size: Optional[int]
    ) -> requests.Response:
        """Transmits the next data chunk with stall control and error recovery.

        Args:
            transport: The requests session.
            stream: The input data stream.
            size: Total size of the stream in bytes, if known.

        Returns:
            The HTTP response for the transmitted chunk.
        """

        def do_transmit() -> requests.Response:
            chunk_size = self._state.chunk_size

            # Retain active chunk in zero-copy buffer if not present
            if self._buffered_chunk is None:
                raw_bytes = stream.read(chunk_size)
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

            def do_http() -> requests.Response:
                per_attempt_timeout = self._compute_chunk_timeout(data_len)
                resp = transport.request(
                    method,
                    url,
                    data=payload,
                    headers=headers,
                    timeout=per_attempt_timeout,
                )
                if not resp.ok:
                    raise exceptions.from_http_response(resp)
                return resp

            try:
                t_start = _monotonic_clock()
                resp = self._get_retry()(do_http)()
                t_elapsed = _monotonic_clock() - t_start

                self._update_stall_control(data_len, t_start, t_elapsed)
                self._state.process_chunk_response(
                    resp.status_code, resp.headers, data_len
                )
                self._buffered_chunk = None
                self._notify_progress(
                    common.ProgressState.FINALIZED
                    if self._state.finished
                    else common.ProgressState.UPLOADING
                )
                return resp
            except Exception as exc:
                self._enrich_exception(exc)
                if isinstance(
                    exc, (requests.exceptions.Timeout, exceptions.DeadlineExceeded)
                ):
                    remaining = self._get_deadline_remaining()
                    if remaining is not None and remaining <= 0:
                        raise exceptions.DeadlineExceeded(
                            f"Resumable upload deadline {self._config.deadline} exceeded."
                        ) from exc
                    stalled_err = exceptions.TransferStalledError(
                        f"Upload stalled: chunk transfer timed out ({exc})."
                    )
                    self._enrich_exception(stalled_err)
                    raise stalled_err from exc

                is_recoverable = (
                    isinstance(exc, exceptions.GoogleAPICallError)
                    and exc.code in common.RECOVERABLE_STATUS_CODES
                ) or isinstance(exc, exceptions.MissingStatusHeaderError)

                if is_recoverable:
                    _LOGGER.info(
                        "Recoverable error %s during chunk upload. Querying server offset.",
                        exc,
                    )
                    self._notify_progress(common.ProgressState.RECOVERING)
                    self._recover(transport, stream)
                    raise _RecoveryRetransmit()
                raise

        recovery_loop = google.api_core.retry.Retry(
            predicate=lambda e: isinstance(e, _RecoveryRetransmit)
        )
        return recovery_loop(do_transmit)()

    def _recover(self, transport: requests.Session, stream: BinaryIO) -> int:
        """Queries server for committed byte offset and adjusts buffer / stream.

        Args:
            transport: The requests session.
            stream: The input data stream.

        Returns:
            The confirmed server byte offset.

        Raises:
            exceptions.UnseekableStreamError: If server offset precedes buffer and stream cannot be rewound.
            exceptions.GoogleAPICallError: If query request fails on the server.
        """
        method, url, headers, payload = self._state.build_query_request()

        def do_query() -> requests.Response:
            timeout = self._get_start_timeout()
            resp = transport.request(
                method, url, data=payload, headers=headers, timeout=timeout
            )
            if not resp.ok:
                raise exceptions.from_http_response(resp)
            return resp

        resp = self._get_retry()(do_query)()
        received = self._state.process_query_response(resp.status_code, resp.headers)
        self._notify_progress(common.ProgressState.OFFSET_RECEIVED)
        return self._reposition_stream_offset(stream, received)

    def cancel(self, transport: Optional[requests.Session] = None) -> None:
        """Cancels the resumable upload session.

        Args:
            transport: Optional requests session to use for dispatching cancellation.

        Raises:
            ValueError: If no requests session is available.
            GoogleAPICallError: If the cancellation request fails on the server.
        """
        sess = self._get_transport(transport)
        method, url, headers, payload = self._state.build_cancel_request()
        timeout = self._get_start_timeout()
        resp = sess.request(method, url, data=payload, headers=headers, timeout=timeout)
        if not resp.ok:
            raise exceptions.from_http_response(resp)
        self._state.process_cancel_response(resp.status_code, resp.headers)

    def _transmit_all_chunks(
        self,
        transport: requests.Session,
        stream_obj: BinaryIO,
        computed_size: Optional[int],
        captured: Optional[List[common.UploadProgress]] = None,
    ) -> Generator[common.UploadProgress, None, None]:
        """Transmits chunks until transfer completes, yielding buffered progress updates.

        Args:
            transport: The requests session.
            stream_obj: Binary stream yielding upload chunks.
            computed_size: Total payload size in bytes if known.
            captured: Optional buffer accumulating progress snapshots.

        Yields:
            UploadProgress snapshots for each transmission milestone.

        Raises:
            ValueError: If upload concludes without a server response.
        """
        if captured:
            while captured:
                yield captured.pop(0)

        final_resp = None
        while not self._state.finished and not self._state.invalid:
            final_resp = self._transmit_chunk(transport, stream_obj, computed_size)
            if captured:
                while captured:
                    yield captured.pop(0)

        if final_resp is None:
            raise ValueError("Upload completed without receiving a final response.")

        self._response = self._format_response(final_resp)

    def upload(
        self,
        stream: Union[BinaryIO, bytes, Iterable[bytes]],
        request_body: Union[str, bytes] = "",
        size: Optional[int] = None,
        transport: Optional[requests.Session] = None,
    ) -> Any:
        """Executes the resumable upload from start to completion.

        Args:
            stream: Data payload to upload (file-like stream, bytes, or iterable of bytes).
            request_body: Initial metadata payload sent with the start request.
            size: Total stream size in bytes, if known.
            transport: Optional requests session.

        Returns:
            The final server response payload or deserialized response message.

        Raises:
            ValueError: If transport is missing or upload completes without a response.
            GoogleAPICallError: If an unrecoverable API error occurs.
        """
        for _ in self.iter_upload(
            stream=stream, request_body=request_body, size=size, transport=transport
        ):
            pass
        return self._response

    def iter_upload(
        self,
        stream: Union[BinaryIO, bytes, Iterable[bytes]],
        request_body: Union[str, bytes] = "",
        size: Optional[int] = None,
        transport: Optional[requests.Session] = None,
    ) -> Generator[common.UploadProgress, None, None]:
        """Streams upload execution, yielding UploadProgress snapshots (PEP 255).

        Args:
            stream: Data payload to upload (file-like stream, bytes, or iterable of bytes).
            request_body: Initial metadata payload sent with the start request.
            size: Total stream size in bytes, if known.
            transport: Optional requests session.

        Yields:
            UploadProgress snapshots for each chunk transmission milestone.

        Raises:
            ValueError: If transport is missing or upload completes without a response.
            GoogleAPICallError: If an unrecoverable API error occurs.
        """
        sess = self._get_transport(transport)
        with self._capture_progress() as captured:
            try:
                stream_obj, computed_size = self._prepare_stream(stream, size)
                self.initiate(
                    transport=sess, request_body=request_body, size=computed_size
                )
                yield from self._transmit_all_chunks(
                    sess, stream_obj, computed_size, captured
                )
            except Exception as exc:
                self._enrich_exception(exc)
                raise

    def resume(
        self,
        upload_url: Optional[str] = None,
        stream: Optional[Union[BinaryIO, bytes, Iterable[bytes]]] = None,
        size: Optional[int] = None,
        chunk_size: Optional[int] = None,
        transport: Optional[requests.Session] = None,
    ) -> Any:
        """Resumes an existing upload from a saved upload URL.

        Args:
            upload_url: The pre-existing upload session URL.
            stream: The data payload to resume uploading from.
            size: Total size of the payload in bytes, if known.
            chunk_size: Optional chunk size override in bytes.
            transport: Optional requests session.

        Returns:
            The final server response payload or deserialized response message.

        Raises:
            ValueError: If required arguments are missing or response not received.
            GoogleAPICallError: If an unrecoverable API error occurs.
        """
        for _ in self.iter_resume(
            upload_url=upload_url,
            stream=stream,
            size=size,
            chunk_size=chunk_size,
            transport=transport,
        ):
            pass
        return self._response

    def iter_resume(
        self,
        upload_url: Optional[str] = None,
        stream: Optional[Union[BinaryIO, bytes, Iterable[bytes]]] = None,
        size: Optional[int] = None,
        chunk_size: Optional[int] = None,
        transport: Optional[requests.Session] = None,
    ) -> Generator[common.UploadProgress, None, None]:
        """Streams resumption of an upload, yielding UploadProgress snapshots.

        Args:
            upload_url: The pre-existing upload session URL.
            stream: The data payload to resume uploading from.
            size: Total size of the payload in bytes, if known.
            chunk_size: Optional chunk size override in bytes.
            transport: Optional requests session.

        Yields:
            UploadProgress snapshots for each chunk transmission milestone.

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
        with self._capture_progress() as captured:
            try:
                stream_obj, computed_size = self._prepare_stream(stream, size)
                self._recover(sess, stream_obj)
                yield from self._transmit_all_chunks(
                    sess, stream_obj, computed_size, captured
                )
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
        if isinstance(stream, bytes):
            stream_obj: BinaryIO = io.BytesIO(stream)
            if computed_size is None:
                computed_size = len(stream)
        elif not hasattr(stream, "read") and isinstance(stream, Iterable):
            stream_obj = io.BytesIO(b"".join(stream))
            if computed_size is None:
                computed_size = stream_obj.getbuffer().nbytes
        else:
            stream_obj = stream
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

        if hasattr(stream_obj, "tell"):
            try:
                self._start_stream_offset = stream_obj.tell()
            except (OSError, AttributeError):
                self._start_stream_offset = 0

        return stream_obj, computed_size

    def _format_response(self, response: requests.Response) -> Any:
        """Formats response into protobuf message type if provided.

        Args:
            response: HTTP response object from final chunk.

        Returns:
            Deserialized protobuf message or the raw response object.
        """
        return _format_response_payload(response, self._config.response_type)


def _format_response_payload(
    response: Union[Any, bytes],
    response_type: Optional[Any],
) -> Any:
    """Formats raw response or bytes into protobuf or proto-plus message type if configured.

    Args:
        response: Raw HTTP response object or response body bytes.
        response_type: Deserializer callable, proto.Message class, or
            google.protobuf.message.Message class or instance.

    Returns:
        Deserialized protobuf message or the raw response object / bytes.
    """
    if response_type is None:
        return response

    content: bytes
    if isinstance(response, bytes):
        content = response
    elif hasattr(response, "content"):
        content = response.content
    else:
        content = bytes(response)

    if isinstance(response_type, type) and issubclass(response_type, proto.Message):
        return response_type.from_json(content, ignore_unknown_fields=True)
    if isinstance(response_type, type) and issubclass(
        response_type, google.protobuf.message.Message
    ):
        instance = response_type()
        return json_format.Parse(content, instance, ignore_unknown_fields=True)
    if isinstance(response_type, google.protobuf.message.Message):
        return json_format.Parse(content, response_type, ignore_unknown_fields=True)
    if hasattr(response_type, "from_json") and callable(response_type.from_json):
        return response_type.from_json(content)
    if callable(response_type):
        return response_type(content)

    return response
