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
from io import BufferedReader
from typing import Optional, Union

from google_crc32c import Checksum
from google.api_core import exceptions

from ._utils import raise_if_no_fast_crc32c
from google.cloud import _storage_v2
from google.cloud.storage._experimental.asyncio.async_grpc_client import (
    AsyncGrpcClient,
)
from google.cloud.storage._experimental.asyncio.async_write_object_stream import (
    _AsyncWriteObjectStream,
)


_MAX_CHUNK_SIZE_BYTES = 2 * 1024 * 1024  # 2 MiB
_DEFAULT_FLUSH_INTERVAL_BYTES = 16 * 1024 * 1024  # 16 MiB


class AsyncAppendableObjectWriter:
    """Class for appending data to a GCS Appendable Object asynchronously."""

    def __init__(
        self,
        client: AsyncGrpcClient.grpc_client,
        bucket_name: str,
        object_name: str,
        generation=None,
        write_handle=None,
        writer_options: Optional[dict] = None,
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
        raise_if_no_fast_crc32c()
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
        # `offset` is the latest size of the object without staleless.
        self.offset: Optional[int] = None
        # `persisted_size` is the total_bytes persisted in the GCS server.
        # Please note: `offset` and `persisted_size` are same when the stream is
        # opened.
        self.persisted_size: Optional[int] = None
        if writer_options is None:
            writer_options = {}
        self.flush_interval = writer_options.get(
            "FLUSH_INTERVAL_BYTES", _DEFAULT_FLUSH_INTERVAL_BYTES
        )
        # TODO: add test case for this.
        if self.flush_interval < _MAX_CHUNK_SIZE_BYTES:
            raise exceptions.OutOfRange(
                f"flush_interval must be >= {_MAX_CHUNK_SIZE_BYTES} , but provided {self.flush_interval}"
            )
        if self.flush_interval % _MAX_CHUNK_SIZE_BYTES != 0:
            raise exceptions.OutOfRange(
                f"flush_interval must be a multiple of {_MAX_CHUNK_SIZE_BYTES}, but provided {self.flush_interval}"
            )
        self.bytes_appended_since_last_flush = 0

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
        self.persisted_size = self.write_obj_stream.persisted_size

    async def append(self, data: bytes) -> None:
        """Appends data to the Appendable object.

        calling `self.append` will append bytes at the end of the current size
        ie. `self.offset` bytes relative to the begining of the object.

        This method sends the provided `data` to the GCS server in chunks.
        and persists data in GCS at every `_DEFAULT_FLUSH_INTERVAL_BYTES` bytes
        or at the last chunk whichever is earlier. Persisting is done by setting
        `flush=True` on request.

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
        while start_idx < total_bytes:
            end_idx = min(start_idx + _MAX_CHUNK_SIZE_BYTES, total_bytes)
            data_chunk = data[start_idx:end_idx]
            is_last_chunk = end_idx == total_bytes
            chunk_size = end_idx - start_idx
            await self.write_obj_stream.send(
                _storage_v2.BidiWriteObjectRequest(
                    write_offset=self.offset,
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=data_chunk,
                        crc32c=int.from_bytes(Checksum(data_chunk).digest(), "big"),
                    ),
                    state_lookup=is_last_chunk,
                    flush=is_last_chunk
                    or (
                        self.bytes_appended_since_last_flush + chunk_size
                        >= self.flush_interval
                    ),
                )
            )
            self.offset += chunk_size
            self.bytes_appended_since_last_flush += chunk_size

            if self.bytes_appended_since_last_flush >= self.flush_interval:
                self.bytes_appended_since_last_flush = 0

            if is_last_chunk:
                response = await self.write_obj_stream.recv()
                self.persisted_size = response.persisted_size
                self.offset = self.persisted_size
                self.bytes_appended_since_last_flush = 0
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
            return await self.finalize()

        await self.write_obj_stream.close()

        self._is_stream_open = False
        self.offset = None
        return self.persisted_size

    async def finalize(self) -> _storage_v2.Object:
        """Finalizes the Appendable Object.

        Note: Once finalized no more data can be appended.
        This method is different from `close`. if `.close()` is called data may
        still be appended to object at a later point in time by opening with
        generation number.
        (i.e. `open(..., generation=<object_generation_number>)`.
        However if `.finalize()` is called no more data can be appended to the
        object.

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
        await self.write_obj_stream.close()

        self._is_stream_open = False
        self.offset = None
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

    async def append_from_file(
        self, file_obj: BufferedReader, block_size: int = _DEFAULT_FLUSH_INTERVAL_BYTES
    ):
        """
        Appends data to an Appendable Object using file_handle which is opened
        for reading in binary mode.

        :type file_obj: file
        :param file_obj: A file handle opened in binary mode for reading.

        """
        while block := file_obj.read(block_size):
            await self.append(block)
