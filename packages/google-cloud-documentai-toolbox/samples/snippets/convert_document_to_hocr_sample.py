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


# [START documentai_toolbox_document_to_hocr]

from google.cloud.documentai_toolbox import document

# TODO(developer): Uncomment these variables before running the sample.
# Given a document.proto or sharded document.proto in path gs://bucket/path/to/folder
# document_path = "path/to/local/document.json"
# document_title = "your-document-title"


def convert_document_to_hocr_sample(document_path: str, document_title: str) -> str:
    wrapped_document = document.Document.from_document_path(document_path=document_path)

    # Converting wrapped_document to hOCR format
    hocr_string = wrapped_document.export_hocr_str(title=document_title)

    print("Document converted to hOCR!")
    return hocr_string


# [END documentai_toolbox_document_to_hocr]
