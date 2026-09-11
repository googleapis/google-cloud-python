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

import dataclasses
import enum
from typing import Optional

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

