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


def create_partitioned_table(client, to_delete):

    # [START bigquery_create_table_partitioned]
    dataset_id = "create_table_partitioned_{}".format(_millis())
    dataset_ref = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset_ref)
    to_delete.append(dataset)

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    table_ref = dataset_ref.table("my_partitioned_table")
    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
        bigquery.SchemaField("date", "DATE"),
    ]
    table = bigquery.Table(table_ref, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date",  # name of column to use for partitioning
        expiration_ms=7776000000,
    )  # 90 days

    table = client.create_table(table)

    print(
        "Created table {}, partitioned on column {}".format(
            table.table_id, table.time_partitioning.field
        )
    )

    assert table.time_partitioning.type_ == "DAY"
    assert table.time_partitioning.field == "date"
    assert table.time_partitioning.expiration_ms == 7776000000

    # [END bigquery_create_table_partitioned]