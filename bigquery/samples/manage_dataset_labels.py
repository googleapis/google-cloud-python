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


def manage_dataset_labels(client, to_delete):

    # [START bigquery_delete_label_dataset]
    dataset_id = "label_dataset_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_label_dataset]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    assert dataset.labels == {}
    labels = {"color": "green"}
    dataset.labels = labels

    dataset = client.update_dataset(dataset, ["labels"])  # API request

    assert dataset.labels == labels
    # [END bigquery_label_dataset]

    # [START bigquery_get_dataset_labels]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    dataset = client.get_dataset(dataset_ref)  # API request

    # View dataset labels
    print("Dataset ID: {}".format(dataset_id))
    print("Labels:")
    if dataset.labels:
        for label, value in dataset.labels.items():
            print("\t{}: {}".format(label, value))
    else:
        print("\tDataset has no labels defined.")
    # [END bigquery_get_dataset_labels]
    assert dataset.labels == labels

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    # This example dataset starts with one label
    assert dataset.labels == {"color": "green"}
    # To delete a label from a dataset, set its value to None
    dataset.labels["color"] = None

    dataset = client.update_dataset(dataset, ["labels"])  # API request

    assert dataset.labels == {}

    # [END bigquery_delete_label_dataset]