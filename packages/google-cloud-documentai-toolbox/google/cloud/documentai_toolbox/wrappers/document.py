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
#
"""Wrappers for Document AI Document type."""

import dataclasses
import re
from typing import List, Optional

from google.api_core import client_info
from google.cloud import documentai
from google.cloud import storage
from google.cloud import documentai_toolbox

from google.cloud.documentai_toolbox import constants
from google.cloud.documentai_toolbox.wrappers.page import Page
from google.cloud.documentai_toolbox.wrappers.entity import Entity


def _entities_from_shards(
    shards: List[documentai.Document],
) -> List[Entity]:
    r"""Returns a list of Entities from a list of documentai.Document shards.

    Args:
        shards (List[google.cloud.documentai.Document]):
            Required. List of document shards.

    Returns:
        List[Entity]:
            a list of Entities.
    """
    result = []
    for shard in shards:
        for entity in shard.entities:
            result.append(Entity(documentai_entity=entity))
    return result


def _pages_from_shards(shards: List[documentai.Document]) -> List[Page]:
    r"""Returns a list of Pages from a list of documentai.Document shards.

    Args:
        shards (List[google.cloud.documentai.Document]):
            Required. List of document shards.

    Returns:
        List[Page]:
            A list of Pages.
    """
    result = []
    for shard in shards:
        text = shard.text
        for page in shard.pages:
            result.append(Page(documentai_page=page, text=text))

    return result


def _get_storage_client():
    r"""Returns a Storage client with custom user agent header.

    Returns:
        storage.Client.

    """
    user_agent = f"{constants.USER_AGENT_PRODUCT}/{documentai_toolbox.__version__}"

    info = client_info.ClientInfo(
        client_library_version=documentai_toolbox.__version__,
        user_agent=user_agent,
    )

    return storage.Client(client_info=info)


def _get_bytes(gcs_bucket_name: str, gcs_prefix: str) -> List[bytes]:
    r"""Returns a list of bytes of json files from Cloud Storage.

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: gs://{bucket}/{optional_folder}/{target_folder}/
                    where gcs_bucket_name={bucket} .
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder

            Format: gs://{bucket}/{optional_folder}/{target_folder}/
                    where gcs_prefix={optional_folder}/{target_folder}/ .
    Returns:
        List[bytes]:
            A list of bytes.

    """
    result = []

    storage_client = _get_storage_client()
    blob_list = storage_client.list_blobs(gcs_bucket_name, prefix=gcs_prefix)

    for blob in blob_list:
        if blob.name.endswith(".json"):
            blob_as_bytes = blob.download_as_bytes()
            result.append(blob_as_bytes)

    return result


def _get_shards(gcs_bucket_name: str, gcs_prefix: str) -> List[documentai.Document]:
    r"""Returns a list of documentai.Document shards from a Cloud Storage folder.

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: gs://{bucket}/{optional_folder}/{target_folder}/
                    where gcs_bucket_name={bucket}.
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder.

            Format: gs://{bucket}/{optional_folder}/{target_folder}/
                    where gcs_prefix={optional_folder}/{target_folder}/.
    Returns:
        List[google.cloud.documentai.Document]:
            A list of documentai.Documents.

    """
    shards = []

    file_check = re.match(r"(.*[.].*$)", gcs_prefix)

    if file_check is not None:
        raise ValueError("gcs_prefix cannot contain file types")

    byte_array = _get_bytes(gcs_bucket_name, gcs_prefix)

    for byte in byte_array:
        shards.append(documentai.Document.from_json(byte))

    return shards


