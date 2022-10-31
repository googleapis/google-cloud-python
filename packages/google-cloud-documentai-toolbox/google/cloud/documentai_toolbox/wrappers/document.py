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

from google.api_core import client_info
from google.cloud import documentai
from google.cloud import storage
from google.cloud import documentai_toolbox

from google.cloud.documentai_toolbox import constants
from google.cloud.documentai_toolbox.wrappers.page import Page
from google.cloud.documentai_toolbox.wrappers.entity import Entity


def _entities_from_shards(
    shards: documentai.Document,
) -> List[Entity]:
    r"""Returns a list of Entitys.

    Args:
        shards (google.cloud.documentai.Document):
            Required. List of document shards.

    Returns:
        List[Entity]:
            a list of Entity.

    """
    result = []
    for shard in shards:
        for entity in shard.entities:
            result.append(Entity(documentai_entity=entity))
    return result


def _pages_from_shards(shards: documentai.Document) -> List[Page]:
    r"""Returns a list of Pages.

    Args:
        shards (google.cloud.documentai.Document):
            Required. List of document shards.

    Returns:
        List[Page]:
            A list of Page.

    """
    result = []
    for shard in shards:
        text = shard.text
        for page in shard.pages:
            result.append(Page(documentai_page=page, text=text))

    return result


def _get_bytes(output_bucket: str, output_prefix: str) -> List[bytes]:
    r"""Returns a list of shards as bytes.

    If the filepaths are gs://abc/def/gh/{1,2,3}.json, then output_bucket should be "abc",
    and output_prefix should be "def/gh".

    Args:
        output_bucket (str):
            Required. The name of the output_bucket.

        output_prefix (str):
            Required. The prefix of the folder where files are excluding the bucket name.

    Returns:
        List[bytes]:
            A list of shards as bytes.

    """
    result = []

    user_agent = f"{constants.USER_AGENT_PRODUCT}/{documentai_toolbox.__version__}"

    info = client_info.ClientInfo(
        client_library_version=documentai_toolbox.__version__,
        user_agent=user_agent,
    )

    storage_client = storage.Client(client_info=info)

    blob_list = storage_client.list_blobs(output_bucket, prefix=output_prefix)

    for blob in blob_list:
        if blob.name.endswith(".json"):
            blob_as_bytes = blob.download_as_bytes()
            result.append(blob_as_bytes)

    return result


def _get_shards(gcs_prefix: str) -> List[documentai.Document]:
    r"""Returns a list of google.cloud.documentai.Document from shards.

    If the filepaths are gs://abc/def/gh/{1,2,3}.json, then gcs_prefix should be "gs://abc/def/gh".

    Args:
        gcs_prefix (str):
            Required. The gcs path to a single processed document.

    Returns:
        List[google.cloud.documentai.Document]:
            A list of google.cloud.documentai.Document from shards.

    """
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


def print_gcs_document_tree(gcs_prefix: str) -> None:
    r"""Prints a tree of filenames in gcs_prefix location.

    Args:
        gcs_prefix (str):
            Required. The gcs path to the folder containing all processed documents.

            Format: `gs://{bucket}/{optional_folder}/{operation_id}`
                    where `{operation-id}` is the operation-id given from BatchProcessDocument.

    Returns:
        None.

    """
    display_filename_prefix_middle = "├──"
    display_filename_prefix_last = "└──"

    match = re.match(r"gs://(.*?)/(.*)", gcs_prefix)

    if match is None:
        raise ValueError("gcs_prefix does not match accepted format")

    output_bucket, output_prefix = match.groups()

    file_check = re.match(r"(.*[.].*$)", output_prefix)

    if file_check is not None:
        raise ValueError("gcs_prefix cannot contain file types")

    user_agent = f"{constants.USER_AGENT_PRODUCT}/{documentai_toolbox.__version__}"

    info = client_info.ClientInfo(
        client_library_version=documentai_toolbox.__version__,
        user_agent=user_agent,
    )

    storage_client = storage.Client(client_info=info)

    blob_list = storage_client.list_blobs(output_bucket, prefix=output_prefix)

    path_list = {}

    for blob in blob_list:
        file_path = blob.name.split("/")
        file_name = file_path.pop()

        file_path2 = "/".join(file_path)

        if file_path2 in path_list:
            path_list[file_path2] += f"{file_name},"
        else:
            path_list[file_path2] = f"{file_name},"

    for key in path_list:
        a = path_list[key].split(",")
        a.pop()
        print(f"{key}")
        togo = 4
        for idx, val in enumerate(a):
            if idx == len(a) - 1:
                if len(a) > 4:
                    print("│  ....")
                print(f"{display_filename_prefix_last}{val}\n")
            elif len(a) > 4 and togo != -1:
                togo -= 1
                print(f"{display_filename_prefix_middle}{val}")
            elif len(a) <= 4:
                print(f"{display_filename_prefix_middle}{val}")


@dataclasses.dataclass
class Document:
    r"""Represents a wrapped Document.

    A single Document protobuf message might be written as several JSON files on
    GCS by Document AI's BatchProcessDocuments method.  This class hides away the
    shards from the users and implements convenient methods for searching and
    extracting information within the Document.

    Attributes:
        gcs_prefix (str):
            Required.The gcs path to a single processed document.

            Format: `gs://{bucket}/{optional_folder}/{operation_id}/{folder_id}`
                    where `{operation_id}` is the operation-id given from BatchProcessDocument
                    and `{folder_id}` is the number corresponding to the target document.
    """

    shards: List[documentai.Document] = dataclasses.field(init=True, repr=False)
    gcs_prefix: str = dataclasses.field(init=True, repr=False, default=None)

    pages: List[Page] = dataclasses.field(init=False, repr=False)
    entities: List[Entity] = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        self.pages = _pages_from_shards(shards=self.shards)
        self.entities = _entities_from_shards(shards=self.shards)

    @classmethod
    def from_documentai_document(cls, documentai_document: documentai.Document):
        return Document(shards=[documentai_document])

    @classmethod
    def from_gcs_prefix(cls, gcs_prefix: str):
        shards = _get_shards(gcs_prefix=gcs_prefix)
        return Document(shards=shards, gcs_prefix=gcs_prefix)

    def search_pages(
        self, target_string: str = None, pattern: str = None
    ) -> List[Page]:
        r"""Returns the list of Page containing target_string.

        Args:
            target_string (str):
                Optional. target str.
            pattern (str):
                Optional. regex str.

        Returns:
            List[Page]:
                A list of Page.

        """
        if (target_string is None and pattern is None) or (
            target_string is not None and pattern is not None
        ):
            raise ValueError(
                "Exactly one of target_string and pattern must be specified."
            )

        found_pages = []
        for page in self.pages:
            for paragraph in page.paragraphs:
                if target_string is not None and target_string in paragraph.text:
                    found_pages.append(page)
                    break
                elif (
                    pattern is not None
                    and re.search(pattern, paragraph.text) is not None
                ):
                    found_pages.append(page)
                    break
        return found_pages

    def get_entity_by_type(self, target_type: str) -> List[Entity]:
        r"""Returns a list of wrapped entities matching target_type.

        Args:
            target_type (str):
                Required. target_type.

        Returns:
            List[Entity]:
                A list of Entity matching target_type.

        """
        return [entity for entity in self.entities if entity.type_ == target_type]
