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
"""Microbenchmarks for Google Cloud Storage write operations.

This module contains performance benchmarks for various write patterns to Google Cloud Storage.
It includes three main test functions:
- `test_uploads_single_proc_single_coro`: Benchmarks uploads using a single process and a single coroutine.
- `test_uploads_single_proc_multi_coro`: Benchmarks uploads using a single process and multiple coroutines.
- `test_uploads_multi_proc_multi_coro`: Benchmarks uploads using multiple processes and multiple coroutines.

All other functions in this module are helper methods for these three tests.
"""

import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import logging

import pytest
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)

from tests.perf.microbenchmarks._utils import (
    publish_benchmark_extra_info,
    RandomBytesIO,
)
from tests.perf.microbenchmarks.conftest import publish_resource_metrics
import tests.perf.microbenchmarks.writes.config as config
from google.cloud import storage

# Get write parameters
all_params = config.get_write_params()


async def create_client():
    """Initializes async client and gets the current event loop."""
    return AsyncGrpcClient()


async def upload_chunks_using_grpc_async(client, filename, other_params):
    """Uploads a file in chunks using the gRPC API asynchronously.

    Args:
        client: The async gRPC client.
        filename (str): The name of the object to create.
        other_params: An object containing benchmark parameters like bucket_name,
                      file_size_bytes, and chunk_size_bytes.

    Returns:
        float: The total time taken for the upload in seconds.
    """
    start_time = time.monotonic_ns()

    writer = AsyncAppendableObjectWriter(
        client=client, bucket_name=other_params.bucket_name, object_name=filename
    )
    await writer.open()

    uploaded_bytes = 0
    upload_size = other_params.file_size_bytes
    chunk_size = other_params.chunk_size_bytes

    while uploaded_bytes < upload_size:
        bytes_to_upload = min(chunk_size, upload_size - uploaded_bytes)
        data = os.urandom(bytes_to_upload)
        await writer.append(data)
        uploaded_bytes += bytes_to_upload
    await writer.close()

    assert uploaded_bytes == upload_size

    end_time = time.monotonic_ns()
    elapsed_time = end_time - start_time
    return elapsed_time / 1_000_000_000


def upload_chunks_using_grpc(loop, client, filename, other_params):
    """Wrapper to run the async gRPC upload in a synchronous context.

    Args:
        loop: The asyncio event loop.
        client: The async gRPC client.
        filename (str): The name of the object to create.
        other_params: An object containing benchmark parameters.

    Returns:
        float: The total time taken for the upload in seconds.
    """
    return loop.run_until_complete(
        upload_chunks_using_grpc_async(client, filename, other_params)
    )


def upload_using_json(_, json_client, filename, other_params):
    """Uploads a file using the JSON API.

    Args:
        _ (any): Unused.
        json_client: The standard Python Storage client.
        filename (str): The name of the object to create.
        other_params: An object containing benchmark parameters like bucket_name
                      and file_size_bytes.

    Returns:
        float: The total time taken for the upload in seconds.
    """
    start_time = time.monotonic_ns()

    bucket = json_client.bucket(other_params.bucket_name)
    blob = bucket.blob(filename)
    upload_size = other_params.file_size_bytes
    # Don't use BytesIO because it'll report high memory usage for large files.
    # `RandomBytesIO` generates random bytes on the fly.
    in_mem_file = RandomBytesIO(upload_size)
    blob.upload_from_file(in_mem_file)

    end_time = time.monotonic_ns()
    elapsed_time = end_time - start_time
    return elapsed_time / 1_000_000_000


@pytest.mark.parametrize(
    "workload_params",
    all_params["write_seq"],
    indirect=True,
    ids=lambda p: p.name,
)
def test_uploads_single_proc_single_coro(
    benchmark, storage_client, blobs_to_delete, monitor, workload_params
):
    """
    Benchmarks uploads using a single process and a single coroutine.
    It passes the workload to either `upload_chunks_using_grpc` (for zonal buckets)
    or `upload_using_json` (for regional buckets) for benchmarking using `benchmark.pedantic`.
    """
    params, files_names = workload_params

    if params.bucket_type == "zonal":
        logging.info("bucket type zonal")
        target_func = upload_chunks_using_grpc
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = loop.run_until_complete(create_client())
    else:
        logging.info("bucket type regional")
        target_func = upload_using_json
        loop = None
        client = storage_client

    output_times = []

    def target_wrapper(*args, **kwargs):
        result = target_func(*args, **kwargs)
        output_times.append(result)
        return output_times

    try:
        with monitor() as m:
            output_times = benchmark.pedantic(
                target=target_wrapper,
                iterations=1,
                rounds=params.rounds,
                args=(
                    loop,
                    client,
                    files_names[0],
                    params,
                ),
            )
    finally:
        if loop is not None:
            tasks = asyncio.all_tasks(loop=loop)
            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            loop.close()
    publish_benchmark_extra_info(
        benchmark, params, benchmark_group="write", true_times=output_times
    )
    publish_resource_metrics(benchmark, m)

    blobs_to_delete.extend(
        storage_client.bucket(params.bucket_name).blob(f) for f in files_names
    )


def upload_files_using_grpc_multi_coro(loop, client, files, other_params):
    """Uploads multiple files concurrently using gRPC with asyncio.

    Args:
        loop: The asyncio event loop.
        client: The async gRPC client.
        files (list): A list of filenames to upload.
        other_params: An object containing benchmark parameters.

    Returns:
        float: The maximum latency observed among all coroutines.
    """

    async def main():
        tasks = []
        for f in files:
            tasks.append(upload_chunks_using_grpc_async(client, f, other_params))
        return await asyncio.gather(*tasks)

    results = loop.run_until_complete(main())
    return max(results)


