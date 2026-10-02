# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Static API contracts, checked by the mypy nox session."""

from __future__ import annotations

from datetime import timedelta
from io import BytesIO, TextIOWrapper
from typing import BinaryIO

from requests import Response, Session
from typing_extensions import assert_type

from google.cloud import _storage_v2
from google.cloud.storage import Blob, Bucket, Client, transfer_manager
from google.cloud.storage._media.requests.upload import XMLMPUPart
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_multi_range_downloader import (
    _is_open_retryable,
    _is_read_retryable,
)
from google.cloud.storage.asyncio.async_read_object_stream import _AsyncReadObjectStream
from google.cloud.storage.asyncio.async_write_object_stream import (
    _AsyncWriteObjectStream,
)
from google.cloud.storage.asyncio.retry._helpers import (
    _extract_bidi_writes_redirect_proto,
)
from google.cloud.storage.batch import _FutureDict, _FutureResponse
from google.cloud.storage.bucket import _raise_if_len_differs
from google.cloud.storage.fileio import BlobReader, BlobWriter, SlidingBuffer
from google.cloud.storage.hmac_key import HMACKeyMetadata
from google.cloud.storage.retry import DEFAULT_RETRY_IF_GENERATION_SPECIFIED


class WriteOnlySink:
    """A download target need not implement the complete IO interface."""

    def write(self, data: bytes) -> None:
        pass


def synchronous_api(client: Client, bucket: Bucket, blob: Blob) -> None:
    assert_type(client.create_anonymous_client(), Client)
    assert_type(client.project, str | None)
    assert_type(next(client.list_buckets()), Bucket)
    assert_type(next(client.list_blobs(bucket)), Blob)
    assert_type(next(bucket.list_blobs()), Blob)
    assert_type(next(client.list_hmac_keys()), HMACKeyMetadata)
    assert_type(next(next(client.list_blobs(bucket).pages)), Blob)
    assert_type(client.list_blobs(bucket).prefixes, set[str])

    assert_type(blob.open("rb"), BlobReader)
    assert_type(blob.open("wb"), BlobWriter)
    assert_type(blob.open(), TextIOWrapper[BinaryIO])
    assert_type(blob.open("rb").read(), bytes)
    assert_type(blob.open("rt").read(), str)
    assert_type(blob.generate_signed_url(expiration=timedelta(minutes=5)), str)

    assert_type(blob.metadata, dict[str, str] | None)
    assert_type(bucket.labels, dict[str, str])
    assert_type(_FutureResponse(_FutureDict()).content, _FutureDict)
    _raise_if_len_differs(2, generations=[1, 2], unset=None)
    buffer = SlidingBuffer()
    assert_type(buffer.write(bytearray(b"payload")), int)
    assert_type(buffer.write(memoryview(b"payload")), int)
    assert_type(buffer.close(), None)
    bucket.delete_blobs([blob])
    bucket.delete_blobs(["object-name"])
    assert_type(_is_open_retryable(Exception()), bool)
    assert_type(_is_read_retryable(Exception()), bool)
    assert_type(
        _extract_bidi_writes_redirect_proto(Exception()),
        _storage_v2.BidiWriteObjectRedirectedError | None,
    )
    assert_type(
        XMLMPUPart("url", "upload-id", "file", 0, 10, 1).upload(Session()), Response
    )

    blob.upload_from_file(BytesIO(b"payload"), timeout=(None, 30))
    blob.upload_from_string(b"payload", retry=DEFAULT_RETRY_IF_GENERATION_SPECIFIED)
    blob.download_to_file(WriteOnlySink(), timeout=None)
    assert_type(
        transfer_manager.upload_many([("source.txt", blob)], deadline=2.5),
        list[BaseException | None],
    )
    assert_type(
        transfer_manager.download_many([(blob, "target.txt")]),
        list[BaseException | None],
    )

    # These ignores must remain necessary, so accidental Any annotations fail
    # mypy's unused-ignore check.
    blob.upload_from_string(42)  # type: ignore[arg-type]
    buffer.write("text")  # type: ignore[arg-type]
    blob.metadata = {"key": 42}  # type: ignore[dict-item]
    bucket.labels = {"key": 42}  # type: ignore[dict-item]
    bucket.delete_blobs([42])  # type: ignore[list-item]
    _raise_if_len_differs(2, generations=42)  # type: ignore[arg-type]
    transfer_manager._ChecksummingSparseFileWrapper("file", "start", True)  # type: ignore[arg-type]
    transfer_manager.upload_many([], deadline="soon")  # type: ignore[arg-type]


async def asynchronous_api(
    client: AsyncGrpcClient,
    reader: _AsyncReadObjectStream,
    writer: _AsyncWriteObjectStream,
) -> None:
    assert_type(client.grpc_client, _storage_v2.StorageAsyncClient)
    assert_type(await reader.recv(), _storage_v2.BidiReadObjectResponse)
    assert_type(await writer.recv(), _storage_v2.BidiWriteObjectResponse)
    await reader.send(_storage_v2.BidiReadObjectRequest())
    await writer.send(_storage_v2.BidiWriteObjectRequest())
