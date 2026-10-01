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

import asyncio
import inspect
import logging
import math
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from google.api_core import exceptions
from google.api_core.retry_async import AsyncRetry

from google.cloud import _storage_v2
from google.cloud.storage._helpers import generate_random_56_bit_integer
from google.cloud.storage.asyncio._stream_multiplexer import (
    _StreamEnd,
    _StreamError,
    _StreamMultiplexer,
)
from google.cloud.storage.asyncio.async_grpc_client import (
    AsyncGrpcClient,
)
from google.cloud.storage.asyncio.async_read_object_stream import (
    _AsyncReadObjectStream,
)
from google.cloud.storage.asyncio.retry._helpers import _handle_redirect
from google.cloud.storage.asyncio.retry.bidi_stream_retry_manager import (
    _BidiStreamRetryManager,
)
from google.cloud.storage.asyncio.retry.reads_resumption_strategy import (
    _DownloadState,
    _ReadResumptionStrategy,
)
from google.cloud.storage.exceptions import DataCorruption

from ._utils import raise_if_no_fast_crc32c

_MAX_READ_RANGES_PER_BIDI_READ_REQUEST = 100
_COMMON_READ_RETRYABLE_EXCEPTIONS = (
    exceptions.InternalServerError,
    exceptions.ServiceUnavailable,
    exceptions.DeadlineExceeded,
    exceptions.TooManyRequests,
)

logger = logging.getLogger(__name__)


def _is_open_retryable(exc):
    """Determine whether opening a read stream should be retried."""
    if isinstance(exc, _COMMON_READ_RETRYABLE_EXCEPTIONS):
        return True

    if not isinstance(exc, exceptions.Aborted):
        return False

    routing_token, read_handle = _handle_redirect(exc)
    return routing_token is not None or read_handle is not None


def _is_read_retryable(exc):
    """Determine whether an active read stream should be retried."""
    return isinstance(
        exc,
        _COMMON_READ_RETRYABLE_EXCEPTIONS + (exceptions.Aborted,),
    )


@dataclass
class MRDStreamConfig:
    """Configuration parameters for multi-stream download scaling and load balancing.

    :type min_connections: int
    :param min_connections: Minimum number of streams opened at initialization. Defaults to 1.

    :type max_connections: int
    :param max_connections: Maximum concurrent streams allowed. Defaults to 8.

    :type target_io_depth: int
    :param target_io_depth: Target outstanding requests per connection before scaling up. Defaults to 8.

    :type target_bytes: int
    :param target_bytes: Target outstanding bytes per connection before scaling up. Defaults to 8 MB.
    """

    min_connections: int = 1
    max_connections: int = 8
    target_io_depth: int = 8
    target_bytes: int = 8 * 1024 * 1024


class _ManagedStream:
    """Wraps an active stream and its multiplexer with local load counters."""

    def __init__(
        self,
        stream: _AsyncReadObjectStream,
        multiplexer: _StreamMultiplexer,
    ):
        self.stream = stream
        self.multiplexer = multiplexer
        self.pending_ranges: int = 0
        self.pending_bytes: int = 0

    def calculate_load(self, target_io_depth: int, target_bytes: int) -> float:
        """Returns normalized load metric combining request count and bytes."""
        u_req = self.pending_ranges / target_io_depth if target_io_depth > 0 else 0.0
        u_bytes = self.pending_bytes / target_bytes if target_bytes > 0 else 0.0
        return 0.5 * u_req + 0.5 * u_bytes

    def record_request(self, range_count: int, byte_count: int) -> None:
        self.pending_ranges += range_count
        self.pending_bytes += byte_count

    def record_completion(self, range_count: int, byte_count: int) -> None:
        self.pending_ranges = max(0, self.pending_ranges - range_count)
        self.pending_bytes = max(0, self.pending_bytes - byte_count)


