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

from google.cloud.storage._experimental.asyncio.async_write_object_stream import (
    _AsyncWriteObjectStream,
)
from google.cloud import _storage_v2

BUCKET = "my-bucket"
OBJECT = "my-object"
GENERATION = 12345
WRITE_HANDLE = b"test-handle"


@pytest.fixture
def mock_client():
    """Mock the async gRPC client."""
    mock_transport = mock.AsyncMock()
    mock_transport.bidi_write_object = mock.sentinel.bidi_write_object
    mock_transport._wrapped_methods = {
        mock.sentinel.bidi_write_object: mock.sentinel.wrapped_bidi_write_object
    }

    mock_gapic_client = mock.AsyncMock()
    mock_gapic_client._transport = mock_transport

    client = mock.AsyncMock()
    client._client = mock_gapic_client
    return client


def test_async_write_object_stream_init(mock_client):
    """Test the constructor of _AsyncWriteObjectStream."""
    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)

    assert stream.client == mock_client
    assert stream.bucket_name == BUCKET
    assert stream.object_name == OBJECT
    assert stream.generation_number is None
    assert stream.write_handle is None
    assert stream._full_bucket_name == f"projects/_/buckets/{BUCKET}"
    assert stream.rpc == mock.sentinel.wrapped_bidi_write_object
    assert stream.metadata == (
        ("x-goog-request-params", f"bucket=projects/_/buckets/{BUCKET}"),
    )
    assert stream.socket_like_rpc is None
    assert not stream._is_stream_open
    assert stream.first_bidi_write_req is None
    assert stream.persisted_size == 0
    assert stream.object_resource is None


def test_async_write_object_stream_init_with_generation_and_handle(mock_client):
    """Test the constructor with optional arguments."""
    generation = 12345
    write_handle = b"test-handle"
    stream = _AsyncWriteObjectStream(
        mock_client,
        BUCKET,
        OBJECT,
        generation_number=generation,
        write_handle=write_handle,
    )

    assert stream.generation_number == generation
    assert stream.write_handle == write_handle


def test_async_write_object_stream_init_raises_value_error():
    """Test that the constructor raises ValueError for missing arguments."""
    with pytest.raises(ValueError, match="client must be provided"):
        _AsyncWriteObjectStream(None, BUCKET, OBJECT)

    with pytest.raises(ValueError, match="bucket_name must be provided"):
        _AsyncWriteObjectStream(mock.Mock(), None, OBJECT)

    with pytest.raises(ValueError, match="object_name must be provided"):
        _AsyncWriteObjectStream(mock.Mock(), BUCKET, None)


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_for_new_object(mock_async_bidi_rpc, mock_client):
    """Test opening a stream for a new object."""
    # Arrange
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc
    socket_like_rpc.open = mock.AsyncMock()

    mock_response = mock.MagicMock(spec=_storage_v2.BidiWriteObjectResponse)
    mock_response.resource = mock.MagicMock(spec=_storage_v2.Object)
    mock_response.resource.generation = GENERATION
    mock_response.write_handle = WRITE_HANDLE
    socket_like_rpc.recv = mock.AsyncMock(return_value=mock_response)

    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)

    # Act
    await stream.open()

    # Assert
    assert stream._is_stream_open
    socket_like_rpc.open.assert_called_once()
    socket_like_rpc.recv.assert_called_once()
    assert stream.generation_number == GENERATION
    assert stream.write_handle == WRITE_HANDLE


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_for_existing_object(mock_async_bidi_rpc, mock_client):
    """Test opening a stream for an existing object."""
    # Arrange
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc
    socket_like_rpc.open = mock.AsyncMock()

    mock_response = mock.MagicMock(spec=_storage_v2.BidiWriteObjectResponse)
    mock_response.resource = mock.MagicMock(spec=_storage_v2.Object)
    mock_response.resource.generation = GENERATION
    mock_response.write_handle = WRITE_HANDLE
    socket_like_rpc.recv = mock.AsyncMock(return_value=mock_response)

    stream = _AsyncWriteObjectStream(
        mock_client, BUCKET, OBJECT, generation_number=GENERATION
    )

    # Act
    await stream.open()

    # Assert
    assert stream._is_stream_open
    socket_like_rpc.open.assert_called_once()
    socket_like_rpc.recv.assert_called_once()
    assert stream.generation_number == GENERATION
    assert stream.write_handle == WRITE_HANDLE


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_when_already_open_raises_error(mock_async_bidi_rpc, mock_client):
    """Test that opening an already open stream raises a ValueError."""
    # Arrange
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc
    socket_like_rpc.open = mock.AsyncMock()

    mock_response = mock.MagicMock(spec=_storage_v2.BidiWriteObjectResponse)
    mock_response.resource = mock.MagicMock(spec=_storage_v2.Object)
    mock_response.resource.generation = GENERATION
    mock_response.write_handle = WRITE_HANDLE
    socket_like_rpc.recv = mock.AsyncMock(return_value=mock_response)

    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
    await stream.open()

    # Act & Assert
    with pytest.raises(ValueError, match="Stream is already open"):
        await stream.open()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_raises_error_on_missing_object_resource(
    mock_async_bidi_rpc, mock_client
):
    """Test that open raises ValueError if object_resource is not in the response."""
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc

    mock_reponse = mock.AsyncMock()
    type(mock_reponse).resource = mock.PropertyMock(return_value=None)
    socket_like_rpc.recv.return_value = mock_reponse

    # Note: Don't use below code as unittest library automatically assigns an
    # `AsyncMock` object to an attribute, if not set.
    # socket_like_rpc.recv.return_value = mock.AsyncMock(
    #     return_value=_storage_v2.BidiWriteObjectResponse(resource=None)
    # )

    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
    with pytest.raises(
        ValueError, match="Failed to obtain object resource after opening the stream"
    ):
        await stream.open()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_raises_error_on_missing_generation(
    mock_async_bidi_rpc, mock_client
):
    """Test that open raises ValueError if generation is not in the response."""
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc

    # Configure the mock response object
    mock_response = mock.AsyncMock()
    type(mock_response.resource).generation = mock.PropertyMock(return_value=None)
    socket_like_rpc.recv.return_value = mock_response

    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
    with pytest.raises(
        ValueError, match="Failed to obtain object generation after opening the stream"
    ):
        await stream.open()
    # assert stream.generation_number is None


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_raises_error_on_missing_write_handle(
    mock_async_bidi_rpc, mock_client
):
    """Test that open raises ValueError if write_handle is not in the response."""
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc
    socket_like_rpc.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(
            resource=_storage_v2.Object(generation=GENERATION), write_handle=None
        )
    )
    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
    with pytest.raises(ValueError, match="Failed to obtain write_handle"):
        await stream.open()


@pytest.mark.asyncio
async def test_unimplemented_methods_raise_error(mock_client):
    """Test that unimplemented methods raise NotImplementedError."""
    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)

    with pytest.raises(NotImplementedError):
        await stream.close()

    with pytest.raises(NotImplementedError):
        await stream.send(_storage_v2.BidiWriteObjectRequest())

    with pytest.raises(NotImplementedError):
        await stream.recv()
