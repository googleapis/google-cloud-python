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
import os
import re
from typing import Dict, List, Optional

from google.api_core import client_info
from google.cloud import bigquery
from google.cloud import documentai
from google.cloud import storage
from google.cloud import documentai_toolbox

from google.cloud.documentai_toolbox import constants
from google.cloud.documentai_toolbox.wrappers.page import Page
from google.cloud.documentai_toolbox.wrappers.page import FormField
from google.cloud.documentai_toolbox.wrappers.entity import Entity

from pikepdf import Pdf


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
            for prop in entity.properties:
                result.append(Entity(documentai_entity=prop))
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

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_bucket_name=`bucket`.
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_prefix=`optional_folder/target_folder`.
    Returns:
        List[bytes]:
            A list of bytes.

    """
    result = []

    storage_client = _get_storage_client()
    blob_list = storage_client.list_blobs(gcs_bucket_name, prefix=gcs_prefix)

    for blob in blob_list:
        if (
            blob.name.endswith(constants.JSON_EXTENSION)
            or blob.content_type == constants.JSON_MIMETYPE
        ):
            result.append(blob.download_as_bytes())

    return result


def _get_shards(gcs_bucket_name: str, gcs_prefix: str) -> List[documentai.Document]:
    r"""Returns a list of documentai.Document shards from a Cloud Storage folder.

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_bucket_name=`bucket`.
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder.

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_prefix=`optional_folder/target_folder`.
    Returns:
        List[google.cloud.documentai.Document]:
            A list of documentai.Documents.

    """
    shards = []

    file_check = re.match(constants.FILE_CHECK_REGEX, gcs_prefix)

    if file_check is not None:
        raise ValueError("gcs_prefix cannot contain file types")

    byte_array = _get_bytes(gcs_bucket_name, gcs_prefix)

    for byte in byte_array:
        shards.append(documentai.Document.from_json(byte, ignore_unknown_fields=True))

    return shards


def print_gcs_document_tree(gcs_bucket_name: str, gcs_prefix: str) -> None:
    r"""Prints a tree of filenames in Cloud Storage folder.

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_bucket_name=`bucket`.
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder.

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_prefix=`optional_folder/target_folder`.
    Returns:
        None.

    """
    FILENAME_TREE_MIDDLE = "├──"
    FILENAME_TREE_LAST = "└──"
    FILES_TO_DISPLAY = 4

    file_check = re.match(constants.FILE_CHECK_REGEX, gcs_prefix)

    if file_check is not None:
        raise ValueError("gcs_prefix cannot contain file types")

    storage_client = _get_storage_client()
    blob_list = storage_client.list_blobs(gcs_bucket_name, prefix=gcs_prefix)

    path_list: Dict[str, List[str]] = {}

    for blob in blob_list:
        directory, file_name = os.path.split(blob.name)

        if directory in path_list:
            path_list[directory].append(file_name)
        else:
            path_list[directory] = [file_name]

    for directory, files in path_list.items():
        print(f"{directory}")
        dir_size = len(files)
        for idx, file_name in enumerate(files):
            if idx == dir_size - 1:
                if dir_size > FILES_TO_DISPLAY:
                    print("│  ....")
                print(f"{FILENAME_TREE_LAST}{file_name}\n")
            elif idx <= FILES_TO_DISPLAY:
                print(f"{FILENAME_TREE_MIDDLE}{file_name}")


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

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_bucket_name=`bucket`.
        gcs_prefix (Optional[str]):
            Optional. The prefix of the json files in the target_folder.

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_prefix=`optional_folder/target_folder`.

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
                Required. The path to the document.json file.
        Returns:
            Document:
                A document from local document_path.
        """

        with open(document_path, "r", encoding="utf-8") as f:
            doc = documentai.Document.from_json(f.read(), ignore_unknown_fields=True)

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

                Format: Given `gs://{bucket_name}/{optional_folder}/{operation_id}/` where gcs_bucket_name=`{bucket_name}`.
            gcs_prefix (str):
                Required. The prefix to the location of the target folder.

                Format: Given `gs://{bucket_name}/optional_folder/target_folder` where gcs_prefix=`{optional_folder}/{target_folder}`.
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
        if (target_string and pattern) or (not target_string and not pattern):
            raise ValueError(
                "Exactly one of target_string and pattern must be specified."
            )

        found_pages = []
        for page in self.pages:
            for paragraph in page.paragraphs:
                if (target_string and target_string in paragraph.text) or (
                    pattern and re.search(pattern, paragraph.text)
                ):
                    found_pages.append(page)
                    break
        return found_pages

    def get_form_field_by_name(self, target_field: str) -> List[FormField]:
        r"""Returns the list of FormFields named target_field.

        Args:
            target_field (str):
                Required. Target field name.

        Returns:
            List[FormField]:
                A list of FormField matching target_field.

        """
        found_fields = []
        for page in self.pages:
            for form_field in page.form_fields:
                if target_field.lower() in form_field.field_name.lower():
                    found_fields.append(form_field)

        return found_fields

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

    def entities_to_dict(self) -> Dict:
        r"""Returns Dictionary of entities in document.

        Returns:
            Dict:
                The Dict of the entities indexed by type.

        """
        entities_dict: Dict = {}
        for entity in self.entities:
            entity_type = entity.type_.replace("/", "_")

            existing_entity = entities_dict.get(entity_type)
            if not existing_entity:
                entities_dict[entity_type] = entity.mention_text
                continue

            # For entities that can have multiple (e.g. line_item)
            # Change Entity Type to a List
            if not isinstance(existing_entity, list):
                existing_entity = [existing_entity]

            existing_entity.append(entity.mention_text)
            entities_dict[entity_type] = existing_entity

        return entities_dict

    def entities_to_bigquery(
        self, dataset_name: str, table_name: str, project_id: Optional[str] = None
    ) -> bigquery.job.LoadJob:
        r"""Adds extracted entities to a BigQuery table.

        Args:
            dataset_name (str):
                Required. Name of the BigQuery dataset.
            table_name (str):
                Required. Name of the BigQuery table.
            project_id (Optional[str]):
                Optional. Project ID containing the BigQuery table. If not passed, falls back to the default inferred from the environment.
        Returns:
            bigquery.job.LoadJob:
                The BigQuery LoadJob for adding the entities.

        """
        bq_client = bigquery.Client(project=project_id)
        table_ref = bigquery.DatasetReference(
            project=project_id, dataset_id=dataset_name
        ).table(table_name)

        job_config = bigquery.LoadJobConfig(
            schema_update_options=[
                bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
                bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
            ],
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        )

        return bq_client.load_table_from_json(
            json_rows=[self.entities_to_dict()],
            destination=table_ref,
            job_config=job_config,
        )

    def split_pdf(self, pdf_path: str, output_path: str) -> List[str]:
        r"""Splits local PDF file into multiple PDF files based on output from a Splitter/Classifier processor.

        Args:
            pdf_path (str):
                Required. The path to the PDF file.
            output_path (str):
                Required. The path to the output directory.
        Returns:
            List[str]:
                A list of output pdf files.
        """
        output_files: List[str] = []
        input_filename, input_extension = os.path.splitext(os.path.basename(pdf_path))
        with Pdf.open(pdf_path) as f:
            for entity in self.entities:
                subdoc_type = entity.type_ or "subdoc"

                if entity.start_page == entity.end_page:
                    page_range = f"pg{entity.start_page + 1}"
                else:
                    page_range = f"pg{entity.start_page + 1}-{entity.end_page + 1}"

                output_filename = (
                    f"{input_filename}_{page_range}_{subdoc_type}{input_extension}"
                )

                subdoc = Pdf.new()
                for page_num in range(entity.start_page, entity.end_page + 1):
                    subdoc.pages.append(f.pages[page_num])

                subdoc.save(
                    os.path.join(
                        output_path,
                        output_filename,
                    ),
                    min_version=f.pdf_version,
                )
                output_files.append(output_filename)
        return output_files
