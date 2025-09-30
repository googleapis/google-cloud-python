# Copyright 2025 Google LLC
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

import pytest
from unittest import mock
from unittest.mock import AsyncMock
from google.cloud import _storage_v2

from google.cloud.storage._experimental.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)
from io import BytesIO


_TEST_BUCKET_NAME = "test-bucket"
_TEST_OBJECT_NAME = "test-object"
_TEST_GENERATION_NUMBER = 123456789
_TEST_READ_HANDLE = b"test-handle"


class TestAsyncMultiRangeDownloader:
    def create_read_ranges(self, num_ranges):
        ranges = []
        for i in range(num_ranges):
            ranges.append(
                _storage_v2.ReadRange(read_offset=i, read_length=1, read_id=i)
            )
        return ranges

    # helper method
    @pytest.mark.asyncio
    async def _make_mock_mrd(
        self,
        mock_grpc_client,
        mock_cls_async_read_object_stream,
        bucket_name=_TEST_BUCKET_NAME,
        object_name=_TEST_OBJECT_NAME,
        generation_number=_TEST_GENERATION_NUMBER,
        read_handle=_TEST_READ_HANDLE,
    ):
        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()
        mock_stream.generation_number = _TEST_GENERATION_NUMBER
        mock_stream.read_handle = _TEST_READ_HANDLE

        mrd = await AsyncMultiRangeDownloader.create_mrd(
            mock_grpc_client, bucket_name, object_name, generation_number, read_handle
        )

        return mrd

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_create_mrd(
        self, mock_grpc_client, mock_cls_async_read_object_stream
    ):
        # Arrange & Act
        mrd = await self._make_mock_mrd(
            mock_grpc_client, mock_cls_async_read_object_stream
        )

        # Assert
        mock_cls_async_read_object_stream.assert_called_once_with(
            client=mock_grpc_client,
            bucket_name=_TEST_BUCKET_NAME,
            object_name=_TEST_OBJECT_NAME,
            generation_number=_TEST_GENERATION_NUMBER,
            read_handle=_TEST_READ_HANDLE,
        )

        mrd.read_obj_str.open.assert_called_once()
        # Assert
        mock_cls_async_read_object_stream.assert_called_once_with(
            client=mock_grpc_client,
            bucket_name=_TEST_BUCKET_NAME,
            object_name=_TEST_OBJECT_NAME,
            generation_number=_TEST_GENERATION_NUMBER,
            read_handle=_TEST_READ_HANDLE,
        )

        mrd.read_obj_str.open.assert_called_once()

        assert mrd.client == mock_grpc_client
        assert mrd.bucket_name == _TEST_BUCKET_NAME
        assert mrd.object_name == _TEST_OBJECT_NAME
        assert mrd.generation_number == _TEST_GENERATION_NUMBER
        assert mrd.read_handle == _TEST_READ_HANDLE
        assert mrd.is_stream_open

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_download_ranges(
        self, mock_grpc_client, mock_cls_async_read_object_stream
    ):
        # Arrange
        mock_mrd = await self._make_mock_mrd(
            mock_grpc_client, mock_cls_async_read_object_stream
        )
        mock_mrd.read_obj_str.send = AsyncMock()
        mock_mrd.read_obj_str.recv = AsyncMock()
        mock_mrd.read_obj_str.recv.return_value = _storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                _storage_v2.ObjectRangeData(
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=b"these_are_18_chars", crc32c=123
                    ),
                    range_end=True,
                    read_range=_storage_v2.ReadRange(
                        read_offset=0, read_length=18, read_id=0
                    ),
                )
            ],
        )

        # Act
        buffer = BytesIO()
        results = await mock_mrd.download_ranges([(0, 18, buffer)])

        # Assert
        mock_mrd.read_obj_str.send.assert_called_once_with(
            _storage_v2.BidiReadObjectRequest(
                read_ranges=[
                    _storage_v2.ReadRange(read_offset=0, read_length=18, read_id=0)
                ]
            )
        )
        assert len(results) == 1
        assert results[0].bytes_requested == 18
        assert results[0].bytes_written == 18
        assert buffer.getvalue() == b"these_are_18_chars"

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_downloading_ranges_with_more_than_1000_should_throw_error(
        self, mock_grpc_client
    ):
        # Arrange
        mrd = AsyncMultiRangeDownloader(
            mock_grpc_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )

        # Act + Assert
        with pytest.raises(ValueError) as exc:
            await mrd.download_ranges(self.create_read_ranges(1001))

        # Assert
        assert (
            str(exc.value)
            == "Invalid input - length of read_ranges cannot be more than 1000"
        )

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_opening_mrd_more_than_once_should_throw_error(
        self, mock_grpc_client, mock_cls_async_read_object_stream
    ):
        # Arrange
        mrd = await self._make_mock_mrd(
            mock_grpc_client, mock_cls_async_read_object_stream
        )  # mock mrd is already opened

        # Act + Assert
        with pytest.raises(ValueError) as exc:
            await mrd.open()

        # Assert
        assert str(exc.value) == "Underlying bidi-gRPC stream is already open"

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_close_mrd(self, mock_grpc_client, mock_cls_async_read_object_stream):
        # Arrange
        mrd = await self._make_mock_mrd(
            mock_grpc_client, mock_cls_async_read_object_stream
        )  # mock mrd is already opened
        mrd.read_obj_str.close = AsyncMock()

        # Act
        await mrd.close()

        # Assert
        assert not mrd.is_stream_open

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_close_mrd_not_opened_should_throw_error(self, mock_grpc_client):
        # Arrange
        mrd = AsyncMultiRangeDownloader(
            mock_grpc_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )

        # Act + Assert
        with pytest.raises(ValueError) as exc:
            await mrd.close()

        # Assert
        assert str(exc.value) == "Underlying bidi-gRPC stream is not open"
        assert not mrd.is_stream_open

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_downloading_without_opening_should_throw_error(
        self, mock_grpc_client
    ):
        # Arrange
        mrd = AsyncMultiRangeDownloader(
            mock_grpc_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )

        # Act + Assert
        with pytest.raises(ValueError) as exc:
            await mrd.download_ranges([(0, 18, BytesIO())])

        # Assert
        assert str(exc.value) == "Underlying bidi-gRPC stream is not open"
        assert not mrd.is_stream_open
