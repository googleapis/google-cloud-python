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
"""
NOTE:
This is _experimental module for upcoming support for Rapid Storage.
(https://cloud.google.com/blog/products/storage-data-transfer/high-performance-storage-innovations-for-ai-hpc#:~:text=your%20AI%20workloads%3A-,Rapid%20Storage,-%3A%20A%20new)

APIs may not work as intended and are not stable yet. Feature is not
GA(Generally Available) yet, please contact your TAM(Technical Account Manager)
if you want to use these Rapid Storage APIs.

"""
from typing import Optional
from google.cloud import _storage_v2
from google.cloud.storage._experimental.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage._experimental.asyncio.async_abstract_object_stream import (
    _AsyncAbstractObjectStream,
)
from google.api_core.bidi_async import AsyncBidiRpc


class _AsyncWriteObjectStream(_AsyncAbstractObjectStream):
    """Class representing a gRPC bidi-stream for writing data from a GCS
      ``Appendable Object``.

    This class provides a unix socket-like interface to a GCS ``Object``, with
    methods like ``open``, ``close``, ``send``, and ``recv``.

    :type client: :class:`~google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client`
    :param client: async grpc client to use for making API requests.

    :type bucket_name: str
    :param bucket_name: The name of the GCS ``bucket`` containing the object.

    :type object_name: str
    :param object_name: The name of the GCS ``Appendable Object`` to be write.

    :type generation_number: int
    :param generation_number: (Optional) If present, creates writer for that
        specific revision of that object. Use this to append data to an
        existing Appendable Object.

        Setting to ``0`` makes the `writer.open()` succeed only if
        object doesn't exist in the bucket (useful for not accidentally
        overwriting existing objects).

        Warning: If `None`, a new object is created. If an object with the
        same name already exists, it will be overwritten the moment
        `writer.open()` is called.

    :type write_handle: _storage_v2.BidiWriteHandle
    :param write_handle: (Optional) An existing handle for writing the object.
                        If provided, opening the bidi-gRPC connection will be faster.
    """

    def __init__(
        self,
        client: AsyncGrpcClient.grpc_client,
        bucket_name: str,
        object_name: str,
        generation_number: Optional[int] = None,  # None means new object
        write_handle: Optional[_storage_v2.BidiWriteHandle] = None,
    ) -> None:
        if client is None:
            raise ValueError("client must be provided")
        if bucket_name is None:
            raise ValueError("bucket_name must be provided")
        if object_name is None:
            raise ValueError("object_name must be provided")

        super().__init__(
            bucket_name=bucket_name,
            object_name=object_name,
            generation_number=generation_number,
        )
        self.client: AsyncGrpcClient.grpc_client = client
        self.write_handle: Optional[_storage_v2.BidiWriteHandle] = write_handle

        self._full_bucket_name = f"projects/_/buckets/{self.bucket_name}"

        self.rpc = self.client._client._transport._wrapped_methods[
            self.client._client._transport.bidi_write_object
        ]

        self.metadata = (("x-goog-request-params", f"bucket={self._full_bucket_name}"),)
        self.socket_like_rpc: Optional[AsyncBidiRpc] = None
        self._is_stream_open: bool = False
        self.first_bidi_write_req = None
        self.persisted_size = 0
        self.object_resource: Optional[_storage_v2.Object] = None

    async def open(self) -> None:
        """
        Opens the bidi-gRPC connection to write to the object.

        This method sends an initial request to start the stream and receives
        the first response containing metadata and a write handle.

        :rtype: None
        :raises ValueError: If the stream is already open.
        :raises google.api_core.exceptions.FailedPrecondition: 
            if `generation_number` is 0 and object already exists.
        """
        if self._is_stream_open:
            raise ValueError("Stream is already open")

        # Create a new object or overwrite existing one if generation_number
        # is None. This makes it consistent with GCS JSON API behavior.
        # Created object type would be Appendable Object.
        # if `generation_number` == 0 new object will be created only if there
        # isn't any existing object.
        is_open_via_write_handle = (
            self.write_handle is not None and self.generation_number
        )
        if self.generation_number is None or self.generation_number == 0:
            self.first_bidi_write_req = _storage_v2.BidiWriteObjectRequest(
                write_object_spec=_storage_v2.WriteObjectSpec(
                    resource=_storage_v2.Object(
                        name=self.object_name, bucket=self._full_bucket_name
                    ),
                    appendable=True,
                    if_generation_match=self.generation_number,
                ),
            )
        else:
            self.first_bidi_write_req = _storage_v2.BidiWriteObjectRequest(
                append_object_spec=_storage_v2.AppendObjectSpec(
                    bucket=self._full_bucket_name,
                    object=self.object_name,
                    generation=self.generation_number,
                    write_handle=self.write_handle,
                ),
            )
        self.socket_like_rpc = AsyncBidiRpc(
            self.rpc, initial_request=self.first_bidi_write_req, metadata=self.metadata
        )

        await self.socket_like_rpc.open()  # this is actually 1 send
        response = await self.socket_like_rpc.recv()
        self._is_stream_open = True
        if is_open_via_write_handle:
            # Don't use if not response.persisted_size because this will be true
            # if persisted_size==0 (0 is considered "Falsy" in Python)
            if response.persisted_size is None:
                raise ValueError(
                    "Failed to obtain persisted_size after opening the stream via write_handle"
                )
            self.persisted_size = response.persisted_size
        else:
            if not response.resource:
                raise ValueError(
                    "Failed to obtain object resource after opening the stream"
                )
            if not response.resource.generation:
                raise ValueError(
                    "Failed to obtain object generation after opening the stream"
                )
            if not response.resource.size:
                # Appending to a 0 byte appendable object.
                self.persisted_size = 0
            else:
                self.persisted_size = response.resource.size

        if not response.write_handle:
            raise ValueError("Failed to obtain write_handle after opening the stream")

        self.generation_number = response.resource.generation
        self.write_handle = response.write_handle

    async def close(self) -> None:
        """Closes the bidi-gRPC connection."""
        if not self._is_stream_open:
            raise ValueError("Stream is not open")
        await self.requests_done()
        await self.socket_like_rpc.close()
        self._is_stream_open = False

    async def requests_done(self):
        """Signals that all requests have been sent."""

        await self.socket_like_rpc.send(None)
        await self.socket_like_rpc.recv()

    async def send(
        self, bidi_write_object_request: _storage_v2.BidiWriteObjectRequest
    ) -> None:
        """Sends a request message on the stream.

        Args:
            bidi_write_object_request (:class:`~google.cloud._storage_v2.types.BidiReadObjectRequest`):
                The request message to send. This is typically used to specify
                the read offset and limit.
        """
        if not self._is_stream_open:
            raise ValueError("Stream is not open")
        await self.socket_like_rpc.send(bidi_write_object_request)

    async def recv(self) -> _storage_v2.BidiWriteObjectResponse:
        """Receives a response from the stream.

        This method waits for the next message from the server, which could
        contain object data or metadata.

        Returns:
            :class:`~google.cloud._storage_v2.types.BidiWriteObjectResponse`:
                The response message from the server.
        """
        if not self._is_stream_open:
            raise ValueError("Stream is not open")
        return await self.socket_like_rpc.recv()

    @property
    def is_stream_open(self) -> bool:
        return self._is_stream_open
