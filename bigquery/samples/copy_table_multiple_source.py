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


def copy_table_multiple_source(client, dataset_id, tables_ids):

    # [START bigquery_copy_table_multiple_source]
    from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset where to copy a table.
    # dataset_id = "your-project.your_dataset"

    # TODO(developer): Set tables_ids to the ID of the original tables.
    # tables_ids = ["your-project.your_dataset.your_table_name", ...]

    dataset = client.get_dataset(dataset_id)

    orig_tables = []
    for table_id in tables_ids:
        orig_tables.append(client.get_table(table_id))

    print(orig_tables)

    dest_table = dataset.table("destination_table")

    job = client.copy_table(
        orig_tables,
        dest_table,
        # Location must match that of the source and destination tables.
        location="US",
    )

    job.result()  # Waits for job to complete.

    if job.state == "DONE":
        print("The process completed")
    dest_table = client.get_table(dest_table)
    if dest_table.num_rows == 2:
        print("A copy of {} tables created".format(len(tables_ids)))

    # [END bigquery_copy_table_multiple_source]
