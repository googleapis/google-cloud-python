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

    print("Document Successfully Loaded!")
    print(f"\t Number of Pages: {len(wrapped_document.pages)}")
    print(f"\t Number of Entities: {len(wrapped_document.entities)}")

    for idx, page in enumerate(wrapped_document.pages):
        print(f"Page {idx}")
        for block in page.blocks:
            print(block.text)
        for paragraph in page.paragraphs:
            print(paragraph.text)

    for entity in wrapped_document.entities:
        print(f"{entity.type_} : {entity.mention_text}")


# [END documentai_toolbox_quickstart]
