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
import google_crc32c

from google.api_core import exceptions
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import NotFound, OutOfRange, InvalidArgument
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_appendable_object_writer import AsyncAppendableObjectWriter
from google.cloud.storage.asyncio.async_multi_range_downloader import AsyncMultiRangeDownloader

REGIONAL_RAPID_BUCKET = "java-storage-reg-rapid-preprod-3fe2bb58"
PREPROD_ENDPOINT = "storage-preprod-test-grpc.googleusercontent.com:443"

# We parameterized the tests to run against REGIONAL_RAPID for now.
# We can expand to others if needed.
@pytest.fixture(scope="module")
def bidi_location_type():
    return "REGIONAL_RAPID"

@pytest.fixture(scope="module")
def grpc_client(bidi_location_type):
    if bidi_location_type == "REGIONAL_RAPID":
        # Point to preprod endpoint
        options = ClientOptions(api_endpoint=PREPROD_ENDPOINT)
        return AsyncGrpcClient(client_options=options)
    else:
        return AsyncGrpcClient()

@pytest.fixture(scope="module")
def bidi_bucket(bidi_location_type):
    if bidi_location_type == "REGIONAL_RAPID":
        # Shared pre-created bucket
        return REGIONAL_RAPID_BUCKET
    elif bidi_location_type == "ZONAL_RAPID":
        zonal_bucket = os.getenv("ZONAL_BUCKET")
        if not zonal_bucket:
            pytest.skip("ZONAL_BUCKET env var not set")
        return zonal_bucket
    else:
        pytest.fail(f"Unsupported location type: {bidi_location_type}")

# Helper to create objects using sync client if needed,
# but using AsyncAppendableObjectWriter is also fine.
# We will use sync client from conftest if available, but it points to Prod.
# For preprod, we need to initialize a sync client pointing to preprod if we want to use it.
# Actually, we can just use AsyncAppendableObjectWriter to create objects for read tests.
async def create_object(grpc_client, bucket, object_name, data):
    writer = AsyncAppendableObjectWriter(grpc_client, bucket, object_name)
    await writer.open()
    await writer.append(data)
    await writer.close(finalize_on_close=True)

# ----------------- Write Tests -----------------

