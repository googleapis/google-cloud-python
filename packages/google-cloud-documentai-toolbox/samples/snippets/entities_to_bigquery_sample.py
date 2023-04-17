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


# [START documentai_toolbox_entities_to_bigquery]

from google.cloud.documentai_toolbox import document

# TODO(developer): Uncomment these variables before running the sample.
# Given a document.proto or sharded document.proto in path gs://bucket/path/to/folder
# gcs_bucket_name = "bucket"
# gcs_prefix = "path/to/folder"
# dataset_name = "test_dataset"
# table_name = "test_table"
# project_id = "YOUR_PROJECT_ID"


def entities_to_bigquery_sample(
    gcs_bucket_name: str,
    gcs_prefix: str,
    dataset_name: str,
    table_name: str,
    project_id: str,
) -> None:
    wrapped_document = document.Document.from_gcs(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix
    )

    job = wrapped_document.entities_to_bigquery(
        dataset_name=dataset_name, table_name=table_name, project_id=project_id
    )

    # Also supported:
    # job = wrapped_document.form_fields_to_bigquery(
    #     dataset_name=dataset_name, table_name=table_name, project_id=project_id
    # )

    print("Document entities loaded into BigQuery")
    print(f"Job ID: {job.job_id}")
    print(f"Table: {job.destination.path}")


# [END documentai_toolbox_entities_to_bigquery]
