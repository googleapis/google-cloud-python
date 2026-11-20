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

"""Experimental asynchronous transfer manager for parallel uploads."""

from __future__ import annotations

import io
import os
from typing import Any, Optional, Union

from google.api_core.retry_async import AsyncRetry

from google.cloud import _storage_v2
from google.cloud.storage import Blob

# Constants to be passed in as `worker_type`.
COROUTINE = "coroutine"
PROCESS = "process"

DEFAULT_MAX_WORKERS = min(4 + (os.cpu_count() or 1) // 2, 16)


async def upload_chunks_concurrently_from_filename(
    client: Any,
    bucket_name: str,
    object_name: str,
    filename: str,
    *,
    blob: Optional[Blob] = None,
    preferred_segment_size_bytes: Optional[int] = None,
    max_workers: int = DEFAULT_MAX_WORKERS,
    worker_type: str = COROUTINE,
    enable_checksum: bool = True,
    retry: Optional[AsyncRetry] = None,
    timeout: Optional[float] = None,
) -> _storage_v2.Object:
    """Uploads a local file concurrently using parallel uploads.

    Args:
        client: Asynchronous Storage client used for the upload.
        bucket_name: Name of the destination Cloud Storage bucket.
        object_name: Name of the destination Cloud Storage object.
        filename: Path to the local file to upload.
        blob: Optional ``Blob`` supplying destination object metadata.
        preferred_segment_size_bytes: Optional preferred segment size in bytes.
        max_workers: Maximum number of concurrent segment uploads. Defaults to
            ``DEFAULT_MAX_WORKERS``.
        worker_type: Concurrency model for workers, either ``COROUTINE`` or
            ``PROCESS``. Defaults to ``COROUTINE``.
        enable_checksum: If ``True`` (default), enables checksum validation.
        retry: Optional ``AsyncRetry`` policy for upload requests.
        timeout: Optional request timeout in seconds.

    Returns:
        The uploaded ``_storage_v2.Object`` resource.

    Raises:
        NotImplementedError: Always raised in this stub interface.
    """
    raise NotImplementedError


async def upload_chunks_concurrently_from_bytes(
    client: Any,
    bucket_name: str,
    object_name: str,
    data: Union[bytes, bytearray, memoryview, io.BytesIO],
    *,
    blob: Optional[Blob] = None,
    preferred_segment_size_bytes: Optional[int] = None,
    max_workers: int = DEFAULT_MAX_WORKERS,
    enable_checksum: bool = True,
    retry: Optional[AsyncRetry] = None,
    timeout: Optional[float] = None,
) -> _storage_v2.Object:
    """Uploads an in-memory buffer concurrently using parallel uploads.

    Args:
        client: Asynchronous Storage client used for the upload.
        bucket_name: Name of the destination Cloud Storage bucket.
        object_name: Name of the destination Cloud Storage object.
        data: In-memory payload to upload (``bytes``, ``bytearray``,
            ``memoryview``, or ``io.BytesIO``).
        blob: Optional ``Blob`` supplying destination object metadata.
        preferred_segment_size_bytes: Optional preferred segment size in bytes.
        max_workers: Maximum number of concurrent segment uploads. Defaults to
            ``DEFAULT_MAX_WORKERS``.
        enable_checksum: If ``True`` (default), enables checksum validation.
        retry: Optional ``AsyncRetry`` policy for upload requests.
        timeout: Optional request timeout in seconds.

    Returns:
        The uploaded ``_storage_v2.Object`` resource.

    Raises:
        NotImplementedError: Always raised in this stub interface.
    """
    raise NotImplementedError
