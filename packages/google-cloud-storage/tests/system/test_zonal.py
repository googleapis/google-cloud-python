# py standard imports
import os
import uuid
from io import BytesIO

# python additional imports
import google_crc32c

import pytest
import gc

# current library imports
from google.cloud.storage._experimental.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
    _DEFAULT_FLUSH_INTERVAL_BYTES,
)
from google.cloud.storage._experimental.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)
from google.api_core.exceptions import FailedPrecondition


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_ZONAL_SYSTEM_TESTS") != "True",
    reason="Zonal system tests need to be explicitly enabled. This helps scheduling tests in Kokoro and Cloud Build.",
)


# TODO: replace this with a fixture once zonal bucket creation / deletion
# is supported in grpc client or json client client.
_ZONAL_BUCKET = os.getenv("ZONAL_BUCKET")
_BYTES_TO_UPLOAD = b"dummy_bytes_to_write_read_and_delete_appendable_object"


def _get_equal_dist(a: int, b: int) -> tuple[int, int]:
    step = (b - a) // 3
    return a + step, a + 2 * step


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "object_size",
    [
        256,  # less than _chunk size
        10 * 1024 * 1024,  # less than _MAX_BUFFER_SIZE_BYTES
        20 * 1024 * 1024,  # greater than _MAX_BUFFER_SIZE
    ],
)
@pytest.mark.parametrize(
    "attempt_direct_path",
    [True, False],
)
async def test_basic_wrd(
    storage_client, blobs_to_delete, attempt_direct_path, object_size
):
    object_name = f"test_basic_wrd-{str(uuid.uuid4())}"

    # Client instantiation; it cannot be part of fixture because.
    # grpc_client's event loop and event loop of coroutine running it
    # (i.e. this test) must be same.
    # Note:
    # 1. @pytest.mark.asyncio ensures new event loop for each test.
    # 2. we can keep the same event loop for entire module but that may
    #  create issues if tests are run in parallel and one test hogs the event
    #  loop slowing down other tests.
    object_data = os.urandom(object_size)
    object_checksum = google_crc32c.value(object_data)
    grpc_client = AsyncGrpcClient(attempt_direct_path=attempt_direct_path).grpc_client

    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)
    await writer.open()
    await writer.append(object_data)
    object_metadata = await writer.close(finalize_on_close=True)
    assert object_metadata.size == object_size
    assert int(object_metadata.checksums.crc32c) == object_checksum

    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, object_name)
    buffer = BytesIO()
    await mrd.open()
    # (0, 0) means read the whole object
    await mrd.download_ranges([(0, 0, buffer)])
    await mrd.close()
    assert buffer.getvalue() == object_data
    assert mrd.persisted_size == object_size

    # Clean up; use json client (i.e. `storage_client` fixture) to delete.
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))
    del writer
    del mrd
    gc.collect()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "object_size",
    [
        10,  # less than _chunk size,
        10 * 1024 * 1024,  # less than _MAX_BUFFER_SIZE_BYTES
        20 * 1024 * 1024,  # greater than _MAX_BUFFER_SIZE_BYTES
    ],
)
async def test_basic_wrd_in_slices(storage_client, blobs_to_delete, object_size):
    object_name = f"test_basic_wrd-{str(uuid.uuid4())}"

    # Client instantiation; it cannot be part of fixture because.
    # grpc_client's event loop and event loop of coroutine running it
    # (i.e. this test) must be same.
    # Note:
    # 1. @pytest.mark.asyncio ensures new event loop for each test.
    # 2. we can keep the same event loop for entire module but that may
    #  create issues if tests are run in parallel and one test hogs the event
    #  loop slowing down other tests.
    object_data = os.urandom(object_size)
    object_checksum = google_crc32c.value(object_data)
    grpc_client = AsyncGrpcClient().grpc_client

    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)
    await writer.open()
    mark1, mark2 = _get_equal_dist(0, object_size)
    await writer.append(object_data[0:mark1])
    await writer.append(object_data[mark1:mark2])
    await writer.append(object_data[mark2:])
    object_metadata = await writer.close(finalize_on_close=True)
    assert object_metadata.size == object_size
    assert int(object_metadata.checksums.crc32c) == object_checksum

    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, object_name)
    buffer = BytesIO()
    await mrd.open()
    # (0, 0) means read the whole object
    await mrd.download_ranges([(0, 0, buffer)])
    await mrd.close()
    assert buffer.getvalue() == object_data
    assert mrd.persisted_size == object_size

    # Clean up; use json client (i.e. `storage_client` fixture) to delete.
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))
    del writer
    del mrd
    gc.collect()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "flush_interval",
    [
        2 * 1024 * 1024,
        4 * 1024 * 1024,
        8 * 1024 * 1024,
        _DEFAULT_FLUSH_INTERVAL_BYTES,
    ],
)
async def test_wrd_with_non_default_flush_interval(
    storage_client,
    blobs_to_delete,
    flush_interval,
):
    object_name = f"test_basic_wrd-{str(uuid.uuid4())}"
    object_size = 9 * 1024 * 1024

    # Client instantiation; it cannot be part of fixture because.
    # grpc_client's event loop and event loop of coroutine running it
    # (i.e. this test) must be same.
    # Note:
    # 1. @pytest.mark.asyncio ensures new event loop for each test.
    # 2. we can keep the same event loop for entire module but that may
    #  create issues if tests are run in parallel and one test hogs the event
    #  loop slowing down other tests.
    object_data = os.urandom(object_size)
    object_checksum = google_crc32c.value(object_data)
    grpc_client = AsyncGrpcClient().grpc_client

    writer = AsyncAppendableObjectWriter(
        grpc_client,
        _ZONAL_BUCKET,
        object_name,
        writer_options={"FLUSH_INTERVAL_BYTES": flush_interval},
    )
    await writer.open()
    mark1, mark2 = _get_equal_dist(0, object_size)
    await writer.append(object_data[0:mark1])
    await writer.append(object_data[mark1:mark2])
    await writer.append(object_data[mark2:])
    object_metadata = await writer.close(finalize_on_close=True)
    assert object_metadata.size == object_size
    assert int(object_metadata.checksums.crc32c) == object_checksum

    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, object_name)
    buffer = BytesIO()
    await mrd.open()
    # (0, 0) means read the whole object
    await mrd.download_ranges([(0, 0, buffer)])
    await mrd.close()
    assert buffer.getvalue() == object_data
    assert mrd.persisted_size == object_size

    # Clean up; use json client (i.e. `storage_client` fixture) to delete.
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))
    del writer
    del mrd
    gc.collect()


