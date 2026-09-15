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

"""Common constants and headers for Resumable Upload protocol."""

import contextlib
import dataclasses
import datetime
import enum
import time
from typing import (
    Any,
    Callable,
    Generator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import google.protobuf.message
import proto
from google.protobuf import json_format
import requests

try:
    import aiohttp
except ImportError:  # pragma: NO COVER
    aiohttp = None  # type: ignore

from google.api_core import exceptions

_NETWORK_ERRORS: Tuple[type, ...] = (
    TimeoutError,
    ConnectionError,
    requests.exceptions.ConnectionError,
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.Timeout,
)
if aiohttp is not None:  # pragma: NO COVER
    _NETWORK_ERRORS = _NETWORK_ERRORS + (aiohttp.ClientError,)

# Default chunk size: 10 MiB
DEFAULT_CHUNK_SIZE = 10 * 1024 * 1024

# Protocol Headers
HEADER_PROTOCOL = "X-Goog-Upload-Protocol"
HEADER_COMMAND = "X-Goog-Upload-Command"
HEADER_STATUS = "X-Goog-Upload-Status"
HEADER_URL = "X-Goog-Upload-URL"
HEADER_OFFSET = "X-Goog-Upload-Offset"
HEADER_SIZE_RECEIVED = "X-Goog-Upload-Size-Received"
HEADER_CONTENT_TYPE = "X-Goog-Upload-Header-Content-Type"
HEADER_CONTENT_LENGTH = "X-Goog-Upload-Header-Content-Length"
HEADER_CHUNK_GRANULARITY = "X-Goog-Upload-Chunk-Granularity"

PROTOCOL_RESUMABLE = "resumable"


class Command(str, enum.Enum):
    """Protocol commands."""

    START = "start"
    UPLOAD = "upload"
    FINALIZE = "finalize"
    QUERY = "query"
    CANCEL = "cancel"


class Status(str, enum.Enum):
    """Server upload status values."""

    ACTIVE = "active"
    FINAL = "final"
    CANCELLED = "cancelled"


class ProgressState(str, enum.Enum):
    """Progress notification state values."""

    STARTED = "started"
    UPLOADING = "uploading"
    RECOVERING = "recovering"
    OFFSET_RECEIVED = "offset received"
    FINALIZED = "finalized"


@dataclasses.dataclass(frozen=True)
class UploadProgress:
    """Upload progress notification payload.

    Attributes:
        upload_url: The unique session URL for this upload.
        chunk_size: The actual negotiated chunk size.
        bytes_uploaded: The total confirmed bytes committed so far.
        total_bytes: The total size of the stream in bytes, if known.
        state: The current progress state.
    """

    upload_url: str
    chunk_size: int
    bytes_uploaded: int
    total_bytes: Optional[int]
    state: ProgressState


# HTTP status codes indicating transient retryable errors
RETRYABLE_STATUS_CODES = (408, 429, 500, 502, 503, 504)

# HTTP status codes indicating state consistency errors requiring recovery
RECOVERABLE_STATUS_CODES = (400, 409, 412, 416)


@dataclasses.dataclass
class ResumableUploadConfig:
    """Configuration options for a resumable upload.

    Attributes:
        chunk_size: Size in bytes for each uploaded data chunk. Defaults to 10 MiB.
        start_timeout: Local per-request timeout in seconds for start request.
        start_retry: Custom retry policy for the start request.
        stall_minimum_rate: Minimum transfer rate in bytes per second. Defaults to 64 KiB/s.
        stall_timeout: Stall duration threshold in seconds. Defaults to 120s.
        headers: Additional HTTP headers dispatched exclusively with start request.
        deadline: Overall global deadline for the upload process.
        timeout: Fallback per-request timeout.
        retry: Fallback retry policy.
        on_progress: Callback function receiving UploadProgress notifications.
        response_type: Optional message class (proto.Message or google.protobuf.message.Message),
            callable deserializer, or None to return raw response.
        content_type: MIME type of the stream payload.
    """

    chunk_size: int = DEFAULT_CHUNK_SIZE
    start_timeout: Optional[float] = None
    start_retry: Optional[Any] = None
    stall_minimum_rate: int = 64 * 1024
    stall_timeout: float = 120.0
    headers: Optional[Union[Mapping[str, str], Sequence[Tuple[str, str]]]] = None
    deadline: Optional[datetime.datetime] = None
    timeout: Optional[float] = None
    retry: Optional[Any] = None
    on_progress: Optional[Callable[[UploadProgress], None]] = None
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
        if self.headers is None:
            return None
        if isinstance(self.headers, Mapping):
            return list(self.headers.items())
        return list(self.headers)


def compute_deadline_remaining(
    deadline: Optional[datetime.datetime],
) -> Optional[float]:
    """Calculates remaining seconds until the configured upload deadline.

    Args:
        deadline: Configured deadline datetime or None.

    Returns:
        Remaining seconds before deadline, or None if no deadline configured.

    Raises:
        exceptions.DeadlineExceeded: If deadline has already elapsed.
    """
    if deadline is not None:
        now = datetime.datetime.now(datetime.timezone.utc)
        if deadline.tzinfo is None:
            dl = deadline.astimezone(datetime.timezone.utc)
        else:
            dl = deadline
        remaining = (dl - now).total_seconds()
        if remaining <= 0:
            raise exceptions.DeadlineExceeded(
                f"Resumable upload deadline {deadline} exceeded."
            )
        return remaining
    return None


def compute_chunk_timeout(
    data_len: int,
    stall_minimum_rate: int,
    stall_timeout: float,
    aggregate_lag: float,
    configured_timeout: Optional[float] = None,
    deadline_remaining: Optional[float] = None,
) -> float:
    """Computes dynamic per-attempt chunk timeout based on stall control and deadlines.

    Args:
        data_len: Length of the chunk in bytes.
        stall_minimum_rate: Configured minimum transfer rate (bytes/s).
        stall_timeout: Configured stall timeout threshold in seconds.
        aggregate_lag: Current accumulated stall lag in seconds.
        configured_timeout: Optional user-configured timeout ceiling in seconds.
        deadline_remaining: Optional remaining seconds until deadline.

    Returns:
        Per-attempt timeout in seconds.
    """
    expected_sec = data_len / stall_minimum_rate if stall_minimum_rate > 0 else 60.0
    next_chunk_timeout = max(
        1.0,
        expected_sec - aggregate_lag + stall_timeout,
    )
    per_attempt_timeout = max(5.0, min(next_chunk_timeout, 2.0 * expected_sec))

    if configured_timeout:
        per_attempt_timeout = min(configured_timeout, per_attempt_timeout)

    if deadline_remaining is not None:
        per_attempt_timeout = min(per_attempt_timeout, deadline_remaining)

    return per_attempt_timeout


class StallTracker:
    """Tracks upload throughput lag against configured stall thresholds."""

    def __init__(
        self,
        minimum_rate: int = 64 * 1024,
        timeout: float = 120.0,
    ) -> None:
        """Initializes the stall tracker.

        Args:
            minimum_rate: Minimum transfer rate in bytes per second.
            timeout: Stall duration threshold in seconds.
        """
        self.minimum_rate = minimum_rate
        self.timeout = timeout
        self.aggregate_lag: float = 0.0
        self.stall_timeout_started: Optional[float] = None

    def update(
        self,
        data_len: int,
        t_start: float,
        t_elapsed: float,
        upload_url: Optional[str] = None,
        chunk_size: Optional[int] = None,
        deadline_checker: Optional[Callable[[], Any]] = None,
    ) -> None:
        """Updates aggregate lag and evaluates stall condition.

        Args:
            data_len: Length of the transmitted chunk in bytes.
            t_start: Monotonic timestamp before chunk transmission began.
            t_elapsed: Elapsed duration in seconds for chunk transmission.
            upload_url: Session upload URL for diagnostic metadata.
            chunk_size: Chunk size in bytes for diagnostic metadata.
            deadline_checker: Optional callback to evaluate deadline before raising stall error.

        Raises:
            exceptions.DeadlineExceeded: If upload deadline is exceeded.
            exceptions.TransferStalledError: If transfer throughput stalls past configured timeout.
        """
        if not (self.minimum_rate and self.timeout):
            return

        rate = self.minimum_rate
        expected_sec = data_len / rate if rate > 0 else 0.0
        current_lag = t_elapsed - expected_sec
        self.aggregate_lag = max(0.0, self.aggregate_lag + current_lag)

        if self.aggregate_lag > 0.0:
            if self.stall_timeout_started is None:
                self.stall_timeout_started = t_start
            if (
                time.monotonic() - self.stall_timeout_started >= self.timeout
                or self.aggregate_lag >= self.timeout
            ):
                if deadline_checker is not None:
                    deadline_checker()
                raise exceptions.TransferStalledError(
                    f"Upload stalled: transfer rate remained below {rate} bytes/s "
                    f"for longer than {self.timeout}s.",
                    upload_url=upload_url,
                    chunk_size=chunk_size,
                )
        else:
            self.stall_timeout_started = None


def format_response_payload(
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
        return cast(Any, response_type).from_json(content, ignore_unknown_fields=True)
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


def is_recoverable_error(exc: Exception) -> bool:
    """Returns True if the exception represents a state error requiring server offset recovery."""
    return (
        isinstance(exc, exceptions.GoogleAPICallError)
        and exc.code in RECOVERABLE_STATUS_CODES
    ) or isinstance(exc, exceptions.MissingStatusHeaderError)


def is_terminal_error(exc: Exception) -> bool:
    """Returns True if the exception is non-retryable and should abort transfer immediately."""
    return isinstance(
        exc,
        (
            exceptions.DeadlineExceeded,
            exceptions.TransferStalledError,
            exceptions.UploadCancelledError,
            exceptions.UnseekableStreamError,
        ),
    )


DEFAULT_START_TIMEOUT = 60.0


def is_http_retryable_error(exc: Any) -> bool:
    """Returns True if exception is transient and retryable for unary requests."""
    if isinstance(exc, exceptions.MissingStatusHeaderError):
        return True
    if isinstance(exc, exceptions.GoogleAPICallError):
        return exc.code in RETRYABLE_STATUS_CODES
    return False


def is_network_error(exc: Any) -> bool:
    """Returns True if exception represents a transient network or connection error."""
    return isinstance(exc, _NETWORK_ERRORS)


def is_retryable_error(exc: Any) -> bool:
    """Determines if an exception is retryable for unary requests (start, query, cancel)."""
    if is_terminal_error(exc):
        return False
    return is_network_error(exc) or is_http_retryable_error(exc)


def is_streaming_retryable_error(exc: Any) -> bool:
    """Determines if an exception is retryable during chunk streaming."""
    if is_terminal_error(exc):
        return False
    return is_retryable_error(exc) or is_recoverable_error(exc)


class BaseResumableUploadSession:
    """Base class providing shared state and protocol helpers for resumable uploads."""

    def __init__(
        self,
        upload_url: Optional[str] = None,
        config: Optional[ResumableUploadConfig] = None,
        resumable_url: Optional[str] = None,
        transport: Optional[Any] = None,
    ) -> None:
        from google.api_core.resumable_transfer import upload_state

        self._config = config or ResumableUploadConfig()
        self._transport = transport
        self._response: Optional[Any] = None
        self._state = upload_state.ProtocolState(
            upload_url=upload_url,
            chunk_size=self._config.chunk_size,
            resumable_url=resumable_url,
        )

        self._buffered_chunk: Optional[memoryview] = None
        self._buffered_chunk_offset: int = 0
        self._start_stream_offset: int = 0
        self._stream_eof: bool = False

        self._needs_recovery: bool = False
        self._recovered_from_error: bool = False

        self._stall_tracker = StallTracker(
            minimum_rate=self._config.stall_minimum_rate,
            timeout=self._config.stall_timeout,
        )

    def _get_retry_predicate(self) -> Callable[[Any], bool]:
        """Returns a predicate function for unary requests (start, query, cancel)."""
        return is_retryable_error

    def _get_streaming_predicate(self) -> Callable[[Any], bool]:
        """Returns a predicate function for determining if an exception is retryable during chunk streaming."""
        return is_streaming_retryable_error

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

    @property
    def _aggregate_lag(self) -> float:
        """float: Current accumulated stall control throughput lag."""
        return self._stall_tracker.aggregate_lag

    @_aggregate_lag.setter
    def _aggregate_lag(self, value: float) -> None:
        self._stall_tracker.aggregate_lag = value

    @property
    def _stall_timeout_started(self) -> Optional[float]:
        """Optional[float]: Monotonic timestamp when stall condition first triggered."""
        return self._stall_tracker.stall_timeout_started

    @_stall_timeout_started.setter
    def _stall_timeout_started(self, value: Optional[float]) -> None:
        self._stall_tracker.stall_timeout_started = value

    def _enrich_exception(self, exc: BaseException) -> None:
        """Attaches session diagnostic metadata to an active exception."""
        setattr(exc, "upload_url", self.upload_url)
        setattr(exc, "chunk_size", self.chunk_size)

    def _create_progress(self, state: ProgressState) -> Optional[UploadProgress]:
        """Creates an UploadProgress snapshot if upload_url is established."""
        if not self.upload_url:
            return None
        return UploadProgress(
            upload_url=self.upload_url,
            chunk_size=self.chunk_size,
            bytes_uploaded=self._state.bytes_uploaded,
            total_bytes=self._state.total_bytes,
            state=state,
        )

    def _notify_progress(self, state: ProgressState) -> Optional[UploadProgress]:
        """Dispatches an UploadProgress snapshot to config.on_progress."""
        progress = self._create_progress(state)
        if progress is not None and self._config.on_progress:
            self._config.on_progress(progress)
        return progress

    def _get_deadline_remaining(self) -> Optional[float]:
        """Calculates remaining seconds until the configured upload deadline."""
        return compute_deadline_remaining(self._config.deadline)

    def _get_start_timeout(self) -> float:
        """Computes timeout in seconds for start and control requests."""
        remaining = self._get_deadline_remaining()
        timeout = (
            self._config.start_timeout or self._config.timeout or DEFAULT_START_TIMEOUT
        )
        if remaining is not None:
            return min(timeout, remaining)
        return timeout

    def _compute_chunk_timeout(self, data_len: int) -> float:
        """Computes dynamic per-attempt chunk timeout based on stall control and deadlines."""
        remaining = self._get_deadline_remaining()
        return compute_chunk_timeout(
            data_len=data_len,
            stall_minimum_rate=self._config.stall_minimum_rate,
            stall_timeout=self._config.stall_timeout,
            aggregate_lag=self._stall_tracker.aggregate_lag,
            configured_timeout=self._config.timeout,
            deadline_remaining=remaining,
        )

    def _update_stall_control(
        self, data_len: int, t_start: float, t_elapsed: float
    ) -> None:
        """Updates aggregate transfer rate lag and enforces stall timeout and deadlines."""
        self._stall_tracker.update(
            data_len=data_len,
            t_start=t_start,
            t_elapsed=t_elapsed,
            upload_url=self.upload_url,
            chunk_size=self.chunk_size,
            deadline_checker=self._get_deadline_remaining,
        )

    def _format_response(self, response: Any) -> Any:
        """Formats response into protobuf message type if provided."""
        return format_response_payload(response, self._config.response_type)

    def _reposition_stream_offset(self, stream_obj: Any, received: int) -> int:
        """Adjusts in-memory chunk buffer or seeks input stream to server offset."""
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
                raise exceptions.UnseekableStreamError(
                    f"Stream is not seekable. Cannot recover upload to offset {received}.",
                    upload_url=self.upload_url,
                    chunk_size=self.chunk_size,
                )
            try:
                stream_obj.seek(self._start_stream_offset + received)
                return received
            except (OSError, AttributeError) as exc:
                raise exceptions.UnseekableStreamError(
                    f"Failed to seek stream to offset {received}: {exc}",
                    upload_url=self.upload_url,
                    chunk_size=self.chunk_size,
                ) from exc

        raise exceptions.UnseekableStreamError(
            f"Server offset {received} precedes active buffer. Stream cannot be rewound."
            if stream_obj is None
            else f"Stream is not seekable. Cannot recover upload to offset {received}.",
            upload_url=self.upload_url,
            chunk_size=self.chunk_size,
        )

    def _finish_response(self) -> Any:
        """Returns the final response or raises ValueError if none received."""
        if self._response is None:
            raise ValueError("Upload completed without receiving a final response.")
        return self._response

