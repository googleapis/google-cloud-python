# Copyright 2026 Google LLC
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

import asyncio
import os
import random
import time
import uuid
import pytest

from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_multi_range_downloader import AsyncMultiRangeDownloader
from google.cloud.storage.asyncio.async_appendable_object_writer import AsyncAppendableObjectWriter

DEFAULT_BUCKET = os.environ.get("DEFAULT_RAPID_ZONAL_BUCKET", "chandrasiri-benchmarks-zb")


class VoidBuffer:
    """A writeable file-like object that discards written data to save memory."""
    def __init__(self):
        self.size = 0

    def write(self, data: bytes) -> int:
        n = len(data)
        self.size += n
        return n

    def tell(self) -> int:
        return self.size


async def download_range(
    grpc_client: AsyncGrpcClient,
    bucket_name: str,
    object_name: str,
    start_byte: int,
    size: int,
    enable_checksum: bool,
):
    mrd = AsyncMultiRangeDownloader(grpc_client, bucket_name, object_name)
    try:
        await mrd.open()
        output_buffer = VoidBuffer()
        await mrd.download_ranges(
            [(start_byte, size, output_buffer)],
            enable_checksum=enable_checksum,
        )
    finally:
        if mrd.is_stream_open:
            await mrd.close()


async def upload_random_object(
    grpc_client: AsyncGrpcClient,
    bucket_name: str,
    object_name: str,
    total_size_bytes: int,
    chunk_size_bytes: int = 2 * 1024 * 1024,
):
    writer = AsyncAppendableObjectWriter(
        client=grpc_client,
        bucket_name=bucket_name,
        object_name=object_name,
        generation=0,
    )
    await writer.open()
    uploaded_bytes = 0
    buffer_size = min(10 * 1024 * 1024, total_size_bytes)
    random_buffer = os.urandom(buffer_size)
    while uploaded_bytes < total_size_bytes:
        bytes_to_write = min(chunk_size_bytes, total_size_bytes - uploaded_bytes)
        slice_start = (uploaded_bytes) % (buffer_size - bytes_to_write + 1)
        data = random_buffer[slice_start : slice_start + bytes_to_write]
        await writer.append(data)
        uploaded_bytes += bytes_to_write
    await writer.finalize()


@pytest.mark.parametrize(
    "download_size",
    [
        1024,                  # 1KiB
        100 * 1024,            # 100KiB
        1024 * 1024,           # 1MiB
        16 * 1024 * 1024,      # 16MiB
        100 * 1024 * 1024,     # 100MiB
        1024 * 1024 * 1024,    # 1GiB
    ],
    ids=["1KiB", "100KiB", "1MiB", "16MiB", "100MiB", "1GiB"],
)
@pytest.mark.parametrize("enable_checksum", [True, False], ids=["checksum_enabled", "checksum_disabled"])
def test_checksum_overhead(benchmark, download_size, enable_checksum):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    grpc_client = AsyncGrpcClient()

    object_name = f"checksum_benchmarking_{download_size}_{uuid.uuid4().hex[:12]}"

    # 1. upload an object
    chunk_size = min(2 * 1024 * 1024, download_size)
    loop.run_until_complete(
        upload_random_object(
            grpc_client,
            DEFAULT_BUCKET,
            object_name,
            download_size,
            chunk_size,
        )
    )

    try:
        # 2. warmup
        warmup_start = time.perf_counter()
        warmup_chunk_size = min(10 * 1024 * 1024, download_size)
        while time.perf_counter() - warmup_start < 10.0:
            if download_size > warmup_chunk_size:
                start_byte = random.randint(0, download_size - warmup_chunk_size)
            else:
                start_byte = 0
            try:
                loop.run_until_complete(
                    download_range(
                        grpc_client,
                        DEFAULT_BUCKET,
                        object_name,
                        start_byte,
                        warmup_chunk_size,
                        enable_checksum,
                    )
                )
            except Exception:
                pass

        # 3. download range (0, download_size) for 5 rounds
        def run_download():
            loop.run_until_complete(
                download_range(
                    grpc_client,
                    DEFAULT_BUCKET,
                    object_name,
                    0,
                    download_size,
                    enable_checksum,
                )
            )

        benchmark.pedantic(
            target=run_download,
            iterations=1,
            rounds=5,
        )

    finally:
        # 4. delete the object
        try:
            loop.run_until_complete(grpc_client.delete_object(DEFAULT_BUCKET, object_name))
        except Exception:
            pass

        tasks = asyncio.all_tasks(loop=loop)
        for task in tasks:
            task.cancel()
        if tasks:
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        loop.close()
