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


def undelete_table(client, to_delete):

    # [START bigquery_undelete_table]
    dataset_id = "undelete_table_dataset_{}".format(_millis())
    table_id = "undelete_table_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    client.create_table(table)

    # TODO(developer): Uncomment the lines below and replace with your values.
    # import time
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'  # Replace with your dataset ID.
    # table_id = 'my_table'      # Replace with your table ID.

    table_ref = client.dataset(dataset_id).table(table_id)

    # TODO(developer): Choose an appropriate snapshot point as epoch
    # milliseconds. For this example, we choose the current time as we're about
    # to delete the table immediately afterwards.
    snapshot_epoch = int(time.time() * 1000)

    # Due to very short lifecycle of the table, ensure we're not picking a time
    # prior to the table creation due to time drift between backend and client.
    table = client.get_table(table_ref)
    created_epoch = datetime_helpers.to_microseconds(table.created)
    if created_epoch > snapshot_epoch:
        snapshot_epoch = created_epoch

    # [START bigquery_undelete_table]

    # "Accidentally" delete the table.
    client.delete_table(table_ref)  # API request

    # Construct the restore-from table ID using a snapshot decorator.
    snapshot_table_id = "{}@{}".format(table_id, snapshot_epoch)
    source_table_ref = client.dataset(dataset_id).table(snapshot_table_id)

    # Choose a new table ID for the recovered table data.
    recovered_table_id = "{}_recovered".format(table_id)
    dest_table_ref = client.dataset(dataset_id).table(recovered_table_id)

    # Construct and run a copy job.
    job = client.copy_table(
        source_table_ref,
        dest_table_ref,
        # Location must match that of the source and destination tables.
        location="US",
    )  # API request

    job.result()  # Waits for job to complete.

    print(
        "Copied data from deleted table {} to {}".format(table_id, recovered_table_id)
    )

    # [END bigquery_undelete_table]