def upload_files_using_json_multi_threaded(_, json_client, files, other_params):
    """Uploads multiple files concurrently using the JSON API with a ThreadPoolExecutor.

    Args:
        _ (any): Unused.
        json_client: The standard Python Storage client.
        files (list): A list of filenames to upload.
        other_params: An object containing benchmark parameters.

    Returns:
        float: The maximum latency observed among all concurrent uploads.
    """
    results = []
    with ThreadPoolExecutor(max_workers=other_params.num_coros) as executor:
        futures = []
        for f in files:
            future = executor.submit(
                upload_using_json, None, json_client, f, other_params
            )
            futures.append(future)

        for future in futures:
            results.append(future.result())

    return max(results)


@pytest.mark.parametrize(
    "workload_params",
    all_params["write_seq_multi_coros"],
    indirect=True,
    ids=lambda p: p.name,
)
def test_uploads_single_proc_multi_coro(
    benchmark, storage_client, blobs_to_delete, monitor, workload_params
):
    """
    Benchmarks uploads using a single process and multiple coroutines.

    For zonal buckets, it uses `upload_files_using_grpc_multi_coro` to upload
    multiple files concurrently with asyncio. For regional buckets, it uses
    `upload_files_using_json_multi_threaded` with a ThreadPoolExecutor.
    """
    params, files_names = workload_params

    if params.bucket_type == "zonal":
        logging.info("bucket type zonal")
        target_func = upload_files_using_grpc_multi_coro
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = loop.run_until_complete(create_client())
    else:
        logging.info("bucket type regional")
        target_func = upload_files_using_json_multi_threaded
        loop = None
        client = storage_client

    output_times = []

    def target_wrapper(*args, **kwargs):
        result = target_func(*args, **kwargs)
        output_times.append(result)
        return output_times

    try:
        with monitor() as m:
            output_times = benchmark.pedantic(
                target=target_wrapper,
                iterations=1,
                rounds=params.rounds,
                args=(
                    loop,
                    client,
                    files_names,
                    params,
                ),
            )
    finally:
        if loop is not None:
            tasks = asyncio.all_tasks(loop=loop)
            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            loop.close()
    publish_benchmark_extra_info(
        benchmark, params, benchmark_group="write", true_times=output_times
    )
    publish_resource_metrics(benchmark, m)

    blobs_to_delete.extend(
        storage_client.bucket(params.bucket_name).blob(f) for f in files_names
    )


def _upload_files_worker(files_to_upload, other_params, bucket_type):
    """A worker function for multi-processing uploads.

    Initializes a client and calls the appropriate multi-coroutine upload function.
    This function is intended to be called in a separate process.

    Args:
        files_to_upload (list): List of filenames for this worker to upload.
        other_params: An object containing benchmark parameters.
        bucket_type (str): The type of bucket ('zonal' or 'regional').

    Returns:
        float: The maximum latency from the uploads performed by this worker.
    """
    if bucket_type == "zonal":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = loop.run_until_complete(create_client())
        try:
            result = upload_files_using_grpc_multi_coro(
                loop, client, files_to_upload, other_params
            )
        finally:
            # cleanup loop
            tasks = asyncio.all_tasks(loop=loop)
            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            loop.close()
        return result
    else:  # regional
        json_client = storage.Client()
        return upload_files_using_json_multi_threaded(
            None, json_client, files_to_upload, other_params
        )


def upload_files_mp_mc_wrapper(files_names, params):
    """Wrapper for multi-process, multi-coroutine uploads.

    Distributes files among a pool of processes and calls the worker function.

    Args:
        files_names (list): The full list of filenames to upload.
        params: An object containing benchmark parameters (num_processes, num_coros).

    Returns:
        float: The maximum latency observed across all processes.
    """
    num_processes = params.num_processes
    num_coros = params.num_coros

    filenames_per_process = [
        files_names[i : i + num_coros] for i in range(0, len(files_names), num_coros)
    ]

    args = [
        (
            filenames,
            params,
            params.bucket_type,
        )
        for filenames in filenames_per_process
    ]

    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(processes=num_processes) as pool:
        results = pool.starmap(_upload_files_worker, args)

    return max(results)


@pytest.mark.parametrize(
    "workload_params",
    all_params["write_seq_multi_process"],
    indirect=True,
    ids=lambda p: p.name,
)
def test_uploads_multi_proc_multi_coro(
    benchmark, storage_client, blobs_to_delete, monitor, workload_params
):
    """
    Benchmarks uploads using multiple processes and multiple coroutines.

    This test distributes files among a pool of processes using `upload_files_mp_mc_wrapper`.
    The reported latency for each round is the maximum latency observed across all processes.
    """
    params, files_names = workload_params

    output_times = []

    def target_wrapper(*args, **kwargs):
        result = upload_files_mp_mc_wrapper(*args, **kwargs)
        output_times.append(result)
        return output_times

    try:
        with monitor() as m:
            output_times = benchmark.pedantic(
                target=target_wrapper,
                iterations=1,
                rounds=params.rounds,
                args=(
                    files_names,
                    params,
                ),
            )
    finally:
        publish_benchmark_extra_info(
            benchmark, params, benchmark_group="write", true_times=output_times
        )
        publish_resource_metrics(benchmark, m)

    blobs_to_delete.extend(
        storage_client.bucket(params.bucket_name).blob(f) for f in files_names
    )
