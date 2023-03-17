# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from google.cloud import storage
from google.cloud.documentai_toolbox.utilities import utilities

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
except ImportError:  # pragma: NO COVER
    import mock


test_bucket = "test-directory"
test_prefix = "documentai/input"


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_list_gcs_document_tree_with_one_folder(mock_storage):
    client = mock_storage.Client.return_value

    mock_bucket = mock.Mock()

    client.Bucket.return_value = mock_bucket

    blobs = [
        storage.Blob(
            name="gs://test-directory/1/test_shard1.json",
            bucket="gs://test-directory/1",
        ),
        storage.Blob(
            name="gs://test-directory/1/test_shard2.json",
            bucket="gs://test-directory/1",
        ),
        storage.Blob(
            name="gs://test-directory/1/test_shard3.json",
            bucket="gs://test-directory/1",
        ),
    ]

    client.list_blobs.return_value = blobs

    doc_list = utilities.list_gcs_document_tree(
        gcs_bucket_name="test-directory", gcs_prefix="/"
    )

    mock_storage.Client.assert_called_once()

    assert "gs://test-directory/1" in list(doc_list.keys())


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_list_gcs_document_tree_with_3_documents(mock_storage, capfd):
    client = mock_storage.Client.return_value

    mock_bucket = mock.Mock()

    client.Bucket.return_value = mock_bucket

    blobs = [
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard1.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard2.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard3.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
    ]

    client.list_blobs.return_value = blobs

    doc_list = utilities.list_gcs_document_tree(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/1/"
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()

    assert "gs://test-directory/documentai/output/123456789/1" in list(doc_list.keys())


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_list_gcs_document_tree_with_more_than_5_document(mock_storage, capfd):
    client = mock_storage.Client.return_value

    mock_bucket = mock.Mock()

    client.Bucket.return_value = mock_bucket

    blobs = [
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard1.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard2.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard3.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard4.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard5.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard6.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
    ]
    client.list_blobs.return_value = blobs

    doc_list = utilities.list_gcs_document_tree(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/1/"
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()

    assert "gs://test-directory/documentai/output/123456789/1" in list(doc_list.keys())


def test_list_gcs_document_tree_with_gcs_uri_contains_file_type():
    with pytest.raises(ValueError, match="gcs_prefix cannot contain file types"):
        utilities.list_gcs_document_tree(
            gcs_bucket_name="test-directory",
            gcs_prefix="documentai/output/123456789/1/test_file.json",
        )


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_print_gcs_document_tree_with_one_folder(mock_storage, capfd):
    client = mock_storage.Client.return_value

    mock_bucket = mock.Mock()

    client.Bucket.return_value = mock_bucket

    blobs = [
        storage.Blob(
            name="gs://test-directory/1/test_shard1.json",
            bucket="gs://test-directory/1",
        ),
        storage.Blob(
            name="gs://test-directory/1/test_shard2.json",
            bucket="gs://test-directory/1",
        ),
        storage.Blob(
            name="gs://test-directory/1/test_shard3.json",
            bucket="gs://test-directory/1",
        ),
    ]

    client.list_blobs.return_value = blobs

    utilities.print_gcs_document_tree(gcs_bucket_name="test-directory", gcs_prefix="/")

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()
    assert (
        out
        == """gs://test-directory/1
├──test_shard1.json
├──test_shard2.json
└──test_shard3.json\n\n"""
    )


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_print_gcs_document_tree_with_3_documents(mock_storage, capfd):
    client = mock_storage.Client.return_value

    mock_bucket = mock.Mock()

    client.Bucket.return_value = mock_bucket

    blobs = [
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard1.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard2.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard3.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
    ]

    client.list_blobs.return_value = blobs

    utilities.print_gcs_document_tree(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/1/"
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()
    assert (
        out
        == """gs://test-directory/documentai/output/123456789/1
├──test_shard1.json
├──test_shard2.json
└──test_shard3.json\n\n"""
    )


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_print_gcs_document_tree_with_more_than_5_document(mock_storage, capfd):
    client = mock_storage.Client.return_value

    mock_bucket = mock.Mock()

    client.Bucket.return_value = mock_bucket

    blobs = [
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard1.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard2.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard3.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard4.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard5.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
        storage.Blob(
            name="gs://test-directory/documentai/output/123456789/1/test_shard6.json",
            bucket="gs://test-directory/documentai/output/123456789/1",
        ),
    ]
    client.list_blobs.return_value = blobs

    utilities.print_gcs_document_tree(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/1/"
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()
    assert (
        out
        == """gs://test-directory/documentai/output/123456789/1
├──test_shard1.json
├──test_shard2.json
├──test_shard3.json
├──test_shard4.json
├──test_shard5.json
│  ....
└──test_shard6.json\n\n"""
    )


def test_print_gcs_document_tree_with_gcs_uri_contains_file_type():
    with pytest.raises(ValueError, match="gcs_prefix cannot contain file types"):
        utilities.print_gcs_document_tree(
            gcs_bucket_name="test-directory",
            gcs_prefix="documentai/output/123456789/1/test_file.json",
        )


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_create_batches_with_empty_directory(mock_storage, capfd):
    client = mock_storage.Client.return_value
    mock_bucket = mock.Mock()
    client.Bucket.return_value = mock_bucket

    mock_blob = mock.Mock(name="test_directory/", content_type="", size=0)
    mock_blob.name.endswith.return_value = True

    client.list_blobs.return_value = [mock_blob]

    actual = utilities.create_batches(
        gcs_bucket_name=test_bucket, gcs_prefix=test_prefix
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()
    assert out == ""
    assert len(actual) == 0


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_create_batches_with_3_documents(mock_storage, capfd):
    client = mock_storage.Client.return_value
    mock_bucket = mock.Mock()
    client.Bucket.return_value = mock_bucket

    mock_blobs = []
    for i in range(3):
        mock_blob = mock.Mock(
            name=f"test_file{i}.pdf", content_type="application/pdf", size=1024
        )
        mock_blob.name.endswith.return_value = False
        mock_blobs.append(mock_blob)
    client.list_blobs.return_value = mock_blobs

    actual = utilities.create_batches(
        gcs_bucket_name=test_bucket, gcs_prefix=test_prefix
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()
    assert out == ""
    assert len(actual) == 1
    assert len(actual[0].gcs_documents.documents) == 3


def test_create_batches_with_invalid_batch_size():
    with pytest.raises(
        ValueError,
        match="Batch size must be less than 50. You provided 51.",
    ):
        utilities.create_batches(
            gcs_bucket_name=test_bucket, gcs_prefix=test_prefix, batch_size=51
        )


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_create_batches_with_large_folder(mock_storage, capfd):
    client = mock_storage.Client.return_value
    mock_bucket = mock.Mock()
    client.Bucket.return_value = mock_bucket

    mock_blobs = []
    for i in range(96):
        mock_blob = mock.Mock(
            name=f"test_file{i}.pdf", content_type="application/pdf", size=1024
        )
        mock_blob.name.endswith.return_value = False
        mock_blobs.append(mock_blob)
    client.list_blobs.return_value = mock_blobs

    actual = utilities.create_batches(
        gcs_bucket_name=test_bucket, gcs_prefix=test_prefix
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()
    assert out == ""
    assert len(actual) == 2
    assert len(actual[0].gcs_documents.documents) == 50
    assert len(actual[1].gcs_documents.documents) == 46


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_create_batches_with_invalid_file_type(mock_storage, capfd):
    client = mock_storage.Client.return_value
    mock_bucket = mock.Mock()
    client.Bucket.return_value = mock_bucket

    mock_blob = mock.Mock(
        name="test_file.json", content_type="application/json", size=1024
    )
    mock_blob.name.endswith.return_value = False
    client.list_blobs.return_value = [mock_blob]

    actual = utilities.create_batches(
        gcs_bucket_name=test_bucket, gcs_prefix=test_prefix
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()
    assert "Invalid Mime Type" in out
    assert not actual


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.storage")
def test_create_batches_with_large_file(mock_storage, capfd):
    client = mock_storage.Client.return_value
    mock_bucket = mock.Mock()
    client.Bucket.return_value = mock_bucket

    mock_blob = mock.Mock(
        name="test_file.pdf", content_type="application/pdf", size=2073741824
    )
    mock_blob.name.endswith.return_value = False
    client.list_blobs.return_value = [mock_blob]

    actual = utilities.create_batches(
        gcs_bucket_name=test_bucket, gcs_prefix=test_prefix
    )

    mock_storage.Client.assert_called_once()

    out, err = capfd.readouterr()
    assert "File size must be less than" in out
    assert not actual
