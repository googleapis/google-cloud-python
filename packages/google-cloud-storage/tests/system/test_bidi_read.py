# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from io import BytesIO
import os
import uuid
import pytest

from google.api_core import exceptions
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import NotFound, OutOfRange
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_appendable_object_writer import AsyncAppendableObjectWriter
from google.cloud.storage.asyncio.async_multi_range_downloader import AsyncMultiRangeDownloader

REGIONAL_RAPID_BUCKET = "java-storage-reg-rapid-preprod-3fe2bb58"
PREPROD_ENDPOINT = "storage-preprod-test-grpc.googleusercontent.com:443"

# Parameterize over LocationType
@pytest.fixture(scope="module", params=["REGIONAL_RAPID"])
def bidi_location_type(request):
    return request.param

@pytest.fixture(scope="module")
def grpc_client(bidi_location_type):
    if bidi_location_type == "REGIONAL_RAPID":
        options = ClientOptions(api_endpoint=PREPROD_ENDPOINT)
        return AsyncGrpcClient(client_options=options)
    else:
        return AsyncGrpcClient()

@pytest.fixture(scope="module")
def bidi_bucket(bidi_location_type):
    if bidi_location_type == "REGIONAL_RAPID":
        return REGIONAL_RAPID_BUCKET
    elif bidi_location_type == "ZONAL_RAPID":
        zonal_bucket = os.getenv("ZONAL_BUCKET")
        if not zonal_bucket:
            pytest.skip("ZONAL_BUCKET env var not set")
        return zonal_bucket
    else:
        pytest.fail(f"Unsupported location type: {bidi_location_type}")

async def create_object(grpc_client, bucket, object_name, data):
    writer = AsyncAppendableObjectWriter(grpc_client, bucket, object_name)
    await writer.open()
    await writer.append(data)
    await writer.close(finalize_on_close=True)

# Module-level dictionary to store pre-created object info
OBJECTS = {}

@pytest.fixture(scope="module", autouse=True)
async def setup_bidi_read_objects(grpc_client, bidi_bucket, bidi_location_type):
    global OBJECTS
    OBJECTS = {
        "large": {
            "name": f"test_read_close_{uuid.uuid4()}",
            "data": os.urandom(5 * 1024 * 1024)
        },
        "zero_copy": {
            "name": f"test_zero_copy_{uuid.uuid4()}",
            "data": os.urandom(1024 * 1024)
        },
        "multi_range": {
            "name": f"test_multi_range_{uuid.uuid4()}",
            "data": os.urandom(1024 * 1024)
        },
        "oob": {
            "name": f"test_oob_{uuid.uuid4()}",
            "data": os.urandom(1024 * 1024)
        }
    }
    
    # Create all objects
    for obj_info in OBJECTS.values():
        await create_object(grpc_client, bidi_bucket, obj_info["name"], obj_info["data"])
        
    if bidi_location_type == "REGIONAL_RAPID":
        # Trigger Ingest-on-Read by doing a small read (1 byte) on each
        for obj_info in OBJECTS.values():
            async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, obj_info["name"]) as mrd:
                buf = BytesIO()
                await mrd.download_ranges([(0, 1, buf)])
                
        # Sleep for 30 minutes
        print("Sleeping for 30 minutes to allow RCU ingestion...")
        await asyncio.sleep(1800)
        print("Woke up from RCU ingestion sleep.")
        
    yield
    
    # Teardown: delete all objects
    for obj_info in OBJECTS.values():
        try:
            await grpc_client.delete_object(bidi_bucket, obj_info["name"])
        except Exception:
            pass

# ----------------- Read Tests -----------------

@pytest.mark.asyncio
async def test_read_post_stream_close(grpc_client, bidi_bucket):
    obj_info = OBJECTS["large"]
    object_name = obj_info["name"]

    mrd = await AsyncMultiRangeDownloader.create_mrd(grpc_client, bidi_bucket, object_name)
    buffer = BytesIO()

    # Start download in background
    task = asyncio.create_task(mrd.download_ranges([(0, 0, buffer)]))

    # Wait a bit to ensure it started
    await asyncio.sleep(0.1)

    # Close the downloader mid-stream
    await mrd.close()

    # Awaiting the task should raise an exception
    with pytest.raises(Exception) as excinfo:
        await task

    assert isinstance(excinfo.value, (exceptions.ServiceUnavailable, asyncio.CancelledError))


@pytest.mark.asyncio
async def test_zero_copy_range_reads(grpc_client, bidi_bucket):
    obj_info = OBJECTS["zero_copy"]
    object_name = obj_info["name"]
    data = obj_info["data"]

    # Define ranges
    r1 = (0, 1000)
    r2 = (50000, 250000)
    r3 = (800000, 10000)

    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        buf1 = BytesIO()
        buf2 = BytesIO()
        buf3 = BytesIO()

        # Concurrent downloads
        t1 = asyncio.create_task(mrd.download_ranges([(r1[0], r1[1], buf1)]))
        t2 = asyncio.create_task(mrd.download_ranges([(r2[0], r2[1], buf2)]))
        t3 = asyncio.create_task(mrd.download_ranges([(r3[0], r3[1], buf3)]))

        await asyncio.gather(t1, t2, t3)

        assert buf1.getvalue() == data[r1[0] : r1[0] + r1[1]]
        assert buf2.getvalue() == data[r2[0] : r2[0] + r2[1]]
        assert buf3.getvalue() == data[r3[0] : r3[0] + r3[1]]


@pytest.mark.asyncio
async def test_multiple_ranged_read(grpc_client, bidi_bucket):
    obj_info = OBJECTS["multi_range"]
    object_name = obj_info["name"]
    data = obj_info["data"]

    r1 = (0, 1000)
    r2 = (50000, 250000)

    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        buf1 = BytesIO()
        buf2 = BytesIO()

        await mrd.download_ranges([
            (r1[0], r1[1], buf1),
            (r2[0], r2[1], buf2)
        ])

        assert buf1.getvalue() == data[r1[0] : r1[0] + r1[1]]
        assert buf2.getvalue() == data[r2[0] : r2[0] + r2[1]]


@pytest.mark.asyncio
async def test_read_from_non_existent_bucket_fails(grpc_client):
    bad_bucket_name = f"non-existent-bucket-{uuid.uuid4()}"
    
    with pytest.raises(NotFound) as excinfo:
        await AsyncMultiRangeDownloader.create_mrd(grpc_client, bad_bucket_name, "some-object")
    
    assert excinfo.value.code == 404


@pytest.mark.asyncio
async def test_read_out_of_range(grpc_client, bidi_bucket):
    obj_info = OBJECTS["oob"]
    object_name = obj_info["name"]
    data = obj_info["data"]
    object_size = len(data)

    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        valid_buffer = BytesIO()
        valid_task = asyncio.create_task(
            mrd.download_ranges([(0, 100, valid_buffer)])
        )

        oob_buffer = BytesIO()
        oob_task = asyncio.create_task(
            mrd.download_ranges([(object_size + 1000, 100, oob_buffer)])
        )

        results = await asyncio.gather(valid_task, oob_task, return_exceptions=True)

        assert valid_buffer.getvalue() == data[:100]
        assert isinstance(results[1], OutOfRange)
