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

import unittest.mock as mock
from unittest.mock import AsyncMock, MagicMock
import pytest
import grpc


from google.cloud.storage.asyncio.async_write_object_stream import (
    _AsyncWriteObjectStream,
)
from google.cloud import _storage_v2

BUCKET = "my-bucket"
OBJECT = "my-object"
GENERATION = 12345
WRITE_HANDLE = b"test-handle"
FULL_BUCKET_PATH = f"projects/_/buckets/{BUCKET}"


@pytest.fixture
def mock_client():
    """Fixture to provide a mock gRPC client."""
    client = MagicMock()
    # Mocking transport internal structures
    mock_transport = MagicMock()
    mock_transport.bidi_write_object = mock.sentinel.bidi_write_object
    mock_transport._wrapped_methods = {
        mock.sentinel.bidi_write_object: mock.sentinel.wrapped_bidi_write_object
    }
    client._client._transport = mock_transport
    return client


class TestAsyncWriteObjectStream:
    """Test suite for AsyncWriteObjectStream."""

    # -------------------------------------------------------------------------
    # Initialization Tests
    # -------------------------------------------------------------------------

    def test_init_basic(self, mock_client):
        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        assert stream.bucket_name == BUCKET
        assert stream.object_name == OBJECT
        assert stream._full_bucket_name == FULL_BUCKET_PATH
        assert stream.metadata == (
            ("x-goog-request-params", f"bucket={FULL_BUCKET_PATH}"),
        )
        assert not stream.is_stream_open

    def test_init_raises_value_error(self, mock_client):
        with pytest.raises(ValueError, match="client must be provided"):
            _AsyncWriteObjectStream(None, BUCKET, OBJECT)
        with pytest.raises(ValueError, match="bucket_name must be provided"):
            _AsyncWriteObjectStream(mock_client, None, OBJECT)
        with pytest.raises(ValueError, match="object_name must be provided"):
            _AsyncWriteObjectStream(mock_client, BUCKET, None)

    # -------------------------------------------------------------------------
    # Open Stream Tests
    # -------------------------------------------------------------------------

    @mock.patch("google.cloud.storage.asyncio.async_write_object_stream.AsyncBidiRpc")
    @pytest.mark.asyncio
    async def test_open_new_object(self, mock_rpc_cls, mock_client):
        mock_rpc = mock_rpc_cls.return_value
        mock_rpc.open = AsyncMock()

        # We don't use spec here to avoid descriptor issues with nested protos
        mock_response = MagicMock()
        mock_response.persisted_size = 0
        mock_response.resource.generation = GENERATION
        mock_response.resource.size = 0
        mock_response.write_handle = WRITE_HANDLE
        mock_rpc.recv = AsyncMock(return_value=mock_response)

        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        await stream.open()

        # Check if BidiRpc was initialized with WriteObjectSpec
        call_args = mock_rpc_cls.call_args
        initial_request = call_args.kwargs["initial_request"]
        assert initial_request.write_object_spec is not None
        assert initial_request.write_object_spec.resource.name == OBJECT
        assert initial_request.write_object_spec.appendable

        assert stream.is_stream_open
        assert stream.write_handle == WRITE_HANDLE
        assert stream.generation_number == GENERATION

    @mock.patch("google.cloud.storage.asyncio.async_write_object_stream.AsyncBidiRpc")
    @pytest.mark.asyncio
    async def test_open_existing_object_with_token(self, mock_rpc_cls, mock_client):
        mock_rpc = mock_rpc_cls.return_value
        mock_rpc.open = AsyncMock()

        # Ensure resource is None so persisted_size logic doesn't get overwritten by child mocks
        mock_response = MagicMock()
        mock_response.persisted_size = 1024
        mock_response.resource = None
        mock_response.write_handle = WRITE_HANDLE
        mock_rpc.recv = AsyncMock(return_value=mock_response)

        stream = _AsyncWriteObjectStream(
            mock_client,
            BUCKET,
            OBJECT,
            generation_number=GENERATION,
            routing_token="token-123",
        )
        await stream.open()

        # Verify AppendObjectSpec attributes
        initial_request = mock_rpc_cls.call_args.kwargs["initial_request"]
        assert initial_request.append_object_spec is not None
        assert initial_request.append_object_spec.generation == GENERATION
        assert initial_request.append_object_spec.routing_token == "token-123"
        assert stream.persisted_size == 1024

    @mock.patch("google.cloud.storage.asyncio.async_write_object_stream.AsyncBidiRpc")
    @pytest.mark.asyncio
    async def test_open_metadata_merging(self, mock_rpc_cls, mock_client):
        mock_rpc = mock_rpc_cls.return_value
        mock_rpc.open = AsyncMock()
        mock_rpc.recv = AsyncMock(return_value=MagicMock(resource=None))

        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        extra_metadata = [("x-custom", "val"), ("x-goog-request-params", "extra=param")]

        await stream.open(metadata=extra_metadata)

        # Verify that metadata combined bucket and extra params
        passed_metadata = mock_rpc_cls.call_args.kwargs["metadata"]
        meta_dict = dict(passed_metadata)
        assert meta_dict["x-custom"] == "val"
        # Params should be comma separated
        params = meta_dict["x-goog-request-params"]
        assert f"bucket={FULL_BUCKET_PATH}" in params
        assert "extra=param" in params

    @pytest.mark.asyncio
    async def test_open_already_open_raises(self, mock_client):
        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        stream._is_stream_open = True
        with pytest.raises(ValueError, match="already open"):
            await stream.open()

    # -------------------------------------------------------------------------
    # Send & Recv & Close Tests
    # -------------------------------------------------------------------------

    @mock.patch("google.cloud.storage.asyncio.async_write_object_stream.AsyncBidiRpc")
    @pytest.mark.asyncio
    async def test_send_and_recv_logic(self, mock_rpc_cls, mock_client):
        # Setup open stream
        mock_rpc = mock_rpc_cls.return_value
        mock_rpc.open = AsyncMock()
        mock_rpc.send = AsyncMock()  # Crucial: Must be AsyncMock
        mock_rpc.recv = AsyncMock(return_value=MagicMock(resource=None))

        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        await stream.open()

        # Test Send
        req = _storage_v2.BidiWriteObjectRequest(write_offset=0)
        await stream.send(req)
        mock_rpc.send.assert_awaited_with(req)

        # Test Recv with state update
        mock_response = MagicMock()
        mock_response.persisted_size = 5000
        mock_response.write_handle = b"new-handle"
        mock_response.resource = None
        mock_rpc.recv.return_value = mock_response

        res = await stream.recv()
        assert res.persisted_size == 5000
        assert stream.persisted_size == 5000
        assert stream.write_handle == b"new-handle"

    @pytest.mark.asyncio
    async def test_close_success(self, mock_client):
        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        stream._is_stream_open = True
        stream.socket_like_rpc = AsyncMock()

        stream.socket_like_rpc.send = AsyncMock()
        first_resp = _storage_v2.BidiWriteObjectResponse(persisted_size=100)
        stream.socket_like_rpc.recv = AsyncMock(side_effect=[first_resp, grpc.aio.EOF])
        stream.socket_like_rpc.close = AsyncMock()

        await stream.close()
        stream.socket_like_rpc.close.assert_awaited_once()
        assert not stream.is_stream_open
        assert stream.persisted_size == 100

    @pytest.mark.asyncio
    async def test_close_with_persisted_size_then_eof(self, mock_client):
        """Test close when first recv has persisted_size, second is EOF."""
        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        stream._is_stream_open = True
        stream.socket_like_rpc = AsyncMock()

        # First response has persisted_size (NOT EOF, intermediate)
        persisted_resp = _storage_v2.BidiWriteObjectResponse(persisted_size=500)
        # Second response is EOF (None)
        eof_resp = grpc.aio.EOF

        stream.socket_like_rpc.send = AsyncMock()
        stream.socket_like_rpc.recv = AsyncMock(side_effect=[persisted_resp, eof_resp])
        stream.socket_like_rpc.close = AsyncMock()

        await stream.close()

        # Verify two recv calls: first has persisted_size (NOT EOF), so read second (EOF)
        assert stream.socket_like_rpc.recv.await_count == 2
        assert stream.persisted_size == 500
        assert not stream.is_stream_open

    @pytest.mark.asyncio
    async def test_close_with_grpc_aio_eof_response(self, mock_client):
        """Test close when first recv is grpc.aio.EOF sentinel."""
        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        stream._is_stream_open = True
        stream.socket_like_rpc = AsyncMock()

        # First recv returns grpc.aio.EOF (explicit sentinel from finalize)
        stream.socket_like_rpc.send = AsyncMock()
        stream.socket_like_rpc.recv = AsyncMock(return_value=grpc.aio.EOF)
        stream.socket_like_rpc.close = AsyncMock()

        await stream.close()

        # Verify only one recv call (grpc.aio.EOF=EOF, so don't read second)
        assert stream.socket_like_rpc.recv.await_count == 1
        assert not stream.is_stream_open

    @pytest.mark.asyncio
    async def test_methods_require_open_raises(self, mock_client):
        stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)
        with pytest.raises(ValueError, match="Stream is not open"):
            await stream.send(MagicMock())
        with pytest.raises(ValueError, match="Stream is not open"):
            await stream.recv()
        with pytest.raises(ValueError, match="Stream is not open"):
            await stream.close()
