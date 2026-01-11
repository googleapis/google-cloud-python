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

from io import BytesIO
import pytest
from unittest import mock

from google_crc32c import Checksum

from google.api_core import exceptions
from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    _MAX_CHUNK_SIZE_BYTES,
    _DEFAULT_FLUSH_INTERVAL_BYTES,
)
from google.cloud import _storage_v2


BUCKET = "test-bucket"
OBJECT = "test-object"
GENERATION = 123
WRITE_HANDLE = b"test-write-handle"
PERSISTED_SIZE = 456
EIGHT_MIB = 8 * 1024 * 1024


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
    assert writer.bytes_appended_since_last_flush == 0

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
    assert writer.bytes_appended_since_last_flush == 0

    mock_write_object_stream.assert_called_once_with(
        client=mock_client,
        bucket_name=BUCKET,
        object_name=OBJECT,
        generation_number=GENERATION,
        write_handle=WRITE_HANDLE,
    )


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
def test_init_with_writer_options(mock_write_object_stream, mock_client):
    """Test the constructor with optional arguments."""
    writer = AsyncAppendableObjectWriter(
        mock_client,
        BUCKET,
        OBJECT,
        writer_options={"FLUSH_INTERVAL_BYTES": EIGHT_MIB},
    )

    assert writer.flush_interval == EIGHT_MIB
    assert writer.bytes_appended_since_last_flush == 0

    mock_write_object_stream.assert_called_once_with(
        client=mock_client,
        bucket_name=BUCKET,
        object_name=OBJECT,
        generation_number=None,
        write_handle=None,
    )


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
def test_init_with_flush_interval_less_than_chunk_size_raises_error(mock_client):
    """Test that an OutOfRange error is raised if flush_interval is less than the chunk size."""

    with pytest.raises(exceptions.OutOfRange):
        AsyncAppendableObjectWriter(
            mock_client,
            BUCKET,
            OBJECT,
            writer_options={"FLUSH_INTERVAL_BYTES": _MAX_CHUNK_SIZE_BYTES - 1},
        )


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
def test_init_with_flush_interval_not_multiple_of_chunk_size_raises_error(mock_client):
    """Test that an OutOfRange error is raised if flush_interval is not a multiple of the chunk size."""

    with pytest.raises(exceptions.OutOfRange):
        AsyncAppendableObjectWriter(
            mock_client,
            BUCKET,
            OBJECT,
            writer_options={"FLUSH_INTERVAL_BYTES": _MAX_CHUNK_SIZE_BYTES + 1},
        )


@mock.patch("google.cloud.storage._experimental.asyncio._utils.google_crc32c")
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
def test_init_raises_if_crc32c_c_extension_is_missing(
    mock_grpc_client, mock_google_crc32c
):
    mock_google_crc32c.implementation = "python"

    with pytest.raises(exceptions.FailedPrecondition) as exc_info:
        AsyncAppendableObjectWriter(mock_grpc_client, "bucket", "object")

    assert "The google-crc32c package is not installed with C support" in str(
        exc_info.value
    )


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_state_lookup(mock_write_object_stream, mock_client):
    """Test state_lookup method."""
    # Arrange
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
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
async def test_state_lookup_without_open_raises_value_error(mock_client):
    """Test that state_lookup raises an error if the stream is not open."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    with pytest.raises(
        ValueError,
        match="Stream is not open. Call open\\(\\) before state_lookup\\(\\).",
    ):
        await writer.state_lookup()


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

    mock_stream.generation_number = GENERATION
    mock_stream.write_handle = WRITE_HANDLE
    mock_stream.persisted_size = 0

    # Act
    await writer.open()

    # Assert
    mock_stream.open.assert_awaited_once()
    assert writer._is_stream_open
    assert writer.generation == GENERATION
    assert writer.write_handle == WRITE_HANDLE
    assert writer.persisted_size == 0


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_open_appendable_object_writer_existing_object(
    mock_write_object_stream, mock_client
):
    """Test the open method."""
    # Arrange
    writer = AsyncAppendableObjectWriter(
        mock_client, BUCKET, OBJECT, generation=GENERATION
    )
    mock_stream = mock_write_object_stream.return_value
    mock_stream.open = mock.AsyncMock()

    mock_stream.generation_number = GENERATION
    mock_stream.write_handle = WRITE_HANDLE
    mock_stream.persisted_size = PERSISTED_SIZE

    # Act
    await writer.open()

    # Assert
    mock_stream.open.assert_awaited_once()
    assert writer._is_stream_open
    assert writer.generation == GENERATION
    assert writer.write_handle == WRITE_HANDLE
    assert writer.persisted_size == PERSISTED_SIZE


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
        await writer.append_from_string("data")

    with pytest.raises(NotImplementedError):
        await writer.append_from_stream(mock.Mock())


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_flush(mock_write_object_stream, mock_client):
    """Test that flush sends the correct request and updates state."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
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
async def test_flush_without_open_raises_value_error(mock_client):
    """Test that flush raises an error if the stream is not open."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    with pytest.raises(
        ValueError, match="Stream is not open. Call open\\(\\) before flush\\(\\)."
    ):
        await writer.flush()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_simple_flush(mock_write_object_stream, mock_client):
    """Test that flush sends the correct request and updates state."""
    # Arrange
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()

    # Act
    await writer.simple_flush()

    # Assert
    mock_stream.send.assert_awaited_once_with(
        _storage_v2.BidiWriteObjectRequest(flush=True)
    )


@pytest.mark.asyncio
async def test_simple_flush_without_open_raises_value_error(mock_client):
    """Test that flush raises an error if the stream is not open."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    with pytest.raises(
        ValueError,
        match="Stream is not open. Call open\\(\\) before simple_flush\\(\\).",
    ):
        await writer.simple_flush()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_close(mock_write_object_stream, mock_client):
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.offset = 1024
    writer.persisted_size = 1024
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(persisted_size=1024)
    )
    mock_stream.close = mock.AsyncMock()
    writer.finalize = mock.AsyncMock()

    persisted_size = await writer.close()

    writer.finalize.assert_not_awaited()
    mock_stream.close.assert_awaited_once()
    assert writer.offset is None
    assert persisted_size == 1024
    assert not writer._is_stream_open


