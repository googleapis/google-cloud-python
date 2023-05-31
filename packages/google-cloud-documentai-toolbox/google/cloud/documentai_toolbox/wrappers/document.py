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

from google.api_core.client_options import ClientOptions

from google.cloud import bigquery
from google.cloud import documentai

from google.cloud.documentai_toolbox import constants

from google.cloud.documentai_toolbox.utilities import gcs_utilities

from google.cloud.documentai_toolbox.wrappers.page import Page
from google.cloud.documentai_toolbox.wrappers.page import FormField
from google.cloud.documentai_toolbox.wrappers.entity import Entity

from google.cloud.vision import AnnotateFileResponse, ImageAnnotationContext
from google.cloud.vision import AnnotateImageResponse

from google.cloud.documentai_toolbox.wrappers import page

from google.cloud.documentai_toolbox.converters.vision_helpers import (
    _convert_document_page,
    _generate_entity_annotations,
    _get_text_anchor_substring,
    PageInfo,
)

from google.longrunning.operations_pb2 import Operation, GetOperationRequest

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
        for documentai_entity in shard.entities:
            entity = Entity(documentai_entity=documentai_entity)
            entity.crop_image(shard)
            result.append(entity)
            for documentai_prop in documentai_entity.properties:
                prop = Entity(documentai_entity=documentai_prop)
                prop.crop_image(shard)
                result.append(prop)

    if len(result) > 1 and result[0].documentai_entity.id:
        result.sort(key=lambda x: int(x.documentai_entity.id))
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
        for shard_page in shard.pages:
            result.append(Page(documentai_page=shard_page, text=text))

    return result


def _get_shards(gcs_bucket_name: str, gcs_prefix: str) -> List[documentai.Document]:
    r"""Returns a list of documentai.Document shards from a Cloud Storage folder.

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/` where gcs_bucket_name=`bucket`.
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder.

            Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/` where gcs_prefix=`{optional_folder}/{target_folder}`.
    Returns:
        List[google.cloud.documentai.Document]:
            A list of documentai.Documents.

    """
    shards = []

    file_check = re.match(constants.FILE_CHECK_REGEX, gcs_prefix)

    if file_check is not None:
        raise ValueError("gcs_prefix cannot contain file types")

    byte_array = gcs_utilities.get_bytes(gcs_bucket_name, gcs_prefix)

    for byte in byte_array:
        shards.append(documentai.Document.from_json(byte, ignore_unknown_fields=True))

    if len(shards) > 1:
        shards.sort(key=lambda x: int(x.shard_info.shard_index))
    return shards


def _text_from_shards(shards: List[documentai.Document]) -> str:
    r"""Gets text from shards.

    Args:
        shards (List[google.cloud.documentai.Document]):
            Required. List of document shards.
    Returns:
        str:
            Text in all shards.
    """
    total_text = ""
    for shard in shards:
        if total_text == "":
            total_text = shard.text
        elif total_text != shard.text:
            total_text += shard.text

    return total_text


def _convert_to_vision_annotate_file_response(text: str, pages: List[page.Page]):
    r"""Convert OCR data from Document.proto to AnnotateFileResponse.proto for Vision API.

    Args:
        text (str):
            Required. Contents of document.
        pages (List[Page]):
            Required. A list of pages.
    Returns:
        AnnotateFileResponse:
            Proto with TextAnnotations.
    """
    responses = []
    vision_file_response = AnnotateFileResponse()
    page_idx = 0
    while page_idx < len(pages):
        page_info = PageInfo(pages[page_idx].documentai_page, text)

        full_text_annotation = _convert_document_page(page_info)
        full_text_annotation.text = _get_text_anchor_substring(
            text, pages[page_idx].documentai_page.layout.text_anchor
        )
        text_annotations = _generate_entity_annotations(page_info)

        responses.append(
            AnnotateImageResponse(
                full_text_annotation=full_text_annotation,
                text_annotations=text_annotations,
                context=ImageAnnotationContext(page_number=page_idx + 1),
            )
        )
        page_idx += 1

    vision_file_response.responses = responses

    return vision_file_response


