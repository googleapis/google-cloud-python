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
"""Microbenchmarks for time-based Google Cloud Storage read operations."""

import time
import asyncio
import random
import logging
import os
import multiprocessing

import pytest

from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)
from tests.perf.microbenchmarks._utils import (
    get_irq_affinity,
    publish_benchmark_extra_info,
)
from tests.perf.microbenchmarks.conftest import (
    publish_resource_metrics,
)
from io import BytesIO
import tests.perf.microbenchmarks.time_based.reads.config as config

all_params = config._get_params()


async def create_client():
    """Initializes async client and gets the current event loop."""
    return AsyncGrpcClient()


# --- Global Variables for Worker Process ---
worker_loop = None
worker_client = None
worker_json_client = None


# TODO: b/479135274 close clients properly.
def _worker_init(bucket_type):
    """Initializes a persistent event loop and client for each worker process."""
    cpu_affinity = get_irq_affinity()
    if cpu_affinity:
        os.sched_setaffinity(
            0, {i for i in range(0, os.cpu_count()) if i not in cpu_affinity}
        )

    global worker_loop, worker_client, worker_json_client
    if bucket_type == "zonal":
        worker_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(worker_loop)
        worker_client = worker_loop.run_until_complete(create_client())
    else:  # regional
        from google.cloud import storage

        worker_json_client = storage.Client()


def _download_time_based_json(client, filename, params):
    """Performs time-based downloads using the JSON API."""
    total_bytes_downloaded = 0
    bucket = client.bucket(params.bucket_name)
    blob = bucket.blob(filename)

    offset = 0
    is_warming_up = True
    start_time = time.monotonic()
    warmup_end_time = start_time + params.warmup_duration
    test_end_time = warmup_end_time + params.duration

    while time.monotonic() < test_end_time:
        current_time = time.monotonic()
        if is_warming_up and current_time >= warmup_end_time:
            is_warming_up = False
            total_bytes_downloaded = 0  # Reset counter after warmup

        bytes_in_iteration = 0
        # For JSON, we can't batch ranges like gRPC, so we download one by one
        for _ in range(params.num_ranges):
            if params.pattern == "rand":
                offset = random.randint(
                    0, params.file_size_bytes - params.chunk_size_bytes
                )

            data = blob.download_as_bytes(
                start=offset, end=offset + params.chunk_size_bytes - 1
            )
            bytes_in_iteration += len(data)

            if params.pattern == "seq":
                offset += params.chunk_size_bytes
                if offset + params.chunk_size_bytes > params.file_size_bytes:
                    offset = 0

        assert bytes_in_iteration == params.chunk_size_bytes * params.num_ranges

        if not is_warming_up:
            total_bytes_downloaded += bytes_in_iteration

    return total_bytes_downloaded


async def _download_time_based_async(client, filename, params):
    total_bytes_downloaded = 0

    mrd = AsyncMultiRangeDownloader(client, params.bucket_name, filename)
    await mrd.open()

    offset = 0
    is_warming_up = True
    start_time = time.monotonic()
    warmup_end_time = start_time + params.warmup_duration
    test_end_time = warmup_end_time + params.duration

    while time.monotonic() < test_end_time:
        current_time = time.monotonic()
        if is_warming_up and current_time >= warmup_end_time:
            is_warming_up = False
            total_bytes_downloaded = 0  # Reset counter after warmup

        ranges = []
        if params.pattern == "rand":
            for _ in range(params.num_ranges):
                offset = random.randint(
                    0, params.file_size_bytes - params.chunk_size_bytes
                )
                ranges.append((offset, params.chunk_size_bytes, BytesIO()))
        else:  # seq
            for _ in range(params.num_ranges):
                ranges.append((offset, params.chunk_size_bytes, BytesIO()))
                offset += params.chunk_size_bytes
                if offset + params.chunk_size_bytes > params.file_size_bytes:
                    offset = 0  # Reset offset if end of file is reached

        await mrd.download_ranges(ranges)

        bytes_in_buffers = sum(r[2].getbuffer().nbytes for r in ranges)
        assert bytes_in_buffers == params.chunk_size_bytes * params.num_ranges

        if not is_warming_up:
            total_bytes_downloaded += params.chunk_size_bytes * params.num_ranges

    await mrd.close()
    return total_bytes_downloaded


def _download_files_worker(process_idx, filename, params, bucket_type):

    if bucket_type == "zonal":
        return worker_loop.run_until_complete(
            _download_time_based_async(worker_client, filename, params)
        )
    else:  # regional
        return _download_time_based_json(worker_json_client, filename, params)


def download_files_mp_mc_wrapper(pool, files_names, params, bucket_type):
    args = [(i, files_names[i], params, bucket_type) for i in range(len(files_names))]

    results = pool.starmap(_download_files_worker, args)
    return sum(results)


@pytest.mark.parametrize(
    "workload_params",
    all_params["read_seq_multi_process"] + all_params["read_rand_multi_process"],
    indirect=True,
    ids=lambda p: p.name,
)
def test_downloads_multi_proc_multi_coro(
    benchmark, storage_client, monitor, workload_params
):
    params, files_names = workload_params
    logging.info(f"num files: {len(files_names)}")

    ctx = multiprocessing.get_context("spawn")
    pool = ctx.Pool(
        processes=params.num_processes,
        initializer=_worker_init,
        initargs=(params.bucket_type,),
    )

    download_bytes_list = []

    def target_wrapper(*args, **kwargs):
        download_bytes_list.append(download_files_mp_mc_wrapper(pool, *args, **kwargs))
        return

    try:
        with monitor() as m:
            benchmark.pedantic(
                target=target_wrapper,
                iterations=1,
                rounds=params.rounds,
                args=(files_names, params, params.bucket_type),
            )
    finally:
        pool.close()
        pool.join()
        total_bytes_downloaded = sum(download_bytes_list)
        throughput_mib_s = (
            total_bytes_downloaded / params.duration / params.rounds
        ) / (1024 * 1024)
        benchmark.extra_info["avg_throughput_mib_s"] = f"{throughput_mib_s:.2f}"
        print(
            f"Avg Throughput of {params.rounds} round(s): {throughput_mib_s:.2f} MiB/s"
        )
        publish_benchmark_extra_info(
            benchmark,
            params,
            download_bytes_list=download_bytes_list,
            duration=params.duration,
        )
        publish_resource_metrics(benchmark, m)
