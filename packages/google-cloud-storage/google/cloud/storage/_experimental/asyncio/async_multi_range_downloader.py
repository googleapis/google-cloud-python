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

from __future__ import annotations

from typing import List, Optional, Tuple

from google.cloud.storage._experimental.asyncio.async_read_object_stream import (
    _AsyncReadObjectStream,
)
from google.cloud.storage._experimental.asyncio.async_grpc_client import (
    AsyncGrpcClient,
)

from io import BytesIO
from google.cloud import _storage_v2


_MAX_READ_RANGES_PER_BIDI_READ_REQUEST = 100


class Result:
    """An instance of this class will be populated and retured for each
    `read_range` provided to ``download_ranges`` method.

    """

    def __init__(self, bytes_requested: int):
        # only while instantiation, should not be edited later.
        # hence there's no setter, only getter is provided.
        self._bytes_requested: int = bytes_requested
        self._bytes_written: int = 0

    @property
    def bytes_requested(self) -> int:
        return self._bytes_requested

    @property
    def bytes_written(self) -> int:
        return self._bytes_written

    @bytes_written.setter
    def bytes_written(self, value: int):
        self._bytes_written = value

    def __repr__(self):
        return f"bytes_requested: {self._bytes_requested}, bytes_written: {self._bytes_written}"


