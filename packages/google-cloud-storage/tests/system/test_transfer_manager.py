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

from google.cloud.storage import transfer_manager

from google.api_core import exceptions


def test_upload_many(shared_bucket, file_data, blobs_to_delete):
    FILE_BLOB_PAIRS = [
        (file_data["simple"]["path"], shared_bucket.blob("simple1")),
        (file_data["simple"]["path"], shared_bucket.blob("simple2")),
    ]

    results = transfer_manager.upload_many(FILE_BLOB_PAIRS)
    assert results == [None, None]

    blobs = shared_bucket.list_blobs()
    for blob in blobs:
        if blob.name.startswith("simple"):
            blobs_to_delete.append(blob)
    assert len(blobs_to_delete) == 2


def test_upload_many_with_file_objs(shared_bucket, file_data, blobs_to_delete):
    FILE_BLOB_PAIRS = [
        (open(file_data["simple"]["path"], "rb"), shared_bucket.blob("simple1")),
        (open(file_data["simple"]["path"], "rb"), shared_bucket.blob("simple2")),
    ]

    results = transfer_manager.upload_many(FILE_BLOB_PAIRS)
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
        FILE_BLOB_PAIRS, skip_if_exists=True, raise_exception=True
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
    tempfiles = [tempfile.TemporaryFile(), tempfile.TemporaryFile()]
    BLOB_FILE_PAIRS = zip(blobs[:2], tempfiles)

    results = transfer_manager.download_many(BLOB_FILE_PAIRS)
    assert results == [None, None]
    for fp in tempfiles:
        assert fp.tell() != 0
