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


def copy_table_multiple_source(client, to_delete):

    # [START bigquery_copy_table_multiple_source]
    dest_dataset_id = "dest_dataset_{}".format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dest_dataset_id))
    dest_dataset.location = "US"
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    source_dataset_id = "source_dataset_{}".format(_millis())
    source_dataset = bigquery.Dataset(client.dataset(source_dataset_id))
    source_dataset.location = "US"
    source_dataset = client.create_dataset(source_dataset)
    to_delete.append(source_dataset)

    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]

    table_data = {"table1": b"Washington,WA", "table2": b"California,CA"}
    for table_id, data in table_data.items():
        table_ref = source_dataset.table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.schema = schema
        body = six.BytesIO(data)
        client.load_table_from_file(
            body,
            table_ref,
            # Location must match that of the destination dataset.
            location="US",
            job_config=job_config,
        ).result()

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # source_dataset_id = 'my_source_dataset'
    # dest_dataset_id = 'my_destination_dataset'

    table1_ref = client.dataset(source_dataset_id).table("table1")
    table2_ref = client.dataset(source_dataset_id).table("table2")
    dest_table_ref = client.dataset(dest_dataset_id).table("destination_table")

    job = client.copy_table(
        [table1_ref, table2_ref],
        dest_table_ref,
        # Location must match that of the source and destination tables.
        location="US",
    )  # API request
    job.result()  # Waits for job to complete.

    assert job.state == "DONE"
    dest_table = client.get_table(dest_table_ref)  # API request
    assert dest_table.num_rows > 0

    assert dest_table.num_rows == 2

    # [END bigquery_copy_table_multiple_source]