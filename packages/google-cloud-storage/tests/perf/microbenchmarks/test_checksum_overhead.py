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
import statistics
import pytest

from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_multi_range_downloader import AsyncMultiRangeDownloader
from google.cloud.storage.asyncio.async_appendable_object_writer import AsyncAppendableObjectWriter

DEFAULT_BUCKET = os.environ.get("DEFAULT_RAPID_ZONAL_BUCKET", "chandrasiri-gcsfs-zb")
DEFAULT_ROUNDS = int(os.environ.get("BENCHMARK_ROUNDS", "5"))


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
    "object_size,download_size",
    [
        (1024, 1024),                  # 1KiB Full
        (1024, 1024 - 1),              # 1KiB Full-1
        (100 * 1024, 100 * 1024),      # 100KiB Full
        (100 * 1024, 100 * 1024 - 1),  # 100KiB Full-1
        (1024 * 1024, 1024 * 1024),    # 1MiB Full
        (1024 * 1024, 1024 * 1024 - 1),# 1MiB Full-1
        (16 * 1024 * 1024, 16 * 1024 * 1024),      # 16MiB Full
        (16 * 1024 * 1024, 16 * 1024 * 1024 - 1),  # 16MiB Full-1
        (100 * 1024 * 1024, 100 * 1024 * 1024),    # 100MiB Full
        (100 * 1024 * 1024, 100 * 1024 * 1024 - 1),# 100MiB Full-1
        (1024 * 1024 * 1024, 1024 * 1024 * 1024),  # 1GiB Full
        (1024 * 1024 * 1024, 1024 * 1024 * 1024 - 1),# 1GiB Full-1
    ],
    ids=[
        "1KiB-Full", "1KiB-Full-1",
        "100KiB-Full", "100KiB-Full-1",
        "1MiB-Full", "1MiB-Full-1",
        "16MiB-Full", "16MiB-Full-1",
        "100MiB-Full", "100MiB-Full-1",
        "1GiB-Full", "1GiB-Full-1"
    ],
)
@pytest.mark.parametrize("enable_checksum", [True, False], ids=["checksum_enabled", "checksum_disabled"])
def test_checksum_overhead(benchmark, object_size, download_size, enable_checksum):
    if not enable_checksum and download_size == object_size - 1:
        pytest.skip("Skip Full-1 range download when checksum is disabled")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    grpc_client = AsyncGrpcClient()

    download_bytes_list = []
    download_elapsed_times = []

    object_name = f"checksum_benchmarking_{object_size}_{uuid.uuid4().hex[:12]}"

    # 1. upload an object
    chunk_size = min(2 * 1024 * 1024, object_size)
    loop.run_until_complete(
        upload_random_object(
            grpc_client,
            DEFAULT_BUCKET,
            object_name,
            object_size,
            chunk_size,
        )
    )

    try:
        # 2. warmup
        warmup_start = time.perf_counter()
        warmup_chunk_size = min(10 * 1024 * 1024, object_size)
        while time.perf_counter() - warmup_start < 10.0:
            if object_size > warmup_chunk_size:
                start_byte = random.randint(0, object_size - warmup_chunk_size)
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
            start_time = time.perf_counter()
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
            elapsed = time.perf_counter() - start_time
            download_bytes_list.append(download_size)
            download_elapsed_times.append(elapsed)

        benchmark.pedantic(
            target=run_download,
            iterations=1,
            rounds=DEFAULT_ROUNDS,
        )

    finally:
        if download_elapsed_times:
            total_bytes = sum(download_bytes_list)
            total_time = sum(download_elapsed_times)
            throughput_mib_s = (total_bytes / total_time) / (1024 * 1024)
            benchmark.extra_info["avg_throughput_mib_s"] = f"{throughput_mib_s:.2f}"
            print(f"\nAvg Throughput: {throughput_mib_s:.2f} MiB/s")

            if len(download_elapsed_times) > 1:
                stdev_time = statistics.stdev(download_elapsed_times)
                throughputs = [download_size / t / (1024 * 1024) for t in download_elapsed_times]
                stdev_throughput = statistics.stdev(throughputs)
            else:
                stdev_time = 0.0
                stdev_throughput = 0.0

            benchmark.extra_info["stdev_throughput_mib_s"] = f"{stdev_throughput:.2f}"
            benchmark.extra_info["avg_elapsed_time_s"] = f"{total_time / len(download_elapsed_times):.4f}"
            benchmark.extra_info["stdev_elapsed_time_s"] = f"{stdev_time:.4f}"

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