@pytest.mark.asyncio
async def test_close_without_open_raises_value_error(mock_client):
    """Test that close raises an error if the stream is not open."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    with pytest.raises(
        ValueError, match="Stream is not open. Call open\\(\\) before close\\(\\)."
    ):
        await writer.close()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_finalize_on_close(mock_write_object_stream, mock_client):
    """Test close with finalizing."""
    # Arrange
    mock_resource = _storage_v2.Object(name=OBJECT, bucket=BUCKET, size=2048)
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.offset = 1024
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(resource=mock_resource)
    )
    mock_stream.close = mock.AsyncMock()

    # Act
    result = await writer.close(finalize_on_close=True)

    # Assert
    mock_stream.close.assert_awaited_once()
    assert not writer._is_stream_open
    assert writer.offset is None
    assert writer.object_resource == mock_resource
    assert writer.persisted_size == 2048
    assert result == mock_resource


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_finalize(mock_write_object_stream, mock_client):
    """Test that finalize sends the correct request and updates state."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    mock_resource = _storage_v2.Object(name=OBJECT, bucket=BUCKET, size=123)
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(resource=mock_resource)
    )
    mock_stream.close = mock.AsyncMock()

    gcs_object = await writer.finalize()

    mock_stream.send.assert_awaited_once_with(
        _storage_v2.BidiWriteObjectRequest(finish_write=True)
    )
    mock_stream.recv.assert_awaited_once()
    mock_stream.close.assert_awaited_once()
    assert writer.object_resource == mock_resource
    assert writer.persisted_size == 123
    assert gcs_object == mock_resource
    assert writer._is_stream_open is False
    assert writer.offset is None