@pytest.mark.asyncio
async def test_read_unfinalized_appendable_object(storage_client, blobs_to_delete):
    object_name = f"read_unfinalized_appendable_object-{str(uuid.uuid4())[:4]}"
    grpc_client = AsyncGrpcClient(attempt_direct_path=True).grpc_client

    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)
    await writer.open()
    await writer.append(_BYTES_TO_UPLOAD)
    await writer.flush()

    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, object_name)
    buffer = BytesIO()
    await mrd.open()
    assert mrd.persisted_size == len(_BYTES_TO_UPLOAD)
    # (0, 0) means read the whole object
    await mrd.download_ranges([(0, 0, buffer)])
    await mrd.close()
    assert buffer.getvalue() == _BYTES_TO_UPLOAD

    # Clean up; use json client (i.e. `storage_client` fixture) to delete.
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))
    del writer
    del mrd
    gc.collect()


@pytest.mark.asyncio
async def test_mrd_open_with_read_handle():
    grpc_client = AsyncGrpcClient().grpc_client
    object_name = f"test_read_handl-{str(uuid.uuid4())[:4]}"
    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)
    await writer.open()
    await writer.append(_BYTES_TO_UPLOAD)
    await writer.close()

    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, object_name)
    await mrd.open()
    read_handle = mrd.read_handle
    await mrd.close()

    # Open a new MRD using the `read_handle` obtained above
    new_mrd = AsyncMultiRangeDownloader(
        grpc_client, _ZONAL_BUCKET, object_name, read_handle=read_handle
    )
    await new_mrd.open()
    # persisted_size not set when opened with read_handle
    assert new_mrd.persisted_size is None
    buffer = BytesIO()
    await new_mrd.download_ranges([(0, 0, buffer)])
    await new_mrd.close()
    assert buffer.getvalue() == _BYTES_TO_UPLOAD
    del mrd
    del new_mrd
    gc.collect()