class _StreamPool:
    """Manages a pool of _ManagedStream instances with dynamic scaling and least-loaded dispatch."""

    def __init__(
        self,
        stream_factory: Callable[[], Awaitable[_ManagedStream]],
        min_connections: int = 1,
        max_connections: int = 8,
        target_io_depth: int = 8,
        target_bytes: int = 8 * 1024 * 1024,
    ):
        self._stream_factory = stream_factory
        self.min_connections = max(1, min_connections)
        self.max_connections = max(self.min_connections, max_connections)
        self.target_io_depth = target_io_depth
        self.target_bytes = target_bytes

        self.workers: List[_ManagedStream] = []
        self._lock = asyncio.Lock()
        self._pending_scale_ups: int = 0
        self._closed = False
        self._background_tasks: set[asyncio.Task] = set()

    async def add_worker(self, worker: _ManagedStream) -> None:
        async with self._lock:
            self.workers.append(worker)

    async def acquire_stream(self, range_count: int, req_bytes: int) -> _ManagedStream:
        """Finds least loaded stream and triggers background scale-up proportional to load."""
        async with self._lock:
            if self._closed:
                raise ValueError("Pool is closed")
            if not self.workers:
                raise ValueError("No workers available in stream pool")
            best = min(
                self.workers,
                key=lambda w: w.calculate_load(self.target_io_depth, self.target_bytes),
            )
            best.record_request(range_count, req_bytes)

            # Trigger background scale-ups proportional to total load across all workers
            total_load = sum(
                w.calculate_load(self.target_io_depth, self.target_bytes)
                for w in self.workers
            )
            desired_workers = math.ceil(total_load)
            planned_workers = len(self.workers) + self._pending_scale_ups
            needed_scale_ups = max(
                0, min(desired_workers, self.max_connections) - planned_workers
            )

            for _ in range(needed_scale_ups):
                self._pending_scale_ups += 1
                task = asyncio.create_task(self._scale_up())
                self._background_tasks.add(task)
                task.add_done_callback(self._background_tasks.discard)

            return best

    async def _scale_up(self) -> None:
        try:
            new_worker = await self._stream_factory()
            async with self._lock:
                if self._closed:
                    try:
                        await new_worker.multiplexer.close()
                    except Exception:
                        pass
                    try:
                        res = new_worker.stream.close()
                        if inspect.isawaitable(res):
                            await res
                    except Exception:
                        pass
                    return
                self.workers.append(new_worker)
        except Exception as e:
            logger.warning(f"Failed to scale up MRD stream: {e}")
        finally:
            async with self._lock:
                self._pending_scale_ups = max(0, self._pending_scale_ups - 1)

    def release_stream(
        self, worker: _ManagedStream, range_count: int, req_bytes: int
    ) -> None:
        worker.record_completion(range_count, req_bytes)

    async def close(self) -> None:
        async with self._lock:
            self._closed = True
            self._pending_scale_ups = 0
            workers = list(self.workers)
            self.workers.clear()
            for task in list(self._background_tasks):
                task.cancel()
        for w in workers:
            try:
                await w.multiplexer.close()
            except Exception:
                pass
            try:
                res = w.stream.close()
                if inspect.isawaitable(res):
                    await res
            except Exception:
                pass


