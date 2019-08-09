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


def table_insert_rows(client, to_delete):

    # [START bigquery_table_insert_rows]
    """Insert / fetch table data."""
    dataset_id = "table_insert_rows_dataset_{}".format(_millis())
    table_id = "table_insert_rows_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    dataset.location = "US"
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)

    # TODO(developer): Uncomment the lines below and replace with your values.
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'  # replace with your dataset ID
    # For this sample, the table must already exist and have a defined schema
    # table_id = 'my_table'  # replace with your table ID
    # table_ref = client.dataset(dataset_id).table(table_id)
    # table = client.get_table(table_ref)  # API request

    rows_to_insert = [(u"Phred Phlyntstone", 32), (u"Wylma Phlyntstone", 29)]

    errors = client.insert_rows(table, rows_to_insert)  # API request

    assert errors == []

    # [END bigquery_table_insert_rows]