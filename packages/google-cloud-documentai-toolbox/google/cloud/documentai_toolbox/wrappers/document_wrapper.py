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
#
"""Wrappers for Document AI Document type."""

import dataclasses
import re
from typing import List

from google.cloud import documentai
from google.cloud import storage

from google.cloud.documentai_toolbox.wrappers import page_wrapper, entity_wrapper


def _entities_from_shards(
    shards: documentai.Document,
) -> List[entity_wrapper.EntityWrapper]:
    result = []
    for shard in shards:
        for entity in shard.entities:
            result.append(entity_wrapper.EntityWrapper.from_documentai_entity(entity))
    return result


def _pages_from_shards(shards: documentai.Document) -> List[page_wrapper.PageWrapper]:
    result = []
    for shard in shards:
        text = shard.text
        for page in shard.pages:
            result.append(page_wrapper.PageWrapper.from_documentai_page(page, text))

    return result


def _get_bytes(output_bucket: str, output_prefix: str) -> List[bytes]:
    result = []

    storage_client = storage.Client()

    blob_list = storage_client.list_blobs(output_bucket, prefix=output_prefix)

    for blob in blob_list:
        if blob.name.endswith(".json"):
            blob_as_bytes = blob.download_as_bytes()
            result.append(blob_as_bytes)

    return result


def _read_output(gcs_prefix: str) -> List[documentai.Document]:
    """Returns a list of Document shards."""

    shards = []

    match = re.match(r"gs://(.*?)/(.*)", gcs_prefix)

    if match is None:
        raise ValueError("gcs_prefix does not match accepted format")

    output_bucket, output_prefix = match.groups()

    file_check = re.match(r"(.*[.].*$)", output_prefix)

    if file_check is not None:
        raise ValueError("gcs_prefix cannot contain file types")

    byte_array = _get_bytes(output_bucket, output_prefix)

    for byte in byte_array:
        shards.append(documentai.Document.from_json(byte))

    return shards


@dataclasses.dataclass
class DocumentWrapper:
    """Represents a wrapped Document.

    A single Document protobuf message might be written as several JSON files on
    GCS by Document AI's BatchProcessDocuments method.  This class hides away the
    shards from the users and implements convenient methods for searching and
    extracting information within the Document.
    """

    gcs_prefix: str

    def __post_init__(self):
        self._shards = _read_output(self.gcs_prefix)
        self.pages = _pages_from_shards(shards=self._shards)
        self.entities = _entities_from_shards(shards=self._shards)

    pages: List[page_wrapper.PageWrapper] = dataclasses.field(init=False, repr=False)
    entities: List[entity_wrapper.EntityWrapper] = dataclasses.field(
        init=False, repr=False
    )
    _shards: List[documentai.Document] = dataclasses.field(init=False, repr=False)
