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

from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud import _storage_v2


BUCKET = "test-bucket"
OBJECT = "test-object"
GENERATION = 123
WRITE_HANDLE = b"test-write-handle"
PERSISTED_SIZE = 456


@pytest.fixture
def mock_client():
    """Mock the async gRPC client."""
    return mock.AsyncMock()


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
def test_init(mock_write_object_stream, mock_client):
    """Test the constructor of AsyncAppendableObjectWriter."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)

    assert writer.client == mock_client
    assert writer.bucket_name == BUCKET
    assert writer.object_name == OBJECT
    assert writer.generation is None
    assert writer.write_handle is None
    assert not writer._is_stream_open
    assert writer.offset is None
    assert writer.persisted_size is None

    mock_write_object_stream.assert_called_once_with(
        client=mock_client,
        bucket_name=BUCKET,
        object_name=OBJECT,
        generation_number=None,
        write_handle=None,
    )
    assert writer.write_obj_stream == mock_write_object_stream.return_value


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
def test_init_with_optional_args(mock_write_object_stream, mock_client):
    """Test the constructor with optional arguments."""
    writer = AsyncAppendableObjectWriter(
        mock_client,
        BUCKET,
        OBJECT,
        generation=GENERATION,
        write_handle=WRITE_HANDLE,
    )

    assert writer.generation == GENERATION
    assert writer.write_handle == WRITE_HANDLE

    mock_write_object_stream.assert_called_once_with(
        client=mock_client,
        bucket_name=BUCKET,
        object_name=OBJECT,
        generation_number=GENERATION,
        write_handle=WRITE_HANDLE,
    )


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_state_lookup(mock_write_object_stream, mock_client):
    """Test state_lookup method."""
    # Arrange
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(persisted_size=PERSISTED_SIZE)
    )

    expected_request = _storage_v2.BidiWriteObjectRequest(state_lookup=True)

    # Act
    response = await writer.state_lookup()

    # Assert
    mock_stream.send.assert_awaited_once_with(expected_request)
    mock_stream.recv.assert_awaited_once()
    assert writer.persisted_size == PERSISTED_SIZE
    assert response == PERSISTED_SIZE


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_open_appendable_object_writer(mock_write_object_stream, mock_client):
    """Test the open method."""
    # Arrange
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    mock_stream = mock_write_object_stream.return_value
    mock_stream.open = mock.AsyncMock()
    mock_stream.send = mock.AsyncMock()
    mock_stream.recv = mock.AsyncMock()

    mock_state_response = mock.MagicMock()
    mock_state_response.persisted_size = 1024
    mock_stream.recv.return_value = mock_state_response

    mock_stream.generation_number = GENERATION
    mock_stream.write_handle = WRITE_HANDLE

    # Act
    await writer.open()

    # Assert
    mock_stream.open.assert_awaited_once()
    assert writer._is_stream_open
    assert writer.generation == GENERATION
    assert writer.write_handle == WRITE_HANDLE

    expected_request = _storage_v2.BidiWriteObjectRequest(state_lookup=True)
    mock_stream.send.assert_awaited_once_with(expected_request)
    mock_stream.recv.assert_awaited_once()
    assert writer.persisted_size == 1024


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_open_when_already_open_raises_error(
    mock_write_object_stream, mock_client
):
    """Test that opening an already open writer raises a ValueError."""
    # Arrange
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True  # Manually set to open

    # Act & Assert
    with pytest.raises(ValueError, match="Underlying bidi-gRPC stream is already open"):
        await writer.open()


@pytest.mark.asyncio
async def test_unimplemented_methods_raise_error(mock_client):
    """Test that all currently unimplemented methods raise NotImplementedError."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)

    with pytest.raises(NotImplementedError):
        await writer.append(b"data")

    with pytest.raises(NotImplementedError):
        await writer.append_from_string("data")

    with pytest.raises(NotImplementedError):
        await writer.append_from_stream(mock.Mock())

    with pytest.raises(NotImplementedError):
        await writer.append_from_file("file.txt")


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_flush(mock_write_object_stream, mock_client):
    """Test that flush sends the correct request and updates state."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(persisted_size=1024)
    )

    persisted_size = await writer.flush()

    expected_request = _storage_v2.BidiWriteObjectRequest(flush=True, state_lookup=True)
    mock_stream.send.assert_awaited_once_with(expected_request)
    mock_stream.recv.assert_awaited_once()
    assert writer.persisted_size == 1024
    assert writer.offset == 1024
    assert persisted_size == 1024


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_close_without_finalize(mock_write_object_stream, mock_client):
    """Test close without finalizing."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.offset = 1024
    mock_stream = mock_write_object_stream.return_value
    mock_stream.close = mock.AsyncMock()
    writer.finalize = mock.AsyncMock()

    await writer.close(finalize_on_close=False)

    writer.finalize.assert_not_awaited()
    mock_stream.close.assert_awaited_once()
    assert not writer._is_stream_open
    assert writer.offset is None


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_close_with_finalize(mock_write_object_stream, mock_client):
    """Test close with finalizing."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.offset = 1024
    mock_stream = mock_write_object_stream.return_value
    mock_stream.close = mock.AsyncMock()
    writer.finalize = mock.AsyncMock()

    await writer.close(finalize_on_close=True)

    writer.finalize.assert_awaited_once()
    mock_stream.close.assert_awaited_once()
    assert not writer._is_stream_open
    assert writer.offset is None


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_finalize(mock_write_object_stream, mock_client):
    """Test that finalize sends the correct request and updates state."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()
    mock_resource = _storage_v2.Object(name=OBJECT, bucket=BUCKET)
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(resource=mock_resource)
    )

    await writer.finalize()

    mock_stream.send.assert_awaited_once_with(
        _storage_v2.BidiWriteObjectRequest(finish_write=True)
    )
    mock_stream.recv.assert_awaited_once()
    assert writer.object_resource == mock_resource
