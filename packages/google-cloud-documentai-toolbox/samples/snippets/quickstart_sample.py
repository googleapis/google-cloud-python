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

from google.cloud.documentai_toolbox import document
from google.cloud.documentai_toolbox import gcs_utilities

# TODO(developer): Uncomment these variables before running the sample.
# Given a document.proto or sharded document.proto in path gs://bucket/path/to/folder
# gcs_bucket_name = "bucket"
# gcs_prefix = "path/to/folder"


def quickstart_sample(gcs_bucket_name: str, gcs_prefix: str) -> None:
    print("Document structure in Cloud Storage")
    gcs_utilities.print_gcs_document_tree(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix
    )

    wrapped_document = document.Document.from_gcs(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix
    )
    # For all properties and methods, refer to:
    # https://cloud.google.com/python/docs/reference/documentai-toolbox/latest/google.cloud.documentai_toolbox.wrappers.document.Document

    # Alternatively, create wrapped document from:
    #
    # - Local `Document` JSON file:     `document.Document.from_document_path()`
    # - `Document` object:              `document.Document.from_documentai_document()`
    # - `BatchProcessMetadata`:         `document.Document.from_batch_process_metadata()`
    # - Batch Processing Operation:     `document.Document.from_batch_process_operation()`

    print("Document Successfully Loaded!")
    print(f"\t Number of Pages: {len(wrapped_document.pages)}")
    print(f"\t Number of Entities: {len(wrapped_document.entities)}")

    for idx, page in enumerate(wrapped_document.pages):
        print(f"Page {idx}")
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
