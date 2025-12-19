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

import asyncio
import pytest
from unittest import mock
from unittest.mock import AsyncMock
from google.cloud import _storage_v2
from google.api_core import exceptions
from google_crc32c import Checksum

from google.cloud.storage._experimental.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)
from google.cloud.storage._experimental.asyncio import async_read_object_stream
from io import BytesIO
from google.cloud.storage.exceptions import DataCorruption


_TEST_BUCKET_NAME = "test-bucket"
_TEST_OBJECT_NAME = "test-object"
_TEST_OBJECT_SIZE = 1024 * 1024  # 1 MiB
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
        mock_stream.persisted_size = _TEST_OBJECT_SIZE
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
        assert mrd.persisted_size == _TEST_OBJECT_SIZE
        assert mrd.is_stream_open

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_download_ranges_via_async_gather(
        self, mock_grpc_client, mock_cls_async_read_object_stream, mock_random_int
    ):
        # Arrange
        data = b"these_are_18_chars"
        crc32c = Checksum(data).digest()
        crc32c_int = int.from_bytes(crc32c, "big")
        crc32c_checksum_for_data_slice = int.from_bytes(
            Checksum(data[10:16]).digest(), "big"
        )

        mock_mrd = await self._make_mock_mrd(
            mock_grpc_client, mock_cls_async_read_object_stream
        )
        mock_random_int.side_effect = [123, 456, 789, 91011]  # for _func_id and read_id
        mock_mrd.read_obj_str.send = AsyncMock()
        mock_mrd.read_obj_str.recv = AsyncMock()

        mock_mrd.read_obj_str.recv.side_effect = [
            _storage_v2.BidiReadObjectResponse(
                object_data_ranges=[
                    _storage_v2.ObjectRangeData(
                        checksummed_data=_storage_v2.ChecksummedData(
                            content=data, crc32c=crc32c_int
                        ),
                        range_end=True,
                        read_range=_storage_v2.ReadRange(
                            read_offset=0, read_length=18, read_id=456
                        ),
                    )
                ]
            ),
            _storage_v2.BidiReadObjectResponse(
                object_data_ranges=[
                    _storage_v2.ObjectRangeData(
                        checksummed_data=_storage_v2.ChecksummedData(
                            content=data[10:16],
                            crc32c=crc32c_checksum_for_data_slice,
                        ),
                        range_end=True,
                        read_range=_storage_v2.ReadRange(
                            read_offset=10, read_length=6, read_id=91011
                        ),
                    )
                ],
            ),
        ]

        # Act
        buffer = BytesIO()
        second_buffer = BytesIO()
        lock = asyncio.Lock()
        task1 = asyncio.create_task(mock_mrd.download_ranges([(0, 18, buffer)], lock))
        task2 = asyncio.create_task(
            mock_mrd.download_ranges([(10, 6, second_buffer)], lock)
        )
        await asyncio.gather(task1, task2)

        # Assert
        mock_mrd.read_obj_str.send.side_effect = [
            _storage_v2.BidiReadObjectRequest(
                read_ranges=[
                    _storage_v2.ReadRange(read_offset=0, read_length=18, read_id=456)
                ]
            ),
            _storage_v2.BidiReadObjectRequest(
                read_ranges=[
                    _storage_v2.ReadRange(read_offset=10, read_length=6, read_id=91011)
                ]
            ),
        ]
        assert buffer.getvalue() == data
        assert second_buffer.getvalue() == data[10:16]

    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    @pytest.mark.asyncio
    async def test_download_ranges(
        self, mock_grpc_client, mock_cls_async_read_object_stream, mock_random_int
    ):
        # Arrange
        data = b"these_are_18_chars"
        crc32c = Checksum(data).digest()
        crc32c_int = int.from_bytes(crc32c, "big")

        mock_mrd = await self._make_mock_mrd(
            mock_grpc_client, mock_cls_async_read_object_stream
        )
        mock_random_int.side_effect = [123, 456]  # for _func_id and read_id
        mock_mrd.read_obj_str.send = AsyncMock()
        mock_mrd.read_obj_str.recv = AsyncMock()
        mock_mrd.read_obj_str.recv.return_value = _storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                _storage_v2.ObjectRangeData(
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=data, crc32c=crc32c_int
                    ),
                    range_end=True,
                    read_range=_storage_v2.ReadRange(
                        read_offset=0, read_length=18, read_id=456
                    ),
                )
            ],
        )

        # Act
        buffer = BytesIO()
        await mock_mrd.download_ranges([(0, 18, buffer)])

        # Assert
        mock_mrd.read_obj_str.send.assert_called_once_with(
            _storage_v2.BidiReadObjectRequest(
                read_ranges=[
                    _storage_v2.ReadRange(read_offset=0, read_length=18, read_id=456)
                ]
            )
        )
        assert buffer.getvalue() == data

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

    @mock.patch("google.cloud.storage._experimental.asyncio._utils.google_crc32c")
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    def test_init_raises_if_crc32c_c_extension_is_missing(
        self, mock_grpc_client, mock_google_crc32c
    ):
        mock_google_crc32c.implementation = "python"

        with pytest.raises(exceptions.FailedPrecondition) as exc_info:
            AsyncMultiRangeDownloader(mock_grpc_client, "bucket", "object")

        assert "The google-crc32c package is not installed with C support" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_multi_range_downloader.Checksum"
    )
    @mock.patch(
        "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
    )
    async def test_download_ranges_raises_on_checksum_mismatch(
        self, mock_client, mock_checksum_class
    ):
        mock_stream = mock.AsyncMock(
            spec=async_read_object_stream._AsyncReadObjectStream
        )

        test_data = b"some-data"
        server_checksum = 12345
        mock_checksum_instance = mock_checksum_class.return_value
        mock_checksum_instance.digest.return_value = (54321).to_bytes(4, "big")

        mock_response = _storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                _storage_v2.ObjectRangeData(
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=test_data, crc32c=server_checksum
                    ),
                    read_range=_storage_v2.ReadRange(read_id=0),
                    range_end=True,
                )
            ]
        )

        mock_stream.recv.side_effect = [mock_response, None]

        mrd = AsyncMultiRangeDownloader(mock_client, "bucket", "object")
        mrd.read_obj_str = mock_stream
        mrd._is_stream_open = True

        with pytest.raises(DataCorruption) as exc_info:
            await mrd.download_ranges([(0, len(test_data), BytesIO())])

        assert "Checksum mismatch" in str(exc_info.value)
        mock_checksum_class.assert_called_once_with(test_data)
