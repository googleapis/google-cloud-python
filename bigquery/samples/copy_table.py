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


def copy_table(client, to_delete):

    # [START bigquery_copy_table]
    dataset_id = "copy_table_dataset_{}".format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dataset_id))
    dest_dataset.location = "US"
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    # from google.cloud import bigquery
    # client = bigquery.Client()

    source_dataset = client.dataset("samples", project="bigquery-public-data")
    source_table_ref = source_dataset.table("shakespeare")

    # dataset_id = 'my_dataset'
    dest_table_ref = client.dataset(dataset_id).table("destination_table")

    job = client.copy_table(
        source_table_ref,
        dest_table_ref,
        # Location must match that of the source and destination tables.
        location="US",
    )  # API request

    job.result()  # Waits for job to complete.

    assert job.state == "DONE"
    dest_table = client.get_table(dest_table_ref)  # API request
    assert dest_table.num_rows > 0

    # [END bigquery_copy_table]