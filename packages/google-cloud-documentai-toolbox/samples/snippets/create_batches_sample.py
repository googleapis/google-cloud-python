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


# [START documentai_toolbox_create_batches]

from google.cloud import documentai
from google.cloud.documentai_toolbox import gcs_utilities

# TODO(developer): Uncomment these variables before running the sample.
# Given unprocessed documents in path gs://bucket/path/to/folder
# gcs_bucket_name = "bucket"
# gcs_prefix = "path/to/folder"
# batch_size = 50


def create_batches_sample(
    gcs_bucket_name: str,
    gcs_prefix: str,
    batch_size: int = 50,
) -> None:
    # Creating batches of documents for processing
    batches = gcs_utilities.create_batches(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix, batch_size=batch_size
    )

    print(f"{len(batches)} batch(es) created.")
    for batch in batches:
        print(f"{len(batch.gcs_documents.documents)} files in batch.")
        print(batch.gcs_documents.documents)

        # Use as input for batch_process_documents()
        # Refer to https://cloud.google.com/document-ai/docs/send-request
        # for how to send a batch processing request
        request = documentai.BatchProcessRequest(
            name="processor_name", input_documents=batch
        )


# [END documentai_toolbox_create_batches]
