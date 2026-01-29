# py standard imports
import os
import uuid
from io import BytesIO
import asyncio

# python additional imports
import google_crc32c

import pytest
import gc

# current library imports
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
    _DEFAULT_FLUSH_INTERVAL_BYTES,
)
from google.cloud.storage.asyncio.async_multi_range_downloader import (
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


async def create_async_grpc_client(attempt_direct_path=True):
    """Initializes async client and gets the current event loop."""
    return AsyncGrpcClient(attempt_direct_path=attempt_direct_path)


@pytest.fixture(scope="session")
def event_loop():
    """Redefine pytest-asyncio's event_loop fixture to be session-scoped."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def grpc_clients(event_loop):
    # grpc clients has to be instantiated in the event loop,
    # otherwise grpc creates it's own event loop and attaches to the client.
    # Which will lead to deadlock because client running in one event loop and
    # MRD or Appendable-Writer in another.
    # https://github.com/grpc/grpc/blob/61fe9b40a986792ab7d4eb8924027b671faf26ba/src/python/grpcio/grpc/aio/_channel.py#L369
    # https://github.com/grpc/grpc/blob/61fe9b40a986792ab7d4eb8924027b671faf26ba/src/python/grpcio/grpc/_cython/_cygrpc/aio/common.pyx.pxi#L249
    clients = {
        True: event_loop.run_until_complete(
            create_async_grpc_client(attempt_direct_path=True)
        ),
        False: event_loop.run_until_complete(
            create_async_grpc_client(attempt_direct_path=False)
        ),
    }
    return clients


# This fixture is for tests that are NOT parametrized by attempt_direct_path
@pytest.fixture
def grpc_client(grpc_clients):
    return grpc_clients[False]


@pytest.fixture
def grpc_client_direct(grpc_clients):
    return grpc_clients[True]


def _get_equal_dist(a: int, b: int) -> tuple[int, int]:
    step = (b - a) // 3
    return a + step, a + 2 * step


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
def test_basic_wrd(
    storage_client,
    blobs_to_delete,
    attempt_direct_path,
    object_size,
    event_loop,
    grpc_clients,
):
    object_name = f"test_basic_wrd-{str(uuid.uuid4())}"

    async def _run():
        object_data = os.urandom(object_size)
        object_checksum = google_crc32c.value(object_data)
        grpc_client = grpc_clients[attempt_direct_path]

        writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)
        await writer.open()
        await writer.append(object_data)
        object_metadata = await writer.close(finalize_on_close=True)
        assert object_metadata.size == object_size
        assert int(object_metadata.checksums.crc32c) == object_checksum

        buffer = BytesIO()
        async with AsyncMultiRangeDownloader(
            grpc_client, _ZONAL_BUCKET, object_name
        ) as mrd:
            # (0, 0) means read the whole object
            await mrd.download_ranges([(0, 0, buffer)])
            assert mrd.persisted_size == object_size

        assert buffer.getvalue() == object_data

        # Clean up; use json client (i.e. `storage_client` fixture) to delete.
        blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))
        del writer
        gc.collect()

    event_loop.run_until_complete(_run())


@pytest.mark.parametrize(
    "object_size",
    [
        10,  # less than _chunk size,
        10 * 1024 * 1024,  # less than _MAX_BUFFER_SIZE_BYTES
        20 * 1024 * 1024,  # greater than _MAX_BUFFER_SIZE_BYTES
    ],
)
def test_basic_wrd_in_slices(
    storage_client, blobs_to_delete, object_size, event_loop, grpc_client
):
    object_name = f"test_basic_wrd-{str(uuid.uuid4())}"

    async def _run():
        object_data = os.urandom(object_size)
        object_checksum = google_crc32c.value(object_data)

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

    event_loop.run_until_complete(_run())


@pytest.mark.parametrize(
    "flush_interval",
    [
        2 * 1024 * 1024,
        4 * 1024 * 1024,
        8 * 1024 * 1024,
        _DEFAULT_FLUSH_INTERVAL_BYTES,
    ],
)
def test_wrd_with_non_default_flush_interval(
    storage_client,
    blobs_to_delete,
    flush_interval,
    event_loop,
    grpc_client,
):
    object_name = f"test_basic_wrd-{str(uuid.uuid4())}"
    object_size = 9 * 1024 * 1024

    async def _run():
        object_data = os.urandom(object_size)
        object_checksum = google_crc32c.value(object_data)

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

    event_loop.run_until_complete(_run())


def test_read_unfinalized_appendable_object(
    storage_client, blobs_to_delete, event_loop, grpc_client_direct
):
    object_name = f"read_unfinalized_appendable_object-{str(uuid.uuid4())[:4]}"

    async def _run():
        grpc_client = grpc_client_direct
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

    event_loop.run_until_complete(_run())

@pytest.mark.skip(reason='Flaky test b/478129078')
def test_mrd_open_with_read_handle(event_loop, grpc_client_direct):
    object_name = f"test_read_handl-{str(uuid.uuid4())[:4]}"

    async def _run():
        writer = AsyncAppendableObjectWriter(
            grpc_client_direct, _ZONAL_BUCKET, object_name
        )
        await writer.open()
        await writer.append(_BYTES_TO_UPLOAD)
        await writer.close()

        mrd = AsyncMultiRangeDownloader(grpc_client_direct, _ZONAL_BUCKET, object_name)
        await mrd.open()
        read_handle = mrd.read_handle
        await mrd.close()

        # Open a new MRD using the `read_handle` obtained above
        new_mrd = AsyncMultiRangeDownloader(
            grpc_client_direct, _ZONAL_BUCKET, object_name, read_handle=read_handle
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

    event_loop.run_until_complete(_run())


def test_mrd_open_with_read_handle_over_cloud_path(event_loop, grpc_client):
    object_name = f"test_read_handl-{str(uuid.uuid4())[:4]}"

    async def _run():
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
        # persisted_size is set regardless of whether we use read_handle or not
        # because read_handle won't work in CLOUD_PATH.
        assert new_mrd.persisted_size == len(_BYTES_TO_UPLOAD)
        buffer = BytesIO()
        await new_mrd.download_ranges([(0, 0, buffer)])
        await new_mrd.close()
        assert buffer.getvalue() == _BYTES_TO_UPLOAD
        del mrd
        del new_mrd
        gc.collect()

    event_loop.run_until_complete(_run())


def test_wrd_open_with_write_handle(
    event_loop, grpc_client_direct, storage_client, blobs_to_delete
):
    object_name = f"test_write_handl-{str(uuid.uuid4())[:4]}"

    async def _run():
        # 1. Create an object and get its write_handle
        writer = AsyncAppendableObjectWriter(
            grpc_client_direct, _ZONAL_BUCKET, object_name
        )
        await writer.open()
        write_handle = writer.write_handle
        await writer.close()

        # 2. Open a new writer using the obtained `write_handle` and generation
        new_writer = AsyncAppendableObjectWriter(
            grpc_client_direct,
            _ZONAL_BUCKET,
            object_name,
            write_handle=write_handle,
            generation=writer.generation,
        )
        await new_writer.open()
        # Verify that the new writer is open and has the same write_handle
        assert new_writer.is_stream_open
        assert new_writer.generation == writer.generation

        # 3. Append some data using the new writer
        test_data = b"data_from_new_writer"
        await new_writer.append(test_data)
        await new_writer.close()

        # 4. Verify the data was written correctly by reading it back
        mrd = AsyncMultiRangeDownloader(grpc_client_direct, _ZONAL_BUCKET, object_name)
        buffer = BytesIO()
        await mrd.open()
        await mrd.download_ranges([(0, 0, buffer)])
        await mrd.close()
        assert buffer.getvalue() == test_data

        # Clean up
        blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))
        del writer
        del new_writer
        del mrd
        gc.collect()

    event_loop.run_until_complete(_run())


def test_read_unfinalized_appendable_object_with_generation(
    storage_client, blobs_to_delete, event_loop, grpc_client_direct
):
    object_name = f"read_unfinalized_appendable_object-{str(uuid.uuid4())[:4]}"
    grpc_client = grpc_client_direct

    async def _run():
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

    event_loop.run_until_complete(_run())


def test_append_flushes_and_state_lookup(
    storage_client, blobs_to_delete, event_loop, grpc_client
):
    """
    System test for AsyncAppendableObjectWriter, verifying flushing behavior
    for both small and large appends.
    """
    object_name = f"test-append-flush-varied-size-{uuid.uuid4()}"

    async def _run():
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

    event_loop.run_until_complete(_run())


def test_open_with_generation_zero(
    storage_client, blobs_to_delete, event_loop, grpc_client
):
    """Tests that using `generation=0` fails if the object already exists.

    This test verifies that:
    1. An object can be created using `AsyncAppendableObjectWriter` with `generation=0`.
    2. Attempting to create the same object again with `generation=0` raises a
       `FailedPrecondition` error with a 400 status code, because the
       precondition (object must not exist) is not met.
    """
    object_name = f"test_append_with_generation-{uuid.uuid4()}"

    async def _run():
        writer = AsyncAppendableObjectWriter(
            grpc_client, _ZONAL_BUCKET, object_name, generation=0
        )

        # Empty object is created.
        await writer.open()
        assert writer.is_stream_open

        await writer.close()
        assert not writer.is_stream_open

        with pytest.raises(FailedPrecondition) as exc_info:
            writer_fail = AsyncAppendableObjectWriter(
                grpc_client, _ZONAL_BUCKET, object_name, generation=0
            )
            await writer_fail.open()
        assert exc_info.value.code == 400

        # cleanup
        del writer
        gc.collect()

        blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))

    event_loop.run_until_complete(_run())


def test_open_existing_object_with_gen_None_overrides_existing(
    storage_client, blobs_to_delete, event_loop, grpc_client
):
    """
    Test that a new writer when specifies `None` overrides the existing object.
    """
    object_name = f"test_append_with_generation-{uuid.uuid4()}"

    async def _run():
        writer = AsyncAppendableObjectWriter(
            grpc_client, _ZONAL_BUCKET, object_name, generation=0
        )

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

        # cleanup
        del writer
        del new_writer
        gc.collect()

        blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))

    event_loop.run_until_complete(_run())
