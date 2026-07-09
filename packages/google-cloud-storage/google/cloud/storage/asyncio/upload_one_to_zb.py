#!/usr/bin/env python

# Copyright 2026 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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
import os
import time
import argparse
import asyncio
import numpy as np

from google.cloud.storage.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
import uuid


# [START storage_finalize_appendable_object_upload]
async def storage_finalize_appendable_object_upload(
    bucket_name, object_name, grpc_client=None, iters=100
):
    """Creates, writes to, and finalizes an appendable object.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """
    if grpc_client is None:
        grpc_client = AsyncGrpcClient()
    # random_data = os.urandom(200*10**6)
    with open(args.file_to_upload, "rb") as fp:
        random_data = fp.read()

    full_times = []
    open_times = []
    append_times = []
    close_times = []
    for i in range(iters):
        object_name_final = f"upload_perf_{str(uuid.uuid4())}"
        t1 = time.monotonic_ns()
        writer = AsyncAppendableObjectWriter(
            client=grpc_client,
            bucket_name=bucket_name,
            object_name=object_name_final,
            # generation=0,  # throws `FailedPrecondition` if object already exists.
        )
        # This creates a new appendable object of size 0 and opens it for appending.
        t_open_start = time.monotonic_ns()
        await writer.open()
        t_open_end = time.monotonic_ns()
        open_times.append((t_open_end - t_open_start) / 10**6)

        # Appends data to the object.
        t_append_start = time.monotonic_ns()
        await writer.append(random_data)
        t_append_end = time.monotonic_ns()
        append_times.append((t_append_end - t_append_start) / 10**6)

        # finalize the appendable object,
        # NOTE:
        # 1. once finalized no more appends can be done to the object.
        # 2. If you don't want to finalize, you can simply call `writer.close`
        # 3. calling `.finalize()` also closes the grpc-bidi stream, calling
        #   `.close` after `.finalize` may lead to undefined behavior.
        t_close_start = time.monotonic_ns()
        object_resource = await writer.close(
            finalize_on_close=True, full_object_checksum=2745245464
        )
        # print(object_resource)
        t_close_end = time.monotonic_ns()
        close_times.append((t_close_end - t_close_start) / 10**6)

        t2 = time.monotonic_ns()
        full_times.append((t2 - t1) / 10**6)
        if i % 20 == 0:
            print(f"Appendable object - {i} {object_name_final} created and finalized.")
        # print("Object Metadata:")
        # print(object_resource)
        await grpc_client.delete_object(bucket_name, object_name_final)

    def print_percentiles(name, times):
        print(f"=== {name} (ms) ===")
        print("percentile 50:  ", np.percentile(times, 50))
        print("percentile 95:  ", np.percentile(times, 95))
        print("percentile 99:  ", np.percentile(times, 99))
        print("percentile 100: ", np.percentile(times, 100))

    print_percentiles("FULL UPLOAD", full_times)
    print_percentiles("WRITER OPEN", open_times)
    print_percentiles("WRITER APPEND", append_times)
    print_percentiles("WRITER CLOSE", close_times)


# [END storage_finalize_appendable_object_upload]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bucket_name", help="Your Cloud Storage bucket name.")
    parser.add_argument("--object_name", help="Your Cloud Storage object name.")
    parser.add_argument("--file_to_upload", help="Your Cloud Storage object name.")
    parser.add_argument("--iters", default=1, type=int)

    args = parser.parse_args()

    asyncio.run(
        storage_finalize_appendable_object_upload(
            bucket_name=args.bucket_name, object_name=args.object_name, iters=args.iters
        )
    )
