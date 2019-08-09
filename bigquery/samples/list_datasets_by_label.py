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


def list_datasets_by_label(client, to_delete):

    # [START bigquery_list_datasets_by_label]
    dataset_id = "list_datasets_by_label_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.labels = {"color": "green"}
    dataset = client.create_dataset(dataset)  # API request
    to_delete.append(dataset)

    # from google.cloud import bigquery
    # client = bigquery.Client()

    # The following label filter example will find datasets with an
    # arbitrary 'color' label set to 'green'
    label_filter = "labels.color:green"
    datasets = list(client.list_datasets(filter=label_filter))

    if datasets:
        print("Datasets filtered by {}:".format(label_filter))
        for dataset in datasets:  # API request(s)
            print("\t{}".format(dataset.dataset_id))
    else:
        print("No datasets found with this filter.")
    found = set([dataset.dataset_id for dataset in datasets])
    assert dataset_id in found

    # [END bigquery_list_datasets_by_label]