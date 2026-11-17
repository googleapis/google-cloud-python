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

from __future__ import annotations

import inspect
import io
from collections.abc import Callable, Sequence
from typing import Any, Optional, Union, get_type_hints
from unittest import mock

import pytest
from google.api_core.retry_async import AsyncRetry

from google.cloud import _storage_v2
from google.cloud.storage import Blob
from google.cloud.storage._experimental.asyncio.async_transfer_manager import (
    COROUTINE,
    DEFAULT_MAX_WORKERS,
    PROCESS,
    upload_chunks_concurrently_from_bytes,
    upload_chunks_concurrently_from_filename,
)

_BUCKET_NAME = "test-bucket"
_OBJECT_NAME = "test-object"
_FILENAME = "/tmp/test-upload.bin"
_PREFERRED_SEGMENT_SIZE_BYTES = 32 * 1024 * 1024
_MAX_WORKERS = 8
_TIMEOUT_SECONDS = 30.0
_PAYLOAD_BYTES = b"parallel-upload-payload"


def _assert_parameter_specs(
    target_callable: Callable[..., Any],
    expected_specs: Sequence[tuple[str, Any, Any]],
) -> None:
    """Asserts exact parameter names, kinds, and defaults on target_callable."""
    signature = inspect.signature(target_callable)
    actual_specs = [
        (param.name, param.kind, param.default)
        for param in signature.parameters.values()
    ]
    assert actual_specs == list(expected_specs)


class TestAsyncTransferManagerConstants:
    """Unit tests for module-level constants in async_transfer_manager."""

    def test_worker_type_constants(self) -> None:
        assert isinstance(COROUTINE, str)
        assert COROUTINE == "coroutine"
        assert isinstance(PROCESS, str)
        assert PROCESS == "process"

    def test_default_max_workers_constant(self) -> None:
        assert isinstance(DEFAULT_MAX_WORKERS, int)
        assert 4 <= DEFAULT_MAX_WORKERS <= 16


class TestUploadChunksConcurrentlyFromFilename:
    """Unit tests for upload_chunks_concurrently_from_filename stub interface."""

    def test_signature_and_type_hints(self) -> None:
        assert inspect.iscoroutinefunction(upload_chunks_concurrently_from_filename)
        _assert_parameter_specs(
            upload_chunks_concurrently_from_filename,
            [
                (
                    "client",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.empty,
                ),
                (
                    "bucket_name",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.empty,
                ),
                (
                    "object_name",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.empty,
                ),
                (
                    "filename",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.empty,
                ),
                ("blob", inspect.Parameter.KEYWORD_ONLY, None),
                (
                    "preferred_segment_size_bytes",
                    inspect.Parameter.KEYWORD_ONLY,
                    None,
                ),
                (
                    "max_workers",
                    inspect.Parameter.KEYWORD_ONLY,
                    DEFAULT_MAX_WORKERS,
                ),
                ("worker_type", inspect.Parameter.KEYWORD_ONLY, COROUTINE),
                ("enable_checksum", inspect.Parameter.KEYWORD_ONLY, True),
                ("retry", inspect.Parameter.KEYWORD_ONLY, None),
                ("timeout", inspect.Parameter.KEYWORD_ONLY, None),
            ],
        )

        type_hints = get_type_hints(upload_chunks_concurrently_from_filename)
        assert type_hints == {
            "client": Any,
            "bucket_name": str,
            "object_name": str,
            "filename": str,
            "blob": Optional[Blob],
            "preferred_segment_size_bytes": Optional[int],
            "max_workers": int,
            "worker_type": str,
            "enable_checksum": bool,
            "retry": Optional[AsyncRetry],
            "timeout": Optional[float],
            "return": _storage_v2.Object,
        }

    def test_rejects_fifth_positional_arg_with_type_error(self) -> None:
        mock_client = mock.MagicMock()
        mock_blob = mock.create_autospec(Blob, instance=True)
        upload_fn: Callable[..., object] = upload_chunks_concurrently_from_filename

        with pytest.raises(TypeError):
            upload_fn(
                mock_client,
                _BUCKET_NAME,
                _OBJECT_NAME,
                _FILENAME,
                mock_blob,
            )

    def test_missing_required_positional_args_raises_type_error(self) -> None:
        mock_client = mock.MagicMock()
        upload_fn: Callable[..., object] = upload_chunks_concurrently_from_filename

        with pytest.raises(TypeError):
            upload_fn(mock_client, _BUCKET_NAME, _OBJECT_NAME)

    @pytest.mark.parametrize(
        "unexpected_kwarg",
        ["chunk_size", "segment_size_bytes"],
    )
    def test_rejects_unexpected_keyword_arg_with_type_error(
        self,
        unexpected_kwarg: str,
    ) -> None:
        mock_client = mock.MagicMock()
        upload_fn: Callable[..., object] = upload_chunks_concurrently_from_filename

        with pytest.raises(TypeError):
            upload_fn(
                mock_client,
                _BUCKET_NAME,
                _OBJECT_NAME,
                _FILENAME,
                **{unexpected_kwarg: _PREFERRED_SEGMENT_SIZE_BYTES},
            )

    @pytest.mark.asyncio
    async def test_defers_until_awaited(self) -> None:
        mock_client = mock.MagicMock()

        coro = upload_chunks_concurrently_from_filename(
            mock_client,
            _BUCKET_NAME,
            _OBJECT_NAME,
            _FILENAME,
        )
        assert inspect.iscoroutine(coro)
        with pytest.raises(NotImplementedError):
            await coro

    @pytest.mark.asyncio
    async def test_all_keyword_options_raises_not_implemented_error(
        self,
    ) -> None:
        mock_client = mock.MagicMock()
        mock_blob = mock.create_autospec(Blob, instance=True)
        mock_retry = mock.create_autospec(AsyncRetry, instance=True)

        with pytest.raises(NotImplementedError):
            await upload_chunks_concurrently_from_filename(
                client=mock_client,
                bucket_name=_BUCKET_NAME,
                object_name=_OBJECT_NAME,
                filename=_FILENAME,
                blob=mock_blob,
                preferred_segment_size_bytes=_PREFERRED_SEGMENT_SIZE_BYTES,
                max_workers=_MAX_WORKERS,
                worker_type=PROCESS,
                enable_checksum=False,
                retry=mock_retry,
                timeout=_TIMEOUT_SECONDS,
            )


