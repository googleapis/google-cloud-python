# coding=utf-8
# Copyright 2022 Google LLC
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

import tempfile
import os

from google.cloud.storage import transfer_manager
from google.cloud.storage._helpers import _base64_md5hash

from google.api_core import exceptions

DEADLINE = 30


def test_upload_many(shared_bucket, file_data, blobs_to_delete):
    FILE_BLOB_PAIRS = [
        (file_data["simple"]["path"], shared_bucket.blob("simple1")),
        (file_data["simple"]["path"], shared_bucket.blob("simple2")),
    ]

    results = transfer_manager.upload_many(
        FILE_BLOB_PAIRS,
        worker_type=transfer_manager.PROCESS,
        deadline=DEADLINE,
    )
    assert results == [None, None]

    blobs = shared_bucket.list_blobs()
    for blob in blobs:
        if blob.name.startswith("simple"):
            blobs_to_delete.append(blob)
    assert len(blobs_to_delete) == 2


def test_upload_many_with_threads_and_file_objs(
    shared_bucket, file_data, blobs_to_delete
):
    FILE_BLOB_PAIRS = [
        (open(file_data["simple"]["path"], "rb"), shared_bucket.blob("simple1")),
        (open(file_data["simple"]["path"], "rb"), shared_bucket.blob("simple2")),
    ]

    results = transfer_manager.upload_many(
        FILE_BLOB_PAIRS,
        worker_type=transfer_manager.THREAD,
        deadline=DEADLINE,
    )
    assert results == [None, None]

    blobs = shared_bucket.list_blobs()
    for blob in blobs:
        if blob.name.startswith("simple"):
            blobs_to_delete.append(blob)
    assert len(blobs_to_delete) == 2


def test_upload_many_skip_if_exists(
    listable_bucket, listable_filenames, file_data, blobs_to_delete
):
    FILE_BLOB_PAIRS = [
        (file_data["logo"]["path"], listable_bucket.blob(listable_filenames[0])),
        (file_data["simple"]["path"], listable_bucket.blob("simple")),
    ]

    results = transfer_manager.upload_many(
        FILE_BLOB_PAIRS,
        skip_if_exists=True,
        raise_exception=True,
        deadline=DEADLINE,
    )
    assert isinstance(results[0], exceptions.PreconditionFailed)
    assert results[1] is None

    blobs = listable_bucket.list_blobs()
    for blob in blobs:
        if blob.name.startswith("simple"):
            blobs_to_delete.append(blob)
    assert len(blobs_to_delete) == 1


def test_download_many(listable_bucket):
    blobs = list(listable_bucket.list_blobs())
    with tempfile.TemporaryDirectory() as tempdir:
        filenames = [
            os.path.join(tempdir, "file_a.txt"),
            os.path.join(tempdir, "file_b.txt"),
        ]
        BLOB_FILE_PAIRS = zip(blobs[:2], filenames)

        results = transfer_manager.download_many(
            BLOB_FILE_PAIRS,
            worker_type=transfer_manager.PROCESS,
            deadline=DEADLINE,
        )
        assert results == [None, None]
        for count, filename in enumerate(filenames):
            with open(filename, "rb") as fp:
                assert len(fp.read()) == blobs[count].size


def test_download_many_with_threads_and_file_objs(listable_bucket):
    blobs = list(listable_bucket.list_blobs())
    with tempfile.TemporaryFile() as file_a, tempfile.TemporaryFile() as file_b:
        tempfiles = [file_a, file_b]
        BLOB_FILE_PAIRS = zip(blobs[:2], tempfiles)

        results = transfer_manager.download_many(
            BLOB_FILE_PAIRS,
            worker_type=transfer_manager.THREAD,
            deadline=DEADLINE,
        )
        assert results == [None, None]
        for fp in tempfiles:
            assert fp.tell() != 0


def test_download_chunks_concurrently(shared_bucket, file_data):
    # Upload a big file
    source_file = file_data["big"]
    upload_blob = shared_bucket.blob("chunky_file")
    upload_blob.upload_from_filename(source_file["path"])
    upload_blob.reload()
    size = upload_blob.size
    chunk_size = size // 32

    # Get a fresh blob obj w/o metadata for testing purposes
    download_blob = shared_bucket.blob("chunky_file")

    with tempfile.TemporaryDirectory() as tempdir:
        full_filename = os.path.join(tempdir, "chunky_file_1")
        transfer_manager.download_chunks_concurrently(
            download_blob,
            full_filename,
            chunk_size=chunk_size,
            deadline=DEADLINE,
        )
        with open(full_filename, "rb") as file_obj:
            assert _base64_md5hash(file_obj) == source_file["hash"]

        # Now test for case where last chunk is exactly 1 byte.
        trailing_chunk_filename = os.path.join(tempdir, "chunky_file_2")
        transfer_manager.download_chunks_concurrently(
            download_blob,
            trailing_chunk_filename,
            chunk_size=size - 1,
            deadline=DEADLINE,
        )
        with open(trailing_chunk_filename, "rb") as file_obj:
            assert _base64_md5hash(file_obj) == source_file["hash"]

        # Also test threaded mode.
        threaded_filename = os.path.join(tempdir, "chunky_file_3")
        transfer_manager.download_chunks_concurrently(
            download_blob,
            threaded_filename,
            chunk_size=chunk_size,
            deadline=DEADLINE,
            worker_type=transfer_manager.THREAD,
        )
        with open(threaded_filename, "rb") as file_obj:
            assert _base64_md5hash(file_obj) == source_file["hash"]
