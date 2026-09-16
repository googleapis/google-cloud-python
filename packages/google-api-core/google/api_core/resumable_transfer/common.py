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

"""Common constants, headers, and shared configuration for Resumable Upload protocol."""

import dataclasses
import datetime
import enum
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple, Union

import google.protobuf.message
import proto
from google.protobuf import json_format

import google.api_core.retry

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
    start_retry: Optional[
        Union[google.api_core.retry.Retry, google.api_core.retry.AsyncRetry]
    ] = None
    stall_minimum_rate: int = 64 * 1024
    stall_timeout: float = 120.0
    headers: Optional[Union[Mapping[str, str], Sequence[Tuple[str, str]]]] = None
    deadline: Optional[datetime.datetime] = None
    timeout: Optional[float] = None
    retry: Optional[
        Union[
            google.api_core.retry.Retry,
            google.api_core.retry.StreamingRetry,
            google.api_core.retry.AsyncRetry,
            google.api_core.retry.AsyncStreamingRetry,
        ]
    ] = None
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
        elif (
            self.start_retry is None
            and self.retry is not None
            and not isinstance(
                self.retry,
                (
                    google.api_core.retry.StreamingRetry,
                    google.api_core.retry.AsyncStreamingRetry,
                ),
            )
        ):
            self.start_retry = self.retry

    @property
    def start_headers(self) -> Optional[Sequence[Tuple[str, str]]]:
        """Returns normalized additional headers for the start request."""
        if self.headers is None:
            return None
        if isinstance(self.headers, Mapping):
            return list(self.headers.items())
        return list(self.headers)


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

    from_json_fn = getattr(response_type, "from_json", None)
    if callable(from_json_fn):
        if isinstance(response_type, type) and issubclass(response_type, proto.Message):
            return from_json_fn(content, ignore_unknown_fields=True)
        return from_json_fn(content)
    if isinstance(response_type, type) and issubclass(
        response_type, google.protobuf.message.Message
    ):
        instance = response_type()
        return json_format.Parse(content, instance, ignore_unknown_fields=True)
    if isinstance(response_type, google.protobuf.message.Message):
        return json_format.Parse(content, response_type, ignore_unknown_fields=True)
    if callable(response_type):
        return response_type(content)

    return response