@pytest.mark.asyncio
async def test_read_unfinalized_appendable_object_with_generation(
    storage_client, blobs_to_delete
):
    object_name = f"read_unfinalized_appendable_object-{str(uuid.uuid4())[:4]}"
    grpc_client = AsyncGrpcClient(attempt_direct_path=True).grpc_client

    async def _read_and_verify(expected_content, generation=None):
        """Helper to read object content and verify against expected."""
        mrd = AsyncMultiRangeDownloader(
            grpc_client, _ZONAL_BUCKET, object_name, generation
        )
        buffer = BytesIO()
        await mrd.open()
        try:
            assert mrd.persisted_size == len(expected_content)
            await mrd.download_ranges([(0, 0, buffer)])
            assert buffer.getvalue() == expected_content
        finally:
            await mrd.close()
        return mrd

    # First write
    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)
    await writer.open()
    await writer.append(_BYTES_TO_UPLOAD)
    await writer.flush()
    generation = writer.generation

    # First read
    mrd = await _read_and_verify(_BYTES_TO_UPLOAD)

    # Second write, using generation from the first write.
    writer_2 = AsyncAppendableObjectWriter(
        grpc_client, _ZONAL_BUCKET, object_name, generation=generation
    )
    await writer_2.open()
    await writer_2.append(_BYTES_TO_UPLOAD)
    await writer_2.flush()

    # Second read
    mrd_2 = await _read_and_verify(_BYTES_TO_UPLOAD + _BYTES_TO_UPLOAD, generation)

    # Clean up
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))
    del writer
    del writer_2
    del mrd
    del mrd_2
    gc.collect()


@pytest.mark.asyncio
async def test_append_flushes_and_state_lookup(storage_client, blobs_to_delete):
    """
    System test for AsyncAppendableObjectWriter, verifying flushing behavior
    for both small and large appends.
    """
    object_name = f"test-append-flush-varied-size-{uuid.uuid4()}"
    grpc_client = AsyncGrpcClient().grpc_client
    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)

    # Schedule for cleanup
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))

    # --- Part 1: Test with small data ---
    small_data = b"small data"

    await writer.open()
    assert writer._is_stream_open

    await writer.append(small_data)
    persisted_size = await writer.state_lookup()
    assert persisted_size == len(small_data)

    # --- Part 2: Test with large data ---
    large_data = os.urandom(38 * 1024 * 1024)

    # Append data larger than the default flush interval (16 MiB).
    # This should trigger the interval-based flushing logic.
    await writer.append(large_data)

    # Verify the total data has been persisted.
    total_size = len(small_data) + len(large_data)
    persisted_size = await writer.state_lookup()
    assert persisted_size == total_size

    # --- Part 3: Finalize and verify ---
    final_object = await writer.close(finalize_on_close=True)

    assert not writer._is_stream_open
    assert final_object.size == total_size

    # Verify the full content of the object.
    full_data = small_data + large_data
    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, object_name)
    buffer = BytesIO()
    await mrd.open()
    # (0, 0) means read the whole object
    await mrd.download_ranges([(0, 0, buffer)])
    await mrd.close()
    content = buffer.getvalue()
    assert content == full_data

@pytest.mark.asyncio
async def test_open_with_generation_zero(storage_client, blobs_to_delete):
    """Tests that using `generation=0` fails if the object already exists.

    This test verifies that:
    1. An object can be created using `AsyncAppendableObjectWriter` with `generation=0`.
    2. Attempting to create the same object again with `generation=0` raises a
       `FailedPrecondition` error with a 400 status code, because the
       precondition (object must not exist) is not met.
    """
    object_name = f"test_append_with_generation-{uuid.uuid4()}"
    grpc_client = AsyncGrpcClient().grpc_client
    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name, generation=0)

    # Empty object is created.
    await writer.open()
    assert writer.is_stream_open

    await writer.close()
    assert not writer.is_stream_open


    with pytest.raises(FailedPrecondition) as exc_info:
        writer = AsyncAppendableObjectWriter(
            grpc_client, _ZONAL_BUCKET, object_name, generation=0
        )
        await writer.open()
    assert exc_info.value.code == 400

    # cleanup
    del writer
    gc.collect()

    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))

@pytest.mark.asyncio
async def test_open_existing_object_with_gen_None_overrides_existing(storage_client, blobs_to_delete):
    """
    Test that a new writer when specifies `None` overrides the existing object.
    """
    object_name = f"test_append_with_generation-{uuid.uuid4()}"

    grpc_client = AsyncGrpcClient().grpc_client
    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name, generation=0)

    # Empty object is created.
    await writer.open()
    assert writer.is_stream_open
    old_gen = writer.generation


    await writer.close()
    assert not writer.is_stream_open



    new_writer = AsyncAppendableObjectWriter(
            grpc_client, _ZONAL_BUCKET, object_name, generation=None
    )
    await new_writer.open()
    assert new_writer.generation != old_gen

    # assert exc_info.value.code == 400

    # cleanup
    del writer
    del new_writer
    gc.collect()

    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))