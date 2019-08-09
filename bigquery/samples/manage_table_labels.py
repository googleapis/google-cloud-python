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


def manage_table_labels(client, to_delete):

    # [START bigquery_delete_label_table]
    dataset_id = "label_table_dataset_{}".format(_millis())
    table_id = "label_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)

    # [START bigquery_label_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('my_table')
    # table = client.get_table(table_ref)  # API request

    assert table.labels == {}
    labels = {"color": "green"}
    table.labels = labels

    table = client.update_table(table, ["labels"])  # API request

    assert table.labels == labels
    # [END bigquery_label_table]

    # [START bigquery_get_table_labels]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)  # API Request

    # View table labels
    print("Table ID: {}".format(table_id))
    print("Labels:")
    if table.labels:
        for label, value in table.labels.items():
            print("\t{}: {}".format(label, value))
    else:
        print("\tTable has no labels defined.")
    # [END bigquery_get_table_labels]
    assert table.labels == labels

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('my_table')
    # table = client.get_table(table_ref)  # API request

    # This example table starts with one label
    assert table.labels == {"color": "green"}
    # To delete a label from a table, set its value to None
    table.labels["color"] = None

    table = client.update_table(table, ["labels"])  # API request

    assert table.labels == {}

    # [END bigquery_delete_label_table]