@pytest.mark.asyncio
async def test_appendable_upload_empty_object(grpc_client, bidi_bucket):
    object_name = f"test_empty_{uuid.uuid4()}"
    
    writer = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer.open()
    object_metadata = await writer.close(finalize_on_close=True)

    # Register for deletion (using sync client, it should work if it can access the bucket,
    # but sync client might be pointing to Prod. Wait, if sync client is pointing to Prod,
    # it won't be able to delete from pre-prod bucket unless we configure it or if the credential
    # has access. The bucket is in 'gcs-hyd-connector-benchmarks' project.
    # If standard client has access to it, it should work.
    # Wait, the sync client in conftest uses default project.
    # If we need to delete it from preprod, maybe we should delete it using grpc_client?
    # AsyncGrpcClient has delete_object!
    # Let's check:
    # await grpc_client.delete_object(bidi_bucket, object_name)
    # Yes, we can do that.
    # So we can manually delete it or use a cleanup helper.
    # Let's register it for deletion using a custom cleanup list.
    
    assert object_metadata.size == 0
    assert int(object_metadata.checksums.crc32c) == int(google_crc32c.value(b""))

    # Read back and verify empty
    buffer = BytesIO()
    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        await mrd.download_ranges([(0, 0, buffer)])
    assert buffer.getvalue() == b""

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_appendable_upload_bytes(grpc_client, bidi_bucket):
    object_name = f"test_bytes_{uuid.uuid4()}"
    data = os.urandom(1000)
    mid = len(data) // 2
    chunk1 = data[:mid]
    chunk2 = data[mid:]

    writer = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer.open()
    await writer.append(chunk1)
    await writer.append(chunk2)
    object_metadata = await writer.close(finalize_on_close=True)

    assert object_metadata.size == len(data)
    expected_crc = google_crc32c.value(data)
    assert int(object_metadata.checksums.crc32c) == expected_crc

    # Read back and verify
    buffer = BytesIO()
    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        await mrd.download_ranges([(0, 0, buffer)])
    assert buffer.getvalue() == data

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_explicit_flush(grpc_client, bidi_bucket):
    object_name = f"test_flush_{uuid.uuid4()}"
    data = os.urandom(1000)
    mid = len(data) // 2
    chunk1 = data[:mid]
    chunk2 = data[mid:]

    writer = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer.open()
    await writer.append(chunk1)
    await writer.flush()  # Explicit flush
    await writer.append(chunk2)
    await writer.close(finalize_on_close=True)

    # Read back and verify
    buffer = BytesIO()
    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        await mrd.download_ranges([(0, 0, buffer)])
    assert buffer.getvalue() == data

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_appendable_blob_upload_takeover(grpc_client, bidi_bucket):
    object_name = f"test_takeover_{uuid.uuid4()}"
    data = os.urandom(1000)
    mid = len(data) // 2
    chunk1 = data[:mid]
    chunk2 = data[mid:]

    # Writer 1 writes chunk 1 and closes WITHOUT finalizing
    writer1 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer1.open()
    await writer1.append(chunk1)
    persisted_size1 = await writer1.close(finalize_on_close=False)
    generation = writer1.generation
    assert persisted_size1 == len(chunk1)
    assert generation is not None

    # Writer 2 takes over using the generation number
    writer2 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name, generation=generation)
    await writer2.open()
    await writer2.append(chunk2)
    object_metadata = await writer2.close(finalize_on_close=True)

    assert object_metadata.size == len(data)

    # Read back and verify
    buffer = BytesIO()
    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        await mrd.download_ranges([(0, 0, buffer)])
    assert buffer.getvalue() == data

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_takeover_just_to_finalize(grpc_client, bidi_bucket):
    object_name = f"test_takeover_fin_{uuid.uuid4()}"
    data = os.urandom(1000)

    # Writer 1 writes chunk 1 and closes WITHOUT finalizing
    writer1 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer1.open()
    await writer1.append(data)
    persisted_size1 = await writer1.close(finalize_on_close=False)
    generation = writer1.generation
    assert persisted_size1 == len(data)

    # Writer 2 takes over and finalizes
    writer2 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name, generation=generation)
    await writer2.open()
    object_metadata = await writer2.finalize()

    assert object_metadata.size == len(data)

    # Read back and verify
    buffer = BytesIO()
    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        await mrd.download_ranges([(0, 0, buffer)])
    assert buffer.getvalue() == data

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_explicit_finalize_with_correct_checksum(grpc_client, bidi_bucket):
    object_name = f"test_fin_crc_{uuid.uuid4()}"
    data = os.urandom(1000)

    writer = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer.open()
    await writer.append(data)
    
    expected_crc = google_crc32c.value(data)
    object_metadata = await writer.finalize(full_object_checksum=expected_crc)

    assert object_metadata.size == len(data)
    assert int(object_metadata.checksums.crc32c) == expected_crc

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_explicit_finalize_with_incorrect_checksum_fails(grpc_client, bidi_bucket):
    object_name = f"test_fin_bad_crc_{uuid.uuid4()}"
    data = os.urandom(1000)

    writer = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer.open()
    await writer.append(data)
    
    bad_crc = 0  # Incorrect checksum
    
    with pytest.raises(exceptions.InvalidArgument) as excinfo:
        await writer.finalize(full_object_checksum=bad_crc)
    
    assert "mismatch" in str(excinfo.value).lower()

    # Cleanup (it should not have been finalized, but we might need to delete the unfinalized object if it exists)
    # Actually, unfinalized objects might not be deleteable normally?
    # Yes they are deleteable.
    try:
        await grpc_client.delete_object(bidi_bucket, object_name)
    except Exception:
        pass


@pytest.mark.asyncio
async def test_takeover_just_to_finalize_with_incorrect_checksum_fails(grpc_client, bidi_bucket):
    object_name = f"test_takeover_bad_crc_{uuid.uuid4()}"
    data = os.urandom(1000)

    # Writer 1 writes chunk 1, closes unfinalized
    writer1 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer1.open()
    await writer1.append(data)
    await writer1.close(finalize_on_close=False)
    generation = writer1.generation

    # Writer 2 takes over, finalizes with bad checksum
    writer2 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name, generation=generation)
    await writer2.open()
    
    bad_crc = 0
    with pytest.raises(exceptions.InvalidArgument) as excinfo:
        await writer2.finalize(full_object_checksum=bad_crc)
    
    assert "mismatch" in str(excinfo.value).lower()

    # Cleanup
    try:
        await grpc_client.delete_object(bidi_bucket, object_name)
    except Exception:
        pass


