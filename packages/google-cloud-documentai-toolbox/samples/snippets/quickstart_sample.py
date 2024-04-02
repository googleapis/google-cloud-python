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


# [START documentai_toolbox_quickstart]
from typing import Optional

from google.cloud import documentai
from google.cloud.documentai_toolbox import document, gcs_utilities

# TODO(developer): Uncomment these variables before running the sample.
# Given a Document JSON or sharded Document JSON in path gs://bucket/path/to/folder
# gcs_bucket_name = "bucket"
# gcs_prefix = "path/to/folder"

# Or, given a Document JSON in path gs://bucket/path/to/folder/document.json
# gcs_uri = "gs://bucket/path/to/folder/document.json"

# Or, given a Document JSON in path local/path/to/folder/document.json
# document_path = "local/path/to/folder/document.json"

# Or, given a Document object from Document AI
# documentai_document = documentai.Document()

# Or, given a BatchProcessMetadata object from Document AI
# operation = client.batch_process_documents(request)
# operation.result(timeout=timeout)
# batch_process_metadata = documentai.BatchProcessMetadata(operation.metadata)

# Or, given a BatchProcessOperation name from Document AI
# batch_process_operation = "projects/project_id/locations/location/operations/operation_id"


def quickstart_sample(
    gcs_bucket_name: Optional[str] = None,
    gcs_prefix: Optional[str] = None,
    gcs_uri: Optional[str] = None,
    document_path: Optional[str] = None,
    documentai_document: Optional[documentai.Document] = None,
    batch_process_metadata: Optional[documentai.BatchProcessMetadata] = None,
    batch_process_operation: Optional[str] = None,
) -> document.Document:
    if gcs_bucket_name and gcs_prefix:
        # Load from Google Cloud Storage Directory
        print("Document structure in Cloud Storage")
        gcs_utilities.print_gcs_document_tree(
            gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix
        )

        wrapped_document = document.Document.from_gcs(
            gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix
        )
    elif gcs_uri:
        # Load a single Document from a Google Cloud Storage URI
        wrapped_document = document.Document.from_gcs_uri(gcs_uri=gcs_uri)
    elif document_path:
        # Load from local `Document` JSON file
        wrapped_document = document.Document.from_document_path(document_path)
    elif documentai_document:
        # Load from `documentai.Document` object
        wrapped_document = document.Document.from_documentai_document(
            documentai_document
        )
    elif batch_process_metadata:
        # Load Documents from `BatchProcessMetadata` object
        wrapped_documents = document.Document.from_batch_process_metadata(
            metadata=batch_process_metadata
        )
        wrapped_document = wrapped_documents[0]
    elif batch_process_operation:
        wrapped_documents = document.Document.from_batch_process_operation(
            location="us", operation_name=batch_process_operation
        )
        wrapped_document = wrapped_documents[0]
    else:
        raise ValueError("No document source provided.")

    # For all properties and methods, refer to:
    # https://cloud.google.com/python/docs/reference/documentai-toolbox/latest/google.cloud.documentai_toolbox.wrappers.document.Document

    print("Document Successfully Loaded!")
    print(f"\t Number of Pages: {len(wrapped_document.pages)}")
    print(f"\t Number of Entities: {len(wrapped_document.entities)}")

    for page in wrapped_document.pages:
        print(f"Page {page.page_number}")
        for block in page.blocks:
            print(block.text)
        for paragraph in page.paragraphs:
            print(paragraph.text)
        for line in page.lines:
            print(line.text)
        for token in page.tokens:
            print(token.text)

        # Only supported with Form Parser processor
        # https://cloud.google.com/document-ai/docs/form-parser
        for form_field in page.form_fields:
            print(f"{form_field.field_name} : {form_field.field_value}")

        # Only supported with Enterprise Document OCR version `pretrained-ocr-v2.0-2023-06-02`
        # https://cloud.google.com/document-ai/docs/process-documents-ocr#enable_symbols
        for symbol in page.symbols:
            print(symbol.text)

        # Only supported with Enterprise Document OCR version `pretrained-ocr-v2.0-2023-06-02`
        # https://cloud.google.com/document-ai/docs/process-documents-ocr#math_ocr
        for math_formula in page.math_formulas:
            print(math_formula.text)

    # Only supported with Entity Extraction processors
    # https://cloud.google.com/document-ai/docs/processors-list
    for entity in wrapped_document.entities:
        print(f"{entity.type_} : {entity.mention_text}")
        if entity.normalized_text:
            print(f"\tNormalized Text: {entity.normalized_text}")

    # [END documentai_toolbox_quickstart]

    return wrapped_document