def _get_batch_process_metadata(
    location: str, operation_name: str
) -> documentai.BatchProcessMetadata:
    r"""Get `BatchProcessMetadata` from a `batch_process_documents()` long-running operation.

    Args:
        location (str):
            Required. The location of the processor used for `batch_process_documents()`.

        operation_name (str):
            Required. The fully qualified operation name for a `batch_process_documents()` operation.
    Returns:
        documentai.BatchProcessMetadata:
            Metadata from batch process.
    """
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    while True:
        operation: Operation = client.get_operation(
            request=GetOperationRequest(name=operation_name)
        )

        if operation.done:
            break

    if not operation.metadata:
        raise ValueError(f"Operation does not contain metadata: {operation}")

    metadata_type = (
        "type.googleapis.com/google.cloud.documentai.v1.BatchProcessMetadata"
    )

    if not operation.metadata.type_url or operation.metadata.type_url != metadata_type:
        raise ValueError(
            f"Operation metadata type is not `{metadata_type}`. Type is `{operation.metadata.type_url}`."
        )

    metadata: documentai.BatchProcessMetadata = (
        documentai.BatchProcessMetadata.deserialize(operation.metadata.value)
    )

    return metadata


def _insert_into_dictionary_with_list(dic: Dict, key: str, value: str) -> Dict:
    r"""Inserts value into a dictionary that can contain lists.

    Args:
        dic (Dict):
            Required. The dictionary to insert into.
        key (str):
            Required. The key to be created or inserted into.
        value (str):
            Required. The value to be inserted.

    Returns:
        Dict:
            The dictionary after adding the key value pair.
    """
    existing_value = dic.get(key)

    if existing_value:
        # For duplicate keys,
        # Change Type to a List if not already
        if not isinstance(existing_value, list):
            existing_value = [existing_value]

        existing_value.append(value)
        dic[key] = existing_value
    else:
        dic[key] = value

    return dic


def _bigquery_column_name(input_string: str) -> str:
    r"""Converts a string into a BigQuery column name.
        https://cloud.google.com/bigquery/docs/schemas#column_names

    Args:
        input_string (str):
            Required: The string to convert.
    Returns:
        str
            The converted string.

    """
    char_map: Dict[str, str] = {
        r":|;|\(|\)|\[|\]|,|\.|\?|\!|\'|\n": "",
        r"/| ": "_",
        r"#": "num",
        r"@": "at",
    }

    for key, value in char_map.items():
        input_string = re.sub(key, value, input_string)

    return input_string.lower()


def _dict_to_bigquery(
    dic: Dict,
    dataset_name: str,
    table_name: str,
    project_id: Optional[str],
) -> bigquery.job.LoadJob:
    r"""Loads dictionary to a BigQuery table.

    Args:
        dic (Dict):
            Required: The dictionary to insert.
        dataset_name (str):
            Required. Name of the BigQuery dataset.
        table_name (str):
            Required. Name of the BigQuery table.
        project_id (Optional[str]):
            Optional. Project ID containing the BigQuery table. If not passed, falls back to the default inferred from the environment.
    Returns:
        bigquery.job.LoadJob:
            The BigQuery LoadJob for adding the dictionary.

    """
    bq_client = bigquery.Client(
        project=project_id, client_info=gcs_utilities._get_client_info()
    )
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
        json_rows=[dic],
        destination=table_ref,
        job_config=job_config,
    )


