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
from google.cloud.storage._experimental.asyncio.async_write_object_stream import (
    _AsyncWriteObjectStream,
)
from google.cloud import _storage_v2

BUCKET = "my-bucket"
OBJECT = "my-object"
GENERATION = 12345
WRITE_HANDLE_BYTES = b"test-handle"
NEW_WRITE_HANDLE_BYTES = b"new-test-handle"
WRITE_HANDLE_PROTO = _storage_v2.BidiWriteHandle(handle=WRITE_HANDLE_BYTES)
NEW_WRITE_HANDLE_PROTO = _storage_v2.BidiWriteHandle(handle=NEW_WRITE_HANDLE_BYTES)


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


async def instantiate_write_obj_stream(mock_client, mock_cls_async_bidi_rpc, open=True):
    """Helper to create an instance of _AsyncWriteObjectStream and open it by default."""
    socket_like_rpc = AsyncMock()
    mock_cls_async_bidi_rpc.return_value = socket_like_rpc
    socket_like_rpc.open = AsyncMock()
    socket_like_rpc.send = AsyncMock()
    socket_like_rpc.close = AsyncMock()

    mock_response = mock.MagicMock(spec=_storage_v2.BidiWriteObjectResponse)
    mock_response.resource = mock.MagicMock(spec=_storage_v2.Object)
    mock_response.resource.generation = GENERATION
    mock_response.resource.size = 0
    mock_response.write_handle = WRITE_HANDLE_PROTO
    socket_like_rpc.recv = AsyncMock(return_value=mock_response)

    write_obj_stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)

    if open:
        await write_obj_stream.open()

    return write_obj_stream


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
    stream = _AsyncWriteObjectStream(
        mock_client,
        BUCKET,
        OBJECT,
        generation_number=GENERATION,
        write_handle=WRITE_HANDLE_PROTO,
    )

    assert stream.generation_number == GENERATION
    assert stream.write_handle == WRITE_HANDLE_PROTO


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
    mock_response.resource.size = 0
    mock_response.write_handle = WRITE_HANDLE_PROTO
    socket_like_rpc.recv = mock.AsyncMock(return_value=mock_response)

    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)

    # Act
    await stream.open()

    # Assert
    assert stream._is_stream_open
    socket_like_rpc.open.assert_called_once()
    socket_like_rpc.recv.assert_called_once()
    assert stream.generation_number == GENERATION
    assert stream.write_handle == WRITE_HANDLE_PROTO
    assert stream.persisted_size == 0


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_for_new_object_with_generation_zero(
    mock_async_bidi_rpc, mock_client
):
    """Test opening a stream for a new object."""
    # Arrange
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc
    socket_like_rpc.open = mock.AsyncMock()

    mock_response = mock.MagicMock(spec=_storage_v2.BidiWriteObjectResponse)
    mock_response.resource = mock.MagicMock(spec=_storage_v2.Object)
    mock_response.resource.generation = GENERATION
    mock_response.resource.size = 0
    mock_response.write_handle = WRITE_HANDLE_PROTO
    socket_like_rpc.recv = mock.AsyncMock(return_value=mock_response)

    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT, generation_number=0)

    # Act
    await stream.open()

    # Assert
    mock_async_bidi_rpc.assert_called_once()
    _, call_kwargs = mock_async_bidi_rpc.call_args
    initial_request = call_kwargs["initial_request"]
    assert initial_request.write_object_spec.if_generation_match == 0
    assert stream._is_stream_open
    socket_like_rpc.open.assert_called_once()
    socket_like_rpc.recv.assert_called_once()
    assert stream.generation_number == GENERATION
    assert stream.write_handle == WRITE_HANDLE_PROTO
    assert stream.persisted_size == 0


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
    mock_response.resource.size = 1024
    mock_response.resource.generation = GENERATION
    mock_response.write_handle = WRITE_HANDLE_PROTO
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
    assert stream.write_handle == WRITE_HANDLE_PROTO
    assert stream.persisted_size == 1024


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
    mock_response.resource.size = 0
    mock_response.write_handle = WRITE_HANDLE_PROTO
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
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_raises_error_on_missing_persisted_size_with_write_handle(
    mock_async_bidi_rpc, mock_client
):
    """Test that open raises ValueError if persisted_size is None when opened via write_handle."""
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc

    #
    mock_response = mock.MagicMock(spec=_storage_v2.BidiWriteObjectResponse)
    mock_response.persisted_size = None  # This is the key part of the test
    mock_response.write_handle = (
        WRITE_HANDLE_PROTO  # Ensure write_handle is present to avoid that error
    )
    socket_like_rpc.recv.return_value = mock_response

    # ACT
    stream = _AsyncWriteObjectStream(
        mock_client,
        BUCKET,
        OBJECT,
        write_handle=WRITE_HANDLE_PROTO,
        generation_number=GENERATION,
    )

    with pytest.raises(
        ValueError,
        match="Failed to obtain persisted_size after opening the stream via write_handle",
    ):
        await stream.open()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_close(mock_cls_async_bidi_rpc, mock_client):
    """Test that close successfully closes the stream."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=True
    )
    write_obj_stream.requests_done = AsyncMock()

    # Act
    await write_obj_stream.close()

    # Assert
    write_obj_stream.requests_done.assert_called_once()
    write_obj_stream.socket_like_rpc.close.assert_called_once()
    assert not write_obj_stream.is_stream_open


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_close_without_open_should_raise_error(
    mock_cls_async_bidi_rpc, mock_client
):
    """Test that closing a stream that is not open raises a ValueError."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=False
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Stream is not open"):
        await write_obj_stream.close()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_send(mock_cls_async_bidi_rpc, mock_client):
    """Test that send calls the underlying rpc's send method."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=True
    )

    # Act
    bidi_write_object_request = _storage_v2.BidiWriteObjectRequest()
    await write_obj_stream.send(bidi_write_object_request)

    # Assert
    write_obj_stream.socket_like_rpc.send.assert_called_once_with(
        bidi_write_object_request
    )


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_send_without_open_should_raise_error(
    mock_cls_async_bidi_rpc, mock_client
):
    """Test that sending on a stream that is not open raises a ValueError."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=False
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Stream is not open"):
        await write_obj_stream.send(_storage_v2.BidiWriteObjectRequest())


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_recv(mock_cls_async_bidi_rpc, mock_client):
    """Test that recv calls the underlying rpc's recv method."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=True
    )
    bidi_write_object_response = _storage_v2.BidiWriteObjectResponse()
    write_obj_stream.socket_like_rpc.recv = AsyncMock(
        return_value=bidi_write_object_response
    )

    # Act
    response = await write_obj_stream.recv()

    # Assert
    write_obj_stream.socket_like_rpc.recv.assert_called_once()
    assert response == bidi_write_object_response


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_recv_without_open_should_raise_error(
    mock_cls_async_bidi_rpc, mock_client
):
    """Test that receiving on a stream that is not open raises a ValueError."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=False
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Stream is not open"):
        await write_obj_stream.recv()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_requests_done(mock_cls_async_bidi_rpc, mock_client):
    """Test that requests_done signals the end of requests."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=True
    )
    write_obj_stream.socket_like_rpc.send = AsyncMock()
    write_obj_stream.socket_like_rpc.recv = AsyncMock()

    # Act
    await write_obj_stream.requests_done()

    # Assert
    write_obj_stream.socket_like_rpc.send.assert_called_once_with(None)
    write_obj_stream.socket_like_rpc.recv.assert_called_once()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_open_for_existing_object_with_none_size(
    mock_async_bidi_rpc, mock_client
):
    """Test opening a stream for an existing object where size is None."""
    # Arrange
    socket_like_rpc = mock.AsyncMock()
    mock_async_bidi_rpc.return_value = socket_like_rpc
    socket_like_rpc.open = mock.AsyncMock()

    mock_response = mock.MagicMock(spec=_storage_v2.BidiWriteObjectResponse)
    mock_response.resource = mock.MagicMock(spec=_storage_v2.Object)
    mock_response.resource.size = None
    mock_response.resource.generation = GENERATION
    mock_response.write_handle = WRITE_HANDLE_PROTO
    socket_like_rpc.recv = mock.AsyncMock(return_value=mock_response)

    stream = _AsyncWriteObjectStream(
        mock_client, BUCKET, OBJECT, generation_number=GENERATION
    )

    # Act
    await stream.open()

    # Assert
    assert stream.persisted_size == 0


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_recv_updates_write_handle(mock_cls_async_bidi_rpc, mock_client):
    """Test that recv updates the write_handle if present in the response."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=True
    )

    assert write_obj_stream.write_handle == WRITE_HANDLE_PROTO  # Initial handle

    # GCS can periodicallly update write handle in their responses.
    bidi_write_object_response = _storage_v2.BidiWriteObjectResponse(
        write_handle=NEW_WRITE_HANDLE_PROTO
    )
    write_obj_stream.socket_like_rpc.recv = AsyncMock(
        return_value=bidi_write_object_response
    )

    # Act
    response = await write_obj_stream.recv()

    # Assert
    write_obj_stream.socket_like_rpc.recv.assert_called_once()
    assert response == bidi_write_object_response
    # asserts that new write handle has been updated.
    assert write_obj_stream.write_handle == NEW_WRITE_HANDLE_PROTO


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_write_object_stream.AsyncBidiRpc"
)
async def test_requests_done_updates_write_handle(mock_cls_async_bidi_rpc, mock_client):
    """Test that requests_done updates the write_handle if present in the response."""
    # Arrange
    write_obj_stream = await instantiate_write_obj_stream(
        mock_client, mock_cls_async_bidi_rpc, open=True
    )
    assert write_obj_stream.write_handle == WRITE_HANDLE_PROTO  # Initial handle

    # new_write_handle = b"new-test-handle"
    bidi_write_object_response = _storage_v2.BidiWriteObjectResponse(
        write_handle=NEW_WRITE_HANDLE_PROTO
    )
    write_obj_stream.socket_like_rpc.send = AsyncMock()
    write_obj_stream.socket_like_rpc.recv = AsyncMock(
        return_value=bidi_write_object_response
    )

    # Act
    await write_obj_stream.requests_done()

    # Assert
    write_obj_stream.socket_like_rpc.send.assert_called_once_with(None)
    write_obj_stream.socket_like_rpc.recv.assert_called_once()
    assert write_obj_stream.write_handle == NEW_WRITE_HANDLE_PROTO