def print_gcs_document_tree(gcs_bucket_name: str, gcs_prefix: str) -> None:
    r"""Prints a tree of filenames in Cloud Storage folder.

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: gs://{bucket}/{optional_folder}/{target_folder}/
                    where gcs_bucket_name={bucket}.
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder.

            Format: gs://{bucket}/{optional_folder}/{target_folder}/
                    where gcs_prefix={optional_folder}/{target_folder}/ .
    Returns:
        None.

    """
    display_filename_prefix_middle = "├──"
    display_filename_prefix_last = "└──"

    file_check = re.match(r"(.*[.].*$)", gcs_prefix)

    if file_check is not None:
        raise ValueError("gcs_prefix cannot contain file types")

    storage_client = _get_storage_client()
    blob_list = storage_client.list_blobs(gcs_bucket_name, prefix=gcs_prefix)

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

    This class hides away the complexities of using Document protobuf
    response outputted by BatchProcessDocuments or ProcessDocument
    methods and implements convenient methods for searching and
    extracting information within the Document.

    Attributes:
        shards: (List[google.cloud.documentai.Document]):
            Optional. A list of documentai.Document shards of the same Document.
            Each shard consists of a number of pages in the Document.
        gcs_bucket_name (Optional[str]):
            Optional. The name of the gcs bucket.

            Format: gs://{bucket}/{optional_folder}/{target_folder}/
                    where gcs_bucket_name={bucket}.
        gcs_prefix (Optional[str]):
            Optional. The prefix of the json files in the target_folder.

            Format: gs://{bucket}/{optional_folder}/{target_folder}/
                    where gcs_prefix={optional_folder}/{target_folder}/.

            For more information please take a look at https://cloud.google.com/storage/docs/json_api/v1/objects/list .
        pages: (List[Page]):
            A list of Pages in the Document.
        entities: (List[Entity]):
            A list of Entities in the Document.
    """

    shards: List[documentai.Document] = dataclasses.field(repr=False)
    gcs_bucket_name: Optional[str] = dataclasses.field(default=None, repr=False)
    gcs_prefix: Optional[str] = dataclasses.field(default=None, repr=False)

    pages: List[Page] = dataclasses.field(init=False, repr=False)
    entities: List[Entity] = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        self.pages = _pages_from_shards(shards=self.shards)
        self.entities = _entities_from_shards(shards=self.shards)

    @classmethod
    def from_document_path(
        cls,
        document_path: str,
    ):
        r"""Loads Document from local document_path.

        Args:
            document_path (str):
                Required. The path to the resp.
        Returns:
            Document:
                A document from local document_path.
        """

        with open(document_path, "r") as f:
            doc = documentai.Document.from_json(f.read())

        return cls(shards=[doc])

    @classmethod
    def from_documentai_document(
        cls,
        documentai_document: documentai.Document,
    ):
        r"""Loads Document from local documentai_document.

        Args:
            documentai_document (documentai.Document):
                Optional. The Document.proto response.
        Returns:
            Document:
                A document from local documentai_document.
        """

        return cls(shards=[documentai_document])

    @classmethod
    def from_gcs(cls, gcs_bucket_name: str, gcs_prefix: str):
        r"""Loads Document from Cloud Storage.

        Args:
            gcs_bucket_name (str):
                Required. The gcs bucket.

                Format: Given `gs://{bucket_name}/{optional_folder}/{operation_id}/`
                        gcs_bucket_name="{bucket_name}".
            gcs_prefix (str):
                Required. The prefix to the location of the target folder.

                Format: Given `gs://{bucket_name}/{optional_folder}/{target_folder}/`
                        gcs_prefix="{optional_folder}/{target_folder}".
        Returns:
            Document:
                A document from gcs.
        """
        shards = _get_shards(gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix)
        return cls(
            shards=shards, gcs_prefix=gcs_prefix, gcs_bucket_name=gcs_bucket_name
        )

    def search_pages(
        self, target_string: Optional[str] = None, pattern: Optional[str] = None
    ) -> List[Page]:
        r"""Returns the list of Pages containing target_string or text matching pattern.

        Args:
            target_string (Optional[str]):
                Optional. target str.
            pattern (Optional[str]):
                Optional. regex str.

        Returns:
            List[Page]:
                A list of Pages.

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
        r"""Returns the list of Entities of target_type.

        Args:
            target_type (str):
                Required. target_type.

        Returns:
            List[Entity]:
                A list of Entity matching target_type.

        """
        return [entity for entity in self.entities if entity.type_ == target_type]
