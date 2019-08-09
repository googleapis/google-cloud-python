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


def table_exists(client, to_delete):

    # [START bigquery_table_exists]
    """Determine if a table exists."""

    DATASET_ID = "get_table_dataset_{}".format(_millis())
    TABLE_ID = "get_table_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset.table(TABLE_ID)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table = client.create_table(table)

    assert table_exists(client, table_ref)
    assert not table_exists(client, dataset.table("i_dont_exist"))

    # [END bigquery_table_exists]