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
    if bidi_location_type == "REGIONAL_STANDARD":
        pytest.skip("Bidi Write (Appendable) is not supported on standard regional buckets")
    elif bidi_location_type == "REGIONAL_RAPID":
        return REGIONAL_RAPID_BUCKET
    elif bidi_location_type == "ZONAL_RAPID":
        zonal_bucket = os.getenv("ZONAL_BUCKET")
        if not zonal_bucket:
            pytest.skip("ZONAL_BUCKET env var not set")
        return zonal_bucket
    else:
        pytest.fail(f"Unsupported location type: {bidi_location_type}")

# ----------------- Write Tests -----------------

@pytest.mark.asyncio
@pytest.mark.parametrize("finalize_on_close", [True, False])
async def test_appendable_upload_empty_object(grpc_client, bidi_bucket, finalize_on_close):
    object_name = f"test_empty_{uuid.uuid4()}"
    
    writer = AsyncAppendableObjectWriter(grpc_client, bidi_bucket, object_name)
    await writer.open()
    object_metadata = await writer.close(finalize_on_close=finalize_on_close)

    # If finalized_on_close is False, we need to finalize it now to get size and CRC,
    # or just verify we can close it.
    # In Java: upload.open().close(); results in 0 size.
    # In Python, if finalize_on_close is False, close() returns persisted_size (which should be 0).
    if not finalize_on_close:
        assert object_metadata == 0
        # Finalize to get the object resource
        object_metadata = await writer.finalize()
    
    assert object_metadata.size == 0
    assert int(object_metadata.checksums.crc32c) == int(google_crc32c.value(b""))

    # Read back and verify empty
    buffer = BytesIO()
    async with AsyncMultiRangeDownloader(grpc_client, bidi_bucket, object_name) as mrd:
        await mrd.download_ranges([(0, 0, buffer)])
    assert buffer.getvalue() == b""

    # Cleanup
    await grpc_client.delete_object(bidi_bucket, object_name)


# Parameterize write options similar to Java
FLUSH_INTERVALS = [None, 2 * 1024 * 1024, 4 * 1024 * 1024]
FINALIZE_ON_CLOSE_OPTS = [True, False]
OBJECT_SIZES = [5, 500, 5000, 500000, 5000000]

@pytest.mark.asyncio
@pytest.mark.parametrize("flush_interval", FLUSH_INTERVALS)
@pytest.mark.parametrize("finalize_on_close", FINALIZE_ON_CLOSE_OPTS)
@pytest.mark.parametrize("object_size", OBJECT_SIZES)
async def test_appendable_upload_bytes(grpc_client, bidi_bucket, flush_interval, finalize_on_close, object_size):
    object_name = f"test_bytes_{uuid.uuid4()}"
    data = os.urandom(object_size)
    mid = len(data) // 2
    chunk1 = data[:mid]
    chunk2 = data[mid:]

    writer_options = {}
    if flush_interval is not None:
        writer_options["FLUSH_INTERVAL_BYTES"] = flush_interval

    writer = AsyncAppendableObjectWriter(
        grpc_client, bidi_bucket, object_name, writer_options=writer_options
    )
    await writer.open()
    await writer.append(chunk1)
    await writer.append(chunk2)
    object_metadata = await writer.close(finalize_on_close=finalize_on_close)

    if not finalize_on_close:
        # Check persisted size so far
        assert object_metadata == len(data)
        object_metadata = await writer.finalize()

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

    # Cleanup
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
