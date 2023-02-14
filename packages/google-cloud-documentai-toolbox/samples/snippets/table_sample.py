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


# [START documentai_toolbox_table]

from google.cloud.documentai_toolbox import document

# TODO(developer): Uncomment these variables before running the sample.
# Given a local document.proto or sharded document.proto in path
# document_path = "path/to/local/document.json"
# output_file_prefix = "output/table"


def table_sample(document_path: str, output_file_prefix: str) -> None:
    wrapped_document = document.Document.from_document_path(document_path=document_path)

    print("Tables in Document")
    for page_number, page in enumerate(wrapped_document.pages):
        for table_number, table in enumerate(page.tables):
            print(table.to_dataframe())

            # Write table to CSV file
            output_file = f"{output_file_prefix}-{page_number}-{table_number}.csv"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(wrapped_document.pages[0].tables[0].to_csv())


# [END documentai_toolbox_table]
