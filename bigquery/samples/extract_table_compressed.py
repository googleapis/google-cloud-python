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


def extract_table_compressed(client, to_delete):

    # [START bigquery_extract_table_compressed]
    bucket_name = "extract_shakespeare_compress_{}".format(_millis())
    storage_client = storage.Client()
    bucket = retry_storage_errors(storage_client.create_bucket)(bucket_name)
    to_delete.append(bucket)

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # bucket_name = 'my-bucket'

    destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv.gz")
    dataset_ref = client.dataset("samples", project="bigquery-public-data")
    table_ref = dataset_ref.table("shakespeare")
    job_config = bigquery.job.ExtractJobConfig()
    job_config.compression = bigquery.Compression.GZIP

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        # Location must match that of the source table.
        location="US",
        job_config=job_config,
    )  # API request
    extract_job.result()  # Waits for job to complete.

    blob = retry_storage_errors(bucket.get_blob)("shakespeare.csv.gz")
    assert blob.exists
    assert blob.size > 0
    to_delete.insert(0, blob)

    # [END bigquery_extract_table_compressed]