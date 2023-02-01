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


# [START documentai_quickstart]

from google.cloud.documentai_toolbox import document

# TODO(developer): Uncomment these variables before running the sample.
# Given a document.proto or sharded document.proto in path gs://bucket/path/to/folder
# gcs_bucket_name = 'bucket'
# gcs_prefix = 'path/to/folder' 

def quickstart_sample(gcs_bucket_name:str,gcs_prefix:str):
    wrapped_document = document.Document.from_gcs(gcs_bucket_name=gcs_bucket_name,gcs_prefix=gcs_prefix)

    print("Document Successfully Loaded!")
    print(f"\t Number of Pages: {len(dt.pages)}")
    print(f"\t Number of Entities: {len(dt.entities)}")

    for idx,page in enumerate(dt.pages):
        for paragraph in page.paragraphs:
            print(paragraph.text)
    
    for entity in enumerate(dt.entities):
        print(f"{entity.type} : {entity.mention_text}")

# [END documentai_quickstart]