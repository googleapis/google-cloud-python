import random
import time
import grpc
import google.auth
from google.auth.transport.requests import Request
from google.auth.transport.grpc import secure_authorized_channel
from google.storage.v2 import storage_pb2, storage_pb2_grpc
import numpy as np
import asyncio
import aiohttp
import subprocess
import math

BUCKET_NAME = "projects/_/buckets/chandrasiri-benchmarks-zb"
JSON_BUCKET_NAME = "chandrasiri-benchmarks-rb"

# Fetch token once
token = subprocess.run(
    ["gcloud", "auth", "print-access-token"],
    capture_output=True,
    text=True,
    check=True,
).stdout.strip()
NUM_OBJECTS = 1


async def open_one_object_using_bidi_read_api(
    stub, bucket_name, object_name, size, chunk_size=1024 * 1024
):
    n = math.ceil(size / chunk_size)

    async def request_generator():
        my_requests = []
        for i in range(n):
            offset = i * chunk_size
            length = min(chunk_size, size - offset)
            if i == 0:
                req = storage_pb2.BidiReadObjectRequest(
                    read_object_spec=storage_pb2.BidiReadObjectSpec(
                        bucket=bucket_name, object=object_name
                    ),
                    read_ranges=[
                        storage_pb2.ReadRange(read_offset=offset, read_length=length)
                    ],
                )
            else:
                req = storage_pb2.BidiReadObjectRequest(
                    read_ranges=[
                        storage_pb2.ReadRange(read_offset=offset, read_length=length)
                    ],
                )
            my_requests.append(req)

        for req in my_requests:
            yield req

    t1 = time.perf_counter()
    response_iter = stub.BidiReadObject(
        request_generator(),
        metadata=(("x-goog-request-params", f"bucket={bucket_name}"),),
    )
    async for response in response_iter:
        pass
    t2 = time.perf_counter()
    latency = t2 - t1
    return latency


async def open_one_object_using_read_api(
    stub, bucket_name, object_name, size, chunk_size=1024 * 1024
):
    n = math.ceil(size / chunk_size)
    t1 = time.perf_counter()
    for i in range(n):
        offset = i * chunk_size
        length = min(chunk_size, size - offset)
        request = storage_pb2.ReadObjectRequest(
            bucket=bucket_name,
            object=object_name,
            read_offset=offset,
            read_limit=length,
        )
        response_iter = stub.ReadObject(
            request,
            metadata=(("x-goog-request-params", f"bucket={bucket_name}"),),
        )
        async for response in response_iter:
            pass
    t2 = time.perf_counter()
    latency = t2 - t1
    return latency


async def open_one_object_using_json_api(
    session, bucket_name, object_name, size, chunk_size=1024 * 1024
):
    n = math.ceil(size / chunk_size)
    t1 = time.perf_counter()
    for i in range(n):
        offset = i * chunk_size
        length = min(chunk_size, size - offset)
        url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}/o/{object_name}?alt=media"
        headers = {
            "Authorization": f"Bearer {token}",
            "Range": f"bytes={offset}-{offset + length - 1}",
        }
        async with session.get(url, headers=headers) as response:
            await response.read()
    t2 = time.perf_counter()
    latency = t2 - t1
    return latency


async def main(api_type):
    sizes = [
        ("1KiB", 1024),
        ("64KiB", 64 * 1024),
        ("2MiB", 2 * 1024 * 1024),
        ("16MiB", 16 * 1024 * 1024),
        ("64MiB", 64 * 1024 * 1024),
        ("100MiB", 100 * 1024 * 1024),
        ("1024MiB", 1024 * 1024 * 1024),
    ]

    async def run_benchmark(read_fn):
        print(
            f"{'API_Type':<10} {'Size':<10} {'Throughput':<12} {'Median':<10} {'Min':<10} {'Max':<10}"
        )
        print("-" * 65)
        for size_name, size_bytes in sizes:
            throughputs = []
            for _ in range(5):
                object_name = f"fio-go_storage_fio.0.{random.randint(0, 95)}"
                latency = await read_fn(object_name, size_bytes)
                # throughput in MiB/s
                throughput = (size_bytes / (1024 * 1024)) / latency
                throughputs.append(throughput)

            mean_tp = np.mean(throughputs)
            p50 = np.percentile(throughputs, 50)
            p0 = np.percentile(throughputs, 0)
            p100 = np.percentile(throughputs, 100)

            print(
                f"{api_type:<10} {size_name:<10} {mean_tp:<12.2f} {p50:<10.2f} {p0:<10.2f} {p100:<10.2f}"
            )

    if api_type == "json":
        async with aiohttp.ClientSession() as session:

            async def json_read(obj_name, size):
                return await open_one_object_using_json_api(
                    session, JSON_BUCKET_NAME, obj_name, size
                )

            await run_benchmark(json_read)

    elif api_type == "grpc":
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        auth_req = Request()
        auth_plugin = google.auth.transport.grpc.AuthMetadataPlugin(
            credentials, auth_req
        )
        google_auth_credentials = grpc.metadata_call_credentials(auth_plugin)
        channel_credentials = grpc.compute_engine_channel_credentials(
            google_auth_credentials
        )
        async with grpc.aio.secure_channel(
            "google-c2p:///storage.googleapis.com", channel_credentials
        ) as channel:
            stub = storage_pb2_grpc.StorageStub(channel)

            async def grpc_read(obj_name, size):
                return await open_one_object_using_read_api(
                    stub, BUCKET_NAME, obj_name, size
                )

            await run_benchmark(grpc_read)

    elif api_type == "grpc_bidi":
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        auth_req = Request()
        auth_plugin = google.auth.transport.grpc.AuthMetadataPlugin(
            credentials, auth_req
        )
        google_auth_credentials = grpc.metadata_call_credentials(auth_plugin)
        channel_credentials = grpc.compute_engine_channel_credentials(
            google_auth_credentials
        )
        async with grpc.aio.secure_channel(
            "google-c2p:///storage.googleapis.com", channel_credentials
        ) as channel:
            stub = storage_pb2_grpc.StorageStub(channel)

            async def grpc_bidi_read(obj_name, size):
                return await open_one_object_using_bidi_read_api(
                    stub, BUCKET_NAME, obj_name, size
                )

            await run_benchmark(grpc_bidi_read)


if __name__ == "__main__":
    asyncio.run(main(api_type="json"))
    asyncio.run(main(api_type="grpc"))
    asyncio.run(main(api_type="grpc_bidi"))