@dataclasses.dataclass
class Document:
    r"""Represents a wrapped `Document`.

    This class hides away the complexities of using `Document` protobuf
    response outputted by `BatchProcessDocuments` or `ProcessDocument`
    methods and implements convenient methods for searching and
    extracting information within the `Document`.

    Attributes:
        shards: (List[google.cloud.documentai.Document]):
            Optional. A list of documentai.Document shards of the same Document.
            Each shard consists of a number of pages in the Document.
        gcs_bucket_name (Optional[str]):
            Optional. The name of the gcs bucket.

            Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/` where gcs_bucket_name=`bucket`.
        gcs_prefix (Optional[str]):
            Optional. The prefix of the json files in the target_folder.

            Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/` where gcs_prefix=`{optional_folder}/{target_folder}`.

            For more information please take a look at https://cloud.google.com/storage/docs/json_api/v1/objects/list .
        pages: (List[Page]):
            A list of Pages in the Document.
        entities: (List[Entity]):
            A list of Entities in the Document.
    """

    shards: List[documentai.Document] = dataclasses.field(repr=False)
    gcs_bucket_name: Optional[str] = dataclasses.field(default=None, repr=False)
    gcs_prefix: Optional[str] = dataclasses.field(default=None, repr=False)
    gcs_input_uri: Optional[str] = dataclasses.field(default=None, repr=False)

    pages: List[Page] = dataclasses.field(init=False, repr=False)
    entities: List[Entity] = dataclasses.field(init=False, repr=False)
    text: str = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        self.pages = _pages_from_shards(shards=self.shards)
        self.entities = _entities_from_shards(shards=self.shards)
        self.text = _text_from_shards(shards=self.shards)

    @classmethod
    def from_document_path(
        cls,
        document_path: str,
    ):
        r"""Loads Document from local document_path.

            .. code-block:: python

                from google.cloud.documentai_toolbox import document

                document_path = "/path/to/local/file.json
                wrapped_document = document.Document.from_document_path(document_path)

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

            .. code-block:: python

                from google.cloud import documentai
                from google.cloud.documentai_toolbox import document

                documentai_document = client.process_documents(request).document
                wrapped_document = document.Document.from_documentai_document(documentai_document)

        Args:
            documentai_document (documentai.Document):
                Optional. The Document.proto response.
        Returns:
            Document:
                A document from local documentai_document.
        """

        return cls(shards=[documentai_document])

    @classmethod
    def from_gcs(cls, gcs_bucket_name: str, gcs_prefix: str, gcs_input_uri: str = None):
        r"""Loads Document from Cloud Storage.

        Args:
            gcs_bucket_name (str):
                Required. The gcs bucket.

                Format: Given `gs://{bucket_name}/{optional_folder}/{operation_id}/` where gcs_bucket_name=`{bucket_name}`.
            gcs_prefix (str):
                Required. The prefix to the location of the target folder.

                Format: Given `gs://{bucket_name}/{optional_folder}/{target_folder}` where gcs_prefix=`{optional_folder}/{target_folder}`.
            gcs_input_uri (str):
                Optional. The gcs uri to the original input file.

                Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/{file_name}.pdf`
        Returns:
            Document:
                A document from gcs.
        """
        shards = _get_shards(gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix)
        return cls(
            shards=shards,
            gcs_bucket_name=gcs_bucket_name,
            gcs_prefix=gcs_prefix,
            gcs_input_uri=gcs_input_uri,
        )

    @classmethod
    def from_batch_process_metadata(cls, metadata: documentai.BatchProcessMetadata):
        r"""Loads Documents from Cloud Storage, using the output from `BatchProcessMetadata`.

            .. code-block:: python

                from google.cloud import documentai

                operation = client.batch_process_documents(request)
                operation.result(timeout=timeout)
                metadata = documentai.BatchProcessMetadata(operation.metadata)

        Args:
            metadata (documentai.BatchProcessMetadata):
                Required. The operation metadata after a `batch_process_documents()` operation completes.

        Returns:
            List[Document]:
                A list of wrapped documents from gcs. Each document corresponds to an input file.
        """
        if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
            raise ValueError(f"Batch Process Failed: {metadata.state_message}")

        documents: List[Document] = []
        # Each process corresponds to one input document
        for process in list(metadata.individual_process_statuses):
            # output_gcs_destination format: gs://BUCKET/PREFIX/OPERATION_NUMBER/INPUT_FILE_NUMBER/
            gcs_bucket_name, gcs_prefix = gcs_utilities.split_gcs_uri(
                process.output_gcs_destination
            )

            documents.append(
                Document.from_gcs(
                    gcs_bucket_name, gcs_prefix, gcs_input_uri=process.input_gcs_source
                )
            )

        return documents

    @classmethod
    def from_batch_process_operation(cls, location: str, operation_name: str):
        r"""Loads Documents from Cloud Storage, using the operation name returned from `batch_process_documents()`.

            .. code-block:: python

                from google.cloud import documentai

                operation = client.batch_process_documents(request)
                operation_name = operation.operation.name

        Args:
            location (str):
                Required. The location of the processor used for `batch_process_documents()`.

            operation_name (str):
                Required. The fully qualified operation name for a `batch_process_documents()` operation.

        Returns:
            List[Document]:
                A list of wrapped documents from gcs. Each document corresponds to an input file.
        """
        return cls.from_batch_process_metadata(
            metadata=_get_batch_process_metadata(
                location=location, operation_name=operation_name
            )
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
        for p in self.pages:
            for paragraph in p.paragraphs:
                if (target_string and target_string in paragraph.text) or (
                    pattern and re.search(pattern, paragraph.text)
                ):
                    found_pages.append(p)
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
        for p in self.pages:
            for form_field in p.form_fields:
                if target_field.lower() in form_field.field_name.lower():
                    found_fields.append(form_field)

        return found_fields

    def form_fields_to_dict(self) -> Dict:
        r"""Returns Dictionary of form fields in document.

        Returns:
            Dict:
                The Dict of the form fields indexed by type.

        """
        form_fields_dict: Dict = {}
        for p in self.pages:
            for form_field in p.form_fields:
                field_name = _bigquery_column_name(form_field.field_name)
                form_fields_dict = _insert_into_dictionary_with_list(
                    form_fields_dict, field_name, form_field.field_value
                )

        return form_fields_dict

    def form_fields_to_bigquery(
        self, dataset_name: str, table_name: str, project_id: Optional[str] = None
    ) -> bigquery.job.LoadJob:
        r"""Adds extracted form fields to a BigQuery table.

        Args:
            dataset_name (str):
                Required. Name of the BigQuery dataset.
            table_name (str):
                Required. Name of the BigQuery table.
            project_id (Optional[str]):
                Optional. Project ID containing the BigQuery table. If not passed, falls back to the default inferred from the environment.
        Returns:
            bigquery.job.LoadJob:
                The BigQuery LoadJob for adding the form fields.

        """

        return _dict_to_bigquery(
            self.form_fields_to_dict(),
            dataset_name,
            table_name,
            project_id,
        )

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
            entity_type = _bigquery_column_name(entity.type_)
            entities_dict = _insert_into_dictionary_with_list(
                entities_dict, entity_type, entity.mention_text
            )

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

        return _dict_to_bigquery(
            self.entities_to_dict(),
            dataset_name,
            table_name,
            project_id,
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

    def convert_document_to_annotate_file_response(self) -> AnnotateFileResponse:
        r"""Convert OCR data from Document.proto to AnnotateFileResponse.proto for Vision API.

        Args:
            None.
        Returns:
            AnnotateFileResponse:
                Proto with TextAnnotations.
        """
        return _convert_to_vision_annotate_file_response(self.text, self.pages)

    def export_images(
        self, output_path: str, output_file_prefix: str, output_file_extension: str
    ) -> List[str]:
        r"""Exports images from `Document` to files.

        Args:
            output_path (str):
                Required. The path to the output directory.
            output_file_prefix (str):
                Required. The output file name prefix.
            output_file_extension (str):
                Required. The output file extension.

                Format: `png`, `jpg`, etc.
        Returns:
            List[str]:
                A list of output image file names.
                Format: `{output_path}/{output_file_prefix}_{index}_{Entity.type_}.{output_file_extension}`
        """
        output_filenames: List[str] = []
        index = 0
        for entity in self.entities:
            if not entity.image:
                continue

            output_filename = (
                f"{output_file_prefix}_{index}_{entity.type_}.{output_file_extension}"
            )
            entity.image.save(os.path.join(output_path, output_filename))
            output_filenames.append(output_filename)
            index += 1

        return output_filenames
