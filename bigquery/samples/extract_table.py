# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def extract_table(client, to_delete):

    # [START bigquery_extract_table]
    bucket_name = "extract_shakespeare_{}".format(_millis())
    storage_client = storage.Client()
    bucket = retry_storage_errors(storage_client.create_bucket)(bucket_name)
    to_delete.append(bucket)

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # bucket_name = 'my-bucket'
    project = "bigquery-public-data"
    dataset_id = "samples"
    table_id = "shakespeare"

    destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv")
    dataset_ref = client.dataset(dataset_id, project=project)
    table_ref = dataset_ref.table(table_id)

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        # Location must match that of the source table.
        location="US",
    )  # API request
    extract_job.result()  # Waits for job to complete.

    print(
        "Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri)
    )

    blob = retry_storage_errors(bucket.get_blob)("shakespeare.csv")
    assert blob.exists
    assert blob.size > 0
    to_delete.insert(0, blob)

    # [END bigquery_extract_table]