# py standard imports
import asyncio
import os
import uuid
from io import BytesIO

# python additional imports
import pytest

# current library imports
from google.cloud.storage._experimental.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage._experimental.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_ZONAL_SYSTEM_TESTS") != "True",
    reason="Zonal system tests need to be explicitly enabled. This helps scheduling tests in Kokoro and Cloud Build.",
)


# TODO: replace this with a fixture once zonal bucket creation / deletion
# is supported in grpc client or json client client.
_ZONAL_BUCKET = os.getenv("ZONAL_BUCKET")
_BYTES_TO_UPLOAD = b"dummy_bytes_to_write_read_and_delete_appendable_object"


async def write_one_appendable_object(
    bucket_name: str,
    object_name: str,
    data: bytes,
) -> None:
    """Helper to write an appendable object."""
    grpc_client = AsyncGrpcClient(attempt_direct_path=True).grpc_client
    writer = AsyncAppendableObjectWriter(grpc_client, bucket_name, object_name)
    await writer.open()
    await writer.append(data)
    await writer.close()


@pytest.fixture(scope="function")
def appendable_object(storage_client, blobs_to_delete):
    """Fixture to create and cleanup an appendable object."""
    object_name = f"appendable_obj_for_mrd-{str(uuid.uuid4())[:4]}"
    asyncio.run(
        write_one_appendable_object(
            _ZONAL_BUCKET,
            object_name,
            _BYTES_TO_UPLOAD,
        )
    )
    yield object_name

    # Clean up; use json client (i.e. `storage_client` fixture) to delete.
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "attempt_direct_path",
    [True, False],
)
async def test_basic_wrd(storage_client, blobs_to_delete, attempt_direct_path):
    object_name = f"test_basic_wrd-{str(uuid.uuid4())}"

    # Client instantiation; it cannot be part of fixture because.
    # grpc_client's event loop and event loop of coroutine running it
    # (i.e. this test) must be same.
    # Note:
    # 1. @pytest.mark.asyncio ensures new event loop for each test.
    # 2. we can keep the same event loop for entire module but that may
    #  create issues if tests are run in parallel and one test hogs the event
    #  loop slowing down other tests.
    grpc_client = AsyncGrpcClient(attempt_direct_path=attempt_direct_path).grpc_client

    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)
    await writer.open()
    await writer.append(_BYTES_TO_UPLOAD)
    object_metadata = await writer.close(finalize_on_close=True)
    assert object_metadata.size == len(_BYTES_TO_UPLOAD)

    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, object_name)
    buffer = BytesIO()
    await mrd.open()
    # (0, 0) means read the whole object
    await mrd.download_ranges([(0, 0, buffer)])
    await mrd.close()
    assert buffer.getvalue() == _BYTES_TO_UPLOAD
    assert mrd.persisted_size == len(_BYTES_TO_UPLOAD)

    # Clean up; use json client (i.e. `storage_client` fixture) to delete.
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))


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


@pytest.mark.asyncio
async def test_mrd_open_with_read_handle(appendable_object):
    grpc_client = AsyncGrpcClient(attempt_direct_path=True).grpc_client

    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, appendable_object)
    await mrd.open()
    read_handle = mrd.read_handle
    await mrd.close()

    # Open a new MRD using the `read_handle` obtained above
    new_mrd = AsyncMultiRangeDownloader(
        grpc_client, _ZONAL_BUCKET, appendable_object, read_handle=read_handle
    )
    await new_mrd.open()
    # persisted_size not set when opened with read_handle
    assert new_mrd.persisted_size is None
    buffer = BytesIO()
    await new_mrd.download_ranges([(0, 0, buffer)])
    await new_mrd.close()
    assert buffer.getvalue() == _BYTES_TO_UPLOAD
