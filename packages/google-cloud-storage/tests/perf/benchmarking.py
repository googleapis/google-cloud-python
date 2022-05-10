# Copyright 2022 Google LLC
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

"""Performance benchmarking script. This is not an officially supported Google product."""

import argparse
import csv
import logging
import multiprocessing
import os
import random
import time
import uuid

from functools import partial, update_wrapper

from google.cloud import storage


##### DEFAULTS & CONSTANTS #####
HEADER = [
    "Op",
    "ObjectSize",
    "AppBufferSize",
    "LibBufferSize",
    "Crc32cEnabled",
    "MD5Enabled",
    "ApiName",
    "ElapsedTimeUs",
    "CpuTimeUs",
    "Status",
    "RunID",
]
CHECKSUM = ["md5", "crc32c", None]
TIMESTAMP = time.strftime("%Y%m%d-%H%M%S")
DEFAULT_API = "JSON"
DEFAULT_BUCKET_LOCATION = "US"
DEFAULT_MIN_SIZE = 5120  # 5 KiB
DEFAULT_MAX_SIZE = 2147483648  # 2 GiB
DEFAULT_NUM_SAMPLES = 1000
DEFAULT_NUM_PROCESSES = 16
DEFAULT_LIB_BUFFER_SIZE = 104857600  # https://github.com/googleapis/python-storage/blob/main/google/cloud/storage/blob.py#L135
NOT_SUPPORTED = -1


def log_performance(func):
    """Log latency and throughput output per operation call."""
    # Holds benchmarking results for each operation
    res = {
        "ApiName": DEFAULT_API,
        "RunID": TIMESTAMP,
        "CpuTimeUs": NOT_SUPPORTED,
        "AppBufferSize": NOT_SUPPORTED,
        "LibBufferSize": DEFAULT_LIB_BUFFER_SIZE,
    }

    try:
        elapsed_time = func()
    except Exception as e:
        logging.exception(
            f"Caught an exception while running operation {func.__name__}\n {e}"
        )
        res["Status"] = ["FAIL"]
        elapsed_time = NOT_SUPPORTED
    else:
        res["Status"] = ["OK"]

    checksum = func.keywords.get("checksum")
    num = func.keywords.get("num", None)
    res["ElapsedTimeUs"] = elapsed_time
    res["ObjectSize"] = func.keywords.get("size")
    res["Crc32cEnabled"] = checksum == "crc32c"
    res["MD5Enabled"] = checksum == "md5"
    res["Op"] = func.__name__
    if res["Op"] == "READ":
        res["Op"] += f"[{num}]"

    return [
        res["Op"],
        res["ObjectSize"],
        res["AppBufferSize"],
        res["LibBufferSize"],
        res["Crc32cEnabled"],
        res["MD5Enabled"],
        res["ApiName"],
        res["ElapsedTimeUs"],
        res["CpuTimeUs"],
        res["Status"],
        res["RunID"],
    ]


def WRITE(bucket, blob_name, checksum, size, **kwargs):
    """Perform an upload and return latency."""
    blob = bucket.blob(blob_name)
    file_path = f"{os.getcwd()}/{uuid.uuid4().hex}"
    # Create random file locally on disk
    with open(file_path, "wb") as file_obj:
        file_obj.write(os.urandom(size))

    start_time = time.monotonic_ns()
    blob.upload_from_filename(file_path, checksum=checksum, if_generation_match=0)
    end_time = time.monotonic_ns()

    elapsed_time = round(
        (end_time - start_time) / 1000
    )  # convert nanoseconds to microseconds

    # Clean up local file
    cleanup_file(file_path)

    return elapsed_time


def READ(bucket, blob_name, checksum, **kwargs):
    """Perform a download and return latency."""
    blob = bucket.blob(blob_name)
    if not blob.exists():
        raise Exception("Blob does not exist. Previous WRITE failed.")

    file_path = f"{os.getcwd()}/{blob_name}"
    with open(file_path, "wb") as file_obj:
        start_time = time.monotonic_ns()
        blob.download_to_file(file_obj, checksum=checksum)
        end_time = time.monotonic_ns()

    elapsed_time = round(
        (end_time - start_time) / 1000
    )  # convert nanoseconds to microseconds

    # Clean up local file
    cleanup_file(file_path)

    return elapsed_time


def cleanup_file(file_path):
    """Clean up local file on disk."""
    try:
        os.remove(file_path)
    except Exception as e:
        logging.exception(f"Caught an exception while deleting local file\n {e}")


def _wrapped_partial(func, *args, **kwargs):
    """Helper method to create partial and propagate function name and doc from original function."""
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func


def _generate_func_list(bucket_name, min_size, max_size):
    """Generate Write-1-Read-3 workload."""
    # generate randmon size in bytes using a uniform distribution
    size = random.randrange(min_size, max_size)
    blob_name = f"{TIMESTAMP}-{uuid.uuid4().hex}"

    # generate random checksumming type: md5, crc32c or None
    idx_checksum = random.choice([0, 1, 2])
    checksum = CHECKSUM[idx_checksum]

    func_list = [
        _wrapped_partial(
            WRITE,
            storage.Client().bucket(bucket_name),
            blob_name,
            size=size,
            checksum=checksum,
        ),
        *[
            _wrapped_partial(
                READ,
                storage.Client().bucket(bucket_name),
                blob_name,
                size=size,
                checksum=checksum,
                num=i,
            )
            for i in range(3)
        ],
    ]
    return func_list


def benchmark_runner(args):
    """Run benchmarking iterations."""
    results = []
    for func in _generate_func_list(args.b, args.min_size, args.max_size):
        results.append(log_performance(func))

    return results


def main(args):
    # Create a storage bucket to run benchmarking
    client = storage.Client()
    if not client.bucket(args.b).exists():
        bucket = client.create_bucket(args.b, location=args.r)

    # Launch benchmark_runner using multiprocessing
    p = multiprocessing.Pool(args.p)
    pool_output = p.map(benchmark_runner, [args for _ in range(args.num_samples)])

    # Output to CSV file
    with open(args.o, "w") as file:
        writer = csv.writer(file)
        writer.writerow(HEADER)
        for result in pool_output:
            for row in result:
                writer.writerow(row)
    print(f"Succesfully ran benchmarking. Please find your output log at {args.o}")

    # Cleanup and delete bucket
    try:
        bucket.delete(force=True)
    except Exception as e:
        logging.exception(f"Caught an exception while deleting bucket\n {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--min_size",
        type=int,
        default=DEFAULT_MIN_SIZE,
        help="Minimum object size in bytes",
    )
    parser.add_argument(
        "--max_size",
        type=int,
        default=DEFAULT_MAX_SIZE,
        help="Maximum object size in bytes",
    )
    parser.add_argument(
        "--num_samples",
        type=int,
        default=DEFAULT_NUM_SAMPLES,
        help="Number of iterations",
    )
    parser.add_argument(
        "--p",
        type=int,
        default=DEFAULT_NUM_PROCESSES,
        help="Number of processes- multiprocessing enabled",
    )
    parser.add_argument(
        "--r", type=str, default=DEFAULT_BUCKET_LOCATION, help="Bucket location"
    )
    parser.add_argument(
        "--o",
        type=str,
        default=f"benchmarking{TIMESTAMP}.csv",
        help="File to output results to",
    )
    parser.add_argument(
        "--b",
        type=str,
        default=f"benchmarking{TIMESTAMP}",
        help="Storage bucket name",
    )
    args = parser.parse_args()

    main(args)