class AsyncMultiRangeDownloader:
    """Provides an interface for downloading multiple ranges of a GCS ``Object``
    concurrently.

    Example usage:

    .. code-block:: python

        client = AsyncGrpcClient().grpc_client
        mrd = await AsyncMultiRangeDownloader.create_mrd(
            client, bucket_name="chandrasiri-rs", object_name="test_open9"
        )
        my_buff1 = open('my_fav_file.txt', 'wb')
        my_buff2 = BytesIO()
        my_buff3 = BytesIO()
        my_buff4 = any_object_which_provides_BytesIO_like_interface()
        results_arr = await mrd.download_ranges(
            [
                # (start_byte, bytes_to_read, writeable_buffer)
                (0, 100, my_buff1),
                (100, 20, my_buff2),
                (200, 123, my_buff3),
                (300, 789, my_buff4),
            ]
        )

        for result in results_arr:
            print("downloaded bytes", result)


    """

    @classmethod
    async def create_mrd(
        cls,
        client: AsyncGrpcClient.grpc_client,
        bucket_name: str,
        object_name: str,
        generation_number: Optional[int] = None,
        read_handle: Optional[bytes] = None,
    ) -> AsyncMultiRangeDownloader:
        """Initializes a MultiRangeDownloader and opens the underlying bidi-gRPC
        object for reading.

        :type client: :class:`~google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client`
        :param client: The asynchronous client to use for making API requests.

        :type bucket_name: str
        :param bucket_name: The name of the bucket containing the object.

        :type object_name: str
        :param object_name: The name of the object to be read.

        :type generation_number: int
        :param generation_number: (Optional) If present, selects a specific
                                  revision of this object.

        :type read_handle: bytes
        :param read_handle: (Optional) An existing handle for reading the object.
                            If provided, opening the bidi-gRPC connection will be faster.

        :rtype: :class:`~google.cloud.storage._experimental.asyncio.async_multi_range_downloader.AsyncMultiRangeDownloader`
        :returns: An initialized AsyncMultiRangeDownloader instance for reading.
        """
        mrd = cls(client, bucket_name, object_name, generation_number, read_handle)
        await mrd.open()
        return mrd

    def __init__(
        self,
        client: AsyncGrpcClient.grpc_client,
        bucket_name: str,
        object_name: str,
        generation_number: Optional[int] = None,
        read_handle: Optional[bytes] = None,
    ) -> None:
        """Constructor for AsyncMultiRangeDownloader, clients are not adviced to
         use it directly. Instead it's adviced to use the classmethod `create_mrd`.

        :type client: :class:`~google.cloud.storage._experimental.asyncio.async_grpc_client.AsyncGrpcClient.grpc_client`
        :param client: The asynchronous client to use for making API requests.

        :type bucket_name: str
        :param bucket_name: The name of the bucket containing the object.

        :type object_name: str
        :param object_name: The name of the object to be read.

        :type generation_number: int
        :param generation_number: (Optional) If present, selects a specific revision of
                                  this object.

        :type read_handle: bytes
        :param read_handle: (Optional) An existing read handle.
        """
        self.client = client
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.generation_number = generation_number
        self.read_handle = read_handle
        self.read_obj_str: Optional[_AsyncReadObjectStream] = None
        self._is_stream_open: bool = False

    async def open(self) -> None:
        """Opens the bidi-gRPC connection to read from the object.

        This method initializes and opens an `_AsyncReadObjectStream` (bidi-gRPC stream) to
        for downloading ranges of data from GCS ``Object``.

        "Opening" constitutes fetching object metadata such as generation number
        and read handle and sets them as attributes if not already set.
        """
        if self._is_stream_open:
            raise ValueError("Underlying bidi-gRPC stream is already open")

        if self.read_obj_str is None:
            self.read_obj_str = _AsyncReadObjectStream(
                client=self.client,
                bucket_name=self.bucket_name,
                object_name=self.object_name,
                generation_number=self.generation_number,
                read_handle=self.read_handle,
            )
        await self.read_obj_str.open()
        self._is_stream_open = True
        if self.generation_number is None:
            self.generation_number = self.read_obj_str.generation_number
        self.read_handle = self.read_obj_str.read_handle
        return

    async def download_ranges(
        self, read_ranges: List[Tuple[int, int, BytesIO]]
    ) -> List[Result]:
        """Downloads multiple byte ranges from the object into the buffers
        provided by user.

        :type read_ranges: List[Tuple[int, int, "BytesIO"]]
        :param read_ranges: A list of tuples, where each tuple represents a
            byte range (start_byte, bytes_to_read, writeable_buffer). Buffer has
            to be provided by the user, and user has to make sure appropriate
            memory is available in the application to avoid out-of-memory crash.

        :rtype: List[:class:`~google.cloud.storage._experimental.asyncio.async_multi_range_downloader.Result`]
        :returns: A list of ``Result`` objects, where each object corresponds
                  to a requested range.

        """

        if len(read_ranges) > 1000:
            raise ValueError(
                "Invalid input - length of read_ranges cannot be more than 1000"
            )

        if not self._is_stream_open:
            raise ValueError("Underlying bidi-gRPC stream is not open")

        read_id_to_writable_buffer_dict = {}
        results = []
        for i in range(0, len(read_ranges), _MAX_READ_RANGES_PER_BIDI_READ_REQUEST):
            read_ranges_segment = read_ranges[
                i : i + _MAX_READ_RANGES_PER_BIDI_READ_REQUEST
            ]

            read_ranges_for_bidi_req = []
            for j, read_range in enumerate(read_ranges_segment):
                read_id = i + j
                read_id_to_writable_buffer_dict[read_id] = read_range[2]
                bytes_requested = read_range[1]
                results.append(Result(bytes_requested))
                read_ranges_for_bidi_req.append(
                    _storage_v2.ReadRange(
                        read_offset=read_range[0],
                        read_length=bytes_requested,
                        read_id=read_id,
                    )
                )
            await self.read_obj_str.send(
                _storage_v2.BidiReadObjectRequest(read_ranges=read_ranges_for_bidi_req)
            )

        while len(read_id_to_writable_buffer_dict) > 0:
            response = await self.read_obj_str.recv()

            if response is None:
                raise Exception("None response received, something went wrong.")

            for object_data_range in response.object_data_ranges:
                if object_data_range.read_range is None:
                    raise Exception("Invalid response, read_range is None")

                data = object_data_range.checksummed_data.content
                read_id = object_data_range.read_range.read_id
                buffer = read_id_to_writable_buffer_dict[read_id]
                buffer.write(data)
                results[read_id].bytes_written += len(data)

                if object_data_range.range_end:
                    del read_id_to_writable_buffer_dict[
                        object_data_range.read_range.read_id
                    ]

        return results

    async def close(self):
        """
        Closes the underlying bidi-gRPC connection.
        """
        if not self._is_stream_open:
            raise ValueError("Underlying bidi-gRPC stream is not open")
        await self.read_obj_str.close()
        self._is_stream_open = False

    @property
    def is_stream_open(self) -> bool:
        return self._is_stream_open
