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
GA(Generally Available) yet, please contact your TAM (Technical Account Manager)
if you want to use these Rapid Storage APIs.

"""
from typing import Optional, Union
from google.cloud import _storage_v2
from google.cloud.storage._experimental.asyncio.async_grpc_client import (
    AsyncGrpcClient,
)
from google.cloud.storage._experimental.asyncio.async_write_object_stream import (
    _AsyncWriteObjectStream,
)


_MAX_CHUNK_SIZE_BYTES = 2 * 1024 * 1024  # 2 MiB
_MAX_BUFFER_SIZE_BYTES = 16 * 1024 * 1024  # 16 MiB


class AsyncAppendableObjectWriter:
    """Class for appending data to a GCS Appendable Object asynchronously."""

    def __init__(
        self,
        client: AsyncGrpcClient.grpc_client,
        bucket_name: str,
        object_name: str,
        generation=None,
        write_handle=None,
    ):
        """
        Class for appending data to a GCS Appendable Object.

        Example usage:

        ```

        from google.cloud.storage._experimental.asyncio.async_grpc_client import AsyncGrpcClient
        from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import AsyncAppendableObjectWriter
        import asyncio

        client = AsyncGrpcClient().grpc_client
        bucket_name = "my-bucket"
        object_name = "my-appendable-object"

        # instantiate the writer
        writer = AsyncAppendableObjectWriter(client, bucket_name, object_name)
        # open the writer, (underlying gRPC bidi-stream will be opened)
        await writer.open()

        # append data, it can be called multiple times.
        await writer.append(b"hello world")
        await writer.append(b"some more data")

        # optionally flush data to persist.
        await writer.flush()

        # close the gRPC stream.
        # Please note closing the program will also close the stream,
        # however it's recommended to close the stream if no more data to append
        # to clean up gRPC connection (which means CPU/memory/network resources)
        await writer.close()
        ```

        :type client: :class:`~google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client`
        :param client: async grpc client to use for making API requests.

        :type bucket_name: str
        :param bucket_name: The name of the GCS bucket containing the object.

        :type object_name: str
        :param object_name: The name of the GCS Appendable Object to be written.

        :type generation: int
        :param generation: (Optional) If present, selects a specific revision of
                            that object.
                            If None, a new object is created.
                            If None and Object already exists then it'll will be
                            overwritten.

        :type write_handle: bytes
        :param write_handle: (Optional) An existing handle for writing the object.
                            If provided, opening the bidi-gRPC connection will be faster.
        """
        self.client = client
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.write_handle = write_handle
        self.generation = generation

        self.write_obj_stream = _AsyncWriteObjectStream(
            client=self.client,
            bucket_name=self.bucket_name,
            object_name=self.object_name,
            generation_number=self.generation,
            write_handle=self.write_handle,
        )
        self._is_stream_open: bool = False
        self.offset: Optional[int] = None
        self.persisted_size: Optional[int] = None

    async def state_lookup(self) -> int:
        """Returns the persisted_size

        :rtype: int
        :returns: persisted size.

        :raises ValueError: If the stream is not open (i.e., `open()` has not
            been called).
        """
        if not self._is_stream_open:
            raise ValueError("Stream is not open. Call open() before state_lookup().")

        await self.write_obj_stream.send(
            _storage_v2.BidiWriteObjectRequest(
                state_lookup=True,
            )
        )
        response = await self.write_obj_stream.recv()
        self.persisted_size = response.persisted_size
        return self.persisted_size

    async def open(self) -> None:
        """Opens the underlying bidi-gRPC stream.

        :raises ValueError: If the stream is already open.

        """
        if self._is_stream_open:
            raise ValueError("Underlying bidi-gRPC stream is already open")

        await self.write_obj_stream.open()
        self._is_stream_open = True
        if self.generation is None:
            self.generation = self.write_obj_stream.generation_number
        self.write_handle = self.write_obj_stream.write_handle

        # Update self.persisted_size
        _ = await self.state_lookup()

    async def append(self, data: bytes) -> None:
        """Appends data to the Appendable object.

        This method sends the provided data to the GCS server in chunks. It
        maintains an internal threshold `_MAX_BUFFER_SIZE_BYTES` and will
        automatically flush the data to make it visible to readers when that
        threshold has reached.

        :type data: bytes
        :param data: The bytes to append to the object.

        :rtype: None

        :raises ValueError: If the stream is not open (i.e., `open()` has not
            been called).
        """

        if not self._is_stream_open:
            raise ValueError("Stream is not open. Call open() before append().")
        total_bytes = len(data)
        if total_bytes == 0:
            # TODO: add warning.
            return
        if self.offset is None:
            assert self.persisted_size is not None
            self.offset = self.persisted_size

        start_idx = 0
        bytes_to_flush = 0
        while start_idx < total_bytes:
            end_idx = min(start_idx + _MAX_CHUNK_SIZE_BYTES, total_bytes)
            await self.write_obj_stream.send(
                _storage_v2.BidiWriteObjectRequest(
                    write_offset=self.offset,
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=data[start_idx:end_idx]
                    ),
                )
            )
            chunk_size = end_idx - start_idx
            self.offset += chunk_size
            bytes_to_flush += chunk_size
            if bytes_to_flush >= _MAX_BUFFER_SIZE_BYTES:
                await self.simple_flush()
                bytes_to_flush = 0
            start_idx = end_idx

    async def simple_flush(self) -> None:
        """Flushes the data to the server.
        Please note: Unlike `flush` it does not do `state_lookup`

        :rtype: None

        :raises ValueError: If the stream is not open (i.e., `open()` has not
            been called).
        """
        if not self._is_stream_open:
            raise ValueError("Stream is not open. Call open() before simple_flush().")

        await self.write_obj_stream.send(
            _storage_v2.BidiWriteObjectRequest(
                flush=True,
            )
        )

    async def flush(self) -> int:
        """Flushes the data to the server.

        :rtype: int
        :returns: The persisted size after flush.

        :raises ValueError: If the stream is not open (i.e., `open()` has not
            been called).
        """
        if not self._is_stream_open:
            raise ValueError("Stream is not open. Call open() before flush().")

        await self.write_obj_stream.send(
            _storage_v2.BidiWriteObjectRequest(
                flush=True,
                state_lookup=True,
            )
        )
        response = await self.write_obj_stream.recv()
        self.persisted_size = response.persisted_size
        self.offset = self.persisted_size
        return self.persisted_size

    async def close(self, finalize_on_close=False) -> Union[int, _storage_v2.Object]:
        """Closes the underlying bidi-gRPC stream.

        :type finalize_on_close: bool
        :param finalize_on_close: Finalizes the Appendable Object. No more data
          can be appended.

        rtype: Union[int, _storage_v2.Object]
        returns: Updated `self.persisted_size` by default after closing the
            bidi-gRPC stream. However, if `finalize_on_close=True` is passed,
            returns the finalized object resource.

        :raises ValueError: If the stream is not open (i.e., `open()` has not
            been called).

        """
        if not self._is_stream_open:
            raise ValueError("Stream is not open. Call open() before close().")

        if finalize_on_close:
            await self.finalize()
        else:
            await self.flush()
            await self.write_obj_stream.close()

        self._is_stream_open = False
        self.offset = None
        return self.object_resource if finalize_on_close else self.persisted_size

    async def finalize(self) -> _storage_v2.Object:
        """Finalizes the Appendable Object.

        Note: Once finalized no more data can be appended.

        rtype: google.cloud.storage_v2.types.Object
        returns: The finalized object resource.

        :raises ValueError: If the stream is not open (i.e., `open()` has not
            been called).
        """
        if not self._is_stream_open:
            raise ValueError("Stream is not open. Call open() before finalize().")

        await self.write_obj_stream.send(
            _storage_v2.BidiWriteObjectRequest(finish_write=True)
        )
        response = await self.write_obj_stream.recv()
        self.object_resource = response.resource
        self.persisted_size = self.object_resource.size
        return self.object_resource

    # helper methods.
    async def append_from_string(self, data: str):
        """
        str data will be encoded to bytes using utf-8 encoding calling

        self.append(data.encode("utf-8"))
        """
        raise NotImplementedError("append_from_string is not implemented yet.")

    async def append_from_stream(self, stream_obj):
        """
        At a time read a chunk of data (16MiB) from `stream_obj`
        and call self.append(chunk)
        """
        raise NotImplementedError("append_from_stream is not implemented yet.")

    async def append_from_file(self, file_path: str):
        """Create a file object from `file_path` and call append_from_stream(file_obj)"""
        raise NotImplementedError("append_from_file is not implemented yet.")