class TestUploadChunksConcurrentlyFromBytes:
    """Unit tests for upload_chunks_concurrently_from_bytes stub interface."""

    def test_signature_and_type_hints(self) -> None:
        assert inspect.iscoroutinefunction(upload_chunks_concurrently_from_bytes)
        _assert_parameter_specs(
            upload_chunks_concurrently_from_bytes,
            [
                (
                    "client",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.empty,
                ),
                (
                    "bucket_name",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.empty,
                ),
                (
                    "object_name",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.empty,
                ),
                (
                    "data",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.empty,
                ),
                ("blob", inspect.Parameter.KEYWORD_ONLY, None),
                (
                    "preferred_segment_size_bytes",
                    inspect.Parameter.KEYWORD_ONLY,
                    None,
                ),
                (
                    "max_workers",
                    inspect.Parameter.KEYWORD_ONLY,
                    DEFAULT_MAX_WORKERS,
                ),
                ("enable_checksum", inspect.Parameter.KEYWORD_ONLY, True),
                ("retry", inspect.Parameter.KEYWORD_ONLY, None),
                ("timeout", inspect.Parameter.KEYWORD_ONLY, None),
            ],
        )

        type_hints = get_type_hints(upload_chunks_concurrently_from_bytes)
        assert type_hints == {
            "client": Any,
            "bucket_name": str,
            "object_name": str,
            "data": Union[bytes, bytearray, memoryview, io.BytesIO],
            "blob": Optional[Blob],
            "preferred_segment_size_bytes": Optional[int],
            "max_workers": int,
            "enable_checksum": bool,
            "retry": Optional[AsyncRetry],
            "timeout": Optional[float],
            "return": _storage_v2.Object,
        }

    def test_rejects_fifth_positional_arg_with_type_error(self) -> None:
        mock_client = mock.MagicMock()
        mock_blob = mock.create_autospec(Blob, instance=True)
        upload_fn: Callable[..., object] = upload_chunks_concurrently_from_bytes

        with pytest.raises(TypeError):
            upload_fn(
                mock_client,
                _BUCKET_NAME,
                _OBJECT_NAME,
                _PAYLOAD_BYTES,
                mock_blob,
            )

    def test_missing_required_positional_args_raises_type_error(self) -> None:
        mock_client = mock.MagicMock()
        upload_fn: Callable[..., object] = upload_chunks_concurrently_from_bytes

        with pytest.raises(TypeError):
            upload_fn(mock_client, _BUCKET_NAME, _OBJECT_NAME)

    @pytest.mark.parametrize(
        "unexpected_kwarg",
        ["chunk_size", "segment_size_bytes", "worker_type"],
    )
    def test_rejects_unexpected_keyword_arg_with_type_error(
        self,
        unexpected_kwarg: str,
    ) -> None:
        mock_client = mock.MagicMock()
        upload_fn: Callable[..., object] = upload_chunks_concurrently_from_bytes

        with pytest.raises(TypeError):
            upload_fn(
                mock_client,
                _BUCKET_NAME,
                _OBJECT_NAME,
                _PAYLOAD_BYTES,
                **{unexpected_kwarg: _PREFERRED_SEGMENT_SIZE_BYTES},
            )

    @pytest.mark.asyncio
    async def test_defers_until_awaited(self) -> None:
        mock_client = mock.MagicMock()

        coro = upload_chunks_concurrently_from_bytes(
            mock_client,
            _BUCKET_NAME,
            _OBJECT_NAME,
            _PAYLOAD_BYTES,
        )
        assert inspect.iscoroutine(coro)
        with pytest.raises(NotImplementedError):
            await coro

    @pytest.mark.asyncio
    async def test_all_keyword_options_raises_not_implemented_error(
        self,
    ) -> None:
        mock_client = mock.MagicMock()
        mock_blob = mock.create_autospec(Blob, instance=True)
        mock_retry = mock.create_autospec(AsyncRetry, instance=True)

        with pytest.raises(NotImplementedError):
            await upload_chunks_concurrently_from_bytes(
                client=mock_client,
                bucket_name=_BUCKET_NAME,
                object_name=_OBJECT_NAME,
                data=_PAYLOAD_BYTES,
                blob=mock_blob,
                preferred_segment_size_bytes=_PREFERRED_SEGMENT_SIZE_BYTES,
                max_workers=_MAX_WORKERS,
                enable_checksum=False,
                retry=mock_retry,
                timeout=_TIMEOUT_SECONDS,
            )
