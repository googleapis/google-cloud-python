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


def add_empty_column(client, to_delete):

    # [START bigquery_add_empty_column]
    """Adds an empty column to an existing table."""
    dataset_id = "add_empty_column_dataset_{}".format(_millis())
    table_id = "add_empty_column_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # API request

    original_schema = table.schema
    new_schema = original_schema[:]  # creates a copy of the schema
    new_schema.append(bigquery.SchemaField("phone", "STRING"))

    table.schema = new_schema
    table = client.update_table(table, ["schema"])  # API request

    assert len(table.schema) == len(original_schema) + 1 == len(new_schema)

    # [END bigquery_add_empty_column]