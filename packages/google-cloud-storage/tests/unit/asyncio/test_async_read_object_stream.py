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

from google.cloud.storage._experimental.asyncio.async_abstract_object_stream import (
    _AsyncAbstractObjectStream,
)
from google.cloud.storage._experimental.asyncio.async_read_object_stream import (
    _AsyncReadObjectStream,
)


def test_inheritance():
    """Test that _AsyncReadObjectStream inherits from _AsyncAbstractObjectStream."""
    assert issubclass(_AsyncReadObjectStream, _AsyncAbstractObjectStream)


def test_init():
    """Test the constructor of _AsyncReadObjectStream."""
    mock_client = mock.Mock(name="client")
    bucket_name = "test-bucket"
    object_name = "test-object"
    generation = 12345
    read_handle = "some-handle"

    # Test with all parameters
    stream = _AsyncReadObjectStream(
        mock_client,
        bucket_name=bucket_name,
        object_name=object_name,
        generation_number=generation,
        read_handle=read_handle,
    )

    assert stream.client is mock_client
    assert stream.bucket_name == bucket_name
    assert stream.object_name == object_name
    assert stream.generation_number == generation
    assert stream.read_handle == read_handle

    # Test with default parameters
    stream_defaults = _AsyncReadObjectStream(
        mock_client, bucket_name=bucket_name, object_name=object_name
    )
    assert stream_defaults.client is mock_client
    assert stream_defaults.bucket_name is bucket_name
    assert stream_defaults.object_name is object_name
    assert stream_defaults.generation_number is None
    assert stream_defaults.read_handle is None


def test_init_with_invalid_parameters():
    """Test the constructor of _AsyncReadObjectStream with invalid params."""

    with pytest.raises(ValueError):
        _AsyncReadObjectStream(None, bucket_name=None, object_name=None)


@pytest.mark.asyncio
async def test_async_methods_are_awaitable():
    """Test that the async methods exist and are awaitable."""
    mock_client = mock.Mock(name="client")
    stream = _AsyncReadObjectStream(mock_client, "bucket", "object")

    # These methods are currently empty, but we can test they are awaitable
    # and don't raise exceptions.
    try:
        await stream.open()
        await stream.close()
        await stream.send(mock.Mock())
        await stream.recv()
    except Exception as e:
        pytest.fail(f"Async methods should be awaitable without errors. Raised: {e}")