class AsyncMultiRangeDownloader:
    """Provides an interface for downloading multiple ranges of a GCS ``Object``
    concurrently.

    Example usage:

    .. code-block:: python

        client = AsyncGrpcClient()
        mrd = await AsyncMultiRangeDownloader.create_mrd(
            client, bucket_name="chandrasiri-rs", object_name="test_open9"
        )
        my_buff1 = open('my_fav_file.txt', 'wb')
        my_buff2 = BytesIO()
        my_buff3 = BytesIO()
        my_buff4 = any_object_which_provides_BytesIO_like_interface()
        await mrd.download_ranges(
            [
                # (start_byte, bytes_to_read, writeable_buffer)
                (0, 100, my_buff1),
                (100, 20, my_buff2),
                (200, 123, my_buff3),
                (300, 789, my_buff4),
            ]
        )

        # verify data in buffers...
        assert my_buff2.getbuffer().nbytes == 20


    """

    @classmethod
    async def create_mrd(
        cls,
        client: AsyncGrpcClient,
        bucket_name: str,
        object_name: str,
        generation: Optional[int] = None,
        read_handle: Optional[_storage_v2.BidiReadHandle] = None,
        retry_policy: Optional[AsyncRetry] = None,
        metadata: Optional[List[Tuple[str, str]]] = None,
        stream_config: Optional[MRDStreamConfig] = None,
        **kwargs,
    ) -> AsyncMultiRangeDownloader:
        """Initializes a MultiRangeDownloader and opens the underlying bidi-gRPC
        object for reading.

        :type client: :class:`~google.cloud.storage.asyncio.async_grpc_client.AsyncGrpcClient`
        :param client: The asynchronous client to use for making API requests.

        :type bucket_name: str
        :param bucket_name: The name of the bucket containing the object.

        :type object_name: str
        :param object_name: The name of the object to be read.

        :type generation: int
        :param generation: (Optional) If present, selects a specific
                                  revision of this object.

        :type read_handle: _storage_v2.BidiReadHandle
        :param read_handle: (Optional) An existing handle for reading the object.
                            If provided, opening the bidi-gRPC connection will be faster.

        :type retry_policy: :class:`~google.api_core.retry_async.AsyncRetry`
        :param retry_policy: (Optional) The retry policy to use for the ``open`` operation.

        :type metadata: List[Tuple[str, str]]
        :param metadata: (Optional) The metadata to be sent with the ``open`` request.

        :type stream_config: Optional[MRDStreamConfig]
        :param stream_config: (Optional) Configuration dataclass grouping all multi-stream
                              parameters. If None, multi-stream is disabled and a single
                              stream is used.

        :rtype: :class:`~google.cloud.storage.asyncio.async_multi_range_downloader.AsyncMultiRangeDownloader`
        :returns: An initialized AsyncMultiRangeDownloader instance for reading.
        """
        mrd = cls(
            client,
            bucket_name,
            object_name,
            generation=generation,
            read_handle=read_handle,
            stream_config=stream_config,
            **kwargs,
        )
        await mrd.open(retry_policy=retry_policy, metadata=metadata)
        return mrd

    def __init__(
        self,
        client: AsyncGrpcClient,
        bucket_name: str,
        object_name: str,
        generation: Optional[int] = None,
        read_handle: Optional[_storage_v2.BidiReadHandle] = None,
        stream_config: Optional[MRDStreamConfig] = None,
        **kwargs,
    ) -> None:
        """Constructor for AsyncMultiRangeDownloader, clients are not advised to
        use it directly. Instead it's advised to use the classmethod `create_mrd`.

        :type client: :class:`~google.cloud.storage.asyncio.async_grpc_client.AsyncGrpcClient`
        :param client: The asynchronous client to use for making API requests.

        :type bucket_name: str
        :param bucket_name: The name of the bucket containing the object.

        :type object_name: str
        :param object_name: The name of the object to be read.

        :type generation: int
        :param generation: (Optional) If present, selects a specific revision of
                                  this object.

        :type read_handle: _storage_v2.BidiReadHandle
        :param read_handle: (Optional) An existing read handle.

        :type stream_config: Optional[MRDStreamConfig]
        :param stream_config: (Optional) Configuration dataclass grouping all multi-stream
                              parameters. If None, multi-stream is disabled and a single
                              stream is used.
        """
        if "generation_number" in kwargs:
            if generation is not None:
                raise TypeError(
                    "Cannot set both 'generation' and 'generation_number'. "
                    "Use 'generation' for new code."
                )
            logger.warning(
                "'generation_number' is deprecated and will be removed in a future "
                "major release. Please use 'generation' instead."
            )
            generation = kwargs.pop("generation_number")

        self.client = client
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.generation = generation
        self.read_handle: Optional[_storage_v2.BidiReadHandle] = read_handle
        self.read_obj_str: Optional[_AsyncReadObjectStream] = None
        self._is_stream_open: bool = False
        self._routing_token: Optional[str] = None
        self._multiplexer: Optional[_StreamMultiplexer] = None
        self.persisted_size: Optional[int] = None  # updated after opening the stream
        self._open_retries: int = 0
        self.is_finalized: bool = False
        self.full_obj_server_crc32c: Optional[int] = None

        self.stream_config = stream_config
        self.min_connections = stream_config.min_connections if stream_config else 1
        self.max_connections = stream_config.max_connections if stream_config else 1
        self.target_io_depth = stream_config.target_io_depth if stream_config else 8
        self.target_bytes = (
            stream_config.target_bytes if stream_config else 8 * 1024 * 1024
        )
        self._pool: Optional[_StreamPool] = None
        self._primary_worker: Optional[_ManagedStream] = None
        self._metadata: Optional[List[Tuple[str, str]]] = None

    async def __aenter__(self):
        """Opens the underlying bidi-gRPC connection to read from the object."""
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the underlying bidi-gRPC connection."""
        if self.is_stream_open:
            await self.close()

    def _on_open_error(self, exc):
        """Extracts routing token and read handle on redirect error during open."""
        logger.warning(f"Error occurred while opening MRD: {exc}")
        routing_token, read_handle = _handle_redirect(exc)
        if routing_token:
            self._routing_token = routing_token
        if read_handle:
            self.read_handle = read_handle

    async def open(
        self,
        retry_policy: Optional[AsyncRetry] = None,
        metadata: Optional[List[Tuple[str, str]]] = None,
    ) -> None:
        """Opens the bidi-gRPC connection to read from the object."""
        if self._is_stream_open:
            raise ValueError("Underlying bidi-gRPC stream is already open")

        if retry_policy is None:

            def on_error_wrapper(exc):
                self._open_retries += 1
                self._on_open_error(exc)

            retry_policy = AsyncRetry(
                predicate=_is_open_retryable, on_error=on_error_wrapper
            )
        else:
            original_on_error = retry_policy._on_error

            def combined_on_error(exc):
                self._open_retries += 1
                self._on_open_error(exc)
                if original_on_error:
                    original_on_error(exc)

            retry_policy = AsyncRetry(
                predicate=_is_open_retryable,
                initial=retry_policy._initial,
                maximum=retry_policy._maximum,
                multiplier=retry_policy._multiplier,
                deadline=retry_policy._deadline,
                on_error=combined_on_error,
            )

        async def _do_open():
            current_metadata = list(metadata) if metadata else []

            # Cleanup stream from previous failed attempt, if any.
            if self.read_obj_str:
                if self.read_obj_str.is_stream_open:
                    try:
                        await self.read_obj_str.close()
                    except exceptions.GoogleAPICallError as e:
                        logger.warning(
                            f"Failed to close existing stream during resumption: {e}"
                        )
                self.read_obj_str = None
                self._is_stream_open = False

            self.read_obj_str = _AsyncReadObjectStream(
                client=self.client.grpc_client,
                bucket_name=self.bucket_name,
                object_name=self.object_name,
                generation_number=self.generation,
                read_handle=self.read_handle,
            )

            if self._routing_token:
                current_metadata.append(
                    ("x-goog-request-params", f"routing_token={self._routing_token}")
                )
                self._routing_token = None

            await self.read_obj_str.open(
                metadata=current_metadata if current_metadata else None
            )

            if self.read_obj_str.generation_number:
                self.generation = self.read_obj_str.generation_number
            if self.read_obj_str.read_handle:
                self.read_handle = self.read_obj_str.read_handle
            if getattr(self.read_obj_str, "routing_token", None):
                self._routing_token = self.read_obj_str.routing_token
            if self.read_obj_str.persisted_size is not None:
                self.persisted_size = self.read_obj_str.persisted_size
            self.is_finalized = self.read_obj_str.is_finalized
            self.full_obj_server_crc32c = self.read_obj_str.full_obj_server_crc32c

            self._is_stream_open = True

        self._metadata = list(metadata) if metadata else []
        await retry_policy(_do_open)()
        self._multiplexer = _StreamMultiplexer(self.read_obj_str)
        self._primary_worker = _ManagedStream(self.read_obj_str, self._multiplexer)

        if self.stream_config is not None and self.stream_config.max_connections > 1:
            self._pool = _StreamPool(
                stream_factory=self._create_new_stream_worker,
                min_connections=self.min_connections,
                max_connections=self.max_connections,
                target_io_depth=self.target_io_depth,
                target_bytes=self.target_bytes,
            )
            await self._pool.add_worker(self._primary_worker)

            for _ in range(self.min_connections - 1):
                worker = await self._create_new_stream_worker()
                await self._pool.add_worker(worker)
        else:
            self._pool = None

    async def _create_new_stream_worker(self) -> _ManagedStream:
        """Opens an additional stream worker using current routing and read_handle."""
        current_metadata = list(self._metadata) if self._metadata else []
        if self._routing_token:
            current_metadata.append(
                ("x-goog-request-params", f"routing_token={self._routing_token}")
            )

        stream = _AsyncReadObjectStream(
            client=self.client.grpc_client,
            bucket_name=self.bucket_name,
            object_name=self.object_name,
            generation_number=self.generation,
            read_handle=self.read_handle,
        )
        await stream.open(metadata=current_metadata if current_metadata else None)

        if stream.generation_number:
            self.generation = stream.generation_number
        if stream.read_handle:
            self.read_handle = stream.read_handle
        if getattr(stream, "routing_token", None):
            self._routing_token = stream.routing_token

        mux = _StreamMultiplexer(stream)
        return _ManagedStream(stream, mux)

    def _create_stream_factory(self, state, metadata, worker=None):
        """Create a factory that opens a new stream with current routing state."""
        target_worker = worker or self._primary_worker

        async def factory():
            current_handle = state.get("read_handle") or self.read_handle
            current_token = state.get("routing_token") or self._routing_token

            stream = _AsyncReadObjectStream(
                client=self.client.grpc_client,
                bucket_name=self.bucket_name,
                object_name=self.object_name,
                generation_number=self.generation,
                read_handle=current_handle,
            )

            current_metadata = list(metadata) if metadata else []
            if current_token:
                current_metadata.append(
                    (
                        "x-goog-request-params",
                        f"routing_token={current_token}",
                    )
                )

            await stream.open(metadata=current_metadata if current_metadata else None)

            if stream.generation_number:
                self.generation = stream.generation_number
            if stream.read_handle:
                self.read_handle = stream.read_handle
            if getattr(stream, "routing_token", None):
                self._routing_token = stream.routing_token
            self.is_finalized = stream.is_finalized
            self.full_obj_server_crc32c = stream.full_obj_server_crc32c

            self.read_obj_str = stream
            if target_worker is not None:
                target_worker.stream = stream
            if target_worker is None or target_worker == self._primary_worker:
                self.read_obj_str = stream
            self._is_stream_open = True

            return stream

        return factory

    async def _download_ranges_on_worker(
        self,
        worker: _ManagedStream,
        read_ranges: List[Tuple[int, int, BytesIO]],
        retry_policy: AsyncRetry,
        metadata: Optional[List[Tuple[str, str]]],
        enable_checksum: bool,
    ) -> None:
        """Downloads multiple byte ranges from the object into the buffers
        provided by user with automatic retries.

        :type read_ranges: List[Tuple[int, int, "BytesIO"]]
        :param read_ranges: A list of tuples, where each tuple represents a
            combination of byte_range and writeable buffer in format -
            (`start_byte`, `bytes_to_read`, `writeable_buffer`). Buffer has
            to be provided by the user, and user has to make sure appropriate
            memory is available in the application to avoid out-of-memory crash.

            Special cases:
            if the value of `bytes_to_read` is 0, it'll be interpreted as
            download all contents until the end of the file from `start_byte`.
            Examples:
                * (0, 0, buffer) : downloads 0 to end , i.e. entire object.
                * (100, 0, buffer) : downloads from 100 to end.

        :type lock: asyncio.Lock
        :param lock: (Deprecated) This parameter is deprecated and has no effect.

        :type retry_policy: :class:`~google.api_core.retry_async.AsyncRetry`
        :param retry_policy: (Optional) The retry policy to use for the operation.

        :type metadata: List[Tuple[str, str]]
        :param metadata: (Optional) The metadata to be sent with the request.

        :type enable_checksum: bool
        :param enable_checksum: (Optional) If True, checksums are verified for downloaded data. Defaults to True.

        :raises ValueError: if the underlying bidi-GRPC stream is not open.
        :raises ValueError: if the length of read_ranges is more than 1000.
        :raises DataCorruption: if a checksum mismatch is detected while reading data.

        """

        if len(read_ranges) > 1000:
            raise ValueError(
                "Invalid input - length of read_ranges cannot be more than 1000"
            )

        if enable_checksum:
            raise_if_no_fast_crc32c()

        if not self._is_stream_open:
            raise ValueError("Underlying bidi-gRPC stream is not open")

        if retry_policy is None:
            retry_policy = AsyncRetry(predicate=_is_read_retryable)

        # Initialize Global State for Retry Strategy
        download_states = {}
        for read_range in read_ranges:
            read_id = generate_random_56_bit_integer()
            # Unpack tuple into self-documenting variable names to improve readability.
            offset, length, user_buffer = read_range

            # Heuristic to detect full object reads:
            # - Implicit full object read: start offset is 0 and length is 0 (read all).
            # - Explicit full object read: start offset is 0 and length matches the exact persisted size.
            is_full_object_read = self.is_finalized and (
                (offset == 0 and length == 0)
                or (
                    self.persisted_size is not None
                    and offset == 0
                    and length == self.persisted_size
                )
            )
            download_states[read_id] = _DownloadState(
                initial_offset=offset,
                initial_length=length,
                user_buffer=user_buffer,
                is_full_object_read=is_full_object_read,
            )

        initial_state = {
            "download_states": download_states,
            "read_handle": self.read_handle,
            "routing_token": None,
            "enable_checksum": enable_checksum,
            "full_obj_server_crc32c": self.full_obj_server_crc32c
            if self.is_finalized
            else None,
        }

        read_ids = set(download_states.keys())
        queue = worker.multiplexer.register(read_ids)

        try:
            attempt_count = 0
            last_broken_generation = None

            def send_and_recv_via_multiplexer(
                requests: List[_storage_v2.ReadRange],
                state: Dict[str, Any],
            ):
                async def generator():
                    nonlocal attempt_count, last_broken_generation
                    attempt_count += 1

                    if attempt_count > 1:
                        logger.info(
                            f"Resuming download (attempt {attempt_count}) for {len(requests)} ranges."
                        )

                    # Reopen stream if needed
                    should_reopen = (
                        attempt_count > 1 and last_broken_generation is not None
                    ) or (attempt_count == 1 and metadata is not None)
                    if should_reopen:
                        broken_gen = (
                            last_broken_generation
                            if attempt_count > 1
                            else worker.multiplexer.stream_generation
                        )
                        stream_factory = self._create_stream_factory(
                            state, metadata, worker=worker
                        )
                        await worker.multiplexer.reopen_stream(
                            broken_gen, stream_factory
                        )

                    stream_generation = worker.multiplexer.stream_generation

                    # Send Requests
                    pending_read_ids = {r.read_id for r in requests}
                    for i in range(
                        0, len(requests), _MAX_READ_RANGES_PER_BIDI_READ_REQUEST
                    ):
                        batch = requests[i : i + _MAX_READ_RANGES_PER_BIDI_READ_REQUEST]
                        try:
                            await worker.multiplexer.send(
                                _storage_v2.BidiReadObjectRequest(read_ranges=batch)
                            )
                        except Exception:
                            last_broken_generation = stream_generation
                            raise

                    # Receive Responses
                    while pending_read_ids:
                        item = await queue.get()

                        if isinstance(item, _StreamEnd):
                            if pending_read_ids:
                                last_broken_generation = stream_generation
                                raise exceptions.ServiceUnavailable(
                                    "Stream ended with pending read_ids"
                                )
                            break

                        if isinstance(item, _StreamError):
                            if item.generation < stream_generation:
                                continue  # stale error, skip
                            last_broken_generation = item.generation
                            raise item.exception

                        # Track completion
                        if item.object_data_ranges:
                            for data_range in item.object_data_ranges:
                                if data_range.range_end:
                                    pending_read_ids.discard(
                                        data_range.read_range.read_id
                                    )
                        yield item

                return generator()

            strategy = _ReadResumptionStrategy()
            retry_manager = _BidiStreamRetryManager(
                strategy, send_and_recv_via_multiplexer
            )

            try:
                await retry_manager.execute(initial_state, retry_policy)
            except DataCorruption:
                if self.is_stream_open:
                    await self.close()
                raise

            if initial_state.get("read_handle"):
                self.read_handle = initial_state["read_handle"]
        finally:
            if self._multiplexer is not None:
                self._multiplexer.unregister(read_ids)
            if worker.multiplexer is not None:
                worker.multiplexer.unregister(read_ids)

    async def download_ranges(
        self,
        read_ranges: List[Tuple[int, int, BytesIO]],
        lock: asyncio.Lock = None,
        retry_policy: Optional[AsyncRetry] = None,
        metadata: Optional[List[Tuple[str, str]]] = None,
        enable_checksum: bool = True,
    ) -> None:
        """Downloads multiple byte ranges from the object into the buffers
        provided by user with automatic retries across a managed multi-stream pool.

        :type read_ranges: List[Tuple[int, int, "BytesIO"]]
        :param read_ranges: A list of tuples, where each tuple represents a
            combination of byte_range and writeable buffer in format -
            (`start_byte`, `bytes_to_read`, `writeable_buffer`). Buffer has
            to be provided by the user, and user has to make sure appropriate
            memory is available in the application to avoid out-of-memory crash.

            Special cases:
            if the value of `bytes_to_read` is 0, it'll be interpreted as
            download all contents until the end of the file from `start_byte`.
            Examples:
                * (0, 0, buffer) : downloads 0 to end , i.e. entire object.
                * (100, 0, buffer) : downloads from 100 to end.

        :type lock: asyncio.Lock
        :param lock: (Deprecated) This parameter is deprecated and has no effect.

        :type retry_policy: :class:`~google.api_core.retry_async.AsyncRetry`
        :param retry_policy: (Optional) The retry policy to use for the operation.

        :type metadata: List[Tuple[str, str]]
        :param metadata: (Optional) The metadata to be sent with the request.

        :type enable_checksum: bool
        :param enable_checksum: (Optional) If True, checksums are verified for downloaded data. Defaults to True.

        :raises ValueError: if the underlying bidi-GRPC stream is not open.
        :raises ValueError: if the length of read_ranges is more than 1000.
        :raises DataCorruption: if a checksum mismatch is detected while reading data.

        """

        if len(read_ranges) > 1000:
            raise ValueError(
                "Invalid input - length of read_ranges cannot be more than 1000"
            )

        if enable_checksum:
            raise_if_no_fast_crc32c()

        if not self._is_stream_open:
            raise ValueError("Underlying bidi-gRPC stream is not open")

        if retry_policy is None:
            retry_policy = AsyncRetry(predicate=_is_read_retryable)

        # Fallback for manually mocked tests that set mrd._multiplexer without calling open()
        if self._primary_worker is None and self.read_obj_str and self._multiplexer:
            self._primary_worker = _ManagedStream(self.read_obj_str, self._multiplexer)

        if self._pool is not None:
            total_bytes = sum(length for _, length, _ in read_ranges)
            total_ranges = len(read_ranges)
            worker = await self._pool.acquire_stream(total_ranges, total_bytes)
            try:
                await self._download_ranges_on_worker(
                    worker, read_ranges, retry_policy, metadata, enable_checksum
                )
            finally:
                self._pool.release_stream(worker, total_ranges, total_bytes)
        else:
            await self._download_ranges_on_worker(
                self._primary_worker,
                read_ranges,
                retry_policy,
                metadata,
                enable_checksum,
            )

    async def close(self):
        """
        Closes the underlying bidi-gRPC connection.
        """
        if not self._is_stream_open:
            raise ValueError("Underlying bidi-gRPC stream is not open")

        if self._pool:
            await self._pool.close()
            self._pool = None

        if self._multiplexer:
            await self._multiplexer.close()
            self._multiplexer = None

        if self.read_obj_str:
            try:
                if getattr(self.read_obj_str, "is_stream_open", True):
                    res = self.read_obj_str.close()
                    if inspect.isawaitable(res):
                        await res
            except (ValueError, asyncio.CancelledError, exceptions.GoogleAPICallError):
                pass
        self.read_obj_str = None
        self._primary_worker = None
        self._is_stream_open = False

    @property
    def is_stream_open(self) -> bool:
        return self._is_stream_open

    @property
    def object_metadata(self) -> Optional[_storage_v2.Object]:
        """The metadata of the object being downloaded."""
        return self.read_obj_str.object_metadata if self.read_obj_str else None