@pytest.mark.asyncio
async def test_finalize_without_open_raises_value_error(mock_client):
    """Test that finalize raises an error if the stream is not open."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    with pytest.raises(
        ValueError, match="Stream is not open. Call open\\(\\) before finalize\\(\\)."
    ):
        await writer.finalize()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_append_raises_error_if_not_open(mock_write_object_stream, mock_client):
    """Test that append raises an error if the stream is not open."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    with pytest.raises(
        ValueError, match="Stream is not open. Call open\\(\\) before append\\(\\)."
    ):
        await writer.append(b"some data")


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_append_with_empty_data(mock_write_object_stream, mock_client):
    """Test that append does nothing if data is empty."""
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()

    await writer.append(b"")

    mock_stream.send.assert_not_awaited()


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_append_sends_data_in_chunks(mock_write_object_stream, mock_client):
    """Test that append sends data in chunks and updates offset."""
    from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
        _MAX_CHUNK_SIZE_BYTES,
    )

    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.persisted_size = 100
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()

    data = b"a" * (_MAX_CHUNK_SIZE_BYTES + 1)
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(
            persisted_size=100 + len(data)
        )
    )

    await writer.append(data)

    assert mock_stream.send.await_count == 2
    first_request = mock_stream.send.await_args_list[0].args[0]
    second_request = mock_stream.send.await_args_list[1].args[0]

    # First chunk
    assert first_request.write_offset == 100
    assert len(first_request.checksummed_data.content) == _MAX_CHUNK_SIZE_BYTES
    assert first_request.checksummed_data.crc32c == int.from_bytes(
        Checksum(data[:_MAX_CHUNK_SIZE_BYTES]).digest(), byteorder="big"
    )
    assert not first_request.flush
    assert not first_request.state_lookup

    # Second chunk (last chunk)
    assert second_request.write_offset == 100 + _MAX_CHUNK_SIZE_BYTES
    assert len(second_request.checksummed_data.content) == 1
    assert second_request.checksummed_data.crc32c == int.from_bytes(
        Checksum(data[_MAX_CHUNK_SIZE_BYTES:]).digest(), byteorder="big"
    )
    assert second_request.flush
    assert second_request.state_lookup

    assert writer.offset == 100 + len(data)


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_append_flushes_when_buffer_is_full(
    mock_write_object_stream, mock_client
):
    """Test that append flushes the stream when the buffer size is reached."""

    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.persisted_size = 0
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()
    mock_stream.recv = mock.AsyncMock()

    data = b"a" * _DEFAULT_FLUSH_INTERVAL_BYTES
    await writer.append(data)

    num_chunks = _DEFAULT_FLUSH_INTERVAL_BYTES // _MAX_CHUNK_SIZE_BYTES
    assert mock_stream.send.await_count == num_chunks

    # All but the last request should not have flush or state_lookup set.
    for i in range(num_chunks - 1):
        request = mock_stream.send.await_args_list[i].args[0]
        assert not request.flush
        assert not request.state_lookup

    # The last request should have flush and state_lookup set.
    last_request = mock_stream.send.await_args_list[-1].args[0]
    assert last_request.flush
    assert last_request.state_lookup
    assert writer.bytes_appended_since_last_flush == 0


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_append_handles_large_data(mock_write_object_stream, mock_client):
    """Test that append handles data larger than the buffer size."""

    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.persisted_size = 0
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()
    mock_stream.recv = mock.AsyncMock()

    data = b"a" * (_DEFAULT_FLUSH_INTERVAL_BYTES * 2 + 1)
    await writer.append(data)

    flushed_requests = [
        call.args[0] for call in mock_stream.send.await_args_list if call.args[0].flush
    ]
    assert len(flushed_requests) == 3

    last_request = mock_stream.send.await_args_list[-1].args[0]
    assert last_request.state_lookup


@pytest.mark.asyncio
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_appendable_object_writer._AsyncWriteObjectStream"
)
async def test_append_data_two_times(mock_write_object_stream, mock_client):
    """Test that append sends data correctly when called multiple times."""
    from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
        _MAX_CHUNK_SIZE_BYTES,
    )

    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.persisted_size = 0
    mock_stream = mock_write_object_stream.return_value
    mock_stream.send = mock.AsyncMock()

    data1 = b"a" * (_MAX_CHUNK_SIZE_BYTES + 10)
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(
            persisted_size= len(data1)
        )
    )
    await writer.append(data1)

    assert mock_stream.send.await_count == 2
    last_request_data1 = mock_stream.send.await_args_list[-1].args[0]
    assert last_request_data1.flush
    assert last_request_data1.state_lookup

    data2 = b"b" * (_MAX_CHUNK_SIZE_BYTES + 20)
    mock_stream.recv = mock.AsyncMock(
        return_value=_storage_v2.BidiWriteObjectResponse(
            persisted_size= len(data2) + len(data1)
        )
    )
    await writer.append(data2)

    assert mock_stream.send.await_count == 4
    last_request_data2 = mock_stream.send.await_args_list[-1].args[0]
    assert last_request_data2.flush
    assert last_request_data2.state_lookup

    total_data_length = len(data1) + len(data2)
    assert writer.offset == total_data_length


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "file_size, block_size",
    [
        (10, 4 * 1024),
        (0, _DEFAULT_FLUSH_INTERVAL_BYTES),
        (20 * 1024 * 1024, _DEFAULT_FLUSH_INTERVAL_BYTES),
        (16 * 1024 * 1024, _DEFAULT_FLUSH_INTERVAL_BYTES),
    ],
)
async def test_append_from_file(file_size, block_size, mock_client):
    # arrange
    fp = BytesIO(b"a" * file_size)
    writer = AsyncAppendableObjectWriter(mock_client, BUCKET, OBJECT)
    writer._is_stream_open = True
    writer.append = mock.AsyncMock()

    # act
    await writer.append_from_file(fp, block_size=block_size)

    # assert
    exepected_calls = (
        file_size // block_size
        if file_size % block_size == 0
        else file_size // block_size + 1
    )
    assert writer.append.await_count == exepected_calls
