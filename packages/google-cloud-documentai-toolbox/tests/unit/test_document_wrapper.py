# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
except ImportError:  # pragma: NO COVER
    import mock

import pytest
import glob

from google.cloud.documentai_toolbox.wrappers import DocumentWrapper, document_wrapper

from google.cloud import documentai


def get_bytes(file_name):
    result = []
    for filename in glob.glob(os.path.join(file_name, "*.json")):
        with open(os.path.join(os.getcwd(), filename), "rb") as f:
            result.append(f.read())

    return result


def test_read_output_with_gcs_uri_contains_file_type():
    with pytest.raises(ValueError, match="gcs_prefix cannot contain file types"):
        document_wrapper._read_output(
            "gs://test-directory/documentai/output/123456789/0.json"
        )


def test_read_output_with_invalid_gcs_uri():
    with pytest.raises(ValueError, match="gcs_prefix does not match accepted format"):
        document_wrapper._read_output("test-directory/documentai/output/")


def test_read_output_with_valid_gcs_uri():
    with mock.patch.object(document_wrapper, "_get_bytes") as factory:
        factory.return_value = get_bytes("tests/unit/resources/0")
        actual = document_wrapper._read_output(
            "gs://test-directory/documentai/output/123456789/0"
        )
        # We are testing only one of the fields to make sure the file content could be loaded.
        assert actual[0].pages[0].page_number == 1


def test_pages_from_shards():
    shards = []
    for byte in get_bytes("tests/unit/resources/0"):
        shards.append(documentai.Document.from_json(byte))

    actual = document_wrapper._pages_from_shards(shards=shards)
    assert len(actual[0].paragraphs) == 31


def test_entities_from_shard():
    shards = []
    for byte in get_bytes("tests/unit/resources/0"):
        shards.append(documentai.Document.from_json(byte))

    actual = document_wrapper._entities_from_shards(shards=shards)

    assert actual[0].mention_text == "$140.00"
    assert actual[0].type_ == "vat"


def test_document_wrapper_with_single_shard():
    with mock.patch.object(document_wrapper, "_get_bytes") as factory:
        factory.return_value = get_bytes("tests/unit/resources/0")
        actual = DocumentWrapper("gs://test-directory/documentai/output/123456789/0")
        assert len(actual.pages) == 1


def test_document_wrapper_with_multiple_shards():
    with mock.patch.object(document_wrapper, "_get_bytes") as factory:
        factory.return_value = get_bytes("tests/unit/resources/1")
        actual = DocumentWrapper("gs://test-directory/documentai/output/123456789/1")
        assert len(actual.pages) == 48
