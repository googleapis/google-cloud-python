# py standard imports
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


@pytest.mark.asyncio
async def test_basic_wrd(storage_client, blobs_to_delete):
    bytes_to_upload = b"dummy_bytes_to_write_read_and_delete_appendable_object"
    object_name = f"test_basic_wrd-{str(uuid.uuid4())}"

    # Client instantiation; it cannot be part of fixture because.
    # grpc_client's event loop and event loop of coroutine running it
    # (i.e. this test) must be same.
    # Note:
    # 1. @pytest.mark.asyncio ensures new event for each test.
    # 2. we can keep the same event loop for entire module but that may
    #  create issues if tests are run in parallel and one test hogs the event
    #  loop slowing down other tests.
    grpc_client = AsyncGrpcClient().grpc_client

    writer = AsyncAppendableObjectWriter(grpc_client, _ZONAL_BUCKET, object_name)
    await writer.open()
    await writer.append(bytes_to_upload)
    object_metadata = await writer.close(finalize_on_close=True)
    assert object_metadata.size == len(bytes_to_upload)

    mrd = AsyncMultiRangeDownloader(grpc_client, _ZONAL_BUCKET, object_name)
    buffer = BytesIO()
    await mrd.open()
    # (0, 0) means read the whole object
    await mrd.download_ranges([(0, 0, buffer)])
    await mrd.close()
    assert buffer.getvalue() == bytes_to_upload

    # Clean up; use json client (i.e. `storage_client` fixture) to delete.
    blobs_to_delete.append(storage_client.bucket(_ZONAL_BUCKET).blob(object_name))
