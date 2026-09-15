#!/usr/bin/env python3
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

"""Pre-seeds test objects in Google Cloud Storage for microbenchmarks."""

import argparse
import asyncio
import concurrent.futures
import os
import sys
import time

from google.cloud import storage
from google.cloud.storage.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient


def check_object(bucket: storage.Bucket, idx: int, expected_size: int):
    """Checks if an object exists and has the expected size."""
    obj_name = f"fio-go_storage_fio.0.{idx}"
    try:
        blob = bucket.get_blob(obj_name)
        if blob and blob.size == expected_size:
            return None
    except Exception as e:
        print(f"Error checking {obj_name}: {e}", file=sys.stderr)
    return idx


async def upload_object(
    bucket_name: str,
    idx: int,
    expected_size: int,
    file_size_mib: int,
    sem: asyncio.Semaphore,
):
    """Uploads a single appendable object using gRPC DirectPath."""
    async with sem:
        obj_name = f"fio-go_storage_fio.0.{idx}"
        t0 = time.time()
        print(
            f"Uploading {obj_name} ({file_size_mib} MiB) via gRPC appendable writer...",
            flush=True,
        )
        writer = AsyncAppendableObjectWriter(
            AsyncGrpcClient(),
            bucket_name,
            obj_name,
            writer_options={"FLUSH_INTERVAL_BYTES": 1026 * 1024**2},
        )
        await writer.open()
        uploaded = 0
        chunk_size = 64 * 1024 * 1024  # 64 MiB buffer
        chunk_data = os.urandom(chunk_size)
        while uploaded < expected_size:
            to_upload = min(chunk_size, expected_size - uploaded)
            if to_upload == chunk_size:
                await writer.append(chunk_data)
            else:
                await writer.append(chunk_data[:to_upload])
            uploaded += to_upload
        await writer.close(finalize_on_close=True)
        print(f"Uploaded {obj_name} in {time.time() - t0:.1f}s", flush=True)


async def upload_all_missing(
    bucket_name: str,
    missing_indices: list,
    expected_size: int,
    file_size_mib: int,
    concurrency: int = 16,
):
    """Uploads all missing objects concurrently using asyncio and gRPC."""
    sem = asyncio.Semaphore(concurrency)
    tasks = [
        upload_object(bucket_name, idx, expected_size, file_size_mib, sem)
        for idx in missing_indices
    ]
    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description="Pre-seed GCS benchmark objects")
    parser.add_argument("--bucket", required=True, help="Target GCS bucket name")
    parser.add_argument(
        "--file-size-mib",
        type=int,
        default=10240,
        help="Expected size per file in MiB",
    )
    parser.add_argument(
        "--num-objects",
        type=int,
        default=48,
        help="Number of benchmark objects to verify/seed",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=16,
        help="Concurrent upload streams",
    )
    args = parser.parse_args()

    expected_size = args.file_size_mib * 1024 * 1024
    print(
        f"Verifying {args.num_objects} objects ({args.file_size_mib} MiB each) in gs://{args.bucket}...",
        flush=True,
    )

    client = storage.Client()
    bucket = client.bucket(args.bucket)

    # Use ThreadPoolExecutor to check object metadata concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        futures = [
            executor.submit(check_object, bucket, i, expected_size)
            for i in range(args.num_objects)
        ]
        missing_indices = [
            f.result() for f in concurrent.futures.as_completed(futures) if f.result() is not None
        ]

    missing_indices.sort()

    if missing_indices:
        print(
            f"Found {len(missing_indices)} missing objects. Seeding via gRPC DirectPath...",
            flush=True,
        )
        asyncio.run(
            upload_all_missing(
                args.bucket,
                missing_indices,
                expected_size,
                args.file_size_mib,
                concurrency=args.concurrency,
            )
        )
        print("All test objects successfully seeded.", flush=True)
    else:
        print("All test objects already exist. Skipping pre-seeding.", flush=True)


if __name__ == "__main__":
    main()
