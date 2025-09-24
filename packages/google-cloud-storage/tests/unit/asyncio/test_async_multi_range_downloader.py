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

from google.cloud.storage._experimental.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)
from io import BytesIO


_TEST_BUCKET_NAME = "test-bucket"
_TEST_OBJECT_NAME = "test-object"
_TEST_GENERATION_NUMBER = 123456789
_TEST_READ_HANDLE = b"test-handle"


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
)
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
@pytest.mark.asyncio
async def test_create_mrd(mock_async_grpc_client, async_read_object_stream):
    # Arrange
    mock_stream_instance = async_read_object_stream.return_value
    mock_stream_instance.open = AsyncMock()
    mock_stream_instance.generation_number = _TEST_GENERATION_NUMBER
    mock_stream_instance.read_handle = _TEST_READ_HANDLE

    # act
    mrd = await AsyncMultiRangeDownloader.create_mrd(
        mock_async_grpc_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
    )

    # Assert
    async_read_object_stream.assert_called_once_with(
        client=mock_async_grpc_client,
        bucket_name=_TEST_BUCKET_NAME,
        object_name=_TEST_OBJECT_NAME,
        generation_number=None,
        read_handle=None,
    )
    mock_stream_instance.open.assert_called_once()

    assert mrd.client == mock_async_grpc_client
    assert mrd.bucket_name == _TEST_BUCKET_NAME
    assert mrd.object_name == _TEST_OBJECT_NAME
    assert mrd.generation_number == _TEST_GENERATION_NUMBER
    assert mrd.read_handle == _TEST_READ_HANDLE
    assert mrd.read_obj_str is mock_stream_instance


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
@pytest.mark.asyncio
async def test_download_ranges(mock_async_grpc_client):
    """Test that download_ranges() raises NotImplementedError."""
    mrd = AsyncMultiRangeDownloader(
        mock_async_grpc_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
    )

    with pytest.raises(NotImplementedError):
        await mrd.download_ranges([(0, 100, BytesIO())])
