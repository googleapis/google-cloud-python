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

from google.cloud.storage._experimental.asyncio.async_read_object_stream import (
    _AsyncReadObjectStream,
)

_TEST_BUCKET_NAME = "test-bucket"
_TEST_OBJECT_NAME = "test-object"
_TEST_GENERATION_NUMBER = 12345
_TEST_READ_HANDLE = b"test-read-handle"


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_read_object_stream.AsyncBidiRpc"
)
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
def test_init_with_bucket_object_generation(mock_client, mock_async_bidi_rpc):
    mock_client._client._transport.bidi_read_object = "bidi_read_object_rpc"
    mock_client._client._transport._wrapped_methods = {
        "bidi_read_object_rpc": mock.sentinel.A
    }
    full_bucket_name = f"projects/_/buckets/{_TEST_BUCKET_NAME}"
    first_bidi_read_req = _storage_v2.BidiReadObjectRequest(
        read_object_spec=_storage_v2.BidiReadObjectSpec(
            bucket=full_bucket_name, object=_TEST_OBJECT_NAME
        ),
    )

    read_obj_stream = _AsyncReadObjectStream(
        client=mock_client,
        bucket_name=_TEST_BUCKET_NAME,
        object_name=_TEST_OBJECT_NAME,
        generation_number=_TEST_GENERATION_NUMBER,
    )

    mock_async_bidi_rpc.assert_called_once_with(
        mock.sentinel.A,
        initial_request=first_bidi_read_req,
        metadata=(("x-goog-request-params", f"bucket={full_bucket_name}"),),
    )
    assert read_obj_stream.socket_like_rpc is mock_async_bidi_rpc.return_value


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
@pytest.mark.asyncio
async def test_open(mock_client):
    # arrange
    read_obj_stream = _AsyncReadObjectStream(
        client=mock_client,
        bucket_name=_TEST_BUCKET_NAME,
        object_name=_TEST_OBJECT_NAME,
    )
    read_obj_stream.socket_like_rpc.open = AsyncMock()

    recv_response = mock.MagicMock(spec=_storage_v2.BidiReadObjectResponse)
    recv_response.metadata = mock.MagicMock(spec=_storage_v2.Object)
    recv_response.metadata.generation = _TEST_GENERATION_NUMBER
    recv_response.read_handle = _TEST_READ_HANDLE
    read_obj_stream.socket_like_rpc.recv = AsyncMock(return_value=recv_response)

    # act
    await read_obj_stream.open()

    # assert
    read_obj_stream.socket_like_rpc.open.assert_called_once()
    read_obj_stream.socket_like_rpc.recv.assert_called_once()

    assert read_obj_stream.generation_number == _TEST_GENERATION_NUMBER
    assert read_obj_stream.read_handle == _TEST_READ_HANDLE


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
@pytest.mark.asyncio
async def test_close(mock_client):
    # arrange
    read_obj_stream = _AsyncReadObjectStream(
        client=mock_client,
        bucket_name=_TEST_BUCKET_NAME,
        object_name=_TEST_OBJECT_NAME,
    )
    read_obj_stream.socket_like_rpc.close = AsyncMock()

    # act
    await read_obj_stream.close()

    # assert
    read_obj_stream.socket_like_rpc.close.assert_called_once()


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
@pytest.mark.asyncio
async def test_send(mock_client):
    # arrange
    read_obj_stream = _AsyncReadObjectStream(
        client=mock_client,
        bucket_name=_TEST_BUCKET_NAME,
        object_name=_TEST_OBJECT_NAME,
    )
    read_obj_stream.socket_like_rpc.send = AsyncMock()

    # act
    bidi_read_object_request = _storage_v2.BidiReadObjectRequest()
    await read_obj_stream.send(bidi_read_object_request)

    # assert
    read_obj_stream.socket_like_rpc.send.assert_called_once_with(
        bidi_read_object_request
    )


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
@pytest.mark.asyncio
async def test_recv(mock_client):
    # arrange
    read_obj_stream = _AsyncReadObjectStream(
        client=mock_client,
        bucket_name=_TEST_BUCKET_NAME,
        object_name=_TEST_OBJECT_NAME,
    )
    bidi_read_object_response = _storage_v2.BidiReadObjectResponse()
    read_obj_stream.socket_like_rpc.recv = AsyncMock(
        return_value=bidi_read_object_response
    )

    # act
    response = await read_obj_stream.recv()

    # assert
    read_obj_stream.socket_like_rpc.recv.assert_called_once()
    assert response == bidi_read_object_response