@pytest.mark.asyncio
async def test_takeover_and_append_with_correct_checksum_works(grpc_client, bidi_bucket):
    object_name = f"test_takeover_append_crc_{uuid.uuid4()}"
    data = os.urandom(1000)
    mid = len(data) // 2
    chunk1 = data[:mid]
    chunk2 = data[mid:]

    # Writer 1 writes chunk 1, closes unfinalized
    writer1 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer1.open()
    await writer1.append(chunk1)
    await writer1.close(finalize_on_close=False)
    generation = writer1.generation

    # Writer 2 takes over, appends chunk 2, and finalizes with correct cumulative checksum
    writer2 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name, generation=generation)
    await writer2.open()
    await writer2.append(chunk2)
    
    expected_crc = google_crc32c.value(data)
    object_metadata = await writer2.finalize(full_object_checksum=expected_crc)

    assert object_metadata.size == len(data)
    assert int(object_metadata.checksums.crc32c) == expected_crc

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_takeover_and_append_with_incorrect_checksum_fails(grpc_client, bidi_bucket):
    object_name = f"test_takeover_append_bad_crc_{uuid.uuid4()}"
    data = os.urandom(1000)
    mid = len(data) // 2
    chunk1 = data[:mid]
    chunk2 = data[mid:]

    # Writer 1 writes chunk 1, closes unfinalized
    writer1 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer1.open()
    await writer1.append(chunk1)
    await writer1.close(finalize_on_close=False)
    generation = writer1.generation

    # Writer 2 takes over, appends chunk 2, finalizes with bad checksum
    writer2 = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name, generation=generation)
    await writer2.open()
    await writer2.append(chunk2)
    
    bad_crc = 0
    with pytest.raises(exceptions.InvalidArgument) as excinfo:
        await writer2.finalize(full_object_checksum=bad_crc)
    
    assert "mismatch" in str(excinfo.value).lower()

    # Cleanup
    try:
        await grpc_client.delete_object(bidi_bucket, object_name)
    except Exception:
        pass


# ----------------- Read Tests -----------------

@pytest.mark.asyncio
async def test_read_post_stream_close(grpc_client, bidi_bucket):
    object_name = f"test_read_close_{uuid.uuid4()}"
    data = os.urandom(5 * 1024 * 1024)  # 5MB
    await create_object(grpc_client, bidi_bucket, object_name, data)

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

    # The exception could be ServiceUnavailable or CancelledError
    assert isinstance(excinfo.value, (exceptions.ServiceUnavailable, asyncio.CancelledError))

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_zero_copy_range_reads(grpc_client, bidi_bucket):
    # We call it zero_copy to match Java test name, but it's standard range read in Python.
    object_name = f"test_zero_copy_{uuid.uuid4()}"
    data = os.urandom(1024 * 1024)  # 1MB
    await create_object(grpc_client, bidi_bucket, object_name, data)

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

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_multiple_ranged_read(grpc_client, bidi_bucket):
    object_name = f"test_multi_range_{uuid.uuid4()}"
    data = os.urandom(1024 * 1024)  # 1MB
    await create_object(grpc_client, bidi_bucket, object_name, data)

    r1 = (0, 1000)
    r2 = (50000, 250000)

    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        buf1 = BytesIO()
        buf2 = BytesIO()

        # Download multiple ranges in a single call (AsyncMultiRangeDownloader supports this)
        await mrd.download_ranges([
            (r1[0], r1[1], buf1),
            (r2[0], r2[1], buf2)
        ])

        assert buf1.getvalue() == data[r1[0] : r1[0] + r1[1]]
        assert buf2.getvalue() == data[r2[0] : r2[0] + r2[1]]

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


@pytest.mark.asyncio
async def test_read_from_non_existent_bucket_fails(grpc_client):
    bad_bucket_name = f"non-existent-bucket-{uuid.uuid4()}"
    
    with pytest.raises(NotFound) as excinfo:
        await AsyncMultiRangeDownloader.create_mrd(grpc_client, bad_bucket_name, "some-object")
    
    assert excinfo.value.code == 404


@pytest.mark.asyncio
async def test_read_out_of_range(grpc_client, bidi_bucket):
    object_name = f"test_oob_{uuid.uuid4()}"
    data = os.urandom(1024 * 1024)  # 1MB
    await create_object(grpc_client, bidi_bucket, object_name, data)

    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        valid_buffer = BytesIO()
        valid_task = asyncio.create_task(
            mrd.download_ranges([(0, 100, valid_buffer)])
        )

        oob_buffer = BytesIO()
        # starts at 2MB, object is 1MB
        oob_task = asyncio.create_task(
            mrd.download_ranges([(2 * 1024 * 1024, 100, oob_buffer)])
        )

        results = await asyncio.gather(valid_task, oob_task, return_exceptions=True)

        # Verify valid one processed correctly
        assert valid_buffer.getvalue() == data[:100]

        # Verify fully OOB request returned OutOfRange
        assert isinstance(results[1], OutOfRange)

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)
