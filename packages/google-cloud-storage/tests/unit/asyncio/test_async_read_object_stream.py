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
from google.cloud import _storage_v2

from google.cloud.storage._experimental.asyncio.async_read_object_stream import (
    _AsyncReadObjectStream,
)


@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_read_object_stream.AsyncBidiRpc"
)
@mock.patch(
    "google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client"
)
def test_init_with_bucket_object_generation(mock_client, mock_async_bidi_rpc):
    # initialize with bucket, object_name and generation number.  & client.
    bucket_name = "test-bucket"
    object_name = "test-object"
    generation_number = 12345
    mock_client._client._transport.bidi_read_object = "bidi_read_object_rpc"
    mock_client._client._transport._wrapped_methods = {
        "bidi_read_object_rpc": mock.sentinel.A
    }

    read_obj_stream = _AsyncReadObjectStream(
        client=mock_client,
        bucket_name=bucket_name,
        object_name=object_name,
        generation_number=generation_number,
    )
    full_bucket_name = f"projects/_/buckets/{bucket_name}"
    first_bidi_read_req = _storage_v2.BidiReadObjectRequest(
        read_object_spec=_storage_v2.BidiReadObjectSpec(
            bucket=full_bucket_name, object=object_name
        ),
    )
    mock_async_bidi_rpc.assert_called_once_with(
        mock.sentinel.A,
        initial_request=first_bidi_read_req,
        metadata=(("x-goog-request-params", f"bucket={full_bucket_name}"),),
    )
    assert read_obj_stream.socket_like_rpc is mock_async_bidi_rpc.return_value


def test_init_with_invalid_parameters():
    """Test the constructor of _AsyncReadObjectStream with invalid params."""

    with pytest.raises(ValueError):
        _AsyncReadObjectStream(None, bucket_name=None, object_name=None)
