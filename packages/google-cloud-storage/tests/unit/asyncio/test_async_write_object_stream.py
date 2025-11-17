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
async def test_unimplemented_methods_raise_error(mock_client):
    """Test that unimplemented methods raise NotImplementedError."""
    stream = _AsyncWriteObjectStream(mock_client, BUCKET, OBJECT)

    with pytest.raises(NotImplementedError):
        await stream.open()

    with pytest.raises(NotImplementedError):
        await stream.close()

    with pytest.raises(NotImplementedError):
        await stream.send(_storage_v2.BidiWriteObjectRequest())

    with pytest.raises(NotImplementedError):
        await stream.recv()
